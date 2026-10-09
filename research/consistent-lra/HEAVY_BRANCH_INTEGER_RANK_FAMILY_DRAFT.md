# HEAVY branch rank-family card — draft, separate acceptance

Actual derivation assignment164; independent mathematical review165 required. Author/root is sole writer. Frozen parents: actual150 proof-dependency review and accepted163 finite witness at main6c002452afccd7deeb6e0c0993a384ce559046b6. This is existing-paper proof analysis, no new algorithm/discovery/empirical run. No project code, symbolic script or numeric evaluator was executed to derive this family. The earlier163 witness remains separate:epsilon0.3,R6>4 alone does not rule out a constant-factor repair or address epsilon<.01. This card targets those two limitations.

## Object, assumptions and exact construction

Take an arbitrary integerm>=11. Set

k=m^4, epsilon=1/m^2<1/100, N=m^8, b=N^2=m^16,
alpha=(N/m)^2=m^14, f=1+epsilon/4=1+1/(4m^2).

Dimension and row count will depend on q defined below, with d=k+q and n<=k+2q<=3k. Orthogonal projector recourse remains ||P-Q||_F^2. RECLUSTER is exact top-k. Preserve the intended persistent Algorithm2 epoch state. The literal inside-loop initialization is a distinct defect/semantics, not silently repaired here.

Define the increasing integer reset sequenceq_1=1 andq_(l+1)=ceil(f q_l). Letq be its largest term not exceedingk. This finite scalar construction fixesq independently of eigenvector tie choices. Asceil(fq)>k, fq>k, hence

q>k/f>4k/5, and q<=k.

There is no zero-state division in this definition. The stream starts withk nonzero integer rows( N+i)e_i,1<=i<=k. It then addsq rowsN e_(k+i),1<=i<=q. Finally add rows(N/m)e_(k+i),1<=i<=q, stopping at the first HEAVY failure triggerj_* defined and proved to exist below. All entries are nonnegative integers of magnitude<=N+k=k^2+k; final arriving rows have integer sizeN/m=m^7. A sparse analytic stream description is sufficient; it has not been instantiated or benchmarked.

## Reachable initial epoch

During the firstk rows,OPT=0 and the outer branch refreshes exact row span. At timek, unique top-k projector isP0=sum_(i=1)^k e_i e_i^T. During initial tail rows1<=r<=q, this unique exact projector remainsP0, since(N+1)^2>b and every new tail eigenvalue isb. Its loss equalsOPT=r b, so no HEAVY inner failure occurs andc=0.

The outer positive-OPT resets occur precisely atr=q_l: whenC=q_l b, the next integer r passingr b>=f C isceil(f q_l). Every such reset sets HEAVY TRUE. The lowest sqrt(k)=m^2 top squared singular values are each>b, so their sum>m^2 b. SinceC<=k b, the HEAVY threshold(epsilon/3)C<=m^2 b/3. Including the paper's extra boundary summand only increases that mass. Thus the state at timek+q is reachable andexact:

C=q b, c=0, HEAVY=TRUE, V spansP0.

It is not a freely supplied arbitrary initial matrix. q's reset-sequence definition removes the stale-C gap that would arise by simply assuming the last initial tail row reset the epoch.

## Exact spectra after j arrivals and quantitative bounds

Define delta_j=sum_(i=1)^j[(N+i)^2-b]
=N j(j+1)+j(j+1)(2j+1)/6,1<=j<=q.

Becausealpha>2Nk+k^2 (equivalentlym^14>2m^12+m^8), each promoted tail eigenvalueb+alpha exceeds all original top eigenvalues(N+i)^2. This inequality holds for everym>=11, since m^6>2m^4+1. The unique top-k projector afterj added rows is

P_j=sum_(i=j+1)^k e_i e_i^T+sum_(i=1)^j e_(k+i)e_(k+i)^T.

All promoted equal eigenvalues are included; the remaining old cutoff is strict whenj<k, and whenj=k all promoted coordinates are included with a strict gap below them. No ambiguity of projector at the cutoff.

