"""B05: separate one-step solver error from recursive/oracle amplification.

The phases are deliberately separate so every scientific command stays below the
frozen 120-second command ceiling.  ``assemble`` only joins already-written
artifacts and cannot change any numerical result.
"""
import argparse
import hashlib
import json
import os
import pathlib
import resource
import time

for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"

import numpy as np

import baseline_matrix_study as baseline
import solver
from atomic_npz import atomic_savez, atomic_write_json, sha256, validate_npz

HERE = pathlib.Path(__file__).resolve().parent
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024 ** 3, 2 * 1024 ** 3))
TOL_PROJECTOR = 1e-8
TOL_ONE_STEP = 1e-10
K = 25


def projector_distance(q, v):
    value = q.shape[1] + v.shape[1] - 2.0 * float(np.sum((q.T @ v) ** 2))
    return float(np.sqrt(max(0.0, value)))


def oracle_for(a):
    out = []
    for t in range(1, len(a) + 1):
        _u, singular, vh = np.linalg.svd(a[:t], full_matrices=False)
        out.append((vh[: min(K, t)].T.copy(), float(np.sum(singular[min(K, t):] ** 2))))
    return out


class SharedOracleArm(baseline.Arm):
    def __init__(self, d, eta, oracle):
        super().__init__(d, K, eta, "boundary", K)
        self.oracle = oracle

    def optimum(self, t):
        self.queries += 1
        v, opt = self.oracle[t - 1]
        self.cached = max(self.cached, opt - 1e-10 * max(1.0, self.E), 0.0)
        return v.copy(), opt


class FreshOracleArm(baseline.Arm):
    def __init__(self, a, eta):
        super().__init__(a.shape[1], K, eta, "boundary", K)
        self.a = a

    def optimum(self, t):
        self.queries += 1
        _u, singular, vh = np.linalg.svd(self.a[:t], full_matrices=False)
        v = vh[: min(K, t)].T.copy()
        opt = float(np.sum(singular[min(K, t):] ** 2))
        self.cached = max(self.cached, opt - 1e-10 * max(1.0, self.E), 0.0)
        return v, opt


def compare_same_input(q, v, g, e, target, tol):
    old, old_fallback = solver.boundary_legacy(q, v, g, e, target, tol)
    new, new_fallback = solver.boundary_newton(q, v, g, e, target, tol)
    return {
        "distance": projector_distance(old, new),
        "old_fallback": bool(old_fallback),
        "new_fallback": bool(new_fallback),
        "near_zero": bool(target <= tol),
        "target": float(target),
        "tol": float(tol),
        "target_over_tol": float(target / tol) if tol > 0 else None,
    }, old, new


