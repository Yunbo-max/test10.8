# Landmark source acquisition and license record

Status: source/access record pending independent review and bounded mechanical
integrity execution.  It is not native scorer qualification or a scientific
baseline result.

## Immutable data source

- Author repository: `samsonzhou/consistent-LRA`
- Commit: `d607c4f6467216c470d1e3b93989d44d5fcdec97`
- Path: `landmark.mtx`
- Git blob: `4c63060bbefcb38e0c705cea1f883d2fb7121f2c`
- Observed byte size: 35,342,655 bytes
- SHA256:
  `29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b`

The actual bytes were acquired by a read-only partial Git checkout from the
frozen author commit:

```text
git clone --no-checkout --filter=blob:none https://github.com/samsonzhou/consistent-LRA.git author-consistent-LRA
git -C author-consistent-LRA checkout d607c4f6467216c470d1e3b93989d44d5fcdec97 -- landmark.mtx
```

The checkout's Git blob exactly equals the identity already recorded in
`SOURCES.md`.  The 34 MiB matrix is not duplicated into the destination branch;
future work can reproduce the exact checkout and verify both hashes.

## Embedded and official metadata

The MatrixMarket header identifies `Pereyra/landmark`, matrix ID 903, a 2003
least-squares problem from Victor Pereyra (Stanford), edited by Tim Davis.  It
declares 71,952 rows, 2,704 columns and 1,151,232 stored pattern entries.

The official SuiteSparse page reports the same shape, 1,146,848 numeric
nonzeros, 4,384 explicit zeros, structural rank 2,673 and numerical rank 2,671.
The Collection's license page states that the matrices are CC-BY 4.0 and asks
users to retain matrix metadata, cite the Collection, and disclose
modifications.  This project will keep the values and row order unchanged; a
first-5,000-row evaluation must be described as the published prefix rather
than redistributed as an unlabelled replacement matrix.

Official source pages inspected 2026-10-09:

- <https://sparse.tamu.edu/Pereyra/landmark>
- <https://sparse.tamu.edu/about>

At inspection time, the Collection front page said matrix-file downloads were
temporarily offline because of excessive download traffic.  This explains why
the official download route is presently unavailable; it does not affect the
identity of the exact author-repository blob acquired above.

## Proposed bounded integrity check

`inspect_landmark_source.py` streams the file without densifying it, verifies
Git/SHA identities, MatrixMarket bounds/order, stored-entry/nonzero/explicit-zero
counts, and records structural counts for the unmodified first 5,000 rows.  It
does not compute SVDs, losses, recourse or any scientific score.

Proposed envelope: one CPU core, 512 MiB RAM, 60-second attempt timeout, one
attempt and no automatic retry.  Execution remains pending independent source
review and an admitted harness plan.
