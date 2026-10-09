# Minimum-recourse feasible refresh candidate

Status: **assignment 186 mathematical method candidate, corrected after the
assignment-187 `CORRECT_AND_REREVIEW` verdict; assignment 188 re-review,
originality, selection, and code admission pending**.

This card uses the obstruction accepted in assignments 183--184 to change the
algorithm rather than continue trying to force an unweighted bound from a
vanishing cutoff gap.  It is not code, a complete experiment design, a theorem
repair, or permission to execute Stage B.

## Source-bound problem

Algorithm 1 of Woodruff and Zhou, *Consistent Low-Rank Approximation* (ICLR
2026), defines `RECLUSTER` as an exact truncated SVD.  In the HEAVY branch of
Algorithm 2, an approximation failure calls that exact `RECLUSTER`, even when
many almost-equivalent rank-\(k\) projectors meet the desired relative error:

<https://proceedings.iclr.cc/paper_files/paper/2026/file/b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf>

Assignments 183--184 prove that old-covariance regret only controls
gap-weighted movement.  The resulting design question is therefore:

> At a refresh, why jump to the exact optimum if a closer projector already
> restores the required approximation margin?

## Formal object

Let \(C=A_{1:t}^{\mathsf T}A_{1:t}\succeq0\), let \(P\) be the current
rank-\(k\) projector, and write

\[
L_C(Q)=\operatorname{tr}((I-Q)C),\qquad
\operatorname{OPT}(C)=\min_{\operatorname{rank}Q=k}L_C(Q).
\]

Choose two prospective hysteresis levels
\(0<\rho_{\rm lo}<\rho_{\rm hi}\).  Keep \(P\) until

\[
L_C(P)>(1+\rho_{\rm hi})\operatorname{OPT}(C).
\]

At a trigger, replace exact `RECLUSTER` by the **minimum-recourse feasible
refresh**

\[
\boxed{
Q^{\rm MR} \in \arg\min_{\substack{Q=Q^2=Q^{\mathsf T}\\
                                   \operatorname{tr}Q=k}}
       \|Q-P\|_F^2
\quad\text{s.t.}\quad
L_C(Q)\leq(1+\rho_{\rm lo})\operatorname{OPT}(C).}
\tag{1}
\]

The lower target restores a margin before the next trigger.  The relative rule
requires positive OPT; the project's separately frozen near-zero-OPT rule remains
necessary and is not replaced by (1).

## Immediate guarantees

The feasible set is nonempty because every exact top-\(k\) projector is feasible,
and it is compact, so a minimizer exists.  Let \(Q^*\) be the exact-SVD refresh.
Then directly from (1),

\[
L_C(Q^{\rm MR})\leq(1+\rho_{\rm lo})\operatorname{OPT}(C),
\qquad
\|Q^{\rm MR}-P\|_F^2\leq\|Q^*-P\|_F^2.
\tag{2}
\]

Thus the candidate weakly dominates exact `RECLUSTER` in **the current
refresh's** movement at the declared accuracy.  Equation (2) does not compare
future trajectories, because selecting a different projector changes later
trigger times and feasible sets.

## Spectral solution path

Since equal-rank projector distance is
\(2k-2\operatorname{tr}(PQ)\), define the required captured energy

\[
\beta=\operatorname{tr}C-(1+\rho_{\rm lo})\operatorname{OPT}(C).
\]

Problem (1) is equivalent to maximizing \(\operatorname{tr}(PQ)\) subject to
\(\operatorname{tr}(CQ)\geq\beta\).  For \(\lambda\geq0\), define

\[
Q_\lambda\in\arg\max_{\operatorname{rank}Q=k}
\operatorname{tr}((P+\lambda C)Q).
\tag{3}
\]

By the Ky Fan maximum principle, (3) is a top-\(k\) eigenspace of
\(P+\lambda C\).  If \(c(\lambda)=\operatorname{tr}(CQ_\lambda)\), then
captured energy is nondecreasing for every pair of scalarized maximizers at
distinct parameters.  Indeed, optimality at
\(0\leq\lambda_1<\lambda_2\) gives

