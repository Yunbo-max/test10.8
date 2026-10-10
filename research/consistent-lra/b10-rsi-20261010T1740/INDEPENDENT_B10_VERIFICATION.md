# B10 候选池独立数学/方法核验

日期：2026-10-10  
角色：独立数学/方法核验者（未继承候选作者的结论）  
被核文件：`B10_CANDIDATE_POOL_DRAFT.md`  
被核文件 SHA-256：`c945cae0607bd824be488c10253026a0ca5d4ac41883a990ef2d476e4205888a`

## 0. 结论先行

**总判定：FAIL。当前不允许进入新候选的代码设计。**

理由不是基本投影代数整体错误，而是代码边界所需的“已验证候选池与 Top-15 选择”尚未成立：

1. $D(P,P_0)$、D1、D2、D3 的核心恒等式成立；D4 的跨参数单调不等式也成立。
2. D4 从单调性跳到“可二分得到最大重叠可行点”仍缺退化特征值处的集合值处理；任意 deterministic tie rule 可以在同一个 μ 上给出可行或不可行的不同最优投影。
3. C12 的“minimum/first”措辞只在明确的主角区间、方向、精确目标与全根选择规则下成立；用严格下界 $L<\mathrm{OPT}$ 时，得到的是对更强测试的最小 recourse，不是对原始 (F) 的最小 recourse。
4. C20 的 lower-bound 方向正确，但前提必须是对 top-$k$ Ky Fan 和的**经认证上界**；普通 Ritz 值通常是相反方向，不能直接代入。
5. 20/20 张卡在文字结构上都有六个字段，排名也确实列出 20 个唯一 ID、Top-15 也确实是唯一的前 15 个；但这不是 20 个经验证、语义独立的方法。多个条目是同一算法族的 solver、basis policy、ablation 或 certificate component。
6. 排名不能由给出的四个 ordinal 分数和 tie-break 规则复现，且存在显式 Pareto dominance 反序。
7. Hara--Yoshida (AISTATS 2026) 的公式和官方实现已确认与 C10 的 $G+\mu P_0$ top-$k$ 核心机制相同；C10 只能作为归因后的 prior-art control。C14/C15 是该已知核心的受限版本/参数搜索包装，不能作为独立新方法计数。

允许的下一步仅是：修订数学陈述、合并/重分类重复族、完成逐卡一手来源碰撞审计、重做可复现排序并再次独立核验。已有的 B09 控制实现不因本报告失效；本判定只阻止以本候选池为依据的新方法代码设计。

## 1. 判定口径与独立性

- `PASS`：陈述按其明确假设成立，或结构要求完整满足。
- `CONDITIONAL`：核心可成立，但必须补充条件、收窄结论或补齐证据后才可使用。
- `FAIL`：当前陈述过强、选择不可复现、语义不独立，或缺少跨越代码边界所需证据。

我独立重做了代数。随后只把现有 `verify_candidate_identities.py` 与 `B10_IDENTITY_CHECK.json` 当作补充材料审阅；没有用其 `passed: true` 代替证明。该脚本自己注明 D4 随机样本“ties have probability zero”，没有测试本报告给出的 tie 反例，也没有测试 C12 的最小性；C20 测试则从精确特征值人工加正偏差构造上界，未验证实际迭代器能产生合格的区间证书。

## 2. 定义、D1--D4、C12、C20 逐项核验

