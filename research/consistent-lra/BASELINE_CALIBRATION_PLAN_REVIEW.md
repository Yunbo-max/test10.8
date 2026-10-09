# Independent review of the Rice baseline cost calibration

Reviewer: `/root/rice_skin_plan_review`.  No execution, edit, commit or
publication was delegated to the reviewer.

## Initial review

Pinned candidate commit:
`b73897b265745de66b9e63f956c5e08f7405c6cb`.

Verdict: **needs correction**.  The plan document claimed a one-thread cost
calibration, but its immutable command invoked Python directly.  The pinned
harness sets `CUDA_VISIBLE_DEVICES` only, while the native runner inherits its
ambient process environment.  The plan therefore did not bind OpenBLAS, OMP,
MKL or NumExpr thread counts, and its one-CPU reservation could understate
actual numerical concurrency.

The reviewer otherwise accepted the scope and finite bounds: engineering-only
with null protocol, one attempt and zero retry; exact Rice source, first 3,000
prefixes, rank 1 and `c=2.5`; retained direct loss, fresh-SVD tail, projector
recourse and separated clocks; JSONL plus summary; 90-second native and
120-second harness limits; explicit quarantine from scorer parity, figures,
method comparisons, G01/E04/Gate A and performance claims.

Initial identities checked by the reviewer:

- native plan SHA256 `6f624e1c9af2269e386ea1e9cce4cfc4144dc7a5b02e6f256174c27056aebb6c`,
  digest `a2f57074260d0852c0f90ca9e682e4df114151c3636ea9e04de9b087fdbad687`;
- harness plan SHA256 `81d5ca96a1abfa9b7d3a1b228e05d6c4e6dc3bbbaa123438c59adbea47862c0d`,
  digest `659f236d2a595398b37efab8911e2256b76726af05e70a237da5ef121c4a4bca`;
- calibration document SHA256
  `07ec47cc4aef9ac3154596efc6bb34562d725a1662c6ce4680dd49ad75d366e5`.

## Correction

The immutable argv now starts with `/usr/bin/env` and binds
`OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`,
`NUMEXPR_NUM_THREADS=1` and `VECLIB_MAXIMUM_THREADS=1`.  Native and harness
digests and the harness `plan_ref` must be regenerated before rereview.

## Correction rereview

Pinned corrected commit:
`2178300b5350698d2a5283854b6636001f668a24`.

Verdict: **accepted**.  The same reviewer confirmed `/usr/bin/env` is
executable on this host and that the immutable argv binds all five declared
thread variables before the absolute Python interpreter imports numerical
libraries.  The native runner preserves that argv through its process guard;
relative script and data paths resolve in the staged workspace.  No execution
blocker remains within this narrowly reviewed engineering scope.

Corrected identities:

- calibration document SHA256
  `9c82aa0af8ffe31655e99ede1cf3990c5920f57521b53993c68f5858234ec1ee`;
- native plan SHA256
  `eb554cc984595a8f2f4efe3b3b669a582fa70b609a0dcf329c7e6a7742806bab`,
  digest `3478d69f2387ed65c06e382859fb579d65891822cada6cfd6b281b435b9a461c`;
- harness plan SHA256
  `47a8b26eddb6aa4f14a6649ebdc2b96a70bc3678d6093a191edb3af7af9e22e1`,
  digest `3d501cb5b10c3a1e40e377737bc37eef00eda2e56326b3e6a55e73cd931b8d5b`;
- harness `plan_ref` exactly matches the corrected native-plan file SHA.

Acceptance remains cost/coverage calibration only, with all scientific and
official-parity exclusions from the plan unchanged.
