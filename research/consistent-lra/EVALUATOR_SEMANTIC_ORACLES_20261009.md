# Repaired evaluator semantic-oracle qualification candidate

Scope: software semantics only. The analytic matrices below are unit-test
oracles, not replacement benchmarks, native performance evidence, an official
scorer, or a scientific experiment.

## Mapped definitions

The frozen repair contract defines, for row-orthonormal `Q`,

- `P = Q^T Q`;
- loss `||A(I-P)||_F^2`;
- recourse increment `||P-P_prev||_F^2`;
- overlap form `rank(Q)+rank(Q_prev)-2||Q Q_prev^T||_F^2`;
- fresh-SVD OPT as the sum of squared singular values below rank `k`.

`baseline_qualify.py` is the production metric source used by the current
baseline draft. `evaluator_semantic_oracles.py` computes explicit projectors
independently and compares those definitions to the production functions.

## Predeclared oracle cases

1. `A=diag(3,2,1)`, `Q=e1`, `k=1`: loss and SVD tail are exactly 5.
2. `span(e1)` versus `span(e2)`: projector recourse is exactly 2.
3. `span(e1,e2)` versus `span(e1)`: rank-varying recourse is exactly 1.
4. `span((e1+e2)/sqrt(2))` versus `span(e1)`: recourse is exactly 1.
5. Initialization from the zero projector is checked separately and equals
   rank 1; the primary streaming convention still excludes it.
6. Four fixed-seed algebraic cases compare direct residual with explicit
   projector and trace forms, and overlap recourse with explicit projector
   difference. The seed is only for deterministic software testing.

The analytic cases avoid spectral ties at the selected cutoff. Tolerances are
`1e-12*max(1,energy)` for loss identities and
`1e-12*max(1,r+r_prev)` for dimensionless recourse identities.

## Finite execution boundary

One engineering job, one attempt, no retry, one CPU reservation, 256 MiB and
30 seconds. It uses only the already installed Python, NumPy, SciPy and
scikit-learn stack, records all four versions, writes one JSON output, and is
run by the pinned RSI native runner inside a single-task harness. No GPU,
network, model service, package installation, paid resource or candidate method
is involved. CPU and memory values are admission reservations, not claims of
OS affinity or an RLIMIT.

Passing all checks establishes only that the current repaired formulas agree
with explicit finite-dimensional definitions on the frozen oracles. It does not
establish author-exact scorer parity (the archive has no separate scorer), total
streaming recourse on native data, FD correctness, baseline performance, G01,
E04, Gate A, or a paper claim.
