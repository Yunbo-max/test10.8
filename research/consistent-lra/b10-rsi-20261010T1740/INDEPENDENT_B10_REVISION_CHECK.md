# B10 修订决策独立复核

日期：2026-10-10  
被核文件：`B10_REVISED_DECISION.md`  
被核文件 SHA-256：`76e16d25ba9beb341c8f13ab3549fa12e470e6b84f66a98be019509d1807a810`  
对照文件：`INDEPENDENT_B10_VERIFICATION.md`

## 0. 双层结论

- **修订忠实度：PASS。** `B10_REVISED_DECISION.md` 忠实吸收了独立报告要求的六项 P0 修正，没有删除负面证据，也没有把候选池重新包装为已验证 Top-15。
- **科学/代码门禁：仍为 FAIL / NO-GO。** 修订稿本身也明确保持“NO-GO for new-method code”，并把下一步放在 Step 2/3 文献与数学核验，而非代码或 endpoint 实验。
- **tie-face 二级问题：CONDITIONAL SPECIFICATION，未完成证明。** 文档给出了正确的必要 face-level 问题结构，并明确说全局 constrained-optimum proof 仍 open；它没有把该段冒称为已完成 solver、theorem 或 code authorization。

因此，本次 PASS 只表示“修订稿忠实吸收了审查意见”，不表示候选数学、选择或实现边界已经 PASS。

## 1. 六项 P0 逐项复核

| P0 项 | 修订吸收判定 | 复核结果 | 残余义务 |
|---|---|---|---|
| D4 tie 措辞 | PASS | 正确改为：跨严格参数的任意全局最优解 overlap 非减、data energy 非增，不需要 cross-parameter consistent tie selection；固定参数 cutoff tie 时解为集合值。 | tie-face 内部优化、标量参数选择、跳跃点返回规则和数值退化簇认证均未完成，且文档未声称完成。 |
| D4 ordinary bisection | PASS | 明确否定“scalar bisection + arbitrary eigensolver tie rule”足以证明最大重叠可行 endpoint。复用了可复现的 $G=\operatorname{diag}(1,3)$ 反例。 | 仍需证明何种 μ/face 能恢复原 constrained optimum，并给出可执行、roundoff-safe 的算法。 |
| C12 exact-vs-$L$ | PASS | 把 minimum 限定为 pre-fixed one-plane path、当前点 infeasible、exact OPT、主角表示、双向枚举全部边界根；明确 $L<\mathrm{OPT}$ 只对应 stronger surrogate boundary。 | 若以后允许 approximate OPT/cost，必须另立带误差的安全定理；当前没有该定理，文档也未声称有。 |
| C20 Ky-Fan 方向 | PASS | 正确写成 $U\ge\sum_{i=1}^k\lambda_i(G)\Rightarrow L=\operatorname{tr}G-U\le\mathrm{OPT}$，并明确 ordinary top Ritz values 与单独 residual 不足。 | 需固定实际 upper-enclosure 方法、index matching、separation、outward rounding；若 candidate cost 也近似，还需用其 certified upper bound。 |
| C10 归因 | PASS | 将 C10 从“collision threat”升级为 Hara--Yoshida 2026 的 attributed prior-art control，并绑定官方 commit/file；C14/C15 降为 restricted variant / search wrapper。 | 后续记录应继续保留具体论文式号和 commit/file/function，不得恢复 residual novelty 标签。 |
| 候选去重 | PASS | 20 个 ID 仅保留 provenance；controls、C16 policies、overlap wrappers、certificate component 均不再计为独立 discovery candidates。明确只有两个未决 family leads，且没有有效 Top-15。 | 两个 family 仍未 `math_verified`；不能把 family、ablation 或 component 再次拆名补足约 20。 |
| NO-GO | PASS | 标题状态、结构 ledger、Step 7 和结尾均一致禁止 new-method code 与 endpoint experiments；要求重新独立核验。 | 在新的 distinct math pool、逐卡碰撞审计和 selection review 通过前保持 NO-GO。 |

