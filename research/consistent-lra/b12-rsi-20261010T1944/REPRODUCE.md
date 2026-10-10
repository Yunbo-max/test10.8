# B12 finite diagnostic reproduction

Set all numerical thread controls to one, then run through the pinned local
Simple command transport:

```bash
python3 -m py_compile verify_b12_boundary.py
python3 verify_b12_boundary.py
```

The commands only check deterministic finite consequences of Theorem B12.1.
They are not a proof, novelty evidence, or a native Landmark benchmark.
