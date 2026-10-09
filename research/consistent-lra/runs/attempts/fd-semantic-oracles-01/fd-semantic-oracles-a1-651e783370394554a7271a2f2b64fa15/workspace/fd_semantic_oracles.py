"""Source-bound software oracles for the existing Frequent Directions baseline.

These deterministic finite matrices are unit tests, not benchmark data.  The
script executes the production baseline plus class definitions extracted from
the frozen author and Liberty source bytes.  It does not make a performance,
paper, or theorem-proof claim.
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
from scipy.linalg import svd as scipy_svd

from baseline_qualify import top_basis
from native_baselines import FrequentDirectionsBaseline


AUTHOR_COMMIT = "d607c4f6467216c470d1e3b93989d44d5fcdec97"
LIBERTY_COMMIT = "691df9edb2ffbc2fdddc2cec3b703a3f1e438d4d"
LIBERTY_BLOB = "4bb3500cbea9c81c21cbeea5cd5db60ac4006d3d"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_class(path: Path, name: str, globals_: dict) -> type:
    """Compile only one class from frozen source, avoiding script side effects."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    nodes = [node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == name]
    if len(nodes) != 1:
        raise ValueError(f"expected exactly one {name} in {path}")
    module = ast.Module(body=nodes, type_ignores=[])
    namespace = dict(globals_)
    exec(compile(module, str(path), "exec"), namespace)
    return namespace[name]


class IndependentLRowReference:
    """Literal l-row compress-before-insert specification, separate from production."""

    def __init__(self, d: int, ell: int):
        self.d = d
        self.ell = ell
        self.rows: list[np.ndarray] = []
        self.shrinks = 0

    def append(self, row: np.ndarray) -> None:
        if len(self.rows) == self.ell:
            packed = np.stack(self.rows)
            _, singular, vh = np.linalg.svd(packed, full_matrices=False)
            delta = singular[-1] ** 2
            shrunk = np.sqrt(np.maximum(singular ** 2 - delta, 0.0))
            compressed = shrunk[:, None] * vh
            self.rows = [compressed[index].copy() for index in range(self.ell - 1)]
            self.shrinks += 1
        self.rows.append(np.asarray(row, dtype=np.float64).copy())

    def sketch(self) -> np.ndarray:
        return np.stack(self.rows) if self.rows else np.zeros((0, self.d))


def covariance(rows: np.ndarray) -> np.ndarray:
    return rows.T @ rows


def boolean_check(checks: list[dict], name: str, passed: bool, **diagnostics) -> None:
    checks.append({"name": name, "passed": bool(passed), **diagnostics})


