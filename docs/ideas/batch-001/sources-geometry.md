# Geometry primary-source retrieval packet

Retriever: `/root/sources_geometry`. Cutoff: 2026-10-08. Project context: sequential multi-source LLM SFT; replacing obsolete current facts while retaining valid time-qualified history and general abilities. This packet records source content and inspected author code only. It does not rank candidates, determine novelty, or close the collision audit.

No training, scientific code execution, tests, inference, model/dataset downloads, reproduction, scorer execution, or GitHub mutations were performed. Public papers and selected author source files were read. Code pins below identify the inspected snapshot; a fetched file is not a validated runnable pipeline. Native scorers, dataset versions/splits, and hardware suitability remain unqualified unless explicitly stated.

## Factual mapping to frozen claims

| Claim | Source components retrieved | Scope boundary |
|---|---|---|
| I01 full-network old/new Jacobian feasibility | OGD uses old output Jacobians; OGD/OGD+ analyzes projected-feature kernel regression and a residual-dependent update norm. | Constant-Jacobian/local assumptions; neither source specifies the full temporal old/new compatibility claim as frozen. |
| I04 temporal guard retirement/history insertion and covariance downdates | Cholesky downdate source specifies subtracting a rank-one outer product and the definiteness condition. | The semantic rule deciding which current/history rows to retire or insert remains unresolved in this retrieval subset. |
| I05 new-only retention certification/probe rank | OGD/OGD+ output retention is conditional on an old Jacobian being represented in memory; perfect-memory theorem specifies broader information requirements. | These are not the exact proposed Jacobian probe-rank lower bound. No absence conclusion. |
| I06 direction-aware guard design | Classical c-optimal design minimizes variance in a specified target direction; SplitLoRA and per-unit projector optimize other spectral/rank allocation criteria. | Different objective and assumptions; target c is known in the classical criterion. |
| I07 adapter tangent capacity | LoRA-TSD defines the current low-rank tangent; NB-LoRA fixes an activation-null right factor; InfLoRA/KeepLoRA/SplitLoRA fix one adapter factor. | Activation-space constraints and full-network output-Jacobian constraints are distinct objects. |
| I08 bilinear update/tangent leakage | LoRA-TSD explicitly gives the finite product expansion and tangent projector. NB-LoRA has a structurally constrained finite parameterization. | Bilinearity alone does not defeat NB-LoRA's exact fixed-null-factor algebra. |
| I09 layer input drift | Per-unit projector explicitly limits its statement to a layer at base inputs. Adam-NSCL proves exact all-layer preservation by induction. | An unconditional claim that layerwise protection cannot compose is too broad. Exact simultaneous conditions can compose; approximate/partial conditions need separate drift analysis. |
| I10 projection and adaptive metric | Adam-NSCL and PaLoRA code project the candidate Adam update after its adaptive normalization. GORP paper projects before low-rank Adam moments. | Operator order is factual; no defect verdict on any uninspected or unexecuted full pipeline. |
| I11 harm at zero old loss gradient | OGD distinguishes loss and output gradients; SplitLoRA's L-smooth bound has a quadratic displacement term; PaLoRA uses local quadratic old-loss curvature. | Local assumptions and chosen retained inputs; no global retention guarantee. |
| I15 weak-mode sketch certificate | Frequent Directions gives a two-sided PSD covariance-error envelope and space lower bounds. | Mathematical covariance-sketch theorem, not by itself a neural retention certificate or selective temporal deletion algorithm. |

## Two scope distinctions for I08 and I09

**I08: tangent versus structural constraint.** LoRA-TSD's current-factor tangent excludes its finite bilinear cross term (S02). NB-LoRA's frozen right-null factor instead constrains the entire finite matrix (S01). Algebraic inference: differences of matrices sharing that factor also retain it. Exact annihilation requires an exact basis and represented inputs; practical spectral-tail approximation is separate.

