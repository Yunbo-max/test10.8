# Independent re-review task: minimum-recourse feasible refresh

Status: **assignment 188 dispatched; exact corrected bytes frozen below**.

Base commit before this evidence batch:
`7d1faceba2dfb9efa7c3b5801b2937c7f74a531d`.

Review these exact bytes:

- candidate: `research/consistent-lra/MINIMUM_RECOURSE_FEASIBLE_REFRESH_CANDIDATE.md`
- corrected candidate SHA-256:
  `10e15b9d352a44947fed213f98679f4cbcb1e864e481cb8d1623904f8cff15cd`
- preserved assignment-187 review:
  `research/consistent-lra/MINIMUM_RECOURSE_FEASIBLE_REFRESH_INDEPENDENT_REVIEW.md`
- assignment-187 review SHA-256:
  `7464f30d474c888d2483d56222c35b56ce75bce2f0e99df2f439fc5574c09f73`

The assignment-187 verdict was `CORRECT_AND_REREVIEW`.  Verify that the
correction actually repairs, rather than hides, both substantive defects:

1. the false real-projector convexity claim is replaced by a valid complex
   k-numerical-range scalarization and a complete recovery of a real cutoff
   subspace;
2. the discrete ceiling law is replaced by the exact continuous rotation law,
   and the actual `rho_hi` trigger condition is included.

Also check existence, monotonicity, present-refresh versus future-trajectory
scope, the degenerate-cutoff implementation obligation, and the collision and
admission boundaries.  Return exactly one of `ACCEPT_CANDIDATE_MATH`,
`CORRECT_AND_REREVIEW`, or `REJECT`, with derivations.  Acceptance means only
that this card may remain in the mathematical candidate pool.  It does not
establish originality, select the method, authorize code, or count as a formal
scientific experiment.
