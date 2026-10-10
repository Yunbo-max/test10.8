# B08 independent saved-result review

Date: 2026-10-10. Reviewer role: independent mathematical/source and saved-result inspection. No new scientific command or experimental replication was executed by this reviewer. Reading saved arrays, hashing files, and independently calculating descriptive paired statistics are the only post-run computations here.

## Scoped disposition

B08 meets its prospectively frozen native512 timing and semantic qualification criteria for both eta values. FD50 is faster in all three paired process measurements at each eta. This is actual complete streaming-loop CPU timing, rather than B07's modeled subtraction of oracle costs. The claim applies to these implementations, this native first512 development prefix, rank25, raw order, and the specified numerical policy. It grants neither a new-method verdict nor independent scientific confirmation or paper readiness.

## Exact evidence inspected

SHA256 identities independently re-read from current bytes:

| Artifact | SHA256 |
|---|---|
| B08_FROZEN_DESIGN.md | 2fb12626563e44ba1b4b08f80d4212e4e575cf12f64b8a0d8ce48b313a6d14a6 |
| run_policy512_operational.py | 2ef7754b23b5bc2f3f2baa451a8e9e8740c681c22fdc35749a25df8234c50c1b |
| verify_policy512_operational.py | 29be14f9df38ee284e8d65f5c7da650aa5d488e0f17b1a2e477fb22a1d78b7d7 |
| B08_RUN_MANIFEST.json | 88d1b10169b5b5b7345d7530d36002bd1a5fd1c98c184f4e577f1d0001729164 |
| B08_OPERATIONAL_AUDIT.json | 294478fe17aa0dd0f17c2e0cdcea21f024dc0b40c5e3fee46590894ea2d5f999 |
| RUNNER_STATUS_FINAL.json | d1eb64679ac4913aabd98ed6bb8ad99e015a7fb40d6528756981c6509a64b9d3 |
| B07 reference FD_POLICY512_RAW.npz | b8c4f5278fa58c96c485d6f547acdd927a5cd5153528219ebc1fd6ada4744fa5 |
| Native input LANDMARK512_FD_RAW.npz | d0de6bb598161e85557321a309e9d720cb1c398b722140725e47d8365e3ec68a |

All24 individual JSON/NPZ hashes match the frozen manifest. All12 individual summaries and raw NPZ files were inspected; each NPZ contains the nine expected512-entry scalar/mask arrays. Raw bytes are identical across the three repeats within each eta/policy cell:

| Cell | Raw NPZ SHA256 |
|---|---|
| baseline, eta .01 | 931dedf17b3f136eb7c1e53c432156ad25f13cdc38fbc0aae941aab379502c0b |
| FD50, eta .01 | 1c56e31d8a553eb75d7692d73d20e210b58562de38089031130c930a9c60786e |
| baseline, eta .1 | c62107a8577ce07db066b9bb943372eaca37b3c6b7aeb37fca1abce2fb555676 |
| FD50, eta .1 | b0b6d5cadf70b068a6224617afb6ea9fce0d1c50e5ca8add0dbac695be833e07 |

The preflight chronology remains as recorded in INDEPENDENT_PREFLIGHT.md. The final verifier's manifest addition occurred after operational runs but before audit, changed provenance checks only, and was independently reviewed. It did not change the operational source, design, results, or scientific acceptance thresholds.

## Independently recalculated paired timings

CPU difference means baseline minus FD50. Ratio means baseline divided by FD50. Values below were recalculated from individual run summaries, rather than copied solely from the audit's paired fields.

| eta | repeat | Baseline CPU s | FD50 CPU s | Saved CPU s | Baseline/FD50 |
|---|---:|---:|---:|---:|---:|
| .01 | 0 | 25.225922533 | 14.407429532 | 10.818493001 | 1.750896819 |
| .01 | 1 | 25.890586956 | 13.743639390 | 12.146947566 | 1.883823216 |
| .01 | 2 | 25.542848055 | 13.618117261 | 11.924730794 | 1.875651940 |
| .1 | 0 | 12.860473164 | 7.274237983 | 5.586235181 | 1.767947817 |
| .1 | 1 | 12.021430245 | 6.950906388 | 5.070523857 | 1.729476643 |
| .1 | 2 | 11.722737277 | 7.147658029 | 4.575079248 | 1.640080881 |

Median paired CPU saving is11.924730794s at eta .01 and5.070523857s at eta .1. Median paired CPU ratio is1.8756519396517775 and1.7294766428956256 respectively. Median paired wall saving is11.921154176990967s and5.072040052982629s; median wall ratio is1.8748290218923285 and1.7295643334989137. All six CPU and wall differences are positive. These medians summarize process variability on the same data; they are not population estimates or statistical independent-sample evidence.

