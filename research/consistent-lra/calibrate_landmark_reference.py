"""Bounded Landmark exact-reference calibration; no baseline comparison.

This task loads only the author-selected first 5,000 rows, removes columns that
are identically zero on that prefix (an isometric restriction for residuals),
and times exact symmetric-eigenvalue reference calculations at frozen prefixes.
It does not run Algorithm 4, FD, a candidate method, or a scientific comparison.
"""

import argparse
import hashlib
import json
import math
import resource
import time
from pathlib import Path

import numpy as np
from scipy.linalg import eigh


EXPECTED = {
    "bytes": 34964305,
    "git_blob": "4c63060bbefcb38e0c705cea1f883d2fb7121f2c",
    "sha256": "29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b",
    "rows": 71952,
    "columns": 2704,
    "entries": 1151232,
    "prefix_rows": 5000,
    "prefix_entries": 80000,
    "prefix_nonempty_columns": 259,
}
PREFIXES = [25, 50, 100, 150, 250, 500, 1000, 2000, 3000, 4000, 5000]
SVD_CHECK_PREFIXES = {150, 1000, 5000}
CANCELLATION_TOLERANCE_SCALE = 1e-10


def source_identity(path: Path):
    size = path.stat().st_size
    git_hash = hashlib.sha1()
    git_hash.update(b"blob " + str(size).encode("ascii") + b"\0")
    sha256 = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            git_hash.update(chunk)
            sha256.update(chunk)
    return size, git_hash.hexdigest(), sha256.hexdigest()


def load_first_5000(path: Path):
    coordinates = []
    dimensions = None
    entries = 0
    with path.open("rt", encoding="utf-8") as handle:
        if handle.readline().rstrip("\n") != "%%MatrixMarket matrix coordinate real general":
            raise ValueError("unexpected MatrixMarket banner")
        for line in handle:
            stripped = line.strip()
            if not stripped or stripped.startswith("%"):
                continue
            fields = stripped.split()
            if dimensions is None:
                dimensions = tuple(map(int, fields))
                if dimensions != (EXPECTED["rows"], EXPECTED["columns"], EXPECTED["entries"]):
                    raise ValueError("unexpected Landmark dimensions")
                continue
            if len(fields) != 3:
                raise ValueError("invalid coordinate")
            row, column = int(fields[0]), int(fields[1])
            value = float(fields[2])
            if not math.isfinite(value):
                raise ValueError("non-finite coordinate")
            entries += 1
            if row <= EXPECTED["prefix_rows"]:
                coordinates.append((row - 1, column - 1, value))
    if entries != EXPECTED["entries"] or len(coordinates) != EXPECTED["prefix_entries"]:
        raise ValueError("Landmark entry counts differ from frozen evidence")
    active = sorted({column for _, column, _ in coordinates})
    if len(active) != EXPECTED["prefix_nonempty_columns"]:
        raise ValueError("Landmark active-column count differs")
    remap = {column: index for index, column in enumerate(active)}
    matrix = np.zeros((EXPECTED["prefix_rows"], len(active)), dtype=np.float64)
    for row, column, value in coordinates:
        matrix[row, remap[column]] += value
    if not np.isfinite(matrix).all():
        raise ValueError("non-finite dense prefix")
    return matrix, active


