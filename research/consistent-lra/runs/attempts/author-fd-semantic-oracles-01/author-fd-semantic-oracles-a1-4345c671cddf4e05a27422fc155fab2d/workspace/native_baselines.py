"""Existing-method baseline audit draft, NOT an admitted scientific queue.

REPAIR_CONTRACT_v1 specifies the repaired metric and warmup convention.
This code must undergo independent semantic/source and native qualification
and be dispatched through a pinned RSI scientific harness protocol before use.
"""
import argparse
import hashlib
import io
import json
import random
import resource
import time
from pathlib import Path

import numpy as np
from scipy.io import mmread

from baseline_qualify import blob_digest, load_native, top_basis, score_direct, recourse_overlap

LANDMARK_BLOB = "4c63060bbefcb38e0c705cea1f883d2fb7121f2c"


def load_stream(args):
    if args.dataset in ("rice", "skin"):
        return load_native(args.dataset, args.source)
    if args.dataset == "landmark":
        raw = Path(args.source).read_bytes()
        if blob_digest(raw) != LANDMARK_BLOB:
            raise ValueError("Landmark source identity mismatch")
        # Slice sparsely before densifying; never allocate all 71952 rows.
        sparse = mmread(io.BytesIO(raw)).tocsr()
        if sparse.shape != (71952, 2704):
            raise ValueError("Landmark source dimensions mismatch")
        a = sparse[:5000].toarray().astype(np.float64)
        return a, {"dataset": "landmark", "source_blob": LANDMARK_BLOB,
                   "source_sha256": hashlib.sha256(raw).hexdigest(),
                   "released_shape": [71952, 2704], "denominator": 5000,
                   "sample_ids": [f"landmark:row:{t}" for t in range(1, 5001)],
                   "preprocessing": "none", "source_access_qualified": True}
    # Only the released unscaled generator family; this is a new seeded
    # instance, never the original unseeded figure or ambiguous normalization.
    if args.random_variant != "released_code_unscaled":
        raise ValueError("ambiguous paper normalization is not implemented as a guessed reproduction")
    rng = random.Random(args.seed)
    a = np.array([[rng.randint(0, 100) for _ in range(4)] for _ in range(3000)], dtype=np.float64)
    return a, {"dataset": "random", "generator_blob": "cfe96c16b699a96720e41cc36ab36a25a45b4627",
               "generator": "Python random.Random(seed).randint(0,100),row_major",
               "seed": args.seed, "denominator": 3000, "preprocessing": "none",
               "sample_ids": [f"random:{args.seed}:row:{t}" for t in range(1, 3001)],
               "matrix_sha256": hashlib.sha256(a.astype("<f8").tobytes()).hexdigest(),
               "original_figure_replication": False}


class RefreshBaseline:
    def __init__(self, matrix, k, mode, parameter):
        self.matrix, self.k, self.mode, self.parameter = matrix, k, mode, parameter
        self.q = np.empty((0, matrix.shape[1]))
        self.energy_at_refresh = 0.0
        self.refreshes = 0

    def update(self, t, energy):
        if not np.isfinite(energy):
            raise ValueError("nonfinite stream energy")
        warmup = t <= self.k
        refresh = warmup or len(self.q) == 0
        if self.mode == "fresh":
            refresh = True
        elif self.mode == "algorithm4":
            refresh = refresh or energy >= self.parameter * self.energy_at_refresh
        elif self.mode == "periodic":
            refresh = refresh or (t > self.k and (t - self.k) % int(self.parameter) == 0)
        elif self.mode != "fixed":
            raise ValueError("unknown refresh baseline")
        if refresh:
            if energy == 0:
                self.q = np.eye(self.matrix.shape[1])[:min(self.k, t)].copy()
            else:
                self.q, _ = top_basis(self.matrix[:t], self.k)
            self.energy_at_refresh = energy
            self.refreshes += 1
        return self.q.copy(), refresh, warmup


class FrequentDirectionsBaseline:
    """Standard l-row shrink FD; exact formula from established FD.

    l <= d. On a full sketch, subtract smallest singularvalue squared,
    leaving a zero final row, and then insert the next released row.
    Output top-k right directions; rows of the weighted sketch are not P.
    This is separately named from the author's l+1-augmented variant and
    Liberty's buffered2l implementation; parity remains a qualification item.
    """
    def __init__(self, matrix, k, ell):
        if not k < ell <= matrix.shape[1]:
            raise ValueError("strong FD requires k<ell<=d")
        self.matrix, self.k, self.ell = matrix, k, ell
        self.b = np.zeros((ell, matrix.shape[1]), dtype=np.float64)
        self.next = 0
        self.shrinks = 0

    def update(self, t, energy):
        if self.next == self.ell:
            _, singular, vh = np.linalg.svd(self.b, full_matrices=False)
            shrunk = np.sqrt(np.maximum(singular ** 2 - singular[-1] ** 2, 0.0))
            self.b = shrunk[:, None] * vh
            self.next = self.ell - 1
            self.shrinks += 1
        self.b[self.next] = self.matrix[t - 1]
        self.next += 1
        q, _ = top_basis(self.b[:self.next], min(self.k, t))
        return q.copy(), True, t <= self.k


