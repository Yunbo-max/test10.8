# B05 frozen design: same-input solver replay

## Question

The B04 old/new recursive runs differed by about `2.5e-8` in projector norm
despite zero certificate violations and despite every observed new-solver
near-zero call falling back to the legacy bisection. Is the failed predicate
caused by a one-step root discrepancy, or by amplification of a tiny difference
in the independently recomputed incoming state/oracle?

## Fixed source and native scope

- Parent: B04 raw evidence SHA-256
  `de536dc37757675a48df592eb48114e4c888a49c02687cd6707d616782685b21`.
- Matrix: author Landmark SHA-256
  `29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b`.
- Raw first 128 rows, `d=2704`, `k=25`, `eta in {0.01,0.1}`, no
  standardization. The stored B04 subset is reused byte-for-byte.
- Frozen projector predicate remains `1e-8`; it is not relaxed.

## Prospective tests

1. Precompute one exact thin-SVD oracle per prefix and give byte-identical
   `(V,opt)` copies to old and new arms. At every boundary call evaluate both
   solvers on the same incoming `Q,V,G,E,target,tol`, while each recursive arm
   returns only its designated solver output.
2. Record all-prefix old/new projector distance, update/query masks, one-step
   same-input distances on both arm states, target/tolerance ratios, and the
   decomposition
   `old(Q_old)-new(Q_new) = [old(Q_old)-old(Q_new)] +
   [old(Q_new)-new(Q_new)]` in projector norm.
3. Run two nominally identical legacy arms with fresh independent SVD calls.
   This control asks whether independent oracle/state recomputation alone can
   reproduce the B04-scale divergence.
4. On every captured same-input boundary state, time legacy and current Newton
   calls in five deterministic randomized repetitions. Report near-zero and
   non-near-zero states separately. Complete-method speed is not inferred from
   this solver-only diagnostic.

## Predictions and decisions

- **Recurrence/oracle mechanism supported:** shared-oracle old/new decisions
  agree and maximum projector distance is at most `1e-8`; every same-input
  one-step distance is at most `1e-10`; and either the duplicate-legacy control
  reproduces a nonzero independent-oracle divergence or the stored B04
  divergence disappears under shared inputs. This diagnoses B04's strict
  solver-parity test as confounded; it does not retroactively pass B04 or weaken
  its threshold.
- **Root discrepancy supported:** a same-input old/new boundary output exceeds
  `1e-8`, or shared-oracle recursive parity still fails. Retire the accelerated
  solver from the native high-dimensional strict-parity lineage.
- **Fallback cost:** if all captured calls already satisfy `target<=tol`, the
  current method already uses legacy on every observed native boundary call;
  broader fallback is a no-op on this pilot and no native acceleration claim is
  available. Otherwise report paired solver-only medians and the non-near-zero
  cost ratio without extrapolating to 512/5000 rows.

The 512-row calibration remains deferred until this diagnostic is audited and a
versioned parity contract is accepted. This is development evidence, not
independent confirmation or a paper-level result.
