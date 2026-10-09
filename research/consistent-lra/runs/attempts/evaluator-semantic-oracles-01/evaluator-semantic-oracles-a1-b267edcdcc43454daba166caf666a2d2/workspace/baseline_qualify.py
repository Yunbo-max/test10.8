"""Native Rice/Skin evaluator qualification under REPAIR_CONTRACT_v1.

No new research method. Does not advance scientific gates.
Run only through an admitted RSI harness task. Selected prefixes are native
identity checks, not a performance comparison or confirmation sample.
"""
import argparse
import hashlib
import io
import json
import platform
import resource
import sys
import time
from pathlib import Path

import numpy as np
import scipy
import sklearn
from sklearn import preprocessing

EXPECTED = {
    "rice": ("745655b79f4ca46a3a65a0a8653bd792fa6f7c31", 3810, 7),
    "skin": ("fc58dda2eaf5b1f0d2d8c7924a298cd7d14ba17d", 245057, 3),
}
PREFIXES = (1, 2, 3, 7, 25, 100, 1000, 3000)


def blob_digest(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def load_native(dataset, source):
    raw = Path(source).read_bytes()
    expected, count, dimensions = EXPECTED[dataset]
    if blob_digest(raw) != expected:
        raise ValueError("original native blob mismatch")
    text = raw.decode("utf-8")
    if dataset == "rice":
        lines = text.splitlines()
        marker = next(i for i, line in enumerate(lines) if line.strip().upper() == "@DATA")
        records = [line.split(",") for line in lines[marker + 1:] if line.strip() and not line.startswith("%")]
        labels = [row[-1].strip() for row in records]
        matrix = np.asarray([row[:-1] for row in records], dtype=np.float64)
        if set(labels) != {"Cammeo", "Osmancik"}:
            raise ValueError("unexpected Rice labels")
    else:
        values = np.loadtxt(io.StringIO(text), dtype=np.int64)
        if values.shape != (count, dimensions + 1):
            raise ValueError("unexpected Skin dimensions")
        labels = values[:, -1].tolist()
        if set(labels) != {1, 2}:
            raise ValueError("unexpected Skin labels")
        matrix = values[:, :dimensions].astype(np.float64)
    if matrix.shape != (count, dimensions) or not np.isfinite(matrix).all():
        raise ValueError("unexpected native dimensions or nonfinite data")
    # Author-compatible fixed stream transformation: fit before prefixing.
    # This is explicitly offline preprocessing, not raw-online information.
    transformed = preprocessing.scale(matrix, axis=0)
    if not np.isfinite(transformed).all():
        raise ValueError("nonfinite transformed stream")
    labels_raw = json.dumps(labels, separators=(",", ":")).encode()
    return transformed[:3000], {
        "dataset": dataset, "source_blob": expected,
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "source_bytes": len(raw), "released_shape": list(matrix.shape),
        "sample_ids": [f"{dataset}:row:{i}" for i in range(1, 3001)],
        "denominator": 3000, "preprocessing": "full_released_data_sklearn_scale_ddof0_before_prefix",
        "mean": matrix.mean(axis=0).tolist(), "scale": matrix.std(axis=0).tolist(),
        "transformed_sha256": hashlib.sha256(transformed[:3000].astype("<f8").tobytes()).hexdigest(),
        "labels_sha256": hashlib.sha256(labels_raw).hexdigest(),
        "first3000_label_counts": {str(v): labels[:3000].count(v) for v in sorted(set(labels))},
    }


def top_basis(matrix, k):
    _, singular, vh = np.linalg.svd(matrix, full_matrices=False)
    return vh[:min(k, matrix.shape[0], matrix.shape[1])].copy(), singular


def score_direct(matrix, basis):
    projected = (matrix @ basis.T) @ basis
    return float(np.sum((matrix - projected) ** 2))


def score_trace(matrix, basis):
    return float(np.sum(matrix ** 2) - np.sum((matrix @ basis.T) ** 2))


def recourse_overlap(q, previous):
    return float(len(q) + len(previous) - 2 * np.sum((q @ previous.T) ** 2))


def recourse_direct(q, previous):
    return float(np.sum((q.T @ q - previous.T @ previous) ** 2))


def qualify(matrix, k):
    """Compare independent direct definitions on prescribed released prefixes."""
    diagnostics = []
    previous = np.empty((0, matrix.shape[1]))
    for t in PREFIXES:
        a = matrix[:t]
        q, singular = top_basis(a, k)
        energy = float(np.sum(a ** 2))
        optimal_tail = float(np.sum(singular[k:] ** 2))
        direct_loss = score_direct(a, q)
        trace_loss = score_trace(a, q)
        overlap = recourse_overlap(q, previous)
        direct_recourse = recourse_direct(q, previous)
        orthogonality_error = float(np.linalg.norm(q @ q.T - np.eye(len(q)), ord="fro"))
        checks = []
        for factor in (1e-12, 1e-10, 1e-8):
            tol = factor * max(1.0, energy)
            # Recourse is dimensionless; do not borrow data-energy tolerance.
            recourse_tol = factor * max(1, len(q) + len(previous))
            checks.append({
                "relative_tolerance": factor, "loss_tolerance": tol,
                "recourse_tolerance": recourse_tol,
                "trace_matches_direct": abs(trace_loss - direct_loss) <= tol,
                "opt_tail_matches_direct": abs(optimal_tail - direct_loss) <= tol,
                "recourse_matches_direct": abs(overlap - direct_recourse) <= recourse_tol,
                "ratio": direct_loss / optimal_tail if optimal_tail > tol else None,
                "ratio_missing_count": int(optimal_tail <= tol),
                "positive_loss_near_zero_count": int(optimal_tail <= tol and direct_loss > tol),
                "near_zero_opt": optimal_tail <= tol,
                "positive_loss_near_zero_opt": optimal_tail <= tol and direct_loss > tol,
            })
        diagnostics.append({
            "prefix": t, "rank": len(q), "energy": energy,
            "fresh_svd_opt_tail": optimal_tail, "direct_loss": direct_loss,
            "additive_excess": direct_loss - optimal_tail,
            "normalized_additive_excess": (direct_loss - optimal_tail) / energy if energy > 0 else None,
            "trace_loss_unclamped": trace_loss,
            "recourse_to_previous_selected_prefix_overlap_unclamped": overlap,
            "recourse_to_previous_selected_prefix_direct": direct_recourse,
            "previous_selected_prefix": diagnostics[-1]["prefix"] if diagnostics else 0,
            "transition_kind": "initialization_from_zero" if not diagnostics else "selected_prefix_transition_not_total_streaming_recourse",
            "orthogonality_error": orthogonality_error,
            "spectrum": singular.tolist(), "basis": q.tolist(),
            "tolerance_checks": checks,
        })
        previous = q.copy()
    # These selected-prefix transitions are NOT total streaming recourse.
    passed = all(
        row["orthogonality_error"] <= 1e-10 * max(1, row["rank"])
        and all(c["trace_matches_direct"] and c["opt_tail_matches_direct"] and c["recourse_matches_direct"]
                for c in row["tolerance_checks"] if c["relative_tolerance"] == 1e-10)
        for row in diagnostics
    )
    return {"k": k, "checks_passed": passed, "primary_tolerance": 1e-10,
            "sensitivity_counts": {str(f): {
                "missing_ratio_count": sum(c["ratio_missing_count"] for row in diagnostics for c in row["tolerance_checks"] if c["relative_tolerance"] == f),
                "positive_loss_near_zero_opt_count": sum(c["positive_loss_near_zero_count"] for row in diagnostics for c in row["tolerance_checks"] if c["relative_tolerance"] == f),
                "identity_failure_count": sum(not(c["trace_matches_direct"] and c["opt_tail_matches_direct"] and c["recourse_matches_direct"]) for row in diagnostics for c in row["tolerance_checks"] if c["relative_tolerance"] == f)
            } for f in (1e-12, 1e-10, 1e-8)}, "diagnostics": diagnostics,
            "scope": "selected native prefix numerical identity qualification, not total recourse/performance"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", choices=sorted(EXPECTED), required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    start = time.perf_counter()
    before = resource.getrusage(resource.RUSAGE_SELF)
    matrix, native = load_native(args.dataset, args.source)
    checks = [qualify(matrix, k) for k in ([1] if args.dataset == "rice" else [1, 2])]
    after = resource.getrusage(resource.RUSAGE_SELF)
    output = {
        "format": "consistent-lra-native-qualification-v1", "command": sys.argv,
        "native": native, "checks": checks, "scientific_gate_advanced": False,
        "performance_claim_eligible": False,
        "environment": {"python": platform.python_version(), "numpy": np.__version__,
                        "scipy": scipy.__version__, "sklearn": sklearn.__version__},
        "usage": {"wall_seconds": time.perf_counter() - start,
                  "cpu_seconds": after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime,
                  "max_rss_kib": after.ru_maxrss},
    }
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, ensure_ascii=False, allow_nan=False, indent=2) + "\n")
    print(json.dumps({"output": str(path), "all_identity_checks_passed": all(x["checks_passed"] for x in checks),
                      "usage": output["usage"]}))
    return 0 if all(x["checks_passed"] for x in checks) else 2


if __name__ == "__main__":
    raise SystemExit(main())
