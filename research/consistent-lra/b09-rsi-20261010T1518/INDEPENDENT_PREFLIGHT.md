# B09 independent pre-execution review

Date2026-10-10. Scope: source and first-principles mathematical review of an existing comparator's implementation-threat audit; no scientific execution by this reviewer. B08 source/results and independent review were read as the parent evidence. This is not novelty adjudication or an independently regenerated experiment.

## Disposition on original bytes

No evident implementation-index or512/1024 memory blocker. Two scientific scope statements must be corrected in the frozen design before execution: B09 also changes residual arithmetic, and a Gram eigensolver plus QR does not automatically reproduce the SVD's deterministic endpoint in tied/rank-deficient spectra. The existing hard semantic-match criterion is essential; do not interpret timings if it fails. The1024 calibration is eligible only as five-checkpoint eigenvalue/OPT and resource calibration, not a continuous policy or full refresh-cost measurement. A final amended-design identity can be recorded below without changing these reviewed sources.

| Original artifact | SHA256 |
|---|---|
| B09_FROZEN_DESIGN.md | 974465861a0fc3f1bf567e501503c0336f55076c5c809d26a96106c8fd8cc0ee |
| run_cached_gram_policy.py | eecbe1dd40f3c4db76fc1657df1b48c1cb405d52e68d25d546d119369f34e679 |
| calibrate_cached_gram1024.py | 28058f3b458afb18768fc0a7831c52755210febfb5ce7b52a6d7e835df0fffa5 |
| atomic_npz.py | e2247cbe36db7138a22c938ad7c83f9a9b3e8b9f972999da7ca896a5c17d909d |
| fd_certificate_audit.py | 12c9f80e5b380c15eb5b4757aa0e64ad276dd036c20fdf8e3613fdf0fd516c88 |
| LANDMARK512_FD_RAW.npz | d0de6bb598161e85557321a309e9d720cb1c398b722140725e47d8365e3ec68a |
| FD_POLICY512_RAW.npz | b8c4f5278fa58c96c485d6f547acdd927a5cd5153528219ebc1fd6ada4744fa5 |
| landmark.mtx | 29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b |

## Gram and oracle mathematics

Appending row x at t requires g=A[:t]x, including the new diagonal ||x||². Assigning both G[t-1,:t]=g and G[:t,t-1]=g preserves exact symmetry and gives G=A_t A_tᵀ by induction. No earlier block is overwritten. The code's subset indices(t-k,t-1) are the largest k eigenvalues in ascending indexing and include exactly k entries. The evr selective interface supports this selection. SciPy's primary API documentation was independently read on2026-10-10: https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh.html . It also warns that eigenvalues-only and eigenvector modes can produce slightly different nearzero eigenvalues. No claim about the installed SciPy version is inferred from the current online documentation.

For PSD G, its nonzero eigenvalues equal squared singular values of A. Thus OPT_k=trG-sum(topk eigenvalues) in exact arithmetic. Positive-eigenvalue vectors q_j=Aᵀu_j/sqrt(lambda_j) are orthonormal right singular vectors. QR preserves their subspace while mitigating orthogonality error. If rank>=k with a separated kth eigenvalue, the top-k projector is unique, even though basis signs/order differ. At a tie or rank<k, optimal complements need not be unique. The t<=k QR branch is optimal but need not choose the same complement as B08 SVD. For zero selected eigenvalues, the algebraic division formula is inapplicable; the code clips negative values and floors the denominator, then QR completes the numerical range. This is a numerical completion convention, not a proof of identical SVD endpoint. It is eligible for the frozen data-dependent audit, not a generic deterministic equivalence theorem.

Gram formation squares the spectral condition number. Subtracting sum(topk eigenvalues) from total energy can lose relative accuracy when OPT is nearzero; max(0,...) suppresses negative cancellation rather than bounding its error. Tiny/negative selected eigenvalues can amplify noise in basis reconstruction. Consequently the energy-scaled1e-10 checks, nearzero OPT separation, and actual incoming-loss/update-mask comparison are mandatory. A mask mismatch must block the frozen timing interpretation even when both outputs are individually optimal.

## Policy and timing semantics

Own-cache and FD-gate formulas, growth handling, query flags, true-violation update flags, tolerance, and cache update match B08's policy equations. Every queried Gram solve is performed in that arm. The qflag/update separation is intact. Exact_q is constructed even for a false query; this is charged identically in both arms but leaves further engineering room for an eigenvalue-first, refresh-only basis construction baseline. B09 is therefore a stronger implementation control, not an exhaustive optimized exact-oracle comparison.

