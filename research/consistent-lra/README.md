# Consistent LRA: bounded CPU research

本项目使用 `Research_Autopilot/autonomous-rsi` 的机器审查流程，研究流式低秩近似的重构质量、子空间稳定性和计算成本。用户授权使用当前 ChatGPT Work 的 CPU，并要求一个 8 小时研究窗口。资源实测为 8 核 CPU 配额、8 GiB 内存上限；无需 GPU 或额外模型 API。

**当前已保存一个经两名独立审查者核验的正式反例：原论文“追加一行后的最优投影 recourse 至多为 8”引理，在其写明的实矩阵条件下不成立，即使最优投影唯一。进一步的独立审查确认：插入/删除序列也否定了无秩依赖的“精确最优动态维护总 recourse 为 O(n)”结论。近似算法的存在定理、原创性与可发表性仍需分别审查。**

新的修正审查进一步确认：该动态反例可逐秩整数化，仍排除秩/维无关常数，但没有给出整数幅值或位长的多项式界，因此不触及带 `M` 参数的近似定理。在线 PCP 主来源和一个保守的二次秩依赖回退也已核验；该回退只在同时满足所有前缀 PCP 与样本数界的高概率事件上成立，并不是新算法。

已完成并独立核验 Landmark 全文件机械完整性，以及 Rice/Skin 真实数据上
8 个预声明 prefix 的评分恒等式检查，以及修复评分器的 25 项解析/代数
semantic oracle。累计可归因进程 CPU 为 1.571700 秒，
准备作业峰值 RSS 148,112 KiB；所有输入、日志、receipts 和原始 JSON 已保存。
这些是来源/工程资格，不是数值基线胜负、已验证新算法或论文分数。

- [固定版本反例](FORMAL_AUDIT_v2.md)与[两份独立审查及精确阈值说明](FORMAL_AUDIT_v2_REVIEW.md)
- [动态更新扩展](FORMAL_AUDIT_v3_EXTENSION.md)、[条件数补充](CONDITION_SCOPE_SUPPLEMENT_DRAFT.md)与[独立审查](FORMAL_EXTENSION_REVIEWS.md)
- [整数输入扩展](FORMAL_AUDIT_v4_INTEGER_DENSITY_DRAFT.md)与[保留首次失败的独立复审记录](FORMAL_AUDIT_v4_REVIEW.md)
- [在线 PCP 来源和保守回退](SAMPLING_SOURCE_QUALIFICATION_20261009.md)与[独立复审记录](SAMPLING_SOURCE_QUALIFICATION_REVIEW.md)
- [谱投影函数的主文献等价性核查](LITERATURE_EQUIVALENCE_20261009_3.md)
- [真实 CPU 准备证据](PREPARATION_REVIEW_20261009.md)
- [Landmark 来源与执行证据](LANDMARK_SOURCE_ACQUISITION_20261009.md)、[独立来源审查](LANDMARK_SOURCE_QUALIFICATION_REVIEW.md)与[完整性执行](LANDMARK_INTEGRITY_EXECUTION_20261009.md)
- [作者归档与 scorer 缺口审计](AUTHOR_ARCHIVE_SCORER_AUDIT_20261009.md)
- [Rice/Skin 身份计划审查](RICE_SKIN_IDENTITY_PLAN_REVIEW.md)与[执行证据](RICE_SKIN_IDENTITY_EXECUTION_20261009.md)
- [随机族不可精确复现边界](RANDOM_FAMILY_IDENTITY_20261009.md)与[独立复审](RANDOM_FAMILY_IDENTITY_REVIEW.md)
- [评分器 semantic oracle](EVALUATOR_SEMANTIC_ORACLES_20261009.md)、[初审/修复复审](EVALUATOR_SEMANTIC_ORACLE_PLAN_REVIEW.md)、[执行证据](EVALUATOR_SEMANTIC_ORACLE_EXECUTION_20261009.md)与[证据复审](EVALUATOR_SEMANTIC_ORACLE_EVIDENCE_REVIEW.md)
- [基线修复源码审查](BASELINE_DRAFT_REVIEW.md)
- [四类原生实验设计草案](NATIVE_PROTOCOL_DRAFT.md)
- [新颖性初步核查](NOVELTY_PRELIMINARY_20261009.md)与[继续工作指引](RESUME.md)

Landmark 大文件读取限制已通过固定 author Git blob 解决；完整作者 tree/ZIP
审计确认没有隐藏的独立官方 scorer。科学数值执行仍受官方可运行评分接口
及其 parity 缺口、FD 资格、完整原生基线与四类 G01 阻塞。published random
stream 已被限定为不可精确复现；只能使用预先冻结的新 seed 作为 prospective
family instance。独立的形式证明、相关文献和下游定理依赖审查继续进行。

成果位于 `Yunbo-max/test10.8` 的独立 `consistent-lra-rsi` 分支。仓库原来的持续学习项目仍由其原分支管理。该研究目标单独计时，不借用原项目的资源、审批或结果。

- [初始目标及停止规则](GOAL.md)
- [论文、代码和数据来源](SOURCES.md)
- [独立源码审查与修复要求](BASELINE_AUDIT.md)
- [执行范围和环境](EXECUTION_SCOPE.md)
- [接续检查点](workflow-checkpoint.yaml)
- [后台任务提示](AUTOMATION_PROMPT.zh-CN.md)

每次后台续做应恢复该分支的最新检查点，完成实际工作并保存真实产物。按小时触发不等于连续占用 CPU，也不保证同一个文件系统在下一次运行仍然存在。代码、推导及小型实验原始记录必须在每次结束前提交并读回。

首先修复公平比较的基础，再独立审查约 20 个有数学依据的候选，按整个候选池排序并选择最多 15 个合格候选进入实现和完整实验设计。新颖性冲突、数学反例、负结果和未完成比较都要保留。不同参数配置不能被当成不同论文。

用户希望找到多个可以超过原方法的论文方向。是否有可发表的贡献、是否超过公平基线，均为待验证结果。只有当前、独立核验的证据支持时才写结果型论文；不足时交付数学记录、代码、完整设计和明确的剩余工作。
