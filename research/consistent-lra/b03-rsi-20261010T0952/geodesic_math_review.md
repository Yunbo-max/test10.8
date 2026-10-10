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
