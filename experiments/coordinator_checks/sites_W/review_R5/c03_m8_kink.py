"""m8: the slope jump of F* at the label switch of the triangle site (published +0.0052, reviewer +0.0056).  Own code.
Three routes: (1) branch-wise: G^A(t), G^B(t) = Renyi programme restricted to the two label structures, crossing t_c by bisection,
slopes by the envelope theorem (analytic d/dt at the optimal M) and by central differences; (2) one-sided difference quotients of
the unrestricted F* with Richardson extrapolation; (3) the workstream's estimate (second difference on a grid of step 5e-4)."""
import sys, time, math
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import minimize
import dlib
import mpmath as mp

t0 = time.time()
site = dlib.Site(*dlib.SITES["tri"])
d = site.d
print("vertices (g[0] = 0) and their kind:")
kinds = []
for v in site.V:
    kind = None
    for b in range(3):
        if np.allclose(v, d[:, b] - d[0, b], atol=1e-9): kind = "dip at %d" % b
        if np.allclose(v, -(d[b, :] - d[b, 0]), atol=1e-9) or np.allclose(v, -(d[:, b] - d[0, b]), atol=1e-9): kind = "anti-dip at %d" % b
    kinds.append(kind)
    print("   ", np.round(v, 4), kind)


def G_restricted(t, idx, dps=30):
    """max over M supported on idx of -t ln sum_a (sum_phi M pi_phi^t)^(1/t), in mpmath (Newton on the simplex via SLSQP start)."""
    P = site.P[idx]
    Pt = P ** t
    k = len(idx)

    def N(M):
        return float(((M @ Pt) ** (1 / t)).sum())

    def dN(M):
        return (Pt * ((M @ Pt) ** (1 / t - 1))[None, :]).sum(axis=1) / t
    best = None
    for s in range(4):
        M0 = np.ones(k) / k if s == 0 else np.random.default_rng(s).dirichlet(np.ones(k))
        res = minimize(N, M0, jac=dN, method="SLSQP", bounds=[(0, 1)] * k,
                       constraints=[{"type": "eq", "fun": lambda M: M.sum() - 1, "jac": lambda M: np.ones(k)}], options={"ftol": 1e-16, "maxiter": 2000})
        M = np.clip(res.x, 0, None); M /= M.sum()
        if best is None or N(M) < best[0]:
            best = (N(M), M)
    M = best[1]
    # polish in high precision: Newton for the stationarity conditions dN/dM_i = const on the support (all weights positive here)
    mp.mp.dps = dps
    Pm = [[mp.mpf(float(x)) for x in row] for row in P]
    tm = mp.mpf(t)
    def grad_eqs(*z):
        Mv = list(z[:k - 1]); Mv.append(1 - sum(Mv))
        s = [sum(Mv[i] * Pm[i][a] ** tm for i in range(k)) for a in range(3)]
        g = [sum(Pm[i][a] ** tm * s[a] ** (1 / tm - 1) for a in range(3)) for i in range(k)]
        return [g[i] - g[k - 1] for i in range(k - 1)]
    try:
        sol = mp.findroot(grad_eqs, [mp.mpf(float(x)) for x in M[:k - 1]], tol=mp.mpf(10) ** (-(dps - 8)))
        Mv = [sol[i] for i in range(k - 1)]; Mv.append(1 - sum(Mv))
    except Exception as ex:
        Mv = [mp.mpf(float(x)) for x in M]
    s = [sum(Mv[i] * Pm[i][a] ** tm for i in range(k)) for a in range(3)]
    Nval = sum(sa ** (1 / tm) for sa in s)
    G = -tm * mp.log(Nval)
    # envelope theorem: dG/dt = partial_t G at fixed M:  -ln N - t (dN/dt)/N,  dN/dt = sum_a s^(1/t) [ -ln(s)/t^2 + (1/t) (ds/dt)/s ]
    dsdt = [sum(Mv[i] * Pm[i][a] ** tm * mp.log(Pm[i][a]) for i in range(k)) for a in range(3)]
    dNdt = sum(s[a] ** (1 / tm) * (-mp.log(s[a]) / tm ** 2 + dsdt[a] / (tm * s[a])) for a in range(3))
    dG = -mp.log(Nval) - tm * dNdt / Nval
    return G, dG, [float(x) for x in Mv]


names = {k: i for i, k in enumerate(kinds)}
A = [names["dip at 2"], names["anti-dip at 2"], names["dip at 0"]]
B = [names["dip at 2"], names["dip at 0"], names["dip at 1"]]
print("branch A = {dip at 2, anti-dip at 2, dip at 0} -> vertex indices", A, "; branch B = three dips -> (2, 0, 1) indices", B)

# (1) crossing of the two branches
lo, hi = 0.370, 0.386
for _ in range(60):
    mid = 0.5 * (lo + hi)
    if G_restricted(mid, A)[0] >= G_restricted(mid, B)[0]: lo = mid
    else: hi = mid
