# B09 V2 repair after the frozen V1 semantic failure

V1 is retained unchanged.  Its exact query/update masks and queried OPT values
matched B07/B08, but every run failed the prospectively frozen loss-trajectory
tolerance because the Gram eigensolver plus QR selected numerically different
top-k endpoints.  V1 timing is therefore not accepted as a semantic-equivalent
comparison.

V2 is a substantive, bounded repair and does not loosen any threshold:

1. Maintain the same incremental row Gram matrix.
2. On every exact query, compute only the leading-k Gram eigenvalues and obtain
   exact OPT from total energy minus their sum.
3. If and only if the exact inequality triggers a refresh (including growth
   prefixes), call the same NumPy full prefix SVD as B08 and take the same
   right-singular basis.  Non-refresh exact queries avoid that full SVD.
4. Keep B08 direct-reconstruction residual arithmetic, FD50 implementation,
   tolerance, order and all policy decisions unchanged.

Both policy arms have the same true refresh mask, so they pay the same number of
refresh SVDs; FD50 additionally pays sketch maintenance but may remove
non-refresh exact eigenvalue queries.  This is a stronger exact baseline/control,
not a new scientific method.

Run the same 2 eta x 2 policy x 3 isolated-process matrix and the same
interleaving.  Acceptance still requires exact query/update masks and
energy-scaled 1e-10 loss/OPT agreement with B07/B08, plus all reservations
settled.  Timing survives only when FD50 is faster in all three pairs for that
eta.  V1's failed audit remains adverse evidence and is never retroactively
converted to a pass.

