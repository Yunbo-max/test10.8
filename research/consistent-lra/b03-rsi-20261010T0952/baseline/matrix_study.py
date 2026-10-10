"""Frozen native-data robustness matrix. Single-thread, CPU-only, no paid API."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import argparse, hashlib, json, math, resource, sys, time
from pathlib import Path
import numpy as np
from scipy.io import arff
from sklearn import datasets

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
OUT = HERE / 'results'
METHODS = ['exact_eigh','certified_full','boundary','fixed_gap','energy','periodic','hold','fd2','fd4']
RANKS = {'skin':[1,2], 'rice':[1,3], 'wine':[1,4], 'cancer':[4,12], 'digits':[4,16]}

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def dump(path, value):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
def load_data(name):
    if name == 'skin':
        path=PROJECT/'data/Skin_NonSkin.txt'
        assert digest(path)=='008f1fb6a169498dec54fb5951be6478e5465942cc4f6df3b5dabbe484c9a98f'
        return np.loadtxt(path)[:3000,:3], {'source_sha256':digest(path),'source':'author-released Skin_NonSkin.txt','released_prefix':3000}
    if name == 'rice':
        path=PROJECT/'data/Rice_Cammeo_Osmancik.arff'
        assert digest(path)=='1af97883100c89de2ea2972f7a28d428f4f1c14711a61defc0b0569e9eb65665'
        data,_=arff.loadarff(path)
        return np.column_stack([data[f] for f in data.dtype.names[:-1]]).astype(float), {'source_sha256':digest(path),'source':'author-released Rice_Cammeo_Osmancik.arff'}
    data={'wine':datasets.load_wine,'cancer':datasets.load_breast_cancer,'digits':datasets.load_digits}[name]()
    a=np.asarray(data.data,dtype=float)
    return a, {'source':'sklearn bundled native '+name,'feature_names':[str(x) for x in data.feature_names],
               'raw_array_sha256':hashlib.sha256(a.astype('<f8').tobytes()).hexdigest()}

def prepare(name, order, preprocessing='calibration'):
    raw,meta=load_data(name); ids=np.arange(len(raw))
    if order!='native': ids=np.random.default_rng(int(order.split('-')[-1])).permutation(ids)
    a=raw[ids].copy(); burn=min(128,len(a)//5)
    if preprocessing=='raw': mean=np.zeros(a.shape[1]); std=np.ones(a.shape[1])
    else:
        fit=a[:burn] if preprocessing=='calibration' else a
        mean=fit.mean(axis=0);std=fit.std(axis=0);std[std==0.0]=1.0
    a=(a-mean)/std
    meta.update({'shape':list(a.shape),'burn':burn,'order':order,'preprocessing':preprocessing,
                 'matrix_sha256':hashlib.sha256(a.astype('<f8').tobytes()).hexdigest()})
    return a,ids,mean,std,meta

def eig(G,k,t):
    vals,V=np.linalg.eigh(G);r=min(k,t)
    return V[:,-r:].copy(),max(0.0,float(np.sum(vals[:-r])))

def boundary_path(Q,V,G,E,target,tol):
    """Feasible interpolation; no claim of global minimum movement."""
    left,s,right=np.linalg.svd(Q.T@V,full_matrices=False)
    B=Q@left; Z=V@right.T
    s=np.clip(s,0.0,1.0)
    D=Z-B*s
    sn=np.linalg.norm(D,axis=0); angles=np.arctan2(sn,s)
    active=sn>1e-8
    U=np.zeros_like(D);U[:,active]=D[:,active]/sn[active]
    # Almost shared directions use the old column; numerical fallback retains V.
    aa=np.sum(B*(G@B),axis=0);bb=np.sum(B*(G@U),axis=0);cc=np.sum(U*(G@U),axis=0)
    def loss(alpha):
        ca=np.cos(alpha*angles);sa=np.sin(alpha*angles)
        return E-float(np.sum(aa*ca*ca+2*bb*sa*ca+cc*sa*sa))
    if loss(1.0)>target+tol: return V.copy(),True
    lo,hi=0.0,1.0
    for _ in range(48):
        mid=(lo+hi)/2
        if loss(mid)<=target:hi=mid
        else:lo=mid
    W=B*np.cos(hi*angles)+U*np.sin(hi*angles)
    W=np.linalg.qr(W,mode='reduced')[0]
    if E-float(np.sum(W*(G@W)))>target+tol: return V.copy(),True
    return W,False

class Arm:
    def __init__(self,d,k,eta,method,burn):
        self.d,self.k,self.eta,self.method,self.burn=d,k,eta,method,burn
        self.G=np.zeros((d,d));self.E=0.;self.Q=None;self.held=0.;self.cached=0.
        self.at_refresh=0.;self.refreshes=0;self.queries=0;self.fallbacks=0;self.decompositions=0
        self.ell=min(d,(2 if method=='fd2' else 4)*k)
        self.B=np.zeros((self.ell,d));self.next=0
    def optimum(self,t):
        self.queries+=1;V,opt=eig(self.G,self.k,t)
        self.cached=max(self.cached,opt-1e-10*max(1.,self.E),0.)
        return V,opt
    def step(self,x,t):
        self.G+=np.outer(x,x);self.E+=float(x@x)
        tol=1e-10*max(1.,self.E)
        if self.Q is not None:self.held+=max(0.,float(x@x)-float(np.sum((x@self.Q)**2)))
        changed=False
        if self.method.startswith('fd'):
            if self.next==self.ell:
                _,sv,vh=np.linalg.svd(self.B,full_matrices=False);self.decompositions+=1
                self.B=np.sqrt(np.maximum(sv**2-sv[-1]**2,0.))[:,None]*vh
                self.next=self.ell-1
            self.B[self.next]=x;self.next+=1
            _,sv,vh=np.linalg.svd(self.B[:self.next],full_matrices=False);self.decompositions+=1
            self.Q=vh[:min(self.k,t)].T.copy();changed=True
        elif self.Q is None or t<=self.k:
            self.Q,_=self.optimum(t);changed=True
        elif self.method=='exact_eigh':
            self.Q,_=self.optimum(t);changed=True
        elif self.method in ('hold','periodic','energy'):
            refresh=(t<=self.burn) or (self.method=='periodic' and (t-self.burn)%50==0) or (self.method=='energy' and self.E>=(1+self.eta)*self.at_refresh)
            if refresh:self.Q,_=self.optimum(t);changed=True
        elif self.held>(1+self.eta)*self.cached+tol:
            V,opt=self.optimum(t)
            if self.held>(1+self.eta)*opt+tol:
                if self.method=='certified_full':self.Q=V
                else:
                    target=(1+self.eta-(.005 if self.method=='fixed_gap' else 0.))*opt
                    self.Q,fallback=boundary_path(self.Q,V,self.G,self.E,target,tol)
                    self.fallbacks+=int(fallback)
                changed=True
        if changed:
            self.refreshes+=1;self.at_refresh=self.E
            self.held=max(0.,self.E-float(np.sum(self.Q*(self.G@self.Q))))
        return self.Q,changed

def overlap_increment(Q,previous):
    return max(0.,Q.shape[1]+previous.shape[1]-2.*float(np.sum((Q.T@previous)**2)))

def run_arm(a,k,eta,method,burn,opt,checkpoints,path):
    arm=Arm(a.shape[1],k,eta,method,burn)
    n=len(a);field={x:np.zeros(n) for x in ('loss','increment','recourse','energy','update_wall','update_cpu')}
    updates=np.zeros(n,dtype=bool);queries=np.zeros(n,dtype=bool)
    previous=None;total=0.;snapshots=[];prev_snapshots=[];previous_rank=[];ranks=[]
    max_identity_error=0.;max_orth_error=0.;checkset=set(checkpoints)
    for i,x in enumerate(a):
        q0=arm.queries; w=time.perf_counter();c=time.process_time()
        Q,changed=arm.step(x,i+1)
        field['update_cpu'][i]=time.process_time()-c;field['update_wall'][i]=time.perf_counter()-w
        updates[i]=changed;queries[i]=arm.queries>q0
        inc=0. if previous is None else (overlap_increment(Q,previous) if changed else 0.)
        total+=inc
        loss=max(0.,arm.E-float(np.sum(Q*(arm.G@Q))))
        field['loss'][i]=loss;field['energy'][i]=arm.E;field['increment'][i]=inc;field['recourse'][i]=total
        if i+1 in checkset:
            pad=np.zeros((a.shape[1],k));pad[:,:Q.shape[1]]=Q;snapshots.append(pad);ranks.append(Q.shape[1])
            padprev=np.zeros_like(pad)
            if previous is not None:padprev[:,:previous.shape[1]]=previous
            prev_snapshots.append(padprev);previous_rank.append(0 if previous is None else previous.shape[1])
        if changed:
            max_orth_error=max(max_orth_error,float(np.max(np.abs(Q.T@Q-np.eye(Q.shape[1])))))
            if previous is not None:
                direct=float(np.sum((Q@Q.T-previous@previous.T)**2))
                max_identity_error=max(max_identity_error,abs(direct-inc))
        previous=Q.copy()
    tol=1e-10*np.maximum(1.,field['energy']);mask=np.arange(n)>=burn;positive=opt>tol
    violations=(field['loss']>(1+eta)*opt+1.01*tol)&mask
    ratio=field['loss'][mask&positive]/opt[mask&positive]
    np.savez_compressed(path,**field,opt=opt,updated=updates,queried=queries,checkpoints=checkpoints,
                        basis=np.array(snapshots),previous_basis=np.array(prev_snapshots),rank=ranks,previous_rank=previous_rank)
    return {'method':method,'certificate_violations':int(violations.sum()),'scored_prefixes':int(mask.sum()),
            'near_zero_opt_count':int((mask&~positive).sum()),'max_ratio_positive_opt':float(ratio.max()) if len(ratio) else None,
            'recourse':float(np.sum(field['increment'][mask])),'total_recourse':total,'max_increment':float(np.max(field['increment'][mask])),
            'refreshes':int(updates[mask].sum()),'queries':int(queries[mask].sum()),'total_exact_queries':arm.queries,
            'fd_decompositions':arm.decompositions,'fallbacks':arm.fallbacks,
            'update_wall_seconds':float(field['update_wall'].sum()),'update_cpu_seconds':float(field['update_cpu'].sum()),
            'max_recourse_identity_error':max_identity_error,'max_orthogonality_error':max_orth_error,
            'raw_file':path.name,'raw_sha256':digest(path)}

def scenario(name,order,k,eta,prep='calibration',prefix='primary'):
    start=time.perf_counter();cpu=time.process_time();a,ids,mean,std,meta=prepare(name,order,prep)
    folder=OUT/prefix/f'{name}-{order}-k{k}-eta{eta:g}-{prep}';folder.mkdir(parents=True,exist_ok=True)
    if (folder/'report.json').exists():raise RuntimeError('immutable scenario already exists')
    np.savez_compressed(folder/'input.npz',a=a,row_ids=ids,mean=mean,std=std)
    G=np.zeros((a.shape[1],a.shape[1]));opt=np.zeros(len(a));oracle_start=time.perf_counter()
    for i,x in enumerate(a):
        G+=np.outer(x,x);vals=np.linalg.eigvalsh(G);opt[i]=max(0.,float(np.sum(vals[:-min(k,i+1)])))
    oracle_wall=time.perf_counter()-oracle_start
    checkpoints=np.unique(np.r_[np.arange(1,min(k+2,len(a))+1),np.linspace(meta['burn']+1,len(a),32,dtype=int)])
    methods=METHODS.copy()
    if min(a.shape[1],2*k)==min(a.shape[1],4*k):methods.remove('fd4')
    # Deterministic randomized execution order; isolated timing is a separate task.
    seed=int(hashlib.sha256(str(folder.name).encode()).hexdigest()[:8],16)
    rng=np.random.default_rng(seed);rng.shuffle(methods)
    rows=[run_arm(a,k,eta,m,meta['burn'],opt,checkpoints,folder/(m+'.npz')) for m in methods]
    report={'dataset':name,'order':order,'k':k,'eta':eta,'preprocessing':prep,'metadata':meta,
            'results':rows,'oracle_wall_seconds':oracle_wall,'input_sha256':digest(folder/'input.npz'),
            'source_sha256':digest(__file__),'design_sha256':digest(HERE/'EXPERIMENT_DESIGN.md'),
            'usage':{'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,
                     'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
    dump(folder/'report.json',report)
    print(json.dumps({'case':folder.name,'arms':len(rows),'wall':report['usage']['wall_seconds'],
                       'violations':{r['method']:r['certificate_violations'] for r in rows}}),flush=True)

def fixtures():
    results=[]
    for a in [np.zeros((20,4)),np.tile([1.,2.,3.,4.],(30,1)),np.tile(np.eye(4),(20,1))]:
        for k in (1,3):
            G=np.zeros((4,4));opt=[]
            for i,x in enumerate(a):G+=np.outer(x,x);opt.append(eig(G,k,i+1)[1])
            for method in ('exact_eigh','certified_full','boundary','fixed_gap'):
                arm=Arm(4,k,.01,method,4)
                for i,x in enumerate(a):
                    Q,_=arm.step(x,i+1);direct=float(np.sum((a[:i+1]-(a[:i+1]@Q)@Q.T)**2))
                    assert direct<=(1.01)*opt[i]+1e-8*max(1.,arm.E)
                    assert np.linalg.norm(Q.T@Q-np.eye(Q.shape[1]))<1e-7
                results.append({'k':k,'method':method,'n':len(a)})
    dump(OUT/'fixtures.json',{'cases':results,'pass':True})
    print(json.dumps({'fixtures':len(results),'pass':True}))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--dataset',choices=list(RANKS));parser.add_argument('--mode',choices=['primary','ablation','pilot','fixtures'],default='primary')
    args=parser.parse_args();OUT.mkdir(exist_ok=True)
    limit=2*1024**3;resource.setrlimit(resource.RLIMIT_AS,(limit,limit))
    if args.mode=='fixtures':fixtures();return
    if args.mode=='pilot':scenario('digits','native',4,.01,prefix='pilot');return
    if args.mode=='ablation':
        for name in ('skin','rice'):
            for k in RANKS[name]:
                for eta in (.01,.03,.1):
                    for prep in ('raw','full_offline'):scenario(name,'native',k,eta,prep,'ablation')
        return
    for order in ['native']+[f'perm-{x}' for x in range(5)]:
        for k in RANKS[args.dataset]:
            for eta in (.01,.03,.1):scenario(args.dataset,order,k,eta)

if __name__=='__main__':main()
