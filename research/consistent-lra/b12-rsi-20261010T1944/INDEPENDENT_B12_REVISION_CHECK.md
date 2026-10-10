# B12 修订闭合独立复核

日期：2026-10-10  
范围：仅检查 `INDEPENDENT_B12_VERIFICATION.md` 所列修订是否闭合；不重新评价原创性，不运行新实验

## 结论

**PASS（严格限于修订闭合）。**

更新后的 Theorem B12.1 已闭合此前报告的三项必要证明修复：

1. $\Delta=0$ 已先作为平凡分支处理，不再错误断言 gain 非负；
2. 累积式右端已只对 $D_t>0$ 求和，并把可行条件下 $D_t=0,\Delta_t=0$ 的贡献定义为零；
3. sharpness 已改成 PSD 的 $G=\operatorname{diag}(D,0)$，并明确 $T=L_G(P)$。

同时，equal-rank singular-value 语句已经按“每个正主角给出两个正奇异值，零主角不贡献”的精确形式澄清；Proposition B12.2 也已把 CPU 结论限定为 unrestricted implementations 下的不可识别性/无有限普适上界，并明确不否定冻结计算模型后的条件复杂度上下界。

repaired script 的 forced-intersection 截断对这项**有限数值诊断**是合理的稳定化处理；五个最终 `*_pass` 字段均为 true，且结果 bytes、输入/输出哈希、成功 receipts 与 `stopped_status.json` 中的两项 task 状态一致。

这个 PASS **不是 theorem 原创性结论、论文通行证、候选方法通过、科学认证、代码设计授权或 native benchmark 授权**。

## 1. 冻结对象与身份闭合

| 对象 | SHA-256 | 结果 |
|---|---|---|
| 更新后的 `b12_work/B12_GEOMETRY_COST_BOUNDARY.md` | `b1a504390fd01912ad37bfb797a7d63cb3857da025cb9ff053c0fb7af7e22e04` | 与 repair window receipt 的 theorem 输入完全一致 |
| 先前独立报告 | `3de38d6a509d476614822b830bd3e6f8a79118967693acc4ac557da1abaed2f3` | 被两项 repair task 作为冻结输入引用 |
| repaired `verify_b12_boundary.py` | `7bf402604c51e78f9cd1f2914377f83155ad5a4aa2223679c310bbd80a03ee21` | 与两份 repair receipt 输入一致 |
| repaired `B12_BOUNDARY_CHECK.json` | `88938e4268de7444f67f5ed95370adf3baee0e61dbe39829dbf08aa56659ba96` | 与 run receipt 输出及 stdout 哈希一致，且文件 bytes 与 stdout 完全相同 |
| `stopped_status.json` | `51941d4bc19ba9519e3cf4efaadb220788f87030ea28faf60a566038792255c2` | 两个 repair task 均为 `succeeded` |

`b12_work` 与 `b12_repair_window` 内的 theorem 副本逐字相同；先前独立报告副本也逐字相同。因此 repair receipt 实际运行时引用的正是本次核验的 theorem 与既有缺陷清单。

## 2. 先前三项证明修复

| 先前问题 | 修订位置/内容 | 判定 |
|---|---|---|
| $\Delta=0$ 时第 36 行错误地推出 $\operatorname{tr}(G(P-Q))\ge0$ | 新第 36--40 行先写 `If Delta=0`，仅在 $\Delta>0$ 时由 $L_G(Q)>T\ge L_G(P)$ 推 gain 下界 | **PASS** |
| 累积式可能出现 $0/0$ | 新第 30--34、59--62 行明确右端只含 $D_t>0$；$D_t=0$ 时可行性迫使 $\Delta_t=0$，该项定义为零且不计算商 | **PASS** |
| sharpness 的 Gram 非 PSD，且未把 energy equality 连到 $\Delta$ | 新第 64--68 行使用 $G=\operatorname{diag}(D,0)$，命名 higher-energy line 为 $P$，设 $T=L_G(P)$，得到 $\Delta=D\sin\phi$ 与 $r=\sin^2\phi$ | **PASS** |

这些改动保持原常数推导不变。取两条线关于第一特征向量的 $45^\circ$ 方向对称、夹角为 $\phi\in[0,\pi/2]$ 时，higher-energy line 的 captured energy 比另一条高 $D\sin\phi$；所以所写 sharpness 等号仍然正确。

## 3. 其余精确性与 CPU 量词

| 项目 | 判定 | 复核说明 |
|---|---|---|
| equal-rank singular values | **PASS** | 新第 47--53 行只称“positive singular values”，每个正主角的 $\sin\theta_i$ 出现两次，零主角不贡献；这也正确覆盖 $d<2k$ 的强制交集。核范数与 recourse 恒等式随之成立。 |
| $D=0$ 边界 | **PASS** | 文本没有计算未定义商；它先用 $G=\lambda I$ 下的等 loss 推出可行时 $\Delta=0$，再把该时刻贡献定义为零。 |
| pathwise 累积条件 | **PASS** | $\Delta_t$ 仍绑定实际上一输出与当前 Gram；求和只是逐时刻必要界相加，没有引入独立样本或虚构 telescoping。 |
| CPU 唯一确定性 | **PASS** | Proposition 新第 90--94 行明确量词为 “Across unrestricted implementations”。 |
| CPU 有限普适上界 | **PASS** | 可插入任意无关操作，故在 unrestricted implementations 上不存在仅由四标量给出的有限普适上界。 |
| 冻结模型后的复杂度界 | **PASS** | 新第 104--107 行明确否认“模型冻结后上下界仍不可能”的过强解释。 |

