# Explicit integer geometric counterexample — author draft awaiting independent review

Actual assignment 103: window02-geometric-explicit-integer-bit-bound-derivation. Author /root/window02_geometric_formal_review. Root integrated the returned derivation; the author issued no acceptance, code, workload or publication. Source pin 4620aab26aa9d5706d0b5861224b84ab9f247c0a. This strengthens the existing published-lemma correction lineage; it is not another algorithm, discovery-pool admission, native result or separate paper.

## Object and proposed claim

For every integer k>=1, construct a nonnegative integer diagonal matrix A_Z with 2k rows/columns and integer appended row h^T, ordering coordinate lambda=-16^k first. The proposed bounds are: unique old/new top-k projectors; R_Z>2k/15-1/100>k/10; every nonempty consecutive block, and the cross-block ratio max_B sigma_max(B)/min_B sigma_min,+(B), has condition <402/103<4; maximum integer entry <=257k16^k. Here sigma_min,+ means smallest positive singular value. At k=61, dimension122, proposed R_Z>122/15-1/100>8. These are new analytic integerization claims pending independent review, not claims established by the existing real-parent certificate.

## Fixed accepted parents

At the source pin: v4 draft blob c879db8883bf9b236d4143ce0394c637bb4c637b, review0f666c03e4789f9ae82fd193111e8d801b821433; v5 draftd722856097a7132c85e63ef007eec6caaa1a18c3, review45a6b833a85d5019cc99d633ebc24b52ae668899; v6 drafta14bb78ed8f36c17f21b9bc36decf7551de7eff4, review824a5f827172aea695a2a9bfafc531779f6aecdc; priority auditf8fc002ff2e1c682bfa972655fdfb6a4d8ae339a. The accepted v5/v6 parents supply A,T=[A;u^T], a=16^k, ||T||op<=2 sqrt(a), R>2k/15, old cutoff gap32/newgap40, and all consecutive blocks' positive squared singular values in [5a/18,4a]. Use the increasing Lambda order, so -a is first, and append u last.

Primary perturbation theorem: Yu, Wang and Samworth, A useful variant of the Davis–Kahan theorem for statisticians, Biometrika2015, Theorem2, https://personal.lse.ac.uk/wangt60/publication/DKvariant.pdf. Author reread the theorem for the original cutoff gap and Frobenius sine-angle bound; equal-rank projector norm is sqrt(2) times that sine-angle norm. This is established machinery, not a novelty claim.

## 1. Explicit rounding construction

Lambda={-16^i,+16^i:1<=i<=k}; M={-16^i/2,2*16^i:1<=i<=k}. Retain positive rational rho_lambda=-prod_mu(lambda-mu)/prod_nu!=lambda(lambda-nu) from v5. Choose S=128k4^k=128k sqrt(a). For x>=0 define rnd(x)=floor(x+1/2), upward ties. Set diagonal (A_Z)_lambda,lambda=rnd(S sqrt(2a+lambda)), h_lambda=rnd(S sqrt(rho_lambda)); off-diagonal entries remain zero. Increasing Lambda order has -a first.

[A_Z;h^T]=ST+Delta. Only 2k diagonal and 2k appended-row entries incur error, each <=1/2. Thus ||Delta||F<=sqrt(k). Delta^T Delta=diag(e_lambda^2)+ff^T, giving ||Delta||op<=sqrt(2k+1)/2<=sqrt(k). Both bounds hold for restricted old-square error. The covariance append identity is exact: T_Z^T T_Z=A_Z^T A_Z+hh^T. The conditioning argument below establishes h nonzero, so the update is positive rank one.

## 2. Covariance error and unique cutoff projectors

For either old or augmented X and normalized rounded Xhat=X+Delta_X/S,

||Xhat^T Xhat-X^T X||F <=2||X||op ||Delta_X||F/S+||Delta_X||F^2/S^2
<=4 sqrt(a) sqrt(k)/S+k/S^2
=1/(32 sqrt(k))+1/(16384ka)
<=8193/(262144 sqrt(k))<1/(30 sqrt(k))=:tau_k.

Operator error is no larger. Eigenvalue Weyl leaves old/new cutoff gaps at least32-2tau_k and40-2tau_k, both positive. Thus both integer covariances have unique top-k projectors; multiplying covariance by S^2 changes no projectors.

