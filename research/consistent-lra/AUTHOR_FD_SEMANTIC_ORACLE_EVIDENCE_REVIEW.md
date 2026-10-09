# Independent evidence review: author FD semantic oracles

Reviewer: `/root/rice_skin_evidence_review`  
Pinned evidence commit: `9ff1976d22c82ce1686f1485ae9243365e834c59`  
Initial verdict: **needs correction**, recordkeeping/provenance label only.

## Accepted raw evidence

The reviewer independently verified the exact plan digests, all source and
input SHA256 values, the terminal harness/receipt/process records, empty
stderr, one attempt with zero retries, one-thread environment bindings, no GPU,
resource accounting, monotonic counters, and released reservation.  The raw
oracle output SHA256 is
`28193d937bd6468c4aa952c948f39c78577d3e8380f9037a314c0db4b5b90665`.

All 58 checks pass: 48 prefix checks, one snapshot check, eight varying-rank
checks, and one zero-row-source check.  All 36 numeric error/tolerance pairs
satisfy the bound.  The largest rank-one projector error is
`5.617933513637005e-16` against `5e-10`; the largest orthonormality error is
`4.440892098500626e-16` against `5e-12`; the largest rank-two projector error
is `5.610375716070294e-16` against `5e-10`.  Shrink counts are exactly
`[0,0,0,1,2,3,4,5]` and match the independent author branch count.

## Required immutable correction

The native plan, runtime plan, receipt, and attempt preserve the label
`fixed_analytic_streams_and_author_fd_blob_294438c22a95ec9be0169c96c792685661197899`.
The suffix is a transcription error: object
`294438c22a95ec9be0169c96c792685661197899` does not exist in this repository.
The actual frozen object, already checked correctly by the oracle and bound by
the source SHA256 everywhere else, is Git blob
`294438ac128556f01a2c3d920bdb4f1225dd819f`, whose bytes have SHA256
`ba16f17017005dfc90d7ff669678911b2b3e6211582efd4014ed592e44926990`.

This document is the immutable correction binding.  The historical plan,
receipt, harness, and output bytes remain unchanged so their original digests
stay auditable.  No rerun is required because the executed source bytes were
the correctly bound blob; only the human-readable `data_revision` label was
wrong.

Correction rereview verdict: **accepted** at commit
`30a59f1685b46c005dc9522327081c977fa02246`, with this correction record at
SHA256 `5611dbee2372bf9598a8f3c9e43a5001b699e1ac44cd302a6e5b288b72e6ca5e`.
The reviewer compared every retained raw plan, receipt, output, and harness
artifact to evidence commit `9ff1976d22c82ce1686f1485ae9243365e834c59`
and found them byte-identical. Final status:
**accepted after recorded data-revision label correction**.

Even after acceptance, scope is engineering/developmental source semantics
only.  It is not official recourse parity, strong FD, native performance,
theorem evidence, G01/E04/Gate A, confirmation, or a paper claim.
