# B13 bounded primary-source record

Search date: 2026-10-10.  Scope: sources needed to decide whether a
geometry-to-work theorem can omit solver and spectral assumptions.  This is a
bounded search, not a saturation or novelty audit.

## Newly inspected primary sources

1. Wang, Zhang and Zhang, *Improved Analyses of the Randomized Power Method and
   Block Lanczos Method*, arXiv:1508.06429v2.  Inspected abstract, Sections 1,
   3, 5.2 and 6 locators exposed by the HTML version.  It explicitly treats
   warm starts, gap-independent matrix-norm bounds, and gap-dependent principal
   angle bounds.  Consequence: a generic claim that warm-start spectral work
   depends on angle and/or eigengap is prior art, not a B13 novelty claim.

2. Musco and Musco, *Randomized Block Krylov Methods for Stronger and Faster
   Approximate Singular Value Decomposition*, arXiv:1504.05477.  Inspected
   abstract and method/guarantee summary.  It gives gap-independent approximate
   low-rank guarantees and separates approximation quality from principal
   component quality.  Consequence: any claimed universal need for an eigengap
   must be restricted to the frozen ordinary power-iteration model and explicit
   projector tolerance.

3. Garber et al., *Faster Eigenvector Computation via Shift-and-Invert
   Preconditioning*, arXiv:1605.08754.  Inspected abstract/runtime statement.
   It makes relative eigengap, stable rank, input sparsity and target accuracy
   explicit and obtains different dependence from classical power/Lanczos.
   Consequence: CPU cost cannot be transferred across solver families from the
   B12 tuple.

4. Jain et al., *Streaming PCA: Matching Matrix Bernstein and Near-Optimal
   Finite Sample Guarantees for Oja's Algorithm*, COLT 2016.  Inspected the PMLR
   abstract and algorithm statement.  It analyzes an O(d)-space single-pass Oja
   update and exposes relative eigengap/sample assumptions.  This is a different
   stochastic streaming objective from repeated exact endpoints.

5. Nie, Kotlowski and Warmuth, *Online PCA with Optimal Regret*, JMLR 2016.
   Inspected the full PDF introduction/objective and outline.  It uses linear
   compression loss and regret to the best fixed subspace, not endpoint
   construction matvec work or per-step recourse.

6. Balsubramani, Dasgupta and Freund, *The Fast Convergence of Incremental PCA*,
   NeurIPS 2013.  Inspected the official paper landing page and abstract-level
   scope.  It concerns statistical convergence of incremental PCA, not the
   consistent-LRA endpoint-construction cost model.

## Collision disposition

- Exact warm-start power convergence is established numerical-linear-algebra
  territory.  B13 Theorem 1 is a re-derived control, not a novel contribution.
- Theorem 2 is currently a project-specific insufficiency counterexample for a
  frozen cost model.  No claim of novelty is made; full closest-work and citation
  expansion remain incomplete.
- Online/streaming PCA regret or estimation guarantees do not, by themselves,
  certify consistent-LRA recourse, feasibility, or endpoint CPU cost.

## Decision

Use the B13 result to reject any future candidate whose cost model contains only
`(Delta,D,k,r)`.  Continue mathematical search only if it introduces and can
measure a solver-relevant spectral/state quantity while preserving the native
consistent-LRA feasibility certificate.  Do not encode B13 as a new method.
