# Actual150 independent approximate-proof dependency audit

Reviewer /root/window02_geometric_formal_review; fixed project snapshot
cf5f60bc155ff20440d3859806138e04ffba4ec4. Read-only existing-paper audit;
no experiment, implementation, novelty or publication admission.
Read conference printed pp4–9, relevant A/B, complete Appendix E/F pp19–25,
and consequential formulas against screenshots pp7/22/25. Additional primary:
Braverman et al., https://arxiv.org/pdf/1805.03765v6 (2023-04-11).
Target: https://proceedings.iclr.cc/paper_files/paper/2026/file/b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf .

## Dependency and scoped verdict

Theorem1.2's displayed proof needs repair: printed p6 explicitly uses Lemma2.1
after Theorem2.4. Theorem2.2 also uses that lemma for rank-uniform exact dynamic
maintenance. Existing reviewed counterexamples establish the lemma's failure;
the unsupported invariant-subspace inference remains decisive, not a dimension
formula typo alone. Approximate existence is unresolved rather than refuted.

Theorem1.3 has the separate stated chain Theorem2.4 -> Algorithm3/2 -> Lemma3.10
-> 3.5/3.9 -> 3.3/3.4/3.6/3.7/3.8 and F.1/F.2/F.3. Algorithm4 -> E.1/E.2
supports additive Theorem1.1, not Theorem1.3; its energy argument does not need
Lemma2.1. Preserve these different claims in baseline/report interpretation.

## Primary-qualified known fallback

Braverman Section1.4 defines online condition by nonzero singular values of
prefixes. Section3.1 Algorithm5 line9 appends a_t/sqrt(p_t) without modifying
earlier weights; complete Theorem3.1 proof gives simultaneous-prefix PCP and
sample count m=O(k delta^-2 log(n) log^2 max(2,kappa)).
For 0<epsilon<=1 choose delta=epsilon/(2+epsilon). On that PCP event, exact
top-k minimization on each sampled prefix yields

L_A(Q)<=((1+delta)/(1-delta))*OPT_A=(1+epsilon)*OPT_A.

For ranks at most k, ||P-Q||_F^2=rank(P)+rank(Q)-2tr(PQ)<=2k. Thus

R_total<=2km=O(k^2 epsilon^-2 log(n) log^2 max(2,kappa)).

For kappa<=n^C with fixed C, this is O(k^2 epsilon^-2 log^3(n)). This closes
the specific sampler prerequisite of the earlier conditional fallback. It is a
known fresh-SVD baseline, no new contribution. Zero/rank-deficient prefixes can
retain row span under an explicit common rank convention. Sample count/span
alone does not remove the extra factor: the refined bound2min(k,r-k) can still
be2k. PCP bounds losses rather than projector angles. A separate aggregate
analysis or approximate output construction might repair the linear bound;
none was established in this audit.

## Independently derived additive Algorithm4 support

Let E_t=||A_t||_F^2 and s be the most recent positive-energy refresh. Before the
next refresh, insertion monotonicity and E_t-E_s<=epsilon*E_s give

L_t(P_s)<=OPT_s+(E_t-E_s)<=OPT_t+epsilon*E_s<=OPT_t+epsilon*E_t.

Refresh outputs are exact. With first positive E_*, positive-energy refreshes
are at most1+floor(log(E_n/E_*)/log(1+epsilon)), each recourse<=2k. Integer
entries imply E_*>=1 and E_n<=ndM^2. Normalized real data require actual energy
ratio; the integer logarithmic bound cannot silently transfer. Freeze zero-output
convention. This qualifies an additive proof scope, not a multiplicative loss ratio.

## Unresolved Theorem1.3 prerequisites, without a falsity claim

1. F.1 HEAVY displacement-to-energy inequality: the identity R=2 sum sin^2(theta)
   makes a factor2 in angle counting potentially harmless. The consequential
   old-covariance loss identity is

   L_C(Q)-OPT_C=sum_(i<=k)lambda_i||(I-Q)e_i||^2
                -sum_(i>k)lambda_i||Qe_i||^2.

   A quantitative lower bound must control the negative tail-capture term.
   The inspected min-max argument does not supply that control. Its
   approximation-failure trigger may add structure; sufficiency was not proved
   here, and no counterexample to F.1 was constructed.
2. Reweighted rows a/sqrt(p) need not be integer or rational. Common scaling
   preserves geometry but does not supply integer determinant integrality and
   the asserted magnitude bound. Explicit rounding/denominator control could
   repair the premise; it is absent from the inspected reduction. F.2 cannot
   automatically apply to arbitrary reweighted rows.
3. Algorithm2's printed initialization is inside the row loop whereas its epoch
   prose requires persistence. Moving it is a plausible notation repair, not
   a theorem refutation. Case labels/rank wording/constants are kept distinct
   from missing quantitative inequalities.

The inspected general-integer sampling theorem retains kappa. Braverman's
bounded-integer Corollary2.15 concerns a different sliding-window structure;
its storage bound does not automatically yield the fixed-weight append-only
stream used by Algorithm2. The full polylog(ndM) reduction remains unqualified.
Initialization counted as rows, arbitrary initial matrices, pure insertions and
insertion/deletion cycles preserve their distinct earlier scopes. No fresh
confirmation or main approximate-theorem counterexample was generated.

## Actual source identities and capture boundary

v2 Gitblobd80cc0d9fe0996ad74ec2daa12d6484b7a5f02ad SHA256
0cbf0413e49df6f81e135219f0cb6ea994129167d2f900dfc5594bdb0d90d477;
v3 Gitblobff83dd2c3d266999ea49f3f6037b4e427c95e1dd SHA256
440edfddc4b9d51a218ea878de78acd1b89b7648bdabdf222c493b3b31331c3c;
actual139 Gitblob3ba8cbadc26b9c55a204702b38daf5647fa33cb3 SHA256
eefb3614c7505cd294f224888714db1b8492aea6c86d506e8af3f91e66b55fb8.
Taskblob1201e7f8205803795eee0a72eec0c3cf202777a2.
Retrieval-object UTF8 JSON.stringify hashes: target
51731d76110c1991f549480a5cb9f6bc230ce80f59538193f6f8b0cfafb3daae;
PCP38137cd3f16e8cafcfe1d45932df99f3b9fd828aa8ceadcabb75f91f975b0a8c.
These are capture hashes; original PDF bytes were not downloaded and no PDF-byte
hash is asserted. Full theorem-by-theorem paper verification remains incomplete.