\[
o_1+\lambda_1c_1\geq o_2+\lambda_1c_2,
\qquad
o_2+\lambda_2c_2\geq o_1+\lambda_2c_1,
\]

where \(o_i=\operatorname{tr}(P Q_{\lambda_i})\).  Adding them yields

\[
(\lambda_2-\lambda_1)(c_2-c_1)\geq0.
\tag{4}
\]

The global scalarization requires a complex enlargement followed by a real
recovery; the analogous set made only from real projectors is not convex in
general.  Temporarily allow complex Hermitian rank-\(k\) projectors.  The
complex \(k\)-numerical range of \(P+iC\), equivalently the set of pairs
\((\operatorname{tr}(PQ),\operatorname{tr}(CQ))\), is convex.  An exact
top-\(k\) projector of \(C\) is strictly feasible because
\(\rho_{\rm lo}>0\) and \(\operatorname{OPT}(C)>0\).  A supporting-line/KKT
argument therefore supplies some \(\lambda_*\geq0\), and every scalarized
maximizer is a top-\(k\) projector of \(M=P+\lambda_*C\).

It remains to recover a real optimizer.  The matrix \(M\) is real symmetric.
Let \(E_>\) contain its eigenspaces strictly above the rank-\(k\) cutoff and
let \(E_=\) be the real cutoff eigenspace.  Every scalarized maximizer contains
\(E_>\) and selects an \(r\)-dimensional subspace of \(E_=\).  On that cutoff
space,

\[
P_{E_=}+\lambda_* C_{E_=}=\mu I.
\]

The values \(\operatorname{tr}(C_{E_=}R)\) over real rank-\(r\) projectors
\(R\) fill the interval between their Ky Fan minimum and maximum: the extrema
are attained by real eigenspaces, and every intermediate value follows by
continuity on the connected real Grassmannian (the endpoint cases are
trivial).  Hence one can choose a real cutoff subspace with the boundary
captured energy; the affine identity above gives the matching overlap.  If
\(\lambda_*=0\), then either the old projector is already feasible or the
full-rank case is trivial.

This proves existence of a real scalarized optimizer but also identifies a
required implementation detail: at a degenerate cutoff, a naive eigensolver
tie choice is insufficient and the compressed real boundary problem must be
solved explicitly.

Consequently the proposed solver is a one-dimensional search in \(\lambda\),
with a projected cutoff-eigenspace boundary solve at a jump.  A future Step-4
implementation must independently verify this real-projector construction and
its numerical stopping rule before it is called complete.

## Exact near-tie prediction

Use the accepted obstruction family

\[
C=\operatorname{diag}((1+\delta)I_k,(1+2\delta)I_k),
\qquad P=\operatorname{diag}(I_k,0),
\qquad \delta>0.
\]

The exact SVD selects the second block and moves \(2k\).  For any real
rank-\(k\) projector \(Q\), define

\[
s=k-\operatorname{tr}(PQ).
\]

Because \(C=(1+\delta)P+(1+2\delta)(I-P)\),

\[
L_C(Q)=k(1+2\delta)-\delta s,
\quad \operatorname{OPT}(C)=k(1+\delta),
\quad \|Q-P\|_F^2=2s.
\]

Every real \(s\in[0,k]\) is attainable: exchange \(\lfloor s\rfloor\)
coordinate pairs, rotate one additional pair through an angle \(\theta\) with
\(\sin^2\theta=s-\lfloor s\rfloor\), and leave the rest unchanged.  Thus the
exact constrained optimum is

\[
\boxed{
s_{\min}=k\left(1-\frac{\rho_{\rm lo}(1+\delta)}{\delta}\right)_+,
\qquad \|Q^{\rm MR}-P\|_F^2=2s_{\min}.}
\tag{5}
\]

