# Independent review of explicit integer bit-bound extension

Actual assignment104 window02-geometric-explicit-integer-bit-bound-independent-review. Reviewer /root/window02_scorer_scope_review, independent of new v7 author /root/window02_geometric_formal_review. Immutable commit3f8aa6e48335052f93b75e55a4ce3a41311481ca restored by git fetch/git show. Candidate SHA256d0f56dbf1ec12c302ad2b42e8ae608a06c9c6c2da63b50da2ee11f6ec8fede79. Verdict ACCEPT v7's stated analytic integerization and encoding claims, no blocking correction. Reviewer authored v5/v6 parents, whose separate independent reviews remain the basis; this is not another independent acceptance of those parents. No workload, code creation, edits, publication or external contact.

All4k rounding errors <=1/2 imply Frobenius<=sqrt(k); diag(e^2)+ff^T gives operator<=sqrt(2k+1)/2<=sqrt(k), including k1. Normalized covariance error <=1/(32sqrt(k))+1/(16384ka)<=8193/(262144sqrt(k))<1/(30sqrt(k)); ||E^T E||F<=||E||F^2 supplies the correct product bound without missing dimension factor.

Old/new cutoff gaps32/40 hold including k1; Weyl leaves positive gaps. Published Yu–Wang–Samworth Theorem2 (original gap, Frobenius sin-angle factor2) and projector sqrt2 conversion yield 2sqrt2 tau/32 and2sqrt2 tau/40. Sum<3sqrt2/(800sqrt(k))<1/(180sqrt(k))<1/(100sqrt(k)). Reverse triangle has positive lower bound; squaring yields R_Z>2k/15-.01>k/10 for everyk>=1. At61,122/15-.01>8. Universal R_Z<=2k remains valid.

Consecutive-block row restriction cannot increase error; normalized relative perturb <=1/(128sqrt(k)a)<=1/2048<.01. Singular perturbation and accepted parent interval give common positive-singular interval ((103/200)Ssqrt(a),(201/100)Ssqrt(a)); sqrt(5/18)>21/40 checks. Diagonal-only, singletonh, proper suffix+h retain full row rank; complete tall stream retains full columnrank2k, excluding structural row-Gramzero. No extra positive singular dimensions appear. h nonzero makes update genuinelyrank1; perblock andcrossblock condition<402/103<4. Rowordering andk1/singleton/tworow/fullstream cases preserved.

Rounded entries<=256ka+.5<=257k16^k; bound+1<=512k16^k implies unsigned bitlength<=4k+ceil(log2k)+9,259at61. Zero entries fit. This is polynomial bitlength, not polynomial magnitude.

Integeronly generation is exact: isqrt(floor4S^2N/D)=floor2Ssqrt(N/D), because flooring cannot cross integer-square threshold; floor((floor2x+1)/2)=floor(x+.5), including upward halfinteger ties. All spectral differences integral; positive rational residue signs normalized. Atmost2k factors ofmagnitude<4a give intermediate productbitbound8k^2+4k+1; scaling addsO(k+logk)bits, so multiplication/division/isqrt have polynomialbitcomplexity.

| Other fixed artifact | SHA256 |
|---|---|
| v4 draft | 9bd273081ee32ec9dbfb0372b1443420265a8be8f483b350c7ca68ea20b1890e |
| v4 review | 5d7722060ab8dcba0d75404cf841fc277c00f6bbd383550881203afb9ce48036 |
| v5 draft | de008df475aba17eb4557fdeb5e7ed57d7843f79dd107ecbed686e40ef717ef5 |
| v5 review | d13f5faa8ce4ebcc75af96b21ee74671fe98da3bb723d32ab91e5740be744f8a |
| v6 draft | 140141fcc4b5e86bc182ea1bf399f80f6df5f1cb4dd8fe6c76b9bd569bd6573b |
| v6 review | d071c3515b981f309ca825950ff872d58fed6467c6167470eb208195225e88f7 |
| Priority audit | f3f43292d88a4ea06652900f2999ba00884b1d7d46c1da85180141d8b0cb6b2e |

Acceptance is constructive exact math/encoding only. Magnitudes exponential, stable floats/generatedintegercertificate/empirical/native/priority/papereligibility not established; approximate-existence theorem not refuted. Existing real rational certificate pertains to real parents only. Primary theorem reviewed: https://personal.lse.ac.uk/wangt60/publication/DKvariant.pdf Theorem2, not a new method.
