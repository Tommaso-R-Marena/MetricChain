"""R11 / 06 -- Proposition D numerically, with ALL vertices of the block polytopes (L <= 3):
exact sub-additivity of F+ (slack K at both ends), exact super-additivity of F- (reduced by kappa_0),
the bound F+ - F- <= t*2(u+K), and a few entries of the tables of sections 6.1, 6.2.

Run:  python3 r11_06_propD.py       (about 1 minute)
"""
import time
import numpy as np
from r11lib import *

T0 = time.time()
u = 1.0


def F_block(L, p, slopes, t, law=None):
    """F*[law on {+-1}^L ; envelope with the given slopes](t): all vertices, duality bracket."""
    s, pi = chain_law(L, p)
    if law is not None:
        pi = law
    V = lipschitz_vertices(L, slopes)
    logP = gibbs_logs(np.log(pi), V)
    lo, up, M = maximise_G_fast(logP, t)
    return lo, up, V.shape[0]


def kappa(p, m):
    lam = 1 - 2 * p
    return np.log((1 + lam ** (m + 1)) / (1 - lam ** (m + 1)))


def slopes_plus(L, K):
    sl = [u] * L
    sl[0] += K
    sl[-1] += K
    return sl


def slopes_minus(L, kap):
    sl = [u] * L
    sl[0] -= kap
    sl[-1] -= kap
    return sl


print("== sub-/super-additivity and the gap, all vertices ==")
for p in (0.4, 0.3):
    K = np.log((1 - p) / p)
    for t in (0.3, 0.45, 0.7):
        Fp = [F_block(L, p, slopes_plus(L, K), t) for L in (1, 2, 3)]
        line = (f"p={p} t={t}: F+_1,2,3 = " + " ".join(f"{a[0]:.6f}" for a in Fp) + f" (|V| = {[a[2] for a in Fp]}, brackets <= {max(a[1]-a[0] for a in Fp):.1e})"
                f" | F+_2 - 2F+_1 = {Fp[1][0]-2*Fp[0][0]:+.6f}, F+_3 - F+_1 - F+_2 = {Fp[2][0]-Fp[0][0]-Fp[1][0]:+.6f} (must be <= 0)")
        if u > 2 * K:        # the reduced envelope is nonnegative also for L = 1
            Fm = [F_block(L, p, slopes_minus(L, K), t) for L in (1, 2, 3)]
            line += (" | F-_1,2,3 = " + " ".join(f"{a[0]:.6f}" for a in Fm) +
                     f" | F-_2 - 2F-_1 = {Fm[1][0]-2*Fm[0][0]:+.6f}, F-_3 - F-_1 - F-_2 = {Fm[2][0]-Fm[0][0]-Fm[1][0]:+.6f} (must be >= 0)"
                     f" | (F+_3 - F-_3)/(t 2(u+K)) = {(Fp[2][0]-Fm[2][0])/(t*2*(u+K)):.3f} (must be <= 1)")
        print(line)

print("\n== plain F_L (no slack): neither monotone nor a bound (report: 0.02895, 0.03280, 0.03359 for n = 1, 2, 3 at p = 0.4, t = 0.45) ==")
p, t = 0.4, 0.45
print("   F_n/n, n = 1, 2, 3:", " ".join(f"{F_block(L, p, [u]*L, t)[0]/L:.5f}" for L in (1, 2, 3)))

print("\n== entries of section 6.1 ((U): h <= max_t F+_L(t)/L) and 6.2 ((L'): h >= max_t F-_{L,m}(t)/(L+m)) ==")
rep61 = {0.4: (0.08302, 0.05804, 0.04948), 0.3: (0.15031, 0.09387, 0.07428), 0.2: (0.22525, 0.13205, 0.10025), 0.1: (0.31125, 0.17250, 0.12692)}
for p in (0.4, 0.3, 0.2, 0.1):
    K = np.log((1 - p) / p)
    vals = []
    for L in (1, 2, 3):
        tt, v = golden_max(lambda t: F_block(L, p, slopes_plus(L, K), t)[0], 0.1, 0.9, tol=1e-4)
        vals.append(F_block(L, p, slopes_plus(L, K), tt)[1] / L)
    print(f"p={p}: (U) h <= " + ", ".join(f"{v:.5f}" for v in vals) + "   report: " + ", ".join(f"{v:.5f}" for v in rep61[p]))
rep62 = {0.4: [(3, 1, 0.02307)], 0.3: [(2, 2, 0.01465), (3, 2, 0.02088)], 0.2: [(3, 3, 0.01742)], 0.1: [(3, 5, 0.01020)]}
for p, lst in rep62.items():
    for L, m, rep in lst:
        kap = kappa(p, m)
        tt, v = golden_max(lambda t: F_block(L, p, slopes_minus(L, kap), t)[0], 0.1, 0.9, tol=1e-4)
        print(f"p={p}: (L') L={L}, m={m}: h >= {v/(L+m):.5f}   report: {rep:.5f}")
print(f"{time.time()-T0:.1f} s")
