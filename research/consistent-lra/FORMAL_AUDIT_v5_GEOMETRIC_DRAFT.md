# Single row insertion can force linear-in-rank exact-optimal recourse

Status: complete finite mathematical construction awaiting an independent reviewer.
Assignment producing the construction: window02-rankone-finite-bound-primary-source-investigation, /root/window02_scorer_scope_review. Root independently checked products and added the common-shift conditioning corollary below. Neither check is the assignment-bound independent acceptance of this final file.
Fixed prior source snapshot: feba4921a767e0e4163a4aec1bcb8bed335e445b.
Existing-paper M/formal audit, not a new-method pool entry, empirical result, novelty or paper-eligibility decision. Preserve all earlier audits.

## Question, objects and mathematical moves

The accepted half-shift construction proves a logarithmic lower bound and refutes an unrestricted constant-eight claim. The unresolved atomic claim3 in LITERATURE_EQUIVALENCE_20261009_3.md asks whether a universal O(log k) replacement might hold. We test this universally quantified hypothesis directly. H06 constructs an admissible finite counterexample; F01 uses a spectral representation; exact residue identities lead to lower bounds and an invariant common shift (A06). No infinite-dimensional limit is used to assert a finite rate.

For equal-rank projectors define R=||P-P'||_F^2. For every positive integer k, the proposed finite family has dimension2k, simple spectra, unique top-k optimizers and a positive rank-one covariance change implemented by one row arrival. Proposed conclusion R>2k/15. These are exact real-arithmetic claims; no numeric software was executed.

## 1. Strict interlacing and positive rank-one realization

Let a_i=16^i, i=1,...,k. Old spectrum Lambda consists of -a_i,+a_i, and prescribed new spectrum M of -a_i/2,2a_i. In increasing order each old eigenvalue is followed by one new eigenvalue, before the next old eigenvalue: -a_i<-a_i/2<-a_(i-1) for i>1; -a_1<-a_1/2<a_1; a_i<2a_i<a_(i+1) for i<k; and a_k<2a_k. Hence strict positive-update interlacing holds at every position.

Define

$$g(z)=\frac{\prod_{i=1}^k(z+a_i/2)(z-2a_i)}{\prod_{i=1}^k(z+a_i)(z-a_i)},\qquad
\rho_\lambda=-\operatorname{Res}_{z=\lambda}g(z),\quad\lambda\in\Lambda.$$

For the j-th ordered old eigenvalue, numerator has 2k-j+1 negative factors and denominator residue has 2k-j negative factors. Thus every residue is negative and every rho_lambda>0. Equal leading coefficients give

$$g(z)=1-\sum_{\lambda\in\Lambda}\frac{\rho_\lambda}{z-\lambda}.$$

Take D=diag(Lambda), u_lambda=sqrt(rho_lambda). The determinant lemma yields det(zI-D-uu^T)=det(zI-D)g(z), so D+uu^T has precisely spectrum M. Spectra are simple. This inverse rank-one mechanism is established prior art, attributed to the prior Gebert residue/Cauchy audit; it is not claimed as a new algorithm.

## 2. Matched old negative coordinate weight

At lambda=-a_i isolate the same-scale factor to obtain

$$\rho_{-a_i}=\frac34a_i\prod_{j\ne i}
\frac{a_i^2+(3/2)a_i a_j-a_j^2}{a_i^2-a_j^2}.$$

If j<i the denominator is positive and the factor exceeds1. If j>i let r=a_i/a_j=16^(i-j), so 0<r<=1/16. The factor is

$$1-\frac{3r}{2(1-r^2)}\ge1-\frac85r>0,$$

since (3/2)/(1-1/256)=128/85<8/5. For x_j in[0,1], induction proves product(1-x_j)>=1-sum x_j. The finite geometric sum is strictly below1/15. Dropping the factors>1 and applying this inequality proves

$$\rho_{-a_i}\ge\frac34a_i(1-8/75)=\frac{67}{100}a_i>\frac23a_i.$$

The same bound covers i=k, where the empty product is1.

## 3. Matched new positive eigenvector normalization

Differentiating the partial fractions gives g'(mu)=sum_lambda rho_lambda/(mu-lambda)^2>0 at every new eigenvalue. At mu_i=2a_i put b_i=1/g'(2a_i). The vector with entries u_lambda/(2a_i-lambda), multiplied by sqrt(b_i), is a normalized eigenvector x^(i) of D+uu^T. Orthogonality follows from distinct eigenvalues of a symmetric matrix. Differentiating the product at its simple zero gives

