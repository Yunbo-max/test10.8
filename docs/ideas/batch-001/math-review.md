# Independent semantic mathematics review

Reviewer: independent mathematics role /root/math_review. Date: 2026-10-08.

Scope: all I01–I20 cards in the frozen draft, and all I01–I21 cards in the first revised file. This is a mathematical and comparison-coherence audit. It contains no literature retrieval, priority adjudication, numerical experiment, scientific project execution, model/data download, or machine-verification claim.

Reviewed artifacts:

- Frozen draft: /workspace/scratch/9151f4814af1/research/math-ideas-draft.md; SHA-256 b358299a6dd9a33e949b4dae2884da6506a31e7f9ec68938b0ec824f58f90b31.
- First revised file: /workspace/scratch/9151f4814af1/research/math-ideas-reviewed.md; SHA-256 5dfd8ddeefca13c869c11f4fffb72a30645a0583843becc33ba2b8922503f4d5.

The second file already repairs the original I05 quantifier, I06 variance model and missing factor, I15 local-KL factor/remainder, I20 projection dimensions, and I02/I18 finite-dual boundary qualifications. Those repairs are mathematically appropriate. Further corrections below refer to what remains in that exact reviewed version. A later changed file needs a bounded rereview of its changes.

## Overall mathematical finding

The cards contain useful exact identities and valid conditional arguments. They do not establish twenty or twenty-one independent new algorithms. The strongest remaining issues are scope and predictions rather than a wholesale algebraic failure:

1. I01 needs aligned pairwise output spaces, a target-dependent singular-value prediction, and explicit separation of linearized infeasibility from finite nonlinear infeasibility.
2. I04 needs positive-weight support in the kernel identity and must allow that retiring a row releases no useful direction.
3. I06's repaired posterior-variance derivation is sound, but its claimed disappearance under random directions/uniform coverage does not follow.
4. I14's bounded weights require a mixture of complete trajectory distributions or normalized prefix distributions; tokenwise mixing is a different proposal.
5. I18 needs explicit nonnegative dual variables, coupled calibration, and a genuine mathematical prediction/falsifier. Its teacher gain is a Jeffreys divergence under the stated full-distribution interpretation.
6. I19 must distinguish conditional pointwise Bayes risk from average Bayes risk and fix the escaped tilde notation.
7. I20 needs feature compatibility as well as low rank. A finite difference of two rank-r LoRA products can have rank 2r.
8. I21 needs a batch-covariance convention, feasible positive counts, cost-aware allocation, a remainder condition valid on sampled steps, and a prediction involving Fisher mean damage rather than only gradient cosine.

Exact identities below are exact in their declared mathematical model. Local approximations, neural representability, unknown-data coverage, native scorer implications and empirical benefits remain conditional or pending. Named nearest alternatives are reviewed only for conceptual coherence; whether those sources actually contain a mechanism is left to the independent source roles.

## Shared conventions and proof obligations

Use $d$ for the full parameter dimension. Jacobian rows are gradients of aligned scalar output contrasts. If $J_H\in\mathbb R^{m_H\times d}$ and $J_C\in\mathbb R^{m_C\times d}$, their subtraction is legal only after choosing the same number and meaning of output coordinates. Extra G/H protection rows may be stacked separately.

For a scalar/vector output $f$, a finite remainder bound of order $\|\delta\|^2$ requires a Hessian bound on the segment from $\theta_0$ to $\theta_0+\delta$, not merely a derivative at $\theta_0$. A cubic KL remainder requires an appropriate third-derivative bound, or a separately justified dominated asymptotic argument. Write its domain/radius and constant explicitly.

For a fixed valid input/prefix measure $\nu$,

$$
D_V(\delta)=\mathbb E_\nu \mathrm{KL}(p_{\theta_0}\|p_{\theta_0+\delta})
=\tfrac12\delta^\top F_V\delta+R_3(\delta).
$$

