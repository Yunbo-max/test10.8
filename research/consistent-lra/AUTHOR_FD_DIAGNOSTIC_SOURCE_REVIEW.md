# Independent source review: author FD diagnostic candidate

Reviewer: `/root/baseline_audit`.  The reviewer executed no project code and
made no edits, commits or publications.

## Initial review

Pinned candidate commit:
`46fd1bd325a842e325f44ee2be47ea396fa6b646`.
Verdict: **needs correction** for the proposed oracle; the production diagnostic
class itself faithfully ports the frozen update.

Reviewed identities:

- `native_baselines.py` SHA256
  `81c3309e659d1d9fdb69040b9becc6009bbe29b84a36aae8bac89ea6737e2c7c`;
- `author_fd_semantic_oracles.py` SHA256
  `5dac118cf81255fa4bedd0c53934ee9a837a941342ce41efef3a85f21872a1a2`;
- qualification document SHA256
  `1e2fcd05a7e4654e2ca330279ccd0a2ecfeb4e4748b695c496fc6c31b447e649`.

Required corrections:

1. The snapshot probe captured its copy only after the full loop and called
   `update(len(stream))` again, duplicating the final row.  Capture the first
   basis immediately and compare it after later valid prefixes.
2. Shrink counts were logged but not checked, despite the design claiming a
   check.  Compare against an independent count of the author's shrink branch.
3. `AUTHOR_BLOB` was metadata only.  Validate the raw bytes against the frozen
   Git blob before decoding/AST compilation, and parse those exact bytes.
4. Both sides used the shared `top_basis`, so projector conversion lacked an
   independent reference, and only `k=1` was exercised.  Use a distinct
   covariance eigendecomposition and add a varying-rank `k=2` probe.

## Correction

The candidate now applies all four repairs.  The initial verdict remains
preserved.  Correction rereview verdict: **accepted** for source fidelity and
finite engineering-oracle scope at commit
`679262574b5316d12c62b399f690c199b31cdf7a`.

Corrected identities independently verified by `/root/baseline_audit`:

- `author_fd_semantic_oracles.py` SHA256
  `df2f214a6d061a1d5f090441262ad0fc5d4c5f02be1ca73999db027ce360e756`;
- qualification document SHA256
  `a40b210528ffe86d6173df4cf6338ab50ec13812b6543e93bb71baa8ac47c59f`;
- this review before acceptance integration SHA256
  `81f50cdc82572f43dea5169d2cf0b251f9a16dd445e466428b89d3987081e181`;
- unchanged `native_baselines.py` SHA256
  `81c3309e659d1d9fdb69040b9becc6009bbe29b84a36aae8bac89ea6737e2c7c`;
- unchanged frozen `originals/consistent-fd.py` SHA256
  `ba16f17017005dfc90d7ff669678911b2b3e6211582efd4014ed592e44926990`.

The rereview confirmed byte-level Git-blob validation before compilation,
valid-prefix snapshot immutability, asserted shrink counts, an independent
covariance-eigendecomposition projector reference, and a separated-spectrum
`k=2` probe.  This acceptance establishes no native performance result,
theorem confirmation, scientific-gate pass, or paper claim.
