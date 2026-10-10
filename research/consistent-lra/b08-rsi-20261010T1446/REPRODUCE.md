# B08 reproduction and scope

Pinned workflow: Yunbo-max/Research_Autopilot autonomous-rsi commit
`7af53173bbd69726877ca04fb77b9466ef1b839d`. The retained Simple `.3` command
transport digest is `97cdb752027748261c1d6a11980d10d7a46f2c79c2a00e975f0c08d2c8847893`;
it is not a claim of a full SQLite/ACP supervisor deployment.

The raw archive contains exact driver/auditor source, prospective design,
independent reviews, 12 JSON+NPZ operational runs, the B07 reference arrays,
all runner contracts/receipts/stdout/stderr and a byte manifest. Verify the outer
manifest and NPZ CRC/SHA256 before use. NumPy and SciPy were already available;
no package installation was performed.

From a fresh copy of the archived `work` directory, each timing command has the
form:

`python3 run_policy512_operational.py --policy baseline|fd50 --eta 0.01|0.1 --repeat 0|1|2`

Run only one at a time with numerical threads1 and the documented2GiB address
space limit. The frozen order is in `B08_FROZEN_DESIGN.md`; output names encode
the arm/eta/repeat. Then run `python3 verify_policy512_operational.py`. That audit
requires the exact frozen `B08_RUN_MANIFEST.json` and `FD_POLICY512_RAW.npz`.
Use different output directories for a new reproduction; do not overwrite the
historical bytes.

The primary timer covers the whole512-prefix online stream loop, including
residuals, decisions, real on-demand exact SVDs, exact top-k refreshes and FD
maintenance. Imports, input loading, object construction, scoring and saving are
excluded; runner command wall and RSS remain separate. Three process repeats
measure timing variability on one development prefix and are not independent
scientific samples. Output equivalence is supported by exact query/update mask
parity, queried-OPT/loss parity and the same deterministic SVD refresh map; dense
projectors were not saved at every prefix.

This is an attributed existing-FD comparator audit on Landmark first512 only.
It is not the author's literal first1..4999 protocol, an optimized incremental
exact-query baseline, unseen confirmation, a new method, or a paper verdict.
Native1024/5000, stronger baselines, cross-dataset confirmation and originality
work remain pending.

