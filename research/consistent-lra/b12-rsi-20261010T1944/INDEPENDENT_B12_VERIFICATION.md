# B12 独立数学与执行核验

日期：2026-10-10  
核验身份：独立核验；不继承 `B12_GEOMETRY_COST_BOUNDARY.md` 的结论  
范围：只读审查指定 theorem/proposition、有限诊断脚本、结果 JSON 与两份 Simple receipts；**没有运行新实验**

## 总结结论

**总体：REVISE。**

Theorem B12.1 的目标下界

$$
r(P,Q)\ge \frac{\Delta^2}{kD^2}
$$

在 $D>0$、$P,Q$ 为同秩 $k\ge1$ 正交投影且 $P$ 达到可行阈值的条件下是正确的，常数也是可达的。但当前文本不能原样标为完全通过，原因有三项：

1. 证明第 36 行在 $\Delta=0$ 时错误地断言 $L_G(Q)-L_G(P)\ge0$；结论此时虽是平凡真命题，证明必须先分情况。
2. 累积式声称适用于“any feasible online sequence”，却可能含 $D_t=0$ 的未定义商；必须限制求和指标或显式定义零直径项为零。
3. sharpness 示例使用 `diag(D/2,-D/2)`，与全文的 $G\succeq0$ 约定不符；平移为 `diag(D,0)` 即可无损修复。

这些都是可做最小精确修复的问题，不推翻主常数。Proposition B12.2 在“跨任意实现、计算模型未冻结”的限定下成立，但应把量词写得更精确，避免被读成“冻结模型后也不可能得到复杂度界”。有限脚本和 receipts 可核实一次确定性有限诊断成功；它们不是 theorem、CPU 不可识别性或原创性的证明。

本结论**不是原创性结论、论文通行证、方法候选通过、代码设计授权或 native-5000 授权**。

## 1. 核验对象与完整性

| 对象 | 只读 SHA-256 | 核验 |
|---|---|---|
| `B12_GEOMETRY_COST_BOUNDARY.md` | `220a20f3c545e19495f212fc626022f325c9f51ffbb9d3553dacb3eaa28a6bde` | 已逐行审查 |
| `verify_b12_boundary.py` | `d093d5eba597cc00202b5e29c042c90255b72cdf46a00b6082fc81ecddcc850b` | 已静态审查；未重跑 |
| `B12_BOUNDARY_CHECK.json` | `3d041073773266caf6ea66ca90162d58613833640b373d285e7a361436435eea` | 已核对字段及 receipt 哈希 |
| `b12-static-check` receipt | attempt `8a316efe...` | `succeeded`，exit 0，stderr 空 |
| `b12-boundary-check` receipt | attempt `018ab605...` | `succeeded`，exit 0，stderr 空 |

两份 receipt 的输入哈希均与当前 theorem 文本和脚本一致；运行 receipt 的输出哈希与当前 JSON 及保存的 stdout 一致。因此它们确实对应当前这组冻结文件，而不是另一版本。

## 2. Theorem B12.1 逐项核验

