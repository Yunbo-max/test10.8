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
Correction rereview verdict: **accepted** at exact commit
`608bce8dafc9bbe7ce7c14082191fab27ac6e372`.

Corrected identities independently matched:

- design SHA256
  `ff5fc67804d5aa705b2c4ae5b2cefebea0bf2391502b13a663ad0d29b1cd0ea2`;
- runner SHA256
  `4d06d29f61f11172a1811e3daea3f0bd74d8b7a10a7661b5e2afd80b3428deab`;
- preserved initial-review-record SHA256
  `b4c78f7eb041a2ca81edc775967e87bdb157ab2f6700ca5b1f4ef69470ec0eec`;
- unchanged `native_baselines.py` / `baseline_qualify.py` SHA256
  `81c3309e659d1d9fdb69040b9becc6009bbe29b84a36aae8bac89ea6737e2c7c` /
  `d5566e2177064d0ddd9f940323ca7d10dfb0d9fef14d93f8ba6d16bde54dd934`.

This closes source/design review only.  Exact execution-plan admission, raw
execution evidence, E04/scientific verdict and all claims remain separate.
