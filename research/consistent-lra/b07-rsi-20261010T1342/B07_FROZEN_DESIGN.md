# B07: existing FD certificate/source qualification (development only)

Frozen before executing numerical code, 2026-10-10. Decision workflow is Research_Autopilot autonomous-rsi@7af53173bbd69726877ca04fb77b9466ef1b839d. Retain Simple .3 digest97cdb752027748261c1d6a11980d10d7a46f2c79c2a00e975f0c08d2c8847893 solely as command transport. No new candidate implementation, method pool approval, independent benchmark confirmation or paper verdict.

Question: Can attributed FD error certificates supply a valid tighter OPT lower bound, and what is the most that a certificate-only change can improve in the existing exact-refresh pipeline?

Native data: original Landmark prefix1..128, d2704, k25, no standardization. Reuse exact A bytes in B06 LANDMARK128_RAW_V3.npz (parent hash de6f3279d021f8a442cd5f6b51ac4948457045263eb334e6cade78b0380b6dff); retain full author source hash29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b. This is the existing 128-row development subset, NOT the author5000 protocol or a fresh holdout.

Attribution: Ghashami et al., arXiv1501.01711, Algorithm2.1 and Properties1--3; Liberty arXiv2202.01780, Algorithm1/Lemma1. L=tr(C)-sum_topk(B'B)-kDelta <= OPT follows from their covariance error inequalities. For exact ell-row smallest-value shrink, L=tail(B)+(ell-k)Delta. Author consistent-fd.py uses an ell+1 augmented shrink and s[ell], so its trace debt is (ell+1)Delta; do not transplant the classic equality.

Tasks:
1. Verify parent artifact, current cgroups, runner source hashes and absence of live science; one numerical thread, single job, <=2GiB address space.
2. Qualify FD comparator algebra on ALL128 native prefixes for delayed classic capacities50/100, and author augmented capacity50. Compute reference OPT by direct singular-value tail, trace debt by both independent scalar paths, record raw per-prefix values and cost. Acceptance: bound<=OPT+1e-10 max(1,E); trace identity error<=1e-10 max(1,E). Report nearzeroOPT separately, no ratio there. Preserve failures.
3. On a fixed deterministic exact-full-refresh trajectory, replay baseline stale lower bound and max(stale,FD-bound) query policies for eta=.01,.1. Direct prefix residual norm; same exact SVD refresh map; FD costs include all per-row sketch decompositions. Predict equal true refresh masks and no missed violations; prospective falsifier is any inequality failure or differing refresh mask. Improvement metric is false queries removed, not update count or recourse.
4. Independent mathematical/source verifier; separately execute live scalar/Gram recomputation of saved qualification output (different arithmetic). No independence claim for same-agent command alone.

Budget: at most8 attempts, <=600 cumulative command wall seconds, <=120 seconds each, <=30min window; single scientific job, no GPU/dependency installs/Docker/API. Same failure <=2 substantive repairs, otherwise park affected task. Old reservations and cumulative counters unchanged. File identity/CRC/readback/hash required. Costs for diagnostics aren't production algorithm timing; no global speed claim.

Gate applicability: existing-comparator/native diagnostic and source/mathematics audit, not new/reopened discovery.20-to15 doesn't apply until an actual new-method pool is opened. No scientific descendant of failed Newton parity is launched. The exact baseline uses legacy full refresh, not the retired Newton branch. All provisional design decisions precede results. No confirmation consumed.

Outputs: FD_CERTIFICATE_RAW.npz, FD_CERTIFICATE_SUMMARY.json, FD_LIVE_AUDIT.json, INDEPENDENT_MATH_REVIEW.md, source audit/report, source/data/receipt hashes and append-only ledger/index delta. Delivery limited to test10.8/main/research/consistent-lra/b07-rsi-20261010T1342 and the existing main index.
