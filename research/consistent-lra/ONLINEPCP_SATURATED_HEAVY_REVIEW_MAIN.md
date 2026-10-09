# Assignment 180 — independent fixed-byte OnlinePCP reachability review

## Verdict

**ACCEPT** for the exact corrected candidate at commit
\`61e3e193f94ec5e9bc16b0914d84056986e70068\`.

The initial review of commit
\`d30940639d22f3d18113f53ded1bc95773e22303\` returned
**NEEDS_CORRECTION**: it ignored Braverman et al. Definition 2.1's explicit
rank-growth convention and contained malformed escaped-LaTeX bytes. That
failure is preserved and is not relabelled as accepted.

Reviewer: \`/root/onlinepcp_math_review\`. The reviewer made no repository
writes.

## Fixed sources and bytes

- Candidate:
  \`research/consistent-lra/ONLINEPCP_SATURATED_HEAVY_MAIN_DRAFT.md\`
- Reviewed commit:
  \`61e3e193f94ec5e9bc16b0914d84056986e70068\`
- Candidate Git blob:
  \`436262bc9c81e43e66cb77a5e0c980f29b9151cf\`
- Woodruff--Zhou, *Consistent Low-Rank Approximation*, ICLR 2026,
  official proceedings PDF, Theorem 2.4, Algorithm 3 and Theorem 1.3 proof.
- Braverman et al., arXiv:1805.03765v6, Definition 2.1, Algorithm 5 and
  Theorem 3.1.

A byte scan found no forbidden control bytes in the corrected candidate.

## Source-semantics check

Braverman et al. Definition 2.1 explicitly sets the zero-regularizer online
leverage score of a rank-increasing row to one. The corrected card therefore
does not retain the rejected empty-fixed-point claim. It analyzes Algorithm 5
under the full source convention.

## Mathematical verification

Let \(m\ge101\), \(k=m^2\), \(\eta=1/m\), and \(H=m+1\). The reviewer checked:

1. The reset recurrence
   \(C_{\ell+1}=\lceil(1+\eta/4)C_\ell\rceil\) contains a first value \(N\)
   above \(9H/(2\eta)\), and
   \[
   4H/\eta<N<5H/\eta.
   \]
2. Unit coordinate rows reach the stated diagonal prefix and its exact reset.
3. HEAVY holds under both the printed \(m+1\)-term endpoint convention and
   the intended \(m\)-term convention.
4. All five stale-projector excess formulas are correct.
5. The outer epoch cannot reset during the added rows, the counter cannot
   reach \(k\), and no approximation failure occurs until more than \(m/2\)
   value-5 tail directions have been completed.
6. A failure occurs by completion of all \(H\) directions.
7. At the first failure, every exact top-\(k\) projector contains the already
   completed value-5 directions, so
   \[
   \|P-Q\|_F^2\ge2q>m=\sqrt{k}.
   \]

## Sampling-probability verification

The induction covers every row type.

- Rank-increasing rows have \(p_t=1\) by Definition 2.1.
- For every other row, the current coordinate count is at most four and
  \[
  \widetilde\lambda_t<2.531,\qquad
  \tau_t=\frac{2}{c+\widetilde\lambda_t}>0.306.
  \]
- If the two-sided PCP error is \(\delta\), the ICLR proof's required
  \(1+\eta/10\) transfer is ensured by
  \[
  \frac{1+\delta}{1-\delta}\le1+\frac{\eta}{10}
  \iff
  \delta\le\frac{\eta}{20+\eta}.
  \]
  Such a \(\delta=\Theta(\eta)\) makes
  \(\alpha=C\delta^{-2}\log n\) large enough that
  \(\alpha\tau_t>1\). Hence every row is sampled with probability one.

All entries are unit integers. Every nonzero prefix singular value lies between
\(1\) and \(\sqrt5\), so the online condition number is at most \(\sqrt5\).

## Accepted conclusion

Under the cited source's explicit rank-growth convention and a valid
\(\Theta(\eta)\) OnlinePCP accuracy choice, the bounded-unit,
constant-condition stream is emitted unchanged and yields one reachable
non-reset HEAVY movement exceeding \(\sqrt{k}\).

This removes the earlier concern that assignment 178's free \(D A_S\) weights
might be unreachable: this stronger construction needs no free weights.

## Retained exclusions

The review does not establish repeated-event recycling, an aggregate recourse
lower bound, falsity of Theorem 1.3, novelty or priority, empirical/native
evidence, a new method, scientific-dispatch readiness, or paper eligibility.
It adds no executable attempt, scientific experiment, discovery round, or CPU
usage.