$F_V$ is the Hessian of this actual fixed-measure KL at the reference. It is PSD. It is not automatically the outer product of gradients of empirical gold-label loss. In logit coordinates its pullback is $J^\top[\mathrm{diag}(p_0)-p_0p_0^\top]J$, averaged under the specified measure. If adapter parameters are used, the corresponding Fisher/Jacobians must be pulled back to those same coordinates.

Euclidean parameter norms, SVDs, projections and norm bounds depend on the chosen parameterization and output-contrast scaling. They are valid diagnostics in frozen coordinates, rather than invariant measures of ability.

An exact zero update on every changed deterministic module's baseline input implies, by forward induction, an unchanged baseline trace. This applies to the protected traces, not automatically every unseen input or all autoregressive prefixes. A claimed failure of an exact full-trace construction must identify an approximation, an unprotected operator, a changed measure, or a genuinely different constraint.

The operation IDs are navigation labels, not proofs. In particular, I20's Eckart–Young argument is a spectral best-approximation theorem, rather than the specific identity-plus-low-rank product operation F04; I13's triangle/Minkowski argument does not prove a contraction under G03. Retain the actual argument even if the operation label is changed.

## I01 — Time distinguishability and the cost of preservation

**Formal object.** $J_H\delta=0$, $J_C\delta=r$ in a frozen linear output model. $N\in\mathbb R^{d\times k}$ has orthonormal columns spanning $\ker J_H$, and $A=J_CN$.

**Operations and conditions.** Nullspace elimination is valid exactly for the stated linear constraints. Moore–Penrose reconstruction is valid for rank-deficient $A$; exact feasibility requires $r\in\mathrm{range}(A)$. A local Taylor interpretation additionally requires a bounded nonlinear remainder.

**Derivation.** $\delta^*=NA^\dagger r$ and

$$
\|\delta^*\|^2=\sum_{\sigma_j>0}\frac{(u_j^\top r)^2}{\sigma_j^2}
$$

are correct. For an aligned current/history pair with $J_H^{\rm pair}\delta=0$, $J_C^{\rm pair}\delta=(J_C^{\rm pair}-J_H^{\rm pair})\delta$ yields the norm lower bound correctly. Subtracting an entire history/G stack from a smaller current Jacobian is dimensionally invalid.

**Assumptions and exact correction.** State “infeasible in the linearized model” when the denominator is zero. Equal Jacobians at one point do not imply equal nonlinear functions or finite-update impossibility. If actual finite changes obey $\Delta f_C=r$, $\Delta f_H=0$ and remainder norms are at most $L_C\|\delta\|^2/2$ and $L_H\|\delta\|^2/2$, then the valid finite necessary condition is

$$
\|r\|\le \|J_C^{\rm pair}-J_H^{\rm pair}\|_{\rm op}\|\delta\|
+\tfrac12(L_C+L_H)\|\delta\|^2.
$$

Protecting a richer stack can only further reduce the linear reachable set.

**Executable expression.** The range test, pseudoinverse minimum-norm step, and a trust-radius/remainder feasibility check form an executable diagnostic in a declared low-dimensional parameterization. Approximate JVP/SVD computation needs a residual/approximation bound before being called a certificate.

**Prediction/falsifier correction.** Small singular values increase the minimum norm only when the desired $r$ has nonzero components along their left singular vectors. Greater historical interference is not a consequence of small singular values alone: an exactly linear model can have a large protected update with zero historical change. Replace the current prediction with: “For fixed aligned $r$, weak required modes increase the minimum step; finite historical leakage may then increase if the relevant curvature is nonzero and controlled.” A measured violation must account for target residual, protection residual, Jacobian error and nonlinear remainder.

**Closest alternative/comparison.** Nullspace editing, time-conditioned inputs, ordinary time replay and retrieval are conceptually coherent alternatives. Share time information, available labels and target output changes. Compare the actual target-weighted norm prediction with a simpler activation/gradient diagnostic; “a small singular value exists” is not the decisive predictor.

