# Scoped independent reviews of the formal extensions

This record is written by the integration writer from actual delivered independent reviewer findings. It is neither a machine-checked proof nor a native scientific gate. Historical draft headers and preassignment plans remain unchanged; the current scoped conclusions are recorded here.

## Dynamic extension

Assignment: dynamic-recourse-extension-independent-review. Registered before dispatch at destination ec82f7d34916be295111e922f75068d56b1cad25. Reviewer: /root/execution_capability. Artifact FORMAL_AUDIT_v3_EXTENSION.md SHA256 440edfddc4b9d51a218ea878de78acd1b89b7648bdabdf222c493b3b31331c3c, checked at intake and after review; prerequisite v2 hash also matched.

The independently delivered verdict accepts the dynamic counterexample in its rank-uniform scope. N initial row insertions followed by N^2 alternating final-row insertion/deletion updates are legal. Each phase-two state has a unique optimal rank-k projector; every exact-optimal algorithm therefore incurs precisely R_k on each toggle. Initial recourse is nonnegative. With L=N+N^2, total/L > H_k/36 >= ln(k+1)/36. No dimension/rank-uniform constant gives total <=C L for all such streams. The reviewer independently inspected proceedings Theorem2.2, which includes insertions/deletions and derives O(n) from Lemma2.1.

This does not contradict fixed-k O(L) with a k-dependent constant or the approximate insertion-only existence statement. The optional zero/u row replacement formulation is valid, without claiming all arbitrary row replacements induce rank-one covariance changes.

The reviewer checked trace ||u||^2=N/2, entry bound sqrt(N), the stated nonzero-spectrum/pseudoinverse quantities, the <=2k projector-change bound and PCP ratio calibration delta=epsilon/(2+epsilon). It required the precision that delta^-2=(2+epsilon)^2/epsilon^2 only simplifies to O(epsilon^-2) for bounded epsilon, such as 0<epsilon<=1. This precision appears in the separately reviewed supplement below. Simultaneous-prefix sampling qualification remains pending.

The reviewer also verified the Algorithm4 energy deduction and dependency map: Theorem1.2's displayed proof invokes Lemma2.1; Theorem1.1 instead uses E.1/E.2; the stated Theorem1.3 route uses Theorem2.4 and Lemma3.10. This is not complete validation of those theorems. Zero prefixes, initialization, rank completion and the noninteger first-positive-energy denominator remain explicit qualifications.

At the time of this fixed-hash review, the exact sampling-source condition convention remained unresolved. The following independent supplement closes only that issue for the base insertion-only family.

## Consecutive-row condition supplement

Assignment: consecutive-condition-supplement-review. Registered before dispatch at destination ea8abd51aeaca59e433b00922ac871d3b4035fc8. Reviewer: /root/execution_capability. Artifact CONDITION_SCOPE_SUPPLEMENT_DRAFT.md SHA256 a283038010597ae8c23846839bbb1202794f67f92c1c35557fcc3fa33cf3546d.

The delivered verdict accepts the supplement with no mathematical gap. The reviewer independently inspected the indexed primary PMC author manuscript's FrameworkI.1 condition definition. Direct page opens returned CAPTCHA, which it reported rather than claiming direct-page inspection. The definition uses every consecutive-row submatrix's largest/smallest nonzero singular values. No arXiv PDF or version-equivalence was inspected.

The four cases exhaust nonempty consecutive blocks of the insertion-only A followed by u stream. In the proper suffix case, delta>=a_1>1/4 proves full row rank. For any row coefficients, the inequality ||x||^2+y^2<=4(N+1)F yields sigma_min^2>=1/[4(N+1)]. PSD row selection yields sigma_max^2<=N+1/2. Hence kappa<2(N+1), polynomial in the N+1 stream length. The other three cases are covered. The reviewer verified the bounded-epsilon PCP precision as well.

Supported: polynomial conditioning under this stronger consecutive-row convention does not restore the constant-eight exact-optimal lemma. Not supported: identifying a dynamic update log with a row-arrival matrix, refuting approximate insertion-only existence, validating the full sampling proof, claiming integer-entry results, empirical improvements, originality or publishability.

Both assignments were read-only source/symbolic work: no numerical scientific code, sampled cases, writes or publication by the reviewer. Both consume the unchanged shared wall window; they create no numerical score or science admission.
