# Independent method Parent Problem review

Assignment 190; reviewer `/root/readiness_review`; source author `/root`.
Source snapshot: `main@ed05bb7616bf31822c29a4a0b35fe6735bf002a1`.
Reviewed candidate SHA-256:
`ebf0deb8466c2f31163ba3d44e8f7cfcd73adf693f386f3f189bfae1dc51755d`.
Reviewed task SHA-256:
`35a526ba3011f78e2db26e232e670fc568650f00773be9b32438fc390640c9f0`.

**Verdict: CORRECT_AND_REREVIEW.** This is a source/design review only. It
does not reject the scientific question, establish a natural failure, activate
the pending evaluator contract, admit a candidate or count a scientific result.

## Required corrections before parent freeze acceptance

1. **Freeze the actual accuracy envelope.** The affected-event predicate,
   strongest-simple oracle, primary endpoint and success prediction all refer
   to a "declared reconstruction envelope," but the card declares no formula
   or numerical quality threshold for it. The retained native protocol freezes
   loss/OPT definitions and numerical tolerances; it does not supply this
   missing scientific envelope. State the exact baseline-derived per-event
   bound, how it is fixed without candidate outputs, whether it applies only
   at the event or to the full trajectory, and the near-zero-OPT rule. Do not
   confuse numerical tolerance with a permitted quality shortfall or import
   free `rho_lo`/`rho_hi` choices from the pre-Gate method card.

2. **Freeze the comparison anchor and resolution predicate.** "Reduces
   movement" could compare a control's own adjacent transition with the target
   transition, or the distance of that control's current projector from the
   target arm's pre-refresh projector. Those are different scientific questions.
   Define each event's target `P^-`, fresh output, control output and movement
   algebraically. Define `alternative_solves` and the unresolved fraction using
   a single exact candidate-independent quality/reduction rule. The oracle's
   selected output is only an event-wise diagnostic; switching between controls
   is not one realizable cumulative trajectory. Preserve that distinction in
   the primary endpoint and later method claims. Document arm/prefix event IDs
   and shared-input dependence; parameter arms cannot manufacture repetitions.

3. **Separate observed rejection from insufficient evidence.** The assertion
   that failure of *any* threshold falsifies the parent conflicts with the
   installed importance-preserving gate. Fewer than 20 valid eligible cases,
   missing/scorer-blocked cases or incomplete source coverage give
   `INCONCLUSIVE`, not `KILL`. Adequate valid observed data below the frozen
   substantive value thresholds gives `KILL`. Keep missing evidence unknown.

4. **Make the natural episode definition match the actual trigger.** The
   candidate opens with an accuracy failure forcing an existing refresh, but
   frozen Algorithm 4 refreshes when energy reaches `c * E_last_refresh`;
   that trigger need not mean the retained projector violates an accuracy bound.
   Correct that source claim and explicitly state which naturally observed
   episodes qualify as failed episodes for this method's failure-census route,
   which are retained as unaffected census members, and which are outside its
   scope. Do not assign `failed_episode: true` to ordinary successful energy
   refreshes solely to satisfy the helper schema. The resulting denominator
   must remain mechanically reproducible and candidate-independent. If the
   population changes, preserve this initial card and its lineage rather than
   silently rewriting an accepted parent.

## Accepted parts and legal next action

The six headings and explicit `contribution_type: method` are present. The
native Landmark identity, first-5000 released ordering, rank 25, no scaling,
259-column map/ambient embedding, warmup exclusion and finite dependent-event
interpretation match the retained baseline design. The reference family is
strong: keep/fixed, periodic, fresh SVD and qualified FD; author FD is correctly
excluded from the strong role. Counts/fractions are explicitly project-specific
screens and do not claim population inference. The normalized projector
movement scale is meaningful for fixed rank. Candidate dependence is expressly
excluded from the proposed simple oracle.

The card correctly retains the official-scorer/faithful-harness blocker and the
project-local paper-math evaluator's design-only status. Stage-A identity and
timing records are not used as the native failure census. No new method code,
candidate-pool promotion, Natural Gate 0 PASS, IPCG or scientific dispatch is
currently legal on this record. The immediate legal next action is a bounded
correction of this parent specification and an independent exact-byte rereview;
after a supported parent freeze, the genuine evaluator authority/qualification
must still be resolved before collecting the native census. A candidate whose
mathematics was previously reviewed remains pre-Gate evidence only.

The reviewer inspected the actual installed `c23/research-autopilot` modules
`references/importance-preserving-gate.md` and
`references/contribution-value-gates.md`, plus AGENTS, the exact candidate/task,
native protocol, frozen repair contract, baseline audit, baseline matrix design
and relevant pre-Gate method/source snippets. Supporting fixed files include
native protocol SHA-256 `dc19834b84e118c5a80ba0cd2f89ee2eb28526a595621cf6d0b920959265631d`,
baseline design SHA-256 `c6b5d2525a87d278f3ad90b2b69045478e4690c66c10459ab16ea574bee11083`,
and repair contract SHA-256 `d00db725241d68629785bfa7ae39bfd90fb32c899c6956047912b4431a540e1e`.
No numerical/scientific code was imported or run. Only this review artifact was
written; the reviewer did not edit the candidate, controls, shared skill/vendor,
publish changes or start jobs.
