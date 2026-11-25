#!/usr/bin/env python3
"""t07 -- small cubes: the isoperimetric statement for the flat-histogram instance H on ALL subsets of Q_3, Q_4
(exhaustive) and by simulated annealing on Q_5, Q_6 (fixed seeds), for a two-phase (or any) Curie-Weiss known part.
For every D:  e_D = ln Phi+_H(D)/n,  theta_D = -ln maxdens(D)/n  (and -ln mu_H(D)/n);
   omega(D) = least omega >= 0 with theta_D <= R(e_D - omega) + omega,     R = the binary single-letter function (table of t09)
(the theorem says omega_n := max_D omega(D) -> 0).  Also, for n <= 4: the exact tail function
   Xi_md(q) = max{ Phi_H(D) : maxdens(D) <= q }   against its restriction to unions of profile classes around one centre.
usage: python3 t07_smallcubes.py bJ bB u table_tag n1,n2,...
"""
import sys, time, math, itertools
import numpy as np
from scipy.special import gammaln, logsumexp
import tlib as T

bJ, bB, u = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
tag = sys.argv[4]
ns = [int(x) for x in sys.argv[5].split(",")]
phi = T.phi_cw(bJ, bB)
tab = np.loadtxt(f"../out/Rtable_{tag}.txt")
te, tR = tab[:, 0], tab[:, 1]
# continuation of R: below the table R(e) = max(-e, linear continuation with the last slope); above: 0 from E on
slope_lo = (tR[1] - tR[0]) / (te[1] - te[0])


def Rfun(e):
    e = np.asarray(e, dtype=float)
    out = np.interp(e, te, tR)
    low = e < te[0]
    out = np.where(low, np.maximum(-e, tR[0] + slope_lo * (e - te[0])), out)
    hi = e > te[-1]
    out = np.where(hi, np.maximum(tR[-1] + (tR[-1] - tR[-2]) / (te[-1] - te[-2]) * (e - te[-1]), 0.0), out)
    return np.maximum(out, np.maximum(-e, 0.0))


def omega_of(eD, thD):
    """least omega >= 0 with thD <= R(eD - omega) + omega (vectorised bisection; the right side increases with omega)"""
    eD = np.asarray(eD, dtype=float)
    thD = np.asarray(thD, dtype=float)
    lo = np.zeros_like(eD)
    hi = np.full_like(eD, 2.0 * u + 2.0)
    ok0 = thD <= Rfun(eD)
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        ok = thD <= Rfun(eD - mid) + mid
        hi = np.where(ok, mid, hi)
        lo = np.where(ok, lo, mid)
    return np.where(ok0, 0.0, hi)


