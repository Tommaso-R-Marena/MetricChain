"""R11 / 10 -- structure claims (section 7) and Lemma B, with ALL vertices.

(a) vertices of the Lipschitz polytope of the n-cube with uniform slope = height functions
    (|f(x) - f(x^i)| = u on every edge): counts 2, 6, 38, 990 for n = 1..4 (my own enumeration);
    n <= 3 against the spanning-tree enumeration;
(b) exact F*_n(0.45)/n at p = 0.4, n = 1..4 (report: 0.02895, 0.03280, 0.03359, 0.03354);
(c) p = 0.1, n = 4: a_4 with all vertices against site-wise labels only (report: 0.5726559
    against 0.5626014, weight 0.092 on f = -min(|x|, 4-|x|));  p >= 0.3: no weight off site-wise labels;
(d) the Renyi centre is not a Markov chain: I(x1; x3 | x2) under Q* (n = 4, t = 0.45; report 2.9e-3, 5.7e-3, 1.2e-3 for p = 0.4, 0.3, 0.1);
(e) Lemma B (product theorem) with all vertices: X1 = a two-site chain block, X2 = one site with a
    field; F*[X1 x X2] over the 38 vertices of the 3-cube against F*[X1] + F*[X2].

Run:  python3 r11_10_structure.py        (about 1-2 minutes)
"""
import time
import numpy as np
from r11lib import *

T0 = time.time()
u = 1.0
h = u / 2


def height_functions(n):
    """all f on {0..2^n-1} with f(0) = 0 and |f(x) - f(x ^ (1<<i))| = 1 on every edge (in units of u)."""
    N = 2 ** n
    out = []
    f = [None] * N
    f[0] = 0

    def rec(x):
        if x == N:
            out.append(list(f))
            return
        # neighbours with smaller index
        nb = [x ^ (1 << i) for i in range(n) if (x ^ (1 << i)) < x]
        cands = {f[nb[0]] + 1, f[nb[0]] - 1}
        for y in nb[1:]:
            cands &= {f[y] + 1, f[y] - 1}
        for v in cands:
            f[x] = v
            rec(x + 1)
        f[x] = None

    rec(1)
    return np.array(out, dtype=float)


print("== (a) vertex counts ==")
H = {}
for n in (1, 2, 3, 4):
    H[n] = height_functions(n) * u
    line = f"n={n}: {H[n].shape[0]} height functions"
    if n <= 3:
        V = lipschitz_vertices(n, [u] * n)
        a = {tuple(np.round(v, 6)) for v in V}
        b = {tuple(np.round(v, 6)) for v in H[n]}
        line += f";  spanning-tree enumeration: {V.shape[0]} vertices;  same set: {a == b}"
    print(line)

print("\n== (b) exact F*_n(0.45)/n at p = 0.4 (report: 0.02895, 0.03280, 0.03359, 0.03354) ==")
row = []
for n in (1, 2, 3, 4):
    s, pi = chain_law(n, 0.4)
    logP = gibbs_logs(np.log(pi), H[n])
    lo, up, M = maximise_G_fast(logP, 0.45)
    row.append(f"n={n}: [{lo/n:.5f}, {up/n:.5f}]")
print("   " + "  ".join(row))

