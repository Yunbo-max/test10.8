# B04 debug card — primary B03 native Landmark repair

- Observation: the historical first-128 run executed but its NPZ was corrupt. The repaired v2 and v3 commands both produced durable, CRC-valid, self-readable versioned NPZ files with stable hashes.
- Frozen native scope: raw Landmark first 128 rows, (d=2704), (k=25), eta 0.01/0.1, old/new/full, exact prefix SVD, no standardization.
- Artifact repair: same-filesystem temporary NPZ, file `fsync`, CRC and full `np.load`, SHA-256, atomic replace, directory `fsync`, final CRC/read/hash.
- Solver repair v2: all 38 observed near-zero new-solver calls used the exact legacy bisection branch.
- Audit v2: 11/12 predicates passed. Old/new checkpoint projector tolerance failed: maximum (2.5914508\times10^{-8}>10^{-8}) at prefix 114, eta 0.01. Update/query masks, relative loss, recourse and certificates passed.
- Competing cause checked: rank-25/26 singular gap at that point was 0.0107433, so a tied target subspace is not the immediate explanation.
- Child repair v3: post-Newton bracket refinement to width (2^{-40}). It reduced/shifted but did not remove recursive divergence: maximum (2.4943902\times10^{-8}>10^{-8}) at prefix 121, eta 0.01. Relative loss difference was (4.98\times10^{-16}).
- Disposition: same frozen predicate failed after two substantive repairs. Do not rerun 128, relax the threshold, or run 512 in this lineage now. The evidence repair is only partially successful: storage integrity is repaired; strict recursive projector parity remains unqualified.
- Resume condition: create an all-prefix state capture or deterministic replay that compares old/new solvers from the *same* incoming (Q_t), then separate one-step root error from recurrence amplification. Measure whether exact legacy fallback outside the near-zero branch eliminates divergence and what CPU benefit remains before deciding whether to retire or revise the accelerated solver.

This is a development result, not independent confirmation, method novelty, full Landmark comparison, or paper-level PASS.
