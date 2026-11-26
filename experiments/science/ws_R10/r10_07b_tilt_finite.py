"""r10_07b: validity test of the cell-based safe recursion on FINITE chains: the safe value
must be >= the exact maximum over ALL vertices of (1-t) D_t(pi_phi || Q), Q = stationary
symmetric Markov chain with flip probability q~ (also q~ < p, which Y did not test), and of
KL(pi || pi_phi), KL(pi_phi || Q).  n = 3, 4, 5."""
import sys, time
import numpy as np
from r10lib import *
from r10_tilt import Tilt

u = 1.0
t0 = time.time()


def finite_renyi(T, n, t, qt):
    """Safe (or restricted) value of max over tilt processes with (*) of -ln sum pi_phi^t Q^(1-t)."""
    G = T.G
    ap, am = T.renyi_stage(t, qt)
    if T.mode == "safe":
        leaf_ok = (T.edges[:-1] <= u + 1e-15) & (T.edges[1:] >= -u - 1e-15)
        lamA, lamB = T.edges[:-1], T.edges[1:]
    else:
        leaf_ok = np.abs(T.mid) <= u + 1e-15
        lamA = lamB = T.mid
    w = np.where(leaf_ok, ap + am, np.inf)
    for i in range(n - 1, 1, -1):
        w = T.renyi_apply(w, ap, am)
    # root: law (1/2,1/2) tilted by lambda_1; Q's first-site law (1/2,1/2)
    tpA = 1 / (1 + np.exp(-lamA)); tmB = 1 - 1 / (1 + np.exp(-lamB))
    bp = tpA ** t * 0.5 ** (1 - t); bm = tmB ** t * 0.5 ** (1 - t)
    if n == 1:
        val = np.where(leaf_ok, bp + bm, np.inf).min()
    else:
        val = T.renyi_apply(w, bp, bm).min()
    return -np.log(val)


def finite_thr(T, n, qt):
    """max over tilt processes of KL(Q || pi_phi), Q = Markov(qt) (qt = p: KL(pi||pi_phi))."""
    G = T.G
    rew = np.maximum(T.kl_q_tau(T.lam_a, qt), T.kl_q_tau(T.lam_b, qt))
    if T.mode == "safe":
        leaf_ok = (T.edges[:-1] <= u + 1e-15) & (T.edges[1:] >= -u - 1e-15)
        lamA, lamB = T.edges[:-1], T.edges[1:]
    else:
        leaf_ok = np.abs(T.mid) <= u + 1e-15
        lamA = lamB = T.mid
    w = np.where(leaf_ok, rew, -np.inf)
    for i in range(n - 1, 1, -1):
        R = -T._range_min(-w); R = np.where(T.valid, R, -np.inf)
        w = rew + ((1 - qt) * R + qt * w[::-1][None, :]).max(axis=1)
    def k1(lam):
        tp = 1 / (1 + np.exp(-lam))
        return 0.5 * np.log(0.5 / tp) + 0.5 * np.log(0.5 / (1 - tp))
    rew1 = np.maximum(k1(lamA), k1(lamB))
    if n == 1:
        return np.where(leaf_ok, rew1, -np.inf).max()
    R = -T._range_min(-w); R = np.where(T.valid, R, -np.inf)
    return (rew1 + (0.5 * R + 0.5 * w[::-1][None, :]).max(axis=1)).max()


worst_safe = 1e9; worst_restr = -1e9; cnt = 0; maxgap = 0.0
rows = []
for n in (3, 4, 5):
    V = hom_vertices(n).astype(float) * u
    for p in (0.4, 0.3, 0.1):
        pi = binary_chain_law(n, p)
        W, _ = gibbs(pi, V)
        lw = np.log(W)
        Ts = Tilt(p, u, 401, "safe"); Tr = Tilt(p, u, 401, "restricted_mid")
        for qt in (p, 0.85 * p, 0.6 * p, min(0.5, 1.3 * p)):
            Q = binary_chain_law(n, qt)
            for t in (0.25, 0.45, 0.7):
                exact = -np.log(((W ** t) @ (Q ** (1 - t))).min())
                s = finite_renyi(Ts, n, t, qt); r = finite_renyi(Tr, n, t, qt)
                worst_safe = min(worst_safe, s - exact); worst_restr = max(worst_restr, r - exact)
                maxgap = max(maxgap, (s - exact) / exact)
                cnt += 1
                rows.append((n, p, qt, t, exact, r, s))
            exactE = (float(Q @ np.log(Q)) - lw @ Q).max()
            sE = finite_thr(Ts, n, qt); rE = finite_thr(Tr, n, qt)
            worst_safe = min(worst_safe, sE - exactE); worst_restr = max(worst_restr, rE - exactE)
            cnt += 1
            rows.append((n, p, qt, 0.0, exactE, rE, sE))
print("n   p    q~     t     exact max over all vertices   restricted_mid(G=401)   safe(G=401)")
for r in rows:
    if r[0] == 4 or (r[0] == 5 and r[1] == 0.1):
        print("%d  %.1f  %.3f  %.2f   %.7f   %.7f   %.7f   %s" % (r + (("<-- relaxation not tight (restricted > exact)" if r[5] > r[4] + 1e-6 else ""),)))
print("%d cases: smallest (safe - exact) = %.2e (must be >= 0);  largest (restricted - exact) = %.2e (>0 means: the relaxation is strictly weaker than the class);  largest relative excess of safe %.3f"
      % (cnt, worst_safe, worst_restr, maxgap))
print("time %.1fs" % (time.time() - t0))
