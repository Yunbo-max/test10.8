"""Independent replay of retained actual154 evidence; never imports its producer.

Read-only fixed-commit Git extraction and exact arithmetic on recorded inputs.
This verifies a finite projector lower-bound certificate, not native performance.
"""
import datetime
from fractions import Fraction as Rational
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import time

COMMIT = "eed4b24ca7549f4bce1ae71ce65008431dbbea67"
REPOSITORY = "/workspace/scratch/bb9f262965cf/lra-window02"
PREFIX = "research/consistent-lra/"
COLLECTION = "evidence/integer-projector-target61-02-collection.json"
NATIVE = "plans/native-integer-projector-target61-02.json"
OUTER = "plans/harness-integer-projector-target61-02.json"
SOURCE_SHA = "e59cf9f03c40007271c14ca98ecd940f59bfa33cbd5a860218310556be67a22d"
FLAGS = ("scientific_gate_advanced", "native_evaluator_qualified",
         "block_condition_computed", "novelty_qualified",
         "performance_claim_eligible", "confirmation",
         "approximate_existence_refuted")


def gitbytes(path):
    return subprocess.check_output(["git", "show", COMMIT+":"+PREFIX+path],
                                   cwd=REPOSITORY)


def load(path):
    return json.loads(gitbytes(path))


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def decode_rational(value):
    n = int(value["numerator_hex"], 16)
    d = int(value["denominator_hex"], 16)
    result = Rational(n, d)
    assert d > 0 and (result.numerator, result.denominator) == (n, d)
    return result


def rational_digest(value):
    encoding = {"numerator_hex": hex(value.numerator),
                "denominator_hex": hex(value.denominator)}
    return {"sha256": hashlib.sha256(canonical(encoding)).hexdigest(),
            "sign": (value > 0)-(value < 0),
            "numerator_bits": abs(value.numerator).bit_length(),
            "denominator_bits": value.denominator.bit_length()}


def references(value, found):
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and isinstance(value.get("sha256"), str):
            found[value["path"]] = value["sha256"]
        for item in value.values():
            references(item, found)
    elif isinstance(value, list):
        for item in value:
            references(item, found)


