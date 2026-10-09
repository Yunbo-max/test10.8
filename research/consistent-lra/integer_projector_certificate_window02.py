"""Generated unexecuted exact integer projector-bound certificate.

Existing accepted lemma audit only; separate source/plan admission required.
No project imports, floating arithmetic, matrix experiments or native scoring.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import resource
import sys
import time

EXPECTED = {
    'design': 'cd5105ae89973017d6512351917eb730f3be4689cc04913f4dafb285e8be6c2f',
    'cost_contract': 'c9e534e32fd787c3f8bd9f0ebba19a65feef820a00767b0c7bdce9f67bdf4fd5',
    'design_review': '5faa7f8837d38a8d8dcbc89fb80bb4e296366a4d8102f53638788f3fcc0e57d4',
    'cost_review': 'dd6c53d12441d7c54ab301ce8f268bd77a3ab999d0f2fe4ad8cfc27acc7097c2',
    'witness_review': 'f7ae275d01ebaa9f4aa536de8e4dbe370e3d318a428e9c44f70d191b7ad6ceab',
    'witness': '323acf9c07264a3168339270e784f4ac302a47aaa0e8da17d224ce96c5c40c2f',
}
FLAGS = dict(scientific_gate_advanced=False, native_evaluator_qualified=False,
             block_condition_computed=False, novelty_qualified=False,
             performance_claim_eligible=False, confirmation=False,
             approximate_existence_refuted=False)
DYADIC_BITS = 32
BISECTIONS = 12


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def encoded(obj):
    return canonical(obj)+b'\n'


def fraction_object(q):
    if not isinstance(q, Fraction):
        raise TypeError('not_fraction')
    return dict(numerator_hex=hex(q.numerator), denominator_hex=hex(q.denominator))


def fraction_digest(q):
    return dict(sha256=sha(canonical(fraction_object(q))),
                sign=(q > 0)-(q < 0), numerator_bits=abs(q.numerator).bit_length(),
                denominator_bits=q.denominator.bit_length())


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_all(stream, data):
    pos = 0
    while pos < len(data):
        n = stream.write(data[pos:])
        if not n:
            raise IOError('short_write')
        pos += n
    stream.flush()
    os.fsync(stream.fileno())


def publish(partial, final, expected_bytes, expected_sha):
    actual = partial.read_bytes()
    if len(actual) != expected_bytes or sha(actual) != expected_sha:
        raise ValueError('partial_intended_identity')
    os.link(partial, final)  # exclusive publication, never replace existing output
    partial.unlink()
    sync_directory(final.parent)
    actual = final.read_bytes()
    if len(actual) != expected_bytes or sha(actual) != expected_sha:
        raise ValueError('final_intended_identity')
    return dict(path=final.name, bytes=expected_bytes, sha256=expected_sha)


def secular(x, poles, squares):
    result = Fraction(1)
    for d, h2 in zip(poles, squares):
        if x == d:
            raise ValueError('secular_at_pole')
        result += Fraction(h2, d-x)
    return result


def certify_root(k, j, a, scale, mus, poles, squares, context):
    wall_start = time.perf_counter()
    cpu_start = time.process_time()
    center = Fraction(scale*scale*(2*a+mus[j]))
    radius = Fraction(scale*scale, 30)
    lo, hi = center-radius, center+radius
    context.update(k=k, pole_index=j, initial_lo=fraction_object(lo),
                   initial_hi=fraction_object(hi))
    if not poles[j] < lo < hi or (j+1 < len(poles) and not hi < poles[j+1]):
        raise ValueError('initial_interval_pole_placement')
    flo = secular(lo, poles, squares)
    fhi = secular(hi, poles, squares)
    context.update(initial_f_lo=fraction_digest(flo), initial_f_hi=fraction_digest(fhi))
    if not flo < 0 < fhi:
        raise ValueError('initial_secular_sign')
    initial = dict(lo=fraction_object(lo), hi=fraction_object(hi),
                   f_lo=fraction_digest(flo), f_hi=fraction_digest(fhi))
    decisions = []
    collapsed = False
    for step in range(BISECTIONS):
        mid = (lo+hi)/2
        fm = secular(mid, poles, squares)
        decision = dict(step=step, midpoint=fraction_object(mid), f=fraction_digest(fm))
        context['current_decision'] = decision
        decisions.append(decision)
        if fm == 0:
            lo = hi = mid
            collapsed = True
            break
        if fm < 0:
            lo = mid
        else:
            hi = mid
    if not collapsed and not secular(lo, poles, squares) < 0 < secular(hi, poles, squares):
        raise ValueError('final_secular_sign')
    lower_numerator, upper_normalizer = Fraction(0), Fraction(0)
    for i, (d, h2) in enumerate(zip(poles, squares)):
        ell = min(abs(lo-d), abs(hi-d))
        upper_distance = max(abs(lo-d), abs(hi-d))
        if ell <= 0:
            raise ValueError('final_interval_at_pole')
        if i < k:
            lower_numerator += Fraction(h2, upper_distance*upper_distance)
        upper_normalizer += Fraction(h2, ell*ell)
    if not 0 < lower_numerator < upper_normalizer:
        raise ValueError('crossmass_bound_domain')
    lower_crossmass = lower_numerator/upper_normalizer
    floor_value = (lower_crossmass.numerator*(1 << DYADIC_BITS))//lower_crossmass.denominator
    if not 0 <= floor_value < (1 << DYADIC_BITS):
        raise ValueError('dyadic_floor_range')
    return dict(record_type='root', k=k, pole_index=j, initial=initial,
                final=dict(lo=fraction_object(lo), hi=fraction_object(hi)),
                bisection_decisions=decisions, actual_decisions=len(decisions),
                requested_bisections=BISECTIONS, exact_root_collapse=collapsed,
                lower_numerator=fraction_digest(lower_numerator),
                upper_normalizer=fraction_digest(upper_normalizer),
                lower_crossmass=fraction_digest(lower_crossmass),
                dyadic_bits=DYADIC_BITS, dyadic_floor=floor_value,
                root_wall_seconds=time.perf_counter()-wall_start,
                root_cpu_seconds=time.process_time()-cpu_start, **FLAGS)


def validate_witness(row):
    k = row['k']
    if type(k) is not int or k not in (1, 2, 61):
        raise ValueError('witness_rank')
    m, h = row['diagonal_integers'], row['appended_row_integers']
    if len(m) != 2*k or len(h) != 2*k:
        raise ValueError('witness_coordinate_inventory')
    if any(type(x) is not int or x <= 0 for x in m+h):
        raise ValueError('witness_not_positive_integer')
    a, scale = int(row['a_hex'], 16), int(row['scale_hex'], 16)
    if a != 16**k or scale != 128*k*4**k:
        raise ValueError('witness_scale')
    expected_mus = sorted([-(16**i//2) for i in range(1, k+1)]+[2*16**i for i in range(1, k+1)])
    mus = [int(v, 16) for v in row['target_parent_mu_hex']]
    if mus != expected_mus:
        raise ValueError('witness_parent_root_inventory')
    poles = [v*v for v in m]
    if not all(x < y for x, y in zip(poles, poles[1:])):
        raise ValueError('non_strict_poles')
    return k, m, h, a, scale, mus, poles, [v*v for v in h]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in EXPECTED:
        parser.add_argument('--'+name.replace('_', '-'), type=Path, required=True)
    parser.add_argument('--mode', choices=('calibration', 'full'), required=True)
    parser.add_argument('--output-directory', type=Path, required=True)
    args = parser.parse_args()
    output = args.output_directory
    output.mkdir(parents=False, exist_ok=False)
    raw = output/'projector-certificate.jsonl'
    partial = output/'projector-certificate.jsonl.partial'
    summary_path = output/'projector-summary.json'
    stream = partial.open('xb')
    digest = hashlib.sha256()
    intended_bytes = 0
    intended_rows = []
    context = dict(mode=args.mode, argv=sys.argv, completed_roots=0, **FLAGS)
    start_wall, start_cpu = time.perf_counter(), time.process_time()
    try:
        provenance = {}
        for name, expected in EXPECTED.items():
            path = getattr(args, name)
            if path.is_symlink() or not path.is_file():
                raise ValueError('not_regular_input:'+name)
            data = path.read_bytes()
            actual = sha(data)
            context.update(checking_input=name, actual_sha256=actual, expected_sha256=expected)
            if actual != expected:
                raise ValueError('input_hash:'+name)
            provenance[name] = dict(path=str(path), bytes=len(data), sha256=actual)
        witness_data = args.witness.read_bytes()
        witness_lines = witness_data.splitlines()
        witness_rows = [json.loads(line) for line in witness_lines]
        if [r['k'] for r in witness_rows] != [1, 2, 61]:
            raise ValueError('all_witness_rank_inventory')

        def record(obj):
            nonlocal intended_bytes
            data = encoded(obj)
            digest.update(data)
            intended_bytes += len(data)
            intended_rows.append(obj)
            write_all(stream, data)

        record(dict(record_type='provenance', mode=args.mode, inputs=provenance,
                    source_sha256=sha(Path(__file__).read_bytes()),
                    fraction_encoding='canonical sorted compact JSON; reduced hex numerator/positive denominator',
                    witness_source_commit='066361e4d3e816fbc6ca4863f74a9afb12dfcaeb', **FLAGS))
        rank_summaries = []
        root_records = []
        for row, line in zip(witness_rows, witness_lines):
            k, m, h, a, scale, mus, poles, squares = validate_witness(row)
            if args.mode == 'full' and k != 61:
                continue
            indices = list(range(k, 2*k))
            if args.mode == 'calibration' and k == 61:
                indices = [61, 121]
            complete = indices == list(range(k, 2*k))
            record(dict(record_type='rank_input', k=k, dimension=2*k,
                        witness_line_sha256=sha(line), diagonal_integers=m,
                        appended_row_integers=h, a_hex=hex(a), scale_hex=hex(scale),
                        target_parent_mu_hex=[hex(v) for v in mus], root_indices=indices,
                        complete_topk_inventory=complete, **FLAGS))
            rank_roots = []
            for j in indices:
                root_record = certify_root(k, j, a, scale, mus, poles, squares, context)
                record(root_record)
                rank_roots.append(root_record)
                root_records.append(root_record)
                context['completed_roots'] += 1
            floor_sum = sum(r['dyadic_floor'] for r in rank_roots)
            recourse_bound = Fraction(2*floor_sum, 1 << DYADIC_BITS) if complete else None
            target_applicable = args.mode == 'full' and k == 61 and complete
            rank_summaries.append(dict(k=k, root_indices=indices, completed_roots=len(rank_roots),
                                       complete_topk_inventory=complete,
                                       recourse_lower_bound=fraction_object(recourse_bound) if complete else None,
                                       target_applicable=target_applicable,
                                       target_strictly_greater_than_8=(recourse_bound > 8) if target_applicable else None,
                                       target_verdict=('certified' if recourse_bound > 8 else 'inconclusive') if target_applicable else 'not_applicable', **FLAGS))
        stream.close()
        raw_receipt = publish(partial, raw, intended_bytes, digest.hexdigest())
        decoded = [json.loads(line) for line in raw.read_bytes().splitlines()]
        if decoded != intended_rows:
            raise ValueError('raw_semantic_readback')
        if args.mode == 'calibration':
            costs = [r['root_wall_seconds'] for r in root_records if r['k'] == 61]
            if len(costs) != 2:
                raise ValueError('calibration_root_cost_inventory')
            envelope = 61*4*max(costs)+30
        else:
            envelope = None
        summary = dict(format='exact-integer-projector-certificate-v1', mode=args.mode,
                       arithmetic_completed=True, ranks=rank_summaries, raw=raw_receipt,
                       raw_records=len(intended_rows), source_sha256=sha(Path(__file__).read_bytes()),
                       prospective_full_cost_envelope_seconds=envelope,
                       cost_envelope_is_planning_heuristic_not_worstcase_proof=True,
                       script_wall_before_summary_seconds=time.perf_counter()-start_wall,
                       script_cpu_before_summary_seconds=time.process_time()-start_cpu,
                       maximum_self_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                       timestamps=dict(completed_before_summary_at=datetime.now(timezone.utc).isoformat()), **FLAGS)
        data = encoded(summary)
        summary_partial = summary_path.with_name(summary_path.name+'.partial')
        with summary_partial.open('xb') as handle:
            write_all(handle, data)
        summary_receipt = publish(summary_partial, summary_path, len(data), sha(data))
        if json.loads(summary_path.read_bytes()) != summary:
            raise ValueError('summary_semantic_readback')
        # Recheck both actual output identities after the summary publication.
        for path, expected in ((raw, raw_receipt), (summary_path, summary_receipt)):
            blob = path.read_bytes()
            if len(blob) != expected['bytes'] or sha(blob) != expected['sha256']:
                raise ValueError('final_post_publication_identity')
        print(json.dumps(dict(status='completed', mode=args.mode, outputs=[raw_receipt, summary_receipt], **FLAGS)))
    except BaseException as error:
        if not stream.closed:
            stream.flush()
            os.fsync(stream.fileno())
            stream.close()
        # A later failure cannot retain an apparently successful summary name.
        if summary_path.exists():
            failed_summary = summary_path.with_name(summary_path.name+'.failed')
            os.link(summary_path, failed_summary)
            summary_path.unlink()
            sync_directory(output)
        failure = dict(status='failed', exception_type=type(error).__name__,
                       exception_message=str(error), context=context,
                       intended_rows=len(intended_rows), intended_bytes=intended_bytes,
                       intended_sha256=digest.hexdigest(),
                       wall_seconds=time.perf_counter()-start_wall,
                       cpu_seconds=time.process_time()-start_cpu, **FLAGS)
        with (output/'failure.json').open('xb') as handle:
            write_all(handle, encoded(failure))
        sync_directory(output)
        raise


if __name__ == '__main__':
    main()