| 项目 | 判定 | 独立核验结果 |
|---|---|---|
| 对象、loss 与 recourse 定义 | PASS | $L_G(P)=\operatorname{tr}((I-P)G)$，且同秩投影满足 $r(P,Q)=\frac12\lVert P-Q\rVert_F^2$。 |
| 主常数 $1/(kD^2)$ | PASS | 中心化后算子范数恰为 $D/2$；核范数恰为 $2\sum_i\sin\theta_i$，两因子相消为 $D\sum_i\sin\theta_i$。Cauchy 给出 $D\sqrt{kr}$，故平方后常数正确。 |
| 从 feasibility 推出 gain 下界 | **REVISE** | 仅当 $\Delta>0$ 时有 $L_G(Q)>T$，继而 $L_G(Q)-L_G(P)\ge L_G(Q)-T=\Delta$。若 $\Delta=0$，可行的 $P$ 可能比 $Q$ 更差，gain 可为负；当前第 36 行不成立，但所求 recourse 下界此时只是 $r\ge0$。 |
| equal-rank projector singular values | PASS（建议澄清） | 对每个非零主角 $\theta_i$，$P-Q$ 有两个奇异值 $\sin\theta_i$；零角只贡献零值。故核范数与 Frobenius/recourse 公式正确。为避免 $d<2k$ 时读者误以为共有 $2k$ 个矩阵奇异值，建议写“每个 $\theta_i>0$ 对应两个非零奇异值；零值按环境维数补齐”。 |
| $D=0$ 边界 | PASS（与累积式联动修订） | $D=0$ 时 $G=\lambda I$，所有秩 $k$ 投影的 loss 都是 $(d-k)\lambda$。存在可行阈值即迫使 $T$ 不低于此值，故 $\Delta=0$。单步商不可使用。 |
| $k=1,d=2$ sharpness | **REVISE** | 角度代数正确，且常数确实可达；但所写 $G=\operatorname{diag}(D/2,-D/2)$ 非 PSD。改为 $G=\operatorname{diag}(D,0)$ 后谱直径仍为 $D$，所有等秩能量差不变。还应取 $T=L_G(P)$，以保证 $\Delta=L_G(Q)-L_G(P)=D\sin\phi$，从而 theorem 的下界本身取等，而不只是辅助绝对值不等式取等。 |
| 累积求和 | **REVISE** | 各时刻只要 $P_t$ 对当前 $(G_t,T_t)$ 可行，且 $\Delta_t$ 用实际 $P_{t-1}$ 计算，单步式可直接求和，不需独立同分布或跨时刻独立性。但当前显示式对 $D_t=0$ 未定义；需仅对 $D_t>0$ 求和，或约定 $0/0$ 项为 0。 |
| “global in endpoint / no eigengap” | PASS | 推导仅用谱直径和两个 endpoint，未用 $k$ 处 eigengap，也不是局部角度展开。 |
| “constant exact” 的范围 | PASS（限定） | exact 指所述普适常数不可整体改小；二维秩一族足以证明。它不表示任意 $k,d,G$ 或任意 deficit 都取等。 |

### 2.1 独立重推

设 $c=(\lambda_{\max}G+\lambda_{\min}G)/2$。同秩给出 $\operatorname{tr}(P-Q)=0$，所以

$$
\begin{aligned}
|\operatorname{tr}(G(P-Q))|
&=|\operatorname{tr}((G-cI)(P-Q))|\\
&\le \lVert G-cI\rVert_2\lVert P-Q\rVert_*\\
&=\frac D2\,2\sum_{i=1}^k\sin\theta_i\\
&\le D\sqrt{k\sum_{i=1}^k\sin^2\theta_i}\\
&=D\sqrt{k\,r(P,Q)}.
\end{aligned}
$$

现在必须分情况：

- 若 $\Delta=0$，目标式就是 $r(P,Q)\ge0$。
- 若 $\Delta>0$，则 $L_G(Q)>T$，而 $L_G(P)\le T$，故

$$
0<\Delta=L_G(Q)-T\le L_G(Q)-L_G(P)
=\operatorname{tr}(G(P-Q)).
$$

与前一显示式合并并平方，得到 theorem。这里没有把负 gain 平方，也没有在 $\Delta=0$ 时使用一个不成立的 gain 符号断言。

### 2.2 可复现的代数反例：当前第 36 行

取 $G=\operatorname{diag}(1,0)$、$k=1$，令 $Q=e_1e_1^\top$、$P=e_2e_2^\top$，并取 $T=1$。则

$$
L_G(Q)=0,\qquad L_G(P)=1\le T,\qquad \Delta=[0-1]_+=0,
$$

但

$$
\operatorname{tr}(G(P-Q))=L_G(Q)-L_G(P)=-1<0=\Delta.
$$

所以“feasibility gives gain $\ge\Delta$”原句为假；theorem 的结论仍然是平凡的 $r\ge0$。

### 2.3 PSD sharpness 的精确构造

取 $0<\phi\le\pi/2$、$G=\operatorname{diag}(D,0)$，令

$$
\alpha=\frac\pi4-\frac\phi2,\quad
p=(\cos\alpha,\sin\alpha),\quad
q=(\cos(\alpha+\phi),\sin(\alpha+\phi)),
$$

并置 $P=pp^\top,Q=qq^\top,T=L_G(P)$。则

$$
\Delta=L_G(Q)-L_G(P)
=D\bigl(\cos^2\alpha-\cos^2(\alpha+\phi)\bigr)
=D\sin\phi,
$$

