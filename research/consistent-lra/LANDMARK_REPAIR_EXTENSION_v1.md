# Landmark scorer accelerator extension v1

Status: generated source candidate, not executed, not scientific admission.
Existing baseline M audit; no new method and no change to REPAIR_CONTRACT_v1.
Bound to accepted design SHA256 c6b5d2525a87d278f3ad90b2b69045478e4690c66c10459ab16ea574bee11083.

The frozen 13 existing arms, actual first5000 native rows, k25, 259 active map,
rank min(25,t), warmup, copy/tie rules, direct/Gram identities, 35 oracle prefixes
and separate dimensionless recourse tolerances are exactly those of
LANDMARK_BASELINE_MATRIX_DESIGN_CANDIDATE.md. Original sources remain unchanged.
The active map is compared byte-bound to the accepted reference calibration.

landmark_stage_a.py implements two explicitly distinct calls. The initial cost
calibration processes only native prefixes1..150 for all13 arms, with identity
oracles at1..25/50/100/150. Qualification processes transitions1..5000, with
oracles only at the full frozen35 prefixes. Each refresh arm owns its Gram,
energy, copy and eigensolver. FD receives no shared reference state. Current
and immediately previous output bases are copied and retained in each oracle.
No all-prefix loss/recourse performance matrix or ratio verdict is produced.

OPT oracle uses independent fresh direct SVD tail; loss oracle explicitly forms
A-(AQ^T)Q; recourse oracle explicitly forms both projectors and their difference.
Gram loss/OPT tolerances are1e-10 max(1,E). Recourse tolerance is independently
1e-10 max(1,r+rprev). Materially negative values, nonfinite output, incorrect
rank/orthogonality, oracle disagreement or raw-output identity failure abort.
Prefix1 initialization is separately labelled and primary increment is0.

Frozen outputs: one JSON summary and two deterministic gzip JSONL files, for
oracle/current+previous bases and every processed prefix/arm update timing.
Closed gzip outputs are fsynced and independently decompressed/hashed before
hard-link no-replace publication; summary is published last. Finals are rehashed
before exit and post-exit collection. Failures/partials are retained, never
silently renamed successes. Row denominators are28*13/150*13 for calibration,
35*13/5000*13 for qualification. Extrapolation of calibration cost is a planning
bound, not a full-matrix runtime claim. Thread cap1 before imports.

This source does not implement Stage B or qualify the near-zero ratio fallback.
Stage B remains separately generated/reviewed after accepted full Stage A and
cost evidence; its direct fallbacks must replace all reported/derived metrics
under the existing accepted design. No official scorer identity, callback,
protocol, Gate0/IPCG/GateA or paper result is supplied by this extension.

Review/dispatch sequence: independent source+semantic review of actual bytes;
bounded calibration plan review and one120-second native attempt within a
180-second harness reservation; independent cost/output evidence review; a new
full Stage-A plan bounded using actual calibration and remaining budget;
independent plan review, execution and evidence review. No automatic retries.
