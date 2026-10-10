# B07 independent pre-execution source review

Scope: existing comparator qualification only; no numerical execution by this reviewer. Reviewed frozen diagnostic and its cited author comparator on 2026-10-10. Verdict: **changes required before treating the current acceptance gate as sound**. The FD algebra is correct for the two explicit widths, but adaptive cache feedback invalidates the asserted query nesting guarantee.

Reviewed identities:

- Original inspected content, now preserved as fd_certificate_audit_v1_unexecuted.py: SHA-256 `742ba4123dc2f8df8f105bd842b25c14cec0d4c56e0c7df088c3495fac2ad3d4`.
- First amended fd_certificate_audit.py (v2) SHA-256 `d3b7be97f0a4941e30ca0b111eda5e2ffe63a9e513eaeb26aba88bd3cb5bedee`.
- B07_FROZEN_DESIGN.md SHA-256 `98ff475ef5d680d6885af3e13981ab261e77933cc477fd8adabca7104cfbc4f2`.
- rsi_b07/sources/consistent-fd.py SHA-256 `c6d39858abb4c074048c7098575d3145627d7f54fa4a25668d61d2480da85217`.
- atomic_npz.py SHA-256 `e2247cbe36db7138a22c938ad7c83f9a9b3e8b9f972999da7ca896a5c17d909d`.

These conclusions are source-specific. Subsequent changes require scoped re-review rather than inheriting approval.

## 1. Blocking logical defect: independently updated OPT caches

The two replay arms start with separate `cached=0` variables and each updates its cache only on its own operational queries (lines 73–84). Therefore `max(strong_own_cache,FD_bound)` need not dominate the baseline arm's cache at the next prefix. A baseline false query can acquire a stronger OPT cache while the FD arm skips that prefix. The latter may query at a later prefix that the baseline now skips. The proof in INDEPENDENT_MATH_REVIEW.md guarantees output/refresh parity for any valid gates, but guarantees query nesting only with pointwise **cross-arm** lower-bound domination.

Concrete exact-arithmetic falsifier for the claimed general nesting premise: take k=1, eta=.1, tau=0, common Q=e1, C_1=diag(100,10), and cached_OPT=0 before the first scored prefix. A certified external bound 100/11 makes the strong gate skip residual 10; the baseline gate queries and caches OPT=10. Insert energy .1 along e2 to obtain C_2=diag(100,10.1), while the external bound stays 100/11 (still valid and nondecreasing). The strong gate now queries residual 10.1 against threshold 10, but baseline skips against threshold 11. No refresh occurs and all bounds/certificates remain valid. This logical construction is not a benchmark and is not a claim that the specific FD run will realize those numbers.

Consequences:

- `query_not_subset_count==0` at line 99 must not be a required theorem-backed gate for these adaptive arms. It may be measured and happen to hold in this dataset.
- `false_queries_removed` is presently **net query-count difference**, not necessarily a nested set of removed calls. Report baseline-only, strong-only, and net counts separately; output parity makes non-initialization asymmetric queries false queries.
- `oracle_cpu_saved_in_replay` currently sums only baseline-only calls. With any strong-only calls, net saved component CPU must subtract those costs.
- Forcing a shared cache would establish pointwise nesting, but supplying skipped-prefix exact OPT to the strong arm would be counterfactual and must be labeled accordingly. Keeping the two real adaptive caches and weakening only the unsupported nesting claim is the simpler scientifically faithful repair.

Refresh-mask equality remains a valid prospective falsifier under common starts, exact shared oracle and map, and valid lower bounds.

## 2. FD trace factors: correct, with semantic qualification

The classic arm waits until its ell rows are full, shrinks with sigma_ell^2, and then inserts the new row into the guaranteed zero last row. Exact shrink loss is ell*delta. The delayed compression schedule does not invalidate the trace identity or directional loss certificate. The all-prefix tail+(ell-k)Delta bound is correct for this schedule in exact arithmetic.

The augmented arm appends x to a full ell-row sketch, SVDs the resulting ell+1 rows, shrinks retained ell modes by delta=sigma_(ell+1)^2, and discards the bottom mode. Its loss is ell*delta+sigma_(ell+1)^2=(ell+1)*delta. The frozen design correctly uses `(ell+1-k)*Delta`, rather than transplanting the classic coefficient. This is a special augmented case of the more general batched trace caveat in the mathematical review, not a contradiction of it.

However the author `append()` scans for the first **exact zero row on every call**. The diagnostic pointer only rescans after an augmented shrink. If an inserted input row is itself zero, the diagnostic consumes a slot whereas the author would reuse it on the next insertion; this can change shrink scheduling/representations. The covariance theorem may remain sound, but exact source semantics have not been preserved for arbitrary streams. For an author-semantic qualification either use that per-call scan or explicitly establish no zero-input row is encountered and label this assumption. Do not claim author equivalence from the trace identity alone.

The author file's experiment initializes capacity25; the diagnostic's capacity50 is an attributed implementation qualification at a different width, not reproduction of that author configuration or the full4999-prefix run.

## 3. Exact oracle, trajectories and tolerances