**I09: partial protection versus exact composition.** Elementary algebra gives `δy=ΔW h+W δh+ΔW δh`. A fixed-input constraint alone leaves input drift. Adam-NSCL proves exact all-layer/all-step composition by induction (S10); its approximate implementation is separate. Applying that condition to transformer subsets requires accounting for every trainable path, bias, normalization parameter, and constrained input. S09 expressly limits its result to base inputs at one layer.

## Source records

### S01 NB-LoRA — Reasoning-Preserving Fine-Tuning of Post-RL LLMs with Null-Basis LoRA

- Primary full text: https://arxiv.org/html/2609.25618v1 ; v1 dated 2026-09-22.
- Retrieval refs: `turn58view0`, `turn59view1`, `turn115view3`, `turn132view1`, `turn133view2`.
- §3.2 Eq. (1) preserves a linear module on fixed token hidden inputs: `H(W+ΔW)^T=HW^T`. §3.3 gives null dimension `n-rank(H)` and explicitly says noisy hidden states are rarely exactly low rank; the practical basis uses the tail after retaining 99% spectral energy of `H^T H`.
- §3.4 Eqs. (4)–(5): `ΔW=B C N_s^T`, frozen `N_s`, trainable `B,C`, and exact `HΔW^T=0` conditional on `H N_s=0`. This is a finite structural constraint, compatible with arbitrary factor optimizer steps under the exact assumption.
- Appendix C.2 merges commonsense adaptation, recomputes the basis using original reasoning plus acquired commonsense examples, then adapts to tool use. Thus the protected activation set expands across the demonstrated sequence.
- Author homepage https://wenzhifang.github.io/index.html lists the paper. No linked implementation was resolved in full text/homepage/exact-title and repository queries. Code/release and native scorer remain unknown, not proved absent.
- Factual mapping: I07/I08/I09; no inspected temporal-history retirement rule.

### S02 LoRA-TSD — Tangent-Space Spectral Descent for LoRA via Muon-Style Updates

- Primary PDF: https://arxiv.org/pdf/2609.02734 ; v1 2026-09-02. HTML fetch failed.
- Retrieval refs: `turn121view0`, `turn132view2`, `turn133view3`.
- §3.1 treats one adapted layer with others fixed, applying the optimizer independently to layers. Eq. (4) factor gradients are `G_A=B^T G_W`, `G_B=G_W A^T`; Eq. (6) is the exact finite bilinear expansion above. Eq. (7) is its current first-order tangent. Eq. (13): `P_T(Z)=P_B Z+Z P_A−P_B Z P_A` under full-factor-rank assumptions. Eqs. (9)–(11) pose a tangent-constrained local spectral surrogate. Appendix Proposition 3 proves the factor-induced map is a retraction and exposes its `ΔBΔA` second-order term.
- Author-linked code: https://github.com/brain-lab-research/LoRA-TSD ; inspected commit `e6ef0e167c367671ed699d6c17b72fb57a81aee6`, 2026-09-01. Selected optimizer/layer code below. No continual protected-old-output constraint is specified in the inspected method.
- Factual mapping: I07/I08; native scorer/config qualification pending.

### S03 Orthogonal Gradient Descent for Continual Learning — Farajtabar et al., AISTATS 2020

- Primary PDF: https://proceedings.mlr.press/v108/farajtabar20a/farajtabar20a.pdf . Ref: `turn61view0`.
- §2 Eq. (4) factors the loss gradient through the model-output Jacobian. §3 Eq. (7) asks the update to be orthogonal to old model-output gradients; Eq. (8) substitutes stored previous endpoint gradients, a local approximation. Eq. (9) subtracts projections onto an orthonormal stored-gradient basis. Algorithm 1 collects old output gradients at task boundaries.
- §3 explains that fitted old examples may have near-zero loss gradients even while their output Jacobians remain informative. Experiments use finite sampled memories and SGD; protection of arbitrary unseen old outputs is not established by those constraints.
- Original author code was not inspected here. The OGD+ author implementation is linked in S04.
- Factual mapping: output versus loss gradients (I01/I05/I11); no temporal semantic role rules.

