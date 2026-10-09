#!/usr/bin/env python3
"""Exact finite audit of accepted geometric rank-one counterexample.

This is not a native-data benchmark, a novel algorithm, a general proof,
or floating-point validation. Fraction/integer calculations certify only
requested ranks (1 <= k <= 61). Root integrates independently reviewed source.
"""
import argparse
import datetime
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import time
import uuid

SCHEMA = "geometric-exact-finite-certificate-v1"
PARENT_V5 = "de008df475aba17eb4557fdeb5e7ed57d7843f79dd107ecbed686e40ef717ef5"
PARENT_V6 = "140141fcc4b5e86bc182ea1bf399f80f6df5f1cb4dd8fe6c76b9bd569bd6573b"


def require(condition, message):
    # Deliberate runtime checks, not assert: -O must not remove qualification.
    if not condition:
        raise ValueError(message)


def exact(value):
    value = Fraction(value)
    return {"numerator_hex": hex(value.numerator),
            "denominator_hex": hex(value.denominator)}


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def file_identity(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def publish_bytes(path, data):
    """Write/read back bytes, then atomically link final without replacement."""
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + ".partial-" + uuid.uuid4().hex)
    expected = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    # Keep a failed partial for diagnosis; never replace an existing final.
    with partial.open("xb", buffering=0) as stream:
        view = memoryview(data)
        while view:
            written = stream.write(view)
            require(written is not None and written > 0, "short/zero output write")
            view = view[written:]
        os.fsync(stream.fileno())
    require(file_identity(partial) == expected, "partial output readback mismatch")
    os.link(partial, path)
    partial.unlink()
    directory = os.open(str(path.parent), os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)
    require(file_identity(path) == expected, "published output readback mismatch")
    return expected


