# FD source-semantic oracle execution record

This is an engineering software/source qualification attempt, not a native
benchmark, performance comparison, theorem proof, scientific experiment or
gate advancement.

## Frozen admission

- Prelaunch branch commit: `b0f6b425d3a22ec41cb6d7ea63b409bb68a75555`.
- Corrected source commit: `c052843d6f9d4389659e71c1a17bcf5f722c048f`.
- Native plan digest:
  `729c080b57df1da31f5a2e98a4d25fe99bce47348c60e81576a6204fb2831eef`.
- Harness plan digest:
  `c460d4af7738793ed67ce204f0c69660de45a0f58e392058da880ca2f40b8cae`.
- Attempt: `fd-semantic-oracles-a1-651e783370394554a7271a2f2b64fa15`;
  one attempt, retry index zero, no GPU.

## Collected execution

The harness completed at `2026-10-09T03:08:34.496800Z`. The native process
exited zero, stderr was empty, and the output reported 45 checks with zero
failures. This completion is not itself an evidence verdict.

- Receipt SHA256:
  `02676afa9a50320d5756e18ddf3cc0e7708f9949499ff9149059aea9b20175ea`.
- Raw oracle output SHA256:
  `8dc34bdced536cadbef966182f759e941e3725f8f400c9d09f780d82a1ee507b`.
- Process guard SHA256:
  `9de1b008eb45ff0a7af5ce6fb42fec08dadf438134a180eb85fdaccd93d863ec`.
- Execution-context SHA256:
  `753fd3229648c8f8cf0b8a80b03becbac426c0556483b7a48b9b0f62d2d92e05`.
- Harness report SHA256:
  `8a39d5afc0c7c4ca58fd27a3787380b955b2319aaeb73d0931fb0a76a8e6cb25`.
- Oracle metric wall/process CPU: `0.00425810399610782` /
  `0.0037859999999999144` seconds; max RSS `115728` KiB.
- Guarded attempt wall: `1.0732064050025656` seconds; harness wall:
  `2.0076340150044416` seconds.

The recorded environment is Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0 and
scikit-learn 1.8.0. All five staged runtime source hashes match the reviewed
plan. The output flags `scientific_gate_advanced=false`,
`performance_claim_eligible=false`, and `theorem_proved=false`.

## Observed semantic boundary

The raw record contains exact per-prefix diagnostics. Production and the
independent same-specification reference had covariance/projector errors within
the predeclared tolerances at every one of eight prefixes; the PSD and
directional-bound checks also passed. This supports no claim until an
independent reviewer verifies the raw bytes, receipt and computation.

The recorded production-to-author covariance distance is zero for the first
three rows and then positive (`5.5352...` at prefix 4); the production-to-
Liberty-visible distance is likewise positive (`6.4031...` at prefix 4).
Thus a later acceptance can qualify the project `ell`-row implementation only;
it cannot relabel the author or Liberty interfaces as prefix-state parity.

The reservation is released by the completed harness state plus this monotonic
ledger record. There is no separate lease-release receipt. Independent
execution-evidence review remains required.
