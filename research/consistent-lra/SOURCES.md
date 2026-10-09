# Source and evidence ledger

This records actual source reading and source identities, not reproduced experiments.

## Pinned sources

- Paper: https://proceedings.iclr.cc/paper_files/paper/2026/file/b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf
- Official proceedings: https://proceedings.iclr.cc/paper_files/paper/2026/hash/b14d76c7266be21b338527cd25deac45-Abstract-Conference.html
- Author repository commit: `samsonzhou/consistent-LRA@d607c4f6467216c470d1e3b93989d44d5fcdec97`.
- RSI workflow commit: `Yunbo-max/Research_Autopilot@1de12dfed5b84957b29ac5b3a2f04904bf3742bc`, on `autonomous-rsi`.
- RSI autonomous contract blob: `f9860c343cb8db5e43ddaf94441ac390b7c34b10`.

| Author file | Git blob identity | Current read scope |
|---|---|---|
| consistent-lra-landmark.py | 6da3eec62de50b5b37c36b26ae725549e354a738 | Full source read by parent and independent audit worker |
| consistent-fd.py | 294438ac128556f01a2c3d920bdb4f1225dd819f | Full source read by parent and independent audit worker |
| consistent-lra-rice.py | eb8e4e97a9538a14dd6b72d5e271b36c96c05e7c | Full source read by parent and independent audit worker |
| consistent-lra-skin.py | 9581652064a08f5b282cee83286ec7c72ac0fdad | Full source read by parent and independent audit worker |
| Rice_Cammeo_Osmancik.arff | 745655b79f4ca46a3a65a0a8653bd792fa6f7c31 | Actual bytes/hash/source-order inspected; numerical qualification pending |
| Skin_NonSkin.txt | fc58dda2eaf5b1f0d2d8c7924a298cd7d14ba17d | Actual bytes/hash/source-order inspected; numerical qualification pending |
| landmark.mtx | 4c63060bbefcb38e0c705cea1f883d2fb7121f2c | Exact root/ZIP bytes, license and full mechanical integrity independently accepted; no numerical score |
| consistent-lra-random.py | cfe96c16b699a96720e41cc36ab36a25a45b4627 | Full source read; independently accepted exact-figure non-replication boundary: unseeded, unscaled, paper/code c and prefix mismatch |
| consistent-lra-random-fast.py | 4edc0664ac183391af3a761e429c67947a61cc1e | Full source read; different 3000x100/k20 family |

The paper's formal objective, core bounds, Algorithm 4 and empirical Sections 4/G were inspected. A full theorem-by-theorem proof verification has not been performed. Initial source inspection alone did not establish any theorem defect. The later, separate FORMAL_AUDIT_v2.md and its two independent symbolic reviews establish a scoped counterexample to Lemma 2.1; they do not establish a blanket main-theorem failure. The source defects below do not prove that the figures used these exact code paths; figure-generation provenance remains pending.

## Independent source audit

Assignment `/root/baseline_audit` independently fetched all four original files at the immutable author commit and matched the requested blob identities. Its source-only conclusions are retained in BASELINE_AUDIT.md. It ran no experiments or tests. Independence here qualifies the scoped reading task; it is not an independent empirical replication.

Assignment `/root/execution_capability` independently read the pinned RSI entry/contracts and official Work/scheduled-task documentation. It confirmed current in-place Work production may continue and the explicit user CPU choice overrides default host placement within scope. It launched no tasks and established no continuous CPU survival.

## Product execution documentation inspected

- https://learn.chatgpt.com/docs/long-running-work
- https://learn.chatgpt.com/docs/automations

Current Work identity is supplied by the host context. Real automation identity, enabled state, conversation binding and immediate-run request must be recorded separately from scientific execution. Web scheduled tasks do not retain a local worktree between runs; restore durable inputs.

## Outstanding reading and qualification

