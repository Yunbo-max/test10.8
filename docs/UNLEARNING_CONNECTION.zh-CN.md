# LLM unlearning 的微调方法与本项目的连接

日期：2026-10-08。用户补充：同时考察 LLM unlearning 中的微调/SFT 路线。本轮扩大相邻工作审查；原有“时间到来的多数据集连续 SFT、选择性更新与能力保留”主线继续有效。

## 1. 三种任务的边界

| 任务 | 希望改变什么 | 希望保留什么 |
|---|---|---|
| 连续 SFT | 吸收新知识与新技能 | 仍有效知识、历史事实、其他能力 |
| LLM unlearning | 去掉指定训练数据的影响或指定知识/行为 | 其他知识与模型效用 |
| 时间知识更新 | 当前条件下过时的答案 | 正确历史版本、稳定事实与其他能力 |

LLM unlearning 中确实有参数微调路线，但标准正向 SFT、梯度上升式遗忘、NPO/SimNPO 是不同训练目标，不能都称作普通交叉熵 SFT。面向指定数据移除时，常用目标参照是不包含 forget set 的重训练模型，而非只让模型拒答。

教学例子沿用假想公司：2024 年甲负责、2026 年乙接任。“现在谁负责”应该变成乙，“2024 年谁负责”仍应该是甲。因此旧版本事实不能仅因为过时就被整体加入删除集合。研究对象需要包含查询时间与事实适用时间。

## 2. 本轮读到的直接相关工作

- **SimNPO / NPO**：提供 forget 目标与 retain 目标的优化入口。参考模型、样本难度与回答长度已经有专门分析，应列为相邻基线线索，不能把自适应遗忘权重或取消参考模型直接算作新方法。
- **FIT to Forget**（2601.21682v2）：已研究连续删除请求、效用保留以及恢复抵抗。本轮读摘要，并检索正文相关范围；实现与原生 PCH 评价资格尚未完成。不能把“多轮 unlearning 同时保留通用能力”当成未经研究的新设定。
- **Unlearning Isn’t Deletion**（2505.16831v3；PMLR 306）：读取任务定义、可逆/不可逆与灾难性/非灾难性的划分、受限 relearning 规则及附录 A.4 的数据来源对照。已有恢复测试包括 forget、retain、无关数据微调；“后续微调会恢复部分被压制的信息”是已有实验证据，不是本项目的新发现。这里的不可逆性依赖规定的恢复预算与数据来源，不能由失败恢复证明绝对删除。
- **TOFU**（2401.06121v1）：读取任务定义与 §2.2 原生评价说明。其实体级删除目标与时间版本保留不同，不能独立覆盖本项目。它可为相邻遗忘问题提供公开评价参考，尚未选作完整实验协议。

来源：
<https://arxiv.org/html/2410.07163v4>
<https://arxiv.org/html/2601.21682v2>
<https://proceedings.mlr.press/v306/xu26cd.html>
<https://arxiv.org/html/2505.16831v3>
<https://arxiv.org/html/2401.06121v1>

## 3. 实际数学核对：SFT 与遗忘的梯度方向不同

固定一个原生样本 (x,y)，参考模型 p_ref 冻结，相关概率为正，β>0，令
\[
r_\theta=\log p_\theta(y|x)-\log p_{\rm ref}(y|x).
\]
标准 SFT 的损失是 \(-\log p_\theta(y|x)\)。NPO 的 forget 项为
\[
\ell_{\rm NPO}=-\frac2\beta\log\sigma(-\beta r_\theta).
\]
直接求导：
\[
\frac{\partial\ell_{\rm NPO}}{\partial r_\theta}
=2\sigma(\beta r_\theta),\qquad
\nabla_\theta\ell_{\rm NPO}
=2\sigma(\beta r_\theta)\nabla_\theta\log p_\theta(y|x).
\]
因此在理想的一阶梯度下降步中，单独的 NPO forget 项沿降低该指定回答 log 概率的方向更新；正向 SFT 沿提高其 log 概率的方向更新。其权重随概率比改变，范围在 (0,2)；权重有界不代表神经参数梯度或整个模型变化有界。

这复核已有 NPO 的梯度结果，不是新推导贡献。它没有证明知识彻底删除、其他能力保留或多轮训练稳定，也不是 Adam/共享参数/多目标训练的精确轨迹结论。

数学操作：将目标写成固定参考下的 log 概率比，应用链式法则，核对真实代码的负号与序列归约。保留上述假设，不据此生成已获资格的新方法。

## 4. 作者代码与原生评价核对范围

作者仓库：<https://github.com/OPTML-Group/Unlearn-Simple>
固定 commit：3083017cb317753725f35cc404c2d5aede1242ef。
实际 tree：1a50930a229e7ec3983eb16578f18c6afcbb9ab2。

本轮读取：
- 完整根 README。
- TOFU/dataloader.py 的 GA、retain fine-tuning、GradDiff、KL、NPO 与 SimNPO 相关损失分支（148–211、269–357）；未完成全文件阅读。
- 完整 TOFU/config/forget.yaml、model_config.yaml、eval_everything.yaml。
- TOFU/TOFU_data/forget01.json 的实际内容；这是扩展名为 .json 的 JSONL，40 条作者发布的原生问答，并非本项目手工生成。
- TOFU/utils.py 的模型效用与 forget-quality 聚合函数。遗忘质量采用与 retain-only 参照的 truth-ratio 分布 KS 检验；较大 p 值不能单独证明分布等价或正式删除保证。模型效用聚合涉及 retain、real authors、world facts。

源码中的 NPO 分支用当前/参考序列 NLL 差构建 log 概率比；SimNPO 分支按监督 token 数归一化，并可与 retain CE 联合。KL 与归约、mask、完整 loader/evaluator 仍需联合检查。

资格限制：未读完完整 evaluator、所有原生评价文件、retain-only 参照的版本与来源链；未执行任何科学代码。作者默认配置为 7B 且保存路径标记 8GPU；论文资源为 8 张 A6000。虽然模型配置出现较小模型条目，也不能据此声称单张 22GB 2080 Ti 已可直接运行或完成完整比较。继续沿用本项目原生 Conda、Web/Local 分工与有限周期。

## 5. 对当前方向的影响

把 unlearning 加入已有工作的对照范围，进一步关注两个概念问题：

1. 保护旧能力与抑制过时的当前答案，是否涉及不同保护对象与信息覆盖？
2. 后续新数据 SFT 能否继续保留正确历史与技能，同时避免已纠正的旧错误回答重新成为当前答案？

第二个问题要对照已有恢复、连续遗忘与时间知识编辑工作，不能把“反弹”本身当成原创。候选差异必须最终落在真实机制和已有方法未解决的后果上。

最简单替代解释仍包括：校准的小学习率 SFT、允许访问的数据重放、既有时间条件目标、既有 retain CE/KL、NPO/SimNPO 和前轮 iSDFT。它们目前是应资格化的比较线索，尚不是已完整验证的本机实验矩阵。

本轮没有选择新的方法、增加科学评价结论或改变数据访问假设。已有三份数学分析继续有效；方法候选数仍为 0。下一步继续检索/推导与原生问题资格，完成完整候选审查后再进入代码与实验设计。
