# Formal extension draft: rank-uniform linear recourse and downstream dependencies

Status: awaiting independent review. Read together with fixed FORMAL_AUDIT_v2.md SHA256 0cbf0413e49df6f81e135219f0cb6ea994129167d2f900dfc5594bdb0d90d477 and FORMAL_AUDIT_v2_REVIEW.md. This is an existing-paper proof audit, not a new algorithm, benchmark or originality verdict.

Primary source: ICLR2026 proceedings PDF, printed pp3,6,9,19–20. Lemma2.1 is used explicitly for Theorem2.2's exact-optimal O(n) update-recourse claim and for the coreset proof of Theorem1.2. Theorem1.1's additive analysis instead uses LemmasE.1/E.2; the stated Theorem1.3 route uses Theorem2.4 and Lemma3.10. The latter routes have not been fully independently verified here.

## 1. Direct counterexample to rank-uniform O(number of updates) in Theorem2.2

Use v2's arbitrary positive integer k and N=2k, with A=diag(sqrt(1),...,sqrt(N)), u_j=sqrt(a_j)>0, covariances D and D+uu^T, and unique top-k projectors P and P'. Their recourse R_k exceeds H_k/18.

Construct an actual finite update stream starting from the empty matrix:

1. Insert the N rows of A in their displayed order.
2. Perform T=N^2 additional updates, alternating insertion of u^T as the final row and deletion of that same final row. T is even because N is even.

After every update in phase2, the current matrix is exactly A or [A;u^T]. Their uniquely determined optimal rank-k subspaces force every exact-optimal algorithm to output P or P', regardless of computational resources, hindsight or ties during phase1. Every phase2 update incurs precisely R_k. Phase1 recourse is nonnegative and cannot cancel phase2's sum.

There are L=N+N^2 updates. Thus every such algorithm has

$$\frac{\text{total recourse}}{L}\ge\frac{N^2R_k}{N+N^2}
=\frac{N}{N+1}R_k>\frac{H_k}{36}\ge\frac{\ln(k+1)}{36}.$$

This diverges as k tends to infinity. Consequently there is no universal rank/dimension-independent constant C such that exact-optimal projector recourse is at most C L on every legal insertion/deletion stream. This directly targets the rank-uniform O(n) assertion in Theorem2.2, not merely its proof. The notation L denotes the number of updates; matrices in phase2 have N or N+1 rows. Bounds whose implicit constant depends on k are outside this refutation.

An equivalent fixed-row-count formulation toggles the final row of [A;0] between 0 and u^T. These are legal rank-one changes to the rectangular input, and the covariance differences are +/-uu^T. The insertion/deletion formulation above already suffices and does not require classifying a general nonzero-row replacement as a covariance rank-one change.

## 2. Conditioning and bounded-entry checks for this family

Taking traces of D+uu^T and its exact eigenvalues m+1/2 gives

$$\|u\|_2^2=\sum_j a_j=N/2.$$

In particular every squared entry a_j<=N/2. Entries of A are at most sqrt(N), so every matrix in the stream has entries bounded by sqrt(N).

During the initial row insertions, the nonzero singular values are sqrt(1),...,sqrt(s) at prefix s, giving smallest nonzero singular value 1. Matrix A has squared eigenvalues 1,...,N. Matrix [A;u^T] has squared eigenvalues 3/2,5/2,...,N+1/2. Thus every nonempty matrix has smallest nonzero singular value >=1 and largest singular value <=sqrt(N+1/2). The pseudoinverse operator norm is <=1 at every nonempty state.

Therefore both the maximum instantaneous nonzero-spectrum condition number and max_s ||A_s||_2 times max_s ||A_s^dagger||_2 are <=sqrt(N+1/2), polynomial in N and in the update count L. The final-norm/prefix-pseudoinverse definition for the insertion-only stream A followed by u has the same bound. The paper does not explicitly define its online-condition-number convention; cited sampling-source convention still needs checking before claiming an exact identity. Any condition convention bounded by these quantities does not remove this example.

A common positive rescaling makes all entries <=1 without changing any projector, recourse or scale-invariant condition number. No integer-entry or rational-entry counterexample is claimed by this argument.

## 3. Conservative implications and a known baseline repair

The counterexample invalidates the specific rank-uniform O(n) exact-optimal dynamic guarantee. It does NOT by itself refute Theorem1.2's approximate insertion-only existence assertion: the alternating deletion stream differs, and approximate projectors need not be the unique exact optimizers. Its displayed Lemma2.1-dependent proof nevertheless requires repair.

For any two rank-k orthogonal projectors, the elementary identity

$$\|P-Q\|_F^2=2k-2\operatorname{tr}(PQ)\le2k$$

always holds. Therefore a stream of s sampled-row insertions with fresh exact top-k recomputation has total recourse at most2ks. Conditional on a valid simultaneous online PCP with s=O(k epsilon^-2 log^3 n), this gives the familiar O(k^2 epsilon^-2 log^3 n) fallback, rather than the displayed rank-linear conclusion. The approximation is (1+delta)/(1-delta), so the PCP tolerance must be calibrated as delta=epsilon/(2+epsilon) (or a smaller suitable constant multiple); it cannot silently reuse epsilon. This is a known strong/simple baseline, not our new method. Simultaneous-prefix PCP and sampling details still need primary-source qualification.

Algorithm4's additive bound can instead be derived from energy added since the last refresh: loss_t<=OPT_s+(E_t-E_s)<=OPT_t+epsilon E_s whenever no refresh occurs. At a refresh the loss is exact OPT_t. Per-refresh recourse <=2k and geometric energy growth bound the positive-energy refresh count. This reasoning does not use Lemma2.1. For noninteger/normalized data the logarithmic count depends on E_final/E_first_positive; the integer lower bound E_first_positive>=1 does not automatically transfer. Zero prefixes and the chosen warmup/rank convention must be handled explicitly.

No downstream theorem other than the scoped rank-uniform exact-optimal claim is declared false. No fresh empirical comparison, numerical native qualification, novelty gate or eligible result paper follows from these deductions.
