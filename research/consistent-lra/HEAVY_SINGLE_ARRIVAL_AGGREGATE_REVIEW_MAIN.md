# Assignment 176 — independent fixed-byte mathematical review

## Verdict

**ACCEPT.** First failing line: none.

The reviewed candidate establishes a reachable single-arrival violation of the
pointwise `sqrt(k)` HEAVY recourse bound, and therefore of the `r=1` real-row
version of Lemma 3.7, under the intended persistent-state interpretation of
Algorithm 2.

This acceptance does **not** extend to integer inputs, sampled matrices
`D A_S`, repeated events, Theorem 1.3 falsity, novelty, empirical validity, a
new method, or paper eligibility.

## Fixed identities

| Item | Identity |
|---|---|
| Reviewed commit | `ad77490323fee335dc64ae390cc37d61b29646eb` |
| Parent commit | `f781bad77fc7984daa118090df5f01883e664aec` |
| Candidate | `HEAVY_SINGLE_ARRIVAL_AGGREGATE_AUDIT_MAIN_DRAFT.md` |
| Candidate SHA-256 | `92ec4600c73754815a5b652f37c9871da3602e3481c605faf17db25d24d14ac5` |
| Candidate Git blob / size | `350fc65c76aa146282d19981d82500c1a252c6b0` / 8,643 bytes |
| Review-task SHA-256 | `a1632be92e6d772ced1071ce2a33fbc3ea9ec32ef315ff7dcb37d7805264dca8` |
| Official ICLR 2026 PDF SHA-256 / size | `ae48c9a75d855fba1ead384ec6860a366542fe2cf383816c03a483edb874ef6f` / 852,552 bytes |

The reviewer independently downloaded the official conference PDF and checked
Algorithm 2, Appendix F.1, Lemmas 3.7, 3.9, 3.10, Theorem 1.3, and Theorem 2.4.
Algorithm 2's printed initialization is inside the loop, but its epoch and
counter lemmas require persistent state; the review therefore checks the exact
intended persistent-state semantics stated by the candidate.

## Independent derivation

Let `k=m^2`, `m>=3`, `B=1024`, `a_i=B^i`, and `T=sum_i a_i`.  The spectra
`Lambda={-a_i,+a_i}` and `Mu={-a_i/2,8a_i}` strictly interlace, including the
central and terminal intervals.  Therefore the residues
`rho_lambda=-Res_lambda g` are positive and the determinant lemma gives
`spec(D+u u^T)=Mu` for `u_lambda=sqrt(rho_lambda)`.

At `lambda=-a_i`, the same-scale residue factor is `(9/4)a_i`.  For `j<i`,
`F_ij=((1-x/2)(1+8x))/(1-x^2)>1` because the cleared difference is
`(15/2)x-3x^2>0`.  For `j>i`,
`F_ij=((1/2-r)(8+r))/(1-r^2)>1` because the difference is
`3-(15/2)r>0`.  Hence `rho_(-a_i)>(9/4)a_i` and their sum exceeds
`(9/4)T`.

At the new eigenvalue `8a_i`, differentiating the partial fraction identity
shows that `b_i=1/g'(8a_i)` is the eigenvector normalizer.  Its same-scale
old-negative coordinate factor is exactly `7/34`.  The reviewer independently
verified the smaller-scale cross factors exceed one and recovered the larger
scale factor

`H(r)=((1/2-r)(8+r)(1-64r^2))/(8(1-r)^2(1+r)(1/2+8r))`.

For `0<r<=1/1024`, this exceeds `1-19r`: after the candidate's first bound,
the cleared difference is `r+240r^2+128r^3>0`.  The finite-product inequality
then gives each selected coordinate weight greater than
`(7/34)(1004/1023)`.  Consequently

`||P-Q||_F^2 > (7028/17391)k > sqrt(k)`

for every square `k>=9`; the last inequality follows from
`3*7028>17391`.

With common shift `gamma=256T`, both covariances are positive definite and
`OPT_s=(256k-1)T`, `OPT_t=(256k-1/2)T`, while the stale-projector excess is
greater than `(7/4)T`.

For `epsilon=5/[2(256k-1)]`, the HEAVY spectral-mass test is strict.  The new
row increases OPT by only `T/2<5T/8`, so no outer reset occurs, while its stale
excess strictly exceeds `(epsilon/2)OPT_t`, so exact `RECLUSTER` occurs and
incurs the displayed movement.

## Reachability check

The diagonal prefix is reachable from the empty stream.  After the `k` top
rows, insert bottom-coordinate energy at targets `x_l=f^l x_0`, where
`f=1+epsilon/4`.  The first positive target resets from `C=0`, and each later
target exactly meets `OPT=fC`.

The explicit counter check is
`x_l-x_(l-1) <= (f-1)OPT_s = (5/8)T`, while each fresh bottom-coordinate
capacity is at least `255T`.  Thus a target increment crosses at most one
capacity boundary and needs at most two rows.  Any non-target partial row
increments the algorithmic counter at most once before the next outer reset,
below both counter thresholds for `sqrt(k)>=3` and `k>=9`.  The final target
fills all capacities exactly, so the last reset reaches `C_0`, `C=OPT_s`,
counter zero, `V=P`, and `HEAVY=TRUE`.

## Accepted consequence and retained boundary

For a one-arrival uninterrupted real-row HEAVY segment, the actual recourse is
strictly larger than the `sqrt(k)` right-hand side used by Lemma 3.7.  The
unconditional projector bound `2k` would give only `O(nk)` and does not recover
the displayed `k^(3/2)` rank scale after substituting the sampled-stream row
count.

The construction's rows are real, and its final row is not proved proportional
to an integer row.  It is neither a literal integer input nor a verified
`D A_S` sampled stream.  It also supplies no repeated-event construction.  A
structure-specific argument or different amortized potential may still repair
the sampled-stream analysis.  The accepted result is therefore a scoped
proof-dependency counterexample, not a proof that the integer-domain Lemma 3.7
or Theorem 1.3 is false.

No numerical experiment, scientific dispatch, discovery round, method gate,
novelty gate, or paper gate is advanced by this review.
