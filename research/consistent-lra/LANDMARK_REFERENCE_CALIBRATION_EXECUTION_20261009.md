# Landmark exact-reference calibration execution

Status: completed engineering workload; independent evidence review pending.

The exact reviewed harness plan digest
`570f6c67bd609cf2adc75144948a3baa897c91d120ca227d2fba9737c6aecf06`
ran once with no retry. The cgroup immediately before dispatch exposed
`cpu.max = 800000 100000`, `memory.max = 8589934592`, effective CPUs `0-8`
and nine visible processors. Admission reserved one CPU, 1024 MiB and zero
GPUs; the memory reservation was not an OS RLIMIT.

## Binding and terminal status

- run: `landmark-reference-calibration-01`;
- attempt: `landmark-reference-cost-a1-177b60cdd7444745b59898cc4731e74a`;
- exact source SHA256:
  `29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b`;
- exact runner SHA256:
  `460c09a4a8016744a1531212276f1fcd04b3b5a38702b2cefa6ef446bf16f7be`;
- one attempt, retry index zero, exit code zero and empty stderr;
- native receipt SHA256:
  `2cf21ec972891eb1477973a981632a638593815d6d7412baf72bedcfcb050d29`;
- attempt SHA256:
  `944fecb6738a19165d979573dcbe52149b4a1cb820257b57d46f37c1e3b0de4f`;
- process-guard SHA256:
  `5ead198698d748b291f24285bce6867de79a13645d15ccf51d80bae17678aefa`;
- output SHA256:
  `25887ba1e2a81776a87a88ab0f78cfc0134a408fa3642686d039d04ba5f9df90`;
- harness report SHA256:
  `6e34216d963813ec172a080aa74d19151524b7a947b1287c8140d5632363629d`.

The harness batch completed in 3.033931 seconds. The native receipt accounts
2.162537 seconds, while the guarded attempt accounts 1.819965 seconds. The
script's post-import/pre-serialization measurement is 1.422161 wall seconds,
1.421907 process CPU seconds and 80,104 KiB process-high-water RSS. Load time is
0.910241 seconds and Gram-update time is 0.295232 seconds. These scopes differ
by design; the harness receipt is authoritative for pipeline dispatch.

## Raw numerical observations

The output contains the 11 frozen prefixes and three Gram references per prefix.
All three direct-SVD checks (prefixes 150, 1000 and 5000) passed. The largest
raw-Gram versus SVD absolute difference is `2.2737367544323206e-13`. Median
copy-plus-eigensolver reference times range from 0.001568 to 0.004070 seconds;
their sum over the 11 selected prefixes is 0.027688 seconds. Prefix 25 has raw
residual `-1.7763568394002505e-15`, inside its frozen cancellation tolerance,
and is therefore the sole clipped negative residual. Prefix 5000 has reported
rank-25 residual `593.627871987748`; its direct-SVD value is
`593.6278719877478`.

The raw output is retained at the exact attempt path referenced by the receipt.
Its post-exit SHA256 was re-read unchanged before this record was written.

## Scope

The output itself records `full_5000_prefix_queue_admitted=false`,
`baseline_comparison_performed=false`, `scientific_experiment=false` and
`gate_advanced=false`. This run measures selected exact-reference costs and
numerical agreement only. It does not establish official scorer parity, execute
any baseline comparison, reproduce a paper figure, qualify near-zero ratio
denominators, pass G01/Gate A, or support a paper claim. Independent evidence
review is required before even this engineering interpretation is accepted.
