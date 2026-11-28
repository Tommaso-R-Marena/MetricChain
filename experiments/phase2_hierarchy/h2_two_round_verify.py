"""
Phase II (adaptive hierarchy) -- independent verification of the two-round separation
(theory report Theorem 11.86 = workstream U, Theorem U3).  Own code; nothing imported from the archive.

Part A  (asymptotic formula).  For u > 0, f(r) = KL(r || 1/2), p_u = 1/(1+e^u), Lambda1 = ln(2/(1+e^-u)),
        k(r) = f(r) + u r - Lambda1,  a = f(p_u),  h = f(Lambda1/u):
            Xi(theta, phi1) = min_{z in [p_u, 1/2], phi1 f(z) <= theta}  phi1 k(z) + phi2 (u rho(z) - Lambda1),
            phi2 f(rho(z)) = theta - phi1 f(z),
            vartheta(phi1)  = min{ phi2 a , root of Xi(., phi1) },      theta2*(u) = max_phi1 vartheta(phi1).
        Recomputed here by direct minimisation and bisection, to be compared with the archive's table.

Part B  (exact finite n).  Twins on two blocks built from scratch as the deepest admissible functions:
        the visible part is the largest function below the flat-histogram cap that depends on d1 only on W1;
        F_D is its deepest extension beyond V2, F_S the extension capped by the flat histogram.
        Reported: the gap ln A(F_D) - ln A(F_S) and E = -(1/n) ln(p1 + 2 p2); the largest E with gap > 1.
        Checks on every pair: admissibility (largest one-step difference <= u), equality on V2,
        dependence on d1 only on W1 n V2.
"""
import sys
import numpy as np
from scipy.special import gammaln
from scipy.optimize import brentq, minimize_scalar

LN2 = np.log(2.0)

def f(r):
    r = np.clip(r, 1e-300, 1 - 1e-16)
    return LN2 + r * np.log(r) + (1 - r) * np.log1p(-r)

def finv(t):
    """inverse of f on [0, 1/2]"""
    if t <= 0: return 0.5
    if t >= LN2: return 0.0
    return brentq(lambda r: f(r) - t, 1e-15, 0.5)

def consts(u):
    pu = 1.0 / (1.0 + np.exp(u)); L1 = np.log(2.0 / (1.0 + np.exp(-u)))
    return pu, L1, f(pu), f(L1 / u)

_RG = np.linspace(1e-9, 0.5, 400001)          # radius grid for the vectorised inverse of f
_FG = f(_RG)                                   # decreasing in the radius

def finv_vec(t):
    """inverse of f on [0, 1/2], vectorised (linear interpolation on a grid of 4e5 radii)"""
    t = np.asarray(t, float)
    return np.interp(-t, -_FG, _RG)

def Xi(u, theta, phi1):
    pu, L1, a, h = consts(u); phi2 = 1 - phi1
    zlo = pu if phi1 * a <= theta else float(finv_vec(theta / phi1))
    zs = np.linspace(zlo, 0.5, 20001)
    c = phi1 * f(zs)
    ok = c <= theta + 1e-15
    rho = finv_vec(np.maximum(theta - c, 0.0) / phi2)
    vals = np.where(ok, phi1 * (f(zs) + u * zs - L1) + phi2 * (u * rho - L1), np.inf)
    return float(vals.min())

def vartheta(u, phi1):
    pu, L1, a, h = consts(u); phi2 = 1 - phi1
    # root of Xi(., phi1): Xi(h) > 0 and Xi is decreasing in theta
    lo, hi = h, a
    if Xi(u, hi, phi1) > 0: root = hi
    else: root = brentq(lambda t: Xi(u, t, phi1), lo, hi, xtol=1e-12)
    return min(phi2 * a, root), root

def part_A(us):
    print("Part A: theta2*(u) recomputed")
    print("   u      a          h        h/a     best phi1   theta2*/a   theta2*/h")
    for u in us:
        pu, L1, a, h = consts(u)
        best = (-1, None)
        for phi1 in np.linspace(0.30, 0.75, 91):
            v, _ = vartheta(u, phi1)
            if v > best[0]: best = (v, phi1)
        # refine
        for phi1 in np.linspace(best[1] - 0.005, best[1] + 0.005, 41):
            v, _ = vartheta(u, phi1)
            if v > best[0]: best = (v, phi1)
        print("  %4.2f  %.6f  %.6f  %.4f   %.3f       %.4f      %.4f" % (u, a, h, h / a, best[1], best[0] / a, best[0] / h))
        sys.stdout.flush()

# ---------------------------------------------------------------- Part B
def logbinom(n):
    k = np.arange(n + 1)
    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1) - n * LN2

def lip_minorant_1d(t, u):
    g = t.copy()
    for i in range(1, len(g)): g[i] = min(g[i], g[i - 1] + u)
    for i in range(len(g) - 2, -1, -1): g[i] = min(g[i], g[i + 1] + u)
    return g

def lip_pass(U, u):
    for ax in (0, 1):
        U = np.moveaxis(U, ax, 0)
        for i in range(1, U.shape[0]): np.minimum(U[i], U[i - 1] + u, out=U[i])
        for i in range(U.shape[0] - 2, -1, -1): np.minimum(U[i], U[i + 1] + u, out=U[i])
        U = np.moveaxis(U, 0, ax)
    return U

def logsumexp(a):
    m = a.max(); return m + np.log(np.exp(a - m).sum())

