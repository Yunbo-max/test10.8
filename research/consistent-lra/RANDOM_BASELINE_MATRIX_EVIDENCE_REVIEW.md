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
Independent repair rereview is pending.

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
