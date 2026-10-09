# Actual139 independent primary collision and correction-scope review

Reviewer /root/integer_density_review; immutable reviewed project
79a74855295674e7a0055f34127774b89e93062a. No edits, publication, numerical
experiments or new v7 mathematical approval. Root integrates the returned review.

Verdict: ADVANCE the narrow correction to conference Lemma 2.1; INCONCLUSIVE
priority of the combined construction; KILL novelty of secular/Cauchy/residue
machinery, claims that approximate existence Theorems 1.2/1.3 are false, and
separate-paper treatment of v5/v6/v7 variants. No paper-eligibility pass.

## Primary sources inspected and collision boundary

Hentschel, Ullmo and Baranger, arXiv cond-mat/0503330v1 (2005-03-14),
https://arxiv.org/pdf/cond-mat/0503330 , Section II.B equations 15–18 and 13:
secular equation, inverse-coordinate eigenvector, normalizer, inverse residue
weights and overlap product are prior machinery. The PDF's internal 2018 date
does not replace the arXiv version date. These mechanisms cannot be new claims.

Gebert, https://arxiv.org/html/1705.02796v2 , Theorem 2.1 equation 2.8,
Section 3.1 equation 3.3, Lemma 3.3 equations 3.5–3.10 and Lemma 3.4/Remark 3.5
equations 3.11–3.14: rank-one interlacing, projection products and Cauchy overlap
identities are prior art. A small product of squared cosines does not alone give
a linear sum of squared sines. Theorem 2.10's small-operator-norm premise does
not apply to the unconstrained update here. Prior Anderson-integral papers
(Küttler–Otte–Spitzer 2013; Gebert–Küttler–Müller–Otte 2016) were inspected only
partially and do not establish the combined collision.

Original conference paper:
https://proceedings.iclr.cc/paper_files/paper/2026/file/b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf
Lemma 2.1, Theorem 2.2 and Appendix proof pages 19–20. In the proof,
w in the old top space intersected with the arrival's orthogonal complement
implies the two matrices act identically on w, but does not imply that this
intersection is spanned by common eigenvectors. A subspace of an invariant
space need not itself be invariant. The inferred k−2 common optimal directions
therefore do not follow. The dimension-formula typo alone is not the decisive
defect: its corrected Grassmann lower bound still holds.

Accepted v5 gives R > 2k/15, hence k=61 exceeds the claimed constant 8;
v6 adds all nonempty ordered consecutive positive blocks with condition <4;
v7 adds deterministic nonnegative integer rounding and O(k+log k) entry bits.
This supports a narrowly scoped Lemma 2.1 correction. The single-arrival example
also contradicts a rank-uniform constant for arbitrary initialization; if the
2k initialization rows count as arrivals, its R=Theta(k) is O(n), and that one
instance alone does not refute a pure-insertion O(n) reinterpretation. Separate
previous insertion/deletion cycle arguments retain their own scope. Conference
numbering 2.1/2.2 differs from arXiv v1 numbering 2.3/2.4.

Approximate-existence Theorem 1.2 allows rank-dependent recourse, compatible with
this exact-optimum lower bound. Its use of the faulty lemma is a proof dependency
requiring repair, not a proof that the existence statement is false. Theorem 1.3's
integer rank/bit-dependent bound is also compatible; Algorithms 3/4 are not
refuted by this family. No optimized method or native performance comparison.

## Actual bounded inquiry

Eight new queries on 2026-10-09; at most three new primary fulltexts allowed:

1. `"rank-one perturbation" "spectral projector" Frobenius linear dimension finite matrix`
2. `"Anderson integral" rank-one finite-dimensional linear rank spectral projection`
3. `"integer matrix" "rank-one perturbation" spectral subspace projector recourse`
4. `"consecutive submatrix" condition number rank-one perturbation spectral projector`
5. `"orthogonality catastrophe" "geometric progression" rank one eigenvalues`
6. `"Cauchy" eigenvector overlaps "rank-one perturbation" finite matrix projector`
7. `"spectral projection" "rank-one perturbation" Hilbert-Schmidt norm finite dimension lower bound`
8. `"Consistent Low-Rank Approximation" "Lemma 2.1" counterexample OR correction OR erratum`

The last query returned the target on arXiv/OpenReview in this limited surface;
absence of a correction result does not establish priority. Backward-citation
coverage and cross-search of the full ordered-condition/integer-bit conjunction
remain incomplete; no author contact or exhaustive erratum search occurred.
Only a narrow correction-note direction is plausible, with known machinery
attributed and conjunction originality pending. No multiple-paper admission.

The review's pinned snapshot had actual138 pending. Subsequent actual138
acceptance at e12a3d10853509cc560c70070c0ab3b990115621 establishes integer
construction bytes/arithmetic only; it does not upgrade this originality verdict
or supply a measured projector/condition certificate.