## 3. Linear recourse survives rounding

Let P,P' be real parents' projectors and Q,Q' integer projectors. The sourced Davis–Kahan theorem and equal-rank projector identity imply

||Q-P||F<=2sqrt(2)tau_k/32;
||Q'-P'||F<=2sqrt(2)tau_k/40.

Their sum <=9sqrt(2)tau_k/80<1/(180sqrt(k))<1/(100sqrt(k)). Reverse triangle therefore gives sqrt(R_Z)>sqrt(2k/15)-1/(100sqrt(k))>0. Squaring,

R_Z>2k/15-(2/100)sqrt(2/15)+1/(10000k)>2k/15-1/100>k/10.

The last inequality uses k/30>1/100 for every k>=1. For k61, R_Z>122/15-1/100>8. The universal upper bound R_Z<=2k applies, hence linear worst-case rank dependence. This establishes no approximate-algorithm refutation.

## 4. All consecutive blocks retain condition <4

For each parent block B, Bhat=B+Delta_B/S, ||Delta_B/S||op<=sqrt(k)/S=1/(128 sqrt(k) sqrt(a)). Relative to sqrt(a), the error is <=1/(128 sqrt(k)a)<=1/2048<1/100. By singular-value perturbation and v6,

sigma_max(Bhat)<(201/100)sqrt(a),
sigma_min,+(Bhat)>(sqrt(5/18)-1/100)sqrt(a)>(103/200)sqrt(a),

using sqrt(5/18)>21/40. Rank cases must be retained: diagonal-only blocks remain full row rank; appended row alone rank1; proper diagonal suffix plus h has <=2k rows and preserves full row rank; full (2k+1)-row matrix preserves full column rank2k. The structural zero of the full row Gram is excluded under positive-singular convention. Thus no former zero is incorrectly used in the minimum. After scaling by S, one uniform positive-singular interval covers all blocks, and max sigma_max/min sigma_min,+ <(201/100)/(103/200)=402/103<4. The specified row order is required, not arbitrary subsets or permutations.

## 5. Entry and encoding bounds

sqrt(2a+lambda)<=sqrt(3a)<2sqrt(a); sqrt(rho_lambda)<=||u||<2sqrt(a). Hence each rounded nonnegative integer <=2Ssqrt(a)+1/2=256ka+1/2<=257k16^k. Each entry uses at most 4k+ceil(log2 k)+9 bits because 257k16^k+1<=512k16^k. At k61 this gives259bits/entry. Bit length is O(k+log k); magnitude remains exponential in k. Dense encoding has polynomial total size; sparse diagonal-plus-row encoding has only4k potentially nonzero entries.

## 6. Formal integer-only generation algorithm (not executed)

Each needed r=N/D>0 is either2a+lambda or a residue. Compute q=floor(4S^2 N/D), n=isqrt(q), m=floor((n+1)/2). Then n=floor(2Ssqrt(r)) and m=rnd(Ssqrt(r)), including exact half-integer ties. No numerical square-root oracle or floating point is needed. Each residue numerator/denominator is a product of at most2k differences with magnitude<4a; unreduced product bit length <=8k^2+4k+1. Scaling/division/isqrt and O(k^2) product operations therefore have polynomial bit complexity. This is a formal generation algorithm, not yet source/execution-qualified software.

## Boundaries, falsifiers and next review

This supplies a constructive quantitative rounding margin and bit bound absent from v4's nonquantitative density argument. Retain v4 and its correction history. It establishes neither polynomial integer magnitude, stable float64 performance, native results, novelty nor paper eligibility. The approximate-existence theorem and bounded-integer approximation guarantees keep their distinct assumptions/parameters; this does not prove them false or repair their proof dependency.

The unchanged k61 rational certificate corroborates the real parents only; it neither constructs these integers nor verifies integer projector/block conclusions. Any executable integer extension needs separate source/plan/evidence admission. Independent reviewer104 must check covariance Frobenius products, both cutoff gaps, Davis–Kahan factors, strict recourse margin, block rank cases, exact rounding identity, bit bounds, and polynomial bits versus exponential magnitude. Any failure of these implications falsifies the corresponding strengthened claim; author has not self-signed acceptance. Application priority remains unresolved.
