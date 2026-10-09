# Independent corrected integer witness source rereview

Actual assignment **138**, reviewer `/root/integer_source_rereview`, independent of the correction writer. Verdict: **ACCEPT the corrected source for its narrowly specified exact integer construction and publication protocol; no blocking source correction**. This is a source review, not execution, finite-plan admission, output verification, a scientific result, or acceptance of a new method.

Reviewed immutable commit `b62528927acd3a8771fb5269fc1fc945b717eed1`. The source was read directly and its immutable `git show` bytes were independently hashed. I also inspected the exact source diff from rejected original commit `e090716f8febd36360821100d39330b9ab02f45f`. No import, generator invocation, matrix/scoring operation, source edit, vendor edit, acceptance-file change, or publication was performed. Only this scoped review artifact was written for the root integration writer.

| Fixed reviewed artifact | SHA256 |
|---|---|
| `integer_witness_window02.py` | `1e77d985b4b2d1f4ed294dcea7afdce9b2c3c4fae31f81fbea548c6e268e8b8e` |
| Source correction contract | `39257b3cfee0825b1cff3f49e3c2850e9d7ffd6b592b20e26079ffb8c2db897a` |
| Integer witness design | `497b7edd245ae7fe802ca4d7aa92a73c33cd98ced0bc2bf7761ce28f52d2e41f` |
| Original source review, assignment 132 | `b99b3d82cf0dbb825d03752bc3e487c20cc25c091babdeef3009d59884cf3a85` |
| Design review, assignment 130 | `9de2a4f8584a7b72104d6323d057cc44c26e9f03ca373fa14775b10b50600ed3` |
| v7 analytic derivation | `d0f56dbf1ec12c302ad2b42e8ae608a06c9c6c2da63b50da2ee11f6ec8fede79` |
| v7 independent review | `bc239b1819de5657b481bd776a17bc949b4fdf305e9f69d742b92bf23fd9d003` |

## Intended bytes and inventory

The correction initializes an incremental SHA256 and byte counter independently of disk readback. Every serialized row updates both **before** `write_all`; the complete partial file must have that intended length and digest. Decoding then requires equality with the original in-memory rows, ranks `[1,2,61]` in that order, three records, and 256 diagonal-plus-appended integer entries. Full equality additionally protects all coordinate records, products, rounding certificates, flags and provenance, rather than merely the aggregate count. `witness` itself enforces `2*k` coordinate records and `4*k` integers per rank.

After exclusive publication, the returned final length and digest must again match the intended identity. `finalize` also reads the final file and compares its bytes with the partial-file bytes. This closes the original self-hash-only gap: a truncated or changed partial file cannot qualify just because its later copy agrees with it. SHA256 is an integrity identity under its usual collision-resistance assumption, not a mathematical proof of arbitrary I/O correctness.

## Late failure quarantine

Once a success summary exists, a caught late failure reaches the new handler. The handler reads that summary's actual bytes, exclusively hard-links them to `integer-witnesses-summary.failed.json`, compares the failed-file bytes, unlinks the success summary, fsyncs the output directory, and records failed-file length/hash in a separate `success=False` diagnostic. It then reraises the original error. A postpublication record/hash failure or final stdout failure therefore has a nonzero outcome and preserves the summary bytes under an explicit failed name instead of retaining a qualified-looking success summary. Earlier failures preserve partial or final record paths and do not create a success summary. Exclusive directory creation and no-replace links prevent overwriting an earlier attempt.

This acceptance concerns the caught-error path with functioning filesystem operations. The handler itself necessarily uses reads, writes, links and fsync; a further failure of those operations can prevent complete quarantine/diagnostic publication. SIGKILL, power loss, persistent I/O failure, or external mutation are not covered by an unconditional crash-recovery guarantee. The outer harness must collect exit/stderr, actual costs and any remaining artifacts and classify such an attempt as failed or incomplete. Neither a success-named file alone nor the source verdict qualifies execution. This is an operational limit of the current contract, not authorization to ignore a failed cleanup or an unverified output.

## Exact arithmetic and output meaning

The diff leaves the arithmetic and rank set unchanged. Ascending `Lambda` starts at `-16**k`; `Mu` uses exact integer halves. Signed integer products are normalized by `Fraction`, with positive-residue checks before rounding. For positive `r=N/D`, the code uses `q=floor(4*S*S*N/D)`, `n=isqrt(q)` and `m=(n+1)//2`. An integer square threshold cannot be crossed by flooring the nonnegative rational first, so `n=floor(2*S*sqrt(r))`. Thus `m=floor(S*sqrt(r)+1/2)`, including upward half ties. The checked inclusive lower and strict upper bounds are exactly the corresponding half-integer rounding interval; the zero case's lower bound is explicitly zero.

The source retains exact reduced radicands, original signed products, `q`, `n`, `m`, and residuals. Hex encodings avoid loss through floating representation. All emitted matrix entries must be positive Python integers no greater than `257*k*16**k`, with bit length at most `4*k+(k-1).bit_length()+9`. The static k=61 bound is 259 bits. The declared sparse reconstruction, `A=diag(diagonal)` and `T=[A; appended_row]`, supplies all needed integer entries without computing any dense covariance or spectrum. It implies the exact algebraic append identity with a nonzero rank-one row contribution; no measured projector recourse follows from that identity.

Expected successful deliverables are the three-record `integer-witnesses.jsonl`, its integrity-bound summary, and stdout output references. The summary's counts are three rank records and 256 integer entries, with dimensions 2, 4 and 122. Actual integer values, observed maxima, file lengths/digests, runtime and RSS remain unknown until execution and independent evidence review. All scientific, native-evaluator, empirical recourse, eigenvalue, block-condition, novelty, performance and confirmation flags remain false.

I checked correspondence to the v7 construction, not merely a repeated prior verdict. The analytic claims `R_Z>8` at k=61 and ordered-block condition `<4` are **not tested by this generator**. Their existing proof/review lineage stays separate; source acceptance supplies no new empirical support, original-priority determination, approximate-existence refutation, or paper eligibility.

## Costs and remaining admission

No workload was run and no runtime/RSS claim is established here. The internal timer begins after imports, argument parsing and initial output setup; its CPU interval ends before summary publication and postpublication checks. `ru_maxrss` is the process high-water mark rather than an interval delta. The summary labels pipeline time as before-summary time, which is appropriately limited. Full process/harness cost, including startup, final publication, cleanup and failed attempts, must govern actual charging; the failure JSON has no independent full-cost measurement.

The unchanged design proposes one CPU, a 256 MiB reservation (not OS enforcement), fixed ranks, 60 seconds inner/90 seconds outer, one attempt and no retry. This source rereview does not validate an executable timeout or dispatch. The corrected source hash/commit must be bound into the prospective native plan and outer plan reference, followed by the already-required independent plan review and current budget/window/ownership check. Historical source rejection and old-plan identities remain immutable. After any admitted execution, independent output checks must reconstruct exact products/rounding/inventory/size and verify raw hashes, receipt, stderr/exit and total actual costs before accepting evidence.