**Status.** Linear algebra exact. Finite neural preservation and the interference prediction conditional. I07 is a parameterization branch of this card.

## I02 — Separate obsolete, replacement and other output events

**Formal object.** $O,N,U$ must be a disjoint, exhaustive partition of one common outcome space. The base masses are strictly positive. Minimize $\mathrm{KL}(q\|p_0)$ subject to $q_O\le\epsilon$ and $q_N\ge a$.

**Operations and conditions.** KL coarse-graining plus conditional decomposition is exact, with zero-mass conditional terms interpreted by convention. Strict convexity makes the feasible minimizer unique. A finite exponential solution requires the interior conditions already added in the revised file; boundary cases use limits/restricted support.

**Derivation.** The group conditional distributions are preserved at the optimum whenever the group has positive optimized mass. The signs in

$$
q_g\propto p_0(g)\exp[-\lambda_O1\{g=O\}+\lambda_N1\{g=N\}]
$$

are correct, with $\lambda_O,\lambda_N\ge0$ and complementary slackness. In the nondegenerate both-active case, put $b=1-\epsilon-a>0$. Then

$$
\lambda_O=\log\frac{o_0b}{u_0\epsilon},\qquad
\lambda_N=\log\frac{a u_0}{n_0b}.
$$

Both must be nonnegative. Thus the finite both-active formula needs $\epsilon,a,b>0$, not merely $\epsilon+a\le1$.

**Assumptions and exact correction.** Specify $0\le\epsilon\le1$, $0\le a\le1$. The two inequalities are generally feasible without $\epsilon+a\le1$ because they do not force $q_O=\epsilon$; that sum condition belongs only to the proposed both-active solution. At $\epsilon+a=1$ the listed vector has $q_U=0$ and cannot be obtained by finite multipliers with $u_0>0$. For ordinary positive $\epsilon$ and $a<1$, such a both-active boundary will not be the optimum: reducing $q_O$ can free positive $U$ mass. The revised general boundary warning is helpful; make this local branch condition explicit.

**Executable expression.** Use the KKT solution and active-set checks. Zero active constraints give $q=p_0$. If only O is active, distribute $1-\epsilon$ proportionally across N/U and check the N lower bound. If only N is active, distribute $1-a$ proportionally across O/U and check the O upper bound. Fit any student to the resulting target separately; a distributional optimum does not guarantee neural realization.

**Prediction/falsifier correction.** The explicit guarantee is $q_O/q_N\le\epsilon/a$ for $a>0$, not unrestricted independent control: normalization couples all masses. Preserve conditional U behavior, while admitting that total U mass changes. Equal student performance does not refute the distributional identity; it can refute the practical need for its construction.

**Closest alternative/comparison.** Positive replacement training plus obsolete-answer suppression and valid-query retention is coherent. Both alternatives need the same event definitions and current labels. This is the same broad I-projection machinery as I18.

**Status.** Exact probability-space result under branch/support conditions; student behavior conditional. Retain as an attributed comparator if source review establishes coverage.

## I03 — Forgetting an answer does not imply learning its replacement

**Formal object.** $u=\nabla\log p(O|x)$ and $v=\nabla\log p(N|x)$ exist where both event probabilities are positive; $P=P^\top=P^2$ projects onto the declared protection kernel.

**Operations and conditions.** An audit of the actual projected update followed by a first-order Taylor expansion is appropriate. The counterexample requires no numerical experiment.

**Derivation.** For $\delta=-\eta Pu$,

$$
\Delta\log p(O)=-\eta\|Pu\|^2+O(\eta^2),\qquad
\Delta\log p(N)=-\eta v^\top Pu+O(\eta^2).
$$

The signs are correct. In the scalar example, declare O to be logit $2w$, N to be logit $w$, and $P=1$. At $w=-1$, the average slope

$$
\bar s=\frac{2e^{-2}+e^{-1}}{e^{-2}+e^{-1}+1}<1,
$$

