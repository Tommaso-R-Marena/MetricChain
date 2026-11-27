#!/usr/bin/env python3
"""r26_hub.py -- workstream R26, Item 2 (iv) and Item 1 (iii): a NEAREST-NEIGHBOUR CHAIN (a band model, r = 1) on
which Algorithm A, run with the tail function of the product class (slope u per outer site), returns a false
certificate -- with the influence confined to ONE outer site (the boundary site, a "hub" in the sense of the
remark at the end of N_REPORT 5.2) -- and the two repairs: the envelope of Theorem N4 (u + iota at the boundary
site) and conditioning on the boundary site.

The chain (binary sites; c outer sites, k inner sites), as a Markov chain = a nearest-neighbour Gibbs measure:
    a_1 .. a_{c-1}  independent uniform;   P(a_c = 1) = pi_h        (a field on the boundary site: a rare state)
    P(b_1 = a_c) = p_x                     (a strong coupling across the cut: ln((1-p_x)/p_x) kT)
    P(b_{j+1} != b_j) = p_in               (a rigid inner chain: coupling ln((1-p_in)/p_in) kT)
Residual: psi(a,b) = u (a_1 + .. + a_{c-1}) + u |b|   (additive, u-Lipschitz in every site; a member of L_u).
So V(a) = e^{-u(a_1+..+a_{c-1})} * E[ e^{-u|b|} | a_c ]: the common boundary state a_c = 0 drives the inner chain
to b = 1..1 (weight e^{-uk}), the rare state a_c = 1 drives it to b = 0..0 (weight 1).

Usage: python3 -B r26_hub.py [runs]
"""
import math
import sys
import time

import numpy as np

import r26_alg as A
import r26_band as B


def chain_moment(k, p_x, p_in, w0, w1):
    """E[ prod_j w(b_j) | a_c = h ] for h = 0, 1, w(0) = w0, w(1) = w1 (transfer recursion along the inner chain)."""
    f = np.array([w0, w1])
    for _ in range(k - 1):
        f = np.array([w0 * ((1 - p_in) * f[0] + p_in * f[1]), w1 * (p_in * f[0] + (1 - p_in) * f[1])])
    return np.array([p_x * f[0] + (1 - p_x) * f[1],          # a_c = 0: b_1 = 1 with probability 1 - p_x
                     (1 - p_x) * f[0] + p_x * f[1]])          # a_c = 1: b_1 = 0 with probability 1 - p_x


def build(c, k, u, pi_h, p_x, p_in):
    Vh = chain_moment(k, p_x, p_in, 1.0, math.exp(-u))                 # E[e^{-u|b|} | a_c]
    pts = np.arange(1 << c)
    bits = (pts[:, None] >> np.arange(c)[None, :]) & 1          # bit c-1 is the boundary site a_c
    ac = bits[:, c - 1]
    rest = bits[:, : c - 1].sum(axis=1)
    mu = np.where(ac == 1, pi_h, 1 - pi_h) / (1 << (c - 1))
    V = np.exp(-u * rest) * Vh[ac]
    ham = np.array([[bin(int(x) ^ int(z)).count("1") for z in pts] for x in pts], dtype=float)
    # Reference data of the class L_u under the TRUE measure, reference point x0 = (a = 0..0 ; b = 1..1), the
    # typical configuration of the known part: psi(x0) = u k, d(x, x0) = |a| + (k - |b|).
    #   ell0 = e^{-psi(x0)} E e^{-d(x,x0)};   Vmax = max_a e^{-psi(a,b0)} E[e^{+u d(b,b0)} | a]   (N_REPORT 2.6)
    Fm = chain_moment(k, p_x, p_in, math.exp(-u), 1.0)                  # E[e^{-u(k-|b|)} | a_c]
    Fp = chain_moment(k, p_x, p_in, math.exp(u), 1.0)                   # E[e^{+u(k-|b|)} | a_c]
    ell0 = float(math.exp(-u * k) * (mu * np.exp(-u * (rest + ac)) * Fm[ac]).sum())
    Vmax = float((np.exp(-u * rest - u * k) * Fp[ac]).max())
    assert ell0 <= float((mu * V).sum()) * (1 + 1e-12) and Vmax >= V.max() * (1 - 1e-12)
    return dict(c=c, k=k, u=u, mu=mu, V=V, Vh=Vh, ac=ac, rest=rest, ham=ham, ell0=ell0, Vmax=Vmax, pts=pts)


