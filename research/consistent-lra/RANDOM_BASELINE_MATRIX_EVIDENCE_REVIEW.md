# Independent evidence review: prospective random baseline matrix

Reviewer: `/root/rice_skin_evidence_review`  
Initially reviewed commit: `373bec07ddb5f48d9861a9884711b220e5733148`  
Initially reviewed tree: `8ebf3215435065617cbcad145f696b55d857e5b9`

Initial verdict: **needs correction; invalid durable archive binding**.

The reviewer fetched the committed archive path rather than trusting the
path-level readback result.  Its Git blob was
`6ecf98cbbb73edcef325f6a013556b69a8542edb`, size 786444 bytes, with SHA-256
`178edc6f1111e531cbedc020825bf1acf880ec06ce797ae6e4d56745db323184`;
`gzip -t` failed.  It therefore was not the 5096362-byte archive declared by
the receipt and manifest.  Commit `373bec07...` is permanently retained as an
invalid durable-publication record and cannot support evidence acceptance.

The surviving local terminal artifact at local evidence commit `f004a1e...`
has size 5096362 bytes, Git blob
`8f0595f7fa9a85b0eb6fb7616d404bfb1409fe6d`, and SHA-256
`af9b40bfb131570d1d5868006d0f4193550ba087f6679bb250a65554bab1bb8e`;
it passes `gzip -t`.  All local receipt/manifest rehash checks remain unchanged.
The failure arose while transporting a large base64 string through a truncated
tool-output channel, not in the admitted CPU execution.

Repair 1 for this publication failure reads the local archive in chunks whose
full sizes are divisible by three, concatenates the unpadded base64 segments,
and asks GitHub to create one blob.  Acceptance requires the returned Git blob
to equal `8f0595f7...`, followed by an independent fresh remote download,
SHA-256, gzip test, 26-member inventory and member-hash verification.  No
numerical source, plan, execution, receipt, manifest or summary is changed.
Independent repair rereview is complete at immutable remote commit
`99de82eefb87be6f7e9da66f6b924fb35b801349`, tree
`1699dcadf286c7b39051b3ab037be8b10dac0db0`.

The reviewer completed a bounded numerical/integrity audit against the
surviving archive while awaiting durable repair.  Every non-archive byte at
remote `373bec07...` matches the local evidence commit.  The correct archive
has 26 unique regular members; all member hashes, 28 output references and 27
publication observations agree.  Independent regeneration recovered matrix
SHA-256 `13256cf8...`.  Recomputing 39,000 rows, 117 summary fields, 104
direct/SVD prefix checks and 9,000 FD-projector prefixes produced zero errors.
Maximum numerical discrepancies were `4.66e-8` for trace loss on the
large-energy scale, `1.77e-8` for eigenvalue OPT, zero for direct/SVD loss,
`5.33e-15` for the projector recourse identity and zero for FD projector
output.  Plans, receipt, attempt, guard, harness and ledger totals also pass.
These checks narrow the failure to durable archive publication, but do not
accept the evidence until a fresh download of the replacement blob passes.

## Repair rereview verdict

Final verdict: **ACCEPTED_DEVELOPMENTAL_PROSPECTIVE_FAMILY_EVIDENCE**.

The independent reviewer freshly fetched the receipt-bound archive at the
exact repaired commit.  `git rev-parse` returned blob
`8f0595f7fa9a85b0eb6fb7616d404bfb1409fe6d`; `git cat-file -s` returned
5096362 bytes; streaming the blob through `sha256sum` returned
`af9b40bfb131570d1d5868006d0f4193550ba087f6679bb250a65554bab1bb8e`;
and `gzip -t` exited zero.  A fresh tar audit found 26 unique regular members,
with no duplicate, non-regular, missing, unexpected or hash-mismatched member
against manifest SHA-256
`5a30b214e230da04364f8cff6e6aef24f7e0b832c54d211fc27f5f550da4609f`.
The receipt remains SHA-256
`21f9577fe9fa837c47a5acb8cae823e4ae46e2d80f53bd2109bd9f8e3f7c8608`.

The diff from invalid publication commit `373bec07...` contains exactly five
intended paths: the corrected archive and the evidence-review, execution,
budget and checkpoint records.  All other source, plan, receipt, manifest,
log, harness and numerical evidence bytes are unchanged.  The review
assignment accidentally named a nonexistent top-level copy; the reviewer
resolved that task-text typo by using the sole path actually bound by the
receipt and manifest.  No second copy was ever declared or required.

This verdict binds the prior full recomputation to durable remote bytes.  Its
scope is only one fixed-seed, unscaled prospective generator-family
development instance.  It is not Figure 3 reproduction, authentic scorer or
normalization parity, confirmation, independent-seed uncertainty, Landmark or
four-family G01, Gate A, theorem/generalization evidence, or a paper claim.
