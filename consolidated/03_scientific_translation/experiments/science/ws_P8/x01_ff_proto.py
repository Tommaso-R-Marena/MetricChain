"""
P8 exploration (NOT rigorous: suprema by sampling) -- where is the slack of the cross bound for pairs of FIXED atoms?

For a pair of fixed atoms (no host), T = B, P3's bound is
    kappa |q_p q_q| sum_{a+b=s} e_{a,b}(delta^p, delta^q) * COEF_{a,b},
    COEF^{P3}_{a,b} = sum_{r1,r2} sup|h^(r1+r2)| Bell_{a,r1}(sup|ell_p^(.)|) Bell_{b,r2}(sup|ell_q^(.)|).
The exact coefficient of the leading term is the mixed partial derivative of Phi(I_p, I_q) = h(ell_p(I_p) + ell_q(I_q); r):
    d_p^a d_q^b Phi = sum_{r1,r2} h^(r1+r2) Bell_{a,r1}(ell_p', ell_p'', ..) Bell_{b,r2}(ell_q', ..)     (signed).
Variants compared (all with suprema SAMPLED on a 9 x 9 grid of the hull rectangle -- exploration only):
    P3s    : P3's formula with sampled suprema                               (should be close to P3's rigorous value)
    Lbell  : sum_{r1,r2} sup|h^(r1+r2)| sup|Bell_{a,r1}(ell_p^(.))| sup|Bell_{b,r2}(ell_q^(.))|
    bver   : sum_{r1,r2} sup|d_1^r1 d_2^r2 Psi| Bell_{a,r1}(sup|b_p^(.)|) Bell_{b,r2}(sup|b_q^(.)|),  Psi(u1,u2) = h as a function of the inverse radii
    bbell  : sum_{r1,r2} sup_D|(2/r) xi_{r1,r2}(D)| sup|b_p^-r1 Bell_{a,r1}(b_p^(.))| sup|b_q^-r2 Bell_{b,r2}(b_q^(.))|
    direct : sup over the rectangle of |d_p^a d_q^b Phi|                      (the best a chain-rule bound with one supremum per (a, b) can do)
usage: python3 -B x01_ff_proto.py SEQ BB TAU     (uses out/m1_<tag>.npz for the exact constants and P3's summands)
"""
import sys, os, math, itertools
import numpy as np
from p8lib import *
import dfun

seq, bb, tau = sys.argv[1], sys.argv[2], float(sys.argv[3])
tag = tagname(seq, bb, tau)
Z = np.load(os.path.join(HERE, "out", f"m1_{tag}.npz"))
G = GBModel(seq, bb, tau=tau)
n, N = G.ns, G.nat
x0 = tuple(int(v) for v in Z["anchor"])
Tlist = [tuple(int(v) for v in row if v >= 0) for row in Z["Tlist"]]
KMAX = 6
ETA = [dict(t) for t in dfun.ETA_TERMS]
while len(ETA) <= KMAX:
    ETA.append(dfun._L(ETA[-1]))


def zeta(k, D):
    E = np.exp(-D); u = 4.0 * D + E
    out = np.zeros_like(D)
    for (a, b, c2), v in ETA[k].items():
        out = out + float(v) * D ** a * E ** b * u ** (-0.5 * c2)
    return np.sqrt(D) * out


# float Taylor-series arithmetic (coefficients c_k = f^(k)/k!) -- the recurrences of encl.py with floats
def s_mul(a, b, K):
    return [sum(a[j] * b[k - j] for j in range(k + 1)) for k in range(K + 1)]


def s_inv(a, K):
    b = [1.0 / a[0]]
    for k in range(1, K + 1):
        b.append(-sum(a[j] * b[k - j] for j in range(1, k + 1)) / a[0])
    return b


def s_exp(a, K):
    e = [np.exp(a[0])]
    for k in range(1, K + 1):
        e.append(sum(j * a[j] * e[k - j] for j in range(1, k + 1)) / k)
    return e


def s_log(a, K):
    l = [np.log(a[0])]
    for k in range(1, K + 1):
        acc = a[k] - (sum(j * l[j] * a[k - j] for j in range(1, k)) / k if k > 1 else 0.0)
        l.append(acc / a[0])
    return l


