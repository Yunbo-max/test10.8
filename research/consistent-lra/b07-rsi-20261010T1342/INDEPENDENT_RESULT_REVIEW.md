# B07 independent source/result inspection

Date: 2026-10-10. Scope: inspect the frozen source, saved diagnostic outcomes, raw scalar arrays, and a separately executed arithmetic audit. This reviewer did not independently rerun scientific experiments, reproduce the trajectory, or execute another SVD/Gram evaluator. The distinction between independent reviewer and independent scientific replication is retained.

## Exact artifacts inspected

| Artifact | SHA-256 |
|---|---|
| Final diagnostic source | `12c9f80e5b380c15eb5b4757aa0e64ad276dd036c20fdf8e3613fdf0fd516c88` |
| FD_CERTIFICATE_RAW.npz | `1278c446a80ef41ec34e59dfcb2767bec5ef75f87a0345f70b37c609d8247cf5` |
| FD_CERTIFICATE_SUMMARY.json | `0c22b5bd2fbe06050070b54e1809a459fe995d9641afdca3c581975991ef5278` |
| verify_fd_certificate.py | `bf39bf049c0d55e1b36748d52dc7b33eb88889517a218270175d532d5249c884` |
| FD_LIVE_AUDIT.json | `15a7cfe1bc026f3897d15da0160a1f085f1dede601e1528b9571398b18f1e795` |

The actual raw file hash matches both saved receipts. Its 56 arrays include A.shape=(128,2704), all-prefix delta/bound/tail/cost values and masks, and eight sketch checkpoints per variant. Byte/data inspection was limited to reading saved arrays and scalar extrema; no scientific replication was performed.

## Verified scope and observed results

The diagnostic reports qualification_pass=true. The arithmetic audit reports audit_pass=true, with 128 all-prefix Gram-vs-SVD OPT comparisons, 384 variant-prefix bound comparisons, 384 scalar trace checks, and 24 checkpoint covariance comparisons. Gram OPT differs from the direct-SVD tail by at most 4.831947204853776e-16 normalized by max(1,prefix energy). The direct-SVD path and independent row-Gram path use different arithmetic. The thin-QR signed-covariance construction in the auditor correctly preserves all nonzero eigenvalues of A^T A-B^T B; adding implicit zero eigenvalues is accounted for by its min/max clipping.

For all three variants, each policy has zero refresh-mask differences. At eta=.01 both arms issue 35 scored queries and make 35 scored full refreshes. At eta=.1 the baseline issues 34 scored queries, the FD arm issues 31, and both make 31 scored refreshes. The audit finds three baseline-only calls, zero strong-only calls and zero net component-cost discrepancy. Query nesting happens in this data; it remains an observation, not an unconditional adaptive-cache theorem.

| Existing comparator | Maintenance plus per-prefix sketch-spectrum CPU | Modeled oracle CPU saved at eta=.1 | Modeled net CPU change from adding FD |
|---|---:|---:|---:|
| classic delayed ell50 | 0.343714785 s | 0.107434245 s | +0.236280540 s |
| classic delayed ell100 | 0.388879271 s | 0.107434245 s | +0.281445026 s |
| author augmented ell50 | 0.197454655 s | 0.107434245 s | +0.090020410 s |

Here positive net change denotes greater component cost. At eta=.01 there is no modeled oracle saving, so the entire measured maintenance component is added. These are component diagnostics from one execution, **not repeated fair end-to-end timings**. They establish no production speedup; the most favorable observed component budget is still negative for adding this FD gate. Mandatory exact-confirmation refreshes are unchanged, as the mathematics predicts.

The retained diagnostic records 4.53092858 CPU seconds, 4.533746133 wall seconds and peak RSS279616 KiB; the retained arithmetic audit records 0.731162131 CPU seconds, 0.731222654 wall seconds and peak RSS101956 KiB. These are in-process measurements, not the complete runner/window budget. This reviewer does not replace the authoritative runner ledger with them.

## Material limitation: this prefix barely exercises nonzero shrink

Each variant classifies 110 of128 prefixes as near-zero OPT at the frozen energy-scaled allowance. Only18 prefixes contribute the positive-OPT ratio summaries. Terminal prefix energy is30.108423750145157 and exact-tail OPT is0.0009566167780586317.

