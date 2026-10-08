# Multi-Dataset SFT Research

Researching supervised fine-tuning across heterogeneous datasets under a single RTX 2080 Ti with **22 GB of user-reported VRAM**.

## Project brief

- Goal: study new-domain capability acquisition while retaining existing capabilities without dedicated training exposure, within multi-dataset SFT and public benchmark evaluation. This research direction was selected by the owner on 2026-10-08; a new method has not yet been selected.
- Scope: mixed-dataset training **and** evaluation across datasets, confirmed by the owner on 2026-10-08.
- Hardware: **one** RTX 2080 Ti, 22 GB VRAM; host inventory and throughput have not yet been measured.
- Local execution: at most **24 elapsed hours per approved cycle**, with progress reports approximately every 8 hours.
- Delivery: this repository, `main`. Hugging Face outputs are explicitly not used for this project at present.
- Roles: Web reviews sources and prepares research/code/design; Local qualifies and executes scientific work on the owner's separate host.
- Environment preference: native Conda; no containers.

## Read first

- [Selected research direction and discussion (中文)](docs/RESEARCH_DIRECTION.zh-CN.md)

1. [Research start and frontier review (中文)](docs/RESEARCH_START.zh-CN.md)
2. [Paper, implementation, and evaluator audit](docs/SOURCE_AUDIT.md)
3. [Sourced project intake](docs/RESEARCH_INTAKE.md)
4. [Current workflow checkpoint](workflow-checkpoint.yaml)

## Current status

The startup source audit and the owner-selected acquisition–retention direction are documented. Actual source coverage and open obligations are listed in the audit. The repository contains research notes and a checkpoint. Candidate derivations, originality adjudication, method selection, implementation, the complete evaluation design, and Local acceptance remain pending.

No training, inference, scientific tests, or evaluations have been executed for this project. Published results in the review belong to their original authors.

The next step is to establish the residual failure and formal research question against the inspected comparators, extend closest-work coverage, and derive/review the candidate pool before selecting methods for implementation. Full comparisons may span multiple Local cycles; a reporting interval does not make a partial comparison complete.
