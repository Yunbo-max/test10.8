# Independent source review: prospective random baseline matrix

Reviewer: `/root/baseline_audit`  
Initially reviewed commit: `0d519c15359c4094f933faf759537dcdd5903937`  
Initially reviewed tree: `767084decec2e6d8e75e5c5c676bca932a5bde2a`

Initial verdict: **needs correction, documentation only**.

The reviewer accepted the 13-arm enumeration, prospective seeded unscaled
matrix identity, reuse of the reviewed scorer/arms and terminal no-replace
publication checks.  The sole correction is that
`RANDOM_BASELINE_MATRIX_SOURCE_CANDIDATE.md` originally claimed every output
contains `original_figure_replication: false`.  In the implementation, that
flag is present in each summary's native identity and in the matrix manifest;
per-prefix raw JSONL records instead carry seeded `sample_id` values and are
bound by the manifest.

The source candidate now states that exact arrangement.  No scorer, arm,
generator, output schema or execution state changed.  This correction does
not qualify numerical evidence and does not change the prospective,
non-reproduction boundary.  Independent rereview is pending.

Final rereview verdict: **accepted source/design only** at exact remote commit
`4b8c428c3fb9e3b6ea2fb63f0bb162f5d77f55ac` (tree
`937df0eeadd6dc1a16c8aa8b28917bf366b5dbff`).  The corrected source-candidate
SHA-256 is
`3b94a807c798b273a26002ec6425384db70bb360b840fbe0d58165e19bc304f5`;
the runner SHA-256 remains
`27f2a10557ec0c63f92756f0e566912a5c5ed966ff57e3a3662f6987d7f6d67a`.
The reviewer confirmed that this was the sole change and that runner,
publication helper, native implementation, scorer and original-source bytes
are unchanged.  Execution and empirical admission remain separate.