def certify(k):
    require(1 <= k <= 61, "rank outside frozen finite range")
    scales = [16 ** i for i in range(1, k + 1)]
    old = sorted([-a for a in scales] + scales)
    new = sorted([-a // 2 for a in scales] + [2 * a for a in scales])
    require(len(set(old)) == len(set(new)) == 2 * k, "non-simple spectrum")
    require(not set(old) & set(new), "old/new spectral collision")
    require(all(old[i] < new[i] < old[i + 1] for i in range(2 * k - 1))
            and old[-1] < new[-1], "strict rank-one interlacing failed")
    rho = {}
    for lam in old:
        numerator = -math.prod(lam - mu for mu in new)
        denominator = math.prod(lam - other for other in old if other != lam)
        rho[lam] = Fraction(numerator, denominator)
        require(rho[lam] > 0, "non-positive residue weight")
    trace_shift = Fraction(sum(new) - sum(old))
    require(sum(rho.values(), Fraction()) == trace_shift, "residue/trace mismatch")
    require(trace_shift == Fraction(3, 2) * sum(scales), "geometric trace mismatch")
    root_records = []
    inverses = {}
    for mu in new:
        secular = sum((rho[lam] / (mu - lam) for lam in old), Fraction())
        require(secular == 1, "secular root identity failed")
        norm_squared = sum((rho[lam] / (mu - lam) ** 2 for lam in old), Fraction())
        # Independent product derivative of the characteristic quotient g.
        derivative = Fraction(math.prod(mu - other for other in new if other != mu),
                              math.prod(mu - lam for lam in old))
        require(norm_squared == derivative and norm_squared > 0,
                "secular/product derivative mismatch")
        inv_norm = 1 / norm_squared
        weight_sum = sum((rho[lam] * inv_norm / (mu - lam) ** 2 for lam in old), Fraction())
        require(weight_sum == 1, "normalized eigenvector squared weights failed")
        inverses[mu] = inv_norm
        root_records.append({"mu": mu, "secular_sum": exact(secular),
                             "norm_squared": exact(norm_squared),
                             "product_derivative": exact(derivative),
                             "inverse_norm_squared": exact(inv_norm),
                             "normalized_weight_sum": exact(weight_sum)})
    matched = []
    for index, a in enumerate(scales, 1):
        crossing = rho[-a] * inverses[2 * a] / (3 * a) ** 2
        require(crossing > Fraction(1, 15), "matched lower bound failed")
        matched.append({"scale_index": index, "a": a,
                        "old_negative_lambda": -a, "new_positive_mu": 2 * a,
                        "squared_coordinate": exact(crossing),
                        "strict_margin_over_one_fifteenth": exact(crossing - Fraction(1, 15))})
    matched_sum = sum((rho[-a] * inverses[2 * a] / (3 * a) ** 2 for a in scales), Fraction())
    recourse_lower_bound = Fraction(2 * k, 15)
    require(2 * matched_sum > recourse_lower_bound, "summed recourse bound failed")
    largest = scales[-1]
    require(rho[-largest] >= Fraction(3 * largest, 4), "v6 first-coordinate bound failed")
    require(trace_shift < Fraction(8 * largest, 5), "v6 total update norm bound failed")
    require(trace_shift - rho[-largest] < Fraction(17 * largest, 20),
            "v6 retained-coordinate budget failed")
    # These exact inequalities corroborate premises of the accepted analytic
    # all-consecutive-block proof. No block singular values are computed here.
    return {"schema": SCHEMA, "k": k, "old_spectrum": old, "new_spectrum": new,
            "shift_c": 2 * largest,
            "residues": [{"lambda": lam, "rho": exact(rho[lam])} for lam in old],
            "trace_shift": exact(trace_shift), "roots": root_records,
            "matched_crossings": matched, "matched_crossing_sum": exact(matched_sum),
            "strict_recourse_lower_bound": exact(recourse_lower_bound),
            "lower_bound_exceeds_eight": recourse_lower_bound > 8,
            "first_coordinate_residue": exact(rho[-largest]),
            "v6_update_norm_squared": exact(trace_shift),
            "v6_retained_coordinate_budget": exact(trace_shift - rho[-largest]),
            "checks": {"strict_interlacing": True, "positive_residues": True,
                       "trace_identity": True, "exact_secular_roots": True,
                       "independent_product_derivative": True,
                       "normalized_eigenvector_weights": True,
                       "each_matched_crossing_gt_one_fifteenth": True,
                       "v6_conditioning_proof_scalar_premises": True},
            "scope": "finite exact identities and matched-coordinate strict lower bound only",
            "full_recourse_computed": False, "block_singular_values_computed": False,
            "native_scientific_qualification": False, "novelty_qualified": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ranks", nargs="+", type=int, required=True)
    parser.add_argument("--records", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    require(args.ranks == sorted(set(args.ranks)), "ranks must be unique, sorted")
    require(all(1 <= k <= 61 for k in args.ranks), "rank outside frozen finite range")
    require(args.records.resolve() != args.summary.resolve(), "output paths must differ")
    require(not args.records.exists() and not args.summary.exists(), "existing output final")
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    wall = time.monotonic()
    cpu = time.process_time()
    source_identity = file_identity(Path(__file__))
    records = []
    timings = []
    for k in args.ranks:
        rank_wall, rank_cpu = time.monotonic(), time.process_time()
        records.append(certify(k))
        timings.append({"k": k, "wall_seconds": time.monotonic() - rank_wall,
                        "process_cpu_seconds": time.process_time() - rank_cpu})
        print(json.dumps({"rank_completed": k, "scope": "exact_formal_audit_only"}), flush=True)
    packet = b"".join(encoded(record) for record in records)
    identity = publish_bytes(args.records, packet)
    # Reparse every retained fraction, inventory and rank before summary last.
    retained = [json.loads(line) for line in args.records.read_bytes().splitlines()]
    require(retained == records, "certificate JSONL semantic readback mismatch")
    require(file_identity(Path(__file__)) == source_identity, "source changed during execution")
    summary = {"schema": SCHEMA, "status": "completed_finite_exact_audit_only",
               "ranks": args.ranks, "record_count": len(records),
               "source_identity": source_identity, "parent_v5_sha256": PARENT_V5,
               "parent_v6_sha256": PARENT_V6, "records": {"path": str(args.records), **identity},
               "started_at": started,
               "completed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "rank_calibration": timings, "pipeline_wall_seconds": time.monotonic() - wall,
               "process_cpu_seconds": time.process_time() - cpu,
               "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               "cpu_semantics": "one CPython process; process_time, excluding caller/harness",
               "finite_checks_passed": True, "general_proof_is_analytic_parent": True,
               "full_recourse_computed": False, "native_scientific_qualification": False,
               "novelty_qualified": False, "paper_eligible": False}
    summary_identity = publish_bytes(args.summary, encoded(summary))
    require(file_identity(args.records) == identity, "certificate changed after summary publication")
    require(file_identity(args.summary) == summary_identity, "summary changed after publication")
    print(json.dumps({"summary": str(args.summary), "summary_identity": summary_identity,
                      "record_count": len(records), "scientific_gate_advanced": False}), flush=True)


if __name__ == "__main__":
    main()
