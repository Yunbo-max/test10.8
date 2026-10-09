"""Independent semantic oracles for the repaired Consistent-LRA evaluator.

Software qualification only: analytic matrices and explicit projectors test
metric implementations. These cases are not benchmark data, performance
evidence, an official scorer, or a scientific experiment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import resource
import sys
import time
from pathlib import Path

import numpy as np

import baseline_qualify as production


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def direct_loss(a: np.ndarray, q: np.ndarray) -> float:
    p = q.T @ q
    return float(np.sum((a @ (np.eye(a.shape[1]) - p)) ** 2))


def direct_recourse(q: np.ndarray, previous: np.ndarray) -> float:
    return float(np.sum((q.T @ q - previous.T @ previous) ** 2))


def record(checks: list[dict], name: str, actual: float, expected: float,
           tolerance: float = 1e-12) -> None:
    error = abs(actual - expected)
    checks.append({
        "name": name,
        "actual": actual,
        "expected": expected,
        "absolute_error": error,
        "tolerance": tolerance,
        "passed": bool(np.isfinite(actual) and error <= tolerance),
    })


def analytic_checks() -> list[dict]:
    checks: list[dict] = []
    e1 = np.array([[1.0, 0.0, 0.0]])
    e2 = np.array([[0.0, 1.0, 0.0]])
    e12 = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    diagonal = np.diag([3.0, 2.0, 1.0])

    # Projection onto e1 retains energy 9 and leaves squared residual 4+1.
    record(checks, "analytic_direct_loss", production.score_direct(diagonal, e1), 5.0)
    record(checks, "analytic_trace_loss", production.score_trace(diagonal, e1), 5.0)
    record(checks, "independent_direct_loss", direct_loss(diagonal, e1), 5.0)

    q_svd, singular = production.top_basis(diagonal, 1)
    record(checks, "fresh_svd_tail", float(np.sum(singular[1:] ** 2)), 5.0)
    record(checks, "fresh_svd_projector_loss", direct_loss(diagonal, q_svd), 5.0)
    record(checks, "fresh_svd_projector_identity",
           float(np.sum((q_svd.T @ q_svd - e1.T @ e1) ** 2)), 0.0)

    # Orthogonal one-dimensional projectors have squared Frobenius distance 2.
    record(checks, "orthogonal_overlap_recourse", production.recourse_overlap(e1, e2), 2.0)
    record(checks, "orthogonal_direct_recourse", production.recourse_direct(e1, e2), 2.0)

    # Adding e2 to span(e1) changes the projector by e2 e2^T, norm squared 1.
    record(checks, "rank_change_overlap_recourse", production.recourse_overlap(e12, e1), 1.0)
    record(checks, "rank_change_direct_recourse", production.recourse_direct(e12, e1), 1.0)

    rotated = np.array([[2 ** -0.5, 2 ** -0.5, 0.0]])
    record(checks, "rotated_overlap_recourse", production.recourse_overlap(rotated, e1), 1.0)
    record(checks, "rotated_direct_recourse", direct_recourse(rotated, e1), 1.0)

    empty = np.empty((0, 3), dtype=np.float64)
    record(checks, "initialization_from_zero_separate", production.recourse_overlap(e1, empty), 1.0)
    return checks


def algebraic_identity_checks() -> list[dict]:
    checks: list[dict] = []
    rng = np.random.default_rng(20261009)
    for case, (rows, d, rank, previous_rank) in enumerate(
            [(2, 4, 1, 0), (5, 4, 2, 1), (8, 7, 3, 2), (11, 7, 5, 3)]):
        a = rng.normal(size=(rows, d))
        q_full, _ = np.linalg.qr(rng.normal(size=(d, d)))
        p_full, _ = np.linalg.qr(rng.normal(size=(d, d)))
        q = q_full[:, :rank].T.copy()
        previous = p_full[:, :previous_rank].T.copy()
        energy = float(np.sum(a ** 2))
        tolerance = 1e-12 * max(1.0, energy)
        record(checks, f"case_{case}_loss_direct_vs_explicit",
               production.score_direct(a, q), direct_loss(a, q), tolerance)
        record(checks, f"case_{case}_loss_trace_vs_explicit",
               production.score_trace(a, q), direct_loss(a, q), tolerance)
        recourse_tolerance = 1e-12 * max(1, rank + previous_rank)
        record(checks, f"case_{case}_recourse_overlap_vs_explicit",
               production.recourse_overlap(q, previous), direct_recourse(q, previous),
               recourse_tolerance)
    return checks


def run(output: Path) -> int:
    started = time.perf_counter()
    usage_before = resource.getrusage(resource.RUSAGE_SELF)
    checks = analytic_checks() + algebraic_identity_checks()
    usage_after = resource.getrusage(resource.RUSAGE_SELF)
    passed = all(check["passed"] for check in checks)
    root = Path(__file__).resolve().parent
    result = {
        "format": "consistent-lra-evaluator-semantic-oracles-v1",
        "scope": "software metric semantics only; no native benchmark or performance claim",
        "official_scorer": False,
        "scientific_gate_advanced": False,
        "performance_claim_eligible": False,
        "command": sys.argv,
        "fixed_seed_for_software_oracle_only": 20261009,
        "source_hashes": {
            "evaluator_semantic_oracles.py": sha256(Path(__file__).resolve()),
            "baseline_qualify.py": sha256(root / "baseline_qualify.py"),
            "REPAIR_CONTRACT_v1.md": sha256(root / "REPAIR_CONTRACT_v1.md"),
        },
        "environment": {"python": platform.python_version(), "numpy": np.__version__},
        "checks": checks,
        "check_count": len(checks),
        "failure_count": sum(not check["passed"] for check in checks),
        "all_checks_passed": passed,
        "usage": {
            "wall_seconds": time.perf_counter() - started,
            "cpu_seconds": usage_after.ru_utime + usage_after.ru_stime
                           - usage_before.ru_utime - usage_before.ru_stime,
            "max_rss_kib": usage_after.ru_maxrss,
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, allow_nan=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "all_checks_passed": passed,
                      "check_count": len(checks), "usage": result["usage"]}))
    return 0 if passed else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    return run(args.output)


if __name__ == "__main__":
    raise SystemExit(main())
