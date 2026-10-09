# Independent plan review: author FD semantic oracles

Reviewer: `/root/rice_skin_plan_review`  
Pinned review commit: `a1d78b55391bf444da5a7a9ca37647fb061a20c6`  
Verdict: **accepted** for one bounded engineering-developmental execution.

The reviewer executed no project code and made no edits, commits, or
publications.  It recomputed and matched:

- native plan SHA256
  `53e7cba2ef4d5c5d7490d7bab49f888390e86c5120853d6dd4d979a599fc09cd`
  and digest
  `76902a7380dc9226f322fc0657477dc3606ef7b593c945c0892d6945274fe52d`;
- harness plan SHA256
  `881a3cabb9f4a9fad46a24fa22dd8eef2a7020f6fd9d46d6458a0cfb9a819a02`
  and digest
  `97897df281b1ad2904f60db7ac863cab8f1ec07e11904b7a27e3bfd94f212d22`;
- every declared input/code hash, including frozen author blob
  `294438ac128556f01a2c3d920bdb4f1225dd819f` and source SHA256
  `ba16f17017005dfc90d7ff669678911b2b3e6211582efd4014ed592e44926990`.

The immutable argv binds OpenBLAS, OMP, MKL, NumExpr, and vecLib thread counts
to one before importing Python.  Admission is one CPU, 256 MiB, one attempt,
zero retry, 30 seconds native and 45 seconds outer, with no GPU, network,
installation, or service.  The pool path exists under the intended checkout,
and the single declared JSON output matches the oracle.

CPU and RAM values are harness admission reservations, not OS affinity or
`RLIMIT` enforcement.  Acceptance is plan admission only.  Any receipt and
output require separate independent evidence review.  This task cannot support
published recourse parity, strong-FD status, native benchmark performance,
theorem validity, G01/E04/Gate A, or paper claims.
