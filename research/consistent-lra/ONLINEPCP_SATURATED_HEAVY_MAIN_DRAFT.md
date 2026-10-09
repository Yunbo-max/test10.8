# Assignment 179: actual OnlinePCP reachability and a saturated small-epsilon HEAVY witness

Status: **corrected frozen source-bound mathematical candidate; independent assignment 180 rereview required**.

Fixed project parent: \`main\` commit
\`e0da36a22e67f756885ef6defe929da9e2f9338e\`. The initial assignment-180
review returned **NEEDS_CORRECTION** because the first draft ignored Definition
2.1's explicit rank-growth convention and contained escaped-LaTeX control-byte
corruption. That failed draft remains in commit
\`d30940639d22f3d18113f53ded1bc95773e22303\`; it is not relabelled as accepted.
Historical branch \`consistent-lra-rsi\` is read-only.

This card closes neither aggregate Theorem 1.3 accounting nor originality,
native evaluation, method discovery, scientific dispatch, or paper eligibility.

Primary sources:

1. Woodruff--Zhou, *Consistent Low-Rank Approximation*, ICLR 2026,
   official proceedings PDF, Theorem 2.4 and Algorithm 3 (pp. 5, 8) and
   Theorem 1.3 proof (p. 24):
   https://proceedings.iclr.cc/paper_files/paper/2026/file/b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf
2. Braverman et al., *Near Optimal Linear Algebra in the Online and Sliding
   Window Models*, arXiv:1805.03765v6, Definition 2.1, preliminaries, and
   Algorithm 5 / Theorem 3.1:
   https://arxiv.org/html/1805.03765v6

The first source invokes online ridge-leverage sampling and feeds its sampled,
reweighted rows to Algorithm 2. The second source prints
\[
 \widetilde\lambda_t
 =\frac{\|M-M_{(k)}\|_F^2}{2k},\qquad
 \tau_t=2a_t(M^\top M+\widetilde\lambda_t I)^{-1}a_t^\top,
\]
\[
 p_t=\min(1,\alpha\tau_t),\qquad
 M\leftarrow M\circ a_t/\sqrt{p_t}
\]
with probability \(p_t\), where
\(\alpha=C\delta^{-2}\log n\). It also defines \(A^{-1}\) as the
Moore--Penrose pseudoinverse, but Definition 2.1 explicitly overrides the
zero-regularizer rank-growth case: an arriving row that increases rank has
online leverage score one.

## Source-semantics correction

The isolated quadratic display would give zero at an empty matrix under the
Moore--Penrose convention. It is not the full sampler semantics: Definition
2.1 explicitly sets a rank-increasing row's zero-regularizer online leverage
score to one. Thus there is no accepted empty-fixed-point defect. The result
below uses the source's own convention, not a proposed repair.

## Claim: the source sampler emits a small-epsilon witness unchanged

Let \(m\ge101\), \(k=m^2\), \(\eta=1/m<1/100\), and \(H=m+1\). Here \(\eta\)
is Algorithm 2's approximation parameter. Let
\(f=1+\eta/4\). Starting from the first positive optimum, define the actual
integer reset sequence
\[
 C_0=1,\qquad C_{\ell+1}=\lceil f C_\ell\rceil .
\]
Let \(N\) be the first reset value at least \(9H/(2\eta)\). Then
\[
 \frac{4H}{\eta}<N<\frac{5H}{\eta}.
\]
The lower inequality is immediate. For the upper inequality, the previous
reset is below \(9H/(2\eta)\), so
\[
 N< f\frac{9H}{2\eta}+1
  =\frac{9H}{2\eta}+\frac{9H}{8}+1
  <\frac{5H}{\eta}
\]
for \(m\ge101\).

Use unit coordinate rows to build a diagonal covariance with

* \(k-H\) stable selected coordinates of value \(3\);
* \(H\) weak selected coordinates of value \(2\); and
* \(N\) tail coordinates of value \(1\).

After the first \(k\) coordinate directions are built, each new unit tail row
increases the exact rank-\(k\) residual by one. The outer-reset values are
therefore exactly the sequence above, and the prefix ending at residual \(N\)
is a reachable reset with stored cost \(N\), counter zero, and the stale
top-\(k\) projector \(P\).

The HEAVY test holds under either the printed inclusive \(m+1\)-term block or
the intended \(m\)-term block. Even the latter has energy \(2m\), while
\[
 \frac{\eta N}{3}<\frac{5H}{3}<2m
\]
for \(m>5\).

Now choose \(H\) distinct tail coordinates and, one coordinate at a time, add
four further copies of its unit row, raising its diagonal value from \(1\) to
\(5\). Let \(q\) be the number already completed and let
\(j\in\{0,1,2,3,4\}\) be the copies added to the current coordinate. Before
the first approximation failure, the stale-projector excess over the exact
optimum is
\[
 E(q,0)=3q,\quad E(q,1)=3q,\quad E(q,2)=3q+1,\quad
 E(q,3)=3q+2,\quad E(q,4)=3(q+1).
\]

The exact optimum is at most \(N+q+1\). No outer reset occurs during these
updates because its total increase is at most \(H<\eta N/4\). The HEAVY
counter cannot reach \(k\), because fewer than \(4H<k\) rows arrive for
\(m\ge6\).

For every state whose number of fully completed value-5 tail coordinates is
at most \(\lfloor m/2\rfloor\), including the endpoint obtained by
\(E(q,4)=3(q+1)\),
\[
 E\le 3\lfloor m/2\rfloor+3<2H<\frac{\eta N}{2}
 \le\frac{\eta}{2}\operatorname{OPT}.
\]
Thus the approximation-failure trigger cannot yet fire. After all \(H\)
coordinates are completed, \(E=3H\), whereas
\[
 \frac{\eta}{2}\operatorname{OPT}
 \le\frac{\eta}{2}(N+H)
 <\frac52H+\frac{\eta H}{2}<3H.
\]
A first failure therefore occurs after strictly more than \(m/2\) tail
coordinates have reached value \(5\).

Every exact top-\(k\) projector at that trigger must include those \(q>m/2\)
value-5 tail coordinates, whereas \(P\) includes none. Hence the exact
RECLUSTER movement satisfies
\[
 \|P-Q\|_F^2\ge2q>m=\sqrt{k}.
\]
This is a reachable single non-reset HEAVY arrival at the small parameter
\(\eta<1/100\).

## Every row has sampling probability one

Induct on the stream. By Definition 2.1, each rank-increasing unit coordinate
has zero-regularizer online leverage score one and therefore \(p_t=1\).
For all other arrivals, the sampled matrix equals the integer prefix if
previous probabilities were one. Its covariance is diagonal. Before the
trigger,
\[
 \widetilde\lambda_t
 =\frac{\operatorname{OPT}_{t-1}}{2k}
 <\frac{5H/\eta+H}{2m^2}
 =\frac{(5m+1)(m+1)}{2m^2}<2.531
\]
for \(m\ge101\). The arriving unit coordinate has current diagonal count at
most four, hence
\[
 \tau_t=\frac{2}{c+\widetilde\lambda_t}>
 \frac{2}{6.531}>0.306.
\]

The ICLR proof requires the sampled-prefix optimum to transfer within factor
\(1+\eta/10\), but Algorithm 3 does not state the OnlinePCP accuracy argument
literally in its pseudocode. If the two-sided PCP error is \(\delta\), it is
sufficient that
\[
 \frac{1+\delta}{1-\delta}\le1+\frac{\eta}{10},
 \qquad\text{equivalently}\qquad
 \delta\le\frac{\eta}{20+\eta}.
\]
Thus a valid composition uses \(\delta=\Theta(\eta)\). With
\(\alpha=C\delta^{-2}\log n\), the stated sufficiently large constant makes
\(\alpha\tau_t>1\) by a large margin for \(m\ge101\). Hence \(p_t=1\), and
the induction closes.

The stream has unit entries. Every nonzero singular value of every prefix lies
between \(1\) and \(\sqrt5\), so its online condition number is at most
\(\sqrt5\). Therefore the actual source convention and probability formula do
not remove this pointwise HEAVY failure; the sampler emits the entire bounded
integer stream unchanged.

## Exact consequence and retained boundary

If independently accepted, this closes the earlier “assignment-178 arbitrary
\(D A_S\) weights may be unreachable” objection with a stronger source-faithful
construction: a bounded-unit, constant-condition, small-\(\eta\) stream is
sampled unchanged and produces one non-reset HEAVY movement greater than
\(\sqrt{k}\).

It still supplies only one large movement. It does not show repeated recycling,
violate the complete aggregate asymptotic recourse bound, prove Theorem 1.3
false, establish novelty, or create an admitted method, experiment, dispatch,
or paper.

## Frozen falsifier for assignment 180 rereview

Review these exact corrected bytes and both primary sources. Check:

* Definition 2.1's rank-growth convention and its use in Algorithm 5;
* existence and bounds for the reset value \(N\);
* prefix reachability and HEAVY under both endpoint conventions;
* all five excess formulas and first-trigger inequalities;
* projector movement at a possibly partial current row;
* regularizer and ridge-score bounds for every row type;
* the corrected PCP parameter relation; and
* the constant-condition and integer-entry claims.

Return \`ACCEPT\`, \`NEEDS_CORRECTION\`, or \`REJECT\`. Retain the initial
failed draft/review. Do not infer repeated events, theorem falsity, novelty,
empirical evidence, method admission, scientific dispatch, or paper eligibility.
