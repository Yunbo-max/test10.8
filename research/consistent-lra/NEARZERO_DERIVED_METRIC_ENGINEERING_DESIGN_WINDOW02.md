# Pure derived-metric engineering design — source/scope review required

Author assignment 115, root single integration writer; independent scope/design
review assignment 116. Parent snapshot fa18157ed860dd351f705b31cd80d934785c63c0;
unchanged scientific input snapshot 7d75f63e21cec0a6e29fddd76121f2518246e732.
Status: complete proposed software-contract design, generated_unexecuted. No
software source, executable plan, reservation or execution is admitted here.

## Consequential question and boundary

The independently reviewed Stage-B source corrected a real defect: normalizing
positive energy below one by max(1,energy) changes the requested metric. The
existing source now uses true energy, but no runtime check has qualified its
scalar branch behavior or denominator accumulation. Test those precise software
properties without invoking any matrix evaluator or baseline.

This is deliberately narrower than native scorer qualification. It cannot
establish numerical residual/SVD agreement at previously untested prefixes,
near-zero direct fallback execution, projector correctness, official parity,
performance, a candidate failure, G01/E04/GateA, confirmation or a paper claim.
Stage B remains unexecuted and scientifically blocked. An actual native matrix
queue cannot be renamed as this task, even for debugging.

Installed native-evaluation.md permits non-evaluation software contract fixtures
as engineering work. The proposed process consumes already recorded scalar
values and labeled software literals; it neither acquires a dataset nor computes
loss/OPT/recourse from data. It imports no project module and cannot run the
Stage-B main, loader, eigensolver, FD, Algorithm 4 or matrix multiplication.
Independent reviewer must judge this boundary before any code generation or
finite executable plan. A rejection blocks this task, not independent literature.

## Immutable dependencies and actual existing evidence

Use run_landmark_stage_b.py at source commit
9154c3d171d2579f7feef40318ea8b111994beb8, SHA256
12fa733061a4ec93983cafeb0fbed7af31b19f85c0d1ab875be8de3803457f5e
(unchanged at the parent snapshot). Preserve both old source eb3f7dc... and its
initial rejection; do not edit Stage B to make a fixture pass.

Reuse independently accepted Stage-A v2 full packet at evidence commit
bc80f1be00f772a8c462f807444cdd4e2b67de35:

- runs/attempts/landmark-stage-a-v2-qualification-02/landmark-stage-a-v2-identity-a1-4132a34d9d364ec9b556ac5d64803735/workspace/evidence/qualification/landmark-stage-a-v2-qualification.json
  SHA256 a0523b88fbc96adae1f035ce9c9974a0d3ae9fe97f3e7ff782c363e6177f6ae7.
- Same directory: landmark-stage-a-v2-qualification.oracles.jsonl.manifest.json,
  SHA256 26c10453a0af471bd3d6c9b089292a7a444f878a56ef2ab351a27aa5212df84a.
  It binds exactly 35 named gzip members, 13 original records per member; input
  member names, bytes and hashes must be taken from this manifest, not a glob
  admitting .partial files. Read and hash every complete member before use.
- LANDMARK_STAGE_A_v2_FULL_EVIDENCE_REVIEW.md, SHA256
  65d566101933c540a6f1e879418f6c1f72f7b186a20bfe4f9c8851bdf015d714.

Each of the 455 records already contains energy, raw/clipped Gram OPT and loss,
direct SVD OPT, direct loss, overlap recourse, original prefix/rank/arm and
initialization increment. Decode these scalars only; do not interpret or evaluate
stored bases. Retain original record identity and byte lineage. Do not modify or
renormalize native rows. Existing first energies include 0.2500000372529044,
0.4939165277733947, 0.7276478959937926 and 0.957810360844844. This is the actual
reason energy<1 behavior matters, not a conjectured scientific failure.

## Source-bound isolated program

A future complete stdlib-only qualification runner must parse the pinned source
with ast, not import it. No uncontrolled exec of a module is permitted. It must
find exactly one assignment for each target below in main and preserve each
original expression, AST position and source segment hash:

`tolerance`, `band`, `opt_fallback`, `opt`, `near_zero`, `loss_fallback`,
`loss`, `increment`, `ratio`, `excess`.

From the unique `row` dictionary assignment, separately select only the values
for `energy_normalized_excess`, `near_zero_positive_loss_violation`,
`opt_source`, and `loss_source`. Reject missing/duplicate selections, unknown
names, calls other than builtin max, attributes, subscripts, comprehensions,
imports and any statement other than the selected assignments. Reorder only into
the original source dependency order. Free input names are exactly energy,
gram_opt, direct_opt, gram_loss, direct_loss, t, rec; the generated temporary
expression targets are declared explicitly. Source labels are pure literals and
conditional expressions. Whitelist operators, compare operators and constants
before compile. Python provides only the explicit max builtin, no import/open
capability. This tiny program exercises copied exact scalar source bytes, not
Stage-B evaluator execution. Record its extracted-source and AST digest.

OPT and loss inputs in recorded rows are already finite/clipped. Negative raw
value clipping belongs to previously qualified Stage A; this task does not
execute checked_nonnegative or assert new coverage of that function.

Separately, AST-extract literal DESCRIPTIVE_FIELDS and the pure functions
new_slice/add_slice. Their allowed operations must be exhaustively checked:
local/dictionary/list arithmetic, append, declared field iteration and int;
no file access, numerical library, arbitrary attribute/call or project import.
Source qualification must define the exact node/call whitelist before compiling
these functions. Retain the original source segments. Do not execute the
whole-source aggregation/publication loop: the final summary reducer can be
checked statically here, while a future source-bound extraction requires its own
review. This initial design qualifies accumulation and eligibility denominators,
not final emitted summaries or the 28-output publication path.