Direct all-prefix `svd(A[:t])` with squared tail `s[k:]@s[k:]` is appropriate and avoids near-zero subtraction of captured energy from total energy. The parent hash and shape assertions establish input identity. Comparing stored parent OPT to recomputed OPT is an additional empirical check, not an independent proof of numerical exactness.

The same stored `ref_v` feeds both replay arms, and their residuals are recomputed by direct projection on the entire prefix. This is a common deterministic full-refresh map. Mandatory growth updates for t<=k are outside the trigger theorem but match between arms; scored counts properly slice them away. The map is full exact top-k refresh, not the retired Newton boundary solver.

`tol=1e-10*max(1,energy)` is the prospectively frozen **energy-normalized absolute** allowance. It is not a 1e-10 relative-OPT allowance; large-energy near-zero-OPT prefixes have potentially substantial tolerance relative to their OPT. The separate `opt>tol` classification and omission of ratios below that cut are appropriate. Subtracting per-prefix tol from the FD and cached bounds is empirically conservative to the frozen allowance, but is not a rigorous floating rounding certificate. Taking maxima of earlier lower bounds is mathematically safe under insertion-only monotonic OPT.

Only the baseline incoming residual is saved; storing strong incoming residual, both incoming lower bounds, both cache histories and true-violation masks would make numerical parity and cache feedback independently inspectable. Refresh-mask parity plus the shared refresh map implies idealized output equality, but explicitly saving/checking the common-state assumptions would be stronger evidence. This is an auditability improvement, not a reason to run unrelated experiments.

The script does not directly test D PSD or ||D||<=Delta at all prefixes. Its all-prefix scalar bound and trace checks test the frozen diagnostic's requested acceptance criteria, while full covariance validity is currently justified by the source mathematics in exact arithmetic. The report should distinguish those scopes.

## 4. Timing and failure preservation

Every FD step includes a sketch singular-value-only decomposition, including insertion-only steps; the charged `update_cpu` thus includes the per-prefix decomposition needed for the diagnostic bound, as well as FD shrink costs. It is not pure FD-append time. The `decompositions` count records both, which is transparent. It also omits the tiny tail/bound scalar arithmetic outside the timer. These are single-pass component diagnostics, not paired production measurements or a global speed test. The explicit `timing_status` disclaimer is suitable once net oracle savings are corrected for asymmetric calls.

All exact OPT SVDs are computed regardless of operational gate decisions, so `oracle_cpu_saved_in_replay` is a modeled component saving from measured calls, not executed end-to-end savings. Source/environment differences in real operation could change those costs. Residual replay, file output and audit overhead still consume actual research CPU and are included only in overall usage/runner costs.

**Failure-preservation blocker:** all acceptance assertions precede the NPZ and summary writes (lines 98–100). A scalar certificate failure or unsupported nesting failure would abort without saving the per-prefix evidence needed to diagnose it. The runner may preserve the exception/logs, but the raw arrays would be lost. Save complete raw arrays and a PASS/FAIL summary before raising on failed acceptance, or use a failure-safe finalization path. The existing atomic writer refuses overwrite, checks ZIP CRC, flushes/fsyncs, validates both before and after replacement and verifies hashes; that persistence machinery is suitable once invoked on failed outcomes too.

## 5. Scope-limited disposition

Proceed after correcting unsupported query nesting as an acceptance requirement, reporting net asymmetric-query cost correctly, and retaining numerical failure artifacts. Match the author zero-row scan or explicitly qualify its domain. No new-method approval, source-wide approval, novelty clearance, new benchmark confirmation or paper PASS follows from this source review.

## 6. Pre-execution amended-source check (v2)

The first amendment, hash d3b7be97f0a4941e30ca0b111eda5e2ffe63a9e513eaeb26aba88bd3cb5bedee, correctly removes the unsupported query-nesting assertion while retaining observed query asymmetry. It also scans every exact zero row at the beginning of every augmented step, matching the author's insertion semantics. B07_PREFLIGHT_CORRECTION.md, hash 0a513ae11b0338e85624eb01bea130fff4ec680f8ca32e6e3b3717d4cabfdbd8, explicitly records the prospective correction and absence of any executed first version. These two review findings are resolved. Net oracle-cost reporting and failure-safe raw persistence remain unresolved in v2; they were immediately communicated before execution.

## 7. Final pre-execution source disposition (v3)

Re-read the complete final script, SHA-256 `12c9f80e5b380c15eb5b4757aa0e64ad276dd036c20fdf8e3613fdf0fd516c88`, and amended correction note, SHA-256 `a11c67f0f50427c37f52ce9d34c87b10ea1eef0bfeea65715679e2f3b0025040`. The script now separately reports removed and added oracle component CPU and their signed difference. It computes a qualification flag, saves the complete raw NPZ and summary, and only then raises for failed certificate/refresh parity. These address the remaining preflight findings; the preliminary top-of-document verdict refers to v1, not this final version.