def main():
    started_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    started_wall, started_cpu = time.perf_counter(), time.process_time()
    child_before = resource.getrusage(resource.RUSAGE_CHILDREN)
    collection = load(COLLECTION)
    native, outer = load(NATIVE), load(OUTER)
    for plan in (native, outer):
        frozen_digest = plan["plan_digest"]
        unsigned = {k: v for k, v in plan.items() if k != "plan_digest"}
        assert hashlib.sha256(canonical(unsigned)).hexdigest() == frozen_digest
    assert native["plan_digest"] == "fbb52f2e5b6f16974f8ffaaff329cabad803909189d732142388a71f304c05e9"
    assert outer["plan_digest"] == "6986ad275e6cd1441a5f55c68ffd38741dafaa4c7b187de2b812b83e886eb993"
    receipt = load("runs/attempts/exact-integer-projector-target61-02/receipt.json")
    assert len(receipt["attempts"]) == 1 and receipt["status"] == "completed"
    attempt = receipt["attempts"][0]
    assert attempt["attempt_id"] == collection["attempt_id"]
    assert attempt["status"] == "completed" and attempt["exit_code"] == 0
    assert attempt["retry_index"] == 0 and receipt["plan_digest"] == native["plan_digest"]
    job = native["jobs"][0]
    assert attempt["command"] == job["command"]
    assert attempt["input_refs"] == job["input_refs"]
    assert attempt["code_refs"] == job["code_refs"]
    assert attempt["cwd"].endswith("/"+attempt["attempt_path"]+"/workspace")
    verified_files = set()
    for ref in collection["files"]+attempt["input_refs"]+attempt["code_refs"]:
        data = gitbytes(ref["path"])
        assert hashlib.sha256(data).hexdigest() == ref["sha256"]
        assert "bytes" not in ref or len(data) == ref["bytes"]
        verified_files.add(ref["path"])
    output_refs = collection["output_readback_boundaries"][0]
    for boundary in collection["output_readback_boundaries"]:
        for ref in boundary:
            data = gitbytes(ref["path"])
            assert len(data) == ref["bytes"] and hashlib.sha256(data).hexdigest() == ref["sha256"]
    raw_data = gitbytes(output_refs[0]["path"])
    rows = [json.loads(line) for line in raw_data.splitlines()]
    summary = load(output_refs[1]["path"])
    assert summary == collection["summary"]
    all_refs = {}
    references(native, all_refs)
    references(outer, all_refs)
    for ref in collection["files"]:
        if ref["path"].endswith(".json"):
            references(load(ref["path"]), all_refs)
    for path, digest in all_refs.items():
        if path == "projector-certificate.jsonl":
            path = output_refs[0]["path"]
        assert hashlib.sha256(gitbytes(path)).hexdigest() == digest
    manifest = load("vendor/rsi/SOURCE_MANIFEST.json")
    assert manifest["commit"] == "1de12dfed5b84957b29ac5b3a2f04904bf3742bc"
    for ref in manifest["files"]:
        data = gitbytes("vendor/rsi/"+ref["relative_path"])
        assert len(data) == ref["byte_length"] and hashlib.sha256(data).hexdigest() == ref["sha256"]
        blob = b"blob "+str(len(data)).encode()+b"\0"+data
        assert hashlib.sha1(blob).hexdigest() == ref["git_blob_sha"]
    assert len(rows) == 63 and summary["raw_records"] == 63
    assert [row["record_type"] for row in rows] == ["provenance", "rank_input"]+["root"]*61
    assert all(all(row[flag] is False for flag in FLAGS) for row in rows)
    assert rows[0]["mode"] == "full" and rows[0]["source_sha256"] == SOURCE_SHA
    for ref in rows[0]["inputs"].values():
        data = gitbytes(ref["path"])
        assert len(data) == ref["bytes"] and hashlib.sha256(data).hexdigest() == ref["sha256"]
    witness_ref = next(ref for ref in job["input_refs"] if ref["sha256"] ==
                       "323acf9c07264a3168339270e784f4ac302a47aaa0e8da17d224ce96c5c40c2f")
    witness_lines = gitbytes(witness_ref["path"]).splitlines()
    witness, line = next((json.loads(line), line) for line in witness_lines if json.loads(line)["k"] == 61)
    rank_input = rows[1]
    assert rank_input["k"] == 61 and rank_input["dimension"] == 122
    assert rank_input["root_indices"] == list(range(61, 122))
    assert rank_input["complete_topk_inventory"] is True
    assert rank_input["witness_line_sha256"] == hashlib.sha256(line).hexdigest()
    for key in ("diagonal_integers", "appended_row_integers", "a_hex",
                "scale_hex", "target_parent_mu_hex", "dimension"):
        assert rank_input[key] == witness[key]
    diagonal, appended = rank_input["diagonal_integers"], rank_input["appended_row_integers"]
    assert len(diagonal) == len(appended) == 122
    assert all(type(v) is int and v > 0 for v in diagonal+appended)
    poles = [v*v for v in diagonal]
    weights = [v*v for v in appended]
    assert all(a < b for a, b in zip(poles, poles[1:]))
    a, scale = int(rank_input["a_hex"], 16), int(rank_input["scale_hex"], 16)
    mus = [int(value, 16) for value in rank_input["target_parent_mu_hex"]]

    def secular_at(x):
        return Rational(1)+sum((Rational(weight)/(pole-x)
                               for pole, weight in zip(poles, weights)), Rational(0))

    floors = []
    roots = rows[2:]
    assert [root["pole_index"] for root in roots] == list(range(61, 122))
    for root in roots:
        index = root["pole_index"]
        assert root["k"] == 61 and root["requested_bisections"] == 12
        lower = Rational(scale*scale*(2*a+mus[index]))-Rational(scale*scale, 30)
        upper = Rational(scale*scale*(2*a+mus[index]))+Rational(scale*scale, 30)
        assert decode_rational(root["initial"]["lo"]) == lower
        assert decode_rational(root["initial"]["hi"]) == upper
        assert poles[index] < lower < upper
        assert index == 121 or upper < poles[index+1]
        f_lower, f_upper = secular_at(lower), secular_at(upper)
        assert f_lower < 0 < f_upper
        assert rational_digest(f_lower) == root["initial"]["f_lo"]
        assert rational_digest(f_upper) == root["initial"]["f_hi"]
        collapsed = False
        decisions = root["bisection_decisions"]
        assert root["actual_decisions"] == len(decisions)
        for step, decision in enumerate(decisions):
            midpoint = (lower+upper)/2
            value = secular_at(midpoint)
            assert step == decision["step"]
            assert midpoint == decode_rational(decision["midpoint"])
            assert rational_digest(value) == decision["f"]
            if value == 0:
                lower = upper = midpoint
                collapsed = True
                assert step+1 == len(decisions)
                break
            if value < 0:
                lower = midpoint
            else:
                upper = midpoint
        assert collapsed == root["exact_root_collapse"]
        assert collapsed or len(decisions) == 12
        assert lower == decode_rational(root["final"]["lo"])
        assert upper == decode_rational(root["final"]["hi"])
        assert collapsed or secular_at(lower) < 0 < secular_at(upper)
        near = [min(abs(lower-pole), abs(upper-pole)) for pole in poles]
        far = [max(abs(lower-pole), abs(upper-pole)) for pole in poles]
        assert all(distance > 0 for distance in near)
        numerator_bound = sum((Rational(weights[i])/far[i]**2 for i in range(61)), Rational(0))
        normalizer_bound = sum((Rational(weights[i])/near[i]**2 for i in range(122)), Rational(0))
        assert 0 < numerator_bound < normalizer_bound
        crossmass_bound = numerator_bound/normalizer_bound
        assert rational_digest(numerator_bound) == root["lower_numerator"]
        assert rational_digest(normalizer_bound) == root["upper_normalizer"]
        assert rational_digest(crossmass_bound) == root["lower_crossmass"]
        dyadic_floor = crossmass_bound.numerator*2**32//crossmass_bound.denominator
        assert root["dyadic_bits"] == 32 and root["dyadic_floor"] == dyadic_floor
        assert Rational(dyadic_floor, 2**32) <= crossmass_bound < Rational(dyadic_floor+1, 2**32)
        floors.append(dyadic_floor)
        if len(floors) % 10 == 0:
            print(json.dumps({"verified_roots": len(floors), "last_index": index}), flush=True)
    bound = Rational(2*sum(floors), 2**32)
    assert bound == Rational(0x8885519b, 0x8000000) and bound > 8
    assert len(summary["ranks"]) == 1
    rank_summary = summary["ranks"][0]
    assert rank_summary["k"] == 61 and rank_summary["root_indices"] == list(range(61, 122))
    assert rank_summary["completed_roots"] == 61 and rank_summary["complete_topk_inventory"] is True
    assert decode_rational(rank_summary["recourse_lower_bound"]) == bound
    assert rank_summary["target_applicable"] is True
    assert rank_summary["target_strictly_greater_than_8"] is True
    assert rank_summary["target_verdict"] == "certified"
    assert summary["mode"] == "full" and summary["arithmetic_completed"] is True
    assert all(summary[flag] is False and rank_summary[flag] is False for flag in FLAGS)
    assert summary["source_sha256"] == SOURCE_SHA
    guard = load(attempt["process_guard_ref"]["path"])
    harness = "runs/harness/exact-integer-projector-target61-batch-02/"
    state = load(harness+"state.json")
    context = load(harness+"tasks/exact-integer-projector-target61-02/execution-context.json")
    assert guard["status"] == state["status"] == "completed" and guard["exit_code"] == 0
    assert context["native_plan_digest"] == native["plan_digest"]
    assert context["batch_plan_digest"] == outer["plan_digest"]
    assert context["declared_resources"] == outer["tasks"][0]["resources"]
    assert context["CUDA_VISIBLE_DEVICES"] == ""
    pids = [guard["guard_process"]["pid"], guard["guard_process"]["parent_pid"]]
    assert all(not Path("/proc", str(pid)).exists() for pid in pids)
    ledger = load("BUDGET_OBSERVATION.json")
    reservation = ledger["window02_integer_projector_target_reservation"]
    assert reservation["released"] is True and reservation["attempts_launched"] == 1
    child_after = resource.getrusage(resource.RUSAGE_CHILDREN)
    result = {"verdict": "ACCEPT_finite_full61_arithmetic_and_evidence_only",
              "commit": COMMIT, "verified_roots": 61, "verified_decisions": sum(len(r["bisection_decisions"]) for r in roots),
              "record_inventory": 63, "distinct_file_refs": len(verified_files),
              "recursive_reference_paths": len(all_refs), "vendor_files": len(manifest["files"]),
              "lower_bound": {"numerator": bound.numerator, "denominator": bound.denominator},
              "strict_excess_over_8": {"numerator": (bound-8).numerator, "denominator": (bound-8).denominator},
              "root_cost_wall_sum": sum(r["root_wall_seconds"] for r in roots),
              "root_cost_cpu_sum": sum(r["root_cpu_seconds"] for r in roots),
              "script_before_summary_wall": summary["script_wall_before_summary_seconds"],
              "script_before_summary_cpu": summary["script_cpu_before_summary_seconds"],
              "launcher": collection["launcher_usage"], "terminal_pids_absent": pids,
              "ledger_cpu_before_review": ledger["observed_process_cpu_seconds"],
              "reviewer_script_path": str(Path(__file__).resolve()),
              "reviewer_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "analysis_cost": {"started_at": started_at,
                   "completed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   "wall_seconds": time.perf_counter()-started_wall,
                   "self_cpu_seconds": time.process_time()-started_cpu,
                   "waited_git_cpu_seconds": child_after.ru_utime+child_after.ru_stime-child_before.ru_utime-child_before.ru_stime,
                   "max_self_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
    print(json.dumps(result, sort_keys=True, allow_nan=False), flush=True)


if __name__ == "__main__":
    main()
