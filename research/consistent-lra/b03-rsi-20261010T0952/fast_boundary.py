"""B03 root-solver repair; preserves legacy path, scoring and fallback semantics."""
import collections
import numpy as np
import matrix_study as ms

LEGACY=ms.boundary_path
COUNTS=collections.Counter()

def coefficients(Q,V,G,E):
    left,s,right=np.linalg.svd(Q.T@V,full_matrices=False)
    B=Q@left;Z=V@right.T;s=np.clip(s,0.,1.)
    D=Z-B*s;sn=np.linalg.norm(D,axis=0);angles=np.arctan2(sn,s)
    active=sn>1e-8;U=np.zeros_like(D);U[:,active]=D[:,active]/sn[active]
    return {'B':B,'U':U,'sn':sn,'angles':angles,'E':E,
            'aa':np.sum(B*(G@B),axis=0),'bb':np.sum(B*(G@U),axis=0),
            'cc':np.sum(U*(G@U),axis=0)}

def value_derivative(p,a):
    theta=p['angles'];ca=np.cos(a*theta);sa=np.sin(a*theta)
    value=p['E']-float(np.sum(p['aa']*ca*ca+2*p['bb']*sa*ca+p['cc']*sa*sa))
    derivative=-float(np.sum(theta*(2*(p['cc']-p['aa'])*sa*ca+2*p['bb']*(ca*ca-sa*sa))))
    return value,derivative

def boundary_path(Q,V,G,E,target,tol):
    COUNTS['calls']+=1
    def legacy(reason):
        COUNTS['scalar_fallbacks']+=1;COUNTS['fallback_'+reason]+=1
        return LEGACY(Q,V,G,E,target,tol)
    if target<=100*tol:return legacy('near_zero')
    p=coefficients(Q,V,G,E)
    if np.any((p['sn']>0)&(p['sn']<=1e-8)):return legacy('inactive_angle')
    def evaluate(a):
        COUNTS['evaluations']+=1
        return value_derivative(p,a)
    f0,_=evaluate(0.);f1,_=evaluate(1.)
    if not (np.isfinite(f0) and np.isfinite(f1) and f0>target and f1<=target):
        return legacy('strict_endpoint')
    lo,hi,a=0.,1.,.5
    accepted=False
    for _ in range(64):
        value,der=evaluate(a);f=value-target
        if not (np.isfinite(value) and np.isfinite(der)) or der>=0:
            return legacy('nonnegative_or_invalid_derivative')
        if f<=0:hi=a
        else:lo=a
        if hi-lo<=4e-14:accepted=True;break
        if f<=0 and abs(f)<=32*np.finfo(float).eps*max(1.,E) and abs(f/der)<=4e-14:
            l=max(lo,a-1.9e-14);h=min(hi,a+1.9e-14)
            fl,_=evaluate(l);fh,_=evaluate(h)
            if np.isfinite(fl) and np.isfinite(fh) and fl>target and fh<=target and h-l<=4e-14:
                lo,hi=l,h;accepted=True;COUNTS['tight_brackets']+=1;break
        nxt=a-f/der
        if not np.isfinite(nxt) or not (lo<nxt<hi) or nxt==a:
            nxt=(lo+hi)/2;COUNTS['bisection_steps']+=1
        else:COUNTS['newton_steps']+=1
        if nxt==lo or nxt==hi:return legacy('stalled')
        a=nxt
    if not accepted:return legacy('iteration_cap')
    W=p['B']*np.cos(hi*p['angles'])+p['U']*np.sin(hi*p['angles'])
    W=np.linalg.qr(W,mode='reduced')[0]
    if E-float(np.sum(W*(G@W)))>target+tol:
        COUNTS['target_fallbacks']+=1;return V.copy(),True
    COUNTS['accelerated']+=1
    return W,False
