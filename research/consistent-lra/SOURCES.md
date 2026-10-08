# Source and evidence ledger

This records actual source reading and source identities, not reproduced experiments.

## Pinned sources

- Paper: https://proceedings.iclr.cc/paper_files/paper/2026/file/b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf
- Official proceedings: https://proceedings.iclr.cc/paper_files/paper/2026/hash/b14d76c7266be21b338527cd25deac45-Abstract-Conference.html
- Author repository commit: `samsonzhou/consistent-LRA@d607c4f6467216c470d1e3b93989d44d5fcdec97`.
- RSI workflow commit: `Yunbo-max/Research_Autopilot@1de12dfed5b84957b29ac5b3a2f04904bf3742bc`, on `autonomous-rsi`.
- RSI autonomous contract blob: `f9860c343cb8db5e43ddaf94441ac390b7c34b10`.

| Author file | Git blob identity | Current read scope |
|---|---|---|
| consistent-lra-landmark.py | 6da3eec62de50b5b37c36b26ae725549e354a738 | Full source read by parent and independent audit worker |
| consistent-fd.py | 294438ac128556f01a2c3d920bdb4f1225dd819f | Full source read by parent and independent audit worker |
| consistent-lra-rice.py | eb8e4e97a9538a14dd6b72d5e271b36c96c05e7c | Full source read by parent and independent audit worker |
| consistent-lra-skin.py | 9581652064a08f5b282cee83286ec7c72ac0fdad | Full source read by parent and independent audit worker |
| Rice_Cammeo_Osmancik.arff | 745655b79f4ca46a3a65a0a8653bd792fa6f7c31 | Directory identity observed; data bytes/access qualification pending |
| Skin_NonSkin.txt | fc58dda2eaf5b1f0d2d8c7924a298cd7d14ba17d | Directory identity observed; data bytes/access qualification pending |
| landmark.mtx | 4c63060bbefcb38e0c705cea1f883d2fb7121f2c | Directory identity observed; data bytes/access qualification pending |
| consistent-lra-random.py / random-fast.py | Not yet pinned in this packet | Actual generator/source reading pending |

The paper's formal objective, core bounds, Algorithm 4 and empirical Sections 4/G were inspected. A full theorem-by-theorem proof verification has not been performed. Source inspection does not establish any theorem defect. The source defects below do not prove that the figures used these exact code paths; figure-generation provenance remains pending.

## Independent source audit

Assignment `/root/baseline_audit` independently fetched all four original files at the immutable author commit and matched the requested blob identities. Its source-only conclusions are retained in BASELINE_AUDIT.md. It ran no experiments or tests. Independence here qualifies the scoped reading task; it is not an independent empirical replication.

Assignment `/root/execution_capability` independently read the pinned RSI entry/contracts and official Work/scheduled-task documentation. It confirmed current in-place Work production may continue and the explicit user CPU choice overrides default host placement within scope. It launched no tasks and established no continuous CPU survival.

## Product execution documentation inspected

- https://learn.chatgpt.com/docs/long-running-work
- https://learn.chatgpt.com/docs/automations

Current Work identity is supplied by the host context. Real automation identity, enabled state, conversation binding and immediate-run request must be recorded separately from scientific execution. Web scheduled tasks do not retain a local worktree between runs; restore durable inputs.

## Outstanding reading and qualification

Actual data contents and official provenance/access/license; published random generator and preprocessing; full native scorer reconciliation; faithful strong/simple baseline implementations; current novelty/collision audit; independent mathematical pool review/ranking; G01, numerical semantics, actual costs, E04 and confirmation. All remain pending.
