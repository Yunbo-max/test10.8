# Independent FD source-semantic oracle plan review

Initial source candidate `0d729ae4d8cf6e5cc0b527bbb9f4c62c4429862e`,
plan candidate `03ab885b6f0083e5d926909b98fe56461d355d74`, assignment
binding `c85d44d4ef2598f318a061b840ba211b1255df4b`, reviewer
`/root/rice_skin_plan_review`.

Initial verdict: **needs_correction**. The reviewer executed no code and wrote
no files.

The reviewer independently accepted the `ell`-row compress-before-insert
reference equivalence, covariance underestimate and directional-bound finite
checks, numerical tolerances, author `ell+1`/live-array diagnosis, Liberty
`2ell`/pending-row visibility diagnosis, fixed resources and engineering-only
scope. It also confirmed that the earlier out-of-harness smoke check is charged
as one executable attempt and invalidated for evidence.

The single required correction is dependency provenance. Importing
`baseline_qualify.top_basis` loads scikit-learn, but the initial oracle output
listed only Python/NumPy/SciPy and omitted `baseline_qualify.py` from runtime
source hashes. The correction must record sklearn, hash `baseline_qualify.py`,
document the full installed stack and reservation boundary, then regenerate all
affected source/input hashes and both plan digests.

Initial independently checked values are retained:

- assignment SHA256 `b444446d87b1da50b65937a4f9a14a5f66cdca1e7155eedbb497ada0ece42c4c`;
- oracle SHA256 `1e0c25c5f0ba4d3181917082946ac0a26b70f1b2b637220337ed3c607312e62d`;
- native plan SHA256 `219e26d50b36766c0c613bcf09d6fc13304a6060dea27ddd0dfa6c2f97335c85`,
  digest `8217559e74bd3cc17153928befac337a2d7c88abf4afc61bbe44c61d301d9840`;
- harness plan SHA256 `53d07fc7bb080c26f190d7330d791d8f00ad445b2374ceed844f8e3f999e89d4`,
  digest `570914e88fab0dbbb84524d19515e92c3d1ad16e8d027046e1e604ce49b45bba`.

No execution is admitted by this review. Even an accepted correction remains
software/source qualification, not a theorem proof, native benchmark,
performance result or scientific gate.
