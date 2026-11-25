"""N3 — the Hilbert-ball class: hypercircle band and the exact consistent interval of ln Z.

For random kernels K (PSD, on a finite set of 2^n points, n = 3..6), random designs A (arbitrary
subsets, not only linear ones), random known parts f and random members g of the ball:

  (a) |g - ghat_A| <= B_A P_A pointwise, with B_A^2 = B^2 - y^T K_AA^+ y  (hypercircle);
  (b) the exact lower end of min(f+g) over consistent g is  min_x [f + ghat_A - B_A P_A];
  (c) U_A := sup_{consistent} ln Z - ln Z(f+ghat_A) = sup_pi [beta B_A sqrt(pi^T K_A pi) - KL(pi||pihat)]
      L_A := ln Z(f+ghat_A) - inf_{consistent} ln Z = inf_pi [beta B_A sqrt(pi^T K_A pi) + KL(pi||pihat)]
      -- compared between a search in function space (r in the ball) and a search over the
      simplex (pi), plus the elementary bounds
         L_A <= beta B_A sqrt(pihat^T K_A pihat) <= U_A <= beta B_A max_x P_A(x).
Run:  python3 n3_ball_lnz.py
"""
import json

import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(7)


def lnE(pi, a):
    m = a.max()
    return float(m + np.log(np.sum(pi * np.exp(a - m))))


def sup_function_space(KA_half, BA, pihat, beta, starts=8):
    """max over ||w|| <= BA of ln E_pihat exp(-beta (KA_half w)) by fixed-point ascent (convex max)."""
    best, d = -np.inf, KA_half.shape[1]
    for s in range(starts):
        w = rng.standard_normal(d)
        w *= BA / np.linalg.norm(w)
        val = -np.inf
        for _ in range(400):
            r = KA_half @ w
            a = -beta * r
            p = pihat * np.exp(a - a.max())
            p /= p.sum()
            grad = -beta * (KA_half.T @ p)
            ng = np.linalg.norm(grad)
            if ng < 1e-300:
                break
            w_new = BA * grad / ng
            val_new = lnE(pihat, -beta * (KA_half @ w_new))
            if val_new <= val + 1e-14:
                break
            w, val = w_new, val_new
        best = max(best, val)
    return best


def inf_function_space(KA_half, BA, pihat, beta):
    """min over ||w|| <= BA of the convex function ln E_pihat exp(-beta KA_half w)."""
    d = KA_half.shape[1]

    def fun(w):
        r = KA_half @ w
        a = -beta * r
        m = a.max()
        e = pihat * np.exp(a - m)
        val = m + np.log(e.sum())
        p = e / e.sum()
        return val, -beta * (KA_half.T @ p)

    cons = {"type": "ineq", "fun": lambda w: BA ** 2 - w @ w, "jac": lambda w: -2 * w}
    best = np.inf
    for s in range(2):
        w0 = rng.standard_normal(d) * 1e-3
        res = minimize(lambda w: fun(w)[0], w0, jac=lambda w: fun(w)[1], constraints=[cons],
                       method="SLSQP", options={"maxiter": 500, "ftol": 1e-13})
        best = min(best, res.fun)
    return best


def variational(KA, BA, pihat, beta, sign, starts=6):
    """sign=+1: sup_pi [beta BA sqrt(pi K pi) - KL];  sign=-1: inf_pi [beta BA sqrt(pi K pi) + KL].
    Softmax parametrisation with analytic gradient."""
    n = len(pihat)
    lph = np.log(pihat)

    def obj(theta):
        t = theta - theta.max()
        p = np.exp(t)
        p /= p.sum()
        Kp = KA @ p
        q = max(float(p @ Kp), 1e-300)
        lp = np.log(np.maximum(p, 1e-300))
        kl = float(np.sum(p * (lp - lph)))
        dq = beta * BA * Kp / np.sqrt(q)
        dkl = lp - lph + 1.0
        if sign > 0:
            val, dp = -(beta * BA * np.sqrt(q) - kl), -(dq - dkl)
        else:
            val, dp = beta * BA * np.sqrt(q) + kl, dq + dkl
        grad = p * (dp - float(p @ dp))
        return val, grad

    best = np.inf
    inits = [lph.copy()] + [lph + 3 * rng.standard_normal(n) for _ in range(starts)]
    if sign > 0:   # localised candidates (point masses) for the sup
        for x in np.argsort(-np.diag(KA))[:4]:
            th = np.full(n, -12.0)
            th[x] = 0.0
            inits.append(th)
    for th0 in inits:
        res = minimize(obj, th0, jac=True, method="L-BFGS-B",
                       options={"maxiter": 800, "ftol": 1e-14, "gtol": 1e-9})
        best = min(best, res.fun)
    return -best if sign > 0 else best


