# 两条路线的论文、公开代码与数学来源审计

核查日期：2026-10-08。与 [数学分析](TWO_ROUTE_MATH_ANALYSIS.zh-CN.md) 配套。以下“优先”指与项目问题贴近、数学可用、来源可靠和公开实现可检查；不表示跨所有数据和硬件存在一篇统一最优论文。

这里记录论文版本和实际文件范围，不把检索到仓库等同于完成复现，也不把数据集仓库称为算法实现。原 [SOURCE_AUDIT.md](SOURCE_AUDIT.md) 保留此前研究轨迹；本表补充并更新本轮涉及的方法/代码读取范围。

## 路线 A 的优先阅读顺序

| 工作 | 本项目用途 | 主来源与状态 | 可检查发布 |
| --- | --- | --- | --- |
| OSFT / Sculpting Subspaces | 参数方向保护、保护与可学习空间的边界 | [ICLR 2026 官方论文](https://proceedings.iclr.cc/paper_files/paper/2026/file/22620cccae29bbb3f18d226ea0320ff5-Paper-Conference.pdf) | [mini_trainer 作者实现](https://github.com/Red-Hat-AI-Innovation-Team/mini_trainer/tree/fd5b552177bde9a551d30e73660d6a96205c97c0)；当前生产 revision 与论文实验 revision 的绑定未闭合 |
| SDFT / Self-Distillation Enables Continual Learning | 连续技能学习的蒸馏比较对象 | [arXiv 2601.19897v2](https://arxiv.org/abs/2601.19897v2)；本轮不以未单独核实的会议标签做排序 | [作者实现](https://github.com/idanshen/Self-Distillation/tree/d77573212fa0a3ae2eeb64b9b44db1c251f75e3e) |
| iSDFT | 信息目标与固定锚点；最新直接相关延伸 | [arXiv 2609.24646v2](https://arxiv.org/html/2609.24646v2)，2026 年 9 月预印本 | [作者实现](https://github.com/KickItLikeShika/iSDFT/tree/9a5f0d7b29af040ddc1195eb782d747e799a98cb) |
| DiSC / Updating Parametric Knowledge with Context Distillation Retains Post-Training Capabilities | 原始新文档的知识获取与后训练能力保留，连接文档适配方向 | [arXiv 2602.16093v1](https://arxiv.org/html/2602.16093v1)；读取页面标为 under review，会议发表未在本轮闭合 | [论文直接链接的作者实现](https://github.com/shankarp8/distillation-retains-capabilities/tree/db609cb678d9d824c9ad7edf644e1bdfeaee5d7f) |
| TALR / SFT Doesn't Always Hurt General Capabilities | 低学习率与 token 重加权；检验“仅因学习较少而保留”的简单解释 | [ICLR 2026 官方论文](https://proceedings.iclr.cc/paper_files/paper/2026/file/4e447acb68f57e29234bc0eb19896f11-Paper-Conference.pdf) | 未定位作者算法仓库；DiSC 作者仓库中有已读的第三方 TALR 基线，不能称作 TALR 作者代码 |

OSFT 与 iSDFT 是本轮参数几何和损失约束的直接数学入口。SDFT 是 iSDFT 的必要母方法比较对象；DiSC 数据契约为原始文档，不可直接与指令 SFT 宣称相同 setting。TALR 与低学习率 SFT 是必要的简单比较对象，而不是凭“简单”予以排除。

## 路线 B 的优先阅读顺序

| 工作 | 本项目用途 | 主来源与状态 | 可检查发布 |
| --- | --- | --- | --- |
| AlphaEdit | 真正公开的零空间编辑实现；精确/近似保护与编辑可行性的数学入口 | [arXiv 2410.02355v4](https://arxiv.org/html/2410.02355v4)；arXiv journal-reference 标为 ICLR 2025 Oral；本轮不依作者 README 独自确认奖项 | [作者算法实现](https://github.com/jianghoucheng/AlphaEdit/tree/b84624f44dfe8fc6cd9e41df916c44124a0c46dc) |
| History Matters / METO / AToKe | 当前事实更新与正确历史保留的直接任务前作 | [arXiv 2312.05497v3](https://arxiv.org/html/2312.05497v3)，作者 README 明确链接 AAAI 2024 论文 | [作者链接仓库](https://github.com/Arvid-pku/ATOKE/tree/a1b42e34e4130507220307ced3d681fb8719831f)目前只有 README 和三个数据集；未找到 METO 算法实现 |
| MTKE / SPIKE | 多粒度时间条件、历史保留与推理条件注入的近期工作 | [AAAI 2026 官方论文](https://ojs.aaai.org/index.php/AAAI/article/view/40107/44068) | [作者链接仓库](https://github.com/LLMs-TKE/MTKE/tree/757d8b555f26a5ae77f833176c47531c2241df7d)目前只有 README 和三个数据集；未找到 SPIKE 算法实现 |

AlphaEdit 是本轮可进行实现级数学核查的核心。METO/AToKe 和 SPIKE/MTKE 更直接覆盖时间知识语义，但作者链接的公开树不能支持“已拥有原算法训练实现”这一结论。没有在该仓库找到，并不证明世界上不存在其他发布渠道。

## 实现读取与固定 revision

### 1. OSFT

固定作者仓库 commit：
fd5b552177bde9a551d30e73660d6a96205c97c0。
实际 tree：
567888a52081fa155005d83af113b270cf1685f7。

已读：
- [osft_utils.py](https://github.com/Red-Hat-AI-Innovation-Team/mini_trainer/blob/fd5b552177bde9a551d30e73660d6a96205c97c0/src/mini_trainer/osft_utils.py)：create_svd_dict / reconstruct_weight_matrix，约 422–540 行；梯度/参数双侧因子投影，约 541–783 行；optim_wrapper，2481–2503 行。长文件只完成这些数学相关路径的 scoped read。
- [setup_model_for_training.py](https://github.com/Red-Hat-AI-Innovation-Team/mini_trainer/blob/fd5b552177bde9a551d30e73660d6a96205c97c0/src/mini_trainer/setup_model_for_training.py)：optimizer 构造及调用 osft_utils.optim_wrapper 的绑定片段，约 1338–1350 行。
- [train.py](https://github.com/Red-Hat-AI-Innovation-Team/mini_trainer/blob/fd5b552177bde9a551d30e73660d6a96205c97c0/src/mini_trainer/train.py)：OSFT CLI rank-ratio 和模型设置片段的定位；未完成全部训练、分布式和评价路径审计。
- [Readme.md](https://github.com/Red-Hat-AI-Innovation-Team/mini_trainer/blob/fd5b552177bde9a551d30e73660d6a96205c97c0/Readme.md)：OSFT 与 CLI 部分。

论文读取重点为 §3.1–3.8；未完成 32 页全部附录/实验的资格核查。论文按权重做 SVD，并用上一任务样本的层输入/输出相似度选择保护比例，不能假定完全不访问增量旧数据。

代码把高因子冻结、低因子投影到高因子的正交补，并在 AdamW 更新之后再次投影参数。该 correction 已经实现。数学分析 MC-A3 显示：论文完整梯度的“去掉高—高块”与当前代码的双侧因子约束，不是自动相同的矩阵空间。不能将当前公开 main 当作已验证的论文精确复现。

### 2. SDFT

固定 commit：
d77573212fa0a3ae2eeb64b9b44db1c251f75e3e。

已读：
- [README.md](https://github.com/idanshen/Self-Distillation/blob/d77573212fa0a3ae2eeb64b9b44db1c251f75e3e/README.md)，全文。
- [distil_trainer.py](https://github.com/idanshen/Self-Distillation/blob/d77573212fa0a3ae2eeb64b9b44db1c251f75e3e/distil_trainer.py)：本轮补读 compute_loss / _compute_loss，约 1585–1705 行，包括教师、学生输入拼接、mask、各 KL 分支、importance correction 和平均方式。生成/teacher 配置只定位了相关片段，长 trainer 未全量审计。

作者 README 明确更正：其结果使用 on-policy sampling 和 per-token forward KL。实际 alpha=0 分支调用 KL 函数的顺序也给出 KL(teacher || student)；代码另支持 reverse 与混合分支，复现必须绑定配置。

作者推荐单 H200。固定树的 tool-use evaluator 是 eval_tooluse.py，而 README 的一个示例调用 eval_tooluse_simple.py；不能把该 README 命令不经核查当作可运行交付。原生评价与完整 sequential 运行契约仍未闭合。

### 3. iSDFT

固定 commit：
9a5f0d7b29af040ddc1195eb782d747e799a98cb。
此前核查 tree：
aea690b3548e1d3ab75e63f6c93a2c218fc9bb2d。

已读：
- [README.md](https://github.com/KickItLikeShika/iSDFT/blob/9a5f0d7b29af040ddc1195eb782d747e799a98cb/README.md)，全文。
- [distil_trainer.py](https://github.com/KickItLikeShika/iSDFT/blob/9a5f0d7b29af040ddc1195eb782d747e799a98cb/distil_trainer.py)：compute_q_star_logps，92–143 行；_compute_loss 的目标构造、KL、mask、固定锚点，1714–1857 行。此前已读 teacher 设置及 main；长 trainer 仍是 scoped read。

论文读取 §2–3 的约束与固定锚点、相应方法解释；此前还有 scoped 实验与消融读取，不代表完成全部原生 scorer 资格审查。

实际 q* 求解约束为 E_q log(T/p) >= rho KL(T||p)，随后 detach。锚点使用与当前学生相同的输入/完成前缀，forward KL(base || student)。MC-A2 推导出 rho=0 的边界通常仍有目标移动；不能把代码注释中的“none”直接作为零移动数学结论。

README 明确训练保留学生、EMA 教师、冻结 base 三份模型，并使用 colocated vLLM 与 BF16。没有本项目 22 GB 单卡可行性证据。

### 4. DiSC

固定 commit：
db609cb678d9d824c9ad7edf644e1bdfeaee5d7f。
实际 tree：
e547f3f25f80888d19effd793f8df1033d04dca0。

已读：
- [README.md](https://github.com/shankarp8/distillation-retains-capabilities/blob/db609cb678d9d824c9ad7edf644e1bdfeaee5d7f/README.md)，全文；默认分支读取随后在上述 immutable commit 回读匹配。
- [src/disc/objectives.py](https://github.com/shankarp8/distillation-retains-capabilities/blob/db609cb678d9d824c9ad7edf644e1bdfeaee5d7f/src/disc/objectives.py)，全文：CE、KL regularization、TALR、DiSC、CD-base。
- [src/disc/trainer.py](https://github.com/shankarp8/distillation-retains-capabilities/blob/db609cb678d9d824c9ad7edf644e1bdfeaee5d7f/src/disc/trainer.py)：split-level 训练与真实 backward / optimizer.step，约 197–289 行；其他路径仅定位，未全读。
- 尚未读完 splits.py、数据 producer、域任务 evaluator、通用 evaluator 和 checkpoint selector。

论文 §2–3 和 §4 的 setting、目标、原生数据/评价说明已 scoped read。作者模型原本从 post-trained policy 初始化；适配输入是原始文档。读取源页面目前为 v1/preprint，不因检索摘要或 repo 描述便升级为确认会议录用。

实际 DiSC 是 teacher-forced 后文 token 上的 forward KL，含温度平方因子，多个切分点等权。当前循环对每个切分点分别调用两个模型；论文讨论的 packed 两次 forward 优化未在已读路径出现。完整后文序列 KL 与此 token 目标也不能无需前缀分布条件就宣称等价。

这份作者代码还包含第三方 TALR 基线。它实现 detached、带 floor 的正确 token 概率重加权；动态 tau、probability clamp 和 normalization 默认值仍需与 TALR 原论文逐项对齐。不能将第三方可运行性当成原作者结果复现性。

### 5. TALR

主来源固定为 ICLR 2026 官方文集 PDF：
4e447acb68f57e29234bc0eb19896f11。

本轮读取 §4 的熵正则权重推导与 Algorithm 1，并读取 Appendix B 的部分理论设置。其理论用指数倾斜作为分析 surrogate，不能不加条件地视为实际 SFT 的精确动力学。更完整的理论条件与全部实验/评价仍需阅读。

论文算法使用未按总权重归一化的 detached 权重与 floor。MC-A4 另外给出固定温度下的梯度等价推导。不能用 normalized simplex 解直接代替实际更新。

检查官方 PDF、作者主页和代码检索后，尚未定位作者算法仓库。公开的第三方实现位置见上面的 DiSC objectives.py。本轮未宣布不存在作者代码，也未宣布第三方默认配置与原论文相同。

### 6. AlphaEdit

固定 commit：
b84624f44dfe8fc6cd9e41df916c44124a0c46dc。
实际 tree：
d853eeb4bc59a6ad32758cfb7d6eee40c21586ff。

已读：
- [README.md](https://github.com/jianghoucheng/AlphaEdit/blob/b84624f44dfe8fc6cd9e41df916c44124a0c46dc/README.md)，全文。
- [AlphaEdit_main.py](https://github.com/jianghoucheng/AlphaEdit/blob/b84624f44dfe8fc6cd9e41df916c44124a0c46dc/AlphaEdit/AlphaEdit_main.py)，全文：目标值/激活、残差、多层分摊、投影 solve、cache_c 更新及 mom2 调用。
- [compute_ks.py](https://github.com/jianghoucheng/AlphaEdit/blob/b84624f44dfe8fc6cd9e41df916c44124a0c46dc/AlphaEdit/compute_ks.py)，全文。
- [compute_z.py](https://github.com/jianghoucheng/AlphaEdit/blob/b84624f44dfe8fc6cd9e41df916c44124a0c46dc/AlphaEdit/compute_z.py)，全文。
- [experiments/evaluate.py](https://github.com/jianghoucheng/AlphaEdit/blob/b84624f44dfe8fc6cd9e41df916c44124a0c46dc/experiments/evaluate.py)：DS_DICT、P/cache_c 初始化和 get_project，约 51–72、187–216、426–447 行；该长文件没有全部闭合。
- [phi-1.5.json](https://github.com/jianghoucheng/AlphaEdit/blob/b84624f44dfe8fc6cd9e41df916c44124a0c46dc/hparams/AlphaEdit/phi-1.5.json)，全文。
- [counterfact.py](https://github.com/jianghoucheng/AlphaEdit/blob/b84624f44dfe8fc6cd9e41df916c44124a0c46dc/dsets/counterfact.py) 与 [eval_utils_counterfact.py](https://github.com/jianghoucheng/AlphaEdit/blob/b84624f44dfe8fc6cd9e41df916c44124a0c46dc/experiments/py/eval_utils_counterfact.py)，全文。

论文 §3 与附录 B.2–B.4 的相关零空间/解法片段已读；全部实验与统计 producer 不代表已资格审查。get_project 以统计矩阵奇异值低于 nullspace_threshold 选择方向。phi-1.5 配置使用 threshold=0.02、L2=10、mom2_dataset=wikipedia、mom2_n_samples=100000。

compute_z 优化 latent delta，而非直接只优化权重 ridge；局部 KL 调用的顺序对应 edited distribution 到初始 distribution，另有范数限制。MC-B2 的闭式解分析只对应随后固定 key/value 的权重步骤。

原生 CounterFact loader 可自动取得未固定远端 JSON；本轮只读 loader，没有下载数据。scorer 分别读 rewrite、paraphrase、neighborhood、generation 字段；概率条目实际存储平均负对数概率，correct 则检查目标序列每个 token 的 argmax。生成侧还有 n-gram entropy 与 TF-IDF reference score。完整 producer/汇总与数据版本尚未闭合，更不能把这些指标当作时间历史保留评价。

该方法额外访问 Wikipedia 激活统计，不应与只可访问当前新增数据的方法默认为相同信息条件。README 要求至少一张 48 GB A40；小模型配置存在不代表本项目 22 GB 可运行。

### 7. METO / AToKe

固定 commit：
a1b42e34e4130507220307ced3d681fb8719831f。
实际 tree：
f3ab972934e4dd7c2f1e11f1bbc88d0c9f4ce54e。

递归 tree 只有 README.md 和 datasets/AToKe-SE.json、AToKe-ME.json、AToKe-EE.json。README 全文已读，其 METO 小节为空。本轮未在该公开树发现方法或评分器代码。

论文任务定义与 METO 方法部分已 scoped read。它研究事实区间、当前/历史提问，并把模型时间当前事实和后续事实联合编辑，添加时间预测目标；更早历史未全部显式 replay。

README 展示 requested_rewrite、time_true/time_new、history_evaluation、answer_alias/new_answer_alias 等字段及 HRS/HES/CRS/CES 的评价维度。展示例子是 README 格式说明，不能冒充已读取真实原生数据行。数据内容、有效样本筛选、区间边界、别名匹配和 scorer 仍未闭合。

因此可引用任务与方法说明，可核查公开数据的存在，但目前不能交付“作者 METO 实现已可复现”的结论。

### 8. SPIKE / MTKE

固定 commit：
757d8b555f26a5ae77f833176c47531c2241df7d。
实际 tree：
bca5454fef80141f772a88309f6f805f402c1a55。

递归 tree 只有 README.md 与三个数据文件：
datasets/MTKE-DG.json；
datasets/MTKE-SG .json（SG 后有一个实际空格）；
datasets/cMTKE_chains.json。

README 全文已读。README 中的 SG/MG 文件描述与实际 tree 命名不同，不能直接照抄示例路径。没有 SPIKE 方法实现或 scorer 出现在该树。

官方 PDF 的任务/筛选、原生指标及 SPIKE 方法/注入公式已 scoped read。方法用 start/end/subject anchor 的 CE 目标，保存增量键表，再按时间粒度与关系匹配选择注入；所读目标公式不能单独推出稀疏性，具体稀疏规则实现仍待定位。它的推理机制和额外存储应单列为比较条件。

论文指标包括新事实置信度增加的 SR、历史置信度下降的 NegSR，以及 TC、TTR、HTC。它们与通用技能评价不同。模型相关的旧知识正确/新知识错误筛选、实际概率/计数实现、样本内容和最终 scorer 均尚未闭合，不能自行编写简化版本后宣称复现原生指标。

## 来源身份与版本记录

| 当前记录身份 | 实际版本 | 与其他版本/名称的处理 |
| --- | --- | --- |
| ICLR-2026:22620cccae29bbb3f18d226ea0320ff5 | 官方 PDF | OSFT 为该论文中的方法名；没有自动合并未核查的其他稿件 |
| arxiv:2601.19897 | v2 | SDFT README 明确链接该 work；固定代码与 v2 实验的精确绑定未确认 |
| arxiv:2609.24646 | v2 | iSDFT 与 SDFT 为不同论文；不会按同一 work 去重 |
| arxiv:2602.16093 | v1 | 论文正文直接提供 DiSC 作者代码链接；未确认会议稿别名 |
| ICLR-2026:4e447acb68f57e29234bc0eb19896f11 | 官方 PDF | 检索也出现 arXiv 2509.20758，本轮用官方 PDF 记录，不把未经版本链接核查的稿件混读 |
| arxiv:2410.02355 | v4 | arXiv journal-reference 提供 ICLR 2025 Oral 元数据；不靠标题相似合并 |
| arxiv:2312.05497 | v3 | 作者 README 的 AAAI 2024 标签和论文链接提供工作身份连接 |
| AAAI:article/40107 | 官方 PDF | README 明确对应 MTKE 工作；SPIKE 是方法、MTKE 是 benchmark，不能计成两篇独立论文 |

## 信息条件、评价与资源的共同未闭合项

1. replay 尚未禁止或确定。区分原预训练数据、旧增量数据、公共校准文本、教师副本和推理键表，才能公平比较。
2. 论文原生训练/评价数据版本、真实样本、所有 producer、scorer 和汇总逻辑尚未完成全链核查。本轮读取代码不等于接受其任意默认设置。
3. 本项目没有科学训练、推理、数值检验或 benchmark 结果。数学文档的“解析反例”也不是实验表现证据。
4. 单 2080 Ti、22 GB 为用户报告值；dtype、主机、吞吐和显存峰值未测。不能把单 H200、48 GB A40、多模型 BF16 或 FP32 大模型条件直接移植到该卡。
5. 数学分析中的覆盖矩阵与激活统计，只是可能的诊断对象，不构成已验证的低成本估计器。
6. 现有正交/零空间方法、固定锚点、信息投影、时间历史保留和条件注入形成明确前作重合。本轮没有完成隔离的对抗新颖性审计。
7. 原 SOURCE_AUDIT、时间 CPT/Kairos、Sampling-SFT、unlearning/recovery 相关记录仍有效；SoFT 及 Null-Basis LoRA（arXiv 2609.25618）等近邻线索还需要完整方法、作者实现与原生协议阅读。未读全文的最新线索不用于证明 gap 或新颖性。

## 对当前研究方向的约束

可以继续提出并分析“有效旧行为的覆盖与必要新更新空间”这一问题；不能只把正交投影、初始模型 KL、加时间标签或 sparse delta 的拼装当作新贡献。

下一阶段应先确认：在本项目可获取的信息与原生评价条件下，强/simple 方法还留下什么重要残余问题；再确定数学上不同且有可区分预测的构造。当前六个 inquiry records 是解释与条件推导，不是已经通过评审的新方法候选池。