The saved maximum cumulative shrink debts are exceptionally small:

| Variant | max Delta | Terminal tail and bound |
|---|---:|---:|
| classic ell50 | 6.837133172657547e-22 | 0.0009566167780586353 |
| classic ell100 | 9.300843301631507e-31 | 0.0009566167780586304 |
| author augmented ell50 | 9.465979295004529e-24 | 0.0009566167780586388 |

For all three, terminal `bound` and `tail` are numerically identical at displayed float precision. The certificate is almost the exact retained-prefix tail; the additional trace-debt term does not materially contribute. This qualifies plumbing and this native input's tolerance-relaxed certificate, but provides essentially no stress test of the nonzero-shrink factor, its accumulated covariance loss, or the approximate-sketch regime. The three variants' coincident query outcomes are not three independent scientific confirmations.

The checkpoint covariance eigenvalues illustrate the limitation: at prefix128 the ell50 classic D has maximum eigenvalue about1.7492e-13 while its stored Delta is6.8371e-22; there are also negative eigenvalues around -7.7e-14. These pass the frozen allowance of approximately3.01e-9, not a literal exact-arithmetic 0<=D<=Delta I test. The source theorem and floating tolerance must be reported separately. Ratios close to1 on the18 positive prefixes do not establish sharpness of a substantially lossy FD certificate. No relative-OPT conclusion is available for the110 near-zero prefixes.

## What the live audit does and does not verify

The live script recomputes OPT/energy using row Gram and direct norm paths, checks bound/trace formulas, and explicitly checks covariance loss at eight saved prefixes per variant. It recomputes query/count/cost summaries from saved masks. It does **not** independently regenerate the two policies' exact state/cache histories, recompute strong-arm residuals, or qualify covariance bounds at every prefix. Those are not hidden failures, but scope boundaries. Source inspection plus saved shared-map refresh parity supports this development diagnosis; it is not a separately reproduced scientific result.

The audit's provenance validation, positive near-zero allowance, and retention of signed query/cost observations are appropriate. No source or saved-output inconsistency requiring invalidation was found in this scoped review. Strict covariance certification, full high-dimensional protocol evaluation, unseen confirmation, and novelty coverage remain unresolved.

## Narrow RFD source observation

Primary source inspected: Luo et al., *Robust Frequent Directions with Application in Online Learning*, JMLR20(45),2019, https://jmlr.org/papers/volume20/17-773/17-773.pdf, Algorithms1–2. They use the same B shrink update; RFD additionally accumulates alpha by half the discarded singular square and represents covariance as B^T B+alpha I. Thus, with matching initialization and schedules, alpha alone does not alter the B trajectory. Adding an isotropic shift preserves eigenspaces and eigenvalue ordering; a deterministic top-k extraction therefore does not obtain a different projector merely from alpha. Degenerate eigenspaces still require common tie-breaking. Its covariance/inverse conditioning improvement cannot be relabeled as different subspace recourse. This is a primary-source observation and mathematical inference, not an implemented comparator, novelty adjudication or comprehensive RFD literature audit.

## Scoped disposition and useful next action

Accept these artifacts as **development-only existing-comparator qualification with a retained component-cost negative result**. The certificate/refresh implementation checks pass within the prospectively frozen tolerance, and the source-derived unchanged-refresh prediction is consistent with saved data. There is no support for faster operation, lower recourse, a new method, unseen confirmation or paper acceptance.

A subsequent native-data resource-calibrated prefix can address whether significant shrink ever appears; report Delta/energy, covariance loss and positive-OPT coverage before treating the matrix dimension alone as a demanding sketch test. Existing development data remain development data. The current result should remain in the record regardless of the next direction.

## Native512 fixed-checkpoint extension: independent inspection

The separately frozen existing-comparator qualification and its live arithmetic audit have now completed. This reviewer inspected their saved sources/JSON/raw scalars and hashes; no new scientific command, SVD, policy replay, or regenerated experiment was executed by this reviewer.