def twins(u, n, n1, T, rule="archive", fs="rising"):
    n2 = n - n1
    lp1, lp2 = logbinom(n1), logbinom(n2)
    c1, c2 = -lp1, -lp2
    t1, t2 = lp1.max() - lp1, lp2.max() - lp2
    C = c1[:, None] + c2[None, :]
    W1 = C <= T
    lp_out1 = logsumexp((lp1[:, None] + lp2[None, :])[~W1]) if (~W1).any() else -np.inf   # ln p1
    # W2: central interval of d2
    order = np.argsort(c2)                       # from the mode outwards
    if rule == "archive":                        # smallest central interval with p2 <= p1
        tail = np.array([logsumexp(lp2[c2 > c2[j]]) if (c2 > c2[j]).any() else -np.inf for j in order])
        ok = np.where(tail <= lp_out1)[0]
        thr = c2[order[ok[0]]]
    else:                                        # same cost threshold as W1
        thr = T
    W2 = c2 <= thr + 1e-12
    lp_out2 = logsumexp(lp2[~W2]) if (~W2).any() else -np.inf                            # ln p2
    cap1 = lip_minorant_1d(t1, u); capB = lip_minorant_1d(t2, u)
    cap2 = cap1[:, None] + capB[None, :]
    INF = 1e18
    vis1 = W1 & W2[None, :]
    U = np.where(vis1, np.broadcast_to(cap1[:, None], C.shape), INF).astype(float)
    Uenv = lip_pass(U.copy(), u)
    Uvis = np.where(W2[None, :], np.minimum(Uenv, cap2), INF)
    UD = lip_pass(Uvis.copy(), u)                 # deepest extension
    if fs == "capped":                            # F_S = max(F_D, flat histogram): our first choice
        US = np.minimum(UD, cap2)
    else:                                         # F_S rises at slope u beyond V2 (the archive's choice)
        US = Uvis.copy()
        idx = np.where(W2)[0]; lo, hi = idx.min(), idx.max()
        for d2 in range(0, lo): US[:, d2] = Uvis[:, lo] - u * (lo - d2)
        for d2 in range(hi + 1, n2 + 1): US[:, d2] = Uvis[:, hi] - u * (d2 - hi)
    # checks
    def maxstep(V):
        return max(np.abs(np.diff(V, axis=0)).max(), np.abs(np.diff(V, axis=1)).max())
    chk = dict(lipD=maxstep(UD) <= u + 1e-9, lipS=maxstep(US) <= u + 1e-9,
               equal_on_V2=bool(np.all(UD[:, W2] == US[:, W2])),
               d1_only_on_W1=bool(np.all(np.where(vis1, UD - cap1[:, None], 0) == 0)),
               S_ge_D=bool(np.all(US <= UD + 1e-12)))
    lP = lp1[:, None] + lp2[None, :]
    lnAD, lnAS = logsumexp(lP + UD), logsumexp(lP + US)
    gap = lnAD - lnAS
    lnp = np.logaddexp(lp_out1, np.log(2.0) + lp_out2)
    j = np.unravel_index(np.argmax(lP + UD), lP.shape)
    return dict(gap=gap, E=-lnp / n, lnp1=lp_out1, lnp2=lp_out2, checks=chk, bulk=(j[0] / n1, j[1] / n2), lnAS=lnAS)

def best_E(u, n, fracs, rule):
    pu, L1, a, h = consts(u)
    best = None
    for fr in fracs:
        n1 = int(round(fr * n))
        lo, hi = 0.8 * h * n, 0.75 * a * n
        if twins(u, n, n1, lo, rule)['gap'] <= 1: continue
        for _ in range(18):
            mid = 0.5 * (lo + hi)
            if twins(u, n, n1, mid, rule)['gap'] > 1: lo = mid
            else: hi = mid
        r = twins(u, n, n1, lo, rule)
        if best is None or r['E'] > best[0]['E']: best = (r, n1, lo)
    return best

def part_B(u, ns, rule):
    pu, L1, a, h = consts(u)
    print("Part B: exact twins, u = %g (h = %.5f), rule for W2: %s" % (u, h, rule))
    print("     n     n1     gap      E        E/h    bulk type (d1/n1, d2/n2)   checks")
    for n in ns:
        r, n1, T = best_E(u, n, [0.45, 0.50, 0.55, 0.60, 0.64, 0.68], rule)
        ok = all(r['checks'].values())
        print("  %6d %5d  %6.3f  %.5f  %.3f   (%.3f, %.3f)              %s" % (n, n1, r['gap'], r['E'], r['E'] / h, r['bulk'][0], r['bulk'][1], "all pass" if ok else str(r['checks'])))
        sys.stdout.flush()

def part_C(u, n, phi1):
    """exact gap per coordinate against the asymptotic gap function min{Xi, phi2 k(y1)}"""
    pu, L1, a, h = consts(u); phi2 = 1 - phi1
    n1 = int(round(phi1 * n))
    print("Part C: u = %g, n = %d, phi1 = %.2f: exact gap/n against min{Xi, phi2 k(y1)}_+" % (u, n, phi1))
    for th in [1.0, 1.1, 1.2, 1.3, 1.4]:
        theta = th * h
        r = twins(u, n, n1, theta * n + 2 * np.log(n), rule="cost")
        y1 = finv(theta / phi2)
        pred = max(min(Xi(u, theta, phi1), phi2 * (f(y1) + u * y1 - L1) if y1 > pu else 0.0), 0.0)
        print("   theta/h = %.2f   exact gap/n = %.5f   formula = %.5f" % (th, r['gap'] / n, pred))

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("A", "all"):
        part_A([0.05, 0.25, 0.5, 1.0, 2.0, 3.0, 4.0, 6.0])
    if mode in ("B", "all"):
        part_B(1.0, [400, 800, 1600, 3200], "archive")
        part_B(2.0, [200, 400, 1600], "archive")
    if mode in ("C", "all"):
        part_C(1.0, 3200, 0.6)
        part_C(1.0, 6400, 0.6)
