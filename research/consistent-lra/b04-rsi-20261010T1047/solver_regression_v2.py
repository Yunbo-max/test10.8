import json
import pathlib
import resource
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
import baseline_matrix_study as baseline
import solver
from atomic_npz import atomic_write_json, sha256

wall0 = time.perf_counter()
cpu0 = time.process_time()
rng = np.random.default_rng(741)
records = []
for d, k in ((7, 3), (30, 12), (64, 16)):
    for scale in (0.0, 1e-14, 1e-10, 1e-6, 1.0):
        X = rng.normal(size=(max(k + 3, 2 * k), d)) * scale
        G = X.T @ X
        energy = float(np.sum(X * X))
        values, vectors = np.linalg.eigh(G)
        V = vectors[:, -k:]
        Q, _ = np.linalg.qr(rng.normal(size=(d, k)), mode="reduced")
        opt = max(0.0, float(np.sum(values[:-k])))
        tol = 1e-10 * max(1.0, energy)
        target = 1.01 * opt
        old, old_fb = baseline.boundary_path(Q, V, G, energy, target, tol)
        new, new_fb = solver.boundary_newton(Q, V, G, energy, target, tol)
        records.append({
            "d": d,
            "k": k,
            "scale": scale,
            "target": target,
            "tol": tol,
            "near_zero": bool(target <= tol),
            "fallback_equal": bool(old_fb == new_fb),
            "projector_difference": float(np.linalg.norm(old @ old.T - new @ new.T)),
        })

near_zero = [item for item in records if item["near_zero"]]
nonzero = [item for item in records if not item["near_zero"]]
out = {
    "scope": "primary-B03 conservative near-zero regression; not a scientific benchmark",
    "cases": len(records),
    "near_zero_cases": len(near_zero),
    "near_zero_max_projector_difference": max(item["projector_difference"] for item in near_zero),
    "near_zero_fallback_mismatches": sum(not item["fallback_equal"] for item in near_zero),
    "nonzero_max_projector_difference": max((item["projector_difference"] for item in nonzero), default=0.0),
    "solver_stats": solver.STATS,
    "acceptance": {
        "near_zero_exact_projector_parity": max(item["projector_difference"] for item in near_zero) <= 1e-12,
        "near_zero_fallback_parity": all(item["fallback_equal"] for item in near_zero),
        "all_near_zero_calls_used_legacy": solver.STATS["near_zero_opt_calls"] == solver.STATS["near_zero_legacy_fallbacks"] > 0,
    },
    "source_sha256": sha256(__file__),
    "solver_sha256": sha256(HERE / "solver.py"),
    "baseline_sha256": sha256(baseline.__file__),
    "usage": {
        "wall_seconds": time.perf_counter() - wall0,
        "cpu_seconds": time.process_time() - cpu0,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    },
    "records": records,
}
if not all(out["acceptance"].values()):
    raise AssertionError(out["acceptance"])
out["scope"] = "primary-B03 bracket-refinement regression v2; not a scientific benchmark"
out["parent_regression_sha256"] = sha256(HERE / "SOLVER_REGRESSION.json")
atomic_write_json(HERE / "SOLVER_REGRESSION_V2.json", out)
print(json.dumps({key: out[key] for key in ("cases", "near_zero_cases", "near_zero_max_projector_difference", "acceptance", "usage")}))