| 项目 | 判定 | 独立核验结果 | 必要修订/限制 |
|---|---|---|---|
| $D(P,P_0)=\frac12\|P-P_0\|_F^2$ | PASS | 对同秩 $k$ 的正交投影，等于 $k-\operatorname{tr}(PP_0)=\sum_{i=1}^k\sin^2\theta_i$。 | 明写“同秩正交投影”；该量是平方 chordal distance，不应在后文无证明地当作满足三角不等式的 metric。 |
| 下界可行性测试 | PASS | 若 $\eta\ge0$ 且 $L\le\mathrm{OPT}$，则 $(1+\eta)L\le(1+\eta)\mathrm{OPT}$，故更强测试安全。 | 明写 $\eta\ge0$；若 $L<0$，测试通常只会变成 vacuous/impossible，而非错误。 |
| D1 rank-one residual | PASS | 若 $G_{t-1}V=V\Lambda$，则 $(I-P)G_{t-1}V=0$，故 $R=(I-P)a(a^\top V)$，秩至多 1。 | “$V$ invariant”足够，不必要求唯一 top-$k$；若只是近似不变，应保留旧 residual 项。 |
| D2 restricted Rayleigh--Ritz | PASS | Ky Fan 极值原理直接给出 $S^\top G S$ 的 top-$k$ Ritz 子空间在固定 span(S) 内最大化 captured energy。用真实 $G_t$ 复算 cost 后通过 (F) 的 endpoint 确实安全。 | restricted failure 不能推出 ambient infeasibility，原稿已正确说明。 |
| D3 energy/recourse identities | PASS | 2×2 Rayleigh 商展开与 recourse $\sin^2\theta$ 均正确。 | 固定其他 $k-1$ 个方向、$u\perp V$，并把目标减去固定方向的 captured energy。 |
| D3 “smallest-magnitude root” | CONDITIONAL | 在当前点不满足目标、对同一 projector 取唯一主角表示 $\theta\in[-\pi/2,\pi/2]$、搜索两侧全部边界根时，最小 $|\theta|$ 等价于最小 $\sin^2\theta$。 | 不能只取某个数值求根器遇到的第一个根；若当前点已可行，最优是 $\theta=0$ 而未必是等式根。 |
| D4 overlap monotonicity | PASS | 对任意 $\mu_1<\mu_2$ 的任意最优解选择，overlap 非减；其实不需要“consistently selected”这一附加措辞。 | 改成“任取两个不同参数处的全局最优解”；tie 影响同一 μ 处的单值性，不推翻跨严格参数的集合顺序。 |
| D4 captured-energy monotonicity | PASS | 由同一对最优性不等式可得 $E_1\ge E_2$。 | 同上；只对全局 top-$k$ 解成立。 |
| D4 “supports bisection to a feasibility boundary” | CONDITIONAL | cost 随 μ 非减，因此 one-sided bracket 可做；但在退化点 feasibility 是选解相关的，路径可跳跃且不必存在普通 tie rule 下恰好等于边界的单值点。 | 二分应返回经实际 (F) 审核的可行侧，并在 $\lambda_k=\lambda_{k+1}$ 时对退化 top eigenspace 做二级约束优化，或给出 set-valued envelope 与容差语义。 |
| C10/D4 “most-overlapping feasible point” | FAIL | 单调性本身没有证明 penalized path 覆盖原始约束问题的全局最大-overlap 解；更重要的是核心 penalized eigensolve 已被 Hara--Yoshida 2026 明确提出。 | 若仍需全局最优措辞，补强对偶/联合数值域及 tie-space 的完整证明；方法身份改为 prior-art control。 |
| C12 minimum one-plane recourse | CONDITIONAL | 只对**预先固定的一条 plane/path**且按上述全根规则成立；不是所有 $u$ 或 Grassmannian 上的全局最小。 | 规定 $u$ 的符号（例如令 $v^\top Gu\ge0$）、主角区间、双向根枚举、起点 infeasible、固定方向能量与 fallback。 |
| C12 使用 $L<\mathrm{OPT}$ | FAIL（若仍称原始 (F) 最小） | $C\le(1+\eta)L$ 比 (F) 更强。其首个边界一般晚于真实 (F) 边界，recourse 更大。 | 只能称“minimum for the lower-bound-certified surrogate boundary”；若声称对 (F) 最小，必须用 exact OPT 或证明 $L=\mathrm{OPT}$。 |
| C20 lower-bound 方向 | PASS | 若 $\bar\lambda_i\ge\lambda_i(G)$ 同时成立，则 $L=\operatorname{tr}G-\sum_i\bar\lambda_i\le\mathrm{OPT}$，接受测试安全。 | 更稳妥地要求 $U\ge\sum_{i=1}^k\lambda_i(G)$ 的 certified Ky Fan-sum upper bound；并用 exact/upper-certified candidate cost。 |
| C20 可实现证书 | CONDITIONAL | residual norm 单独不够，错误 invariant cluster 可 residual=0；原稿对此判断正确。 | 必须给出 cluster separation、index matching、roundoff/outward rounding 与区间来源。普通 Ritz 值不能冒充上界。 |

