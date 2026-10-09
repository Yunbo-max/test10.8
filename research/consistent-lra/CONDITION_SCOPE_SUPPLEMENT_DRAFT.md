# Consecutive-row conditioning supplement (draft awaiting independent review)

Base artifact: FORMAL_AUDIT_v2.md SHA256 0cbf0413e49df6f81e135219f0cb6ea994129167d2f900dfc5594bdb0d90d477. This supplements the explicit unresolved definition in fixed FORMAL_AUDIT_v3_EXTENSION.md; neither earlier artifact is rewritten.

## Primary definition and reading scope

Braverman et al., *Near Optimal Linear Algebra in the Online and Sliding Window Models*, FOCS2020 author manuscript, https://pmc.ncbi.nlm.nih.gov/articles/PMC8375632/ . FrameworkI.1 defines stream conditioning using every matrix consisting of consecutive input rows, rather than merely the prefixes. TheoremI.2/III.1 concern online rank-k PCP. This author manuscript is the primary source used here. The arXiv identity is 1805.03765; its current version is v6 (11 April 2023), but the versioned PDF retrieval failed in this run, so no claim of reading that PDF or exact version-equivalence is made.

## Explicit polynomial bound for the insertion-only counterexample

Take the insertion-only row stream consisting of all N rows of A=diag(sqrt(1),...,sqrt(N)), followed by u^T from v2. Every nonempty consecutive-row submatrix is one of the following:

1. Diagonal coordinate rows, without u. Its nonzero singular values are sqrt(j) for the selected indices, so its condition number is <=sqrt(N).
2. Only u. It has one nonzero singular value and condition number1.
3. All diagonal rows and u. Its covariance eigenvalues are exactly m+1/2; hence its condition number is <=sqrt(N+1/2).
4. A proper nonempty suffix S={l,...,N}, with l>1, of the diagonal rows followed by u.

For case4, set a_j=u_j^2. The trace identity gives sum_j a_j=N/2. The coordinates of u outside S have squared norm delta=sum_(j<l) a_j>=a_1>1/4, using the independently reviewed v2 crossing-weight bound. Therefore the selected rows and u are linearly independent.

For any real row coefficients x=(x_j)_(j in S) and y, put z_j=sqrt(j)x_j+yu_j. The norm of their combined row is

$$F=\sum_{j\in S}z_j^2+\delta y^2.$$

Since j>=1,

$$\|x\|_2^2\le2\sum_{j\in S}\frac{z_j^2}{j}
+2y^2\sum_{j\in S}\frac{a_j}{j}
\le2\|z\|_2^2+Ny^2.$$

It follows that

$$\|x\|_2^2+y^2\le2\|z\|_2^2+(N+1)y^2
\le4(N+1)F.$$

The smallest nonzero singular value squared of this full-row-rank submatrix is consequently >=1/[4(N+1)]. Its largest squared singular value is <=N+1/2: selecting rows only decreases the full-stream covariance in the PSD order. Thus

$$\kappa_{\mathrm{consecutive}}\le
\sqrt{4(N+1)(N+1/2)}<2(N+1).$$

The bound holds for every consecutive-row submatrix of this particular insertion-only stream. Its length is N+1, so even this stronger stream-conditioning quantity is polynomial in the stream length. Polynomial conditioning therefore does not restore the false constant-eight real-matrix lemma. This does not refute the separate approximate insertion-only existence theorem or qualify its entire sampling proof.

No claim is made that a chronological list of dynamic update events is itself a row-arrival matrix suitable for online PCP. The insert/delete lower bound of v3 is a separate argument. All entries can be simultaneously rescaled to <=1 without changing recourse or condition ratios; they are real and are not asserted to be integers.

## Precision supplement for the known PCP fallback

The v3 fallback uses delta=epsilon/(2+epsilon). Therefore delta^-2=(2+epsilon)^2/epsilon^2. The abbreviated epsilon^-2 asymptotic rate assumes a bounded approximation range, for example 0<epsilon<=1. Outside that range retain the exact factor. This known-baseline clarification is not a new method or a scoring protocol.
