# Landmark exact-reference calibration candidate

Status: generated source candidate, not executed and not admitted.

`calibrate_landmark_reference.py` measures the cost and numerical agreement of
the exact rank-25 prefix reference needed by the repaired scorer. It consumes
the frozen author `landmark.mtx` blob, retains the first 5,000 rows in source
order, and removes only columns identically zero on those rows. The accepted
mechanical evidence predicts 259 represented columns; this is an isometric
restriction for right-space residuals, not a rank claim.

The frozen prefixes are 25, 50, 100, 150, 250, 500, 1000, 2000, 3000, 4000
and 5000. At each, the script performs three top-25 symmetric-Gram eigenvalue
references. Every reference time includes the Gram copy and records copy and
solver time separately. The raw Gram residual, top-25 eigenvalue sum and frozen
`1e-10 * max(1, energy)` cancellation tolerance are retained; a residual below
the negative tolerance fails, and only an in-tolerance negative value is clipped
to zero for reporting. Prefixes 150, 1000 and 5000 also receive an independent
direct-SVD tail-energy check against both raw and reported Gram residuals. Its
`1e-9 * max(1, energy)` agreement tolerance is engineering-only and does not
qualify a near-zero optimum as a future ratio denominator.

Internal wall and CPU timing begins after NumPy/SciPy import and ends before JSON
serialization/write. `ru_maxrss` is process high-water RSS, not incremental
allocation; the future harness receipt remains authoritative for workload and
pipeline cost. The script does not enforce or observe a thread count. A reviewed
harness must set OpenBLAS, OMP, MKL, NumExpr and platform-BLAS thread variables to
one before process start/import and retain those settings and the CPU guard.

This is engineering calibration only. It does not run Algorithm 4, FD, fixed,
periodic or fresh-SVD arms; it does not estimate a baseline win, reproduce
Table 1, admit the complete 5,000-prefix queue or advance a scientific gate.
Execution requires independent source/semantic review followed by a separately
reviewed one-CPU harness plan with one attempt, zero retries and a short timeout.
