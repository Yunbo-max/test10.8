# Candidate repair: immutable low-dimensional matrix publication

Status: source candidate only; no retry is admitted by this document.

The first reviewed matrix process returned zero but produced unusable evidence.
Its three archives were truncated, four of 78 surviving staged members were
partial, and the staging directory was recreated after native and harness
completion. Independent review accepted only the failure record at commit
`17bde0dbd39d9409dc7a792e020e7d15c1b88e7f`.

This candidate changes evidence publication, not any method, dataset,
preprocessing, score, seed, cohort, arm or parameter:

1. Raw and summary files use the fixed exclusive directory
   `evidence/baselines/lowdim-matrix-raw-v2/` and are never deleted.
2. Every raw and summary file is fsynced after its producer closes it; the
   staging directory is fsynced after each cohort.
3. Each archive is written to an exclusive `.partial` path, fsynced, reopened,
   and every member hash is compared with the retained source before atomic
   no-replace hard-link publication and parent-directory fsync.
4. All 78 retained member hashes are checked again before manifest publication.
5. The manifest records hash, size, inode, mtime and ctime for each retained
   member and archive. It is itself fsynced and atomically renamed.
6. A repaired execution plan must declare the manifest, three archives and all
   78 retained files as outputs so the harness receipt binds every byte. These
   are point-in-time integrity checks; the independent collector must rehash
   the same paths because publication cannot prevent later external writes.

The original invalid attempt remains immutable. A repaired run, if admitted,
is the first repair of the evidence-integrity failure and a new executable
engineering attempt. It is still developmental existing-baseline qualification,
not a scientific experiment, official-scorer parity, G01/E04/Gate A evidence,
confirmation, discovery admission or a paper claim.
