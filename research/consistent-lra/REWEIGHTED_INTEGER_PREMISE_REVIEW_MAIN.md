# Independent review: reweighted-online-PCP integer premise

Reviewer: `/root/reweight_premise_review`
Review type: fixed-byte source and mathematical review; no execution, novelty,
theorem-falsity, method, benchmark, or paper admission.

## Preserved initial review

- Candidate: `REWEIGHTED_INTEGER_PREMISE_AUDIT_MAIN.md`
- Initial SHA256:
  `b039e79ac40812e3f1c9f0c8844a3e7ab575bf6384554adc37bfa4d49c023250`
- Verdict: **NEEDS_CORRECTION**

The initial candidate correctly observed that Braverman et al. Algorithm 5
appends `a_t/sqrt(p_t)` and therefore does not literally output integer rows.
It incorrectly inferred that the determinant-based spectral floor in Lemma F.2
was therefore unavailable.

For the sampled rows, write `M = D A_S`, where `A_S` is the integer row
submatrix and `D_ii = p_i^(-1/2) >= 1`. If `rank(M)=r`, Cauchy--Binet gives

`prod_(j=1)^r sigma_j(M)^2`

`= sum_(|I|=|J|=r) det(M_[I,J])^2`

`= sum_(|I|=|J|=r) (prod_(i in I) D_ii^2) det((A_S)_[I,J])^2 >= 1`.

At least one rank-`r` minor of `A_S` is a nonzero integer, and every diagonal
weight is at least one. Consequently, the exact product floor used by Lemma
F.2 survives the row enlargements. The initial `B_delta` example concerned an
arbitrary bounded real matrix and did not respect this `D A_S` structure.
Common denominators, commensurability, and rounding are not needed for that
spectral-floor argument.

The independently accepted correction target is therefore narrower: the ICLR
proof's sentence that the sampled matrix is integer is unsupported/literally
false for general probabilities, but this alone does not leave the recourse
proof unclosed. Exact representation or bit complexity may remain a separate
question only if separately derived; it cannot be inferred from the rejected
spectral-floor argument.

## Primary-source locators checked

- ICLR 2026 paper, Theorem 2.4 on p. 5: output consists of rescaled rows.
- ICLR overview on p. 15: reduced stream consists of reweighted rows and only
  a polynomial magnitude statement is asserted.
- ICLR Appendix F.2 on p. 22: integer coefficients are used to establish the
  product-of-nonzero-eigenvalues floor.
- ICLR Theorem 1.3 proof on p. 24: sampled `M` is asserted to have integer
  entries before Algorithm 2 is invoked.
- Braverman et al., arXiv:1805.03765v6, Section 3.1, Algorithm 5/Theorem 3.1:
  `p_t=min(1,alpha*tau_t)` and an accepted row is `a_t/sqrt(p_t)`; the theorem
  promises real rescaled rows.

Corrected-candidate rereview is recorded below after its final fixed hash.

## Corrected-candidate rereview

- Corrected candidate SHA256:
  `be08ca12844b2dbc71e0fa1e78bd86ac59f6a0c8184ddca161e17b5896b18d45`
- Verdict: **ACCEPT**

The fixed bytes faithfully distinguish the unsupported literal-integrality
sentence from the sampled-row form `M=D A_S`. The Cauchy--Binet identity is
correct: accepted rows have `0<p_i<=1`, hence `D_ii=p_i^(-1/2)>=1`; a nonzero
rank-`r` integer minor of `A_S` contributes at least one, yielding
`prod_j sigma_j(M)^2>=1`. Appendix F.2's spectral floor therefore extends
without integerization, conditional on the separately asserted sampled-entry
upper bound.

The review does not independently prove that magnitude bound, resolve exact
finite-bit representation, or review `freshSVD`, HEAVY/F.1, aggregate
accounting, theorem-wide correctness, novelty, or execution. The candidate's
reference to Algorithm 5 “lines 6--9” is a non-substantive locator imprecision:
the relevant row update is line 7 and the algorithm ends at line 8. The accepted
hash is preserved rather than silently rewriting that fixed candidate.
