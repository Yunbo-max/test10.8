# B08 independent pre-execution source review

Date:2026-10-10. Scope: inspect existing-policy operational timing driver, frozen design, retained B07 references and amended audit before execution. No scientific code was executed by this reviewer. This is a source/mathematical review, not candidate approval, replication, novelty adjudication or paper verdict.

## Exact reviewed identities

| Artifact | SHA-256 |
|---|---|
| run_policy512_operational.py | `2ef7754b23b5bc2f3f2baa451a8e9e8740c681c22fdc35749a25df8234c50c1b` |
| Amended verify_policy512_operational.py | `15735d1fd4b4988d9963ac0f8a6fdf1ad15ae450a717cde6a04aec0aba4f896e` |
| B08_FROZEN_DESIGN.md | `2fb12626563e44ba1b4b08f80d4212e4e575cf12f64b8a0d8ce48b313a6d14a6` |
| Imported fd_certificate_audit.py | `12c9f80e5b380c15eb5b4757aa0e64ad276dd036c20fdf8e3613fdf0fd516c88` |
| B07 FD_POLICY512_RAW.npz reference | `b8c4f5278fa58c96c485d6f547acdd927a5cd5153528219ebc1fd6ada4744fa5` |
| Native LANDMARK512_FD_RAW.npz input | `d0de6bb598161e85557321a309e9d720cb1c398b722140725e47d8365e3ec68a` |

The first inspected verifier hashb957943a8105960fc2368cf02f23dcf328cf607b403838148b5fe41824d47909 omitted explicit certificate/held-state checks and reference hash pinning. These preflight coverage items were corrected before scientific execution. Current reviewed bytes above are the applicable source disposition; it does not transfer to later changes without scoped review.

## Operational semantics

The driver really computes direct prefix SVD only when its current operational arm queries. It does not consume saved B07 per-prefix OPT/bases as an oracle. Baseline maintains its own queried OPT cache; fd50 independently maintains that cache plus the running maximum of the tol-subtracted FD lower bound. A false exact query can change its own cache without changing Q. This is the same adaptive own-cache policy previously reviewed, not a shared-cache counterfactual.

The FD class is the exact reviewed unbatched delayed width50 implementation. Its trace coefficient50 and lower bound tail+(50-k)Delta are correct under the documented source assumptions; tolerance subtraction and running maxima match B07. Each row is inserted before its FD bound gates the current prefix. Both arms use identical direct full-prefix residual arithmetic, eta, rank, energy allowance and growth convention.

The conditional update logic is consistent: growth prefixes t<=25 necessarily query and update; after growth, u is true only on a true exact-confirmed residual inequality violation. When u is true, the queried SVD supplies Q=v[:min(k,t)].T.copy(). The copy releases the irrelevant backing matrix and avoids the B07 scaling defect. Nonquery prefixes cannot update. Every exact query supplies both tail OPT and the refresh endpoint, preserving the B07 source map in ideal arithmetic.

Reference key construction is correct: eta texts0.01/0.1 format to eta0.01/eta0.1 and select classic_delayed_ell50_baseline or strong masks. The B07 stored incoming residual belongs to the common full-refresh trajectory; using it for both arms is justified by their B07 verified common update sequence and shared endpoint source. The audit compares exact query/update masks, queried OPT and incoming loss trajectory. It does not directly compare saved projectors, because neither reference nor operational raw arrays contain full output projectors; projector parity is source/map derived and supported by residual parity, not an independently measured matrix-by-matrix result.

## Audit coverage and amendments

The amended evaluator pins the exact B07 reference byte hash, validates operational NPZ CRC/hash, checks summary counts, and checks gate_lower<=reference_OPT+tol. For fd50 it also checks every operational FD bound<=reference_OPT+tol. At every held-state prefix it independently checks incoming residual<=(1+eta)reference_OPT+tol. These predicates close the explicit no-held-output/certificate-violation item in the frozen design without changing the timed driver. On refresh prefixes, feasibility follows from the source-qualified exact top-k SVD map; the evaluator does not recompute a post-refresh projection residual there.

Numerical checks remain energy-scaled empirical allowances, not a floating-rounding theorem. The cached_before/gate_lower/FD bounds and Delta arrays improve inspectability of the operational state. Query nesting remains an observation rather than an acceptance requirement. The auditor's equal expected-update comparisons indirectly imply baseline/fd50 update equality, since the exact frozen references have equal update masks.

