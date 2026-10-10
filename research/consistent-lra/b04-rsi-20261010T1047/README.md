# B04 primary-B03 Landmark repair

This packet records a bounded repair and rerun of the primary B03 native
Landmark-128 pilot. It is development evidence, not an independent
confirmation or a paper-level result.

## Frozen scope

- Source workflow: `Yunbo-max/Research_Autopilot@7af53173bbd69726877ca04fb77b9466ef1b839d`
- Command transport: `rsi-simple 0.3.0-simple.3`, source digest
  `97cdb752027748261c1d6a11980d10d7a46f2c79c2a00e975f0c08d2c8847893`
- Data: author Landmark matrix, SHA-256
  `29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b`
- Protocol: raw first 128 rows, `d=2704`, `k=25`, `eta in {0.01, 0.1}`,
  old/new/full arms, exact prefix SVD, no standardization.

## Result

The atomic/versioned NPZ repair passed ZIP CRC, full `np.load` self-read,
pre/post-replace hashing, file `fsync`, directory `fsync`, and final readback.
Both solver versions had zero certificate violations, and all 38 observed
near-zero new-solver calls used the exact 48-step legacy bisection branch.

Strict recursive projector parity still failed. V2 had maximum checkpoint
projector difference `2.591450778128931e-8`; V3, which refined the final
bracket to width at most `2^-40`, had `2.4943901532427057e-8`. Both exceed the
frozen `1e-8` threshold. The other 11 frozen predicates passed. The largest
V3 loss discrepancy was only about `5e-16` relative to energy, and the local
rank-25/26 gap was nonzero, so the current leading explanation is recurrence
amplification of small state differences rather than insufficient precision
of one scalar root.

After two substantive repairs of the same failed predicate, this lineage was
stopped. The 512-row calibration and 5,000-row author protocol were not run.

## Reproduction and evidence

The durable raw packet is `consistent_lra_b04_landmark_repair_raw_evidence.zip`,
SHA-256 `de536dc37757675a48df592eb48114e4c888a49c02687cd6707d616782685b21`,
Library ID `libfile_9dcee774aefc8191bb38b6d399cace32`. It contains the
runner database and receipts, versioned NPZ results, source, audit reports,
diagnoses, manifests, and the retained corrupt historical artifact. The large
Landmark source matrix is not duplicated; restore the exact prior source by
the hash above.

Start with `REPORT.zh-CN.md`, `B04_CHECKPOINT.json`, `B04_DEBUG_CARD.md`, and
`FROZEN_DESIGN.md`. Do not resume the stopped runner instance. The next bounded
action is an all-prefix same-incoming-projector replay to separate one-step
root error from recursive state amplification, together with CPU measurement
of broader legacy fallback before revising or retiring the accelerated solver.
