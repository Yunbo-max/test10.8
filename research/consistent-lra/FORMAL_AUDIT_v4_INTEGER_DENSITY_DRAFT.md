# Integer-input density extension (draft awaiting independent review)

Base evidence: `FORMAL_AUDIT_v2.md` SHA256 `0cbf0413e49df6f81e135219f0cb6ea994129167d2f900dfc5594bdb0d90d477` and its two-reviewer record. This is a formal consequence of the accepted finite real construction, not a numerical experiment, explicit small example, replacement theorem, originality verdict or claim about the approximate algorithms.

## Claim

There exists a finite integer matrix `A_Z` and an integer row `u_Z^T` such that the optimal rank-`k` projectors before and after appending the row are both unique and

$$
\|P_k(A_Z)-P_k([A_Z;u_Z^T])\|_F^2>8.
$$

The construction is existential through rational density. It gives no useful bound on the common denominator or maximum integer entry.

## Proof

Fix the finite real pair `(A,u)` from `FORMAL_AUDIT_v2.md` at `k=2^210`. Write

$$
C=A^T A,\qquad C^+=A^T A+uu^T.
$$

Both covariances have simple spectra: the eigenvalues of `C` are `1,2,...,2k`, and those of `C^+` are `3/2,5/2,...,2k+1/2`. In particular, each has a positive eigengap at its top-`k` cutoff. Let `P_k(M)` denote the unique top-`k` spectral projector of `M^T M` whenever that cutoff gap is positive.

On the open set of matrices with a positive top-`k` cutoff gap, the spectral projector is continuous in the matrix entries. For example, choose a contour enclosing exactly the top `k` covariance eigenvalues; in a sufficiently small neighborhood the same contour stays in the resolvent set, and the Riesz integral

$$
P_k(M)=\frac{1}{2\pi i}\oint_\Gamma (zI-M^TM)^{-1}\,dz
$$

is continuous. Therefore

$$
F(B,v)=\|P_k(B)-P_k([B;v^T])\|_F^2
$$

is continuous in a neighborhood of `(A,u)`, and both cutoff gaps remain positive there.

The reviewed real construction has the strict inequality `F(A,u)>8`. Hence there is an open neighborhood `U` of `(A,u)` on which both optimal projectors remain unique and `F(B,v)>8`. Rational points are dense in the finite-dimensional real coordinate space, so choose `(\widetilde A,\widetilde u)\in U` with every entry rational.

Let `q` be a positive common denominator of all entries of `\widetilde A` and `\widetilde u`, and define

$$
A_{\mathbb Z}=q\widetilde A,\qquad u_{\mathbb Z}=q\widetilde u.
$$

These entries are integers. Both covariance matrices are multiplied by the same positive scalar `q^2`, which changes neither eigenvectors, cutoff uniqueness nor spectral projectors. Consequently

$$
\|P_k(A_{\mathbb Z})-P_k([A_{\mathbb Z};u_{\mathbb Z}^T])\|_F^2
=F(\widetilde A,\widetilde u)>8.
$$

This proves the claim.

## Dynamic and conditioning consequences

Alternating insertion and deletion of the same integer row gives the same phase-2 dynamic lower bound as `FORMAL_AUDIT_v3_EXTENSION.md`. Thus restricting the exact-optimal dynamic problem to finite integer entries does not restore a rank/dimension-uniform constant per update.

The continuity neighborhood can also be chosen so that the nonzero singular values of every finite matrix used in the fixed construction stay within constant factors of their base values. A common scaling by `q` leaves condition-number ratios unchanged. Hence polynomial conditioning can be retained. This is only a continuity existence statement; it does not give a polynomial bound on `q` or on the maximum integer magnitude `M`.

## Limits and required independent checks

- Verify continuity at both cutoff projectors, simultaneous preservation of the strict recourse inequality and rational-density selection.
- Verify that one common scaling preserves the row-arrival relation and both projectors.
- Check whether the dynamic theorem has any hidden bit-complexity or entry-magnitude dependence before stating the integer corollary against it.
- Do **not** use this to claim failure of Theorem 1.3: that result has an explicit integer-magnitude parameter and separate approximation/proof obligations. Algorithm 4 and the insertion-only approximate results remain outside this argument.
- This existence proof does not make the enormous example executable on the 8 GiB host and is not a benchmark or CPU result.
