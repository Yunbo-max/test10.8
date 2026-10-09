# Independent review of the minimum-recourse feasible refresh

Status: **assignment 187 completed on the exact assignment-186 candidate
bytes; verdict `CORRECT_AND_REREVIEW`**.

Reviewed candidate:

- path: `research/consistent-lra/MINIMUM_RECOURSE_FEASIBLE_REFRESH_CANDIDATE.md`
- base commit stated by the assignment:
  `7d1faceba2dfb9efa7c3b5801b2937c7f74a531d`
- candidate SHA-256:
  `375deb767117b9ff1f670e2572834532b9831f44c802928f0860b83836b6bff1`

## Verdict

`CORRECT_AND_REREVIEW`.

The constrained minimum-movement refresh in (1), its existence, and its
current-refresh dominance statement are valid.  The monotonicity inequality
(4) is also valid.  However, the candidate's global scalarization paragraph
identifies a **real-projector** two-coordinate set with a convex
(k)-numerical range; that identification is false in general.  A corrected
complex-relaxation plus real-recovery argument appears to establish the desired
real optimizer, but that argument must replace the current one and be
re-reviewed.  Independently, equation (5) is the minimum number of **whole
coordinate exchanges** only.  It is not the optimum of (1), because real
rank-(k) projectors permit continuous rotations.  The exact optimum has no
ceiling.  The trigger condition involving \(\rho_{\rm hi}\) is also missing
from the claimed near-tie prediction.

These are mathematical corrections rather than implementation details, so the
candidate should not be accepted on its current bytes.

## 1. Existence and pairwise dominance

Let

\[
\mathcal G_k=\{Q:Q=Q^{\mathsf T}=Q^2,\ \operatorname{tr}Q=k\}.
\]

This real Grassmannian is a closed and bounded subset of the finite-dimensional
space of symmetric matrices, hence compact.  Its intersection with the closed
halfspace

\[
\operatorname{tr}(CQ)\ge
\beta=\operatorname{tr}C-(1+\rho_{\rm lo})\operatorname{OPT}(C)
\]

is compact.  It is nonempty because every exact top-\(k\) projector \(Q^*\)
satisfies \(L_C(Q^*)=\operatorname{OPT}(C)\).  The continuous distance
objective therefore attains a minimum.

For equal-rank orthogonal projectors,

\[
\|Q-P\|_F^2
=\operatorname{tr}Q+\operatorname{tr}P-2\operatorname{tr}(PQ)
=2k-2\operatorname{tr}(PQ).
\]

Because any exact-SVD output \(Q^*\) is a feasible comparison point, a
minimizer \(Q^{\rm MR}\) satisfies

\[
L_C(Q^{\rm MR})\le(1+\rho_{\rm lo})\operatorname{OPT}(C),\qquad
\|Q^{\rm MR}-P\|_F^2\le\|Q^*-P\|_F^2.
\]

This proves only a pairwise statement at the current covariance \(C\).
Different outputs can produce different later trigger times and covariances,
so the candidate correctly declines to infer trajectory or cumulative-recourse
dominance.

## 2. Lagrange path and monotone captured energy

The loss constraint is exactly

\[
\operatorname{tr}(CQ)\ge\beta,
\]

and minimizing projector distance is equivalent to maximizing
\(o(Q)=\operatorname{tr}(PQ)\).  For \(\lambda\ge0\), maximizing

\[
o(Q)+\lambda c(Q)
=\operatorname{tr}((P+\lambda C)Q)
\]

over rank-\(k\) projectors gives a top-\(k\) eigenspace of
\(P+\lambda C\) by Ky Fan's principle.

For any maximizers \(Q_1,Q_2\) at \(0\le\lambda_1<\lambda_2\), write
\(o_i=\operatorname{tr}(PQ_i)\) and \(c_i=\operatorname{tr}(CQ_i)\).
Optimality gives

\[
o_1+\lambda_1c_1\ge o_2+\lambda_1c_2,
\qquad
o_2+\lambda_2c_2\ge o_1+\lambda_2c_1.
\]

Adding yields

\[
(\lambda_2-\lambda_1)(c_2-c_1)\ge0,
\]

so \(c_2\ge c_1\).  This conclusion does not require a special
"consistent extremal selection" across two distinct parameter values; it
holds for every such pair of scalarized maximizers.  At a single degenerate
parameter value, however, the attainable captured energies form a set that a
solver must resolve deliberately.

## 3. The stated real convexity argument is invalid

The set made from **real** projectors need not be convex.  A two-dimensional
counterexample already suffices.  Take \(k=1\),

\[
P=\begin{pmatrix}1&0\\0&0\end{pmatrix},\qquad
C=\begin{pmatrix}1&a\\a&1\end{pmatrix},\qquad 0<a<1,
\]

where \(C\succ0\).  Every real rank-one projector is \(Q=xx^{\mathsf T}\)
with \(x=(\cos\theta,\sin\theta)\), and hence

\[
(\operatorname{tr}(PQ),\operatorname{tr}(CQ))
=(\cos^2\theta,\ 1+a\sin 2\theta).
\]

This traces an ellipse boundary rather than its filled interior and is not
convex.  Thus the candidate cannot directly invoke convexity of the displayed
real set \(\mathcal W_k(P,C)\) to obtain a supporting line.

### Corrected route that appears sufficient

