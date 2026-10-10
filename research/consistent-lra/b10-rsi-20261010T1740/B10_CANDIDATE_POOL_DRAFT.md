# B10 autonomous-RSI candidate pool (candidate-author draft)

Date: 2026-10-10

Status: **candidate-author draft, not independently verified, not a novelty claim, no code authorization**.

## 1. Frozen research question and mathematical object

For a row stream \(a_1,a_2,\ldots\in\mathbb R^d\), let

\[
G_t=A_t^\top A_t=\sum_{s\le t}a_sa_s^\top,\qquad
P=VV^\top,\quad V^\top V=I_k.
\]

The rank-\(k\) projection cost and exact optimum are

\[
C_t(P)=\operatorname{tr}((I-P)G_t),\qquad
\mathrm{OPT}_t=\operatorname{tr}(G_t)-\sum_{i=1}^k\lambda_i(G_t).
\]

The one-step projector recourse used in this pool is

\[
D(P,P_0)=\tfrac12\lVert P-P_0\rVert_F^2
=k-\operatorname{tr}(PP_0)=\sum_i\sin^2\theta_i.
\]

The exact-query feasibility test is

\[
C_t(P)\le (1+\eta)\mathrm{OPT}_t. \tag{F}
\]

If only a certified lower bound \(L_t\le\mathrm{OPT}_t\) is available, the stronger test
\(C_t(P)\le(1+\eta)L_t\) is safe. The converse is not safe. The B09 cached-Gram
full eigensolve is the principal exact comparator: any proposed speed result must include
Gram maintenance and endpoint construction, not merely a core kernel.

Research question: **when (F) first fails for the currently emitted projector, can a
certified endpoint with less CPU than the B09 cached-Gram exact comparator be found,
without increasing the emitted loss/recourse trajectory beyond a frozen tolerance?**

The question deliberately does not assert novelty or a positive speedup.

## 2. Reusable derivations

### D1. Residual and rank-one arrival

For current \(V\), the Grassmann residual is

\[
R=(I-VV^\top)G_tV.
\]

If \(V\) is invariant for \(G_{t-1}\), then after \(G_t=G_{t-1}+aa^\top\),

\[
R=(I-VV^\top)a(a^\top V),
\]

which has rank at most one. If \(V\) is stale or approximate, the old residual does not
vanish; the rank-one claim then fails. This is an explicit assumption, not a generic fact.

### D2. Safe restricted Rayleigh--Ritz refresh

For an orthonormal search basis \(S\in\mathbb R^{d\times m}\), \(m\ge k\), let
\(Y_k\) be the top-\(k\) eigenvectors of \(S^\top G_tS\) and \(W=SY_k\). Then
\(W\) is the best captured-energy rank-\(k\) projector whose range lies in
\(\operatorname{span}(S)\). Its actual cost is still evaluated as

\[
C_t(WW^\top)=\operatorname{tr}(G_t)-\operatorname{tr}(W^\top G_tW).
\]

Passing (F), or the stronger lower-bound form, certifies the endpoint even though the
search space is restricted. Failure certifies nothing and requires expansion or fallback.

### D3. Exact one-plane rotation

Replace one \(v\in V\) by \(w(\theta)=v\cos\theta+u\sin\theta\), where
\(u\perp V\), \(\lVert u\rVert=1\). The changing captured energy is exactly

\[
q(\theta)=\begin{bmatrix}\cos\theta&\sin\theta\end{bmatrix}
\begin{bmatrix}v^\top Gv&v^\top Gu\\u^\top Gv&u^\top Gu\end{bmatrix}
\begin{bmatrix}\cos\theta\\\sin\theta\end{bmatrix},
\]

and the projector recourse is \(\sin^2\theta\). Thus the smallest-magnitude root that
meets a captured-energy target is the minimum-recourse point **on this one-dimensional
path only**; it is not a global statement over the Grassmannian.

### D4. Overlap-regularized spectral path

For \(\mu\ge0\), let a chosen optimizer

\[
P_\mu\in\arg\max_{\operatorname{rank}P=k}\{
\operatorname{tr}(PG_t)+\mu\operatorname{tr}(PP_0)\}.
\]

