"""w03: the pair (theta_na, R^max) and the level recursion of theory report section 11.18,

    R[T](g) = inf_{0<phi<1, 0<beta<g} sup_{gamma >= beta} [ min(gamma, phi*theta_na((g-beta)/phi)) + (1-phi)*T(gamma/(1-phi)) ],
    T_1 = theta_na,  T_{k+1} = min(T_k, R[T_k]),

for the heteropolymer chains of wsites.py.  Tested:
  (i)   game-function properties of F* = sum_j lam_j F*_j on a grid: zeros at 0 and 1, F*/t nonincreasing,
        F*/(1-t) nondecreasing, the limits E and a; concavity (second differences) -- F* need not be concave;
  (ii)  HintPair properties of (theta_na, R): R convex, slopes in [-1, 0], theta_na(e + R(e)) = R(e) (also e < 0);
  (iii) the lower barrier (DEAD_ENDS D45): no level of the recursion built on the pair lies below R^max, and the
        levels approach R^max;
  (iv)  mutations: the recursion built on the pair of a WRONG game function (zero residual; single dips only;
        the worst binary reduction of every ternary site) falls below the proved lower bound R^max.
usage: python3 w03_recursion.py <chain> [levels]
"""
import sys
import time

import numpy as np

from wlib import *
from wsites import chains

name = sys.argv[1] if len(sys.argv) > 1 else "mix"
levels = int(sys.argv[2]) if len(sys.argv) > 2 else 10
t00 = time.time()
ch = chains()[name]
NT = 801
ts = np.linspace(0.0, 1.0, NT)


def table(fun):
    return np.array([fun(t) if 0 < t < 1 else 0.0 for t in ts])


class Pair:
    """the pair of a game function tabulated on ts"""

    def __init__(self, F, label):
        self.F, self.label = F, label
        self.E = float(np.max(F[1:] / ts[1:]))
        self.a = float(np.max(F[:-1] / (1 - ts[:-1])))

    def R(self, e):
        e = np.atleast_1d(np.asarray(e, float))
        obj = self.F[None, :] - e[:, None] * ts[None, :]
        k = np.argmax(obj, axis=1)
        out = obj[np.arange(len(e)), k]
        # quadratic refinement of the grid maximum
        kk = np.clip(k, 1, NT - 2)
        y0, y1, y2 = obj[np.arange(len(e)), kk - 1], obj[np.arange(len(e)), kk], obj[np.arange(len(e)), kk + 1]
        den = y0 - 2 * y1 + y2
        with np.errstate(divide="ignore", invalid="ignore"):
            corr = np.where(den < 0, -(y2 - y0) ** 2 / (8 * den), 0.0)
        corr = np.where((k > 0) & (k < NT - 1), np.minimum(corr, 1e-5), 0.0)
        return out + corr

    def theta_na(self, x):
        """max_{tau<1} (F(tau) - tau x)/(1-tau), 0 beyond E"""
        x = np.atleast_1d(np.asarray(x, float))
        obj = (self.F[None, :-1] - x[:, None] * ts[None, :-1]) / (1 - ts[None, :-1])
        return np.maximum(obj.max(axis=1), 0.0)


def binary_reduction_sites(s):
    """the three coarse-grainings {a} | rest of a ternary site as binary sites (possibly asymmetric)"""
    out = []
    for a in range(s.q):
        rest = [b for b in range(s.q) if b != a]
        u01 = min(s.d[a, b] for b in rest)          # psi(B) - psi(B^c) <= d(a', b') for all a' in B, b' in B^c
        u10 = min(s.d[b, a] for b in rest)
        out.append(Site([s.pi[a], 1 - s.pi[a]], [[0, u01], [u10, 0]], f"{s.name}|{{{a}}}"))
    return out


# ---- game functions -------------------------------------------------------------------------------------------
Fstar = table(ch.Fstar)
P_true = Pair(Fstar, "all vertices, hardest additive instance (F*)")
F0 = table(lambda t: sum(l * s.F(np.zeros(s.q), t) for l, s in zip(ch.lam, ch.sites)))
P_zero = Pair(F0, "zero residual gamma = 0")
chd = Chain(ch.sites, ch.lam, cols=[np.where(s.is_dist)[0] for s in ch.sites])
Fdip = table(chd.Fstar)
P_dip = Pair(Fdip, "single dips only (distance-function vertices), hardest additive instance")
Fred = np.zeros(NT)
for l, s in zip(ch.lam, ch.sites):
    if s.q == 2:
        Fred += l * table(lambda t: s.Fstar(t))
    else:
        reds = binary_reduction_sites(s)
        Fred += l * np.max([table(lambda t, r=r: r.Fstar(t)) for r in reds], axis=0)
P_red = Pair(Fred, "worst binary reduction of every site (pointwise maximum over the cuts)")

