# Native evaluation coverage and G01 design draft
Version 2; route M baseline/evaluator qualification. Entire-paper comparison NOT ready. No candidate methods are implemented or admitted.
Question: can a repaired implementation measure the published reconstruction/recourse tradeoff without evaluator-induced artifacts? Rival explanation: mismatched recourse or reference, prefix omission, future preprocessing, warmup rank and numerical degeneracy.
Acceptance for qualification: native dimensions/counts/order/hash match; independent scorer calculations agree within frozen numerical tolerance; every intended prefix appears; no hidden zero-OPT ratio; independent reviewer accepts code/source mapping. Failure invalidates the relevant software/scorer path, not the paper's theorem.

## Coverage
| Family | Exact native source | Scope/preprocessing | Current prerequisites |
|---|---|---|---|
| Rice | author ARFF blob745655b79f4ca46a3a65a0a8653bd792fa6f7c31; UCI545 DOI10.24432/C5MW4Z | 3810x7 features+class; full-data StandardScaler equivalent, first3000/k1; preserve row IDs1..3810 and class | 13-arm/39000-row developmental matrix accepted under the repaired local scorer |
| Skin | author TXT blobfc58dda2eaf5b1f0d2d8c7924a298cd7d14ba17d; UCI229 | 245057 BGR triples+label; full-data scaling, first3000/k1,2 | two 13-arm/39000-row developmental matrices accepted under the repaired local scorer |
| Landmark | author MTX blob4c63060bbefcb38e0c705cea1f883d2fb7121f2c; SuiteSparse903 Pereyra/landmark | 71952x2704, first5000/k25, no scaling in author code | exact bytes and mechanical first-5000 counts accepted; blob reacquired on the current host; exact all-prefix reference cost and numerical matrix remain pending, with no approximate OPT relabelling |
| Random published family | consistent-lra-random.py blobcfe96c16b699a96720e41cc36ab36a25a45b4627 | Python random.randint(0,100),3000x4/k1; no upstream seed; released code unscaled, paper says column-normalized | exact original stream cannot be reconstructed; one frozen seed has an accepted 13-arm/39000-row prospective developmental matrix, NOT figure replication or confirmation |
| Random fast diagnostic | consistent-lra-random-fast.py blob4edc0664ac183391af3a761e429c67947a61cc1e |3000x100/k20/c10; no seed, randomizedSVD each prefix | diagnostic source only; cannot replace published3000x4 |

Rice and Skin official UCI pages state CC BY4.0; no class prediction is claimed.
The SuiteSparse Collection license record is CC-BY 4.0 with attribution and
modification-disclosure requirements.  Author-repository code licensing remains
unresolved; retain minimal provenance and unmodified originals for audit and do
not assert a permissive software license.

## Arms, parameters and metrics
Primary source repair arms: exact Algorithm4; fresh prefix SVD; sourced FD with ell=min(d,2k) and ell=min(d,4k), both clipped to d and require ell>k; fixed warmup subspace; periodic refresh intervals10,100. Author FD is a source diagnostic, not the qualified strong FD comparator. All arms use the same stream, rank convention and float64; tuning is absent for qualification.
Paper/source c disagreement: main figures 2.5 versus code/table2. Record both as distinct predeclared values c={1.1,2,2.5,5,10,100}; Skin k2 separately includes1.5. They are sensitivity settings of the same method, never independent papers.
Metrics per prefix: raw loss, OPT, energy, additive excess, normalized excess
`(loss-OPT)/energy` when energy is positive, ratio only when
`OPT > 1e-10 * max(1, energy)`, projector increment, cumulative recourse from
prefix 2, steady recourse excluding initialization, refresh count,
numerical/tie diagnostics and separated update/scoring/pipeline timings. Ratios
cannot replace the additive guarantee. Aggregation reports final endpoints plus
mean/median/max over all declared eligible prefixes, the exact denominator and
near-zero-OPT exclusion count. Prefixes are dependent, not replications.

Accepted developmental denominators are frozen as follows: Rice k1 is 2999
defined / 1 excluded; Skin k1 is 2999 / 1; Skin k2 is 2986 / 14; and the
prospective random k1 instance is 2999 / 1. Every cohort has zero positive-loss
case with near-zero OPT. Landmark has no accepted denominator. The paper
caption's “between 150 and 5000 updates” does not join reproducibly to the
frozen source: author code processes prefixes 1..4999 and contains no Table-1
aggregation. A repaired future runner must retain prefixes 1..5000 and may
separately report the labelled project slice 150..5000 inclusive (4851
prefixes); neither is called the source Table-1 denominator until parity is
demonstrated.

