# Independent Landmark baseline-matrix design review

Reviewer: `/root/baseline_audit`.
Reviewed immutable commit: `f8af5e3a27ca2983d58a505566995d87d4591d9e`;
tree: `dca69ca37f03e4879ebb6a080ab77f1914efb0b4`.
Reviewed design blob: `399ad6eb9955f25f9386aa1b515576821b009c8b`;
SHA256: `51f08f98262cb01f29f7435016111f11c340e4b095084668e06cfd5c55f22b73`.
Initial verdict: **NEEDS_CORRECTION**. No code was generated or executed.

The reviewer accepted source identity, the 13-arm inventory, both denominators,
Gram identities, supported active-column embedding, calibration limits and
non-admission scope. Five defects blocked code: version and separately qualify
the Gram acceleration against canonical direct scoring; use `1e-10` separate
loss/OPT and dimensionless recourse oracle tolerances with direct fallback for
uncertain ratios; assign Gram/energy/copy/solver ownership without free shared
arm state; freeze active-map/zero-energy/warmup/rank-deficiency/tie policies and
retain both projectors for selected recourse oracles; and require partial-only,
fsynced, no-replace, rehashed publication of exactly 26 members plus archive and
manifest (28 successful files), excluding partials.

The review is design-only and grants no runner, plan or execution admission.

## First correction rereview

Reviewed immutable commit: `b1a4f3a65352c170232e0cbaf23338b5bfe6c4f4`;
tree: `5ae0448f4659ff44c3f0c1d6052f81dd61e9e983`;
corrected design SHA256:
`f66e56e580b1771bcd9afd22c20ca7629ee477cbc8496904f264cf7c0442c3ec`.
Verdict: **NEEDS_CORRECTION**. No code was generated or executed.

The rereviewer accepted versioning, two-stage admission, separate oracle
tolerances, independent arm state/timing, active mapping, rank/tie policy and
paired recourse snapshots. Two ambiguities remained: direct fallback needed to
replace every reported/derived OPT and loss metric while retaining Gram
diagnostics, including direct loss for every arm when direct OPT is near zero;
and raw/summary finals needed the same hard-link no-replace, partial-unlink,
immediate-final-rehash and directory-fsync contract as archive/manifest. Only
unpublished working/partial files may be excluded from the 28-file inventory.

## Final rereview

Reviewed immutable commit: `85d84381ad02e01050c978f3611ed6f80ed88e2b`;
tree: `287eab8752e3764d97153fa6b7bbd51137bc2210`;
design blob: `a8c9332857eba826bea79d0476bdd76e27d0c0ee`;
SHA256: `c6b5d2525a87d278f3ad90b2b69045478e4690c66c10459ab16ea574bee11083`.
Verdict: **ACCEPT — design only**. No code was generated or executed.

The independent reviewer confirmed that direct fallback now replaces every
reported and derived OPT/loss metric while preserving Gram diagnostics, and
that near-zero direct OPT forces direct residual scoring for all arms. The
reviewer also confirmed the hard-link no-replace, partial-unlink, immediate
final rehash and directory-fsync publication contract for raw and summary
finals, including published finals located under staging in the 28-file
inventory. Previously accepted state, timing, rank/tie, denominator and
resource boundaries remain unchanged. This verdict authorizes neither runner
generation, an execution plan nor a workload.