## Independent scalar oracle and finite case inventory

The independent oracle uses supplied scalar inputs and the published project
contract, not the extracted expressions. It computes expected classification
and derived values with exact Fraction representations of float inputs wherever
an arithmetic reference is needed. Nullness, source labels, booleans and counts
must agree exactly. Finite arithmetic values must match correctly rounded
float references within at most four ulps of the reference (absolute subnormal
spacing where relevant); no tolerance based on max(1,energy) is permitted for
normalized excess. For direct native scalar routing, retain all supplied direct
values and never recompute them.

1. All 455 retained native scalar records: original order and identities; expected
   tau=1e-10*max(1,E), band=10*tau, uncertainty if GramOPT<=band, selected direct
   OPT when uncertain, near-zero iff selectedOPT<=tau, direct loss chosen when
   near-zero or GramLoss<=band. Expected ratio missing iff near-zero; otherwise
   loss/OPT. Excess remains signed loss-OPT. Positive E uses excess/E; zero E is
   undefined. Prefix1 primary increment zero; later increment supplied recourse.
   These are software-derived values, not new native performance observations.
2. Labeled scalar branch fixtures, never scientific samples: zero E with zero
   loss/OPT; positive E below one and above one; exact tau/band boundaries and
   math.nextafter immediately below/above each; direct OPT moving an uncertain
   Gram value across tau; near-zero OPT forcing large GramLoss to supplied direct
   loss; certain OPT with uncertain GramLoss; direct loss above/below/equal tau;
   signed small negative excess; prefix1 versus prefix2 initialization. Freeze
   explicit float/hex input and exact expected output records before execution.
   No matrix, fabricated benchmark, or performance score is created.
3. Fail-closed fixture validation rejects NaN/Inf, negative energy or supplied
   clipped OPT/loss/recourse, missing required direct inputs on a chosen branch,
   duplicate/missing fixture IDs, unexpected fields or non-integer t<1. These
   are runner input-contract checks, not new rejection behavior attributed to
   the Stage-B source. Keep that attribution explicit.
4. Accumulator tests use labeled scalar fixture rows containing all 16 declared
   descriptive fields. Exercise defined/missing ratio and normalized excess,
   no-defined cases, signed excess, and near-zero positive-loss counts. Every
   new_slice/add_slice collection and sum is compared to an independent
   batch-derived reference; count closure must hold at each append. Native rows
   are not duplicated or called a complete native slice. The test can feed a
   finite literal collection such as 7 rows; it must not claim the original
   full5000 or inclusive4851 summary was runtime-qualified.

The fixture inventory must be committed with all IDs/expected outputs before
plan review. Any mismatch retains both source output and expected output as a
software failure, not scientific counterevidence. Finite cases qualify only these
branches; no universal floating error theorem or pipeline pass follows.

## Resources, commands, artifacts and repair rules

Only after this design is independently accepted: register a complete runner
source generation task and a separate independent source review. The full runner
must have actual CLI arguments for source, accepted packet inputs, frozen fixture
file and exclusive output directory; source must include acquisition/manifest
checks and bounded failure collection, not a placeholder. Use existing stdlib
only. Do not import numpy/scipy or any scientific project module.

A later native/harness plan pins the actual generated runner/fixture/source/input
bytes and independent source/design reviews; no nonexistent file can be pinned.
Use the unchanged historical project execution harness, one process, one CPU,
256MiB reservation (state whether enforced), 60s inner/90s outer timeouts,
one executable attempt and zero automatic retries. Recheck actual CPU/RAM and
remaining deadline; no launch after17:10:43Z. These are proposed upper bounds,
not a present reservation or calibrated usage guarantee. The plan reviewer can
require a smaller collection/calibration first; preserve actual cost either way.

Successful outputs: one JSONL record per native scalar input and per fixture,
a manifest with input/extracted-source hashes, complete IDs/counts and
acceptance failures, scope flags, argv/timestamps/RSS/process and pipeline CPU,
and a summary. Write exclusive partial files, close/fsync/hash, publish
no-replace, directory fsync, post-exit rehash twice, and exact-commit byte readback.
Raw evidence labels must say derived_scalar_contract_only and
software_fixture_only; native_evaluator_qualified, nearzero_matrix_fallback_qualified,
stage_b_execution_admitted, scientific_gate_advanced and performance_claim_eligible
all remain false. No paper-table/performance aggregate may be emitted.

On source/dependency mismatch, unapproved AST, fixture mismatch, decode/hash
failure, source-output discrepancy, timeout or nonzero exit: retain logs/partial
and failed predicates, no automatic rerun. Any source defect needs an independent
record and separately frozen correction contract; preserve original source.
A retry requires actual changed evidence and the project repair bounds, not a
counter reset. On success independent evidence review checks actual argv,
receipts, raw outputs/hash/denominators, cost and scope before any engineering
acceptance. It still cannot release Stage B's scientific authority block.

## Specific remaining obligations

Direct SVD/residual substitution over every uncertain native prefix, numerical
recourse correctness, full/scoped descriptive summary finalization, full native
baseline performance and formal evaluator replay remain separate pending tasks.
A positive scalar test can close source routing/missingness/accumulation only.
This is not the requested scientific comparison and cannot become discovery
failure evidence or a prospective confirmation dataset.
