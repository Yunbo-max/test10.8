# HEAVY multi-refresh potential candidate

Status: **assignment 183 candidate; not yet independently accepted**.

This is a mathematical candidate only.  It is not a scientific experiment, a
new algorithm, a theorem refutation, or permission to bypass the blocked native
evaluation contract.  It addresses the earliest open mathematical premise left
by the accepted single-event HEAVY witnesses: whether repeated large projector
motions admit a different amortization even though the pointwise argument used
in Lemma F.1 is invalid.

## Fixed source and object

The source object is Algorithm 2 and Lemmas 3.7/F.1 of the ICLR 2026 paper
*Consistent Low-Rank Approximation*:

<https://proceedings.iclr.cc/paper_files/paper/2026/file/b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf>

Use the intended persistent-state reading of `HEAVY`, `C`, and `c`.  Consider
only fixed-rank reclustering times after rank warm-up.  Let

\[
0=t_0<t_1<\cdots<t_J,
\qquad C_j=A_{1:t_j}^{\mathsf T}A_{1:t_j},
\]

and let \(P_j\) be an exact rank-\(k\) top-eigenspace projector of \(C_j\).
Set

\[
D_j=C_j-C_{j-1}\succeq0,
\quad L_C(P)=\operatorname{tr}((I-P)C),
\quad \operatorname{OPT}(C)=\min_{\operatorname{rank}P=k}L_C(P).
\]

Define the movement, old-covariance regret, and update residual

\[
R_j=\|P_j-P_{j-1}\|_F^2,
\quad G_j=L_{C_{j-1}}(P_j)-\operatorname{OPT}(C_{j-1}),
\quad U_j=L_{D_j}(P_j).
\]

All three quantities are nonnegative.

## Exact trigger ledger

For every reclustering interval,

\[
\boxed{\operatorname{OPT}(C_j)-\operatorname{OPT}(C_{j-1})=G_j+U_j.}
\tag{1}
\]

This follows by expanding the new optimum at \(P_j\):

\[
\begin{aligned}
\operatorname{OPT}(C_j)
 &=L_{C_{j-1}+D_j}(P_j)\\
 &=L_{C_{j-1}}(P_j)+L_{D_j}(P_j)\\
 &=\operatorname{OPT}(C_{j-1})+G_j+U_j.
\end{aligned}
\]

Consequently, the old-covariance regret is a non-recyclable budget:

\[
\boxed{\sum_{j=1}^{J}G_j
\leq \operatorname{OPT}(C_J)-\operatorname{OPT}(C_0).}
\tag{2}
\]

Equation (2) is the precise safe replacement for attempts to sum only the
missed old-head mass.  In the notation of the accepted F1 audit, that missed
mass is offset by captured old-tail mass; their difference is exactly \(G_j\).
The positive head term alone is therefore not a valid telescoping potential.

## Gap-weighted projector motion

Let

\[
\gamma_{j-1}=\lambda_k(C_{j-1})-\lambda_{k+1}(C_{j-1})\geq0.
\]

The standard equal-rank overlap identity gives

\[
G_j\geq \frac{\gamma_{j-1}}2R_j.
\tag{3}
\]

For completeness, in an eigenbasis of \(C_{j-1}\), let \(\alpha_i\) be the
mass omitted by \(P_j\) from old top coordinates and \(\beta_i\) the mass
captured from old tail coordinates.  Equal ranks imply

\[
\sum_{i\leq k}\alpha_i=\sum_{i>k}\beta_i=R_j/2.
\]

Thus

\[
G_j=\sum_{i\leq k}\lambda_i\alpha_i-
    \sum_{i>k}\lambda_i\beta_i
\geq(\lambda_k-\lambda_{k+1})R_j/2.
\]

Combining (2) and (3) yields the rigorously amortized statement

\[
\boxed{\sum_{j=1}^{J}\gamma_{j-1}R_j
\leq 2\bigl(\operatorname{OPT}(C_J)-\operatorname{OPT}(C_0)\bigr).}
\tag{4}
\]

This proves that repeated large moves cannot repeatedly spend the same
old-covariance regret.  It does **not** bound unweighted recourse when the cutoff
gap can be small.

## Sharp obstruction to completing the paper's bound from this ledger alone

Fix \(0<\delta<1\) and use dimension \(2k\):

\[
C_0=\operatorname{diag}((1+\delta)I_k,I_k),
\qquad
D_1=\operatorname{diag}(0,2\delta I_k).
\]

Both old and new top-\(k\) spaces are unique.  They are the first and second
coordinate blocks respectively, so

\[
R_1=2k,
\qquad G_1=\delta k,
\qquad U_1=0,
\qquad \operatorname{OPT}(C_1)-\operatorname{OPT}(C_0)=\delta k.
\]

The update is positive semidefinite and is a sum of \(k\) rank-one row
updates.  As \(\delta\downarrow0\), arbitrarily large unweighted movement has
arbitrarily small OPT-growth charge.  Therefore PSD monotonicity, OPT growth,
and (1) alone cannot imply a gap-free lower bound \(G_j\geq cR_j\).  This is a
limitation example for the proposed potential, not a source-faithful integer
stream counterexample to the paper.

## Consequence for the open proof branch

The accepted single-event constructions invalidate a pointwise
\(O(\sqrt{k})\) motion claim, but they do not by themselves violate an
\(O(n\sqrt{k})\) aggregate bound.  Equations (1)--(4) narrow a possible repair
to one of two missing ingredients:

1. prove that HEAVY refreshes with large \(R_j\) also have enough cutoff gap,
   or otherwise convert the weighted sum (4) into an unweighted sum; or
2. introduce a second potential that controls motion inside near-degenerate
   spectral bands without counting captured old-tail mass as fresh progress.

Neither ingredient is established here.  In particular, HEAVY controls a sum
of bottom top-\(k\) eigenvalues, not the cutoff gap, so it cannot simply be
substituted for \(\gamma_{j-1}\).

## Six-field candidate card

- **Object:** exact top-\(k\) projectors at successive Algorithm 2
  reclustering times in an append-only covariance stream.
- **Assumptions:** fixed rank; exact reclustering; disjoint chronological
  update blocks \(D_j\succeq0\); no claim about scorer or experiments.
- **Derivation:** exact OPT ledger (1), telescoping charge (2), eigengap
  conversion (3), and weighted recourse potential (4).
- **Prediction:** any valid multi-refresh proof that charges only OPT growth
  must explicitly control near-cutoff degeneracy; a proof that silently
  replaces \(G_j\) by missed old-head mass will fail on old-tail capture.
- **Falsifier:** one valid fixed-rank trigger interval for which (1), (3), or
  the telescoping inequality (2) fails under the definitions above.
- **Boundary:** this does not prove the advertised total-recourse theorem and
  does not construct repeatable large-motion events.  It is a partial
  amortization lemma plus a precise obstruction.

## Required independent review (assignment 184)

The reviewer must independently check the algebra, the equal-rank factor of
two, the near-tie obstruction, and the distinction between a gap-weighted
partial result and a proof of the paper's unweighted claim.  Acceptance must
not be converted into experiment admission, theorem refutation, originality,
or a completed research cycle.
