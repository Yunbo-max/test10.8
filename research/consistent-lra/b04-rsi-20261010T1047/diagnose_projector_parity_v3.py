import json
import os
import pathlib
import resource
import time

for variable in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[variable] = "1"

import numpy as np

from atomic_npz import atomic_write_json, sha256

HERE = pathlib.Path(__file__).resolve().parent
wall0 = time.perf_counter()
cpu0 = time.process_time()
rows = []
with np.load(HERE / "LANDMARK128_RAW_V3.npz", allow_pickle=False) as z:
    a = z["a"]
    energy = np.sum(a * a, axis=1).cumsum()
    for eta in (0.01, 0.1):
        old = f"old_eta{eta:g}"
        new = f"new_eta{eta:g}"
        for index, prefix in enumerate(z["checkpoints"]):
            Q = z[f"{old}_basis"][index]
            V = z[f"{new}_basis"][index]
            singular = np.linalg.svd(Q.T @ V, compute_uv=False)
            spectrum = np.linalg.svd(a[:prefix], compute_uv=False)
            gap = float(spectrum[24] - spectrum[25]) if len(spectrum) > 25 else None
            rows.append({
                "eta": eta,
                "prefix": int(prefix),
                "projector_difference": float(np.linalg.norm(Q @ Q.T - V @ V.T)),
                "max_principal_sine": float(np.sqrt(max(0.0, 1.0 - float(np.min(singular)) ** 2))),
                "loss_difference": float(abs(z[f"{old}_loss"][prefix - 1] - z[f"{new}_loss"][prefix - 1])),
                "relative_loss_difference_to_energy": float(abs(z[f"{old}_loss"][prefix - 1] - z[f"{new}_loss"][prefix - 1]) / max(1.0, energy[prefix - 1])),
                "singular_gap_25_26": gap,
                "sigma25": float(spectrum[24]),
                "sigma26": float(spectrum[25]) if len(spectrum) > 25 else None,
            })
rows.sort(key=lambda item: item["projector_difference"], reverse=True)
out = {
    "scope": "post-second-repair diagnosis of the still-failed frozen first128 parity predicate; no threshold revision or retry",
    "raw_sha256": sha256(HERE / "LANDMARK128_RAW_V3.npz"),
    "parent_v2_diagnosis_sha256": sha256(HERE / "PROJECTOR_PARITY_DIAGNOSIS.json"),
    "maximum": rows[0],
    "top_differences": rows[:10],
    "usage": {
        "wall_seconds": time.perf_counter() - wall0,
        "cpu_seconds": time.process_time() - cpu0,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    },
}
atomic_write_json(HERE / "PROJECTOR_PARITY_DIAGNOSIS_V3.json", out)
print(json.dumps(out))
