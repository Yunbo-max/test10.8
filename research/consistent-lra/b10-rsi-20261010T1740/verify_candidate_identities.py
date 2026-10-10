#!/usr/bin/env python3
"""Finite numerical checks for B10 algebra; not a theorem or scientific confirmation."""

import json
import math
import os
import resource
import time
from pathlib import Path

import numpy as np


def top_basis(g, k):
    vals, vecs = np.linalg.eigh(g)
    idx = np.argsort(vals)[::-1][:k]
    return vals[idx], vecs[:, idx]


def projector(v):
    return v @ v.T


def cost(g, v):
    return float(np.trace(g) - np.trace(v.T @ g @ v))


def main():
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    rng = np.random.default_rng(20261010)
    t0 = time.perf_counter()
    c0 = time.process_time()

    maxima = {
        "D1_rank_one_residual_abs": 0.0,
        "D2_rr_optimality_violation": 0.0,
        "D3_energy_formula_abs": 0.0,
        "D3_recourse_formula_abs": 0.0,
        "D4_overlap_monotonicity_violation": 0.0,
        "D4_energy_monotonicity_violation": 0.0,
        "C20_safe_bound_violation": 0.0,
    }
    checks = 0
    wrong_cluster_examples = 0

    for rep in range(200):
        d = int(rng.integers(6, 13))
        k = int(rng.integers(1, min(4, d - 1)))
        x = rng.normal(size=(d + 4, d))
        g0 = x.T @ x
        _, v = top_basis(g0, k)
        a = rng.normal(size=d)
        g = g0 + np.outer(a, a)

        # D1, under its explicit exact-invariance assumption.
        r_direct = (np.eye(d) - projector(v)) @ g @ v
        r_rank1 = (np.eye(d) - projector(v)) @ a[:, None] @ (a[None, :] @ v)
        maxima["D1_rank_one_residual_abs"] = max(
            maxima["D1_rank_one_residual_abs"], float(np.linalg.norm(r_direct - r_rank1))
        )

        # D2: Ritz basis must beat random k-subspaces inside the same S.
        q_extra, _ = np.linalg.qr(rng.normal(size=(d, min(3, d - k))))
        s, _ = np.linalg.qr(np.column_stack([v, q_extra]))
        m = s.shape[1]
        _, y = top_basis(s.T @ g @ s, k)
        w = s @ y
        rr_energy = float(np.trace(w.T @ g @ w))
        for _ in range(10):
            z, _ = np.linalg.qr(rng.normal(size=(m, k)))
            random_energy = float(np.trace(z.T @ s.T @ g @ s @ z))
            maxima["D2_rr_optimality_violation"] = max(
                maxima["D2_rr_optimality_violation"], random_energy - rr_energy
            )

        # D3 formulas.
        vv = v[:, 0]
        u = rng.normal(size=d)
        u = u - v @ (v.T @ u)
        u /= np.linalg.norm(u)
        theta = float(rng.uniform(-1.2, 1.2))
        ww = vv * math.cos(theta) + u * math.sin(theta)
        h = np.array([[vv @ g @ vv, vv @ g @ u], [u @ g @ vv, u @ g @ u]])
        cs = np.array([math.cos(theta), math.sin(theta)])
        maxima["D3_energy_formula_abs"] = max(
            maxima["D3_energy_formula_abs"], abs(float(ww @ g @ ww - cs @ h @ cs))
        )
        v_new = v.copy()
        v_new[:, 0] = ww
        recourse = 0.5 * np.linalg.norm(projector(v_new) - projector(v), ord="fro") ** 2
        maxima["D3_recourse_formula_abs"] = max(
            maxima["D3_recourse_formula_abs"], abs(float(recourse - math.sin(theta) ** 2))
        )

        # D4 monotonicity on a deterministic grid. Ties have probability zero here.
        p0 = projector(v)
        overlaps = []
        energies = []
        for mu in np.geomspace(1e-8, 1e4, 60):
            _, vm = top_basis(g + mu * p0, k)
            pm = projector(vm)
            overlaps.append(float(np.trace(pm @ p0)))
            energies.append(float(np.trace(pm @ g)))
        maxima["D4_overlap_monotonicity_violation"] = max(
            maxima["D4_overlap_monotonicity_violation"],
            max([overlaps[i] - overlaps[i + 1] for i in range(len(overlaps) - 1)] + [0.0]),
        )
        maxima["D4_energy_monotonicity_violation"] = max(
            maxima["D4_energy_monotonicity_violation"],
            max([energies[i + 1] - energies[i] for i in range(len(energies) - 1)] + [0.0]),
        )

        # C20 direction: true upper bounds on top eigenvalues yield L <= OPT.
        vals = np.linalg.eigvalsh(g)[::-1]
        eps = rng.uniform(0, 0.05, size=k)
        upper = vals[:k] + eps
        lower_opt = float(np.trace(g) - upper.sum())
        true_opt = float(np.trace(g) - vals[:k].sum())
        maxima["C20_safe_bound_violation"] = max(
            maxima["C20_safe_bound_violation"], lower_opt - true_opt
        )

        # A wrong invariant cluster can have exactly zero residual: residual alone is unsafe.
        all_vals, all_vecs = np.linalg.eigh(g)
        wrong = all_vecs[:, :k]
        residual = (np.eye(d) - projector(wrong)) @ g @ wrong
        if np.linalg.norm(residual) < 1e-9 and cost(g, wrong) > true_opt + 1e-8:
            wrong_cluster_examples += 1
        checks += 1

    tolerances = {
        "D1_rank_one_residual_abs": 5e-10,
        "D2_rr_optimality_violation": 5e-10,
        "D3_energy_formula_abs": 5e-10,
        "D3_recourse_formula_abs": 5e-10,
        "D4_overlap_monotonicity_violation": 5e-9,
        "D4_energy_monotonicity_violation": 5e-9,
        "C20_safe_bound_violation": 5e-10,
    }
    passed = all(maxima[k] <= tolerances[k] for k in maxima) and wrong_cluster_examples == checks
    out = {
        "schema": "b10-candidate-identity-check-v1",
        "seed": 20261010,
        "random_cases": checks,
        "maxima": maxima,
        "tolerances": tolerances,
        "wrong_invariant_cluster_zero_residual_examples": wrong_cluster_examples,
        "passed": passed,
        "wall_seconds": time.perf_counter() - t0,
        "cpu_seconds": time.process_time() - c0,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "scope_note": "Finite checks only; does not prove the statements or establish novelty.",
    }
    path = Path("B10_IDENTITY_CHECK.json")
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    print(json.dumps(out, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

