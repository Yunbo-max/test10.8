# Frequent Directions source-semantic qualification candidate

Scope: existing-baseline engineering qualification only. The deterministic
matrices are software unit-test oracles, not native benchmark data, a paper
experiment, a performance result, or a proof of the FD theorem.

## Frozen implementations

Three different update interfaces must remain separately named:

1. The project strong baseline is an `ell`-row, compress-before-insert FD with
   `k < ell <= d`; its output is the top-`k` right singular subspace of the
   weighted sketch.
2. The author archive at `d607c4f6467216c470d1e3b93989d44d5fcdec97`
   uses an `ell+1` augmented SVD after all `ell` stored rows are nonzero. The
   released experiment sets `ell=k=25`, and its `get_sketch()` returns the live
   internal array. It is a source-diagnostic arm, not the qualified strong FD.
3. Liberty's source at
   `691df9edb2ffbc2fdddc2cec3b703a3f1e438d4d`, blob
   `4bb3500cbea9c81c21cbeea5cd5db60ac4006d3d`, buffers `2ell` rows, compresses
   to the leading `ell`, and `get()` returns only those leading rows. Pending
   lower-buffer rows therefore are not visible through `get()` until a later
   rotation. This is not prefix-by-prefix state parity with the project arm.

The Liberty source text fetched from the pinned public blob is retained at
`originals/frequentDirections-liberty-691df9e.py`; the remote blob identity is
the authority because the local text snapshot normalizes insignificant trailing
whitespace. The execution script parses and compiles only the named classes
from both frozen sources, so their top-level CLI/data side effects are not
executed.

## Predeclared checks

On one fixed 8-by-5 stream with `k=1, ell=3`, every prefix checks:

- production sketch covariance against a separately implemented literal
  `ell`-row compress-before-insert reference;
- top-`k` projector equality and output orthonormality;
- finite-instance FD covariance underestimation and the directional bound
  `lambda_max(A^T A-B^T B) <= ||A-A_k||_F^2/(ell-k)`;
- recorded covariance distances to the author and Liberty interfaces.

Additional source-bound probes require the observed author live-array alias,
the Liberty pending-row visibility behavior, and immutability of a previously
returned production basis. Passing does not claim that all FD implementations
have parity. It establishes the narrower and useful conclusion that the current
production arm implements its declared `ell`-row specification on these
oracles, while the other frozen interfaces are detectably different.

## Execution boundary

One engineering attempt, no retries, one CPU core, 256 MiB admission
reservation, and 30 seconds. The pinned RSI native runner and single-task outer
harness must bind exact code/input hashes. No GPU, network, package install,
model service, native dataset, candidate method, or scientific gate is used.

Independent source/semantic review is required before execution, followed by a
separate receipt/output/hash review. Even acceptance leaves native baseline
performance, author diagnostic runs, sensitivity, G01, E04, Gate A and all
paper claims pending.