so $u=2-\bar s>0$ and $v=1-\bar s>0$.

**Assumptions/correction.** “Both decrease” means for sufficiently small positive $\eta$ when the leading coefficients are nonzero and the remainder is bounded. A safer expression than “$\le O(\eta^2)$” is a signed leading term plus an absolute remainder bound. “Safe” denotes first-order safety on the observed protected rows.

**Executable expression.** The stated convex QP is well-defined for $\kappa,\gamma>0$. If $Pu=0$ or $Pv=0$, its respective positive requirement is infeasible. If $Pv=cPu$ with $c>0$, suppression and promotion are incompatible. Positive inner product alone does not imply infeasibility; independent projected vectors can satisfy both constraints.

**Prediction/falsifier.** The replacement's infinitesimal change is governed by $-v^\top Pu$. A small-step comparison with a remainder estimate can challenge the modeled sign; a long NPO trajectory cannot test this one-step identity directly.

**Closest alternative/comparison.** A suppression-only step, positive replacement SFT, and their constrained combination distinguish the mechanism. Share labels and valid-query constraints. The QP is an inequality version of I01's general constraint geometry.

**Status.** Local derivative result and analytic counterexample sound. No implication about prevalence or complete optimizer trajectories.

## I04 — Retire the current role and preserve the historical role

**Formal object.** $C_V=\sum_{i\in V}w_i a_i a_i^\top$ is a PSD Gram sum in a single declared vector space. A full-parameter Jacobian feature and an input-activation feature cannot be added to one Gram unless dimensions and meaning coincide.

**Operations and conditions.** Provenance-backed sufficient statistics permit exact deletion of terms. Exact nullspace relations follow from nonnegative weights. Feature refresh/estimation is a separate error term.

**Derivation.** For any $v$, $v^\top C_Vv=\sum_iw_i(a_i^\top v)^2$. Therefore

$$
\ker C_V=\bigcap_{i:w_i>0}\ker(a_i^\top).
$$

The draft's kernel identity must exclude zero-weight rows. Removing a genuinely present term leaves a PSD sum and weakly enlarges the kernel; adding a historical term weakly shrinks it.

**Assumptions/correction.** Replace “can release replacement directions while retaining history” with a conditional statement. A retired row may be redundant, the released directions may not affect current outputs, and the added historical row may remove all useful release. The updated set need not be compatible with the new target. Floating-point downdates also need their own numerical residuals.

**Executable expression.** Maintain source IDs, role/valid interval, weight, and the exact term or sufficient removal data; compute $P_{\ker C_V}b$ or a declared soft quadratic budget. The data needed to identify obsolete current roles cannot be assumed to emerge from new samples alone.

**Prediction/falsifier.** Predict a change in the effective reachable set or target-conditioned minimum cost only when retired and historical rows change the relevant span. Compare no retirement, indiscriminate deletion, and role-aware substitution. A case with identical old/new spans is a predicted null regime, not a refutation.

**Closest alternative/comparison.** Time-labeled replay/retrieval and refreshed protection bases are coherent alternatives. They must share the same time annotations and old source records. A simple temporal replay result can remove the need for this extra statistic.

**Status.** Gram/downdate algebra exact. Correct role labeling, useful released capacity and nonlinear capability retention conditional. This is a semantic change in I01's constraint set, not a new projection identity.

## I05 — What finite protection information can guarantee

**Formal object.** $A\in\mathbb R^{m\times d}$ contains observed scalar contrast gradients; the allowed old feature family includes every unit vector used by the adversarial argument.

**Operations and conditions.** The nullspace counterexample and the empirical-to-population distinction are coherent. It is a conditional linear-function impossibility result.

**Derivation.** If $\mathrm{rank}(A)<d$, choose unit $v\in\ker A$ and $\delta=sv$. Then $A\delta=0$ but $v^\top\delta=s$. Cauchy–Schwarz gives the exact dual-norm identity

