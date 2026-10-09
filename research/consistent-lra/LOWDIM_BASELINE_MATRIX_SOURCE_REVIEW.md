# Independent source/design review: low-dimensional baseline matrix

Reviewer: `/root/baseline_audit`.  The reviewer executed no project code and
made no edits, commits, or publications.

## Initial review

Pinned candidate commit:
`364e98ccc98ee270eb53cc1b1262f6a8f4067a58`.  Verdict:
**needs correction**.  The exact 39-arm enumeration, shared scorer/stream/rank
semantics, strong-FD clipping/deduplication, author-FD diagnostic label and
claim boundaries were accepted.

Reviewed identities:

- `LOWDIM_BASELINE_MATRIX_20261009.md` SHA256
  `5a41c2df738e722d98841fe9a14b0c9bc3c260b00a405717131057ce976ae8be`;
- `run_lowdim_baseline_matrix.py` SHA256
  `e60ae8450aaaa3c87bfbbb56dcb4abb3857c0264440703a0d82da1cde6f30dd6`.

Required corrections:

1. Preflight manifest/archive paths as distinct and absent, and open outputs
   exclusively; otherwise a manifest path equal to an archive could overwrite
   it.
2. Preserve the uniquely owned work directory and partial raw results on every
   failure.  Delete it only after successful lossless archives and manifest.
3. Record `baseline_qualify.py`, runtime/argv/thread provenance, and compare the
   source/transformed/label identity across all arms in each cohort.

The 180-second/512-MiB estimate was judged plausible from the retained Rice
calibration, not guaranteed.  The candidate now implements the three repairs.
Correction rereview verdict: **pending**.
