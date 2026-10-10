# Independent geodesic and B03 numerical-contract review

Review date: 2026-10-10. Scope: existing-method mathematical audit and prospective solver-contract review. No experiment, solver execution, code modification, GitHub write, or independent-agent delegation was performed. The only review artifact written is this report.

## Scoped verdict

- **Exact-path derivation: correct**, with the explicit domain assumptions below. It covers arbitrary rank, including `k > d/2`, when sums involving `H_j` are restricted to nonzero principal angles.
- **Legacy-surrogate derivative in B03: correct.** It differentiates the actual retained quadratic/trigonometric coefficients, including their cross terms. It does not require spectral invariance.
- **Original B03 stopping/bracketing contract: required correction.** Its tolerant endpoint check did not establish a strict-target feasible right endpoint, and the Newton residual/derivative estimate alone did not certify root distance.
- **B03_DESIGN_V2: suitable to implement and test under its frozen empirical parity gates.** It repairs those two gaps and requires negative finite derivatives. This is approval of a numerical validation protocol, not approval of an implementation or result. Both endpoint and probe losses must be finite, and direct feasibility of all returned states must be recorded by validation.
- **Final source gate: qualified to run the frozen 30-cell native parity check only.** The revised harness repairs the qualification gaps described in the addendum. Timing remains conditional on a full runtime parity pass. No test or benchmark output was independently reviewed.
- **No verdict is granted on novelty, global minimum recourse, cumulative online recourse, empirical parity, empirical speed, or paper eligibility.**

## Reviewed file identities

| File | SHA256 |
|---|---|
| `evidence/consistent-lra-expanded/continuation-12/GEODESIC_MONOTONICITY.md` | `204d75c24d868f9b31ec1e643d938d14eac5fc1cfc1282e863e486fae5e34838` |
| `B03_DESIGN.md` | `c60ad554d4db3773915bb61f8300bc1f834ca15d455ebd719b1610cc9f4d7c09` |
| `B03_DESIGN_V2.md` | `566b79b659cef53c13f38309e53e56894b8d767a2c37edf5a7cd09791c9fb5b7` |
| `evidence/consistent-lra-expanded/continuation-11/matrix_study.py` | `73d2ecceaf73e8fe43c1c9c0534678541892ae7b35a038ca3215a098187e970e` |

Paths in this table are relative to `/workspace/scratch/fc9ea2af50dd`. The source inspection covered the retained `boundary_path`, its `Arm.step` caller, eigentarget construction, and adjacent evaluation definitions.

## Independent derivation

Let `G` be a real symmetric PSD `d x d` matrix and let `Q,V` have `k` orthonormal columns. Assume `span(V)` is a top-`k` spectral subspace, with any selection inside a tied boundary eigenspace allowed. Initially take `0 < k < d`. Assume `eta >= 0` when using the multiplicative feasibility threshold.

Choose principal bases `B=QL` and `Z=VR` such that `B'Z=diag(s_j)`, where `s_j=cos(theta_j)` and `0 <= theta_j <= pi/2`. Define the active index set `I={j: theta_j>0}` and, only for `j` in `I`,

`H_j = (B_j-s_j Z_j)/sin(theta_j)`.

The principal-basis identities imply `Z'H_j=0` and `H_i'H_j=delta_ij` for active indices. Thus these are orthonormal vectors in the orthogonal complement of `span(V)`. For an inactive index, `B_j=Z_j` exactly, so no `H_j` is needed. In particular, `|I| <= min(k,d-k)`. When `k>d/2`, at least `2k-d` angles are zero; there is no requirement to fit `k` orthonormal `H` columns into a complement of dimension `d-k`.

Invariance and symmetry give `Z_i'G H_j=0` for every target-basis index `i` and active index `j`. Set `lambda_j=Z_j'GZ_j` and `h_j=H_j'GH_j`. The vectors `Z_j` need not individually be eigenvectors. Nevertheless, the target and complement Rayleigh bounds give

`lambda_j >= eig_k(G) >= eig_(k+1)(G) >= h_j`.

Hence `g_j=lambda_j-h_j >= 0` on `I`. The sum of all `lambda_j` equals the sum of the top `k` eigenvalues, even if the principal basis mixes their eigenvectors.

For `t_j=(1-alpha)theta_j`, use

`W_j(alpha)=Z_j cos(t_j)+H_j sin(t_j)` for active indices,

and `W_j(alpha)=Z_j` for inactive ones. Its columns are orthonormal. Trace uses only the per-column quadratic forms, so off-diagonal entries of `Z'GZ` and `H'GH` cause no missing terms. Therefore

