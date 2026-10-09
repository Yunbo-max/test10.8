# Rank-family v2 strict-trigger clarification — frozen addendum

Root integrates separately proved consequence supplied by actual independent reviewer165. This addendum does not change v1's stream, bounds, epsilon, thresholds or prediction. It supplies the missing strictness proof necessary to apply F.1's approximation-failure premise; v1's first>=trigger by itself was insufficient to rule out equality. Preserve HEAVY_BRANCH_INTEGER_RANK_FAMILY_DRAFT.md unchanged, SHA25675407facfe13695286ed775dc49c072806db14e0d2e30a187769c2d5ae52d675 atc3b221820ce96f93e1cdecd47a3158f1b0ab8f50. Actual165 accepts its construction/state/recourse algebra; strict-F.1 implication is held pending the separate166 review of this addendum. Source proposition is the same existing-paper audit, no newmethod/paper/code/experiment.

## Added exact proof, all1<=j<=q<=k=m^4

KeepN=m^8,b=m^16,m>=11,delta_j=N j(j+1)+j(j+1)(2j+1)/6 andepsilon1/m^2. Eachdelta_j is a positive integer. Moreover

delta_(k-1)=N k(k-1)+(k-1)k(2k-1)/6
<b-m^12+m^12/3=b-(2/3)m^12<b,

since(k-1)k(2k-1)/6<k^3/3. Also

delta_k=b+m^12+k(k+1)(2k+1)/6>b,

delta_k<=b+2m^12<2b,

becausek(k+1)(2k+1)/6<=k^3 forintegerk>=1 and2<m^4. The incrementsdelta_(j+1)-delta_j=2N(j+1)+(j+1)^2 are strictlypositive. Thus all1<=j<=k have0<delta_j<2b, withdelta_j<b forj<=k-1 anddelta_k>b. No suchdelta_j equalsb or any positive multipleofb below2b.

IfD_j=0, multiplicationby2m² gives

(2j-q)b=(2m²+1)delta_j.

Everyprimefactorofb=m^16 dividesm; but2m²+1 is1moduloeveryprimefactorofm. Thusgcd(b,2m²+1)=1, implyingbdividesdelta_j, a contradiction. ThereforeD_j isneverzero for1<=j<=q. Sincev1alreadyprovedD_q>0,thefirst>=triggerj_*actuallyhasD_(j_*)>0. The previousP0 strictlyfails the1+epsilon/2 bound, so the exactreachable HEAVY output pair satisfies F.1's strict premise.

## Clarified accepted-claim target

After166independentlyacceptsbothv1andthisproof,the family impliesR=2j_*>q>4k/5 for arbitrarilylargem,k=m^4,epsilon1/m²<1/100,withnonnegativeintegerrowsandM=k²+k. Consequentlyno uniformconstantK independentofepsiloncanrepairF.1toR<=Ksqrt(k). Epsilonchangeswithk; epsilon-dependentconstants are NOT excluded. This is a per-refresh assertion only; no refutationofTheorem1.3'sapproximateexistence/fulltotal-recourse bound, no all-consecutivecondition<4, no one-rowchangebetweenconsecutiveexactoptima, no empirical/newmethod/novelty/paperpass. PersistentAlgorithm2semantics remainexplicit.

## Independent166 falsifier

Reject/correctifdeltaarithmetic,positivity/integrality,strictordering,gcdimplication,firsttrigger,primarysourcepremiseorclaimscopefails. Reviewer166mustbeindependentof165'snewstrictnessderivation; hashbothv1/addendum/taskatthesuppliedimmutablemaincommitandderiveproofagain. No sourceimport, script, numeric work, publication or thresholdchange. Rootaccepts onlyactualreturnedpredicate andpreserves all gaps.
