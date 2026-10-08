# Continual LLM Updates: Acquisition and Retention

Researching continual LLM updates on text and supervision arriving over time, with a single RTX 2080 Ti and **22 GB of user-reported VRAM**.

## Project brief

- Goal: absorb arriving knowledge and skills while preserving still-valid knowledge, historical answers, and existing capabilities. The owner clarified on 2026-10-08 that temporal data means text arriving over time. Continual SFT and time-incremental continued pretraining are the routes under discussion; a new method has not been selected.
- Scope: chronological updates across text/ supervision sources, retaining the multi-dataset training and evaluation context. Access to prior incremental data and replay remains unresolved.
- Hardware: **one** RTX 2080 Ti, 22 GB VRAM; host inventory and throughput have not yet been measured.
- Local execution: at most **24 elapsed hours per approved cycle**, with progress reports approximately every 8 hours.
- Delivery: this repository, `main`. Hugging Face outputs are explicitly not used for this project at present.
- Roles: Web reviews sources and prepares research/code/design; Local qualifies and executes scientific work on the owner's separate host.
- Environment preference: native Conda; no containers.

## Read first

- [Latest clarification: temporal text, forgetting, and research directions (中文)](docs/STREAMING_RESEARCH.zh-CN.md)
- [Selected acquisition–retention direction (中文)](docs/RESEARCH_DIRECTION.zh-CN.md)

1. [Research start and frontier review (中文)](docs/RESEARCH_START.zh-CN.md)
2. [Paper, implementation, and evaluator audit](docs/SOURCE_AUDIT.md)
3. [Sourced project intake](docs/RESEARCH_INTAKE.md)
4. [Current workflow checkpoint](workflow-checkpoint.yaml)

## Current status

The startup source audit, owner-selected acquisition–retention goal, and chronological-text clarification are documented. The latest note joins scoped reads of recent papers, pinned author code, and native KairosQA loading/scoring contracts. Actual source coverage and open obligations are listed in the audit. The repository contains research notes and a checkpoint. Candidate derivations, originality adjudication, method selection, implementation, the complete evaluation design, and Local acceptance remain pending.

No training, inference, scientific tests, or evaluations have been executed for this project. Published results in the review belong to their original authors.

The next step is to establish the residual failure and formal research question against the inspected comparators, extend closest-work coverage, and derive/review the candidate pool before selecting methods for implementation. Full comparisons may span multiple Local cycles; a reporting interval does not make a partial comparison complete.
