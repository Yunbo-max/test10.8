# Independent v5 geometric-family formal review

Assignment: window02-geometric-formal-independent-review (83). Actual reviewer /root/window02_geometric_formal_review, independent of construction author /root/window02_scorer_scope_review. Reviewed exact commit a32730715cf772e8c492b1bf880d6e58cbc35617, artifact FORMAL_AUDIT_v5_GEOMETRIC_DRAFT.md, SHA256 de008df475aba17eb4557fdeb5e7ed57d7843f79dd107ecbed686e40ef717ef5, Git blob d722856097a7132c85e63ef007eec6caaa1a18c3. Reviewer fetched exact GitHub contents and matched local bytes; no edits, numerical experiments or evaluator dispatch.

Verdict: ACCEPT all stated exact mathematical claims; no blocking correction. This is not novelty, native scoring or paper eligibility.

## Independently checked predicates

1. Strict rank-one interlacing holds for negative and positive scales, including central and largest transitions. At ordered old eigenvalue j, numerator and residue-denominator negative-factor counts differ by one, hence every rho=-Res g is positive. Equal-degree monic products give constant partial-fraction term 1. Determinant lemma yields the prescribed simple updated spectrum.
2. At -a_i, own-scale residue prefactor is 3a_i/4. Smaller-scale product factors exceed 1; larger-scale factor is 1-3r/[2(1-r²)] >=1-(8/5)r>0. Using the finite geometric sum <1/15 and product inequality gives rho_-ai >=67a_i/100>2a_i/3.
3. g(mu)=0 gives sum rho/(mu-lambda)=1; w_lambda=u_lambda/(mu-lambda) is a genuine updated eigenvector. Its squared norm is g'(mu), so b=1/g' normalizes it. For mu=2a_i, own-scale reciprocal derivative prefactor is6a_i/5 and other denominator is4a_i²-3a_i a_j-a_j². Smaller scales have factor>1; larger scales >=1-3r. Therefore b_i>=24a_i/25>9a_i/10. Orthogonality follows from symmetric simple spectrum.
4. Matched cross-cutoff mass rho_-ai*b_i/(9a_i²)>1/15. Both top-k spaces are unique. Equal-rank projector identity gives R=2*sum cross masses>2k/15. Dropping unmatched nonnegative terms is sound.
5. c=2a_k makes old covariance spectrum [a_k,3a_k], updated [3a_k/2,4a_k]. A=C^(1/2) with appended u^T is an actual real row arrival. k61, dimension122, gives R>122/15>8. General equal-rank upper bound R<=2k makes unrestricted worst-case rank dependence Theta(k), rejecting the prior assumption-free logarithmic replacement conjecture.
6. Full covariance condition numbers3 and8/3, old data condition sqrt3, are exact. Increasing common shift preserves projectors while full covariance conditions approach1. This is not yet a condition over row blocks. Relative cutoff gap32/(3*16^k) decays exponentially, and ordinary floating representation cannot preserve small shifted separations at k61. No stable float64/performance claim.

## Paper and originality scope

Reviewer independently read the proceedings Lemma2.1 and AppendixE, plus arXiv-v1 Lemma2.3; their constant-eight real-row-arrival assertion is contradicted as stated by this family. This does not refute the main approximate-existence result or Algorithm4's separate additive-error energy argument. Known weighted Cauchy/residue machinery is attributed to Gebert (equations3.13–3.16 and AppendixA.1). A complete priority audit of the geometric family/application remains pending. This refines the same formal correction lineage, not a second paper from spectral spacing.

Primary sources: https://proceedings.iclr.cc/paper_files/paper/2026/file/b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf ; https://arxiv.org/abs/2603.02148 ; Gebert primary source already recorded in the pinned card/lineage ledger.

## Separate unreviewed follow-on

Reviewer suggested a separately ordered-row consecutive-conditioning corollary. It is excluded from this pinned acceptance and requires a new derivation and an independent reviewer who did not author it. Formal/native/novelty gates are not advanced by that suggestion.