| Artifact | SHA-256 |
|---|---|
| landmark512_fd_qualification.py | `0cbdebe75bdf7951f733db5cd61a4e9178a9e225a65e19a564ee511753d57f22` |
| LANDMARK512_FD_RAW.npz | `d0de6bb598161e85557321a309e9d720cb1c398b722140725e47d8365e3ec68a` |
| LANDMARK512_FD_SUMMARY.json | `38fc8735a98daf3a1c121c1821c3cc4be1c3abdc8ad37b8cba1834deab3628c7` |
| verify_landmark512_fd.py | `bac3f15e35bebfc3bed5b11f4a444ffa5ec01428fb312dd9fb7deb8e0066ab39` |
| LANDMARK512_FD_LIVE_AUDIT.json | `c7a6fe8f3f74f9429a8291fdc2f17feef6f8d70dbb195b76f1e7eef40fbb0826` |

The actual raw file hash matches both saved receipts. Its27 arrays contain512x2704 native A, all512 scalar FD histories, and sketches at exactly128/160/192/256/320/384/448/512. Native Matrix Market hash remains29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b. The native slice array hash is3c28b6310309dd64e9b04a8eaa16c47ae3f9de13bc43027422091bbba0f383b8.

The source-approved qualifier reports qualification_pass=true and the alternate arithmetic audit reports audit_pass=true. There are24 checkpoint-variant comparisons with144 scalar predicates, and all512 trace histories pass their frozen allowance. This **does not mean512 exact-quality checks**. Exact OPT and covariance checks exist only at the eight frozen prefixes. There is no adaptive query policy, continuous512 output-quality comparison, legacy/Newton parity upgrade, new-method confirmation or author's5000-protocol result.

At prefix512, energy is117.87539774695635, allowance is1.1787539774695635e-8, direct-SVD OPT is0.9821450254124238, and the energy-cutoff effective rank is64. Effective ranks at the eight prefixes are32/37/46/51/52/52/63/64. This cutoff-based effective rank is not exact algebraic rank.

| Existing comparator | Terminal Delta | Delta / frozen allowance | Terminal tail | Terminal bound | Bound / exact OPT |
|---|---:|---:|---:|---:|---:|
| classic ell50 | 4.271866897763181e-4 | approximately36240 | 0.9714647174449832 | 0.9821443846893911 | 0.999999347628898 |
| classic ell100 | 1.580996499084514e-29 | approximately1.34e-21 | 0.9821450254124217 | 0.9821450254124217 | 0.9999999999999979 |
| author augmented ell50 | 2.7017568612330216e-4 | approximately22920 | 0.9751201645766090 | 0.9821447324158149 | 0.9999997016768387 |

The two width50 variants now materially exercise shrink: their covariance-loss maxima at512 are4.2718669041512245e-4 and2.701756874508685e-4, respectively, consistent with Delta within about1e-12. Their debt is many orders above the frozen numerical allowance. The trace-derived lower bound adds25*Delta or26*Delta to the retained sketch tail, a material contribution that was absent in128. It recovers a bound very close to exact OPT on these fixed checkpoints; closeness is a measured property of this native prefix, not a universal accuracy guarantee.

The width100 variant remains essentially lossless at this scale. Its Delta is rounding-sized despite412 reported positive-debt prefixes. This directly demonstrates why positive_delta_prefixes alone is insufficient to claim a stress test. The native512 extension qualifies meaningful nonzero debt for widths50, but supplies no such evidence for width100.

Checkpoint covariance matrices retain tiny negative eigenvalues (about1e-15 in the materially lossy width50 tail and up to1.6e-12 in width100). The floating comparison remains tolerance-relaxed, not a literally exact Loewner certificate. Row-Gram OPT matches the direct-SVD tail within the frozen allowance at all eight points; those repeated data/configuration points are not independent scientific samples.

Maintenance plus bound-spectrum component CPU is1.644776818s for classic50,3.691283032s for classic100, and1.788116301s for augmented50. The eight exact-OPT checkpoint SVD calls total0.279572060s. Comparing those values as a speed ratio would be invalid: the FD costs process512 rows and include per-row bound-spectrum work, while the exact oracle costs cover only eight selected calls. No oracle savings or production speed benefit were measured in this extension. The qualifier reports8.528873196CPU seconds/8.444410260wall seconds/RSS127440KiB; the live audit reports2.076634572CPU seconds/2.077157006wall seconds/RSS177548KiB. In-process measurements do not replace the authoritative runner/window ledger.

