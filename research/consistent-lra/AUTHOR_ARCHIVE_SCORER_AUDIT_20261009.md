# Author archive and scorer-interface audit

Status: source-only audit pending independent review.  It does not establish
which script produced a published figure and it is not a reproduction.

## Frozen scope

The complete 34-path Git tree of `samsonzhou/consistent-LRA` at
`d607c4f6467216c470d1e3b93989d44d5fcdec97` contains seven Python scripts,
three data/text artifacts (`Rice_Cammeo_Osmancik.arff`, `Skin_NonSkin.txt`,
`landmark.mtx`), `output.csv`, images and `consistent-lra.zip`.  The ZIP's 33
entries are exactly all Git-tree paths except the ZIP itself.  There is no
test suite, package manifest, command-line evaluator, schema, metric fixture or
separately named scorer in that frozen tree.

`consistent-lra.zip` contains the same seven scripts, data, CSV and images.
For all seven scripts and `output.csv`, the ZIP bytes differ from the root only
by CRLF versus LF line endings: replacing CRLF with LF makes each pair exactly
equal.  The root and ZIP Landmark matrix are byte-identical without
normalization.  Therefore the archive does not supply a hidden alternative
evaluation implementation.

## Additional root artifacts

- `consistent-lra-test.py` is Git blob
  `d6037741f3ebf8d797108896b24d658c4043eba0`, SHA256
  `a3d6947eb5460db40ef962184fbbedca867186edefcd8828243c9ca7a5e54169`.
  It reads Rice after 16 lines, drops labels, standardizes the full dataset,
  truncates to 3,000 rows, evaluates only `c_list=[10]`, assigns ratio 1 when
  the reference cost is zero, and plots cumulative wall time.  It has no
  projector-distance recourse calculation and no reusable scorer interface.
- Root `output.csv` is Git blob
  `0a81ae8d54f363dabacc0a32bcb78eda3732f7cb`, SHA256
  `f7c5408812c9d63d92d16860f385e7dbea31f13de3414bba9306851877dfb801`.
  It has 18 LF terminators comprising 15 nonempty headerless records and three
  empty lines, and is 751,522 bytes.  It carries
  no dataset/configuration/seed/metric schema, no command or code revision, and
  cannot by itself authenticate the native scoring path or map every row to a
  published curve.

## Consequence for admission

The full frozen author tree confirms that the executable empirical material is
the already audited plotting scripts, not an omitted official scorer.  The
scripts' inline `frob_cost_of_proj`, zero-opt fallback, rank/prefix choices,
recourse definitions and timing boundaries remain the only released metric
implementations.  The defects recorded in `BASELINE_AUDIT.md` therefore cannot
be bypassed by selecting another released scorer file.

This narrows the blocker but does not resolve it.  A versioned repaired
evaluator may implement the paper's stated projector loss and recourse, yet it
must first receive independent semantic review and parity/oracle qualification;
it must be labelled a project repair rather than “the official scorer.”  The
archive audit alone does not authorize numerical baseline dispatch or a theorem
claim.

## Independent verdict

Reviewer `/root/author_archive_review` independently re-enumerated the frozen
Git tree and ZIP, normalized CRLF to LF, and checked the exact blobs, hashes and
script behavior against immutable candidate
`39243725f7418e71ef3b1517e6a33787a7c26624` and assignment
`37f5da4394e46b23e0695f4c1bdd104bfe3c350c`.  Verdict: `accepted`.
No code was executed and no files were written.  The reviewer supplied the
non-blocking 15-record/three-empty-line precision correction incorporated
above; the missing-official-scorer conclusion is unchanged.
