# Landmark developmental baseline-matrix implementation design

Status: complete design candidate, no runner generated and no execution admitted.

## Fixed object and scope

Input is the exact author `landmark.mtx` at commit
`d607c4f6467216c470d1e3b93989d44d5fcdec97`, Git blob
`4c63060bbefcb38e0c705cea1f883d2fb7121f2c`, SHA256
`29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b`.
Retain rows 1--5,000 in released order, no scaling, `k=25`. Drop only columns
identically zero on this prefix, leaving the accepted 259 represented columns.
All algorithm projectors are embedded back into the 2,704-dimensional ambient
space only conceptually; residual loss and pairwise projector recourse are
isometrically unchanged by the zero-column restriction.

This is developmental qualification of existing baselines under the repaired
local scorer. It is not official scorer parity, paper reproduction,
confirmation, Gate A or a new method.

## Frozen 13-arm inventory

The inventory matches the accepted G01 family design and low-dimensional matrix:

- Algorithm 4 at `c in {1.1, 2.0, 2.5, 5.0, 10.0, 100.0}`;
- fresh exact rank-25 prefix subspace;
- fixed subspace after warmup;
- periodic refresh at intervals 10 and 100;
- qualified ell-row Frequent Directions at `ell=50` and `ell=100`;
- frozen-author ell+1 FD diagnostic at `ell=50`, explicitly not a qualified
  strong comparator.

There are no tuned parameters, seeds or replacements. All arms receive identical
rows and use rank `min(25,t)` during warmup and rank 25 thereafter.

## Shared exact reference and independent arm work

Maintain `G_t = sum_{i<=t} a_i^T a_i` and energy `E_t = trace(G_t)` in float64.
At every prefix compute the top `min(25,t)` eigenvalues of symmetric `G_t` with
the reviewed SciPy `eigh` subset convention. Record

`raw_opt_t = E_t - sum(top eigenvalues)`.

With frozen tolerance `tau_t = 1e-10 * max(1,E_t)`, fail if
`raw_opt_t < -tau_t`; otherwise report `opt_t=max(0,raw_opt_t)`. Retain raw
value, top-eigenvalue sum and tolerance. This shared reference is scoring work,
not an arm update. Fresh and every refresh arm must separately compute its own
eigenvectors so their update times are not hidden by reference reuse.

Algorithm 4 refreshes through warmup and when
`E_t >= c * E_last_refresh`. Fixed refreshes through warmup only. Periodic arms
refresh through warmup and thereafter when `(t-k) mod interval = 0`. FD arms use
the already reviewed `native_baselines.py` update semantics on the restricted
stream; all emitted bases are copied and row-orthonormal.

## Repaired scorer

For every arm and every prefix compute

`raw_loss_t = E_t - trace(Q_t G_t Q_t^T)`.

Fail below `-tau_t`; otherwise report `loss_t=max(0,raw_loss_t)`. The ratio is
defined only when `opt_t > tau_t`; otherwise record a missing ratio and count a
violation if `loss_t > tau_t`. Record additive and energy-normalized excess.

Recourse uses the common rank-aware projector identity

`r_t = rank(Q_t) + rank(Q_{t-1}) - 2 ||Q_t Q_{t-1}^T||_F^2`,

with the same dimensionless tolerance as the accepted scorer, failing a
materially negative value and clipping only an in-tolerance negative. Prefix 1
has zero transition increment in the primary total; report initialization from
the zero projector separately as rank 1. Primary steady recourse excludes all
warmup transitions through prefix 25.

At prefixes `{25,150,1000,5000}`, recompute every arm's loss by direct
`||A_t(I-P_t)||_F^2` and recourse by direct Frobenius projector difference.
At `{150,1000,5000}`, independently compare exact OPT with direct SVD tail
energy. Require the accepted `1e-9 * max(1,E_t)` engineering agreement bound,
but never use it to qualify a near-zero ratio denominator. Record selected
projectors for these oracle prefixes only; do not emit a 25x259 basis on every
row.

## Raw outputs and denominators

Retain one raw JSONL member per arm with all 5,000 prefixes: sample ID, rank,
warmup/update flags, energy, raw/reported OPT and loss, ratio/missingness,
excesses, raw/reported recourse, cumulative/steady recourse, orthogonality,
update/reference/scoring/energy times and selected-prefix oracle fields. Retain
13 summaries, an exact manifest and a deterministic tar.gz archive. The manifest
must verify member hashes before atomic no-replace publication; staging remains
retained until evidence collection is complete.

Report two descriptive slices without changing stored rows:

- repaired full denominator: prefixes 1--5,000;
- labelled project slice: prefixes 150--5,000 inclusive, exactly 4,851 rows.

Never call either the paper's Table-1 denominator because the author source has
no recoverable aggregation contract. Report ratio denominators, near-zero
exclusions and positive-loss/near-zero violations separately for each arm and
slice.

## Timing, resources and falsifiers

Set OpenBLAS, OMP, MKL, NumExpr and platform BLAS variables to one before
NumPy/SciPy import; retain argv and process guard. Separately account shared
reference, each arm update, scoring, energy maintenance, serialization and
pipeline time. `ru_maxrss` is process high-water RSS, not per-arm incremental
memory.

The accepted 11-prefix calibration observed median copy-plus-eigensolver times
of 0.001568--0.004070 seconds and a 1.422-second total calibration workload.
This does not qualify the full matrix cost, especially FD updates, serialization
or 5,000 references. A later plan must first perform a bounded all-arm timing
calibration or conservatively reserve from measured source execution; it may not
claim that multiplying 11 timings proves completion time.

Abort and retain failure evidence on any source/hash mismatch, missing prefix,
nonfinite value, materially negative loss/OPT/recourse, orthogonality failure,
direct-oracle mismatch, archive mismatch, duplicate/final output collision,
resource timeout or nonzero exit. One bounded attempt and zero automatic retry
remain mandatory. A valid completed matrix still does not resolve official
scorer parity, prospective confirmation, Parent/Gate0/IPCG or method discovery.