`L(alpha)=OPT + sum_(j in I) g_j sin^2((1-alpha)theta_j)`,

`L'(alpha)=-sum_(j in I) g_j theta_j sin(2(1-alpha)theta_j) <= 0`.

Here `OPT=tr(G)-sum_(j=1)^k lambda_j`. Both formulas in the supplied derivation are correct with this active-index convention.

For an active direction the corresponding old-basis tangent is `U_j=Z_j sin(theta_j)-H_j cos(theta_j)`. Substitution proves `B_j cos(alpha theta_j)+U_j sin(alpha theta_j)=Z_j cos((1-alpha)theta_j)+H_j sin((1-alpha)theta_j)`, verifying the claimed exact-arithmetic equivalence of the two path parameterizations.

For every `0<alpha<1`, each summand with `g_j>0` and `theta_j>0` gives a strictly negative derivative. Thus any positive initial excess over `OPT` makes the path strictly decreasing throughout its open interval. At `alpha=1`, the derivative is zero. At `alpha=0`, it can also be zero when all improving angles equal `pi/2`; this is a real endpoint degeneracy, not evidence of a constant path.

### Feasibility and edge cases

- If `L(0) <= (1+eta)OPT`, the first feasible parameter is `0`.
- If `L(0) > (1+eta)OPT`, `OPT>0`, and `eta>0`, there is exactly one crossing in `(0,1)`, and the feasible set is the interval from that crossing to `1`.
- Under the same violation with `eta=0`, the unique feasible parameter is `1`.
- If `OPT=0` and the old state is infeasible, at least one active `g_j` is positive and `L(alpha)>0` for every `alpha<1`. Exact zero-loss feasibility forces `alpha=1`. If the old loss is already zero, the first feasible parameter is `0`.
- Eigenvalue ties permit `g_j=0`. Such directions can rotate with no loss change. If every active gap is zero, the whole loss curve is constant; a true multiplicative violation with `eta>=0` cannot then occur.
- `G=0` is a constant-zero case.
- `k=d` has no active angles, `P=I`, and zero loss and movement. The displayed `eig_(k+1)` bound must be omitted. `k=0` also has a constant path and must be handled separately.
- The assumption `eta>=0` should be made explicit. With negative `eta`, the threshold can lie below the optimum; violation alone then proves neither descent nor existence of a feasible point.

### Movement claim

Principal-plane orthogonality gives

`||P(alpha)-P(0)||_F^2 = 2 sum_j sin^2(alpha theta_j)`,

whose derivative is `2 sum_j theta_j sin(2 alpha theta_j) >= 0`. Consequently the first feasible point minimizes movement from the fixed starting projector among points on this selected principal geodesic. Right-angle degeneracy may make the shortest geodesic nonunique; the argument still holds for each selected principal path. It does not compare different feasible paths or historical starting states.

More generally, on the same exact path,

`||P(a)-P(b)||_F <= sqrt(2 sum_j theta_j^2) |a-b|`.

This is a useful exact-model parity bound. It does not establish stability of finite-precision QR or equality of future update decisions.

## Approximate-target limitation

For an arbitrary orthonormal target, define `c_j=Z_j'GH_j`. The exact loss of the constructed orthonormal path instead is

`L(alpha)=L(V)+sum_j [(lambda_j-h_j) sin^2(t_j)-c_j sin(2t_j)]`,

`L'(alpha)=-sum_j (lambda_j-h_j)theta_j sin(2t_j)+2 sum_j c_j theta_j cos(2t_j)`.

An approximate target need not have zero cross terms or nonnegative gaps. Arbitrarily small target error does not alone guarantee monotonicity near the endpoint, where the favorable spectral derivative vanishes.

An exact symbolic falsifier is `G=diag(2,1)`, `k=1`, target `V=(cos beta,sin beta)`, and old state `Q=(cos beta,-sin beta)`, for any `0<beta<pi/4`. Their principal angle is `2 beta`, and the selected geodesic has angle `-beta+2 beta alpha` to the leading eigenvector. Its loss is

`L(alpha)=1+sin^2(-beta+2 beta alpha)`.

It decreases to `1` at `alpha=1/2` and then increases. Taking `beta` arbitrarily small makes the target arbitrarily accurate without restoring monotonicity.

A sign-preserving bisection with a continuous scalar function and opposite endpoint signs can retain some feasible boundary without monotonicity. That fact alone does not prove it found the first feasible parameter. An approximate endpoint can also be infeasible, in which case the proposed initial bracket does not exist. V2 correctly excludes off-invariant targets from accelerated scientific claims. `numpy.linalg.eigh` is a floating-point realization of the exact spectral construction, not a literal exact-arithmetic eigensolver.

