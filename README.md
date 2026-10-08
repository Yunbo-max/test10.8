# Continual LLM Updates: Acquisition and Retention

Researching continual LLM updates on text and supervision arriving over time, with a single RTX 2080 Ti and **22 GB of user-reported VRAM**.

## Project brief

- Goal: absorb arriving knowledge and skills while preserving still-valid knowledge, historical answers, and existing capabilities. The owner clarified on 2026-10-08 that temporal data means text arriving over time. The owner has agreed to two analytical routes: protection coverage for untrained capabilities and selective preservation during temporal knowledge updates. Continual SFT is the main setting; time-incremental document adaptation supplies related comparators. A new method has not been selected.
- Scope: chronological updates across text/ supervision sources, retaining the multi-dataset training and evaluation context. Access to prior incremental data and replay remains unresolved.
- Hardware: **one** RTX 2080 Ti, 22 GB VRAM; host inventory and throughput have not yet been measured.
- Local execution: at most **24 elapsed hours per approved cycle**, with progress reports approximately every 8 hours.
- Delivery: this repository, `main`. Hugging Face outputs are explicitly not used for this project at present.
- Roles: Web reviews sources and prepares research/code/design; Local qualifies and executes scientific work on the owner's separate host.
- Environment preference: native Conda; no containers.

## Read first

- [Two-route mathematical analysis: six conditional inquiry records (中文)](docs/TWO_ROUTE_MATH_ANALYSIS.zh-CN.md)
- [Two-route primary papers and pinned source-code audit (中文)](docs/TWO_ROUTE_SOURCE_CODE_AUDIT.md)
- [Unlearning, SFT, retention and recovery: connected-work review (中文)](docs/UNLEARNING_CONNECTION.zh-CN.md)
- [Direction and first mathematical inquiry records (中文)](docs/DIRECTION_AND_MATH_START.zh-CN.md)
- [Uploaded paper review: Finetuning with Sampling and implications (中文)](docs/SAMPLING_SFT_REVIEW.zh-CN.md)
- [Latest clarification: temporal text, forgetting, and research directions (中文)](docs/STREAMING_RESEARCH.zh-CN.md)
- [Selected acquisition–retention direction (中文)](docs/RESEARCH_DIRECTION.zh-CN.md)

1. [Research start and frontier review (中文)](docs/RESEARCH_START.zh-CN.md)
2. [Paper, implementation, and evaluator audit](docs/SOURCE_AUDIT.md)
3. [Sourced project intake](docs/RESEARCH_INTAKE.md)
4. [Current workflow checkpoint](workflow-checkpoint.yaml)

## Current status

The owner has agreed to analyze protection coverage and selective temporal preservation before developing new methods. The first mathematical pass now contains six conditional inquiry records: distribution/Fisher coverage, distillation targets and anchor boundaries, OSFT's actual projection geometry, TALR's update rule, temporal conditioning versus shared-parameter interference, and AlphaEdit's approximate-null-space editing feasibility.

Eight directly relevant works are indexed with actual read scope. Five author algorithm repositories are pinned; the DiSC repository also provides a third-party TALR baseline. The inspected AToKe and MTKE author releases contain datasets, without the corresponding METO/SPIKE algorithm implementations. Paper versions, current code, and incomplete native data/scorer contracts are distinguished.

The repository contains research notes and a checkpoint. The conditional derivations are conceptual analyses, not an empirically qualified new method pool or an originality verdict. No training, inference, scientific tests, numerical checks, or evaluations have been executed for this project. Published results belong to their original authors.

The next step is to establish a consequential residual problem against strong and simple methods, qualify native data/scoring and training-information access, and calibrate single-card costs. Only then should the project invest in empirical method candidates and complete mathematical review/ranking before new-method implementation. Full comparisons may span multiple Local cycles; a reporting interval does not make a partial comparison complete.