print(f"=== w03: chain {ch.name}, fractions {ch.lam} ===")
E, a = ch.E(), ch.a()[0]
print(f"(i) game function F* on {NT} points: F*(0) = F*(1) = 0; max F* = {Fstar.max():.6f} at t = {ts[np.argmax(Fstar)]:.4f};")
r1 = Fstar[1:] / ts[1:]
r2 = Fstar[:-1] / (1 - ts[:-1])
print(f"    F*(t)/t nonincreasing: largest increase {np.max(np.diff(r1)):.2e}; value at t = 1/800: {r1[0]:.6f}, E = sum_j lam_j E_j = {E:.6f}")
print(f"    F*(t)/(1-t) nondecreasing: largest decrease {np.max(-np.diff(r2)):.2e}; value at t = 1 - 1/800: {r2[-1]:.6f}, a = sum_j lam_j a_j = {a:.6f}")
d2 = Fstar[:-2] - 2 * Fstar[1:-1] + Fstar[2:]
print(f"    concavity: largest second difference {d2.max():.3e} (x {(NT-1)**2} = second derivative {d2.max()*(NT-1)**2:+.4f}) at t = {ts[1:-1][np.argmax(d2)]:.4f}"
      f"  -> F* is {'concave on the grid' if d2.max() < 1e-12 else 'NOT concave'}")
for j, s in enumerate(ch.sites):
    Fj = table(lambda t: s.Fstar(t))
    d2j = Fj[:-2] - 2 * Fj[1:-1] + Fj[2:]
    print(f"    site {s.name}: largest second difference of F*_j: {d2j.max():.3e} at t = {ts[1:-1][np.argmax(d2j)]:.4f}")

# ---- (ii) pair properties ---------------------------------------------------------------------------------------
es = np.linspace(-0.9 * a, 1.05 * E, 400)
R = P_true.R(es)
slopes = np.diff(R) / np.diff(es)
conv = np.diff(R, 2)
S = es + R
idn = np.max(np.abs(P_true.theta_na(S[S > 1e-6]) - R[S > 1e-6]))
print(f"(ii) R convex: smallest second difference {conv.min():.2e}; slopes in [{slopes.min():.5f}, {slopes.max():.5f}];"
      f" S = e + R nondecreasing: {bool(np.all(np.diff(S) > -1e-9))}; pair identity theta_na(e + R(e)) = R(e) on 400 accuracies (both signs): max abs error {idn:.1e}")
print(f"     h = R(0) = {float(P_true.R(0.0)[0]):.6f}; theta_na(h) = {float(P_true.theta_na(P_true.R(0.0))[0]):.6f}; R(E) = {float(P_true.R(E)[0]):.2e}")


# ---- (iii), (iv) the recursion ------------------------------------------------------------------------------------
def recursion(pair, levels, Eref):
    gs = Eref * np.concatenate([np.geomspace(1e-3, 0.05, 12)[:-1], np.linspace(0.05, 0.995, 48)])
    xs = np.concatenate([[0.0], gs, [Eref, 50.0]])                       # nodes of the piecewise-linear T
    phis = np.linspace(0.02, 0.98, 49)
    bfr = np.array([0.003, 0.01, 0.03, 0.06, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.97])
    lam = np.linspace(0.0, 1.0, 41)
    G, PH, B = np.meshgrid(gs, phis, bfr, indexing="ij")
    beta = G * B
    mu = PH * pair.theta_na(((G - beta) / PH).ravel()).reshape(G.shape)
    top = np.maximum(beta, mu)
    gam = beta[..., None] + (top - beta)[..., None] * lam                 # gamma in [beta, max(beta, mu)]
    T = pair.theta_na(gs)
    out = [T.copy()]
    for k in range(1, levels):
        Tn = np.concatenate([[T[0]], T, [0.0, 0.0]])
        Tn[-2] = min(T[-1], float(pair.theta_na(np.array([Eref]))[0]))
        val = np.minimum(gam, mu[..., None]) + (1 - PH)[..., None] * np.interp(gam / (1 - PH)[..., None], xs, Tn)
        sup = val.max(axis=-1)
        RT = sup.reshape(len(gs), -1).min(axis=1)
        T = np.minimum(T, RT)
        out.append(T.copy())
    return gs, np.array(out)


show = [0.01, 0.05, 0.1, 0.25, 0.5, 0.75]
for pair in (P_true, P_zero, P_dip, P_red):
    gs, Tk = recursion(pair, levels, E)
    Rtrue = P_true.R(gs)
    Rown = pair.R(gs)
    low = (Tk - Rtrue[None, :]).min() / a
    print(f"\n(iii/iv) recursion built on the pair of: {pair.label}")
    print(f"     own E = {pair.E:.6f}, own a = {pair.a:.6f}, own h = {float(pair.R(0.0)[0]):.6f}   (true: E = {E:.6f}, a = {a:.6f}, h = {float(P_true.R(0.0)[0]):.6f})")
    idx = [int(np.argmin(np.abs(gs / E - f))) for f in show]
    print("     g/E      " + "  ".join(f"{gs[i]/E:7.3f}" for i in idx))
    for k in (0, 1, 3, levels - 1):
        print(f"     T_{k+1:<2d}/a   " + "  ".join(f"{Tk[k][i]/a:7.4f}" for i in idx))
    print("     R^max/a  " + "  ".join(f"{Rtrue[i]/a:7.4f}" for i in idx))
    print("     own R/a  " + "  ".join(f"{Rown[i]/a:7.4f}" for i in idx))
    print(f"     min over levels and accuracies of (T_k - R^max)/a = {low:+.5f}"
          f"  -> {'never below the lower bound' if low > -2e-4 else 'FALLS BELOW the proved lower bound R^max'};"
          f" max_g (T_{levels} - own R)/a = {((Tk[-1] - Rown).max())/a:+.5f}")
print(f"time {time.time()-t00:.0f} s")
