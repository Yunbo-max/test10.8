# Assignment 161: HEAVY plus approximation failure does not control old-tail capture

Binding: integrated `main` `e9faa76b2d34b51d0a2b31247c28d3938db3920e`,
underlying legacy `7286e6d5b301f01ebda45d6fa1387afd9d383906`.
This is an unreviewed mathematical card, not novelty, method admission,
experiment evidence, theorem-wide refutation or paper eligibility.

## Formal objects and the missing inequality

For prefix `u`, let `C_u=A(u)^T A(u)`, let
`lambda_1(u)>=...>=lambda_d(u)`, let `P_u` be an exact rank-`k` top
projector, and write

`L_C(P)=tr((I-P)C)`, `OPT_u=L_{C_u}(P_u)`, and
`R(P,Q)=||P-Q||_F^2`.

Put `D=C_t-C_r>=0`, `P=P_r`, and `Q=P_t`. Then exactly

`OPT_t-OPT_r = U + Delta_r(Q)`,

where

`U=tr((I-Q)D)>=0`

and

`Delta_r(Q)=L_{C_r}(Q)-OPT_r`

`= sum_{i<=k} lambda_i alpha_i - sum_{i>k} lambda_i beta_i`,

with `alpha_i=||(I-Q)e_i||^2` and `beta_i=||Qe_i||^2` in an eigenbasis
of `C_r`. For equal ranks,

`sum_i alpha_i = sum_i beta_i = R(P,Q)/2`.

Displacement therefore controls unweighted head miss and old-tail capture
equally, not their difference. The universally valid eigengap bound is

`Delta_r(Q) >= (lambda_k-lambda_{k+1}) R(P,Q)/2`.

If `H_r=sum_{i=k-sqrt(k)}^k lambda_i(r)` denotes the paper's HEAVY block,
the displayed Appendix F.1 inference needs

`U + A - B > H_r`, equivalently `B < U + A - H_r`,

where `A=sum_{i<=k}lambda_i alpha_i` and
`B=sum_{i>k}lambda_i beta_i`. HEAVY lower-bounds `H_s`; displacement does
not supply the required tail-capture control.

The approximation-failure trigger does not repair this direction. Let
`G_D=tr((Q-P)D)` be the appended-energy capture advantage. Then

`L_t(P)-OPT_t = G_D-Delta_r(Q)`.

The Algorithm-2 trigger
`L_t(P)>=(1+epsilon/2)OPT_t` permits `G_D` to be large because new energy
is captured by `Q` and missed by `P`; it does not upper-bound `B`.

## Exact integer row-stream counterexample

Take `epsilon=1/2`, `k=144`, `h=sqrt(k)=12`, `d=281`, and `s=r`.
Build `A(s)` from `0/1` standard-basis rows:

- three copies of `e_i` for `i=1,...,131`;
- two copies of `e_i` for `i=132,...,144`;
- one copy of `e_i` for `i=145,...,281`.

Thus

`C_s=diag(3 x 131, 2 x 13, 1 x 137)`,

`P_r=span(e_1,...,e_144)`, and `OPT_s=137`.

This state is reachable from the empty stream under the intended persistent
Algorithm-2 state. Order the rows by first forming the `k` top directions and
then adding the 137 distinct unit tail rows. The optimum increases through the
integers 1 to 137. With `epsilon=1/2`, line 4 resets at
`C'=ceil((9/8)C)`, producing

`1,2,3,4,5,6,7,8,9,11,13,15,17,20,23,26,30,34,39,44,50,57,65,74,84,95,107,121,137`.

Thus a reset occurs exactly at `s` with `C=OPT_s=137` and `c=0`. The
printed HEAVY block `i=k-h,...,k` has thirteen terms, indices 132--144, so

`H_s=13*2=26 >= (epsilon/3)OPT_s=137/6`.

If only twelve terms were intended, their sum is 24; the example is
robust to the endpoint ambiguity.

Continue the stream with four copies of each of
`e_145,...,e_156` (48 rows), then three copies of `e_157` (3 rows). At the
final time `t`, the thirteen selected old-tail eigenvalues are 5 for the first
twelve coordinates and 4 for the last. The unique top-`k` projector `Q=P_t`
spans these thirteen coordinates plus `e_1,...,e_131`; the boundary is
`3>2`. Hence

`R(P_t,P_r)=2*(144-131)=26 > sqrt(k)=12`.

Exact losses are

`OPT_t=124*1+13*2=150`, so `OPT_t-OPT_s=13`.

Appendix F.1's displayed min--max step would require
`OPT_t>OPT_s+H_r`, namely `OPT_t>163` with the literal thirteen-term
block (or `>161` with twelve terms). The actual value 150 violates both.
In the exact decomposition, `A=26`, `B=13`, and `U=0`; the omitted negative
tail term is precisely the thirteen-unit discrepancy.

## Trigger and epoch checks

No earlier approximation-failure trigger or epoch reset occurs. After
`q<=12` coordinates receive four repeated rows,

`L_t(P_r)=137+4q`, `OPT_t=137+q`,

and

`L_t(P_r)-(1+epsilon/2)OPT_t = 2.75q-34.25 <= -1.25`.

Intermediate copies within those coordinates have a smaller margin. For the
final coordinate, after `j=1,2` copies, `(loss,OPT)` is respectively

`(186,150), (187,150)`,

both below `1.25*OPT=187.5`. After `j=3`, `(loss,OPT)=(188,150)` and

`188-1.25*150=0.5>0`.

Thus Algorithm 2's `(1+epsilon/2)` failure fires first at the stated `t`,
with `V(t-1)=P_r`. Throughout,

`OPT<=150 < (1+epsilon/4)*137 = 154.125`,

so the epoch-reset condition does not fire. Here `G_D=51` and
`Delta_r(Q)=13`; the old-output excess 38 exceeds
`(epsilon/2)OPT_t=37.5` through newly captured energy.

## Prediction, falsifier and scope

An independent replay should reject the displayed displacement-to-OPT-growth
inference unless another invariant supplies `B<=U+A-H_r`. A repair must add a
tail-capture/spectral-gap condition or replace `H_r` by a gap-weighted term.
HEAVY and the approximation-failure trigger alone are insufficient.

This card is falsified if the official definitions impose an additional
invariant forbidding the `s=r` standard-basis stream, force an earlier reset
beyond the checked thresholds, or use a different recourse/OPT quantity.
Otherwise it is a counterexample to the specific F.1 min--max implication and
its stated HEAVY subcase. It is not a proof that Theorem 1.3 is false: another
argument or invariant could still establish the theorem.

Three printed ambiguities remain separate from the counterexample: Algorithm 2
places its initialization line inside the row loop even though the epoch proof
requires persistent state; `k-sqrt(k),...,k` contains `sqrt(k)+1` terms; and
Appendix F.1 writes singular values of `V(s)`/`V(r)` where `A(s)`/`A(r)` is
evidently intended. The construction uses the intended persistent state and
works for either twelve or thirteen HEAVY terms.

Primary target: Woodruff and Zhou, ICLR 2026, Appendix F.1 pp. 21--22,
https://proceedings.iclr.cc/paper_files/paper/2026/file/b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf .
