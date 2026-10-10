#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
import os
import resource
import tempfile
import time
import zipfile
from pathlib import Path

for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"

import numpy as np
from scipy.linalg import eigh
from scipy.stats import rankdata, spearmanr

INPUT_SHA256 = "d0de6bb598161e85557321a309e9d720cb1c398b722140725e47d8365e3ec68a"
REFERENCE_SHA256 = "b8c4f5278fa58c96c485d6f547acdd927a5cd5153528219ebc1fd6ada4744fa5"
K = 25
BAND_MULTIPLIER = 10.0
ANGLE_TARGET_SIN2 = 1e-6


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def auc(labels, scores):
    labels = np.asarray(labels, dtype=bool)
    scores = np.asarray(scores, dtype=float)
    good = np.isfinite(scores)
    labels, scores = labels[good], scores[good]
    n1, n0 = int(labels.sum()), int((~labels).sum())
    if n1 == 0 or n0 == 0:
        return float("nan"), int(good.sum())
    ranks = rankdata(scores, method="average")
    value = (float(ranks[labels].sum()) - n1 * (n1 + 1) / 2) / (n1 * n0)
    return value, int(good.sum())


def atomic_json(path, obj):
    path = Path(path)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(obj, f, indent=2, allow_nan=False)
            f.write("\n")
            f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)


