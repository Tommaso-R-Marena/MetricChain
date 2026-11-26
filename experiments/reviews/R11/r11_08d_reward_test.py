"""R11 / 08d -- finite-horizon test of my safe REWARD recursion (threshold version of Prop. G):
the exact maximum over ALL vertices of KL(pi || pi_phi) for n = 3, 4 against the safe recursion
(must be >=), and against ln Z_n(h)/Z_n(0).

Run:  python3 r11_08d_reward_test.py     (seconds)
"""
import numpy as np
from r11lib import *
from r11_08_propG import Grid, u, BIG

h = u / 2


def height_functions(n):
    N = 2 ** n
    out = []
    f = [None] * N
    f[0] = 0

    def rec(x):
        if x == N:
            out.append(list(f))
            return
        nb = [x ^ (1 << i) for i in range(n) if (x ^ (1 << i)) < x]
        cands = {f[nb[0]] + 1, f[nb[0]] - 1}
        for y in nb[1:]:
            cands &= {f[y] + 1, f[y] - 1}
        for v in cands:
            f[x] = v
            rec(x + 1)
        f[x] = None

    rec(1)
    return np.array(out, dtype=float) * u


for n in (3, 4):
    V = height_functions(n)
    for p in (0.4, 0.3, 0.2, 0.1):
        s, pi = chain_law(n, p)
        logP = gibbs_logs(np.log(pi), V)
        kl = (pi * np.log(pi)).sum() - logP @ pi               # KL(pi || pi_phi) for every vertex
        exact = float(kl.max())
        unif = float(np.log((pi * np.exp(h * s.sum(axis=1))).sum()))
        out = []
        for G in (201, 801):
            gr = Grid(p, G)
            tp = lambda lam: (1 - p) * np.exp(lam / 2) / ((1 - p) * np.exp(lam / 2) + p * np.exp(-lam / 2))
            k = lambda lam: (1 - p) * np.log((1 - p) / tp(lam)) + p * np.log(p / (1 - tp(lam)))
            kmax = np.maximum(k(gr.e[:-1]), k(gr.e[1:]))
            inside = (gr.e[1:] > -u - 1e-12) & (gr.e[:-1] < u + 1e-12)
            # last site: lam in [-u, u], reward only; cells that touch [-u, u] get the maximum of k over the part inside
            e1, e2 = np.clip(gr.e[:-1], -u, u), np.clip(gr.e[1:], -u, u)
            W = np.where(inside, np.maximum(k(e1), k(e2)), -BIG)
            for lev in range(n - 2):                           # middle sites
                rm = gr.rmq(W, 'max')
                val = np.where(gr.feas, (1 - p) * rm + p * W[::-1][None, :], -BIG)
                W = kmax + val.max(axis=1)
            # first site: no previous letter, P = (1/2, 1/2); reward KL((1/2,1/2) || tau_lam), tau = logistic(lam)
            t0 = lambda lam: 1.0 / (1.0 + np.exp(-lam))
            k0 = lambda lam: 0.5 * np.log(0.5 / t0(lam)) + 0.5 * np.log(0.5 / (1 - t0(lam)))
            k0max = np.maximum(k0(gr.e[:-1]), k0(gr.e[1:]))
            rm = gr.rmq(W, 'max')
            val = np.where(gr.feas, 0.5 * rm + 0.5 * W[::-1][None, :], -BIG)
            root = k0max + val.max(axis=1)
            out.append(float(root.max()))
        print(f"n={n} p={p}: exact max_phi KL(pi||pi_phi) over {V.shape[0]} vertices = {exact:.7f};  uniform field {unif:.7f};"
              f"  safe recursion G=201: {out[0]:.7f}, G=801: {out[1]:.7f};  safe >= exact: {out[1] >= exact - 1e-10}")
