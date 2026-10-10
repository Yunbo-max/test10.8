"""B09 exact-query policy using an incrementally cached row Gram matrix."""
import os
for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"

import argparse
import hashlib
import json
import resource
import time
from pathlib import Path

import numpy as np
from scipy.linalg import eigh

from atomic_npz import atomic_savez, atomic_write_json
from fd_certificate_audit import ExistingFD

HERE = Path(__file__).resolve().parent
INPUT_SHA256 = "d0de6bb598161e85557321a309e9d720cb1c398b722140725e47d8365e3ec68a"
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))


def exact_topk_from_gram(A, G, t, k, energy):
    if t <= k:
        q, _ = np.linalg.qr(A[:t].T, mode="reduced")
        return 0.0, q
    vals, left = eigh(
        G[:t, :t],
        subset_by_index=(t - k, t - 1),
        driver="evr",
        check_finite=False,
        overwrite_a=False,
    )
    vals = np.maximum(vals, 0.0)
    opt = max(0.0, float(energy - np.sum(vals)))
    scale = np.sqrt(np.maximum(vals, np.finfo(float).tiny))
    q = A[:t].T @ (left / scale[None, :])
    q, _ = np.linalg.qr(q, mode="reduced")
    return opt, q


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", choices=("baseline", "fd50"), required=True)
    ap.add_argument("--eta", choices=("0.01", "0.1"), required=True)
    ap.add_argument("--repeat", type=int, choices=range(3), required=True)
    args = ap.parse_args()
    eta = float(args.eta)
    stem = f"B09_{args.policy}_eta{args.eta.replace('.', 'p')}_r{args.repeat}"
    source = HERE / "LANDMARK512_FD_RAW.npz"
    assert hashlib.sha256(source.read_bytes()).hexdigest() == INPUT_SHA256
    load0 = time.perf_counter()
    with np.load(source, allow_pickle=False) as z:
        A = z["a"].copy()
        energy = z["energy"].copy()
    load_seconds = time.perf_counter() - load0
    assert A.shape == (512, 2704)
    n, d = A.shape
    k = 25
    tol = 1e-10 * np.maximum(1.0, energy)
    G = np.zeros((n, n), dtype=np.float64)
    fd = ExistingFD(50, d, False) if args.policy == "fd50" else None
    Q = None
    cached = 0.0
    running_fd_lower = 0.0
    query = np.zeros(n, dtype=bool)
    update = np.zeros(n, dtype=bool)
    loss = np.zeros(n)
    queried_opt = np.full(n, np.nan)
    cached_before = np.zeros(n)
    gate_lower = np.zeros(n)
    component = {
        "gram_update": 0.0,
        "residual": 0.0,
        "exact_eigh": 0.0,
        "fd": 0.0,
        "bookkeeping": 0.0,
    }
    whole_wall0 = time.perf_counter()
    whole_cpu0 = time.process_time()
    for i, x in enumerate(A):
        t = i + 1
        c = time.process_time()
        g = A[:t] @ x
        G[i, :t] = g
        G[:t, i] = g
        component["gram_update"] += time.process_time() - c
        c = time.process_time()
        if fd is not None:
            ss = fd.step(x)
            bound = float(ss[k:] @ ss[k:]) + (50 - k) * fd.delta
            running_fd_lower = max(running_fd_lower, max(0.0, bound - tol[i]))
        component["fd"] += time.process_time() - c
        c = time.process_time()
        if Q is None:
            r = 0.0
        else:
            reconstructed = (A[:t] @ Q) @ Q.T
            r = float(np.linalg.norm(A[:t] - reconstructed) ** 2)
        component["residual"] += time.process_time() - c
        loss[i] = r
        cached_before[i] = cached
        lower = max(cached, running_fd_lower) if fd is not None else cached
        gate_lower[i] = lower
        qflag = Q is None or t <= k or r > (1.0 + eta) * lower + tol[i]
        uflag = Q is None or t <= k
        query[i] = qflag
        if qflag:
            c = time.process_time()
            opt, exact_q = exact_topk_from_gram(A, G, t, k, energy[i])
            component["exact_eigh"] += time.process_time() - c
            queried_opt[i] = opt
            cached = max(cached, opt - tol[i], 0.0)
            if r > (1.0 + eta) * opt + tol[i]:
                uflag = True
            if uflag:
                Q = exact_q
        update[i] = uflag
    whole_cpu = time.process_time() - whole_cpu0
    whole_wall = time.perf_counter() - whole_wall0
    component["bookkeeping"] = whole_cpu - sum(component.values())
    raw = {
        "query": query,
        "update": update,
        "loss": loss,
        "queried_opt": queried_opt,
        "cached_before": cached_before,
        "gate_lower": gate_lower,
        "energy": energy,
        "gram_diagonal": np.diag(G),
    }
    receipt = atomic_savez(HERE / f"{stem}.npz", raw, list(raw))
    out = {
        "study": "B09-native512-cached-gram-exact-query",
        "policy": args.policy,
        "eta": eta,
        "repeat": args.repeat,
        "rows": n,
        "dimension": d,
        "rank": k,
        "queries_after_growth": int(query[k:].sum()),
        "refreshes_after_growth": int(update[k:].sum()),
        "algorithm_cpu_seconds": whole_cpu,
        "algorithm_wall_seconds": whole_wall,
        "component_cpu_seconds": component,
        "input_load_wall_seconds_excluded": load_seconds,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "input_sha256": INPUT_SHA256,
        "raw_artifact": receipt,
        "development_only": True,
        "exact_in_real_arithmetic": True,
        "whole_landmark5000": False,
        "new_method": False,
    }
    atomic_write_json(HERE / f"{stem}.json", out)
    print(json.dumps({key: value for key, value in out.items() if key != "raw_artifact"}, allow_nan=False))


if __name__ == "__main__":
    main()

