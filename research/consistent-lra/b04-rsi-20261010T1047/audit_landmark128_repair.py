import json
import os
import pathlib
import resource
import time
import zipfile

for variable in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[variable] = "1"

import numpy as np

from atomic_npz import atomic_write_json, sha256, validate_npz

HERE = pathlib.Path(__file__).resolve().parent
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024 ** 3, 2 * 1024 ** 3))
wall0 = time.perf_counter()
cpu0 = time.process_time()
raw_path = HERE / "LANDMARK128_RAW_V2.npz"
pilot = json.loads((HERE / "LANDMARK128_REPORT_V2.json").read_text())
validation = validate_npz(raw_path, pilot["raw_validation"]["inventory"].keys())
assert validation["sha256"] == pilot["raw_validation"]["sha256"]

with np.load(raw_path, allow_pickle=False) as z:
    a = z["a"]
    opt = z["opt"]
    energy = np.sum(a * a, axis=1).cumsum()
    checkpoints = z["checkpoints"]
    records = []
    for eta in (0.01, 0.1):
        for method in ("old", "new", "full"):
            stem = f"{method}_eta{eta:g}"
            losses = z[f"{stem}_loss"]
            increments = z[f"{stem}_increment"]
            violations = int(np.sum(losses > (1 + eta) * opt + 1.01e-10 * np.maximum(1.0, energy)))
            loss_errors, opt_errors, orth_errors, increment_errors = [], [], [], []
            for index, prefix in enumerate(checkpoints):
                Q = z[f"{stem}_basis"][index]
                previous = z[f"{stem}_previous_basis"][index]
                residual = a[:prefix] - (a[:prefix] @ Q) @ Q.T
                direct_loss = float(np.sum(residual * residual))
                singular = np.linalg.svd(a[:prefix], compute_uv=False)
                direct_opt = float(np.sum(singular[25:] ** 2))
                loss_errors.append(abs(direct_loss - losses[prefix - 1]))
                opt_errors.append(abs(direct_opt - opt[prefix - 1]))
                orth_errors.append(float(np.linalg.norm(Q.T @ Q - np.eye(25))))
                direct_increment = float(np.sum((Q @ Q.T - previous @ previous.T) ** 2))
                increment_errors.append(abs(direct_increment - increments[prefix - 1]))
            source = next(item for item in pilot["records"] if item["method"] == method and item["eta"] == eta)
            recourse_error = abs(float(np.sum(increments[25:], dtype=np.longdouble)) - source["post_rank_growth_recourse"])
            records.append({
                "method": method,
                "eta": eta,
                "certificate_violations": violations,
                "checkpoint_records": len(checkpoints),
                "max_explicit_residual_loss_error": max(loss_errors),
                "max_reference_opt_error": max(opt_errors),
                "max_orthogonality_error": max(orth_errors),
                "max_dense_projector_increment_error": max(increment_errors),
                "recourse_sum_error": recourse_error,
            })
        old = f"old_eta{eta:g}"
        new = f"new_eta{eta:g}"
        old_loss = z[f"{old}_loss"]
        new_loss = z[f"{new}_loss"]
        projector_differences = [
            float(np.linalg.norm(Q @ Q.T - V @ V.T))
            for Q, V in zip(z[f"{old}_basis"], z[f"{new}_basis"])
        ]
        parity = {
            "eta": eta,
            "update_difference": int(np.count_nonzero(z[f"{old}_updated"] != z[f"{new}_updated"])),
            "query_difference": int(np.count_nonzero(z[f"{old}_queried"] != z[f"{new}_queried"])),
            "max_loss_difference": float(np.max(np.abs(old_loss - new_loss))),
            "max_relative_loss_difference_to_energy": float(np.max(np.abs(old_loss - new_loss) / np.maximum(1.0, energy))),
            "max_checkpoint_projector_difference": max(projector_differences),
            "total_recourse_difference": abs(float(np.sum(z[f"{old}_increment"])) - float(np.sum(z[f"{new}_increment"]))),
        }
        records.append({"parity": parity})

parity_records = [item["parity"] for item in records if "parity" in item]
arm_records = [item for item in records if "method" in item]
acceptance = {
    "npz_crc_and_self_read": bool(validation["zip_crc_pass"] and validation["np_load_pass"]),
    "allprefix_certificate": all(item["certificate_violations"] == 0 for item in arm_records),
    "checkpoint_residual": max(item["max_explicit_residual_loss_error"] for item in arm_records) <= 1e-7,
    "checkpoint_opt": max(item["max_reference_opt_error"] for item in arm_records) <= 1e-7,
    "orthogonality": max(item["max_orthogonality_error"] for item in arm_records) <= 1e-10,
    "projector_increment": max(item["max_dense_projector_increment_error"] for item in arm_records) <= 1e-8,
    "old_new_decisions": all(item["update_difference"] == 0 and item["query_difference"] == 0 for item in parity_records),
    "old_new_loss": all(item["max_relative_loss_difference_to_energy"] <= 1e-9 for item in parity_records),
    "old_new_projector": all(item["max_checkpoint_projector_difference"] <= 1e-8 for item in parity_records),
    "old_new_recourse": all(item["total_recourse_difference"] <= 1e-8 for item in parity_records),
    "near_zero_branch_accounted": pilot["solver_stats"]["near_zero_opt_calls"] == pilot["solver_stats"]["near_zero_legacy_fallbacks"] > 0,
    "historical_failure_preserved": sha256(HERE / "historical" / "LANDMARK_PILOT_RAW_CORRUPT.npz") == "2a690c48f50617ade1f59c6689f6aa5d119dc47675b7e0a16c1448dadce24f5b",
}
out = {
    "scope": "independent command arithmetic audit of primary-B03 repaired first128 Landmark development pilot",
    "input_sha256": validation["sha256"],
    "records": records,
    "acceptance": acceptance,
    "all_acceptance_pass": all(acceptance.values()),
    "full5000_comparison_run": False,
    "usage": {
        "wall_seconds": time.perf_counter() - wall0,
        "cpu_seconds": time.process_time() - cpu0,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    },
}
if not out["all_acceptance_pass"]:
    raise AssertionError(acceptance)
atomic_write_json(HERE / "LANDMARK128_AUDIT_V2.json", out)
print(json.dumps({"all_acceptance_pass": True, "acceptance": acceptance, "usage": out["usage"]}))
