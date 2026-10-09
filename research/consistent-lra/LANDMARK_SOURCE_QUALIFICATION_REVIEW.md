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

## Correction rereview verdict: accepted

- Reviewer: `/root/landmark_source_review`
- Corrected candidate: `2dc532076a9a09541c975fd462a496edf6dd89e1`
- Assignment/binding: `4478b2865ac8add57df28a06fdeb19ed5846d61f`
- Verdict: `accepted`
- Execution performed by reviewer: none

The reviewer independently recomputed the root and streaming ZIP-copy byte
count, line count, Git blob and SHA256, with `cmp` exit 0.  It also checked both
copies of the frozen author script for `n = 5000` and
`dataset = all_data[:n]`, and confirmed that the inspector enforces byte count
before both hashes while remaining streaming and free of SVD, loss, recourse
or scientific scoring.

Exact corrected artifact identities reviewed:

| Artifact | Git blob | SHA256 |
|---|---|---|
| `LANDMARK_SOURCE_ACQUISITION_20261009.md` | `3a4f30702ba14065933e0a1f3164f78bdbb194f8` | `283a2484d05f48eabc31411d8fe598a22d9f530d76406c365fb8160beef7028d` |
| `inspect_landmark_source.py` | `4e20da093408bea7a522e42af832c185556c3a5d` | `fbace7373933a792f9796e1d735047aaa149a25a9236cbe248804c9d8d2eece4` |
| review history before this acceptance | `d65bbf6df2cbcd4a4abe4112dd35a00471e188a6` | `a91e465df5407a7a38499aa946b6780b24c3ed0382db809425b3eacf59cfc562` |
| rereview assignment | `39f7cad747b4959185f28c8e9e0360c504d4adcb` | `902b9dec2c905fc774607da95294e61ba21affaefe7afa9640bd588fa2a2d7ba` |

This acceptance admits only the bounded mechanical integrity run.  It does not
qualify the missing official scorer or advance any scientific gate.
