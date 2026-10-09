# Preserve legacy writer progress during main migration

The initial live legacy pin was b62528927acd3a8771fb5269fc1fc945b717eed1.
It was migrated byte-identically into main2584996b627adb9a2096acc86d5ccee0f5d08f5b.
The original legacy worker then advanced its own already-active integer task.
This main integration invocation detected the advance before planning or
dispatching any additional workload. It launched no generator, native scorer,
experiment or second harness. Legacy attempts and receipts are preserved.

The source review and scorer audit in this invocation are separate actual agent
tasks /root/integer_source_rereview and /root/scorer_admission_audit. Their initial
numbers138/139 were main-local provisional ordinals before the legacy worker's
new assignments were observable; the merged budget counts their unique task
names after all retained legacy assignments. Historical ordinal text is retained
and explicitly reconciled here rather than silently rewritten.

The old writer is not addressable by this invocation's collaboration tree.
Therefore this integration writer does not claim to have cancelled or hot-steered
it. The saved current authorization directs future recovery and publication to
main. Additional legacy evidence must be integrated with expected-main-parent
updates until that already-active worker's final packet is observed; no stale
subtree overwrite, new goal, duplicate job or budget reset is permitted.

Migration and integration are delivery operations, not controller research rounds
or scientific iterations. All independent reviews and the new analytic
exact/approximate clarification consume the same remaining assignment and wall
budget. Evidence-source SHA and exact latest budget will be recorded in the
current controls at each integration commit.
