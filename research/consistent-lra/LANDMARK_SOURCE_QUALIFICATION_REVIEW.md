# Landmark source qualification review

This records the independent review history.  It is neither a native scorer
qualification nor a scientific result.

## Initial independent verdict: needs correction

- Reviewer assignment: `/root/landmark_source_review`
- Candidate commit: `22d6ae44b52489e643495d2b02b550032777b1d5`
- Assignment commit: `8bb842c7f92fd7ae92fe06d753186a5246beee32`
- Verdict: `needs_correction`

The reviewer independently resolved the author Git blob and found that the
recorded 35,342,655-byte observation was wrong: blob
`4c63060bbefcb38e0c705cea1f883d2fb7121f2c` is 34,964,305 bytes.  It also
recommended replacing “published prefix” with “author-script-selected prefix.”
The initial verdict is retained rather than overwritten.

The reviewer otherwise confirmed the frozen Git/SHA identities, official
SuiteSparse shape/count metadata, CC-BY-4.0 attribution summary, streaming
implementation, absence of densification/SVD/scoring, and the safety of the
one-core/512-MiB/60-second/one-attempt envelope.

## Writer correction evidence

At the frozen author commit, the root `landmark.mtx` and the copy embedded in
`consistent-lra.zip` were checked independently.  Both have:

- byte count: 34,964,305;
- line count: 1,151,246;
- Git blob: `4c63060bbefcb38e0c705cea1f883d2fb7121f2c`;
- SHA256: `29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b`;
- byte comparison: identical (`cmp` exit 0).

The acquisition record and inspector were corrected.  Acceptance remains
pending a bound independent rereview of the immutable corrected candidate.
