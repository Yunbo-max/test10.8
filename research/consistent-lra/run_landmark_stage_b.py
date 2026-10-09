"""Generated, unexecuted complete Landmark existing-baseline scorer candidate.

No Stage-B command is admitted: authentic native evaluator authority, independent
source/semantic review, near-zero qualification and a fresh plan are required.
This code implements the accepted project repair design; it is not official.
No novel method, discovery batch, confirmation or result-paper pass is implied.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import sys
import time

import numpy as np
import scipy
from scipy.linalg import eigh
from calibrate_landmark_reference import EXPECTED, load_first_5000, source_identity
from landmark_stage_a_v2 import (K, N, ORACLE_PREFIXES, THREAD_NAMES, GramRefresh,
                                arm_inventory, checked_nonnegative, sha256,
                                CALIBRATION_SHA256)
from run_lowdim_baseline_matrix import (deterministic_archive, fsync_directory,
                                       publish_no_replace)

STAGE_A_SUMMARY_SHA256 = "a0523b88fbc96adae1f035ce9c9974a0d3ae9fe97f3e7ff782c363e6177f6ae7"
STAGE_A_REVIEW_SHA256 = "65d566101933c540a6f1e879418f6c1f72f7b186a20bfe4f9c8851bdf015d714"


def publish_json(path, value):
    partial = path.with_name(path.name + ".partial")
    with partial.open("x") as stream:
        stream.write(json.dumps(value, sort_keys=True, allow_nan=False, indent=2) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    expected = sha256(partial)
    publish_no_replace(partial, path)
    if sha256(path) != expected:
        raise ValueError("JSON publication mismatch")
    return {"path": path.name, "sha256": expected, "bytes": path.stat().st_size}


class RawRows:
    def __init__(self, path, arm):
        self.path, self.arm = path, arm
        self.partial = path.with_name(path.name + ".partial")
        self.stream = self.partial.open("x")
        self.rows, self.digest = 0, hashlib.sha256()

    def write(self, value):
        if value["prefix"] != self.rows + 1 or value["arm"] != self.arm:
            raise ValueError("nonsequential raw inventory")
        data = json.dumps(value, allow_nan=False, separators=(",", ":")) + "\n"
        if self.stream.write(data) != len(data):
            raise IOError("short raw write")
        self.digest.update(data.encode())
        self.rows += 1

    def finish(self):
        self.stream.flush()
        os.fsync(self.stream.fileno())
        self.stream.close()
        if self.rows != N or sha256(self.partial) != self.digest.hexdigest():
            raise ValueError("raw count/hash mismatch")
        count = 0
        with self.partial.open() as stream:
            for count, line in enumerate(stream, 1):
                record = json.loads(line)
                if not line.endswith("\n") or record["prefix"] != count or record["arm"] != self.arm:
                    raise ValueError("raw semantic readback failure")
        if count != N:
            raise ValueError("raw denominator mismatch")
        expected = self.digest.hexdigest()
        publish_no_replace(self.partial, self.path)
        if sha256(self.path) != expected:
            raise ValueError("raw publication mismatch")
        return {"path": self.path.name, "sha256": expected,
                "bytes": self.path.stat().st_size, "rows": self.rows}

    def close_failed(self):
        if not self.stream.closed:
            self.stream.flush()
            os.fsync(self.stream.fileno())
            self.stream.close()


def new_slice(first):
    return {"first_prefix": first, "last_prefix": N, "prefix_count": 0,
            "ratio_denominator": 0, "ratio_missing_count": 0,
            "near_zero_positive_loss_violations": 0, "ratio_sum": 0.0,
            "maximum_defined_ratio": None, "loss_sum": 0.0, "opt_sum": 0.0,
            "excess_sum": 0.0, "energy_normalized_excess_sum": 0.0}


def add_slice(stat, row):
    stat["prefix_count"] += 1
    stat["loss_sum"] += row["loss"]
    stat["opt_sum"] += row["opt"]
    stat["excess_sum"] += row["additive_excess"]
    stat["energy_normalized_excess_sum"] += row["energy_normalized_excess"]
    ratio = row["ratio"]
    if ratio is None:
        stat["ratio_missing_count"] += 1
        stat["near_zero_positive_loss_violations"] += int(row["near_zero_positive_loss_violation"])
    else:
        stat["ratio_denominator"] += 1
        stat["ratio_sum"] += ratio
        stat["maximum_defined_ratio"] = ratio if stat["maximum_defined_ratio"] is None else max(ratio, stat["maximum_defined_ratio"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--landmark", required=True)
    parser.add_argument("--calibration", required=True)
    parser.add_argument("--stage-a-summary", required=True)
    parser.add_argument("--stage-a-review", required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    args = parser.parse_args()
    threads = {n: os.environ.get(n) for n in THREAD_NAMES}
    if any(v != "1" for v in threads.values()):
        raise ValueError("one-thread environment must be set before import")
    source = Path(args.landmark)
    if source_identity(source) != (EXPECTED["bytes"], EXPECTED["git_blob"], EXPECTED["sha256"]):
        raise ValueError("native Landmark bytes mismatch")
    for path, expected in [(args.calibration, CALIBRATION_SHA256),
                           (args.stage_a_summary, STAGE_A_SUMMARY_SHA256),
                           (args.stage_a_review, STAGE_A_REVIEW_SHA256)]:
        if sha256(path) != expected:
            raise ValueError("accepted dependency byte mismatch")
    stage_a = json.loads(Path(args.stage_a_summary).read_text())
    if not stage_a["stage_a_complete"] or not stage_a["all_frozen_identity_checks_passed"]:
        raise ValueError("finite Stage-A dependency incomplete")
    start = time.perf_counter()
    before = resource.getrusage(resource.RUSAGE_SELF)
    matrix, active = load_first_5000(source)
    prior = json.loads(Path(args.calibration).read_text())
    if [c + 1 for c in active] != prior["source"]["represented_columns_one_based"]:
        raise ValueError("fixed active map mismatch")
    if matrix.shape != (N, 259):
        raise ValueError("fixed stream shape mismatch")
    out = args.output_directory
    out.parent.mkdir(parents=True, exist_ok=True)
    out.mkdir(exist_ok=False)
    fsync_directory(out.parent)
    arms = arm_inventory(matrix)
    raw = {name: RawRows(out / (name + ".jsonl"), name) for name, _ in arms}
    previous = {name: np.empty((0, matrix.shape[1])) for name, _ in arms}
    aggregates = {name: {"full": new_slice(1), "project_150_inclusive": new_slice(150),
                         "cumulative_recourse": 0.0, "steady_recourse": 0.0,
                         "update_seconds": 0.0, "scoring_seconds": 0.0,
                         "maximum_update_seconds": 0.0, "refreshes": 0,
                         "direct_loss_fallbacks": 0, "maximum_orthogonality_error": 0.0}
                  for name, _ in arms}
    gram = np.zeros((matrix.shape[1], matrix.shape[1]))
    energy = energy_seconds = reference_seconds = serialization_seconds = 0.0
    direct_opt_fallbacks = 0
    try:
        for t, input_row in enumerate(matrix, 1):
            tick = time.perf_counter()
            gram += np.outer(input_row, input_row)
            energy += float(input_row @ input_row)
            energy_time = time.perf_counter() - tick
            energy_seconds += energy_time
            tolerance = 1e-10 * max(1.0, energy)
            band = 10 * tolerance
            rank = min(K, t)
            tick = time.perf_counter()
            top = eigh(gram.copy(), subset_by_index=[len(gram) - rank, len(gram) - 1],
                       eigvals_only=True, driver="evr", check_finite=False)
            top_sum = float(np.sum(top))
            raw_opt = float(energy - top_sum)
            gram_opt = checked_nonnegative(raw_opt, tolerance, "Gram OPT")
            opt_fallback = gram_opt <= band
            oracle = t in ORACLE_PREFIXES
            direct_opt = None
            if opt_fallback or oracle:
                singular = np.linalg.svd(matrix[:t], full_matrices=False, compute_uv=False)
                direct_opt = float(np.sum(singular[rank:] ** 2))
                if not np.isfinite(direct_opt) or direct_opt < 0:
                    raise ValueError("invalid direct OPT")
                if abs(raw_opt - direct_opt) > tolerance:
                    raise ValueError("Gram/direct OPT disagreement")
            opt = direct_opt if opt_fallback else gram_opt
            near_zero = opt <= tolerance
            direct_opt_fallbacks += int(opt_fallback)
            reference_time = time.perf_counter() - tick
            reference_seconds += reference_time
            for name, arm in arms:
                agg = aggregates[name]
                tick = time.perf_counter()
                if isinstance(arm, GramRefresh):
                    q, updated, warmup = arm.update(t)
                else:
                    q, updated, warmup = arm.update(t, None)
                update_time = time.perf_counter() - tick
                tick = time.perf_counter()
                prev = previous[name]
                orth = float(np.linalg.norm(q @ q.T - np.eye(rank), ord="fro"))
                if q.shape != (rank, matrix.shape[1]) or not np.isfinite(q).all() or orth > 1e-10 * max(1, rank):
                    raise ValueError("basis rank/finite/orthogonality failure")
                raw_loss = float(energy - np.trace(q @ gram @ q.T))
                gram_loss = checked_nonnegative(raw_loss, tolerance, "Gram loss")
                loss_fallback = near_zero or gram_loss <= band
                direct_loss = None
                if loss_fallback or oracle:
                    residual = matrix[:t] - (matrix[:t] @ q.T) @ q
                    direct_loss = float(np.sum(residual ** 2))
                    if not np.isfinite(direct_loss) or direct_loss < 0:
                        raise ValueError("invalid direct residual")
                    if abs(raw_loss - direct_loss) > tolerance:
                        raise ValueError("Gram/direct loss disagreement")
                loss = direct_loss if loss_fallback else gram_loss
                raw_rec = float(rank + len(prev) - 2 * np.sum((q @ prev.T) ** 2))
                rec_tol = 1e-10 * max(1, rank + len(prev))
                rec = checked_nonnegative(raw_rec, rec_tol, "projector recourse")
                direct_rec = None
                if oracle:
                    direct_rec = float(np.sum((q.T @ q - prev.T @ prev) ** 2))
                    if abs(raw_rec - direct_rec) > rec_tol:
                        raise ValueError("overlap/direct recourse disagreement")
                increment = 0.0 if t == 1 else rec
                agg["cumulative_recourse"] += increment
                agg["steady_recourse"] += increment if t > K else 0.0
                ratio = None if near_zero else loss / opt
                excess = loss - opt
                row = {"prefix": t, "sample_id": f"landmark:row:{t}", "arm": name,
                       "rank": rank, "previous_rank": len(prev), "previous_prefix": t - 1,
                       "updated": updated, "warmup": warmup, "energy": energy,
                       "top_eigenvalue_sum": top_sum, "tolerance": tolerance,
                       "uncertainty_band": band, "raw_gram_opt": raw_opt,
                       "gram_opt": gram_opt, "direct_opt": direct_opt, "opt": opt,
                       "opt_source": "direct_svd_fallback" if opt_fallback else "qualified_gram",
                       "raw_gram_loss": raw_loss, "gram_loss": gram_loss,
                       "direct_loss": direct_loss, "loss": loss,
                       "loss_source": "direct_residual_fallback" if loss_fallback else "qualified_gram",
                       "ratio": ratio, "near_zero_opt": near_zero,
                       "near_zero_positive_loss_violation": near_zero and loss > tolerance,
                       "additive_excess": excess,
                       "energy_normalized_excess": excess / max(1.0, energy),
                       "raw_recourse": raw_rec, "recourse": rec, "recourse_tolerance": rec_tol,
                       "direct_recourse_oracle": direct_rec, "primary_increment": increment,
                       "initialization_from_zero": rec if t == 1 else None,
                       "cumulative_recourse": agg["cumulative_recourse"],
                       "steady_recourse": agg["steady_recourse"],
                       "orthogonality_error": orth, "update_seconds": update_time,
                       "shared_reference_seconds": reference_time,
                       "shared_energy_maintenance_seconds": energy_time,
                       "selected_oracle": oracle, "direct_opt_fallback": opt_fallback,
                       "direct_loss_fallback": loss_fallback}
                if oracle or opt_fallback or loss_fallback:
                    row["retained_fallback_or_oracle_inputs"] = {
                        "source_sha256": EXPECTED["sha256"], "prefix": t,
                        "basis": q.tolist(), "previous_basis": prev.tolist(),
                        "active_map_ref": "manifest.source.represented_columns_one_based"}
                previous[name] = q.copy()
                scoring_time = time.perf_counter() - tick
                row["scoring_seconds"] = scoring_time
                agg["update_seconds"] += update_time
                agg["scoring_seconds"] += scoring_time
                agg["maximum_update_seconds"] = max(agg["maximum_update_seconds"], update_time)
                agg["refreshes"] += int(updated)
                agg["direct_loss_fallbacks"] += int(loss_fallback)
                agg["maximum_orthogonality_error"] = max(agg["maximum_orthogonality_error"], orth)
                add_slice(agg["full"], row)
                if t >= 150:
                    add_slice(agg["project_150_inclusive"], row)
                tick = time.perf_counter()
                raw[name].write(row)
                serialization_seconds += time.perf_counter() - tick
            if t % 500 == 0:
                print(json.dumps({"processed_prefix": t, "scope": "project_scoring_only_no_official_parity"}), flush=True)
        publication_start = time.perf_counter()
        members = []
        for name, _ in arms:
            agg = aggregates[name]
            for slice_name, expected in [("full", N), ("project_150_inclusive", 4851)]:
                stat = agg[slice_name]
                if stat["prefix_count"] != expected or stat["ratio_denominator"] + stat["ratio_missing_count"] != expected:
                    raise ValueError("slice denominator mismatch")
                stat["mean_defined_ratio"] = stat["ratio_sum"] / stat["ratio_denominator"] if stat["ratio_denominator"] else None
                stat["is_paper_table1_denominator"] = False
            raw_ref = raw[name].finish()
            summary = {"arm": name, "strong_comparator": name != "author-fd-ell50",
                       "aggregates": agg, "raw": raw_ref, "k": K, "n": N,
                       "scope": "project_repair_developmental_only", "confirmation": False,
                       "official_scorer_parity": False, "scientific_gate_advanced": False,
                       "performance_claim_eligible": False}
            summary_ref = publish_json(out / (name + ".summary.json"), summary)
            members += [raw_ref, summary_ref]
        archive = out / "landmark-stage-b.tar.gz"
        archive_sha = deterministic_archive(archive, [(out / x["path"], x["path"]) for x in members])
        if sha256(archive) != archive_sha:
            raise ValueError("archive publication mismatch")
        outputs = members + [{"path": archive.name, "sha256": archive_sha, "bytes": archive.stat().st_size}]
        after = resource.getrusage(resource.RUSAGE_SELF)
        manifest = {"format": "landmark-project-stage-b-v1", "status": "completed_project_packet_only",
                    "source": {"sha256": EXPECTED["sha256"], "git_blob": EXPECTED["git_blob"],
                               "upstream_commit": "d607c4f6467216c470d1e3b93989d44d5fcdec97",
                               "represented_columns_one_based": [c + 1 for c in active],
                               "matrix_sha256": hashlib.sha256(matrix.astype("<f8").tobytes()).hexdigest(),
                               "preprocessing": "first5000 released rows; zero-column restriction only"},
                    "k": K, "n": N, "arms": [name for name, _ in arms],
                    "raw_rows": N * 13, "direct_opt_fallbacks": direct_opt_fallbacks,
                    "outputs": outputs, "manifest_path": "landmark-stage-b.manifest.json",
                    "successful_final_inventory_count_including_this_manifest": 28,
                    "usage": {"pipeline_before_manifest_seconds": time.perf_counter() - start,
                              "process_cpu_seconds": after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime,
                              "maximum_rss_kib": after.ru_maxrss,
                              "shared_reference_seconds": reference_seconds,
                              "shared_energy_maintenance_seconds": energy_seconds,
                              "serialization_seconds": serialization_seconds,
                              "raw_summary_archive_publication_seconds": time.perf_counter() - publication_start,
                              "rss_semantics": "process high-water, not incremental arm memory"},
                    "environment": {"python": platform.python_version(), "numpy": np.__version__,
                                    "scipy": scipy.__version__, "thread_env": threads,
                                    "actual_numerical_thread_count_observed": None},
                    "argv": sys.argv, "tie_policy": "pinned_scipy_evr_sign_canonical_FD_numpy_svd_no_recourse_theorem",
                    "recourse_convention": "primary excludesinitialization;steady excludesprefixes1..25",
                    "native_scientific_authority_qualified": False, "official_scorer_parity": False,
                    "confirmation": False, "scientific_gate_advanced": False,
                    "performance_claim_eligible": False}
        final_manifest = publish_json(out / manifest["manifest_path"], manifest)
        for x in outputs + [final_manifest]:
            if sha256(out / x["path"]) != x["sha256"]:
                raise ValueError("final packet mutated after manifest publication")
        print(json.dumps({"manifest": str(out / manifest["manifest_path"]),
                          "inventory": 28, "scientific_gate_advanced": False}), flush=True)
    finally:
        for writer in raw.values():
            writer.close_failed()


if __name__ == "__main__":
    main()
