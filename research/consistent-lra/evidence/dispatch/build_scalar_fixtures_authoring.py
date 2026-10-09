"""Authoring-only fixture asset builder; no project import or qualification run."""
from fractions import Fraction as F
import math,json,pathlib
FIELDS=['energy','gram_opt','direct_opt','gram_loss','direct_loss','t','rec']
def oracle(x):
 e=x['energy']; tau=float(F(1e-10)*F(max(1.,e))); band=float(F(10)*F(tau))
 of=x['gram_opt']<=band; opt=x['direct_opt'] if of else x['gram_opt']; nz=opt<=tau
 lf=nz or x['gram_loss']<=band; loss=x['direct_loss'] if lf else x['gram_loss']
 ex=float(F(loss)-F(opt)); ratio=None if nz else float(F(loss)/F(opt)); ne=None if e==0 else float(F(ex)/F(e))
 return dict(tolerance=tau,band=band,opt_fallback=of,opt=opt,near_zero=nz,loss_fallback=lf,loss=loss,increment=0. if x['t']==1 else x['rec'],ratio=ratio,excess=ex,energy_normalized_excess=ne,near_zero_positive_loss_violation=nz and loss>tau,opt_source='direct_svd_fallback' if of else 'qualified_gram',loss_source='direct_residual_fallback' if lf else 'qualified_gram')
def encoded(d):return {k:v.hex() if isinstance(v,float) else v for k,v in d.items()}
b=dict(energy=.25,gram_opt=2e-9,direct_opt=2e-9,gram_loss=3e-9,direct_loss=3e-9,t=2,rec=.125);cases=[]
def add(n,**kw):
 d={**b,**kw};cases.append(dict(id=n,scope='software_fixture_only',inputs=encoded(d),expected=encoded(oracle(d))))
add('energy-below-one');add('zero-energy',energy=0.,gram_opt=0.,direct_opt=0.,gram_loss=0.,direct_loss=0.)
add('energy-above-one',energy=2.,gram_opt=4e-9,direct_opt=4e-9,gram_loss=8e-9,direct_loss=8e-9)
tau=1e-10;band=10*tau
for side,v in [('below',math.nextafter(tau,0.)),('equal',tau),('above',math.nextafter(tau,math.inf))]:add('direct-opt-tau-'+side,gram_opt=0.,direct_opt=v,gram_loss=2e-9,direct_loss=5e-11)
for side,v in [('below',math.nextafter(band,0.)),('equal',band),('above',math.nextafter(band,math.inf))]:add('gram-opt-band-'+side,gram_opt=v,direct_opt=5e-11,gram_loss=3e-9,direct_loss=3e-11)
for side,v in [('below',math.nextafter(band,0.)),('equal',band),('above',math.nextafter(band,math.inf))]:add('gram-loss-band-'+side,gram_loss=v,direct_loss=3e-9)
for side,v in [('below',math.nextafter(tau,0.)),('equal',tau),('above',math.nextafter(tau,math.inf))]:add('direct-loss-tau-'+side,gram_opt=0.,direct_opt=0.,gram_loss=3e-9,direct_loss=v)
add('nearzero-forces-large-loss-direct',gram_opt=0.,direct_opt=0.,gram_loss=.1,direct_loss=2e-10)
add('direct-opt-crosses-above-tau',gram_opt=0.,direct_opt=2e-10,gram_loss=.1,direct_loss=.05)
add('certain-opt-uncertain-loss',gram_loss=0.,direct_loss=3e-9)
add('signed-negative-excess',gram_loss=math.nextafter(2e-9,0.),direct_loss=math.nextafter(2e-9,0.))
add('initialization-excluded',t=1);add('prefix-two-included',t=2)
add('positive-small-energy',energy=2.**-20)
reject=[]
def bad(n,change,reason):reject.append(dict(id=n,scope='runner_input_rejection_only',inputs={**encoded(b),**change},expected_error=reason))
bad('nan-energy',{'energy':'nan'},'nonfinite_or_negative');bad('inf-loss',{'gram_loss':'inf'},'nonfinite_or_negative');bad('negative-energy',{'energy':(-.25).hex()},'nonfinite_or_negative');bad('negative-opt',{'gram_opt':(-1.).hex()},'nonfinite_or_negative');bad('negative-loss',{'gram_loss':(-1.).hex()},'nonfinite_or_negative');bad('negative-recourse',{'rec':(-1.).hex()},'nonfinite_or_negative');bad('zero-prefix',{'t':0},'invalid_prefix');bad('boolean-prefix',{'t':True},'invalid_prefix');bad('fractional-prefix',{'t':1.5},'invalid_prefix');bad('missing-direct-opt',{'gram_opt':0.0.hex(),'direct_opt':None},'missing_direct_input');bad('missing-direct-loss',{'gram_loss':0.0.hex(),'direct_loss':None},'missing_direct_input');bad('unexpected-input',{'unapproved':0},'unexpected_fields')
p=pathlib.Path('research/consistent-lra/scalar_contract_fixtures_window02.json');p.write_text(json.dumps(dict(format='scalar-engineering-fixtures-v1',qualification_executed=False,scope='software_fixtures_not_scientific_samples',cases=cases,reject_cases=reject,accumulator_case_ids=[x['id'] for x in cases[:7]]),indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(valid_cases=len(cases),rejection_cases=len(reject),fixture_path=str(p))))
