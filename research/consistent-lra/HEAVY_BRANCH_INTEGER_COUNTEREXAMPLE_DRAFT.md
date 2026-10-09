# HEAVY branch exact integer counterexample — consequential math card (draft)

Author /root; actual mathematical assignment162. Source-bound M/R audit of the existing Algorithm2/LemmaF.1, not new-method discovery. Current recovery main e9faa76b2d34b51d0a2b31247c28d3938db3920e. Paper official ICLR2026 PDF, printed Algorithm2 p7, F.1 pp22–23. Root reread exact statements/inequalities and screenshot pages before constructing this card. No project code, matrix generator, numerical scorer or executable arithmetic verification was run. Independent review163 is required; draft conclusions may be rejected.

## Object and assumptions

For orthogonal rank16 projectors, recourse is squared Frobenius projector distance. Set k=16, d=32, epsilon=3/10. Define the ordered 35-row integer stream:

- row i=(100+i)e_i for1<=i<=16;
- row16+i=100 e_(16+i) for1<=i<=16;
- row32+j=100 e_(16+j) for1<=j<=3.

All entries are integers of magnitude at most116, including zeros. No row is zero. Use the paper's intended persistent-epoch interpretation: HEAVY,C,c initialize once, not every row. This is the interpretation required by its epoch proofs and is explicitly separated from the literally printed line3 inside the loop. RECLUSTER computes the exact top16 subspace. Only the HEAVY branch is used once positive OPT begins. Rank-deficient initialization/tie choices before row16 do not affect the unique top16 projector at row16 onward. This card does not repair every unrelated initialization/notation issue.

Write P0=sum_(i=1)^16 e_i e_i^T. At row32 the covariance is diagonal, old top eigenvalues(101^2,...,116^2), tail eigenvalues10000 repeated16. The top16 projector is unique, because101^2>10000. At each earlier row16+q (1<=q<=16) the exact top16 remains P0 and OPT=10000q. P0 achieves OPT, so failure refresh never occurs; c remains0 after each outer reset.

## Reachable state, not an arbitrary initial matrix

The outer epoch test is OPT >= (1+epsilon/4)C=(43/40)C. Once positive OPT begins, forq=1,...,14 the test resets each time: q/(q-1)>43/40 for2<=q<=14, and q1 starts fromC0. Atq15,15/14<43/40, so no outer reset and P0 still exactly minimizes. Atq16,16/14>43/40, so row32 resets C=160000,c=0,RECLUSTER givesP0.

HEAVY is TRUE at every positive-OPT outer reset: even the four smallest top eigenvalues sum
101^2+102^2+103^2+104^2=42030 >= (epsilon/3)OPT,
and OPT<=160000 makes RHS<=16000. The printed inclusive indexing uses five values rather than four whenk is a square; their sum53055 is larger, so either reading passes. No square-root rounding is needed. The final refresh at35 does not reset HEAVY,C,c by the outer condition.

## Exact steps and prediction

Afterj extra rows,1<=j<=3, thej promoted tail coordinates have covariance eigenvalue20000>116^2=13456. Thus the unique exact top16 contains thosej coordinates plus the16-j largest original top coordinates. The cutoff is strict: the kept last original top coordinate has square(101+j)^2, exceeding the discarded last square(100+j)^2. Repeated20000 values are entirely included, so ties inside the top subspace do not affect its unique projector.

The exact OPT and loss of retainedP0 are

OPT_(32+j)=160000+sum_(i=1)^j[(100+i)^2-10000],
L_(32+j)(P0)=160000+10000j.

| Time | j | OPT | L(P0) | 20 L(P0) -23 OPT | Outer threshold |
|---|---:|---:|---:|---:|---:|
|33|1|160201|170000|-284623|172000|
|34|2|160605|180000|-93915|172000|
|35|3|161214|190000|92078|172000|

The inner failure test L >= (1+epsilon/2)OPT=(23/20)OPT is false at33/34 and strictly true at35. Every OPT is strictly below172000, and c remains0<16 before35, so no outer reset. Therefore Algorithm2 retainsP0 at33/34 and executes its HEAVY failure-triggered RECLUSTER at35. The new projectorP3 replaces exactlye1,e2,e3 with e17,e18,e19; the other13 top coordinates remain.

P3-P0 is diagonal with three entries+1 and three entries-1, giving

R(P3,P0)=||P3-P0||_F^2=6 > sqrt(k)=4.

This directly falsifies F.1's displayed numerical bound under the intended persistent Algorithm2 semantics, if all arithmetic/state claims above are independently accepted. Approximation at35 is restored by exact RECLUSTER. It does not refute approximation correctness or the subquadratic asymptotic existence theorem. A constant-factor relaxation of the lemma could handle this one example; this draft does not establish rank-asymptotic violation.

## Consequential proof diagnostic and known mechanism

At row32, evaluating the newP3 against old covariance replaces old captured energy101^2+102^2+103^2=31214 by old tail energy30000. The old-cost increase is1214, not the sum of displaced top energies. Tail capture cancels30000. At35 OPT rises only1214 over160000, below epsilon/4 epoch allowance12000. HEAVY's bottom-top mass condition alone does not control that cancellation.

Coordinate-spectrum crossings, diagonal covariance, exact top-k loss and projector recourse are established mechanisms already described in the target's own related-work examples. No novelty or new algorithm is claimed. This is a proposed different proof-defect witness from the earlier rank-one geometric Lemma2.1 construction, but distinct defects are not automatically distinct publishable papers.

## Falsifier and independent acceptance contract

Reject/correct if the official F.1 uses a different recourse metric, inaccessible algorithm state, nonpersistent interpretation, extra hypothesis excluding this stream, a different exact RECLUSTER contract, inaccurate branch arithmetic or any cutoff ambiguity. Reviewer must independently reconstruct all35row covariance evolution analytically (no source import/CPU experiment), read Algorithm2/F.1 and the paper recourse definition, verify reachability at32 and unchanged state at33/34, and derive6 rather than inherit this verdict. Check both inclusive HEAVY indexing conventions and initialization boundary. Return ACCEPT/NEEDS_CORRECTION/REJECT plus checked source identities and scope. No baseline/scorer/new-method/paper qualification follows.

Remaining obligations: wider constant/asymptotic repair analysis, primary priority audit and independent review. No executable task is proposed by this card.
