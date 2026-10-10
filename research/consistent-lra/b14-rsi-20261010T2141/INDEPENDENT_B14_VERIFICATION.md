# Independent B14 verification

- Reviewer: `/root/b14_independent_verifier`
- Reviewed at: `2026-10-10T20:50:43Z`
- Review type: independent fixed-artifact mathematical, semantic, arithmetic, and scope audit
- Verdict for the scoped B14 diagnostic: **REVISE**

## Frozen subject and identities

I reviewed only the requested B14 candidate artifacts and the two immutable B09 inputs.  I did not modify the candidate artifacts.

| Artifact | SHA-256 |
|---|---|
| `B14_ROUND_CONTRACT.json` | `4dd52b0ff975029ef2ed2345e385b22638d7771d15dad9b98835ed2aaf3b7195` |
| `B14_MATH_AND_SCOPE.md` | `10d4e276bde1fe84c39d3795c587d2fc73f260aed4579122e6ee910b2756ed03` |
| `b14_gap_angle_diagnostic.py` | `d654c3c2fe619e48f52bf294d2655687e598016589d325d5b7c32ce141b0ae92` |
| `B14_GAP_ANGLE_RESULT.json` | `2b0c587b67c12f893405ef55c9e4a6993d303954a18b8a5cb2b87d0e842317a4` |
| `B14_GAP_ANGLE_RAW.npz` | `2580f0cade9be57f467f46daf793c0de07686f7f34b7ea7eb1199f63243df9ae` |
| `LANDMARK512_FD_RAW.npz` | `d0de6bb598161e85557321a309e9d720cb1c398b722140725e47d8365e3ec68a` |
| `FD_POLICY512_RAW.npz` | `b8c4f5278fa58c96c485d6f547acdd927a5cd5153528219ebc1fd6ada4744fa5` |

The raw NPZ hash recorded in the result matches the file. ZIP CRC checks pass for all three inspected NPZ files. The contract, mathematics, and program timestamps precede the result/raw artifacts.

## Mathematical review

### Statewise excess-loss sandwich: PASS

For PSD `G=A^T A`, a rank-`k` leading spectral projector `P`, and any rank-`k` projector `Q`, write `p_i=v_i^TQv_i`. Then

`X=tr(G(P-Q)) = sum_{i<=k} lambda_i(1-p_i) - sum_{i>k} lambda_i p_i`.

Because `sum_{i<=k}(1-p_i)=sum_{i>k}p_i=k-tr(PQ)=r(P,Q)`, termwise eigenvalue bounds give

`(lambda_k-lambda_{k+1})r(P,Q) <= X <= (lambda_1-lambda_d)r(P,Q)`.

This remains valid at a boundary tie; the lower bound merely becomes zero. It is a statewise certificate only and does not imply a refresh-count, amortized-work, or CPU theorem. The candidate states this limitation correctly.

### Subspace-iteration proxy: theorem valid under its stated strict assumptions, implementation edge cases need revision

With a unique target top-`k` invariant subspace, `lambda_k>lambda_{k+1}>=0`, and nonsingular initial top-block overlap, the standard tangent envelope supports the displayed integer proxy. The one-step `rho=0` branch is valid when `lambda_k>0` and the bottom eigenvalues are zero.

However, B14 contains 16 queried prefixes per eta with a computed zero boundary gap. Fifteen have `rho=1`; prefix 36 has both clipped boundary eigenvalues zero and is assigned `rho=0`, so the implementation reports a one-step proxy although the target top-`k` subspace is not unique and `lambda_k>0` is false. At the other tied/numerically null states, `worst_sin2` and per-eigenvector hard mass depend on the eigensolver-selected basis unless an invariant tied block or deterministic numerical convention is explicitly part of the estimand.

The near-band code also uses

`10 * max(gap, eps * max(1,lambda_1))`

whereas the frozen metric says exactly `10*(lambda_k-lambda_{k+1})`. This only matters at zero/nearly-zero gaps, precisely where uniqueness is already unresolved.

## B09 state reconstruction semantics: PASS

I independently replayed the retained endpoint sequence from the saved B09 update masks. At each update I recomputed the full prefix SVD and used the resulting right top-25 endpoint for subsequent incoming losses. Across 1,024 eta/state positions:

- unique recomputed SVD endpoints: 273;
- maximum absolute incoming-loss discrepancy: `1.539879335155092e-13`;
- violations of the frozen `1e-10*max(1,energy)` tolerance: 0.