print("\n== (c) n = 4: all 990 vertices against the 16 site-wise labels ==")
n = 4
s, pi0 = chain_law(n, 0.5)
sig = configs(n).astype(float)
site_phis = -h * sig @ s.T.astype(float)
site_phis -= site_phis[:, [0]]                         # normalise f(0) = 0 (index 0 = all +1)
is_site = np.array([any(np.allclose(v, sp) for sp in site_phis) for v in H[n]])
print(f"   {is_site.sum()} of the 990 vertices are site-wise labels")
mag = s.sum(axis=1)
fpara = -np.minimum((n - mag) / 2, n - (n - mag) / 2) * u     # -min(|x|, 4 - |x|), |x| = number of -1
fpara -= fpara[0]
ipara = [k for k, v in enumerate(H[n]) if np.allclose(v, fpara) or np.allclose(v, -fpara)]
for p in (0.4, 0.3, 0.1):
    s, pi = chain_law(n, p)
    logP = gibbs_logs(np.log(pi), H[n])
    la, ua, Ma = maximise_a_fast(logP)
    ls, us_, Ms = maximise_a_fast(logP[is_site])
    lt, ut, Mt = maximise_G_fast(logP, 0.45)
    lts, uts, Mts = maximise_G_fast(logP[is_site], 0.45)
    le, ue, Me = maximise_E_fast(logP)
    print(f"   p={p}: a_4 = [{la:.7f}, {ua:.7f}] (site-wise only {ls:.7f}); weight off site-wise labels {Ma[~is_site].sum():.4f}"
          f" (on +-min(|x|,4-|x|): {Ma[ipara].sum():.4f})")
    print(f"          F*_4(0.45) = [{lt:.7f}, {ut:.7f}] (site-wise only {lts:.7f}), weight off site-wise {Mt[~is_site].sum():.1e};"
          f"  E_4 = [{le:.7f}, {ue:.7f}], ln Z_4(h)/Z_4(0) = {np.log((pi*np.exp(h*s.sum(axis=1))).sum()):.7f}   [{time.time()-T0:.0f} s]", flush=True)

print("\n== (d) the Renyi centre is not Markov (n = 4, t = 0.45) ==")
for p in (0.4, 0.3, 0.1):
    s, pi = chain_law(n, p)
    logP = gibbs_logs(np.log(pi), H[n])
    lo, up, M = maximise_G_fast(logP, 0.45)
    Q = np.exp(centre_of_M(logP, M, 0.45))
    # I(x1; x3 | x2) under Q
    def cmi(Pr):
        b = ((s + 1) // 2).astype(int)                # 1 for +1, 0 for -1
        J = np.zeros((2, 2, 2))
        np.add.at(J, (b[:, 0], b[:, 1], b[:, 2]), Pr)
        tot = 0.0
        for x2 in range(2):
            pj = J[:, x2, :]
            m = pj.sum()
            pa, pc = pj.sum(axis=1), pj.sum(axis=0)
            for a in range(2):
                for c in range(2):
                    if pj[a, c] > 0:
                        tot += pj[a, c] * np.log(pj[a, c] * m / (pa[a] * pc[c]))
        return tot
    sup = np.where(M > 1e-6)[0]
    kinds = "uniform fields only" if all(np.allclose(np.abs(H[n][k] - H[n][k][0]), np.abs(h * (s.sum(axis=1) - n))) for k in sup) else "other labels too"
    print(f"   p={p}: I(x1;x3|x2) under Q* = {cmi(Q):.2e}  (under pi: {cmi(pi):.1e});  support of M*: {len(sup)} labels ({kinds})")

print("\n== (e) Lemma B with all vertices ==")
for p in (0.3, 0.1):
    for t in (0.3, 0.6):
        s2, pi2 = chain_law(2, p)
        s3 = configs(3)
        # X1 = sites 0,1 (chain block), X2 = site 2 with law (0.7, 0.3); product law on the 3-cube
        idx = np.arange(8)
        law = pi2[idx & 3] * np.where(s3[:, 2] == 1, 0.7, 0.3)
        F12 = maximise_G_fast(gibbs_logs(np.log(law), H[3]), t)
        F1 = maximise_G_fast(gibbs_logs(np.log(pi2), H[2]), t)
        F2 = maximise_G_fast(gibbs_logs(np.log(np.array([0.7, 0.3])), H[1]), t)
        print(f"   p={p} t={t}: F*[X1 x X2] = [{F12[0]:.9f}, {F12[1]:.9f}];  F*[X1] + F*[X2] = {F1[0]+F2[0]:.9f}")
print(f"{time.time()-T0:.1f} s")
