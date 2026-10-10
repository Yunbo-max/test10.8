# B14 mathematical diagnostic and scope

Let `G=A^T A`, let `P` be its exact rank-`k` top spectral projector, and let
`Q` be the retained rank-`k` endpoint immediately before a saved exact query.
Write the eigenvalues as `lambda_1 >= ... >= lambda_d >= 0` and

`r(P,Q)=k-tr(PQ)=sum_j sin^2(theta_j)`.

The exact excess reconstruction loss is

`X = ||A(I-Q)||_F^2 - ||A(I-P)||_F^2 = tr(G(P-Q))`.

Expanding in an eigenbasis, with `p_i=||Q^T v_i||^2`, gives

`X = sum_{i<=k} lambda_i(1-p_i) - sum_{i>k} lambda_i p_i`.

Since the missing top mass equals the spilled bottom mass and both equal
`r(P,Q)`, the deterministic sandwich is

`(lambda_k-lambda_{k+1}) r(P,Q) <= X <= (lambda_1-lambda_d) r(P,Q)`.

This is only a statewise certificate. It does not turn the gap into a refresh
count or CPU theorem. The frozen empirical question is narrower: whether the
gap and overlap quantities distinguish saved true-refresh from query-without-
refresh states on the same native Landmark-512 development prefix.

For a simultaneous-iteration proxy, if `rho=lambda_{k+1}/lambda_k < 1` and
the initial top-`k` overlap is nonsingular, the standard subspace-iteration
angle envelope is `tan(theta_m) <= rho^m tan(theta_0)`. B14 records the
corresponding integer work proxy for a fixed target `sin^2(theta)=1e-6`.
It is not reported as the iteration count of LOBPCG, Lanczos, block Krylov, or
the current full-SVD endpoint implementation.

The near-boundary hard mass is frozen before inspection. It sums missed mass
only over top eigenvectors within ten boundary gaps of `lambda_{k+1}`. Ten is
not tuned after seeing B14. The result is descriptive and dependent across
prefixes; no p-value or independent-sample language is permitted.
