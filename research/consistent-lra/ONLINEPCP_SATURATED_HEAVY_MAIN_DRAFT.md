# Assignment 179: actual OnlinePCP reachability and a saturated small-epsilon HEAVY witness

Status: **frozen source-bound mathematical candidate; independent assignment 180 required**.

Fixed project parent: `main` commit
`e0da36a22e67f756885ef6defe929da9e2f9338e`. Historical branch
`consistent-lra-rsi` is read-only. This card closes neither aggregate
Theorem 1.3 accounting nor originality, native evaluation, method discovery,
scientific dispatch, or paper eligibility.

Primary sources:

1. Woodruff--Zhou, *Consistent Low-Rank Approximation*, ICLR 2026,
   official proceedings PDF, Theorem 2.4 and Algorithm 3 (pp. 5, 8) and
   Theorem 1.3 proof (p. 24):
   https://proceedings.iclr.cc/paper_files/paper/2026/file/b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf
2. Braverman et al., *Near Optimal Linear Algebra in the Online and Sliding
   Window Models*, arXiv:1805.03765v6, preliminaries and Algorithm 5 /
   Theorem 3.1:
   https://arxiv.org/html/1805.03765v6

The first source invokes online ridge-leverage sampling and feeds its sampled,
reweighted rows to Algorithm 2. The second source defines (A^{-1}) as the
Moore--Penrose pseudoinverse and prints
[
 widetildelambda_t
 =rac{|M-M_{(k)}|_F^2}{2k},qquad
 	au_t=2a_t(M^	op M+widetildelambda_t I)^{-1}a_t^	op,
]
[
 p_t=min(1,alpha	au_t),qquad
 Mleftarrow Mcirc a_t/sqrt{p_t}
]
with probability (p_t), where
(alpha=Carepsilon_{m PCP}^{-2}log n).

## Claim A: the literal printed sampler has an empty fixed point

At initialization (M=arnothing), so
(widetildelambda_1=0) and (M^	op M=0). Under the paper's explicit
Moore--Penrose convention, (0^{-1}=0). Therefore
(	au_1=0), (p_1=0), and the first row is not appended. Inductively the
same calculation holds at every time, so the literal displayed Algorithm 5
returns the empty matrix for every nonempty input.

Consequently, “can the printed sampler emit the assignment-178 stream?” has
no nontrivial answer without an omitted initialization/rank-growth convention.
This is a source-level specification defect. It is **not** by itself a
refutation of Theorem 3.1 or Theorem 1.3, because a standard intended repair
may assign probability one to a row outside the current span when the
regularizer is zero.

## Claim B: a minimal rank-growth repair still permits a small-epsilon witness

Adopt only the following repaired convention:

> If (widetildelambda_t=0) and (a_t) is outside the current row span,
> set (p_t=1). Otherwise use the printed formula.

This is a conditional repair for analysis, not an official erratum. Under this
repair, the sampler deterministically emits the following all-integer stream
without reweighting.

Let (mge101), (k=m^2), (eta=1/m<1/100), and (H=m+1). Here (eta)
is Algorithm 2's approximation parameter. Let
(f=1+eta/4). Starting from the first positive optimum, define the actual
integer reset sequence
[
 C_0=1,qquad C_{ell+1}=lceil f C_ellceil .
]
Let (N) be the first reset value at least (9H/(2eta)). Then
[
 rac{4H}{eta}<N<rac{5H}{eta}.
]
The lower inequality is immediate. For the upper inequality, the previous
reset is below (9H/(2eta)), so
[
 N< frac{9H}{2eta}+1
  =rac{9H}{2eta}+rac{9H}{8}+1
  <rac{5H}{eta}
]
for (mge101).

Use unit coordinate rows to build a diagonal covariance with

* (k-H) stable selected coordinates of value (3);
* (H) weak selected coordinates of value (2); and
* (N) tail coordinates of value (1).

After the first (k) coordinate directions are built, each new unit tail row
increases the exact rank-(k) residual by one. The outer-reset values are
therefore exactly the sequence above, and the prefix ending at residual (N)
is a reachable reset with stored cost (N), counter zero, and the stale
top-(k) projector (P).

The HEAVY test holds under either the printed inclusive (m+1)-term block or
the intended (m)-term block. Even the latter has energy (2m), while
[
 rac{eta N}{3}<rac{5H}{3}<2m
]
for (m>5).

Now choose (H) distinct tail coordinates and, one coordinate at a time, add
four further copies of its unit row, raising its diagonal value from (1) to
(5). Let (q) be the number already completed and let (jin{0,1,2,3,4})
be the copies added to the current coordinate. Before the first approximation
failure, the stale-projector excess over the exact optimum is

