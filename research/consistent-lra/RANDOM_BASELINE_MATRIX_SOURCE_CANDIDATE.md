# Prospective random-family baseline matrix: source-review candidate

Status: **not admitted and not executed**.  This record freezes a source/design
candidate for independent review before any plan may be created.

## Identity boundary

The released `consistent-lra-random.py` generator blob is
`cfe96c16b699a96720e41cc36ab36a25a45b4627`.  It calls Python
`random.randint(0,100)` without a recorded seed.  The paper and released code
also disagree about normalization, `c`, and the evaluated prefix range.
Consequently the original Figure 3 stream cannot be reconstructed.

This candidate freezes a **new prospective development instance**:

- shape `3000 x 4`, rank `k=1`;
- Python `random.Random(20261009).randint(0,100)`, row-major;
- no scaling, matching the released code path rather than guessing the paper's
  ambiguous column normalization;
- every per-arm summary and the matrix manifest say
  `original_figure_replication: false`; manifest-linked raw rows identify the
  prospective instance through seeded `sample_id` values.

It may qualify behavior on one member of the released generator family.  It
cannot be described as a reproduction, confirmation or held-out test because
the seed and design have been inspected during development.

## Frozen arms and scorer

The runner reuses the independently reviewed `native_baselines.py` scorer and
arms without changing their semantics.  The 13 arms are Algorithm 4 at
`c in {1.1,2,2.5,5,10,100}`, fresh SVD, fixed, periodic intervals 10 and 100,
strong FD at `ell in {2,4}`, and the author `ell=2` FD diagnostic.  All arms
receive the same generated matrix.  Loss is `||A_t(I-P_t)||_F^2`; recourse is
the sum of squared projector increments under the already frozen initialization
and near-zero-OPT conventions.

The author FD arm remains a diagnostic because its `ell+1` interface differs
from the strong `ell`-row FD interface.  Fresh SVD is a scoring reference and
not a candidate improvement.

## Publication and execution boundary

Candidate runner: `run_random_baseline_matrix.py`  
SHA-256: `27f2a10557ec0c63f92756f0e566912a5c5ed966ff57e3a3662f6987d7f6d67a`

The runner reuses the accepted terminal publication helpers whose source
SHA-256 is `4934100cd9e7b4d91aee361d1c8e09b7f3fb790e06784c137df7a3a012bfab20`.
Raw JSONL and summaries are written under hidden partial names, fsynced,
published by no-replace hardlink, rehashed, and packed into a deterministic
archive.  The manifest is published last and records the prospective matrix
SHA, seed, member hashes, source hashes, timing components, environment and
publication inode observations.  Final/partial/staging path collision and all
five numerical thread variables are rejected.

No command has been admitted.  A later plan, if independently accepted, must
use the pinned RSI harness, one CPU, at most 512 MiB, a calibrated timeout,
zero automatic retries, explicit final-output inventory and post-exit rehash.
An execution can supply only developmental family-instance evidence.  It
cannot close published-random identity, official scorer parity, Landmark,
four-family G01, Gate A or paper readiness.