### Machine next-step recommendation

Retain both128 and512 evidence. The512 findings resolve the specific objection that widths50 only exercised numerical shrink debt. They do not resolve the earlier runtime negative result or establish novelty. A sensible next empirical step is a separately frozen, budget-calibrated native512 **full-refresh baseline and trigger-only FD gate policy comparison** using common initialization, independently tracked own-cache histories and source-qualified legacy refresh, if resource calibration permits. Recompute exact-confirmation decisions across the evaluated stream and measure operational components fairly; record both removed and added queries, all false/true violations, and Delta/OPT coverage. Do not substitute an eight-checkpoint diagnostic for that full trajectory. This is qualification of existing assets and need not reopen the retired Newton implementation.

Before any new-method claim, return to primary-literature collision review and derive a distinct falsifiable mechanism that changes refresh policy or reduces its computation cost. The proven gate-only theorem forbids promising reduced recourse from a lower-bound-only change. RFD's isotropic compensation likewise supplies no different projector merely by adding alpha. New candidate screening, unseen confirmation and full author5000 protocol remain separate pending work.

Final scoped verdict: the512 fixed-checkpoint existing-comparator qualification and its alternate arithmetic audit are coherent with the approved source and recorded bytes, including meaningful width50 shrink. Accept as development evidence only. No continuous512 quality, new-method, independent experiment replication, novelty clearance or paper PASS is granted.

## Full-prefix native512 gate-policy diagnostic: final inspection

The corrected, separately frozen all-prefix512 policy diagnostic has now completed, followed by its alternate arithmetic audit. This reviewer inspected the actual saved artifacts/source, byte hashes and mask-array counts; no independent experiment or additional scientific command was executed by this reviewer.

| Artifact | SHA-256 |
|---|---|
| Corrected fd_policy512.py | `26a583b7ea29f09e877ea293066aefc200dcdc8bea79a158396d63fd361013db` |
| FD_POLICY512_RAW.npz | `b8c4f5278fa58c96c485d6f547acdd927a5cd5153528219ebc1fd6ada4744fa5` |
| FD_POLICY512_SUMMARY.json | `5ca3b7d3a1d9b435f2d80688090c915ed5e40c17585af8fa6e1b9a15514bfb3c` |
| verify_fd_policy512.py | `ad26b18d092ec096a75154beae104079fb950b63a5501da63b78ca2257e71684` |
| FD_POLICY512_LIVE_AUDIT.json | `9fd1de2f4beaa0079d23a668065922c318d2a3c6badfcc63885ae530ddefacd1` |

The raw file hash matches both producer and audit receipts. It contains56 arrays with native512x2704 A, all512 exact-tail OPT values and FD scalar trajectories, policy masks and eight covariance snapshots at26/95/164/234/303/373/442/512. The array hash remains3c28b6310309dd64e9b04a8eaa16c47ae3f9de13bc43027422091bbba0f383b8. The corrected top-k-basis copy was executed; the rejected memory-retaining first version remained unexecuted.

### Recorded outcomes and justified interpretation

The producer reports qualification_pass=true. The audit reports audit_pass=true with512 Gram-vs-SVD OPT comparisons,1536 variant-prefix bound comparisons, all-prefix scalar trace checks and24 covariance-snapshot checks. Maximum OPT discrepancy normalized by prefix energy is7.829078874390072e-16. No all-prefix scalar bound or frozen trace-identity violation is reported. These are tolerance-relaxed checks; strict floating-point Loewner certification remains outside the claim.

Across all three variants, scored growth-excluded query and refresh counts are:

| eta | Stale-cache queries | FD-gate queries | Refreshes in either arm | Baseline-only calls | Strong-only calls |
|---|---:|---:|---:|---:|---:|
| .01 | 408 | 222 | 222 | 186 | 0 |
| .1 | 205 | 100 | 100 | 105 | 0 |

