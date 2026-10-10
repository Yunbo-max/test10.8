"""Independent arithmetic path over frozen native FD evidence; no new scorer."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
import json,time,resource
from pathlib import Path
import numpy as np
from atomic_npz import atomic_write_json,validate_npz
HERE=Path(__file__).resolve().parent
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
w=time.perf_counter();c=time.process_time()
inventory=validate_npz(HERE/'FD_CERTIFICATE_RAW.npz',['a','opt','energy','checkpoints'])
with np.load(HERE/'FD_CERTIFICATE_RAW.npz',allow_pickle=False) as z:raw={key:z[key] for key in z.files}
A=raw['a'];k=25;n,d=A.shape;E=np.asarray([np.linalg.norm(A[:t])**2 for t in range(1,n+1)]);tol=1e-10*np.maximum(1.,E)
gram_opts=[]
for t in range(1,n+1):
    vals=np.linalg.eigvalsh(A[:t]@A[:t].T)[::-1]
    gram_opts.append(float(np.sum(np.maximum(vals[k:],0.))))
gram_opts=np.asarray(gram_opts);records=[]
for name,debtrows in [('classic_delayed_ell50',50),('classic_delayed_ell100',100),('author_augmented_ell50',51)]:
    checks=[]
    for j,t in enumerate(raw['checkpoints']):
        B=raw[name+'_sketch_checkpoints'][j];S=B@B.T
        spectrum=np.maximum(np.linalg.eigvalsh(S)[::-1],0.)
        delta=float(raw[name+'_delta'][t-1]);generic=E[t-1]-float(np.sum(spectrum[:k]))-k*delta
        # Thin QR preserves the nonzero spectrum of the signed covariance difference.
        _,R=np.linalg.qr(np.vstack([A[:t],B]).T,mode='reduced')
        signs=np.r_[np.ones(t),-np.ones(len(B))]
        eigdiff=np.linalg.eigvalsh((R*signs)@R.T)
        record={'prefix':int(t),'generic_bound':generic,'stored_bound':float(raw[name+'_bound'][t-1]),
            'generic_difference_normalized':float(abs(generic-raw[name+'_bound'][t-1])/max(1.,E[t-1])),
            'trace_identity_error':float(E[t-1]-np.sum(B*B)-debtrows*delta),
            'covariance_min_eigenvalue':float(min(0.,eigdiff[0])),
            'covariance_max_eigenvalue':float(max(0.,eigdiff[-1])),
            'delta_certificate':delta,
            'pass':bool(abs(generic-raw[name+'_bound'][t-1])<=tol[t-1] and abs(E[t-1]-np.sum(B*B)-debtrows*delta)<=tol[t-1] and eigdiff[0]>=-tol[t-1] and eigdiff[-1]<=delta+tol[t-1])}
        checks.append(record)
    records.append({'variant':name,'allprefix_scalar_bound_violations_vs_gram':int(np.sum(raw[name+'_bound']>gram_opts+tol)),
        'allprefix_trace_identity_violations':int(np.sum(abs(E-raw[name+'_trace_sketch']-debtrows*raw[name+'_delta'])>tol)),
        'checkpoint_covariance_checks':checks})
summary=json.loads((HERE/'FD_CERTIFICATE_SUMMARY.json').read_text());policy=[]
for row in summary['policy']:
    stem=row['variant']+f"_eta{row['eta']:g}";qb=raw[stem+'_baseline_queried'];qs=raw[stem+'_strong_queried'];ub=raw[stem+'_baseline_updated'];us=raw[stem+'_strong_updated']
    cpu=raw['oracle_cpu'];net=float(np.dot(cpu,qb.astype(float)-qs.astype(float)))
    policy.append({'variant':row['variant'],'eta':row['eta'],'baseline_only_queries':int(np.sum((qb&~qs)[k:])),
        'strong_only_queries':int(np.sum((qs&~qb)[k:])), 'net_query_difference':int(np.sum(qb[k:])-np.sum(qs[k:])),
        'update_mask_difference':int(np.sum(ub!=us)),
        'net_cpu_component_error':abs(net-row['oracle_cpu_net_saved_in_replay']),
        'summary_count_pass':bool(int(np.sum(qb[k:]))==row['baseline_queries'] and int(np.sum(qs[k:]))==row['strong_queries'] and int(np.sum(ub[k:]))==row['refreshes_after_growth'])})
passed=bool(np.all(np.abs(gram_opts-raw['opt'])<=tol) and np.all(abs(E-raw['energy'])<=tol) and all(r['allprefix_scalar_bound_violations_vs_gram']==0 and r['allprefix_trace_identity_violations']==0 and all(x['pass'] for x in r['checkpoint_covariance_checks']) for r in records) and all(x['update_mask_difference']==0 and x['summary_count_pass'] and x['net_cpu_component_error']<1e-10 for x in policy))
out={'audit_pass':passed,'prefix_gram_opt_checks':n,'variant_prefix_bound_checks':3*n,'covariance_checkpoint_checks':24,
    'max_opt_gram_vs_svd_normalized_error':float(np.max(abs(gram_opts-raw['opt'])/np.maximum(1.,E))),
    'records':records,'policy':policy,'raw_sha256':inventory['sha256'],'independent_arithmetic':True,
    'independent_scientific_confirmation':False,'usage':{'wall_seconds':time.perf_counter()-w,'cpu_seconds':time.process_time()-c,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
atomic_write_json(HERE/'FD_LIVE_AUDIT.json',out);print(json.dumps({k:v for k,v in out.items() if k not in ['records','policy']},allow_nan=False))
assert passed,'Raw audit failure retained'