## Controls and planned complete comparisons
The fixed/periodic controls separate stability achieved by staleness from accuracy; freshSVD measures exact reconstruction/recourse ceiling; FD measures sketch approximation and its output recourse; exact versus randomized reclustering is a separate repair/accuracy confound requiring qualified approximate reference if used. Fair matched tuning is developmental and limited; no test-selected c or interval.
All four families remain required for any “improves this paper” scope.  The
accepted Rice/Skin matrix and one prospective random seed cannot substitute for
the missing Landmark numerical matrix or the unreconstructable published random
stream.  A repaired-local-scorer qualification is not official parity or
confirmation.
No new candidate is accepted until Parent/Gate0/IPCG, real baseline residual failure, approximately20 consequential math cards, primary source/code novelty audit, independent pool review/ranking and verify_methods.py boundaries. Candidate-specific mechanism controls, frozen effect sizes/uncertainty and fresh confirmation are therefore pending.

## Development/confirmation, resources and commands
Qualification prefix set for lowdim inputs:1,2,3,7,25,100,1000,3000, each within the actual released prefix; these are direct software identity checks, not an arbitrary benchmark used to claim gains. Full baseline development now retains all 3000 prefixes for 39 Rice/Skin arms and 13 arms on the single prospective random seed. Development values are never promoted to fresh confirmation.
Published deterministic order itself is an existing finite case study; no confidence interval from treating adjacentprefixes as independent. Future random independent seeds and heldout existing conditions must be frozen before inspection to support appropriate paired uncertainty and broader claims. No statistical performance criterion or GateA is frozen here.
Initial reservation per qualification process is one CPU, 512 MiB, bounded wall
time, one attempt and no automatic retry.  All subprocesses must be admitted to
the pinned RSI harness and retain raw per-prefix diagnostics, stdout/stderr,
immutable input/code/output hashes and CPU/RSS.  The accepted low-dimensional
matrix used 6.64 process CPU seconds for the prospective random family and the
accepted final Rice/Skin repair used 22.41 process CPU seconds.  These costs do
not predict Landmark: its active first-5000 prefix still has 259 represented
columns and k=25, so exact all-prefix reference calibration must precede any
queue; no fit claim is made.

The accepted Rice/Skin execution is bound to
`plans/native-lowdim-baseline-matrix-final-repair.json` (SHA-256
`f8fc3ced...`, digest `d30ea825...`) and
`plans/harness-lowdim-baseline-matrix-final-repair.json` (SHA-256
`09fbf88d...`, digest `280abf63...`): one CPU, 512 MiB, one attempt, zero
retries, native 180-second timeout and harness 210-second total / 180-second
window. Its exact dispatch was:

```text
PYTHONPATH=vendor/rsi/scripts python vendor/rsi/scripts/run_harness.py --root . --execute --approved-plan-digest 280abf635dfb5662bce6a15ffb63977c72d72a320f44ef22f1554d9ec5b9e6cf plans/harness-lowdim-baseline-matrix-final-repair.json
```

The execution record is `LOWDIM_BASELINE_MATRIX_FINAL_REPAIR_EXECUTION_20261009.md`
(SHA-256 `3c108756...`). The accepted prospective-random execution is bound
to `plans/native-prospective-random-baseline-matrix.json` (SHA-256
`42a7cea3...`, digest `280027a1...`) and
`plans/harness-prospective-random-baseline-matrix.json` (SHA-256
`47cdbf44...`, digest `95657d85...`): one CPU, 512 MiB, one attempt, zero
retries, native 120-second timeout and harness 150-second total / 120-second
window. Its exact dispatch was:

```text
PYTHONPATH=vendor/rsi/scripts python vendor/rsi/scripts/run_harness.py --root . --execute --approved-plan-digest 95657d85b176afddc3bb682c8fc6b246cac8ba26e2f8db9de40f899be86d6292 plans/harness-prospective-random-baseline-matrix.json
```

Its record is `RANDOM_BASELINE_MATRIX_EXECUTION_20261009.md` (SHA-256
`1d8908f5...`).

The Landmark source can be restored by the already reviewed partial Git
checkout and must reverify blob `4c63060b...`, SHA-256 `29fb8701...`, and
34,964,305 bytes.  Restoration is data acquisition, not an executable numerical
queue. The reviewed acquisition command is:

```text
git clone --no-checkout --filter=blob:none https://github.com/samsonzhou/consistent-LRA.git author-consistent-LRA
git -C author-consistent-LRA checkout d607c4f6467216c470d1e3b93989d44d5fcdec97 -- landmark.mtx
```

There is no admitted Landmark numerical command, native plan or queue. Those
remain blocked until exact-reference cost calibration, source/semantic review
and independent plan review. No automatic package install is allowed.

G01 status: complete family-level design and explicit gaps, with accepted
developmental matrices for Rice, Skin and one prospective random seed.  It is
still pending an authentic upstream scorer-interface parity decision, Landmark
cost calibration and numerical matrix, candidate-specific controls, frozen
effect/uncertainty criteria, prospective confirmation and independent E04.
There is no G01 or Gate A pass.
