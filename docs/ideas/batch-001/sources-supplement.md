# 补充检索与实现来源（2026-10-08）

这是事实来源包，不是新颖性判决。检索/代码为静态阅读，无训练、数值实验、推理或 scorer 执行。直接源码访问的失败保留为访问未知，不作不存在判断。

## PaRSP / ACL 2026

- 官方论文与 metadata：[ACL Anthology](https://aclanthology.org/2026.acl-long.1244/)、[PDF](https://aclanthology.org/2026.acl-long.1244.pdf)。论文 21 页；本轮 scoped read §3.2/参数约束、Appendix A.3 Eq.8 和 P15 校准/Task0部分，未声称全量资格核查。
- §3.2 以旧输入零空间、uncentered covariance 和空间 mask 约束更新。Appendix A.3 Eq.8 使用 PSD 和的零空间等于各零空间交集，递归累加各旧任务 covariance；此算法数学组件是已有工作。P15描述每任务256训练例校准并用通用 Task0 anchor。已读部分未给出过时“当前角色”退休和显式历史角色重新插入的规则；语义差异需进一步查，不是“没有前作”的结论。
- 作者仓库 [JinhuiBot/PaRSP](https://github.com/JinhuiBot/PaRSP)，固定 commit `00685fe4f9086f03ac1d1a725dcb280714e6125a`，tree `b15ca6e6b85df3db9117951a300f4f2ece80d571`。读取 README 全文和 [parsp/methods/projection.py](https://github.com/JinhuiBot/PaRSP/blob/00685fe4f9086f03ac1d1a725dcb280714e6125a/parsp/methods/projection.py) 全文，blob `05fe46f4f870c3c629d7f247c2ef3f67e4c559ae`。
- `common_null_space_projector_sum_method_llama/qwen` 用 CPU float32 eigh，先按 `rcond*max_eig` 选 tail，再在维数不足 `min_ratio` 时强制选择至少该比例的小特征值方向。函数默认 min_ratio=.2，hook 注册默认 .3；实参绑定仍未检查。该近似选取不自动等同于 exact nullspace。
- `register_nullspace_hooks_llama/qwen` 的 weight gradient hook 返回 `grad @ projector`；此文件是梯度 hook，不能据此声称实际 Adam step 已在零空间，也不能据此断言完整训练器有错误。完整 optimizer/binding、covariance producer、mask、原生数据与 scorer 尚未核查。
- README 提供 TRACE/LS/通用 anchor 路径。实际树存在 `parsp/engine/evaluator_llama.py`/`evaluator_qwen.py`、`parsp/data/loader.py` 与 CL JSON 数据；仅位置可见，未读实际样本/评分，也未下载。没有 22GB 单卡运行资格。
- 关联：I04 additive guard 对照；I05 coverage；I09 approximate/partial fixed-input scope；I10 actual-step audit；I15 weak-mode bounds。此来源不批准相关新方法。

## VR-MCL / ICLR 2024

- [官方30页 PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/0b6df1a973b82b3cf7fadca6c387ae5a-Paper-Conference.pdf)：Meta Continual Learning Revisited: Implicitly Enhancing Online Hessian Approximation via Variance Reduction。读取 §2–4 的近似对象、§4.1 Eq.4 更新及局部方差解释、§5 相关对照、Appendix E 算法定位；没有复现或完整证明审定。
- Eq.4 在相邻参数上重用当前 replay batch 的 hypergradient，用 momentum 形成 variance-reduced meta-update；§4.2 将其联系到 implicit Hessian 近似/罚项。随机记忆样本导致曲率估计错误与 forgetting 的关联已被明确研究。
- 这与 I21 的“固定新数据 mixture mean、普通 SGD 有限小步、source-count covariance 及 source 分层”是不同对象；是否存在覆盖 I21 全部主张的更直接方法仍未解决。不能因为对象不同就自动批准原创性。
- 论文链接 `https://github.com/WuYichen-97/Meta-CL-Revised`，本轮 GitHub API读取返回404；未取得可读 author implementation。代码、native vision data/scorer 与资源未知。
- I21 的总方差分解与 Neyman allocation 是标准统计工具；本轮没有捕获 Neyman 原始论文 span。正式优先权/代码投资前需继续检索 SGD noise、stratified SFT、loss-aware sampling、variance-reduced CL、Fisher-weighted allocation，并做 citation expansion。

## Dynamic Orthogonal Continual Fine-tuning

[OpenReview forum 14Sq0m94oA](https://openreview.net/forum?id=14Sq0m94oA) 的检索摘要指向 representation drift/动态保护；页面读取被 browser verification 挡住。完整方法、作者 code、原生 protocol 未读，作为 I09 的高风险邻居保留。摘要不支持机制等价判断。

## 本轮检索边界

- 原20卡先冻结再按目标、约束、update、state/information、预测和别名检索，新增 I21 再单独检索；检索 dated snapshot 为2026-10-08，覆盖具体 source 的版本必须独立记录。
- 辅助 query families：temporal guard retirement/history/covariance downdate；cumulative KL/fixed reference/Hellinger；margin-constrained continual SFT；gradient noise/covariance/stratified/Neyman/SGD forgetting。检索可命中综述/二手页面，但技术映射仅用上述 primary/full-text 与独立包内 primary来源。
- 完整两轮无高风险新族、所有必要 aliases/citation expansion、全部 native data/scorer、originality/IPCG 与 empirical residual 尚未闭合。不能称完成 novelty saturation，也不能将代码不可读作为原创证据。