tc = 0.5 * (lo + hi)
GA, dGA, MA = G_restricted(tc, A); GB, dGB, MB = G_restricted(tc, B)
full = dlib.renyi(site, tc)
print("(1) t_c = %.9f;  G^A = %.12f, G^B = %.12f, unrestricted F* = %.12f (dual bound %.12f)" % (tc, float(GA), float(GB), full[0], full[1]))
print("    weights at t_c:  A (dip 2, anti-dip 2, dip 0) = %s;   B (dip 2, dip 0, dip 1) = %s" % (np.round(MA, 4), np.round(MB, 4)))
print("    branch slopes by the envelope theorem:  dG^A/dt = %.9f,  dG^B/dt = %.9f;   SLOPE JUMP = %+.9f" % (float(dGA), float(dGB), float(dGB - dGA)))
for h in (1e-3, 1e-4, 1e-5):
    cA = (G_restricted(tc + h, A)[0] - G_restricted(tc - h, A)[0]) / (2 * h); cB = (G_restricted(tc + h, B)[0] - G_restricted(tc - h, B)[0]) / (2 * h)
    print("    central differences, h = %.0e:  A %.9f, B %.9f, jump %+.9f" % (h, float(cA), float(cB), float(cB - cA)))
# which branch is the larger one on each side, and is the unrestricted optimum one of the two?
for tt in (tc - 0.004, tc - 0.0005, tc + 0.0005, tc + 0.004):
    a_, b_ = float(G_restricted(tt, A)[0]), float(G_restricted(tt, B)[0]); f_ = dlib.renyi(site, tt)
    print("    t = %.6f: G^A = %.12f, G^B = %.12f, F* = %.12f [dual %.12f]  -> F* - max(G^A, G^B) = %.1e, larger branch: %s" % (tt, a_, b_, f_[0], f_[1], f_[0] - max(a_, b_), "A" if a_ > b_ else "B"))

# (2) one-sided difference quotients of the unrestricted F*, Richardson
def F(t):
    v = dlib.renyi(site, t); return v[0]
print("(2) one-sided quotients of the unrestricted F* at t_c (h, left slope, right slope, jump), and Richardson (2 q(h) - q(2h)):")
prev = None
for h in (4e-3, 2e-3, 1e-3, 5e-4):
    left = (F(tc) - F(tc - h)) / h; right = (F(tc + h) - F(tc)) / h
    line = "    h = %.0e: left %.8f, right %.8f, jump %+.8f" % (h, left, right, right - left)
    if prev is not None:
        line += "   | Richardson: left %.8f, right %.8f, jump %+.8f" % (2 * left - prev[0], 2 * right - prev[1], (2 * right - prev[1]) - (2 * left - prev[0]))
    prev = (left, right)
    print(line)

# (3) the workstream's estimate: second difference on the grid t_k = k/2000 at the grid point nearest to the kink, times 2000
k0 = round(tc * 2000)
Fs = [F((k0 + i) / 2000) for i in (-1, 0, 1)]
print("(3) workstream's formula ((F[k+1]-F[k]) - (F[k]-F[k-1]))*2000 at t_k = %.4f: %+.5f   (w08_misc.txt prints +0.00516; W_REPORT rounds to +0.0052)" % (k0 / 2000, ((Fs[2] - Fs[1]) - (Fs[1] - Fs[0])) * 2000))
# curvature of each branch, to explain the bias: second difference = J (1 - |t_c - t_k|/h) + F'' h
h = 1e-3
ddA = float((G_restricted(tc + h, A)[0] - 2 * G_restricted(tc, A)[0] + G_restricted(tc - h, A)[0]) / h ** 2)
ddB = float((G_restricted(tc + h, B)[0] - 2 * G_restricted(tc, B)[0] + G_restricted(tc - h, B)[0]) / h ** 2)
J = float(dGB - dGA)
print("    curvatures of the branches at t_c: A %.4f, B %.4f;  predicted second-difference estimate J(1 - |t_c - t_k|/h) + F''h (h = 5e-4): %+.5f" %
      (ddA, ddB, J * (1 - abs(tc - k0 / 2000) / 5e-4) + 0.5 * (ddA + ddB) * 5e-4))

# the corner of Rhat: e_c with both branches optimal; slopes -t on both sides
E = dlib.E_site(site)
# R(e) = max_t F*(t) - t e; on branch A the maximiser tA(e) solves G^A'(t) = e, etc.  Corner: e where max_t[G^A - te] = max_t[G^B - te].
def branch_R(e, idx, a=0.30, b=0.46):
    t, v = dlib.golden(lambda t: float(G_restricted(t, idx, dps=20)[0]) - t * e, a, b, tol=1e-9)
    return v, t
lo, hi = 0.15 * E, 0.25 * E
for _ in range(34):
    mid = 0.5 * (lo + hi)
    # for small e the maximiser is at larger t (branch B side); A wins for larger e
    if branch_R(mid, B)[0] >= branch_R(mid, A)[0]: lo = mid
    else: hi = mid
ec = 0.5 * (lo + hi)
vA, tA = branch_R(ec, A); vB, tB = branch_R(ec, B)
print("corner of Rhat: e_c = %.6f = %.4f E (E = %.6f); Rhat(e_c) = %.7f; maximisers t = %.4f (branch A) and %.4f (branch B): slope of Rhat jumps from %.4f to %.4f" %
      (ec, ec / E, E, vA, tA, tB, -max(tA, tB), -min(tA, tB)))
print("time %.1f s" % (time.time() - t0))
