# Independent source audit of the published baseline

Status: source-only findings. No code execution, numerical test, reproduced metric or scientific comparison has been performed.

All locations refer to author commit `d607c4f6467216c470d1e3b93989d44d5fcdec97`. The separate read-only verifier was `/root/baseline_audit`.

| Finding | Source | Supported consequence |
|---|---|---|
| Landmark denominator reuses the last-refresh V. | consistent-lra-landmark.py, lines 76–96 | After warmup, factors and V[:kcurr] can be identical, making numerator and denominator the same cost. Ratios can therefore be 1 by construction rather than by comparison to a fresh optimum. |
| Landmark refresh rank uses stale state. | consistent-lra-landmark.py, lines 56–80 | r starts at zero; kcurr is computed before the current SVD; factors is sliced before updating r. First refresh yields an empty subspace, later ranks can lag, and r carries across parameter sweeps. |
| Recourse metrics differ. | landmark line 81; rice lines 94–97; consistent-fd.py lines 82–117/160 | Author refreshes cost k; FD counts weighted sketch rows outside a previous row span using a numerical tolerance. Neither evaluates the paper's squared projector distance. |
| FD historical state aliases mutable state. | consistent-fd.py lines 47–50/70–74/158–162 | get_sketch returns B directly and V_old=V_new. In-place zero-row insertions alter both references. Shrinking replaces B, so the issue is transition-dependent. |
| Intended final prefixes are omitted. | landmark lines 68–69; FD 156–157; rice 84–85; skin 83–84 | Landmark/FD process 4,999 rows. Rice/Skin include the empty prefix and stop at length 2,999. |
| Zero denominator maps unconditionally to ratio 1. | landmark lines 93–96; rice 109–112; skin 107–110 | Positive approximation cost with zero reference would be hidden. Whether this occurs in the native datasets is unmeasured. |
| Runtime traces include evaluation and prior sweeps. | landmark lines 62–100; rice 65–116 | One clock spans parameter sweeps; scoring/reference decomposition is timed with algorithm work. Reported traces cannot isolate update cost. |

Rice (lines 50–55) and Skin (52–57) standardize all loaded columns before selecting the first 3,000 prefixes. This depends on future raw data. It is legitimate only if the experiment explicitly defines an offline-transformed fixed stream; it does not establish a raw-data streaming protocol.

## Native metrics and a fair repair

The paper defines cumulative recourse using squared Frobenius distance between orthogonal projectors. For row-orthonormal bases Q_t and Q_{t-1}, including an explicit convention for their ranks,

```text
recourse_t = rank(Q_t) + rank(Q_prev) - 2 * ||Q_t @ Q_prev.T||_F^2
```

The fixed-rank form is 2k minus twice the squared overlap. A lower rank in warmup and near-degenerate eigenspaces requires a declared convention; the scorer cannot silently mix basis changes with subspace changes.

Before any new method comparison:

1. Preserve original source identities and independently version the repair contract.
2. Fix initialization, every intended prefix and per-sweep state/clock.
3. Compute the optimal/reference reconstruction residual independently of the candidate's retained factors. An approximate reference needs explicit accuracy bounds.
4. Snapshot an immutable orthonormal output basis for each algorithm. FD's weighted sketch rows are not themselves a rank-k output basis.
5. Apply identical native projector recourse, residual scoring, preprocessing, prefixes and fair numerical/compute allowances to every method.
6. Keep OPT=0 cases and positive-cost violations; use an explicit numerical tolerance and absolute error instead of ratio=1.
7. Separate update time, score time and complete pipeline time; retain raw per-prefix measurements.
8. Qualify the repaired evaluator against independent direct calculations on native data before scientific verdicts.

Section 4 reports a greater-than-400-fold recourse separation. These inspected scripts do not qualify that ratio under the paper's projector metric. They do not establish that no large separation exists. Figure provenance and a faithful rerun are pending; no conclusion about theorem validity follows.

## Source URLs

- https://github.com/samsonzhou/consistent-LRA/blob/d607c4f6467216c470d1e3b93989d44d5fcdec97/consistent-lra-landmark.py
- https://github.com/samsonzhou/consistent-LRA/blob/d607c4f6467216c470d1e3b93989d44d5fcdec97/consistent-fd.py
- https://github.com/samsonzhou/consistent-LRA/blob/d607c4f6467216c470d1e3b93989d44d5fcdec97/consistent-lra-rice.py
- https://github.com/samsonzhou/consistent-LRA/blob/d607c4f6467216c470d1e3b93989d44d5fcdec97/consistent-lra-skin.py
- https://proceedings.iclr.cc/paper_files/paper/2026/file/b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf

## Versioned repair and later source review

REPAIR_CONTRACT_v1.md freezes the intended numerical semantics. BASELINE_DRAFT_REVIEW.md records exact code versions and independent correction findings. The repaired evaluator formulas, project strong FD arm, and frozen-author `ell+1` diagnostic now have independently accepted finite software-semantic evidence, including 45 strong-FD and 58 author-diagnostic checks. The author diagnostic matches the frozen update state on its analytic fixtures while retaining the source's zero-row ambiguity; it emits a copied common-projector basis rather than the author's alias/row-span recourse. This is not native baseline performance, full sensitivity, published recourse parity, Liberty parity or a corrected scientific comparison. Historical source-integrity preparation uses the old draft and must not be relabeled proof of the repaired draft. Official scorer admission remains blocked as recorded in vendor/rsi/SCORER_BLOCKER.md.

RICE_ALG4_CALIBRATION_EXECUTION_20261009.md and its independent evidence review
add one bounded all-3,000-prefix cost/coverage observation for Rice, rank 1,
Algorithm 4 at c=2.5.  The complete raw stream, receipt and separated clocks are
retained.  This checks that path's coverage and real resource fit; because it is
only one arm under the project repair, it is not a qualified comparative result
and does not resolve the official scorer, sensitivity, author-FD or four-family
gaps.
