# Finite numerical certificate for the multi-refresh ledger

Status: **assignment 185; software sanity certificate only**.

This certificate is not a scientific experiment and is not evidence for the
paper's unweighted recourse claim.  It checks the algebra accepted by
independent assignment 184 against finite random matrices and retains both
execution attempts.

## Attempt 25 — terminal launch failure

- Intended command: run the finite NumPy property check under
  `/usr/bin/time` with BLAS/OpenMP thread counts fixed to one.
- Terminal result: `env: ‘/usr/bin/time’: No such file or directory`.
- Python launched: no.
- Scientific output: none.
- Measured CPU contribution: none available; the cumulative lower bound is not
  increased for this failed wrapper lookup.

## Attempt 26 — terminal pass

- Replacement timer: Bash `time`, without installing anything.
- Thread limits: `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1`,
  `MKL_NUM_THREADS=1`.
- Seed: `183184`.
- Trials: 12,000 random pairs \(C=X^TX\), \(D=Y^TY\), with
  \(k=1,\ldots,6\) and dimension \(2k+1\).
- Checked on every trial:
  \[
  (\operatorname{OPT}(C+D)-\operatorname{OPT}(C))-(G+U)=0
  \]
  and
  \[
  G-\tfrac12(\lambda_k(C)-\lambda_{k+1}(C))R\geq0.
  \]
- Also checked the near-tie construction at \(k\in\{1,3,9\}\) and
  \(\delta=10^{-7}\).
- Exact terminal summary:
  `PASS trials=12000 max_identity_error=3.553e-14 min_gap_slack=1.372e-09 near_tie_k=1,3,9`
- Measured wall: 0.786 s.
- Measured process CPU: user 0.762 s + system 0.024 s = **0.786 CPU s**.
- Peak RSS: not reported by the available shell timer.

The finite check can detect an implementation/algebra mismatch but cannot
replace the exact derivation.  Independent assignment 184 is the semantic
acceptance record.  Including attempt 25, the monotonic project ledger becomes
185 assignments, 26 executable attempts, two controller rounds, zero discovery
rounds, and **319.730499767 measured process/core-seconds lower bound**.  Formal
scientific experiments and completed scientific cycles remain zero.