def brute_check(c, k, u, pi_h, p_x, p_in):
    """V_h by enumeration of the 2^k inner configurations, and the class-relative influence by the LP."""
    conf = B.configs(2, k)
    flips = (conf[:, 1:] != conf[:, :-1]).sum(axis=1)
    base = p_in ** flips * (1 - p_in) ** (k - 1 - flips)
    mu0 = np.where(conf[:, 0] == 0, p_x, 1 - p_x) * base        # a_c = 0
    mu1 = np.where(conf[:, 0] == 1, p_x, 1 - p_x) * base        # a_c = 1
    w = np.exp(-u * conf.sum(axis=1))
    return (mu0 * w).sum(), (mu1 * w).sum(), mu0, mu1


def run_cell(P, inst, tails, runs, seed0, pi_star):
    mu, V = inst["mu"], inst["V"]
    n = len(V)
    cdf = np.cumsum(mu)
    res = []
    for r in range(runs):
        rng = np.random.default_rng(seed0 + r)
        rec = A.run_A(P, V, lambda m_: np.minimum(np.searchsorted(cdf, rng.random(m_)), n - 1), tails.Xi,
                      tails.Theta, inst["ell0"], pi_star, rng, Vmax=inst["Vmax"])
        chk = A.check_run(rec, P, mu, V)
        chk["close"] = rec["close"]
        res.append(chk)
    return res


def report(res, label, Atot):
    n = len(res)
    inval = sum(not r["valid"] for r in res)
    f = lambda key: sum(not r[key] for r in res)
    below = [Atot / r["U"] for r in res if r["U"] < Atot]
    above = [r["L"] / Atot for r in res if r["L"] > Atot]
    reasons = {}
    for r in res:
        if r["stop"] == "abort":
            reasons[r["abort"]] = reasons.get(r["abort"], 0) + 1
    line = (f"  {label}: runs {n}; INVALID {inval}; median outer points {int(np.median([r['points'] for r in res]))}; "
            f"false: q {f('cert_q')}, plow {f('cert_p')}, ell {f('cert_ell')}, tail {f('cert_tail')}; Chernoff "
            f"failed {f('chernoff')}")
    if below:
        line += f"; A/U (U < A): median {np.median(below):.1f}"
    if above:
        line += f"; L/A (L > A): median {np.median(above):.2f}"
    if reasons:
        line += f"; aborts {reasons}"
    print(line)
    return inval


def influence_recursion(k, u, p_x, p_in):
    """Class-relative influence of the boundary site by the pairwise recursion of r26_band (exact for binary
    chains: self-test 4 of r26_band.py), on the chain a_c - b_1 - .. - b_k."""
    n = 1 + k
    pair = {(0, 1): -np.log(np.array([[p_x, 1 - p_x], [1 - p_x, p_x]]))}
    for j in range(1, n - 1):
        pair[(j, j + 1)] = -np.log(np.array([[1 - p_in, p_in], [p_in, 1 - p_in]]))
    model = dict(n=n, q=2, r=1, pair=pair, h=np.zeros((n, 2)))
    rec, _ = B.recursion_bound_nn(model, 1, u)
    return float(rec[1, 0]), float(rec[0, 1])


