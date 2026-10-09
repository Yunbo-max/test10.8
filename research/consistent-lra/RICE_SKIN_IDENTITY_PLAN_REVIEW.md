# Rice/Skin selected-prefix identity plan review

- Reviewer: `/root/rice_skin_plan_review`
- Candidate: `6d2c1021aa01c62d0e4398142fa1b3bf37c3c528`
- Assignment/binding: `62d5062e8dc54ca4a4668497968fffe983d2a88f`
- Registered order: 19
- Verdict: `accepted`
- Reviewer execution/writes: none

The reviewer independently recomputed native digest
`9dca9c9df1c59f7ecf359a4426d3d33ef3d4dc95da9b2a7052e5a4561d7b3eee`
and harness digest
`b6c9a8f6550e1cc71851d7ca3dc71cfde90ba4b861ad800740d1478102ba6cc9`
with the pinned canonical algorithm.  It verified exact code/input/environment
refs, distinct outputs, sequential job execution, two-attempt/zero-retry limits,
and the engineering-only semantics: direct residual versus trace, fresh SVD
tail versus direct reconstruction, and direct versus overlap projector change
between prescribed selected prefixes.

The acceptance explicitly excludes official-scorer parity, total streaming
recourse, baseline performance, confirmation and all scientific gates.  The
resource fields are admission reservations, not OS affinity or RLIMIT
enforcement.  The execution caller must cap numerical threads to one; 512 MiB
must not be reported as an enforced hard process limit.
