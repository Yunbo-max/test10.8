"""Attributed existing FD comparator certificate qualification; no new method."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import hashlib,json,resource,time
from pathlib import Path
import numpy as np
from atomic_npz import atomic_savez,atomic_write_json

HERE=Path(__file__).resolve().parent
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))

class ExistingFD:
    def __init__(self,ell,d,augmented=False):
        self.ell=ell;self.B=np.zeros((ell,d));self.next=0;self.delta=0.;self.decomps=0;self.augmented=augmented
    def step(self,x):
        if self.augmented:
            zeros=np.flatnonzero(~np.any(self.B,axis=1))
            if len(zeros):
                self.B[int(zeros[0])]=x;self.next=self.ell
                self.decomps+=1
                return np.linalg.svd(self.B,compute_uv=False)
        if self.next==self.ell:
            Z=np.vstack([self.B,x]) if self.augmented else self.B
            _,s,v=np.linalg.svd(Z,full_matrices=False);self.decomps+=1
            ix=self.ell if self.augmented else self.ell-1
            delta=float(s[ix]**2);self.delta+=delta
            self.B=np.sqrt(np.maximum(s[:self.ell]**2-delta,0.))[:,None]*v[:self.ell]
            self.next=self.ell if self.augmented else self.ell-1
            if self.augmented:
                # Author augmented variant may free additional exactly-zero rows.
                zeros=np.flatnonzero(~np.any(self.B,axis=1))
                if len(zeros): self.next=int(zeros[0])
                self.decomps+=1
                return np.linalg.svd(self.B,compute_uv=False)
        self.B[self.next]=x;self.next+=1
        self.decomps+=1
        return np.linalg.svd(self.B[:self.next],compute_uv=False)

def main():
    w0=time.perf_counter();c0=time.process_time()
    parent=HERE/'LANDMARK128_RAW_V3.npz'
    assert hashlib.sha256(parent.read_bytes()).hexdigest()=='de6f3279d021f8a442cd5f6b51ac4948457045263eb334e6cade78b0380b6dff'
    with np.load(parent,allow_pickle=False) as z: A=z['a'].copy();saved_opt=z['opt'].copy()
    assert A.shape==(128,2704)
    k=25;n,d=A.shape;energy=np.cumsum(np.sum(A*A,axis=1));tol=1e-10*np.maximum(1.,energy)
    ref_s=[];ref_v=[];opt=[];oracle_cpu=[]
    for t in range(1,n+1):
        c=time.process_time();_,s,v=np.linalg.svd(A[:t],full_matrices=False)
        oracle_cpu.append(time.process_time()-c);opt.append(float(s[k:]@s[k:]));ref_s.append(s);ref_v.append(v[:min(k,t)].T)
    opt=np.asarray(opt);oracle_cpu=np.asarray(oracle_cpu)
    assert np.max(np.abs(opt-saved_opt)/np.maximum(1.,energy))<1e-10
    checkpoints=np.unique(np.r_[np.linspace(26,n,8,dtype=int)])
    raw={'a':A,'opt':opt,'energy':energy,'oracle_cpu':oracle_cpu,'checkpoints':checkpoints}
    rows=[];policy=[]
    for ell,aug in [(50,False),(100,False),(50,True)]:
        name=('author_augmented' if aug else 'classic_delayed')+f'_ell{ell}'
        fd=ExistingFD(ell,d,aug);debt_rows=ell+int(aug)
        values={x:[] for x in ['delta','tail','bound','trace_sketch','trace_identity_error','update_cpu']}
        snapshots=[]
        for i,x in enumerate(A):
            c=time.process_time();s=fd.step(x);update_cpu=time.process_time()-c
            tail=float(s[k:]@s[k:]);trace=float(s@s);bound=tail+(debt_rows-k)*fd.delta
            for key,val in [('delta',fd.delta),('tail',tail),('bound',bound),('trace_sketch',trace),('trace_identity_error',energy[i]-trace-debt_rows*fd.delta),('update_cpu',update_cpu)]:values[key].append(val)
            if i+1 in checkpoints:snapshots.append(fd.B.copy())
        for key,val in values.items():raw[name+'_'+key]=np.asarray(val)
        raw[name+'_sketch_checkpoints']=np.asarray(snapshots)
        bound=np.asarray(values['bound']);tail=np.asarray(values['tail']);positive=opt>tol
        rows.append({'variant':name,'capacity':ell,'shrink_trace_factor':debt_rows,'prefixes':n,'near_zero_opt_prefixes':int(np.sum(~positive)),
            'bound_violations':int(np.sum(bound>opt+tol)),
            'max_bound_excess_normalized':float(np.max((bound-opt)/np.maximum(1.,energy))),
            'trace_identity_violations':int(np.sum(np.abs(values['trace_identity_error'])>tol)),
            'min_bound_ratio_positive_opt':float(np.min(bound[positive]/opt[positive])),
            'median_bound_ratio_positive_opt':float(np.median(bound[positive]/opt[positive])),
            'tail_only_median_ratio_positive_opt':float(np.median(tail[positive]/opt[positive])),
            'fd_update_cpu_seconds':float(np.sum(values['update_cpu'])),'decompositions':fd.decomps})
        for eta in [.01,.1]:
            masks=[];queries=[];residuals=[]
            for strong in [False,True]:
                Q=None;cached=0.;qmask=[];umask=[];loss=[]
                for i,x in enumerate(A):
                    t=i+1
                    r=0. if Q is None else float(np.linalg.norm(A[:t]-(A[:t]@Q)@Q.T)**2)
                    lower=cached
                    if strong:lower=max(cached,float(np.max(np.maximum(0.,bound[:t]-tol[:t]))))
                    query=Q is None or t<=k or r>(1+eta)*lower+tol[i]
                    update=Q is None or t<=k
                    if query:
                        cached=max(cached,float(opt[i]-tol[i]),0.)
                        if r>(1+eta)*opt[i]+tol[i]:update=True
                    if update:Q=ref_v[i].copy()
                    qmask.append(query);umask.append(update);loss.append(r)
                masks.append(np.asarray(umask));queries.append(np.asarray(qmask));residuals.append(np.asarray(loss))
            stem=name+f'_eta{eta:g}'
            for label,arr in [('baseline_updated',masks[0]),('strong_updated',masks[1]),('baseline_queried',queries[0]),('strong_queried',queries[1]),('incoming_residual',residuals[0])]:raw[stem+'_'+label]=arr
            policy.append({'variant':name,'eta':eta,'baseline_queries':int(np.sum(queries[0][k:])),
                'strong_queries':int(np.sum(queries[1][k:])), 'refreshes_after_growth':int(np.sum(masks[0][k:])),
                'refresh_mask_differences':int(np.sum(masks[0]!=masks[1])),
                'query_not_subset_count':int(np.sum(queries[1]&~queries[0])),
                'false_queries_removed':int(np.sum(queries[0][k:])-np.sum(queries[1][k:])),
                'oracle_cpu_removed_in_replay':float(np.sum(oracle_cpu[queries[0]&~queries[1]])),
                'oracle_cpu_added_in_replay':float(np.sum(oracle_cpu[queries[1]&~queries[0]])),
                'oracle_cpu_net_saved_in_replay':float(np.sum(oracle_cpu[queries[0]&~queries[1]])-np.sum(oracle_cpu[queries[1]&~queries[0]])),
                'fd_update_cpu_cost':float(np.sum(values['update_cpu'])),
                'timing_status':'single diagnostic measured components, not fair repeated production runtime'})
    passed=all(x['bound_violations']==0 and x['trace_identity_violations']==0 for x in rows) and all(x['refresh_mask_differences']==0 for x in policy)
    receipt=atomic_savez(HERE/'FD_CERTIFICATE_RAW.npz',raw,list(raw))
    out={'study':'B07-existing-FD-certificate-qualification','rows':rows,'policy':policy,'data_array_sha256':hashlib.sha256(A.astype('<f8').tobytes()).hexdigest(),
        'oracle_cpu_total':float(np.sum(oracle_cpu)), 'raw_artifact':receipt,'development_only':True,'full_landmark5000':False,'qualification_pass':passed,
        'usage':{'wall_seconds':time.perf_counter()-w0,'cpu_seconds':time.process_time()-c0,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
    atomic_write_json(HERE/'FD_CERTIFICATE_SUMMARY.json',out)
    print(json.dumps(out,allow_nan=False))
    assert passed, 'Qualification failed; complete raw arrays and failure summary retained'

if __name__=='__main__':main()
