# Low-dimensional native baseline matrix candidate

Status: implementation/design candidate; **not admitted for execution**.

## Question and scope

On the exact frozen first 3,000 offline-scaled rows, what reconstruction and
projector-recourse trade-offs do the repaired existing-method baselines produce
for Rice at rank 1 and Skin at ranks 1 and 2?  This is developmental baseline
qualification under the project repair, not an official-author scorer replay,
fresh confirmation, E04/Gate A, or evidence for a new method.

The three cohorts are:

| Cohort | Frozen source | Rank | Dimension |
|---|---|---:|---:|
| `rice-k1` | author Rice ARFF blob `745655b79f4ca46a3a65a0a8653bd792fa6f7c31`, first 3,000 after released full-data scaling | 1 | 7 |
| `skin-k1` | author Skin TXT blob `fc58dda2eaf5b1f0d2d8c7924a298cd7d14ba17d`, first 3,000 after released full-data scaling | 1 | 3 |
| `skin-k2` | same exact Skin stream | 2 | 3 |

Labels are retained only as source/order metadata and are never features.
Future-aware full-data scaling is explicitly the released fixed-stream
protocol, not an online preprocessing claim.

## Arms and fixed sensitivity

For every cohort, evaluate Algorithm 4 at
`c={1.1,2,2.5,5,10,100}`; `skin-k2` additionally evaluates the paper/source
setting `c=1.5`.  Simple controls are fresh prefix SVD, a fixed warmup
subspace, and periodic refresh intervals 10 and 100.  Strong FD uses every
distinct clipped member of `ell={2k,4k}` satisfying `k<ell<=d`: Rice k1 has
`ell={2,4}`, Skin k1 has `ell={2,3}`, and Skin k2 has `ell={3}`.  The frozen
author diagnostic uses `ell=2` in all cohorts and remains separately labelled;
it is not a strong FD arm.  This gives 13 arms per cohort and 39 total.

There is no tuning against observed outcomes.  All arms receive identical
ordered matrix bytes, rank convention, prefix denominator, repaired scorer,
near-zero-OPT rule, and timing instrumentation.  The Algorithm 4 values are
sensitivity settings of one existing method, never separate contributions.

## Metrics and archive

`native_baselines.run` retains all 3,000 per-prefix records for every arm:
loss, fresh OPT, additive and normalized excess, defined ratio, zero-OPT flag,
projector increment/cumulative/steady recourse, rank/warmup/update flags,
orthogonality, basis and separated update/reference/scoring times.  Each raw
JSONL plus its summary is placed in a deterministic gzip-compressed tar archive
per cohort.  The manifest records member and archive SHA256, exact configuration,
headline aggregates and total process CPU/RSS.  Compression is lossless and
must be independently decompressed/hash-checked before any verdict.

## Falsifiers and interpretation

The execution is invalid if a cohort lacks 13 arms, an arm lacks exactly 3,000
prefixes, any source/hash/rank differs, a raw hash fails after decompression,
any basis/metric is nonfinite, orthonormality exceeds the frozen tolerance,
near-zero OPT is divided through, thread bindings exceed one, or the run does
not terminate inside its reviewed budget.  Any malformed arm blocks only this
matrix and descendants; it is not repaired silently.

A valid result may expose residual accuracy/recourse/cost failures among
existing baselines and bound later G01 planning.  It cannot establish whole-
paper superiority because Landmark and the prospective published-random family
are absent, the scorer is a project repair rather than an independent official
interface, development data are not fresh confirmation, and no new candidate
has passed Parent/Gate0/IPCG or pool review.

## Proposed bounded execution

One reviewed process, one numerical thread, no GPU/network/install/service,
one attempt and zero retry.  The earlier Rice c=2.5 observation measured about
0.5 s pipeline and 120,220 KiB RSS; a conservative candidate reservation is
180 seconds and 512 MiB.  This extrapolation is limited to the low-dimensional
cohorts and says nothing about Landmark.  The exact native/harness plan and
reservation must be created, independently reviewed, and persisted before any
execution.
