# B06 frozen numerical-metric audit

## Hypothesis

B04/B05 measured the Frobenius projector distance using

`sqrt(max(0, 2*k - 2*sum((Q.T @ V)**2)))`.

For nearly identical rank-`k` subspaces this subtracts two numbers of order
`k`, so floating-point error of order `k*eps` becomes an apparent distance of
order `sqrt(k*eps)`.  At `k=25` in float64 this is about `7.45e-8`, the same
scale as the reported failures.  The frozen prediction is that the B05
`1e-7`-scale discrepancies collapse below their original thresholds when the
same solver outputs are evaluated with a residual-based distance.

## Stable quantity

For orthonormal bases `Q,V`,

`||QQ.T - VV.T||_F^2 = ||(I-QQ.T)V||_F^2 + ||(I-VV.T)Q||_F^2`.

The audit first obtains reduced QR bases and evaluates the two residuals.  It
also records the raw residual calculation, orthogonality defects, the old
cancellation-prone formula, and selected dense-projector controls.  QR does not
change the represented subspace.

## Frozen scope and acceptance

1. Re-evaluate every one of the 148 saved same-input boundary states by running
   both saved B05 solvers on the reconstructed prefix Gram matrix.
2. Deterministically replay both shared-oracle recursive arms and both duplicate
   legacy fresh-SVD controls on native Landmark rows 1--128, `d=2704`, `k=25`,
   `eta in {0.01,0.1}`.
3. Re-evaluate all saved B04 checkpoint basis pairs.
4. A prior numerical-parity failure is classified as a metric artifact only if
   the stable QR-residual distance passes the originally frozen threshold on
   the corresponding replay and selected dense-projector controls agree within
   `5e-12` absolute error.  No threshold is relaxed.
5. This audit changes no algorithm and cannot establish speedup, novelty,
   independent confirmation, a 512/5000-row result, or paper readiness.

The old distances and prior negative decisions remain preserved as historical
outputs; any correction must explicitly identify the invalid numerical metric.
