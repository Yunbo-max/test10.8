# Independent Landmark source/provenance reconciliation

Review date: 2026-10-10 (UTC). Reviewer: `/root/source_reconciliation`.

**Verdict:** The Simple B02 HTTP 502 record and the older project's successful acquisition are compatible records of different acquisition routes. Exact Landmark data was historically acquired and independently accepted in the older project. The Simple evidence packet did not recover that earlier dataset or qualification history. I could not locate the matrix at the sourced historical paths or inside the inspected existing archives on this host. Therefore the source identity and prior evidence are reusable, but there are no currently verified local matrix bytes available for a new run within this review's search scope.

This review used authenticated GitHub plugin reads and read-only local metadata/hash/archive-directory inspection. It downloaded no matrix/archive from upstream, ran no project code or scientific experiment, and changed no repository, automation or scientific status. Its sole written artifact is this review.

## Immutable snapshots and source identity

The observed `Yunbo-max/test10.8/main` head was pinned once to `42016612c10550acaffe1bb117c984ba29218270` (commit timestamp `2026-10-09T19:29:23Z`). All old-project files below were read at that SHA. Its `research/consistent-lra` subtree is `d134493bc9f3dcd374d0278c1c89e496c4c5f706`.

The upstream author tree was independently read through the GitHub plugin at `samsonzhou/consistent-LRA@d607c4f6467216c470d1e3b93989d44d5fcdec97`; it reports:

| Object | Exact identity |
|---|---|
| Original matrix path | `landmark.mtx` |
| Matrix Git blob | `4c63060bbefcb38e0c705cea1f883d2fb7121f2c` |
| Matrix byte size | `34,964,305` |
| Matrix SHA256, recorded by accepted historical byte checks | `29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b` |
| Author script | `consistent-lra-landmark.py`, blob `6da3eec62de50b5b37c36b26ae725549e354a738`, `4,494` bytes |
| Author ZIP | `consistent-lra.zip`, blob `c21ab360aa60d7f9d77df11dad21b16ae5cee21e`, `13,565,419` bytes |

The current upstream tree read independently confirms the matrix's Git object and byte size. The matrix SHA256 above is authenticated historical evidence, **not a newly recomputed matrix hash on this host**. No matrix bytes were obtained in this review.

Exact source locators:

