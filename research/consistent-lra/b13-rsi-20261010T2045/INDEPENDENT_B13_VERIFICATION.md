# Independent B13 mathematical verification

## Verdict: REVISE

The fixed-tuple counterexample (Theorem 2), its divergence claim, and the
float64 diagnostic are internally consistent.  Theorem 1 needs one explicit
edge-case repair before the mathematical artifact can pass: its assumptions
allow `lambda_2=0`, but formula (2) is then undefined and the informal
extended-real interpretation gives a false zero-iteration threshold.

This verdict keeps the code gate at **NO-GO**.  B13 is a theory diagnostic,
not an implementation candidate, and this review does not authorize native
5000-row work or a new method.

## Files reviewed without modification

- `B13_POWER_MODEL_THEOREM.md`
- `B13_LITERATURE_RECORD.md`
- `b13_power_work_diagnostic.py`
- `B13_POWER_WORK_DIAGNOSTIC.json`
- `B13_ROUND_CONTRACT.json`

## Algebraic review

### 1. Exact power error identity: correct

Writing `q=sum_i c_i u_i` gives

`G^m q=sum_i lambda_i^m c_i u_i`.

After normalization, the squared top overlap is the top weight divided by
the sum of all weights, so subtracting it from one gives exactly the stated
formula.  The `m=0` identity uses the conventional value `lambda_i^0=1`,
including a zero eigenvalue.  The assumption `c_1 != 0`, together with
`lambda_1>lambda_2>=0`, guarantees a nonzero normalization denominator.

### 2. Gap envelope: correct under the stated PSD ordering

For `i>=2`, `0<=lambda_i/lambda_1<=rho`, hence the off-top weight is at most
`rho^(2m) r`.  For fixed top weight `1-r`, the map `s -> s/(1-r+s)` is
increasing.  This yields (1).  Equality holds when each nonzero off-top
coefficient is supported on eigenvalue `lambda_2`; zero coefficients outside
that eigenspace are harmless.

### 3. Iteration threshold: one required edge-case repair

For `0<lambda_2<lambda_1` and `0<epsilon<r<1`, solving (1) gives

`rho^(2m) <= epsilon(1-r)/(r(1-epsilon))`,

so the stated logarithmic ratio and sign are correct.  Since `epsilon<r`,
the numerator logarithm is strictly positive, and taking the ceiling gives
the exact minimal integer in the equality case.

However, the theorem currently permits `lambda_2=0`.  Then
`log(lambda_1/lambda_2)` in (2) is undefined.  Treating it informally as
infinity gives threshold zero, but `E_0=r>epsilon`; one matvec is necessary
and sufficient because all off-top eigenvalues are zero.  Repair by either:

1. adding `lambda_2>0` to the statement of (2), plus a separate
   `lambda_2=0 => m_min=1` branch for `epsilon<r`; or
2. stating the exact piecewise minimal-work rule.

The finite diagnostic samples eigenvalues from `[0.01,1]`, so it does not
exercise this admitted edge case and cannot close it.

### 4. Fixed-tuple construction: correct

For `0<gamma<delta/r_0`, the numerator of
`a_gamma=(delta-gamma r_0)/(1-gamma)` is positive.  Moreover,

`a_gamma<r_0 <=> delta<r_0`,

so `0<a_gamma<r_0` and `q_gamma` is unit length.  Direct calculation gives

`tr(PG)-tr(QG)=a_gamma+gamma(r_0-a_gamma)=delta`.

Because `T=L(P)`, this is exactly the positive deficit.  The spectrum is
`{1,1-gamma,0}`, hence `D=1`; rank is one; and
`1-(e_1^T q_gamma)^2=r_0`.  Thus `(Delta,D,k,r)` is fixed exactly as claimed.

### 5. Exact counterexample work and divergence: correct

For `m>=1`, the zero-eigenvalue coordinate vanishes and the third coordinate
is multiplied by `(1-gamma)^m`, which yields (3).  Solving `E_m<=epsilon`
produces (4) with denominator `-2 log(1-gamma)>0`.

Also

`r_0-a_gamma=(r_0-delta)/(1-gamma)`.

The stipulated
`epsilon<(r_0-delta)/(1-delta)` makes the limiting logarithmic numerator
strictly positive.  It also implies `epsilon<r_0`, so zero work is excluded
and the displayed ceiling is at least one.  As `gamma -> 0+`, the numerator
converges to that positive constant and the denominator tends to zero from
above, proving divergence.

## Diagnostic-semantics review

The script tests the exact identity, the envelope, the equality construction,
the fixed tuple, and both sides of the claimed minimal integer work.  The JSON
is consistent with those semantics: 6000 random positive-spectrum cases have
errors at floating-point scale, the tuple errors are at floating-point scale,
and work grows from 15 to 7361 as `gamma` decreases from `0.1` to `0.0002`.
The reported `gamma * work` stabilizing near `1.472` is also consistent with
the predicted `Theta(1/gamma)` divergence.

Limitations of the diagnostic are accurately labelled.  In particular, it is
finite float64 arithmetic, it does not prove the theorem, and it deliberately
does not test `lambda_2=0`.  `required_work` uses `max(1,...)`, which handles
the selected counterexample regime but does not repair the missing theorem
branch.

## Claim scope and collision assessment

The bounded source record supports the stated conservative scope:

- Wang--Zhang--Zhang treat gap-dependent principal-angle bounds and a
  gap-independent warm-start block-Lanczos result.
- Musco--Musco give gap-independent low-rank/block-Krylov guarantees and
  distinguish low-rank approximation quality from principal-component
  quality.
- Garber et al. make solver-specific relative-gap, sparsity, stable-rank and
  accuracy dependencies explicit for shift-and-invert methods.
- Jain et al. concern stochastic single-pass Oja estimation; Nie et al.
  concern online compression regret; Balsubramani et al. concern statistical
  incremental-PCA convergence.  None of those scopes can be silently
  transferred into per-step consistent-LRA feasibility, recourse, or the
  frozen exact-matvec work model.

Therefore Theorem 1 must remain an attributed/re-derived classical control,
and Theorem 2 may only be called a project-specific insufficiency
counterexample pending a substantially broader closest-work audit.  The
record is explicitly bounded and does not establish exhaustive novelty.

## Required revision and recheck criterion

Patch only the `lambda_2=0` branch (and, preferably, clarify that the
solver-relevant quantity is the relative ratio/gap).  A revision can pass
when the theorem states a correct piecewise threshold and a small check covers
the zero-off-spectrum case.  No change to Theorem 2 is required by this
review.

## Explicit nonclaims

This review does **not** establish novelty, a universal lower bound for other
eigensolvers, a CPU-time lower bound, native consistent-LRA correctness,
independent experimental confirmation, NeurIPS readiness, or paper PASS.  It
does not authorize coding a candidate method.  It only verifies the displayed
frozen-model mathematics subject to the required edge-case revision above.
