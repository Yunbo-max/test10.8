# B04 child repair v3 — bracket-width refinement

The failed v2 audit is retained. Its only failed predicate was the fixed (10^{-8}) old/new checkpoint projector tolerance: maximum (2.59145\times10^{-8}) at prefix 114, eta 0.01. The loss discrepancy there was (1.07\times10^{-14}), the update/query masks were identical, and the rank-25/26 singular-value gap was (1.07\times10^{-2}), so this is not explained by a tied target subspace.

The v2 Newton code could stop when `target - loss <= 32 eps * energy` even if its alpha bracket was still comparatively wide. Along the fixed principal-angle path,

\[
\lVert P(\alpha)-P(\alpha_*)\rVert_F
\le \sqrt{2}\,\lVert\theta\rVert_2\,|\alpha-\alpha_*|.
\]

The child repair keeps the same path, target, feasibility check and conservative near-zero legacy branch. After Newton it bisects the existing feasible/infeasible bracket until width at most (2^{-40}). This is a numerical precision repair, not a new scientific method. It is falsified if the rerun still exceeds any frozen v2 predicate. The v2 raw artifact and failed audit receipt remain immutable parents.
