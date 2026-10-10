"""Primary-B03 solver repair: conservative near-zero branch, otherwise original Newton path."""
import numpy as np

STATS = {
    "calls": 0,
    "evaluations": 0,
    "newton_steps": 0,
    "protected_midpoints": 0,
    "tail_bisections": 0,
    "endpoint_fallbacks": 0,
    "near_zero_opt_calls": 0,
    "near_zero_legacy_fallbacks": 0,
}


def coefficients(Q, V, G):
    left, singular, right = np.linalg.svd(Q.T @ V, full_matrices=False)
    B = Q @ left
    Z = V @ right.T
    singular = np.clip(singular, 0.0, 1.0)
    D = Z - B * singular
    sine_norm = np.linalg.norm(D, axis=0)
    theta = np.arctan2(sine_norm, singular)
    U = np.zeros_like(D)
    active = sine_norm > 1e-8
    U[:, active] = D[:, active] / sine_norm[active]
    aa = np.sum(B * (G @ B), axis=0)
    bb = np.sum(B * (G @ U), axis=0)
    cc = np.sum(U * (G @ U), axis=0)
    return B, Z, U, theta, aa, bb, cc, sine_norm


def analytic(alpha, theta, aa, bb, cc, energy):
    cosine = np.cos(alpha * theta)
    sine = np.sin(alpha * theta)
    loss = energy - float(np.sum(aa * cosine * cosine + 2 * bb * sine * cosine + cc * sine * sine))
    derivative = float(
        np.sum(theta * (2 * (aa - cc) * sine * cosine - 2 * bb * (cosine * cosine - sine * sine)))
    )
    return loss, derivative


def boundary_legacy(Q, V, G, energy, target, tol):
    """Mathematical logic of the B01/B03 48-step bisection baseline."""
    B, _Z, U, theta, aa, bb, cc, _sine_norm = coefficients(Q, V, G)

    def loss(alpha):
        cosine = np.cos(alpha * theta)
        sine = np.sin(alpha * theta)
        return energy - float(np.sum(aa * cosine * cosine + 2 * bb * sine * cosine + cc * sine * sine))

    if loss(1.0) > target + tol:
        return V.copy(), True
    lo, hi = 0.0, 1.0
    for _ in range(48):
        mid = (lo + hi) / 2
        if loss(mid) <= target:
            hi = mid
        else:
            lo = mid
    W = B * np.cos(hi * theta) + U * np.sin(hi * theta)
    W = np.linalg.qr(W, mode="reduced")[0]
    if energy - float(np.sum(W * (G @ W))) > target + tol:
        return V.copy(), True
    return W, False


def boundary_newton(Q, V, G, energy, target, tol):
    STATS["calls"] += 1
    if target <= tol:
        STATS["near_zero_opt_calls"] += 1
        STATS["near_zero_legacy_fallbacks"] += 1
        return boundary_legacy(Q, V, G, energy, target, tol)

    B, _Z, U, theta, aa, bb, cc, _sine_norm = coefficients(Q, V, G)

    def value(alpha):
        STATS["evaluations"] += 1
        return analytic(alpha, theta, aa, bb, cc, energy)

    fzero, _ = value(0.0)
    if fzero <= target:
        return Q.copy(), False
    fhi, _ = value(1.0)
    if fhi > target + tol:
        STATS["endpoint_fallbacks"] += 1
        return V.copy(), True
    lo, hi, alpha = 0.0, 1.0, 0.5
    eps = 32 * np.finfo(float).eps * max(1.0, energy)
    for _ in range(24):
        loss, derivative = value(alpha)
        if loss <= target:
            hi = alpha
            if target - loss <= eps:
                break
        else:
            lo = alpha
        if hi - lo <= 2 ** -40:
            break
        candidate = alpha - (loss - target) / derivative if derivative < 0.0 and np.isfinite(derivative) else float("nan")
        if np.isfinite(candidate) and lo < candidate < hi:
            alpha = candidate
            STATS["newton_steps"] += 1
        else:
            alpha = (lo + hi) / 2
            STATS["protected_midpoints"] += 1
    # A residual-sized early Newton stop may leave a wide alpha bracket when the
    # loss curve is locally flat.  Refine the certified bracket geometrically;
    # ||P(alpha)-P(alpha*)||_F <= sqrt(2)||theta||_2 |alpha-alpha*|.
    for _ in range(48):
        if hi - lo <= 2 ** -40:
            break
        STATS["tail_bisections"] += 1
        alpha = (lo + hi) / 2
        loss, _ = value(alpha)
        if loss <= target:
            hi = alpha
        else:
            lo = alpha
    W = B * np.cos(hi * theta) + U * np.sin(hi * theta)
    W = np.linalg.qr(W, mode="reduced")[0]
    if energy - float(np.sum(W * (G @ W))) > target + tol:
        STATS["endpoint_fallbacks"] += 1
        return V.copy(), True
    return W, False
