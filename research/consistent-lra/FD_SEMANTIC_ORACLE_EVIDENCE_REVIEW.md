# Independent FD source-semantic execution-evidence review

Evidence candidate `75ea9dfd01da41ee63d7005c4115d0970b45ccfc`,
assignment binding `0402c6fe105cefc6e3e45919e0badee5d12553b4`, reviewer
`/root/rice_skin_evidence_review`.

Initial verdict: **needs_correction**. The reviewer executed no project code and
wrote no files.

The reviewer accepted the complete raw chain: exactly one attempt, retry zero,
exit zero, no GPU, empty stderr, exact native/harness digests and all staged
source/input hashes. It independently checked 45 unique checks (eight prefixes
times five numerical checks plus five source probes), all passing, with no
nonfinite JSON values. It confirmed same-spec covariance/projector parity,
orthonormality, PSD covariance underestimate, the finite directional bound,
and the author/Liberty non-parity and mutation/visibility probes.

Exact accepted raw bindings include receipt SHA256
`02676afa9a50320d5756e18ddf3cc0e7708f9949499ff9149059aea9b20175ea`,
output SHA256
`8dc34bdced536cadbef966182f759e941e3725f8f400c9d09f780d82a1ee507b`,
guard SHA256
`9de1b008eb45ff0a7af5ce6fb42fec08dadf438134a180eb85fdaccd93d863ec`,
and harness report SHA256
`8a39d5afc0c7c4ca58fd27a3787380b955b2319aaeb73d0931fb0a76a8e6cb25`.
CPU, wall, RSS, cumulative attempt/task counts and reservation release were
otherwise consistent.

The sole correction is administrative. With deadline `07:47:45Z`, the evidence
observation at `03:08:34Z` had 16,751 seconds remaining and the assignment
observation at `03:10:32Z` had 16,633 seconds, not the carried-forward 18,136.
The checkpoint's last resource observation must also advance from `01:02:08Z`
to the actual FD launch observation `03:08:34Z`. Raw plan, receipt, output,
harness and log bytes must remain unchanged.

This review cannot establish a theorem, author/Liberty state parity, native
benchmark performance, G01, E04, Gate A or a paper claim.

## Time-ledger correction rereview

Corrected candidate `c36734766f80c85864e005711cfe7ab1c36c61be`,
rereview binding `77932f7ccfe13f1091ef70acf3c862bbda9e3937`. The same
independent reviewer returned **accepted** without execution or writes.

It verified the historical remaining times (16,751 and 16,633 seconds), the
corrected-candidate value (16,338), the rereview-binding value (16,269), and
the `03:08:34Z` resource observation. Tasks increased monotonically from 29 to
30 while attempts remained 7, scientific attempts remained zero and cumulative
process CPU remained 1.581142 seconds. It compared Git blob identities and
confirmed every raw FD plan, receipt, output, harness and log byte was unchanged.
Acceptance is limited to the finite engineering source/software qualification.
