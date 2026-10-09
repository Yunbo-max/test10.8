# Integer-input density extension (corrected draft awaiting re-review)

Base evidence: `FORMAL_AUDIT_v2.md` SHA256 `0cbf0413e49df6f81e135219f0cb6ea994129167d2f900dfc5594bdb0d90d477` and its two-reviewer record. This is a formal consequence of the accepted finite real construction, not a numerical experiment, explicit small example, replacement theorem, originality verdict or claim about the approximate algorithms.

Revision note: the immutable first draft at commit
`8f35727ad9e096e58936d30437285d01321793ee` received a `needs_correction`
verdict.  It integerized only one fixed `k`, which does not by itself disprove a
rank-uniform linear constant.  This revision keeps the fixed-pair claim and
adds the required separately integerized family over every `k`.

## Fixed-pair claim

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

## Arbitrary-rank integer family and dynamic consequence

For every positive integer `k`, start instead from the corresponding reviewed
real pair in `FORMAL_AUDIT_v2.md`, with `N=2k` and strict recourse

$$
R_k>H_k/18.
$$

Repeat the continuity argument separately for that `k`, choosing its rational
neighborhood small enough to preserve both cutoff gaps and the stronger strict
inequality `F_k>H_k/18`.  Clearing that pair's common denominator `q_k` gives
an integer pair `(A_{Z,k},u_{Z,k})` with exactly the same projectors and
recourse inequality.  No uniform control of `q_k` is asserted.

Now insert the `N` rows of `A_{Z,k}`, followed by `T=N^2` updates alternating
insertion and deletion of the same integer row `u_{Z,k}^T`.  With
`L=N+N^2`, every phase-2 transition is forced between the two unique optimal
rank-`k` projectors, so

$$
\frac{\operatorname{Recourse}}{L}
>\frac{N^2}{N+N^2}\frac{H_k}{18}
=\frac{N}{N+1}\frac{H_k}{18}
>\frac{H_k}{36}\longrightarrow\infty.
$$

Thus restricting the exact-optimal insertion/deletion problem to finite
integer entries does not restore a rank/dimension-uniform constant per update.
This is a family indexed by `k`; no fixed member alone is claimed to have
superlinear-in-`L` recourse.

## Conditioning consequence and its boundary

For each `k`, only finitely many distinct prefix and consecutive-row matrices
occur in the insertion-only base stream.  Intersect the two cutoff-gap
neighborhoods above with open neighborhoods preserving the positive nonzero
singular values of every relevant full-rank prefix/consecutive block (in the
appropriate rectangular sense) within
constant factors of their base values.  The reviewed real family has polynomial
consecutive-block condition number; the sufficiently close rational pair
therefore retains a polynomial bound up to constant factors.  Common scaling
by `q_k` leaves all condition-number ratios unchanged.

This is a per-`k` continuity existence statement.  It provides no polynomial
bound on `q_k`, the maximum integer magnitude `M_k`, or bit length.  The
official exact-optimal dynamic Theorem 2.2 has no such entry-magnitude,
bit-complexity or condition-number parameter, whereas Theorem 1.3 has separate
approximation and bounded-integer-magnitude obligations and is not implicated.

## Limits and required independent checks

- Verify continuity at both cutoff projectors, simultaneous preservation of the strict recourse inequality and rational-density selection.
- Verify that one common scaling preserves the row-arrival relation and both projectors.
- Re-check the arbitrary-`k` quantifier, retained `H_k/18` margin and dynamic
  averaging, rather than accepting the fixed-`k` pair as sufficient.
- Verify the finite open-neighborhood intersection used for the conditioning
  family and retain the explicit lack of a bound on `q_k`, `M_k` or bit length.
- Do **not** use this to claim failure of Theorem 1.3: that result has an explicit integer-magnitude parameter and separate approximation/proof obligations. Algorithm 4 and the insertion-only approximate results remain outside this argument.
- This existence proof does not make the enormous example executable on the 8 GiB host and is not a benchmark or CPU result.

## Independent status

Accepted on correction re-review at immutable candidate commit
`e6ca030dae13084a116659a78d8f1e680e862b95`.  The wording clarification above
does not change the reviewed argument: for the full augmented block,
`sigma_min([B;v]) >= sigma_min(B)` supplies the required control.
