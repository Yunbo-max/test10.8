"""Frozen B03 native replay/parity/timing; original datasets and scoring retained."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import pathlib,sys,argparse,time,resource,json,random,hashlib
import numpy as np
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'baseline'))
import matrix_study as ms
import fast_boundary as fast
OLD=fast.LEGACY
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))

def cases():
    for name in ms.RANKS:
        for k in ms.RANKS[name]:
            for eta in (.01,.03,.1):yield name,k,eta

def parity():
    rows=[];all_calls=[];failures=[]
    out=HERE/'parity';out.mkdir(exist_ok=True)
    for name,k,eta in cases():
        a,ids,mean,std,meta=ms.prepare(name,'native');n,d=a.shape;case=f'{name}-k{k}-eta{eta:g}'
        checks=[]
        def check_old(Q,V,G,E,target,tol):
            R,rf=OLD(Q,V,G,E,target,tol);W,wf=fast.boundary_path(Q,V,G,E,target,tol)
            diff=float(np.linalg.norm(W@W.T-R@R.T));loss=E-float(np.sum(W*(G@W)))
            orth=float(np.linalg.norm(W.T@W-np.eye(W.shape[1])))
            # Independent direct basis evaluation of the frozen coefficients.
            p=fast.coefficients(Q,V,G,E);formula=0.
            for alpha in (0.,.25,.5,.75,1.):
                U=p['B']*np.cos(alpha*p['angles'])+p['U']*np.sin(alpha*p['angles'])
                v,_=fast.value_derivative(p,alpha)
                formula=max(formula,abs(v-(E-float(np.trace(U.T@G@U)))))
            finite=bool(np.all(np.isfinite(W)) and np.all(np.isfinite(R)) and np.all(np.isfinite([diff,loss,target,tol,orth,formula])))
            checks.append({'projector_diff':diff,'loss':loss,'target':target,'tol':tol,'orth':orth,'legacy_target_fallback':rf,'new_target_fallback':wf,'formula_diff':formula,'finite':finite})
            return R,rf
        old=ms.Arm(d,k,eta,'boundary',meta['burn']);new=ms.Arm(d,k,eta,'boundary',meta['burn'])
        records={key:[] for key in ('old_loss','new_loss','opt','old_increment','new_increment','old_changed','new_changed','energy')}
        prev_old=prev_new=None
        for i,x in enumerate(a):
            ms.boundary_path=check_old;qo,co=old.step(x,i+1)
            ms.boundary_path=fast.boundary_path;qn,cn=new.step(x,i+1)
            vals=np.linalg.eigvalsh(old.G);opt=max(0.,float(vals[:-min(k,i+1)].sum()))
            values=(old.E-float(np.trace(qo.T@old.G@qo)),new.E-float(np.trace(qn.T@new.G@qn)),opt,
                    0. if prev_old is None else float(np.sum((qo@qo.T-prev_old@prev_old.T)**2)),
                    0. if prev_new is None else float(np.sum((qn@qn.T-prev_new@prev_new.T)**2)),co,cn,old.E)
            for key,val in zip(records,values):records[key].append(val)
            prev_old=qo.copy();prev_new=qn.copy()
        ms.boundary_path=OLD
        f={key:np.asarray(val) for key,val in records.items()};tol=1e-10*np.maximum(1.,f['energy']);burn=meta['burn']
        rec_old=float(f['old_increment'].sum());rec_new=float(f['new_increment'].sum())
        cum_old=np.cumsum(f['old_increment']);cum_new=np.cumsum(f['new_increment'])
        scored_old=np.cumsum(f['old_increment'][burn:]);scored_new=np.cumsum(f['new_increment'][burn:])
        row={'case':case,'dataset':name,'k':k,'eta':eta,'metadata':meta,'n':n,'calls':len(checks),
             'change_mismatches':int(np.sum(f['old_changed']!=f['new_changed'])),
             'new_violations':int(np.sum(f['new_loss']>(1+eta)*f['opt']+1.01*tol)),
             'old_violations':int(np.sum(f['old_loss']>(1+eta)*f['opt']+1.01*tol)),
             'max_relative_loss_diff':float(np.max(abs(f['new_loss']-f['old_loss'])/np.maximum(1.,abs(f['old_loss'])))),
             'total_old_recourse':rec_old,'total_new_recourse':rec_new,
             'scored_old_recourse':float(f['old_increment'][burn:].sum()),'scored_new_recourse':float(f['new_increment'][burn:].sum()),
             'same_state_max_projector_diff':max((c['projector_diff'] for c in checks),default=0.),
             'same_state_feasibility_failures':sum(c['loss']>c['target']+c['tol'] for c in checks),
             'same_state_orth_failures':sum(c['orth']>1e-8 for c in checks),
             'same_state_fallback_mismatches':sum(c['legacy_target_fallback']!=c['new_target_fallback'] for c in checks),
             'same_state_nonfinite':sum(not c['finite'] for c in checks),
             'same_state_formula_failures':sum(c['formula_diff']>c['tol'] for c in checks),
             'same_state_formula_error':max((c['formula_diff'] for c in checks),default=0.),
             'all_records_finite':all(bool(np.all(np.isfinite(v))) for v in f.values()),
             'max_cumulative_relative_recourse_diff':float(np.max(abs(cum_old-cum_new)/np.maximum(1.,cum_old))),
             'max_scored_cumulative_relative_recourse_diff':float(np.max(abs(scored_old-scored_new)/np.maximum(1.,scored_old))),
             'relative_recourse_diff':abs(rec_old-rec_new)/max(1.,rec_old)}
        passed=(row['all_records_finite'] and row['change_mismatches']==row['old_violations']==row['new_violations']==row['same_state_feasibility_failures']==row['same_state_orth_failures']==row['same_state_fallback_mismatches']==row['same_state_nonfinite']==row['same_state_formula_failures']==0 and row['max_relative_loss_diff']<=1e-6 and row['max_cumulative_relative_recourse_diff']<=1e-6 and row['max_scored_cumulative_relative_recourse_diff']<=1e-6 and row['relative_recourse_diff']<=1e-6 and row['same_state_max_projector_diff']<=5e-7)
        row['passed']=passed
        if not passed:failures.append(case)
        np.savez_compressed(out/(case+'.npz'),**f,row_ids=ids,final_old=old.Q,final_new=new.Q)
        ms.dump(out/(case+'.json'),{'summary':row,'calls':checks});rows.append(row)
        ms.dump(HERE/'PARITY_PARTIAL.json',{'rows':rows,'failures':failures})
        print(json.dumps({'case':case,'passed':passed,'max_diff':row['same_state_max_projector_diff'],'changes':row['change_mismatches']}),flush=True)
    return {'rows':rows,'failures':failures,'passed':not failures,'counts':dict(fast.COUNTS),'complete_cells':len(rows)}

def timing():
    qualification=json.loads((HERE/'PARITY.json').read_text())
    assert qualification['passed'] and qualification['complete_cells']==30
    assert qualification['fast_source_sha256']==ms.digest(fast.__file__)
    assert qualification['base_source_sha256']==ms.digest(ms.__file__)
    assert qualification['source_sha256']==ms.digest(__file__)
    qualified_inputs={(r['dataset'],r['k'],r['eta']):r['metadata']['matrix_sha256'] for r in qualification['rows']}
    rng=random.Random(2026101013);rows=[]
    for name,k,eta in cases():
        a,_,_,_,meta=ms.prepare(name,'native');trials={m:[] for m in ('certified_full','legacy','newton')}
        assert meta['matrix_sha256']==qualified_inputs[(name,k,eta)]
        for repeat in range(5):
            order=list(trials);rng.shuffle(order)
            for method in order:
                ms.boundary_path=fast.boundary_path if method=='newton' else OLD
                arm=ms.Arm(a.shape[1],k,eta,'certified_full' if method=='certified_full' else 'boundary',meta['burn'])
                w=time.perf_counter();c=time.process_time()
                for i,x in enumerate(a):arm.step(x,i+1)
                tc=time.process_time()-c;tw=time.perf_counter()-w
                trials[method].append({'repeat':repeat,'order':order,'cpu_seconds':tc,'wall_seconds':tw,'queries':arm.queries,'updates':arm.refreshes,'target_fallbacks':arm.fallbacks,'final_projector_sha256':hashlib.sha256((arm.Q@arm.Q.T).tobytes()).hexdigest()})
        row={'dataset':name,'k':k,'eta':eta,'trials':trials}
        cpu={m:float(np.median([t['cpu_seconds'] for t in tr])) for m,tr in trials.items()}
        row.update(median_cpu=cpu,legacy_over_newton=cpu['legacy']/cpu['newton'],full_over_newton=cpu['certified_full']/cpu['newton'])
        rows.append(row);ms.dump(HERE/'TIMING_PARTIAL.json',{'rows':rows})
        print(json.dumps({key:row[key] for key in ('dataset','k','eta','legacy_over_newton','full_over_newton')}),flush=True)
    ms.boundary_path=OLD
    return {'rows':rows,'whole_method_runs':len(rows)*15,'counts':dict(fast.COUNTS)}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['parity','timing']);args=ap.parse_args()
    w=time.perf_counter();c=time.process_time();report=parity() if args.mode=='parity' else timing()
    report.update(source_sha256=ms.digest(__file__),fast_source_sha256=ms.digest(fast.__file__),base_source_sha256=ms.digest(ms.__file__),usage={'wall_seconds':time.perf_counter()-w,'cpu_seconds':time.process_time()-c,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
    ms.dump(HERE/(args.mode.upper()+'.json'),report)
    if args.mode=='parity' and not report['passed']:sys.exit(1)
