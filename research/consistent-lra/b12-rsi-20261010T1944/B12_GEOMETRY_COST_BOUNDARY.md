# B12: certified repair geometry versus endpoint computation

Status: mathematical boundary result and next-model specification; **not** a new
method, novelty claim, or paper gate.

## 1. Objects and conventions

At a stream time, let `G` be the symmetric positive-semidefinite Gram matrix and
let `Q` be the previous rank-`k` orthogonal projector.  A candidate endpoint `P`
is another rank-`k` orthogonal projector.  Define

* reconstruction loss `L_G(P) = tr((I-P)G)`;
* projector recourse `r(P,Q) = (1/2)||P-Q||_F^2`;
* a required loss threshold `T` (for example `(1+eps) OPT_k(G)`);
* the repair deficit `Delta = [L_G(Q)-T]_+`; and
* spectral diameter `D = lambda_max(G)-lambda_min(G)`.

The threshold is feasible when some rank-`k` projector has loss at most `T`.

## 2. Necessary recourse theorem

**Theorem B12.1.**  If `D>0` and `P` is feasible, then

`r(P,Q) >= Delta^2 / (k D^2)`.

Therefore, for any feasible online sequence `P_0,...,P_n`,

`sum_t r(P_t,P_{t-1}) >= sum_t Delta_t^2/(k D_t^2)`,

where `Delta_t` is evaluated at the actual previous output `P_{t-1}` and current
Gram matrix, and the sum on the right contains only times with `D_t>0` (times
with `D_t=0` necessarily have `Delta_t=0` under feasibility and contribute zero).
This is a pathwise inequality; it does not treat times or prefixes as independent
samples.

**Proof.**  If `Delta=0`, the conclusion is the trivial `r(P,Q)>=0`; no sign claim
about `tr(G(P-Q))` is needed.  Suppose henceforth that `Delta>0`.  Then
`L_G(Q)>T`, and feasibility gives

`tr(G(P-Q)) = L_G(Q)-L_G(P) >= Delta`.

Because `tr(P-Q)=0`, center `G` at
`c=(lambda_max(G)+lambda_min(G))/2`.  Holder duality gives

`|tr(G(P-Q))| <= ||G-cI||_2 ||P-Q||_*`.

If `theta_1,...,theta_k` are the principal angles between the two subspaces,
the positive singular values of `P-Q` are `sin(theta_i)`, each twice; zero
principal angles add no term (this convention also covers `d<2k`).  Hence

`||G-cI||_2 = D/2`,
`||P-Q||_* = 2 sum_i sin(theta_i)`, and
`r(P,Q) = sum_i sin^2(theta_i)`.

Thus

`Delta <= D sum_i sin(theta_i) <= D sqrt(k r(P,Q))`,

which rearranges to the claim.  Summing the pointwise inequalities over `D_t>0`
proves the cumulative statement.  If `D=0`, all rank-`k` projectors have the same
loss, so a feasible threshold forces `Delta=0`; this term is defined as zero and
the displayed quotient is not evaluated.

**Sharpness.**  The constant is exact already for `k=1,d=2`.  Set the PSD matrix
`G=diag(D,0)` and choose two unit lines separated by angle `phi`, with their
bisector at 45 degrees to the first eigenvector.  Name the higher-energy line `P`
and the other line `Q`, and set `T=L_G(P)`.  Then `P` is feasible,
`Delta=L_G(Q)-T=D sin(phi)`, and recourse is `sin^2(phi)`, so equality holds.

## 3. What the theorem does and does not establish

The theorem turns a certified loss deficit into an unavoidable **output motion**.
It is global in the endpoint `P`, needs no eigengap at `k`, and yields a valid
cumulative lower bound.  It can diagnose whether a proposed repair is close to a
geometry-imposed floor.

