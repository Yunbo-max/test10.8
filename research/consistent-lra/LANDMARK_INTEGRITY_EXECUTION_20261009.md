# Landmark mechanical integrity execution

Status: completed once, pending independent evidence review.  This is source
qualification only, not native numerical scoring or a scientific result.

## Bound execution

- Admitted plan commit: `8db6f5269794ff7c980f1b13795658b497432190`
- Native plan digest: `924ec160b40fed5973c93dd6fd12c3fc6b58bfe443b1e6b4568a546240d661c3`
- Harness plan digest: `b669223f69923da2f7a47d03ffd142d8407a0df24449a8062c4df53bc6395252`
- Run/attempt: `landmark-source-integrity-01` /
  `landmark-source-integrity-01-a1-da869994c8214556a5969d39ee316ae5`
- Attempts/retries: one / zero
- Receipt SHA256:
  `a535fc7f3da44abd05f19b9614f71d2122eabe32e40ad57d1bcf53703115fa00`
- Evidence SHA256:
  `62595f9dec8c563b05ebe92a0ecc66ac569c2f9730b699728613f5a366fc8e35`
- Exit/status: 0 / completed; stderr is empty.
- Workload: 1.0675 s; process CPU: 1.000666 s; inspector wall: 0.9763 s;
  maximum RSS: 12,588 KiB.
- Harness: completed in 2.0313 s; no GPU and no LLM calls; `gate_advanced=false`.

The process guard records the exact Python argv and a completed child within
the 60-second timeout.  The reservation is released.

## Mechanical observations

The exact frozen source passed full streaming identity/count validation:

- 34,964,305 bytes; Git blob `4c63060bbefcb38e0c705cea1f883d2fb7121f2c`;
- SHA256 `29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b`;
- 71,952 by 2,704; 1,151,232 stored entries; 1,146,848 numeric nonzeros;
- 4,384 explicit zeros; zero adjacent duplicate coordinates; source is ordered
  column then row.

For the author-script-selected first 5,000 rows, the descriptive counts are
80,000 stored entries, 79,325 numeric nonzeros, 675 explicit zeros, all 5,000
rows nonempty, 259 represented columns, and exactly 16 stored entries per row.

The output itself says `numerical_qualification=false` and
`scientific_gate_advanced=false`.  No SVD, projector loss, recourse, baseline
comparison, parameter search or claim test was performed.

## Review state

Independent review is assigned separately against an immutable candidate.
Until accepted, these are collected raw observations rather than an accepted
evidence verdict.
