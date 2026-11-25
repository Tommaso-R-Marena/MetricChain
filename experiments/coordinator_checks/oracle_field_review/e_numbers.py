"""Own recomputation of the numbers of SCI-RES-0006 section 2 at the test point of Proposition 11.109(e):
p = 1/4, u = 1, e = 0.02, zero residual (gamma = 0)."""
import math, sys
import numpy as np
from scipy.optimize import minimize_scalar, minimize

def kl(a, b):
    a = min(max(a, 1e-300), 1 - 1e-16) if not (0 < a < 1) else a
    out = 0.0
    if a > 0: out += a * math.log(a / b)
    if a < 1: out += (1 - a) * math.log((1 - a) / (1 - b))
    return out

def h(x):
    return 0.0 if x <= 0 or x >= 1 else -x * math.log(x) - (1 - x) * math.log(1 - x)

def R0(e, p, u):
    """hinted exponent of the zero residual: max_m [h(m) - h((Lambda_m + e)/u)]_+  (theory report, Theorem 11.59(c))."""
    q = 1 - p
    L0, L1 = -math.log(q + p * math.exp(-u)), -math.log(p + q * math.exp(-u))
    def neg(m):
        x = ((1 - m) * L0 + m * L1 + e) / u
        if x >= 0.5: return 0.0
        if x <= 0: return -h(m)
        return -(h(m) - h(x))
    best = 0.0
    for a, b in ((1e-9, 0.5), (0.5, 1 - 1e-9), (1e-9, 1 - 1e-9)):
        r = minimize_scalar(neg, bounds=(a, b), method="bounded", options=dict(xatol=1e-13))
        best = max(best, -r.fun)
    return best

def tilt_bound(e, p, u):
    c = lambda lam: math.log(1 - p + p * math.exp(lam)) - lam * p
    def val(lam):
        if c(lam) >= e: return math.inf
        pl = 1 / (1 + math.exp(-(math.log(p / (1 - p)) + lam)))
        return R0(e - c(lam), pl, u)
    lams = np.linspace(-1.5, 1.5, 6001)
    vals = [val(l) for l in lams]
    i = int(np.argmin(vals))
    r = minimize_scalar(val, bounds=(lams[max(i - 2, 0)], lams[min(i + 2, len(lams) - 1)]), method="bounded", options=dict(xatol=1e-12))
    return r.fun, r.x

def f_profile(m, v0, v1, e, p, u):
    """min{ I(M, V') : u sum_phi M(phi)|v'_phi - v_phi| <= e + D(V || pi | M) }   (gamma = 0)."""
    budget = (e + (1 - m) * kl(v0, p) + m * kl(v1, p)) / u
    def I(a0, a1):
        bar = (1 - m) * a0 + m * a1
        return (1 - m) * kl(a0, bar) + m * kl(a1, bar)
    if (1 - m) * abs(v0 - v1) * 0 + budget >= 0:
        pass
    # the minimiser moves the two block laws towards each other; parametrise by the amount moved in block 0 (x0) and
    # block 1 (x1), with (1-m) x0 + m x1 = budget; if the budget suffices to merge them, the value is 0
    lo, hi = (v0, v1) if v0 <= v1 else (v1, v0)
    mlo, mhi = ((1 - m), m) if v0 <= v1 else (m, (1 - m))
    if mlo * 0 + budget >= 0 and budget >= mlo * mhi * (hi - lo) / 1.0 * 0 + min(mlo, mhi) * 0 + 0:
        pass
    # merging cost: move lo up by a, hi down by b with lo + a = hi - b: minimal weighted cost mlo a + mhi b s.t. a + b = hi - lo
    if budget >= min(mlo, mhi) * (hi - lo):
        return 0.0
    def obj(a):                       # a = shift of the lower block upwards (cost mlo a); the rest of the budget on the upper
        b = (budget - mlo * a) / mhi
        if b < 0 or lo + a > hi - b: return 0.0 if lo + a >= hi - b else math.inf
        A, B = lo + a, hi - b
        bar = mlo * A + mhi * B
        return mlo * kl(A, bar) + mhi * kl(B, bar)
    r = minimize_scalar(obj, bounds=(0.0, budget / mlo), method="bounded", options=dict(xatol=1e-13))
    return min(r.fun, obj(0.0), obj(budget / mlo))

def sup_profiles(e, p, u, window):
    q = 1 - p
    pm = p * math.exp(-u) / (q + p * math.exp(-u)); pp = p * math.exp(u) / (q + p * math.exp(u))
    lo, hi = (pm, pp) if window else (1e-6, 1 - 1e-6)
    best, arg = 0.0, None
    for m in np.linspace(0.02, 0.98, 97):
        for v1 in np.linspace(lo, hi, 400):
            v0 = (p - m * v1) / (1 - m)
            if not (lo - 1e-12 <= v0 <= hi + 1e-12): continue
            val = f_profile(m, v0, v1, e, p, u)
            if val > best: best, arg = val, (m, v0, v1)
    # refine
    def neg(z):
        m, v1 = z
        if not (0.01 < m < 0.99): return 1.0
        v0 = (p - m * v1) / (1 - m)
        if not (lo - 1e-12 <= v0 <= hi + 1e-12 and lo - 1e-12 <= v1 <= hi + 1e-12): return 1.0
        return -f_profile(m, v0, v1, e, p, u)
    r = minimize(neg, [arg[0], arg[2]], method="Nelder-Mead", options=dict(xatol=1e-10, fatol=1e-14, maxiter=4000))
    if -r.fun > best:
        best, arg = -r.fun, (r.x[0], (p - r.x[0] * r.x[1]) / (1 - r.x[0]), r.x[1])
    return best, arg, (pm, pp)

if __name__ == "__main__":
    p, u, e = 0.25, 1.0, 0.02
    print("R_0(e) without the oracle       :", f"{R0(e, p, u):.6f}")
    U, lam = tilt_bound(e, p, u)
    print("tilt upper bound U_0(e)         :", f"{U:.6f}", " at lambda =", f"{lam:+.5f}")
    b, a, win = sup_profiles(e, p, u, window=False)
    print("sup over profiles of type p     :", f"{b:.6f}", " at (m, v0, v1) =", tuple(round(float(x), 4) for x in a))
    b, a, win = sup_profiles(e, p, u, window=True)
    print("... block laws in the window    :", f"{b:.6f}", " at (m, v0, v1) =", tuple(round(float(x), 4) for x in a), " window =", tuple(round(x, 4) for x in win))
    # plain dips with the centre type forced by c0(m) = p: profile (m, p-, p+)
    pm, pp = win
    m0 = (p - pm) / (pp - pm)
    print("dips around the Gibbs shell of cones of the forced centre type m0 (annular):", f"{f_profile(m0, pm, pp, e, p, u):.6f}", " m0 =", round(m0, 4))
    q = 1 - p
    L0, L1 = -math.log(q + p * math.exp(-u)), -math.log(p + q * math.exp(-u))
    print("plain cone dips (balls) of the forced centre type m0, h(m0) - h((Lambda_m0 + e)/u):",
          f"{h(m0) - h(((1 - m0) * L0 + m0 * L1 + e) / u):.6f}")
    print("decrease by the oracle: between", f"{100 * (1 - U / R0(e, p, u)):.1f} %", "and", f"{100 * (1 - b / R0(e, p, u)):.1f} %")
