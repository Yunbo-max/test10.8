# Assignment 178 — independent fixed-byte `D A_S` transfer review

## Verdict

**ACCEPT.** First failing line: none.

For every square `k>=9`, the accepted one-arrival real-row HEAVY witness can
be transferred to a finite stream `M=D A_S`, where `A_S` is integer and every
diagonal entry of `D` is at least one.  The transfer preserves the reachable
HEAVY state, all Algorithm2 branch decisions, and final projector recourse
greater than `sqrt(k)`.

It does not establish that the particular online ridge-leverage sampler can
emit the constructed rows or weights.

## Fixed identities

| Item | Identity |
|---|---|
| Reviewed commit | `97fc0e424ddea8eac706af0eb618624fc2e02dd5` |
| Parent commit | `65b348910205b8f3bba621c3ff80cad4b8d6002b` |
| Candidate | `HEAVY_DAS_TRANSFER_MAIN_DRAFT.md` |
| Candidate SHA-256 / Git blob / size | `6f2468aea1245c7a13d25446add1f0b5a0db18b5c7510c6dc2e771b3325eb7b8` / `6811b210b4d4019af5e6f145580aaa9edeb49880` / 5,744 bytes |
| Review-task SHA-256 / Git blob | `27ca87167f9909f81805cb258d7195abd14f61be87185a9bffe372adff2d1359` / `85067a2b4190538d0fc2b35a8d9a4be8a9ab8772` |
| Assignment175 candidate | commit `ad77490323fee335dc64ae390cc37d61b29646eb`, SHA-256 `92ec4600c73754815a5b652f37c9871da3602e3481c605faf17db25d24d14ac5` |
| Assignment176 acceptance | commit `65b348910205b8f3bba621c3ff80cad4b8d6002b`, review SHA-256 `c7109d99883d528d44327462d848cf0308939f4820d51e2afcfb4fee176f60da` |
| Official ICLR PDF SHA-256 | `ae48c9a75d855fba1ead384ec6860a366542fe2cf383816c03a483edb874ef6f` |

## Strict inherited predicates

At the final accepted prefix, stored cost is `OPT_s`, the counter is zero,
`V=P`, and `HEAVY=TRUE`.  At the accepted final row `u`:

* the top/bottom cutoff gap is `(17/2)a_1>0`;
* `OPT(u)<(1+epsilon/4)OPT_s` strictly;
* `loss(P;u)>(1+epsilon/2)OPT(u)` strictly; and
* `||P-Q(u)||_F^2>(7028/17391)k>sqrt(k)`.

These are the four strictly positive margins used by the transfer.

## Open-neighborhood and rational-density check

The map `v -> C_0+v v^T` is polynomial.  Ordered symmetric eigenvalues and
therefore the sum of the bottom `k` eigenvalues are continuous.  The stale
projector loss is polynomial.  The positive cutoff gap gives continuity of the
top-`k` spectral projector in a neighborhood of `u`, hence continuity of its
squared Frobenius distance from `P`.

The four positive-margin sets therefore have a common open intersection `U`
containing `u`.  Because `Q^(2k)` is dense in `R^(2k)`, choose a rational
`q in U`.  The prefix is unchanged, so no earlier algorithm state or branch is
perturbed.  On the final arrival, the outer reset remains false, the inner
HEAVY failure remains true, the exact top projector is unique, and its recourse
still exceeds `sqrt(k)`.

## Prefix-row and common-scaling check

The accepted reachability prefix contains only positive scalar coordinate
rows: top diagonal rows, the first positive bottom-energy row, unsplit target
increments, and at most two positive coordinate pieces when a capacity
boundary is crossed.  An endpoint boundary needs no zero row.  Thus every
actual prefix row is `r_j=alpha_j e_(h_j)` with `alpha_j>0`.  The prefix is
finite, so `alpha_min=min_j alpha_j>0`.

Let `L` clear all denominators of rational `q`.  Choose an integer multiple
`S` of `L` with `S alpha_min>=1`.  Define the integer base rows

* `a_j=e_(h_j)` for every prefix row; and
* `a_(N+1)=S q` for the final row.

Define diagonal weights `d_j=S alpha_j>=1` on the prefix and
`d_(N+1)=1`.  The globally scaled stream is then exactly `D A_S`, with integer
`A_S` and `D>=I`.

## Full homogeneity check

Global scaling by `S` multiplies every prefix covariance, OPT, stored cost,
fixed-projector loss, and both sides of every outer, HEAVY, and inner comparison
by `S^2`.  Projectors, recourse, counter values, and counter thresholds are
unchanged.  In the LIGHT branch, minimizing-vector comparisons scale by
`S^2`, and row normalization satisfies `S a/||S a||=a/||a||`.  Exact
`RECLUSTER` eigenspaces and any coupled tie choice are unchanged.  Induction
therefore preserves the complete Algorithm2 trajectory and the final
recourse.

The external entry-magnitude bound changes under scaling, but no Algorithm2
branch depends numerically on its declared value.

## Accepted consequence and retained exclusions

The algebraic conditions `M=D A_S`, integer `A_S`, and `D>=I` alone do not
restore the domain-free `r=1` Lemma3.7 bound.  Writing a constructed weight as
`d_j=p_j^(-1/2)` with `p_j=d_j^(-2)` is only a numerical parametrization; it
does not prove that the cited online algorithm computes those probabilities or
selects those rows.

This review does not establish actual sampler reachability, a literal integer
stream, polynomial representation bounds, repeated events, Theorem1.3 falsity,
novelty or priority, native/empirical evidence, a method, scientific-dispatch
readiness, or paper eligibility.  No numerical attempt, experiment, discovery
round, or paper gate is advanced.