def atom_derivs(p, I, K):
    """derivatives (not Taylor coefficients) of ib and ell at the points I (array), orders 0..K: two lists of arrays."""
    o = G.orr[p]; rad = o + G.off
    z = np.zeros_like(I)
    psi = [o * I, o + z] + [z] * (K - 1)
    psi2 = s_mul(psi, psi, K); psi3 = s_mul(psi2, psi, K)
    P = [G.al[p] * psi[k] - G.be[p] * psi2[k] + G.ga[p] * psi3[k] for k in range(K + 1)]
    e2 = s_exp([2 * c for c in P], K); e2[0] = e2[0] + 1.0
    inv = s_inv(e2, K)
    ib = [2 * c / rad for c in inv]; ib[0] = ib[0] + 1.0 / o - 1.0 / rad
    ell = [-c for c in s_log(ib, K)]
    f = [math.factorial(k) for k in range(K + 1)]
    return [ib[k] * f[k] for k in range(K + 1)], [ell[k] * f[k] for k in range(K + 1)]


def bell(L, s):
    """partial Bell polynomials B[a][r] of the (signed) arrays L[1..s]."""
    one = np.ones_like(L[1])
    B = [[None] * (s + 1) for _ in range(s + 1)]
    B[0][0] = one
    for a in range(1, s + 1):
        B[a][0] = np.zeros_like(one)
        for r in range(1, a + 1):
            acc = np.zeros_like(one)
            for j in range(1, a - r + 2):
                if B[a - j][r - 1] is None:
                    continue
                acc = acc + math.comb(a - 1, j - 1) * L[j] * B[a - j][r - 1]
            B[a][r] = acc
    return B


def falling_poly(a):
    """coefficients c[k] of x(x-1)...(x-a+1)."""
    c = np.array([1.0])
    for j in range(a):
        c = np.convolve(c, np.array([-float(j), 1.0]))
    return c


# check of the float series against dfun's closed forms (orders <= 4)
p_ = int(G.fixed[3]); It = np.array([2.0, 5.0, 9.0])
ib_, ell_ = atom_derivs(p_, It, 4)
ref_b = dfun.ib_derivs(It, G.orr[p_], G.rad[p_], G.al[p_], G.be[p_], G.ga[p_]); ref_l = dfun.ell_derivs(It, G.orr[p_], G.rad[p_], G.al[p_], G.be[p_], G.ga[p_])
dev = max(np.abs(np.array(ib_) - np.array(ref_b)).max(), np.abs(np.array(ell_) - np.array(ref_l)).max())
print(f"float series against dfun closed forms: max deviation {dev:.2e}")

F = G.fixed
nf = len(F)
A = [G.A[i] for i in range(n)]                        # (k_i, nf)
cmin = np.array([c.min(axis=0) for c in A]); cmax = np.array([c.max(axis=0) for c in A])
Ilo = G.I0 + cmin.sum(0); Ihi = G.I0 + cmax.sum(0)
dlt = np.array([np.abs(A[i] - A[i][x0[i]][None]).max(axis=0) for i in range(n)])       # anchored deltas (n, nf)
Xf = G.Xf
print(f"{seq}/{bb}: {nf} fixed atoms; hull width of I: median {np.median(Ihi - Ilo):.2f}, max {(Ihi - Ilo).max():.2f} nm^-1; "
      f"B range over the hull: median ratio Bmax/Bmin {np.median([atom_derivs(int(F[j]), np.array([Ilo[j]]), 1)[0][0][0] / atom_derivs(int(F[j]), np.array([Ihi[j]]), 1)[0][0][0] for j in range(nf)]):.2f}")
