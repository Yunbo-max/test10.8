# B11 finite diagnostic reproduction

This reproduces only finite algebra checks. It does not reproduce the literature
audit, establish novelty, or authorize candidate implementation.

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 -m py_compile verify_b11_math.py
python3 verify_b11_math.py
```

Expected output: `B11_MATH_CHECK.json`.
