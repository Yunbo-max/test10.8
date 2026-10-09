"""Generated, unexecuted isolated scalar engineering qualifier. No matrix scoring.

Parse fixed sources; execute only reviewed AST-selected scalar expressions and
pure accumulation functions in closed namespaces. Never import a project module.
Requires separately admitted source/fixture/plan review before execution.
"""
import argparse
import ast
import copy
from datetime import datetime, timezone
from fractions import Fraction as F
import gzip
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import sys
import time

SOURCE_HASH = '12fa733061a4ec93983cafeb0fbed7af31b19f85c0d1ab875be8de3803457f5e'
HELPER_HASH = 'aba46507a5b60f4b39d237418b79566ed9b8dd6aee9d65586e8ac7d3031bd16a'
SUMMARY_HASH = 'a0523b88fbc96adae1f035ce9c9974a0d3ae9fe97f3e7ff782c363e6177f6ae7'
MANIFEST_HASH = '26c10453a0af471bd3d6c9b089292a7a444f878a56ef2ab351a27aa5212df84a'
REVIEW_HASH = '65d566101933c540a6f1e879418f6c1f72f7b186a20bfe4f9c8851bdf015d714'
FIXTURE_HASH = '02a7569f3673e4483f5397580510a967e1aef7e502cf3957eae1b1b9b1e7f0bc'
INPUTS = ('energy', 'gram_opt', 'direct_opt', 'gram_loss', 'direct_loss', 't', 'rec')
TARGETS = ('tolerance', 'band', 'opt_fallback', 'opt', 'near_zero', 'loss_fallback',
           'loss', 'increment', 'ratio', 'excess')
DICT_KEYS = ('energy_normalized_excess', 'near_zero_positive_loss_violation',
             'opt_source', 'loss_source')
FIELDS = ('raw_gram_opt', 'opt', 'raw_gram_loss', 'loss', 'energy', 'ratio',
          'additive_excess', 'energy_normalized_excess', 'primary_increment',
          'cumulative_recourse', 'steady_recourse', 'orthogonality_error',
          'update_seconds', 'scoring_seconds', 'shared_reference_seconds',
          'shared_energy_maintenance_seconds')
PREFIXES = tuple(range(1, 26)) + (50,100,150,250,500,1000,2000,3000,4000,5000)
ARMS = ('algorithm4-c1.1','algorithm4-c2.0','algorithm4-c2.5','algorithm4-c5.0',
        'algorithm4-c10.0','algorithm4-c100.0','fresh','fixed','periodic-10',
        'periodic-100','fd-ell50','fd-ell100','author-fd-ell50')
FALSE_FLAGS = dict(native_evaluator_qualified=False,
                   nearzero_matrix_fallback_qualified=False,
                   stage_b_execution_admitted=False, scientific_gate_advanced=False,
                   performance_claim_eligible=False, confirmation=False)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def checked_bytes(path, expected):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise ValueError('not_regular_input')
    data = path.read_bytes()
    if digest(data) != expected:
        raise ValueError('input_hash_mismatch:' + str(path))
    return data


def unique(items, label):
    if len(items) != 1:
        raise ValueError('nonunique_source:' + label)
    return items[0]


def dump(node):
    return ast.dump(node, include_attributes=False)


def target_name(node):
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        return node.targets[0].id
    return None


