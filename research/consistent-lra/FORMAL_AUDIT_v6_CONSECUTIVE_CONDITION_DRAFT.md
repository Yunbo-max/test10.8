# Geometric-family consecutive-row condition extension — draft

Parent: independently accepted FORMAL_AUDIT_v5_GEOMETRIC_DRAFT.md SHA256 de008df475aba17eb4557fdeb5e7ed57d7843f79dd107ecbed686e40ef717ef5 at a32730715cf772e8c492b1bf880d6e58cbc35617; review FORMAL_AUDIT_v5_REVIEW.md. Author /root/window02_scorer_scope_review, actual assignment window02-geometric-consecutive-conditioning-derivation (85). A different independent reviewer must check this extension; its author and the reviewer who proposed a looser extension cannot accept it.

## Object, hypotheses and construction

For any integer k>=1, retain the geometric rank-one realization a_i=16^i, a=a_k, old centered eigenvalues Lambda={-a_i,+a_i}, updated M={-a_i/2,2a_i}, D=diag(Lambda), u_lambda=sqrt(rho_lambda). Set C=D+2aI, A=C^(1/2) diagonal. Order the diagonal row corresponding to lambda=-a_k first; remaining diagonal rows arbitrary; append u^T last. Let T denote this entire (2k+1) by2k real stream.

Conditioning uses the smallest **nonzero** singular value, not the smallest eigenvalue of a tall row Gram. For every nonempty consecutive-row block B, define cond(B)=sigma_max(B)/sigma_min_positive(B). The proof gives even max_B sigma_max(B)/min_B sigma_min_positive(B) <=sqrt(72/5)<4. Online prefixes and sliding-window blocks are both covered. Braverman et al., Near Optimal Linear Algebra in the Online and Sliding Window Models, arXiv1805.03765v6 section1.4, defines the nonzero singular value convention; online versus sliding-window scope must not be conflated. Historical author manuscript FrameworkI.1 already used all consecutive blocks in CONDITION_SCOPE_SUPPLEMENT_DRAFT.md; keep that historical document untouched.

## Exact derivation

At largest negative scale,
\[
\rho_{-a}=\frac34a\prod_{j<k}\frac{a^2+\frac32aa_j-a_j^2}{a^2-a_j^2}\ge\frac34a.
\]
Each factor exceeds1; k1 empty product is1. Spectrum trace identity gives
\[
\|u\|^2=\frac32\sum_i a_i<\frac85a.
\]
Every diagonal row squared norm d_j²=2a+lambda_j lies in[a,3a]; complete updated covariance has eigenvalues in[3a/2,4a].

Every consecutive block is exhaustively: diagonal-only, u-only, entire T, or proper nonempty suffix S of diagonal rows followed by u. Diagonal-only nonzero squared singulars lie[a,3a]. u-only has one value ||u||²>=3a/2 and<8a/5. Entire T has squared positive singulars[3a/2,4a].

For proper suffix S, its omitted coordinates include first lambda=-a, hence delta=||u_(S^c)||²>=3a/4, ||u_S||²<17a/20. For arbitrary real row coefficients x,y put z_j=d_j*x_j+y*u_j. Then exactly
\[
F=\|B^T(x,y)\|^2=\|z\|^2+\delta y^2.
\]
Since d_j²>=a,
\[
\|x\|^2+y^2\le\frac2a\|z\|^2+(1+\frac2a\|u_S\|^2)y^2
\le\frac2a\|z\|^2+\frac{27}{10}y^2
\le\frac{18}{5a}F.
\]
The last inequality uses2<=18/5 and(18/(5a))*delta>=27/10. Thus B has full row rank and sigma_min(B)²>=5a/18. Row selection yields B^T B<=T^T T, so sigma_max(B)²<=4a. Every nonempty block consequently has its positive squared singular values in[5a/18,4a] and conditioning<=sqrt(72/5)<4. This covers k1, single and two-row blocks; whole T's zero row-Gram eigenvalue is correctly excluded.

## Prediction, falsifiers and limits

Ordering and shift do not change the unique final old/new top-k projectors, so final recourse R>2k/15 remains. k61 gives R>8 under constant conditioning of all consecutive blocks. This rejects assumption-free or bounded-online-condition universal constant/logarithmic rank dependence for **exact** top-k projector recourse. Falsifiers: any wrong residue sign/normalization; failure of delta bound due to row order; omitted class of consecutive block; using zeros rather than positive singular values; failure of equal-rank recourse identity.

This is the same formal correction lineage, not a second method or paper. It does not prove or refute approximate-existence Theorem1.2, repair its proof, certify Algorithm4, or establish novelty. Paper Lemma2.1 and AppendixE make a constant-eight claim; paragraph after Theorem2.4 invokes it, leaving a proof dependency gap. A conclusion could still hold by a different argument. All entries are exact real algebraic; bounded integers/polynomial precision are not proved. Relative cutoff gap still decays exponentially; no stable floating implementation or empirical result is claimed. Ordering matters; arbitrary row subsets/permutations are not covered.

Primary sources: target proceedings https://proceedings.iclr.cc/paper_files/paper/2026/file/b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf ; https://arxiv.org/html/1805.03765v6 ; author manuscript https://pmc.ncbi.nlm.nih.gov/articles/PMC8375632/ . Existing Gebert/Krein/Uebersohn lineage and geometric-card attribution remain authoritative; complete correction priority audit pending.
