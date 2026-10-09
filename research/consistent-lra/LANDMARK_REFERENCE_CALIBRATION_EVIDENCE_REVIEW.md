# Independent Landmark reference-calibration evidence review

Reviewer: `/root/landmark_evidence_review`.
Reviewed immutable commit: `d29281f1ec6f757455c03d95b2aaf645397b53a6`;
tree: `7cfac23222e369744cda86a799a51d82b69e519c`.
Verdict: **ACCEPT** for engineering exact-reference cost and numerical-agreement
evidence only. The reviewer edited no file and did not rerun the workload.

## Binding and terminal execution

The reviewer independently recomputed native digest
`568c5193935ff57d686cde51b8fe46e9a6e7a0a1776e43b89d928ac321635f57`
and harness digest
`570f6c67bd609cf2adc75144948a3baa897c91d120ca227d2fba9737c6aecf06`.
Published and frozen plans agree. Plan, receipt, attempt and process guard carry
the same argv, including all five pre-import numerical thread variables set to
one. The script itself correctly reports the runtime thread count as unobserved.

There is one attempt, retry index zero, exit code zero and empty stderr. Exact
SHA256 identities are:

- receipt: `2cf21ec972891eb1477973a981632a638593815d6d7412baf72bedcfcb050d29`;
- attempt: `944fecb6738a19165d979573dcbe52149b4a1cb820257b57d46f37c1e3b0de4f`;
- process guard: `5ead198698d748b291f24285bce6867de79a13645d15ccf51d80bae17678aefa`;
- raw output: `25887ba1e2a81776a87a88ab0f78cfc0134a408fa3642686d039d04ba5f9df90`;
- harness report: `6e34216d963813ec172a080aa74d19151524b7a947b1287c8140d5632363629d`;
- execution record: `0cad485e00a4ef9c5927aa0823767b8968dca6375f4ff2832df04117edcf30a4`.

## Independent numerical check

The source identity, 5,000 rows, 2,704 released columns, 259 represented
columns, `k=25`, three repeats and ordered 11-prefix set all match. Each reference
time equals its copy plus solver time, and every median is the actual median.

Prefix 25 is the only negative raw residual:
`-1.7763568394002505e-15`, within tolerance
`6.006062328983297e-10`, so it is the sole clipped value. Prefix 50 is exactly
zero; prefix 100 is positive and is not clipped. Direct-SVD absolute differences
are `4.014583804279326e-15`, `1.829647544582258e-13` and
`2.2737367544323206e-13` at prefixes 150, 1000 and 5000, respectively, all
inside the frozen engineering tolerances. Prefix 5000 Gram and SVD residuals are
`593.627871987748` and `593.6278719877478`.

The reviewer reproduced a 0.001568--0.004070 second range and 0.027688 second
sum for the 11 median reference times. The retained load, Gram update, script
wall, process CPU and high-water RSS are 0.910241 seconds, 0.295232 seconds,
1.422161 seconds, 1.421907 seconds and 80,104 KiB. The process guard itself
records 1.734953 seconds; the attempt layer records 1.819965 seconds, the native
receipt 2.162537 seconds and the harness 3.033931 seconds. These boundaries are
distinct and must not be conflated.

## Ledger and scope

The reviewer recomputed `73.202525 + 1.421907 = 74.624432` process CPU seconds,
attempts 13 to 14 and registered tasks 64 to 65. Scientific experiments remain
zero and the reservation is released. Raw and harness flags deny full-queue
admission, baseline comparison, scientific verification and gate advancement.

Acceptance does not establish actual BLAS thread observation, official scorer
parity, a Landmark baseline matrix, near-zero denominator qualification,
published-figure replication, G01, Gate A, scientific evidence or a paper claim.
