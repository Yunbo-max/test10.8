# B09 frozen design: cached-Gram exact-query comparator

Frozen before any B09 scientific command on 2026-10-10.

## Question

B08 compared the existing FD50 certificate against a baseline whose exact
queries recomputed a full prefix SVD.  Does the scoped FD50 CPU advantage remain
after replacing that oracle in *both* arms by a stronger exact-query
implementation that incrementally caches the prefix Gram matrix and asks LAPACK
only for the leading 25 eigenpairs?

This is an implementation-threat audit for an existing comparator.  It is not a
new method, a novelty claim, or an independent confirmation dataset.

## Mathematics and implementation

For the raw prefix matrix (A_t\in\mathbb R^{t\times d}), maintain
(G_t=A_tA_t^\top) by appending the vector (A_tx_t).  At an exact query,
compute the leading (k=25) eigenpairs ((\lambda_j,u_j)) of (G_t).  Then

[
  \mathrm{OPT}_k(A_t)=\lVert A_t\rVert_F^2-\sum_{j=1}^k\lambda_j,
  \qquad
  q_j=A_t^\top u_j/\sqrt{\lambda_j}.
]

Thus the oracle objective is algebraically exact in real arithmetic.  It reuses the
incremental Gram state and a selective symmetric eigensolver; it is stronger
engineering than the B08 fresh full SVD but supplies the same mathematical
quantity and top-k subspace.  The Gram-update cost is charged on every prefix.
Tied or rank-deficient spectra may make LAPACK choose a different optimal basis;
therefore objective equality alone does not grant deterministic trajectory
equivalence.  Exact B07/B08 mask and loss audits below are mandatory before any
timing interpretation.

## Prospective experiment

- Native Landmark first 512 rows, raw order, (d=2704,k=25), no
  standardization.
- Policies, direct-reconstruction residual arithmetic and eta values are
  unchanged: own-cache baseline versus classic
  delayed FD50 for eta in {0.01, 0.1}.
- Three isolated process repeats per cell, prospectively interleaved:
  repeat0 baseline then FD50; repeat1 FD50 then baseline; repeat2 baseline then
  FD50.  Algorithm CPU covers Gram maintenance, residuals, exact eigenqueries,
  refresh reconstruction, FD maintenance and bookkeeping; input load/save and
  audit are excluded.
- Exact query/update masks, queried OPT values and incoming residuals must match
  the frozen B07/B08 reference at energy-scaled tolerance (10^{-10}).
- Report both within-B09 paired FD speed and the change from B08 full-SVD
  medians.  Repeats measure timing variability and are not independent
  scientific samples.

## 1024-row resource calibration

In a separate command, read the author-source Landmark matrix and materialize
only the first 1024 rows.  Incrementally build its Gram matrix and, at
prefixes 512, 640, 768, 896 and 1024, compare the selective-Gram top-k objective
against a fresh full singular-value decomposition.  Record CPU/RSS and normalized
OPT error.  The calibration asks for eigenvalues only and therefore excludes
operational eigenvectors, basis reconstruction and QR.  This is a
resource/numerical calibration only; it does not execute
the continuous 1024-row policy and cannot establish a 1024/5000 speed claim.

## Outcomes

The B08 speed conclusion survives this implementation threat only if all masks
and numerical checks pass and FD50 is faster in all three paired repeats for
each eta.  A null/reversal is retained as adverse evidence and blocks a
strong-baseline speed claim.  Any semantic mismatch blocks timing
interpretation.  The 1024 calibration is acceptable when every normalized OPT
error is at most (10^{-10}), each command is below 120 seconds and no
reservation remains.

One process at a time, numeric threads1, RLIMIT_AS2GiB, actual cgroup8CPU/8GiB,
at most32 attempts, at most600 command-wall seconds, per command120 seconds,
total window30 minutes.  No GPU, dependency installation or container.

