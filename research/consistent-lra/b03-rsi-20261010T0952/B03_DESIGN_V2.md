# B03 design correction before implementation or benchmark dispatch

Parent: B03_DESIGN.md SHA256 c60ad554d4db3773915bb61f8300bc1f834ca15d455ebd719b1610cc9f4d7c09.
Independent geodesic_review identified two contract gaps. Preserve the parent and apply these exact corrections; all data, parity tolerances, coverage, limits and claims stay fixed.

1. Enter accelerated solving only if finite legacy-surrogate loss(0)>target AND loss(1)<=target. The original loss(1)<=target+tol check alone is insufficient for a strict feasible right bracket. When either strict predicate fails, call the unchanged legacy function.
2. A small Newton residual/derivative estimate is only a trigger for extra bracket probes, never sufficient for acceptance. Probe max(lo,a-1.9e-14) and min(hi,a+1.9e-14). Accept the tighter interval only when the actually evaluated left loss is strictly >target and right loss<=target. Finish only when a sign-verified bracket is <=4e-14; return its feasible right endpoint. If those probes do not qualify, continue the original safeguarded iteration or the unchanged legacy fallback. No interval-arithmetic/root-distance theorem is claimed from floating point sign tests. Direct QR feasibility and original legacy-parity qualification remain mandatory.
3. An off-invariant target is outside the speed candidate's scientific scope. The raw derivative identity still holds, but no monotonicity/minimum-movement claim extends to approximate targets. The unchanged B01 Arm creates exact numpy.linalg.eigh targets. Unit tests distinguish this scope.

4. Accelerated steps require a finite strictly negative derivative; a positive derivative routes to legacy with an explicit monotonicity diagnostic. Keep the returned fallback Boolean in its original meaning (the target V was returned by the legacy/post-QR fallback). Record scalar-solver fallback counts separately. Do not relax inactive-angle fallback after observing k>d/2 runtime.

This is a reviewed numerical-repair protocol; mathematical exact-path monotonicity is separate from empirical numerical parity. Source publication is not scientific admission or paper eligibility.
