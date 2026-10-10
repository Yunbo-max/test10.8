"""Audit B08 operational runs against frozen B07 reference arrays."""
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


def main():
    wall0 = time.perf_counter()
    cpu0 = time.process_time()
    reference_path = HERE / "FD_POLICY512_RAW.npz"
    assert hashlib.sha256(reference_path.read_bytes()).hexdigest() == REFERENCE_SHA256
    run_manifest = json.loads((HERE / "B08_RUN_MANIFEST.json").read_text())
    assert len(run_manifest["entries"]) == 24
    for path, expected in run_manifest["entries"].items():
        assert hashlib.sha256((HERE / path).read_bytes()).hexdigest() == expected
    ref_inventory = validate_npz(reference_path, ["a", "opt", "energy"])
    with np.load(reference_path, allow_pickle=False) as z:
        ref = {key: z[key] for key in z.files}
    k = 25
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
                stem = f"B08_{policy}_eta{eta_text.replace('.', 'p')}_r{repeat}"
                raw_path = HERE / f"{stem}.npz"
                summary_path = HERE / f"{stem}.json"
                inv = validate_npz(raw_path, ["query", "update", "loss", "queried_opt"])
                with np.load(raw_path, allow_pickle=False) as z:
                    raw = {key: z[key] for key in z.files}
                summary = json.loads(summary_path.read_text())
                q = raw["query"]
                u = raw["update"]
                queried = np.flatnonzero(q)
                tol = 1e-10 * np.maximum(1.0, raw["energy"])
                checks = {
                    "query_mask_exact": bool(np.array_equal(q, expected_query)),
                    "update_mask_exact": bool(np.array_equal(u, expected_update)),
                    "loss_close": bool(np.all(np.abs(raw["loss"] - expected_loss) <= tol)),
                    "queried_opt_close": bool(np.all(np.abs(raw["queried_opt"][queried] - ref["opt"][queried]) <= tol[queried])),
                    "summary_counts": bool(summary["queries_after_growth"] == int(q[k:].sum()) and summary["refreshes_after_growth"] == int(u[k:].sum())),
                    "raw_hash": inv["sha256"] == summary["raw_artifact"]["sha256"],
                    "gate_is_valid_lower_bound": bool(np.all(raw["gate_lower"] <= ref["opt"] + tol)),
                    "nonrefresh_is_feasible": bool(np.all(raw["loss"][~u] <= (1.0 + eta) * ref["opt"][~u] + tol[~u])),
                }
                if policy == "fd50":
                    checks["fd_bound_is_valid"] = bool(np.all(raw["fd_bound"] <= ref["opt"] + tol))
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
                    "raw_sha256": inv["sha256"],
                })
    for eta in (0.01, 0.1):
        for repeat in range(3):
            a = next(r for r in records if r["eta"] == eta and r["repeat"] == repeat and r["policy"] == "baseline")
            b = next(r for r in records if r["eta"] == eta and r["repeat"] == repeat and r["policy"] == "fd50")
            a["paired_fd_cpu_saved_seconds"] = a["algorithm_cpu_seconds"] - b["algorithm_cpu_seconds"]
            a["paired_baseline_over_fd_cpu"] = a["algorithm_cpu_seconds"] / b["algorithm_cpu_seconds"]
    out = {
        "audit_pass": bool(all_pass),
        "records": records,
        "reference_raw_sha256": ref_inventory["sha256"],
        "run_manifest_sha256": hashlib.sha256((HERE / "B08_RUN_MANIFEST.json").read_bytes()).hexdigest(),
        "verified_operational_runs": len(records),
        "scope": "native512 development; exact B07 semantic replay; not independent experiment replication or native5000",
        "usage": {
            "wall_seconds": time.perf_counter() - wall0,
            "cpu_seconds": time.process_time() - cpu0,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
    }
    atomic_write_json(HERE / "B08_OPERATIONAL_AUDIT.json", out)
    print(json.dumps({k: v for k, v in out.items() if k != "records"}, allow_nan=False))
    assert all_pass, "B08 audit failed; evidence retained"


if __name__ == "__main__":
    main()