def run_oracles(root: Path) -> tuple[list[dict], dict]:
    author_path = root / "originals" / "consistent-fd.py"
    liberty_path = root / "originals" / "frequentDirections-liberty-691df9e.py"
    AuthorFD = load_class(author_path, "FrequentDirections", {"np": np, "math": __import__("math")})
    LibertyFD = load_class(
        liberty_path,
        "FrequentDirections",
        {
            "MatrixSketcherBase": object,
            "zeros": np.zeros,
            "sqrt": np.sqrt,
            "dot": np.dot,
            "diag": np.diag,
            "svd": np.linalg.svd,
            "LinAlgError": np.linalg.LinAlgError,
            "scipy_svd": scipy_svd,
        },
    )

    # Fixed, nonrandom, nonsymmetric row stream chosen before execution.
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
    k, ell, d = 1, 3, stream.shape[1]
    production = FrequentDirectionsBaseline(stream, k, ell)
    reference = IndependentLRowReference(d, ell)
    author = AuthorFD(sketch_size=ell, dim=d)
    liberty = LibertyFD(d=d, ell=ell)
    checks: list[dict] = []
    prefixes: list[dict] = []
    production_q_snapshots: list[np.ndarray] = []

    for t, row in enumerate(stream, start=1):
        q, _, _ = production.update(t, float(np.sum(stream[:t] ** 2)))
        reference.append(row)
        author.append(row)
        liberty.append(row)
        b_prod = production.b.copy()
        b_ref = reference.sketch()
        b_author = np.asarray(author.get_sketch()).copy()
        b_liberty = np.asarray(liberty.get()).copy()
        prod_cov = covariance(b_prod)
        ref_cov = covariance(b_ref)
        prefix_cov = covariance(stream[:t])
        error = prefix_cov - prod_cov
        error_eigenvalues = np.linalg.eigvalsh((error + error.T) / 2)
        singular = np.linalg.svd(stream[:t], full_matrices=False, compute_uv=False)
        residual_k = float(np.sum(singular[k:] ** 2))
        theorem_bound = residual_k / (ell - k)
        covariance_scale = max(1.0, float(np.linalg.norm(prefix_cov, ord=2)))
        tolerance = 2e-11 * covariance_scale
        projector = q.T @ q
        q_ref, _ = top_basis(b_ref, min(k, t))
        projector_ref = q_ref.T @ q_ref
        cov_error = float(np.linalg.norm(prod_cov - ref_cov, ord="fro"))
        projector_error = float(np.linalg.norm(projector - projector_ref, ord="fro"))
        boolean_check(checks, f"prefix_{t}_independent_covariance_parity", cov_error <= tolerance,
                      actual=cov_error, tolerance=tolerance)
        boolean_check(checks, f"prefix_{t}_independent_projector_parity", projector_error <= 5e-10,
                      actual=projector_error, tolerance=5e-10)
        boolean_check(checks, f"prefix_{t}_orthonormal_output",
                      float(np.linalg.norm(q @ q.T - np.eye(len(q)), ord="fro")) <= 5e-12,
                      rank=len(q))
        boolean_check(checks, f"prefix_{t}_fd_psd_underestimate",
                      float(error_eigenvalues[0]) >= -tolerance,
                      minimum_eigenvalue=float(error_eigenvalues[0]), tolerance=tolerance)
        boolean_check(checks, f"prefix_{t}_fd_directional_bound",
                      float(error_eigenvalues[-1]) <= theorem_bound + tolerance,
                      maximum_eigenvalue=float(error_eigenvalues[-1]),
                      theorem_bound=theorem_bound, tolerance=tolerance)
        prefixes.append({
            "prefix": t,
            "production_shrinks": production.shrinks,
            "production_reference_covariance_error": cov_error,
            "production_reference_projector_error": projector_error,
            "production_author_covariance_distance": float(np.linalg.norm(prod_cov - covariance(b_author), ord="fro")),
            "production_liberty_visible_covariance_distance": float(np.linalg.norm(prod_cov - covariance(b_liberty), ord="fro")),
            "fd_error_min_eigenvalue": float(error_eigenvalues[0]),
            "fd_error_max_eigenvalue": float(error_eigenvalues[-1]),
            "fd_directional_bound": theorem_bound,
            "production_basis": q.tolist(),
        })
        production_q_snapshots.append(q.copy())

    boolean_check(
        checks,
        "author_and_lrow_are_not_state_parity",
        any(row["production_author_covariance_distance"] > 1e-8 for row in prefixes[ell:]),
        maximum_distance=max(row["production_author_covariance_distance"] for row in prefixes),
    )
    boolean_check(
        checks,
        "liberty_visible_get_and_lrow_are_not_state_parity",
        any(row["production_liberty_visible_covariance_distance"] > 1e-8 for row in prefixes[ell:]),
        maximum_distance=max(row["production_liberty_visible_covariance_distance"] for row in prefixes),
    )

    # Directly expose the frozen author's mutable-return behavior.
    alias_probe = AuthorFD(sketch_size=ell, dim=d)
    live = alias_probe.get_sketch()
    before = live.copy()
    alias_probe.append(stream[0])
    boolean_check(checks, "author_get_sketch_returns_live_mutable_state",
                  live is alias_probe.get_sketch() and not np.array_equal(live, before))

    # Liberty get() exposes only the leading ell rows while pending rows occupy
    # the lower half of its 2ell buffer.
    liberty_probe = LibertyFD(d=d, ell=ell)
    for row in stream[:ell]:
        liberty_probe.append(row)
    visible_before = liberty_probe.get().copy()
    liberty_probe.append(stream[ell])
    visible_after = liberty_probe.get().copy()
    boolean_check(checks, "liberty_get_excludes_pending_lower_buffer_rows",
                  np.array_equal(visible_before, visible_after), pending_rows=1)

    # A returned production basis is a copy and remains unchanged after update.
    copy_probe = FrequentDirectionsBaseline(stream, k, ell)
    q_before, _, _ = copy_probe.update(1, float(np.sum(stream[0] ** 2)))
    frozen_q = q_before.copy()
    copy_probe.update(2, float(np.sum(stream[:2] ** 2)))
    boolean_check(checks, "production_returned_basis_is_snapshot",
                  np.array_equal(q_before, frozen_q))

    diagnostics = {
        "stream": stream.tolist(),
        "k": k,
        "ell": ell,
        "prefixes": prefixes,
        "semantic_conclusion": (
            "production matches an independent l-row compress-before-insert specification; "
            "the frozen author l+1-augmented and Liberty 2ell-buffer/get interfaces are intentionally "
            "distinct and must not be labeled state-parity comparators"
        ),
    }
    return checks, diagnostics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    started = time.perf_counter()
    usage_before = resource.getrusage(resource.RUSAGE_SELF)
    checks, diagnostics = run_oracles(root)
    usage_after = resource.getrusage(resource.RUSAGE_SELF)
    passed = all(item["passed"] for item in checks)
    result = {
        "format": "consistent-lra-fd-source-semantic-oracles-v1",
        "scope": "engineering source and software semantics only; not benchmark or performance evidence",
        "source_pins": {
            "author_commit": AUTHOR_COMMIT,
            "liberty_commit": LIBERTY_COMMIT,
            "liberty_blob": LIBERTY_BLOB,
        },
        "source_hashes": {
            "fd_semantic_oracles.py": sha256(Path(__file__).resolve()),
            "native_baselines.py": sha256(root / "native_baselines.py"),
            "baseline_qualify.py": sha256(root / "baseline_qualify.py"),
            "author_consistent_fd.py": sha256(root / "originals" / "consistent-fd.py"),
            "liberty_frequentDirections.py": sha256(root / "originals" / "frequentDirections-liberty-691df9e.py"),
        },
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "sklearn": sklearn.__version__,
        },
        "checks": checks,
        "check_count": len(checks),
        "failure_count": sum(not item["passed"] for item in checks),
        "all_checks_passed": passed,
        "diagnostics": diagnostics,
        "scientific_gate_advanced": False,
        "performance_claim_eligible": False,
        "theorem_proved": False,
        "usage": {
            "wall_seconds": time.perf_counter() - started,
            "cpu_seconds": usage_after.ru_utime + usage_after.ru_stime - usage_before.ru_utime - usage_before.ru_stime,
            "max_rss_kib": usage_after.ru_maxrss,
        },
        "command": sys.argv,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, allow_nan=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "all_checks_passed": passed,
                      "check_count": len(checks), "usage": result["usage"]}))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
