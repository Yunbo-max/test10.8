"""Regression checks for the stable low-memory projector metric."""
import json
import pathlib
import resource
import time

import numpy as np

from projector_metric import projector_frobenius

HERE = pathlib.Path(__file__).resolve().parent


def dense(q, v):
    q = np.linalg.qr(q, mode="reduced")[0]
    v = np.linalg.qr(v, mode="reduced")[0]
    return float(np.linalg.norm(q @ q.T - v @ v.T, ord="fro"))


def old(q, v):
    return float(np.sqrt(max(0.0, q.shape[1] + v.shape[1] - 2.0 * np.square(q.T @ v).sum())))


def main():
    wall0, cpu0 = time.perf_counter(), time.process_time()
    resource.setrlimit(resource.RLIMIT_AS, (2 * 1024 ** 3, 2 * 1024 ** 3))
    rng = np.random.default_rng(20261010)
    synthetic = []
    for d, k, scale in ((64, 5, 0.0), (64, 5, 1e-12), (64, 5, 1e-8), (64, 5, 1e-4), (100, 25, 1e-8)):
        q = np.linalg.qr(rng.standard_normal((d, k)), mode="reduced")[0]
        v = q + scale * rng.standard_normal((d, k))
        stable = projector_frobenius(q, v)
        reference = dense(q, v)
        synthetic.append({"d": d, "k": k, "scale": scale, "stable": stable, "dense": reference,
                          "absolute_error": abs(stable - reference)})
    with np.load(HERE / "LANDMARK128_RAW_V3.npz", allow_pickle=False) as z:
        real = []
        for eta in ("0.01", "0.1"):
            for prefix, q, v in zip(z["checkpoints"], z[f"old_eta{eta}_basis"], z[f"new_eta{eta}_basis"]):
                stable = projector_frobenius(q, v)
                real.append({"eta": eta, "prefix": int(prefix), "stable": stable, "old": old(q, v)})
    checks = {
        "synthetic_dense_agreement": max(x["absolute_error"] for x in synthetic) <= 5e-12,
        "identity_is_near_roundoff": synthetic[0]["stable"] <= 1e-13,
        "real_max_matches_independent_verifier": abs(max(x["stable"] for x in real) - 2.4943901584177335e-08) <= 5e-15,
        "real_old_false_positives_reproduced": sum(x["old"] > 1e-8 and x["stable"] <= 1e-8 for x in real) == 4,
        "real_old_false_negatives_reproduced": sum(x["old"] <= 1e-8 and x["stable"] > 1e-8 for x in real) == 5,
    }
    out = {
        "checks": checks,
        "pass": all(checks.values()),
        "synthetic": synthetic,
        "real_summary": {"pairs": len(real), "max": max(x["stable"] for x in real),
                         "old_false_positives": sum(x["old"] > 1e-8 and x["stable"] <= 1e-8 for x in real),
                         "old_false_negatives": sum(x["old"] <= 1e-8 and x["stable"] > 1e-8 for x in real)},
        "usage": {"wall_seconds": time.perf_counter() - wall0, "cpu_seconds": time.process_time() - cpu0,
                  "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
    }
    (HERE / "PROJECTOR_METRIC_TEST.json").write_text(json.dumps(out, indent=2, allow_nan=False) + "\n")
    print(json.dumps(out, allow_nan=False))
    if not out["pass"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