It is not an upper bound, an algorithm, or a guarantee that a low-recourse
endpoint can be found cheaply.  It can be loose for `k>1` because the Cauchy step
allows all principal-angle sines to contribute equally.  It also does not convert
recourse into wall time or CPU operations.

The nearby PCA literature already uses eigengap/trace curvature to relate excess
PCA objective to projector distance (for example the variational sin-Theta or
curvature lemmas in Vu--Lei).  B12.1 uses the opposite direction needed here: a
required objective improvement implies a minimum displacement from the *previous*
projector.  This bounded read does not establish that the statement is novel.

## 4. No model-free CPU coupling

**Proposition B12.2 (boundary).**  Across unrestricted implementations, certified
slack and projector recourse alone neither uniquely determine endpoint-construction
CPU cost nor give a finite universal upper bound on it.  Any nontrivial complexity
claim must additionally declare a computational model, available state/cache,
precision, and required output form.

**Reason.**  Two implementations can return the identical endpoint sequence and
therefore have identical loss, certificates, and recourse, while one performs any
number of irrelevant operations before returning.  Conversely, a finite stream
and all endpoints can be precomputed and returned from a lookup table, whereas a
stateless implementation can recompute a decomposition.  The online setting may
impose input/output lower bounds, but those depend on dimension, representation,
precision, and state access—not on the four geometric scalars above.

This is an identifiability failure, not evidence that computation is free and not
a claim that lower or upper complexity bounds are impossible after a model is
frozen.  It means the B11 next target was under-specified: geometry can be proved
now, while an amortized CPU theorem requires a frozen oracle/operation model.

## 5. Consequence for the project

Do not count this theorem, a solver, a certificate, a wrapper, or a refresh policy
as a method candidate.  The next derivation must first freeze:

1. state retained between rows (`G_t`, basis, Ritz values, residuals, factorization);
2. allowed primitives (rank-one update, matrix-vector product, QR, small dense
   eigensolve, full eigensolve) and their charged costs;
3. numerical precision and certificate tolerance;
4. whether the endpoint projector itself or only a basis/action is required; and
5. an adversarial or distributional stream model.

Only then is a statement coupling repair deficit, cumulative recourse, and
amortized construction work falsifiable.  Until that model exists, native-5000
execution or implementation of a new endpoint rule is not authorized by this
round.

## 6. Source and implementation join

Newly read in this round:

* Vu and Lei, *Minimax sparse principal subspace estimation in high dimensions*,
  arXiv:1211.0373, especially the variational sin-Theta/curvature result (primary
  paper; scientific read of the relevant theorem family).
  https://arxiv.org/abs/1211.0373
* Nie, Kotlowski, and Warmuth, *Online PCA with Optimal Regret*, JMLR 17(173),
  problem definition and projection-matrix online loss/cost discussion (primary
  paper, D1/D2 relevant sections).
  https://jmlr.org/papers/v17/15-320.html
* Balsubramani, Dasgupta, and Freund, *The Fast Convergence of Incremental PCA*,
  NeurIPS 2013, incremental update framing and sub-quadratic time/memory claim
  (primary paper, D1/D2 relevant sections).
  https://papers.nips.cc/paper_files/paper/2013/hash/c913303f392ffc643f7240b180602652-Abstract.html
* Samson Zhou's author repository at commit
  `d607c4f6467216c470d1e3b93989d44d5fcdec97`, file
  `consistent-lra-landmark.py`, blob
  `6da3eec62de50b5b37c36b26ae725549e354a738`.  Static inspection confirms the
  released Landmark script performs fresh `randomized_svd` at norm-growth
  refreshes and records cumulative wall time/recourse; it does not define an
  oracle-model lower bound connecting those quantities.

Reused unchanged: the exact Landmark dataset/source identity, raw-first-5000,
`d=2704,k=25`, no-standardization protocol, and B01--B11 evidence inventory.
No new benchmark was executed because this round is a formal boundary check and
the missing computational model makes an endpoint benchmark scientifically
non-discriminating.

