# Native baseline cost calibration plan

Status: proposed engineering calibration; no execution or scientific verdict yet.

## Fixed question and boundary

Measure the actual CPU, wall-time, RSS, prefix coverage and raw-output size of one
complete low-dimensional native baseline path before admitting a larger queue.
The fixed workload is the released Rice order after the author's full-dataset
standardization, first 3,000 rows, rank 1, repaired Algorithm 4 with `c=2.5`,
all prefixes 1 through 3,000.  This is the paper-text `c` value and is chosen
before inspecting any full-stream output; it is not tuning.

The executable computes the project repair's direct residual, independent fresh
SVD tail, projector recourse and separated update/reference/scoring clocks.  It
must retain every per-prefix record and basis.  The task is an engineering cost
and coverage calibration only.  It cannot establish official-author scorer
parity, reproduce a published figure, compare methods, advance Gate A/G01/E04,
or support a performance claim.  Numeric metrics are retained because they are
needed to check the executable, but are quarantined from scientific claims.

## Identities and finite reservation

- Restored parent: `a516dd86975f83753e4539bc6da21f0102172fc6`.
- Input: `originals/Rice_Cammeo_Osmancik.arff`, Git blob
  `745655b79f4ca46a3a65a0a8653bd792fa6f7c31`, project SHA256
  `1af97883100c89de2ea2972f7a28d428f4f1c14711a61defc0b0569e9eb65665`.
- Code: `native_baselines.py` SHA256
  `4d005ff930d4b577569d09cd99f20bb2fc48ad04ba2ac7dfd5351827f278b382`
  and `baseline_qualify.py` SHA256
  `d5566e2177064d0ddd9f940323ca7d10dfb0d9fef14d93f8ba6d16bde54dd934`.
- Contract/design inputs: `REPAIR_CONTRACT_v1.md` and
  `NATIVE_PROTOCOL_DRAFT.md` at the hashes declared in the native plan.
- Reservation: one CPU core, 512 MiB admission estimate (not an OS-enforced
  hard memory limit), one attempt, zero retry, 90-second process timeout,
  120-second harness window, no GPU and no additional package installation.
- Thread environment: numerical libraries are capped at one thread by the
  admitted command environment inherited from the harness invocation.

The output paths are
`evidence/calibration/rice-algorithm4-c2p5.jsonl` and its adjacent
`.summary.json`.  Success requires exit zero, exactly 3,000 parseable JSONL
records with consecutive prefixes/sample IDs, finite metrics, summary/input/code
hash binding through the receipt, and independently reviewed receipt/output
identities.  Timeout, missing prefix, non-finite value, hash mismatch or
unreviewed output is retained as a failed/invalid engineering attempt; no retry
is authorized by this plan.

## Queue consequences

The observation may bound later low-dimensional Rice/Skin/random engineering
qualification, but cannot extrapolate Landmark cost: Landmark has dimension
2,704 and the current exact fresh-reference loop decomposes every growing
prefix.  Landmark remains pending a separately reviewed exact scoring/reference
strategy and its own calibration.  The complete four-family G01 remains a
design with gaps, not a passed protocol.