## Actual legacy arithmetic and derivative

The retained source forms `D=Z-B*s`, `sn=norm(D,axis=0)`, `theta=atan2(sn,s)`, and sets `U_j=D_j/sn_j` only when `sn_j>1e-8`; otherwise `U_j=0`. It evaluates the surrogate for `W(a)=B cos(a theta)+U sin(a theta)` through

`ell(a)=E-sum_j[aa_j cos^2(a theta_j)+2bb_j sin(a theta_j)cos(a theta_j)+cc_j sin^2(a theta_j)]`.

Direct differentiation gives exactly

`ell'(a)=-sum_j theta_j[(cc_j-aa_j)sin(2a theta_j)+2bb_j cos(2a theta_j)]`.

This matches B03. It is the derivative of the real scalar expression defined by the retained coefficients. Direct matrix evaluation and coefficient evaluation can differ by floating-point evaluation order; bitwise equality is not established.

For an inactive but nonzero angle, the actual column is `B_j cos(a theta_j)`, not a unit geodesic column. Its individual surrogate loss contribution can increase with `a`. QR removes column scaling but changes the relation between this surrogate and the returned projector. Consequently the exact spectral formula cannot simply replace the legacy expression. Routing every `0<sn<=1e-8` case to the unchanged reference is a sound scope restriction. Shared directions forced by `k>d/2` may have tiny nonzero numerical residuals and trigger this fallback frequently; that is not a reason to relax the frozen gate after seeing results.

The legacy precheck accepts `ell(1)<=target+tol`, whereas its bisection predicate is `ell(a)<=target`. It can therefore start with a right endpoint that is not feasible for the strict predicate. Also, `Arm.held` and recomputed `ell(0)` are not guaranteed bitwise equal. The V2 requirement to verify both strict endpoint predicates before acceleration repairs this mismatch without modifying reference behavior.

## Safe numerical protocol and remaining acceptance blockers

The following is the precise operational contract supported by this review. It is a floating-point protocol with empirical validation, not an interval-arithmetic certificate.

1. Retain the original path construction, coefficients, raw loss expression, comparator, target, tolerance, QR, and target-return behavior. Do not silently clamp or substitute analytic gaps, OPT, or target losses.
2. Invoke the unchanged reference for the frozen near-zero-target and inactive-angle gates. Otherwise accelerate only if both endpoint losses are finite, `ell(0)>target`, and `ell(1)<=target`.
3. Maintain stored, finite evaluated endpoint losses with `ell(lo)>target` and `ell(hi)<=target`. Update an endpoint only using a finite evaluated loss. Always return the feasible right endpoint.
4. Use a Newton proposal only with a finite strictly negative derivative and a finite candidate strictly inside the current bracket. Reject an outside proposal by bisection. A nonnegative or nonfinite derivative, nonfinite evaluation, representational stall, or iteration exhaustion routes to the unchanged reference with a separate diagnostic. The fixed iteration cap plus reference fallback supplies bounded termination even without a uniform Newton contraction guarantee.
5. Finish only on an actually sign-verified bracket of width at most `4e-14`. In V2, the residual/derivative estimate may trigger the proposed `a +/- 1.9e-14` probes, but both probe losses must be finite, their strict signs must hold, and their actual represented bracket width must qualify. The estimate alone never accepts a result.
6. Apply the retained QR and direct post-QR `loss<=target+tol` check. Log raw loss separately from tolerance-adjusted classification. The old early target-`V` return trusts the eigentarget without a direct check; validation must record direct loss for returned `V` as well before labeling that return numerically feasible.
7. Preserve the original returned Boolean's meaning: a target-`V` fallback occurred. Record scalar-solver fallbacks, their reasons, derivative evaluations, scalar loss evaluations, and probe evaluations separately.
8. Apply the complete frozen boundary replay and end-to-end trajectory gates before timing or claiming parity. No proof here replaces those gates, and no failed gate may be repaired by silently changing tolerances.

A 48-step exact bisection of `[0,1]` has width `2^-48`, approximately `3.55e-15`; `4e-14` is a different, looser scalar stopping threshold. If both solvers return feasible right endpoints around the same unique exact root, their parameter difference is at most the larger width, and the exact projector Lipschitz bound above is far below the frozen `5e-7` projector tolerance for these ranks. This explains why the proposed numerical tolerance is plausible; it is not proof of actual implementation parity or later decision equality.

