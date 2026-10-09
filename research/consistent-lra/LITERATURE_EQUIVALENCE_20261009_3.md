# Primary-source functional-equivalence audit

Date: 2026-10-09 UTC. Destination source snapshot: `Yunbo-max/test10.8@03b9ed0a4eebc59f5fdcd650fa24df20ff1d9865`. Workflow source: `Yunbo-max/Research_Autopilot@1de12dfed5b84957b29ac5b3a2f04904bf3742bc`. This is a bounded existing-paper collision audit, not an exhaustive search, originality approval, numerical result or paper-eligibility decision.

## Frozen atomic claims

1. **Known mechanism claim (must not be advertised as new):** a positive rank-one perturbation of a self-adjoint matrix has interlacing eigenvalues, Cauchy-form eigenvector overlaps and can accumulate growing cross-cutoff spectral-projector mass.
2. **Correction-application claim (still unresolved as prior art):** the explicit half-shift finite family in `FORMAL_AUDIT_v2.md` refutes the constant-eight assertion in Woodruff--Zhou Lemma 2.1 and, through alternating insertion/deletion, the rank-uniform exact-optimal statement in Theorem 2.2.
3. **Replacement-bound claim (not established):** the correct worst-case rank dependence for a single update is logarithmic rather than merely bounded by the trivial `2k` projector diameter.

## Exact functional identification

Let `P` and `P'` be the old and new top-`k` projectors from the fixed counterexample and put `E=I-P`, `F=I-P'`. Both bottom projectors have rank `k` because the construction has dimension `2k`. The projector recourse is

$$
R=\|P-P'\|_F^2=2\operatorname{tr}((I-P)P')
=2\operatorname{tr}(E(I-F)E).
$$

The last trace is exactly the Anderson integral/cross-Fermi-projection mass for the two equal-rank occupied subspaces. This is an algebraic identity, not an analogy. The `FORMAL_AUDIT_v2.md` lower bound is therefore an explicit finite-dimensional lower bound on an established spectral-projection functional.

## Primary works and actual read depth

### Gebert 2018 -- decisive functional/mechanism collision (D3 on relevant spans)

Martin Gebert, *On an integral formula for Fredholm determinants related to pairs of spectral projections*, arXiv:1705.02796v2, published DOI `10.1007/s00020-018-2461-7`, https://arxiv.org/html/1705.02796v2 . Newly checked spans: Introduction (1.1--1.2), Theorem 2.1, Corollary 2.4 (2.11--2.13), finite-matrix Section 3.1, Lemmas 3.3--3.4 (3.5--3.16), and Appendix A.1 as already recorded.

- It studies self-adjoint `B=A+|phi><phi|` and products/differences of spectral projections, explicitly as a subspace-perturbation problem.
- In the finite cyclic case it states strict eigenvalue interlacing, identifies overlap determinants with projector products, gives the Cauchy overlap formula, and computes the spectral weights from old/new eigenvalues.
- Equations (3.13)--(3.16) use the same weighted Cauchy eigenvector-overlap structure as the fixed half-shift construction. Appendix A.1 supplies the corresponding product/residue weights.

Disposition: the rank-one residue construction, interlacing, Cauchy overlaps and spectral-projector functional are established prior tools. They cannot be a new-method claim here. Gebert's determinant identity is not itself the trace lower bound `R>8`, and the inspected spans do not mention Woodruff--Zhou or the exact half-shift counterexample.

### Kuettler--Otte--Spitzer 2013/2014 -- decisive growth-phenomenon collision (D2)

H. Kuettler, P. Otte and W. Spitzer, *Anderson's Orthogonality Catastrophe for One-dimensional Systems*, arXiv:1301.4923v2, linked journal DOI `10.1007/s00023-013-0287-z`, https://arxiv.org/pdf/1301.4923v2 . Reused inspected spans: Introduction including equation (1.2), Proposition 2.1 and Theorem 5.3.

The paper defines the Anderson integral through cross-eigenvector squared overlaps and proves a leading logarithmic particle-number term under its one-dimensional Schroedinger/thermodynamic assumptions. Via the exact identity above, logarithmic growth of the same projector-cross-mass functional is an established phenomenon. Its operator family and limiting assumptions do not supply the fixed finite diagonal-plus-rank-one row-arrival counterexample, so this is a functional/growth collision rather than a proof that the exact correction application was published.

### Uebersohn 2015 and Krein lineage -- contextual collision only (D1)

- Christoph Uebersohn, *On the difference of spectral projections*, arXiv:1406.6516v2, https://arxiv.org/abs/1406.6516 . Abstract/version page inspected: rank-one spectral-projection differences are represented by bounded Hankel operators outside an exceptional countable set.
- Kostrykin--Makarov, *On Krein's Example*, arXiv:math/0606249, https://arxiv.org/abs/math/0606249 . Abstract inspected: it reports Krein's rank-one example whose spectral-projection difference is not trace class in the interior of the spectrum.

These reinforce that large/infinite spectral-projection changes under rank-one perturbations are classical concerns. Abstract-only depth does not support a more specific equivalence or bound and is not used for the decisive collision.

## Search protocol and bounded result

Search date/cutoff: 2026-10-09. Providers: current web search index plus primary arXiv/full-text pages. Query families included:

- `rank-one perturbation spectral projections Hilbert-Schmidt logarithmic bound`;
- `difference of spectral projections rank one perturbation trace norm logarithmic`;
- `Anderson integral rank one perturbation upper bound log N`;
- `principal angles spectral subspaces rank one perturbation harmonic numbers`;
- exact target title with `counterexample`, `correction`, `Lemma 2.1` and `recourse 8`;
- `half-integer rank-one perturbation spectral projection Anderson integral`;
- `Cauchy matrix spectral projections rank-one perturbation logarithmic`.

The first two batches located Gebert, Kuettler--Otte--Spitzer, Uebersohn and the Krein lineage. A third exact-target/half-shift batch added no new primary correction or exact half-shift application. It did return the target paper, the repeated Gemini proof lineage and generic rank-one SVD/Cauchy computation work; those do not correct the target lemma. Search nonappearance is not evidence that no correction exists. Citation expansion, exact priority and an independently adjudicated novelty decision remain incomplete.

## Collision decision and remaining falsifiers

- **Known mechanism/growth atom:** functional collision. Route to attributed background/comparator, not a novel method.
- **Exact 2026 correction atom:** `INCONCLUSIVE_EXPAND_SEARCH`. No inspected primary source states the same finite half-shift counterexample or applies it to this paper, but coverage is not exhaustive and full citation/provenance adjudication is unfinished.
- **Universal logarithmic replacement bound:** unproved lead only. Infinite-dimensional and model-specific logarithmic results do not imply a finite worst-case `O(log k)` upper bound. A finite family with `R/\log k` unbounded would falsify it; a correct general proof must use rank-one interlacing/Cauchy structure and handle arbitrary gaps and perturbation weights.

This audit reduces the defensible contribution scope. It does not create a paper, admit a new-method pool, qualify a numerical scorer, or authorize code/experiment dispatch.