### S04 Generalisation Guarantees for Continual Learning with Orthogonal Gradient Descent — Bennani et al.

- Primary PDF: https://arxiv.org/pdf/2006.11942 . Refs: `turn64view0`, `turn66view5`, `turn91view2`, `turn66view6`, `turn115view2`.
- §4.1 Theorem 1 gives recursive projected-feature kernel regression with residual targets under NTK linearization, squared regression loss, and ridge regularization. Corollary 1 gives update norm `r^T(K+λI)^−1 K(K+λI)^−1 r`.
- §5.1 Theorem 2 preserves an old sample's output when its Jacobian is represented in stored memory, with constant-Jacobian assumptions. Infinite memory extends this to old training outputs. §7.2 discusses changing Jacobians outside the overparameterized approximation; OGD+ refreshes feature maps. Appendix F.2.4 specifies refreshing task slots, finite memory, and multihead projection scope.
- Author-linked repo https://github.com/MehdiAbbanaBennani/continual-learning-ogdplus was accessible; metadata/default branch `master` inspected only. No commit, update functions, or scorer were inspected.
- Factual mapping: I01/I05/I09. This is not the frozen temporal feasibility theorem or an exact probe-rank lower bound.

### S05 InfLoRA — Interference-Free Low-Rank Adaptation for Continual Learning, CVPR 2024

- Primary text: https://arxiv.org/html/2404.00228v1 . Refs: `turn74view3`, `turn79view4`. Author PDF: https://cs.nju.edu.cn/_upload/tpl/00/ce/206/template206/paper/CVPR24_InfLoRA.pdf .
- §3.1 Proposition 1, Eqs. (2)–(5), relates effective matrix updates to one trainable factor and a fixed factor with orthonormal row vectors. §3.2 selects a fixed reduction space within the current-task useful subspace and orthogonal to the stored previous activation space, estimated using SVD and DualGPM.
- Author code `liangyanshuo/InfLoRA`, commit `e08b00edd54f2f10cf2f9826eae7d44fdcb6354b` (2025-03-13) inspected in two files below. Paper/code A/B labels differ: the semantic fixed-down/train-up structure is the relevant scope.
- Factual mapping: I07/I08 and activation-subspace protection; vision continual tasks rather than the requested temporal factual LLM setting. Native scorer data/metric contract unqualified.

### S06 KeepLoRA: Continual Learning with Residual Gradient Adaptation, ICLR 2026

- Primary text: https://arxiv.org/html/2601.19659v1 . Refs: `turn61view1`, `turn64view4`, `turn64view5`, `turn64view6`, `turn137view0`.
- §3.2 removes pretrained principal-weight and previous-feature subspace components from the new gradient. §3.3 Proposition 3.1 Eq. (7), Appendix A.1 Eqs. (9)–(10), relates fixed-factor training to an effective projected gradient. Eq. (8)/Appendix A.2 constrains the orthonormal fixed factor to the complement of protected spaces and minimizes discarded new-gradient energy; leading singular directions solve the constrained problem.
- Author repo https://github.com/MaolinLuo/KeepLoRA current default is KeepLoRA++ `v2`; original `v1` snapshot inspected at `a17f9c24a4d31593a3792d0db447f5782cdc27e3` (2026-02-28). MTIL helper calls an initializer not defined in the inspected module class; dynamic definitions and separate MCIT/LLM paths were not checked. This limits implementation qualification, not an executed bug finding.
- KeepLoRA++ 2606.16256 metadata located; full-text fetches failed, so its extension remains unqualified.
- Factual mapping: I06/I07/I08; scorer unqualified.

### S07 SplitLoRA: Balancing Stability and Plasticity in Continual Learning Through Gradient Space Splitting, ICLR 2026