[
 E(q,0)=3q,quad E(q,1)=3q,quad E(q,2)=3q+1,quad
 E(q,3)=3q+2,quad E(q,4)=3(q+1).
]

The exact optimum is at most (N+q+1). No outer reset occurs during these
updates because its total increase is at most (H<eta N/4). The HEAVY
counter cannot reach (k), because fewer than (4H<k) rows arrive for
(mge6).

For every state with (qlelfloor m/2floor),
[
 E(q,j)le 3q+2<2H<rac{eta N}{2}
 lerac{eta}{2}operatorname{OPT},
]
so the approximation-failure trigger cannot yet fire. After all (H)
coordinates are completed, (E=3H), whereas
[
 rac{eta}{2}operatorname{OPT}
 lerac{eta}{2}(N+H)
 <rac52H+rac{eta H}{2}<3H.
]
Thus a first failure occurs at some intermediate state after strictly more than
(m/2) tail coordinates have already reached value (5).

Every exact top-(k) projector at that trigger must include those (q>m/2)
value-5 tail coordinates, whereas (P) includes none. Hence the exact
RECLUSTER movement satisfies
[
 |P-Q|_F^2ge2q>m=sqrt{k}.
]
This is a reachable single non-reset HEAVY arrival at the small parameter
(eta<1/100).

## Claim C: every row is sampled with probability one

Induct on the stream. Under the repaired rank-growth rule, every new coordinate
direction while the regularizer is zero has (p_t=1). For all other arrivals,
the sampled matrix equals the integer prefix if previous probabilities were
one. Its covariance is diagonal. Before the trigger,
[
 widetildelambda_t
 =rac{operatorname{OPT}_{t-1}}{2k}
 <rac{5H/eta+H}{2m^2}
 =rac{(5m+1)(m+1)}{2m^2}<2.531
]
for (mge101). The arriving unit coordinate has current diagonal count at
most four, hence
[
 	au_t=rac{2}{c+widetildelambda_t}>
 rac{2}{6.531}>0.306.
]
Algorithm 3 uses a PCP accuracy no larger than a constant multiple of (eta);
in particular for the paper's (eta/10)-scale composition,
(alpha=Carepsilon_{m PCP}^{-2}log n) is far larger than (1/0.306)
for the stated sufficiently large constant. Thus (alpha	au_t>1),
(p_t=1), and the induction closes. The stream has unit entries and all
nonzero singular values of every prefix lie between (1) and (sqrt5), so
its online condition number is at most (sqrt5).

Therefore the special probability formula and sampled-row form do not remove
the pointwise HEAVY failure under this minimal intended initialization repair.
The earlier assignment-178 continuity construction is not needed for this
conditional result.

## Exact consequence and retained boundary

If independently accepted, the actual-sampler branch splits as follows.

1. Literal Algorithm 5 is degenerate from the empty state under its own
   pseudoinverse convention, so Algorithm 3 needs an explicit initialization
   repair.
2. Under the minimal standard rank-growth repair above, a bounded-unit,
   constant-condition, small-(eta) stream is emitted unchanged and produces
   one non-reset HEAVY movement greater than (sqrt{k}).

This closes the earlier “arbitrary (D A_S) weights may be unreachable”
objection for a natural repaired sampler, but it still supplies only one
large movement. It does not show repeated recycling, violate the complete
aggregate asymptotic recourse bound, prove Theorem 1.3 false, establish
novelty, or create an admitted method/experiment/paper.

## Frozen falsifier for assignment 180

Review the exact candidate bytes and both primary sources. Check:

* the pseudoinverse convention and empty-state induction;
* whether either source states a contrary initialization convention;
* existence and bounds for the reset value (N);
* the prefix reachability and HEAVY test under both endpoint conventions;
* all five excess formulas and first-trigger inequalities;
* the lower bound on projector movement at a possibly partial current row;
* the regularizer and ridge-score bounds, including every row type;
* the parameter relation used by Algorithm 3; and
* the constant-condition and integer-entry claims.

Return `ACCEPT`, `NEEDS_CORRECTION`, or `REJECT`. Narrow or reject Claim A
if the primary text contains an explicit rank-growth convention. Narrow or
reject Claims B/C if a sampled-probability parameter, tie, earlier reset,
counter reset, or score bound prevents the stated event. Do not infer repeated
events, theorem falsity, novelty, empirical evidence, method admission,
scientific dispatch, or paper eligibility.
