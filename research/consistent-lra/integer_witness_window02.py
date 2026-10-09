"""Generated unexecuted exact-integer witness constructor for an accepted lemma audit.

No project import, floating square root, matrix evaluation or measured recourse.
Separately reviewed source and finite plan required before executing this file.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import sys
import time

EXPECTED = {
    'contract': '497b7edd245ae7fe802ca4d7aa92a73c33cd98ced0bc2bf7761ce28f52d2e41f',
    'draft': 'd0f56dbf1ec12c302ad2b42e8ae608a06c9c6c2da63b50da2ee11f6ec8fede79',
    'review': 'bc239b1819de5657b481bd776a17bc949b4fdf305e9f69d742b92bf23fd9d003',
}
FLAGS = dict(scientific_gate_advanced=False, native_evaluator_qualified=False,
             empirical_projector_recourse_computed=False, eigenvalues_computed=False,
             block_condition_computed=False, novelty_qualified=False,
             performance_claim_eligible=False, confirmation=False)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(data):
    return (json.dumps(data, sort_keys=True, allow_nan=False)+'\n').encode()


def write_all(stream, data):
    offset = 0
    while offset < len(data):
        written = stream.write(data[offset:])
        if not written:
            raise IOError('short_write')
        offset += written
    stream.flush()
    os.fsync(stream.fileno())


def finalize(partial, final):
    data = partial.read_bytes()
    os.link(partial, final)  # exclusive, no replacement
    partial.unlink()
    fd = os.open(final.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    if final.read_bytes() != data:
        raise ValueError('publication_readback')
    return dict(path=final.name, bytes=len(data), sha256=sha(data))


def publish(final, data):
    partial = final.with_name(final.name+'.partial')
    with partial.open('xb') as stream:
        write_all(stream, data)
    if partial.read_bytes() != data:
        raise ValueError('partial_readback')
    return finalize(partial, final)


def bracket(radical, scale, context):
    numerator, denominator = radical.numerator, radical.denominator
    if numerator <= 0 or denominator <= 0:
        raise ValueError('nonpositive_radicand')
    scaled = 4*scale*scale*numerator
    q = scaled // denominator
    n = math.isqrt(q)
    rounded = (n+1)//2
    lower = (2*rounded-1)**2*denominator if rounded else 0
    upper = (2*rounded+1)**2*denominator
    record = dict(radicand_numerator_hex=hex(numerator),
                  radicand_denominator_hex=hex(denominator),
                  scaled_numerator_hex=hex(scaled), q_hex=hex(q),
                  isqrt_hex=hex(n), rounded_integer=rounded,
                  lower_residual_hex=hex(scaled-lower),
                  strict_upper_residual_hex=hex(upper-scaled))
    context['current_entry'] = record
    if not n*n <= q < (n+1)*(n+1):
        raise ValueError('isqrt_bracket')
    if not lower <= scaled < upper:
        raise ValueError('rounding_bracket')
    return record


def witness(k, context):
    a, scale = 16**k, 128*k*4**k
    lambdas = sorted([-16**i for i in range(1,k+1)]+[16**i for i in range(1,k+1)])
    mus = sorted([-(16**i//2) for i in range(1,k+1)]+[2*16**i for i in range(1,k+1)])
    if len(lambdas) != 2*k or len(set(lambdas)) != 2*k or lambdas[0] != -a:
        raise ValueError('lambda_inventory')
    entry_bound = 257*k*a
    bit_bound = 4*k+(k-1).bit_length()+9
    entries, diagonal, appended = [], [], []
    for coordinate, lam in enumerate(lambdas):
        context.update(k=k, coordinate=coordinate, lambda_hex=hex(lam))
        signed_num = -math.prod(lam-mu for mu in mus)
        signed_den = math.prod(lam-nu for nu in lambdas if nu != lam)
        context.update(signed_numerator_hex=hex(signed_num), signed_denominator_hex=hex(signed_den))
        residue = Fraction(signed_num, signed_den)
        if residue <= 0:
            raise ValueError('nonpositive_residue')
        d = bracket(Fraction(2*a+lam), scale, context)
        h = bracket(residue, scale, context)
        pair = (d['rounded_integer'], h['rounded_integer'])
        if any(type(v) is not int or v <= 0 or v > entry_bound or v.bit_length() > bit_bound for v in pair):
            raise ValueError('integer_entry_bound')
        diagonal.append(pair[0]); appended.append(pair[1])
        entries.append(dict(coordinate=coordinate, lambda_hex=hex(lam),
                            signed_residue_product_numerator_hex=hex(signed_num),
                            signed_residue_product_denominator_hex=hex(signed_den),
                            diagonal_rounding=d, appended_rounding=h))
    if len(entries) != 2*k or len(diagonal)+len(appended) != 4*k:
        raise ValueError('integer_inventory')
    return dict(format='exact-integer-lemma-witness-v1',k=k,dimension=2*k,
                a_hex=hex(a),scale_hex=hex(scale),lambda_order_hex=[hex(v) for v in lambdas],
                target_parent_mu_hex=[hex(v) for v in mus],
                diagonal_integers=diagonal,appended_row_integers=appended,
                reconstruction='old A=diag(diagonal); new T=[A; appended_row]',
                entries=entries,entry_bound_hex=hex(entry_bound),bit_bound=bit_bound,
                actual_max_entry=max(diagonal+appended),actual_max_bit_length=max(v.bit_length() for v in diagonal+appended),
                rounding_entries_verified=4*k,passed=True,
                analytic_projector_and_condition_claim_basis='accepted v7 proof; not measured by this constructor',**FLAGS)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('contract','draft','review','output-directory'):
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--ranks',type=int,nargs='+',required=True)
    args = parser.parse_args()
    if tuple(args.ranks) != (1,2,61):
        raise ValueError('unapproved_ranks')
    args.output_directory.mkdir(exist_ok=False,parents=False)
    final = args.output_directory/'integer-witnesses.jsonl'
    partial = final.with_name(final.name+'.partial')
    stream = partial.open('xb')
    context = dict(argv=sys.argv,recorded_rank_count=0,**FLAGS)
    start = time.perf_counter(); before = resource.getrusage(resource.RUSAGE_SELF)
    try:
        provenance = {}
        for name,expected_hash in EXPECTED.items():
            path = getattr(args,name)
            if path.is_symlink() or not path.is_file():
                raise ValueError('not_regular_input:'+name)
            data = path.read_bytes(); actual = sha(data)
            context.update(checking_input=name,actual_sha256=actual,expected_sha256=expected_hash)
            if actual != expected_hash:
                raise ValueError('input_hash_mismatch:'+name)
            provenance[name] = dict(path=str(path),bytes=len(data),sha256=actual)
        rows = []; intended_hash = hashlib.sha256(); intended_length = 0
        for k in args.ranks:
            row = witness(k,context)
            row['provenance'] = provenance
            intended = encoded(row)
            intended_hash.update(intended); intended_length += len(intended)
            write_all(stream,intended); rows.append(row)
            context['recorded_rank_count'] = len(rows)
        stream.close()
        expected_hash = intended_hash.hexdigest()
        context.update(expected_records_sha256=expected_hash,expected_records_bytes=intended_length)
        partial_data = partial.read_bytes()
        if len(partial_data) != intended_length or sha(partial_data) != expected_hash:
            raise ValueError('intended_partial_bytes_mismatch')
        decoded_rows = [json.loads(line) for line in partial_data.splitlines()]
        if decoded_rows != rows or [r['k'] for r in decoded_rows] != [1,2,61] or len(decoded_rows) != 3 or sum(len(r['diagonal_integers'])+len(r['appended_row_integers']) for r in decoded_rows) != 256:
            raise ValueError('rank_inventory_semantic_readback')
        output_ref = finalize(partial,final)
        if output_ref['bytes'] != intended_length or output_ref['sha256'] != expected_hash:
            raise ValueError('intended_final_bytes_mismatch')
        after = resource.getrusage(resource.RUSAGE_SELF)
        summary = dict(format='exact-integer-witness-summary-v1',ranks=args.ranks,
                       rank_records=len(rows),integer_entries=sum(4*r['k'] for r in rows),
                       per_rank=[dict(k=r['k'],dimension=r['dimension'],bit_bound=r['bit_bound'],
                                      actual_max_bit_length=r['actual_max_bit_length']) for r in rows],
                       output_ref=output_ref,provenance=provenance,argv=sys.argv,
                       observed_at=datetime.now(timezone.utc).isoformat(),
                       usage=dict(pipeline_before_summary_seconds=time.perf_counter()-start,
                                  process_cpu_seconds=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,
                                  maximum_rss_kib=after.ru_maxrss),**FLAGS)
        summary_ref = publish(args.output_directory/'integer-witnesses-summary.json',encoded(summary))
        for ref in (output_ref,summary_ref):
            data = (args.output_directory/ref['path']).read_bytes()
            if len(data) != ref['bytes'] or sha(data) != ref['sha256']:
                raise ValueError('postpublication_hash')
        print(json.dumps(dict(outputs=[output_ref,summary_ref],**FLAGS)),flush=True)
    except BaseException as err:
        if not stream.closed:
            stream.flush(); os.fsync(stream.fileno()); stream.close()
        summary_path = args.output_directory/'integer-witnesses-summary.json'
        quarantined_summary = None
        if summary_path.exists():
            failed_path = args.output_directory/'integer-witnesses-summary.failed.json'
            intended_summary_bytes = summary_path.read_bytes()
            os.link(summary_path,failed_path)
            if failed_path.read_bytes() != intended_summary_bytes:
                raise ValueError('failure_summary_quarantine_readback') from err
            summary_path.unlink()
            fd = os.open(args.output_directory,os.O_RDONLY | os.O_DIRECTORY)
            try:os.fsync(fd)
            finally:os.close(fd)
            quarantined_summary = dict(path=failed_path.name,bytes=len(intended_summary_bytes),sha256=sha(intended_summary_bytes))
        failure = dict(context=context,quarantined_summary=quarantined_summary,error_type=type(err).__name__,error=str(err),
                       partial_records_path=partial.name if partial.exists() else final.name,
                       success=False,**FLAGS)
        publish(args.output_directory/'integer-witnesses-failure.json',encoded(failure))
        raise


if __name__ == '__main__':
    main()
