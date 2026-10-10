#!/usr/bin/env python3
"""Finite diagnostics for B13 power-work identities; not theorem proof."""

from __future__ import annotations

import json
import math
import os
import resource
import time
from pathlib import Path

import numpy as np


def projector_recourse(x: np.ndarray, y: np.ndarray) -> float:
    x = x / np.linalg.norm(x)
    y = y / np.linalg.norm(y)
    return float(max(0.0, 1.0 - float(x @ y) ** 2))


def exact_error(evals: np.ndarray, coeffs: np.ndarray, m: int) -> float:
    weights = np.square(coeffs) * np.power(evals, 2 * m)
    return float(weights[1:].sum() / weights.sum())


def bound_error(r: float, rho: float, m: int) -> float:
    z = (rho ** (2 * m)) * r
    return float(z / ((1.0 - r) + z))


def counterexample(gamma: float, delta: float, r0: float) -> tuple[np.ndarray, np.ndarray, float]:
    a = (delta - gamma * r0) / (1.0 - gamma)
    g = np.diag([1.0, 0.0, 1.0 - gamma])
    q = np.array([math.sqrt(1.0 - r0), math.sqrt(a), math.sqrt(r0 - a)])
    return g, q, a


def required_work(gamma: float, delta: float, r0: float, eps: float) -> int:
    a = (delta - gamma * r0) / (1.0 - gamma)
    ratio = (r0 - a) * (1.0 - eps) / (eps * (1.0 - r0))
    return max(1, math.ceil(math.log(ratio) / (-2.0 * math.log1p(-gamma))))


def main() -> None:
    started_wall = time.perf_counter()
    started_cpu = time.process_time()
    rng = np.random.default_rng(20261010)

    random_cases = 6000
    max_identity_error = 0.0
    max_direct_error = 0.0
    max_bound_violation = 0.0
    equality_error = 0.0
    zero_lambda2_cases = 0

    for _ in range(random_cases):
        d = int(rng.integers(3, 16))
        evals = np.sort(rng.uniform(0.01, 1.0, size=d))[::-1]
        if evals[0] == evals[1]:
            evals[0] += 1e-6
        coeffs = rng.normal(size=d)
        coeffs /= np.linalg.norm(coeffs)
        if abs(coeffs[0]) < 1e-5:
            coeffs[0] += 0.1
            coeffs /= np.linalg.norm(coeffs)
        m = int(rng.integers(0, 31))
        expected = exact_error(evals, coeffs, m)
        vec = np.power(evals, m) * coeffs
        actual = projector_recourse(np.eye(d)[0], vec)
        r = 1.0 - coeffs[0] ** 2
        upper = bound_error(float(r), float(evals[1] / evals[0]), m)
        max_identity_error = max(max_identity_error, abs(expected - actual))
        max_direct_error = max(max_direct_error, abs(actual - expected))
        max_bound_violation = max(max_bound_violation, actual - upper)

        eq_coeffs = np.zeros(d)
        eq_coeffs[0] = math.sqrt(1.0 - r)
        eq_coeffs[1] = math.sqrt(r)
        eq_actual = exact_error(evals, eq_coeffs, m)
        equality_error = max(equality_error, abs(eq_actual - upper))

    # The logarithmic work formula excludes lambda_2=0.  In that endpoint,
    # every off-top component is killed by the first matvec, but not at m=0.
    for r_zero in [0.1, 0.3, 0.7, 0.95]:
        evals = np.array([1.0, 0.0, 0.0, 0.0])
        coeffs = np.array([math.sqrt(1.0 - r_zero), math.sqrt(r_zero), 0.0, 0.0])
        err0 = exact_error(evals, coeffs, 0)
        err1 = exact_error(evals, coeffs, 1)
        eps_zero = r_zero / 2.0
        if not (err0 > eps_zero and err1 <= eps_zero and err1 == 0.0):
            raise AssertionError((r_zero, err0, err1))
        zero_lambda2_cases += 1

    delta = 0.2
    r0 = 0.6
    eps = 0.05
    gammas = [0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001, 0.0005, 0.0002]
    table = []
    max_tuple_error = 0.0
    max_work_boundary_error = 0.0
    for gamma in gammas:
        g, q, a = counterexample(gamma, delta, r0)
        p = np.array([1.0, 0.0, 0.0])
        recourse = projector_recourse(p, q)
        gain = float(p @ g @ p - q @ g @ q)
        diameter = float(np.linalg.eigvalsh(g)[-1] - np.linalg.eigvalsh(g)[0])
        work = required_work(gamma, delta, r0, eps)
        at_work = projector_recourse(p, np.linalg.matrix_power(g, work) @ q)
        before = projector_recourse(p, np.linalg.matrix_power(g, work - 1) @ q)
        max_tuple_error = max(
            max_tuple_error,
            abs(recourse - r0),
            abs(gain - delta),
            abs(diameter - 1.0),
        )
        max_work_boundary_error = max(max_work_boundary_error, max(0.0, at_work - eps))
        if before <= eps:
            raise AssertionError("analytic work was not minimal")
        table.append(
            {
                "gamma": gamma,
                "a_gamma": a,
                "work": work,
                "gamma_times_work": gamma * work,
                "error_at_work": at_work,
                "error_before_work": before,
            }
        )

    if max_identity_error > 2e-13:
        raise AssertionError(max_identity_error)
    if max_bound_violation > 2e-13:
        raise AssertionError(max_bound_violation)
    if equality_error > 2e-13:
        raise AssertionError(equality_error)
    if max_tuple_error > 2e-13:
        raise AssertionError(max_tuple_error)
    if max_work_boundary_error > 2e-13:
        raise AssertionError(max_work_boundary_error)
    if not all(table[i + 1]["work"] > table[i]["work"] for i in range(len(table) - 1)):
        raise AssertionError("work did not increase as gamma decreased")

    result = {
        "status": "PASS",
        "scope": "finite algebra diagnostics only; not theorem proof, novelty, or native benchmark",
        "seed": 20261010,
        "random_cases": random_cases,
        "max_identity_abs_error": max_identity_error,
        "max_direct_abs_error": max_direct_error,
        "max_bound_violation": max_bound_violation,
        "max_equality_abs_error": equality_error,
        "zero_lambda2_endpoint_cases": zero_lambda2_cases,
        "counterexample": {
            "delta": delta,
            "r0": r0,
            "epsilon": eps,
            "max_fixed_tuple_abs_error": max_tuple_error,
            "max_work_boundary_violation": max_work_boundary_error,
            "table": table,
        },
        "environment": {
            "python": os.sys.version,
            "numpy": np.__version__,
            "numeric_threads": {
                name: os.environ.get(name)
                for name in [
                    "OMP_NUM_THREADS",
                    "OPENBLAS_NUM_THREADS",
                    "MKL_NUM_THREADS",
                    "NUMEXPR_NUM_THREADS",
                ]
            },
        },
        "usage": {
            "process_wall_seconds": time.perf_counter() - started_wall,
            "process_cpu_seconds": time.process_time() - started_cpu,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
    }
    out = Path(__file__).with_name("B13_POWER_WORK_DIAGNOSTIC.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
