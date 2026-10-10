#!/usr/bin/env python3
"""Finite diagnostics for B11. These checks support algebra only, not proof/novelty."""
from __future__ import annotations

import json
import math
import resource
import time
from pathlib import Path

import numpy as np


def q(theta: float, a: float, b: float, c: float) -> float:
    return a * math.cos(theta) ** 2 + 2.0 * b * math.sin(theta) * math.cos(theta) + c * math.sin(theta) ** 2


def boundary_roots(a: float, b: float, c: float, target: float) -> list[float]:
    m = 0.5 * (a + c)
    p = 0.5 * (a - c)
    rho = math.hypot(p, b)
    if rho == 0.0 or target < m - rho - 1e-12 or target > m + rho + 1e-12:
        return []
    z = max(-1.0, min(1.0, (target - m) / rho))
    phi = math.atan2(b, p)
    alpha = math.acos(z)
    roots = []
    for sign in (-1.0, 1.0):
        for n in range(-3, 4):
            theta = 0.5 * (phi + sign * alpha + 2.0 * math.pi * n)
            if -0.5 * math.pi - 1e-12 <= theta <= 0.5 * math.pi + 1e-12:
                theta = min(0.5 * math.pi, max(-0.5 * math.pi, theta))
                if not any(abs(theta - old) < 1e-10 for old in roots):
                    roots.append(theta)
    return sorted(roots)


def main():
    start_wall = time.perf_counter()
    start_cpu = time.process_time()
    rng = np.random.default_rng(20261010)

    root_error = 0.0
    root_grid_recourse_gap = 0.0
    kkt_stationarity_error = 0.0
    multi_root_cases = 0
    checked = 0
    for _ in range(500):
        M = rng.normal(size=(2, 2))
        H = M.T @ M
        a, b, c = float(H[0, 0]), float(H[0, 1]), float(H[1, 1])
        grid = np.linspace(-0.5 * np.pi, 0.5 * np.pi, 40001)
        vals = a * np.cos(grid) ** 2 + 2 * b * np.sin(grid) * np.cos(grid) + c * np.sin(grid) ** 2
        q0 = a
        qmax = float(vals.max())
        if qmax <= q0 + 1e-9:
            continue
        target = q0 + float(rng.uniform(0.1, 0.9)) * (qmax - q0)
        roots = boundary_roots(a, b, c, target)
        assert roots
        checked += 1
        multi_root_cases += int(len(roots) > 1)
        root_error = max(root_error, max(abs(q(t, a, b, c) - target) for t in roots))
        theta = min(roots, key=lambda t: math.sin(t) ** 2)
        feasible = vals >= target - 1e-12
        grid_best = float(np.min(np.sin(grid[feasible]) ** 2))
        root_grid_recourse_gap = max(root_grid_recourse_gap, abs(math.sin(theta) ** 2 - grid_best))

        dq = (c - a) * math.sin(2 * theta) + 2 * b * math.cos(2 * theta)
        dD = math.sin(2 * theta)
        if abs(dq) > 1e-8:
            lam = dD / dq
            kkt_stationarity_error = max(kkt_stationarity_error, abs(dD - lam * dq))

    assert checked >= 400

    fd_trials = 120
    admissible_tuples = 0
    fd_psd_violation = 0.0
    fd_kyfan_violation = 0.0
    fd_lower_bound_violation = 0.0
    fd_formula_error = 0.0
    for _ in range(fd_trials):
        d, ell, k = 9, 6, 2
        B = rng.normal(size=(ell, d))
        delta = float(rng.uniform(1e-3, 2.0))
        Z = rng.normal(size=(d, ell))
        Q, _ = np.linalg.qr(Z)
        GB = B.T @ B
        # Every exact FD prefix obeys these two sufficient identities:
        # 0 <= G-B^T B <= Delta I and tr(G-B^T B)=ell Delta.
        # A rank-ell projector produces independent admissible tuples without
        # re-testing the already studied streaming FD implementation.
        G = GB + delta * (Q @ Q.T)
        admissible_tuples += 1
        e = np.linalg.eigvalsh(G - GB)
        fd_psd_violation = max(fd_psd_violation, float(max(0.0, -e[0])), float(max(0.0, e[-1] - delta)))
        lamG = np.linalg.eigvalsh(G)[::-1]
        lamB = np.linalg.eigvalsh(GB)[::-1]
        true_kyfan = float(lamG[:k].sum())
        U = float(lamB[:k].sum() + k * delta)
        fd_kyfan_violation = max(fd_kyfan_violation, true_kyfan - U)
        opt = float(np.trace(G) - true_kyfan)
        L = float(np.trace(G) - U)
        fd_lower_bound_violation = max(fd_lower_bound_violation, L - opt)
        tail_formula = float(lamB[k:].sum() + (ell - k) * delta)
        fd_formula_error = max(fd_formula_error, abs(L - tail_formula), abs((np.trace(G) - np.trace(GB)) - ell * delta))

    result = {
        "scope": "finite algebra diagnostics only; not proof, novelty evidence, or method validation",
        "seed": 20261010,
        "c12": {
            "random_psd_planes_checked": checked,
            "cases_with_multiple_principal_interval_roots": multi_root_cases,
            "max_boundary_equation_error": root_error,
            "max_dense_grid_recourse_gap": root_grid_recourse_gap,
            "max_kkt_stationarity_residual": kkt_stationarity_error,
            "conclusion": "all-root enumeration supports only fixed-plane minimum recourse"
        },
        "c20_fd_equivalence": {
            "trials": fd_trials,
            "admissible_fd_identity_tuples_checked": admissible_tuples,
            "max_psd_or_delta_enclosure_violation": fd_psd_violation,
            "max_kyfan_upper_bound_violation": fd_kyfan_violation,
            "max_opt_lower_bound_violation": fd_lower_bound_violation,
            "max_algebraic_formula_error": fd_formula_error,
            "identity": "tr(G)-[KyFan_k(B^T B)+k Delta] = tail_k(B^T B)+(ell-k)Delta"
        },
        "cpu_seconds": time.process_time() - start_cpu,
        "wall_seconds": time.perf_counter() - start_wall,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    }
    tolerances = {
        "root_error": 2e-11,
        "root_grid_recourse_gap": 2e-4,
        "kkt_stationarity": 1e-12,
        "fd_enclosure": 2e-10,
        "fd_formula": 2e-10
    }
    result["tolerances"] = tolerances
    result["passed"] = bool(
        root_error <= tolerances["root_error"]
        and root_grid_recourse_gap <= tolerances["root_grid_recourse_gap"]
        and kkt_stationarity_error <= tolerances["kkt_stationarity"]
        and fd_psd_violation <= tolerances["fd_enclosure"]
        and fd_kyfan_violation <= tolerances["fd_enclosure"]
        and fd_lower_bound_violation <= tolerances["fd_enclosure"]
        and fd_formula_error <= tolerances["fd_formula"]
    )
    Path("B11_MATH_CHECK.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
