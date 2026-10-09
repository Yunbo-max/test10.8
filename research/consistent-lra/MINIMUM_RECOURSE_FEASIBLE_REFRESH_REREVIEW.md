# Independent re-review of the corrected minimum-recourse refresh

Status: **assignment 188 completed on the frozen corrected bytes; verdict
`ACCEPT_CANDIDATE_MATH`**.

Reviewed identities:

- corrected candidate:
  `research/consistent-lra/MINIMUM_RECOURSE_FEASIBLE_REFRESH_CANDIDATE.md`
- corrected candidate SHA-256:
  `10e15b9d352a44947fed213f98679f4cbcb1e864e481cb8d1623904f8cff15cd`
- preserved assignment-187 review SHA-256:
  `7464f30d474c888d2483d56222c35b56ce75bce2f0e99df2f439fc5574c09f73`
- base commit stated by the task:
  `7d1faceba2dfb9efa7c3b5801b2937c7f74a531d`

## Verdict

`ACCEPT_CANDIDATE_MATH`.

The corrected candidate repairs both substantive defects found in assignment
187 rather than hiding them.  The complex \(k\)-numerical range is now used
only for the convex scalarization, and the candidate gives a valid recovery of
a real projector in the cutoff eigenspace.  Equation (5) is now the continuous
rank-\(k\) projector optimum rather than a whole-coordinate ceiling law, and
the actual \(\rho_{\rm hi}\) trigger condition is stated.  Existence,
current-refresh dominance, monotonicity, and scope boundaries also check out.

Acceptance means only that this card may remain in the mathematical candidate
pool.  It does not establish originality, select the method, admit Step 4 or
5, qualify a numerical solver, authorize native execution, or count as a
formal scientific experiment.

## 1. Feasibility, existence, and current-refresh comparison

For fixed rank \(k\), the real projector set

\[
\mathcal G_k=\{Q:Q=Q^{\mathsf T}=Q^2,\ \operatorname{tr}Q=k\}
\]

is compact.  The loss constraint in (1) is closed, and an exact top-\(k\)
projector \(Q^*\) of \(C\) is feasible because

\[
L_C(Q^*)=\operatorname{OPT}(C)
<(1+\rho_{\rm lo})\operatorname{OPT}(C)
\]

in the stated positive-OPT regime.  Hence the feasible set is nonempty and
compact and the continuous distance objective attains a minimum.

For equal-rank projectors,

\[
\|Q-P\|_F^2
=\operatorname{tr}(Q)+\operatorname{tr}(P)-2\operatorname{tr}(PQ)
=2k-2\operatorname{tr}(PQ).
\]

Because every selected exact-SVD refresh is a feasible comparison point, the
minimum-recourse solution satisfies both its declared loss target and

\[
\|Q^{\rm MR}-P\|_F^2\le \|Q^*-P\|_F^2.
\]

This ordering is pointwise at the current covariance.  It does not order later
trigger streams or cumulative movement, exactly as the candidate states.

## 2. Monotonic scalarized path

The constraint is equivalent to

\[
c(Q)=\operatorname{tr}(CQ)\ge
\beta=\operatorname{tr}C-(1+\rho_{\rm lo})\operatorname{OPT}(C),
\]

and minimizing movement is maximizing
\(o(Q)=\operatorname{tr}(PQ)\).  For \(\lambda\ge0\), Ky Fan's principle
therefore makes each scalarized maximizer a top-\(k\) projector of
\(P+\lambda C\).

For arbitrary maximizers \(Q_1,Q_2\) at
\(0\le\lambda_1<\lambda_2\), scalarized optimality gives

\[
o_1+\lambda_1c_1\ge o_2+\lambda_1c_2,
\qquad
o_2+\lambda_2c_2\ge o_1+\lambda_2c_1.
\]

Adding and cancelling the overlap terms yields

\[
(\lambda_2-\lambda_1)(c_2-c_1)\ge0,
\]

so \(c_2\ge c_1\).  The revised wording correctly says this holds for every
pair of maximizers at distinct parameter values.  Set-valued ambiguity at one
degenerate cutoff remains and is handled separately rather than being hidden
by the monotonicity statement.

## 3. Complex scalarization and recovery of a real projector

The revision no longer asserts that the joint range of real projectors is
convex.  Temporarily allowing complex Hermitian rank-\(k\) projectors gives

\[
\{(\operatorname{tr}(PQ),\operatorname{tr}(CQ)):Q
  \text{ complex Hermitian rank-}k\},
\]

the real and imaginary coordinate representation of the complex
\(k\)-numerical range of \(P+iC\).  This set is compact and convex.

Let \(c_{\max}\) be the captured energy of an exact top-\(k\) projector of
\(C\).  Since

\[
c_{\max}=\operatorname{tr}C-\operatorname{OPT}(C),
\qquad
\beta=c_{\max}-\rho_{\rm lo}\operatorname{OPT}(C),
\]

the assumptions \(\rho_{\rm lo}>0\) and \(\operatorname{OPT}(C)>0\) imply
\(c_{\max}>\beta\).  Thus the convex halfspace problem is strictly feasible.
A supporting-line, equivalently KKT, argument supplies a multiplier
\(\lambda_*\ge0\) for which a constrained optimum maximizes

