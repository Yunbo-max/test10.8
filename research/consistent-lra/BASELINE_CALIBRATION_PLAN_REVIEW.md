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

Rereview verdict: **pending**.
