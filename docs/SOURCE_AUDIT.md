# Initial joined source audit

Cutoff and access date: 2026-10-08. This is a scoped startup investigation, not a saturation certificate, reproduction report, or novelty verdict.

## Primary-paper inventory

| Work and version | Scientific sections inspected | What is established at this stage | Remaining source obligation |
| --- | --- | --- | --- |
| [IDEAL, arXiv 2505.12762v1](https://arxiv.org/html/2505.12762v1) | Sections 1–4, including the bilevel objective, inverse-Hessian approximation, iteration, and benchmark setup | The author specification already treats multi-domain SFT mixture adjustment as an influence-based optimization problem | Reconcile the arXiv specification with the final venue version; inspect the remaining K-FAC modules and actual training/evaluation pipeline |
| [mSFT, arXiv 2603.21606v6](https://arxiv.org/html/2603.21606v6) | Sections 3.2 and 4.1; method, comparator setup, main table; Appendix FLOPs/checkpoint descriptions | The authors report heterogeneous overfitting times and use dataset exclusion plus checkpoint rollback | Independently qualify splits, selection, scorer fidelity, optimizer restart semantics, and costs; no project reproduction exists |
| [DynamixSFT, ACL Findings 2026](https://aclanthology.org/2026.findings-acl.1972/) | Official publication metadata and abstract | Bandit-based mixture updates with a prior and one-step look-ahead are directly relevant | Full PDF algorithm, code, task inventory, and total search overhead remain unread/unqualified |
| [OP-Mix, arXiv 2605.15220v1](https://arxiv.org/html/2605.15220v1) | Problem definition, mixture objective, and on-policy adapter-interpolation search description | Low-rank adapter interpolation is an existing mixture-search mechanism spanning training stages | Inspect the full continual instruction-tuning controller, released input shards, regression/search, and evaluator |
| [SoFT, arXiv 2609.32493v1](https://arxiv.org/html/2609.32493v1) | Sections 2–4 and reasoning-results table | Minimum-KL soft targets and domain-level initial-gradient budgets address acquisition versus retention | No corresponding author-code link was verified in the inspected paper page; full release/input/scorer access remains to be resolved |
| [Data Mixing Optimization for SFT, arXiv 2508.11953v1](https://arxiv.org/html/2508.11953v1) | Dataset preparation and training/resource appendix | Existing SFT mixture research spans general instruction, math, code, and medical data, with small and large models | Full objective, estimator, implementation, and comparison fidelity remain to be inspected |

The publication dates and source versions must remain separate. A new search snippet does not establish a read or a reproduced result.

## Actual author implementation reads

### mSFT

Repository: [reiss-koh/msft](https://github.com/reiss-koh/msft). Observed main commit: `4cf68d9004ef0d4dae02edc854183b70b258f167`.

| Inspected file | Blob identity | Consequence |
| --- | --- | --- |
| README.md | 54d7f8524087fad685f1f5323b5a6f8067900d28 | Default recipe assumes four RTX 3090s |
| sft/train_eval.py | 6cb54a8e0ce9f2c7e03b03ddbd74e8512011ff4b | Inspecting resumed weights and newly constructed optimizer/scheduler identifies stage-state semantics as a comparison obligation |
| sft/modules/updaters/checkpoint_updater.py | 906646fda5a260631edc80772f6bbc493739d5f3 | Per-category and global best-checkpoint bookkeeping affects selection and storage |
| sft/utils/vllm_evaluator.py | d149c785f854e395160765a9f2a1acdc920553fc | FSDP export plus a vLLM subprocess needs a hardware-specific compatibility review |
| sft/utils/utils_test.py | 89f69d69d4492d931295998750cf58b91a65fba9 | Shared numeric/text answer parsing and pooled accuracy need comparison with the native task contracts |

Source inspection is not a finding that a comparator is invalid. Qualify the exact recipe, and preserve a paper-faithful reproduction separately from a harmonized comparison if they differ.

The repository tree was also inspected. Released mixture files for 5, 10, and 15 categories exist, but their full data bytes, IDs, preprocessing, and contamination status were **not** read or qualified in this round.

### IDEAL

Repository: [ming-bot/IDEAL](https://github.com/ming-bot/IDEAL). Observed main commit: `9438d0cfbb556d385437ce0bbab4e9a3b5ad9078`.

- `main.py`, blob `fffac4f5d810f41b26d67d6572ef3930ce12e41a`: inspected the DDP setup, train/reference gradient collection, K-FAC entry, and influence output.
- `reweighting.py`, blob `f20dc1248f22780555747843e15e706ec33a881b`: inspected the example influence values, scaling, resampling, and local paths.
- The latter is an example script, not a complete parameter-free comparator. A faithful adaptation must use measured influence values and pin training/scoring inputs. Whether total dataset volume is preserved must be declared and matched.

### OP-Mix

Repository: [michahu/on-policy-mix](https://github.com/michahu/on-policy-mix). Observed main commit: `0b4469c2457ae5e5e21dc13aaa2aa9394d5f3867`.

- `src/merge.py`, blob `8efafb6e0b23b1e2b5db56ef0eaaa6d0c1c5d8f0`: inspected interpolation, CPU copies, and model residency.
- `pipeline/merge_lora.py`, blob `bfac0c36268625de6fef56dba26e14267e8c9f6e`: inspected LoRA merge/scaling entry.
- `data-mixes/tulu_flan_v2.txt`, blob `51e468c9a36bcb5d456757bdc1e71e29d874759e`: inspected paths to preprocessed instruction-data shards.
- Tree inspection located `pipeline/continual_opm.py`, `pipeline/continual_opm_standalone.py`, and regression/OLMix components. Their full implementation was not read. A file being present does not establish task completeness or accessibility of its shards.

## Native benchmark and data reads

### Tulu 3 mixture

Publisher card: [allenai/tulu-3-sft-mixture](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture).

The published card and visible released examples were read. Fields include `id`, `messages`, and `source`. The card identifies varied general, mathematical, code, instruction, and other inputs, with component-specific terms. The live card and viewer show slightly different row totals; final sizing must use an immutable downloaded revision and a verified manifest, rather than copy a rounded number.

A source label is not necessarily a disjoint capability label. Sample-level IDs and cross-source duplicate/contamination checks remain necessary. No dataset was downloaded for scientific execution.

### GSM8K and IFEval

Implementation: [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness), observed main commit `d6de81643928d653435c431bae19945d41d32520`.

| File read | Blob SHA | Native contract visible in the source |
| --- | --- | --- |
| lm_eval/tasks/gsm8k/gsm8k.yaml | 9266ab1f80af13b228f55f474442eb8db34f8a13 | openai/gsm8k, main; train few-shot data and test evaluation; greedy generation; defined strict/flexible answer filters and exact match |
| lm_eval/tasks/ifeval/ifeval.yaml | 508a63a9452874109cd949f5d5a5e00ad5f66b36 | google/IFEval; published split named train is the evaluation split; zero-shot generation; four native accuracy variants |
| lm_eval/tasks/ifeval/utils.py | 985e8d5ae578c484267c7c2d90ee7c896028941f | Strict/loose instruction checks; prompt accuracy differs from the flattened instruction denominator |

No scoring command was executed. The implementation copies/ports instruction checks; verify its lineage and exact selected revision against the original release before scientific acceptance. IFEval's evaluation records must not be used as SFT data or repeatedly tuned against as a final test.

The mSFT paper also names CommonsenseQA, OpenBookQA, AQUA-RAT, SciQ, ARC-Easy, HellaSwag, Winogrande, BoolQ, MedMCQA, and GSM8K. Only their inventory and author evaluation code were inspected here. Their original data/scorers are not all qualified.

Code-generation scoring such as EvalPlus, MBPP+, and HumanEval+ remains an unresolved native-source read, not a selected or complete comparison.

## Resource/source feasibility

- User-confirmed capacity is one RTX 2080 Ti with 22 GB VRAM. No connected SSH host, native capacity reservation, peaks, or throughput measurements exist in this project.
- The author [FlashAttention documentation](https://github.com/Dao-AILab/flash-attention) was inspected: its main FlashAttention-2 CUDA support targets Ampere/Ada/Hopper; it links a separate Turing implementation with a subset of features. BF16 is not the default assumption for this hardware.
- The publisher [Qwen3-1.7B card](https://huggingface.co/Qwen/Qwen3-1.7B) was read for size, architecture, and thinking-mode controls. This is a post-trained model; a Base checkpoint must be explicitly distinguished if the question concerns acquisition from a pretrained model.
- 0.5B full tuning and 1.5B–1.7B LoRA are provisional capacity-first options, not a frozen model slate or a runtime promise. Actual context, loss-logit memory, optimizer state, reference model, precision, CPU/RAM, and evaluator settings still determine feasibility.
- The 24-hour maximum cycle requires a calibrated queue. Search/probes, validation, discarded rollback work, tuning, and final evaluation must be counted; incomplete comparisons carry forward.

## Search coverage and limits

Queries were issued through both web search providers. Discovery families covered supervised fine-tuning generalization, data mixture/data mixing, multi-task SFT, gradient interference, low-rank mixture search, dataset order, and optimizer/momentum effects. Primary paper pages and author repositories were then inspected as listed above.

Discovery also surfaced DomainPilot (2607.22769), TANDEM (2606.04401), and Lie-Bracket Geometry in Sequential Learning (2606.24993). Their direct arXiv retrieval failed in this round. Their mechanisms therefore remain **unverified leads** and must be read before adjudicating collisions in corresponding directions.

This audit does not have the normalized raw-capture/index/expansion evidence needed to certify collision-search saturation. No “no prior work exists” claim, approved method, or final originality verdict is made.

## Current research decision

Continue joint primary-paper, implementation, and native-evaluator inquiry to determine a residual acquisition/retention or interference problem under matched total resources. Extend the current closest-work set before constructing the initial mathematical candidate pool.

Published phenomena are evidence to investigate; they have not been personally reproduced. Natural Gate 0, the frozen Parent Problem, collision/IPCG decisions, candidate verification and ranking, G01 complete design, Local acceptance, and confirmation remain open.
