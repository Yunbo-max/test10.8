# Independent execution-plan review: matrix publication repair

Reviewer: `/root/rice_skin_plan_review`

Pinned commit: `1e6d644c44eb59c49415dc1a89acce4822a1937f`

Pinned tree: `8ae882aefffb6771ef7eca60fcfde5eb3522ba71`

Verdict: **accepted for one bounded engineering-developmental repair attempt**.

The reviewer executed no project code and made no edits. It independently
recomputed native-plan SHA-256
`0d00c459466254db025c019d7ebf3ca9e01ad67a76b2a6d3b27ac9410979cbeb`
and digest
`10f6cacb9074dbcb3b5f8f539371aef148cb09b91eb606334d35e7b14f7969bf`,
and harness-plan SHA-256
`9f494be5d29827561331f3901bc7a07bdf399fe053100d818784ca0dda65b3cc`
and digest
`78ce83b3889722561525987f4248782f0325061cf7692c3eb93adb17a1d276de`.

The plan preserves the same 39 arms, cohort identities, inputs, preprocessing,
seed and parameters as the invalid first run. It declares 82 unique successful
outputs: one v2 manifest, three archives, 39 JSONL files and 39 summaries. The
new run/trial/batch/task identifiers do not collide with existing directories.
Repair provenance binds the original failed attempt, exact failure identifier
and `repair_ordinal=1`.

Admission is one process, one CPU, 512 MiB reservation, one attempt, zero
retry, 180 seconds native and 210 seconds outer. Five numerical thread
variables equal one before Python import; no GPU, network or installation is
allowed. The memory figure is a reservation, not `RLIMIT`.

Acceptance is not execution acceptance, scorer parity or scientific evidence.
The run remains engineering/developmental with null protocol and zero
scientific attempts. A terminal process still requires immediate collector
rehashing of all 82 outputs and independent receipt/output review; later
external writes remain possible.