\[
\operatorname{tr}((P+\lambda_*C)Q).
\]

It remains necessary to show that this complex optimum value is realized by a
real projector.  Put \(M=P+\lambda_*C\), which is real symmetric.  Let
\(E_>\) be the direct sum of eigenspaces strictly above the rank-\(k\) cutoff,
let \(E_=\) be the real cutoff eigenspace, and put
\(r=k-\dim E_>\).  Every scalarized top-\(k\) projector contains \(E_>\)
and chooses a rank-\(r\) projector \(R\) inside \(E_=\).  Compression to the
cutoff eigenspace gives

\[
P_{E_=}+\lambda_*C_{E_=}=\mu I_{E_=}.
\tag{R1}
\]

For the real symmetric compression \(C_{E_=}\), Ky Fan's principle makes the
minimum and maximum of \(\operatorname{tr}(C_{E_=}R)\) over real rank-\(r\)
projectors equal to the sums of its \(r\) smallest and largest eigenvalues.
The real Grassmannian is connected for \(0<r<\dim E_=\), and the trace map is
continuous, so its image is the entire interval between those extrema.  The
endpoint cases are unique/trivial.  A complex rank-\(r\) projector has trace
inside the same spectral interval.  Consequently the captured energy of the
complex boundary optimum can be matched by a real \(R\).  Equation (R1) then
forces the matching overlap as well:

\[
\operatorname{tr}(P_{E_=}R)
=\mu r-\lambda_*\operatorname{tr}(C_{E_=}R).
\]

Adding the fixed contribution of \(E_>\) recovers a real constrained optimum
with the same objective value.

When \(\lambda_*=0\) and \(0<k<d\), \(P\) is the unique top-\(k\) projector
of itself; feasibility of the supported optimum therefore means the old
projector is already feasible.  The \(k=d\) case is trivial.  Hence the
revision covers the zero-multiplier case too.

This is a valid mathematical existence argument.  It is not yet a robust
solver: an implementation must detect the cutoff multiplicity, compute the
compressed problem, and choose the real boundary subspace.  The candidate
correctly retains that obligation.

## 4. Continuous near-tie law and trigger

For the stated family, let

\[
s=k-\operatorname{tr}(PQ).
\]

Since \(C=(1+\delta)P+(1+2\delta)(I-P)\), direct substitution gives, for
every real rank-\(k\) projector,

\[
\|Q-P\|_F^2=2s,
\qquad
L_C(Q)=k(1+2\delta)-\delta s,
\qquad
\operatorname{OPT}(C)=k(1+\delta).
\]

Thus feasibility is exactly

\[
s\ge k\left(1-
\frac{\rho_{\rm lo}(1+\delta)}{\delta}\right).
\]

Every \(s\in[0,k]\) is realized by whole exchanges plus at most one real
two-coordinate rotation with
\(\sin^2\theta=s-\lfloor s\rfloor\).  Since movement is increasing in
\(s\), the corrected equation

\[
s_{\min}=k\left(1-
\frac{\rho_{\rm lo}(1+\delta)}{\delta}\right)_+,
\qquad
\|Q^{\rm MR}-P\|_F^2=2s_{\min}
\]

is the exact optimum of (1); no integer ceiling remains.

The old projector's relative excess is

\[
\frac{L_C(P)}{\operatorname{OPT}(C)}-1
=\frac{\delta}{1+\delta}.
\]

Therefore it triggers if and only if

\[
\frac{\delta}{1+\delta}>\rho_{\rm hi},
\]

as the revision now states.  Under this strict trigger and
\(\rho_{\rm lo}<\rho_{\rm hi}\),

\[
0<\frac{s_{\min}}k
=1-\frac{\rho_{\rm lo}(1+\delta)}{\delta}<1,
\]

so the candidate makes a strict current-refresh movement saving relative to
the exact SVD in this symmetric family.

One qualitative sentence should be read using the exact displayed ratio: the
method approaches exact refresh when
\(\rho_{\rm lo}(1+\delta)/\delta\to0\).  The shorthand
"\(\delta\gg\rho_{\rm lo}\)" alone is not sufficient over an unrestricted
large-\(\delta\) limit with fixed \(\rho_{\rm lo}\), where the saving fraction
tends to \(\rho_{\rm lo}\).  This precision note does not affect equation
(5), the trigger law, or acceptance of the mechanism into the candidate pool;
downstream design should use the exact ratio rather than the shorthand.

## 5. Scope, collision, and admission

The corrected card preserves the required boundaries:

- (2) is a present-refresh statement, not future-trajectory or cumulative
  recourse dominance;
- the degenerate-cutoff real solve and numerical stopping rule remain pending
  Step-4 implementation obligations;
- broad collisions with smooth/proximal subspace tracking are disclosed, while
  priority for the exact constrained hysteretic construction remains
  unresolved;
- the card still requires primary-paper/code collision audit, whole-pool
  ranking, method verification, complete experiment design, and scientific
  admission;
- there is no theorem-repair, originality, code-completion, native-execution,
  Stage-B, formal-experiment, or completed-research-cycle claim.

Those boundaries are consistent with `ACCEPT_CANDIDATE_MATH` and prevent this
mathematical acceptance from being misreported as a later-stage result.