### 2.1 $D(P,P_0)$ 的复核推导

对 $P^2=P=P^\top$、$P_0^2=P_0=P_0^\top$、$\operatorname{rank}P=\operatorname{rank}P_0=k$，

\[
\frac12\|P-P_0\|_F^2
=\frac12\operatorname{tr}(P+P_0-2PP_0)
=k-\operatorname{tr}(PP_0).
\]

若 $P=VV^\top,P_0=V_0V_0^\top$，则

\[
\operatorname{tr}(PP_0)=\|V^\top V_0\|_F^2
=\sum_{i=1}^k\cos^2\theta_i,
\]

故等于 \(\sum_i\sin^2\theta_i\)。该部分无方向错误。

### 2.2 D4 的正确单调证明

记

\[
E_i=\operatorname{tr}(P_{\mu_i}G),\qquad
O_i=\operatorname{tr}(P_{\mu_i}P_0),\qquad 0\le\mu_1<\mu_2.
\]

两次全局最优性分别给出

\[
E_1+\mu_1O_1\ge E_2+\mu_1O_2,
\qquad
E_2+\mu_2O_2\ge E_1+\mu_2O_1.
\]

相加得

\[
(\mu_2-\mu_1)(O_2-O_1)\ge0,
\]

所以 $O_2\ge O_1$。再由第一式

\[
E_1-E_2\ge\mu_1(O_2-O_1)\ge0,
\]

所以 $E_2\le E_1$，亦即 cost 非减。这个论证对两个不同 μ 上的**任意**最优解选择成立；“consistent selection”不是证明单调性所需条件。

### 2.3 可复现的 D4 tie 反例

取 (d=2,k=1)，

\[
G=\begin{bmatrix}1&0\\0&3\end{bmatrix},\qquad
P_0=e_1e_1^\top,\qquad \mu_*=2.
\]

此时

\[
G+\mu_*P_0=3I,
\]

所以任意单位向量 (w(\theta)=(\cos\theta,\sin\theta)) 都是 penalized 问题的最优解。原 PCA 的

\[
\mathrm{OPT}=1,\qquad
C(P(\theta))=4-[\cos^2\theta+3\sin^2\theta]
=1+2\cos^2\theta.
\]

令 \(\eta=1\)，则 (F) 为 (C\le2)。在同一个 (\mu_*=2) 上：

- 选 (P=e_2e_2^\top)：cost=1，可行，overlap=0；
- 选 (P=e_1e_1^\top)：cost=3，不可行，overlap=1；
- 选 \(\cos^2\theta=1/2\)：cost=2，恰在边界，overlap=1/2。

因此：跨严格参数的单调性仍正确，但“某个 deterministic tie rule + 普通 bisection”不自动给出边界或最大重叠可行点。必须在退化 eigenspace 内解二级问题，至少也要返回经 (F) 实测的可行侧并承认可能的 jump gap。

### 2.4 C12 的可复现措辞风险

一维 Rayleigh 商可写成

\[
q(\theta)=a\cos^2\theta+2b\sin\theta\cos\theta+c\sin^2\theta.
\]

它是周期为 π 的正弦函数，通常有多个边界根。“first root”若不规定方向和主角代表并不唯一。正确可执行陈述应是：

1. 当前 (\theta=0) 对所用目标 infeasible；
2. 只比较 projector 的主角代表 (\theta\in[-\pi/2,\pi/2])；
3. 枚举两侧所有满足等式的根；
4. 取使 (\sin^2\theta) 最小者；
5. 若使用 (L)，结论只针对 stronger surrogate boundary。

下界与真实边界不一致的简单数值例：令 \(\eta=0.1\)、\(\mathrm{OPT}=2\)、(L=1)。真实 (F) 允许 cost ≤2.2，而下界测试只允许 cost ≤1.1。若路径 cost 连续地从 3 降到 1，则到 2.2 的最小角严格早于到 1.1 的最小角；后者不能称为原始 (F) 的 minimum recourse。

### 2.5 C20 的方向与错误用法反例

正确方向是

\[
U\ge\sum_{i=1}^k\lambda_i(G)
\quad\Longrightarrow\quad
L=\operatorname{tr}G-U\le\mathrm{OPT}.
\]

