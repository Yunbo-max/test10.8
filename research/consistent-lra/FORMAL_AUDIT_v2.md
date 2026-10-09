# Unique-spectrum formal counterexample draft for the constant-eight assertion

Status: exact algebraic construction awaiting independent review. Existing-paper proof audit (M route), not a scientific benchmark, numerical experiment, new-method implementation or originality verdict. Preserve FORMAL_AUDIT_v1.md and its scoped independent review. The following extends its unique-spectrum proof-gap question to a direct recourse lower bound.

## Statement being audited

The ICLR2026 proceedings Lemma2.1 asserts recourse at most8 between optimal rank-k subspaces before and after appending a single row. Corresponding arXiv2603.02148v1 assertion is Lemma2.3. The scope of this draft is that assertion for real matrices; it does not by itself disprove any main existence theorem, which might admit a different algorithm/proof.

## 1. Construct a real row-arrival pair with uniquely determined top-k spaces

Let k be a positive integer and N=2k. Put D=diag(1,2,...,N), and prescribe mu_m=m+1/2, m=1,...,N. Define

$$g(z)=\frac{\prod_{m=1}^N(z-m-1/2)}{\prod_{j=1}^N(z-j)},\qquad
a_j=-\frac{\prod_{m=1}^N(j-m-1/2)}{\prod_{i\ne j}(j-i)}.$$

Exactly one additional negative factor occurs in the numerator relative to the denominator, so every a_j>0. All a_j are explicit positive rational numbers. Since both products defining g are monic of equal degree, partial fractions give

$$g(z)=1-\sum_{j=1}^N\frac{a_j}{z-j}.$$

Let u_j=sqrt(a_j), A=diag(1,sqrt(2),...,sqrt(N)), and append the one row u^T. The covariance before is D and after is D'=D+uu^T. The determinant lemma gives

$$\det(zI-D')=\det(zI-D)\left(1-u^T(zI-D)^{-1}u\right)
=\prod_{m=1}^N(z-m-1/2).$$

Thus both spectra are simple. The old top-k subspace is the span of coordinate vectors j=k+1,...,N. The new top-k subspace contains the uniquely determined eigenvectors m=k+1,...,N. No eigenvalue ties or optimizer-choice loophole is involved.

## 2. Normalize the new eigenvectors exactly

For mu_m=m+1/2, an eigenvector has components proportional to u_j/(mu_m-j). Differentiating the partial fraction identity gives

$$g'(\mu_m)=\sum_{j=1}^N\frac{a_j}{(\mu_m-j)^2}>0.$$

Write b_m=1/g'(mu_m). An orthonormal eigenvector matrix X therefore has squared entries

$$X_{jm}^2=\frac{a_j b_m}{(m+1/2-j)^2}.$$

Distinct symmetric-matrix eigenvalues ensure orthogonality; the derivative ensures unit norm. Define w_n=binom(2n,n)/4^n, including w_0=1. Expanding the half-integer products into factorials gives the exact rational identities

$$a_j=(N-j+1/2)\,w_{j-1}w_{N-j},\qquad
b_m=(m-1/2)\,w_{m-1}w_{N-m}.$$

The second identity also follows directly by differentiating the product formula at its simple zero: b_m=prod_j(mu_m-j)/prod_(q!=m)(mu_m-mu_q). No approximation, floating-point score or asymptotic equality is used.

## 3. An elementary finite lower bound on the cross-space weights

For all n>=0,

$$w_n\ge (4n+1)^{-1/2}.$$

Proof by induction: w_0=1; w_(n+1)/w_n=(2n+1)/(2n+2). The needed squared inequality follows exactly from

$$ (2n+1)^2(4n+5)-(2n+2)^2(4n+1)=1>0.$$

If j<=k, set p=N-j and q=j-1, so p>=q. Hence

$$a_j=(p+1/2)w_p w_q\ge
\frac{p+1/2}{\sqrt{(4p+1)(4q+1)}}\ge
\frac{p+1/2}{4p+1}>\frac14.$$

If m>k, set p=m-1 and q=N-m, again p>=q. The identical argument gives b_m>1/4. Therefore a_j b_m>1/16 for EVERY j<=k,m>k.

## 4. Projector recourse grows at least logarithmically with k

Let P be the old top-k projector and P' the new one. Both have rank k. The component outside the old top-k space is precisely coordinates j<=k, so

$$R=\|P'-P\|_F^2
=2\operatorname{tr}(P'(I-P))
=2\sum_{j=1}^k\sum_{m=k+1}^{2k}X_{jm}^2
>\frac18\sum_{j=1}^k\sum_{m=k+1}^{2k}\frac1{(m+1/2-j)^2}.$$

For every r=m-j in1,...,k there are exactly r such index pairs. Discarding the remaining positive terms and using r+1/2<=3r/2 gives

$$R>\frac18\sum_{r=1}^k\frac{r}{(r+1/2)^2}
\ge\frac1{18}\sum_{r=1}^k\frac1r
=\frac{H_k}{18}
\ge\frac{\log(k+1)}{18}.$$

Choose k=2^210, N=2^211. Since 210log2>144, the final expression exceeds8. This is an explicit FINITE real matrix and a SINGLE appended row, with SIMPLE spectra and unique optimal rank-k projectors, for which R>8.

The dimension is enormous because the elementary lower bound is deliberately loose. That affects practical value and constructibility on an8GiB machine, but not the logical counterexample to an unrestricted dimension-independent assertion. This construction is formal mathematics, not an invented empirical benchmark and not a CPU performance demonstration. No claim of a small practical counterexample is made.

## Scope, evidence and required review

- Verify residue signs, determinant identity, derivative normalization, both factorial identities, the induction, projector trace formula, cross-pair count and explicit dimension threshold independently.
- If correct, this refutes the stated constant-eight assertion even after imposing uniqueness. It does not imply Algorithm4's additive guarantee fails; that energy-trigger argument uses different ingredients.
- Determine every downstream use of the lemma and whether a valid alternative bound can repair it. A failed proof/lemma does not automatically refute a main existence theorem.
- Current primary literature/implementations must be audited before claiming originality or a publishable correction. Elementary Cauchy/residue mechanisms may be known; this is not a novelty verdict or an eligible paper.
- No native numerical scorer, G01/GateA/full-validation gate or scientific CPU experiment has passed. This formal audit has no empirical score.
