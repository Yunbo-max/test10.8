# Independent evidence review: low-dimensional baseline matrix failure

Reviewer: `/root/rice_skin_evidence_review`  
Pinned commit: `17bde0dbd39d9409dc7a792e020e7d15c1b88e7f`  
Pinned tree: `875ca1384463447a14cd0246d10a32d222d951c0`  
Verdict: **accepted as a failure record; the execution remains invalid/confounded**.

The reviewer ran no scientific code and made no project edits. It independently
recomputed the frozen source, plan, receipt, guard, log, manifest and harness
identities. The failure record itself has SHA-256
`139772a7723b0cfc12c0e735d91facc00a8fa9d844cf9d42ac3fd4a540f06778`.

All three surviving archives fail both gzip and tar integrity checks. Their
current hashes disagree with the producer manifest; the Skin-k2 archive also
changed after the harness receipt. Rehashing all 78 surviving staged members
found zero missing members and exactly the four mismatches listed in the
failure record. The surviving manifest is byte-identical to the committed
manifest.

Time evidence is also consistent with post-execution recreation or mutation:
native completion was `2026-10-09T04:29:05.602294Z`, task completion was
`04:29:05.616978Z`, the harness report was written at `04:29:06.169673Z`, and
the surviving staging directory has birth time `04:29:07.113300679Z`. This
supports a post-exit boundary failure but does not identify an actor or root
cause.

Accounting is accepted: executable/preparation attempts increased from 9 to
10, scientific attempts remain 0, process CPU is
`2.084459 + 23.294645 = 25.379104` seconds, maximum RSS is 157864 KiB, and the
reservation is released. The failure is evidence-integrity engineering history,
not a scientific refutation.

No score, ranking, parameter preference, plot, performance claim, Gate A,
G01/E04 decision, confirmation claim, discovery admission or paper claim may
use this attempt. A retry requires a newly frozen plan and is the first repair
of this identical failure. The reviewer recommends producer-side close/fsync
and full member verification, atomic publication, no deletion of raw staging,
and before/after collection inode/time/size/hash observations.
