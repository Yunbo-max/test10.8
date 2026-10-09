# Consistent LRA: bounded CPU research

## Current delivery authorization — 2026-10-09 12:29 Europe/London

The owner instructed “以后直接更新到main就行”. Current delivery is
`Yunbo-max/test10.8/main`, limited to `research/consistent-lra/`.
This supersedes all older branch prohibitions and delivery hints below.
The legacy `consistent-lra-rsi` branch is a read-only historical source.
Use one integration writer, current expected main head and exact commit/subtree
readback. Preserve other paths, every historical receipt and cumulative budget.
No scientific gate, resource limit or deadline is waived.
See [migration provenance](MAIN_DELIVERY_AUTHORIZATION_20261009.md).


**2026-10-09 restart:** the owner reopened this project using Research Autopilot Auto
0.2.0-autonomous.2. The new window ends at **18:15:43 Europe/London today**.
See [restart authorization and exact pending work](RESTART_AUTHORIZATION_20261009.md). Prior results and
negative history are retained; background activation is recorded separately.

**当前证据（2026-10-09）：** Landmark Stage A v2 已独立接受 35 个前缀、13 个对照的 455 条评分恒等式记录，以及全部 5,000 次更新的 65,000 条计时记录；38 个输出完整。实际整次 wall 79.251553 秒、CPU 78.791094 秒、RSS 190,604 KiB。[独立验收](LANDMARK_STAGE_A_v2_FULL_EVIDENCE_REVIEW.md)只接受这些有限恒等式、输出完整性和成本，不是全前缀性能胜负。原 v1 gzip 失败保留，根因未证明。

实数父构造的秩 61 精确有理数记录也已实际执行并完整独立复核：122 项 residue、122 项 secular/导数/归一化、61 项交叉权重，严格下界 `122/15>8`。原执行 wall 32.111198 秒、CPU 31.346881 秒；另外独立只读算术验收消耗 CPU 13.176209 秒，单独累计。[代码](formal_geometric_certificate.py)、[完整验收](FORMAL_CERTIFICATE_TARGET61_EVIDENCE_REVIEW_WINDOW02.md)。它验证实数父卡的有限恒等式，不生成或验证 v7 整数输入，也不计算完整 recourse。

完整 13 对照、5,000 前缀的 [Stage B 代码草案](run_landmark_stage_b.py)及[保留初审问题的独立复审](LANDMARK_STAGE_B_SOURCE_REVIEW.md)已生成，近零直接 SVD/残差回退、分母、初始与稳态 recourse、原始输出和归档均有实现；初审指出归一化分母和角色分类问题；一次修正后已通过独立源码审查，未导入/未执行。正式数值比较仍缺原生 evaluator 资格，不因代码或 Stage A 接受而绕过。累计 2 轮控制迭代、130 个登记任务、21 次执行尝试、至少 291.911595 秒实测 CPU；正式科学实验、新候选发现轮和合格论文均为 0。新颖性/优先权仍未结案。


新增隔离标量软件验收已真实运行：501 条记录全部通过，四个输出两次退出后哈希一致，整次 wall 1.155050 秒、CPU 1.095581 秒、RSS 37,044 KiB；[原始收集包](evidence/scalar-contract-02-collection.json)已保存，独立证据复审进行中。只检查冻结来源中的标量分支/分母/累计逻辑，不计算新的矩阵指标，不资格化完整 Stage B 或官方评分器。另有[整数见证生成设计](INTEGER_WITNESS_DESIGN_WINDOW02.md)等待独立设计审查，尚无整数生成源码或执行。

本项目使用 `Research_Autopilot/autonomous-rsi` 的机器审查流程，研究流式低秩近似的重构质量、子空间稳定性和计算成本。用户授权使用当前 ChatGPT Work 的 CPU，并要求一个 8 小时研究窗口。资源实测为 8 核 CPU 配额、8 GiB 内存上限；无需 GPU 或额外模型 API。