For \(0\le\mu_1<\mu_2\), adding the two optimizer inequalities gives
\((\mu_2-\mu_1)[\operatorname{tr}(P_{\mu_2}P_0)-
\operatorname{tr}(P_{\mu_1}P_0)]\ge0\). Hence a consistently selected overlap is
nondecreasing along the path, while the captured data energy is nonincreasing by the
same inequalities. This supports bisection to a feasibility boundary, subject to
eigenvalue-tie handling. It does not establish originality: the 2026 Consistent PCA work
is a direct collision threat.

## 3. Twenty candidate cards

Each card has object/assumptions, prediction, falsifier, collision status, and disposition.

### C01 — Cached-Gram exact top-\(k\) refresh

- Object: maintain \(G_t\); on failure of (F), compute its exact top-\(k\) eigenspace.
- Assumptions: enough memory for \(d^2\); symmetric eigensolver is numerically qualified.
- Prediction: exact endpoint and OPT; strongest current engineering control.
- Falsifier: reconstructed cost/OPT disagrees with direct SVD beyond frozen tolerance.
- Collision: classical PCA/eigendecomposition; B09 already implements the project control.
- Disposition: **retain only as mandatory control; zero novelty**.

### C02 — Exact symmetric rank-one secular update

- Object: update an eigendecomposition of \(G_{t-1}\) under \(aa^\top\) through a secular equation.
- Assumptions: a sufficiently complete spectrum is maintained; repeated eigenvalues are handled.
- Prediction: avoid a fresh full eigensolve when the update is well conditioned.
- Falsifier: orthogonality/residual drift or end-to-end CPU no better than C01.
- Collision: longstanding symmetric rank-one eigendecomposition modification literature.
- Disposition: **retain as exact comparator; zero novelty**.

### C03 — Brand-style exact incremental SVD

- Object: bordered small-matrix SVD for row addition (left/right roles swapped from column update).
- Assumptions: retained factors include what is required for exactness; reorthogonalization is stable.
- Prediction: exact incremental factors can reduce repeated factorization cost.
- Falsifier: truncation changes the exact trajectory, or reorthogonalization erases the gain.
- Collision: Brand (2002) incremental SVD and subsequent update literature.
- Disposition: **retain as exact comparator; zero novelty**.

### C04 — Warm-start LOBPCG endpoint

- Object: initialize a block eigensolver at the previous \(V\), stop only after an exact feasibility check.
- Assumptions: matvec with \(G_t\) is available and eigen-cluster behavior is benign.
- Prediction: few iterations after small rank-one perturbations.
- Falsifier: iteration count/fallback rate or endpoint CPU loses to C01.
- Collision: LOBPCG explicitly supports block warm starts and Rayleigh--Ritz extraction.
- Disposition: **retain as iterative comparator; zero novelty**.

### C05 — Recycled block Lanczos/randomized Krylov

- Object: seed a Krylov search with \(V\), augment by powers of \(G_t\), and use D2.
- Assumptions: matvecs are cheaper than factorization and finite precision does not destroy the basis.
- Prediction: a small block depth reaches (F).
- Falsifier: depth or orthogonalization makes it slower than C01.
- Collision: block Krylov, randomized low-rank approximation, and subspace recycling.
- Disposition: **exclude from Top-15; subsumed by C04/C16 and high collision**.

### C06 — Oja/streaming-PCA endpoint

- Object: stochastic rank-one gradient updates followed by orthonormalization and exact check.
- Assumptions: stepsize schedule and spectral conditions permit tracking.
- Prediction: low per-row cost away from refreshes.
- Falsifier: feasibility failures or recourse/accuracy drift under exact audit.
- Collision: Oja and streaming PCA literature.
- Disposition: **exclude; known mechanism and weak deterministic certificate story**.

### C07 — GROUSE residual rotation

- Object: rotate the subspace in the sample residual direction, then check (F).
- Assumptions: residual direction is informative and data are compatible with tracking assumptions.
- Prediction: rank-one geodesic updates cheaply follow slow drift.
- Falsifier: persistent infeasibility or worse recourse at matched loss.
- Collision: GROUSE is precisely a Grassmannian rank-one update method.
- Disposition: **exclude; direct algorithmic collision**.

### C08 — PETRELS/RLS subspace tracking

