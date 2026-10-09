# Independent source review: final low-dimensional matrix publication repair

Reviewer: `/root/baseline_audit`  
Pinned commit: `a328a4d836c498bd2c0eb036e48ac9e622107254`  
Pinned tree: `1cf02b72af660d792e44a4c66d2d6ee0b036ad11`  
Verdict: **accepted, source/design only**.

The reviewer verified the exact runner SHA-256
`4934100cd9e7b4d91aee361d1c8e09b7f3fb790e06784c137df7a3a012bfab20`
and repair-contract SHA-256
`5c69a676b5326615eef56db59acc41b571210bf27806fff9a4db89823078b703`.

All progressive raw and summary writes use unpublished `.partial-*` names.
After the native producer returns, the wrapper fsyncs and hashes the working
files, publishes each final with a no-replace hard link, unlinks the partial,
and immediately rehashes the final. The explicit `published_members` inventory
contains only the 78 final raw/summary members, excluding any replayed partial
names. Archive verification and no-replace archive/manifest publication remain
in force, followed by reconciliation of three archives plus 78 members.

The reviewer checked the native summary naming rule: replacing the working
`.jsonl` suffix with `.summary.json` produces exactly the path expected by the
wrapper. Methods, scorer, loaders, cohorts, 39 arms, parameters, seed and
numerical metrics are unchanged. Repair ordinal 2 is consistent with the
accepted failure ledger and is the final repair allowed for this identical
failure.

A plan may declare 82 successful outputs only in a fresh attempt parent;
existing archive names must be rejected. Post-exit collection must rehash all
82 outputs. This review admits source design only, not execution, empirical
results, official scorer parity or a scientific claim.
