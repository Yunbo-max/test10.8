# B10 finite diagnostic reproduction

This reproduces only the finite identity checks, not the literature audit or independent proof review.

```bash
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
python3 -m py_compile verify_candidate_identities.py
python3 verify_candidate_identities.py
```

Expected output artifact: `B10_IDENTITY_CHECK.json`, SHA-256
`48906396167ef87bbd17e29b8d8fd47e242ff1282cb19f478e9e118cf4ee6faf`.

The recorded run used simple-runner source digest
`97cdb752027748261c1d6a11980d10d7a46f2c79c2a00e975f0c08d2c8847893`.
Receipts are included in the raw evidence archive under `runner_receipts/`.