The desired scalarization can instead be proved in two steps.

1. Enlarge temporarily to **complex Hermitian** rank-\(k\) projectors.  The
   complex \(k\)-numerical range of \(P+iC\), equivalently the set of pairs
   \((\operatorname{tr}(PQ),\operatorname{tr}(CQ))\), is convex.  Because
   \(\operatorname{OPT}(C)>0\) and \(\rho_{\rm lo}>0\), an exact top-\(k\)
   projector of \(C\) has captured energy strictly above \(\beta\).  The
   halfspace constraint therefore has a strictly feasible point, and a
   supporting-line/KKT argument supplies \(\lambda_*\ge0\).

2. Recover a real projector from the scalarized complex optimum.  The matrix
   \(M=P+\lambda_*C\) is real symmetric.  Let \(E_>\) contain eigenvectors
   strictly above the rank-\(k\) cutoff and let \(E_=\) be the real cutoff
   eigenspace.  All scalarized maximizers contain \(E_>\) and choose an
   \(r\)-dimensional subspace of \(E_=\).  On \(E_=\),

   \[
   P_{E_=}+\lambda_*C_{E_=}=\mu I.
   \]

   The values \(\operatorname{tr}(C_{E_=}R)\) over real rank-\(r\)
   projectors \(R\) fill the interval between the sums of the \(r\) smallest
   and \(r\) largest eigenvalues of the real symmetric compression
   \(C_{E_=}\).  The extrema are Ky Fan extrema, and all intermediate values
   occur by continuity on the connected real Grassmannian (with the endpoint
   cases \(r=0\) or \(r=\dim E_=\) trivial).  Hence a real cutoff subspace can
   match the boundary captured energy.  The displayed affine identity then
   gives the matching overlap as well.

If \(\lambda_*=0\), \(P\) itself is the unique scalarized top-\(k\) projector
when \(0<k<d\), and this case corresponds to the old projector already being
feasible; \(k=d\) is trivial.

This supplies the missing existence of a real boundary projector, but it is
not the argument currently written in the candidate.  A corrected candidate
should state the complex enlargement and the real cutoff recovery explicitly,
then receive a new independent review.  A future numerical implementation
still must detect cutoff multiplicity and solve the compressed real problem;
a default eigensolver tie choice does not provide this guarantee.

## 4. Near-tie calculation and correction to equation (5)

For

\[
C=\operatorname{diag}((1+\delta)I_k,(1+2\delta)I_k),\qquad
P=\operatorname{diag}(I_k,0),
\]

let

\[
s=k-\operatorname{tr}(PQ).
\]

For any real rank-\(k\) projector \(Q\), not just a coordinate projector,

\[
\|Q-P\|_F^2=2s
\]

and, because \(C=(1+\delta)P+(1+2\delta)(I-P)\),

\[
L_C(Q)=k(1+2\delta)-\delta s,
\qquad
\operatorname{OPT}(C)=k(1+\delta).
\]

Feasibility is therefore equivalent to

\[
s\ge
k\left(1-\frac{\rho_{\rm lo}(1+\delta)}{\delta}\right).
\]

Every real value \(s\in[0,k]\) is attainable.  For example, fully exchange
\(\lfloor s\rfloor\) coordinate pairs, rotate one additional pair by an angle
\(\theta\) with \(\sin^2\theta=s-\lfloor s\rfloor\), and leave the remaining
pairs unchanged.  Consequently the true optimum of (1) is

\[
\boxed{
s_{\min}=k\left(1-\frac{\rho_{\rm lo}(1+\delta)}{\delta}\right)_+,
\qquad
\|Q^{\rm MR}-P\|_F^2=2s_{\min}.}
\]

The candidate's

\[
m_{\min}=\left\lceil s_{\min}\right\rceil
\]

is correct only after imposing an additional discrete restriction that the
projector exchange whole coordinate directions.  No such restriction appears
in (1), so calling (5) the exact law of the proposed refresh is incorrect.  A
simple sharp discrepancy is \(k=1\) and \(0<s_{\min}<1\): (1) makes a partial
rotation of movement \(2s_{\min}<2\), while (5) prescribes one full exchange
of movement \(2\).

The old projector is feasible exactly when

\[
\rho_{\rm lo}\ge\frac{\delta}{1+\delta},
\]

as stated.  But this family actually reaches a refresh trigger only if

\[
\frac{\delta}{1+\delta}>\rho_{\rm hi},
\]

because \(L_C(P)/\operatorname{OPT}(C)=1+\delta/(1+\delta)\).  Since
\(\rho_{\rm lo}<\rho_{\rm hi}\), a corrected prediction must report this
additional condition.  Discussion of being only slightly beyond the
\(\rho_{\rm lo}\) feasibility boundary does not by itself describe an actual
triggered refresh.

## 5. Scope and admission boundary

The candidate is appropriately explicit that current-refresh dominance does
not imply future-trajectory or cumulative-recourse dominance.  It also makes
no completed theorem-repair, novelty, Step-4 code/design admission, native
execution, Stage-B admission, or completed research-cycle claim.  Those scope
limits are correct and must remain after revision.

This review likewise establishes neither originality nor experimental
readiness.  It only validates the core constrained objective and identifies a
plausible corrected scalarization proof.  The candidate requires correction
and independent re-review before it can enter later method selection or
implementation gates.
