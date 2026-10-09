# Frozen baseline/evaluator repair contract v1
Scope: existing-method M audit, not a novel method, experiment result or gate pass.
Frozen against original author revision d607c4f6467216c470d1e3b93989d44d5fcdec97 and the independently recorded defects in BASELINE_AUDIT.md. Original source must remain unchanged. Contract changes create v2, never edit v1 after execution.

## Mathematical identities
For an actual row-orthonormal output Q with r rows, P=Q^T Q. Primary loss is the direct residual ||A-(AQ^T)Q||_F^2; the trace identity energy-||AQ^T||_F^2 is only an independently qualified accelerator, because cancellation can destroy small residuals. Independent OPT is the sum of squared singular values beyond k from a fresh thin SVD of the actual prefix. A retained refresh decomposition cannot serve as OPT.

Expand trace(P-Pprev)^2: trace(P)+trace(Pprev)-2trace(P Pprev)=r+rprev-2||Q Qprev^T||_F^2. This handles different ranks without counting basis signs or sketch row replacements. Save actual Q snapshots; never use aliases. For a separate low-dimensional verifier, explicitly materialize both projectors and calculate their direct Frobenius difference.

All intended prefixes t=1,...,n are scored. Recourse sums t=2,...,n; an optional initialization-from-zero cost is stored separately and never substituted. Preserve unrounded values, OPT, energy, numerical tolerance, additive excess, normalized additive excess, defined ratios and missing/near-zero ratio counts. No unconditional ratio=1.

## Baseline arms
Fresh SVD recomputes a thin decomposition on each prefix and returns the first min(k,t,d) rows of Vh.
Algorithm4 stores refresh energy C, initially 0, and triggers on energy >= c*C, c>1; it uses fresh exact SVD only at triggers and retains Q otherwise. Zero-energy prefixes are initialized deterministically. For rank-varying thin-SVD convention, all t<=k refresh in every comparator; this is an explicit warmup extension, NOT an unqualified fixed-rank reproduction. Save the warmup flag; separately report steady-state recourse after t>=k+1. A later fixed-rank nullspace-completion protocol needs its own review.
Fixed refresh retains the warmup output after t=k; periodic refresh has predeclared interval. These are established simple controls, not new discoveries.
FD must maintain a bounded sketch by the sourced standard shrink rule and expose top-k orthonormal right directions, with sketch size >k when dimension permits. Its weighted B rows are not scored as a projector. The source-author ell=k variant is retained as a separate diagnostic, not the strongest FD.

## Numerical rules and qualification
Float64; no negative energy/OPT or non-finite input accepted. Check Q Q^T approximately I. Relative residual tolerance is 1e-10*max(1,energy); diagnostic sensitivity at 1e-12 and 1e-8. Record the actual raw residual instead of silently rounding. Ratio is null when OPT<=tolerance, with positive-cost/zero-OPT violations counted separately. For trace and recourse accelerated calculations, an error larger than tolerance invalidates qualification; small signed roundoff is retained in diagnostics and clamped only in final mathematical metric.
Qualification uses actual released Rice/Skin prefixes and compares direct residual versus trace, direct-projector versus overlap recourse, fresh-SVD tail versus fresh-SVD reconstruction. No fabricated numerical examples or replacement benchmarks. Prefix selection is declared before results. Qualification results are software/scorer evidence only, not performance or theory confirmation.

## Information, clocks and freeze
Keep source order and remove labels only after retaining label/source identities. For author-compatible Rice/Skin, standardize using the whole released dataset, then select the published prefix. This defines an OFFLINE-transformed stream; no raw-online claim. No labels feed algorithm decisions.
Each arm resets its clock/state; separately measure update, scoring and total pipeline time. Exact reference decomposition is evaluator work except for fresh-SVD arm's own update. Record time.perf_counter and resource.getrusage CPU/RSS, interpreter/dependency/source hashes, command, outputs and all failed attempts.
One scientific process; thread cap 1 initially, CPU quota<=8; no GPU/API/cloud charges. Baseline qualification tasks only become executable after independent source review, exact input acquisition, pinned harness/native-plan admission and finite timeout/RSS. No candidate discovery, G01 PASS or empirical queue is approved by this document.