剩余的 lookup-table 例子仍只用于说明未声明预处理/缓存收费时的不可识别性；文本没有把它冒称为真实在线算法的免费计算或机器下界。

## 4. repaired script 的 forced-intersection 处理

脚本对主角余弦先计算

$$
\sigma_i=\sigma_i(P_B^\top Q_B),\qquad
\sin\theta_i=\sqrt{\max(0,1-\sigma_i^2)}.
$$

当 $d<2k$ 时，维数公式保证至少 $2k-d$ 个零主角，即对应的余弦在精确算术中为 1。浮点 SVD 若返回 $1-\varepsilon$，随后平方根会把末位误差放大到 $O(\sqrt\varepsilon)$。第 64--67 行把满足 $|1-\sigma_i|\le10^{-12}$ 的余弦置为 1，正是在处理这个已知病态变换。

| 检查 | 判定 | 说明 |
|---|---|---|
| 是否改变 theorem | **否** | 截断只在有限诊断脚本中；证明仍是精确主角恒等式。 |
| 是否把 $P-Q$ 一侧一起截断 | **否，合理** | 核范数仍由 `svd(p-q)` 独立计算，recourse 仍由 Frobenius 范数独立计算。若把一个真实的非零小角误截为零，另一侧通常仍保留其贡献，倾向于造成 identity 检查失败，而非自动制造通过。 |
| 是否精确识别“恰好 $2k-d$ 个”强制角 | **否，但有限诊断可接受** | 代码按 near-one 阈值处理全部余弦，而非只处理最大的强制个数；这可能在人工近重合 case 中造成假失败或条件敏感，但本批随机有限 case 仍由独立 $P-Q$ 量校验。不可把该启发式提升为通用数值认证器。 |
| 覆盖 | **PASS（有限）** | $d\in\{3,4,5,7\}$、所有 $1\le k<d$、每组 40 次，共 600 cases，包含多个 $d<2k$ 组合。 |
| 最终误差 | **PASS（有限）** | 最大核范数 identity error `6.927791673660977e-14`，最大 recourse identity error `2.4424906541753444e-15`，均低于脚本阈值 `2e-12`。 |

这项处理闭合的是先前有限诊断的数值故障，而不是对所有维数、所有近相交子空间的稳定性证明。

## 5. 最终 pass 字段与 receipts

`B12_BOUNDARY_CHECK.json` 的全部五个最终 pass 字段如下：

| 字段 | 值 | 脚本 gate |
|---|---:|---|
| `inequality_pass` | `true` | 是 |
| `tightness_pass` | `true` | 是 |
| `principal_angle_identities_pass` | `true` | 是 |
| `edge_delta_zero_branch_pass` | `true` | 是 |
| `flat_spectrum_zero_contribution_pass` | `true` | 是 |

脚本第 142--146 行对这五项执行 `all(...)`；任一为假都会 exit 1。对应执行 receipt：

- `b12-repair-static` / attempt `e8f9eb4d...`：`succeeded`，exit 0，耗时 `0.030851355` s，stdout/stderr 均空；
- `b12-repair-boundary-check` / attempt `e68b0e0e...`：`succeeded`，exit 0，耗时 `0.475523089` s，stderr 空；输出哈希为 `88938e...`，与最终 JSON 和 stdout 完全一致。

两份 receipt 都固定了上述 script、theorem、先前独立报告的正确哈希。`stopped_status.json` 也列出 `attempts_used=2`，两个 task 均为 `succeeded`，没有把旧失败覆盖成成功。

历史失败仍被正确保留：`b12_work` 中 attempt `aac8df9a...` 固定的是旧脚本哈希 `5a8f2f...`，其 `principal_angle_identities_pass=false`、exit 1；repair window 的成功 attempt 固定新脚本哈希 `7bf402...`。二者是有版本区分的失败→修复证据链，不是相互矛盾的同一执行记录。

### 对 `stopped_status.json` 的必要限定

`status="stopped"` 只表示本次有限 repair window 已停止；文件同时保留：

- `complete_goal=false`；
- `idea_status="active"`；
- `journal.scientific_certification=false`；
- stop reason 明确写有 `overall research continuation pending`。

因此它支持“修订后的有限诊断完成并成功”的窄结论，不支持“整个研究目标完成”“科学结论认证”或“允许进入论文/代码阶段”。

## 6. 最终门禁

| 门禁 | 结论 |
|---|---|
| 此前报告的三项 theorem 修复 | **PASS / 已闭合** |
| equal-rank singular-value 措辞 | **PASS / 已闭合** |
| CPU 命题量词修复 | **PASS / 已闭合** |
| repaired finite diagnostics 与 receipt 一致性 | **PASS** |
| forced-intersection 处理作为有限诊断 | **PASS，限于当前冻结 case 与阈值** |
| forced-intersection 处理作为普遍证明/认证算法 | **不成立** |
| 原创性、论文通行证、候选方法或科学认证 | **未建立** |
| 新方法代码设计/native-5000 | **仍无授权** |

结论为 **PASS**，但只关闭此前独立报告指出的修订缺口；B12 仍是几何边界结果和下一步计算模型规格，不是新方法或论文级贡献证明。
