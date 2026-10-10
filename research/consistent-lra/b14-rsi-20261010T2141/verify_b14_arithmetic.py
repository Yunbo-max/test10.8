#!/usr/bin/env python3
import json
from pathlib import Path
import numpy as np
from scipy.stats import rankdata, spearmanr

HERE = Path(__file__).resolve().parent

def auc(y, s):
    y=np.asarray(y,dtype=bool); s=np.asarray(s,dtype=float)
    keep=np.isfinite(s); y=y[keep]; s=s[keep]
    n1=int(y.sum()); n0=int((~y).sum())
    ranks=rankdata(s,method='average')
    return (float(ranks[y].sum())-n1*(n1+1)/2)/(n1*n0), int(keep.sum())

result=json.loads((HERE/'B14_GAP_ANGLE_RESULT.json').read_text())
features=['rho','worst_sin2','hard_mass','hard_fraction','work_proxy','positive_control_excess_ratio']
qualified=[]
with np.load(HERE/'B14_GAP_ANGLE_RAW.npz',allow_pickle=False) as z:
    for eta,key in [('0.01','0p01'),('0.1','0p1')]:
        y=z[f'eta{key}_update']
        assert int(y.sum())==result['summaries'][eta]['update_states']
        assert len(y)==result['summaries'][eta]['query_states_after_growth']
        excess=z[f'eta{key}_excess_ratio']
        for feat in features:
            raw_name='excess_ratio' if feat=='positive_control_excess_ratio' else feat
            score=z[f'eta{key}_{raw_name}']
            av,cov=auc(y,score)
            saved=result['summaries'][eta]['features'][feat]
            assert abs(av-saved['auc_update_vs_query_no_update'])<1e-15
            assert cov==saved['finite_coverage']
            finite=np.isfinite(score)&np.isfinite(excess)
            sp=float(spearmanr(score[finite],excess[finite]).statistic)
            assert abs(sp-saved['spearman_with_excess_ratio'])<1e-14
    for feat in features[:-1]:
        if all(result['summaries'][eta]['features'][feat]['auc_update_vs_query_no_update']>=0.75 for eta in ('0.01','0.1')):
            qualified.append(feat)
assert qualified==result['development_discriminative_features']==[]
assert result['hypothesis_pass'] is False
assert result['semantic_checks']['gap_times_distance_violations']==0
print(json.dumps({'audit_pass':True,'qualified':qualified,'hypothesis_pass':False,'raw_sha256':result['raw_artifact']['sha256']}))
