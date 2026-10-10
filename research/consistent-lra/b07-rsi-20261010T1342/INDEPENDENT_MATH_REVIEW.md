# B07 independent mathematical review

Reviewer scope: existing-asset/formal/source audit only. This review reconstructs the two requested propositions from first principles; it does not execute scientific benchmarks, implement a new algorithm, adjudicate novelty, or approve a paper. Literature coverage remains incomplete. Date: 2026-10-10.

## 1. Certified spectral lower bound

Let the insertion-only matrix have rows x_1^T,...,x_t^T, let C=A^T A=sum_s x_s x_s^T, and let S=B^T B. Let k be an integer with 0<=k<=d. All losses here are **squared Frobenius** losses, not unsquared norms or operator-norm losses. Eigenvalues are ordered decreasingly, including zero padding. Define

    OPT_k(C) = tr(C) - sum_{i=1}^k lambda_i(C).

Assume the maintained certificate is genuinely valid:

    0 <= D=C-S <= Delta I,  Delta>=0.

For any rank-k orthogonal projector P,

    tr(PC)=tr(PS)+tr(PD) <= sum_{i=1}^k lambda_i(S)+k Delta.

The first inequality follows by expressing tr(PS) in an eigenbasis of S: diagonal entries of P lie in [0,1] and sum to k, so allocating all weight to the top k eigenvalues maximizes that sum. The second follows from D<=Delta I and tr(P)=k. Maximizing the left side over P gives the top-k captured energy of C. Subtracting from tr(C) therefore proves

    tr(C)-sum_{i=1}^k lambda_i(S)-k Delta <= OPT_k(C).

Since OPT>=0, the requested

    L=max(0,tr(C)-sum_topk(S)-k Delta)

is a valid lower bound. This proof does not need an FD implementation, only its stated covariance certificate. The PSD side C>=S additionally implies tail_k(C)>=tail_k(S), but that observation does not establish a new method or attribution.

### Exact unbatched FD identity

Assume an initially zero ell-row sketch with k<ell<=d, exact SVD arithmetic, insertion only into a zero row, and classical shrink at delta_j=sigma_ell^2 of the ell-row matrix M_j after insertion. Its post-shrink singular squares are sigma_i^2-delta_j for all ell slots. Each shrink loses exactly ell*delta_j energy, while insertion adds exactly ||x||^2. With Delta=sum_j delta_j, telescoping from zero gives

    tr(C)-tr(S)=ell Delta.

Each shrink's covariance loss is delta_j times an orthogonal projector, so its PSD loss lies between zero and delta_j I. Summing establishes the covariance certificate above. Deferred zero-delta steps do not affect the argument if all inserted rows remain represented. Substitution yields

    tr(C)-sum_topk(S)-k Delta
       = tail_k(S)+(ell-k)Delta >=0,

and hence exactly

    L=tail_k(S)+(ell-k)Delta <= OPT_k(C).

This is an identity under those operational assumptions, not merely the usual inequality (ell-k)Delta<=OPT.

### Where the identity does not transfer

- A larger buffered/batched compression has singular squares a_1,...,a_m and loss sum_i min(a_i,delta). With threshold delta=a_ell and m>ell, the loss is ell*delta+sum_{i>ell}a_i, rather than ell*delta. Truncating additional positive modes adds further loss. The generic L formula still applies if its covariance certificate is separately established; the unbatched equality must not be substituted blindly.
- Shrinking only selected modes, alpha-FD, approximate SVD, changing sketch width, and merge schedules require their own trace bookkeeping. A constant ell times cumulative shrink is not justified by the name FD.
- Even classical FD loses the equality if Delta is replaced by an inflated conservative upper bound. Such inflation can preserve a safe lower bound while making it weaker.
- Nonzero initialization must include its historical covariance loss and energy accounting. An ignored buffer, deleted rows, a changing centering transform, or forgetting factors changes the target covariance or breaks the telescoping proof.
- Floating-point stored energy and reconstructed sketch norms are not equal by mathematical identity alone. Numerical safety margins must cover actual error; empirical agreement is distinct from a certified rounding bound.

### Prior-work attribution, independently inspected

Ghashami and Phillips, *Relative Errors for Deterministic Low-Rank Matrix Approximations*, arXiv:1307.7454 / SODA 2014, Algorithm 2.1 and Lemmas 2.3–2.4 explicitly provide the original unbatched shrink, directional covariance control, and exact ell*Delta trace-loss identity; the paper attributes that FD machinery to Liberty. These are prior-work assets. The expression for L follows here algebraically from those assets; this review does not claim that expression or its use as a trigger is novel. The journal synthesis is Ghashami, Liberty, Phillips and Woodruff, *Frequent Directions: Simple and Deterministic Matrix Sketching*, SIAM J. Comput. 45(5), 2016, DOI 10.1137/15M1009718.

Primary documents consulted:

- https://arxiv.org/pdf/1307.7454 (Algorithm 2.1, Lemmas 2.3–2.4).
- https://arxiv.org/pdf/1501.01711 (journal synthesis).
- https://www-old.cs.utah.edu/~jeffp/papers/alpha-FD-ESA14.pdf (Desai/Ghashami/Phillips variant context; Section 1.1 distinguishes general FD facts from variant assumptions).

The original Liberty paper and all modern variants have not been exhaustively inspected; this is incomplete collision coverage.