To certify real-arithmetic feasibility from arbitrary floating-point data would require validated error bounds or interval signs, including orthogonality and eigenspace errors. Ordinary floating-point sign checks, direct loss computations, and inherited tolerances provide a numerical certificate only. V2 explicitly retains that scope.

**Remaining blockers before a result can pass:** no derivative, reconstruction, endpoint, or parity test output was independently reviewed; no complete-method timing was reviewed. The final source snapshot is qualified for parity dispatch, but all empirical gates remain open.

## Concrete falsifiers for the next review

- A valid exact top-`k` example with any increasing exact loss interval, negative active gap, or nonzero exact invariant/complement cross term would refute the proof or reveal a violated input assumption.
- Use a forced shared-direction case such as `d=3,k=2`, `G=diag(3,2,1)`, `V=[e1,e2]`, and `Q=[e1,cos(theta)e2+sin(theta)e3]`. It must have one active plane and loss `1+sin^2((1-alpha)theta)`.
- Equal-eigenvalue rotations must have constant loss where their active gap is zero. Mixing target eigenvectors in the principal basis must use the principal-basis Rayleigh values, not mistakenly assign sorted eigenvalues by column.
- Exact zero angles must require no division by sine. Values immediately below, at, and above `sn=1e-8` must preserve the frozen fallback boundary.
- An improving `pi/2` angle must permit zero derivative at `alpha=0` and strict interior decrease. Zero OPT with an infeasible old state must not receive an exact zero-loss claim at any `alpha<1`.
- The explicit approximate-target example above must not be asserted monotone. Its derivative must agree with the retained general cross-term formula.
- Endpoint surrogate loss in `(target,target+tol]`, or an already-feasible recomputed left endpoint, must route to the unchanged reference rather than enter an invalid strict bracket.
- A small Newton correction without successful tight-bracket probes must not accept a result. Positive/nonfinite derivatives, nonfinite losses, stalled representable intervals, and exhausted iterations must exercise their documented fallback paths.
- Direct QR-projected or target-return loss above `target+tol`, orthogonality above the frozen bound, any replay projector error above `5e-7`, any changed end-to-end update decision, or any frozen loss/recourse discrepancy failure disqualifies parity.
- Timing gains confined to root-loop time, omitted fallback/probe costs, or treating five repetitions as five independent datasets cannot support the proposed complete-method performance claim.

These are audit targets, not reported test outcomes.

## Source-audit addendum: first implementation snapshot

The root subsequently supplied two additional files for a read-only audit before native parity dispatch:

| File under `evidence/consistent-lra-expanded/continuation-13/` | SHA256 |
|---|---|
| `fast_boundary.py` | `a57eae949245765362062b063fb00d9f159c30d1cebab52204e97a6c3b5ccfc7` |
| `validate_and_time.py` | `3ca09d7181404085a666abc44ab46a7306d5b38be910eed935586e3c64c68617` |

The first solver snapshot preserves the source path coefficients and numerical value expression. Its derivative expression is algebraically identical to the reviewed formula. Both strict endpoint losses are checked for finiteness. It rejects nonnegative derivatives, maintains the sign bracket, qualifies tight probes by their evaluated signs and width, returns the feasible right endpoint, retains QR and the original tolerance, and stores scalar fallback reasons separately from the returned Boolean. The 64-iteration cap correctly routes to the captured unchanged reference. Capturing `LEGACY` before caller monkeypatching avoids recursive fallback.

The native validation harness uses the unchanged legacy state trajectory for same-state boundary replay and separately advances an end-to-end new trajectory from the same start. That is an appropriate distinction. It requires identical update decisions, direct numerical feasibility, projector proximity, orthogonality, and final aggregate recourse proximity before timing.

Two qualification gaps were sent to the root before dispatch:

1. The harness initially gates only the final total recourse difference. Prefix discrepancies can cancel, and it records scored-interval recourse without gating it. The stated cumulative-recourse parity requirement needs the maximum normalized difference of the cumulative prefix sequences, including the scored sequence where that is the retained metric. This requires no tolerance change.
2. The solver's final direct-loss `>` comparison and several replay checks can treat NaN as a nonviolation; Python `max` can also ignore a later NaN. The harness must explicitly require finite returned bases, losses, orthogonality and difference metrics, and trajectory records. The solver should reject nonfinite post-QR loss before returning an accelerated state. This is especially relevant to the independent same-state replay, whose bad result need not propagate into the separate new trajectory.

Until these are repaired, the source may be run as a diagnostic but cannot qualify a timing result under the advertised gates. No mathematical solver defect requiring a different method was found.

