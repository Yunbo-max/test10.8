# B09 independent saved-result review

Date2026-10-10. Scope: independent source, provenance, saved-array and descriptive-statistical inspection. No new scientific run, SVD, eigensolver experiment, or independently regenerated algorithm replay was performed by this reviewer.

## Scoped conclusion

**B08's positive FD50 speed result is not robust to the stronger exact-query implementation tested here.** The V1 Gram-subspace implementation fails its frozen loss-trajectory audit and is ineligible for semantic-equivalent timing interpretation. The V2 Gram-OPT/full-SVD-refresh repair passes the unchanged semantic audit, but FD50 is faster in only1 of6 CPU pairs. Both eta values fail the prospectively required3-of3 speed criterion and have negative median paired savings. Preserve B08 as a valid narrower result against its full-SVD-at-every-query implementation, and B09 as the implementation-threat evidence limiting its generalization.

## Artifact identities and provenance

Current SHA256 identities independently calculated:

| Artifact | SHA256 |
|---|---|
| V1 B09_RUN_MANIFEST.json | 46868412641e9b1fc89bf032b29a0865441b41813d649c9fba7fed546896c57f |
| V1 B09_CACHED_GRAM_AUDIT.json | e9a2c4357d4256cd5fd5842d348dbe975a7dfb16e673112dfe7191c39329a68f |
| B09_V2_REPAIR_DESIGN.md | 7c2fa033e74ddbd8137fe7fab8a7fb44a53049fd1e2cceaed60173b06f09289a |
| run_cached_gram_policy_v2.py | 16719651f770e6cb85c81b6107a8c76e00f9fa2746a21f2c774e2a1db223b505 |
| verify_cached_gram_policy_v2.py | 40aa4e8b30c136255c9925eefb266915b48832a81f1690d8aeaf7edd6a7ff40c |
| B09_V2_RUN_MANIFEST.json | 25f1aa6f7ba428724587a4bdfb3e3ab7cdbf36327c95d61a4598a0b4222217c0 |
| B09_V2_CACHED_GRAM_AUDIT.json | d471bde88d1108636854e596a50a38dfd35bda558ac28f49fed0978968f29572 |
| B09_GRAM1024_CALIBRATION.json | eb5aaf473db77e4139bd8c7919f2330d84581dc946e9422918bf7cab192b1f06 |
| B09_GRAM1024_CALIBRATION_RAW.npz | 93bb33977d0f28fd0ed44b066b9c5c92fe1facf666fbd5f84b1fe4b5fe88c77b |
| Final RUNNER_STATUS_FINAL.json | 909e4262f1210ddde052115c4402f4f37bc0aceb9201534e442aa2e350a3e8bc |

All26 V1-manifest files(24 run JSON/NPZ plus2 calibration files) and24 V2-manifest files match their frozen hashes. All52 output references across29 receipts match current retained bytes. Pinned B07 reference is b8c4f5278fa58c96c485d6f547acdd927a5cd5153528219ebc1fd6ada4744fa5; native512 input is d0de6bb598161e85557321a309e9d720cb1c398b722140725e47d8365e3ec68a; original Landmark source is29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b.

V2 raw arrays are byte-identical across repeats within each eta/policy cell. Their r0 identities are: baseline .01 66c6d97fed7983abc55c8ccf5b571f2613281a627a9993584e243632a76355e6; FD50 .01 9d82678f6820878c285bcc8cef4480b1f9838d19a42190af7ff5150b99b16e2b; baseline .1 b7ab2139b4f38289085d5ee2a10737330d68938ffe28ad939ad183d7c276d083; FD50 .1 218eca2e89d244175a986a1dc88e01470fb6c2f7c1c1a0b13f1a77016400e913.

## V1 falsification retained

All12 V1 records fail loss_close only, despite exact query/update-mask matches, queried-OPT tolerance agreement and the other recorded checks. Independent inspection of saved V1 residuals gives maximum absolute reference deviation .0010067311772416192 and maximum energy-normalized deviation7.368920376408263e-5, far above1e-10. This is a material semantic mismatch under the frozen criterion, not an inconsequential threshold edit. The Gram-eigenvector/QR endpoint map differs from B08; the saved audit alone does not identify a unique causal numerical mechanism. V1's apparently faster costs cannot qualify the equivalence claim. Its failed audit exits1 and remains in both costs and evidence.

## V2 semantic acceptance

The final V2 audit source was independently read against its saved output. It checks the frozen24-file manifest, reference identity, masks, queried OPT, incoming residuals, summary counts/raw hashes, Gram diagonal, gate validity, held-state feasibility, and preservation of V1 failure. The audit does not silently redefine V1 as passing. My separate saved-array inspection reproduced these relevant comparisons without running the algorithm.

All12 V2 records pass. Query and update masks exactly match the corresponding B07 reference. Baseline and FD50 have identical update masks in every pair. Incoming-residual arrays exactly equal their B07 reference and one another, maximum loss difference0.0. The largest queried-OPT absolute difference is8.926193117986259e-14; maximum normalized difference8.761240730145033e-16, within the unchanged1e-10 tolerance. Saved gates meet OPT+tolerance; nonrefresh held-state residuals meet(1+eta)OPT+tolerance. Recomputed mask counts agree with summaries, and each update implies a query.

| eta | Baseline queries after growth | FD50 queries after growth | Shared refreshes after growth | Queries including growth, baseline/FD50 | Shared total refreshes |
|---|---:|---:|---:|---|---:|
| .01 | 408 | 222 | 222 | 433/247 | 247 |
| .1 | 205 | 100 | 100 | 230/125 | 125 |