class AuthorAugmentedFDDiagnostic:
    """Frozen-author ell+1 update, scored with the common projector contract.

    The update mirrors `originals/consistent-fd.py`: fill the first row for
    which ``np.any`` is false; once all ell rows are nonzero, append the new
    row, decompose the (ell+1)-row matrix, subtract sigma_{ell+1}^2 and retain
    ell weighted right-singular rows.  This intentionally preserves the
    author's all-zero-row ambiguity.  It does *not* preserve the author's live
    array alias or row-span recourse metric: the diagnostic emits a copied,
    row-orthonormal top-k basis for the shared repaired scorer.
    """
    def __init__(self, matrix, k, ell):
        if not 1 <= k <= ell < matrix.shape[1]:
            raise ValueError("author FD diagnostic requires 1<=k<=ell<d")
        self.matrix, self.k, self.ell = matrix, k, ell
        self.b = np.zeros((ell, matrix.shape[1]), dtype=np.float64)
        self.shrinks = 0

    def update(self, t, energy):
        row = self.matrix[t - 1]
        for index in range(self.ell):
            if not np.any(self.b[index]):
                self.b[index] = row
                break
        else:
            augmented = np.vstack([self.b, row])
            _, singular, vh = np.linalg.svd(augmented, full_matrices=False)
            delta = singular[self.ell] ** 2
            shrunk = np.sqrt(np.maximum(singular[:self.ell] ** 2 - delta, 0.0))
            self.b = shrunk[:, None] * vh[:self.ell]
            self.shrinks += 1
        q, _ = top_basis(self.b, min(self.k, t))
        return q.copy(), True, t <= self.k


def make_arm(args, matrix):
    if args.arm == "fd":
        return FrequentDirectionsBaseline(matrix, args.k, args.ell)
    if args.arm == "author_fd":
        return AuthorAugmentedFDDiagnostic(matrix, args.k, args.ell)
    if args.arm == "algorithm4" and (not np.isfinite(args.c) or not args.c > 1):
        raise ValueError("c must be greater than1")
    if args.arm == "periodic" and args.interval <= 0:
        raise ValueError("period must be positive")
    parameter = args.c if args.arm == "algorithm4" else args.interval
    return RefreshBaseline(matrix, args.k, args.arm, parameter)