Additional reporting points are nonblocking for parity dispatch: the independent explicit-projector recourse increments differ in evaluation order from the legacy overlap identity and should be labeled; the recorded coefficient/matrix formula discrepancy must be inspected because it is not a pass predicate; the timing handoff should verify reference-source, harness and data identities in addition to the fast-source hash; timing rows should retain fallback counts. The global `target_fallbacks` counter in the initial snapshot counts only the accelerated post-QR branch, not target returns occurring inside a scalar legacy fallback, so it must not be interpreted as all target fallbacks.

## Final source gate after qualification repairs

The root revised the harness before dispatch. The final reviewed source identities are:

| File under `evidence/consistent-lra-expanded/continuation-13/` | SHA256 |
|---|---|
| `validate_and_time.py` | `1b2f0a9ee4d2e984331019302ef778d0eb93802daf497d553bebfd9b42601ed4` |
| `fast_boundary.py` | `a57eae949245765362062b063fb00d9f159c30d1cebab52204e97a6c3b5ccfc7` |
| `baseline/matrix_study.py` | `73d2ecceaf73e8fe43c1c9c0534678541892ae7b35a038ca3215a098187e970e` |

The copied reference source independently hashes to the original source. The revised harness includes returned-state and recorded-value finiteness gates; whole and scored cumulative-prefix recourse gates at the unchanged `1e-6` tolerance; both old and new certificate counts; a formula discrepancy predicate at the inherited tolerance; and the originally required update, projector, loss, orthogonality and fallback checks. Timing now verifies the fast, baseline and harness source digests and the prepared data matrix digest against the qualifying parity report. Each timed arm records its target-fallback count.

**Final source verdict: qualified to run the frozen 30 native cells as an existing-method numerical parity repair.** No remaining blocker to that dispatch was found for the frozen inputs. A timing dispatch still requires a complete runtime parity pass with these source identities. This gate neither asserts that parity will pass nor supplies an exact floating-point feasibility theorem. It grants no novelty, cumulative-recourse theorem, empirical speed result or paper-level claim.

The remaining counter-label caveat is interpretive: aggregate fast-module `target_fallbacks` still describes only its direct post-QR branch; the per-arm count is the appropriate total for reported target returns. The independent projector-increment recourse calculation should continue to be labeled as an independent evaluation of the same mathematical quantity.

## Post-result audit: frozen native parity PASS

The root subsequently supplied the completed parity outputs for independent read-only review. This section records the post-result gate and preserves the preceding predispatch review unchanged. No scientific method, eigensolver, trajectory, or benchmark was rerun. The reviewer independently recomputed the qualification predicates from retained arrays and call records from the single execution.

**Result verdict: PASS; qualified for the predeclared 450 complete-method timing runs, subject to the existing resource limits and unchanged protocol.** This admits `30 cells x 3 methods x 5 repetitions` to the next timing stage. It grants no speed claim and is not independent numerical replication.

### Result identity and coverage

`PARITY.json` SHA256 is `325f2648c37a78a64d4e9a5e6bd610ef788993122fd5b0d859bd958716d84b9c`.

The report's recorded source identities match the current bytes and the final qualified snapshot exactly:

- Harness: `1b2f0a9ee4d2e984331019302ef778d0eb93802daf497d553bebfd9b42601ed4`.
- Fast solver: `a57eae949245765362062b063fb00d9f159c30d1cebab52204e97a6c3b5ccfc7`.
- Copied baseline: `73d2ecceaf73e8fe43c1c9c0534678541892ae7b35a038ca3215a098187e970e`.

Exactly 30 trajectory NPZ files and 30 per-cell JSON files are present. The call records are inside `parity/<case>.json`, not separately named `_calls.json` files. The SHA256 of the canonical JSON mapping from all 60 relative output paths to their individual SHA256 digests is `670ac21764fa76ecae35e8ca7cd395c70d54ceec5eda1b9aa417b7cf10ce3843`. To reproduce this digest, use paths relative to `continuation-13`, hash each file's bytes, serialize the mapping with `json.dumps(mapping, sort_keys=True, separators=(',', ':'))`, encode it as UTF-8, and SHA256 the resulting bytes. `PARITY.json` is bound separately by its digest above.

All dataset/rank/eta combinations appear once, in the predeclared order. Each dataset has its two declared ranks and eta values `0.01`, `0.03`, and `0.1`. All row-ID arrays equal the native integer range. Every cell retains calibration preprocessing, its original burn value, and a consistent prepared-matrix hash across that dataset's six cells.

