# B09 V2 independent repair preflight

Date2026-10-10. Scope: independently reviewed frozen repair source and prior saved audit; no scientific command executed by reviewer. This is an existing exact-query comparator repair, not a new candidate or novelty assessment.

## Disposition and identities

**No execution blocker for this bounded V2 repair on the following bytes.** Outcome acceptance remains conditional on the original exact mask/loss/OPT reference checks and complete budget/receipt settlement. No threshold relaxation is approved.

| Artifact | SHA256 |
|---|---|
| B09_V2_REPAIR_DESIGN.md | 7c2fa033e74ddbd8137fe7fab8a7fb44a53049fd1e2cceaed60173b06f09289a |
| run_cached_gram_policy_v2.py | 16719651f770e6cb85c81b6107a8c76e00f9fa2746a21f2c774e2a1db223b505 |
| Preserved B09_CACHED_GRAM_AUDIT.json | e9a2c4357d4256cd5fd5842d348dbe975a7dfb16e673112dfe7191c39329a68f |
| Preserved B09_RUN_MANIFEST.json | 46868412641e9b1fc89bf032b29a0865441b41813d649c9fba7fed546896c57f |
| Pre-V2 RUNNER_STATUS_FINAL.json | ab61f252c38002bda6568495b90bcf184b6401fa31f93a794593c6d45b1deb47 |
| Native512 input | d0de6bb598161e85557321a309e9d720cb1c398b722140725e47d8365e3ec68a |
| B07 scalar/mask reference | b8c4f5278fa58c96c485d6f547acdd927a5cd5153528219ebc1fd6ada4744fa5 |

Helpers remain the previously reviewed atomic_npz.py e2247cbe36db7138a22c938ad7c83f9a9b3e8b9f972999da7ca896a5c17d909d and fd_certificate_audit.py12c9f80e5b380c15eb5b4757aa0e64ad276dd036c20fdf8e3613fdf0fd516c88.

## Preserved falsification and repair target

The actual V1 audit has audit_pass=false and12 runs. Every run fails loss_close while passing query/update-mask, queried-OPT, gate, held-state feasibility, diagonal and summary/hash checks. These timings cannot qualify the frozen semantic-equivalent claim, even where a paired CPU difference is positive. Gram-eigensolver/QR endpoint differences are a plausible source-supported explanation; the audit alone does not isolate their causal contribution from all numerical effects. The preflight already identified this endpoint risk. V1 results and manifest remain adverse evidence; V2 is a substantive repair rather than a reclassification.

## Mathematical and source checks

The V2 Gram append is unchanged and valid by induction: adding g=A[:t]x to both symmetric border positions maintains G=A_t A_tᵀ in real arithmetic. Selective index(t-k,t-1) obtains k largest eigenvalues; OPT=max(0,E-sum(max(lambda,0))) is the real-arithmetic top-k tail objective for a PSD Gram matrix. The t<=k branch correctly returns zero objective. Numerical cancellation/condition-number concerns remain and must be checked at queried prefixes, particularly nearzero OPT.

V2 no longer reconstructs the right subspace from Gram eigenvectors or QR. It computes Gram eigenvalues only on qflag, applies the same cache subtraction and true-violation threshold, and calls the B08 full prefix SVD **only inside uflag**. Growth flags ensure all first25 endpoints are refreshed. For each true refresh, `np.linalg.svd(A[:t],full_matrices=False)` and `right[:min(k,t)].T.copy()` reproduce the exact B08 source map, including the copy that prevents retained-SVD-view memory growth. Direct reconstruction residual arithmetic and FD50 formulas are unchanged. No full SVD executes on a nonrefresh query.

If Gram OPT produces the same query/update decisions within the frozen arithmetic policy, the common SVD endpoint map and common start inductively produce the same Q and incoming-loss sequence as B08. This is a conditional prediction that the new audit can falsify. Algebraic objective equality alone cannot guarantee floating-point threshold decisions; the source's numerical Gram cache is not a universal certified lower bound without error analysis. V2 deliberately avoids changing tolerance or cache rules to make this audit easier.

## Fairness and cost boundaries

Both baseline and FD50 maintain Gram on every prefix, evaluate the same direct residual, perform their actual own-cache exact eigenvalue queries, and pay SVD on true refreshes. They use identical code for each shared operation. If masks match the reference, the two arms have the same247/.01 and125/.1 total refresh SVD calls including growth, with247/.01 and125/.1 FD queries versus433/.01 and230/.1 baseline queries. These are predictions from the frozen reference, not observed V2 outcomes. FD maintenance is an additional cost and nonrefresh eigenvalue-query removal may be too cheap to repay it. A null/reversal must remain an accepted scientific outcome.

The complete stream-loop CPU timer charges Gram, residual, eigvals, refresh SVD and FD costs. Input loading, imports, initial allocation, saving and external audit are excluded, matching B08's loop scope. Component exact_eigvals is correctly separate from refresh_svd. The refresh_svd component ends before Q copying, so the copy is charged in whole CPU/bookkeeping rather than this component; no cost is omitted from whole-loop timing. V2 avoids full SVD on false queries but adds Gram/eigenvalue work at true refreshes; it is a concrete stronger-control implementation, not a proof of optimal baseline engineering. Do not add modeled component savings to measured whole CPU or compare excluded startup-to-output costs as if measured.

V2 uses separate B09V2 filenames, retaining V1 results. Selective eigensolver arrays are not cumulatively retained; the current Q is copied and compact. The512 memory pattern stays bounded well below2GiB before measured library/workspace overhead. Actual serial commands, thread settings, timeout and RSS remain mandatory. Pre-V2 status records15 attempts,59.80404277500929 command-wall seconds, reservation0, with17 attempts and540.1959572249907 wall seconds available;12 operational runs plus one audit fit the attempt cap prospectively, provided actual wall/deadline costs do so. These historical costs must remain charged. Do not reset budgets or reservations.

## Necessary post-run gate

Pin V2 source/design and freeze a new manifest without overwriting V1. Review the adapted auditor, compare raw masks exactly and OPT/loss at the unchanged energy-scaled1e-10 tolerance, verify gate<=OPT+tolerance and held-state feasibility, record all successful/failed receipts and actual zero reservations. Same-prefix repeats remain timing variability measurements, not independent scientific confirmation. Passing this scoped repair does not transfer qualification to V1 or to a Gram-subspace implementation, does not establish native5000 resources, recourse gain, novelty, or paper readiness. Literature coverage remains incomplete.
