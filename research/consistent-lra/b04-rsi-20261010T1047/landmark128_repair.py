import hashlib
import json
import os
import pathlib
import resource
import sys
import time

for variable in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[variable] = "1"

import numpy as np
from scipy.io import mmread

HERE = pathlib.Path(__file__).resolve().parent
import baseline_matrix_study as baseline
import solver
from atomic_npz import atomic_savez, atomic_write_json, sha256

resource.setrlimit(resource.RLIMIT_AS, (2 * 1024 ** 3, 2 * 1024 ** 3))
wall0 = time.perf_counter()
cpu0 = time.process_time()
matrix = mmread(HERE / "landmark.mtx").tocsr()
stored_entries = matrix.nnz
numerical_nonzeros = int(np.count_nonzero(matrix.data))
assert matrix.shape == (71952, 2704)
assert stored_entries == 1151232
assert numerical_nonzeros == 1146848
a = matrix[:128].toarray()
del matrix
n, d = a.shape
k = 25
checkpoints = np.unique(np.r_[np.linspace(k + 1, n, 16, dtype=int), n])
checkpoint_set = set(checkpoints)
opts = []
energy = []
for i in range(n):
    singular = np.linalg.svd(a[: i + 1], compute_uv=False)
    opts.append(float(np.sum(singular[min(k, i + 1):] ** 2)))
    energy.append(float(np.sum(a[: i + 1] ** 2)))
opts = np.asarray(opts)
energy = np.asarray(energy)


class SVDArm(baseline.Arm):
    def optimum(self, t):
        self.queries += 1
        _u, singular, vh = np.linalg.svd(a[:t], full_matrices=False)
        V = vh[: min(k, t)].T.copy()
        opt = float(np.sum(singular[min(k, t):] ** 2))
        self.cached = max(self.cached, opt - 1e-10 * max(1.0, self.E), 0.0)
        return V, opt


records = []
raw = {"a": a, "opt": opts, "energy_reference": energy, "checkpoints": checkpoints}
for eta in (0.01, 0.1):
    for method in ("old", "new", "full"):
        if method == "old":
            baseline.boundary_path = solver.boundary_legacy
        elif method == "new":
            baseline.boundary_path = solver.boundary_newton
        arm = SVDArm(d, k, eta, "certified_full" if method == "full" else "boundary", k)
        previous = None
        loss, increment, updated, queried, basis, previous_basis = [], [], [], [], [], []
        update_wall = 0.0
        update_cpu = 0.0
        for i, row in enumerate(a):
            query0 = arm.queries
            w = time.perf_counter()
            c = time.process_time()
            Q, changed = arm.step(row, i + 1)
            update_wall += time.perf_counter() - w
            update_cpu += time.process_time() - c
            current_loss = max(0.0, arm.E - float(np.sum(Q * (arm.G @ Q))))
            movement = 0.0 if previous is None or not changed else baseline.overlap_increment(Q, previous)
            loss.append(current_loss)
            increment.append(movement)
            updated.append(changed)
            queried.append(arm.queries - query0)
            if i + 1 in checkpoint_set:
                basis.append(Q.copy())
                previous_basis.append(previous.copy())
            previous = Q.copy()
        stem = f"{method}_eta{eta:g}"
        for key, values in (
            ("loss", loss), ("increment", increment), ("updated", updated), ("queried", queried),
            ("basis", basis), ("previous_basis", previous_basis),
        ):
            raw[f"{stem}_{key}"] = np.asarray(values)
        loss_array = np.asarray(loss)
        near_zero = opts <= 1e-10 * np.maximum(1.0, energy)
        records.append({
            "method": method,
            "eta": eta,
            "update_wall_seconds": update_wall,
            "update_cpu_seconds": update_cpu,
            "queries": arm.queries,
            "refreshes": arm.refreshes,
            "fallbacks": arm.fallbacks,
            "total_recourse": float(np.sum(increment)),
            "post_rank_growth_recourse": float(np.sum(increment[k:])),
            "certificate_violations": int(np.sum(loss_array > (1 + eta) * opts + 1.01e-10 * np.maximum(1.0, energy))),
            "near_zero_opt_count": int(np.sum(near_zero)),
            "max_raw_loss_near_zero_opt": float(np.max(loss_array[near_zero])),
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        })

required_keys = list(raw)
validation = atomic_savez(HERE / "LANDMARK128_RAW_V2.npz", raw, required_keys)
corrupt = HERE / "historical" / "LANDMARK_PILOT_RAW_CORRUPT.npz"
report = {
    "scope": "native first128 raw rows,k25,d2704,exact prefix SVD; primary-B03 repair development, not author5000 reproduction",
    "shape": [71952, 2704],
    "stored_entries": stored_entries,
    "numeric_nonzeros": numerical_nonzeros,
    "input_mtx_sha256": sha256(HERE / "landmark.mtx"),
    "native_subset_sha256": hashlib.sha256(a.astype("<f8").tobytes()).hexdigest(),
    "historical_corrupt_npz_sha256": sha256(corrupt),
    "historical_corrupt_npz_size": corrupt.stat().st_size,
    "records": records,
    "solver_stats": solver.STATS,
    "raw_validation": validation,
    "source_sha256": sha256(__file__),
    "solver_sha256": sha256(HERE / "solver.py"),
    "baseline_sha256": sha256(baseline.__file__),
    "usage": {
        "wall_seconds": time.perf_counter() - wall0,
        "cpu_seconds": time.process_time() - cpu0,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    },
}
assert report["input_mtx_sha256"] == "29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b"
assert report["historical_corrupt_npz_sha256"] == "2a690c48f50617ade1f59c6689f6aa5d119dc47675b7e0a16c1448dadce24f5b"
assert all(record["certificate_violations"] == 0 for record in records)
assert solver.STATS["near_zero_opt_calls"] == solver.STATS["near_zero_legacy_fallbacks"] > 0
atomic_write_json(HERE / "LANDMARK128_REPORT_V2.json", report)
print(json.dumps({"records": len(records), "raw_sha256": validation["sha256"], "solver_stats": solver.STATS, "usage": report["usage"]}))
