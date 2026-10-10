#!/usr/bin/env python3
"""Finite diagnostics for B12.1; not a proof or a benchmark."""
import json
import math
import os
import resource
import time
from pathlib import Path

import numpy as np


def projector(rng, d, k):
    q, _ = np.linalg.qr(rng.normal(size=(d, k)))
    return q @ q.T, q


def main():
    # The launcher also freezes numerical thread counts. Record them here.
    env_keys = [
        "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS",
    ]
    started_wall = time.perf_counter()
    started_cpu = time.process_time()
    rng = np.random.default_rng(20261010)

    max_violation = -math.inf
    min_margin = math.inf
    n_random = 0
    records = []
    for d in (2, 3, 5, 8, 16):
        for k in range(1, min(d, 5)):
            for _ in range(400):
                a = rng.normal(size=(d, d))
                g = a @ a.T
                p, pb = projector(rng, d, k)
                q, qb = projector(rng, d, k)
                eig = np.linalg.eigvalsh(g)
                diameter = float(eig[-1] - eig[0])
                gain = float(np.trace(g @ (p - q)))
                recourse = float(0.5 * np.linalg.norm(p - q, "fro") ** 2)
                rhs = diameter * math.sqrt(k * max(recourse, 0.0))
                violation = abs(gain) - rhs
                max_violation = max(max_violation, violation)
                min_margin = min(min_margin, rhs - abs(gain))
                n_random += 1
                if len(records) < 12:
                    records.append({"d": d, "k": k, "gain": gain,
                                    "diameter": diameter, "recourse": recourse,
                                    "rhs": rhs, "violation": violation})

    # Independently check the principal-angle nuclear/Frobenius identities,
    # including dimensions d<2k where forced zero angles occur.
    principal_angle_cases = 0
    max_nuclear_identity_error = 0.0
    max_recourse_identity_error = 0.0
    for d in (3, 4, 5, 7):
        for k in range(1, d):
            for _ in range(40):
                p, pb = projector(rng, d, k)
                q, qb = projector(rng, d, k)
                cosines = np.clip(np.linalg.svd(pb.T @ qb, compute_uv=False), 0, 1)
                sines = np.sqrt(np.maximum(0.0, 1.0 - cosines ** 2))
                diff_singular = np.linalg.svd(p - q, compute_uv=False)
                nuclear = float(diff_singular.sum())
                recourse = float(0.5 * np.linalg.norm(p - q, "fro") ** 2)
                max_nuclear_identity_error = max(
                    max_nuclear_identity_error, abs(nuclear - 2 * float(sines.sum())))
                max_recourse_identity_error = max(
                    max_recourse_identity_error, abs(recourse - float((sines ** 2).sum())))
                principal_angle_cases += 1

    # Exact edge cases: Delta=0 must use the trivial branch, and D=0 contributes
    # zero under feasibility.  These are theorem-domain checks, not performance.
    g_edge = np.diag([1.0, 0.0])
    q_edge = np.diag([1.0, 0.0])
    p_edge = np.diag([0.0, 1.0])
    t_edge = 1.0
    loss_q_edge = float(np.trace((np.eye(2) - q_edge) @ g_edge))
    loss_p_edge = float(np.trace((np.eye(2) - p_edge) @ g_edge))
    delta_zero = max(loss_q_edge - t_edge, 0.0)
    negative_gain_with_delta_zero = float(np.trace(g_edge @ (p_edge - q_edge)))
    g_flat = 3.0 * np.eye(4)
    q_flat, _ = projector(rng, 4, 2)
    flat_loss = float(np.trace((np.eye(4) - q_flat) @ g_flat))
    flat_delta = max(flat_loss - flat_loss, 0.0)

    # Exact sharpness family for k=1,d=2.  If q has angle alpha+phi and p alpha,
    # alpha=(pi/2-phi)/2 maximizes the Rayleigh-quotient difference.
    tight = []
    dval = 7.0
    g = np.diag([dval, 0.0])
    for phi in np.linspace(1e-5, math.pi / 2 - 1e-5, 200):
        alpha = (math.pi / 2 - phi) / 2
        vp = np.array([math.cos(alpha), math.sin(alpha)])
        vq = np.array([math.cos(alpha + phi), math.sin(alpha + phi)])
        p = np.outer(vp, vp)
        q = np.outer(vq, vq)
        gain = float(np.trace(g @ (p - q)))
        recourse = float(0.5 * np.linalg.norm(p - q, "fro") ** 2)
        rhs = dval * math.sqrt(recourse)
        tight.append(abs(gain - rhs))

    result = {
        "scope": "finite algebra diagnostic only; not proof, novelty, or endpoint benchmark",
        "seed": 20261010,
        "random_cases": n_random,
        "max_numerical_violation": max_violation,
        "minimum_nonnegative_margin": min_margin,
        "tightness_cases": len(tight),
        "max_tightness_abs_error": max(tight),
        "principal_angle_identity_cases": principal_angle_cases,
        "max_nuclear_identity_error": max_nuclear_identity_error,
        "max_recourse_identity_error": max_recourse_identity_error,
        "edge_delta_zero": delta_zero,
        "edge_negative_gain_with_delta_zero": negative_gain_with_delta_zero,
        "edge_delta_zero_branch_pass": delta_zero == 0.0 and negative_gain_with_delta_zero < 0.0,
        "flat_spectrum_diameter": float(np.ptp(np.linalg.eigvalsh(g_flat))),
        "flat_spectrum_delta": flat_delta,
        "flat_spectrum_zero_contribution_pass": flat_delta == 0.0,
        "inequality_pass": max_violation <= 5e-10,
        "tightness_pass": max(tight) <= 5e-12,
        "principal_angle_identities_pass": (
            max_nuclear_identity_error <= 2e-12 and
            max_recourse_identity_error <= 2e-12
        ),
        "sample_records": records,
        "wall_seconds": time.perf_counter() - started_wall,
        "process_cpu_seconds": time.process_time() - started_cpu,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "pid": os.getpid(),
        "numeric_thread_env": {k: os.environ.get(k) for k in env_keys},
        "numpy_version": np.__version__,
    }
    out = Path("B12_BOUNDARY_CHECK.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not all((result["inequality_pass"], result["tightness_pass"],
                result["principal_angle_identities_pass"],
                result["edge_delta_zero_branch_pass"],
                result["flat_spectrum_zero_contribution_pass"])):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

