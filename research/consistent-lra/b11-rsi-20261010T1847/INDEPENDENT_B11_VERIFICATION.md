# B11 候选碰撞闭合独立核验

日期：2026-10-10  
核验方式：只读；未运行重计算  
核验对象：

- `B11_COLLISION_AND_DERIVATION.md`，SHA-256 `184852c669e5ff9873ecab27ee4bfd18493be895e88ca2814391dda490a47576`
- `REPORT_B11.zh-CN.md`，SHA-256 `4ac330697f77565056ecb76e4a7199067ca07498e7153db50e523bbc2c076625`
- `verify_b11_math.py`，SHA-256 `bd8f7db9be73737b378adc9c3b5893a2f6fbdc4d2ab1b518ddce6c676dd20e31`
- `B11_MATH_CHECK.json`，SHA-256 `a202547bc988265583299cea57e6264429b973307587b1fd1d8d46ecc7a0788d`
- 四个 attempt 的 `receipt.json` 与 `stderr.txt`

## 0. 总结论

**B11“候选碰撞已经完全闭合”的总判定：PARTIAL。**

**B11 保持新方法代码门禁 NO-GO 的判定：PASS。**

分项结论：

| 项目 | 判定 | 核心结论 |
|---|---|---|
| C12 固定平面全根公式 | PASS（带边界条件） | 正弦化与全根公式正确；最小 recourse 只在预先固定的 plane/path、当前点 infeasible、目标可达时成立。 |
| C12/C13 推广到 (H+\mu J) top-(k) | PARTIAL | 对 supported scalarized points 正确；不等于已经证明所有 constrained optimum 均被覆盖，也不自动等于预选 C12 plane。 |
| C20 FD Ky-Fan/OPT 恒等式 | PASS（条件恒等式） | 在声明的 FD 包络和 trace convention 下方向与代数正确；有限脚本只检查蕴含，不验证真实 streaming FD 实现或 B07 代码身份。 |
| C16 与 block-Davidson/LOBPCG/JD 碰撞 | PARTIAL | Ritz–block residual–subspace expansion 核心与 block-Davidson 高度/直接重合；但 LOBPCG、JD 不是完整 computation-graph 等价，certificate audit + exact fallback 的组合也未被直接先验覆盖。 |
| 有限检查与 receipts | PASS（仅证据完整性） | 最终 hash/成功 receipt/JSON 一致；两次 streaming-FD 失败被保留。有限检查没有证明全局性、新颖性或碰撞闭合。 |
| 代码门禁 NO-GO | PASS | 无约 20 个 verified distinct candidates、无合法 Top-15、关键碰撞/全局推导仍未闭合；即便某个 wrapper 尚有 residual delta，也不能过 `--before code`。 |

B11 可以可靠地得出：“当前材料不足以授权任何新方法代码，且 C12/C13/C16/C20 均不能按现状计入 verified Top-15。”它尚不能可靠地得出更强的命题：“这些候选的所有完整 computation graph 均已被文献功能等价覆盖，故结构差异严格为零。”

## 1. C12 固定平面全根推导

### 1.1 解析式复核

令

\[
q(\theta)=a\cos^2\theta+2b\sin\theta\cos\theta+c\sin^2\theta.
\]

用二倍角恒等式，

\[
q(\theta)
=\frac{a+c}{2}
+\frac{a-c}{2}\cos 2\theta
+b\sin 2\theta.
\]

记

\[
m=\frac{a+c}{2},\qquad
p=\frac{a-c}{2},\qquad
\rho=\sqrt{p^2+b^2},\qquad
\phi=\operatorname{atan2}(b,p),
\]

则

\[
q(\theta)=m+\rho\cos(2\theta-\phi).
\]

当 $\rho>0$ 且 $T'\in[m-\rho,m+\rho]$ 时，边界方程 $q(\theta)=T'$ 的根为