但 top Ritz values 通常从下方逼近 top eigenvalues。取 (G=\operatorname{diag}(5,2),k=1\)。若把未认证的 Ritz 值 4 错当上界，则 (L=7-4=3>\mathrm{OPT}=2)。在 \(\eta=0\) 时，cost=2.5 的候选会被错误接受。因此 C20 必须提供真正的 upper enclosure 或 Ky Fan-sum upper bound；“残差小”或“Ritz 值接近”都不够。

## 3. 二十张卡的字段完整性与实质资格

静态复核结果：C01--C20 共 20 个唯一卡；每张都逐字包含 `Object`、`Assumptions`、`Prediction`、`Falsifier`、`Collision`、`Disposition` 六个字段，故**字段存在性为 20/20 PASS**。

下表的“6字段”只判断有没有写；“实质判定”判断它能否作为语义独立、已验证的 method card 进入 20→15 选择。

| ID | 6字段 | 实质判定 | 独立核验意见 |
|---|---:|---|---|
| C01 | PASS 6/6 | CONDITIONAL | 合格 mandatory exact control，但不是新方法候选；应移入 comparator ledger。 |
| C02 | PASS 6/6 | CONDITIONAL | 已知 secular/rank-one eigensystem update comparator；需具体主文献、公式与数值稳定性条件。 |
| C03 | PASS 6/6 | CONDITIONAL | Brand-style incremental SVD 属 prior art；“exact”依赖保留完整所需谱/秩，截断后不再 exact。 |
| C04 | PASS 6/6 | CONDITIONAL | 合格 iterative comparator；LOBPCG warm start/Ritz extraction 已知。 |
| C05 | PASS 6/6 | FAIL | 一张卡混合 block Lanczos 与 randomized Krylov，且与 C04/C16 高度重叠，不是单一可审计 construction。 |
| C06 | PASS 6/6 | CONDITIONAL | Oja/streaming PCA 已知 comparator；缺 candidate-specific source locator 与从 stochastic objective 到 (F) 的推导。 |
| C07 | PASS 6/6 | CONDITIONAL | GROUSE 直接 prior art；只能作为 comparator/ablation。 |
| C08 | PASS 6/6 | CONDITIONAL | PETRELS/RLS prior art，且 forgetting objective 与累计 (G_t) 的 (F) 不同；不能与主问题混为同一 endpoint method。 |
| C09 | PASS 6/6 | CONDITIONAL | FD/RFD 已知且已有 B08/B09 历史；适合作 comparator，不应填充新方法配额。 |
| C10 | PASS 6/6 | FAIL | 核心 (G+\mu P_0) top-(k) 与 Hara--Yoshida 2026 公式/代码直接相同；只能归因后作为 control。 |
| C11 | PASS 6/6 | FAIL | 是一次 residual correction/Rayleigh--Ritz，也是 C16 的首步特例；不应同时按独立方法计数。 |
| C12 | PASS 6/6 | CONDITIONAL | 需按 §2.4 修订 minimum 语义并完成 exact boundary rule 的一手碰撞审计；目前只能是 lead。 |
| C13 | PASS 6/6 | CONDITIONAL | 是 C12 的 block-$q$ 家族扩展；缺具体 $2q$ 优化式、可行边界求法与独立于已知 block Grassmann 方法的 delta。 |
| C14 | PASS 6/6 | FAIL | 标准 restricted Ritz 与已碰撞 C10 的直接组合；不是独立方法，最多是同一家族实现变体。 |
| C15 | PASS 6/6 | FAIL | 是 C10/C14 的 μ 搜索器，不是独立 endpoint construction；tie 处还存在 §2.3 问题。 |
| C16 | PASS 6/6 | CONDITIONAL | 有工程假设价值，但目前是包含多种 expansion policy 的 meta-algorithm；需固定唯一 policy、停止规则与成本模型。 |
| C17 | PASS 6/6 | FAIL | short-history basis policy 是 C16 的一个 augmentation policy，与 thick restart/subspace recycling 直接重叠。 |
| C18 | PASS 6/6 | FAIL | FD-tail basis policy 是 C16 的一个 augmentation policy，并非独立 method card。 |
| C19 | PASS 6/6 | FAIL | randomized basis policy 仍是 C16 的一个 augmentation policy；seed/fallback 不使其成为独立机制。 |
| C20 | PASS 6/6 | CONDITIONAL | 有用的 cross-cutting certificate/stopping component，但不是单独 endpoint method；需给出实际 certified enclosure。 |