**Disposition: no remaining source blocker for executing this narrowly frozen development diagnostic.** All scientific/measurement limitations above remain: floating tolerance is empirical, covariance PSD/spectral guarantees are derived rather than numerically exhaustively checked here, adaptive own-cache gates have no unconditional query nesting, component timings are neither fair repeated production runtimes nor end-to-end realized savings, and the data are the existing 128-row development prefix. Mathematical output parity remains the appropriate acceptance condition, while query differences and net component CPU are signed observations. This disposition is specific to the final hash and grants no benchmark/novelty/paper verdict. Post-run arithmetic audit remains required.

## 8. Prospective native512 comparator qualification extension

Separately reviewed before execution: landmark512_fd_qualification.py hash `0cbdebe75bdf7951f733db5cd61a4e9178a9e225a65e19a564ee511753d57f22` and B07_LANDMARK512_QUALIFICATION.md hash `cae84037fe3e86ae6870aceada13248fd6f50c0204144e66a598ba3411c47fef`. The imported ExistingFD file remains exactly the reviewed v3 hash12c9f80e5b380c15eb5b4757aa0e64ad276dd036c20fdf8e3613fdf0fd516c88.

The extension verifies the exact parent Matrix Market hash, shape and nnz, slices512 rows while sparse and only then densifies. It retains the native dimension2704 and rank25. It computes direct-SVD tail OPT at exactly the frozen eight prefixes128/160/192/256/320/384/448/512, and processes all512 rows through the unchanged existing FD variants. The coefficients50/100/51, energy allowance and failure-safe persistence match the established derivations. A per-row FD spectrum call is included in maintenance cost. No adaptive policy or continuous output-quality claim is produced.

Disposition: **no source blocker for this bounded existing-comparator shape/resource diagnostic**, conditional on the externally enforced one-job/window120s budget and current resource allowances. Independent checkpoint arithmetic/covariance audit remains necessary. The final Delta/OPT and tail-gap values must determine whether it actually reaches a lossy approximation regime. `positive_delta_prefixes` merely counts Delta>0 and can count rounding-sized debt; it does not alone show meaningful shrink. `checkpoint_effective_rank` is the count of singular squares above the frozen energy allowance, not literal algebraic rank or a universal machine-rank convention. As before, a source check grants no boundary/Newton parity, new-method, novelty, holdout-confirmation or paper verdict.

## 9. Prospective full-prefix native512 gate-policy development diagnostic

Reviewed original unexecuted fd_policy512_v1_unexecuted.py hash `6d9fe2099f42b4e0baa70f5912c12c170098e2aa55915e78d9af90fca6f45359`, corrected final fd_policy512.py hash `26a583b7ea29f09e877ea293066aefc200dcdc8bea79a158396d63fd361013db`, verify_fd_policy512.py hash `ad26b18d092ec096a75154beae104079fb950b63a5501da63b78ca2257e71684`, and amended B07_POLICY512_FROZEN_DESIGN.md hash `9246a7b54de521de5df330c2c0b5fe8e3cefa30ba87e2fdd2337cdb1c9767022` before execution.

### Caught and repaired memory-scaling blocker

The original128 policy stored `v[:min(k,t)].T` as a view. At512, those views retain the complete t-by2704 right-SVD matrices for every prefix: total2704*512*513/2*8=2840887296bytes (2.64578247GiB), already above the2GiB address-space cap. This was a deterministic source-scaling problem detectable before execution. The first512 version is preserved and was not launched. The corrected version stores a `.copy()` of the truncated top-k basis, reducing retained basis arrays to270400000bytes (0.25182962GiB). The only source diff between the preserved first512 version and corrected version is that copy. It preserves identical basis values and deterministic refresh maps while releasing irrelevant full-SVD backing arrays. It does not constitute a new method or relaxing a scientific gate.

### Remaining source disposition

The corrected diagnostic uses the exact audited native512 raw parent hash, recomputes all512 direct-SVD OPTs and bases, and confirms OPT agreement at the parent's eight exact points. The reviewed FD shrink algebra and independent-cache replay logic are unchanged. Mandatory growth prefixes remain outside scored query counts; output-mask parity is asserted, query nesting is only observed, and removed/added/net oracle component CPU is recorded. Raw data and summary persist before the final scientific acceptance assertion. The covariance snapshot points are the diagnostic's deterministic linspace26..512 schedule, not the earlier fixed8 qualification schedule; source-defined snapshots are distinct from the all512 scalar checks.

The audit recomputes all512 OPTs using row-Gram spectra,1536 variant-prefix scalar bounds, trace histories,24 signed-covariance snapshots, and saved policy mask/count/net-cost summaries. It still does not regenerate the two exact state/cache histories independently. The producer maintains distinct own-cache histories during execution; the arrays do not explicitly log every cache value, though those histories are reconstructable from saved query masks, OPT, tolerance and initial zero cache. Do not call that a separately executed recursive-state audit.

**Disposition: no remaining source blocker for executing the corrected bounded development policy diagnostic.** The120s timeout is a prospective resource cap, not a runtime guarantee; if exceeded, retain its receipt and analyze rather than blindly repeating.2GiB address cap and cumulative-window accounting remain externally enforced. Measurements remain single diagnostic component timings, not repeated fair production timing or unseen scientific confirmation. No new candidate/novelty/paper verdict is granted by this preflight.
