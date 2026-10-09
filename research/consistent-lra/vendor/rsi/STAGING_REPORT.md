# Pinned CPU harness source staging

This is a project-local source copy, not a shared skill installation, daemon, ACP controller, scientific execution, or gate approval.

Source: Yunbo-max/Research_Autopilot at immutable commit 1de12dfed5b84957b29ac5b3a2f04904bf3742bc. SOURCE_MANIFEST.json records every copied repository path, connector Git blob SHA, independently recomputed local Git blob SHA verification, byte length, and SHA256. All 31 copied files passed byte-identity checks; Python was parsed as source with ast.parse and schemas were parsed as JSON without importing or executing the copied modules.

## Dependencies and limits

The CPU harness requires Linux/POSIX, Python 3.11 or newer, standard-library fcntl/signals/subprocess, /proc process/boot identities, and writable project-local output/pool directories. JSON plans require no third-party package. Non-JSON YAML optionally uses the already-installed PyYAML. Optional statistical helpers use existing numpy/scipy. No package, environment, service, or skill was installed.

The fetched transitive local modules are included. GPU memory-profile support is deliberately outside this CPU packet. Source snapshots are not an OS sandbox. GitHub repository metadata reported license=null; this staging does not assert a redistribution license or alter ownership.

The source's --inspect-host reports CPU affinity and host MemAvailable, not cgroup CPU quota or memory cap. The parent must separately recheck the actual cgroup envelope. Harness CPU/RAM reservations do not enforce OS partitions or BLAS thread limits. Cap reviewed numerical thread environment variables, retain headroom below the current 8 GiB cap, and collect actual CPU time/RSS through the reviewed workload. Native receipts record wall time but do not themselves supply CPU/RSS measurements.

The original deadline is 2026-10-09T07:47:45Z. Each new outer total_wall_seconds and inner wall_time_seconds/attempt_timeout_seconds must fit the actual remaining window with at least five minutes for collection. The native/harness deadlines are monotonic relative bounds; they do not automatically consult BACKGROUND_TASK.json.

## Native plan API

run_experiments.make_plan(root, run_id=..., jobs=..., provenance=..., limits=..., purpose=..., evidence_mode=..., protocol_ref=..., output_root=...) validates and returns the canonical plan_digest. run_experiments.validate_plan(root, plan) is read-only. There is no separate preparation/qualification purpose enum: only engineering and scientific.

A mechanical preparation job may use purpose=engineering, evidence_mode=developmental, protocol_ref=null, protocol_digest=null. It can materialize already authorized source inputs or inspect integrity/environment metadata. It cannot establish baseline/scorer semantic or native scientific qualification.

A numerical baseline/evaluator qualification job must use purpose=scientific with a real pinned protocol and complete native_eval_contract. An actual existing-method audit protocol with no method_discovery does not require fabricating a new candidate pool. Omitting method_discovery from a new-method protocol would evade the admission contract and is prohibited.

Every job requires stable trial_id, argv command, project-relative cwd, pinned input_refs and code_refs, declared output_paths, seed, group and arm_role. References have real existing project-relative paths and SHA256. The job is copied into an isolated attempt workspace; declared absolute input/code path arguments are rewritten to the staged copies. Pin imported project modules and file dependencies as well as the entry point. Outputs cannot overwrite pinned inputs. Jobs must remain foreground processes.

Provenance requires git_revision, model_revision, data_revision and environment_digest; optional git_refs/model_refs/data_refs/environment_refs bind retained identity manifests. Use an explicit sourced no-model value when appropriate, not a fabricated model revision. Limits require max_attempts, max_development_trials, max_confirmation_trials, max_retries_per_trial, wall_time_seconds and attempt_timeout_seconds. Start with one admitted attempt and zero automatic retries. Confirmation and retrospective audit cannot retry.

A scientific protocol must bind the native published definition/publication bytes, ordered sample manifest and labels/tests, authentic benchmark/revision/split, exact primary/secondary metrics and denominators, budget/sampling/prediction format, reviewed scorer and implementation bytes, seed/group inventory, declared baseline/treatment/control arms, and prospective qualification predicates/source references. A faithful scorer additionally requires independent source-bound verification and sourced tolerances. Generated scorer metadata cannot be labeled an official published scorer to satisfy the schema. These are still pending; no protocol was created by this staging task.

## Outer harness requirements

run_harness.make_plan(root, batch_id=..., tasks=..., pool_dir=..., limits=..., gpus=..., output_root=...) returns a validated digested harness plan.

Each task needs task_id, idea_id, a path/SHA256 plan_ref to an existing validated native plan, depends_on, priority and resources. CPU resources: cpu_cores and ram_mib within observed remaining headroom; gpu_count=0; gpu_peak_mib=null; allow_gpu_share=false; memory_profile_ref=null; exclusive_keys covering shared mutable assets.

Outer limits: window_seconds, total_wall_seconds, max_parallel_tasks=1, cpu_cores <= actual quota, ram_mib below actual available cap/headroom, max_gpu_task_seconds=0. GPU inventory: uuids=[], safety_margin_mib positive, max_tasks_per_gpu=1. Set an absolute project-local pool_dir, not a new shared-service path. Register/reserve the actual task/attempt budget before execution.

## Commands for the parent

The source inspection command is ready and launches no workload:

```bash
python3 /workspace/scratch/bb9f262965cf/research/consistent-lra/vendor/rsi/scripts/run_harness.py --inspect-host
```

After the parent has authored and independently reviewed real native and outer plan files, validate/freeze using the exact paths below (the plan files have not been created by this staging task):

```bash
python3 /workspace/scratch/bb9f262965cf/research/consistent-lra/vendor/rsi/scripts/run_experiments.py /workspace/scratch/bb9f262965cf/research/consistent-lra/plans/native-qualification.json --root /workspace/scratch/bb9f262965cf/research/consistent-lra
python3 /workspace/scratch/bb9f262965cf/research/consistent-lra/vendor/rsi/scripts/run_harness.py /workspace/scratch/bb9f262965cf/research/consistent-lra/plans/harness-qualification.draft.json --root /workspace/scratch/bb9f262965cf/research/consistent-lra --freeze > /workspace/scratch/bb9f262965cf/research/consistent-lra/plans/harness-qualification.reviewed.json
python3 /workspace/scratch/bb9f262965cf/research/consistent-lra/vendor/rsi/scripts/run_harness.py /workspace/scratch/bb9f262965cf/research/consistent-lra/plans/harness-qualification.reviewed.json --root /workspace/scratch/bb9f262965cf/research/consistent-lra
```

Execution is only through this outer harness with --execute --approved-plan-digest followed by its actual reviewed digest. Keep the one owner/pool, reviewed thread environment and original deadline. This staging task executed none of those commands.

Resume the same reviewed batch and digest only after actual host/process/receipt reconciliation. --status reads retained state and is not fresh liveness proof. Uncertain launch identity parks rather than retrying with a new batch. Do not use --stop-after-report merely to abandon active work at a chat boundary; retained workers still consume the original deadline. Collect receipts, stdout/stderr, context/process identities, declared output hashes and adverse attempts before ending. Successful exit is execution completion only; E04 and independent native verification remain required.