def one_chain(runs, c, k, u, cx, cin, pi_list, thetas, cellno, do_lp):
    p_x, p_in = 1 / (1 + math.exp(cx)), 1 / (1 + math.exp(cin))
    viol = 0
    print(f"\n=== chain: c = {c} outer sites, k = {k} inner sites, u = {u}; cross-cut coupling ln((1-p_x)/p_x) = "
          f"{cx:.2f} kT, inner coupling ln((1-p_in)/p_in) = {cin:.2f} kT")
    inst = build(c, k, u, 0.002, p_x, p_in)
    i10, i01 = influence_recursion(k, u, p_x, p_in)
    if do_lp:
        V0b, V1b, mu0, mu1 = brute_check(c, k, u, 0.002, p_x, p_in)
        d = max(abs(V0b - inst["Vh"][0]) / V0b, abs(V1b - inst["Vh"][1]) / V1b)
        print(f"V_h by the transfer recursion against enumeration of the 2^{k} inner configurations: rel. diff {d:.1e}")
        viol += d > 1e-10
        Aub = B.lipschitz_constraints(2, k, u)
        l10 = math.log(B.lp_ratio(mu1, mu0, Aub))
        l01 = math.log(B.lp_ratio(mu0, mu1, Aub))
        print(f"class-relative influence of the boundary site: LP on 2^{k} points {l10:.4f} / {l01:.4f}; own recursion "
              f"{i10:.4f} / {i01:.4f}")
        viol += abs(l10 - i10) > 1e-5 or abs(l01 - i01) > 1e-5
    print(f"influence of the boundary site on the inner block: pointwise {cx:.3f} (= the cross-cut coupling);  "
          f"class-relative (u-Lipschitz fibre weights): iota(1->0) = {i10:.4f}, iota(0->1) = {i01:.4f};  "
          f"ln(V_1/V_0) = {math.log(inst['Vh'][1] / inst['Vh'][0]):.4f}  (u*k = {u * k})")
    viol += not (math.log(inst["Vh"][1] / inst["Vh"][0]) <= i10 + 1e-6)
    for pi_h in pi_list:
        inst = build(c, k, u, pi_h, p_x, p_in)
        mu, V, ham, ac = inst["mu"], inst["V"], inst["ham"], inst["ac"]
        Atot = float((mu * V).sum())
        share = float((mu * V)[ac == 1].sum()) / Atot
        print(f"\npi_h = P(a_c = 1) = {pi_h}:  A = {Atot:.4e}; share of the boundary state a_c = 1: {100 * share:.2f} %"
              f" (ratio to the rest {share / (1 - share):.1f}); V_0 = {inst['Vh'][0]:.3e}, V_1 = {inst['Vh'][1]:.3e}; "
              f"ell0 = {inst['ell0']:.3e}, Vmax = {inst['Vmax']:.3e}")
        T_ass = A.EnumeratedEnvelope(mu, u * ham)
        iota = np.where((ac[:, None] == 1) & (ac[None, :] == 0), i10, 0.0) + \
               np.where((ac[:, None] == 0) & (ac[None, :] == 1), i01, 0.0)
        T_n4 = A.EnumeratedEnvelope(mu, u * ham + iota)
        S = A.SharpestTails(mu, V)
        tu_ass = max(S.excess[i] / (v * T_ass.Xi(S.above[i])) for i, v in enumerate(S.vals[:-1])
                     if 0 < S.above[i] < 1)
        tu_n4 = max(S.excess[i] / (v * T_n4.Xi(S.above[i])) for i, v in enumerate(S.vals[:-1])
                    if 0 < S.above[i] < 1)
        tl_ass = max(v * max(S.atleast[i], T_ass.Theta(S.atleast[i])) / S.trunc[i] for i, v in enumerate(S.vals))
        tl_n4 = max(v * max(S.atleast[i], T_n4.Theta(S.atleast[i])) / S.trunc[i] for i, v in enumerate(S.vals))
        print(f"  (TU) worst ratio: product-class envelope {tu_ass:.3e}; N4 envelope {tu_n4:.4f} (must be <= 1).   "
              f"(TL) worst ratio: product-class {tl_ass:.3f}; N4 {tl_n4:.4f} (must be <= 1)")
        viol += (tu_n4 > 1 + 1e-9) or (tl_n4 > 1 + 1e-9)
        pi_star = float(mu.min())
        for theta in thetas:
            P = A.Params(lam=1.0, eta=0.5, etap=1.0, theta=theta, nu1=1.0, b=0.5, delta=0.05, kappa0=1.0,
                         x=(2 * u * k, 2.0, 0.5), C=(1.0, 1.0, 1.0))
            print(f" theta = {theta}, e^x_out = {math.exp(P.x_out()):.1f}  (seeds default_rng(10000*cell + r), "
                  f"r = 0..{runs - 1}; first cell of this line group: {cellno})")
            ra = run_cell(P, inst, T_ass, runs, 10000 * cellno, pi_star); cellno += 1
            report(ra, "(A) product-class tail function (slope u at every outer site)   ", Atot)
            rb = run_cell(P, inst, T_n4, runs, 10000 * cellno, pi_star); cellno += 1
            viol += report(rb, "(B) envelope of Theorem N4 (u + iota at the boundary site)      ", Atot)
            H = A.HarperCube(c - 1, u)
            pop3 = np.array([bin(int(x)).count("1") for x in range(1 << (c - 1))])
            nbad, pts_tot = 0, []
            for r in range(runs):
                Ltot = Utot = 0.0
                npts = 0
                for h in (0, 1):
                    Vsub = np.exp(-u * pop3) * inst["Vh"][h]
                    ell0 = float(Vsub[0] * ((1 + math.exp(-u)) / 2) ** (c - 1))
                    Vmax = float(Vsub[0] * math.exp(u * (c - 1)))
                    Ph = A.Params(lam=1.0, eta=0.5, etap=1.0, theta=theta, nu1=1.0, b=0.5, delta=0.025, kappa0=1.0,
                                  x=(2 * u * k, 2.0, 0.5), C=(1.0, 1.0, 1.0))
                    rng = np.random.default_rng(10000 * cellno + 2 * r + h)
                    rec = A.run_A(Ph, Vsub, lambda m_: rng.integers(0, 1 << (c - 1), m_), H.Xi, H.Theta, ell0,
                                  1.0 / (1 << (c - 1)), rng, Vmax=Vmax)
                    wgt = pi_h if h == 1 else 1 - pi_h
                    Ltot += wgt * rec["L"]
                    Utot += wgt * rec["U"]
                    npts += rec["points"]
                pts_tot.append(npts)
                if not (Ltot <= Atot * (1 + 1e-9) and Atot <= Utot * (1 + 1e-9)):
                    nbad += 1
            cellno += 1
            print(f"  (C) conditioning on the boundary site (2 product sub-problems)       : runs {runs}; INVALID "
                  f"{nbad}; median outer points {int(np.median(pts_tot))}")
            viol += nbad
    print("\ncontrol: the same chain with NO coupling across the cut (p_x = 1/2), algorithm (A):")
    nctl = 0
    for pi_h in pi_list:
        inst = build(c, k, u, pi_h, 0.5, p_in)
        mu, V, ham = inst["mu"], inst["V"], inst["ham"]
        Atot = float((mu * V).sum())
        T_ass = A.EnumeratedEnvelope(mu, u * ham)
        for theta in thetas:
            P = A.Params(lam=1.0, eta=0.5, etap=1.0, theta=theta, nu1=1.0, b=0.5, delta=0.05, kappa0=1.0,
                         x=(2 * u * k, 2.0, 0.5), C=(1.0, 1.0, 1.0))
            rc = run_cell(P, inst, T_ass, runs, 10000 * cellno, float(mu.min())); cellno += 1
            bad = report(rc, f"pi_h={pi_h} theta={theta}", Atot)
            other = sum((not r["cert_q"]) or (not r["cert_p"]) or (not r["cert_ell"]) or (not r["cert_tail"])
                        or (not r["width"]) for r in rc)
            nctl += bad + other
    print(f"control violations: {nctl}")
    return viol + nctl, cellno


def main(runs):
    v1, cell = one_chain(runs, c=4, k=12, u=1.0, cx=10.0, cin=7.6, pi_list=(0.002, 0.2), thetas=(20.0, 5.0, 1.0),
                         cellno=0, do_lp=True)
    v2, cell = one_chain(runs, c=4, k=16, u=1.0, cx=14.0, cin=11.0, pi_list=(0.002, 0.02, 0.2),
                         thetas=(20.0, 5.0, 1.0), cellno=cell, do_lp=False)
    print(f"\nviolations of the statements that must hold ((B), (C), controls, exact checks): {v1 + v2}")
    return v1 + v2


if __name__ == "__main__":
    t0 = time.time()
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    print(f"r26_hub.py runs {runs}; started {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    v = main(runs)
    print(f"finished {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}; elapsed {time.time() - t0:.1f} s; "
          f"peak memory {A.peak_mb():.0f} MB")
    sys.exit(1 if v else 0)
