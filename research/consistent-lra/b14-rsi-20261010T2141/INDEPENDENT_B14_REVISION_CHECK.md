# Independent B14 V2 revision-closure check

- Reviewer: `/root/b14_independent_verifier`
- Reviewed at: `2026-10-10T20:54:46.664Z`
- Subject: versioned repair of the fixed B14 V1 diagnostic
- Revision-closure verdict: **PASS**

This verdict closes the five scientific/arithmetic repairs assigned to this reviewer. It does not replace or erase the V1 `REVISE` report, and it does not cover the separately supplied execution-resource receipt.

## Reviewed identities

| Artifact | SHA-256 |
|---|---|
| `B14_REVISION_CONTRACT.md` | `48f37ce4954ebd7f8ff418d80b5a1fc51d6fad0d8de33524afda2b3ef1852aef` |
| `b14_gap_angle_diagnostic_v2.py` | `3bc16cd6b745978454c2cbb689264c1b973e5f05de07e5f29aadad5ba68b6d57` |
| `B14_GAP_ANGLE_RESULT_V2.json` | `3528d54a86be5ef5a6515cd0c135bf96d7aedc010591cdb7315b1f7e998b97ff` |
| `B14_GAP_ANGLE_RAW_V2.npz` | `43332f8d0ba42294d74b56472ef027caf2c024a185009d6e7eaf01c70fc58653` |
| retained V1 review | `40fced5ed7b26feb73e7552ccd9a62cfc27b41bf4de0d038f286c1d3dbefe591` |

The V2 raw NPZ SHA recorded in the result matches the file, and its ZIP CRC passes.

## Repair-by-repair findings

### 1. Ordered infinities and undefined values: PASS

The V2 AUROC routine excludes only `NaN`; ordered `+infinity` and `-infinity` remain legitimate maximal/minimal scores. Independent pairwise U-statistic recomputation reproduces the transparent V1 work-proxy correction:

| eta | V1 corrected AUROC | coverage |
|---:|---:|---:|
| 0.01 | 0.5118424876489392 | 408 |
| 0.1 | 0.5324761904761904 | 205 |

For the repaired V2 proxy, tied/rank-deficient states are `NaN`, not infinities. There are 392/408 and 189/205 eligible proxy states for eta 0.01 and 0.1. No V2 proxy entry is infinite. The JSON field name `finite_coverage` is slightly imprecise because the routine now means non-NaN coverage, but its values and acceptance arithmetic are correct here.

### 2. `lambda_k` and gap-tie handling: PASS

`work_proxy` is undefined exactly when `strict_unique` is false. In the saved arrays,

- `strict_unique == (absolute_gap > 0)` at every state;
- 16 states per eta are excluded as exact ties/rank-deficient boundary states;
- every excluded state has a `NaN` proxy;
- the invalid V1 `lambda_k=0 -> one step` treatment is absent.

The valid `rho=0, lambda_k>0` branch remains available only after the strict-unique guard.

### 3. Tie estimand and strict sensitivity: PASS

The result explicitly labels all-state angle and hard-mass values at a boundary tie as solver-basis-dependent diagnostics. The strict-unique analysis is separately labelled a post-hoc sensitivity required by review, not the original prospective endpoint.

Independent AUROC recomputation matches every strict-sensitivity value. The most favorable strict result is worst-angle AUROC 0.7628144900 for eta 0.01, but its eta 0.1 counterpart is 0.5704081633, so it cannot satisfy the two-eta rule.

This is an exact-double, exact-zero-gap convention. Very small positive numerical gaps remain solver-conditioned; V2 does not turn this sensitivity into an invariant real-arithmetic theorem.

### 4. Exact near-band formula: PASS

The source now implements exactly

`lambda_i-lambda_{k+1} <= 10*(lambda_k-lambda_{k+1})`

with no epsilon widening. Relative to V1, hard mass changes at 13 states per eta, and all 13 are among the 16 non-strict states. Independent AUROCs reproduce the V2 values:

| eta | all-state hard-mass AUROC | strict post-hoc AUROC |
|---:|---:|---:|
| 0.01 | 0.7468274726339242 | 0.7320179559452970 |
| 0.1 | 0.6192380952380953 | 0.5587301587301587 |

### 5. `hard_fraction` acceptance removal: PASS

`hard_fraction` remains only as an explicitly exploratory descriptive field. It is absent from `prospective_features`, `candidate_names`, and the qualification decision.

### 6. Negative decision and semantic replay: PASS

The V2 prefixes exactly equal the saved B09 post-growth query indices, and the V2 labels exactly equal the saved update masks:

| eta | queries | updates | no-update queries |
|---:|---:|---:|---:|
| 0.01 | 408 | 222 | 186 |
| 0.1 | 205 | 100 | 105 |

The V2 loss-reconstruction-error arrays are byte-for-value identical to V1. The prior independent V1 replay recomputed 273 unique full-SVD endpoints across all 1,024 state/eta positions and found maximum absolute error `1.539879335155092e-13` with zero frozen-tolerance violations. V2 retains that maximum, reports zero gap-times-distance lower-bound violations, and does not change the state trajectory.

Independent AUROC readback reproduces every prospective and strict-sensitivity value. `development_discriminative_features=[]` and `hypothesis_pass=false` follow the frozen two-eta threshold. The negative outcome is unchanged.

## Reviewer execution disclosure

This revision check used three bounded shell commands in total: artifact/source inspection, independent NPZ/arithmetic audit, and final report hash/readback. One `apply_patch` operation wrote this review and is not counted as a scientific command. No long spectral computation was rerun.

Only the arithmetic-audit command was internally instrumented:

- wall: `0.282213077` seconds;
- process CPU: `0.280101738` seconds;
- peak RSS: `84,416` KiB.

Exact aggregate wall/CPU/RSS for all three verifier commands is unknown because the inspection and final-readback commands were not internally instrumented. These verifier costs are separate from the candidate's own usage.

## Scope and limitations

The closure supports only this statement: on the saved dependent Landmark-512 development-query states, none of the prospectively eligible gap/angle/hard-mass/work-proxy features reaches fixed-orientation AUROC 0.75 for both eta values.

It does not establish causality, independence, generalization, a new method, native-5000 behavior, originality, a CPU improvement, or a paper/Gate PASS. The positive-control AUROC remains deterministic from the refresh rule and is not predictive confirmation. Resource-receipt closure is outside this review and must remain separately evidenced.

## Signature

`/root/b14_independent_verifier` — independent revision reviewer; no candidate V1 or V2 artifact modified.
