# Canonical assignment168 (worker-local 162): bounded priority audit for the integer conjunction

Binding: `main` `e9faa76b2d34b51d0a2b31247c28d3938db3920e`, with
underlying legacy evidence at `7286e6d5b301f01ebda45d6fa1387afd9d383906`.
This is a primary-source collision audit, not a novelty, execution or paper gate.

## Disposition

**Advance the narrow correction; combined-conjunction priority remains
inconclusive.** The secular equation, inverse-coordinate eigenvector formula,
residue recovery, Cauchy overlap matrix and determinant/product identities are
established prior machinery. Under the bounded search below, no direct collision
was located for the full conjunction:

1. a finite-dimensional rank-one PSD update;
2. `||P_new-P_old||_F^2 = Omega(k)`;
3. nonnegative integer input data;
4. constant conditioning for every relevant nonempty/full-rank consecutive row
   block under the documented rectangular convention; and
5. polynomial entry bit length.

This supports a narrowly scoped correction/counterexample to conference Lemma
2.1 with the classical machinery attributed. It does not establish exhaustive
novelty, priority or paper eligibility.

## Primary-source comparison

- Woodruff and Zhou, *Consistent Low-Rank Approximation*, ICLR 2026 conference
  PDF, Lemma 2.1 and proof pp. 19--20:
  https://proceedings.iclr.cc/paper_files/paper/2026/file/b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf .
  This is the corrected target, not a prior collision.
- Hentschel, Ullmo and Baranger, arXiv:cond-mat/0503330v1, Section II.B,
  equations 13 and 15--18: rank-one secular equation, inverse-coordinate
  eigenvectors, normalisation/residue weights and overlap products. This is a
  collision for the machinery, not the integer/block-conditioning/bit-complexity
  conjunction.
- Gebert, arXiv:1705.02796v2, Theorem 2.1, Section 3.1 and Lemmas 3.3--3.4:
  interlacing, projection-product determinants and Cauchy overlap identities.
  A small product of squared cosines does not alone prove a linear sum of
  squared principal sines.
- Mitz, Sharon and Shkolnisky, arXiv:1710.02774v4, equations 1--3:
  classical symmetric rank-one update, secular equation and eigenvector formula.
- J. Anderson, *Linear Algebra and its Applications* 246 (1996), 49--70,
  “A secular equation for the eigenvalues of a diagonal matrix perturbation”:
  an adjacent inverse/secular framework; full text was not forensically checked.
- Zimmermann, *Mathematics of Computation* 90 (2021), Definition 3.1,
  Lemma 3.2 and Corollary 3.3: a direct column-range update has one nonzero
  principal angle. It is not the top-k invariant subspace of a Gram matrix after
  a row append and therefore is not a collision.
- Uebersohn, arXiv:1406.6516, and Post--Uebersohn, arXiv:1710.10975:
  infinite-dimensional rank-one examples with large/non-Hilbert--Schmidt
  spectral-projection differences. They make the broad instability phenomenon
  prior art, but do not cover the finite integer conjunction.
- Luo, Han and Zhang, arXiv:2008.01312: general principal-angle/Schatten
  perturbation bounds and lower bounds under different hypotheses; no direct
  conjunction collision.

The certificate's rational `Omega(k)` inequality and integer realization are
construction evidence, not priority evidence.

## Exact bounded queries, 2026-10-09