def shared_oracle_run(a, eta, oracle, captured):
    old_arm = SharedOracleArm(a.shape[1], eta, oracle)
    new_arm = SharedOracleArm(a.shape[1], eta, oracle)
    rows = []
    old_calls = []
    new_calls = []

    def old_path(q, v, g, e, target, tol):
        item, old, _new = compare_same_input(q, v, g, e, target, tol)
        item.update({"arm": "old", "eta": eta, "prefix": current_prefix})
        old_calls.append(item)
        captured.append((q.copy(), v.copy(), float(e), float(target), float(tol), eta, current_prefix, "old"))
        return old, item["old_fallback"]

    def new_path(q, v, g, e, target, tol):
        item, _old, new = compare_same_input(q, v, g, e, target, tol)
        item.update({"arm": "new", "eta": eta, "prefix": current_prefix})
        new_calls.append(item)
        captured.append((q.copy(), v.copy(), float(e), float(target), float(tol), eta, current_prefix, "new"))
        return new, item["new_fallback"]

    for current_prefix, x in enumerate(a, 1):
        qo_before = None if old_arm.Q is None else old_arm.Q.copy()
        qn_before = None if new_arm.Q is None else new_arm.Q.copy()
        old_q0, new_q0 = old_arm.queries, new_arm.queries
        baseline.boundary_path = old_path
        qo, old_changed = old_arm.step(x, current_prefix)
        baseline.boundary_path = new_path
        qn, new_changed = new_arm.step(x, current_prefix)
        incoming_distance = 0.0 if qo_before is None else projector_distance(qo_before, qn_before)
        actual_distance = projector_distance(qo, qn)
        rows.append({
            "prefix": current_prefix,
            "incoming_distance": incoming_distance,
            "actual_distance": actual_distance,
            "old_changed": bool(old_changed),
            "new_changed": bool(new_changed),
            "old_queried": old_arm.queries > old_q0,
            "new_queried": new_arm.queries > new_q0,
        })
    return {
        "eta": eta,
        "rows": rows,
        "old_calls": old_calls,
        "new_calls": new_calls,
        "max_recursive_projector_distance": max(x["actual_distance"] for x in rows),
        "first_nonzero_prefix": next((x["prefix"] for x in rows if x["actual_distance"] > 0), None),
        "first_over_threshold_prefix": next((x["prefix"] for x in rows if x["actual_distance"] > TOL_PROJECTOR), None),
        "update_mask_differences": sum(x["old_changed"] != x["new_changed"] for x in rows),
        "query_mask_differences": sum(x["old_queried"] != x["new_queried"] for x in rows),
        "max_same_input_distance": max([x["distance"] for x in old_calls + new_calls] or [0.0]),
        "boundary_calls": len(old_calls) + len(new_calls),
        "near_zero_boundary_calls": sum(x["near_zero"] for x in old_calls + new_calls),
    }


def duplicate_legacy_run(a, eta):
    left = FreshOracleArm(a, eta)
    right = FreshOracleArm(a, eta)
    rows = []
    baseline.boundary_path = solver.boundary_legacy
    for prefix, x in enumerate(a, 1):
        ql, lc = left.step(x, prefix)
        qr, rc = right.step(x, prefix)
        rows.append({"prefix": prefix, "distance": projector_distance(ql, qr), "left_changed": bool(lc), "right_changed": bool(rc)})
    return {
        "eta": eta,
        "max_projector_distance": max(x["distance"] for x in rows),
        "first_nonzero_prefix": next((x["prefix"] for x in rows if x["distance"] > 0), None),
        "first_over_threshold_prefix": next((x["prefix"] for x in rows if x["distance"] > TOL_PROJECTOR), None),
        "update_mask_differences": sum(x["left_changed"] != x["right_changed"] for x in rows),
        "rows": rows,
    }


