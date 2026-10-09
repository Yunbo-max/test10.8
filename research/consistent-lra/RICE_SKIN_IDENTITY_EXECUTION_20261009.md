# Rice/Skin selected-prefix identity execution

Status: completed raw engineering evidence, pending independent evidence review.
Not official-scorer parity, total streaming recourse, baseline performance or a
scientific result.

## Bound execution

- Prelaunch review: `RICE_SKIN_IDENTITY_PLAN_REVIEW.md`, verdict `accepted`
- Admitted prelaunch commit: `2b178b3b8afe32fe13565f4ab91f04cf2993b96e`
- Native digest: `9dca9c9df1c59f7ecf359a4426d3d33ef3d4dc95da9b2a7052e5a4561d7b3eee`
- Harness digest: `b6c9a8f6550e1cc71851d7ca3dc71cfde90ba4b861ad800740d1478102ba6cc9`
- Receipt SHA256: `a7c5861993e6030cafd261550aa3087d8e570fa384f4d976ba6cec27ee24c5cd`
- Attempts: two sequential first attempts; zero retries; both exit 0; both
  stderr files empty.
- Harness wall: 3.0142 s; native-wrapper wall: 2.8259 s; no GPU or scheduler
  LLM call; `gate_advanced=false`, `scientific_result_verified=false`.
- Rice: attempt wall 1.2677 s, measured workload wall 0.0758 s, CPU 0.0758 s,
  max RSS 120,372 KiB.
- Skin: attempt wall 1.5228 s, measured workload wall 0.3043 s, CPU 0.3038 s,
  max RSS 148,112 KiB.

Numerical thread environment was capped at one by the caller.  The 512-MiB
field was a reservation, not an OS RLIMIT; actual RSS is reported above.  The
reservation is released.

## Raw identity observations

Both outputs evaluate the prescribed prefixes
`1,2,3,7,25,100,1000,3000` after author-compatible offline full-released-data
standardization.  Every primary `1e-10` check passed; sensitivity checks at
`1e-12` and `1e-8` also have zero identity failures.

| Data/rank | Output SHA256 | Missing ratios at each tolerance | Positive-loss / near-zero-OPT | Max abs direct-minus-tail | Max orthogonality error |
|---|---|---:|---:|---:|---:|
| Rice k=1 | `35aa4b0b420b837a66a4058412ef79a133fba89a986f400ae11e333e7c228eb9` | 1 | 0 | 2.7285e-12 | 4.4409e-16 |
| Skin k=1 | `45dffa731cd23b38e0c729f786926124e04486357370cd55bf2fc956c3ca92a0` | 1 | 0 | 9.0949e-13 | 6.6613e-16 |
| Skin k=2 | same Skin output | 4 | 0 | 5.3291e-14 | 1.1333e-15 |

The ratios for near-zero OPT are missing, not forced to one.  Direct residual
versus trace, fresh-SVD tail versus direct residual, and direct versus overlap
projector change agree within the declared tolerances on these selected
prefixes.

Rice released shape is 3,810 by 7; first-3,000 labels are 1,630 Cammeo and
1,370 Osmancik.  Skin released shape is 245,057 by 3; its first 3,000 rows are
all label 1 in released order.  Labels are retained for provenance but never
used by the evaluator.  The single-class Skin prefix is a source-order fact and
a generalization confound, not an evaluation success.

Both raw outputs state `scientific_gate_advanced=false` and
`performance_claim_eligible=false`.  The recourse comparisons are only between
successive selected prefixes, never claimed as total per-row streaming
recourse.  Independent evidence review remains required before accepting this
engineering qualification.
