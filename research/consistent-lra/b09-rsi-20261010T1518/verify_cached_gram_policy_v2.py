"""Audit B09 V2 hybrid Gram-OPT/full-SVD-refresh policy runs."""
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
    vals = [
        json.loads((HERE / f"{prefix}_{policy}_eta{eta_text.replace('.', 'p')}_r{r}.json").read_text())["algorithm_cpu_seconds"]
        for r in range(3)
    ]
    return float(np.median(vals)), vals


def main():
    wall0 = time.perf_counter()
    cpu0 = time.process_time()
    ref_path = HERE / "FD_POLICY512_RAW.npz"
    assert hashlib.sha256(ref_path.read_bytes()).hexdigest() == REFERENCE_SHA256
    manifest = json.loads((HERE / "B09_V2_RUN_MANIFEST.json").read_text())
    assert len(manifest["entries"]) == 24
    for path, expected in manifest["entries"].items():
        assert hashlib.sha256((HERE / path).read_bytes()).hexdigest() == expected
    with np.load(ref_path, allow_pickle=False) as z:
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
                stem = f"B09V2_{policy}_eta{eta_text.replace('.', 'p')}_r{repeat}"
                inv = validate_npz(HERE / f"{stem}.npz", ["query", "update", "loss", "queried_opt", "energy"])
                with np.load(HERE / f"{stem}.npz", allow_pickle=False) as z:
                    raw = {key: z[key] for key in z.files}
                summary = json.loads((HERE / f"{stem}.json").read_text())
                queried = np.flatnonzero(raw["query"])
                tol = 1e-10 * np.maximum(1.0, raw["energy"])
                loss_abs = np.abs(raw["loss"] - expected_loss)
                checks = {
                    "query_mask_exact": bool(np.array_equal(raw["query"], expected_query)),
                    "update_mask_exact": bool(np.array_equal(raw["update"], expected_update)),
                    "loss_close": bool(np.all(loss_abs <= tol)),
                    "queried_opt_close": bool(np.all(np.abs(raw["queried_opt"][queried] - ref["opt"][queried]) <= tol[queried])),
                    "summary_counts": bool(
                        summary["queries_after_growth"] == int(raw["query"][25:].sum())
                        and summary["refreshes_after_growth"] == int(raw["update"][25:].sum())
                    ),
                    "raw_hash": inv["sha256"] == summary["raw_artifact"]["sha256"],
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
                    "max_loss_difference": float(np.max(loss_abs)),
                    "max_normalized_loss_difference": float(np.max(loss_abs / np.maximum(1.0, raw["energy"]))),
                    "algorithm_cpu_seconds": summary["algorithm_cpu_seconds"],
                    "algorithm_wall_seconds": summary["algorithm_wall_seconds"],
                    "component_cpu_seconds": summary["component_cpu_seconds"],
                    "peak_rss_kib": summary["peak_rss_kib"],
                    "raw_sha256": inv["sha256"],
                })
    paired = []
    for eta in (0.01, 0.1):
        for repeat in range(3):
            base = next(x for x in records if x["eta"] == eta and x["repeat"] == repeat and x["policy"] == "baseline")
            fd = next(x for x in records if x["eta"] == eta and x["repeat"] == repeat and x["policy"] == "fd50")
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
            b09_median, b09 = median_cpu("B09V2", policy, eta_text)
            timing[eta_text][policy] = {
                "b08_full_query_svd_cpu": b08,
                "b09v2_gram_opt_refresh_svd_cpu": b09,
                "b08_median_cpu": b08_median,
                "b09v2_median_cpu": b09_median,
                "b08_over_b09v2_median": b08_median / b09_median,
            }
    v1 = json.loads((HERE / "B09_CACHED_GRAM_AUDIT.json").read_text())
    v1_failure_preserved = (
        v1["audit_pass"] is False
        and all(
            sorted(key for key, value in row["checks"].items() if not value) == ["loss_close"]
            for row in v1["records"]
        )
    )
    all_pass &= v1_failure_preserved
    out = {
        "audit_pass": bool(all_pass),
        "verified_policy_runs": len(records),
        "records": records,
        "paired": paired,
        "timing_comparison": timing,
        "v1_semantic_failure_preserved": v1_failure_preserved,
        "reference_sha256": REFERENCE_SHA256,
        "run_manifest_sha256": hashlib.sha256((HERE / "B09_V2_RUN_MANIFEST.json").read_bytes()).hexdigest(),
        "scope": "native512 same-prefix stronger exact-query implementation audit; existing comparator; not independent confirmation or native5000",
        "usage": {
            "wall_seconds": time.perf_counter() - wall0,
            "cpu_seconds": time.process_time() - cpu0,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
    }
    atomic_write_json(HERE / "B09_V2_CACHED_GRAM_AUDIT.json", out)
    print(json.dumps({key: value for key, value in out.items() if key != "records"}, allow_nan=False))
    assert all_pass, "B09 V2 audit failed; evidence retained"


if __name__ == "__main__":
    main()