| Dataset | Ranks | Rows per cell | Burn | Cells | Prefix pairs | Same-state boundary calls |
|---|---|---:|---:|---:|---:|---:|
| skin | 1, 2 | 3,000 | 128 | 6 | 18,000 | 1,130 |
| rice | 1, 3 | 3,810 | 128 | 6 | 22,860 | 5,801 |
| wine | 1, 4 | 178 | 35 | 6 | 1,068 | 768 |
| cancer | 4, 12 | 569 | 113 | 6 | 3,414 | 1,323 |
| digits | 4, 16 | 1,797 | 128 | 6 | 10,782 | 3,771 |
| Total | | | | 30 | 56,124 | 12,793 |

For every cell, the call-record count equals the count of old-trajectory update flags minus the initial `k` rank-building updates. The global fast-solver call count is 25,586, exactly twice the 12,793 same-state calls, consistent with separate same-state replay and end-to-end new-trajectory execution.

### Independently recomputed predicates

The reviewer loaded each NPZ with pickle disabled, checked its fields, dimensions, finiteness, native row IDs and final basis shapes, and recomputed both certificate counts, update-decision differences, loss differences, total recourse, scored recourse, and both cumulative-prefix discrepancy gates. Every per-cell JSON summary equals its corresponding top-level report row. The recomputed predicates and extrema exactly match the reported values; there were no discrepancies.

All 30 cells have zero old certificate violations, new certificate violations, update-decision mismatches, same-state feasibility failures, orthogonality failures, target-fallback Boolean mismatches, nonfinite retained values, and formula-tolerance failures. All trajectory fields and final bases are finite. The per-call numeric values were independently checked for finiteness rather than trusting only the recorded Boolean.

| Quantity | Largest observed value | Frozen upper bound | Worst cell |
|---|---:|---:|---|
| Same-state projector difference | `4.468431401574982e-12` | `5e-7` | skin-k1-eta0.03 |
| Scaled trajectory loss difference | `1.1957904930841333e-12` | `1e-6` | rice-k3-eta0.03 |
| Scaled cumulative recourse difference | `1.3752979672629707e-13` | `1e-6` | digits-k16-eta0.01 |
| Scaled scored cumulative recourse difference | `1.100143574663743e-12` | `1e-6` | digits-k16-eta0.01 |
| Scaled final total recourse difference | `1.3322811073357064e-13` | `1e-6` | digits-k16-eta0.01 |
| Same-state orthogonality error | `2.3209105968755468e-15` | `1e-8` | digits-k16-eta0.01 |
| Formula discrepancy divided by inherited tolerance | `2.1140754046607754e-5` | `1` | digits-k16-eta0.03 |
| Same-state loss excess above target, divided by tolerance | `3.2379119888436604e-5` | `1` | digits-k16-eta0.01 |

Scaling here is exactly the frozen `max(1, reference)` denominator. The largest absolute coefficient-versus-matrix formula discrepancy is `4.656612873077393e-10`; the normalized check above is the relevant gate because energy and inherited tolerance vary by call.

Across all stored prefixes, the largest old and new loss excesses over `(1+eta)OPT`, measured in inherited tolerance units, are respectively `0.4137526542125539` and `0.4137600424092144`, both below the frozen `1.01` certificate bound. These are numerical tolerance certificates, not proof that every raw floating-point loss is below the exact multiplicative target.

As an additional retained-array consistency check, independently reconstructed final projectors differ by at most `6.975023644956198e-13`; the largest final new-basis orthogonality error is `1.769844451166619e-15`. These checks use saved final bases and do not rerun the trajectories.

The call accounting is internally consistent: 24,027 accelerated returns plus 1,559 scalar fallbacks equals 25,586 calls. The recorded scalar fallbacks comprise 1,416 inactive-angle cases and 143 iteration-cap cases. Their presence does not disqualify the repair; they are part of its measured complete-method cost. The output records 374,596 value/derivative evaluations and 7,187 successful tight-bracket acceptances. These counts alone establish no wall-time advantage.

The report records process wall time `32.57780801499757` seconds, CPU time `32.574488591000005` seconds, and peak RSS `134072` KiB. This is the instrumented parity execution, not the forthcoming timing comparison. The separate runner wall time reported by the root was not independently checked from a runner receipt in this result audit.

### Admission and limits

The frozen timing handoff is now satisfied: all 30 expected cells passed, source identities match, prepared data identities are recorded, and the timing harness rechecks them. The admitted stage is the existing three-method, five-repetition, randomized-order protocol with complete `Arm.step` costs and the original resource bounds. Five repetitions remain repeated timing measurements, not five independent datasets.

