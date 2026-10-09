# Independent Landmark reference-calibration source review

Reviewer: `/root/landmark_source_review`.
Reviewed immutable commit: `91ead65a9bb1c604844c3a1742287b9d976aea32`.
Verdict: **NEEDS_CORRECTION**. No code was executed and no files were written by
the reviewer.

Reviewed blobs and SHA256 identities:

- `calibrate_landmark_reference.py`: Git blob
  `1e3dbf74b9d0dd969d1a0b16900b42c27d6b6b01`, SHA256
  `61812867e637f0b2c6d1fea30ed1832ab61a30112bc74e8ad1201b5ceca99436`;
- `LANDMARK_REFERENCE_CALIBRATION_CANDIDATE.md`: Git blob
  `de0b4f2e3dd43b430732447440103d3c3dcdaf11`, SHA256
  `3f732ff443e8f639e49b1ab27a6bdf5c5778d4dc504b6fa004ea7c19a9d7ac78`.

The reviewer accepted the exact author source identity, MatrixMarket orientation,
first-5,000 source order, 80,000-entry and 259-column expectations, active-column
restriction, rank-25 Gram subset indices, direct-SVD tail definition, frozen
prefixes/repetitions and non-scientific scope flags. The active-column statement
is limited to residual geometry for supported/embedded right subspaces; it is not
an ambient-nullspace or recourse claim.

Execution was blocked pending three corrections:

1. retain the raw Gram residual and top-k eigenvalue sum, reject a materially
   negative residual under a frozen tolerance, and compare both raw and clipped
   residuals against direct SVD;
2. include the 259-by-259 Gram copy in the reference-path timing or expose copy
   and solver timings separately, and delimit internal timing/RSS semantics;
3. treat one-thread operation as a pre-import harness obligation with receipt and
   CPU-guard evidence, not as an observation made by the script.

This review neither challenges source identity nor grants execution admission,
native-scoring parity, G01, Gate A, mathematical proof or scientific evidence.

## Correction rereview

Rereviewer: `/root/landmark_source_review`.
Reviewed immutable commit: `c0c7239cc9a07374108e77d0a50e79bb34891f9a`;
tree: `fcc0e8320ddd64efe19525b97998e1ab7b7b3e34`.
Verdict: **ACCEPT** for corrected static source/semantics only. No code was
executed and no files were written by the reviewer.

Exact accepted identities:

- runner blob `5766d2d64a500b6a67ae2a6b48eb911dc89b135c`, SHA256
  `460c09a4a8016744a1531212276f1fcd04b3b5a38702b2cefa6ef446bf16f7be`;
- candidate-document blob `86eceab7e101ad8682a7baeed5d10b75b885d441`,
  SHA256 `ec7ae383d90818ac0875c8c251845d64b56a962e20598e953a3799c235c3a6f5`;
- preserved initial-review blob `219fc1946417754963f46c124959aefb4a9ed4d6`,
  SHA256 `ef5b87c651a3408f6458c5bb736d19a5f264934d19e767c5dd46dcba85bfdfa0`.

The rereviewer verified the raw/clipped residual and cancellation controls,
copy-plus-solver timing, explicit timing/RSS scope, and pre-import harness thread
obligation. No new defect was found in the unchanged source/parser/reference
path. Acceptance permits only a later separately reviewed bounded harness plan;
it does not admit execution, validate numerical output or establish official
scorer parity, G01, Gate A or scientific evidence.
