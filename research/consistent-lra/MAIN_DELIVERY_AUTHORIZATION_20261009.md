# Main delivery authorization and exact subtree migration

Owner instruction at 12:29 Europe/London: “以后直接更新到main就行”.

The current authorization changes only delivery. The main project was absent;
the complete legacy project subtree was inserted with its existing Git tree SHA.
No files outside that subtree were changed. Old receipts retain original branch
and runtime identities; prior history is not re-certified. The legacy branch
remains untouched. Future recovery starts at live main.

```json
{
  "source_main_head": "9ae52f70f629487b937e49e79d052b5e26299b76",
  "source_legacy_head": "b62528927acd3a8771fb5269fc1fc945b717eed1",
  "source_project_subtree": "6c2ba1bf546909ff02b76693f8f49352aac3fa85",
  "migration_commit": "2584996b627adb9a2096acc86d5ccee0f5d08f5b",
  "migration_root_tree": "60dd3affdf8aba6920d87b962e99f4ce24337c1c",
  "project_subtree_readback": "identical",
  "main_other_paths_readback": "README/docs/root-checkpoint all original blob/tree SHAs identical",
  "delivery_branch": "main",
  "historical_branch": "consistent-lra-rsi",
  "scope": "research/consistent-lra/",
  "observed_at": "2026-10-09T12:22:59.462457+00:00",
  "scientific_gate_advanced": false
}
```

Existing unlaunched integer reservation is carried forward, not executed or
released by migration. Original source rejection and amended unexecuted source
are retained. Budget baseline: 136 assignments, 21 attempts, 2 controller
rounds, 0 discovery, 0 scientific experiments, CPU lower bound292.775693082s.
Host remeasured: cpu.max800000/100000, memory.max8589934592, no matching
scientific/formal/harness processes observed before new work.