Direct diagonal accounting gives

OPT_j=q b+delta_j, L_j(P0)=q b+j alpha.

Forj<=q<=k, delta_j<=delta_k. Usingk+1<=2k,2k+1<=3k gives

delta_k<=2N k^2+k^3=2m^16+m^12.

For m>=11,

2m^16+m^12<m^18/5,

because10/m^2+5/m^6<=10/121+5/11^6<1. Alsoq>4k/5 yields

q b/(4m^2)>m^18/5.

Therefore the useful strict bound is

delta_j<q b/(4m^2)=(epsilon/4)C.

At everyj<=q,OPT_j<(1+epsilon/4)C=f C. No outer cost reset can occur before the first failure; counterc stays0<k,HEAVY staysTRUE. Thus this bound explicitly checks the epoch assumption rather than presuming it.

## First-trigger existence, prediction and falsifier

LetD_j=L_j(P0)-(1+epsilon/2)OPT_j
=j alpha-delta_j-(q b+delta_j)/(2m^2).

Forj<=q/2, j alpha<=q b/(2m^2), whiledelta_j>=0; henceD_j<=0, and forpositivej it is strictlynegative. Atj=0 it is also strictlynegative. So none of these rows triggers the inner >= test.

Atj=q,

D_q=q b/(2m^2)-(1+1/(2m^2))delta_q>0,

since delta_q<q b/(4m^2) and1+1/(2m^2)<2. The finite set of indices satisfyingD_j>=0 is therefore nonempty. Definej_* as its smallest integer index. No monotonicity assertion forD is needed. It follows that

q/2<j_*<=q.

The previous output isP0 at everyj<j_*, so the HEAVY branch actually reclusters for the first time atj_*, within the original epoch and withc0. The output isP_(j_*), and the exact squared-Frobenius recourse is

R=2 j_*>q>4k/5.

Thus R/sqrt(k)>4m^2/5 is unbounded alongm>=11, even with epsilon<.01 and polynomial-magnitude nonnegative integer rows. If independently accepted, the displayed F.1 bound and any uniformconstant-times-sqrt(k) replacement cannot hold for this intended persistent Algorithm2 branch. It does NOT refute the claimed approximate-existence Theorem1.3 or its full total-recourse bound; losing an intermediate uniform per-refresh bound is a proof defect, not automatically a theorem counterexample. This family usesTheta(k) arrivals since the last stored exact optimizer; it is not a one-row rank-one change between consecutive exact optimizers.

## Mechanism, scope and constructive alternatives

Against the old covariance, replacingj top coordinates costs delta_j after subtracting old captured tail energyj b. The HEAVY condition bounds top mass, but the old tail nearly cancels that mass. The approximation trigger depends on accumulatednew alpha energy in coordinates omitted byP0. Thus large stale-to-fresh motion is compatible with onlysmall OPT growth. Diagonal spectrum crossing and delayed exact refresh are established mechanisms, no priority/newmethod claim.

No uniform all-consecutive-row condition bound is asserted: a block containing originaltail rowsN and final rowsN/m can have a condition factor depending onm. The integer theorem requires no such condition hypothesis, andM=k^2+k andn<=3k remain polynomial. Full-prefix singular ratios can be bounded separately, but they are not needed by this card.

Frozen falsifier: reject/correct ifq is not an actual last reset, HEAVY does notpersist, the strict delta/outer-bound fails, the firsttrigger is not reachable, the covariance cutoff is ambiguous,epsilon restriction or row integrality fails, actual RECLUSTER differs, or any unstated F.1 hypothesis excludes the stream. Independent reviewer must reconstructq-state algebra, all inequalities and exact projection movement from primary source, without script/projectimport/numericalexperiment; return ACCEPT/NEEDS_CORRECTION/REJECT, source hashes, limitations and what theorem consequences remain unproven. Do not infer empirical/native/novelty/publication eligibility. This card admits no executable task.
