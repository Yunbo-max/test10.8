# B07 primary-source collision addendum — 2026-10-10

This is a bounded first-pass audit, not an exhaustive novelty verdict. Queries:
`Brand 2002 incremental singular value decomposition thin singular value decomposition rank one updates pdf`;
`GROUSE Balzano Nowak Recht 2010 Grassmannian rank one update subspace estimation online pdf`.
Search engine2; no exposed index version. Primary full texts opened and relevant sections read.

|Source|Located operation|Consequence for this project|Unresolved distinction|
|---|---|---|---|
|Brand, ECCV2002, https://www.merl.com/publications/docs/TR2002-24.pdf, §3 equations2–5|Project incoming columns onto a retained basis, factor the orthogonal residual, diagonalize a bordered small matrix, rotate bases; row insertion by transposition|An incremental SVD update by itself is existing work. Exact untruncated factors differ from a rank-k truncation whose discarded spectrum must be tracked.|A cheap certified approximation must account for accumulated truncation and numerical orthogonality. No implementation or timing here.|
|Balzano/Nowak/Recht, GROUSE2010, https://people.eecs.berkeley.edu/~brecht/papers/10.Bal.Now.Rec.GROUSE.pdf, §3 equations9–12, Algorithm1; §3.2 equations14–15|Rank-one residual gradient and Grassmann geodesic update; explicitly relates its update to incremental QR/SVD|A residual direction or geodesic rank-one rotation cannot be presented as a new primitive. Its sampled instantaneous objective is different from all-prefix LRA loss.|A certified feasible stopping rule and recourse/cost guarantee for the project's all-prefix objective are not established by this bounded reading.|

The earlier B02 exact-top-k target monotonicity theorem uses an exact spectral endpoint. It does not transfer to an arbitrary GROUSE or truncated incremental endpoint. An accepted surrogate endpoint must first have all-prefix loss below the required threshold; endpoint feasibility alone does not certify every intermediate point on a general geodesic.

Next mathematical investigation: construct about20 explicit candidates for certified approximate refresh, including a small augmented projected subspace and residual spectral enclosure; separate known updates from potentially distinct certificate/stopping/recourse claims, independently verify before ranking15 or writing new method code. This is a research question, not a selected new method or originality claim.
