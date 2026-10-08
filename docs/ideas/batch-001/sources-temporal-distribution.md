# Primary-source packet: temporal updating, targets, and gradient conflicts

Prepared 2026-10-08. Retrieval role only: factual element mapping, not novelty adjudication, ranking, or a completed collision audit. All scientific paper/source-code access was read-only. No experiments, inference, tests, model/data downloads, or repository mutations were performed. No feasibility claim is made for the user-reported single 22 GB 2080Ti.

## Scope and primary-source index

| Source inspected | Exact version / date | Frozen elements to compare | Retrieval references for root verification |
|---|---|---|---|
| [SoFT](https://arxiv.org/html/2609.32493v1) | arXiv:2609.32493v1, 2026-09-26 | I02, I18 | `turn63view0`, `turn65view0`, `turn65view1`, `turn70view1`, `turn128view0` |
| [Unilogit](https://arxiv.org/html/2505.06027v1) | arXiv:2505.06027v1, 2025-05-09; [ACL Findings 2025 record](https://aclanthology.org/2025.findings-acl.1154/) | I02, I18 | `turn92view1`, `turn95view4`, `turn97view1`, `turn88search0` |
| [LOKA final paper](https://aclanthology.org/2026.acl-long.760v2.pdf) | ACL 2026, July; Anthology PDF version 2 | I03, memory routing context for I20 | `turn117view5`, `turn105view1`, `turn100view0`, `turn117view6` |
| [Resolving Editing-Unlearning Conflicts](https://arxiv.org/html/2502.00158v1) | arXiv:2502.00158v1, 2025-01-31 | I03 | `turn90view0`, `turn92view2`, `turn95view7` |
| [G-effect](https://arxiv.org/html/2502.19301v1) | arXiv:2502.19301v1, February 2025 | I03 | `turn65view3`, `turn70view5`, `turn77view3`, `turn85view3` |
| [Geometric-disentanglement Unlearning](https://arxiv.org/html/2511.17100v4) | arXiv:2511.17100v4, 2026-02-02 | I03; projection assumptions | `turn77view0`, `turn81view1`, `turn85view0`, `turn85view1` |
| [LLM Surgery](https://arxiv.org/pdf/2409.13054v1) | arXiv:2409.13054v1, 2024-09-19 | I03, I17; updating/retaining benchmark | `turn81view0`, `turn85view4`, `turn129view1` |
| [Trust the Uncertain Teacher / CUD](https://arxiv.org/html/2602.12687v2) | arXiv:2602.12687v2, 2026-05-18 | I02, I17, I18 | `turn120view0`, `turn126view0`, `turn128view1` |
| [Residual-learning KD](https://cdn.amazon.science/e5/df/a7c7e954442aad1010753a200620/13988-knowledge-distillation-f.pdf) | Published ICLR 2026 author PDF | I17 | `turn113view0`, `turn114view0`; OpenReview `Dh6KxUxG20` |
| [TILDE](https://arxiv.org/html/2607.06432v1) | arXiv:2607.06432v1, 2026-07-07 | I02, I18; different model modality | `turn92view0`, `turn97view0` |

Ref IDs are local retrieval handles; direct versioned URLs are the durable identifiers. Root should open these primary URLs before citing them in its user response. This packet does not silently merge the LOKA preprint and ACL publication: same authors/mechanism were inspected, but an explicit preprint-to-final identity link was not captured.

## Decisive distribution mathematics

### SoFT: full target and budget equations

At a teacher-forced state \(s_t=(x,y^\star_{<t})\), §3.2 Eq.3 solves

\[
q_t=\arg\min_{q\in\Delta(V)}\mathrm{KL}(q\Vert\pi_0(\cdot\mid s_t)),\qquad q(y_t^\star)\ge\tau_x.
\]

Eq.4 sets \(q_t(y_t^\star)=\max\{p_t,\tau_x\}\) and \(q_t(v)=\pi_0(v)(1-q_t(y_t^\star))/(1-p_t)\) otherwise, where \(p_t=\pi_0(y_t^\star\mid s_t)\). Eq.5 gives \(a_t=[\tau_x-p_t]_+/(1-p_t)\), \(\lambda_t=1-a_t\), \(q_t=a_t\delta_{y_t^\star}+\lambda_t\pi_0\). Eq.6 is weighted gold NLL plus \(\lambda_t\mathrm{CE}(\pi_0,\pi_\theta)\), equivalent to a forward-KL anchor plus a constant.

§3.4 Eq.7 calibrates \(\tau_x\) by

\[
R_x(\tau_x)=\frac{\sum_t a_t(1-p_t)}{\sum_t(1-p_t)}=R^\star.
\]

§4.1 Eq.8 replaces \(R^\star\) with a domain budget \(R^\star_{d(x)}\). Targets remain fixed during training. Appendix A specifies **initial token-logit** gradient budgets, not a general parameter-gradient or final-performance guarantee. Factual mapping: minimum-KL floor, unchanged non-gold ratios, coupled acquisition/retention, and calibrated domain budgets. The inspected equations use a single demonstrated-token constraint rather than the frozen multi-fact expectation constraints.

**Implementation:** Appendix B contains inspected dense PyTorch target/loss/bisection snippets. B.2.1 Eq.24 approximates the target with top-32 plus gold and a tail bucket, preserving gold probability and aggregate tail mass. No author repository was verified. [Author Haoyu Huang’s homepage](https://hhy-huang.github.io/) lists SoFT with a paper entry but no code link in the inspected entry (`turn126view1`).

### Unilogit: forget target with preserved alternative ratios

§3 and Appendix B set the observed forget token’s logit to

\[
\widetilde h_k=\log\left(\frac{\sum_{i\ne k}\exp h_i}{V-1}\right),\qquad \widetilde h_i=h_i\ (i\ne k).
\]

Therefore \(\widetilde p_k=1/V\), while ratios among all alternatives are unchanged. Targets use the **current** model’s detached logits; reverse-KL distillation moves the model toward this target. This specifies uncertainty about the forgotten token; the inspected construction does not label a correct replacement answer. Factual mapping: selective probability modification, preservation of relative alternatives, and the distinction between forgetting and learning a replacement.

**Actual author code:** paper-linked repository now resolves to [eBay/unilogit-acl-2025](https://github.com/eBay/unilogit-acl-2025). Inspected commit `641c65887217a415183616196a0b11c7abee911d` (2025-10-13), [trainer.py](https://github.com/eBay/unilogit-acl-2025/blob/641c65887217a415183616196a0b11c7abee911d/LLaMA-Factory/src/llmtuner/train/unilogit/trainer.py), `get_uniform_loss()` lines 45–88. It masks the gold logit, applies log-sum-exp minus `log(V-1)`, restores that target logit, and uses `F.kl_div(soft_targets, soft_outputs, log_target=True)` on supervised positions. An original-model target option is commented out. Code was read, not run.

### CUD: correct/wrong target mass and teacher-error conditioning

Latest pre-cutoff v2 §2.3 R1 combines entropy bounds with neighborhood mass \(q(N)\ge\alpha\); R2 bounds wrong-class mass \(q(W)\le\epsilon\). Main §2.4 Eq.2 permits a generic discrepancy, including symmetric KL or Wasserstein examples. **Appendix A specializes to \(\mathrm{KL}(q\Vert p_T)\)** and describes linear halfspaces; Eq.11 yields

\[
q_k^*=Z^{-1}p_T(k)\exp\{\mu\mathbf1_{k\in N}-\nu\mathbf1_{k\in W}\}.
\]

It preserves ratios for unconstrained classes. Keep the main entropy formulation and appendix linear-constraint formulation distinct when checking assumptions.

§3.2 W-Clip transfers mass from an incorrect teacher argmax \(k^*\) to ground truth \(y\): \(\delta=\min\{\eta p_T(k^*),m[p_T(k^*)-p_T(y)]\}\), increasing \(p_T(y)\) by \(\delta\), decreasing \(p_T(k^*)\) by \(\delta\), leaving other entries unchanged. That substage leaves correct-teacher cases unchanged. §3.3 Eq.9 combines calibrated-target forward KL with labeled CE. Experiments are BERT-based multiclass classification, not chronological autoregressive updating. No author code was verified.

Factual mapping: minimum-discrepancy constrained mass target, wrong-teacher correction, unconstrained ratios, and explicit correctness-conditioned transfer.

### TILDE: conditional KL projection with a shared multiplier

§2.1 Eq.1 minimizes prompt-averaged \(\mathrm{KL}(p(\cdot\mid y)\Vert p_{pre}(\cdot\mid y))\) at fixed prompt distribution \(\pi\), subject to an expected undesired-concept energy bound. Eq.2 yields

\[
p^*(x\mid y)=p_{pre}(x\mid y)\exp[-\beta E_C(x)]/Z_\beta(y).
\]

Zero-energy outputs keep relative ratios. Appendix D.1 Proposition 4, Eqs.49–52 provide the KKT derivation with nonempty/strictly feasible constraints, integrability/support assumptions, uniqueness up to prompt-null sets, and a shared \(\beta\). This is diffusion concept removal, without an explicit new factual answer constraint. Appendix C.6 distinguishes the target-level characterization from nonconvex LoRA/surrogate training. [Author homepage](https://ngk2110.github.io/) lists TILDE with a paper entry; no author code was verified.

Factual mapping: conditional KL target, expectation constraint, exponential tilt, and proportional preservation on a benign set. It supplies a cross-modality mathematical comparison; no LLM or temporal transfer claim is inferred.

## Gradient conflict, safe projection, and update versus forgetting

### LOKA: explicit learning–unlearning conflict

ACL final paper §2.1 defines conflict by \(\nabla L_l^\top\nabla L_u\le0\). Appendix A Definition A.1 / Assumption A.2 / Theorem A.3 uses log-probability Lipschitz constant \(C\):

\[
\operatorname{TV}(\mathcal D_l,\mathcal D_u)\le\frac{\max\{\|\nabla L_l\|,\|\nabla L_u\|\}}{2C}
\]

is a sufficient conflict condition. Proposition A.4 compares joint versus separate task updates for sufficiently small steps. The earlier arXiv v1 states the same mechanism in §2.2 Definition 2.1 / Theorem 2.3 / Proposition 2.4. §3 uses separate memory units for severe conflicts and minimum-norm convex gradient mixtures for milder cases, with new-data CE, NPO forgetting, and retention KL. Its inspected setting is batch knowledge updating; historical time conditioning is not established by these results.

**Actual author code:** [author publications page](https://zhangbinchi.github.io/publications/) links the ACL title to [zhangbinchi/LOKA](https://github.com/zhangbinchi/LOKA). Commit `985bb2d64261c0ce17e7f354b3f760c7d4332c0b` (2026-03-29). Inspected [loka_model.py](https://github.com/zhangbinchi/LOKA/blob/985bb2d64261c0ce17e7f354b3f760c7d4332c0b/src/models/loka_model.py): `_mgda_scales()` lines 216–245 normalizes NPO/learning gradients and calls MinNormSolver; `_estimate_conflict_ratio()` lines 247–269 measures positive-gradient-cosine frequency without weight updates; `update()` lines 426–483 selects separate memories or mixed updating. Also inspected `utils.py`, `adapter.py`, README. Router/codebook chooses memory by query embeddings; native configurations cover TOFU/toxic/ZsRE. No execution.

Factual mapping: learning–forgetting alignment criterion and adaptive conflict handling, for comparison with I03’s projected alignment boundary.

### G-effect: first-order risk alignment plus inspected measurement code

§3 Definition 1 defines

\[
e^{(t)}=\nabla_\theta R(\mathcal D;\theta_t)^\top\nabla_\theta L_u(\mathcal D_u;\theta_t).
\]

Under descent, positive values correspond to improving evaluation risk and negative values to worsening it; forgetting aims for negative forget-risk and nonnegative retained-risk effects. Appendix A Eqs.9–13 derives small-step risk changes and cumulative effects involving gradient alignment, Hessians, and update order. This is a local risk analysis, not an identity between forgetting and acquiring a replacement.

**Actual author code:** paper links [tmlr-group/G-effect](https://github.com/tmlr-group/G-effect), commit `ef368eea3b2c6dba1e090b9ebb021ac9f047e0ae` (2025-02-27). Inspected [dataloader_ge.py](https://github.com/tmlr-group/G-effect/blob/ef368eea3b2c6dba1e090b9ebb021ac9f047e0ae/dataloader_ge.py), `gradient_unlearn_effect()` lines 87–111 and `gradient_retain_effect()` lines 113–139: sums products of objective/metric gradient tensors by layer and globally. Gradient collection uses EMA `0.6*old+0.4*current`; distinguish this measurement implementation from the instantaneous mathematical definition. README and actual code were read; no benchmark was run.

Factual mapping: gradient dot-product sign as a first-order effect criterion.

### Geometric-disentanglement Unlearning: retain-null projection

Latest pre-cutoff v4 §3 works in optimizer metric \(H\succ0\), using \(H\)-gradients and a retained-gradient span. Lemma 3.2 characterizes steepest feasible descent under \(U^\top H\Delta=0\), \(\|\Delta\|_H\le1\) as normalized negative projected forget gradient. Proposition 3.3 Eq.8 splits the step into retained-orthogonal forgetting and retained-tangent descent; Eq.9 gives first-order retained-risk change \(-\rho\beta\|g_r\|_H^2\le0\). Corollary 3.4 bounds second-order drift under metric smoothness. At \(\beta=0\), its stated retention claim allows second-order drift.

**Actual author-code provenance:** paper links [Lemutisme/Geometric-Unlearning](https://github.com/Lemutisme/Geometric-Unlearning), whose inspected head contains README/license/figures. **README redirects to implementation** [Lemutisme/geo-unlearning, dev](https://github.com/Lemutisme/geo-unlearning/tree/dev). Inspected commit `bbe4d5077b21f6ded0ddbff8bf49b0336260626a` (2026-02-04), [geometric.py](https://github.com/Lemutisme/geo-unlearning/blob/bbe4d5077b21f6ded0ddbff8bf49b0336260626a/src/trainer/unlearn/geometric.py). `RetainNullProjector` maintains per-parameter fp16 retain bases, default rank 8, Adam/EMA whitening and Gram–Schmidt; `GeometricUnlearn.optimizer_step()` reconstructs the forgetting component and applies projected plus sign-selected tangent components. Inspected YAML and `gu_eval.sh` cover TOFU, MUSE, WMDP. These are finite minibatch/per-parameter approximations; hook validity and runtime behavior remain untested.

Factual mapping: projected forgetting and explicit retention bounds/assumptions. Neither the theorem nor inspected code establishes correct replacement acquisition automatically.

### LLM Surgery: simultaneous explicit update and retention objectives

§2 Eq.1 writes a signed objective of dataset/sequence-averaged forget CE, **minus** update CE, **minus** \(\mathrm{KL}(P_{surgery}\Vert P_{pre})\) on retained text. The accompanying text specifies ascent on forget CE, descent on update CE, and KL minimization. Preserve that sign convention when quoting the equation rather than silently calling the printed objective a minimization loss.

§3.1 pairs 119 obsolete biographies with 119 GPT-4-generated fictitious replacement biographies about the same subjects, alongside problematic biographies and retained general text; evaluation includes update/forget/retain MCQA and ARC-Easy. §4’s GD+KL ablation retains obsolete-answer performance; authors attribute reduced forgetting to the KL anchor. This is the paper’s reported result, not independent replication or a validity theorem.

**Access:** linked anonymous code URL [llm_surgery_code-24E8](https://anonymous.4open.science/r/llm_surgery_code-24E8/README.md) returned no readable source (`turn88view2`), so implementation was not verified. HTML omitted Eq.1 math; the PDF was read.

Factual mapping: explicit learning signal for replacements separate from obsolete-answer suppression; anchor behavior can oppose forgetting. No historical-validity guarantee is inferred.

## Additional I17 teacher-error source

[Knowledge Distillation for Large Language Models through Residual Learning](https://www.amazon.science/publications/knowledge-distillation-for-large-language-models-through-residual-learning), Thinh On et al., published ICLR 2026, uses ground truth to identify wrong teacher tokens. §3.2 Eq.4 subtracts projected teacher-state residuals only where teacher argmax differs from the gold token; Eqs.6/11 give residual CE plus SFT. Appendix A Theorem 1 Eq.13 states a supervised-gradient decomposition with a teacher-conditioned correction. Its proof explicitly uses a first-order Taylor expansion and an \(o(\beta)\) term; do not treat the displayed equation as an independently established exact finite-step identity.

The author-hosted published PDF was inspected. [OpenReview Dh6KxUxG20](https://openreview.net/forum?id=Dh6KxUxG20) produced a browser-verification wall (`turn117view2`). No author repository was verified. Factual mapping: teacher correctness conditions the transfer, rather than unconditionally retaining teacher behavior. This does not by itself supply temporal validity labels or a full risk decomposition for an obsolete base teacher.

## I19/I20 coverage boundaries and unresolved access

These two elements were not resolved to a full decisive mathematical source in this retrieval pass.

- [Time-Aware Language Models as Temporal Knowledge Bases](https://aclanthology.org/2022.tacl-1.15.pdf), Dhingra et al., TACL 2022, was partially read. It contrasts time conditioning with averaging facts across time and studies future-query entropy (§3.2). This is contextual evidence; it does **not** establish the frozen missing-time posterior mixture/Bayes-risk proposition. PDF refs: `turn117view4`, `turn119view2`, `turn119view4`.
- [Physics of Language Models, Part 3.3: Knowledge Capacity Scaling Laws](https://proceedings.iclr.cc/paper_files/paper/2025/hash/26d3c9a66836ded8f34a944f2bfe868e-Abstract-Conference.html), Allen-Zhu and Li, ICLR 2025, official abstract and author project page were retrieved (`turn120view2`, `turn120view3`, `turn126view2`). ArXiv full-text access failed. The controlled factual-storage claim cannot be substituted for a universal temporal-version or adapter-rank capacity theorem. No full decisive proof or implementation was inspected here.
- LOKA supplies inspected memory/routing implementation, but no capacity lower bound for a bounded temporal-version memory was established in the retrieved sections.
- Absence of a verified author repository in this packet means **access/provenance remains unknown**, not that code does not exist. Numerical reported outcomes have not been independently checked. The completed collision audit remains the parent’s next independent stage.