$$
\sup_{\|a\|\le1}|a^\top\delta|=\|\delta\|.
$$

The revised quantifier is correct:

$$
\big[A\delta=0\Longrightarrow a^\top\delta=0\ \forall a\in S\big]
\quad\text{for every }\delta
\iff S\subseteq\mathrm{rowspan}(A).
$$

Consequently $\mathrm{rank}(A)\ge\dim S$ is necessary for this particular automatic certification mechanism.

**Assumptions.** The true LLM query Jacobians need not fill the unit ball. Without a realizable missed query/feature, this is not a theorem about all language tasks. It is not a lower bound on all algorithms that inspect parameters, use additional structure, or choose only a smaller family of updates.

**Executable expression.** The coverage/rank test and an explicit norm cap $\|\delta\|\le b$ are valid linear diagnostics; the latter bounds all allowed unit-feature drifts by $b$. If features are norm bounded by L instead, the bound is $L\|\delta\|$.

**Prediction/falsifier.** Additional samples that repeat the same functional span cannot close the worst-case certificate gap. Good empirical retention on finitely many native cases does not refute the adversarial theorem. Proven feature restrictions or coverage can remove its applicability.

**Closest alternative/comparison.** Equal-information calibration versus genuinely broader calibration tests the coverage question. Never grant the candidate native test labels/directions absent from comparators. The statement can motivate an information-access study; it does not yet prove the minimum information needed for a realistic LLM.

**Status.** Correct after the revised quantifier repair. Exact in the allowed linear feature model; true capability generalization unresolved.

## I06 — Direction-aware calibration design

**Formal object.** Use a distinct unknown linear coefficient vector, say $\beta$, in observations $y_i=a_i^\top\beta+\xi_i$. The fixed direction $\delta$ defines the scalar target $\delta^\top\beta$. Nonnegative w is repetition count or relative observation precision; $M=\lambda I+\sum_iw_i a_ia_i^\top$.

**Operations and conditions.** Inverse-matrix differentiation and Sherman–Morrison are valid when M is SPD. Gaussian conjugacy or full-rank OLS supplies the variance interpretation. The revised file now supplies the needed statistical model.

**Derivation.** Under prior precision $(\lambda/\sigma^2)I$, posterior covariance is $\sigma^2M^{-1}$, and

$$
\partial_{w_i}\{\sigma^2\delta^\top M^{-1}\delta\}
=-\sigma^2(a_i^\top M^{-1}\delta)^2.
$$

Increasing one row's precision by $\alpha>0$ lowers that variance by

$$
\frac{\sigma^2\alpha(\delta^\top M^{-1}a_i)^2}
{1+\alpha a_i^\top M^{-1}a_i}.
$$

The revised unit-precision formula is correct. For fixed-parameter frequentist ridge, with information $Q=\sum_iw_i a_ia_i^\top$, the covariance is $\sigma^2M^{-1}QM^{-1}$ under the corresponding repeated/precision observation convention, and the bias is $-\lambda M^{-1}\beta$ (zero prior center). The original $M^{-1}$ variance claim was wrong in that interpretation.

**Assumptions.** $\lambda>0$ corresponds to a proper prior; $\lambda=0$ requires enough information for an invertible OLS problem. If weights merely reweight fixed observations rather than encode precision/repetition, their covariance changes and must be derived separately. Fixed δ is part of the design problem.

**Executable expression.** Choose the row with largest displayed marginal variance reduction per declared acquisition cost, then update M. This is an exact classical c-optimal/Bayesian design rule under its model, rather than an old-capability certificate.

**Prediction/falsifier correction.** The current assertion that the benefit should disappear for random directions or uniform coverage is unsupported. A known fixed direction can benefit from aligned observations even when M is isotropic. If δ is unknown and isotropically random before the design, the averaged criterion becomes proportional to $\mathrm{tr}(M^{-1})$—an A-optimal design criterion—not “no benefit.” Use the actual leverage/alignment score to predict gains, and compare fixed-known versus unknown/redrawn directions.