The independent work here is the audit of retained evidence and recomputation of acceptance arithmetic. The stored per-call projector distances, direct losses and formula discrepancies were produced by the original execution; the reviewer did not reconstruct every such value from original per-call matrices, which are not included in these outputs. This review therefore supports the declared numerical parity gate on the 30 development cells, not independent reproduction, exact real-arithmetic feasibility, untouched confirmation, novelty, a cumulative online recourse theorem, or an empirical speed claim.

## Post-result audit: 450 timing runs

The completed timing outputs and terminal runner receipt were reviewed without rerunning any numerical method. The reviewer independently checked coverage, the seeded execution-order schedule, finite positive durations, repeat invariants, final-state hashes, source and input identities, and every reported median and ratio.

**Timing-integrity verdict: PASS. Scientific interpretation: partial engineering benefit over the legacy boundary implementation only.** The candidate has a smaller median CPU time than legacy boundary solving in 24 of 30 cells. It has a larger median CPU time than `certified_full` in all 30 cells. A speedup-over-`certified_full` claim is rejected by these retained results. No source or tolerance was changed for this review.

### Timing and receipt identities

- `TIMING.json` SHA256: `8ff32bc6e72901def7f1555d8f3dd3ed4e5588519e06febd41feff30981397eb`.
- The qualification `PARITY.json` remains `325f2648c37a78a64d4e9a5e6bd610ef788993122fd5b0d859bd958716d84b9c`.
- The timing report's harness, fast-solver and baseline hashes match the previously qualified source identities and current file bytes exactly.
- Runner attempt: `attempt-6a06ac9ced3f46b489a6c4cd5523b45a`, task `b03-native-timing-v1`.
- Its terminal `receipt.json` SHA256 is `ff5ead666726f49c861a4ea9903b1006dabc12c4fdf0b0acc9e25f8ec55339b8`.
- Its retained `attempt.json` hashes to the receipt's contract digest, `36846bd60e40d55f96bbc637d131ef02004824a308d37c360afe0c1bff84a911`.

The terminal receipt records the intended `validate_and_time.py timing` command, success, exit code 0, no error, and elapsed time `107.52648794899869` seconds, within the 120-second task limit. Its output digest matches the current timing report. All eight retained input references match their current bytes: the three source files, two raw data files, qualification report, and both frozen design files. The stdout and stderr digests also match; stdout contains exactly the 30 reported per-cell ratio records, and stderr is empty. Earlier launch/status snapshots are not used as terminal evidence.

### Coverage, order and deterministic state checks

The outputs contain exactly the 30 declared dataset/rank/eta cells, in the expected order. Each has all three methods and repeat IDs 0 through 4 once, giving 450 positive finite CPU and wall durations. `TIMING_PARTIAL.json`'s final row list equals the final report's rows.

Replaying only the predeclared pseudorandom order generation with seed `2026101013` reproduces every stored execution-order list. The three trial records for each cell/repetition agree on that list. The 150 three-method orderings have these counts:

| Order | Count |
|---|---:|
| legacy, certified_full, newton | 28 |
| newton, legacy, certified_full | 22 |
| certified_full, newton, legacy | 25 |
| certified_full, legacy, newton | 32 |
| legacy, newton, certified_full | 24 |
| newton, certified_full, legacy | 19 |

This matches randomized order, not exact counterbalancing. Across first/second/third positions, `certified_full` appears `57/47/46` times, legacy `52/54/44`, and newton `41/49/60` times.

For every one of the 90 cell/method groups, all five repetitions have identical query counts, update counts, target-fallback counts and final-projector hashes. Legacy and newton also have identical query/update/target-fallback counts in each cell; their update totals agree with the retained parity update flags. All timed target-fallback counts are zero. The separate newton scalar-fallback count is not zero: 3,885, comprising 3,540 inactive-angle and 345 iteration-cap fallbacks, all included in timed execution. The fast-solver call count is 63,965, equal to five times the 12,793 qualified boundary updates; 60,080 accelerated returns plus 3,885 scalar fallbacks accounts for every call.

All 60 legacy/newton final-state hash groups match hashes reconstructed from the corresponding saved parity basis using the actual expression `Q@Q.T` with a single loaded `Q`. The hash is constant across repetitions. Legacy and newton have identical final-projector byte hashes in the three skin rank-2 cells; their other byte hashes can differ while satisfying the already established numerical projector parity gate. Equality across `certified_full` and boundary-method states is neither expected nor asserted.

