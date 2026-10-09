# Assignment 172: reweighted-online-PCP integer-premise audit

Status: **corrected source-bound mathematical audit; independent rereview pending**.

Fixed parent: `main` commit
`09c32113738111503df663988e06ae96ad76f218` (project subtree
`cdb1b4092842788de0db03b2ecdfe1ad7cf432df`). Historical branch
`consistent-lra-rsi` was pinned read-only at
`7286e6d5b301f01ebda45d6fa1387afd9d383906` and contains no project artifact
absent from the reconciled main lineage that changes this premise.

This is not a theorem-falsity, novelty, method, experiment, benchmark, or paper
claim. It audits one displayed inference in the proof of Theorem 1.3 of Woodruff
and Zhou, *Consistent Low-Rank Approximation*, ICLR 2026.

## Exact dependency being checked

The ICLR paper first says that online ridge-leverage sampling produces a stream
of **reweighted** rows. Its overview then says that sampled rows are enlarged by
at most a polynomial factor and therefore their entry magnitudes remain
polynomially bounded. In the formal proof of Theorem 1.3 it makes the stronger
statement that the sampled matrix `M` has **integer** entries bounded by
`M * poly(n)`, and applies Algorithm 2/Lemmas 3.9--3.10, whose stated input
condition is an integer matrix with bounded entries.

Primary locators:

- ICLR 2026 conference PDF, p. 15, lines 1132--1157 in the proceedings text:
  the reduced stream consists of reweighted rows; the text argues only that
  their magnitudes grow by at most `poly(n)`.
- The same PDF, p. 24, Theorem 1.3 proof, lines 2418--2467: the proof asserts
  without an intervening discretization lemma that the sampled `M` has integer
  entries bounded by `M * poly(n)` and then invokes Algorithm 2.
- Braverman et al., arXiv:1805.03765v6 (2023-04-11), Section 3.1,
  Algorithm 5 lines 6--9 and Theorem 3.1: an accepted row is appended as
  `a_t / sqrt(p_t)`, and the theorem promises `(rescaled)` rows over the reals.

URLs:

- https://proceedings.iclr.cc/paper_files/paper/2026/file/b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf
- https://arxiv.org/html/1805.03765v6

Read depth is D3 for the stated proof transition and the cited Algorithm 5/
Theorem 3.1 only. This audit does not claim a complete reread of every proof in
either paper. The author implementation is irrelevant to this purely formal
sampling-to-integer transition and was not treated as proof evidence.

## What the cited theorem actually supplies

For a sampled row, Algorithm 5 defines

`p_t = min(1, alpha * tau_t)`

and appends

`b_t = a_t / sqrt(p_t)`.

Thus an integer input row `a_t` generally becomes a real row. The cited theorem
states projection-cost preservation and a bound on the number of rescaled rows;
it does not state that the row weights are rational, share a polynomially bounded
common denominator, or can be rounded to integers while preserving the PCP event.

The ICLR overview's magnitude statement is a different property. Even granting
`1/sqrt(p_t) <= poly(n)`, it follows only that `|b_t,j| <= M * poly(n)`. It does
not imply `b_t,j` is an integer.

## The special row-scaling structure repairs the spectral-floor step

The literal integrality statement is unsupported, but the sampled matrix is not
an arbitrary bounded real matrix. Let `A_S` be the integer submatrix consisting
of the rows selected by Algorithm 5 and let

`D = diag(p_i^(-1/2))`.

Every accepted probability satisfies `0 < p_i <= 1`, so `D_ii >= 1` and the
sampled matrix is exactly `M = D A_S`. Row scaling by nonzero diagonal entries
preserves rank. If `rank(M)=r`, the rank-`r` Cauchy--Binet identity yields

`prod_(j=1)^r sigma_j(M)^2`

`= sum_(|I|=|J|=r) det(M_[I,J])^2`

`= sum_(|I|=|J|=r) (prod_(i in I) D_ii^2) det((A_S)_[I,J])^2`.

At least one rank-`r` minor of the integer matrix `A_S` is a nonzero integer,
so its squared determinant is at least one. Every multiplier from `D` is also
at least one. Therefore

`prod_(j=1)^r sigma_j(M)^2 >= 1`.

This is precisely the product floor needed by Lemma F.2. Conditional on the
paper's separately asserted upper bound `|M_ij| <= M * poly(n)`, the rest of
the smallest-singular-value/optimal-cost calculation can be repeated for `M`
without making its entries integers.

The rejected initial draft used a bounded real matrix with an arbitrarily small
entry. That example did not have the required form `D A_S` with integer `A_S`
and `D_ii >= 1`, so it cannot diagnose this sampling reduction.

## Corrected verdict proposed for independent rereview

The p. 24 statement that the sampled `M` has integer entries is not supplied by
the cited online PCP theorem and is generally false as written. Nevertheless,
the stronger conclusion originally proposed by this audit does not follow: the
special `D A_S` structure extends the determinant/product floor directly, so no
integerization, common denominator, or rounding lemma is needed for Appendix
F.2's spectral lower bound.

Accordingly this audit **does not identify an unclosed recourse-proof premise on
this ground**. It identifies a repairable proof-writing omission: replace the
false integrality assertion by the Cauchy--Binet argument above, while retaining
the separately required high-probability upper bound on sampled row magnitudes.

Exact finite-bit representation of arbitrary `sqrt(p_i)` weights may be a
separate computational-model question, especially where a bit-space or update-
time claim is intended. This audit has not established that such a concern
changes the mathematical recourse/existence theorem, and it does not elevate it
to a proof gap without a separate bit-model analysis.

The already qualified `freshSVD` PCP route remains a known fallback, but it is
not needed to repair this particular determinant premise.

## Prediction, falsifier, and downstream effect

Prediction: line-by-line verification will confirm both that the cited theorem
does not output integer rows and that every output row retains the form
`p_i^(-1/2) a_i` with `p_i<=1`, making the Cauchy--Binet repair applicable.

Falsifier: either a sampled output not representable as a positive enlargement
of an original integer row, or another use of literal integrality in the
Algorithm-2/Theorem-1.3 chain that is not implied by the `D A_S` structure and
the asserted magnitude bound.

If independently accepted, this closes the reweighted-integer audit as a
**non-blocking wording/proof-detail correction**, not a theorem defect. The
separate HEAVY F.1 flaw, aggregate-accounting question, priority, native
evaluation, new-method discovery, and paper eligibility remain unchanged.
Machine step 7 stays at source/mathematical investigation (2/3), not execution.
