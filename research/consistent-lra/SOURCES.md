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

Rice/Skin native byte identity, source order, labels and UCI metadata/license have now been inspected. Their selected-prefix direct/trace/tail/projector formula identities are independently accepted as engineering evidence, with raw outputs retained. Generator/preprocessing code and relevant proof sections are recorded in SOURCE_JOIN_20261009.md. Landmark exact bytes, duplicate archive identity, official metadata and CC-BY-4.0 obligations are recorded in LANDMARK_SOURCE_ACQUISITION_20261009.md; its bounded mechanical integrity evidence is independently accepted. RANDOM_FAMILY_IDENTITY_20261009.md freezes the irrecoverable exact-figure provenance boundary, including normalization, c and prefix mismatches. The repaired evaluator's 25 software-semantic oracles are independently accepted, but no official author scorer exists. The project strong FD arm now has independently accepted finite source-semantic evidence: it matches a separate `ell`-row compress-before-insert reference on eight analytic prefixes and passes 45 checks, while the author `ell+1` and Liberty `2ell` interfaces are explicitly non-parity. Remaining: qualified strong/simple native performance baselines and FD sensitivity/author diagnostics, completed collision audit, independent new-method pool review/ranking, full G01, numerical costs/results, scientific E04 and fresh confirmation.

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