The raw B14 prefixes equal the exact saved baseline query indices after growth. Their update labels equal the saved update masks exactly:

| eta | query states | update states | query-no-update states |
|---:|---:|---:|---:|
| 0.01 | 408 | 222 | 186 |
| 0.1 | 205 | 100 | 105 |

The baseline and strong update masks are identical. Independently applying `loss > (1+eta)*OPT + tol` to every queried post-growth state reproduces every saved update label. The recorded lower-bound check has zero violations; direct raw arithmetic gives `max(gap*r-excess)=-3.223712263259627e-09` before tolerance.

## AUROC audit

Independent rank/U-statistic recomputation exactly reproduces the reported AUROCs for `rho`, `worst_sin2`, `hard_mass`, and `hard_fraction`. It also reproduces the reported work-proxy AUROC **only after deleting all `+infinity` scores**.

That deletion is not faithful to the frozen fixed-orientation AUROC. `+infinity` is a valid maximal ordered work score produced by the declared proxy, not a missing observation. The program's `np.isfinite` filter silently removes 15 states per eta. Retaining those states gives:

| eta | reported work-proxy AUROC / n | corrected ordered-score AUROC / n |
|---:|---:|---:|
| 0.01 | 0.4764687549 / 393 | 0.5118424876 / 408 |
| 0.1 | 0.4499719888 / 190 | 0.5324761905 / 205 |

This correction does **not** change the frozen scientific decision: neither corrected value reaches 0.75, and no other declared spectral/angle feature reaches 0.75 for both eta values. A post-hoc sensitivity that removes all 16 exact-zero-gap states also remains negative; its worst-angle AUROCs are `0.7628144900` and `0.5704081633`, and hard-mass AUROCs are `0.7320179560` and `0.5587301587`.

`hard_fraction` was not declared in `frozen_metrics` and should not be eligible for the prospective acceptance list. It failed here, so this scope leak did not alter the result, but it must be labelled exploratory or removed from acceptance logic.

## Acceptance and claims

The negative conclusion is supported in substance: **the prospectively named gap, worst-angle, and hard-mass features do not achieve fixed-orientation AUROC >=0.75 at both eta values on this saved native-512 development prefix.** This is dependent, adaptively exposed development evidence only.

The candidate correctly forbids claims of a new method, causality, independent dataset confirmation, native-5000 performance, generalization, originality, or paper/Gate PASS. The positive-control AUROC of 1.0 is expected because the update label is deterministically thresholded from the same loss and OPT; it is a pipeline check, not independent predictive evidence.

The result reports 18.691 wall seconds, 18.650 process-CPU seconds, and 356,540 KiB peak RSS with numeric threads set to one. These numbers are below the frozen limits. The currently visible cgroup is 8 CPU and 8 GiB. The five frozen candidate artifacts do not include an external command receipt or historical cgroup snapshot, so this review verifies internal consistency and current-host compatibility, not independent attestation of the original run's resource accounting.

## Required versioned repairs

1. Preserve the current files as the original attempt. In a child revision, compute AUROC over all non-NaN ordered scores; retain `+infinity` as a maximal tied score. Report coverage separately.
2. Mark the subspace-iteration proxy undefined when `lambda_k<=0` or the target boundary is tied/non-unique. Do not map the `lambda_k=0` case to the valid `rho=0, lambda_k>0` one-step branch.
3. State an explicit tie/rank-deficiency estimand. Either report the all-state angle/hard-mass values as solver-basis-dependent diagnostics, or use an invariant tied-block definition. Any strict-gap exclusion or numerical-rank threshold introduced after this run must be labelled post-hoc sensitivity, not the original prospective endpoint.
4. Make the near-band implementation match the frozen formula exactly, or prospectively version the numerical tolerance rule and explain its effect at a zero gap.
5. Remove `hard_fraction` from prospective qualification or label it exploratory. Retain the original negative outcome and the corrected negative decision; do not turn repair into confirmation evidence.
6. If resource compliance is promoted beyond self-reported usage, attach the command exit/elapsed/RSS receipt and the execution-time cgroup/thread snapshot.

After repairs 1--5 and exact-result readback, this scoped diagnostic is expected to close as a qualified negative result. It still cannot support a new-method, native-5000, generalization, originality, or paper claim.

## Signature

`/root/b14_independent_verifier` — independent reviewer; no candidate artifact edited.