- Object: recursively least-squares update the subspace factors, with exact feasibility audit.
- Assumptions: forgetting/regularization is tuned and the stream matches tracking assumptions.
- Prediction: cheaper state updates than spectral refreshes.
- Falsifier: cumulative objective differs materially or certificate fallback dominates.
- Collision: PETRELS and recursive subspace estimation.
- Disposition: **exclude; different objective and direct collision**.

### C09 — FD/RFD sketch endpoint

- Object: extract candidate directions from a Frequent-Directions-type sketch and audit with (F).
- Assumptions: sketch size is sufficient; all sketch/update time is charged.
- Prediction: compressed state lowers endpoint search cost.
- Falsifier: B09 already found FD50 faster in only 1/6 matched settings against cached Gram, or audit fails.
- Collision: FD/RFD are established deterministic streaming sketches.
- Disposition: **exclude from discovery Top-15; retain historical B08/B09 comparator evidence**.

### C10 — Globally overlap-regularized consistent PCA

- Object: D4 on the full ambient matrix \(G_t+\mu P_0\), choosing the most-overlapping feasible point.
- Assumptions: ties are resolved consistently; exact/bounded OPT is available.
- Prediction: explicit accuracy--recourse tradeoff and monotone overlap path.
- Falsifier: monotonicity breaks under the implemented tie rule or full eigensolves dominate CPU.
- Collision: Hara--Yoshida, *Consistent PCA and Spectral Clustering* (AISTATS 2026), reports a
  subspace-preserving regularizer with approximation/consistency guarantees; full formula/code audit pending.
- Disposition: **retain only as high-priority collision/control; novelty presumed absent until disproved**.

### C11 — One-shot residual-augmented Rayleigh--Ritz

- Object: \(S=\operatorname{orth}[V,R]\), then D2 and exact feasibility audit.
- Assumptions: residual rank is small and \(S\) can be formed cheaper than C01.
- Prediction: after a small perturbation, the first correction subspace often suffices.
- Falsifier: pass rate is low or total CPU exceeds C01 at identical endpoint tolerance.
- Collision: standard residual correction/Rayleigh--Ritz; close to block eigensolver iterations.
- Disposition: **retain as ablation building block; not standalone novelty**.

### C12 — Certified minimum one-plane boundary rotation

- Object: choose a residual direction \(u\), use D3, and solve analytically for the first \(\theta\)
  meeting (F); if no root exists, fall back.
- Assumptions: a one-plane path intersects the feasible set and OPT/lower bound is certified.
- Prediction: strictly smaller path recourse than rotating to the 2D Ritz maximizer when the boundary
  is reached first, with negligible small-problem overhead.
- Falsifier: no feasible root on most refreshes, or global trajectory/cost is worse after fallbacks.
- Collision: GROUSE/geodesic coordinate updates and the consistent-LRA paper's partial-change motif;
  the exact boundary rule may be a combination, not a new method.
- Disposition: **retain for theorem/collision audit; no novelty claim**.

### C13 — Certified block-\(q\) residual geodesic

- Object: select \(q\) singular directions of \(R\), optimize inside the associated \(2q\)-dimensional
  principal-angle block, and stop at the feasibility boundary.
- Assumptions: small \(q\) captures sufficient missing energy and block angles are stably computed.
- Prediction: fewer changed directions than a full refresh while covering cases C12 misses.
- Falsifier: required \(q\approx k\), unstable angles, or CPU/recourse loses to full D4.
- Collision: block Grassmann optimization, subspace tracking, and the source paper's partial update.
- Disposition: **retain as C12 generalization; high collision risk**.

### C14 — Restricted overlap-regularized Rayleigh--Ritz

- Object: in \(S=[V,Q]\), take top-\(k\) of \(S^\top(G_t+\mu P_0)S\), using D4 and exact feasibility.
- Assumptions: the restricted span contains a feasible low-recourse point.
- Prediction: cheaper than full D4 while improving overlap over the unregularized D2 endpoint.
- Falsifier: restricted infeasibility/fallback rate or CPU exceeds C01.
- Collision: direct composition of subspace-preserving regularization and standard Rayleigh--Ritz.
- Disposition: **retain as compositional hypothesis; novelty not established**.