V2 uses Gram eigenvalues only for queried OPT and the original NumPy full SVD basis only on updates. Identical update masks and the common deterministic SVD map support endpoint parity, consistent with exact saved incoming-loss parity. Full Q/projector matrices and postrefresh residuals are not stored or independently regenerated; do not claim those absent matrices were directly compared. There is no refresh/recourse benefit.

## Independently recalculated V2 operational CPU

Difference is baseline minus FD50; ratio is baseline divided by FD50. All values below were recalculated from individual saved summaries.

| eta | repeat | Baseline CPU s | FD50 CPU s | Difference s | Ratio |
|---|---:|---:|---:|---:|---:|
| .01 | 0 | 15.556028968 | 15.082561809 | .473467159 | 1.031391694 |
| .01 | 1 | 14.346178362 | 15.189835485 | -.843657123 | .944459101 |
| .01 | 2 | 14.093060346 | 15.168072835 | -1.075012489 | .929126627 |
| .1 | 0 | 6.298888438 | 7.640749974 | -1.341861536 | .824380913 |
| .1 | 1 | 6.623487437 | 7.666157400 | -1.042669963 | .863990535 |
| .1 | 2 | 6.020289875 | 7.559698854 | -1.539408979 | .796366362 |

Median paired CPU difference is-.843657123s at .01 and-1.341861536s at .1; median ratios are .9444591007036836 and .8243809127944122. Median wall differences are-.8451147690066136s and-1.3424855769990245s, with wall ratios .944375974094867 and .8243308828871498. Only .01 repeat0 has a positive CPU/wall difference. The prospective speed criterion fails separately at both eta values; do not pool these repetitions into independent-sample significance or discard the slower pairs.

Component records offer a plausible cost explanation: removed Gram eigenvalue-query work saves about1.16–1.31CPU seconds at .01 and .59–.64s at .1, while FD maintenance costs about1.66–1.78s per run. These differences do not by themselves equal measured whole-loop savings; shared refresh and residual costs also vary between processes. V2 actually charges every true-refresh SVD and every Gram append. The complete-loop timer excludes imports/input loading, initial allocations, saves and external audit, as before. It is a measured operational-loop reversal, not a modeled component result or a total application-runtime claim.

Sequential B08-to-V2 median comparisons: baseline CPU changes25.542848055→14.346178362(.01) and12.021430245→6.298888438(.1), B08/V2 ratios1.7804635778583109 and1.908500263709544. FD50 medians change13.743639390→15.168072835 and7.147658029→7.640749974. These cross-run implementation comparisons are descriptive; only the prospective within-V2 interleaved pairs directly test FD addition to this stronger baseline. This implementation is still not a proof of the fastest possible exact baseline.

## Native1024 calibration scope and resources

The saved five-checkpoint arrays at512/640/768/896/1024 have recomputed normalized OPT errors equal to recorded values, maximum8.8967799487957e-16. Gram OPT at those checkpoints is approximately .9821450254,2.5402606730,4.6902910645,9.6022576398,15.8484458938. Gram build CPU is .202055109s; selective eigenvalues-only query CPU ranges .016101716–.065536511s, whereas singular-values-only reference SVD ranges .092688160–.374106693s. This supports sampled objective accuracy and component resource measurement only. It does not test Gram eigenvectors/QR, V2 true-refresh endpoints at1024, continuous policy costs, or native5000 speed.

Calibration usage reports CPU1.513194009s,wall1.431918426s,RSS120540KiB; its command receipt wall is1.778655026s. Values refer to different boundaries and should not be conflated. Numeric-library thread limits are set in source; no independent measured thread census was obtained. The fact that this calibration CPU exceeds its inner wall should be retained rather than described as a direct proof that every source-reader helper used one CPU.

All29 receipts are terminal:28 succeeded/exit0 and one retained V1 frozen-audit failure/exit1. The set includes2 static checks,24 operational runs,1 native1024 calibration and2 audits. Receipt time intervals do not overlap. Total charged command wall195.2255382819858s; longest15.859715988000971s, below120s. V2 operational peak RSS ranges140540–153988KiB; V2 audit reports70464KiB,CPU .182648963s,wall .182669942s. Current status: attempts_used29/32, elapsed195.2255382819858/600, reservation0, awaiting_decision, remaining deadline811.9163012504578s. All prior V1 and failure costs remain charged. Executor identity remains the retained simple runner; no full SQLite/ACP supervisor deployment is inferred.

## Machine step7

Treat FD50 as an attributed quality/certificate comparator, with an implementation-dependent CPU effect and no recourse effect. Return to original-source/modern-baseline collision review and mathematical discovery of certified approximate-refresh improvements, using the stronger exact-query control in future fair comparisons. Do not promote the B08 engineering gain into a broad method-speed claim or replay these matrices merely to seek positive signs.

The1024 sampled objective calibration can inform a bounded native5000 resource plan, but does not justify a full4999-prefix run, time extrapolation, or a speed claim. Any further native scale work must freeze its precise diagnostic/policy scope, cap every command and total budget, measure effective rank and nearzero regimes, and validate continuation states if used. Existing comparator repair is not a new candidate requiring an artificial20-to15 cycle. This evidence remains one developed data sequence with process repeats, not independent scientific confirmation, novelty proof, or paper readiness; literature and broader comparator coverage remain incomplete.
