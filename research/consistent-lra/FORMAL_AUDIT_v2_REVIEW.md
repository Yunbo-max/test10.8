# Independent review of the unique-spectrum counterexample

Reviewed artifact: FORMAL_AUDIT_v2.md, SHA256 `0cbf0413e49df6f81e135219f0cb6ea994129167d2f900dfc5594bdb0d90d477`. The artifact remains unchanged, including its historical awaiting-review header. This separate record gives the subsequently received review status.

The integration writer records delivered independent reviewer findings below. These are scoped symbolic/source reviews, not a machine-checked proof, signed publication, native evaluation receipt or canonical research gate.

## Assignment: unique-spectrum-counterexample-review

Reviewer `/root/baseline_audit` inspected the exact candidate bytes and the proceedings statement. It independently checked the residue signs, determinant identity, derivative normalization, half-integer products, Wallis-factor induction, crossing-pair count and projector trace identity. Its verdict: no mathematical correction required; the finite construction refutes the stated constant-eight real-matrix lemma with unique optimal projectors. It confirmed R > H_k/18 >= ln(k+1)/18 and the explicit k=2^210 threshold.

The reviewer supplied an exact threshold justification: strict convexity of 1/x on the intervals [1,3/2] and [3/2,2] gives ln 2 > (1/2)/(5/4)+(1/2)/(7/4)=24/35. Therefore 210 ln 2 >144. It recommended explicitly declaring natural logarithms and the polynomial extension of the determinant identity away from its initial poles.

## Assignment: second-unique-spectrum-counterexample-review

Reviewer `/root/execution_capability` was separately assigned the actual candidate, without being given the first review's consensus. It checked the SHA256 before and after review and independently inspected official proceedings Lemma 2.1 and Appendix E. Its verdict: accepted for the stated lemma; no mathematical gap found. Neither lemma statement restricts k, row norms, spectral gaps or dimension.

It independently derived a_j=-P(j)/Q'(j)>0, the secular identity, the eigenvector normalization b_m=1/g'(mu_m), both exact central-binomial product formulas, the induction identity whose difference is 1, a_j,b_m>1/4 for crossing indices and the r crossing-pairs count. Both covariance spectra are simple with strict cutoff gaps, so the optimal projectors are unique.

Its independent exact threshold bound is ln 2 = 2 integral_0^(1/3) 1/(1-t^2) dt > 56/81 > 24/35. This also closes k=2^210 without floating-point arithmetic.

The reviewer diagnosed Appendix E's error: agreement of two covariance operators on W=V_old intersect u-perp does not imply that W is invariant or spanned by common eigenvectors. In this construction every old eigenvector is a coordinate vector and every u_j>0; none is in u-perp. The nonzero W for k>=2 cannot have the claimed spanning property.

## Exposition supplement and limits

All logarithms in v2 are natural. The determinant identity is initially evaluated away from poles and then extends as a polynomial identity. The exact threshold bounds above complete the exposition without changing the reviewed artifact.

Supported: an explicit finite real row-arrival pair with unique projectors and recourse >8; no universal dimension-independent constant for unrestricted optimal-projector recourse.

Not established: a small executable counterexample, a defect in Algorithm 4's additive guarantee, failure of the main existence theorems, originality, publishability, better empirical performance or any native scoring/protocol gate. The enormous construction is formal mathematics and is not dispatched as a CPU benchmark.

Primary targets: official ICLR 2026 proceedings PDF, Lemma 2.1 and Appendix E, and arXiv:2603.02148v1 Lemma 2.3. Originality and downstream dependencies remain pending.
