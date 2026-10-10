# B08 prospectively frozen native512 operational timing

Date: 2026-10-10. Frozen before any B08 scientific command.

Question: on the exact native Landmark first512 rows (raw order, d=2704, k=25,
no standardization), does the best existing B07 FD lower-bound gate reduce
actual whole-policy CPU while preserving the baseline's exact-query-confirmed
refresh/output trajectory?

This is development evidence for an attributed existing FD comparator, not a
new method, Gate A confirmation, or the author's literal first1..4999 protocol.
The B07 fixed-checkpoint and modeled-component results are parents, not outcomes
of this timing experiment.

## Arms and semantics

For eta in {0.01,0.1}, compare two operational arms in separate processes:

1. `baseline`: own cached exact OPT; query the exact prefix SVD whenever the
   incoming residual cannot be certified by that cache.
2. `fd50`: the same own-cache policy plus classic delayed unbatched FD width50.
   The gate uses the running maximum of
   `max(0, tail_k(B_t)+(50-k)*Delta_t-tol_t)` and its own exact-OPT cache.

Every queried exact SVD is really computed in that arm. A query supplies both
exact OPT and, if the true inequality is violated, the exact top-k refresh
endpoint. Residual arithmetic, tolerance, refresh map, input rows and numeric
threading are identical. B07 used the same semantic map. Neither arm reuses the
precomputed B07 all-prefix SVD as its oracle.

Primary outcome: per-process algorithm CPU seconds, paired by eta and repeat.
Secondary: command wall/CPU/RSS, exact-query count, refresh count, component
CPU (residual, exact SVD, FD), and exact equality of query/update/output-loss
masks against the frozen B07 reference. Report absolute paired differences and
ratios; prefixes and repeats are not independent scientific samples.

## Prospective execution

- First run one calibration repeat for each of four eta/policy cells. If every
  command is <=120s and the window retains budget, add repeats1 and2 for three
  paired process measurements per cell. Otherwise freeze a smaller completed
  matrix and report why; do not silently change timeout or drop an adverse arm.
- Calibration order is eta0.01 baseline, eta0.01 fd50, eta0.1 fd50,
  eta0.1 baseline. Added repeats alternate arm order within each eta:
  repeat1 fd50 then baseline; repeat2 baseline then fd50. Algorithm timing
  excludes import/input loading and scoring. Each process pays its own first-SVD
  and allocation effects; paired interpretation retains the repeat identity.
- One scientific process at a time; BLAS/OpenMP threads1; RLIMIT_AS2GiB;
  actual cgroup observed8CPU/8GiB. Window <=32 attempts, <=600 command wall,
  <=30min, per command<=120s. No dependency install/GPU/container.
- Atomic JSON+NPZ with flush/fsync/self-read/CRC/hash; input, code, design and
  review hashes pinned in every task. Preserve failures. At most two substantive
  repairs for one failure signature.

Acceptance for scoped timing qualification: all commands exit0; for every run
the query/update masks, queried OPT, and loss trajectory match the appropriate
B07 frozen reference within energy-scaled1e-10; baseline and fd50 update masks
are exactly equal; no output/certificate violation; all reservations settle.
Positive speed evidence additionally requires the FD arm to have lower CPU in
all three paired repeats for that eta and a positive median paired difference.
This is still one development prefix, so it cannot establish cross-dataset
speed, originality, recourse benefit, independent scientific confirmation, or
paper readiness.

Falsifiers: any refresh/output mismatch, certificate failure, timeout, or
non-positive paired CPU result. A failed eta remains adverse evidence; results
are not pooled across eta. Scoring/audit commands are charged and reported but
excluded from policy timing.

Machine step7 after verification: if timing is positive and semantically clean,
use measured costs to freeze a bounded native5000 plan while continuing source/
math collision work. If null/adverse, retain FD as a quality comparator and
return to certified approximate-refresh discovery; do not revive Newton.