## 2. Trigger-only lower bounds cannot change exact refresh trajectories

Fix eta>=0 and a common tolerance tau_t. Let the current Q have orthonormal columns and projector P=QQ^T, with residual

    r_t(Q)=tr(C_t)-tr(Q^T C_t Q).

The algorithm skips an exact oracle when r_t(Q)<=(1+eta)L_t+tau_t. Otherwise it obtains exact OPT_t and refreshes only if

    r_t(Q)>(1+eta)OPT_t+tau_t.                 [true violation]

On a true violation, it applies the same deterministic refresh map F_t to the same Q and data. False queries do not change Q. Initial Q, burn-in/end-of-burn state, stream, eta, tau, and refresh map must match. The oracle and refresh map cannot depend on query count, randomized solver history, or a different tie-breaking cache. Gate-only state may differ but its lower bound must remain valid.

### Proof by induction, stronger than the requested comparison

Suppose both algorithms enter prefix t with the same Q. They then have the same r_t and exact OPT_t. If the true violation is absent, each either skips or performs a false query, and neither changes Q. If it is present, validity L_t<=OPT_t and 1+eta>=0 gives

    r_t>(1+eta)OPT_t+tau_t >= (1+eta)L_t+tau_t.

Thus **every valid lower-bound gate must query** at that prefix. Both then observe the same true violation and apply the same F_t, producing the same Q. The common initial state closes the induction. Consequently ANY two certified lower-bound gates, even without pointwise domination, have the same refresh times, projectors, residuals, and cumulative recourse in exact arithmetic. This is not a global recourse optimality statement.

Now suppose additionally that L_strong>=L_weak at every common prefix state. Its query set is a subset of the weak gate's set, because

    r>(1+eta)L_strong+tau  implies  r>(1+eta)L_weak+tau.

The removed queries are precisely prefixes satisfying

    (1+eta)L_weak+tau < r <= (1+eta)L_strong+tau.

These are false queries, since L_strong<=OPT. Strict domination alone does not ensure any query is removed: the interval may contain no observed r. Query count is at least the number of true-violation refresh events, excluding initialization or externally mandated queries; equality holds if all false queries are eliminated. This lower bound is specific to this query-then-confirm policy, not a universal lower bound for all certified streaming algorithms.

### Boundaries of the conclusion

- Burn-in that updates regardless of violations is outside the induction. Start both arms at its identical endpoint and report its work separately. A different burn trajectory invalidates the common-state premise.
- A fixed or data-dependent common additive tau preserves the proof. Different tau values or different residual rounding may change decisions. An accepted r<=threshold+tau is a tolerance-relaxed certificate; it must not be reported as a strict zero-tolerance theorem.
- An old exact OPT is still a lower bound for insertion-only data: for every rank-k projector its residual gains nonnegative energy on insertion, so their minimum cannot decrease. Deletions/forgetting break that reasoning.
- A lower-bound computation that triggers a refresh without exact confirmation is a different algorithm; it can change the path. So can skipping stream positions, counting failed queries as refreshes, or making F depend on sketch state.
- In floating arithmetic, tiny differences at the boundary can produce genuine recursive divergence. Error-aware interval tests or fallback may restore safety, but finite measured parity is not a proof of exact numerical equivalence.
- Even if exact-query count decreases, FD maintenance plus sketch SVD, bookkeeping, confirmation, and output costs may erase the CPU benefit. Offline diagnostic exact OPT computations at every prefix must be reported separately from operational oracle calls and excluded from an isolated operational timing, without hiding their total research cost.
- A diagnostic showing L>OPT beyond the frozen rounding allowance is a **bound/certificate defect**; a timing regression with a valid bound is a **cost failure**. Output divergence can be a refresh-map/oracle/rounding/state defect. These are different findings.

## 3. Direct falsifiers and audit consequences

This section specifies logical falsifiers only; no experiments were run by this verifier.

1. Spectral certificate: any prefix with a reliably reconstructed negative eigenvalue of D, lambda_max(D)>Delta, or L>OPT beyond the declared numerical allowance falsifies its implemented preconditions/result. An exact-arithmetic construction satisfying both matrix inequalities cannot falsify Proposition 1.
2. Trace identity: log each shrink's m, ell, delta, and discarded squared energy. A step with loss !=ell*delta falsifies using the unbatched equality on that variant. It need not falsify the generic certificate.
3. Gate-only parity: under identical data/initial projector/refresh map and a valid bound, a true violation skipped by either gate or different refresh times contradicts Proposition 2's implementation assumptions. Query reduction alone cannot imply improved recourse.
4. Stronger-gate query nesting: if the strong arm makes an operational query where the weak arm does not, independently check pointwise L_strong>=L_weak, comparison tolerances, and state identity. Without domination, output parity still follows, but nesting does not.
5. Cost hypothesis: fewer queries with unchanged refresh/output traces but no lower operational CPU is a valid negative result. It does not contradict either mathematical proposition.

Verdict: both requested mathematical propositions hold with the explicit assumptions above. The unbatched FD equality is variant-sensitive and prior-work derived. Gate-only stronger lower bounds can remove false oracle calls; they cannot reduce refreshes or recourse while retaining the exact same confirmation/refresh policy and common start. No new-method, novelty, independent benchmark-confirmation, or paper PASS is granted.
