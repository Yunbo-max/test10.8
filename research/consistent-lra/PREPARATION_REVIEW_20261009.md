# Completed source-integrity preparation and scoped evidence review

This coherent batch is mechanical preparation only. It imports/executes no numerical baseline. Scientific E04, numerical qualification, G01, native scorer parity and scientific gates remain pending.

Source/code state was committed at c80b84cf251ef1b9379cb3797373159ad23dc3f5; prelaunch plans and reservation were persisted at 73246d5058e40660bab4c74170c436ae20418243. The read-only vendored harness is from RSI source 1de12dfed5b84957b29ac5b3a2f04904bf3742bc, as recorded by vendor/rsi/SOURCE_MANIFEST.json.

Actual command:

```sh
python3 -B /workspace/scratch/bb9f262965cf/research/consistent-lra/vendor/rsi/scripts/run_harness.py /workspace/scratch/bb9f262965cf/research/consistent-lra/plans/harness-source-integrity.json --root /workspace/scratch/bb9f262965cf/research/consistent-lra --execute --approved-plan-digest d962a49eef524eb2c27226b7d094c98d41d77bd45406a3929f37975bf1374838
```

The native mechanical plan digest is bc8b69698233feacd2e1b8a9dcc07b1a9ab62efe35ad73ff690557cb2a1649c8. One attempt completed with exit 0 at 2026-10-09T00:08:12Z; no retry. Workload wall 0.165110690 s, process CPU 0.190072 s, peak RSS 99,788 KiB. Outer harness wall 1.010280157 s and attempt wall 0.265120199 s are different scopes, not extra CPU time. The 1-core/512-MiB/60-second reservation is released.

`evidence/source-integrity-01.json` and the workspace output both have SHA256 b5d87432c73b0500cd0e0909aed9e6b50be130c57d39ffd7e6cf1ae9d9bbf0b9. Receipt SHA256 abe68964844ec38e356b6c1573f615ea6319756185361d4a0eedf49dbbb0d378. It contains the exact commands, input/code hashes, actual timestamps, exit status, output/log/guard refs and source revisions. Raw runner stdout/stderr, process guard and actual staged workspace are retained under runs/. Absolute paths/PIDs in these historical receipts must not be rewritten or treated as active on a later host.

Independent reviewer `/root/execution_capability` examined the actual plans before launch and the completed run afterward. It checked 13 referenced artifacts and five staged input/code bindings, the command/cwd, process guard and cleanup. No matching worker/process group or visible lock holder remained. Its verdict is scoped to this preparation batch and does not admit science.

Verified native bytes and released order: Rice 3,810 rows/7 features (first 3,000: Cammeo 1,630, Osmancik 1,370); Skin 245,057 rows/3 features (first 3,000 all label 1). AST parsing covered baseline_qualify.py hash d5566e2177064d0ddd9f940323ca7d10dfb0d9fef14d93f8ba6d16bde54dd934 and historical native_baselines.py hash ce279d41df2aa4ef76464acac720e94318e2b858b3f8ad2c94a59b51d9eba3e5. The later repaired baseline has a different hash and this run is not evidence of its numerical behavior or even a new AST check.

Blockers retained: missing authentic upstream predictions-to-JSON scorer interface under the pinned runtime; Landmark 34,964,305-byte blob exceeds the connector's 8,388,608-byte response bound. Neither is a scientific falsification. No per-prefix loss/OPT/recourse metrics exist yet; do not fabricate them or present the preparation's completed status as a scientific verdict.