\[
\theta=\frac12\left[
\phi\pm\arccos\frac{T'-m}{\rho}+2\pi n
\right],
\]

再筛到 projector 主角代表区间 ([-π/2,π/2])。原推导的符号与相位方向正确。

### 1.2 minimum recourse 的必要限定

若：

1. 其余 (k-1) 个方向固定；
2. 当前 θ=0 对该目标 infeasible；
3. 目标在该 plane 上可达；
4. 枚举主角区间内两侧全部 boundary roots；

则最近的可行集合点必在 boundary 上，且在主角区间 $\sin^2\theta$ 随 $|\theta|$ 单调，所以选择最小 $\sin^2\theta$ 的根确实给出该固定 path 的最小 projector recourse。

这不是：

- 对所有 plane/search directions 的最小值；
- Grassmannian 全局最小；
- 对 approximate OPT 或未认证 threshold 的结论；
- 新 search direction 的构造。

### 1.3 未写出的边界分支

推导正文应显式保留以下分支，但缺失不改变核心公式：

- ρ=0：(q) 为常数；若当前点 infeasible，则整条 path 均无根。
- $T'>m+\rho$：目标不可达，必须 fallback。
- $T'<m-\rho$：整条 path 均严格可行；这与“当前点刚失败”的使用场景不相容，应作为输入一致性检查。
- $T'=m\pm\rho$：切触/重根，需要去重与 roundoff-safe clipping。
- 若当前点已可行，最小 recourse 是 θ=0，而不应强制找 boundary root。

**C12 固定平面解析判定：PASS，且仅为局部 path policy。**

## 2. 从固定 plane 推广到 (H+\mu J) top-(k)

### 2.1 正确的部分

在固定搜索空间 (S) 中，令

\[
H=S^\top GS,\qquad J=S^\top P_0S,
\]

约束问题

\[
\max_{Y^\top Y=I_k}\operatorname{tr}(Y^\top JY)
\quad\text{s.t.}\quad
\operatorname{tr}(Y^\top HY)\ge T
\tag{R}
\]

的 Lagrangian 可写为

\[
\operatorname{tr}(Y^\top JY)
+\lambda[\operatorname{tr}(Y^\top HY)-T],
\qquad\lambda\ge0.
\]

当约束 active 且 λ>0 时，除以 λ 后等价于最大化

\[
\operatorname{tr}\{Y^\top(H+\mu J)Y\},
\qquad \mu=1/\lambda,
\]

其全局 scalarized optimum 是 (H+\mu J) 的 top-(k) eigenspace。正文用“at a supported boundary point”限定这一步是正确的。

### 2.2 不能从 KKT/scalarization 自动推出的部分

正文随后把 C12/C13 全部归入 restricted penalized family，强度超过已给证明：

1. **supported 不等于全部。** KKT 给必要 stationary/scalarization 关系时，还需 constraint qualification；weighted-sum scalarization只自动覆盖 supported Pareto points。正文没有证明 rank-(k) real-projector attainable set 的所有相关 Pareto optimum 都 supported，也没有处理非唯一 top eigenspace/tie face。
2. **penalty parameter 的存在与求取未闭合。** 没有证明对每个可行 threshold 都存在有限 μ，使某个 top-(k) 解恰落在所需 boundary；跳跃/tie 时仍可能需要 face 内二级问题。
3. **restricted global optimum 不等于预选 C12 path。** (R) 允许 $S$ 内任意 rank-$k$ 子空间。若 C12 固定某个 $v$ 向 $u$ 旋转并保持其余方向不变，(R) 通常还允许改换哪个旧方向与 $u$ 旋转。只有 $k=1$，或显式把其余 $k-1$ 方向固定并把变量降到该 2×2 plane 时，ellipse 论证才直接等同于原 C12 path。
4. **C13 的 $2q$ block 更非一维 ellipse。** 若只走一条 prescribed geodesic，必须直接分析其标量边界；若优化整个 block，则需要证明其 constrained optimum 与 supported penalized family 的等价范围。

一个简单的“fixed-(S) 比预选 plane 更大”例子：取 (k=2,d=3)，(P_0=\operatorname{span}(e_1,e_2))，预选 C12 plane 只允许把 (e_1) 向 (e_3) 旋转并固定 (e_2)，而 (S=I_3)。令 (G=\operatorname{diag}(10,0,9))。预选 path 的 captured energy 从 10 最多降到 9，无法达到阈值 15；但 (R) 可固定 (e_1) 并把 (e_2) 换成 (e_3)，达到 energy 19。两者不是同一个可行集合。

因此：

- “C12 fixed path 是局部 policy”成立；
- “若主动把 plane selection 扩展为整个 fixed-(S) constrained problem，则其 supported points 属于 restricted (H+\mu J) family”成立；
- “这证明 C12/C13 的每个 constrained minimum 都与 C14/C15 完全等价”尚未成立。

**推广判定：PARTIAL。** 这不恢复 C12/C13 的代码资格；它只阻止把“完全碰撞已经证明”写得过强。

## 3. C20 FD Ky-Fan/OPT 恒等式

### 3.1 代数方向

假设经典 width-ℓ FD 约定满足

\[
0\preceq G-B^\top B\preceq\Delta I,
\qquad
\operatorname{tr}(G)-\operatorname{tr}(B^\top B)=\ell\Delta.
\]

由 (G\preceq B^\top B+\Delta I) 和 Ky-Fan 单调性，

\[
\sum_{i=1}^k\lambda_i(G)
\le
\sum_{i=1}^k\lambda_i(B^\top B)+k\Delta
=:U.
\]

所以

\[
L:=\operatorname{tr}G-U\le
\operatorname{tr}G-sum_{i=1}^k\lambda_i(G)
=\mathrm{OPT}.
\]

再由 trace identity，

\[
L
=\operatorname{tr}(B^\top B)-\sum_{i=1}^k\lambda_i(B^\top B)
+(\ell-k)\Delta
=\operatorname{tail}_k(B^\top B)+(\ell-k)\Delta.
\]

方向与系数在该 convention 下均正确。若实现采用 append-then-shrink 的 ℓ+1 capacity，则 trace-loss 系数以及最终 $(\ell+1-k)\Delta$ 必须按实际实现重新绑定，不能混用符号。

### 3.2 有限脚本实际检查了什么

最终脚本没有运行 streaming FD。它人工构造

\[
G=B^\top B+\Delta QQ^\top,
\]

其中 (Q) 有 ℓ 个正交列，因此构造本身强制满足 envelope 与 trace identity。随后的 120 次检查验证的是：**一旦这些前提成立，Ky-Fan/OPT 推论与 tail 恒等式在浮点下未被反例推翻。**

这不是：

- 对真实 FD update 的验证；
- 对 B07 作者 convention/实现的 readback；
- “所有满足这两个恒等式的 tuple 都来自 FD”的证明；
- C20 与 B07 文件/函数身份相同的机器证据。

脚本注释和报告已基本诚实说明这一范围。两次旧脚本的 streaming-FD 尝试均因 `standard FD invariant lost: no empty row` 失败，且没有输出结果；不能把最终 admissible-tuple 检查描述成对失败实现的修复或通过。

**C20 代数判定：PASS（条件恒等式）。**  
**“exactly B07 implemented”身份判定：PARTIAL，需 B07 实际 code/convention locator；本次指定材料只提供转述。**

## 4. C16 与 block-Davidson/LOBPCG/JD 的碰撞范围

### 4.1 可确认的碰撞

C16 的冻结核心：

1. 当前子空间内 Rayleigh--Ritz；
2. 形成 block Ritz residual (R=GX-X\Theta)；
3. 用 residual 扩展并重正交 trial space；
4. 重复 extraction/expansion；

与 unpreconditioned block-Davidson/residual-correction family 的 computation graph 高度一致。把 C11 视作第一步 ablation、把 C17/C18/C19 视作 basis/expansion policies，也是合理去重。

### 4.2 原碰撞结论的过强处

以下三者不应混成“完整等价”：

- **block-Davidson**：最接近步骤 1--4，可支持“核心 solver 已知”。
- **LOBPCG**：trial space 通常还显式含 preconditioned residual 与 previous conjugate direction；它是邻近 family，不是原四步 graph 的逐操作同一实现。
- **Jacobi--Davidson**：通过 projected correction equation 生成 correction direction；保留 residual-driven extraction 的思想，但不是简单 append raw residual。

此外，C16 的步骤 5——每轮外部 exact feasibility audit、冻结 dimension cap、失败后 exact cached-Gram fallback——改变了停止语义和 worst-case correctness envelope。经典 eigensolver primitives 已知，并不自动证明这个**完整 certified composition** 已在所引文献中功能等价出现；组合本身也可能只是一项工程 pipeline，而不是新理论方法，但需要按完整 computation graph、保证和 observable behavior 做 source-backed comparison。

因此，“no distinct algorithmic operation remains”应收窄为：

> 未发现新的 eigensolver primitive；核心迭代属于 block-Davidson/residual-correction family。certificate/fallback wrapper 是否具有 consequential、source-distinct 的完整方法性质尚未证明，当前仍不足以计入 verified candidate。

**C16 碰撞判定：PARTIAL。** 核心 collision 足以否定把它当作未经归因的新 eigensolver；现有材料不足以对完整 certified wrapper 作 high-confidence functional KILL。

## 5. 有限检查与 receipt 审计

### 5.1 attempt 清单

| Attempt | 状态 | 输入脚本 SHA | 结果 |
|---|---|---|---|
| `attempt-8e340e6af6624e5ab5ba515a00cc83a0` | succeeded | `f3ebb8bc...` | 仅 `py_compile`；无科学结果。 |
| `attempt-3731d2d72f184f968baf0008ef7aa754` | failed | `f3ebb8bc...` | streaming FD empty-row assertion；无 `B11_MATH_CHECK.json`。 |
| `attempt-2e118231a1cb4af99375ce4d682c2a6b` | failed | `7393aaa6...` | 同类 streaming FD empty-row assertion；无结果。 |
| `attempt-eab94d0d91534ca48ac6b0e886f42ca8` | succeeded | `bd8f7db9...` | 输出当前 `B11_MATH_CHECK.json`，output hash 与当前文件一致。 |

最终成功 receipt 的 runner elapsed 为 `1.0481195509928511 s`；JSON 内脚本自行测得 wall 为 `0.9710163490090054 s`。`REPORT_B11.zh-CN.md` 把后者称为“成功命令 wall”略不精确；它是脚本内部 wall，不是外层 receipt elapsed。四次 receipt elapsed 求和确为报告中的 `3.598604521 s`，该措辞差异不影响科学结论。

### 5.2 C12 数值检查的证据强度

500 个样本被专门选成 (q_{\max}>q(0))，再把 target 取在二者之间，所以它们只覆盖“当前点 infeasible 且正向存在可达改善”的常规情形。稠密 40,001 点网格只是近似参照，`7.78e-05` gap 不是真正解析最优性的证明。

`max_kkt_stationarity_residual` 的检查几乎是恒等式：脚本先令

\[
\lambda=\frac{dD/d\theta}{dq/d\theta},
\]

再检查 $dD/d\theta-\lambda\,dq/d\theta$。只要分母非零，该残差按构造即为零；脚本还跳过 $|dq/d\theta|$ 很小的切触情形，并未检查 multiplier sign、constraint qualification 或二阶/全局条件。该数值 `1.11e-16` 不能作为独立 KKT 验证。

### 5.3 正确的证据表述

`B11_MATH_CHECK.json` 的 `scope` 明确写着“finite algebra diagnostics only; not proof, novelty evidence, or method validation”，报告也重复了这一限制。因此：

- JSON `passed: true` 只表示冻结脚本中的有限阈值通过；
- 它不能证明 C12/C13 的全局 scalarization 等价；
- 它不能证明真实 FD update 或 B07 identity binding；
- 它不能证明 C16 的文献功能等价；
- 两次失败必须继续保留，不能被最终成功 attempt 擦除。

**有限证据使用判定：PASS，附带上述严格范围。**

## 6. 碰撞闭合与代码门禁

### 6.1 为什么“零 surviving candidates”作为 novelty 终局过强

当前证据足以把以下内容降级：

- C12：known path 上的 threshold policy；无全局最小 claim；
- C13：restricted constrained/penalized family 的高碰撞 hypothesis；
- C16：known block-Davidson-like core 加未证实有贡献的 certificate/fallback wrapper；
- C20：已知 FD certificate algebra，且项目自报与 B07 重复。

但 C12 的 exact threshold truncation、C16 的完整 certified composition 是否已有逐操作、逐保证的直接先验覆盖，并未在指定材料中完成 high-confidence equivalence。C13 的 unsupported/tie cases也未闭合。因此“没有任何内容能按现状计入 verified method pool”成立；“所有 residual method delta 已被数学上消灭”不成立。

### 6.2 为什么 NO-GO 仍证据充分

代码门禁不要求先证明候选必然不新颖；只要缺失必需正证据就必须保持关闭。当前至少有：

1. 没有约 20 个 mathematically verified、structurally distinct candidates；
2. 没有逐卡完整 source locator/equivalence report；
3. 没有有效 whole-pool ranking 与 Top-15 selection review；
4. C12/C13 全局/支持性问题未闭合；
5. C16 完整 wrapper 的 consequential delta 未建立；
6. C20 实际 FD/B07 identity binding 未由本次指定 artifacts 验证；
7. 有限随机检查明确不能替代证明或 novelty audit。

这些缺口中的任一项都足以阻止 `--before code`；合在一起使 NO-GO 非常充分。

**代码门禁判定：PASS——继续 NO-GO。**

## 7. 必要限定与下一步

在任何后续摘要、checkpoint 或候选 ledger 中，应使用以下限定：

1. C12 是“fixed-plane all-root minimum”，不是 global minimum。
2. $H+\mu J$ 结论限于 supported scalarized optima；若要覆盖全部 (R)，需补 attainable-set/duality/tie-face 证明。
3. C13 若走 prescribed geodesic，是 path heuristic；若优化 block，是更大的 constrained problem，不能用二维 ellipse 一句带过。
4. C20 是“在 FD envelope + trace identity 前提下”的条件恒等式；真实实现与 ℓ/ℓ+1 convention 必须逐文件绑定。
5. C16 应写“block-Davidson-like core collision”；LOBPCG/JD 是近邻而非逐操作等价；完整 certified wrapper 仍未 high-confidence KILL。
6. `B11_MATH_CHECK.json` 只能称 finite falsification/identity diagnostic；尤其 KKT residual 项不是独立验证。
7. 继续保留两次 FD 失败 attempt 和最终成功 attempt 的不同脚本 hash；不得叙述成同一实现最终通过。

合法下一步仍是 Step 2/3：补齐 supported/global 推导、tie-face/duality处理、C16 完整 computation-graph closest-work audit、B07 实际 convention/code readback。若这些工作仍不能产生一个 consequentially distinct hypothesis，保留候选池 shortfall 或转负结果/benchmark 叙事；在此之前不写新方法代码。

## 8. 最终裁定

- **解析代数：PASS/PARTIAL。** C12 fixed-plane 与 C20 conditional FD identities PASS；C12/C13 的 full restricted-family equivalence PARTIAL。
- **碰撞审计：PARTIAL。** 已知 primitive/family collision 很强，但 C16 完整 wrapper 与 C12 threshold policy 尚未达到逐操作 high-confidence closure。
- **有限检查使用：PASS（仅诊断范围）。** receipts 与最终 hash 一致，失败历史保留；数值通过不是证明。
- **代码门禁：PASS，维持 NO-GO。** 不存在合法 Top-15 或 code-boundary evidence。
- **B11 总体：PARTIAL。** 可接受其负面门禁决定，不接受把所有候选的完整功能等价描述为已经严格证明。
