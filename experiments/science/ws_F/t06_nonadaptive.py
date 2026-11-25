"""N5b/N6: the non-adaptive pair with compensation.
 (A) exhaustive enumeration (n <= 14): cyclically symmetrised cone and its type-wise truncation, plus b * additive
     component: class membership, exact equality of all one-body marginals, separation, density of the difference set.
 (B) exact type-class sums (n up to 3200): the resulting lower bound exponent against theta_na(eps1)."""
import numpy as np, sys, itertools
from sl import *
from ts import *
from t03_enum_adaptive import cube, popcount, in_class, marginals, rot
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s); sys.stdout.flush()


def enum_pair(n, p, u, k, q):
    qq = 1 - p
    X, bits, wt = cube(n)
    pi = p ** wt * qq ** (n - wt)
    s0 = (1 << k) - 1
    def cone(s):
        c = np.exp(-u * popcount(X ^ s)); return c / (pi * c).sum()
    def trunc(c):
        ct = c.copy(); diff = np.zeros(len(c), bool)
        for kap in range(n + 1):
            idx = np.where(wt == kap)[0]
            vals = np.unique(c[idx])                     # ascending
            # t = smallest value v on the class with density{c > v} <= q
            t = vals[-1]
            for v in vals:
                if (c[idx] > v * (1 + 1e-12)).mean() <= q:
                    t = v; break
            sel = idx[c[idx] > t * (1 + 1e-12)]
            ct[sel] = t; diff[sel] = True
        return ct, diff
    orbit = sorted(set(rot(s0, j, n) for j in range(n)))
    cbar = np.zeros(2 ** n); ctbar = np.zeros(2 ** n); Dbar = np.zeros(2 ** n, bool)
    single_ok = None; dens_single = None
    for s in orbit:
        c = cone(s); ct, diff = trunc(c)
        if single_ok is None:
            single_ok = in_class(ct, n, u)
            dens_single = max(diff[wt == kap].mean() for kap in range(n + 1))
        cbar += c / len(orbit); ctbar += ct / len(orbit); Dbar |= diff
    At = (pi * ctbar).sum(); Ad = (pi * (cbar - ctbar)).sum()
    ct_d = (pi * ctbar * wt).sum() / (n * At); cD = (pi * (cbar - ctbar) * wt).sum() / (n * Ad)
    g2 = -u if cD > ct_d else u
    p2 = pgam(p, g2)
    b = At * (cD - ct_d) / (p2 - cD)
    w2 = np.exp(-g2 * wt); w2 /= (pi * w2).sum()
    w0 = ctbar + b * w2; w1 = cbar + b * w2
    ok0, _ = in_class(w0, n, u); ok1, _ = in_class(w1, n, u)
    m0, A0 = marginals(pi, w0, bits); m1, A1 = marginals(pi, w1, bits)
    mc, _ = marginals(pi, cbar, bits); mt, _ = marginals(pi, ctbar, bits)
    dens = max(Dbar[wt == kap].mean() for kap in range(n + 1))
    P(f"--- n={n} p={p} u={u} k={k} q={q}: single truncated cone in class: {single_ok[0]} (max|ln ratio|={single_ok[1]:.6f}); density of its difference set per type class <= {dens_single:.4f}")
    P(f"    A_t={At:.6f} (removed {Ad:.6f}); densities: cone {(pi*cbar*wt).sum()/n:.6f}, truncated {ct_d:.6f}, removed {cD:.6f}; b={b:.6f} (gamma2={g2:+.1f})")
    P(f"    compensated pair in class: {ok0}, {ok1}; one-body marginals: truncated+b: {m0.mean():.12f} (spread {np.ptp(m0):.1e}), cone+b: {m1.mean():.12f} (spread {np.ptp(m1):.1e}); max diff {np.abs(m0-m1).max():.2e}")
    P(f"    without compensation: cone {mc.mean():.9f} vs truncated {mt.mean():.9f}: gap {mc.mean()-mt.mean():+.3e}")
    P(f"    separation ln A(w1)/A(w0) = {np.log(A1/A0):.6f} (uncompensated {np.log(1/At):.6f}); max density of the symmetrised difference set = {dens:.4f} (<= n q = {n*q:.3f})")
    return b >= 0 and ok0 and ok1 and single_ok[0], np.abs(m0 - m1).max()

P("(A) exhaustive enumeration")
oks = []
for (n, p, u, k, q) in ((10, 0.3, 1.0, 5, 0.05), (12, 0.3, 1.0, 6, 0.02), (12, 0.1, 2.0, 5, 0.02), (14, 0.2, 1.5, 6, 0.01), (14, 0.1, 2.0, 7, 0.005), (12, 0.4, 0.7, 4, 0.1)):
    oks.append(enum_pair(n, p, u, k, q))
P("SUMMARY (A): all valid:", all(o[0] for o in oks), "; max marginal difference:", max(o[1] for o in oks))

P("\n(B) exact type-class sums: exponent of the non-adaptive bound with the oracle against theta_na")
for (p, u, f) in ((0.3, 1.0, 0.25), (0.1, 2.0, 0.25), (0.1, 2.0, 0.05), (0.5, 1.0, 0.25)):
    E = E_threshold(p, u); e1 = f * E
    th, tau = theta_na(p, u, e1)
    a, ma = a_capacity(p, u)
    P(f"\n=== p={p} u={u} eps1={f}E={e1:.6f}: theta_na={th:.6f} (capacity a={a:.6f}, capacity-achieving m={ma:.4f})")
    P("    n |   k | with oracle: -ln(n q)/n   sep-eps   b/A_t    c_0      c_t      c_D   | no oracle: -ln(q0)/n | theta_na - with  [x n/ln n]")
    for n in (100, 200, 400, 800, 1600, 3200):
        eps = e1 * n
        best = None
        k0 = int(round(ma * n))
        ks = range(max(1, k0 - int(0.06 * n)), min(n - 1, k0 + int(0.06 * n)) + 1, max(1, n // 100))
        for k in ks:
            G = Grid(n, p, u, k)
            # smallest density q with compensated separation > eps
            lo, hi = -n * np.log(2) - 5, 0.0
            if compensated_pair(n, p, u, k, hi, G) is None: continue
            for _ in range(50):
                mid = (lo + hi) / 2
                T = compensated_pair(n, p, u, k, mid, G)
                if T is not None and T['b'] >= 0 and T['sep'] > eps: hi = mid
                else: lo = mid
            T = compensated_pair(n, p, u, k, hi, G)
            if T is None or not (T['b'] >= 0 and T['sep'] > eps): continue
            # no oracle: smallest q with sep0 > eps
            lo0, hi0 = -n * np.log(2) - 5, 0.0
            for _ in range(50):
                mid = (lo0 + hi0) / 2
                T0 = compensated_pair(n, p, u, k, mid, G)
                if T0 is not None and T0['sep0'] > eps: hi0 = mid
                else: lo0 = mid
            T0 = compensated_pair(n, p, u, k, hi0, G)
            val = -(np.log(n) + T['ldens']) / n
            if best is None or val > best[0]:
                best = (val, k, T, -T0['ldens'] / n)
        val, k, T, val0 = best
        P(f"{n:5d} | {k:4d} | {val:.6f}   {T['sep']-eps:+.4f}  {T['b']/np.exp(T['lAt']):.4f}  {T['c0']:.5f}  {T['ct']:.5f}  {T['cD']:.5f} | {val0:.6f} | {th-val:+.6f} [{(th-val)*n/np.log(n):.3f}]")
open('out/t06_nonadaptive.txt', 'w').write('\n'.join(out) + '\n')