records = []
viol = {"band": 0, "min_lower": 0.0, "U_gap": 0.0, "L_gap": 0.0, "bounds": 0}
for trial in range(16):
    n = int(rng.integers(3, 6))
    size = 1 << n
    rank = int(rng.integers(2, size + 1))
    Fm = rng.standard_normal((size, rank)) * rng.exponential(1.0, rank)[None, :]
    K = Fm @ Fm.T / rank
    N = int(rng.integers(0, min(rank, size // 2) + 1))
    A = rng.choice(size, N, replace=False)
    # a member of the ball of radius B
    coef = rng.standard_normal(rank)
    g = Fm @ coef / np.sqrt(rank)                      # ||g||_K = ||coef||  (Fm full column rank a.s.)
    B = np.linalg.norm(coef) * float(rng.uniform(1.0, 1.5))
    f = rng.standard_normal(size) * float(rng.uniform(0, 2))
    beta = float(rng.uniform(0.2, 3.0))
    if N:
        KAA = K[np.ix_(A, A)]
        KAAi = np.linalg.pinv(KAA, hermitian=True)
        W = K[:, A] @ KAAi
        ghat = W @ g[A]
        KA = K - W @ K[A, :]
        BA2 = B ** 2 - g[A] @ KAAi @ g[A]
    else:
        ghat = np.zeros(size)
        KA = K.copy()
        BA2 = B ** 2
    assert BA2 > -1e-9
    BA = np.sqrt(max(BA2, 0.0))
    P = np.sqrt(np.maximum(np.diag(KA), 0.0))
    # (a) hypercircle band
    if np.any(np.abs(g - ghat) > BA * P + 1e-8 * (1 + B)):
        viol["band"] += 1
    # (b) exact lower end of the minimum: attained by r = -BA K_A(.,x)/P(x)
    x0 = int(np.argmin(f + ghat - BA * P))
    lower = float((f + ghat - BA * P)[x0])
    if P[x0] > 1e-12:
        r = -BA * KA[:, x0] / P[x0]
        viol["min_lower"] = max(viol["min_lower"], abs(float(np.min(f + ghat + r)) - lower))
    # (c) ln Z interval
    a0 = -beta * (f + ghat)
    pihat = np.exp(a0 - a0.max())
    pihat /= pihat.sum()
    ev, evec = np.linalg.eigh((KA + KA.T) / 2)
    keep = ev > 1e-10 * max(ev.max(), 1e-300)
    KA_half = evec[:, keep] * np.sqrt(ev[keep])[None, :]
    if keep.sum() == 0 or BA < 1e-9:
        continue
    U_fs = sup_function_space(KA_half, BA, pihat, beta)
    U_var = variational(KA, BA, pihat, beta, +1)
    L_fs = -inf_function_space(KA_half, BA, pihat, beta)
    L_var = variational(KA, BA, pihat, beta, -1)
    mid = beta * BA * np.sqrt(max(float(pihat @ KA @ pihat), 0.0))
    top = beta * BA * P.max()
    rel = 1e-6 * (1 + top)
    viol["U_gap"] = max(viol["U_gap"], abs(U_fs - U_var) / (1 + top))
    viol["L_gap"] = max(viol["L_gap"], abs(L_fs - L_var) / (1 + top))
    if not (L_var <= mid + rel and mid <= U_var + rel and U_var <= top + rel):
        viol["bounds"] += 1
    # the true member lies in the interval
    lz = lnE(np.ones(size) / size, -beta * (f + g)) - lnE(np.ones(size) / size, -beta * (f + ghat))
    assert -L_var - rel <= lz <= U_var + rel, (lz, L_var, U_var)
    print(trial, n, rank, N, round(U_fs, 6), round(U_var, 6), round(L_fs, 6), round(L_var, 6), flush=True)
    records.append({"n": n, "rank": rank, "N": N, "beta": beta, "U_fs": U_fs, "U_var": U_var,
                    "L_fs": L_fs, "L_var": L_var, "mid": mid, "top": top, "true": lz})

print("violations:", viol, " records:", len(records))
with open("n3_ball_lnz.json", "w") as fh:
    json.dump({"viol": viol, "records": records}, fh, indent=1)
assert viol["band"] == 0 and viol["bounds"] == 0 and viol["min_lower"] < 1e-7
print("largest relative mismatch sup:", viol["U_gap"], " inf:", viol["L_gap"])