- Primary PDF: https://proceedings.iclr.cc/paper_files/paper/2026/file/5035a409f5798e188079e236f437e522-Paper-Conference.pdf . Refs: `turn64view3`, `turn66view8`, `turn68view3`, `turn138view0`.
- Proposition 4.1 Eq. (7) is an L-smooth total old-loss upper bound containing gradient inner product and a quadratic update cost. Theorem 4.2 Eqs. (11)–(12) relates retained-tail energy to expected stability and retained dimension to expected plasticity; the latter assumes equal expected projection across feature directions. Eq. (15) trades spectral tail against dimension, and Eq. (17) constructs a fixed reduction factor from minor directions; the other factor trains.
- Author link redirects from `qhmiao/SplitLoRA` to `iLearn-Lab/ICLR26-SplitLoRA`. Inspected commit `1d7b48821bf001c8d9f29d5d8da07e2bbf2b94e1` (2026-04-06), two files below. Native scorer/config contracts not qualified.
- Factual mapping: I06/I07/I08/I11; vision task scope and stated expectation assumptions.

### S08 PaLoRA — Paced Low-Rank Adaptation for Continual Learning

- Primary PDF: https://arxiv.org/pdf/2610.04226 ; v1 2026-10-03. Refs: `turn64view2`, `turn66view2`, `turn72view5`, `turn74view6`. HTML fetch failed.
- §3.2 analyzes one frozen linear layer, full-batch Frobenius regression, positive-definite new-input covariance, and old accumulated adapter right-singular spans. Exact right-nullspace updates preserve that represented old span. It assumes anisotropic leakage `Eε_i²=η²γ_i²/s²` and locally quadratic old-loss curvature `λ_i>0`. Eq. (1) bounds expected old quadratic harm; Eq. (2) gives first-order new progress; Lemma 3.1 Eq. (3) derives pace `s*=sqrt(R/c)` under its forgetting budget. This is not a proved end-to-end deep-transformer guarantee.
- Author repo `liyuxuan-github/PaLoRA`, inspected commit `4aa4a3b1ed9629b6a6272232eccd78dcadec3562` (2026-10-06), actual custom-Adam + factor/model paths below. Both factors train; the candidate Adam update is projected after moments/normalization.
- Factual mapping: I07/I08/I10/I11; vision EFCIL scorer unqualified.

### S09 A Tropical Geometry View of Forgetting: A Per-Unit Projector for Knowledge-Preserving Fine-Tuning

- Primary text: https://arxiv.org/html/2610.04670v1 ; v1 2026-10-03. Refs: `turn93view0`, `turn109view2`, `turn115view4`.
- §2 Theorem 5 Eq. (2) decomposes ReLU-layer output changes by old/new gate status. §3 Definition 7 Eq. (4) projects each row's cumulative displacement after the optimizer using selected old base inputs: `u←u−A_i^T(A_iA_i^T+ρI)^−1A_i u`. Proposition 8 gives exact fixed-input annihilation at `ρ=0` and ridge residual factor `ρ/(σ_+²+ρ)`.
- The source explicitly says jointly training fc1 layers also causes input drift and limits its claims to a layer at base inputs. Theorem 9 compares per-unit rank cost with shared union rank; Proposition 10 assumes isotropic proposed updates for expected-damage spectral allocation.
- §7 says companion implementation/scorer/histories exist, but no author release URL was resolved from full text/exact-title queries. Code and scorer remain unknown, not proved absent.
- Factual mapping: I09/I10 and rank/design components I05/I06.

### S10 Adam-NSCL — Training Networks in Null Space of Feature Covariance for Continual Learning, CVPR 2021

