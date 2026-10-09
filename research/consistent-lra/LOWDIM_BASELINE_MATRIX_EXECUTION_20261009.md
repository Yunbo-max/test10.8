# Low-dimensional baseline matrix execution: integrity failure

Status: **invalid / confounded; no numerical result is admissible**.

This record preserves the first and only execution of the independently
reviewed developmental existing-baseline matrix.  The process reached exit
code 0, but post-execution byte checks contradict both the native manifest and
the harness receipt.  A terminal harness state is therefore not treated as
evidence acceptance.

## Frozen admission

- admitted project commit: `b919a10b30d962d8a0d1fccd67321f8969e1a100`
- source candidate: `608bce8dafc9bbe7ce7c14082191fab27ac6e372`
- native plan digest: `7358225c54cbe1f78fc9d6b0dfe80d32c83f906d83c0307047a0d36e7076f467`
- harness plan digest: `6a488ed4362dbdc9e9d99799f6ccca07a5cb20e0ce53e575c4b036f379fdde96`
- attempt: `rice-skin-lowdim-existing-baseline-matrix-a1-86d48c102a9d4a22862ba72047016fb7`
- retry count: 0
- receipt SHA-256: `a2160582c6feb89dae45a0caf1ef185929cd63fe8a86e5662a610380226ce826`
- process guard SHA-256: `ea8e72f19510635fd5163f4bc40c33014726c1ba3a9b48a6402a8570aae3fd25`
- stdout SHA-256: `1fdf3b67d1cdfec2b1ee6afb181e00ea65be313022c306219d7f33de9c557f3e`
- stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- native manifest SHA-256: `eaefff5ad920faa8cc3f61b26b3b446af3f4ba8108d5ecb3f4b429a57316dbfd`

The admitted command started at `2026-10-09T04:28:41.219860Z` and the native
attempt recorded completion at `2026-10-09T04:29:05.602294Z`.  Native usage
was 23.299657982 wall seconds, 23.294645 process CPU seconds, and 157864 KiB
maximum RSS.  This charges one executable/preparation attempt and zero
scientific attempts.

## Post-execution integrity observations

All three archive files raise `EOFError: Compressed file ended before the
end-of-stream marker was reached` when read as gzip/tar.  Their current hashes
also disagree with the hashes written by the native process:

| Archive | native-manifest hash | harness-receipt hash | current hash |
| --- | --- | --- | --- |
| Rice k=1 | `75af6d2ca4b0de706c04892ab4e7c57b26b3967bcdcbba1dfb66ad18e783015b` | `71cfc22009bee9e2ae56e2be96cb6a01a08ce0308551d67ad39b63c2fe17369e` | `71cfc22009bee9e2ae56e2be96cb6a01a08ce0308551d67ad39b63c2fe17369e` |
| Skin k=1 | `2cd63fb9a5098a2577d0e03a304de6511dc1327f73f81598ca5b2e82c81197a2` | `dff09b42a524d0e5020be4bd767c2d6d2da037fe5a801bf7520bb50ca5e12603` | `dff09b42a524d0e5020be4bd767c2d6d2da037fe5a801bf7520bb50ca5e12603` |
| Skin k=2 | `35fb0cbf209843d3d1dfa393d5ba14d7d0e50c4a893f224b1b21876b8523cccb` | `35fb0cbf209843d3d1dfa393d5ba14d7d0e50c4a893f224b1b21876b8523cccb` | `5e3588ab14553460cc17c66112fafe76b003dd7648cc918621cfc1c6212dacba` |

The runner was specified to delete its temporary staging directory after
successful archive creation.  Nevertheless,
`evidence/baselines/lowdim-matrix-xqdpr195/` was present after termination. Its
filesystem birth time is `2026-10-09T04:29:07.113300679Z`, after the recorded
native completion.  This is an observation only; the cause is unresolved.

Checking the surviving staged members against the immutable manifest found
four raw JSONL mismatches:

| Member | manifest hash | current hash |
| --- | --- | --- |
| `rice-k1__algorithm4-c2p0.jsonl` | `efa30249adadedcaac3fc61c092ba00018f7a9f3563086a28d27689c53d287d6` | `5ea4c818ac9fc549c3dac4f27b9c560a27c390372bb8955262add291051443af` |
| `rice-k1__fd-ell2.jsonl` | `976f434069448b978057d5b633cf19b6d61debbc08f7eda7d8b339c72c899fed` | `b4c1b029202d832d6024800ec9fda57a83b812d64699e1671d760e15a425cb26` |
| `skin-k2__algorithm4-c5p0.jsonl` | `016c205a25b49e5424cecb9a1093cda99d35ab3254f76da9c927150423664c8b` | `1f4ac858581199418a2c353d8fd4ee83d27551e8bee66ac745913ef28c9befef` |
| `skin-k2__periodic-interval10.jsonl` | `1e119495c33be347e49b6487a41fd60cab35f9a6352f9eb94c6c08c851108106` | `7e7baeb12ad08a338d4cb0e46ea039a73a34c3c0e510b5abda88b12ea5f88193` |

The staged Skin-k1 members had zero manifest mismatches at observation time,
but that does not rehabilitate its truncated archive or the batch as a whole.
The corrupted archives and the 94 MiB surviving staging directory are retained
unchanged in the attempt workspace for local diagnosis.  They are not used to
derive scores, rankings, plots, parameter choices, or claims.

## Gate consequence

- Harness `completed` means only that the guarded process returned zero.
- Evidence verdict before independent review: `invalid_confounded_output_mutation`.
- Scientific failures charged: zero; this is an evidence-integrity failure.
- Gate A, G01, E04, confirmation, discovery, and writing remain closed.
- No blind retry is permitted.  The next action is independent review of this
  fixed record and exact source/collection diagnosis.  Any repair needs a new
  frozen plan and counts against the two-repair cap for this identical failure.

