"""Numerical/resource calibration of cached-Gram exact queries at native1024."""
import os
for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"

import hashlib
import json
import resource
import time
from pathlib import Path

import numpy as np
from scipy.io import mmread
from scipy.linalg import eigh

from atomic_npz import atomic_savez, atomic_write_json

HERE = Path(__file__).resolve().parent
SOURCE_SHA256 = "29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b"
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))


def main():
    wall0 = time.perf_counter()
    cpu0 = time.process_time()
    source = HERE / "landmark.mtx"
    assert hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA256
    load0 = time.perf_counter()
    matrix = mmread(source).tocsr()
    assert matrix.shape == (71952, 2704) and matrix.nnz == 1151232
    A = matrix[:1024].toarray()
    del matrix
    load_wall = time.perf_counter() - load0
    n, d = A.shape
    k = 25
    energy = np.cumsum(np.sum(A * A, axis=1))
    G = np.zeros((n, n), dtype=np.float64)
    gram_cpu = 0.0
    for i, x in enumerate(A):
        c = time.process_time()
        g = A[: i + 1] @ x
        G[i, : i + 1] = g
        G[: i + 1, i] = g
        gram_cpu += time.process_time() - c
    checkpoints = np.asarray([512, 640, 768, 896, 1024])
    gram_opt, svd_opt, gram_query_cpu, svd_query_cpu = [], [], [], []
    for t in checkpoints:
        c = time.process_time()
        vals = eigh(
            G[:t, :t],
            eigvals_only=True,
            subset_by_index=(t - k, t - 1),
            driver="evr",
            check_finite=False,
        )
        gram_query_cpu.append(time.process_time() - c)
        gram_opt.append(max(0.0, float(energy[t - 1] - np.sum(np.maximum(vals, 0.0)))))
        c = time.process_time()
        singular = np.linalg.svd(A[:t], compute_uv=False)
        svd_query_cpu.append(time.process_time() - c)
        svd_opt.append(float(singular[k:] @ singular[k:]))
    gram_opt = np.asarray(gram_opt)
    svd_opt = np.asarray(svd_opt)
    normalized_error = np.abs(gram_opt - svd_opt) / np.maximum(1.0, energy[checkpoints - 1])
    raw = {
        "checkpoints": checkpoints,
        "energy": energy[checkpoints - 1],
        "gram_opt": gram_opt,
        "svd_opt": svd_opt,
        "normalized_error": normalized_error,
        "gram_query_cpu": np.asarray(gram_query_cpu),
        "svd_query_cpu": np.asarray(svd_query_cpu),
    }
    receipt = atomic_savez(HERE / "B09_GRAM1024_CALIBRATION_RAW.npz", raw, list(raw))
    passed = bool(np.all(normalized_error <= 1e-10))
    out = {
        "study": "B09-native1024-cached-gram-resource-calibration",
        "rows": n,
        "dimension": d,
        "rank": k,
        "checkpoints": checkpoints.tolist(),
        "gram_build_cpu_seconds": gram_cpu,
        "gram_query_cpu_seconds": gram_query_cpu,
        "svd_query_cpu_seconds": svd_query_cpu,
        "max_normalized_opt_error": float(np.max(normalized_error)),
        "numerical_pass": passed,
        "input_load_wall_seconds_excluded": load_wall,
        "usage": {
            "wall_seconds": time.perf_counter() - wall0,
            "cpu_seconds": time.process_time() - cpu0,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
        "raw_artifact": receipt,
        "development_only": True,
        "continuous_policy_executed": False,
        "whole_landmark5000": False,
        "new_method": False,
    }
    atomic_write_json(HERE / "B09_GRAM1024_CALIBRATION.json", out)
    print(json.dumps({key: value for key, value in out.items() if key != "raw_artifact"}, allow_nan=False))
    assert passed, "cached-Gram calibration mismatch; evidence retained"


if __name__ == "__main__":
    main()