def extract(source_path, helper_path):
    source = checked_bytes(source_path, SOURCE_HASH).decode('utf-8')
    helper = checked_bytes(helper_path, HELPER_HASH).decode('utf-8')
    tree, ht = ast.parse(source), ast.parse(helper)
    main = unique([n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main'], 'main')
    n_node = unique([n for n in ht.body if target_name(n) == 'N'], 'helper N')
    if ast.literal_eval(n_node.value) != 5000:
        raise ValueError('changed_N')
    imports = [n for n in tree.body if isinstance(n, ast.ImportFrom) and n.module == 'landmark_stage_a_v2' and any(a.name == 'N' for a in n.names)]
    imp = unique(imports, 'N import')
    if any(a.asname for a in imp.names):
        raise ValueError('aliased_N_import')
    f_node = unique([n for n in tree.body if target_name(n) == 'DESCRIPTIVE_FIELDS'], 'fields')
    if ast.literal_eval(f_node.value) != FIELDS:
        raise ValueError('changed_fields')
    selected = [unique([n for n in ast.walk(main) if target_name(n) == name], name) for name in TARGETS]
    selected.sort(key=lambda n:n.lineno)
    row = unique([n for n in ast.walk(main) if target_name(n) == 'row'], 'row').value
    if not isinstance(row, ast.Dict):
        raise ValueError('row_not_dict')
    for key in DICT_KEYS:
        value = unique([v for k,v in zip(row.keys,row.values) if isinstance(k,ast.Constant) and k.value == key], key)
        selected.append(ast.Assign(targets=[ast.Name(id=key,ctx=ast.Store())],value=copy.deepcopy(value)))
    scalar_allowed = (ast.Module,ast.Assign,ast.Name,ast.Load,ast.Store,ast.Constant,
                      ast.BinOp,ast.Mult,ast.Sub,ast.Div,ast.Call,ast.Compare,
                      ast.LtE,ast.Gt,ast.Eq,ast.IfExp,ast.BoolOp,ast.Or,ast.And)
    scalar = ast.fix_missing_locations(ast.Module(body=copy.deepcopy(selected),type_ignores=[]))
    names = set(INPUTS+TARGETS+DICT_KEYS+('max',))
    for node in ast.walk(scalar):
        if not isinstance(node, scalar_allowed):
            raise ValueError('scalar_ast_not_allowed:' + type(node).__name__)
        if isinstance(node,ast.Name) and node.id not in names:
            raise ValueError('scalar_name_not_allowed')
        if isinstance(node,ast.Call) and (not isinstance(node.func,ast.Name) or node.func.id!='max' or len(node.args)!=2 or node.keywords):
            raise ValueError('scalar_call_not_allowed')
    functions = [unique([n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name], name) for name in ('new_slice','add_slice')]
    accumulator = ast.Module(body=copy.deepcopy(functions),type_ignores=[])
    allowed = (ast.Module,ast.FunctionDef,ast.arguments,ast.arg,ast.Return,ast.Dict,
               ast.List,ast.DictComp,ast.comprehension,ast.Assign,ast.AugAssign,
               ast.Add,ast.Expr,ast.If,ast.IfExp,ast.For,ast.Subscript,ast.Constant,
               ast.Name,ast.Load,ast.Store,ast.Call,ast.Attribute,ast.Compare,
               ast.Is,ast.IsNot)
    local_names = {'new_slice','add_slice','first','stat','row','normalized','field','value','ratio','N','DESCRIPTIVE_FIELDS','int','max'}
    append_shape = dump(ast.parse('stat["_metric_values"][field].append(value)',mode='eval').body)
    int_shape = dump(ast.parse('int(row["near_zero_positive_loss_violation"])',mode='eval').body)
    max_shape = dump(ast.parse('max(ratio,stat["maximum_defined_ratio"])',mode='eval').body)
    for node in ast.walk(accumulator):
        if not isinstance(node,allowed):
            raise ValueError('accumulator_ast_not_allowed:' + type(node).__name__)
        if isinstance(node,ast.Name) and node.id not in local_names:
            raise ValueError('accumulator_name_not_allowed:' + node.id)
        if isinstance(node,ast.Attribute) and node.attr!='append':
            raise ValueError('accumulator_attribute_not_allowed')
        if isinstance(node,ast.Call) and dump(node) not in (append_shape,int_shape,max_shape):
            raise ValueError('accumulator_call_not_allowed')
        if isinstance(node,ast.FunctionDef) and (node.decorator_list or node.returns or node.args.defaults or node.args.kw_defaults or node.args.vararg or node.args.kwarg):
            raise ValueError('function_signature_not_allowed')
    namespace = {'__builtins__':{},'N':5000,'DESCRIPTIVE_FIELDS':FIELDS,'int':int,'max':max}
    exec(compile(ast.fix_missing_locations(accumulator),'<reviewed-accumulator>','exec'),namespace)
    segments=[]
    for n in selected[:len(TARGETS)]+functions+[n_node,f_node]:
        text = ast.get_source_segment(helper if n is n_node else source,n)
        segments.append({'line':n.lineno,'end_line':n.end_lineno,'sha256':digest(text.encode()),'source':text})
    return compile(scalar,'<reviewed-scalar>','exec'),namespace,dict(
        scalar_ast_sha256=digest(dump(scalar).encode()),
        accumulator_ast_sha256=digest(dump(accumulator).encode()),source_segments=segments,
        scalar_source_hash=SOURCE_HASH,helper_hash=HELPER_HASH,
        row_value_expression_ast={key:dump(selected[len(TARGETS)+i].value) for i,key in enumerate(DICT_KEYS)})


def validate_input(x):
    if set(x) != set(INPUTS):
        raise ValueError('unexpected_fields')
    if type(x['t']) is not int or x['t']<1:
        raise ValueError('invalid_prefix')
    for key in INPUTS:
        if key=='t':
            continue
        v=x[key]
        if v is None and key in ('direct_opt','direct_loss'):
            continue
        if type(v) not in (float,int) or not math.isfinite(v) or v<0:
            raise ValueError('nonfinite_or_negative')
    tau=float(F(1e-10)*F(max(1.,x['energy'])))
    band=float(F(10)*F(tau))
    if x['gram_opt']<=band and x['direct_opt'] is None:
        raise ValueError('missing_direct_input')
    opt=x['direct_opt'] if x['gram_opt']<=band else x['gram_opt']
    if (opt<=tau or x['gram_loss']<=band) and x['direct_loss'] is None:
        raise ValueError('missing_direct_input')


def decode(x):
    return {k:float.fromhex(v) if k!='t' and isinstance(v,str) else v for k,v in x.items()}


def expected(x):
    # Independent arithmetic staging: exact input ratios, rounded per operation.
    energy=F(x['energy']); scale=energy if energy>1 else F(1)
    tau=float(F(1e-10)*scale); band=float(F(tau)*10)
    route_opt=x['gram_opt']<=band
    opt=x['direct_opt'] if route_opt else x['gram_opt']
    near=not opt>tau
    route_loss=near or not x['gram_loss']>band
    loss=x['direct_loss'] if route_loss else x['gram_loss']
    excess=float(F(loss)-F(opt))
    return dict(tolerance=tau,band=band,opt_fallback=route_opt,opt=opt,near_zero=near,
                loss_fallback=route_loss,loss=loss,increment=x['rec'] if x['t']>1 else 0.,
                ratio=float(F(loss)/F(opt)) if not near else None,excess=excess,
                energy_normalized_excess=float(F(excess)/energy) if energy>0 else None,
                near_zero_positive_loss_violation=near and loss>tau,
                opt_source='direct_svd_fallback' if route_opt else 'qualified_gram',
                loss_source='direct_residual_fallback' if route_loss else 'qualified_gram')


def equal(actual,reference):
    if reference is None or type(reference) in (bool,str,int):
        return type(actual) is type(reference) and actual==reference
    return type(actual) is float and math.isfinite(actual) and abs(actual-reference)<=4*math.ulp(reference)


def compare(actual,reference):
    if set(actual)!=set(reference):
        raise ValueError('output_field_mismatch')
    bad=[key for key in reference if not equal(actual[key],reference[key])]
    if bad:
        raise ValueError('scalar_disagreement:'+','.join(bad))


def evaluate(code,x):
    validate_input(x)
    ns={'__builtins__':{},'max':max,**x}
    exec(code,ns)
    result={k:ns[k] for k in TARGETS+DICT_KEYS}
    compare(result,expected(x))
    return result


def recorded_rows(manifest_path,summary_path):
    manifest=json.loads(checked_bytes(manifest_path,MANIFEST_HASH))
    summary=json.loads(checked_bytes(summary_path,SUMMARY_HASH))
    if manifest['rows']!=455 or tuple(manifest['expected_prefixes'])!=PREFIXES or len(manifest['members'])!=35 or tuple(summary['arms'])!=ARMS:
        raise ValueError('native_packet_inventory')
    parent=Path(manifest_path).parent; records=[]; identities=[]
    for prefix,member in zip(PREFIXES,manifest['members']):
        name=f'landmark-stage-a-v2-qualification.oracles.jsonl.prefix-{prefix:05d}.gz'
        if member['path']!=name or member['prefix']!=prefix or member['rows']!=13:
            raise ValueError('member_inventory')
        data=checked_bytes(parent/name,member['sha256'])
        if len(data)!=member['bytes'] or member['plain_bytes']>32*1024*1024:
            raise ValueError('member_size')
        plain=gzip.decompress(data)
        if len(plain)!=member['plain_bytes'] or digest(plain)!=member['uncompressed_sha256']:
            raise ValueError('plain_hash')
        lines=plain.splitlines(keepends=True)
        if len(lines)!=13 or any(not line.endswith(b'\n') for line in lines):
            raise ValueError('native_member_rows')
        for arm,line in zip(ARMS,lines):
            row=json.loads(line)
            if row['prefix']!=prefix or row['arm']!=arm or row['sample_id']!=f'landmark:row:{prefix}':
                raise ValueError('native_identity')
            x=dict(energy=row['energy'],gram_opt=row['gram_opt'],direct_opt=row['direct_svd_opt'],gram_loss=row['gram_loss'],direct_loss=row['direct_loss'],t=prefix,rec=row['overlap_recourse'])
            # Stored bases are not used or evaluated; only supplied scalar values.
            records.append((f'{prefix}:{arm}',x,dict(member=name,member_sha256=member['sha256'],record_sha256=digest(line))))
        identities.append({'path':name,'bytes':len(data),'sha256':digest(data)})
    return records,identities


def accumulator_tests(namespace,fixtures,outputs):
    byid={c['id']:c for c in fixtures['cases']}
    ids=fixtures['accumulator_case_ids']
    if len(ids)!=7 or len(set(ids))!=7 or any(i not in byid for i in ids):
        raise ValueError('accumulator_fixture_ids')
    stat=namespace['new_slice'](1); rows=[]; results=[]
    for index,caseid in enumerate(ids,1):
        x=decode(byid[caseid]['inputs']); v=outputs[caseid]
        row={field:0.0 for field in FIELDS}
        row.update(prefix=index,loss=v['loss'],opt=v['opt'],energy=x['energy'],ratio=v['ratio'],
                   raw_gram_opt=x['gram_opt'],raw_gram_loss=x['gram_loss'],
                   additive_excess=v['excess'],energy_normalized_excess=v['energy_normalized_excess'],
                   primary_increment=v['increment'],near_zero_positive_loss_violation=v['near_zero_positive_loss_violation'])
        rows.append(row);namespace['add_slice'](stat,row)
        ratio_values=[r['ratio'] for r in rows if r['ratio'] is not None]
        norm_values=[r['energy_normalized_excess'] for r in rows if r['energy_normalized_excess'] is not None]
        counts=dict(prefix_count=index,ratio_denominator=len(ratio_values),ratio_missing_count=index-len(ratio_values),
                    energy_normalized_excess_denominator=len(norm_values),energy_normalized_excess_missing_count=index-len(norm_values),
                    near_zero_positive_loss_violations=sum(r['ratio'] is None and r['near_zero_positive_loss_violation'] for r in rows))
        if any(type(stat[k]) is not int or stat[k]!=v for k,v in counts.items()) or stat['first_prefix']!=1 or stat['last_prefix']!=5000:
            raise ValueError('accumulator_counts')
        sums={'loss_sum':'loss','opt_sum':'opt','excess_sum':'additive_excess','energy_normalized_excess_sum':'energy_normalized_excess','ratio_sum':'ratio'}
        for dest,field in sums.items():
            vals=[r[field] for r in rows if r[field] is not None]
            ref=float(sum((F(val) for val in vals),F(0)))
            if not equal(stat[dest],ref):
                raise ValueError('accumulator_sum:'+dest)
        for field in FIELDS:
            if stat['_metric_values'][field]!=[r[field] for r in rows if r[field] is not None]:
                raise ValueError('accumulator_values')
        if stat['maximum_defined_ratio']!=(max(ratio_values) if ratio_values else None):
            raise ValueError('accumulator_max')
        if stat['final_endpoint']!={'prefix':index,**{f:row[f] for f in FIELDS}}:
            raise ValueError('accumulator_endpoint')
        results.append(dict(case_id=caseid,append_index=index,counts=counts,passed=True,
                            scope='software_fixture_accumulator_only',**FALSE_FLAGS))
    empty=namespace['new_slice'](150)
    if empty['prefix_count']!=0 or empty['ratio_denominator']!=0 or empty['maximum_defined_ratio'] is not None:
        raise ValueError('empty_accumulator')
    return results


def publish(path,data):
    partial=path.with_name(path.name+'.partial')
    with partial.open('xb') as f:
        offset=0
        while offset<len(data):
            n=f.write(data[offset:])
            if not n:
                raise IOError('short_write')
            offset+=n
        f.flush();os.fsync(f.fileno())
    if partial.read_bytes()!=data:
        raise ValueError('partial_readback')
    os.link(partial,path);partial.unlink()
    fd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)
    if path.read_bytes()!=data:
        raise ValueError('publication_readback')
    return dict(path=path.name,bytes=len(data),sha256=digest(data))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('source','helper','summary','oracle-manifest','accepted-review','fixtures','output-directory'):
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--fixtures-sha256',required=True)
    args=parser.parse_args(); start=time.perf_counter(); before=resource.getrusage(resource.RUSAGE_SELF)
    checked_bytes(args.accepted_review,REVIEW_HASH)
    if args.fixtures_sha256!=FIXTURE_HASH:
        raise ValueError('fixture_contract_hash')
    fixtures=json.loads(checked_bytes(args.fixtures,FIXTURE_HASH))
    if fixtures['format']!='scalar-engineering-fixtures-v1' or fixtures['qualification_executed'] is not False or len(fixtures['cases'])!=22 or len(fixtures['reject_cases'])!=12:
        raise ValueError('fixture_inventory')
    allids=[c['id'] for c in fixtures['cases']+fixtures['reject_cases']]
    if len(set(allids))!=34:
        raise ValueError('fixture_duplicate_id')
    args.output_directory.mkdir(exist_ok=False,parents=False)
    code,namespace,extraction=extract(args.source,args.helper)
    native,input_members=recorded_rows(args.oracle_manifest,args.summary)
    result=[]; fixture_outputs={}
    for caseid,x,lineage in native:
        actual=evaluate(code,x)
        result.append(dict(id=caseid,scope='derived_scalar_contract_only',lineage=lineage,
                           source_outputs=actual,expected_outputs=expected(x),passed=True,**FALSE_FLAGS))
    for case in fixtures['cases']:
        if case['scope']!='software_fixture_only':
            raise ValueError('fixture_scope')
        x=decode(case['inputs']);actual=evaluate(code,x)
        # Decode float expected hex fields; bool/string classifications stay exact.
        frozen={k:float.fromhex(v) if isinstance(v,str) and (v.startswith(('0x','-0x'))) else v for k,v in case['expected'].items()}
        compare(actual,frozen);fixture_outputs[case['id']]=actual
        result.append(dict(id=case['id'],scope=case['scope'],source_outputs=actual,expected_outputs=frozen,passed=True,**FALSE_FLAGS))
    for case in fixtures['reject_cases']:
        if case['scope']!='runner_input_rejection_only':
            raise ValueError('rejection_scope')
        try:validate_input(decode(case['inputs']))
        except ValueError as err:
            if str(err)!=case['expected_error']:
                raise ValueError('wrong_rejection:'+case['id']) from err
        else:raise ValueError('unrejected_invalid_input:'+case['id'])
        result.append(dict(id=case['id'],scope=case['scope'],expected_error=case['expected_error'],passed=True,**FALSE_FLAGS))
    accum=accumulator_tests(namespace,fixtures,fixture_outputs)
    raw=b''.join((json.dumps(r,sort_keys=True,allow_nan=False)+'\n').encode() for r in result+accum)
    refs=[publish(args.output_directory/'scalar-contract-records.jsonl',raw)]
    after=resource.getrusage(resource.RUSAGE_SELF)
    summary=dict(format='isolated-scalar-contract-engineering-v1',native_recorded_scalars=455,
                 software_fixtures=22,input_rejections=12,accumulator_appends=7,raw_record_count=496,
                 qualified_scope='finite_source_scalar_routing_missingness_normalization_and_accumulation_only',
                 full5000_summary_qualified=False,final_summary_reducer_qualified=False,
                 argv=sys.argv,extraction=extraction,input_members=input_members,
                 fixture_sha256=args.fixtures_sha256,outputs=refs,
                 observed_at=datetime.now(timezone.utc).isoformat(),
                 usage=dict(pipeline_before_summary_seconds=time.perf_counter()-start,
                            process_cpu_seconds=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,
                            maximum_rss_kib=after.ru_maxrss),**FALSE_FLAGS)
    if len(result+accum)!=496:
        raise ValueError('output_denominator')
    refs.append(publish(args.output_directory/'scalar-contract-summary.json',(json.dumps(summary,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()))
    manifest=dict(format='scalar-contract-output-manifest-v1',outputs=refs,
                  raw_record_count=496,scope='finite_engineering_only',**FALSE_FLAGS)
    refs.append(publish(args.output_directory/'scalar-contract-manifest.json',(json.dumps(manifest,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()))
    for ref in refs:
        checked_bytes(args.output_directory/ref['path'],ref['sha256'])
    print(json.dumps(dict(outputs=refs,scientific_gate_advanced=False)),flush=True)


if __name__=='__main__':
    main()
