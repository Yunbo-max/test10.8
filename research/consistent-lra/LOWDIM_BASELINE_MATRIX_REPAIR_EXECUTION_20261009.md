# Low-dimensional matrix repair execution: mutation detected and rejected

Status: **failed safely; no numerical result is admissible**.

The independently admitted first repair ran once and returned exit code 1. The
new producer-side checks detected that retained members had changed before any
manifest was published. This is an evidence-integrity failure, not a method
comparison or scientific refutation.

## Frozen execution

- admitted project commit: `c0124b54efa688d0f3ddd88707f2d9c05a832a84`
- native plan digest: `10f6cacb9074dbcb3b5f8f539371aef148cb09b91eb606334d35e7b14f7969bf`
- harness plan digest: `78ce83b3889722561525987f4248782f0325061cf7692c3eb93adb17a1d276de`
- attempt: `rice-skin-lowdim-existing-baseline-matrix-repair-a1-ff7ec599eafb41258231aa7dc8473f6e`
- repair ordinal: 1
- retry count: 0
- receipt SHA-256: `4e79b341350560232cd49f3836eb575828ea23657a0267a6d540e6945caf3235`
- attempt SHA-256: `004f348deb153681ce34430ce7fd34ff59e6ca95ea424c4e446ffda1b9a54218`
- process guard SHA-256: `754d602c277c7401e3c0e56470d1de91b7318ba357a208cb52b9a9a9b451884c`
- stdout SHA-256: `8142070e4414aefb3ce92e8f3d385bd7f01a18233a20a1bd88316ee1bda57a0a`
- stderr SHA-256: `c500e6c585db286db7e202cfd9f2469f64462562ed48f7086882f0e781a54284`

The guard records 23.738794235 wall seconds. Because the failed runner did not
reach its aggregate usage manifest, exact whole-process CPU is unavailable.
Summing the 39 independently measured per-arm process deltas gives a retained
lower bound of 18.774782 CPU seconds; peak reported RSS is 158096 KiB. The
ledger therefore labels the cumulative 44.153886 CPU seconds as a lower bound.

## Detected mutation

All 39 summaries survived. Comparing their producer-recorded raw SHA-256 with
the current retained raw files found exactly four mismatches:

| Raw member | expected hash | current hash | surviving lines |
| --- | --- | --- | ---: |
| `rice-k1__fd-ell2.jsonl` | `1a4572b4d32e7e81138e1f7b53343e030da699be726f4146b5a2c1d244df6e19` | `be463e96d78c40fda606a39ed89777399848c30d10a02f16a1fd2f00c6de65b6` | 2330 |
| `rice-k1__fresh-default.jsonl` | `7e5804e4bb5a88bc1d4d88096747c0a4388cd79099069135a51422fd52c23c1c` | `18cedbd2bd008ebb3f18a39580e7a3cf90a1d84919cb7908c20ec71a9ce9ca53` | 2460 |
| `skin-k2__algorithm4-c5p0.jsonl` | `397243fc62bf0cdb66c4adeca9dd80581cdf9cdf27c44e510584a2e750c42c01` | `24e50c433d29ff03bfbea1258814c62ea206de8d949194996a1643ce0ad4a6d8` | 2431 |
| `skin-k2__periodic-interval10.jsonl` | `2c52faffbe068f14a9879130ae16910818c8e3504419c95a10371daba16bf217` | `123dd140c49cbcf1cd2d72e88e164f38c87399937d116f265aa1eda1db74f074` | 2133 |

The three no-clobber archive finals remain readable and each contains 26
members. Nevertheless, all three deleted archive `.partial` paths reappeared
with truncated, different bytes. This independently localizes the remaining
problem: progressive writes made directly to final raw paths can be replayed by
the surrounding workspace layer, whereas archive finals created only after a
complete partial was closed remain intact and the obsolete partial name is
recreated separately.

## Consequence and bounded diagnosis

- No manifest exists; the runner rejected the batch before publication.
- Harness `failed` is correct. Its retained output refs are failure artifacts,
  not evidence acceptance.
- No score, ranking, sensitivity choice, plot or paper claim may use this run.
- Scientific attempts and scientific failures remain zero.
- The reservation is released and repair count for this identical integrity
  failure becomes one.
- A second and final repair is justified only if every progressively written
  raw/summary file uses an unlinked partial name and the final path is created
  once from the complete inode. It requires fresh source and plan review.