### 3.1 六字段齐全不等于 `math_verified`

这些段落不是 research-autopilot `method-verification` 所要求的完整 math cards。普遍缺少：

- 明确的 operation/condition/condition status；
- 可逐步复核的 consequential derivation；
- executable method expression（许多只有算法族名称）；
- candidate-specific `closest_alternative` 与 `decisive_comparison`；
- 一手来源的页/式/算法/commit/file/function locator；
- 独立 semantic math review。

所以“20 张卡都写了六个 bullet”只能关闭格式检查，不能推出 `math_pool_verified`。

## 4. 重复/嵌套候选审计

| 家族 | 重复或嵌套关系 | 判定 |
|---|---|---|
| Penalized overlap | C10=ambient D4；C14=restricted D4+Ritz；C15=对 C10/C14 做 μ-bisection | C14/C15 不能与 C10 同时算三个独立方法；C10 核心又已是 prior art。 |
| Residual/Ritz expansion | C11=一次 residual-RR；C16=自适应多次 expansion；C05=Krylov expansion 变体 | 至少 C11 是 C16 的嵌套特例；C05 的确定性与随机机制还应拆开后再审。 |
| C16 basis policies | C17=history union；C18=FD tail；C19=random probes | 三者应是 C16 的 ablations/policies，而非四个独立方法。 |
| Grassmann boundary | C12: $q=1$；C13: block-$q$ generalization | 可保留同一家族的两个尺度假设，但必须证明 consequential difference；目前 C12 是 C13 的特例。 |
| Exact endpoint controls | C01(full eig), C02(secular update), C03(incremental SVD) | 输出目标相同但算法机制不同，可作为三个 comparator；不能作为三个新颖候选。 |

因此本稿只有“20 个编号”，没有通过 structural distinctness 的“20 个方法”。保守处理应将 C01--C04、C06--C10 归为已知 comparators；C11、C14、C15、C17--C20 归为 family component/solver/ablation；仅把经修订的 C12、C13、C16 当作待查 hypotheses。即使这种归类不是唯一，它已足以否定当前 20→15 边界。

## 5. Top-15 计数与排序逻辑

| 检查 | 判定 | 结果 |
|---|---|---|
| 卡数 | PASS | 20 个 ID，C01--C20，均唯一。 |
| whole-pool ranking 覆盖 | PASS | 排名表包含 20 个 ID，每个恰一次。 |
| Top-15 数量 | PASS | 15 个唯一 ID。 |
| Top-15 是否等于排名前缀 | PASS | 文本列表与表格 rank 1--15 完全一致。 |
| 是否为 15 个语义独立候选 | FAIL | 包含 comparator、直接 prior art、solver、certificate 与 C16 的多个 policy。 |
| 分数能否复现排序 | FAIL | 未声明加权和/lexicographic/role quota；给出的 tie-break 也无法解释多处严格支配反序。 |
| 是否给出逐候选完整 rank reason | FAIL | `Provisional role` 不是 problem value、math consequence、closest-work delta、prediction、cost 五维 rationale。 |
| 是否可据此进入 code | FAIL | 数学卡、碰撞、distinctness 与 selection review 均未关闭。 |

### 5.1 可复现的排序矛盾

若四个分数用于比较，至少应满足：在未报告其他维度时，被逐项弱支配且有一项严格更差的候选不应排在支配者之前。但表中：

- C11=(N0,C3,E3,V3) 严格支配 C14=(0,3,2,3) 和 C15=(0,3,1,3)，却排在二者之后。
- C01=(0,3,2,3) 严格支配 C17=(0,3,2,2)、C19=(0,3,2,2)、C18=(0,3,1,2)，却排在三者之后。
- 简单求和时，C11 总分 9 却排第 7，低于总分 8/7 的 C14/C15；C01--C04 总分均为 8，却排在总分 6--7 的若干 ablation 后。

