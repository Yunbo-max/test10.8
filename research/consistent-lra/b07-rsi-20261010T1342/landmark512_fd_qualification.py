"""Native512 existing FD comparator resource/stress qualification at fixed checkpoints."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
import hashlib,json,resource,time
from pathlib import Path
import numpy as np
from scipy.io import mmread
from fd_certificate_audit import ExistingFD
from atomic_npz import atomic_savez,atomic_write_json
HERE=Path(__file__).resolve().parent
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
w=time.perf_counter();c=time.process_time()
p=HERE/'landmark.mtx';sourcehash=hashlib.sha256(p.read_bytes()).hexdigest()
assert sourcehash=='29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b'
M=mmread(p).tocsr();assert M.shape==(71952,2704) and M.nnz==1151232
A=M[:512].toarray();del M
n,d=A.shape;k=25;points=np.asarray([128,160,192,256,320,384,448,512]);energy=np.cumsum(np.sum(A*A,axis=1));tol=1e-10*np.maximum(1.,energy)
opts=[];ranks=[];oracle_cpu=[]
for t in points:
    cc=time.process_time();s=np.linalg.svd(A[:t],compute_uv=False);oracle_cpu.append(time.process_time()-cc)
    opts.append(float(s[k:]@s[k:]));ranks.append(int(np.sum(s*s>tol[t-1])))
raw={'a':A,'energy':energy,'checkpoints':points,'checkpoint_opt':np.asarray(opts),'checkpoint_effective_rank':np.asarray(ranks),'checkpoint_oracle_cpu':np.asarray(oracle_cpu)}
rows=[]
for ell,aug in [(50,False),(100,False),(50,True)]:
    name=('author_augmented' if aug else 'classic_delayed')+f'_ell{ell}';fd=ExistingFD(ell,d,aug);factor=ell+int(aug)
    arrays={x:[] for x in ['bound','delta','tail','trace_sketch','update_cpu','trace_identity_error']};snapshots=[]
    for i,x in enumerate(A):
        cc=time.process_time();s=fd.step(x);cost=time.process_time()-cc
        tail=float(s[k:]@s[k:]);trace=float(s@s);bound=tail+(factor-k)*fd.delta
        for key,v in [('bound',bound),('delta',fd.delta),('tail',tail),('trace_sketch',trace),('update_cpu',cost),('trace_identity_error',energy[i]-trace-factor*fd.delta)]:arrays[key].append(v)
        if i+1 in points:snapshots.append(fd.B.copy())
    for key,val in arrays.items():raw[name+'_'+key]=np.asarray(val)
    raw[name+'_sketch_checkpoints']=np.asarray(snapshots)
    checked_bound=np.asarray(arrays['bound'])[points-1];checked_tol=tol[points-1];optsarr=np.asarray(opts);positive=optsarr>checked_tol
    rows.append({'variant':name,'capacity':ell,'shrink_trace_factor':factor,'rows_processed':n,'exact_opt_checked_prefixes':[int(t) for t in points],
        'bound_checkpoint_violations':int(np.sum(checked_bound>optsarr+checked_tol)),
        'allprefix_trace_identity_violations':int(np.sum(np.abs(arrays['trace_identity_error'])>tol)),
        'positive_delta_prefixes':int(np.sum(np.asarray(arrays['delta'])>0.)),
        'final_delta':float(fd.delta),'final_delta_over_opt':float(fd.delta/opts[-1]) if opts[-1]>checked_tol[-1] else None,
        'bound_ratio_positive_opt_checkpoints':[float(x) for x in checked_bound[positive]/optsarr[positive]],
        'fd_cpu_seconds':float(np.sum(arrays['update_cpu'])),'decompositions':fd.decomps})
passed=all(r['bound_checkpoint_violations']==0 and r['allprefix_trace_identity_violations']==0 for r in rows)
receipt=atomic_savez(HERE/'LANDMARK512_FD_RAW.npz',raw,list(raw))
out={'qualification_pass':passed,'rows':rows,'checkpoint_opt':[float(x) for x in opts],'checkpoint_effective_rank':ranks,
    'oracle_cpu_seconds':sum(oracle_cpu),'native_source_sha256':sourcehash,'a_sha256':hashlib.sha256(A.astype('<f8').tobytes()).hexdigest(),
    'raw_artifact':receipt,'continuous_output_quality_evaluated':False,'newton_parity_promoted':False,'development_only':True,
    'usage':{'wall_seconds':time.perf_counter()-w,'cpu_seconds':time.process_time()-c,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
atomic_write_json(HERE/'LANDMARK512_FD_SUMMARY.json',out);print(json.dumps({k:v for k,v in out.items() if k!='raw_artifact'},allow_nan=False));assert passed,'Qualification failure artifacts retained'
