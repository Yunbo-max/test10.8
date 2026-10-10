"""Independent arithmetic verification for the B06 numerical-metric audit."""
import hashlib
import json
import os
import pathlib
import resource
import time

for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"

import numpy as np
import solver

HERE = pathlib.Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def qr_residual(q, v):
    q = np.linalg.qr(q, mode="reduced")[0]
    v = np.linalg.qr(v, mode="reduced")[0]
    a = v - q @ (q.T @ v)
    b = q - v @ (v.T @ q)
    return float(np.hypot(np.linalg.norm(a), np.linalg.norm(b))), q, v


def old_metric(q, v):
    return float(np.sqrt(max(0.0, q.shape[1] + v.shape[1] - 2.0 * np.square(q.T @ v).sum())))


def dense_metric(q, v):
    return float(np.linalg.norm(q @ q.T - v @ v.T, ord="fro"))


def main():
    wall0, cpu0 = time.perf_counter(), time.process_time()
    resource.setrlimit(resource.RLIMIT_AS, (2 * 1024 ** 3, 2 * 1024 ** 3))
    result = json.loads((HERE / "STABLE_METRIC_AUDIT.json").read_text())
    with np.load(HERE / "LANDMARK128_RAW_V3.npz", allow_pickle=False) as z:
        a = z["a"].copy()
        parent_rows = []
        parent_pairs = []
        for eta in ("0.01", "0.1"):
            for checkpoint, q, v in zip(z["checkpoints"], z[f"old_eta{eta}_basis"], z[f"new_eta{eta}_basis"]):
                stable, qq, vv = qr_residual(q, v)
                parent_rows.append({"eta": eta, "checkpoint": int(checkpoint), "stable": stable,
                                    "old": old_metric(q, v)})
                parent_pairs.append((stable, qq, vv, eta, int(checkpoint)))
    parent_max = max(parent_pairs, key=lambda x: x[0])
    parent_dense = dense_metric(parent_max[1], parent_max[2])

    selected = result["dense_controls"]["same_input"]["selected_state_index"]
    with np.load(HERE / "SAME_INPUT_CAPTURE.npz", allow_pickle=False) as z:
        prefix = int(z["prefix"][selected])
        q, v = z["q"][selected], z["v"][selected]
        e, target, tol = float(z["e"][selected]), float(z["target"][selected]), float(z["tol"][selected])
    g = a[:prefix].T @ a[:prefix]
    old_out, _ = solver.boundary_legacy(q, v, g, e, target, tol)
    new_out, _ = solver.boundary_newton(q, v, g, e, target, tol)
    same_stable, qq, vv = qr_residual(old_out, new_out)
    same_dense = dense_metric(qq, vv)

    expected_parent = result["aggregate"]["parent"]["stable_qr_symmetric_residual_max"]
    expected_same = result["same_input"]["summary"]["stable_qr_symmetric_residual_max"]
    checks = {
        "result_hash_matches_runner_output": digest(HERE / "STABLE_METRIC_AUDIT.json") == "0f821fb29924a5c8d3850f0a5ab2b9b38554f4355731399140e74c0172cc08a4",
        "parent_max_matches": abs(parent_max[0] - expected_parent) <= 5e-15,
        "parent_dense_matches_residual": abs(parent_dense - parent_max[0]) <= 5e-12,
        "same_input_selected_is_global_max": abs(same_stable - expected_same) <= 5e-15,
        "same_input_dense_matches_residual": abs(same_dense - same_stable) <= 5e-12,
        "old_metric_has_false_positive_parent_pairs": any(r["old"] > 1e-8 and r["stable"] <= 1e-8 for r in parent_rows),
        "old_metric_has_false_negative_parent_pairs": any(r["old"] <= 1e-8 and r["stable"] > 1e-8 for r in parent_rows),
    }
    out = {
        "scope": "independent arithmetic verifier; selected same-input state and every saved B04 checkpoint pair",
        "checks": checks,
        "pass": all(checks.values()),
        "parent": {
            "pairs": len(parent_rows),
            "max": parent_max[0],
            "max_eta": parent_max[3],
            "max_checkpoint": parent_max[4],
            "dense": parent_dense,
            "old_false_positive_pairs": sum(r["old"] > 1e-8 and r["stable"] <= 1e-8 for r in parent_rows),
            "old_false_negative_pairs": sum(r["old"] <= 1e-8 and r["stable"] > 1e-8 for r in parent_rows),
        },
        "same_input_selected": {"state_index": selected, "prefix": prefix, "stable": same_stable, "dense": same_dense},
        "source_hashes": {name: digest(HERE / name) for name in (
            "verify_stable_metric.py", "STABLE_METRIC_AUDIT.json", "solver.py",
            "SAME_INPUT_CAPTURE.npz", "LANDMARK128_RAW_V3.npz")},
        "usage": {"wall_seconds": time.perf_counter() - wall0, "cpu_seconds": time.process_time() - cpu0,
                  "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
    }
    path = HERE / "INDEPENDENT_VERIFY.json"
    path.write_text(json.dumps(out, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"pass": out["pass"], "checks": checks, "parent": out["parent"],
                      "same_input_selected": out["same_input_selected"], "usage": out["usage"],
                      "sha256": digest(path)}, allow_nan=False))
    if not out["pass"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
