# Evaluator semantic-oracle execution record

Status: completed engineering software check; independent evidence review
accepted after a recorded ledger correction. This is not an official scorer, native benchmark, performance result,
scientific experiment or gate pass.

## Admission

- Corrected code/plan candidate: `6f104ad753ffe0fc441265405072b39bc4fe5590`.
- Independent correction-rereview binding:
  `39947aebe92eb798a653e4219e1ae659bc81b64f`, verdict `accepted`.
- Native plan digest:
  `902f36cff8bfb36f13ace951719272e7dcd703a0709d67653dc284284663fdd5`.
- Harness plan digest:
  `843f8fa71948b3881471889efb3c74a4d4c87238d5564ac2c5fe667cee94516a`.
- Host at launch: cgroup `cpu.max=800000 100000` (8-core quota),
  `memory.max=8589934592`; no GPU. OMP/MKL/OpenBLAS/NumExpr thread variables
  were set to 1 in the controller command, but are not captured in the frozen
  execution context, so OS-affinity/one-thread enforcement is not claimed.

## Actual attempt

- Run: `evaluator-semantic-oracles-01`.
- Attempt: `evaluator-semantic-oracles-a1-b267edcdcc43454daba166caf666a2d2`.
- One attempt, retry index 0, exit code 0, empty stderr.
- Command: installed primary-runtime Python,
  `evaluator_semantic_oracles.py --output evidence/qualification/evaluator-semantic-oracles.json`.
- Output SHA256:
  `ee7870a3b84bb4cafaa6732c03cd4489663b691be9ece43b1b7330e5ce1cdef3`.
- Receipt SHA256:
  `cebc7c5a7fe9e8c31c0f497bc90fa4c1afd797fc0517ddd896280ae636d167fa`.
- Attempt SHA256:
  `b9267a37754bc2cc5970837c471373064b93fd2d9113477f6fab8017bd77cec8`.
- Process-guard SHA256:
  `eb5d760cfa9ae484d19bcfc5dc77c0159502bf136dc8881ff13ef9d45764e419`.
- Stdout/stderr SHA256:
  `f6571f794350894977e5531e73005697f8e829967ad06270b8dd50f446b5339b` /
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

The JSON reports 25 checks, zero failures. All analytic expected values are
exact except floating-point differences at most about `1.1e-14`, within the
predeclared tolerances. It records Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0
and scikit-learn 1.8.0. The in-process metric work used 0.001427 CPU seconds,
0.001842 wall seconds and peak RSS 114,008 KiB. The guarded attempt wall time
was 1.016842 seconds; harness wall time was 2.007363 seconds.

## Exact scope

The observed output supports only finite software identities for direct versus
trace loss, fresh-SVD tail versus projector loss, and overlap versus explicit
projector recourse, including rank-changing and separately reported
initialization cases. It does not establish author-exact parity because the
frozen author archive supplies no separate scorer. It does not test native
total streaming recourse, Frequent Directions, baseline performance or any new
method. `gate_advanced=false`, `scientific_result_verified=false`, and the
scientific-attempt count remains zero.

Independent evidence review first returned `needs_correction` because the
frozen budget/checkpoint predated execution. Corrected candidate
`a63878b314df9113bc2c60a2dcd8656cf7207e3c` monotonically updated the ledger
without changing raw evidence; rereview binding
`9736a2207b2430b6514e34fd52daf112520b6d77` was accepted.