The verifier expects all three repeats and12 complete runs. This matches the intended complete experiment if calibration permits. If the frozen budget fallback produces a smaller completed matrix, this fixed-three-repeat verifier cannot approve it; a separately scoped, prospectively documented evaluator must first reflect the actual retained matrix, and a three-pair speed claim remains unavailable. Missing or failed cells must never be silently dropped to make the current auditor pass.

## Timing fairness and resource scope

Each arm runs in a separate process and pays for its own operational queried SVD calls, residual projection work, FD maintenance, bound-spectrum queries and loop bookkeeping. Full-loop CPU/wall measurements now constitute actual operational processing measurements, unlike the B07 modeled component subtraction. Component timers do not replace whole-loop timing. Both policies retain the same residual arithmetic and diagnostics, so the difference isolates the gate's operational tradeoff within this chosen implementation.

The timers begin immediately before the streaming loop, after imports, input load, tolerance setup, FD construction and diagnostic-array allocation. JSON/NPZ saving and external audit are also outside the algorithm timer. Accordingly report the primary measurement as the complete **stream-processing loop** of this policy implementation; it is not full command/startup/import/I/O latency. The FD construction itself is excluded along with common setup. Command wall/CPU/RSS still capture those costs and must be separately retained. First operational SVD/workspace effects inside the loop remain charged to each fresh process.

The newly frozen interleaved arm ordering avoids always placing the same policy first. Repeat identity must be retained for paired ratios/differences. It does not make repeats or prefixes independent scientific samples, nor provide global confidence about cross-dataset runtime. The frozen positive condition requires lower FD CPU in all three paired measurements at a given eta and a positive median difference; the audit records paired measurements but does not itself grant this speed verdict. Report each eta separately, preserving any adverse pair.

The driver keeps only current Q and the most recent SVD backing arrays, rather than every-prefix full bases. Other retained numeric arrays are small512-length diagnostic vectors plus native512x2704 A and current FD50x2704 sketch. No analogous2.6GiB retention bug was found.2GiB address space and numerical threads1 are configured in source; one-process discipline, actual cgroup limits,120s timeout,32attempt/600s cumulative window and remaining reservations remain executor/ledger duties. The budgeted calibration is a runtime probe, not a promised upper bound.

## Disposition

**No remaining source blocker for running the currently frozen complete B08 operational timing matrix under its executor budget.** Semantic-equivalence and scoped certificate predicates are prospectively testable with the current artifacts. Retain failed commands and mismatching arrays; do not lower criteria after results. Post-run independent reviewer inspection remains required before reporting completion or positive speed evidence. The original5000 protocol, unseen confirmation, mathematical discovery, originality and paper readiness remain separate unresolved tasks. The retired Newton branch remains retired.

## Pre-audit provenance amendment after operational runs

The12 operational runs are now complete, but the scientific semantic audit has not yet executed. Reviewed amended verifier hash `29be14f9df38ee284e8d65f5c7da650aa5d488e0f17b1a2e477fb22a1d78b7d7` and frozen B08_RUN_MANIFEST.json hash `88d1b10169b5b5b7345d7530d36002bd1a5fd1c98c184f4e577f1d0001729164`.

The amendment adds an upfront24-entry manifest/file-hash check and writes the manifest hash into the audit output. It does not alter any semantic, numerical, certificate, count or paired timing predicate previously reviewed. This is post-run/pre-audit provenance strengthening, not changing acceptance after observing a failed scientific check. The driver hash and operational artifacts remain unchanged.

This reviewer independently inspected metadata-only bytes: the manifest contains exactly the expected12 cells (baseline/fd50 ×eta0.01/0.1 ×repeat0/1/2), each with one JSON and one NPZ. All24 current actual file SHA-256 values match their frozen entries; there are no missing/extra listed cells. Within each policy/eta, repeated NPZ hashes are identical; runtime-bearing JSON hashes differ. This is consistent with deterministic numeric outputs and separate measured repetitions, though neither hash consistency nor this metadata inspection grants semantic or timing success.

Disposition: **no source/provenance blocker for executing the amended scientific audit**, provided the task pins this exact verifier and manifest hash as reviewed. This inspection did not execute the scientific audit or regenerate any numerical result. The previously frozen acceptance predicates, report scope and pending post-run reviewer inspection remain in force.