Rice/Skin native byte identity, source order, labels and UCI metadata/license have now been inspected. Their selected-prefix direct/trace/tail/projector formula identities are independently accepted as engineering evidence, with raw outputs retained. Generator/preprocessing code and relevant proof sections are recorded in SOURCE_JOIN_20261009.md. Landmark exact bytes, duplicate archive identity, official metadata and CC-BY-4.0 obligations are recorded in LANDMARK_SOURCE_ACQUISITION_20261009.md; its bounded mechanical integrity evidence is independently accepted. RANDOM_FAMILY_IDENTITY_20261009.md freezes the irrecoverable exact-figure provenance boundary, including normalization, c and prefix mismatches. The repaired evaluator's 25 software-semantic oracles are independently accepted, but no official author scorer exists. The project strong FD arm now has independently accepted finite source-semantic evidence: it matches a separate `ell`-row compress-before-insert reference on eight analytic prefixes and passes 45 checks, while the author `ell+1` and Liberty `2ell` interfaces are explicitly non-parity. The frozen-author diagnostic separately passes 58 state/projector/shrink/snapshot/rank/zero-row checks after a preserved data-revision-label correction; this qualifies finite source/software semantics only. A separately reviewed Rice Algorithm 4 engineering calibration covers all 3,000 prefixes and fixes an actual low-dimensional cost/RSS observation, but it is one non-official repaired-scorer arm and is not performance evidence. Remaining: qualified strong/simple native performance baselines and FD sensitivity/native author-diagnostic results, completed collision audit, independent new-method pool review/ranking, full G01, numerical costs/results, scientific E04 and fresh confirmation.

## 2026-10-09 retained evidence and primary-source additions

The original source/data copies and their attribution are preserved in originals/ and ORIGINALS_ATTRIBUTION.md. Actual preparation receipt and inputs are preserved under runs/; see PREPARATION_REVIEW_20261009.md. Source-integrity output SHA256 b5d87432c73b0500cd0e0909aed9e6b50be130c57d39ffd7e6cf1ae9d9bbf0b9.

Relevant target proofs read: main Algorithm4 argument, Appendix E.1/E.2 and empirical Appendix G. Lemma2.1 has a separately verified finite real-matrix counterexample; other theorem dependencies remain pending. ArXiv https://arxiv.org/abs/2603.02148 showed v1 (2 March 2026) in the inspected submission history; its assertion is Lemma2.3.

Canonical FD source read: edoliberty/frequent-directions@691df9edb2ffbc2fdddc2cec3b703a3f1e438d4d, frequentDirections.py blob4bb3500cbea9c81c21cbeea5cd5db60ac4006d3d. Independent source-semantic qualification confirms its `2ell` buffer/leading-`ell` `get()` interface is intentionally not prefix-state parity with either the author `ell+1` variant or the project `ell`-row strong arm.

New primary mathematical source locators, actual reading scopes and unresolved equivalence/novelty questions are in NOVELTY_PRELIMINARY_20261009.md. No source full-text hash is asserted where only web full-text retrieval was available. Repeated target proof in Accelerating Scientific Research with Gemini was read at Theorem7.33 only.

Later formal dependency work is retained in FORMAL_AUDIT_v3_EXTENSION.md, CONDITION_SCOPE_SUPPLEMENT_DRAFT.md and FORMAL_EXTENSION_REVIEWS.md. The specific rank-uniform exact-optimal dynamic Theorem2.2 is contradicted; approximate insertion-only Theorem1.2 is not thereby refuted, although its displayed lemma-dependent proof needs repair. Algorithm4's energy argument is separate. Additional primary-source locators, access caveats and search observations are in LITERATURE_READ_20261009_2.md.

The integer-density continuation and both independent verdicts are retained in
FORMAL_AUDIT_v4_INTEGER_DENSITY_DRAFT.md and FORMAL_AUDIT_v4_REVIEW.md.  It
establishes a separately integerized arbitrary-rank family, with no polynomial
integer-magnitude or bit-length claim and no implication for Theorem1.3.

The exact identity with the Anderson integral and the bounded primary-source
collision search are in LITERATURE_EQUIVALENCE_20261009_3.md.  The underlying
rank-one/Cauchy/projector mechanism and logarithmic-growth phenomenon are prior
art; exact priority for the application to the 2026 paper remains inconclusive.

Braverman et al., arXiv:1805.03765v6 (11 April 2023), and the target official
PDF were jointly checked for the online PCP dependency.  The corrected record
and independent review are in SAMPLING_SOURCE_QUALIFICATION_20261009.md and
SAMPLING_SOURCE_QUALIFICATION_REVIEW.md.  The quadratic-in-rank fallback is
conditional on a joint high-probability event for the theoretical append-only
sampler; executable parity and native scoring remain pending.

