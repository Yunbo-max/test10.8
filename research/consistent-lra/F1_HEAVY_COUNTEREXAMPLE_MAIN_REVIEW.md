# Independent review: Appendix F.1 HEAVY counterexample

## Scope and fixed bytes

- Project branch at assignment: `main`.
- Parent integration commit: `e9faa76b2d34b51d0a2b31247c28d3938db3920e`.
- Final reviewed artifact: `F1_HEAVY_COUNTEREXAMPLE_MAIN_DRAFT.md`.
- Final SHA256: `2d6a1fbc256d5fe943eadd93c4266f0c113d3f1e90894ef1729e44997266e056`.
- Canonical assignments: 169 (initial), 170 (corrected core), 171 (exact final bytes).
- Worker-local labels 163--165 collided with concurrent project labels and were remapped at integration; the reviewed bytes and verdicts are unchanged.
- This was a symbolic/source review. It used no executable-attempt or scientific-experiment budget.

## Preserved initial rejection

Canonical assignment169 (worker-local 163) reviewed the initial draft at SHA256
`46a934606dbb1965afc567e7b1cf90fae0afb377a0b8e3768252452346533f46` and returned
**NEEDS_CORRECTION**. The proposed old tail energy `C=144` was not shown reachable as
an actual persistent Algorithm 2 reset value: multiplying a reset threshold by `9/8`
can skip 144. Consequently the HEAVY premise was not yet tied to a valid epoch start.
That failure is retained; it was not relabelled as accepted.

## Corrected construction checked

The author changed the old tail energy to `C=137` and exhibited the complete reset
sequence

`1,2,3,4,5,6,7,8,9,11,13,15,17,20,23,26,30,34,39,44,50,57,65,74,84,95,107,121,137`.

For `epsilon=1/2`, `k=144`, `d=281`, the frozen prefix covariance is
`diag(3^131,2^13,1^137)`, so `OPT_s=137` and the old top-144 projector is unique.
The reviewer checked that the literal 13-term HEAVY sum is 26 and the intended
12-term sum is 24; both exceed `137/6`.

After four copies of each `e_145,...,e_156` and three copies of `e_157`, the first
approximation failure is the third copy of `e_157`: before it the old-projector loss
is at most `187 <= 1.25*150`, while after it the loss is `188 > 187.5` and
`OPT_t=150`. No epoch reset intervenes because `150 < (9/8)137 = 154.125`.
The final spectrum has unique boundary `3>2`. Exactly 13 coordinates exchange
between the projectors, giving squared Frobenius recourse `R=26>sqrt(144)=12`.

The exact trace decomposition was also checked:
`A=26`, `B=13`, `U=0`, `Delta_r(Q)=A-B=13`, and `G_D=51`. The proof step that
drops the old-tail capture `B` would force `OPT_t>163` under the literal block
(or `>161` under the intended 12-term block), contradicting the actual value 150.

Canonical assignment170 (worker-local 164) returned **ACCEPT** for the corrected core bytes at SHA256
`1c997e8717c80bb67f5569a58982b5b8c20d68d1a19fff12024841c6d7f672bb`.
Canonical assignment171 (worker-local 165) then reviewed the exact final bytes, including the printed-algorithm
and index-range ambiguity statements, and returned **ACCEPT** at the final SHA above.

## Accepted conclusion and exclusions

Accepted: the displayed Appendix F.1 HEAVY min-max/displacement implication, under
the intended persistent-state reading of Algorithm 2, has an explicit reachable
nonnegative-integer counterexample. The missing negative old-tail capture term is
material, not merely a loose constant.

Not accepted: that Theorem 1.3 is false; that no repair is possible; that the
construction is novel; that any native benchmark, method-admission, Gate A, or
paper-eligibility condition has passed. The paper's printed initialization placement
and inclusive block index are genuine source ambiguities and remain scope limits.
