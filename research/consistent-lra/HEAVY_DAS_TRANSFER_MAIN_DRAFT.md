# Assignment 177: transfer the accepted one-arrival witness to `D A_S`

Status: **frozen mathematical candidate; independent assignment 178 required**.
This is a narrow consequence of the independently accepted assignment175
real-row construction.  It is not a literal-integer construction, an actual
ridge-leverage-sampling execution, a repeated-event theorem counterexample, a
novelty decision, a method, an empirical result, or a paper admission.

Fixed parent: `main` commit
`65b348910205b8f3bba621c3ff80cad4b8d6002b`.  Dependency: the exact candidate
bytes SHA-256
`92ec4600c73754815a5b652f37c9871da3602e3481c605faf17db25d24d14ac5`
and their assignment176 independent review.  The historical
`consistent-lra-rsi` branch remains read-only.

## Claim

For every square `k>=9`, there is a finite stream `M` of the form

`M = D A_S`,

where `A_S` is an integer matrix and `D` is diagonal with every `D_ii>=1`,
such that the intended persistent-state Algorithm2 reaches a HEAVY reset state
and the next single non-reset arrival triggers exact `RECLUSTER` with projector
recourse greater than `sqrt(k)`.

Thus the algebraic conditions “integer selected rows followed by arbitrary
row enlargement” alone do not restore the domain-free `r=1` Lemma3.7 bound.
This does **not** show that the stream or its weights can actually be emitted by
the particular online ridge-leverage sampler in Theorem2.4.

## Open inequalities around the accepted update

Use the assignment175 notation.  Its diagonal prefix reaches covariance
`C_0`, stale projector `P`, stored cost `OPT_s`, counter zero, and
`HEAVY=TRUE`.  Let `u` be its last row, let

`C(v)=C_0+v v^T`,

let `OPT(v)` be the sum of the bottom `k` eigenvalues of `C(v)`, and let
`Q(v)` be its unique top-`k` projector whenever the cutoff is separated.
At `v=u`, the accepted construction has all of the following strict margins:

1. the top/bottom spectral cutoff is separated;
2. `OPT(u) < (1+epsilon/4) OPT_s` (outer reset does not fire);
3. `loss(P;u) > (1+epsilon/2) OPT(u)` (inner failure fires); and
4. `||P-Q(u)||_F^2 > sqrt(k)`.

The covariance entries are polynomial in `v`.  Ordered eigenvalues are
continuous, hence so is `OPT(v)`.  The stale-projector loss is polynomial in
`v`.  At a separated cutoff the spectral projector `Q(v)` is continuous, so
its squared Frobenius distance from fixed `P` is continuous.  Therefore there
is an open ball `U` about `u` on which all four strict properties hold.

Rational vectors are dense in real Euclidean space.  Choose any

`q in U intersect Q^(2k)`.

Appending `q^T` to the unchanged diagonal prefix consequently produces the
same branch decisions and recourse greater than `sqrt(k)` on one non-reset
HEAVY arrival.  No quantitative perturbation radius is needed for this
existence statement; the strict margins and finite dimension provide it.

## Common scaling gives an exact `D A_S` stream

Let the finite unchanged prefix rows be `r_1,...,r_N`.  Every such row is a
positive scalar multiple of a standard basis vector: `r_j=alpha_j e_(h_j)`
with `alpha_j>0`.  This includes the split diagonal rows used to hit the exact
outer-reset targets.  Let `L` clear all denominators of `q`.

Choose a positive integer `S` that is a multiple of `L` and satisfies

`S min_j alpha_j >= 1`.

Scale **every** row, including the last row, by `S`.  Define integer base rows
and enlargement weights by

* for `j<=N`, `a_j=e_(h_j)` and `d_j=S alpha_j>=1`;
* for the final row, `a_(N+1)=S q in Z^(2k)` and `d_(N+1)=1`.

Then the scaled stream is exactly `M=D A_S` with integer `A_S` and diagonal
`D>=I`.  Global row scaling multiplies every covariance, optimum, stored cost,
loss, and threshold quantity by `S^2`, while leaving every projector,
comparison truth value, reset time, counter transition, and HEAVY decision
unchanged.  Hence the scaled `D A_S` stream has the same one-arrival recourse
greater than `sqrt(k)`.

The integer base rows and diagonal weights are finite but no bit-complexity,
entry-magnitude, sampling-probability, or online-sampler-reachability bound is
claimed.  In particular, choosing formal probabilities `p_j=d_j^(-2)` only
shows each weight has the numerical sampler form `p_j^(-1/2)`; it does not show
that those probabilities are the ones computed by the cited algorithm.

## Consequence and boundary

If assignment178 accepts the derivation, an aggregate repair cannot rely only
on `M=D A_S`, `A_S` integer, and `D>=I`; it must use additional restrictions of
the actual sampling process or a different amortized argument.  The result
still supplies one event, not a repeated aggregate lower bound, and therefore
does not establish Theorem1.3 false.  It also does not establish the literal
integer-input Lemma3.7 false because the diagonal enlargement factors need not
be integral or rational.

## Frozen independent-review falsifier

Assignment178 must review the exact parent and dependency bytes, verify that
all four properties used above are strict in assignment175/176, check the
continuity statements at the separated cutoff, check rational density and the
finite common scaling, inspect every prefix-row type used by the reachability
construction, and verify that every resulting diagonal entry is at least one.
It must reject or narrow the claim if Algorithm2 contains a non-continuous
hidden state dependency affected before the last row, if some prefix row is not
a scalar standard-basis row, or if common scaling changes a branch comparison.
Return `ACCEPT`, `NEEDS_CORRECTION`, or `REJECT`.

Do not infer actual ridge-leverage-sampler reachability, literal integrality,
bounded bits/magnitudes, repeated events, theorem falsity, novelty, empirical
evidence, a method, scientific dispatch, or paper eligibility.
