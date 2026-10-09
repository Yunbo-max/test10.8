# Author FD diagnostic implementation and qualification candidate

Status: generated, unexecuted code candidate.  Independent source/semantic
review is required before any harness plan or native run.

## Purpose and exact boundary

The released author script uses an `ell`-row array but, when it is full, appends
the incoming row and performs an SVD of an `ell+1`-row matrix.  It subtracts the
squared `(ell+1)`-st singular value and keeps `ell` weighted right-singular rows.
This differs from the project's already qualified strong `ell`-row
compress-before-insert FD and from Liberty's `2ell` buffer.

`AuthorAugmentedFDDiagnostic` in `native_baselines.py` reproduces only that
frozen update state.  It also deliberately preserves the source rule that a row
is “empty” whenever `np.any(row)` is false, including its ambiguity for an
actually inserted all-zero row.  It removes two evaluator defects rather than
copying them into the comparison:

1. the returned state is converted to a copied, row-orthonormal top-`k` basis;
2. recourse is computed by the shared squared projector metric, not by counting
   sketch rows outside an aliased previous row span.

The result is therefore an **author-update diagnostic under the common repaired
scorer**, not exact parity with the published script's reported recourse, not a
strong FD baseline, and not a new method.

## Proposed finite semantic oracles

`author_fd_semantic_oracles.py` parses and compiles only the
`FrequentDirections` class only after validating the raw file's Git blob against
the frozen author identity.  On the fixed 8-by-5 software-test stream already
used for FD qualification, with `k=1,ell=3`, every prefix will compare:

- the complete diagnostic sketch state to the frozen author state;
- sketch covariance and top-`k` projector, with the latter independently
  reconstructed by an eigendecomposition of the author sketch covariance;
- orthonormality and snapshot immutability of the emitted basis;
- shrink counts against an independent count of the frozen author's branch
  condition, plus the explicit zero-row source behavior.

A separate `k=2,ell=3` probe checks the varying-rank warmup convention and
independent projector reference at ranks one and two.  Snapshot immutability is
checked by retaining the first emitted basis while later valid prefixes execute;
the oracle never appends the final row twice.

These analytic fixtures are software oracles, not native scientific benchmark
data.  A later native author-diagnostic run remains blocked until this exact code
and plan are independently reviewed, dispatched through the pinned harness and
given a separate receipt/output review.  Even a pass cannot establish official
scorer parity, FD theorem validity, native performance, complete sensitivity,
G01/E04/Gate A or a paper claim.
