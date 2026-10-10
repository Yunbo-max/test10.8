# B10 revised decision after independent verification

Date: 2026-10-10

Status: **NO-GO for new-method code; candidate pool shortfall retained as a negative result.**

Inputs:

- candidate-author draft `B10_CANDIDATE_POOL_DRAFT.md`;
- independent review `INDEPENDENT_B10_VERIFICATION.md`;
- finite diagnostic `B10_IDENTITY_CHECK.json` and runner receipts;
- Hara--Yoshida paper record and official code at
  `sato9hara/consistent-pca-sc@2d04e05e2370d68d3cb2e0f06fb964d7ab36042f`.

This document supersedes the draft's provisional Top-15. It does not erase the draft or the
review, and it does not claim a new method.

## 1. Accepted corrections

### 1.1 D4 monotonicity is valid, ordinary boundary bisection is not enough

For any global optimizers at two strictly ordered parameters, overlap with the previous
projector is nondecreasing and captured data energy is nonincreasing. No cross-parameter
"consistent tie selection" assumption is needed.

At a fixed parameter with a cutoff tie, however, the maximizing projector is set-valued.
The review's reproducible example

\[
G=\operatorname{diag}(1,3),\quad P_0=e_1e_1^\top,\quad k=1,\quad \mu=2
\]

gives \(G+\mu P_0=3I\). With \(\eta=1\), different optimal projectors at that same
\(\mu\) can be feasible, infeasible, or exactly on the boundary. Therefore a scalar
bisection plus an arbitrary eigensolver tie rule does not prove the maximum-overlap
feasible endpoint.

A necessary candidate tie-face secondary specification is as follows; its sufficiency for the
global constrained problem and its solver remain unproved. Let \(M_\mu=G+\mu P_0\), let \(E_>\)
span eigenvectors strictly above the cutoff eigenvalue, and let \(E_=\) span the cutoff
eigenspace. Every penalized optimum has

\[
P=P_>+E_=QE_=^\top,
\]

where \(Q\) is a rank-\(r\) projector in the tied space. For \(\mu>0\),
\(\operatorname{tr}(PM_\mu)\) is constant on this face, so

\[
\operatorname{tr}(PG)=\text{constant}-\mu\operatorname{tr}(PP_0).
\]

Thus the tie-face secondary problem must explicitly maximize overlap subject to the real
feasibility constraint, rather than accepting an arbitrary basis. This is a correction to the
solver specification, not a novelty claim; its full global constrained-optimum proof remains open.

### 1.2 C12 minimum statement is narrowed

The only retained statement is:

> For a pre-fixed one-plane path, with the current point infeasible, exact OPT, principal-angle
> representatives in \([-\pi/2,\pi/2]\), and enumeration of all boundary roots on both sides,
> the feasible root minimizing \(|\theta|\) minimizes \(\sin^2\theta\) on that path.

It is not a Grassmann-global minimum. If a strict lower bound \(L<\mathrm{OPT}\) is used,
the statement applies only to the stronger surrogate boundary
\(C\le(1+\eta)L\), not to the original (F) boundary.

### 1.3 C20 is a component, not a method

The safe condition is a certified Ky Fan upper enclosure

\[
U\ge\sum_{i=1}^k\lambda_i(G),\qquad
L=\operatorname{tr}(G)-U\le\mathrm{OPT}.
\]

Ordinary top Ritz values point in the unsafe direction, and a small residual does not identify
the top cluster. Until a concrete interval method supplies index matching, separation and
roundoff-safe enclosures, C20 is only a certificate research task. If candidate cost is itself
approximate, acceptance additionally requires a certified upper bound \(\overline C(P)\ge C(P)\)
with \(\overline C(P)\le(1+\eta)L\).

## 2. Direct collision upgrade for C10

C10 is no longer merely a collision threat. The official Hara--Yoshida implementation
`packages/ConsistentML/src/ConsistentML/PCA.py` defines `ConsistentPCA.update` using

```python
A = x.T @ x / x.shape[0] \
    + 0.5 * (lam / x.shape[0]) * W_prev @ W_prev.T
```

and takes its top eigenvectors. This is the same \(G+\mu P_0\) computation as C10 up to
positive scaling and parameterization. The independent review also located the matching
projector-distance definition and penalized objective in the AISTATS 2026 paper.

Disposition: **C10 is attributed prior-art control.** C14 is its restricted Rayleigh--Ritz
implementation variant and C15 is a parameter-search wrapper; neither counts as a distinct
new method.

## 3. Corrected structural ledger

The draft's 20 identifiers are retained for provenance but are not treated as 20 methods.

| Class | IDs | Counted as independent discovery candidates? | Revised status |
|---|---|---:|---|
| Exact/iterative comparators | C01--C04 | No | controls |
| Known streaming/tracking/sketch comparators | C05--C10 | No | controls or excluded |
| Residual-RR primitive | C11 | No | C16 first-step ablation |
| One-plane/block boundary family | C12--C13 | One family | unresolved high-collision hypothesis |
| Overlap regularizer family | C14--C15 | No | C10 variants/wrappers |
| Adaptive certified expansion | C16 | One family | unresolved engineering hypothesis; policy not frozen |
| Expansion policies | C17--C19 | No | C16 ablations |
| Spectral certificate | C20 | No | cross-cutting component |

The honest pool now contains **two unresolved families**, not about twenty verified distinct
candidates. Calling both the high-collision boundary family and the still-unfrozen C16 engineering
family discovery leads is already a generous count. There is therefore
no valid Top-15 selection and no `--before code` pass in B10.

## 4. What the finite CPU check did and did not establish

The simple-runner window used two successful attempts after replacing an initial zero-attempt
budget-fit plan (the original 120-second timeout could not fit the 120-second aggregate budget
plus cleanup reserve). Actual command wall was 0.581792941 s; the diagnostic reported
0.831112142 CPU s and 24,264 KiB peak RSS.

Across 200 deterministic random cases:

- D1 rank-one residual identity max error: \(1.30\times10^{-13}\);
- D3 energy identity max error: \(1.42\times10^{-14}\);
- D3 recourse identity max error: \(1.44\times10^{-15}\);
- no D2 sampled restricted-optimality violation;
- no D4 overlap monotonicity violation and max energy monotonicity roundoff
  \(2.70\times10^{-13}\);
- all 200 deliberately wrong invariant clusters had near-zero residual but suboptimal cost.

These are finite diagnostics, not proofs. They deliberately do not override the tie counterexample,
the missing C12 global claim, or the missing practical C20 certificate.

## 5. Revised machine Step 7

Route: **Step 2/3 literature and mathematics; do not code or run endpoint experiments yet.**

Next bounded actions, in order:

1. perform equation-level collision audits for the fixed-path feasibility-boundary rule (C12/C13),
   including exact Grassmann line-search and geometric subspace-update literature;
2. freeze one concrete C16 computation graph (basis source, expansion order, stopping rule,
   exact audit and fallback) and decide whether it has any theorem-level delta beyond
   Davidson/Jacobi--Davidson/LOBPCG/recycling;
3. choose one implementable, outward-safe Ky Fan upper-enclosure mechanism for C20 or retire it;
4. create new full math cards only for genuinely distinct mechanisms discovered by that audit;
5. rerun independent verification. If the pool remains below about twenty, retain the shortfall
   and park the novelty branch instead of manufacturing method names.

Overall project status remains `continuation_pending`; this B10 negative gate does not invalidate
B01--B09 experiments and does not close the broader research task.

