# Independently reviewed B03 RSI engineering variant

Unique study: `B03-RSI-independent-20261010T0952`. See [Chinese report](REPORT.zh-CN.md). This variant does not replace the distinct primary scheduled B03 solver stored in main index v15.

The 30-cell parity check and 450 whole-method timings were independently audited from retained outputs. Timing benefit over legacy is partial; no cell beat certified_full. No novelty, global-recourse theorem, independent rerun, untouched confirmation, or completed-paper claim.

## Reproduce after restoring inputs

Use the installed Python/library versions in ENVIRONMENT.json; no dependency installation was performed. Restore the exact raw evidence archive identified by RAW_EVIDENCE.json into this directory's parent. It supplies data/, parity/, the complete TIMING.json, and original attempt logs. Source and audit documents are Git-backed. Verify both manifests before executing.

From this directory, with at most one numerical process and the fixed limits in B03_DESIGN/V2:

```bash
PYTHONPATH=baseline python3 test_solver.py
python3 validate_and_time.py parity
python3 validate_and_time.py timing
```

The last two commands write outputs; use a fresh execution directory and new finite task identity, preserving original evidence. The original unit script also has a historical sibling-path lookup; PYTHONPATH=baseline makes its unchanged source portable. The baseline file is byte-identical to B01. Numerical threads and a 2GiB address-space cap are enforced by the native harness; the timing command requires the exact passed parity/source/data identities.

B03_DESIGN_V2.md corrects the initial draft's endpoint and residual-stop rules. The predispatch review geodesic_math_review.md is frozen; INDEPENDENT_REVIEW.md appends parity and timing outcomes. Five timing repeats are not independent datasets. Shared-host exclusivity across other conversations is not established.

The same recurring project continues using the merged latest index and STEP7_DECISION.json. Archived local runner state is stopped; it is not a deployed autonomous daemon.