## Explicit restart and plugin selection — 2026-10-09

The owner selected Research Autopilot Auto private plugin version 0.2.0-autonomous.2
and then instructed "你就重新开始跑吧？". This explicitly reopens the same project
with a new eight-hour wall window (2026-10-09T09:15:43Z through 2026-10-09T17:15:43Z); all previous
usage, failures, task identities, limits and reviews remain authoritative. Read
[RESTART_AUTHORIZATION_20261009.md](RESTART_AUTHORIZATION_20261009.md) and the active fields of BACKGROUND_TASK.json. This section
supersedes old deadline and workflow-source requirements only. Use installed
plugin c23/research-autopilot and same-package modules; historical vendor/rsi
at 1de12dfed5b84957b29ac5b3a2f04904bf3742bc remains pinned for prior receipts
and unchanged runtime/checker execution. No shared skill or runtime upgrade
is authorized. Reuse background task 6ac82bb085c081919fa92002384b073b and branch scope; no second writer.

## Window02 targeted constructive-integer priority audit

Assignment114 atfa18157ed860dd351f705b31cd80d934785c63c0 found earlier finite residue/Cauchy formulas in Hentschel–Ullmo–Baranger2005 (cond-mat/0503330v1, §II B eq15–18). Root separately opened arXiv/PDF and verified those sections. Other targeted primary trace/physics/bit-complexity reads and all16queries are retained in INTEGER_PRIORITY_TARGETED_AUDIT_WINDOW02.md. The reader authored v7; no independent novelty adjudication or complete collision snapshot is supplied. Exact conditioned integer family priority remains inconclusive; full search response captures not durable. No new scientific experiment or paper pass.

## Window02 complete integer certificate and consequential proof dependencies

Actual154 independently verifies complete61 roots/732 decisions for the fixed integer witness, Rlower2290438555/134217728>8; raw/receipts and unchanged independent replay are linked in INTEGER_COUNTEREXAMPLE_CERTIFICATE_WINDOW02.md. It does not supply native benchmark scoring, novelty or paper eligibility. Actual139 primary collision/scope review keeps known secular/Cauchy mechanisms separate from unresolved conjunction priority.

Actual150 read full related conference Appendix E/F proofs pp19–25 and original Braverman arXiv1805.03765v6 Section3.1/Theorem3.1 proof (2023-04-11). Exact known freshSVD/append-only simultaneous-prefix PCP fallback is qualified at O(k^2 epsilon^-2 log(n) log^2 max(2,kappa)); rank-linear Theorem1.2 displayed proof remains unrepaired. Algorithm4 supports additive Theorem1.1, independently ofLemma2.1. Theorem1.3 has a separate chain with unresolved HEAVY loss/tail-capture and integer reweighting/sampling premises, without theorem-falsity verdict. Full locators, mathematical derivations and actual retrieval-object capture hashes are in APPROXIMATE_PROOF_DEPENDENCY_REVIEW_WINDOW02.md; those hashes are explicitly not original PDF-byte hashes. Full all-theorem verification remains incomplete.

Assignments172--174 revisited the reweighted-integer premise against the official ICLR paper and Braverman et al. Algorithm5/Theorem3.1. The sampled matrix is generally not integer, contrary to one sentence in the Theorem1.3 proof, but it has exact form `M=D A_S` for an integer selected-row submatrix and `D_ii=p_i^(-1/2)>=1`. An initial arbitrary-real counterexample was independently rejected because it ignored this structure. The corrected fixed candidate, SHA256 `be08ca12844b2dbc71e0fa1e78bd86ac59f6a0c8184ddca161e17b5896b18d45`, was independently accepted: Cauchy--Binet gives `prod_j sigma_j(M)^2>=1`, preserving AppendixF.2's spectral floor conditional on the separately asserted sampled-entry magnitude bound. This is a proof-detail repair, not a theorem defect, novelty result, or execution gate. Exact bit representation remains unanalysed; HEAVY aggregate accounting remains open. See REWEIGHTED_INTEGER_PREMISE_AUDIT_MAIN.md and REWEIGHTED_INTEGER_PREMISE_REVIEW_MAIN.md.

