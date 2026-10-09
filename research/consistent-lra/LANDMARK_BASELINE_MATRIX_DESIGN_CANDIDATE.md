# Landmark developmental baseline-matrix implementation design

Status: corrected complete design candidate, no runner generated and no execution
admitted. The initial independent verdict was `NEEDS_CORRECTION`; its history is
preserved in `LANDMARK_BASELINE_MATRIX_DESIGN_REVIEW.md`.

## Fixed object and scope

Input is the exact author `landmark.mtx` at commit
`d607c4f6467216c470d1e3b93989d44d5fcdec97`, Git blob
`4c63060bbefcb38e0c705cea1f883d2fb7121f2c`, SHA256
`29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b`.
Retain rows 1--5,000 in released order, no scaling, `k=25`. Drop only columns
identically zero on this prefix, leaving the accepted 259 represented columns.
Freeze the active map as the sorted one-based 259-column list retained by
`landmark-reference-calibration-v1`. All chosen supported algorithm projectors
are embedded into the 2,704-dimensional ambient space by zero padding on the
complement. Residual loss and pairwise projector recourse are isometrically
unchanged for those embeddings. This is not equality with arbitrary ambient
nullspace completions.

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

## Versioned scorer extension and two-stage admission

`REPAIR_CONTRACT_v1.md` remains canonical: primary loss is direct residual and
primary OPT is direct fresh SVD. This design proposes, but does not yet qualify,
`LANDMARK_REPAIR_EXTENSION_v1`: an incremental-Gram acceleration that must pass
its own bounded native qualification before the 13-arm matrix plan can exist.
The accepted 11-prefix cost calibration is dependency evidence, not that pass.

Stage A is a separate engineering scorer-qualification task. On prefixes
`1..25` plus `{50,100,150,250,500,1000,2000,3000,4000,5000}`, it compares Gram
OPT versus direct SVD-tail OPT, Gram loss versus direct residual loss for every
arm, and overlap versus direct Frobenius projector recourse for every arm. It
retains both `Q_t` and `Q_(t-1)` at every selected oracle transition.

Loss and OPT agreement use `1e-10 * max(1,E_t)` separately. Recourse agreement
uses dimensionless `1e-10 * max(1,rank_t+rank_(t-1))`. Stage A fails on any
identity mismatch; it cannot adopt the earlier looser `1e-9` calibration
tolerance. Only independent acceptance of Stage A qualifies the extension and
permits a Stage-B full matrix plan.

During Stage B, any prefix with Gram OPT at or below
`10 * 1e-10 * max(1,E_t)` is uncertain and must run direct SVD before ratio
classification. Any arm loss within the same uncertainty band must run direct
residual scoring. If the direct OPT remains at or below its boundary, the ratio
is null; positive direct loss beyond tolerance is a violation. A missing or
failed fallback invalidates the run, never approximately classifies the prefix.

## Shared exact evaluator and independent arm work

Maintain `G_t = sum_{i<=t} a_i^T a_i` and energy `E_t = trace(G_t)` in float64.
At every prefix compute the top `min(25,t)` eigenvalues of symmetric `G_t` with
the reviewed SciPy `eigh` subset convention. Record

`raw_opt_t = E_t - sum(top eigenvalues)`.

With frozen tolerance `tau_t = 1e-10 * max(1,E_t)`, fail if
`raw_opt_t < -tau_t`; otherwise report `opt_t=max(0,raw_opt_t)`. Retain raw
value, top-eigenvalue sum and tolerance. This shared Gram, energy and reference
are evaluator work, not arm state or an arm update. The evaluator charges its
row outer product, energy update, Gram copy and eigensolver to shared-reference
time.

Fresh, fixed, periodic and each Algorithm-4 arm independently maintain their own
Gram and energy from released rows. Each charges its own outer product, energy
update and Gram copy on every prefix, plus its own eigensolver whenever it
refreshes. No arm consumes evaluator Gram, eigenvalues or eigenvectors. FD and
author-FD own and charge only their sketch update/SVD state; they receive no
evaluator Gram state. Serialization is a separate pipeline component.

Algorithm 4 refreshes through warmup and when
`E_t >= c * E_last_refresh`. Fixed refreshes through warmup only. Periodic arms
refresh through warmup and thereafter when `(t-k) mod interval = 0`. FD arms use
the already reviewed `native_baselines.py` update semantics on the restricted
stream; all emitted bases are copied and row-orthonormal.

For zero-energy prefixes, refresh arms use the first `min(25,t)` canonical active
coordinate directions. For nonzero rank-deficient prefixes, request exactly
`min(25,t)` vectors from pinned SciPy `eigh(driver="evr")`, order by descending
eigenvalue, and canonicalize each sign by making its largest-magnitude coordinate
positive (lowest index breaks equal magnitudes). A cutoff tie or nullspace
completion follows this pinned library/environment policy and is labelled as
having no low-recourse theorem guarantee. Warmup rank `min(25,t)` is the existing
repaired-project extension, not source parity.

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

Stage-A oracle prefixes and tolerances are fixed above. Retain both current and
previous bases plus direct and overlap recourse at every selected transition.
Stage B retains direct fallback inputs and outputs for every uncertain prefix.
Do not emit a 25x259 basis on every ordinary row.

## Raw outputs and denominators

After Stage A is independently accepted, retain one Stage-B raw JSONL member per
arm with all 5,000 prefixes: sample ID, rank,
warmup/update flags, energy, raw/reported OPT and loss, ratio/missingness,
excesses, raw/reported recourse, cumulative/steady recourse, orthogonality,
update/reference/scoring/energy times and selected-prefix oracle fields. Retain
13 summaries, an exact manifest and a deterministic tar.gz archive. Each raw and
summary is produced under a partial-only name, closed, file-fsynced and hashed;
the staging directory is directory-fsynced. The archive is produced as a partial,
closed/fsynced, member-hash verified, atomically no-replace published and
directory-fsynced. The manifest is last: partial-only, closed/fsynced, hashed,
no-replace published and directory-fsynced. Final raw/summary/archive/manifest
files are rehashed before process exit and again during post-exit collection.

The successful inventory is exactly 26 complete archive members (13 raw JSONL
plus 13 summaries), one archive and one manifest: 28 files. Staging files,
partials and recreated diagnostic partials stay outside the successful inventory.

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

The accepted 11-prefix calibration observed median evaluator
copy-plus-eigensolver times
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