1. `site:arxiv.org rank-one PSD update spectral projector Frobenius norm lower bound linear rank finite-dimensional matrix`
2. `site:arxiv.org positive integer matrix rank-one perturbation spectral subspace projector lower bound`
3. `site:arxiv.org Cauchy matrix eigenvector overlap rank-one perturbation spectral projector Hilbert-Schmidt finite dimension`
4. `site:arxiv.org consecutive row blocks condition number constant integer matrix spectral projector perturbation`
5. `Gebert 1705.02796 rank one perturbation spectral projection overlap theorem 2.1`
6. `Küttler Otte Spitzer 2013 Anderson integral rank one perturbation spectral projections finite volume`
7. `Gebert Küttler Müller Otte 2016 Anderson orthogonality catastrophe rank one perturbation spectral projections`
8. `lower bound Hilbert-Schmidt norm difference spectral projections rank one perturbation rank k`
9. `site:arxiv.org inverse eigenvalue problem diagonal plus rank one prescribed interlacing eigenvalues positive residues`
10. `site:doi.org diagonal rank-one update inverse eigenvalue problem interlacing positive weights secular equation`
11. `site:arxiv.org exact integer matrix eigenvectors rank-one perturbation polynomial bit complexity spectral projector`
12. `site:arxiv.org well-conditioned row prefixes integer matrix low rank approximation counterexample projector recourse`
13. `"online condition number" "rank-one" spectral projector top-k subspace counterexample`
14. `"well-conditioned" "spectral projector" "rank-one perturbation" lower bound`
15. `"top-k subspace" "rank-one update" Frobenius lower bound`
16. `"rank-one PSD update" "top-k" eigenspace changes`
17. `"principal angles" "rank-one perturbation" eigenspaces lower bound`
18. `"Frobenius norm" "difference of spectral projections" rank-one`
19. `"Hilbert-Schmidt norm" "difference of spectral projections" rank one finite-dimensional`
20. `"subspace distance" "rank-one update" eigenspace can change`
21. `"Proof of a Conjecture of De Cock and De Moor" Cauchy matrix principal angles pdf`
22. `"rank-one perturbation" "principal angles" Cauchy matrix rational interpolation`
23. `"A geometric approach to subspace updates" rank-one modifications principal angles pdf`
24. `"A geometric approach to subspace updates and orthogonal matrix decompositions under rank-one modifications"`
25. `"integer" "diagonal plus rank-one" eigenvalues interlacing matrix`
26. `"integer matrix" "secular equation" rank-one update`
27. `"polynomial bit length" rank-one perturbation eigenvalues`
28. `"positive integer" matrix "rank-one perturbation" eigenvector`
29. `"Consistent Low-Rank Approximation" "Lemma 2.1" counterexample`
30. `"Consistent Low-Rank Approximation" erratum correction recourse`
31. `"optimal rank-k subspace" "recourse" "rank-one"`
32. `"rank-one updates" "recourse" spectral subspace`
33. `"all consecutive row blocks" "condition number" matrix`
34. `"every consecutive submatrix" condition number matrix`
35. `"online condition number" matrix row prefixes polynomial low rank approximation`
36. `"all prefixes" condition number bounded matrix rows spectral subspace`
37. `site:arxiv.org "The Spectral Density of a Difference of Spectral Projections" rank one explicit pair`
38. `site:arxiv.org "difference of spectral projections" rank(H-H0)=1 noncompact`
39. `site:arxiv.org Pushnitski Yafaev difference spectral projections rank one explicit example`
40. `site:arxiv.org Frank Pushnitski spectral density product spectral projections rank one`
41. `"A geometric approach to subspace updates" "principal angle" rank-one`
42. `Zimmermann rank-one subspace update "one nonzero principal angle"`
43. `"subspace distance" "Xnew = X + abT" principal angle`
44. `"rank-preserving rank-one modifications" Grassmann geodesic principal angle`
45. `"A secular equation for the eigenvalues of a diagonal matrix perturbation" Anderson 1996`
46. `"secular equation" "diagonal matrix perturbation" Anderson Linear Algebra Applications 246`
47. `"A secular equation for the eigenvalues" pdf`
48. `site:sciencedirect.com "A secular equation for the eigenvalues of a diagonal matrix perturbation"`
49. `OpenReview 3sJ4zKToW6 Consistent Low-Rank Approximation comments correction Lemma 2.1`
50. `site:openreview.net/forum?id=3sJ4zKToW6 Lemma 2.1`
51. `site:openreview.net "Consistent Low-Rank Approximation" "counterexample"`
52. `site:openreview.net "Consistent Low-Rank Approximation" "rank-one"`

## Coverage gaps and allowed wording

No exhaustive forward/backward expansion from Anderson 1996, Gebert 2018,
Zimmermann 2021 or the target paper was completed. MathSciNet, zbMATH, Scopus
and Web of Science were not searched; Anderson's full text was not fully read;
there was no author contact. Bounded OpenReview/arXiv searches cannot prove that
no erratum or independent correction exists. Terminology for the consecutive-
block and bit-complexity conjunction may differ and is the least-covered part.

Use **nonnegative integer matrix**, not entrywise positive. Entry magnitudes are
exponential while `O(k+log k)` entry bits are polynomial. State exactly which
nonempty/full-rank blocks and rectangular condition-number convention are used.
This audit did not re-enumerate every block; it assessed the stored analytic
claim.

Recommended boundary: “The conference Lemma 2.1 proof is false, and the
certified family refutes its constant bound. Classical rank-one secular/Cauchy
formulas are used. Under the documented bounded search, no prior source was
located containing the entire integer, uniformly block-conditioned,
polynomial-bit `Omega(k)` construction.”