### C15 — Dual bisection to the feasible overlap boundary

- Object: bisection in \(\mu\) along D4 (ambient or restricted) to maximize overlap subject to (F).
- Assumptions: a deterministic tie rule and evaluable cost; feasibility changes monotonically along the selected path.
- Prediction: avoids a dense grid of regularization strengths and reaches a boundary endpoint.
- Falsifier: discontinuous ties invalidate bracketing or repeated eigensolves erase any gain.
- Collision: regularization paths/parametric eigenproblems; likely part of or adjacent to Consistent PCA.
- Disposition: **retain for a precise theorem and as a control; originality doubtful**.

### C16 — Certificate-first adaptive residual expansion

- Object: start with \(S_0=V\); append residual/Krylov blocks one at a time, solve D2 or C14,
  audit (F), and fall back to C01 after a frozen maximum dimension.
- Assumptions: early restricted spaces pass often enough and all audits/fallbacks are charged.
- Prediction: identical feasibility guarantee to C01 with lower median endpoint CPU in easy prefixes.
- Falsifier: fallback frequency, endpoint mismatch, or end-to-end CPU fails the frozen threshold.
- Collision: adaptive subspace expansion, Davidson/Jacobi--Davidson/LOBPCG and recycling.
- Disposition: **retain as the leading engineering hypothesis; not yet a novel algorithm**.

### C17 — Short-history union recycling

- Object: \(S=\operatorname{orth}[V_t,V_{t-1},\ldots,V_{t-h},R]\), then D2/C14 and (F).
- Assumptions: recent endpoint subspaces encode reusable directions and \(h\) remains small.
- Prediction: fewer matvecs than fresh residual Krylov expansion under recurring rotations.
- Falsifier: union dimension/orthogonalization cost grows or old directions do not improve pass rate.
- Collision: thick restart and subspace recycling.
- Disposition: **retain as an ablation; standalone novelty absent**.

### C18 — FD-tail augmented certified refresh

- Object: augment current \(V\) by leading directions from the existing FD/RFD state, then D2/C14.
- Assumptions: the sketch retains missing tail directions and maintenance cost is already charged.
- Prediction: higher restricted-feasibility rate than residual-only search at bounded dimension.
- Falsifier: no improvement over C16 or the B09 FD timing deficit persists.
- Collision: direct hybrid of FD and Rayleigh--Ritz.
- Disposition: **retain only as a mechanism ablation; no novelty**.

### C19 — Randomized residual augmentation with deterministic acceptance

- Object: sample a small block from the residual/complement, build \(S\), and accept only through (F).
- Assumptions: reproducible seeds, enough probe dimension, and deterministic fallback.
- Prediction: on flat/multidirectional residuals, fewer structured iterations reach feasibility.
- Falsifier: variance, audit failures, or charged retries erase speed.
- Collision: randomized range finding/subspace iteration plus certification.
- Disposition: **retain as stochastic comparator; no novelty claim**.

### C20 — Certified eigenvalue-interval early stopping

- Object: during an iterative eigensolve, obtain valid upper bounds \(\bar\lambda_i\ge\lambda_i(G_t)\)
  for the top cluster and set \(L=\operatorname{tr}(G_t)-\sum_{i\le k}\bar\lambda_i\le\mathrm{OPT}_t\);
  accept a candidate only if \(C_t(P)\le(1+\eta)L\).
- Assumptions: top-cluster identification and interval bounds are certified; a residual norm alone is
  insufficient because an invariant but wrong cluster can have zero residual.
- Prediction: terminate before high-accuracy eigenvectors are available when feasibility has slack.
- Falsifier: intervals remain too loose, cluster certification fails, or bound overhead exceeds saved work.
- Collision: a posteriori Ritz/singular-vector bounds and verified eigensolvers.
- Disposition: **retain as a certificate accelerator; likely compositional rather than novel**.

## 4. Whole-pool ranking and provisional Top-15

Scores are ordinal 0--3 and serve only to force a whole-pool comparison. `N` is residual
novelty potential after the present collision audit (not a novelty verdict), `C` certifiability,
`E` CPU plausibility against B09, and `V` value as a scientific control. Rank ties are broken
by falsifiability and relevance to the frozen question.

