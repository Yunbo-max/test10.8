"""Native Landmark numerical-identity qualification and bounded update calibration.

Version2 output-container mitigation; root cause of v1 gzip loss is unknown.
No new algorithm or scientific performance verdict. Execute only through the
reviewed pinned CPU harness. Calibration is the first 150 native prefixes;
qualification uses all 5000 transitions but computes only prescribed identity
oracles, never a 5000-prefix loss/recourse performance matrix.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import platform
import resource
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.linalg import eigh

from calibrate_landmark_reference import EXPECTED, load_first_5000, source_identity
from native_baselines import FrequentDirectionsBaseline, AuthorAugmentedFDDiagnostic
from run_lowdim_baseline_matrix import fsync_directory, fsync_file, publish_no_replace

K = 25
N = 5000
ORACLE_PREFIXES = list(range(1, 26)) + [50, 100, 150, 250, 500, 1000, 2000, 3000, 4000, 5000]
THREAD_NAMES = ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
                "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")
CALIBRATION_PATH = ("runs/attempts/landmark-reference-calibration-01/"
                    "landmark-reference-cost-a1-177b60cdd7444745b59898cc4731e74a/"
                    "workspace/evidence/calibration/landmark-reference-calibration.json")
CALIBRATION_SHA256 = "25887ba1e2a81776a87a88ab0f78cfc0134a408fa3642686d039d04ba5f9df90"


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def checked_nonnegative(value, tolerance, description):
    if not np.isfinite(value) or value < -tolerance:
        raise ValueError(f"invalid {description}: {value}, allowance {tolerance}")
    return max(0.0, value)


def basis_from_gram(gram, energy, rank):
    if energy == 0:
        return np.eye(len(gram), dtype=np.float64)[:rank].copy()
    _, vectors = eigh(gram.copy(), subset_by_index=[len(gram) - rank, len(gram) - 1],
                      eigvals_only=False, driver="evr", check_finite=False)
    q = vectors[:, ::-1].T.copy()
    for row in q:
        pivot = int(np.argmax(np.abs(row)))
        if row[pivot] < 0:
            row *= -1
    return q


class GramRefresh:
    """Each refresh comparator pays for its own Gram, energy and copy state."""
    def __init__(self, matrix, mode, parameter=None):
        self.matrix, self.mode, self.parameter = matrix, mode, parameter
        self.gram = np.zeros((matrix.shape[1], matrix.shape[1]), dtype=np.float64)
        self.energy = self.refresh_energy = 0.0
        self.q = np.empty((0, matrix.shape[1]), dtype=np.float64)

    def update(self, t):
        row = self.matrix[t - 1]
        self.gram += np.outer(row, row)
        self.energy += float(row @ row)
        # This copy is paid for at every prefix, including a no-refresh prefix.
        private_copy = self.gram.copy()
        refresh = t <= K or self.mode == "fresh"
        if self.mode == "algorithm4":
            refresh = refresh or self.energy >= self.parameter * self.refresh_energy
        elif self.mode == "periodic":
            refresh = refresh or (t > K and (t - K) % self.parameter == 0)
        if refresh:
            self.q = basis_from_gram(private_copy, self.energy, min(K, t))
            self.refresh_energy = self.energy
        return self.q.copy(), refresh, t <= K


def arm_inventory(matrix):
    arms = [(f"algorithm4-c{c}", GramRefresh(matrix, "algorithm4", c))
            for c in (1.1, 2.0, 2.5, 5.0, 10.0, 100.0)]
    arms += [("fresh", GramRefresh(matrix, "fresh")), ("fixed", GramRefresh(matrix, "fixed")),
             ("periodic-10", GramRefresh(matrix, "periodic", 10)),
             ("periodic-100", GramRefresh(matrix, "periodic", 100)),
             ("fd-ell50", FrequentDirectionsBaseline(matrix, K, 50)),
             ("fd-ell100", FrequentDirectionsBaseline(matrix, K, 100)),
             ("author-fd-ell50", AuthorAugmentedFDDiagnostic(matrix, K, 50))]
    if len(arms) != 13:
        raise ValueError("incorrect frozen inventory")
    return arms


class AuditedRaw:
    """Reject short writes; retain physical identities without changing metrics."""
    def __init__(self, path):
        self.stream = path.open("xb")
        self.requested_bytes = self.returned_bytes = self.write_calls = 0
        self.initial = self.identity()

    def identity(self):
        st = os.fstat(self.stream.fileno())
        return {"device": st.st_dev, "inode": st.st_ino, "bytes": st.st_size}

    def write(self, data):
        size = len(data)
        count = self.stream.write(data)
        self.write_calls += 1
        self.requested_bytes += size
        if count is not None:
            self.returned_bytes += count
        if count != size:
            raise IOError(f"short compressed write: requested {size}, returned {count}")
        return count

    def flush(self):
        self.stream.flush()

    def tell(self):
        return self.stream.tell()


class RetainedGzip:
    def __init__(self, output):
        self.output = Path(output)
        self.partial = self.output.with_name(self.output.name + ".partial")
        if self.output.exists():
            raise FileExistsError(self.output)
        self.raw = AuditedRaw(self.partial)
        self.zipped = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.rows = 0
        self.plain_bytes = 0
        self.plain_hash = hashlib.sha256()

    def write(self, row):
        data = (json.dumps(row, allow_nan=False, separators=(",", ":")) + "\n").encode()
        written = self.zipped.write(data)
        if written != len(data):
            raise IOError("short uncompressed gzip write")
        self.plain_hash.update(data)
        self.plain_bytes += len(data)
        self.rows += 1

    def publish(self):
        before_finalize = self.raw.identity()
        self.zipped.close()
        self.raw.flush()
        os.fsync(self.raw.stream.fileno())
        after_finalize = self.raw.identity()
        self.raw.stream.close()
        stat = self.partial.stat()
        if (stat.st_dev, stat.st_ino, stat.st_size) != (after_finalize["device"], after_finalize["inode"], after_finalize["bytes"]):
            raise ValueError("compressed file identity changed after close")
        if stat.st_size != self.raw.returned_bytes:
            raise ValueError("compressed file size disagrees with returned write bytes")
        expected = sha256(self.partial)
        digest = hashlib.sha256()
        rows = plain_bytes = 0
        with gzip.open(self.partial, "rb") as stream:
            for line in stream:
                if not line.endswith(b"\n"):
                    raise ValueError("incomplete JSON line")
                json.loads(line)
                digest.update(line)
                rows += 1
                plain_bytes += len(line)
        if digest.hexdigest() != self.plain_hash.hexdigest() or rows != self.rows or plain_bytes != self.plain_bytes:
            raise ValueError("gzip content integrity failure")
        publish_no_replace(self.partial, self.output)
        if sha256(self.output) != expected:
            raise ValueError("published gzip hash mismatch")
        return {"path": self.output.name, "sha256": expected, "rows": rows,
                "uncompressed_sha256": digest.hexdigest(), "bytes": self.output.stat().st_size,
                "plain_bytes": plain_bytes,
                "write_audit": {"calls": self.raw.write_calls, "requested_bytes": self.raw.requested_bytes,
                                "returned_bytes": self.raw.returned_bytes, "initial": self.raw.initial,
                                "before_finalize": before_finalize, "after_finalize": after_finalize,
                                "after_close": {"device": stat.st_dev, "inode": stat.st_ino, "bytes": stat.st_size}}}


class PrefixOracleGzip:
    """Finalize one immutable 13-record member at each selected prefix."""
    def __init__(self, output, expected_prefixes):
        self.output = output.with_name(output.stem + ".manifest.json")
        self.base = output
        self.expected_prefixes = expected_prefixes
        self.members = []
        self.current = None
        self.prefix = None
        self.rows = 0
        if self.output.exists() or self.output.with_name(self.output.name + ".partial").exists():
            raise FileExistsError(self.output)

    def finish_current(self):
        if self.current is not None:
            if self.current.rows != 13:
                raise ValueError("oracle member denominator mismatch")
            self.members.append({"prefix": self.prefix, **self.current.publish()})
            self.current = None

    def write(self, row):
        prefix = row["prefix"]
        if prefix != self.prefix:
            self.finish_current()
            if prefix not in self.expected_prefixes or (self.prefix is not None and prefix <= self.prefix):
                raise ValueError("unexpected or repeated oracle prefix")
            self.prefix = prefix
            name = self.base.with_name(self.base.stem + f".prefix-{prefix:05d}.gz")
            self.current = RetainedGzip(name)
        self.current.write(row)
        self.rows += 1

    def publish(self):
        self.finish_current()
        if [member["prefix"] for member in self.members] != self.expected_prefixes or self.rows != 13 * len(self.expected_prefixes):
            raise ValueError("oracle inventory mismatch")
        result = {"format": "landmark-oracle-member-manifest-v2", "rows": self.rows,
                  "expected_prefixes": self.expected_prefixes, "members": self.members,
                  "root_cause_repaired": False, "scope": "output container mitigation only"}
        partial = self.output.with_name(self.output.name + ".partial")
        with partial.open("x") as stream:
            stream.write(json.dumps(result, allow_nan=False, indent=2) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        expected = sha256(partial)
        publish_no_replace(partial, self.output)
        if sha256(self.output) != expected or any(sha256(self.output.parent / m["path"]) != m["sha256"] for m in self.members):
            raise ValueError("oracle member final integrity failure")
        return {"path": self.output.name, "sha256": expected, "rows": self.rows,
                "bytes": self.output.stat().st_size, "member_count": len(self.members)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--landmark", required=True)
    parser.add_argument("--calibration", required=True)
    parser.add_argument("--mode", choices=["calibration", "qualification"], required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    threads = {name: os.environ.get(name) for name in THREAD_NAMES}
    if any(value != "1" for value in threads.values()):
        raise ValueError("pre-import one-thread contract missing")
    start = time.perf_counter()
    before = resource.getrusage(resource.RUSAGE_SELF)
    source = Path(args.landmark)
    if source_identity(source) != (EXPECTED["bytes"], EXPECTED["git_blob"], EXPECTED["sha256"]):
        raise ValueError("source mismatch")
    prior_path = Path(args.calibration)
    if sha256(prior_path) != CALIBRATION_SHA256:
        raise ValueError("accepted calibration byte mismatch")
    prior = json.loads(prior_path.read_text())
    matrix, active = load_first_5000(source)
    if [column + 1 for column in active] != prior["source"]["represented_columns_one_based"]:
        raise ValueError("accepted active-column map mismatch")
    n = 150 if args.mode == "calibration" else N
    prefixes = [t for t in ORACLE_PREFIXES if t <= n]
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() or output.with_name(output.name + ".partial").exists():
        raise FileExistsError(output)
    oracle_output = output.with_name(output.stem + ".oracles.jsonl.gz")
    timing_output = output.with_name(output.stem + ".timings.jsonl.gz")
    oracles = PrefixOracleGzip(oracle_output, prefixes)
    timings = RetainedGzip(timing_output)
    arms = arm_inventory(matrix)
    previous = {name: np.empty((0, matrix.shape[1])) for name, _ in arms}
    totals = {name: {"update_seconds": 0.0, "oracle_seconds": 0.0,
                     "maximum_update_seconds": 0.0, "refreshes": 0} for name, _ in arms}
    gram = np.zeros((matrix.shape[1], matrix.shape[1]))
    energy = reference_seconds = oracle_seconds = serialization_seconds = 0.0
    maxima = {"opt_absolute_error": 0.0, "loss_absolute_error": 0.0,
              "recourse_absolute_error": 0.0, "orthogonality_error": 0.0}
    prefix_reference = []
    for t, row in enumerate(matrix[:n], start=1):
        tick = time.perf_counter()
        gram += np.outer(row, row)
        energy += float(row @ row)
        reference_seconds += time.perf_counter() - tick
        tolerance = 1e-10 * max(1.0, energy)
        reference = None
        if t in prefixes:
            tick = time.perf_counter()
            eigenvalues = eigh(gram.copy(), subset_by_index=[len(gram) - min(K, t), len(gram) - 1],
                               eigvals_only=True, driver="evr", check_finite=False)
            raw_opt = float(energy - np.sum(eigenvalues))
            gram_opt = checked_nonnegative(raw_opt, tolerance, "Gram OPT")
            singular = np.linalg.svd(matrix[:t], full_matrices=False, compute_uv=False)
            direct_opt = float(np.sum(singular[min(K, t):] ** 2))
            error = abs(raw_opt - direct_opt)
            if error > tolerance:
                raise ValueError(f"OPT mismatch at prefix {t}")
            maxima["opt_absolute_error"] = max(maxima["opt_absolute_error"], error)
            reference = {"prefix": t, "sample_id": f"landmark:row:{t}", "energy": energy,
                         "raw_gram_opt": raw_opt, "gram_opt": gram_opt, "direct_svd_opt": direct_opt,
                         "tolerance": tolerance, "opt_absolute_error": error,
                         "reference_seconds": time.perf_counter() - tick}
            reference_seconds += reference["reference_seconds"]
            prefix_reference.append(reference)
        for name, arm in arms:
            tick = time.perf_counter()
            if isinstance(arm, GramRefresh):
                q, updated, warmup = arm.update(t)
            else:
                # Existing FD API ignores energy; it receives no evaluator state.
                q, updated, warmup = arm.update(t, None)
            update_seconds = time.perf_counter() - tick
            totals[name]["update_seconds"] += update_seconds
            totals[name]["maximum_update_seconds"] = max(totals[name]["maximum_update_seconds"], update_seconds)
            totals[name]["refreshes"] += int(updated)
            rank, prev = len(q), previous[name]
            orthogonality = float(np.linalg.norm(q @ q.T - np.eye(rank), ord="fro"))
            if rank != min(K, t) or not np.isfinite(q).all() or orthogonality > 1e-10 * max(1, rank):
                raise ValueError(f"basis invalid {name} prefix {t}")
            maxima["orthogonality_error"] = max(maxima["orthogonality_error"], orthogonality)
            if reference is not None:
                tick = time.perf_counter()
                raw_loss = float(energy - np.trace(q @ gram @ q.T))
                loss = checked_nonnegative(raw_loss, tolerance, "Gram loss")
                residual = matrix[:t] - (matrix[:t] @ q.T) @ q
                direct_loss = float(np.sum(residual ** 2))
                raw_recourse = float(rank + len(prev) - 2 * np.sum((q @ prev.T) ** 2))
                recourse_tol = 1e-10 * max(1, rank + len(prev))
                overlap_recourse = checked_nonnegative(raw_recourse, recourse_tol, "overlap recourse")
                direct_recourse = float(np.sum((q.T @ q - prev.T @ prev) ** 2))
                loss_error, recourse_error = abs(raw_loss - direct_loss), abs(raw_recourse - direct_recourse)
                if loss_error > tolerance or recourse_error > recourse_tol:
                    raise ValueError(f"oracle mismatch {name} prefix {t}")
                maxima["loss_absolute_error"] = max(maxima["loss_absolute_error"], loss_error)
                maxima["recourse_absolute_error"] = max(maxima["recourse_absolute_error"], recourse_error)
                elapsed = time.perf_counter() - tick
                totals[name]["oracle_seconds"] += elapsed
                oracle_seconds += elapsed
                observation = {**reference, "arm": name, "rank": rank, "previous_rank": len(prev),
                               "previous_prefix": t - 1, "basis": q.tolist(), "previous_basis": prev.tolist(),
                               "updated": updated, "warmup": warmup, "raw_gram_loss": raw_loss,
                               "gram_loss": loss, "direct_loss": direct_loss, "loss_absolute_error": loss_error,
                               "overlap_recourse_raw": raw_recourse, "overlap_recourse": overlap_recourse,
                               "direct_recourse": direct_recourse, "recourse_absolute_error": recourse_error,
                               "recourse_tolerance": recourse_tol, "orthogonality_error": orthogonality,
                               "initialization_from_zero_diagnostic": t == 1,
                               "primary_increment": 0.0 if t == 1 else overlap_recourse,
                               "oracle_seconds": elapsed, "update_seconds": update_seconds}
                tick = time.perf_counter()
                oracles.write(observation)
                serialization_seconds += time.perf_counter() - tick
            tick = time.perf_counter()
            timings.write({"prefix": t, "arm": name, "rank": rank, "updated": updated,
                           "warmup": warmup, "update_seconds": update_seconds,
                           "orthogonality_error": orthogonality, "is_oracle_prefix": reference is not None})
            serialization_seconds += time.perf_counter() - tick
            previous[name] = q.copy()
        if t % 500 == 0:
            print(json.dumps({"processed_prefix": t, "mode": args.mode,
                              "elapsed_seconds": time.perf_counter() - start}), flush=True)
    if oracles.rows != len(prefixes) * 13 or timings.rows != n * 13:
        raise ValueError("incomplete denominators")
    outputs = [oracles.publish(), timings.publish()]
    after = resource.getrusage(resource.RUSAGE_SELF)
    result = {"format": "landmark-stage-a-identity-v2", "mode": args.mode,
              "scope": "native numerical identity and bounded update cost only",
              "source": {"upstream": "samsonzhou/consistent-LRA@d607c4f6467216c470d1e3b93989d44d5fcdec97",
                         "sha256": EXPECTED["sha256"], "git_blob": EXPECTED["git_blob"],
                         "prefix_rows_loaded": N, "prefixes_processed": n, "k": K,
                         "represented_columns_one_based": [c + 1 for c in active],
                         "matrix_sha256": hashlib.sha256(matrix.astype("<f8").tobytes()).hexdigest(),
                         "preprocessing": "none; zero columns restricted with accepted fixed active map"},
              "oracle_prefixes": prefixes, "oracle_rows": len(prefixes) * 13,
              "timing_rows": n * 13, "arms": [name for name, _ in arms], "maxima": maxima,
              "references": prefix_reference, "arm_costs": totals, "outputs": outputs,
              "usage": {"process_cpu_seconds": after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime,
                        "pipeline_seconds_before_summary_publication": time.perf_counter() - start,
                        "maximum_rss_kib": after.ru_maxrss, "shared_reference_seconds": reference_seconds,
                        "identity_oracle_seconds": oracle_seconds, "serialization_seconds": serialization_seconds},
              "environment": {"python": platform.python_version(), "numpy": np.__version__,
                              "scipy": scipy.__version__, "thread_environment": threads,
                              "actual_numerical_thread_count_observed": None},
              "all_frozen_identity_checks_passed": True,
              "stage_a_complete": args.mode == "qualification",
              "stage_b_admitted": False, "official_scorer_parity": False,
              "scientific_gate_advanced": False, "performance_claim_eligible": False,
              "near_zero_denominator_policy_qualified": False,
              "output_mitigation_contract": "LANDMARK_STAGE_A_OUTPUT_MITIGATION_v2.md",
              "original_gzip_root_cause_repaired": False,
              "tie_policy": "refresh_scipy_evr_sign_canonical; FD_existing_numpy_svd; no low-recourse guarantee"}
    partial = output.with_name(output.name + ".partial")
    with partial.open("x") as stream:
        stream.write(json.dumps(result, allow_nan=False, indent=2) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    expected = sha256(partial)
    publish_no_replace(partial, output)
    if sha256(output) != expected or any(sha256(output.parent / x["path"]) != x["sha256"] for x in outputs):
        raise ValueError("final published output mismatch")
    print(json.dumps({"output": str(output), "mode": args.mode, "maxima": maxima, "usage": result["usage"]}), flush=True)


if __name__ == "__main__":
    main()