def top_k_opt_from_gram(gram, energy, k):
    copy_start = time.perf_counter()
    eig_input = gram.copy()
    copy_seconds = time.perf_counter() - copy_start
    start = time.perf_counter()
    eigenvalues = eigh(
        eig_input,
        subset_by_index=[eig_input.shape[0] - k, eig_input.shape[0] - 1],
        eigvals_only=True,
        driver="evr",
        check_finite=False,
    )
    solver_seconds = time.perf_counter() - start
    top_k_eigenvalue_sum = float(np.sum(eigenvalues))
    raw_residual = float(energy - top_k_eigenvalue_sum)
    cancellation_tolerance = CANCELLATION_TOLERANCE_SCALE * max(1.0, energy)
    if raw_residual < -cancellation_tolerance:
        raise ValueError("materially negative Gram residual")
    reported_residual = max(0.0, raw_residual)
    return {
        "reported_residual": reported_residual,
        "raw_residual": raw_residual,
        "top_k_eigenvalue_sum": top_k_eigenvalue_sum,
        "cancellation_tolerance": cancellation_tolerance,
        "copy_seconds": copy_seconds,
        "solver_seconds": solver_seconds,
        "reference_seconds": copy_seconds + solver_seconds,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--landmark", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--k", type=int, default=25)
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()
    if args.k != 25 or args.repeats != 3:
        raise ValueError("this calibration freezes k=25 and repeats=3")

    wall_start = time.perf_counter()
    usage_start = resource.getrusage(resource.RUSAGE_SELF)
    source = Path(args.landmark)
    byte_count, git_blob, sha256 = source_identity(source)
    if (byte_count, git_blob, sha256) != (
        EXPECTED["bytes"], EXPECTED["git_blob"], EXPECTED["sha256"]
    ):
        raise ValueError("Landmark source identity mismatch")

    load_start = time.perf_counter()
    matrix, active_columns = load_first_5000(source)
    load_seconds = time.perf_counter() - load_start
    gram = np.zeros((matrix.shape[1], matrix.shape[1]), dtype=np.float64)
    energy = 0.0
    observations = []
    prefix_set = set(PREFIXES)
    gram_update_seconds = 0.0
    for prefix, row in enumerate(matrix, start=1):
        update_start = time.perf_counter()
        gram += np.outer(row, row)
        energy += float(np.dot(row, row))
        gram_update_seconds += time.perf_counter() - update_start
        if prefix not in prefix_set:
            continue
        references = []
        for _ in range(args.repeats):
            references.append(top_k_opt_from_gram(gram, energy, args.k))
        reported_opts = [item["reported_residual"] for item in references]
        raw_opts = [item["raw_residual"] for item in references]
        if max(raw_opts) - min(raw_opts) > 1e-8 * max(1.0, energy):
            raise ValueError("repeated eigen references disagree")
        svd = None
        if prefix in SVD_CHECK_PREFIXES:
            svd_start = time.perf_counter()
            singular = np.linalg.svd(matrix[:prefix], full_matrices=False, compute_uv=False)
            svd_seconds = time.perf_counter() - svd_start
            svd_opt = float(np.sum(singular[args.k:] ** 2))
            raw_absolute = abs(svd_opt - raw_opts[0])
            reported_absolute = abs(svd_opt - reported_opts[0])
            tolerance = 1e-9 * max(1.0, energy)
            if raw_absolute > tolerance or reported_absolute > tolerance:
                raise ValueError("Gram eigenvalue and direct SVD references disagree")
            svd = {
                "optimal": svd_opt,
                "seconds": svd_seconds,
                "raw_gram_absolute_difference": raw_absolute,
                "reported_gram_absolute_difference": reported_absolute,
                "tolerance": tolerance,
                "near_zero_opt_relative_accuracy_qualified": False,
            }
        observations.append({
            "prefix": prefix,
            "energy": energy,
            "optimal": reported_opts[0],
            "raw_gram_residual": raw_opts[0],
            "top_k_eigenvalue_sum": references[0]["top_k_eigenvalue_sum"],
            "cancellation_tolerance": references[0]["cancellation_tolerance"],
            "reference_seconds": [item["reference_seconds"] for item in references],
            "reference_seconds_median": float(np.median([item["reference_seconds"] for item in references])),
            "gram_copy_seconds": [item["copy_seconds"] for item in references],
            "eigh_solver_seconds": [item["solver_seconds"] for item in references],
            "direct_svd_check": svd,
        })
    usage_end = resource.getrusage(resource.RUSAGE_SELF)
    result = {
        "format": "landmark-reference-calibration-v1",
        "scope": "engineering_exact_reference_cost_and_identity_only",
        "source": {
            "upstream": "samsonzhou/consistent-LRA@d607c4f6467216c470d1e3b93989d44d5fcdec97",
            "git_blob": git_blob,
            "sha256": sha256,
            "bytes": byte_count,
            "prefix_rows": len(matrix),
            "released_columns": EXPECTED["columns"],
            "represented_columns": len(active_columns),
            "represented_columns_one_based": [column + 1 for column in active_columns],
            "restriction": "drop only columns identically zero on first5000; residual geometry preserved",
        },
        "configuration": {
            "k": args.k,
            "prefixes": PREFIXES,
            "repeats": args.repeats,
            "threads_required_by_harness_before_process_start": 1,
            "thread_count_observed_by_script": None,
            "reference": "scipy.linalg.eigh symmetric Gram top-k eigenvalues",
            "direct_svd_checks": sorted(SVD_CHECK_PREFIXES),
            "cancellation_tolerance_scale": CANCELLATION_TOLERANCE_SCALE,
            "near_zero_opt_ratio_denominator_qualified": False,
        },
        "observations": observations,
        "usage": {
            "load_seconds": load_seconds,
            "gram_update_seconds": gram_update_seconds,
            "wall_seconds": time.perf_counter() - wall_start,
            "process_cpu_seconds": (
                usage_end.ru_utime + usage_end.ru_stime
                - usage_start.ru_utime - usage_start.ru_stime
            ),
            "max_rss_kib": usage_end.ru_maxrss,
            "timing_scope": "after imports and before JSON serialization/write",
            "max_rss_scope": "process high-water RSS, not incremental allocation",
        },
        "full_5000_prefix_queue_admitted": False,
        "baseline_comparison_performed": False,
        "scientific_experiment": False,
        "gate_advanced": False,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "usage": result["usage"]}, allow_nan=False))


if __name__ == "__main__":
    main()