When \(\rho_{\rm lo}\geq\delta/(1+\delta)\), the old projector is already
feasible and movement is zero.  This family actually triggers the proposed
refresh only when

\[
\frac{\delta}{1+\delta}>\rho_{\rm hi}.
\]

Conditional on that trigger, (5) can still move strictly less than the exact
SVD because \(\rho_{\rm lo}<\rho_{\rm hi}\); the saving is continuous rather
than restricted to whole-direction exchanges.  When
\(\delta\gg\rho_{\rm lo}\), the advantage vanishes and the method approaches
exact refresh.  This is a specific spectral-regime prediction, not a claim of
uniform improvement.

## Predictions, controls, and falsifiers

1. **Prediction:** movement reduction concentrates at triggers with a dense
   near-cutoff spectrum and small relative loss excess.  Large-gap triggers should
   show little or no reduction.
2. **Mechanism control:** compare the same trigger stream using exact SVD versus
   (1), with identical \(\rho_{\rm hi}\); sweep only the frozen
   \(\rho_{\rm lo}\) hysteresis grid in development.  Record both the spectral
   band occupancy and the number of partially replaced directions.
3. **Trajectory control:** a per-trigger win is insufficient.  The full prefix
   comparison must retain later trigger counts, cumulative projector recourse,
   raw loss/OPT, and solver/update/scoring time.
4. **Falsifier:** reject the mechanism if the independently verified constrained
   solution usually equals exact SVD at consequential triggers, violates the
   target due to numerical/tie handling, or merely shifts movement to later
   prefixes without lowering cumulative recourse at matched accuracy.

## Collision and evidence boundary

The target paper already uses stale projectors, HEAVY/LIGHT casework, and
partial factor replacement.  Saad-Falcon et al., *Subspace Tracking with
Dynamical Models on the Grassmannian* (2024), explicitly regularize adjacent
subspace distance and trade data fit against smooth motion:
<https://arxiv.org/abs/2402.10352>.  A targeted search also found a 2026 item
titled *Subspace regularized PCA using prior exposure information* whose search
summary describes rotation/turnover regularization, but its primary text was
not accessible in this run; it cannot be treated as resolved evidence.

These are broad mechanism collisions.  The search did not establish that the
exact accuracy-constrained minimum-projector-distance refresh and its
hysteretic use here are new.  Therefore this is a **candidate mechanism with
priority unresolved**, not an originality claim.  It must enter the complete
approximately-20-card pool, primary paper/code collision audit, independent
whole-pool ranking, and method-verification boundary before code generation.

## Six-field card

- **Object:** current rank-\(k\) projector and prefix covariance at a failed
  relative-accuracy trigger.
- **Assumptions:** exact or independently qualified OPT during development;
  positive-OPT relative regime; fixed rank; stable real symmetric eigensolver.
- **Derivation:** constrained movement problem (1), pairwise dominance (2),
  spectral scalarization (3)--(4), and exact near-tie law (5).
- **Constructed method:** hysteretic trigger plus minimum-recourse feasible
  refresh, solved along the top-\(k\) path of \(P+\lambda C\) with explicit
  cutoff-degeneracy handling.
- **Prediction:** large benefit only when the cutoff is dense and the old output
  barely violates the target; no material benefit in large-gap regimes.
- **Falsifier:** invalid boundary solution, no cumulative gain at matched loss,
  or a substantive collision showing the same mechanism and claim already known.

## Required independent re-review (assignment 188)

Review the corrected exact candidate bytes while preserving assignment 187 as
the audit trail.  Check the complex scalarization and real cutoff recovery,
monotonicity, continuous near-tie law and trigger condition, and every
originality/admission boundary.  Return `ACCEPT_CANDIDATE_MATH`,
`CORRECT_AND_REREVIEW`, or `REJECT`.  Acceptance does not establish originality,
select the method, or authorize Step 4/5.
