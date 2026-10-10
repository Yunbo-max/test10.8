"""Audit B09 cached-Gram policy runs and native1024 calibration."""
import os
for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"

import hashlib
import json
import resource
import time
from pathlib import Path

import numpy as np

from atomic_npz import atomic_write_json, validate_npz

HERE = Path(__file__).resolve().parent
REFERENCE_SHA256 = "b8c4f5278fa58c96c485d6f547acdd927a5cd5153528219ebc1fd6ada4744fa5"
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))


def median_cpu(prefix, policy, eta_text):
    values = []
    for repeat in range(3):
        path = HERE / f"{prefix}_{policy}_eta{eta_text.replace('.', 'p')}_r{repeat}.json"
        values.append(json.loads(path.read_text())["algorithm_cpu_seconds"])
    return float(np.median(values)), values


def main():
    wall0 = time.perf_counter()
    cpu0 = time.process_time()
    reference_path = HERE / "FD_POLICY512_RAW.npz"
    assert hashlib.sha256(reference_path.read_bytes()).hexdigest() == REFERENCE_SHA256
    manifest = json.loads((HERE / "B09_RUN_MANIFEST.json").read_text())
    assert len(manifest["entries"]) == 26
    for path, expected in manifest["entries"].items():
        assert hashlib.sha256((HERE / path).read_bytes()).hexdigest() == expected
    with np.load(reference_path, allow_pickle=False) as z:
        ref = {key: z[key] for key in z.files}
    records = []
    all_pass = True
    for eta_text in ("0.01", "0.1"):
        eta = float(eta_text)
        suffix = f"eta{eta:g}"
        for policy in ("baseline", "fd50"):
            label = "baseline" if policy == "baseline" else "strong"
            expected_query = ref[f"classic_delayed_ell50_{suffix}_{label}_queried"]
            expected_update = ref[f"classic_delayed_ell50_{suffix}_{label}_updated"]
            expected_loss = ref[f"classic_delayed_ell50_{suffix}_incoming_residual"]
            for repeat in range(3):
                stem = f"B09_{policy}_eta{eta_text.replace('.', 'p')}_r{repeat}"
                raw_path = HERE / f"{stem}.npz"
                summary_path = HERE / f"{stem}.json"
                inventory = validate_npz(raw_path, ["query", "update", "loss", "queried_opt", "energy"])
                with np.load(raw_path, allow_pickle=False) as z:
                    raw = {key: z[key] for key in z.files}
                summary = json.loads(summary_path.read_text())
                queried = np.flatnonzero(raw["query"])
                tol = 1e-10 * np.maximum(1.0, raw["energy"])
                checks = {
                    "query_mask_exact": bool(np.array_equal(raw["query"], expected_query)),
                    "update_mask_exact": bool(np.array_equal(raw["update"], expected_update)),
                    "loss_close": bool(np.all(np.abs(raw["loss"] - expected_loss) <= tol)),
                    "queried_opt_close": bool(np.all(np.abs(raw["queried_opt"][queried] - ref["opt"][queried]) <= tol[queried])),
                    "summary_counts": bool(
                        summary["queries_after_growth"] == int(raw["query"][25:].sum())
                        and summary["refreshes_after_growth"] == int(raw["update"][25:].sum())
                    ),
                    "raw_hash": inventory["sha256"] == summary["raw_artifact"]["sha256"],
                    "gram_diagonal_close": bool(np.all(np.abs(raw["gram_diagonal"] - np.diff(np.r_[0.0, raw["energy"]])) <= tol)),
                    "gate_is_valid_lower_bound": bool(np.all(raw["gate_lower"] <= ref["opt"] + tol)),
                    "nonrefresh_is_feasible": bool(
                        np.all(raw["loss"][~raw["update"]] <= (1.0 + eta) * ref["opt"][~raw["update"]] + tol[~raw["update"]])
                    ),
                }
                passed = all(checks.values())
                all_pass &= passed
                records.append({
                    "policy": policy,
                    "eta": eta,
                    "repeat": repeat,
                    "checks": checks,
                    "pass": passed,
                    "algorithm_cpu_seconds": summary["algorithm_cpu_seconds"],
                    "algorithm_wall_seconds": summary["algorithm_wall_seconds"],
                    "peak_rss_kib": summary["peak_rss_kib"],
                    "raw_sha256": inventory["sha256"],
                })
    paired = []
    for eta in (0.01, 0.1):
        for repeat in range(3):
            base = next(r for r in records if r["eta"] == eta and r["repeat"] == repeat and r["policy"] == "baseline")
            fd = next(r for r in records if r["eta"] == eta and r["repeat"] == repeat and r["policy"] == "fd50")
            paired.append({
                "eta": eta,
                "repeat": repeat,
                "fd_cpu_saved_seconds": base["algorithm_cpu_seconds"] - fd["algorithm_cpu_seconds"],
                "baseline_over_fd_cpu": base["algorithm_cpu_seconds"] / fd["algorithm_cpu_seconds"],
            })
    timing = {}
    for eta_text in ("0.01", "0.1"):
        timing[eta_text] = {}
        for policy in ("baseline", "fd50"):
            b08_median, b08 = median_cpu("B08", policy, eta_text)
            b09_median, b09 = median_cpu("B09", policy, eta_text)
            timing[eta_text][policy] = {
                "b08_full_svd_cpu": b08,
                "b09_cached_gram_cpu": b09,
                "b08_median_cpu": b08_median,
                "b09_median_cpu": b09_median,
                "b08_over_b09_median": b08_median / b09_median,
            }
    cal_inventory = validate_npz(
        HERE / "B09_GRAM1024_CALIBRATION_RAW.npz",
        ["checkpoints", "energy", "gram_opt", "svd_opt", "normalized_error"],
    )
    calibration = json.loads((HERE / "B09_GRAM1024_CALIBRATION.json").read_text())
    with np.load(HERE / "B09_GRAM1024_CALIBRATION_RAW.npz", allow_pickle=False) as z:
        cal = {key: z[key] for key in z.files}
    cal_checks = {
        "raw_hash": cal_inventory["sha256"] == calibration["raw_artifact"]["sha256"],
        "fixed_checkpoints": bool(np.array_equal(cal["checkpoints"], np.asarray([512, 640, 768, 896, 1024]))),
        "reported_error": bool(np.isclose(np.max(cal["normalized_error"]), calibration["max_normalized_opt_error"], rtol=0, atol=1e-18)),
        "normalized_opt_error": bool(np.all(cal["normalized_error"] <= 1e-10)),
        "numerical_pass": calibration["numerical_pass"] is True,
        "continuous_policy_not_claimed": calibration["continuous_policy_executed"] is False,
    }
    all_pass &= all(cal_checks.values())
    out = {
        "audit_pass": bool(all_pass),
        "verified_policy_runs": len(records),
        "records": records,
        "paired": paired,
        "timing_comparison": timing,
        "calibration1024_checks": cal_checks,
        "calibration1024": calibration,
        "reference_sha256": REFERENCE_SHA256,
        "run_manifest_sha256": hashlib.sha256((HERE / "B09_RUN_MANIFEST.json").read_bytes()).hexdigest(),
        "scope": "native512 same-prefix stronger exact-query implementation audit plus sampled native1024 resource/numerical calibration; not independent confirmation or native5000",
        "usage": {
            "wall_seconds": time.perf_counter() - wall0,
            "cpu_seconds": time.process_time() - cpu0,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
    }
    atomic_write_json(HERE / "B09_CACHED_GRAM_AUDIT.json", out)
    print(json.dumps({key: value for key, value in out.items() if key not in ("records",)}, allow_nan=False))
    assert all_pass, "B09 audit failed; evidence retained"


if __name__ == "__main__":
    main()