**Closest alternative/comparison.** c-optimal design and active replay are conceptually appropriate. Equal sample count may not mean equal cost; row/token acquisition costs must be included. Share the candidate pool and its features.

**Status.** Repaired statistical algebra sound. Remaining null-regime prediction needs correction. Attributed standard design comparator unless a separate scientific residual survives source review.

## I07 — Full parameter feasibility versus adapter tangent feasibility

**Formal object.** $T\in\mathbb R^{d\times k}$ maps an infinitesimal adapter increment to a full-parameter increment. Adapter-safe steps are $\{Tz:J_HTz=0\}$.

**Operations and conditions.** A coordinate pullback and nullspace elimination apply at the same frozen parameter point. No injectivity of T is required for reachability; parameter redundancies do matter for coefficient norms.

**Derivation.** Every adapter-safe full increment lies in $\ker J_H$. Hence

$$
\mathrm{range}(J_CT N_{J_HT})
\subseteq \mathrm{range}(J_C N_{J_H})
$$

is correct. At $B=0$, the differential of $BA$ is $\Delta B\,A$; $\Delta A$ contributes only through later/higher-order terms.

**Assumptions/correction.** A first-order unreachable target may become reachable after changing the tangent point or by finite second-order movement. Training can increase tangent capacity; it does not guarantee monotone inclusion of reachable sets, since A, B and network Jacobians all change. If comparing minimum step costs, $\|Tz\|$ and $\|z\|$ are different unless T is isometric.

**Executable expression.** Pull back the I01 range/residual test to a declared adapter configuration. Choosing rank/modules from that diagnostic is a design branch, not a separate algorithm.

**Prediction/falsifier.** A target outside the initial adapter-safe reachable range is impossible to achieve exactly at first order, while it may be full-parameter feasible. A finite many-step success does not contradict that claim.

**Closest alternative/comparison.** Adapter protection and rank/module choices are coherent; compare with the same information and parameter/compute budget. Larger rank alone does not isolate the diagnostic's value.

**Status.** Correct local parameterization branch. Merge with I01 for independent hypothesis counting.

## I08 — The finite LoRA factor-product term

**Formal object.** $B\in\mathbb R^{m\times r}$, $A\in\mathbb R^{r\times n}$, and fixed protected inputs $K\in\mathbb R^{n\times s}$; a LoRA scaling factor is absorbed into the definition or must multiply every term.

**Operations and conditions.** This is an exact finite polynomial identity, not just a Taylor approximation. A submultiplicative matrix norm supplies the residual bound.

**Derivation.** $\Delta W=B\Delta A+\Delta B A+\Delta B\Delta A$ is exact. Under the stated tangent constraint,

$$
\Delta WK=\Delta B\Delta A K,\qquad
\|\Delta WK\|_F\le\|\Delta B\|_{\rm op}\|\Delta A K\|_F.
$$

The same style of bound holds for compatible operator norms. If $A=C N^\top$ for a fixed N with $N^\top K=0$, both initial and final products annihilate K exactly, for arbitrary finite B/C changes.

**Assumptions/correction.** An $\eta^2$ leading term requires nonzero first-order changes in both factors and a nonzero product coefficient. At zero-B initialization, ordinary simultaneous SGD has zero initial A gradient, so the first step need not display this term. Fixed K and fixed N are essential.

**Executable expression.** Compute/audit the exact finite layer residual versus its tangent prediction. The structural right-nullspace construction is a resolving comparator, not a new proposal here.

**Prediction/falsifier.** Where the product coefficient is nonzero, tangent-only layer leakage has second-order scale; where an exact fixed basis annihilates K, this specific leakage vanishes. Remaining drift must be assigned to a violated condition or another mechanism.

**Closest alternative/comparison.** Tangent-only protection versus structural finite protection is decisive for this term. All changing modules protected exactly on the same baseline trace eliminate the upstream mechanism too.