- Primary PDF: https://arxiv.org/pdf/2103.07113 . Refs: `turn103view3`, `turn107view2`, `turn109view1`, `turn132view0`, `turn133view1`.
- §3.2 Lemma 1 Eq. (1), Lemma 2 Eq. (2), and Appendix A give exact all-layer/all-step old-output preservation through layer and step induction. The model has linear/convolutional transformations followed by unchanged nonlinearities. Condition 1 Eq. (3) replaces full old input rows by their uncentered covariance, whose exact nullspace is the same.
- §4/Algorithm 1 forms an Adam candidate then projects it; Eq. (6) is the layerwise projection. Practical §4.1 uses small-singular-value directions as an approximate nullspace, not the exact sufficient condition.
- Author repo `ShipengWang/Adam-NSCL`, inspected commit `a2f39b4273aa300739c460b33a5e8d2c674632b2` (2021-07-24); custom optimizer below normalizes the projector by Frobenius norm. Full binding/scorer not qualified.
- Factual mapping: I09 exact composition caveat and I10 operator order; partial/approximate conditions remain separate.

### S11 Continual Gradient Low-Rank Projection Fine-Tuning for LLMs — GORP, ACL 2025

- Primary PDF: https://aclanthology.org/2025.acl-long.721.pdf . Refs: `turn115view0`, `turn118view2`, `turn118view3`.
- §3.2 Eqs. (6)–(12) and Algorithm 1 project a gradient into low-rank coordinates, calculate Adam moments there, expand the normalized update, and update parameters. Eq. (7) precedes Eqs. (8)–(10). The method combines LoRA on attention with fuller MLP parameter updates.
- Author-linked https://github.com/Wcxwcxw/GORP was accessible; metadata/default branch `main` read only. Actual update code, task bindings, and native scorer were not inspected. The paper's operator order alone is not a code defect verdict.
- Factual mapping: hybrid adapter/full parameter scope I07 and optimizer-order comparator I10.

### S12 Frequent Directions — Simple and Deterministic Matrix Sketching

- Primary PDF: https://arxiv.org/pdf/1501.01711 . Refs: `turn93view1`, `turn99view0`, `turn109view0`.
- §1.4 Theorem 1.1 guarantees, for all unit vectors x, `0≤||Ax||²−||Bx||²≤||A−A_k||_F²/(ℓ−k)`. Equivalently `0≼A^T A−B^T B≼εI`. Theorem 1.3 gives a corresponding space lower bound under constant-size-word assumptions. The stream consists of inserted matrix rows; selective removal based on temporal fact roles is not specified.
- Author-linked `edoliberty/frequent-directions`, inspected commit `691df9edb2ffbc2fdddc2cec3b703a3f1e438d4d` (2016-04-19). `frequentDirections.py` uses a 2ℓ buffer and SVD shrink `sqrt(σ_i²−σ_ℓ²)`; it does not expose a running ε certificate in that inspected file. Imported dependency not checked/run.
- Factual mapping: I15 covariance PSD envelope; identifying `F=A^T A`, `Fhat=B^T B` is a notation mapping, not an independent neural guarantee.

### S13 Design of c-Optimal Experiments for High dimensional Linear Models — Eftekhari, Banerjee, Ritov

- Primary PDF: https://arxiv.org/pdf/2010.12580 . Ref: `turn103view0`.
- §1.5 restates the classical low-dimensional criterion. For a specified direction c, unbiased estimation requires `c∈span(X)` and variance is `σ² c^T(X^T X)^+ c`. Problem P0 allocates integer measurement counts; approximate P1 minimizes `c^T Σ^+ c` over `Σ=Σ_i w_i x_i x_i^T`, `w_i≥0`, `Σ_i w_i=1`. P1' gives an equivalent ℓ1 representation of c by candidate vectors via Elfving's characterization. Their high-dimensional extension imposes PSD bounds to control debiasing bias.
- This is a primary paper restating the classical objective, not the original 1952 paper. Author code and any experimental scorer were not inspected.
- Factual mapping: I06 direction-specific design comparator; assumes known target direction and available candidate design vectors.

