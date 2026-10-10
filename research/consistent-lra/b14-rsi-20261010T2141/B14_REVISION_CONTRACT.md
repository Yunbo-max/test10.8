# B14 V2 independent-review repair contract

The V1 artifacts and negative decision are immutable. V2 repairs only the
reviewed arithmetic/estimand defects on the same saved development states; it is
not fresh confirmation.

Required changes are fixed from the independent report:

1. AUROC keeps ordered `+infinity` and `-infinity`; only `NaN` denotes an
   undefined score. V1's all-state work-proxy AUROC is recomputed transparently.
2. The simultaneous-iteration work proxy is undefined if `lambda_k<=0` or the
   exact boundary gap is zero. Those states cannot use the valid one-step
   `rho=0, lambda_k>0` branch.
3. All-state angle and hard-mass values at a boundary tie are labelled
   solver-basis-dependent. A strict-unique analysis excluding exact zero-gap
   states is reported only as a post-hoc sensitivity.
4. The near band is exactly the frozen set
   `lambda_i-lambda_{k+1} <= 10*(lambda_k-lambda_{k+1})`, without epsilon
   widening.
5. `hard_fraction` is exploratory and removed from prospective acceptance.

Closure requires exact B09 mask/loss replay, zero lower-bound violations,
independent arithmetic readback, and preservation of the negative result. No
new-method, native5000, generalization, novelty, or paper claim is eligible.