The algorithm timer encloses the complete512-step stream loop including FD maintenance, direct-prefix residual arithmetic, every actual queried exact SVD, updates, bookkeeping, and component-timer overhead. It excludes imports, input loading, initial FD/diagnostic allocations, output saving, and external scoring. Each arm computes its own queried exact SVD; no precomputed B07 oracle supplies operational results. This is a fair scoped comparison of the two loops, but should not be described as total startup-to-output application CPU. Both implementations use a costly direct full-prefix reconstruction to evaluate residuals; superiority against optimized implementations is untested.

## Semantic and numerical acceptance

The saved audit reports PASS for12 runs. I independently compared saved masks and scalars to the pinned B07 reference without regenerating Q or any SVD. Query and update masks exactly match each corresponding B07 baseline/strong reference. Baseline and FD50 update masks have zero differing entries for every pair. Their saved incoming-residual arrays are exactly equal, maximum absolute pair difference0.0; each also exactly matches the B07 incoming-residual array. Queried OPT is exactly equal to the saved B07 value at each queried prefix, maximum observed absolute difference0.0. Query/refresh totals recomputed from arrays match every summary; updates imply queries, queried OPT is finite exactly on queried entries and NaN elsewhere.

| eta | Baseline queries after growth | FD queries after growth | Shared refreshes after growth | Queries including25 growth steps | Refreshes including growth |
|---|---:|---:|---:|---|---:|
| .01 | 408 | 222 | 222 | baseline433, FD247 | 247 |
| .1 | 205 | 100 | 100 | baseline230, FD125 | 125 |

All saved gate lower bounds are at most saved OPT plus the frozen energy-scaled tolerance. The maximum positive unadjusted FD-bound excess is8.673617379884035e-17; this is rounding scale. Nonrefresh incoming residuals meet `(1+eta)*OPT+tol`. The maximum positive excess before tolerance is1.938244768357363e-9, which is permitted by the frozen tolerance; do not claim zero error without tolerance. The maximum positive unadjusted gate excess observed is0.0. The existing FD mathematical assumptions and exact-query confirmation remain essential; numerical checks on one prefix do not establish an unconditional floating-point certificate.

No projector matrices or postrefresh losses are saved in B08. Identical refresh endpoints follow from reviewed identical deterministic source/map, common input, and identical update times; this is a source-supported implication, not a separately measured projector equality. Incoming-loss parity and nonrefresh feasibility are directly checked. Exact top-k refresh feasibility follows from the reviewed exact-SVD map with the stated tolerance; a fresh independent recursive algorithm replay was not conducted here. There is no recourse improvement because the refresh/output sequence is unchanged.

## Runtime and reservations

All13 runner receipts (12 operational processes plus the audit) report succeeded and exit0. Receipt input identities agree with frozen driver/helper/design or audit/manifest/reference identities, and output identities agree with the manifest and audit artifact. Receipt times show serial nonoverlapping scientific commands and the prospective interleaved arm order. Total charged command wall is178.79976894601714s; maximum command wall is26.047013826988405s, below120s. Operational peak RSS ranges123192–129420KiB; the audit reports69144KiB, CPU .477911344s and wall .4779377119994024s. No scientific failure was dropped from this13-command set. Separate orchestration incidents remain in ORCHESTRATION_FAILURES.json and are not experimental trials.

Current final runner status independently read: attempts_used13 of32, command elapsed178.79976894601714s of600, reserved_seconds0, status awaiting_decision, remaining deadline450.02914476394653s. Thus the reservation acceptance item is directly observed after the audit. The command executor remains the retained simple runner; these observations do not establish deployment of a full SQLite/ACP supervisor.

## Limits and machine step7 recommendation

This is one already-developed native first512 prefix measured in fresh processes three times per arm. Process isolation and timing repeats improve cost measurement; they are not independent datasets, held-out confirmation, independent scientific replication, or three research discoveries. FD50 was selected using B07 development evidence. This prefix has terminal effective rank64 under the earlier energy cutoff, so the width50 sketch is unusually informative; gains may change when effective rank and stream length grow. Preserve the adverse128 component-cost outcome, the distinct B07 modeled512 result, and this B08 measured-loop result separately.

The next appropriate action is a bounded native5000 resource plan with prospectively frozen intermediate resource calibration, rather than more copies of these12 timings. Do not extrapolate the512 speed ratios or wall linearly to5000. Exact prefix SVD cost, whole-prefix residual cost, and transient memory depend on growing shape; a5000-row complete policy may exceed single-command120s or cumulative600s. Freeze intermediate sizes/checkpoints, resource predictions, stop rules, all charged jobs and source/state identities before running; if continuation is used, validate its state and timing boundaries. Keep the author's literal first1..4999 protocol distinct from engineering calibration and any5000-row comparison. Further512 controls should resolve a concrete remaining implementation/fairness concern or compare a materially different baseline, not repeat settled arithmetic.

Continue literature collision review and certified approximate-refresh derivation in parallel with planning. Existing FD qualification does not supply a novel method, recourse benefit, or a submission-ready result. Coverage of prior work and strong modern baselines remains incomplete; no novelty adjudication or global paper PASS is issued.
