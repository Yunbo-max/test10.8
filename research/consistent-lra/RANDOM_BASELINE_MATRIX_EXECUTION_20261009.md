# Prospective random-family baseline matrix execution

Status: **completed; pending independent evidence/E04 review**.  This is one
predeclared prospective, unscaled development instance.  It is not a replay of
the unseeded Appendix-G/Figure-3 stream and does not yet support performance
claims.

## Admission and command

The execution followed the independently accepted plans at remote commit
`e9323da6bd4907f2585acdbb424913f807d71cce` and the admission ledger at
`387758bacb5bf3443971875252d1551281a1095e`.  Native plan digest:
`280027a1d2bc2279654868cd69d54182617e6c628017f842fd4b23327efea87f`.
Harness digest:
`95657d85b176afddc3bb682c8fc6b246cac8ba26e2f8db9de40f899be86d6292`.

The host was re-observed immediately before execution as cgroup CPU
`800000/100000` (8-core quota), memory `8589934592` bytes, effective cpuset
`0-8`; `nproc=9` is not the CPU quota.  The task used one process/CPU, a
512-MiB admission reservation, no GPU, one attempt and zero retry.  OpenBLAS,
OMP, MKL, NumExpr and vecLib thread variables were all set to one.

The exact harness command was:

```text
PYTHONPATH=vendor/rsi/scripts python vendor/rsi/scripts/run_harness.py --root . --execute --approved-plan-digest 95657d85b176afddc3bb682c8fc6b246cac8ba26e2f8db9de40f899be86d6292 plans/harness-prospective-random-baseline-matrix.json
```

Attempt:
`prospective-random-seed20261009-existing-baseline-matrix-a1-4effb02f72124183a5e61a1913b8b325`.
It exited zero with no retry.  Receipt SHA-256 is
`21f9577fe9fa837c47a5acb8cae823e4ae46e2d80f53bd2109bd9f8e3f7c8608`;
attempt record SHA-256 is
`af6e3ec256d477e0d4ccd9682886764d4fe25a84f2dfe23b6583b35edde944a1`;
process-guard SHA-256 is
`dbf49617e7e55c6d34080d311adbcb8983b0bf31585a50816d4637758a11c3c5`.
Stdout SHA-256 is
`f62b443316330466286da12585ea871c2e50505b5eabd94f5585134403f8fb70`;
stderr is empty with SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Identity, outputs and cost

The manifest records Python `random.Random(20261009).randint(0,100)`, row-major,
unscaled, `3000 x 4`, `k=1`, with matrix SHA-256
`13256cf8e42a78ada22dcf95253af44d593187a8009fa73e39223b98695752e1`
and `original_figure_replication=false`.  Manifest SHA-256 is
`5a30b214e230da04364f8cff6e6aef24f7e0b832c54d211fc27f5f550da4609f`.
The archive SHA-256 is
`af9b40bfb131570d1d5868006d0f4193550ba087f6679bb250a65554bab1bb8e`.

The receipt contains all 28 declared final outputs.  Two independent post-exit
rehash passes found 0/28 mismatches.  The archive is readable and contains 26
unique members (13 raw JSONL plus 13 summaries); its inventory and every
member hash match the manifest.  The manifest contains 27 pre-manifest
publication observations, all consistent with the receipt.  There are 39,000
per-prefix rows in the archive.

Producer usage was 6.640327 wall seconds, 6.639743 process CPU seconds and
120196 KiB maximum RSS.  Process-guard time was 7.777671 seconds; native
attempt time was 7.838890 seconds; harness elapsed time was 8.071583 seconds.
The reservation is released after terminal completion and post-exit rehash.

## Unreviewed descriptive summaries

The following values are transcribed from the manifest for independent
recomputation.  They are not accepted results yet.  Ratios exclude the one
near-zero-OPT prefix in every arm; each defined denominator is 2,999.  Rank-one
warmup makes total and steady recourse equal here.

| arm | ratio mean | ratio max | total recourse | steady recourse | pipeline s |
|---|---:|---:|---:|---:|---:|
| algorithm4-c1p1 | 1.00009168 | 1.00744355 | 0.158102508 | 0.158102508 | 0.385192 |
| algorithm4-c2p0 | 1.00100163 | 1.15206337 | 0.120433142 | 0.120433142 | 0.330170 |
| algorithm4-c2p5 | 1.00154073 | 1.72501896 | 0.159666730 | 0.159666730 | 0.330169 |
| algorithm4-c5p0 | 1.00434414 | 1.72501896 | 0.196733306 | 0.196733306 | 0.330329 |
| algorithm4-c10p0 | 1.00775573 | 1.72501896 | 0.204793266 | 0.204793266 | 0.338213 |
| algorithm4-c100p0 | 1.03894793 | 1.72501896 | 0.290682544 | 0.290682544 | 0.352963 |
| fresh-default | 1 | 1.00000000 | 0.157746609 | 0.157746609 | 0.596945 |
| fixed-default | 1.61153730 | 1.77272397 | 0 | 0 | 0.374209 |
| periodic-interval10 | 1.00152248 | 1.72501896 | 0.193526222 | 0.193526222 | 0.399097 |
| periodic-interval100 | 1.01995439 | 1.72501896 | 0.277277941 | 0.277277941 | 0.368230 |
| fd-ell2 | 1.00003932 | 1.00054150 | 0.177756949 | 0.177756949 | 0.509977 |
| fd-ell4 | 1 | 1.00000000 | 0.157746609 | 0.157746609 | 0.493265 |
| author_fd-ell2 | 1.00000196 | 1.00007171 | 0.160961335 | 0.160961335 | 0.526388 |

## Claim boundary

Before independent evidence review, none of the numerical summaries is
accepted.  Even after a successful review, the maximum scope is descriptive
development evidence for this one seeded member of the released unscaled
generator family.  It cannot establish original Figure-3 reproduction,
normalization parity, official scorer parity, confirmation, independent-seed
uncertainty, Landmark coverage, complete four-family G01, Gate A, theorem
validation, generalized superiority, paper readiness or a new paper.