可以因为“先投资源给 hypotheses、后放 controls”而故意这样排，但该 role quota 是未报告的第五维，且与“scores force a whole-pool comparison”的表述不一致。修订时必须声明可执行排序规则，或把 methods、controls、components 分层而不强行混排成一个 Top-15。

## 6. 一手文献/代码碰撞核验

检索截止：2026-10-10。这里只给出本次实际核到的一手来源；未完成的 family-wide search 仍标为 `INCONCLUSIVE_EXPAND_SEARCH`，不作“无 prior work”结论。

### 6.1 C10：确认直接碰撞

Hara & Yoshida, *Consistent PCA and Spectral Clustering*, AISTATS 2026：

- PMLR 页面与正式论文：[PMLR 300, pp. 910--918](https://proceedings.mlr.press/v300/hara26a.html)，[PDF](https://raw.githubusercontent.com/mlresearch/v300/main/assets/hara26a/hara26a.pdf)。
- 论文 Eq. (1) 定义 $\frac12\|P-P_0\|_F^2=k-\operatorname{tr}(PP_0)$。
- 论文 Eq. (2)/§3.1 最大化 captured variance 减去该 regularizer，等价于取 $G+\lambda P_0$ 的 top-$k$ eigenspace（减去 $\lambda I$ 不改变 eigenspace）。这与 D4/C10 的核心 objective 完全相同。
- 官方代码 HEAD `2d04e05e2370d68d3cb2e0f06fb964d7ab36042f`；[`packages/ConsistentML/src/ConsistentML/PCA.py`](https://github.com/sato9hara/consistent-pca-sc/blob/2d04e05e2370d68d3cb2e0f06fb964d7ab36042f/packages/ConsistentML/src/ConsistentML/PCA.py) 中 `ConsistentPCA.update` 明确构造 covariance 加 previous-projector regularizer 后取 top eigenvectors。

判定：C10=`REROUTE_EVIDENCE/COMPARATOR`，不能保留 residual novelty。C14/C15 若没有超出“restricted implementation / parameter search”的独立理论与行为，只是 C10 的工程包装。

### 6.2 Consistent LRA：问题与 recourse 先验已存在，但不单独杀死 C12

Woodruff & Zhou, *Consistent Low-Rank Approximation*，arXiv:2603.02148：

- [论文](https://arxiv.org/abs/2603.02148)
- 官方代码 HEAD `d607c4f6467216c470d1e3b93989d44d5fcdec97`：[samsonzhou/consistent-LRA](https://github.com/samsonzhou/consistent-LRA/tree/d607c4f6467216c470d1e3b93989d44d5fcdec97)

该工作已经正式定义 row-stream、relative $(1+\epsilon)$ LRA 与 recourse，并讨论部分替换 singular directions 的机制。这确认 frozen parent problem 与“partial change”不是新颖点。但本次阅读没有发现其明确给出 C12 的“固定 one-plane 上精确 feasibility-boundary 首根”规则，因此对 C12 的 disposition 是 `INCONCLUSIVE_EXPAND_SEARCH`，不是 ADVANCE，也不是 KILL。

### 6.3 C12/C13/C16/C20 的高风险邻居

- 一维/块 Grassmann Rayleigh quotient line search 已是成熟方向；例如 [Gradient-Type Subspace Iteration Methods for the Symmetric Eigenvalue Problem](https://epubs.siam.org/doi/abs/10.1137/23M1590792) 明确使用 efficient exact line search。
- [Geometric Subspace Updates with Applications to Online Adaptive Nonlinear Model Reduction](https://epubs.siam.org/doi/10.1137/17M1123286) 基于 GROUSE rank-one geodesic，并给出沿 geodesic 的 closed-form residual。这使 C12 的“解析边界根”处于高碰撞风险，但还需逐式等价审计。
- residual correction、Rayleigh--Ritz、Davidson/Jacobi--Davidson/LOBPCG 与 recycling 覆盖 C11/C16/C17 的主体 computation graph；“加 exact audit/fallback”可形成可靠工程 pipeline，但不会自动变成新算法。
- Ritz/eigenvalue a posteriori bounds 是成熟领域；例如 [Grubišić 2005](https://arxiv.org/abs/math/0503328) 讨论 spectrum identification 与 Temple--Kato 型 bounds，[Knyazev--Argentati 2007](https://arxiv.org/abs/math/0701784) 给出 Rayleigh--Ritz error bounds。C20 最多是把合格证书接到本项目 acceptance rule 的组合。

这些来源足以否定“由代数本身推出 residual novelty”，但不足以完成每张卡要求的全覆盖碰撞审计。当前每卡 `Collision` 多为算法族名，没有 dated query family、页/式、commit/file/function、不可达范围与 decisive comparison，故总体仍是 `INCONCLUSIVE_EXPAND_SEARCH`。

## 7. 是否把已知方法误称新颖

严格按字面，原稿多次声明 “not a novelty claim”，并没有直接把 C01--C20 宣称为新颖，因此**没有发现一句明确的虚假 novelty verdict**。

但以下表述存在升级风险，不能带入后续论文/代码元数据：

1. C10 的 collision 已经从“direct threat/full formula audit pending”升级为**公式与官方代码确认的核心机制碰撞**。
2. N=1 的 C12/C13/C16/C20 只是“尚未排除的 residual possibility”，不是正向 originality evidence。
3. C16 是标准 residual/Krylov/Ritz expansion 加 certificate/fallback 的工程组合；除非固定的新 computation graph 带来可证的新性质，否则只能称 engineering hypothesis。
4. C20 是 certificate accelerator/component，不是独立新 endpoint method。
5. C14/C15、C11/C17/C18/C19 不应通过改名或 solver/policy 拆分来填充 20 个候选配额。

## 8. 进入代码设计前必须关闭的修订清单

| 优先级 | 必须修订 | 验收条件 |
|---:|---|---|
| P0 | 修订 D4 tie/bisection | 给出 set-valued 或 degenerate-eigenspace 二级优化算法；用 §2.3 反例测试，明确返回可行侧/容差/最优性范围。 |
| P0 | 修订 C12 minimum 声明 | 明确 $u$ 与符号、主角区间、双向全部根、起点 infeasible、exact OPT vs lower-bound surrogate；标题不再暗示 Grassmannian/global minimum。 |
| P0 | 重新分类 C10 | 记录 Hara--Yoshida 论文 Eq. (1)/(2)/§3.1 与官方 commit/file，C10 仅作 attributed comparator。 |
| P0 | 重建候选池 distinctness | controls、method families、components/ablations 分账；C14/C15、C11/C17/C18/C19 不再各占一个独立方法名额。若不足约 20 个实质候选，诚实报告 shortfall。 |
| P0 | 重做 Top-15 | 声明可复现规则；消除未解释的 dominance inversion；每项给完整 rank rationale 与 source-bound closest-work delta。 |
| P1 | 完成 C20 certificate specification | 固定一个真实可计算的 Ky Fan upper enclosure、cluster/index 证明、roundoff 语义与 candidate-cost upper check。 |
| P1 | 补齐全卡数学证据 | 每张保留候选给 formal object、operations/conditions、逐步 derivation、method expression、prediction/falsifier、closest alternative/decisive comparison。 |
| P1 | 完成逐卡碰撞审计 | 一手论文全文、实际作者/基线代码、页/式/算法和 commit/file/function locator；缺失项明确标为 inaccessible/unknown。 |
| P1 | 新一轮独立 review | 对修订后的 math cards、structural distinctness、完整排名与 exact Top-15 给独立 PASS，之后才可跑 `--before code` 边界。 |

## 9. 最终授权判定

**不允许进入新候选代码设计（NO-GO）。**

当前可确认的只是：基础 projector algebra、D1/D2、D3 identities、D4 的跨参数单调不等式和 C20 的理想界方向。尚未确认的是：D4 tie-aware boundary solver、C12 对原始 (F) 的最小性、C20 的实际可获得证书、20 个语义独立方法、可复现 whole-pool ranking、完整 Top-15 selection review 与逐卡碰撞覆盖。

建议下一节点：先完成 P0 数学/去重/碰撞修订；若实质候选数低于 20，则报告真实 shortfall，而不是用 controls、solver wrappers 或 basis policies 补齐。修订完成后重新独立核验；在此之前不得据本稿生成新方法实现或实验设计。