## 2. tie-face 二级问题专项审查

### 2.1 正确吸收的部分

令

\[
M_\mu=G+\mu P_0.
\]

若第 $k$ 个特征值处存在退化，令 $E_>$ 包含所有严格高于 cutoff 的特征方向，$E_=$ 为 cutoff eigenspace，则任一 top-$k$ penalized optimum 可写成

\[
P=P_>+E_=Q E_=^\top,
\]

其中 $Q$ 是 tied-space 内的 projector。这个 face 表示是正确方向；更精确地，应令

\[
r=k-\operatorname{rank}(P_>),
\]

并要求 $Q^2=Q=Q^\top,\ \operatorname{rank}Q=r$。修订稿没有定义 $r$，但不影响其作为待完善规格的含义。

在固定 μ 的同一 penalized-optimum face 上，

\[
\operatorname{tr}(PM_\mu)
=\operatorname{tr}(PG)+\mu\operatorname{tr}(PP_0)
\]

为常数。因此当 μ>0 时，face 内 data energy 与 overlap 满足

\[
\operatorname{tr}(PG)=c_\mu-\mu\operatorname{tr}(PP_0).
\]

所以任意 basis selection 都不够；若该 face 与真实 feasibility set 相交，至少需要在 face 内解

\[
\max_Q\ \operatorname{tr}(PP_0)
\quad\text{s.t.}\quad
C(P)\le(1+\eta)\mathrm{OPT},
\quad Q^2=Q=Q^\top,
\quad\operatorname{rank}Q=r.
\]

修订稿对此的核心表述正确：它把 secondary problem 当成对 solver specification 的修正，而非 novelty claim。

### 2.2 没有被冒称完成

以下关键缺口仍然存在：

1. 没有证明原始“maximize overlap subject to feasibility”的全局最优解一定落在某个 $M_\mu$ 的 exposed optimum face 上。
2. 没有给出在 bisection jump/cutoff tie 时如何找到正确 μ、正确 face 及可行侧的完整算法。
3. 没有给出上述 rank-constrained tie-space 子问题的 closed-form 或有保证求解器。
4. 没有给出 finite-precision 下如何认证“严格高于 cutoff”与“属于 tied cluster”。
5. 没有证明 restricted C14 路径继承 ambient 问题所需的全局性质。

修订稿在该段结尾明确写明 “its full global constrained-optimum proof remains open”，并在 Step 7 继续禁止 code/endpoint experiments。因此该段没有把待证规格伪装成已完成定理。

### 2.3 唯一需要收窄的措辞

句子 “A correct tie-aware subproblem is as follows” 略强。更精确的含义应是：

> “A necessary candidate tie-face secondary specification is as follows; its sufficiency for the global constrained problem and its solver remain unproved.”

由于原句紧接着已经明确全局证明 open，故本项是 **CONDITIONAL wording issue**，不足以把整体修订忠实度降为 FAIL；但后续材料不得截取前一句而省略 open caveat。

## 3. C12 专项复核

修订稿保留的 statement 与独立报告一致：

- path 预先固定；
- 当前点对目标 infeasible；
- 使用 exact OPT；
- θ 取主角代表 ([-π/2,π/2])；
- 双向枚举全部 boundary roots；
- 最小 |θ| 因而最小化该 path 上的 (\sin^2\theta)。

它同时明确：strict (L<\mathrm{OPT}) 只证明 stronger test (C\le(1+\eta)L) 的 path minimum，不是原 (F) minimum；也没有恢复 Grassmann-global claim。**判定：PASS。**

残余小项：实现规格最终还应明确 (u) 的定向/符号、固定其余 (k-1) 个方向的 captured-energy offset，以及“无根”与数值重根的 fallback。但修订稿当前仍处在数学/碰撞阶段，没有声称这些已实现。