而 $r(P,Q)=\sin^2\phi$。所以

$$
r(P,Q)=\frac{\Delta^2}{D^2},
$$

正好达到 $k=1$ 的界。原 indefinite 构造与此构造只差 $(D/2)I$，所以其差值计算没错，但对象类别写错。

### 2.4 累积式的最小精确版本

令 $S_+=\{t:D_t>0\}$。若每个 $P_t$ 对 $(G_t,T_t)$ 可行，且

$$
\Delta_t=[L_{G_t}(P_{t-1})-T_t]_+,
$$

则

$$
\sum_t r(P_t,P_{t-1})
\ge \sum_{t\in S_+}\frac{\Delta_t^2}{kD_t^2}.
$$

对 $D_t=0$，可行性保证 $\Delta_t=0$，这些时刻只贡献平凡下界 0。等价地可显式定义该项为 0，但不能未经约定书写 $0/0$。

## 3. Proposition B12.2 的适用范围

| 声明 | 判定 | 核验 |
|---|---|---|
| 仅由 $(\Delta,D,k,r)$ 不能确定实际 CPU cost | PASS | 四个量描述几何/证书，不编码维数、数据表示、缓存、精度、机器或算法；相同 endpoint 可由不同实现以不同工作量返回。 |
| 跨任意实现不存在仅依赖四标量的有限普适上界 | PASS | 对同一输入输出行为插入任意多无关操作，即可保持四标量不变而使 CPU 任意增大。 |
| 未冻结 output form 时不存在有意义的统一 I/O 下界 | PASS | 显式 $d\times k$ 基、隐式 action、句柄或已缓存对象的输出成本不同；文本已承认这一点。 |
| “no nontrivial universal cost function” | **REVISE（量词澄清）** | 这句话若指跨任意实现的唯一成本预测或有限上界，成立；若被理解为冻结算法、维数、表示、精度与机器后仍不可能有条件复杂度界，则过强且不是当前论证所得。 |
| lookup-table 论证 | PASS（限定） | 它展示未指定预处理/非均匀性收费时的不可识别性；不能用来声称真实在线算法“计算免费”，文本随后也正确否认了这种解释。 |

建议把命题核心改写为：

> Across unrestricted implementations and with preprocessing, state, representation, precision, machine, and output form uncharged or unspecified, no unique CPU cost or finite universal CPU upper bound is determined by $(\Delta,D,k,r)$ alone. This does not preclude conditional upper/lower bounds after a computational model and algorithm are fixed.

这是一条**建模边界/不可识别性陈述**，不是已证明的机器复杂度下界，也不是新方法。

## 4. 脚本实际测试了什么

### 4.1 覆盖与未覆盖

| 项目 | 判定 | 证据 |
|---|---|---|
| 随机核心不等式 | PASS（有限） | 固定 seed 下生成 6000 组 PSD Gram 与随机同秩投影，检查更强的对称式 $|\operatorname{tr}(G(P-Q))|\le D\sqrt{kr}$。JSON 报告最大 violation 为 `-1.764792107518875e-05`。 |
| case 计数 | PASS | $d\in\{2,3,5,8,16\}$；各 $d$ 的 $k$ 数为 $1,2,4,4,4$，乘 400，合计 6000。 |
| 二维等号族 | PASS（有限代数诊断） | 200 个 $\phi$ 点，最大绝对误差 `8.881784197001252e-16`。构造的 gain 为正，因此代码的 `abs(gain-rhs)` 在该族上有效。 |
| theorem 的 PSD sharpness 示例 | **REVISE** | sharpness loop 使用 indefinite `diag(3.5,-3.5)`。中心平移解释其数学等价性，但若声称直接测试 theorem 对象，应使用 `diag(7,0)`。 |
| $\Delta=0$ 与 proof sign 边界 | NOT TESTED | 脚本没有阈值 $T$、feasibility 或 $\Delta$；因此无法发现第 36 行错误。 |
| $D=0$ | NOT TESTED | 随机 Wishart 几乎处处 $D>0$，没有标量矩阵专门 case。 |
| 累积式 | NOT TESTED | 所有 case 独立成对，无路径或逐时刻 threshold。 |
| 奇异值重数公式 | NOT TESTED DIRECTLY | 脚本不计算主角或 $P-Q$ 的奇异值，只间接测试最终界。 |
| $k=d$、较大 $k$ | NOT TESTED | `range(1,min(d,5))` 排除了 $k=d$，且在 $d=8,16$ 时仅到 $k=4$。这不影响“有限诊断”定位。 |
| Proposition B12.2 | NOT TESTED / 不宜称为测试 | 脚本没有实现、成本模型或成对不可识别性实例；CPU/RSS 字段只是该诊断自身的运行元数据。 |
| 原创性、论文性、native benchmark | NOT TESTED | scope 字段与文档已明确否认这些用途，表述正确。 |