### S14 Optimal Continual Learning has Perfect Memory and is NP-hard — Knoblauch, Husain, Diethe, ICML 2020

- Primary PDF: https://proceedings.mlr.press/v119/knoblauch20a/knoblauch20a.pdf . Refs: `turn103view2`, `turn107view3`.
- The formalization uses task-specific satisfactory-parameter sets and their intersections. Theorem 2 derives perfect memory under its criterion conditions and finite-intersection availability of parameter equivalence classes. Corollary 2 strengthens conditions when each equivalence class can itself be a valid task set. Perfect memory here means preserving sufficient task-equivalence information, not necessarily retaining all raw data.
- Factual mapping: I05 broader information-retention requirement. It does not directly specify the frozen Jacobian-span/probe-rank bound. No code/scorer claim relevant to the mathematical theorem.

### S15 A Note on Downdating the Cholesky Factorization — Bojanczyk, Brent, van Dooren, de Hoog, 1987

- Primary PDF: https://maths-people.anu.edu.au/brent/pd/rpb095i.pdf . Refs: `turn107view0` (unparsed PDF), `turn109view3`/`turn109view4` (inspected screenshots, pages 1–2).
- §1 Eq. (1) poses `B^T B=A^T A−xx^T` for triangular A. A positive-diagonal triangular B exists when the right-hand side is positive definite. With `A^T z=x`, the condition becomes `||z||²<1`. The paper addresses numerical downdating/stability.
- The earlier Gill–Golub–Murray–Saunders 1974 primary PDF https://web.stanford.edu/group/SOL/papers/ggms74.pdf was located (`turn99search2`) but full fetch failed (`turn103view1`); it is not treated as read.
- Factual mapping: I04 outer-product retirement algebra/definiteness. No current-fact/history semantic selection rule. No code inspected.

### S16 LoRA — Low-Rank Adaptation of Large Language Models

- Primary PDF: https://arxiv.org/pdf/2106.09685 . Refs: `turn115view1`, `turn118view4`.
- §4.1 Eq. (3) defines `h=W_0x+BAx` with frozen base weights, trainable factors, Gaussian A initialization and zero B initialization; experiments use Adam. This specifies the underlying bilinear parameterization. S02 explicitly expands its finite update and current tangent.
- Original LoRA code was not inspected here. Factual mapping: I07/I08 foundational parameterization.

## Pinned author code: inspected functions and scope

Line numbers refer to the fetched full UTF-8 files at the exact commit. All were inspected statically only. Source URLs are pinned and may be opened independently for adjudication.