def run(args):
    start = time.perf_counter()
    cpu_start = resource.getrusage(resource.RUSAGE_SELF)
    matrix, native = load_stream(args)
    if args.k < 1 or args.k >= matrix.shape[1]:
        raise ValueError("require1<=k<d for nontrivial audit")
    if not np.isfinite(matrix).all():
        raise ValueError("nonfinite native input")
    arm = make_arm(args, matrix)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    previous = None
    cumulative = steady = update_total = scoring_total = reference_total = energy_total = 0.0
    finite_ratios = []
    excluded = zero_violations = 0
    energy = 0.0
    with output.open("w", encoding="utf-8") as stream:
        for t in range(1, len(matrix) + 1):
            then = time.perf_counter()
            energy += float(np.dot(matrix[t - 1], matrix[t - 1]))
            energy_time = time.perf_counter() - then
            energy_total += energy_time
            if not np.isfinite(energy):
                raise ValueError("nonfinite energy")
            then = time.perf_counter()
            q, updated, warmup = arm.update(t, energy)
            update_time = time.perf_counter() - then
            if args.arm == "algorithm4":
                update_time += energy_time
            update_total += update_time
            # Fresh prefix OPT has no access to the arm's retained basis.
            then = time.perf_counter()
            singular = np.linalg.svd(matrix[:t], full_matrices=False, compute_uv=False)
            optimal = float(np.sum(singular[args.k:] ** 2))
            reference_time = time.perf_counter() - then
            reference_total += reference_time
            then = time.perf_counter()
            loss = score_direct(matrix[:t], q)
            if not np.isfinite(q).all() or not np.isfinite(loss) or not np.isfinite(optimal):
                raise ValueError("nonfinite arm basis or score")
            orthogonality = float(np.linalg.norm(q @ q.T - np.eye(len(q)), ord="fro"))
            if orthogonality > 1e-10 * max(1, len(q)):
                raise ValueError("nonorthonormal arm output")
            increment_raw = recourse_overlap(q, previous) if previous is not None else 0.0
            recourse_tol = 1e-10 * max(1, 2 * args.k)
            if increment_raw < -recourse_tol:
                raise ValueError("negative recourse beyond numerical allowance")
            increment = max(0.0, increment_raw)
            cumulative += increment
            if t > args.k:
                steady += increment
            tolerance = 1e-10 * max(1.0, energy)
            ratio = loss / optimal if optimal > tolerance else None
            excluded += ratio is None
            zero_violations += optimal <= tolerance and loss > tolerance
            if ratio is not None:
                finite_ratios.append(ratio)
            scoring_time = time.perf_counter() - then
            scoring_total += scoring_time
            record = {"prefix": t, "sample_id": native["sample_ids"][t - 1],
                      "rank": len(q), "warmup": warmup, "updated": updated,
                      "energy": energy, "loss": loss, "opt": optimal,
                      "additive_excess": loss - optimal,
                      "normalized_additive_excess": (loss - optimal) / energy if energy > 0 else None,
                      "ratio": ratio, "loss_tolerance": tolerance,
                      "near_zero_opt": optimal <= tolerance,
                      "recourse_increment_unclamped": increment_raw,
                      "recourse_increment": increment, "recourse": cumulative,
                      "steady_recourse": steady, "orthogonality_error": orthogonality,
                      "update_seconds": update_time, "reference_seconds": reference_time,
                      "energy_maintenance_seconds": energy_time,
                      "scoring_seconds": scoring_time, "basis": q.tolist()}
            stream.write(json.dumps(record, allow_nan=False, separators=(",", ":")) + "\n")
            previous = q.copy()
    cpu_end = resource.getrusage(resource.RUSAGE_SELF)
    summary = {"format": "consistent-lra-existing-baseline-audit-v1", "configuration": vars(args),
               "native": native, "prefix_denominator": len(matrix),
               "defined_ratio_denominator": len(finite_ratios), "near_zero_opt_exclusions": excluded,
               "positive_loss_near_zero_opt_count": zero_violations,
               "ratio_mean": float(np.mean(finite_ratios)) if finite_ratios else None,
               "ratio_median": float(np.median(finite_ratios)) if finite_ratios else None,
               "ratio_max": float(np.max(finite_ratios)) if finite_ratios else None,
               "final_recourse": cumulative, "final_steady_recourse": steady,
               "raw_sha256": file_sha256(output),
               "usage": {"pipeline_seconds": time.perf_counter() - start,
                         "update_seconds": update_total, "reference_seconds": reference_total,
                         "scoring_seconds": scoring_total, "max_rss_kib": cpu_end.ru_maxrss,
                         "energy_maintenance_seconds": energy_total,
                         "cpu_seconds": cpu_end.ru_utime + cpu_end.ru_stime - cpu_start.ru_utime - cpu_start.ru_stime},
               "confirmation": False, "scientific_gate_advanced": False,
               "low_recourse_theorem_transferred": False,
               "zero_energy_convention": ("refresh canonical first min(k,t) coordinate directions"
                                          if args.arm not in ("fd", "author_fd")
                                          else "FD numpy_svd_library_tie_policy_pending_qualification"),
               "timing_accounting": "Algorithm4 update_seconds includes energy_maintenance_seconds; do not add this diagnostic twice",
               "nonzero_degenerate_spectrum_convention": "numpy_svd_library_tie_policy_no_low_recourse_guarantee",
               "initialization_from_zero_excluded_from_primary_recourse": True,
               "fd_variant": ({"fd": "strong_ell_row_compress_before_insert",
                               "author_fd": "frozen_author_ell_plus_one_update_common_projector_output"}.get(args.arm)),
               "author_fd_is_diagnostic_not_strong_baseline": args.arm == "author_fd",
               "sensitivity_and_author_FD_diagnostic": "implementation candidate present; execution and complete G01 pending",
               "qualification_pending": True}
    output.with_suffix(".summary.json").write_text(json.dumps(summary, allow_nan=False, indent=2) + "\n")
    print(json.dumps({"output": str(output), "usage": summary["usage"], "scientific_gate_advanced": False}))


def file_sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", choices=["rice", "skin", "landmark", "random"], required=True)
    parser.add_argument("--source", default="")
    parser.add_argument("--arm", choices=["algorithm4", "fresh", "fixed", "periodic", "fd", "author_fd"], required=True)
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--c", type=float, default=1.1)
    parser.add_argument("--interval", type=int, default=100)
    parser.add_argument("--ell", type=int, default=2)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--random-variant", choices=["released_code_unscaled"], default="released_code_unscaled")
    parser.add_argument("--output", required=True)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