因此 `inequality_pass=true` 和 `tightness_pass=true` 只表示预先指定的有限数值谓词通过，不能补上 theorem 的 case split，也不能证明普遍命题。

### 4.2 线程、预算与 receipts

| 检查 | 判定 | 结果 |
|---|---|---|
| 静态编译 task | PASS | timeout 20 s；receipt elapsed `0.056718592` s，exit 0，空 stdout/stderr。 |
| 有限诊断 task | PASS | timeout 30 s；receipt elapsed `0.522620147` s，exit 0，空 stderr；脚本内部 wall `0.371337296` s、process CPU `0.371334856` s。 |
| 总配置预算 | PASS | config 为 max 8 attempts、max command 120 s、deadline 1200 s、max concurrency 1；两任务均远低于各自 timeout，时间戳显示顺序执行。 |
| 线程环境 | PASS（环境证据） | JSON 记录 OMP/OpenBLAS/MKL/VECLIB/NUMEXPR 五个变量均为 `1`。脚本在导入 NumPy 后只读取而不设置环境，所以单线程性依赖 launcher；receipt 本身未记录实际 BLAS thread-pool introspection。可据此声称“运行环境请求/呈现单线程变量”，不宜声称已动态审计实际线程数。 |
| receipt 可追溯性 | PASS | source/input/output hashes 全部闭合；运行 stdout 哈希等于输出 JSON 哈希。 |

这里的 budget PASS 只说明指定的两个轻量诊断在约束内完成，不是 native 数据集预算或算法成本证据。

## 5. 最小精确修复清单

无需改变 theorem 主公式；建议只做以下最小改动：

1. 在证明第 36 行前加入：`If Delta=0, the claim is trivial. Assume Delta>0.`
2. 把奇异值句改为：`For every principal angle theta_i>0, P-Q has two nonzero singular values sin(theta_i); zero angles contribute only zeros.`
3. 把 sharpness 的 Gram 改成 `G=diag(D,0)`，并明确 `T=L_G(P)` 与 $0<\phi\le\pi/2$。
4. 把累积式的右侧求和限制为 `t: D_t>0`，或明确定义 $D_t=\Delta_t=0$ 时该项为 0；同时显式写出每个 $P_t$ 对当前 threshold 可行。
5. 把 Proposition B12.2 的“不存在 cost function”限定为跨 unrestricted implementations 的唯一成本/有限上界不可由四标量确定，并保留“冻结模型后可有条件复杂度界”。
6. 若保留诊断脚本用于对齐 theorem 对象，把 tightness 矩阵平移为 PSD；可选增加 $\Delta=0$、$D=0$ 和 principal-angle identity 的确定性单元 case。后者是增强有限回归覆盖，不是证明要求。

## 6. 最终门禁

| 门禁 | 结论 |
|---|---|
| B12.1 主不等式与常数 | **PASS** |
| 当前证明文本原样 | **REVISE** |
| 当前 sharpness 对象原样 | **REVISE** |
| 当前累积式原样 | **REVISE** |
| B12.2 作为未冻结计算模型的边界 | **PASS，需量词限定** |
| 有限脚本与 receipt 所称有限后果 | **PASS，限于明确覆盖项** |
| 数值结果作为普遍证明 | **FAIL / 不允许** |
| 原创性或论文通行证 | **未建立 / 不允许** |
| 新方法、代码设计或 native-5000 授权 | **NO-GO** |

在完成上述最小文字/对象修复后，可把 B12.1 作为已核对的几何必要条件使用；在计算模型、候选方法与独立原创性证据仍未闭合前，不应由此进入新方法代码设计或论文主张。
