"""Live arithmetic qualification of native512 FD fixed checkpoints."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
import json,resource,time
from pathlib import Path
import numpy as np
from atomic_npz import validate_npz,atomic_write_json
HERE=Path(__file__).resolve().parent
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3));w=time.perf_counter();c=time.process_time()
valid=validate_npz(HERE/'LANDMARK512_FD_RAW.npz',['a','checkpoints','checkpoint_opt'])
with np.load(HERE/'LANDMARK512_FD_RAW.npz',allow_pickle=False) as z:r={key:z[key] for key in z.files}
A=r['a'];k=25;E=np.cumsum(np.einsum('ij,ij->i',A,A));rows=[]
for name,factor in [('classic_delayed_ell50',50),('classic_delayed_ell100',100),('author_augmented_ell50',51)]:
    for j,t in enumerate(r['checkpoints']):
        B=r[name+'_sketch_checkpoints'][j];delta=float(r[name+'_delta'][t-1]);tol=1e-10*max(1.,E[t-1])
        vals=np.linalg.eigvalsh(A[:t]@A[:t].T)[::-1];opt=float(np.sum(np.maximum(vals[k:],0.)))
        sb=np.linalg.eigvalsh(B@B.T)[::-1];generic=E[t-1]-float(np.sum(sb[:k]))-k*delta
        _,R=np.linalg.qr(np.vstack([A[:t],B]).T,mode='reduced');signs=np.r_[np.ones(t),-np.ones(len(B))]
        eig=np.linalg.eigvalsh((R*signs)@R.T)
        checks={'bound_vs_gram':bool(r[name+'_bound'][t-1]<=opt+tol),'opt_gram_vs_svd':bool(abs(opt-r['checkpoint_opt'][j])<=tol),
            'generic_lower_identity':bool(abs(generic-r[name+'_bound'][t-1])<=tol),
            'trace_loss':bool(abs(E[t-1]-np.sum(B*B)-factor*delta)<=tol),
            'loewner_lower':bool(eig[0]>=-tol),'loewner_upper':bool(eig[-1]<=delta+tol)}
        rows.append({'variant':name,'prefix':int(t),'opt_gram':opt,'opt_svd':float(r['checkpoint_opt'][j]),
            'bound':float(r[name+'_bound'][t-1]),'covariance_min':float(eig[0]),'covariance_max':float(eig[-1]),'delta':delta,'tolerance':float(tol),'checks':checks})
passed=all(all(x['checks'].values()) for x in rows)
out={'audit_pass':passed,'checkpoint_variant_pairs':len(rows),'scalar_predicates':6*len(rows),'records':rows,'raw_sha256':valid['sha256'],
    'scope':'8fixed exact checkpoints x3 FD variants, not continuous512quality or production timing',
    'usage':{'wall_seconds':time.perf_counter()-w,'cpu_seconds':time.process_time()-c,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
atomic_write_json(HERE/'LANDMARK512_FD_LIVE_AUDIT.json',out);print(json.dumps({k:v for k,v in out.items() if k!='records'}));assert passed,'Live audit failure retained'