- [Frozen matrix](https://github.com/samsonzhou/consistent-LRA/blob/d607c4f6467216c470d1e3b93989d44d5fcdec97/landmark.mtx)
- [Frozen author script](https://github.com/samsonzhou/consistent-LRA/blob/d607c4f6467216c470d1e3b93989d44d5fcdec97/consistent-lra-landmark.py)
- [Acquisition record](https://github.com/Yunbo-max/test10.8/blob/42016612c10550acaffe1bb117c984ba29218270/research/consistent-lra/LANDMARK_SOURCE_ACQUISITION_20261009.md)
- [Source correction/review history](https://github.com/Yunbo-max/test10.8/blob/42016612c10550acaffe1bb117c984ba29218270/research/consistent-lra/LANDMARK_SOURCE_QUALIFICATION_REVIEW.md)
- [Mechanical execution and evidence-review record](https://github.com/Yunbo-max/test10.8/blob/42016612c10550acaffe1bb117c984ba29218270/research/consistent-lra/LANDMARK_INTEGRITY_EXECUTION_20261009.md)

The acquisition record says the data was checked out read-only from the frozen author commit. The root matrix and ZIP member were compared byte-for-byte, with identical Git/SHA256 identities and 1,151,246 text lines. An initial erroneous 35,342,655-byte observation was rejected, corrected to 34,964,305 bytes, and independently rereviewed as accepted. This is preserved correction history, not two matrix versions.

The accepted mechanical run was `landmark-source-integrity-01`, attempt `landmark-source-integrity-01-a1-da869994c8214556a5969d39ee316ae5`, completed at `2026-10-09T02:04:49.736273Z`, one attempt and zero retries. Its evidence says `numerical_qualification=false` and `scientific_gate_advanced=false`; the receipt says `gate_advanced=false`.

## Hash verification performed in this review

I reconstructed UTF-8 bytes from the pinned GitHub file responses, independently computed SHA256 and Git blob hashes, and checked each computed Git blob against GitHub's returned object identity. All eight checks agreed:

| Artifact under `research/consistent-lra/` unless noted | SHA256 recomputed here |
|---|---|
| `LANDMARK_SOURCE_ACQUISITION_20261009.md` | `283a2484d05f48eabc31411d8fe598a22d9f530d76406c365fb8160beef7028d` |
| `LANDMARK_INTEGRITY_EXECUTION_20261009.md` | `bec72037c615dee114f772415fafe92d4adde5d1ceffba5b601a0b0732cae6e2` |
| `inspect_landmark_source.py` | `fbace7373933a792f9796e1d735047aaa149a25a9236cbe248804c9d8d2eece4` |
| `LANDMARK_SOURCE_QUALIFICATION_REVIEW.md` | `004f6ddd287cb45d9eab149fa85ba1f1e45dca15c0905ec2409a96fc1e6f99a5` |
| `evidence/landmark-source-integrity.json` | `62595f9dec8c563b05ebe92a0ecc66ac569c2f9730b699728613f5a366fc8e35` |
| `runs/attempts/landmark-source-integrity-01/receipt.json` | `a535fc7f3da44abd05f19b9614f71d2122eabe32e40ad57d1bcf53703115fa00` |
| `EXPERIMENT_READINESS_SOURCE_MANIFEST_20261009.json` | `70c225b26b807e9434a252bfb8c5657cbab87debbc54b7579923860981c9347b` |
| Upstream `consistent-lra-landmark.py` | `5999ad7cbfbe8e17677550c2c58fcce09d016ebd2eb7d99d6f57bbc57c295a86` |

The evidence and receipt hashes exactly match the historical execution record. The inspector and acquisition hashes exactly match the accepted correction review. Inspector source inspection confirms streaming identity/count checks only, with no densification, SVD, loss or recourse computation; it was not executed here.

The readiness manifest is a historical source-read manifest bound to base `4ab8e122fcaed61b6f1ac9ec4d8e899989402036` and legacy head `7286e6d5b301f01ebda45d6fa1387afd9d383906`, explicitly marked `raw_outputs_rerun=false` and `proposal_status=design_only_unadmitted`. It is not a source dataset bundle or an experiment receipt.

## Current-host recovery check

The old workspace `/workspace/scratch/bb9f262965cf` exists. The following exact matrix paths were resolved from pinned plans/receipts and all are absent:

```text
/workspace/scratch/bb9f262965cf/destination-repo/research/consistent-lra/originals/landmark.mtx
/workspace/scratch/bb9f262965cf/destination-repo/research/consistent-lra/runs/attempts/landmark-source-integrity-01/landmark-source-integrity-01-a1-da869994c8214556a5969d39ee316ae5/workspace/originals/landmark.mtx
/workspace/scratch/bb9f262965cf/lra-resume-nR15vW/research/consistent-lra/originals/landmark.mtx
/workspace/scratch/bb9f262965cf/lra-resume-nR15vW/research/consistent-lra/runs/attempts/landmark-reference-calibration-01/landmark-reference-cost-a1-177b60cdd7444745b59898cc4731e74a/workspace/originals/landmark.mtx
/workspace/scratch/bb9f262965cf/lra-window02/research/consistent-lra/originals/landmark.mtx
/workspace/scratch/bb9f262965cf/lra-window02/research/consistent-lra/runs/attempts/landmark-stage-a-v2-qualification-02/landmark-stage-a-v2-identity-a1-4132a34d9d364ec9b556ac5d64803735/workspace/originals/landmark.mtx
```

A targeted filename search under that sourced historical workspace found only Simple acquisition/author scripts, no `.mtx` file. Central directories of its 60 existing ZIP files were inspected without extraction; no `.mtx` or Landmark binary member was found and no archive read errored. The five current `restored/*.zip` archives likewise contain no matrix; only `consistent_lra_b02_evidence_03.zip` has Landmark items, namely the author script, acquisition script and failed-acquisition JSON. These are bounded search observations, not a claim that every possible filesystem or remote store was searched. Nested ZIP members were not recursively expanded.

The pinned destination repository tree contains no `landmark.mtx`, consistent with its acquisition record's explicit choice not to duplicate the 34 MiB input in the destination branch.

## Simple B02 reconciliation

Current local input root: `/workspace/scratch/fc9ea2af50dd/evidence/consistent-lra-expanded/continuation-12`.

Its `LANDMARK_ACQUISITION.json` records only `https://sparse-files.engr.tamu.edu/MM/Pereyra/landmark.tar.gz`, `status=source_unavailable`, and `HTTP Error 502: Bad Gateway`. The source code tries only that URL, bounded to 40 MiB and a 20-second request timeout. It does not attempt the already identified author-repository blob. Its failed retrieval does not invalidate the earlier independent acquisition through GitHub.

The following local hashes agree with `B02_MANIFEST.json`:

| Local artifact | Bytes | SHA256 |
|---|---:|---|
| `LANDMARK_ACQUISITION.json` | 543 | `69da63c01126947b22dc2558b0c1e544e827787b7118637d25a436c6e8349644` |
| `acquire_landmark.py` | 1,344 | `df0ccc30623b301c394e4316ab19616fc3600ad6e125a800e2ae66597d56b398` |
| `author_landmark_pinned.py` | 4,495 | `8fed7f0f391fc630e0b59c96dff9f71f5cd63b6c7bef38348eea599015a7ae51` |

The B02 manifest itself is 105,901 bytes, SHA256 `f42daa08ed39523b5a02ede8cd4408fd5fd35e1121426556c3f4d87cafef51dc`. The local author script equals the upstream script plus exactly one trailing LF. Its bytes are therefore not the upstream blob's exact bytes, but there is no substantive source change; preserve both identities when joining provenance.

Recommended corrected status: **“Simple B02's SuiteSparse retrieval failed; the older project already qualified the exact frozen author matrix and retained source/integrity evidence. The matrix is currently not restored at the checked paths. Complete scientific Landmark comparison remains unestablished.”** Keep the original 502 receipt unchanged.

## Original Landmark protocol

Directly verified against the complete frozen author script:

- Read `landmark.mtx` with `scipy.io.mmread`, convert the full matrix to dense, select `dataset = all_data[:5000]` in original row order, retain all 2,704 columns, and use `k=25`.
- No standardization, normalization, shuffle or split is applied. `StandardScaler` is imported but never called. The correct description is **author-script-selected first-5,000-row prefix**, not a separately published 5,000-row matrix.
- Set Python and NumPy seeds to 1. Evaluate `c_list=[1.1,2,5,10,100]` with `randomized_svd(..., n_components=25, n_iter=7, random_state=None)` when the running squared energy exceeds `c*count`.
- Literal loop `range(n-1)` evaluates prefixes **1 through 4,999**, despite selecting 5,000 rows. A repaired 1-through-5,000 evaluation must disclose that repair. The old project's protocol draft also distinguishes a proposed 150-through-5,000 slice (4,851 prefixes) from any unverified paper Table-1 denominator.
- The released script counts recourse as `+k` per refresh. It computes its purported reference using the most recently refreshed `V`, sets a zero-reference ratio to 1, retains some state across `c` values, and uses a runtime start outside the `c` loop. Consequently source recovery does not itself qualify its scores or establish parity with an independently repaired scorer.

Historical accepted mechanical evidence reports the original matrix shape as 71,952 × 2,704, with 1,151,232 stored entries, 1,146,848 numeric nonzeros and 4,384 explicit zeros. The first 5,000 rows contain 80,000 stored entries, 79,325 numeric nonzeros and 675 explicit zeros, exactly 16 stored entries per row, all rows nonempty, and 259 represented columns. The native dimension remains 2,704. Historical work's 259-column representation is a documented engineering reduction, not a new native dataset identity.

## Reuse boundary

The older main also retains [accepted full Stage-A v2 engineering evidence](https://github.com/Yunbo-max/test10.8/blob/42016612c10550acaffe1bb117c984ba29218270/research/consistent-lra/LANDMARK_STAGE_A_v2_FULL_EVIDENCE_REVIEW.md): 35 selected native prefixes × 13 arms = 455 oracle records, plus 5,000 prefixes × 13 arms = 65,000 timing records. This is retained accepted evidence of finite numerical identities/output integrity/engineering costs, not a new independent replay performed by this review. Thus “no high-dimensional pilot ran” is only accurate when scoped to Simple B02, not the combined project history.

The same review explicitly leaves all-prefix scoring, near-zero derived-metric classification, scientific evaluator authority/protocol, Stage-B dispatch and fresh confirmation open. Reuse its records as historical engineering evidence; do not relabel them as a complete scientific comparison or fresh confirmation.

For future data restoration, reuse the exact author commit/path/blob/size/SHA256 above and verify actual restored bytes. There is no reason to replace this dataset, normalize it silently, create a different matrix, or rerun already accepted source-integrity/Stage-A work merely because old scratch files are absent. This audit does not authorize a download or new numerical dispatch; it establishes their exact provenance target and current recovery gap.