Assignments175--176 then audited the remaining HEAVY aggregate dependency against the official Algorithm2, AppendixF.1 and Lemmas3.7/3.9/3.10. The fixed candidate SHA256 `92ec4600c73754815a5b652f37c9871da3602e3481c605faf17db25d24d14ac5` is independently accepted: for every square `k>=9`, a reachable real-row state has one non-reset HEAVY arrival with projector recourse greater than `sqrt(k)`, invalidating the domain-free `r=1` extension of Lemma3.7. The exact residue/eigenvector constants, triggers, and reachability counter behavior were rederived. This does not cover literal integer rows or the sampled `D A_S` class, does not repeat the event, and does not establish Theorem1.3 false. See HEAVY_SINGLE_ARRIVAL_AGGREGATE_AUDIT_MAIN_DRAFT.md and HEAVY_SINGLE_ARRIVAL_AGGREGATE_REVIEW_MAIN.md.

Assignments177--178 independently transfer the accepted event to the algebraic class `M=D A_S` by choosing a rational final row inside the strict open predicate neighborhood and scaling the finite whole stream. The candidate SHA256 `6f2468aea1245c7a13d25446add1f0b5a0db18b5c7510c6dc2e771b3325eb7b8` and review SHA256 `e73c0665d859b1d0c0a5038fc5d7368d1d7987d84a6723fbdf6838d4761cf4f0` are accepted. `A_S` is integer and `D>=I`, but actual online ridge-leverage-sampler reachability, bounded representation, literal integer delivery rows, repeated events and theorem falsity remain unproved. See HEAVY_DAS_TRANSFER_MAIN_DRAFT.md and HEAVY_DAS_TRANSFER_REVIEW_MAIN.md.

## Main consolidated primary and mathematical audit,2026-10-09

Main authorization/reconciliation preserves old immutable runtime/receipts and bothcontrolsource snapshots. Actual161 primarybackwardchain adds Aleiner–Matveev cond-mat/9712020v1(1997-12-02), Makarov–Seelmann1007.1575v1(2010-07-09), Gladwell–Jones–Willms1402.5890(2014-02-21). FullURLs/equations/hypothesisandmetriccomparison/searchbudget in INTEGER_JOINT_PRIORITY_REVIEW_MAIN.md; classicalmechanismcollision accepted, fulljointpriorityinconclusive. Root also openedtheseprimarypages directly; no absence-of-search noveltypass.

OfficialconferenceAlgorithm2/F.1recourse/branches reread for actual162/163; independent163 accepts35rowinteger numericalF1counterexample, withpersistentstate/epsilon0.3/factorrepairlimits. Actual164 rankfamily is separatelyfrozen;165 pending, notacceptedby163. Thesearesymbolicexistingpaperaudits,notnativebenchmarkresults.

Actual165rankfamilystate/recourse review and actual166independentstrictnessreviewnowaccepted,primaryofficialAlgorithm2/F.1/Theorem1.3epsilonchecked. V1preserved;v2recordsreviewer-provedgcdargumentandoneclarification. Internalclaim-evidence statusretainsaggregate/existence/epsilon-dependent/priority/nativegaps. NoPDF-bytehash,newmethod,empiricalscoreorpublicationgateclaimed.

## Experiment readiness correction, 2026-10-09

Assignment181 restored main4ab8e122fcaed61b6f1ac9ec4d8e899989402036 and legacy7286e6d5b301f01ebda45d6fa1387afd9d383906. The exact inspected source/review hashes are in EXPERIMENT_READINESS_SOURCE_MANIFEST_20261009.json, including the captured current installed native-evaluation module. Existing accepted reviews are reused; historical raw matrices were not rerun or newly accepted. The concrete project-local independent-paper-metric/runtime alternative is design-only in EXPERIMENT_READINESS_CORRECTION_20261009.md; assignment182 independently accepts the final exact-byte proposal as design-only; its review preserves both inventory corrections. No correct official interface was found in the already audited pinned release; whole-tree search was not repeated. No independent contract or oracle implementation, scientific launch or gate pass is claimed.
