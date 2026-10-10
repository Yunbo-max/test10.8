"""B06: audit cancellation in the B04/B05 projector-distance implementation."""
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
import same_input_replay_b05 as b05
import solver

HERE = pathlib.Path(__file__).resolve().parent
K = 25
PROJECTOR_TOL = 1e-8
ONE_STEP_TOL = 1e-10


def sha256(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def old_distance(q, v):
    sq = q.shape[1] + v.shape[1] - 2.0 * float(np.sum((q.T @ v) ** 2))
    return float(np.sqrt(max(0.0, sq))), float(sq)


def orth_defect(q):
    return float(np.linalg.norm(q.T @ q - np.eye(q.shape[1]), ord="fro"))


def stable_distance(q, v, reorthogonalize=True):
    if reorthogonalize:
        q = np.linalg.qr(q, mode="reduced")[0]
        v = np.linalg.qr(v, mode="reduced")[0]
    left = v - q @ (q.T @ v)
    right = q - v @ (v.T @ q)
    return float(np.sqrt(np.sum(left * left) + np.sum(right * right)))


def metrics(q, v):
    old, old_sq = old_distance(q, v)
    return {
        "old_cancelling_distance": old,
        "old_unclipped_squared": old_sq,
        "stable_raw_symmetric_residual": stable_distance(q, v, False),
        "stable_qr_symmetric_residual": stable_distance(q, v, True),
        "q_orthogonality_fro": orth_defect(q),
        "v_orthogonality_fro": orth_defect(v),
    }


def direct_dense_distance(q, v):
    q = np.linalg.qr(q, mode="reduced")[0]
    v = np.linalg.qr(v, mode="reduced")[0]
    p = q @ q.T
    p -= v @ v.T
    return float(np.linalg.norm(p, ord="fro"))


def summarize(rows, threshold):
    keys = (
        "old_cancelling_distance",
        "stable_raw_symmetric_residual",
        "stable_qr_symmetric_residual",
        "q_orthogonality_fro",
        "v_orthogonality_fro",
    )
    out = {"count": len(rows), "threshold": threshold}
    for key in keys:
        vals = np.asarray([r[key] for r in rows], dtype=float)
        out[key + "_max"] = float(vals.max(initial=0.0))
        out[key + "_median"] = float(np.median(vals)) if len(vals) else 0.0
    out["old_over_threshold"] = sum(r["old_cancelling_distance"] > threshold for r in rows)
    out["stable_qr_over_threshold"] = sum(r["stable_qr_symmetric_residual"] > threshold for r in rows)
    return out


def audit_same_input(a, capture):
    by_prefix = {}
    for idx, prefix in enumerate(capture["prefix"]):
        by_prefix.setdefault(int(prefix), []).append(idx)
    g = np.zeros((a.shape[1], a.shape[1]), dtype=float)
    rows = []
    max_pair = None
    max_stable = -1.0
    for prefix, x in enumerate(a, 1):
        g += np.outer(x, x)
        for idx in by_prefix.get(prefix, []):
            q = capture["q"][idx]
            v = capture["v"][idx]
            e = float(capture["e"][idx])
            target = float(capture["target"][idx])
            tol = float(capture["tol"][idx])
            old, old_fb = solver.boundary_legacy(q, v, g, e, target, tol)
            new, new_fb = solver.boundary_newton(q, v, g, e, target, tol)
            row = metrics(old, new)
            row.update({
                "state_index": int(idx), "prefix": prefix,
                "eta": float(capture["eta"][idx]), "arm": str(capture["arm"][idx]),
                "near_zero": bool(target <= tol),
                "old_fallback": bool(old_fb), "new_fallback": bool(new_fb),
                "output_bitwise_equal": bool(np.array_equal(old, new)),
            })
            rows.append(row)
            if row["stable_qr_symmetric_residual"] > max_stable:
                max_stable = row["stable_qr_symmetric_residual"]
                max_pair = (old.copy(), new.copy(), int(idx))
    assert len(rows) == len(capture["prefix"])
    dense = direct_dense_distance(max_pair[0], max_pair[1])
    return rows, {
        "selected_state_index": max_pair[2],
        "stable_qr": max_stable,
        "dense_projector": dense,
        "absolute_difference": abs(dense - max_stable),
    }


def oracle_for(a):
    out = []
    for t in range(1, len(a) + 1):
        _u, singular, vh = np.linalg.svd(a[:t], full_matrices=False)
        out.append((vh[: min(K, t)].T.copy(), float(np.sum(singular[min(K, t):] ** 2))))
    return out


def replay_shared(a, eta, oracle):
    old_arm = b05.SharedOracleArm(a.shape[1], eta, oracle)
    new_arm = b05.SharedOracleArm(a.shape[1], eta, oracle)
    rows = []
    for prefix, x in enumerate(a, 1):
        baseline.boundary_path = solver.boundary_legacy
        qo, oc = old_arm.step(x, prefix)
        baseline.boundary_path = solver.boundary_newton
        qn, nc = new_arm.step(x, prefix)
        row = metrics(qo, qn)
        row.update({"prefix": prefix, "old_changed": bool(oc), "new_changed": bool(nc),
                    "output_bitwise_equal": bool(np.array_equal(qo, qn))})
        rows.append(row)
    best = max(rows, key=lambda r: r["stable_qr_symmetric_residual"])
    idx = best["prefix"] - 1
    # Deterministically replay only to the selected prefix for an independent dense control.
    old_arm = b05.SharedOracleArm(a.shape[1], eta, oracle)
    new_arm = b05.SharedOracleArm(a.shape[1], eta, oracle)
    qo = qn = None
    for prefix, x in enumerate(a[: idx + 1], 1):
        baseline.boundary_path = solver.boundary_legacy
        qo, _ = old_arm.step(x, prefix)
        baseline.boundary_path = solver.boundary_newton
        qn, _ = new_arm.step(x, prefix)
    dense = direct_dense_distance(qo, qn)
    return rows, {"selected_prefix": idx + 1, "stable_qr": best["stable_qr_symmetric_residual"],
                  "dense_projector": dense, "absolute_difference": abs(dense - best["stable_qr_symmetric_residual"])}


def replay_duplicate(a, eta):
    left = b05.FreshOracleArm(a, eta)
    right = b05.FreshOracleArm(a, eta)
    baseline.boundary_path = solver.boundary_legacy
    rows = []
    for prefix, x in enumerate(a, 1):
        ql, lc = left.step(x, prefix)
        qr, rc = right.step(x, prefix)
        row = metrics(ql, qr)
        row.update({"prefix": prefix, "left_changed": bool(lc), "right_changed": bool(rc),
                    "output_bitwise_equal": bool(np.array_equal(ql, qr))})
        rows.append(row)
    return rows


def audit_parent(parent):
    out = {}
    all_rows = []
    for eta in ("0.01", "0.1"):
        rows = []
        for checkpoint, q, v in zip(parent["checkpoints"], parent[f"old_eta{eta}_basis"], parent[f"new_eta{eta}_basis"]):
            row = metrics(q, v)
            row["checkpoint"] = int(checkpoint)
            rows.append(row)
            all_rows.append(row)
        out[eta] = {"summary": summarize(rows, PROJECTOR_TOL), "rows": rows}
    return out, all_rows


def main():
    wall0, cpu0 = time.perf_counter(), time.process_time()
    resource.setrlimit(resource.RLIMIT_AS, (2 * 1024 ** 3, 2 * 1024 ** 3))
    with np.load(HERE / "LANDMARK128_RAW_V3.npz", allow_pickle=False) as z:
        a = z["a"].copy()
        parent = {key: z[key].copy() for key in z.files}
    with np.load(HERE / "SAME_INPUT_CAPTURE.npz", allow_pickle=False) as z:
        capture = {key: z[key].copy() for key in z.files}

    same_rows, same_dense = audit_same_input(a, capture)
    oracle = oracle_for(a)
    shared = {}
    duplicate = {}
    dense_controls = {"same_input": same_dense}
    for eta in (0.01, 0.1):
        srows, dense = replay_shared(a, eta, oracle)
        drows = replay_duplicate(a, eta)
        shared[str(eta)] = {"summary": summarize(srows, PROJECTOR_TOL), "rows": srows}
        duplicate[str(eta)] = {"summary": summarize(drows, PROJECTOR_TOL), "rows": drows}
        dense_controls[f"shared_eta_{eta}"] = dense
    parent_result, parent_rows = audit_parent(parent)

    same_summary = summarize(same_rows, ONE_STEP_TOL)
    shared_rows = [r for x in shared.values() for r in x["rows"]]
    duplicate_rows = [r for x in duplicate.values() for r in x["rows"]]
    dense_ok = all(x["absolute_difference"] <= 5e-12 for x in dense_controls.values())
    acceptance = {
        "same_input_stable_at_most_1e-10": same_summary["stable_qr_over_threshold"] == 0,
        "shared_recursive_stable_at_most_1e-8": summarize(shared_rows, PROJECTOR_TOL)["stable_qr_over_threshold"] == 0,
        "duplicate_legacy_stable_at_most_1e-8": summarize(duplicate_rows, PROJECTOR_TOL)["stable_qr_over_threshold"] == 0,
        "parent_checkpoint_stable_at_most_1e-8": summarize(parent_rows, PROJECTOR_TOL)["stable_qr_over_threshold"] == 0,
        "dense_controls_agree_at_most_5e-12": dense_ok,
        "all_same_input_outputs_bitwise_equal": all(r["output_bitwise_equal"] for r in same_rows),
    }
    acceptance["prior_projector_failures_are_metric_artifacts"] = all(list(acceptance.values())[:5])
    result = {
        "scope": "B06 numerical definition audit; native Landmark rows 1-128; no algorithm change",
        "formula": {
            "invalid_near_identity": "sqrt(max(0, 2k - 2||Q^T V||_F^2)) evaluated by subtracting O(k) scalars",
            "stable": "sqrt(||(I-QQ^T)V||_F^2 + ||(I-VV^T)Q||_F^2) after reduced QR",
            "identity": "both equal ||QQ^T-VV^T||_F for orthonormal equal-rank bases",
        },
        "float64_eps": float(np.finfo(float).eps),
        "sqrt_k_eps": float(np.sqrt(K * np.finfo(float).eps)),
        "source_hashes": {name: sha256(HERE / name) for name in (
            "stable_metric_audit.py", "B06_FROZEN_DESIGN.md", "solver.py", "baseline_matrix_study.py",
            "same_input_replay_b05.py", "SAME_INPUT_CAPTURE.npz", "LANDMARK128_RAW_V3.npz")},
        "same_input": {"summary": same_summary, "rows": same_rows},
        "shared_recursive": shared,
        "duplicate_legacy": duplicate,
        "parent_checkpoints": parent_result,
        "dense_controls": dense_controls,
        "aggregate": {
            "shared": summarize(shared_rows, PROJECTOR_TOL),
            "duplicate": summarize(duplicate_rows, PROJECTOR_TOL),
            "parent": summarize(parent_rows, PROJECTOR_TOL),
        },
        "acceptance": acceptance,
        "scientific_limits": [
            "No algorithm changed and no CPU advantage is inferred.",
            "This is a numerical-metric correction on development data, not independent scientific confirmation.",
            "B05 timing equivalence and the absence of a solver speedup remain unchanged.",
            "Landmark-512/5000, originality review, and paper readiness remain open.",
        ],
        "usage": {
            "wall_seconds": time.perf_counter() - wall0,
            "cpu_seconds": time.process_time() - cpu0,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
    }
    path = HERE / "STABLE_METRIC_AUDIT.json"
    path.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"acceptance": acceptance, "same": same_summary, "aggregate": result["aggregate"],
                      "usage": result["usage"], "result_sha256": sha256(path)}, allow_nan=False))


if __name__ == "__main__":
    main()
