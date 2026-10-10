#!/usr/bin/env python3
import hashlib, json
from pathlib import Path
import numpy as np
from scipy.stats import rankdata

HERE=Path(__file__).resolve().parent

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def auc(y,s):
    y=np.asarray(y,dtype=bool); s=np.asarray(s,dtype=float)
    keep=~np.isnan(s); y=y[keep]; s=s[keep]
    n1=int(y.sum()); n0=int((~y).sum()); ranks=rankdata(s,method='average')
    return (float(ranks[y].sum())-n1*(n1+1)/2)/(n1*n0), int(keep.sum())

r=json.loads((HERE/'B14_GAP_ANGLE_RESULT_V2.json').read_text())
assert r['raw_artifact']['sha256']==digest(HERE/'B14_GAP_ANGLE_RAW_V2.npz')
assert r['development_discriminative_features']==[] and r['hypothesis_pass'] is False
assert r['semantic_checks']['gap_times_distance_violations']==0
with np.load(HERE/'B14_GAP_ANGLE_RAW_V2.npz',allow_pickle=False) as z:
    for eta,key in [('0.01','0p01'),('0.1','0p1')]:
        y=z[f'eta{key}_update']; strict=z[f'eta{key}_strict_unique']
        assert int((~strict).sum())==16
        assert np.all(np.isnan(z[f'eta{key}_work_proxy'][~strict]))
        for feat in ['rho','worst_sin2','hard_mass','work_proxy']:
            av,cov=auc(y,z[f'eta{key}_{feat}'])
            saved=r['summaries'][eta]['features'][feat]
            assert abs(av-saved['auc_update_vs_query_no_update'])<1e-15
            assert cov==saved['finite_coverage']
        for feat in ['rho','worst_sin2','hard_mass','work_proxy']:
            av,cov=auc(y[strict],z[f'eta{key}_{feat}'][strict])
            saved=r['summaries'][eta]['strict_unique_posthoc_sensitivity']['features'][feat]
            assert abs(av-saved['auc'])<1e-15 and cov==saved['coverage']
with np.load(HERE/'B14_GAP_ANGLE_RAW.npz',allow_pickle=False) as z:
    for eta,key in [('0.01','0p01'),('0.1','0p1')]:
        av,cov=auc(z[f'eta{key}_update'],z[f'eta{key}_work_proxy'])
        saved=r['v1_all_non_nan_work_proxy_auc_correction'][eta]
        assert abs(av-saved['ordered_infinity_auc'])<1e-15 and cov==saved['coverage']
print(json.dumps({'audit_pass':True,'v1_preserved':True,'v2_negative':True,'raw_v2_sha256':r['raw_artifact']['sha256']}))
