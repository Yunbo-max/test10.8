# Exact proof audit draft: rank-one updates and optimal-subspace recourse

Existing-paper M audit, not new-method discovery, benchmark construction or a performance result. Source: proceedings Appendix E pp.20–21, Lemma2.1; arXiv2603.02148v1 renumbers the corresponding assertion Lemma2.3. Current independently reviewed scope is stated below; no full-theorem refutation or paper eligibility is asserted.

## A. Ties require an optimizer-selection convention

Let d=2k, k>=5, and take A=I_(2k). Append the single row e_(k+1)^T, giving B=A^T A=I and B'=I+e_(k+1)e_(k+1)^T.

The old subspace U=span(e1,...,ek) is an optimal rank-k subspace: every k-dimensional projector captures k units of energy. The new subspace V=span(e_(k+1),...,e_(2k)) is also optimal: it captures the eigenvalue2 plus k-1 eigenvalues1. Their projectors have disjoint support, so tr(P_U P_V)=0 and ||P_U-P_V||_F^2=2k>8.

This exact algebra contradicts an interpretation that bounds recourse for EVERY arbitrary pair of optimizers. A stable tie policy may instead keep k-1 old directions and replace one, with recourse2. Therefore the construction does NOT disprove existence of stable choices, a uniqueness-restricted bound, or the main algorithms. It establishes the need to state which optimizer/tie policy is being bounded.

Independent reviewer /root/baseline_audit checked this algebra and distinction. No numerical experiment was used.

## B. The claimed large eigenspace intersection does not follow, even with unique spectra

Take k=3,d=6, D=diag(6,5,4,3,2,1), u=(1,1,1,1,1,1)^T, A=diag(sqrt(6),sqrt(5),sqrt(4),sqrt(3),sqrt(2),1). Appending u^T realizes D'=D+uu^T as an actual row-arrival covariance update.

Write lambda_j=7-j. A D' eigenvector x for eigenvalue mu satisfies (mu-lambda_j)x_j=u_j(u^T x). No eigenvalue can equal any lambda_j: the corresponding coordinate forces u^T x=0, all other coordinates then vanish, and finally that coordinate vanishes too. Also u^T x cannot vanish for a nonzero eigenvector.

Thus x_j is a nonzero common scalar times u_j/(mu-lambda_j). The secular equation is 1=sum_j u_j^2/(mu-lambda_j). On each interval (lambda_(i+1),lambda_i), its right side decreases continuously from positive infinity to negative infinity, giving exactly one simple root; one further root lies above lambda1. Hence all six eigenvalues are distinct, with strict interlacing.

The old top-three space U is span(e1,e2,e3). Let X consist of the new top-three eigenvectors with eigenvalues mu1,mu2,mu3. Its bottom-three rows form, up to invertible row/column scalings, the 3x3 Cauchy matrix C_(i,j)=1/(mu_j-lambda_(i+3)). The lambda values in these rows are3,2,1; the mu values are distinct and exceed4. Its determinant is a nonzero product of pairwise differences divided by nonzero mu-lambda differences. Therefore the bottom block is invertible.

If Xc lies in U, its bottom coordinates vanish. Invertibility forces c=0. Consequently U intersect span(X)={0}, although k-2=1. This refutes the proof's claimed intersection lower bound under a unique top-k spectrum. A vector w orthogonal to u obeys D'w=Dw, but that does not make w an eigenvector nor make U intersect u-perp invariant under D. Equality on individual vectors is insufficient for the claimed eigenspace containment.

This intersection counterexample alone does NOT show that ||P_U-P_X||_F^2>8. For k3 the universal rank bound is already <=6. Principal angles, rather than exact intersection dimensions, would be needed to repair a constant recourse argument. Independent verification of the complete unique-spectrum derivation is pending.

## C. Consequential next questions and exclusions

1. Recover the precise optimizer selection and assumptions in every use of Lemma2.1. Any bound transferring to numerical baselines must account for ties and null completion.
2. Determine whether the constant8 bound survives under simple spectrum/canonical stable ties; seek a valid principal-angle or spectral-projector proof, or an exact formal counterexample. Do not treat the failed intersection proof as a disproof of that bound.
3. Separately retain the energy-trigger additive argument, which does not depend on this intersection argument. The audit does not establish that Algorithm4's additive guarantee fails.
4. Check current primary versions/corrections and prior spectral perturbation work before presenting a novel result. The above elementary observations are audit findings, not an originality verdict or separate paper.

No numerical qualification, scientific gate, theorem-wide verification or new-paper claim has passed. A formal correction contribution would require its own parent/value/novelty/proof closure before manuscript claims.
