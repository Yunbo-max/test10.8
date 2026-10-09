# Independent random-family identity review

Initial candidate `19a46f250bc196c3892e1a01edb6c8a5d7b7440d`, assignment
binding `812e583c91be30143573afe5df6bd6d6be155d6b`, reviewer
`/root/author_archive_review`.

Initial verdict: **needs_correction**. No project code was executed and no file
was written by the reviewer.

The reviewer confirmed the core source conclusion: the 3,000 by 4 script uses
module-global inclusive `random.randint(0,100)` in row-major order, has no seed,
state or saved matrix, and applies no normalization; Appendix G.1 says the
matrix was normalized by column without defining the operation. The different
3,000 by 100 randomized-SVD script cannot substitute. Exact figure provenance
is therefore absent, without implying a false qualitative paper result.

Four corrections were required:

1. replace two incorrect copied SHA256 strings with hashes of the frozen files;
2. record paper `c=2.5` versus released-script `c=2`;
3. record the script's empty-through-2,999 prefix loop and `xlim(1,300)`;
4. freeze runtime/Python identity and the resulting matrix hash for prospective
   seeded family instances.

The initial `needs_correction` verdict is retained. A later rereview must bind
the corrected artifact and does not authorize numerical execution or a paper
claim.

## Correction rereview

Corrected candidate `6f104ad753ffe0fc441265405072b39bc4fe5590`, binding
`39947aebe92eb798a653e4219e1ae659bc81b64f`. The same independent reviewer
returned **accepted** without execution or writes. It verified corrected
artifact blob `7366bbd70de269280a4dfe1a22bbee0c0c4d3ae3`, SHA256
`ccff5d82ccdc196b0c186e6eb08f0182f01145b641f811c31434b3efc59aa077`,
both frozen source hashes, both paper/code discrepancies and the prospective
runtime/matrix-hash rule. All downstream scientific blockers remain open.
