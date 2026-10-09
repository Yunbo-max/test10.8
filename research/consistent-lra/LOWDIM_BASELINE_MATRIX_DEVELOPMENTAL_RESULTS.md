# Rice/Skin developmental baseline matrix

Status: descriptive development evidence only.  Independent E04 review accepted
the underlying 39-arm, 117,000-prefix matrix at remote commit
`f7225f3ef51115a620e4c1e0ec89141be1e27d21`; the acceptance ledger was then
read back at `9f2ec0ddcde9454352ec92576ff72866d1b61635`.

## Scope and metric contract

These are the first 3,000 released rows of Rice (`k=1`) and UCI Skin
(`k=1,2`), transformed with the frozen full-released-data offline scaling used
by this development protocol.  They are scored by the repaired local projector
scorer, not an authenticated upstream official scorer.  For prefix matrix
`A_t` and rank-`k` projector `P_t`, loss is
`||A_t(I-P_t)||_F^2` and recourse is
`sum_t ||P_t-P_{t-1}||_F^2`.  The initial transition from the zero projector is
excluded from primary recourse.  `steady recourse` additionally excludes the
rank-build warmup, which matters for Skin `k=2`.

Ratios are reported only when the fresh-SVD optimum is above the frozen
near-zero tolerance.  Thus the defined-ratio denominator is 2,999 for each
`k=1` cohort and 2,986 for Skin `k=2`; the excluded counts are explicit below.
Fresh-SVD ratios equal one by construction and are a scorer reference, not an
algorithmic win.  Pipeline seconds are one-run engineering observations and
must not be used as stable performance claims.

## Independently checked summaries

| cohort | arm | ratio mean | ratio max | defined n | near-zero excluded | total recourse | steady recourse | pipeline s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| rice-k1 | algorithm4-c100p0 | 1.04561835 | 2.16494611 | 2999 | 1 | 0.444983009 | 0.444983009 | 0.439545 |
| rice-k1 | algorithm4-c10p0 | 1.01149109 | 2.16494611 | 2999 | 1 | 0.408278668 | 0.408278668 | 0.459370 |
| rice-k1 | algorithm4-c1p1 | 1.00012046 | 1.01136102 | 2999 | 1 | 0.200832607 | 0.200832607 | 0.510761 |
| rice-k1 | algorithm4-c2p0 | 1.00141613 | 1.3623114 | 2999 | 1 | 0.272381134 | 0.272381134 | 0.459081 |
| rice-k1 | algorithm4-c2p5 | 1.00264256 | 1.58217283 | 2999 | 1 | 0.2903298 | 0.2903298 | 0.466791 |
| rice-k1 | algorithm4-c5p0 | 1.00516803 | 2.16021203 | 2999 | 1 | 0.431944169 | 0.431944169 | 0.460938 |
| rice-k1 | author_fd-ell2 | 1.00000091 | 1.00000691 | 2999 | 1 | 0.208005479 | 0.208005479 | 0.575288 |
| rice-k1 | fd-ell2 | 1.00006056 | 1.00114561 | 2999 | 1 | 0.245124613 | 0.245124613 | 0.524169 |
| rice-k1 | fd-ell4 | 1 | 1 | 2999 | 1 | 0.207624544 | 0.207624544 | 0.548990 |
| rice-k1 | fixed-default | 1.4961289 | 2.16494611 | 2999 | 1 | 5.32729416e-12 | 5.32729416e-12 | 0.446142 |
| rice-k1 | fresh-default | 1 | 1 | 2999 | 1 | 0.207621097 | 0.207621097 | 0.764920 |
| rice-k1 | periodic-interval10 | 1.00219545 | 2.16021203 | 2999 | 1 | 0.426696304 | 0.426696304 | 0.478505 |
| rice-k1 | periodic-interval100 | 1.02169233 | 2.16494611 | 2999 | 1 | 0.464177512 | 0.464177512 | 0.449067 |
| skin-k1 | algorithm4-c100p0 | 3.29864847 | 4.82008315 | 2999 | 1 | 0.153607736 | 0.153607736 | 0.388471 |
| skin-k1 | algorithm4-c10p0 | 1.13248069 | 4.82008315 | 2999 | 1 | 0.451155853 | 0.451155853 | 0.418610 |
| skin-k1 | algorithm4-c1p1 | 1.00060476 | 1.03831782 | 2999 | 1 | 0.110178039 | 0.110178039 | 0.498457 |
| skin-k1 | algorithm4-c2p0 | 1.00878099 | 1.78701825 | 2999 | 1 | 0.428850152 | 0.428850152 | 0.396898 |
| skin-k1 | algorithm4-c2p5 | 1.01324418 | 2.04112026 | 2999 | 1 | 0.540047658 | 0.540047658 | 0.444071 |
| skin-k1 | algorithm4-c5p0 | 1.03738524 | 2.60367643 | 2999 | 1 | 0.543872971 | 0.543872971 | 0.421022 |
| skin-k1 | author_fd-ell2 | 1 | 1 | 2999 | 1 | 0.0337081138 | 0.0337081138 | 0.525643 |
| skin-k1 | fd-ell2 | 1.00001088 | 1.00032239 | 2999 | 1 | 0.0338350753 | 0.0338350753 | 0.486913 |
| skin-k1 | fd-ell3 | 1 | 1 | 2999 | 1 | 0.0337081138 | 0.0337081138 | 0.465673 |
| skin-k1 | fixed-default | 6.56283002 | 7.71372508 | 2999 | 1 | 0 | 0 | 0.403018 |
| skin-k1 | fresh-default | 1 | 1 | 2999 | 1 | 0.0337081138 | 0.0337081138 | 0.565584 |
| skin-k1 | periodic-interval10 | 1.00755706 | 4.82008315 | 2999 | 1 | 0.301822624 | 0.301822624 | 0.439307 |
| skin-k1 | periodic-interval100 | 1.02798236 | 4.82008315 | 2999 | 1 | 0.602767404 | 0.602767404 | 0.408131 |
| skin-k2 | algorithm4-c100p0 | 1.24353291 | 6.86016027 | 2986 | 14 | 1.00037472 | 0.000374718855 | 0.420683 |
| skin-k2 | algorithm4-c10p0 | 1.20178376 | 22.6367415 | 2986 | 14 | 1.20280336 | 0.202803362 | 0.439135 |
| skin-k2 | algorithm4-c1p1 | 1.00158788 | 1.15212451 | 2986 | 14 | 1.10841105 | 0.108411048 | 0.419548 |
| skin-k2 | algorithm4-c1p5 | 1.01483287 | 5.15326971 | 2986 | 14 | 1.24745997 | 0.247459972 | 0.397389 |
| skin-k2 | algorithm4-c2p0 | 1.05063463 | 23.2964698 | 2986 | 14 | 1.33011194 | 0.330111941 | 0.402449 |
| skin-k2 | algorithm4-c2p5 | 1.10244384 | 25.07511 | 2986 | 14 | 1.33712729 | 0.337127291 | 0.443771 |
| skin-k2 | algorithm4-c5p0 | 1.08282039 | 6.86016027 | 2986 | 14 | 1.00462557 | 0.00462556976 | 0.445266 |
| skin-k2 | author_fd-ell2 | 1 | 1 | 2986 | 14 | 1.07006663 | 0.070066625 | 0.557579 |
| skin-k2 | fd-ell3 | 1 | 1 | 2986 | 14 | 1.07006663 | 0.070066625 | 0.543399 |
| skin-k2 | fixed-default | 1.07362472 | 6.86016027 | 2986 | 14 | 1 | 0 | 0.508424 |
| skin-k2 | fresh-default | 1 | 1 | 2986 | 14 | 1.07006663 | 0.070066625 | 0.584017 |
| skin-k2 | periodic-interval10 | 1.00292186 | 1.98603327 | 2986 | 14 | 1.191326 | 0.191325998 | 0.463331 |
| skin-k2 | periodic-interval100 | 1.05860902 | 6.86016027 | 2986 | 14 | 1.00170982 | 0.00170982123 | 0.438124 |

