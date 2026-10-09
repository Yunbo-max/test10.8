# Assignment 175: one-arrival HEAVY segment counterexample and aggregate dependency audit

Status: **frozen mathematical candidate; independent assignment 176 required**.
This is a source-bound audit of the existing ICLR 2026 proof, not a new
algorithm, empirical result, theorem-wide refutation, novelty decision, or paper
admission.  No project code or numerical experiment was run.

Fixed project parent: `main` commit
`f781bad77fc7984daa118090df5f01883e664aec`.  The historical
`consistent-lra-rsi` head `7286e6d5b301f01ebda45d6fa1387afd9d383906`
is read-only.  Primary source: Woodruff and Zhou, *Consistent Low-Rank
Approximation*, ICLR 2026, official PDF SHA-256
`ae48c9a75d855fba1ead384ec6860a366542fe2cf383816c03a483edb874ef6f`.

## Claim and proof dependency

Appendix F.1 gives a pointwise `sqrt(k)` recourse bound in the HEAVY branch.
Lemma 3.7 sums that bound over an uninterrupted segment; Lemma 3.9 uses the
result for all non-reset HEAVY times; Lemma 3.10 and Theorem 1.3 then inherit
the `n sqrt(k)` term.  Replacing F.1 by the unconditional projector bound
`R<=2k` gives only `O(nk)`, which becomes the known quadratic-rank scale after
the sampled stream has `O(k epsilon^-2 polylog)` rows.  It does not recover the
claimed `k^(3/2)` scale.

The previously accepted rank family has one `Theta(k)` refresh only after
`Theta(k)` arrivals, so it does not by itself falsify Lemma 3.7's segment sum.
The construction below removes that limitation over real row streams: after a
reachable HEAVY reset, one row produces recourse greater than `sqrt(k)` while
the outer epoch does not reset.  Thus the algebraic HEAVY segment assertion
used in Lemma 3.7 (take `r=1`) does not extend to arbitrary real rows under the
intended persistent-state semantics.  The new construction is not yet an
integer stream or a sampled matrix of the special form `D A_S`; that domain
boundary is retained below.

## Inverse rank-one construction

Let `k=m^2` for any integer `m>=3`, let `B=1024`, `a_i=B^i`, and
`T=sum_i a_i`.  Start from the centered old spectrum

`Lambda={-a_i,+a_i:1<=i<=k}`

and prescribe the new spectrum

`Mu={-a_i/2,8a_i:1<=i<=k}`.

The order strictly interlaces: `-a_i<-a_i/2<-a_(i-1)` on the negative
side and `a_i<8a_i<a_(i+1)` on the positive side.  Put

`g(z)=prod_(mu in Mu)(z-mu)/prod_(lambda in Lambda)(z-lambda)` and
`rho_lambda=-Res_(z=lambda) g(z)`.

Strict positive-update interlacing makes every `rho_lambda>0`.  With
`D=diag(Lambda)` and `u_lambda=sqrt(rho_lambda)`, the determinant lemma gives
`spec(D+uu^T)=Mu`.

For an old negative coordinate `-a_i`, direct residue factorization gives

`rho_(-a_i)=(9/4)a_i prod_(j!=i) F_ij`.

For `j<i`, with `x=a_j/a_i`,

`F_ij=((1-x/2)(1+8x))/(1-x^2)>1`.

For `j>i`, with `r=a_i/a_j<=1/B`,

`F_ij=((1/2-r)(8+r))/(1-r^2)>1`.

Hence `rho_(-a_i)>(9/4)a_i` and

`sum_i rho_(-a_i)>(9/4)T`.                                      (1)

At the new positive eigenvalue `8a_i`, let `b_i=1/g'(8a_i)`.  The normalized
new eigenvector has squared old-negative coordinate

`w_i=rho_(-a_i)b_i/(9a_i)^2`.

The same-scale factor is exactly `7/34`.  Cross factors for `j<i` are each
greater than one.  For `j>i`, their product is

`H(r)=((1/2-r)(8+r)(1-64r^2)) /
      (8(1-r)^2(1+r)(1/2+8r))`.

For `0<r<=1/1024`,

`H(r)>=(1-2r)(1-64r^2)/(1+16r)>=1-19r`.

The finite-product inequality and
`sum_(j>i) B^(i-j)<1/(B-1)` therefore give

`w_i>(7/34)(1-19/1023)=(7/34)(1004/1023)`.

If `P` and `Q` are the old and new top-`k` projectors, all omitted cross
terms are nonnegative, so

`R(P,Q)=2 tr((I-P)Q)
        > (7028/17391) k
        > sqrt(k)`                                                   (2)

for every square `k>=9`.  Both cutoffs are strict.

## Positive covariance, HEAVY state, and one-row trigger

Choose the integer common shift `c=256T`.  Let

`C_0=D+cI`, `C_1=C_0+uu^T`,

