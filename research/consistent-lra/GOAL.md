# Initial finite research delegation

## Requested outcome

Starting from Woodruff and Zhou, *Consistent Low-Rank Approximation*, ICLR 2026, seek several scientifically distinct improvements that may support separate papers. The owner requests Research Autopilot's autonomous-rsi branch, background continuation over eight hours, and execution using the GPT environment's CPU.

The goal is a research decision and evidence-backed deliverable. A positive result or a fixed number of papers is not a guaranteed stopping condition.

## Scope and initial assumptions

- Input route: existing published method/code (M audit, followed by new discovery only when qualified).
- Host: current ChatGPT Work managed environment; scientific CPU use explicitly chosen by the owner.
- Resources observed 2026-10-08 23:40 UTC: eight-core CPU quota and 8 GiB memory cap. The nine visible CPUs are not a nine-core quota. Repeat inventory at each actual execution.
- Compute: CPU only; no GPU, paid cloud, additional model API, new service, or arbitrary dependency installation.
- Delivery default: isolated `consistent-lra-rsi` branch and `research/consistent-lra/` directory of existing `Yunbo-max/test10.8`, selected conservatively after the optional destination questions returned no answers. Do not write to that repository's main or the skill repository.
- Hugging Face destination: unresolved; no HF upload or account creation. Small results belong in GitHub; large-asset limits must be stated if they become material.
- Time: one cumulative eight-hour wall-clock window anchored to the actual background task setup timestamp, recorded in BACKGROUND_TASK.json. It is not eight continuously allocated CPU hours. Scheduled invocations and any immediate invocation spend the same window.
- Automatic machine review may return to steps 1/2/3/4/5/6 or eligible writing within this scope. No permission, source qualification, gate, scientific result or budget can be fabricated.

## Earliest obligations

1. Reconcile complete paper/code/native benchmark reading. Source-level implementation defects are already independently audited; empirical qualification is pending.
2. Preserve the original implementation and freeze a separately versioned faithful repair contract for its evaluator/baseline.
3. Establish the parent problem and actual consequential baseline failures under native scoring. Formal assumptions must distinguish additive and multiplicative error.
4. For new method discovery, derive approximately 20 justified mathematical candidates: object, assumptions, actual derivation, constructed method, distinguishing prediction and falsifier. Audit each against current primary papers and code, then independently verify the whole pool and select at most 15 qualified candidates. Do not pad a weak pool or relabel known methods as novel.
5. Generate full implementation and G01 design only for admitted candidates. The initial scope includes all four published experiment families below; access/cost gaps block their actual consumers rather than independent work.
6. Qualify evaluator semantics and numerical accuracy independently, measure real costs, freeze development and separate confirmation protocols, and run only admitted native CPU tasks that fit the remaining window.
7. Apply E04 to real outputs; retain failed, mixed, null, interrupted and unsupported cases. Machine review chooses the next bounded action based on those records.
8. Produce manuscript material only for eligible claims. If multiple contributions do not survive, report the actual surviving count, including zero.

## Native experimental coverage to investigate

This list restores the paper's scope; it is not an approved empirical queue.

| Experiment family | Source identity | Published coverage / unresolved points |
|---|---|---|
| Landmark | SuiteSparse matrix; author `landmark.mtx` at d607c4f6467216c470d1e3b93989d44d5fcdec97 | 71,952 × 2,704; paper first 5,000 rows, k=25. Source processes 4,999; repaired full coverage and independent reference need qualification. |
| Skin Segmentation | UCI Skin_NonSkin; author snapshot at same commit | 245,057 × 3 feature values plus label; published first 3,000, k=1/2. Paper/code subset wording and full-data scaling need reconciliation. |
| Rice Cammeo/Osmancik | UCI ARFF; author snapshot at same commit | 3,810 × 7 numeric features plus class; author first 3,000, k=1. Full-data standardization must be explicit. |
| Published random matrix | Appendix G.1 and author's random scripts | 3,000 × 4 integer entries in [0,100], column transformation. Read and pin the actual generator/seed before claiming reproduction; no new handmade scientific benchmark. |

Inspect capable simple/strong comparators and their actual implementation: faithful Algorithm 4, fresh truncated SVD, qualified Frequent Directions with a proper output rank/sketch size, fixed/periodic refresh controls, and any mechanism-specific prior work. Shared preprocessing, stream prefixes, initialization, error budgets, evaluation denominators and compute allowances are required.

The native core objects are $L_t(P)=\|A_{1:t}(I-P)\|_F^2$ and $R=\sum_{t=2}^n\|P_t-P_{t-1}\|_F^2$. Accuracy and recourse are joint objectives. Runtime must separate algorithm updates from evaluator work. Near-zero optimal residuals require an explicit absolute-error rule, not automatic ratio=1.

## Budget, recovery and completion

Use at most one scientific CPU experiment process at a time until actual resource calibration qualifies more. Cap total numerical threads at the observed quota and leave runtime memory headroom. Freeze actual per-run timeout/RSS and repair bounds before dispatch. Maximum 12 controller rounds across all Step-7 routes, 256 registered tasks, 128 executable attempts, three discovery rounds, three verified failures per scientific direction and two qualified repairs of the same failure within the original wall-clock window. Persist and restore monotonic admitted-task/attempt/round/repair/failure counters, actual usage and unresolved reservations; scheduler ticks are not scientific task completions. Preserve all consumed time and history.

At each milestone save an exact source/evidence artifact and a compact checkpoint. The same actual scheduler task is resumed; do not create a new goal after a failed idea. Reconcile live ownership before another writer or process. Future schedules are hourly, finite and may be delayed by the platform.

Pause after a real blocking dependency once independent authorized work is exhausted, after complete scoped delivery, or when the original eight-hour window ends. On expiry retain complete and incomplete comparisons, exact observed usage, all negative outcomes, manuscript eligibility and the next prerequisite. Do not call an incomplete matrix a completed paper.