## Descriptive observations, not claims

- Within the frozen Algorithm 4 sensitivity grid, `c=1.1` has the smallest
  mean and maximum ratio in all three cohorts.  This is a development-set
  observation after viewing these data, not prospective confirmation.
- Fixed projectors expose the intended stability/fit trade-off: essentially
  zero steady recourse but materially larger ratios, especially for Skin
  `k=1`.  Periodic and large-`c` arms show that recourse is not monotone in the
  nominal refresh threshold on these fixed streams.
- On these low-dimensional streams, the qualified FD variants closely track
  fresh SVD.  The `author_fd` arms are retained as diagnostics because their
  `ell+1` interface is not the same interface as the qualified project FD arm.
- Skin `k=2` demonstrates why total and steady recourse cannot be conflated:
  every arm includes a rank-build contribution of one before the steady
  component.

## Evidence boundary

The committed archives are `lowdim-rice-k1.tar.gz`,
`lowdim-skin-k1.tar.gz`, and `lowdim-skin-k2.tar.gz` in the terminal final
repair attempt.  Their SHA-256 values are respectively
`e959e370355baf4d2a173c84f34a4596843696c90b8ed5a7bc4d50dd6a848197`,
`6f7985f7ae1f4f87844585d857986e1119413673d61343dffbe266fe364e1cea`,
and `95a9e652597ccb85d0842eb24ec3ff31551069d7e42cd6f3013fcb1c5538816a`.
The independent review recomputed 351 summary checks and 312 direct/SVD spot
checks with zero errors and verified all 82 declared outputs.

This record does **not** establish official-scorer parity, Landmark or random
coverage, confirmation, Gate A, a complete G01, theorem validation,
generalized superiority, paper readiness, or any new paper.  Those descendants
remain blocked, so the machine decision remains `2` (return to sources and
benchmarks).