| Repository / commit | Inspected file, blob SHA | Functions / decisive scope |
|---|---|---|
| LoRA-TSD / `e6ef0e167c367671ed699d6c17b72fb57a81aee6` | [src/optimizers/lora_tsd.py](https://github.com/brain-lab-research/LoRA-TSD/blob/e6ef0e167c367671ed699d6c17b72fb57a81aee6/src/optimizers/lora_tsd.py), blob `782e73159b34fa0bd8f4159fd9723d83f95b614b` | `_spd_inv` 48–52 uses relative ridge; `tangent_projected_grad` 56–74 reconstructs projected weight gradient; `LoRATSD.step` recomputes current QR/Gram factors, iterates sign-plus-tangent projection (315–322), reconstructs linearized factor steps (342–347), and updates both factors. No old-data/null-history guard in inspected optimizer. |
| LoRA-TSD / same | [src/models/lora.py](https://github.com/brain-lab-research/LoRA-TSD/blob/e6ef0e167c367671ed699d6c17b72fb57a81aee6/src/models/lora.py), blob `7a0a5a42e15b359b16cb5a2c25bd618f9f8f4a55` | `get_lora_param_groups` freezes general parameters then enables both A and B; optional `add_W` additionally enables W. Binding to actual experiment factory/scorer not inspected. |
| InfLoRA / `e08b00edd54f2f10cf2f9826eae7d44fdcb6354b` | [methods/inflora.py](https://github.com/liangyanshuo/InfLoRA/blob/e08b00edd54f2f10cf2f9826eae7d44fdcb6354b/methods/inflora.py), blob `73fbdce05a1920a6caa0eab6ada1b3fff5b8f799` | `_train` 93–108 trains classifier/current `lora_B`; 118–157 estimates current activation covariance, removes/retains stored subspace components and initializes fixed `lora_A`; 195–205 records DualGPM. `update_DualGPM` starts 321. |
| InfLoRA / same | [models/vit_inflora.py](https://github.com/liangyanshuo/InfLoRA/blob/e08b00edd54f2f10cf2f9826eae7d44fdcb6354b/models/vit_inflora.py), blob `5a1a919225a70ab6d0051fb9a55eee4cdc546d37` | `Attention_LoRA` 175–207 defines k/v factors; `forward` 232–238 accumulates token covariance, 246–247 sums task factor products. Scope is selected ViT attention paths and classifier. |
| KeepLoRA original v1 / `a17f9c24a4d31593a3792d0db447f5782cdc27e3` | [MTIL/model/keeplora_helper.py](https://github.com/MaolinLuo/KeepLoRA/blob/a17f9c24a4d31593a3792d0db447f5782cdc27e3/MTIL/model/keeplora_helper.py), blob `5bffbfe465b79a32ac793b57c275f396bce245d7` | `initialize_keeplora_for_task` 70–94 forms projectors and calls module initialization. Author repo branch identity was checked; path-specific initialization resolution remains incomplete. |
| KeepLoRA v1 / same | [MTIL/model/peft_modules.py](https://github.com/MaolinLuo/KeepLoRA/blob/a17f9c24a4d31593a3792d0db447f5782cdc27e3/MTIL/model/peft_modules.py), blob `f3e78d538361761e55738a9335684b4cec4530d3` | `KeepLoRA` reset uses fixed tensor A and trainable nn.Parameter B (22–24); forward 67–70 and delta 73–79. Called initializer not defined in inspected class; separate LLM paths not inspected. |
| SplitLoRA / `1d7b48821bf001c8d9f29d5d8da07e2bbf2b94e1` | [lora/utils.py](https://github.com/iLearn-Lab/ICLR26-SplitLoRA/blob/1d7b48821bf001c8d9f29d5d8da07e2bbf2b94e1/lora/utils.py), blob `da489b2a3845ffa48ec5d376f3b9f2a67b2cd037` | `LoRALayer` 120–168 merges previous products; before-task fixed A is drawn in stored minor space; after-task SVD uses linear singular-value proportions and argmin `(task+1)*(1−cumsum)−α*k`; retained tail starts at `max(r,1)+1`. |
| SplitLoRA / same | [train_splitlora.py](https://github.com/iLearn-Lab/ICLR26-SplitLoRA/blob/1d7b48821bf001c8d9f29d5d8da07e2bbf2b94e1/train_splitlora.py), blob `12bed3ba583748a22250aba99d5546872f0d023f` | 136–144 freezes all except classifier/head/current `lora_B`; 271 constructs AdamW; 283 prepares fixed basis and 299 updates it after training. Scorer/data helper not qualified. |
| PaLoRA / `4aa4a3b1ed9629b6a6272232eccd78dcadec3562` | [optimgrad/adam_paced.py](https://github.com/liyuxuan-github/PaLoRA/blob/4aa4a3b1ed9629b6a6272232eccd78dcadec3562/optimgrad/adam_paced.py), blob `a068f33ae8a07eb0ae22da2dcef18f9d6b20ec95` | `Adam.step` 86 forms `get_update` before 88–101 directional projection; `get_update` 152–191 includes Adam moments, decay and elementwise denominator. `get_transforms` 114–130 uses 99% cumulative singular values, tail P, and pace-scaled P for one factor. |
| PaLoRA / same | [methods/palora.py](https://github.com/liyuxuan-github/PaLoRA/blob/4aa4a3b1ed9629b6a6272232eccd78dcadec3562/methods/palora.py), blob `9cf628927f3ad522bb043d2a39afa7ce5de777ef` | Custom optimizer imported at17; `_train` 98–120 enables both factors/current classifier; 129–149 binds factor projections to accumulated adapters; optimizer groups 251–278 use `svd=True`, threshold .99 with classifier excluded. |
| PaLoRA / same | [models/vit_palora.py](https://github.com/liyuxuan-github/PaLoRA/blob/4aa4a3b1ed9629b6a6272232eccd78dcadec3562/models/vit_palora.py), blob `5ed29d9c6e5e9593acb5b602df2b187d31e4c4cb` | `Attention_LoRA.get_cum` 242–264 accumulates normalized B A/norm(A), compresses by SVD using linear singular sum; forward 314–315 adds current normalized product to compressed history. |
| Adam-NSCL / `a2f39b4273aa300739c460b33a5e8d2c674632b2` | [optim/adam_svd.py](https://github.com/ShipengWang/Adam-NSCL/blob/a2f39b4273aa300739c460b33a5e8d2c674632b2/optim/adam_svd.py), blob `9ee0a4d87879bb8e9f84eb2c815e44ab8baea8e6` | `Adam.step` 78–90 gets Adam update then right-multiplies transform (reshaping convolution); `get_transforms` 102–115 selects eigenvalues ≤minimum×threshold and Frobenius-normalizes P. `get_update` 130–170 implements moments/decay/adaptive denominator. |
| Adam-NSCL / same | [svd_agent/svd_based.py](https://github.com/ShipengWang/Adam-NSCL/blob/a2f39b4273aa300739c460b33a5e8d2c674632b2/svd_agent/svd_based.py), blob `d4df6b40d19122f8b16e70ae772e516ab2a60580` | Wrapper only; referenced `SVDAgent` implementation and scorer were not inspected. |
| Frequent Directions / `691df9edb2ffbc2fdddc2cec3b703a3f1e438d4d` | [frequentDirections.py](https://github.com/edoliberty/frequent-directions/blob/691df9edb2ffbc2fdddc2cec3b703a3f1e438d4d/frequentDirections.py), blob `4bb3500cbea9c81c21cbeea5cd5db60ac4006d3d` | `append` 16–20, `rotate` 22–36 implement stream insertion, SVD and shrinking the retained singular values. Running error certificate and imported base dependency unqualified. |

## Unresolved and located-only items

- NB-LoRA author release and native scorer; per-unit projector author release and scorer; original OGD code; OGD+ and GORP actual update/scorer files; KeepLoRA v1 initializer scope and separate LLM path; full KeepLoRA++ text/code mechanism.
- GDLoRA, arXiv 2609.37027, title *Beyond Low-Rank Parameterization: Narrowing the Gap Between LoRA and Full Fine-Tuning via Gradient Decomposition*, was located (`turn115academia31`); HTML and PDF fetches failed (`turn118view1`, `turn121view1`). Its abstract is not treated as a verified mechanism.
- Additional tangent-related leads were located but not read: ICML2026 *Towards Understanding Dynamics of LoRA* https://proceedings.mlr.press/v306/ding26k.html (`turn115search1`), a LoRA NTK2024 result (`turn115search0`), PRISM (`turn115search3`), ISO-LoRA 2609.12123 (`turn115academia32`). These are retrieval leads only.
- No exact temporal guard-retirement/history insertion mechanism or exact new-only Jacobian probe-rank lower-bound source was resolved by this subset. This is unresolved coverage, not an absence-of-prior-work finding.
- Retrieval convergence was requested before two no-new-mechanism rounds. The completeness/novelty audit remains pending. Recent sources were inspected through Oct 3–6, within the cutoff; later versions/commits are not assumed.