Raw masks inspected by this reviewer reproduce those counts. All six variant/eta replay configurations have zero refresh-mask differences. Under the reviewed shared deterministic refresh-map implementation and common initialization, the result is consistent with unchanged projectors and recourse. No separate recourse reduction was measured or permitted by the gate-only proposition. All strong-arm scored queries coincide with its scored refresh count in this native trajectory, so the observed gate eliminates all baseline false calls here. This behavior is not guaranteed for arbitrary streams/own-cache feedback; cross-arm query nesting happens in this data and is not elevated to a general theorem.

There remain110 near-zero-OPT prefixes, now out of512, leaving402 prefixes above the frozen energy allowance. Width50 delta/debt and fixed-checkpoint source conclusions persist; width100 still largely retains the effective spectrum. The three variants' identical policy counts do not constitute three independent confirmations.

### Positive component budget, still no measured whole-method speedup

| Variant | Measured FD maintenance/spectrum CPU | Modeled oracle CPU saved, eta=.01 | Modeled oracle CPU saved, eta=.1 |
|---|---:|---:|---:|
| classic50 | 1.469970344s | 14.404976795s | 6.947905818s |
| classic100 | 3.176809684s | 14.404976795s | 6.947905818s |
| augmented50 | 1.686643947s | 14.404976795s | 6.947905818s |

Unlike128, the native512 trajectory now has a **positive modeled oracle-minus-maintenance budget** for every tested variant/eta: approximately11.23–12.94s at eta=.01 and3.77–5.48s at eta=.1. This is valid reason to perform a controlled production timing experiment. It is not an executed whole-method saving: the diagnostic actually computes all512 exact OPT/bases up front, uses those stored oracle results inside each replay, replays multiple policies in one process, and separately adds measured selected-prefix oracle components. Full prefix-residual replay, output costs and state allocation are not represented by that simple component subtraction. No speed ratio or realized end-to-end acceleration is established by these files.

The diagnostic records52.614441467CPU seconds/52.631260663wall seconds/peakRSS424744KiB. The audit records6.348221460CPU seconds/6.349040653wall seconds/peakRSS183356KiB. These are in-process measurements and retain their distinct roles; the runner ledger remains authoritative for attempts, resource windows and failures. The memory repair materially enabled this scaling within the frozen2GiB cap without changing numerical endpoint values.

The alternate audit recomputes exact-tail loss through Gram spectra and verifies saved mask/count/component arithmetic. It does not independently regenerate every recursive Q/cache state. Cache histories are reconstructable from masks/OPT/tolerance, rather than explicitly stored. This is independent reviewer inspection plus alternate arithmetic evidence, **not independently regenerated scientific confirmation**. The parent source/data identities, failed preflight version and earlier128 cost-negative evidence remain part of the record.

### Next machine decision

The new positive component budget warrants Step4/5 continuation: prospectively freeze a fair full native512 operational policy timing comparison, execute each arm serially with the same initial state/data/residual evaluation and verified legacy exact refresh, and obtain repeated paired CPU/wall/RSS measurements. Compute exact OPT **only when that arm actually queries**, rather than supplying a precomputed every-prefix oracle within the timed path; retain a separate untimed/independently charged scorer and compare output decisions/projectors with the frozen reference. Track all removed/added queries and full costs, preserve the adaptive own-cache policy, and keep first-prefix growth and initialization handling identical. Do not announce a whole-method gain from modeled components. Use measured512 costs to plan any larger original5000 protocol within the finite resources; fixed-checkpoint or512 evidence does not discharge that protocol.

In parallel with the research sequence, continue primary-literature collision review and approximate-refresh mathematical discovery. A lower-bound-only gate with identical exact confirmation and refresh cannot improve recourse; any claimed distinct mechanism must alter another mathematically explicit component and receive applicable candidate screening/falsification. The failed Newton parity line remains retired. FD's established derivations and RFD's isotropic compensation remain attributed prior-work assets.

Final disposition for this completed extension: accept the immutable files as development-only full-prefix512 **existing-policy query-reduction evidence with promising component-cost accounting**. They justify the next fair timing step. They do not establish whole-method speedup, a new algorithm, unseen confirmation, independent experimental replication, original5000 reproduction, restored Newton parity or paper PASS.