def timing_summary_from_rows(rows):
    summary = {}
    for near_zero in (True, False):
        group = [x for x in rows if x["near_zero"] == near_zero]
        if not group:
            continue
        entry = {"states_times_repeats": len(group) // 2}
        for name in ("legacy", "newton"):
            subset = [x for x in group if x["solver"] == name]
            entry[name + "_median_cpu_seconds"] = float(np.median([x["cpu_seconds"] for x in subset]))
            entry[name + "_median_wall_seconds"] = float(np.median([x["wall_seconds"] for x in subset]))
        entry["legacy_over_newton_median_cpu"] = entry["legacy_median_cpu_seconds"] / entry["newton_median_cpu_seconds"]
        summary["near_zero" if near_zero else "non_near_zero"] = entry
    return summary


def timed_calls(captured, a, repeats=5):
    rng = np.random.default_rng(20261010)
    rows = []
    for index, state in enumerate(captured):
        q, v, e, target, tol, eta, prefix, arm = state
        g = a[:prefix].T @ a[:prefix]
        jobs = [name for _ in range(repeats) for name in ("legacy", "newton")]
        rng.shuffle(jobs)
        reference = None
        for name in jobs:
            w0, c0 = time.perf_counter(), time.process_time()
            if name == "legacy":
                out, fallback = solver.boundary_legacy(q, v, g, e, target, tol)
            else:
                out, fallback = solver.boundary_newton(q, v, g, e, target, tol)
            wall, cpu = time.perf_counter() - w0, time.process_time() - c0
            if reference is None:
                reference = out
            rows.append({
                "state_index": index,
                "solver": name,
                "wall_seconds": wall,
                "cpu_seconds": cpu,
                "near_zero": bool(target <= tol),
                "eta": eta,
                "prefix": prefix,
                "arm": arm,
                "fallback": bool(fallback),
                "distance_to_first_output": projector_distance(reference, out),
            })
        del g
    return rows, timing_summary_from_rows(rows)


def load_parent():
    assert sha256(HERE / "LANDMARK128_RAW_V3.npz") == "de6f3279d021f8a442cd5f6b51ac4948457045263eb334e6cade78b0380b6dff"
    assert sha256(HERE / "landmark.mtx") == "29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b"
    with np.load(HERE / "LANDMARK128_RAW_V3.npz", allow_pickle=False) as z:
        a = z["a"].copy()
        parent = {
            "eta0.01_max_checkpoint": max(float(projector_distance(q, v)) for q, v in zip(z["old_eta0.01_basis"], z["new_eta0.01_basis"])),
            "eta0.1_max_checkpoint": max(float(projector_distance(q, v)) for q, v in zip(z["old_eta0.1_basis"], z["new_eta0.1_basis"])),
        }
    return a, parent


def phase_shared():
    wall0, cpu0 = time.perf_counter(), time.process_time()
    a, parent = load_parent()
    oracle = oracle_for(a)
    captured = []
    shared = [shared_oracle_run(a, eta, oracle, captured) for eta in (0.01, 0.1)]
    all_calls = [x for run in shared for x in run["old_calls"] + run["new_calls"]]
    acceptance = {
        "shared_update_masks_equal": all(x["update_mask_differences"] == 0 for x in shared),
        "shared_query_masks_equal": all(x["query_mask_differences"] == 0 for x in shared),
        "shared_recursive_projector_at_most_1e-8": all(x["max_recursive_projector_distance"] <= TOL_PROJECTOR for x in shared),
        "same_input_step_at_most_1e-10": all(x["max_same_input_distance"] <= TOL_ONE_STEP for x in shared),
        "captured_calls_nonempty": bool(all_calls),
        "all_observed_calls_near_zero": bool(all_calls) and all(x["near_zero"] for x in all_calls),
    }
    capture_arrays = {
        "q": np.stack([x[0] for x in captured]),
        "v": np.stack([x[1] for x in captured]),
        "e": np.asarray([x[2] for x in captured]),
        "target": np.asarray([x[3] for x in captured]),
        "tol": np.asarray([x[4] for x in captured]),
        "eta": np.asarray([x[5] for x in captured]),
        "prefix": np.asarray([x[6] for x in captured], dtype=np.int64),
        "arm": np.asarray([x[7] for x in captured], dtype="U3"),
    }
    capture_validation = atomic_savez(HERE / "SAME_INPUT_CAPTURE.npz", capture_arrays, capture_arrays.keys())
    out = {
        "scope": "B05 frozen same-input shared-oracle replay on native Landmark first128",
        "design_sha256": sha256(HERE / "B05_FROZEN_DESIGN.md"),
        "source_sha256": sha256(__file__),
        "solver_sha256": sha256(HERE / "solver.py"),
        "baseline_sha256": sha256(HERE / "baseline_matrix_study.py"),
        "parent_raw_sha256": sha256(HERE / "LANDMARK128_RAW_V3.npz"),
        "matrix_sha256": sha256(HERE / "landmark.mtx"),
        "parent_checkpoint_differences": parent,
        "shared_oracle": shared,
        "acceptance": acceptance,
        "capture_validation": capture_validation,
        "usage": {
            "wall_seconds": time.perf_counter() - wall0,
            "cpu_seconds": time.process_time() - cpu0,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
    }
    atomic_write_json(HERE / "SAME_INPUT_SHARED.json", out)
    print(json.dumps({"acceptance": acceptance, "shared": [{k: x[k] for k in ("eta","max_recursive_projector_distance","max_same_input_distance","boundary_calls","near_zero_boundary_calls")} for x in shared], "capture_validation": capture_validation, "usage": out["usage"]}))


def phase_duplicate():
    wall0, cpu0 = time.perf_counter(), time.process_time()
    a, _parent = load_parent()
    duplicate = [duplicate_legacy_run(a, eta) for eta in (0.01, 0.1)]
    out = {
        "scope": "B05 two fresh-SVD legacy controls on native Landmark first128",
        "source_sha256": sha256(__file__),
        "duplicate_legacy_fresh_oracle": duplicate,
        "usage": {"wall_seconds": time.perf_counter() - wall0, "cpu_seconds": time.process_time() - cpu0, "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
    }
    atomic_write_json(HERE / "SAME_INPUT_DUPLICATE.json", out)
    print(json.dumps({"duplicate": [{k: x[k] for k in ("eta","max_projector_distance","first_nonzero_prefix","first_over_threshold_prefix","update_mask_differences")} for x in duplicate], "usage": out["usage"]}))


def phase_timing(shard):
    wall0, cpu0 = time.perf_counter(), time.process_time()
    a, _parent = load_parent()
    validation = validate_npz(HERE / "SAME_INPUT_CAPTURE.npz", ("q", "v", "e", "target", "tol", "eta", "prefix", "arm"))
    with np.load(HERE / "SAME_INPUT_CAPTURE.npz", allow_pickle=False) as z:
        # Each compressed member must be materialized once.  Repeating z["q"]
        # inside the comprehension decompresses the complete member on every
        # iteration and the returned row views retain all those allocations.
        q_all, v_all = z["q"], z["v"]
        e_all, target_all, tol_all = z["e"], z["target"], z["tol"]
        eta_all, prefix_all, arm_all = z["eta"], z["prefix"], z["arm"]
        all_captured = [(q_all[i], v_all[i], float(e_all[i]), float(target_all[i]), float(tol_all[i]), float(eta_all[i]), int(prefix_all[i]), str(arm_all[i])) for i in range(len(e_all))]
    captured = [state for i, state in enumerate(all_captured) if i % 2 == shard]
    timings, timing_summary = timed_calls(captured, a)
    out = {
        "scope": "B05 solver-only randomized timing on captured same-input states",
        "shard": shard,
        "shard_count": 2,
        "global_state_indices": [i for i in range(len(all_captured)) if i % 2 == shard],
        "source_sha256": sha256(__file__),
        "capture_validation": validation,
        "timing_summary": timing_summary,
        "timing_records": timings,
        "usage": {"wall_seconds": time.perf_counter() - wall0, "cpu_seconds": time.process_time() - cpu0, "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
    }
    atomic_write_json(HERE / f"SAME_INPUT_TIMING_{shard}.json", out)
    print(json.dumps({"timing_summary": timing_summary, "usage": out["usage"]}))


def phase_assemble():
    shared = json.loads((HERE / "SAME_INPUT_SHARED.json").read_text())
    duplicate = json.loads((HERE / "SAME_INPUT_DUPLICATE.json").read_text())
    timing_parts = [json.loads((HERE / f"SAME_INPUT_TIMING_{i}.json").read_text()) for i in range(2)]
    timing_records = []
    for part in timing_parts:
        for local_index, row in enumerate(part["timing_records"]):
            copied = dict(row)
            copied["shard"] = part["shard"]
            copied["global_state_index"] = part["global_state_indices"][row["state_index"]]
            copied["shard_record_index"] = local_index
            timing_records.append(copied)
    global_indices = sorted(set(x["global_state_index"] for x in timing_records))
    per_state_solver_counts = {
        i: {name: sum(x["global_state_index"] == i and x["solver"] == name for x in timing_records) for name in ("legacy", "newton")}
        for i in global_indices
    }
    assert global_indices == list(range(148))
    assert len(timing_records) == 148 * 2 * 5
    assert all(counts == {"legacy": 5, "newton": 5} for counts in per_state_solver_counts.values())
    assert sorted(timing_parts[0]["global_state_indices"] + timing_parts[1]["global_state_indices"]) == list(range(148))
    timing_summary = timing_summary_from_rows(timing_records)
    acceptance = shared["acceptance"]
    interpretation = {
        "recurrence_or_oracle_mechanism_supported": all(acceptance[k] for k in ("shared_update_masks_equal", "shared_query_masks_equal", "shared_recursive_projector_at_most_1e-8", "same_input_step_at_most_1e-10")),
        "root_discrepancy_supported": (not acceptance["same_input_step_at_most_1e-10"]) or (not acceptance["shared_recursive_projector_at_most_1e-8"]),
        "broader_fallback_changes_observed_native_calls": not acceptance["all_observed_calls_near_zero"],
        "native_acceleration_active_on_captured_calls": not acceptance["all_observed_calls_near_zero"],
        "fresh_oracle_numeric_drift_at_or_above_1e-8": any(x["max_projector_distance"] > TOL_PROJECTOR for x in duplicate["duplicate_legacy_fresh_oracle"]),
        "solver_same_input_discrepancy_at_or_above_1e-10": not acceptance["same_input_step_at_most_1e-10"],
        "b04_retroactively_passed": False,
        "landmark512_admitted_by_this_command": False,
    }
    out = dict(shared)
    out.update({
        "scope": "B05 frozen same-input replay on native Landmark first128; development mechanism diagnosis and solver-only timing",
        "duplicate_legacy_fresh_oracle": duplicate["duplicate_legacy_fresh_oracle"],
        "timing_summary": timing_summary,
        "timing_records": timing_records,
        "interpretation": interpretation,
        "audit": {
            "timing_states_complete_and_disjoint": True,
            "timing_record_count": len(timing_records),
            "five_repeats_per_solver_per_state": True,
            "max_distance_to_first_output": max(x["distance_to_first_output"] for x in timing_records),
            "near_zero_dispatch_records": sum(x["near_zero"] for x in timing_records),
            "non_near_zero_records": sum(not x["near_zero"] for x in timing_records),
            "returned_endpoint_fallback_records": sum(x["fallback"] for x in timing_records),
            "fallback_field_semantics": "endpoint-or-certificate fallback return flag; near-zero legacy dispatch is represented by near_zero",
        },
        "phase_hashes": {name: sha256(HERE / name) for name in ("SAME_INPUT_SHARED.json", "SAME_INPUT_DUPLICATE.json", "SAME_INPUT_TIMING_0.json", "SAME_INPUT_TIMING_1.json", "SAME_INPUT_CAPTURE.npz")},
        "phase_usage": {"shared": shared["usage"], "duplicate": duplicate["usage"], "timing_0": timing_parts[0]["usage"], "timing_1": timing_parts[1]["usage"]},
    })
    out["usage"] = {
        "wall_seconds_sum": sum(x["wall_seconds"] for x in out["phase_usage"].values()),
        "cpu_seconds_sum": sum(x["cpu_seconds"] for x in out["phase_usage"].values()),
        "peak_rss_kib_max": max(x["peak_rss_kib"] for x in out["phase_usage"].values()),
    }
    atomic_write_json(HERE / "SAME_INPUT_REPLAY.json", out)
    print(json.dumps({"acceptance": acceptance, "interpretation": interpretation, "timing_summary": out["timing_summary"], "usage": out["usage"]}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True, choices=("shared", "duplicate", "timing", "assemble"))
    parser.add_argument("--shard", type=int, choices=(0, 1))
    args = parser.parse_args()
    if args.phase == "timing":
        if args.shard is None:
            parser.error("--phase timing requires --shard {0,1}")
        phase_timing(args.shard)
    else:
        {"shared": phase_shared, "duplicate": phase_duplicate, "assemble": phase_assemble}[args.phase]()


if __name__ == "__main__":
    main()