t0 = time.time()
print(f"Curie-Weiss bJ={bJ} bB={bB} u={u}; R from table '{tag}' ({len(te)} points, e in [{te[0]:.3f},{te[-1]:.3f}])")
for n in ns:
    N = 2 ** n
    X = np.array(list(itertools.product([0, 1], repeat=n)), dtype=np.int8)
    wt = X.sum(axis=1)
    Dm = (X[:, None, :] != X[None, :, :]).sum(axis=2).astype(float)
    tt = np.arange(n + 1)
    lCn = gammaln(n + 1.0) - gammaln(tt + 1.0) - gammaln(n - tt + 1.0)
    logw = lCn - n * phi(tt / n)
    J = -(logw - logsumexp(logw))
    V = J.copy()
    for t in range(1, n + 1):
        V[t] = min(V[t], V[t - 1] + u)
    for t in range(n - 1, -1, -1):
        V[t] = min(V[t], V[t + 1] + u)
    pi = np.exp(-J[wt] - lCn[wt])
    w = np.exp(V[wt])                          # weights of H: psi_H = -V_n(|x|)
    ZH = float((pi * w).sum())
    mu = pi * w / ZH
    M = u * Dm - V[wt][:, None] + V[wt][None, :]          # slack s_H(x,y) = u d(x,y) + psi(x) - psi(y)
    tsize = np.array([(wt == t).sum() for t in range(n + 1)], dtype=float)
    onehot = (wt[:, None] == tt[None, :]).astype(float)   # (N, n+1)
    print(f"\nn = {n}: J_t = {np.round(J, 4)}, V_n = {np.round(V, 4)}, Z_H = {ZH:.4f}, contact types {[int(t) for t in tt if abs(J[t]-V[t])<1e-12]}")

    def evaluate(inD):
        """inD: (nsub, N) bool.  Returns Phi+, Phi, mu(D), maxdens"""
        sl = np.full(inD.shape, np.inf)
        for y in range(N):
            cand = np.where(inD[:, y][:, None], np.inf, M[:, y][None, :])
            np.minimum(sl, cand, out=sl)
        sl = np.where(inD, sl, 0.0)
        PhiP = (inD * mu[None, :] * np.exp(sl)).sum(axis=1)
        Phi = (inD * mu[None, :] * np.expm1(sl)).sum(axis=1)
        muD = (inD * mu[None, :]).sum(axis=1)
        md = ((inD.astype(float) @ onehot) / tsize[None, :]).max(axis=1)
        return PhiP, Phi, muD, md

    if n <= 4:
        masks = np.arange(1, 2 ** N - 1, dtype=np.int64)
        res = []
        chunk = 1 << 14
        for a in range(0, len(masks), chunk):
            mm = masks[a:a + chunk]
            inD = ((mm[:, None] >> np.arange(N)[None, :]) & 1).astype(bool)
            res.append(evaluate(inD))
        PhiP, Phi, muD, md = [np.concatenate(z) for z in zip(*res)]
        eD = np.log(PhiP) / n
        thD = -np.log(md) / n
        om = omega_of(eD, thD)
        i = int(np.argmax(om))
        print(f"  all {len(masks)} subsets: max omega = {om.max():.5f} (= {om.max()/(math.log(n)/n):.3f} ln n/n) at e_D = {eD[i]:.4f}, theta_D = {thD[i]:.4f},"
              f" |D| = {bin(int(masks[i])).count('1')};  subsets with omega > 0: {(om > 1e-12).sum()}")
        thmu = -np.log(muD) / n
        om2 = omega_of(eD, thmu)
        print(f"  the same with -ln mu_H(D)/n in place of -ln maxdens(D)/n: max omega = {om2.max():.5f}")
        # exact tail function against unions of profile classes around one centre
        fam = set()
        for s in range(N):
            ii = ((X[s] == 1)[None, :] & (X == 0)).sum(axis=1)
            jj = ((X[s] == 0)[None, :] & (X == 1)).sum(axis=1)
            cls = ii * (n + 1) + jj
            ids = np.unique(cls)
            for r in range(1, 2 ** len(ids) - 1):
                sel = [ids[b] for b in range(len(ids)) if (r >> b) & 1]
                m = 0
                for x in np.nonzero(np.isin(cls, sel))[0]:
                    m |= (1 << int(x))
                fam.add(m)
        fam = np.array(sorted(fam), dtype=np.int64)
        infam = np.zeros(2 ** N, dtype=bool)
        infam[fam] = True
        infam = infam[1:-1]
        qs = np.unique(np.round(md, 12))
        worst = (0.0, None)
        for q in qs[:-1]:
            sel = md <= q + 1e-12
            ex = Phi[sel].max()
            selF = sel & infam
            fa = Phi[selF].max() if selF.any() else 0.0
            if fa > 0 and ex / fa > worst[0]:
                worst = (ex / fa, q)
        print(f"  exact tail function Xi_md(q) against unions of profile classes around one centre ({len(fam)} sets): largest ratio {worst[0]:.4f} at q = {worst[1]:.4f}   [{time.time()-t0:.0f}s]", flush=True)
    else:
        rng = np.random.default_rng(2024 + n)
        best = (-1.0, None, None)
        nrest = 12 if n == 5 else 8
        steps = 6000 if n == 5 else 5000
        for rest in range(nrest):
            inD = rng.random(N) < rng.uniform(0.05, 0.6)
            if inD.all() or not inD.any():
                continue
            def score(v):
                PhiP, Phi, muD, md = evaluate(v[None, :])
                return float(omega_of(np.log(PhiP) / n, -np.log(md) / n)[0]), float(np.log(PhiP[0]) / n), float(-np.log(md[0]) / n)
            cur = score(inD)
            temp = 0.02
            for it in range(steps):
                x = rng.integers(N)
                inD[x] = ~inD[x]
                if inD.all() or not inD.any():
                    inD[x] = ~inD[x]
                    continue
                new = score(inD)
                if new[0] >= cur[0] or rng.random() < math.exp((new[0] - cur[0]) / temp):
                    cur = new
                    if cur[0] > best[0]:
                        best = (cur[0], cur[1], cur[2], int(inD.sum()))
                else:
                    inD[x] = ~inD[x]
                temp = max(temp * 0.999, 1e-4)
        print(f"  annealing ({nrest} restarts x {steps} steps): max omega found = {best[0]:.5f} (= {best[0]/(math.log(n)/n):.3f} ln n/n) at e_D = {best[1]:.4f}, theta_D = {best[2]:.4f}, |D| = {best[3]}   [{time.time()-t0:.0f}s]", flush=True)
print(f"time {time.time()-t0:.0f}s")
