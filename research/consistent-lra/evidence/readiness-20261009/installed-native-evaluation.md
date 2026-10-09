# Existing benchmark evaluation

Apply this contract to every scientific evaluation, including Gate A, development
measurements, debugging runs, controls, and confirmation. Use an existing
published benchmark with released native samples, splits, labels or tests,
scoring, sampling parameters, and budgets. Reuse its official scorer or a
faithful harness verified against that scorer. Never construct a new evaluation
set, substitute handcrafted cases, invent a metric, or write an ad hoc scorer.

Non-evaluation software contract fixtures are separate engineering work. Reuse
existing fixtures to test parsers, authorization, rejection, logging, and bounded
process execution. Do not report fixture literals as scientific scores. The
installed unit tests deliberately use this engineering category and run no
benchmark or GPU workload.

## Frozen contract

Store `native_eval_contract` inline in each scientific protocol before freezing.
Validate it with `scripts/_native_eval.py:verify_protocol(root, protocol)`.
The `native-eval-contract` schema requires:

| Field | Binding |
| --- | --- |
| `benchmark_id`, `benchmark_revision`, `split` | Exact existing published benchmark version and native split |
| `published_source_refs`, `native_definition_ref` | Retained authentic official source captures and their hashes |
| `sample_manifest_ref`, `labels_or_tests_ref` | Released native sample identities and original labels or test cases |
| `primary_metric`, `metrics` | Official primary metric and every declared metric, each with an explicit native JSON `output_path` |
| `prediction_format` | Native JSON/JSONL record location and sample-ID path |
| `sampling`, `budget` | Original native policy, parameters, and resource limits |
| `scorer` | Official identity, revision, code/source refs, existing argv, working directory, output format, and denominator path |
| `contrasts`, `arm_requirements` | Frozen treatment, baseline, and all controls, including implementation revisions and refs |
| `baseline_qualification`, `control_qualifications` | Native metric thresholds with source refs; applied to replayed outputs |

`native_definition_ref` points to a captured upstream definition normalized into
an identity sidecar: benchmark identity, publication date/URL, official primary
metric and metric paths, released split refs, prediction format, native
sampling/budget, official scorer, and publication refs. Preserve the original
upstream artifacts behind its source refs. This is an adapter for existing
definitions; filling a sidecar with invented facts does not create a benchmark.
The host must acquire and authenticate these sources. Offline hash checking alone
does not establish their upstream authenticity.

The native sample manifest records benchmark identity, split, `sample_ids`,
`denominator`, `predictions_per_sample`, original labels/tests ref, and native
sampling/budget. Every receipt must match this manifest. Prediction IDs and
multiplicity must match released IDs exactly. Missing predictions, additional
handcrafted cases, changed denominators, altered sampling/budgets, and substituted
labels or tests are rejected.

For full validation across multiple existing benchmarks, optionally provide
`native_eval_contracts` keyed by exactly every `required_groups` value. Keep the
scalar `native_eval_contract` as one declared primary contract. Each group uses
its own released benchmark identity, split, metric definitions, sampling, budget,
and official scorer. A criterion's `groups` must select only contracts exposing
that native metric; default criteria apply to all groups. `contract_for_group`
selects the exact group contract, and `verify_run` binds it to the manifest group.
No group may borrow another benchmark's metric or receipt.

## Native subsets for Gate A

When the existing scorer supports subset evaluation, freeze an optional
`selection` descriptor. Keep `sample_manifest_ref` bound to the released full
manifest; store the derived manifest in `selection.selected_manifest_ref`.
Bind `source_manifest_ref`, `rule` (`prefix` or `sha256_rank`), integer `seed`,
positive `count`, and a sourced `capability_ref` before examining results.

The upstream definition must declare `subset_capability` with `allowed_rules`,
`denominator_rule: sample_count`, and the same official `source_ref`. The verifier
reconstructs selection from released IDs and rejects every other subset. Hash
selection sorts by SHA-256 of canonical JSON `[seed, sample_id]` and takes the
first `count`; prefix selection uses original native order. Labels/tests,
prediction multiplicity, sampling, budgets, metric definitions, and scorer remain
native. Other denominator rules need a versioned official adapter and currently
block. Restrict claims to the returned `evaluation_scope`.

## Receipts and live scorer replay

`verify_run(root, protocol, manifest, replay_context=None)` requires
`manifest.native_eval_receipts` keyed by `treatment`, `baseline`, and every
declared control role. Each `native-eval-receipt` binds protocol/contract/run
identities, seed/group, arm implementation, effective sample and label/test refs,
denominator, prediction output ref, sampling/budget/resources, scorer revision and
code, recorded native metrics, and retained raw/native outputs.

A static JSON receipt, matching hash, or `baseline_qualified` /
`positive_control_passed` boolean cannot certify scorer recomputation. Without a
live callable injected by an authorized trusted host, verification raises
`NATIVE_SCORER_REPLAY_REQUIRED`; gate evaluation must return `INCONCLUSIVE`.
The host callable receives a fresh nonce, request digest, exact pinned command,
input/code refs, and native budget. It must execute the existing scorer and return
nonce-bound execution identity, exit code, timestamps, actual argv/cwd, input/code
bindings, and stdout/stderr/native-output refs. Copied static results lack these
live bindings and raise `NATIVE_SCORER_REPLAY_NOT_LIVE`.

The verifier parses only frozen paths from native scorer output. It computes no
replacement metric. It checks the native denominator, compares replayed metrics
with recorded native metrics, and rechecks frozen input/code/proof hashes after
execution. Baseline and control qualification come from the replayed native
values and their predeclared source-backed rules.
When arm resource consumption differs, bind `manifest.native_arm_resources`
by every declared arm role; receipts must match that role's telemetry and each
native budget. Without it, receipts bind the manifest's common resource record.

For `faithful_harness`, require a `verification_ref` binding the official and
harness scorer identities/code, released sample manifest, source refs, and
metric tolerances. Tolerances are zero unless the native definition explicitly
declares matching tolerances. Replay both pinned scorers on each arm's same
native predictions. Reject disagreement; accepted metric values come from the
official scorer. Neither a parity boolean nor a saved parity output suffices.

The return object includes native paired `metrics`, `arm_metrics`, computed
qualification flags/control results, deterministic frozen `proof_refs`, and
`evaluation_scope`. Fresh execution records are returned separately as
`replay_audit`; retain them in runtime audit storage without including their
random paths in deterministic gate IDs. No verifier advances a research gate.
