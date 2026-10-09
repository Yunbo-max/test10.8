# Published random-family identity boundary

Status: source/provenance qualification only. This is not a numerical result,
an official-scorer parity result, or a replacement benchmark.

## Frozen sources

- Paper: *Consistent Low-Rank Approximation*, Appendix G.1, proceedings PDF
  `b14d76c7266be21b338527cd25deac45-Paper-Conference.pdf`.
- Author repository: `samsonzhou/consistent-LRA` at
  `d607c4f6467216c470d1e3b93989d44d5fcdec97`.
- Released 3,000 by 4 generator:
  `consistent-lra-random.py`, Git blob
  `cfe96c16b699a96720e41cc36ab36a25a45b4627`, SHA256
  `32bda4b19dcb2b9a9bfc344092a45ce12126fd1591e3202bc5f40b726b22bd7b`.
- Released fast diagnostic:
  `consistent-lra-random-fast.py`, Git blob
  `4edc0664ac183391af3a761e429c67947a61cc1e`, SHA256
  `b570e0ae0b760d02973a4dde6e9b6e502f57c4759608d264ec39278c30a0d99d`.

## What the released code determines

The 3,000 by 4 script calls the module-global Python `random.randint(0,100)`
once per entry in row-major order. Endpoints are inclusive. It then converts
the nested list to a NumPy array and performs no transformation before the
prefix loop. The script contains no call to `random.seed`, does not serialize
the generated matrix or PRNG state, and writes no machine-readable result.
Consequently it fixes a generator family and draw order, but not the exact
matrix used for the published figure.

The fast script is a different diagnostic: 3,000 by 100, rank 20, `c=10`, and
`sklearn.utils.extmath.randomized_svd(..., random_state=None)`. It has a second
unrecorded random source and cannot stand in for the Appendix G.1 3,000 by 4
experiment.

## Unresolved paper/code join

Appendix G.1 describes a column-normalized random matrix, whereas the released
3,000 by 4 code scores the unscaled integer matrix. Neither source specifies a
normalization formula, fitted constants, the original matrix, a Python version,
or a seed. “Column normalized” is insufficient to distinguish unit-L2 column
normalization from centering/scaling or another convention. No unique byte
stream or unique transformed matrix can therefore be reconstructed from the
released evidence.

This is an irrecoverable provenance gap for exact figure replication unless an
additional upstream artifact appears. It is not evidence that the paper's
reported qualitative behavior is false.

## Admissible future use

`native_baselines.py` may generate a **prospective code-compatible family
instance** with a predeclared integer seed via
`random.Random(seed).randint(0,100)` in the released row-major order. Such an
instance must be labeled unscaled and `original_figure_replication=false`.
It is suitable only after evaluator qualification and protocol admission; it
cannot be presented as the original figure stream.

No normalized variant is admitted under the present record. A future protocol
may predeclare an explicit transformation as a new diagnostic, but must call it
a project-defined interpretation rather than an author-exact reproduction and
must not choose the interpretation after inspecting comparative results.

## Consequences for G01

- Keep the published random family in the required four-family coverage table.
- Mark exact Appendix G.1 replay unavailable, not silently deleted.
- Keep unscaled prospective seeds separate from any project-defined normalized
  diagnostic.
- Freeze seeds and transformations before results; adjacent prefixes are not
  independent replications.
- Do not use the fast 100-dimensional diagnostic to fill the 4-dimensional
  coverage requirement.

This closes the source-identity question only by establishing a precise
non-replication boundary. It does not close evaluator parity, baseline
qualification, G01, E04, Gate A, or any paper claim.
