# Independent evidence review: Rice Algorithm 4 calibration

Reviewer: `/root/rice_skin_evidence_review`.
Evidence commit: `4ffc2d57a43e740a4205cdabba7fab303ddd8f15`.
Verdict: **accepted** for engineering cost/prefix-coverage calibration only.
The reviewer performed read-only verification and launched no workload.

## Binding and execution

The reviewer recomputed the native plan digest
`3478d69f2387ed65c06e382859fb579d65891822cada6cfd6b281b435b9a461c`
and harness digest
`3d501cb5b10c3a1e40e377737bc37eef00eda2e56326b3e6a55e73cd931b8d5b`.
Plan, receipt, attempt and process guard have the same exact argv, binding all
five numerical thread variables to one before the fixed interpreter runs Rice
Algorithm 4 with `k=1,c=2.5`.  There is one attempt, retry index zero, exit zero,
empty stderr, no GPU device and no second attempt.  Harness events are exactly
batch start, task start and completed task; report/state are terminal with
`gate_advanced=false` and `scientific_result_verified=false`.

Key evidence SHA256 identities:

- execution record:
  `c5d88c601d1946e09447ca95567c643fc7c5eed14cdf3abf4d44c1620298389d`;
- verification JSON:
  `c74f62832bd87372f2d3b010902d7490d3ccb7409d04ebc25fd34cba299b109a`;
- receipt:
  `5c7fc845d29f0bed4adda18d0102a6055dbc69b21640f6c991aab7f09f21fc45`;
- attempt:
  `0a115236755cd40b99514e0fea6fd425e63b852d9ecafad9272a8ef60e4c5578`;
- process guard:
  `34a431b4d674ff0e5fab9e1296990599e13bc6b58e63fb314f9cbfb2e8fe88b7`;
- gzip/raw/summary:
  `70351bcf505b93af38e0cfd28eecda099a9cabbb68a2c2edb4d8b0461a6e22fd`,
  `921e5b8f63387d15a5e893a35e3eac97fb936c15617042641b88c83c6536589e`,
  `2c124b017e374642fc020c13df402d26a8186b874e0fc2bfd26a73fc924b075d`.

## Independent raw-output verification

Streaming decompression produced exactly 2,572,831 bytes and 3,000 lines with
the declared raw hash.  Prefixes are the consecutive integers 1 through 3,000,
without duplicate or skip; sample IDs are exactly `rice:row:<prefix>`.  Rank is
one and each basis is 1 by 7.  All inspected numeric core, basis and timing
values are finite.

The reviewer independently recomputed one near-zero-OPT exclusion, zero
positive-loss near-zero cases and 2,999 ratios.  Mean differs from the stored
value only by 1.5e-15 summation-order rounding; median, maximum and final
recourse match.  Update, reference, scoring and energy timing sums, pipeline
0.502146982 seconds, CPU 0.498551 seconds and peak RSS 120,220 KiB all match the
stdout, summary, verification and ledger.  Rice source/transformed/label hashes
and the first-3,000 label counts also match the retained input.

The uncompressed output is not separately committed, but the deterministic
gzip reconstructs it byte-for-byte, so the reviewer found no evidence gap.
Ledger arithmetic is exact at recorded precision: prior CPU 1.581142 plus run
CPU 0.498551 equals 2.079693; attempts move from 7 to 8, scientific attempts
remain zero, and the terminal receipt/guard plus ledger support the released
reservation.  There is no separate lease-release receipt or independent live
OS liveness proof, so that conclusion is limited to retained evidence.

## Scope

Acceptance does not confer official scorer parity, published-figure
reproduction, complete baseline qualification, G01/E04/Gate A, confirmation,
performance-claim eligibility or Landmark cost extrapolation.  Sensitivity,
author FD diagnostics, other comparators and the other three families remain
pending.
