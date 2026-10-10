# B04 primary-B03 Landmark repair — frozen development design

This is an evidence repair and resource-calibration batch, not a new method and not confirmation.

## Causal hypotheses

1. The unusable first-128 artifact was caused by direct in-place NPZ writing without a same-command durability/readback boundary. A versioned same-filesystem temporary file followed by file `fsync`, ZIP CRC, full `np.load`, SHA-256, `os.replace`, directory `fsync`, and final revalidation should remove that artifact-integrity failure.
2. At `target <= tol`, floating-point Newton progress is not decision-relevant and may stagnate. Calling the frozen 48-step legacy bisection exactly in that branch should preserve old/new decisions and projectors while retaining the Newton path elsewhere.

## Frozen native scope and falsifiers

- Source: verified raw Landmark Matrix Market bytes, SHA-256 `29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b`.
- Pilot: first 128 rows, all 2704 dimensions, rank 25, no standardization, eta 0.01 and 0.1, old/new/certified-full arms, exact prefix thin SVD.
- Artifact acceptance: versioned target, CRC pass, full self-read, stable pre/post-replace SHA-256; historical corrupt NPZ retained separately.
- Numerical acceptance: zero all-prefix certificate violations; old/new update and query masks identical; relative loss discrepancy at most `1e-9 * max(1, energy)`; checkpoint projector discrepancy at most `1e-8`; total recourse discrepancy at most `1e-8`; every counted near-zero call uses legacy bisection.
- Independent command audit recomputes checkpoint residual, OPT, orthogonality and dense projector movement.
- Any failed predicate blocks the 512-row calibration and triggers diagnosis; it is not a hypothesis refutation.

After all predicates pass, measure exact SVD at native first-512 prefixes 128/256/384/512. This is a resource calibration only, not full 512-prefix evaluation or the author 5000-row protocol.