| Rank | ID | N | C | E | V | Provisional role |
|---:|:---:|---:|---:|---:|---:|---|
| 1 | C16 | 1 | 3 | 3 | 3 | leading engineering hypothesis |
| 2 | C12 | 1 | 3 | 3 | 2 | exact one-plane theorem candidate |
| 3 | C20 | 1 | 3 | 2 | 3 | certificate accelerator |
| 4 | C13 | 1 | 3 | 2 | 2 | block generalization |
| 5 | C14 | 0 | 3 | 2 | 3 | restricted regularized control |
| 6 | C15 | 0 | 3 | 1 | 3 | parametric-path theorem/control |
| 7 | C11 | 0 | 3 | 3 | 3 | residual-RR ablation |
| 8 | C17 | 0 | 3 | 2 | 2 | recycling ablation |
| 9 | C19 | 0 | 3 | 2 | 2 | randomized ablation |
| 10 | C18 | 0 | 3 | 1 | 2 | FD mechanism ablation |
| 11 | C01 | 0 | 3 | 2 | 3 | mandatory exact control |
| 12 | C02 | 0 | 3 | 2 | 3 | exact-update control |
| 13 | C03 | 0 | 3 | 2 | 3 | exact-SVD-update control |
| 14 | C04 | 0 | 3 | 2 | 3 | warm-start iterative control |
| 15 | C10 | 0 | 3 | 1 | 3 | direct 2026 collision/control |
| 16 | C05 | 0 | 2 | 2 | 2 | subsumed Krylov family |
| 17 | C09 | 0 | 3 | 1 | 3 | already tested family |
| 18 | C07 | 0 | 1 | 2 | 2 | direct GROUSE collision |
| 19 | C06 | 0 | 1 | 2 | 2 | stochastic feasibility risk |
| 20 | C08 | 0 | 1 | 1 | 1 | objective mismatch |

The provisional Top-15 is therefore C16, C12, C20, C13, C14, C15, C11, C17, C19,
C18, C01, C02, C03, C04, C10. This is a **research-value selection**, not fifteen novel
methods. Only four constructions retain even a small residual novelty possibility, and all four
remain high-risk combinations of known primitives.

## 5. Literature/code collision ledger used for this draft

| Family | Primary evidence read in B10 | Consequence |
|---|---|---|
| Consistent LRA | Woodruff--Zhou 2026 paper plus pinned official `samsonzhou/consistent-LRA@d607c4f...` code | partial changes, feasibility/recourse framing and author protocol are prior art/baseline |
| Consistent PCA | Hara--Yoshida, AISTATS 2026 PMLR page/abstract | direct threat to C10/C14/C15; full formula/code audit still required |
| Exact incremental SVD | Brand 2002 paper | C03 is prior art |
| Symmetric rank-one eigensolvers | secular/rank-one update literature | C02 is prior art |
| Warm-start block eigensolvers | LOBPCG survey/paper | C04/C11/C16 overlap established eigensolver mechanisms |
| Randomized/Krylov LRA | Halko--Martinsson--Tropp; Musco--Musco | C05/C19 primitives are prior art |
| Streaming PCA | Oja analyses | C06 is prior art |
| Grassmann tracking | GROUSE paper | C07 and the rotation primitive in C12/C13 collide |
| Recursive tracking | PETRELS paper | C08 is prior art and objective-misaligned |
| Deterministic sketches | FD and RFD papers/code | C09/C18 primitives are prior art; B09 is negative timing evidence |
| A posteriori spectral bounds | Ritz/singular-vector error-bound papers | C20 is at best a certified composition |

## 6. Candidate-author decision before independent review

1. **Do not code yet.** The pool is drafted but not independently verified.
2. The most important new collision is Hara--Yoshida (AISTATS 2026), which substantially
   weakens any novelty story based on overlap/subspace-preserving regularization.
3. If an independent verifier accepts D3/D4 and the ranking logic, the next mathematical task is
   a full-text/formula/code audit of Consistent PCA and a sharp statement of what, if anything,
   remains beyond known residual correction, regularization paths, and certified fallback.
4. If that audit closes the residual gap, park the novelty branch and treat C12/C16/C20 only as
   engineering comparators; do not manufacture a NeurIPS claim from a known-method combination.