and realize `C_0=A_0^T A_0` by diagonal rows.  Both matrices are positive
definite.  The old exact projector selects the `+a_i` coordinates.  The old
and new optimum residuals satisfy

`OPT_s=kc-T=(256k-1)T`,

`OPT_t=OPT_s+T/2=(256k-1/2)T`,                              (3)

because each new bottom eigenvalue rises from `c-a_i` to `c-a_i/2`.
The old projecter's final loss is `OPT_s+sum_i rho_(-a_i)`, so its excess over
`OPT_t` is, by (1),

`E=sum_i rho_(-a_i)-T/2>(7/4)T`.                            (4)

Set

`epsilon=5/(2(256k-1))<1/100`.

At a reset holding `C=OPT_s`, the HEAVY test is strict: even the intended
`sqrt(k)`-term block of the old top spectrum has mass greater than
`sqrt(k)c`, while `(epsilon/3)C=5T/6`.

On appending the single row `u^T`, the outer reset does not fire, since

`OPT_t-OPT_s=T/2 < (epsilon/4)OPT_s=5T/8`.                  (5)

The inner approximation-failure test does fire, since

`(epsilon/2)OPT_t
 =5(256k-1/2)T/[4(256k-1)] <(7/4)T<E`.                     (6)

Thus Algorithm 2 calls exact `RECLUSTER` once, moves from `P` to `Q`, and
incurs the recourse in (2) at a single non-reset HEAVY arrival.

## Reachability from the empty stream

The reset state above need not be assumed.  First insert the `k` top diagonal
rows `sqrt(c+a_i)e_i`.  Then build the `k` bottom diagonal eigenvalues
`c-a_i` using rows along their own coordinates.  While those directions stay
below the top cutoff, `OPT` is exactly their cumulative squared row energy.

Let `f=1+epsilon/4`.  Choose a finite `L` so
`x_0=OPT_s/f^L` is below the smallest bottom-coordinate capacity, and use
targets `x_l=f^l x_0`, ending at `x_L=OPT_s`.  Partition every positive
increment `x_l-x_(l-1)` across the remaining bottom-coordinate capacities;
if a capacity boundary occurs inside an increment, split that increment into
two diagonal rows.  Every partial sum is below its target, and its final piece
hits the target exactly.  Hence the first positive target and every subsequent
`x_l` invoke the outer reset, with the last reset occurring at the exact
covariance `C_0`.  At that time `C=OPT_s`, `c=0`, `V=P`, and HEAVY is TRUE.
This is a finite real row stream and uses no arbitrary supplied algorithm
state.  It diagnoses the unqualified real-matrix extension suggested by the
actual reweighted sampling step.  It is **not** shown to have the special form
`D A_S` with integer `A_S` and row-enlargement diagonal `D>=I`; consequently it
does not by itself refute the segment claim on the literal integer input domain
or on the narrower sampled-matrix class.

## Aggregate consequence and precise boundary

Accepted equations (2)--(6) would refute the domain-free real-row form of
Lemma 3.7, not only the displayed F.1 inference: its `r=1` right-hand side is
`sqrt(k)`, while the actual segment recourse is larger.  The official
Algorithm 2 input is declared integer, whereas Theorem 1.3 applies it to
reweighted real rows after an unsupported literal-integrality sentence.  The
separate accepted Cauchy--Binet repair restores F.2 only on matrices `D A_S`;
it does not automatically prove F.1/3.7 on that class.  Therefore the published
derivation still lacks a stated `O(n sqrt(k))` argument for the actual sampled
stream, but this card does not prove that no such structure-specific argument
exists.

This still does **not** prove the literal integer Lemma 3.7 or Theorem 1.3
false.  The setup uses finitely many real rows, is not qualified as `D A_S`,
and may itself be long; the card does not repeat the one-row event often enough
to violate the theorem's complete aggregate asymptotic bound.
An alternative amortized potential could in principle replace Lemma 3.7.
However, any valid repair must control old-tail capture across multiple
refreshes.  Epoch growth alone is insufficient pointwise, and the trivial
`2k` projector bound recovers only `O(nk)`.  A tail-gap assumption would change
the theorem, while a new telescoping potential must show why captured old-tail
mass cannot be recycled.

## Frozen independent-review falsifier

Assignment 176 must independently check the official Algorithm 2/F.1/3.7/3.9/
3.10/Theorem 1.3 dependency and input-domain boundary, strict interlacing and residue signs, both residue
factor families, the `b_i` normalization and `H(r)` product bound, projector
constant, optimum/excess identities, both strict trigger inequalities, and the
finite reset-state construction.  Return `ACCEPT`, `NEEDS_CORRECTION`, or
`REJECT` against these exact bytes.  Reject or narrow if any step fails, if the
state is unreachable under persistent semantics, or if a hidden published
invariant excludes the stream.  Do not infer integer-input, repeated-event,
integer-input or `D A_S` membership, repeated-event, theorem-falsity, novelty,
empirical, method, or paper eligibility.

