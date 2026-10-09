"""Source-bound oracles for the frozen author's ell+1 FD diagnostic.

Engineering software evidence only.  The fixed matrix is a unit-test fixture,
not a native benchmark or performance comparison.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import platform
import resource
import sys
import time
from pathlib import Path

import numpy as np
import scipy
import sklearn

from native_baselines import AuthorAugmentedFDDiagnostic


AUTHOR_COMMIT = "d607c4f6467216c470d1e3b93989d44d5fcdec97"
AUTHOR_BLOB = "294438ac128556f01a2c3d920bdb4f1225dd819f"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_blob_digest(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def load_author(path: Path) -> type:
    raw = path.read_bytes()
    actual_blob = git_blob_digest(raw)
    if actual_blob != AUTHOR_BLOB:
        raise ValueError(f"frozen author blob mismatch: {actual_blob}")
    tree = ast.parse(raw.decode("utf-8"), filename=str(path))
    nodes = [node for node in tree.body if isinstance(node, ast.ClassDef)
             and node.name == "FrequentDirections"]
    if len(nodes) != 1:
        raise ValueError("expected exactly one frozen author FrequentDirections class")
    namespace = {"np": np}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), namespace)
    return namespace["FrequentDirections"]


def projector(q: np.ndarray) -> np.ndarray:
    return q.T @ q


def independent_top_projector(matrix: np.ndarray, rank: int) -> np.ndarray:
    covariance = matrix.T @ matrix
    eigenvalues, eigenvectors = np.linalg.eigh((covariance + covariance.T) / 2)
    order = np.argsort(eigenvalues)[::-1][:rank]
    return eigenvectors[:, order] @ eigenvectors[:, order].T


def check(rows: list[dict], name: str, passed: bool, **diagnostics) -> None:
    rows.append({"name": name, "passed": bool(passed), **diagnostics})


def run(root: Path) -> tuple[list[dict], list[dict]]:
    author_path = root / "originals" / "consistent-fd.py"
    AuthorFD = load_author(author_path)
    stream = np.array([
        [4.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 3.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 2.0, 0.0, 0.0],
        [1.0, 1.0, 0.0, 1.0, 0.0],
        [0.0, 2.0, 1.0, 0.0, 1.0],
        [2.0, 0.0, 1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0, 2.0, 1.0],
        [1.0, 0.0, 2.0, 0.0, 2.0],
    ], dtype=np.float64)
    k, ell = 1, 3
    production = AuthorAugmentedFDDiagnostic(stream, k, ell)
    author = AuthorFD(sketch_size=ell, dim=stream.shape[1])
    checks: list[dict] = []
    prefixes: list[dict] = []
    first_basis = first_snapshot = None
    author_shrinks = 0

    for t, row in enumerate(stream, start=1):
        q, updated, warmup = production.update(t, float(np.sum(stream[:t] ** 2)))
        will_shrink = all(np.any(author.B[index]) for index in range(ell))
        author.append(row)
        author_shrinks += int(will_shrink)
        expected_b = np.asarray(author.get_sketch()).copy()
        state_error = float(np.linalg.norm(production.b - expected_b, ord="fro"))
        covariance_error = float(np.linalg.norm(
            production.b.T @ production.b - expected_b.T @ expected_b, ord="fro"))
        expected_projector = independent_top_projector(expected_b, min(k, t))
        projector_error = float(np.linalg.norm(projector(q) - expected_projector, ord="fro"))
        scale = max(1.0, float(np.linalg.norm(expected_b, ord="fro")))
        check(checks, f"prefix_{t}_exact_state", state_error <= 2e-12 * scale,
              actual=state_error, tolerance=2e-12 * scale)
        check(checks, f"prefix_{t}_covariance", covariance_error <= 5e-11 * scale ** 2,
              actual=covariance_error, tolerance=5e-11 * scale ** 2)
        check(checks, f"prefix_{t}_projector", projector_error <= 5e-10,
              actual=projector_error, tolerance=5e-10)
        orthogonality = float(np.linalg.norm(q @ q.T - np.eye(len(q)), ord="fro"))
        check(checks, f"prefix_{t}_orthonormal", orthogonality <= 5e-12,
              actual=orthogonality, tolerance=5e-12)
        check(checks, f"prefix_{t}_flags", updated and warmup == (t <= k),
              updated=updated, warmup=warmup)
        check(checks, f"prefix_{t}_shrink_count", production.shrinks == author_shrinks,
              production_shrinks=production.shrinks, author_condition_count=author_shrinks)
        prefixes.append({"prefix": t, "state_error": state_error,
                         "covariance_error": covariance_error,
                         "projector_error": projector_error,
                         "production_shrinks": production.shrinks,
                         "basis": q.tolist()})
        if first_basis is None:
            first_basis = q
            first_snapshot = q.copy()
    check(checks, "returned_basis_is_snapshot", np.array_equal(first_basis, first_snapshot))

    # Exercise the shared varying-rank convention separately at k=2.  The
    # independent reference is an eigendecomposition of the frozen-author
    # sketch covariance, not the production SVD helper.
    rank_two_prod = AuthorAugmentedFDDiagnostic(stream, 2, ell)
    rank_two_author = AuthorFD(sketch_size=ell, dim=stream.shape[1])
    for t, row in enumerate(stream[:4], start=1):
        q, _, warmup = rank_two_prod.update(t, float(np.sum(stream[:t] ** 2)))
        rank_two_author.append(row)
        expected_rank = min(2, t)
        rank_projector = independent_top_projector(
            np.asarray(rank_two_author.get_sketch()), expected_rank)
        error = float(np.linalg.norm(projector(q) - rank_projector, ord="fro"))
        check(checks, f"rank_two_prefix_{t}_rank_convention",
              len(q) == expected_rank and warmup == (t <= 2),
              actual_rank=len(q), expected_rank=expected_rank, warmup=warmup)
        check(checks, f"rank_two_prefix_{t}_independent_projector", error <= 5e-10,
              actual=error, tolerance=5e-10)

    # The frozen source treats an actually inserted zero row as still empty.
    zero_stream = np.array([[0.0] * 5, [1.0, 2.0, 0.0, 0.0, 0.0]], dtype=np.float64)
    zero_prod = AuthorAugmentedFDDiagnostic(zero_stream, 1, ell)
    zero_author = AuthorFD(sketch_size=ell, dim=5)
    for t, row in enumerate(zero_stream, start=1):
        zero_prod.update(t, float(np.sum(zero_stream[:t] ** 2)))
        zero_author.append(row)
    zero_error = float(np.linalg.norm(zero_prod.b - zero_author.get_sketch(), ord="fro"))
    check(checks, "zero_row_source_behavior_preserved", zero_error == 0.0,
          state_error=zero_error,
          interpretation="second row occupies the same first slot because the zero row remains source-empty")
    return checks, prefixes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    started = time.perf_counter()
    before = resource.getrusage(resource.RUSAGE_SELF)
    checks, prefixes = run(root)
    after = resource.getrusage(resource.RUSAGE_SELF)
    passed = all(item["passed"] for item in checks)
    result = {
        "format": "consistent-lra-author-fd-diagnostic-semantic-oracles-v1",
        "scope": "engineering source/software semantics only; no native performance evidence",
        "source_pin": {"author_commit": AUTHOR_COMMIT, "author_blob": AUTHOR_BLOB},
        "source_hashes": {
            "author_fd_semantic_oracles.py": sha256(Path(__file__).resolve()),
            "native_baselines.py": sha256(root / "native_baselines.py"),
            "baseline_qualify.py": sha256(root / "baseline_qualify.py"),
            "originals/consistent-fd.py": sha256(root / "originals" / "consistent-fd.py"),
        },
        "environment": {"python": platform.python_version(), "numpy": np.__version__,
                        "scipy": scipy.__version__, "sklearn": sklearn.__version__},
        "checks": checks,
        "check_count": len(checks),
        "failure_count": sum(not item["passed"] for item in checks),
        "all_checks_passed": passed,
        "prefixes": prefixes,
        "usage": {"wall_seconds": time.perf_counter() - started,
                  "cpu_seconds": after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime,
                  "max_rss_kib": after.ru_maxrss},
        "command": sys.argv,
        "scientific_gate_advanced": False,
        "performance_claim_eligible": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, allow_nan=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "all_checks_passed": passed,
                      "check_count": len(checks), "usage": result["usage"]}))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