## 4. C20 专项复核

Ky-Fan lower-bound 方向完全正确：

\[
U\ge\sum_{i=1}^k\lambda_i(G)
\Longrightarrow
L=\operatorname{tr}(G)-U
\le
\operatorname{tr}(G)-\sum_{i=1}^k\lambda_i(G)
=\mathrm{OPT}.
\]

修订稿也正确保留了两条反向警告：普通 top Ritz values 不能自动作为 upper bounds；错误 invariant cluster 可有零 residual。因此 C20 被降为 certificate research task / component，而不是 method。**判定：PASS。**

残余条件：若实际验收使用近似 candidate cost $\widehat C(P)$，安全规则应是

\[
\overline C(P)\ge C(P),
\qquad
\overline C(P)\le(1+\eta)L,
\]

而不能用未经认证的近似 cost。修订稿没有讨论 candidate-cost 误差；在当前未实现、NO-GO 状态下这是待补规格，不是已发生的错误接受。

## 5. 去重、计数与状态逻辑

结构 ledger 已完成最重要的纠正：

- C01--C10 不计入独立 discovery candidates；
- C11 是 C16 first-step ablation；
- C12--C13 只算一个未决 boundary family；
- C14--C15 是 C10 variants/wrappers；
- C17--C19 是 C16 policies；
- C20 是 component；
- 不存在有效 Top-15，也不存在 `--before code` pass。

**判定：PASS。** 这忠实保留了 shortfall，而非用已知方法或组件补配额。

一处逻辑措辞可改进：文中“C12 is nested in C13, so even the two-family count is generous”并不由 nesting 直接推出。ledger 已经把 C12/C13 合并成一个 family；另一个 family 是 C16，所以 nesting 不会把 family 总数从 2 再降为 1。更准确的理由应是“boundary family 仍是高碰撞 lead，故把它与 C16 都称为 unresolved families 已属宽松计数”。这不影响“远少于约 20、无 Top-15”的结论。

## 6. 残余过强声明清单

| 位置/措辞 | 严重度 | 判定与处理 |
|---|---:|---|
| “A correct tie-aware subproblem” | 低--中 | 应理解为 necessary candidate specification；全局充分性与 solver 未证。后句 open caveat 保住 NO-GO。 |
| “two unresolved families ... C12 nested ... so count generous” | 低 | nesting 已在一-family 计数中消化；理由表述不严，但 shortfall 结论不变。 |
| C20 只写 Ky-Fan enclosure，未写 candidate-cost enclosure | 低 | 若 cost exact 则无问题；若 cost approximate，必须补 $\overline C(P)$ 安全方向。 |
| finite CPU diagnostics 的 wall/CPU/RSS 叙述 | 不影响 P0 | 只是历史诊断；不能也没有被用作 theorem、tie solver 或 C20 实际证书。 |

未发现以下过强声明：

- 未声称 tie-face global proof 已完成；
- 未声称 ordinary bisection 已修好；
- 未把 lower-bound surrogate 称为原 (F) minimum；
- 未把 ordinary Ritz values 称为安全 upper bounds；
- 未把 C10/C14/C15 恢复为新颖方法；
- 未声称已有约 20 个 distinct candidates 或有效 Top-15；
- 未授权 new-method code 或 endpoint experiments。

## 7. 最终判定

**对“是否忠实吸收独立报告 P0 问题”的问题：PASS。**

**对“是否已可进入代码设计”的问题：FAIL / NO-GO，且修订稿正确保持该状态。**

tie-face 段落的正确身份是：**待证、待实现的二级优化规格**。它修复了“任意 tie rule 即可”的错误，但尚未证明全局 constrained optimum、尚未给出 solver、尚未处理 finite precision，因此不能被后续摘要成“D4 tie 已解决”。下一合法动作仍是修订稿 Step 7 所列的 equation-level collision/math work，之后重新独立核验。