def atomic_npz(path, arrays):
    path = Path(path)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".npz", dir=path.parent)
    os.close(fd)
    try:
        np.savez_compressed(tmp, **arrays)
        with open(tmp, "rb") as f: os.fsync(f.fileno())
        with np.load(tmp, allow_pickle=False) as z:
            assert sorted(z.files) == sorted(arrays)
            for k, v in arrays.items():
                assert np.array_equal(z[k], v, equal_nan=True)
        with zipfile.ZipFile(tmp) as zf:
            assert zf.testzip() is None
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
    return {"path": path.name, "sha256": sha256(path), "size_bytes": path.stat().st_size}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--reference", required=True)
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()
    outdir = Path(args.output_dir); outdir.mkdir(parents=True, exist_ok=True)
    wall0, cpu0 = time.perf_counter(), time.process_time()
    assert sha256(args.input) == INPUT_SHA256
    assert sha256(args.reference) == REFERENCE_SHA256
    with np.load(args.input, allow_pickle=False) as z:
        A = z["a"].copy(); energy = z["energy"].copy()
    with np.load(args.reference, allow_pickle=False) as z:
        ref = {k: z[k].copy() for k in z.files}
    assert A.shape == (512, 2704)
    n, d = A.shape
    row_gram = A @ A.T
    eig_cache = {}
    q_cache = {}

    def top_eig(t):
        if t not in eig_cache:
            vals, vecs = eigh(row_gram[:t, :t], subset_by_index=(t-K-1, t-1), driver="evr", check_finite=False)
            eig_cache[t] = (np.maximum(vals[::-1], 0.0), vecs[:, ::-1])
        return eig_cache[t]

    def refresh_q(t):
        if t not in q_cache:
            _, _, vh = np.linalg.svd(A[:t], full_matrices=False)
            q_cache[t] = vh[:min(K, t)].T.copy()
        return q_cache[t]

    all_arrays = {}
    summaries = {}
    inequality_violations = 0
    max_lower_violation = 0.0
    max_loss_reconstruction_error = 0.0
    for eta_text in ("0.01", "0.1"):
        eta = float(eta_text)
        suffix = f"eta{eta:g}"
        query = ref[f"classic_delayed_ell50_{suffix}_baseline_queried"]
        update = ref[f"classic_delayed_ell50_{suffix}_baseline_updated"]
        assert np.array_equal(update, ref[f"classic_delayed_ell50_{suffix}_strong_updated"])
        incoming_loss = ref[f"classic_delayed_ell50_{suffix}_incoming_residual"]
        Q = None
        rows = []
        for i in range(n):
            t = i + 1
            if t > K and query[i]:
                assert Q is not None and Q.shape == (d, K)
                vals, left = top_eig(t)
                lam_top, lam_next = vals[:K], float(vals[K])
                lam_k = float(lam_top[-1])
                gap = max(0.0, lam_k - lam_next)
                rho = 0.0 if lam_k == 0.0 else min(1.0, max(0.0, lam_next / lam_k))
                AQ = A[:t] @ Q
                overlap = (left[:, :K].T @ AQ) / np.sqrt(np.maximum(lam_top, np.finfo(float).tiny))[:, None]
                per_top_capture = np.minimum(1.0, np.maximum(0.0, np.sum(overlap * overlap, axis=1)))
                missed = 1.0 - per_top_capture
                r = max(0.0, float(missed.sum()))
                singular = np.clip(np.linalg.svd(overlap, compute_uv=False), 0.0, 1.0)
                worst_sin2 = max(0.0, float(1.0 - singular[-1] ** 2))
                tan0 = math.sqrt(worst_sin2 / max(1.0 - worst_sin2, np.finfo(float).tiny))
                target_tan = math.sqrt(ANGLE_TARGET_SIN2 / (1.0 - ANGLE_TARGET_SIN2))
                if tan0 <= target_tan:
                    work_proxy = 0.0
                elif rho == 0.0:
                    work_proxy = 1.0
                elif rho >= 1.0:
                    work_proxy = float("inf")
                else:
                    work_proxy = float(math.ceil(math.log(tan0 / target_tan) / math.log(1.0 / rho)))
                near = (lam_top - lam_next) <= BAND_MULTIPLIER * max(gap, np.finfo(float).eps * max(1.0, float(vals[0])))
                hard_mass = float(missed[near].sum())
                hard_fraction = 0.0 if r <= 1e-15 else hard_mass / r
                opt = float(ref["opt"][i])
                loss = float(incoming_loss[i])
                calc_loss = max(0.0, float(energy[i] - np.sum(AQ * AQ)))
                loss_err = abs(calc_loss - loss)
                max_loss_reconstruction_error = max(max_loss_reconstruction_error, loss_err)
                tol = 1e-10 * max(1.0, float(energy[i]))
                excess = max(0.0, loss - opt)
                lower = gap * r
                violation = max(0.0, lower - excess - tol)
                max_lower_violation = max(max_lower_violation, violation)
                inequality_violations += int(violation > 0.0)
                rows.append((t, bool(update[i]), rho, 1.0-rho, worst_sin2, hard_mass, hard_fraction,
                             work_proxy, r, excess, excess / max(opt, tol), gap, loss_err))
            if update[i]:
                Q = refresh_q(t)
        names = ["prefix","update","rho","relative_gap","worst_sin2","hard_mass","hard_fraction",
                 "work_proxy","projector_distance","excess","excess_ratio","absolute_gap","loss_reconstruction_error"]
        cols = {name: np.array([row[j] for row in rows], dtype=(bool if name=="update" else int if name=="prefix" else float)) for j,name in enumerate(names)}
        key = eta_text.replace(".", "p")
        for name, arr in cols.items(): all_arrays[f"eta{key}_{name}"] = arr
        features = {
            "rho": cols["rho"],
            "worst_sin2": cols["worst_sin2"],
            "hard_mass": cols["hard_mass"],
            "hard_fraction": cols["hard_fraction"],
            "work_proxy": cols["work_proxy"],
            "positive_control_excess_ratio": cols["excess_ratio"],
        }
        metrics = {}
        for name, score in features.items():
            av, coverage = auc(cols["update"], score)
            finite = np.isfinite(score) & np.isfinite(cols["excess_ratio"])
            sp = spearmanr(score[finite], cols["excess_ratio"][finite]).statistic if finite.sum() > 2 else float("nan")
            metrics[name] = {
                "auc_update_vs_query_no_update": float(av),
                "finite_coverage": int(coverage),
                "spearman_with_excess_ratio": float(sp),
                "median_update": float(np.median(score[cols["update"] & np.isfinite(score)])),
                "median_no_update": float(np.median(score[(~cols["update"]) & np.isfinite(score)])),
            }
        summaries[eta_text] = {
            "query_states_after_growth": len(rows),
            "update_states": int(cols["update"].sum()),
            "query_without_update_states": int((~cols["update"]).sum()),
            "features": metrics,
            "relative_gap_quantiles": [float(x) for x in np.quantile(cols["relative_gap"], [0,0.25,0.5,0.75,1])],
            "work_proxy_quantiles_finite": [float(x) for x in np.quantile(cols["work_proxy"][np.isfinite(cols["work_proxy"])], [0,0.25,0.5,0.75,1])],
        }
    artifact = atomic_npz(outdir / "B14_GAP_ANGLE_RAW.npz", all_arrays)
    candidate_names = ["rho", "worst_sin2", "hard_mass", "hard_fraction", "work_proxy"]
    qualified = [name for name in candidate_names if all(summaries[e]["features"][name]["auc_update_vs_query_no_update"] >= 0.75 for e in ("0.01","0.1"))]
    result = {
        "study": "B14-native512-gap-angle-development-diagnostic",
        "input_sha256": INPUT_SHA256,
        "reference_sha256": REFERENCE_SHA256,
        "rows": n,
        "dimension": d,
        "rank": K,
        "band_multiplier_frozen": BAND_MULTIPLIER,
        "angle_target_sin2_frozen": ANGLE_TARGET_SIN2,
        "summaries": summaries,
        "semantic_checks": {
            "max_loss_reconstruction_error": max_loss_reconstruction_error,
            "loss_tolerance_rule": "1e-10*max(1,energy)",
            "gap_times_distance_violations": inequality_violations,
            "max_gap_times_distance_violation_beyond_tolerance": max_lower_violation,
            "unique_eigensystems": len(eig_cache),
            "unique_full_svd_refresh_endpoints": len(q_cache),
        },
        "development_discriminative_features": qualified,
        "hypothesis_pass": bool(qualified),
        "claim_scope": "same-prefix native512 dependent development diagnostic; no new method, causal proof, independent confirmation, native5000 claim, or paper gate",
        "raw_artifact": artifact,
        "usage": {
            "wall_seconds": time.perf_counter()-wall0,
            "cpu_seconds": time.process_time()-cpu0,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "numeric_threads": 1,
        },
    }
    atomic_json(outdir / "B14_GAP_ANGLE_RESULT.json", result)
    print(json.dumps(result, allow_nan=False))


if __name__ == "__main__":
    main()