$$b_i=\frac65a_i\prod_{j\ne i}
\frac{4a_i^2-a_j^2}{4a_i^2-3a_i a_j-a_j^2}.$$

For j<i, a_j/a_i<=1/16 makes the denominator positive and the factor>1. For j>i use r=a_i/a_j<=1/16. The factor is

$$\frac{1-4r^2}{1+3r-4r^2}=1-\frac{3r}{1+3r-4r^2}\ge1-3r>0.$$

Here1+3r-4r^2>=1. The same finite-product bound therefore gives

$$b_i\ge\frac65a_i(1-3/15)=\frac{24}{25}a_i>\frac9{10}a_i.$$

## 4. Fixed cross-cutoff mass at every scale

For old coordinate lambda=-a_i and new eigenvector mu_i=2a_i,

$$|x^{(i)}_{-a_i}|^2=\frac{\rho_{-a_i}b_i}{9a_i^2}>\frac{(2/3)(9/10)}9=\frac1{15}.$$

Old and new top-k subspaces contain exactly the respective positive eigenvalues. Their projectors P,P' have equal rank. Thus

$$R=2\operatorname{tr}((I-P)P')
=2\sum_{i=1}^k\sum_{j=1}^k |x^{(j)}_{-a_i}|^2
>\frac{2k}{15}.$$

All omitted cross terms are nonnegative. No eigenspace tie or optimizer-selection loophole enters.

## 5. Positive-definite covariances and actual row arrival

Choose c=2a_k and C=D+cI. It has spectrum within[a_k,3a_k], and C+uu^T within[(3/2)a_k,4a_k]. Both are positive definite. Take A=C^(1/2) and append the single row u^T. Then A^T A=C and [A;u^T]^T[A;u^T]=C+uu^T. A is a real2k-by2k diagonal square-root matrix in the chosen coordinate order. Common shift preserves every eigenvector and projector. Both top-k cutoffs are c with exactly k eigenvalues above and k below, so optimizers are unique.

At k=61, dimension122, R>122/15>8. This is an exact symbolic finite counterexample candidate, not a claimed stable float64 computation or native data experiment. Matrix-row entries contain square roots; no integer-row claim is made.

## 6. Rank order and conditioning scope

For any equal rank-k projectors, R=2k-2tr(PP')<=2k. If the lower construction is independently accepted, the supremum over finite positive-definite row-arrival pairs with unique optimizers has order Theta(k), between2k/15 and2k. In particular, an assumption-free O(log k) upper bound is impossible.

The common shift chosen above yields kappa_2(C)=3, kappa_2(C+uu^T)=8/3, kappa_2(A)=sqrt(3). Therefore ordinary full-covariance condition number alone does not restore the rejected logarithmic bound. One can make these full-matrix condition numbers arbitrarily close to1 by increasing c, without changing R. This conclusion does NOT bound the target paper's condition of all consecutive-row submatrices; partial row blocks including u may be much worse conditioned.

The centered spectral scales span an exponential range, and the cutoff gap relative to covariance norm decays exponentially: old gap is2a_1=32, while norm(C)=3a_k. Large common shift hides small spectral separations in nearly equal diagonal values, so bounded full condition does not establish numerical projector stability. No practical finite-precision advantage follows. Bounds imposing relative cutoff gaps, spectral-scale regularity or consecutive-row assumptions remain separate questions.

## Predictions, falsifiers and decision

Prediction: worst-case exact-optimal projector recourse under one positive rank-one row arrival grows linearly in rank, even with bounded full covariance condition numbers. Alternative: the old half-shift log bound is a special evenly spaced family, not a worst-case upper bound.
Falsifiers: interlacing or residue sign fails; either exact product identity is wrong; a denominator changes sign in the claimed range; b_i does not normalize actual eigenvectors; finite product bound is inapplicable; top-k ranks/cutoffs mismatch; common shift invalidates row-arrival representation. Every point requires independent review of this exact file.

If accepted, retire only the prior universal-logarithmic replacement conjecture and strengthen the existing constant-eight proof audit. It does not refute Algorithm4's separate energy argument or the main approximate existence theorem. General spectral sensitivity and residue machinery are established; exact finite application/priority still needs primary collision adjudication. This is one refinement of the existing formal correction contribution, not a second paper merely because scales changed. Scientific experiments0, candidate pool0, selected methods0, eligible papers0.