An audit-expression correction was resolved before this verdict: initially, the reviewer loaded the same NPZ basis entry twice within the multiplication expression. That produced product-rounding differences of at most `1.1102230246251565e-16` in 18 cell/method groups and therefore different byte hashes. Reusing one loaded basis, as the timing code does, matches all 60 expected groups exactly. This was a difference in the reviewer's matrix-product evaluation, not evidence of a changed trajectory; no experimental output was modified.

### Recomputed performance summaries

For each cell, the primary ratio is the median of its five legacy CPU durations divided by the median of its five newton CPU durations. It is a ratio of medians, not the median of paired run ratios. All 90 stored method medians and all 60 stored per-cell comparison ratios match independent recomputation exactly.

| Dataset | Median legacy/newton CPU ratio across six cells | Cells with smaller newton median than legacy | Cells with smaller newton median than certified_full |
|---|---:|---:|---:|
| skin | `0.9859912867539734` | 2/6 | 0/6 |
| rice | `1.1844268555388755` | 4/6 | 0/6 |
| wine | `1.5653728382244725` | 6/6 | 0/6 |
| cancer | `1.1743320836484166` | 6/6 | 0/6 |
| digits | `1.1074091682252343` | 6/6 | 0/6 |
| All 30 cells | `1.1349257660194068` | 24/30 | 0/30 |

A ratio greater than 1 favors newton. Across cells, the legacy/newton CPU ratio ranges from `0.9107610041372258` to `1.6941714833302333`. The six slower cells are skin-k1-eta0.01; skin-k2 at all three eta values; and rice-k3 at eta0.01 and eta0.1. These negative results are retained in the aggregate.

The median `certified_full/newton` CPU ratio across cells is `0.13191632753686677`, with range `0.05220495936949967` to `0.4354047647747158`. Thus newton takes approximately `2.30` to `19.16` times the `certified_full` median CPU time across these cells. This is evidence against a runtime advantage over that comparison method. It does not establish which method offers the best recourse/runtime tradeoff, which is a different claim.

Wall-duration summaries agree with the direction of the CPU results: newton is faster than legacy in 24/30 cells and faster than `certified_full` in 0/30; the median legacy/newton wall ratio is `1.1349433413702597`. As a distinct descriptive statistic, the median of all 150 paired-run legacy/newton CPU ratios is `1.1434300618022273`, with 117 of those paired ratios above 1. This latter statistic is not substituted for the predeclared cell summary or treated as 150 independent problem instances.

### Cost accounting and interpretation limits

The timed intervals surround the complete sequence of `Arm.step` calls, including Gram updates, triggers, eigensolves, scalar solving, fallback work and state updates. Arm construction, data preparation, result hashing and I/O are outside those intervals as specified. All 450 timed durations are positive and finite; CPU durations range from `0.0028635680000022035` to `1.6067879069999975` seconds.

Summed CPU duration across timed runs is `105.80311277599999` seconds: `6.912444289000024` for `certified_full`, `52.15829299699996` for legacy, and `46.732375489999995` for newton. These totals are workload-weighted cost accounting, not replacements for the predeclared per-cell medians.

The report records total process CPU `106.41216761` seconds, process wall `106.42506994499854` seconds, and peak RSS `132656` KiB. Subtracting summed timed intervals accounts for `0.6090548340000055` CPU seconds and `0.608699767915823` wall seconds of aggregate untimed preparation/bookkeeping/I/O. The terminal runner elapsed time exceeds the report's measured wall interval by `1.101418004000152` seconds, covering additional startup/wrapper work outside that interval. The source explicitly pins numeric-library thread counts before NumPy import; the observed process accounting is consistent with the intended CPU-only execution.

The supported claim is narrow: under this retained host, implementation, order and five-repeat development protocol, the existing scalar-solver repair reduced complete-method median time against legacy boundary solving in most tested cells, with regressions in six cells and no improvement over `certified_full`. The five repetitions are repeated timings of each fixed cell, and the 30 cells share five datasets. They are not 30 independent datasets or an untouched confirmation set. This is an independent audit of the one retained execution and its summaries, not independent numerical reproduction, a statistical significance claim, a new-method result, a universal speed claim, or a cumulative-recourse theorem.

### Variant identity after integration reconciliation

The root identifies the exact local variant reviewed here as `B03-RSI-independent-20261010T0952`. Every source, parity and timing verdict in this report applies only to the explicitly hashed `continuation-13` files and the 450 timing runs bound above. The word "independent" in the variant identifier does not establish independent numerical replication. This report does not assess another worker's solver, its experiments or artifacts, and does not designate this variant as a replacement for that work.