B09 replaces direct reconstruction residual ||A-AQQᵀ||² by max(0,E-||AQ||²). These are equal in real arithmetic for orthonormal Q, but the latter has cancellation error nearzero. This is an additional common-arm engineering change and must be named when comparing B09 with B08. It can also affect query decisions at tolerance boundaries; the saved reference audit resolves this for the inspected development data. A gate's mathematical validity is not established merely by labeling OPT exact in real arithmetic.

Whole-loop CPU includes Gram append at every prefix, FD maintenance, residuals, selective eigenquery plus basis reconstruction/QR, and bookkeeping. G/FD/array allocation, input loading, imports, output save, and external audit are excluded. These exclusions match the B08 streaming-loop timing convention, but a B08-to-B09 CPU difference is a sequential cross-implementation comparison, not a contemporaneous random paired trial. B09 baseline-vs-FD should use the frozen interleaved per-repeat pairs and all three differences, retaining null or reversal separately for each eta. Different repeated processes still use one development prefix.

The operational raw output does not include full Gram state, Q matrices, raw FD bound or Delta. It does include diagonal, energy, masks, cached/gate scalars and queried OPT. Reference audits can validate scalar/mask equivalence and gate feasibility; complete independent state/projector validation would require another instrumented scope, not silent claims that the absent matrices were checked. No new source edits are imposed by this observation for the present scoped timing test.

## Resource calibration

At512, A is11,075,584bytes and G2,097,152bytes; at1024, A22,151,168bytes and G8,388,608bytes. No per-prefix collection retains full eigensolver arrays. A retained current Q has at most2704*25 entries. The reviewed allocation pattern has no analogue of the previously caught B07 view-retention memory bug. LAPACK workspaces, imports, sparse-source parsing, and allocator overhead still require actual RSS/timeout checks; numeric thread1 and2GiB address-space caps are present. No runtime success is promised.

The calibration reads the entire MatrixMarket source sparsely, then materializes only the first1024 rows as dense A. Its Gram-building cost is cumulative over1024 rows; its oracle checks occur only at512/640/768/896/1024. It compares selective eigenvalues-only OPT against fresh singular-values-only SVD. It does not reconstruct Q, test refresh orthogonality/quality, replay gates, or measure the full operational eigenvector/QR query path. The JSON usage CPU/wall encloses source verification/read and saving up to usage collection, while input_load_wall_seconds_excluded is a separately reported component; clarify which timer is being cited. At five checkpoints, passing normalized OPT error<=1e-10 is valid limited numerical evidence. Save-before-assert retains failed numerical arrays. No1024/5000 continuous-policy speed follows.

Native5000 introduces a200,000,000byte row Gram matrix and108,160,000byte dense input, before solver workspace and temporaries; selected eigensolvers still process growing matrices. Neither512 loop cost nor1024 five-checkpoint cost justifies direct scale extrapolation or exceeding120s/600s caps. Freeze later calibration/continuation plans from actual results.

## Remaining acceptance gate

Before result qualification, an independently reviewed saved-output auditor must pin exact inputs/source/reference, check query/update masks, queried OPT, incoming residuals, gate lower bounds and held-state feasibility, and record all hashes, receipts and settled reservations. It must retain numerical or timing failures and cannot relax the prospective mask criterion after seeing results. This preflight permits a bounded experiment after the scope amendment; it does not grant outcome acceptance, originality, global recourse/speed improvement, or paper PASS. Literature coverage remains incomplete.


## Final amended pre-execution disposition

The parent amended the design and driver before scientific execution. I re-read the amended design and current residual block. Driver now uses exactly B08's direct reconstruction/norm residual rather than subtracting projected energy; the residual change discussed above is a preserved review of superseded original bytes, not the final implementation. Design explicitly acknowledges tied/rank-deficient endpoint risks, requires hard reference semantic audit before timing interpretation, and limits1024 eigenvalues-only costs to diagnostic scope.

Final reviewed hashes: design7687bf7d95005391cab5d91d6c2113aa74ab904aa313603710330c5257b272e4; driver8f2ebd61667291a352a826233a9c10852e96837ce5739a63d376c44a5b5cf011; calibration unchanged28058f3b458afb18768fc0a7831c52755210febfb5ce7b52a6d7e835df0fffa5.

**Final execution disposition: no blocker for the bounded existing-comparator experiment on these amended bytes.** Gram algebra, selective indices, own-cache flags, common residual implementation and timing boundaries are acceptable for the prospective scope. This approval is for execution only; rank-deficient endpoint behavior and nearzero numerical stability remain falsifiable by the required saved-result audit. The auditor has not yet been supplied or reviewed in this preflight. No outcome qualification or5000 feasibility is granted.
