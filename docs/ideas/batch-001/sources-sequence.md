# Primary-source packet: sequential SFT operators

Retrieval cutoff: 2026-10-08 UTC. Read-only source retrieval for frozen I12, I13, I14, and I16; this packet does not adjudicate novelty or rank ideas. Scientific code, training, evaluation, model downloads, and dataset downloads were not executed. GitHub checks below are static reads of author-linked repositories. Source refs are this retriever's refs; the root should open the URLs itself before citing them to the user.

## I12: noncommuting gradients and bracket correction

**John Sweeney, The Geometry of Sequential Learning: Lie-Bracket Prediction of Transfer Order, arXiv:2606.24993v1, 23 June 2026.** [Full text](https://arxiv.org/html/2606.24993v1), [PDF](https://arxiv.org/pdf/2606.24993v1). Refs: turn71view0, turn73view1–3, turn131view1; abstract turn69search0. Full relevant derivations read.

| Locator | Inspected mathematical element |
|---|---|
| §2.1–2.2, Lemma 2.1, Eqs. 7–8; App. A.1 | Two memoryless GD steps give θ_AB−θ_BA=η²b_AB+O(η³), with b_AB=H_Bg_A−H_Ag_B. Assumes local smoothness and sufficiently small steps. |
| Remark 2.2 | A fixed trainable subspace uses projected gradients and Hessians. |
| §2.3, Prop. 2.3, Eq. 10; App. A.2 | Target loss difference is η²〈g_E,b_AB〉+O(η³). |
| §2.4, Eqs. 14–17 | Evaluates target gradient at the shared first-order drift reference. |
| App. E.8, Eqs. 28–29 | θ_ref=θ₀−η(g_A+g_B); θ_ctrl=θ_ref−0.5 sign(σ̂)η²b_AB. The target expansion at the reference has O(η⁴) remainder. Reported correction improves the drift point in 179/204 cases and beats both sequential endpoints in 95/204. |

The same bracket therefore appears as both an ordering predictor and an applied correction direction. §4.5 expressly limits the derivation to memoryless dynamics; AdamW would require augmented optimizer state. The inspected treatment makes source gradients/HVPs available together. A protocol in which source B is unknown until later arrival is not established by the inspected derivations.

**Author code status:** an official OpenReview LinkToCode result points to [Sideplane/GradientUpdateFields](https://github.com/Sideplane/GradientUpdateFields) (turn112search1, forum KL0eu92H3K, note PGfAOsjWn1). The OpenReview page subsequently hit a browser challenge; GitHub API/root fetch returned **404 Not Found**. No commit, functions, native scorer, or experiment config could be inspected. Do not count this as verified executable author code.

**Benoît Dherin, Implicit biases in multitask and continual learning from a backward error analysis perspective, arXiv:2311.00235v1, 1 November 2023.** [Abstract](https://arxiv.org/abs/2311.00235v1), [full PDF](https://arxiv.org/pdf/2311.00235v1). Refs: turn135view0, turn71view2, turn73view4.

§4, pp. 3–4: Definition 4.1/Eq. 7 defines the Lie bracket. Theorem 4.2/Eq. 9 derives the modified ODE −∇L̃+(h/2)[∇L₁,∇L₂]+O(h²) corresponding to sequential Euler updates; Eqs. 10–15 give the Taylor proof. Eq. 8 includes separate gradient-norm regularizers. Remark 4.3 conjectures a connection between abrupt distribution changes, large brackets, and catastrophic forgetting; it does not prove a retained-capability certificate. Author implementation was not located/inspected.

**Nichol, Achiam, Schulman, On First-Order Meta-Learning Algorithms, arXiv:1803.02999v3, 22 October 2018.** [Abstract](https://arxiv.org/abs/1803.02999v3), [PDF](https://arxiv.org/pdf/1803.02999v3). Refs: turn135view1, turn71view3, turn73view5.

§5.1, pp. 5–7, Eqs. 13–16: expands later minibatch gradients as g_i=ḡ_i−αH̄_iΣ_{j<i}ḡ_j+O(α²), then analyzes Reptile/FOMAML/MAML alignment terms. This is a same-task meta-learning operator neighbor. The author repository [openai/supervised-reptile](https://github.com/openai/supervised-reptile) was located (turn62search30), but no pinned code was read in this packet.

## I14: prefix measures, importance weighting, and OPD

**Xie et al., On the Position Bias of On-Policy Distillation, arXiv:2606.22600v3, 26 June 2026.** [Abstract](https://arxiv.org/abs/2606.22600), [full text](https://arxiv.org/html/2606.22600v3). Refs: turn104view0, turn106view0, turn131view0, turn134view0. Full relevant appendix read.

| Locator | Inspected operator |
|---|---|
| §3.2, Proposition 1, Eq. 8; App. A.1 | Common-support, active trust-region optimum q*=π_student(π_teacher/π_student)^α/Z_α, 0<α<1. |
| App. A.2, Eqs. 37–42 | Exact trajectory change of measure uses the full powered sequence ratio and its normalizer. |
| App. A.2, Eqs. 43–47 | Factorizes prefix and suffix ratios; prefix r_t=∏_{k<t}π_teacher(y_k\|h_k)/π_student(y_k\|h_k). The appendix calls replacement by the causal prefix component a token-level surrogate. |
| §4.1, Eqs. 11–13 | Detached normalized prefix weighting multiplies the OPD advantage. |
| §4.2, Eqs. 14–17 | Replaces unstable raw ratios with cumulative absolute log-probability discrepancies, within-sample normalization, and interpolation with OPD; default γ=0.5. |

This is a teacher/student trust-region construction. Its exact trajectory identity and its causal surrogate must be kept distinct from a fixed-original-base forward-KL retention objective. The rendered main-text α notation and Eq. 42 left-hand expression require independent equation verification; the appendix and context were used to record the intended factorization.

**Pinned actual author code:** [YannX1e/Importance-Weighted-On-Policy-Distillation](https://github.com/YannX1e/Importance-Weighted-On-Policy-Distillation), commit **b1320d3b446ae4ecfb8cb1c0f4ec7fcea9d3d878**, 24 June 2026.

| File, blob, locator | Static read |
|---|---|
| [verl/verl/workers/actor/dp_actor.py](https://github.com/YannX1e/Importance-Weighted-On-Policy-Distillation/blob/b1320d3b446ae4ecfb8cb1c0f4ec7fcea9d3d878/verl/verl/workers/actor/dp_actor.py), e3016e6c229b8b529444eb66cac20da98ad0cbd3; update_policy, lines 533–594 | IW branch forms d_t=abs(ref_log_prob−old_log_prob), previous-prefix cumulative mass / total sampled-sequence mass, then w_t=1+(weight_max−1)(1−F_prev). It multiplies advantages by w_t. Default weight_max=1.5. This branch does not compute a product of exact prefix likelihood ratios. |
| [verl/verl/trainer/ppo/core_algos.py](https://github.com/YannX1e/Importance-Weighted-On-Policy-Distillation/blob/b1320d3b446ae4ecfb8cb1c0f4ec7fcea9d3d878/verl/verl/trainer/ppo/core_algos.py), cb09503f03dff008f1da026b901463bb2c9d1a53 | Actual policy-loss function registry and PPO loss implementations read; dp_actor forwards weighted advantages to the selected policy loss, lines 775–789. |
| [run_qwen3-30b-a3b-instruct-opd_4b_iw_opd.sh](https://github.com/YannX1e/Importance-Weighted-On-Policy-Distillation/blob/b1320d3b446ae4ecfb8cb1c0f4ec7fcea9d3d878/verl/examples/opd/run_qwen3-30b-a3b-instruct-opd_4b_iw_opd.sh), 488ae9a66350bbe618032d7e19cd9036a1c77952 | Student Qwen3-4B; teacher Qwen3-30B-A3B-Instruct-2507; DeepMath filtered level6; AIME24/25 validation; γ=.5 equivalent weight_max=1.5; max response 16384; 8 GPUs/node ×4 nodes; TP4; rollout IS token threshold5; naive reward manager. |

Native math/code evaluation directories are present, but scorers, data hashes, train/test contamination, and numerical reproduction were not verified. This supplied config establishes no feasibility on the user's one 22GB GPU.

**Gu et al., MiniLLM: On-Policy Distillation of Large Language Models, arXiv:2306.08543v6, 31 January 2026.** [Full text](https://arxiv.org/html/2306.08543v6), ref turn80view0.

§2.1/Eq. 1 uses sequence reverse KL. §2.2/Eqs. 2–3 separates full-vocabulary single-step loss and future reward. Teacher-mixture Eq. 4 changes sampling; Eq. 5 introduces cumulative products of student/mixture ratios, then explicitly approximates them with a single-token ratio to reduce variance. Algorithm 1 uses PPO clipping and a pretraining-language-model loss.

**Pinned code:** author-linked microsoft/LMOps, minillm subtree commit **48fca1acc61ffa20ebb7c31c74a1d8e33499b476**, 13 November 2025. [sampler.py](https://github.com/microsoft/LMOps/blob/48fca1acc61ffa20ebb7c31c74a1d8e33499b476/minillm/minillm/sampler.py), blob 509a3f2c262cb9775a42748da735ad49bac4c1a0: Sampler.run_sample, lines 107–119 uses exp(student logprob−mixture logprob), pointwise. [losses.py](https://github.com/microsoft/LMOps/blob/48fca1acc61ffa20ebb7c31c74a1d8e33499b476/minillm/minillm/losses.py), blob f3325c80cf33f0a55805111f56376bf27df06094: Loss._pg_loss lines 58–96 combines w with PPO ratios/clipping; Loss.ppo_loss lines 126–175 passes w to PG and adds optional _reg_loss. The inspected _reg_loss does not multiply by w. arguments.py default cliprange=.2. No scientific execution or scorer qualification.

**Agarwal et al., On-policy Distillation of Language Models: Learning from Self-Generated Mistakes, arXiv:2306.13649v3, 17 January 2024, ICLR 2024.** [Full text](https://arxiv.org/html/2306.13649v3), ref turn67view3. §3/Eqs. 2–4: per-token divergence over student-sampled prefixes; sampling distribution is stop-gradient. GKD mixes fixed-data and on-policy sequences. Author code not verified; third-party implementations were not treated as author code.

**Fu et al., Revisiting On-Policy Distillation: Empirical Failure Modes and Simple Fixes, arXiv:2603.25562v1.** [Full text](https://arxiv.org/html/2603.25562v1), refs turn106view2, turn108view5. §3.1 contrasts the sequence policy gradient, including future-token returns, with token-local semi-gradients; §3.2 studies atypical prefixes and special tokens. This addresses gradient bias rather than fixed-base retention. Author-linked hhh675597/revisiting_opd was located but not pinned/read.

**Cui et al., Gains and Collapse in On-Policy Distillation: A Reinforcement Learning Perspective, arXiv:2610.03185v1, 2 October 2026.** [Abstract](https://arxiv.org/abs/2610.03185v1), [full text](https://arxiv.org/html/2610.03185v1), refs turn130view1, turn106view3, turn108view3–4. Within cutoff. §2.1/Eq. 1 freezes the rollout-prefix distribution for conditional reverse KL; §2.2 gives implicit-reward interpretation and sampled/PPO updates. Author-linked [HancCui/opd_hacking](https://github.com/HancCui/opd_hacking) not pinned/read.

## I13: cumulative/global retention neighbors and bounded gap

**Friedman and Meir, PAC-Bayes bounds for cumulative loss in Continual Learning, ICLR 2026.** [Official OpenReview](https://openreview.net/forum?id=hWw269fPov), ref turn112search0; published 26 January 2026, modified 10 April. [Official six-page slides](https://iclr.cc/media/iclr-2026/Slides/10008051.pdf), ref turn130view2. Slides read; full paper PDF repeatedly hit browser challenge.

Slides pp. 4–6 define sequential posteriors and cumulative loss over each arriving task, with consecutive **parameter-posterior** KL complexity terms, i.i.d. samples within each task, and inaccessible historic data. This is not the same object as cumulative predictive drift on a fixed set of still-valid original anchors. Full theorem conditions/proof, code, data, and scorer remain unresolved. Do not substitute the slide formula for the inaccessible full theorem.

**Sason and Verdú, f-Divergence Inequalities, arXiv:1508.00335v7, 4 December 2016.** [Full PDF](https://arxiv.org/pdf/1508.00335v7), refs turn104view2, turn134view2, turn116view2–3. Eq. 16, p. 3, gives squared-Hellinger-divergence ≤ KL under its convention/log units; Eq. 17 generalizes via Rényi divergence. The Hellinger triangle-based accumulated path formula and stage-budget optimization were not located as a specific continual-learning result in this retrieval. Their derivation should be independently checked, with normalization/log-base conventions explicit. This is a bounded retrieval gap, not evidence of novelty.

**Chaudhry et al., Riemannian Walk for Incremental Learning, arXiv:1801.10112v3, 14 August 2018, ECCV.** [Abstract](https://arxiv.org/abs/1801.10112v3), [PDF](https://arxiv.org/pdf/1801.10112v3), refs turn135view2, turn80view2, turn86view1. §2.3/Eqs. 1–2: local predictive KL ≈½δᵀFδ; §4.1 combines Fisher importance and accumulated loss-improvement/path information. App. A.1 distinguishes true and empirical Fisher. These local path/importance objects do not supply an inspected fixed-anchor global certificate. Author A-GEM repository below contains statically inspected RWalk branches: create_pathint_ops lines 1008–1072 and create_fisher_ops 1074–1120.

**Ferenc Huszár, Note on quadratic penalties in elastic weight consolidation, PNAS 115(11):E2496–E2497, 20 February 2018; arXiv:1712.03847 alias On Quadratic Penalties in Elastic Weight Consolidation.** [Primary full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC5856534/), refs turn87view3, turn83search0. Corrects separate old-optimum-centered penalties to a recursive latest-optimum-centered accumulated curvature penalty; explains double counting from the third task. This concerns posterior/quadratic approximation rather than fixed predictive anchors. Code not verified.

## I16 and standard constraint/sketch neighbors

| Primary source and exact locator | Inspected element / limitation |
|---|---|
| Lopez-Paz and Ranzato, Gradient Episodic Memory for Continual Learning, [arXiv:1706.08840v6](https://arxiv.org/pdf/1706.08840v6), 13 September 2022; §3, pp. 3–4, Eqs. 6–8; turn94view0 | Episodic old-loss inequalities, first-order gradient halfspaces, and minimum-change QP projection. Allows beneficial old-loss reductions. Memory representativeness and local linearization are required; it is not an exact per-example correctness-margin certificate. |
| Chaudhry et al., Efficient Lifelong Learning with A-GEM, [arXiv:1812.00420v2](https://arxiv.org/pdf/1812.00420v2), 9 January 2019; §4, Eqs. 10–11, App. C; turn94view1, turn98view2, turn135view3 | Average-old-memory gradient halfspace and closed-form projection g−(gᵀg_ref/||g_ref||²)g_ref when dot product is negative. |
| Farajtabar et al., Orthogonal Gradient Descent for Continual Learning, [AISTATS 2020 full paper](https://proceedings.mlr.press/v108/farajtabar20a/farajtabar20a.pdf); §3, pp. 2–4, Eqs. 7–9; turn94view2, turn98view1 | Projects away stored old-logit Jacobian directions; correct-label-only approximation and first-order logit preservation. Local limitation stated; original author code not verified. |
| Wolczyk et al., Continual Learning with Guarantees via Weight Interval Constraints, [ICML 2022 full paper](https://proceedings.mlr.press/v162/wolczyk22a/wolczyk22a.pdf); §3, Thms. 3.1–3.2, §4, §6; turn80view3, turn96view0–1, turn98view0 | Interval output bounds give worst-case cross-entropy/correctness constraints over nested weight regions. Certificates cover training examples and conditional model bounds; test shift and unforeseen normalization changes are not covered. Author gmum/InterContiNet linked but code not read. |
| Heckel, Provable Continual Learning via Sketched Jacobian Approximations, [AISTATS 2022 full paper](https://proceedings.mlr.press/v151/heckel22a/heckel22a.pdf); §3/Eq. 2 and §5/Thm. 1; turn94view3, turn96view4, turn134view1 | Stores K_T=S_TJ_T with Gaussian S entries N(0,1/s), adds accumulated old quadratic forms around latest solution; sketch approximation guarantees under linear/wide-network assumptions. Memory p(1+Ks). |

**Pinned standard author code inspected:**

- [facebookresearch/GradientEpisodicMemory/model/gem.py](https://github.com/facebookresearch/GradientEpisodicMemory/blob/34c6b8e9a0607db7567301c48b727430d20bee7e/model/gem.py), commit **34c6b8e9a0607db7567301c48b727430d20bee7e**, 22 October 2018. `Net.observe` recalculates old memory CE gradients and projects negative dot products; `project2cone2` uses quadprog. Its margin parameter is a dual-QP parameter, not the frozen I16 correctness margin. Native scorer unverified.
- [facebookresearch/agem/model/model.py](https://github.com/facebookresearch/agem/blob/45421499483b28935491251e9e821c55e8b3c089/model/model.py), commit **45421499483b28935491251e9e821c55e8b3c089**, 28 February 2019, blob **ccb3e966f71e6b20b923781697453876b78b4048**. `Model.create_stochastic_gem_ops`, lines 1147–1190, stores reference gradients and uses conditional projection. Includes RWalk path/Fisher operations noted above. Native scoring/data not verified.
- [MLI-lab/regularization_based_continual_learning/include/algs.py](https://github.com/MLI-lab/regularization_based_continual_learning/blob/808f2131add659c8c96fb8318e480df74e19f936/include/algs.py), commit **808f2131add659c8c96fb8318e480df74e19f936**, 8 February 2022, blob **f09b964809ca07a710f4d36661bc673c13c097a1**. Class `EWCplusplus` lines 154–213 stores per-task random sketched logit gradients: `compute_task_data` samples randn(s)/sqrt(s), accumulates outer products; `loss` sums squared sketch-times-parameter-displacement norms. Latest center updated in `update`. Paper's RSJ operator therefore has an actual author implementation under a different class name. MNIST notebooks present; native scorer and numerical behavior unverified.

No exact inspected source for the frozen base-correct pairwise margin inequality plus rigorously bounded Taylor remainder was located in this pass. GEM/A-GEM, OGD, and interval certificates are distinct neighboring operators; this bounded gap must remain open. Standard optimal-design coverage was not completed.

## Audit boundary

Searches covered sequential-gradient/Lie-bracket/backward-error aliases; Reptile/MAML alignment; OPD/GKD/MiniLLM prefix and importance-weight aliases; continual KL/Hellinger/cumulative PAC-Bayes; Fisher/EWC/RWalk; GEM/A-GEM/OGD; correctness/interval constraints; and RSJ memory sketches. Full-paper reading, version metadata, and pinned static code are distinguished above. The 2026 PAC-Bayes paper's full proof and the Lie-bracket author repository remain inaccessible. No source absence claim, completed collision audit, novelty conclusion, benchmark proposal, or hardware feasibility result is asserted.