NG = 9
tgrid = np.linspace(0.0, 1.0, NG)
PPm = Z["PP"]; PBp = Z["PBp"]
for T in Tlist:
    s = len(T)
    if s > KMAX:
        continue
    ti = Tlist.index(T)
    tot = dict(exact=0.0, P3=0.0, P3s=0.0, Lbell=0.0, bver=0.0, bbell=0.0, direct=0.0)
    # per-atom sampled derivative data on the hull
    ad = []
    for j, p in enumerate(F):
        Ig = Ilo[j] + (Ihi[j] - Ilo[j]) * tgrid
        ib, ell = atom_derivs(int(p), Ig, s)
        Bl = bell(ell, s); Bb = bell(ib, s)
        ad.append(dict(ib=ib, ell=ell, Bl=Bl, Bb=Bb,
                       supL=[None] + [np.abs(ell[k]).max() for k in range(1, s + 1)], supB=[None] + [np.abs(ib[k]).max() for k in range(1, s + 1)]))
    for j1 in range(nf):
        for j2 in range(j1 + 1, nf):
            p, q = int(F[j1]), int(F[j2])
            ex = PPm[ti, p, q]
            r = float(np.linalg.norm(Xf[j1] - Xf[j2]))
            d1, d2 = ad[j1], ad[j2]
            # e_{a,b} over the sites of T
            e = [[0.0] * (s + 1) for _ in range(s + 1)]
            e[0][0] = 1.0
            for i in T:
                x, y = dlt[i, j1], dlt[i, j2]
                for t_ in range(s, 0, -1):
                    for a in range(t_, -1, -1):
                        b = t_ - a
                        if a > 0:
                            e[a][b] += x * e[a - 1][b]
                        if b > 0:
                            e[a][b] += y * e[a][b - 1]
            w = d1["ell"][0][:, None] + d2["ell"][0][None, :]          # (NG, NG)
            D = r * r * np.exp(-w) / 4.0
            hk = [None] + [(2.0 / r) * zeta(k, D) for k in range(1, s + 1)]
            supH = [None] + [np.abs(hk[k]).max() for k in range(1, s + 1)]
            # Psi partials: u1^-a u2^-b (2/r) xi_ab(D)
            xi = {}
            for ra in range(s + 1):
                for rb in range(s + 1 - ra):
                    if ra + rb == 0:
                        continue
                    c = np.convolve(falling_poly(ra), falling_poly(rb))
                    v = np.zeros_like(D)
                    for k in range(1, len(c)):
                        v = v + c[k] * (-1.0) ** k * zeta(k, D)
                    xi[(ra, rb)] = (2.0 / r) * v
            u1 = d1["ib"][0][:, None]; u2 = d2["ib"][0][None, :]
            BLs1 = bell([None] + d1["supL"][1:], s) if False else None
            sL1 = bell([np.array(0.0)] + [np.array(v) for v in d1["supL"][1:]], s); sL2 = bell([np.array(0.0)] + [np.array(v) for v in d2["supL"][1:]], s)
            sB1 = bell([np.array(0.0)] + [np.array(v) for v in d1["supB"][1:]], s); sB2 = bell([np.array(0.0)] + [np.array(v) for v in d2["supB"][1:]], s)
            val = dict(P3s=0.0, Lbell=0.0, bver=0.0, bbell=0.0, direct=0.0)
            for a in range(s + 1):
                b = s - a
                if e[a][b] == 0.0:
                    continue
                c_p3 = c_lb = c_bv = c_bb = 0.0
                direct = np.zeros((NG, NG))
                for r1 in range(0, a + 1):
                    if a > 0 and r1 == 0:
                        continue
                    for r2 in range(0, b + 1):
                        if b > 0 and r2 == 0:
                            continue
                        k = r1 + r2
                        c_p3 += supH[k] * float(sL1[a][r1]) * float(sL2[b][r2])
                        c_lb += supH[k] * np.abs(d1["Bl"][a][r1]).max() * np.abs(d2["Bl"][b][r2]).max()
                        psi_part = u1 ** (-r1) * u2 ** (-r2) * xi[(r1, r2)]
                        c_bv += np.abs(psi_part).max() * float(sB1[a][r1]) * float(sB2[b][r2])
                        c_bb += np.abs(xi[(r1, r2)]).max() * np.abs(d1["ib"][0] ** (-r1) * d1["Bb"][a][r1]).max() * np.abs(d2["ib"][0] ** (-r2) * d2["Bb"][b][r2]).max()
                        direct = direct + hk[k] * d1["Bl"][a][r1][:, None] * d2["Bl"][b][r2][None, :]
                val["P3s"] += e[a][b] * c_p3; val["Lbell"] += e[a][b] * c_lb; val["bver"] += e[a][b] * c_bv; val["bbell"] += e[a][b] * c_bb
                val["direct"] += e[a][b] * np.abs(direct).max()
            coef = KAPPA * abs(G.q[p] * G.q[q]) / KCAL
            tot["exact"] += ex; tot["P3"] += PBp[ti, p, q]
            for k_ in val:
                tot[k_] += coef * val[k_]
    print(f"T = {T} (order {s}), pairs of fixed atoms, sums in kcal/mol:  exact {tot['exact']:.4e} | P3 rigorous {tot['P3']:.4e} | P3 sampled {tot['P3s']:.4e} | "
          f"Lbell {tot['Lbell']:.4e} | bver {tot['bver']:.4e} | bbell {tot['bbell']:.4e} | direct {tot['direct']:.4e}")
    print(f"      ratios to exact: P3 {tot['P3'] / tot['exact']:.2f}, Lbell {tot['Lbell'] / tot['exact']:.2f}, bver {tot['bver'] / tot['exact']:.2f}, "
          f"bbell {tot['bbell'] / tot['exact']:.2f}, direct {tot['direct'] / tot['exact']:.2f}", flush=True)
