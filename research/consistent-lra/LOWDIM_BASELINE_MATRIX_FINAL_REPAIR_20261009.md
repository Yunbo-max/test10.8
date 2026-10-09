# Candidate second repair: isolate all progressive writes

Status: source candidate only; no execution is admitted by this document.

Repair 01 safely rejected its output before manifest publication. Four raw
files written progressively to their final workspace names were later observed
as truncated. In contrast, all three archives written progressively only to a
`.partial` name and then published by a no-replace hard link remained complete
and readable; only their unlinked partial names were recreated with truncated
bytes. This is a controlled within-attempt contrast, not a scientific result.

The second and final allowed repair applies the already accepted archive
publication pattern to every raw and summary file:

1. `native_baselines` writes each raw and summary progressively only under an
   unpublishable `.partial-*` name inside `lowdim-matrix-raw-v3/`.
2. After close and fsync, the producer verifies raw/summary hashes, creates the
   final name with atomic no-replace hard linking, and unlinks the partial.
3. It immediately verifies the final inode bytes against the pre-publication
   hashes. Later workspace replay to the obsolete partial name creates a
   different inode and cannot modify the published final.
4. Archive and manifest publication retain the same no-replace pattern.
5. Final inventory is explicit rather than directory-based, so recreated
   partial failure artifacts cannot enter the successful 81-file inventory.
6. A new plan must bind the v3 manifest, three archives and 78 v3 final members;
   collector and independent reviewer must rehash all 82 paths after exit.

No method, native scorer, loader, dataset, preprocessing, cohort, arm,
parameter, seed or metric changes. If this second repair fails, the identical
workspace-integrity failure has exhausted its two-repair cap and this execution
route must stop. Even a successful repair remains engineering/developmental
baseline qualification, not official scorer parity, G01/E04/Gate A,
confirmation, discovery admission or paper evidence.
