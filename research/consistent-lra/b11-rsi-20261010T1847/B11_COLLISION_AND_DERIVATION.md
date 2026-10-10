# B11 collision closure for C12/C13/C16/C20

Date: 2026-10-10

Status: mathematical and source audit; no new-method code authorization.

## 1. Fixed objects

Let (G=A^\top A\succeq0), (P_0) be the previously emitted rank-(k)
projector, (E(P)=\operatorname{tr}(PG)), and
(D(P,P_0)=k-\operatorname{tr}(PP_0)). Feasibility is
(E(P)\ge T:=\operatorname{tr}G-(1+\eta)\mathrm{OPT}).

## 2. C12: exact formula, but only a fixed-plane policy

For (w(\theta)=v\cos\theta+u\sin\theta), (u\perp V), define
(a=v^\top Gv,b=v^\top Gu,c=u^\top Gu). The varying captured energy is

\[
q(\theta)=m+\rho\cos(2\theta-\phi),\quad
m=(a+c)/2,\quad \rho=\sqrt{((a-c)/2)^2+b^2},
\quad\phi=\operatorname{atan2}(b,(a-c)/2).
\]

Every boundary root in the principal projector interval is therefore

\[
\theta=\tfrac12\left[\phi\pm\arccos((T'-m)/\rho)+2\pi n\right],
\qquad \theta\in[-\pi/2,\pi/2],
\]

where (T') subtracts the unchanged captured energy. Enumerating all roots and
choosing the one with smallest (\sin^2\theta) is the minimum recourse only on
that already chosen plane. Multiple roots are normal, so a one-sided "first
root" rule remains incorrect.

This root does not define a new search direction. GROUSE already supplies the
rank-one Grassmann geodesic update, and Alimisis--Saad--Vandereycken give an
accurate exact line search for the symmetric eigenspace objective. Replacing the
line-search optimum by the first certified threshold crossing is an acceptance
truncation of that known path.

Disposition: C12 is a useful path policy/ablation, not a structurally independent
method candidate. Its only proven minimum is fixed-plane minimum recourse.

## 3. C12/C13 collapse into the restricted overlap family

Fix any orthonormal search basis (S\in\mathbb R^{d\times m}), and write
(P=SYY^\top S^\top), (Y^\top Y=I_k). Put

\[
H=S^\top GS,\qquad J=S^\top P_0S.
\]

The globally best endpoint *inside this fixed search space* solves

\[
\max_Y\ \operatorname{tr}(Y^\top JY)
\quad\text{s.t.}\quad
\operatorname{tr}(Y^\top HY)\ge T.
\tag{R}
\]

At a supported boundary point, the KKT scalarization is

\[
\max_{Y^\top Y=I_k}\operatorname{tr}\{Y^\top(H+\mu J)Y\},
\]

so (Y) is the top-(k) eigenspace of (H+\mu J). This is precisely C14 plus
C15's parameter search: restricted overlap-regularized Rayleigh--Ritz. For the
one-plane C12 case the numerical range is an ellipse, hence every Pareto boundary
point is supported and the reduction is exact. C13 either:

1. claims the minimum-recourse endpoint in its (2q) block, in which case it is
   the same restricted penalized family; or
2. restricts itself to a prescribed residual geodesic, in which case it is a
   path heuristic and must enumerate a generally non-monotone scalar boundary.

The ambient objective (G+\mu P_0) is already the core of Hara--Yoshida's
Consistent PCA. Restriction to a residual block and a threshold stopping wrapper
do not create a distinct mathematical family.

Disposition: C13 is not an independent generalization of C12. Both move to the
attributed restricted Consistent-PCA/control family; any remaining claim must be
an empirical engineering claim, not method novelty.

## 4. C16 frozen computation graph

The only unambiguous C16 graph is:

1. (Q_0=V_{t-1}).
2. Rayleigh--Ritz: take top-(k) Ritz pairs of (Q_j^\top GQ_j).
3. Form block residual (R_j=GX_j-X_j\Theta_j).
4. Expand (Q_{j+1}=\operatorname{orth}[Q_j,R_j]).
5. Accept only after the external feasibility audit; otherwise repeat to a
   frozen dimension cap and fall back to the exact cached-Gram eigensolve.

Steps 2--4 are the unpreconditioned block-Davidson/residual-correction graph.
LOBPCG uses Rayleigh--Ritz on the current approximation, residual/preconditioned
residual and previous direction; Jacobi--Davidson changes the correction
equation but retains residual-driven subspace expansion and extraction. Step 5
is a project-specific stopping/audit wrapper. It can be benchmarked as an
engineering pipeline, but no distinct algorithmic operation remains.

Disposition: freeze C16 as a known-method engineering comparator, not a new
candidate. C11/C17/C18/C19 remain its first-step or basis-policy ablations.

## 5. C20 is already B07's FD certificate

For a classical width-(\ell) Frequent Directions sketch (B) with cumulative
shrinkage (\Delta),

\[
G\preceq B^\top B+\Delta I
\quad\Longrightarrow\quad
\sum_{i=1}^k\lambda_i(G)
\le \sum_{i=1}^k\lambda_i(B^\top B)+k\Delta=:U.
\]

Since (\operatorname{tr}G=\operatorname{tr}(B^\top B)+\ell\Delta),

\[
L=\operatorname{tr}G-U
=\operatorname{tail}_k(B^\top B)+(\ell-k)\Delta\le\mathrm{OPT}.
\]

This is exactly the lower-bound form already derived, implemented and audited in
B07 (with the documented 
(\ell+1-k) coefficient for the author's append-then-shrink capacity convention)
and then tested end-to-end in B08/B09. B09 found no speed advantage against the
strong cached-Gram query baseline.

Disposition: retire C20 as a new candidate. It is the existing FD certificate
component with preserved B07--B09 negative timing evidence.

## 6. Source-level collision evidence

- Woodruff--Zhou, *Consistent Low-Rank Approximation*, ICLR 2026, Algorithm 3:
  exact OPT checks, partial replacement of bottom directions, and full
  reclustering are prior problem mechanisms. Official code
  `samsonzhou/consistent-LRA@d607c4f...` refreshes by randomized/full SVD and does
  not implement C12's boundary root.
- Alimisis, Saad, Vandereycken, *Gradient-Type Subspace Iteration Methods for the
  Symmetric Eigenvalue Problem*, arXiv:2306.10379 / SIMAX 2024, §3.2 and
  Algorithm 3: safeguarded exact line search for a Grassmann eigenspace update.
- Balzano et al., GROUSE/Oja equivalence, PMLR 151 (2022), Eq. 14 and the
  rank-one sine/cosine geodesic update: C12's path primitive is prior art.
- Sleijpen--van der Vorst, Jacobi--Davidson (1996), and Knyazev, LOBPCG (2001):
  residual expansion plus Rayleigh--Ritz extraction covers C16's core graph.
- Hara--Yoshida, *Consistent PCA and Spectral Clustering*, AISTATS 2026, Eq. 1--2
  and official `ConsistentPCA.update`: top-(k) of covariance plus scaled prior
  projector covers the penalized parent of C12/C13/C14/C15.

## 7. Gate decision

B10's two unresolved families collapse as follows:

- C12/C13: restricted prior-art/control family or path policy;
- C16: standard eigensolver graph plus audit/fallback;
- C20: duplicate of the already tested FD certificate.

Therefore there are **zero currently surviving structurally distinct new-method
candidates**, not a valid Top-15. The code gate remains NO-GO. This is a candidate
pool failure, not proof that the parent scientific question is unimportant.

Step 7 selects a contextual Step-2/3 restart. The next discovery parent must ask
for a consequential property not obtained by known endpoint solvers plus wrappers:
for example, a theorem linking certified approximation slack to *amortized endpoint
construction cost and cumulative projector recourse* under the native row stream.
Any new pool must exclude solver choice, certificate choice, fallback, parameter
search, and basis policies from the method count unless they change that theorem.
