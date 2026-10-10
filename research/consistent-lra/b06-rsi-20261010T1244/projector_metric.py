"""Stable low-memory distances between equal-rank subspaces."""
import numpy as np


def projector_frobenius(q, v, *, reorthogonalize=True):
    """Return ||QQ^T - VV^T||_F without forming dense d-by-d projectors.

    ``q`` and ``v`` must have the same shape ``(d, k)`` and full column rank.
    Reduced QR is enabled by default because callers may only be orthonormal to
    working precision.  For orthonormal bases the two residual terms below sum
    exactly to the squared projector Frobenius distance.
    """
    q = np.asarray(q, dtype=float)
    v = np.asarray(v, dtype=float)
    if q.ndim != 2 or v.ndim != 2 or q.shape != v.shape:
        raise ValueError("q and v must be equal-shape two-dimensional arrays")
    if reorthogonalize:
        q = np.linalg.qr(q, mode="reduced")[0]
        v = np.linalg.qr(v, mode="reduced")[0]
    q_residual = v - q @ (q.T @ v)
    v_residual = q - v @ (v.T @ q)
    return float(np.hypot(np.linalg.norm(q_residual), np.linalg.norm(v_residual)))