**Status.** Exact layer identity and bound. The observed neural drift coefficient and generality are conditional. Do not claim every LoRA step or exact structural method necessarily leaks.

## I09 — Transport from changed upstream representations

**Formal object.** $W,X\in\mathbb R^{m\times n}$ and $K,D\in\mathbb R^{n\times s}$. K is the baseline input batch and D its actual upstream change.

**Operations and conditions.** The finite layer error decomposition is exact. Linear matrix-equation elimination has a standard rowspace consistency condition.

**Derivation.** The three terms $XK+WD+XD$ are correct. The equation $XK=-WD$ is feasible iff

$$
WD=WDK^\dagger K.
$$

The unique minimum-Frobenius-norm solution is $X^*=-WDK^\dagger$, and all solutions add $Z(I-KK^\dagger)$.

**Assumptions/correction.** Specify the Frobenius norm. With $D=O(\eta)$, $X^*=O(\eta)$ needs a fixed bounded pseudoinverse and bounded W; poor conditioning can make the compensator too large for a local argument. Then $XD=O(\eta^2)$. The finite exact compensation equation is instead $X(K+D)=-WD$, with its own compatibility condition. The first-order compensator is not an exact finite solver.

**Executable expression.** The displayed pseudoinverse compensator is an executable local diagnostic/construction when D can be observed. It does not ensure compatibility with the new target; simultaneous new-output constraints need a joint feasibility check.

**Prediction/falsifier correction.** $WD$ predicts the first-order change at this layer when $XK=0$. To claim a final-logit contribution, include the downstream Jacobian: $\Delta z\approx J_{z\leftarrow y}WD$, plus other changing-layer contributions. Cancellations can prevent the term from dominating final scores. In an exact all-module baseline-trace protection control, D is zero by induction and this mechanism disappears.

**Closest alternative/comparison.** Refreshing features, replay and a local compensator are coherent controls if they share old samples and upstream access. Attribution to this term requires measuring it rather than merely seeing a retention loss.

**Status.** Exact decomposition/linear solution; small compensator and whole-network explanatory dominance conditional.

## I10 — Protect the actual optimizer step

**Formal object.** $g\in\mathbb R^d$, $A\in\mathbb R^{m\times d}$, $M\succ0$, and $\eta>0$. M and g are frozen for the one-step quadratic program.

**Operations and conditions.** Strict convexity and KKT yield a unique primal solution; dependent rows of A are handled by the pseudoinverse. This is standard constrained metric optimization.

**Derivation.** The formula

$$
\delta^*=-\eta\left[M^{-1}-M^{-1}A^\top(AM^{-1}A^\top)^\dagger AM^{-1}\right]g
$$

is correct and satisfies $A\delta^*=0$. It can also be written $-\eta M^{-1/2}P_{\ker(AM^{-1/2})}M^{-1/2}g$.

**Assumptions/correction.** A noncommuting symmetric preconditioner D and Euclidean P implies that some directions can leak, not that every particular g leaks. The direct condition is $ADPg\ne0$. The actual step includes momentum, clipping, weight decay, and any other parameter mutation. Project an increment relative to the appropriate reference affine set, rather than projecting the absolute parameter vector onto a zero-origin kernel indiscriminately.

**Executable expression.** The metric-QP solution and a simpler post-step Euclidean projection are both valid protection baselines. The latter is generally not metric-optimal. A static M analysis does not equal a full Adam trajectory.

**Prediction/falsifier.** Quantify leakage through $\|ADPg\|$, or compare its disappearance after actual-step projection. For a commuting D/P or a g in a special invariant direction, the predicted leakage is zero.

**Closest alternative/comparison.** Projected optimizers and the reported post-step method are coherent alternatives. No claim about an author's implementation is independently verified by this mathematics review.

**Status.** Exact QP result. Optimizer identification and empirical necessity conditional. An attributed baseline rather than a separate new-method claim.