**当前已保存一个经两名独立审查者核验的正式反例：原论文“追加一行后的最优投影 recourse 至多为 8”引理，在其写明的实矩阵条件下不成立，即使最优投影唯一。进一步的独立审查确认：插入/删除序列也否定了无秩依赖的“精确最优动态维护总 recourse 为 O(n)”结论。近似算法的存在定理、原创性与可发表性仍需分别审查。**

最新独立审查给出了构造性的整数反例：秩 61、维度 122 时，追加一行使精确最优投影 recourse 大于 8；全部非空连续行块的非零奇异值条件数小于 4，每个整数元素最多 259 位。一般秩满足 recourse 大于 `2k/15−1/100`，整数位长为 `O(k+log k)`，幅值仍随秩指数增长。这加强了同一引理审计，不是新的近似算法，也没有推翻带 `M` 参数的近似存在定理。详见 [v7 推导](FORMAL_AUDIT_v7_EXPLICIT_INTEGER_BIT_BOUND_DRAFT.md)及[独立审查](FORMAL_AUDIT_v7_REVIEW.md)。历史 v4 密度证明及其首次更正永久保留。

已完成并独立核验 Landmark 全文件机械完整性，以及 Rice/Skin 真实数据上
8 个预声明 prefix 的评分恒等式检查、修复评分器的 25 项解析/代数
semantic oracle、强 FD 基线的 45 项来源/语义 oracle，以及作者 `ell+1`
FD 诊断的 58 项来源/语义 oracle。这部分早期工程检查可归因进程 CPU 为 2.084459 秒，
准备作业峰值 RSS 148,112 KiB；所有输入、日志、receipts 和原始 JSON 已保存。
这些是来源/工程资格，不是数值基线胜负、已验证新算法或论文分数。另有一次
经独立审查接受的 Rice Algorithm 4 全 3,000-prefix 成本/覆盖校准：pipeline
0.502147 秒、进程 CPU 0.498551 秒、峰值 RSS 120,220 KiB；完整逐-prefix raw
已无损压缩保存。它只资格化这条执行路径的成本与覆盖，不是完整 baseline
比较或 performance claim。

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
- [FD 来源/语义 oracle](FD_SEMANTIC_QUALIFICATION_20261009.md)、[计划审查](FD_SEMANTIC_ORACLE_PLAN_REVIEW.md)、[执行证据](FD_SEMANTIC_ORACLE_EXECUTION_20261009.md)与[证据复审](FD_SEMANTIC_ORACLE_EVIDENCE_REVIEW.md)
- [作者 FD 诊断资格化](AUTHOR_FD_DIAGNOSTIC_QUALIFICATION_20261009.md)、[源码审查](AUTHOR_FD_DIAGNOSTIC_SOURCE_REVIEW.md)、[计划审查](AUTHOR_FD_DIAGNOSTIC_PLAN_REVIEW.md)、[执行记录](AUTHOR_FD_SEMANTIC_ORACLE_EXECUTION_20261009.md)与[保留 provenance 更正的证据复审](AUTHOR_FD_SEMANTIC_ORACLE_EVIDENCE_REVIEW.md)
- [Rice 全前缀成本校准计划](BASELINE_CALIBRATION_PLAN_20261009.md)、[计划审查](BASELINE_CALIBRATION_PLAN_REVIEW.md)、[执行记录](RICE_ALG4_CALIBRATION_EXECUTION_20261009.md)与[证据审查](RICE_ALG4_CALIBRATION_EVIDENCE_REVIEW.md)
- [基线修复源码审查](BASELINE_DRAFT_REVIEW.md)
- [四类原生实验设计草案](NATIVE_PROTOCOL_DRAFT.md)
- [新颖性初步核查](NOVELTY_PRELIMINARY_20261009.md)与[继续工作指引](RESUME.md)

Landmark 大文件读取限制已通过固定 author Git blob 解决；完整作者 tree/ZIP
审计确认没有隐藏的独立官方 scorer。科学数值执行仍受官方可运行评分接口
及其 parity 缺口、完整原生性能基线、FD sensitivity/作者诊断的原生性能与四类 G01 阻塞。published random
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
