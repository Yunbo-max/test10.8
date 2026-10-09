# Rice Algorithm 4 cost/coverage calibration execution

Status: completed engineering execution; independent evidence review pending.
No official scorer parity, performance comparison or scientific gate is claimed.

## Bound execution

- Admitted parent: `17c4008854dee58acdf34ccbdc37e742b99b1fb2`.
- Native plan digest:
  `3478d69f2387ed65c06e382859fb579d65891822cada6cfd6b281b435b9a461c`.
- Harness plan digest:
  `3d501cb5b10c3a1e40e377737bc37eef00eda2e56326b3e6a55e73cd931b8d5b`.
- Attempt:
  `rice-algorithm4-c2p5-a1-c5d167bc4a6b40faa8284dded1c0d14d`.
- Start/completion: `2026-10-09T03:31:20.926797Z` /
  `2026-10-09T03:31:22.938875Z`; harness terminal status `completed`.
- Receipt SHA256:
  `5c7fc845d29f0bed4adda18d0102a6055dbc69b21640f6c991aab7f09f21fc45`.
- Raw JSONL SHA256:
  `921e5b8f63387d15a5e893a35e3eac97fb936c15617042641b88c83c6536589e`;
  deterministic gzip SHA256
  `70351bcf505b93af38e0cfd28eecda099a9cabbb68a2c2edb4d8b0461a6e22fd`.
- Summary SHA256:
  `2c124b017e374642fc020c13df402d26a8186b874e0fc2bfd26a73fc924b075d`.

The deterministic gzip is the durable copy of the full 2,572,831-byte raw
JSONL.  Decompression must reproduce the declared raw hash before analysis.
The receipt, attempt record, process guard, stdout/stderr and harness state are
retained beside it.

## Mechanical verification and observed cost

The retained verification parsed all 3,000 JSON lines.  Prefixes are exactly
1 through 3,000, every sample ID equals `rice:row:<prefix>`, and the selected
energy/loss/OPT/excess/recourse/timing fields are finite.  The run has one
near-zero-OPT exclusion at the first prefix, zero positive-loss near-zero-OPT
violations and 2,999 defined ratios.

Observed workload usage: pipeline 0.502146982 seconds, process CPU 0.498551
seconds, peak RSS 120,220 KiB.  Component clocks are update 0.007995399,
fresh-reference 0.238555392, scoring 0.139484232 and energy maintenance
0.003951160 seconds.  These are single-run engineering calibration values, not
hardware-independent performance benchmarks.

The raw output contains ratio mean 1.002642561, median 1.001234885 and maximum
1.582172828, with final and post-warmup projector recourse 0.290329800.  These
numeric observations are disclosed for audit but remain quarantined: one arm,
one dataset and the project-repaired non-official scorer cannot decide a fair
baseline comparison or any paper claim.

The finite reservation is released because the harness and guarded attempt are
terminal and no descendant is retained.  Release does not imply evidence
acceptance.  An independent reviewer must bind the exact receipt, compressed
raw output, summary, prefix verification and scope before this calibration can
guide any further low-dimensional queue.
