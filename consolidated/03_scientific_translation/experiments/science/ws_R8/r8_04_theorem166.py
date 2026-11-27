#!/usr/bin/env python3
"""R8 / script 04 -- Theorem A16.6 (the cost at the visible basin with the datum): bookkeeping.

Own code.  Uses r8_02_twin.find_case for exact plateau twins and exact radial sums for the
plateau on a ball,  g_pl(d) = -min(c, u (R+1-d)_+),  Zpl(R,U0) its partition function at the
level c* with mean energy U0.

 1  the table of exponents of A16 (b) and the three values of eps1^c
 2  (i)/(iii): for exact twins, G(r2-2), G(r2-1), G(r2) against the gap of the twin; the radius
    the lemma actually allows for the twin (|D|+|V| <= |B(n,R)|  =>  R = r2); sign of gap - G(r2-1)
 3  (ii)/(iii): for a given accuracy eps: R(eps) = largest R with width of the bracket <= eps;
    r2(eps) = smallest twin radius with gap > eps; ratio of the two sample sizes; probability
    that the M samples meet the visible basin; expected cost with a fallback
 4  (iv): bracket width as a function of the datum for instances constant outside a small set;
    exact (finite n) against the exponential-scale formula; position of the maximum
 5  (ii) correctness: the bracket contains ln Z + v on random members that are constant outside
    at most |B(n,R)| points (n = 10, 12; general members with dips and hills; random gauge)
 6  a bounded-accuracy remark: "gap = G(r2-1)" is an extensive-accuracy statement

Run:  python3 r8_04_theorem166.py        (about 2 minutes)
"""
import math, sys, time, io, contextlib
import numpy as np
from scipy.special import logsumexp
from r8_lib import *
import r8_02_twin as TW


def plateau_ball(n, u, R, U0, lc=None):
    """ln Zpl(R,U0), level c*.  Radial exact sums."""
    if lc is None:
        lc = lnC(n)
    d = np.arange(n + 1)
    wall = u * np.maximum(R + 1 - d, 0.0)
    def stats(c):
        g = -np.minimum(c, wall)
        lw = lc - g
        lnZ = float(logsumexp(lw))
        p = np.exp(lw - lnZ)
        return lnZ, float((p * g).sum())
    cmax = u * (R + 1)
    lnZc, Uc = stats(cmax)
    if Uc >= U0:
        return lnZc, cmax
    lo, hi = 0.0, cmax
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if stats(mid)[1] > U0:
            lo = mid
        else:
            hi = mid
    c = 0.5 * (lo + hi)
    return stats(c)[0], c


def part1():
    print("== 1: exponents of the table in A16 (b) ==")
    print("   u    eps1      equal twins  plateau twin  theta_hint   | addendum: equal, plateau, hint")
    quoted = {(1, 0.1): (0.0180, 0.0238, 0.0240), (1, 0.5): (None, 0.0059, 0.0084), (2, 0.25): (0.0153, 0.0600, 0.0632),
              (2, 0.5): (None, 0.0263, 0.0369), (4, 0.25): (0.0885, 0.1715, 0.1840), (4, 0.5): (None, 0.0969, 0.1374),
              (4, 0.75): (None, 0.0275, 0.0985)}
    ok = True
    for (u, f), q in quoted.items():
        e1 = f * a_of(u)
        hh = LN2 - hb(rho0(u))
        eq = hh - e1
        pl = theta_pl(u, e1)
        th = theta_hint(u, e1)
        print(f"   {u}  {f:.2f}a={e1:.4f}   {eq if eq>0 else float('nan'):8.4f}     {pl:.4f}       {th:.4f}      | {q}")
        ok &= abs(pl - q[1]) < 6e-5 and abs(th - q[2]) < 6e-5 and (q[0] is None or abs(eq - q[0]) < 6e-5)
    for u, qc, qa in ((1, 0.086, 0.111), (2, 0.273, 0.328), (4, 0.557, 0.603)):
        print(f"   u={u}: eps1^c = {eps1c(u):.4f} (addendum {qc}),  a(u) = {a_of(u):.4f} (addendum {qa})")
        ok &= abs(eps1c(u) - qc) < 6e-4 and abs(a_of(u) - qa) < 6e-4
    print("   all quoted values reproduced:", ok)
    return ok


def twin_case(n, u, rho1, eps1, Dfrac):
    with contextlib.redirect_stdout(io.StringIO()):
        r = TW.find_case(n, u, rho1, eps1, Dfrac)
    return r


CASES = [(800, 1.0, rho0(1.0) + 0.02, 0.03, 0.5), (1500, 1.0, rho0(1.0) + 0.01, 0.05, 0.5),
         (1000, 2.0, rho0(2.0) + 0.01, 0.10, 0.5), (1000, 2.0, rho0(2.0) + 0.01, 0.20, 0.47),
         (700, 4.0, rho0(4.0) + 0.01, 0.30, 0.5), (700, 4.0, rho0(4.0) + 0.01, 0.45, 0.53),
         (900, 3.0, rho0(3.0) + 0.015, 0.25, 0.5), (2400, 1.0, rho0(1.0) + 0.005, 0.02, 0.5),
         (400, 1.0, rho0(1.0) + 0.03, 0.02, 0.5), (1200, 0.5, rho0(0.5) + 0.01, 0.006, 0.5)]


def part2():
    print("== 2: twins against G(R) = ln Zpl(R,U0) - ln Z0 ==")
    print("    n    u   r1   r2   gap(twin)   G(r2-2)    G(r2-1)    G(r2)     gap-G(r2-1)   R with |D|+|V|<=|B(n,R)|   gap<=G(R)")
    rows = []
    ok = True
    for c in CASES:
        r = twin_case(*c)
        n, u, r1, r2 = r["n"], r["u"], r["r1"], r["r2"]
        lc = lnC(n); lbt = np.logaddexp.accumulate(lc)
        G = {R: plateau_ball(n, u, R, r["U0"], lc)[0] - r["lnZ0"] for R in (r2 - 2, r2 - 1, r2)}
        lnDV = np.logaddexp(lbt[r2 - 1], lbt[r1 - 1])
        Rl = int(np.searchsorted(lbt, lnDV - 1e-12))
        GR = plateau_ball(n, u, Rl, r["U0"], lc)[0] - r["lnZ0"]
        print(f"  {n:5d} {u:4.1f} {r1:4d} {r2:4d}  {r['gap']:10.4f} {G[r2-2]:10.4f} {G[r2-1]:10.4f} {G[r2]:10.4f}   {r['gap']-G[r2-1]:+.2e}        R = {Rl} (= r2: {Rl==r2})"
              f"            {r['gap'] <= GR + 1e-9}")
        ok &= r["gap"] <= GR + 1e-9
        r["G"] = G
        rows.append(r)
    return ok, rows


def part3(rows, delta=0.05):
    print(f"== 3: lower and upper bound on the cost at g0 (delta = {delta}) ==")
    print("    n    u   eps      R(eps) [alg]  r2(eps) [twin]  radius diff   ln(M_alg/LB)   P(samples meet V)   "
          "ln E[cost]/M if fallback = 2^n     exponent of ratio if fallback = e^{n theta_hint}")
    for r in rows:
        n, u, r1 = r["n"], r["u"], r["r1"]
        lc = lnC(n); lbt = np.logaddexp.accumulate(lc)
        s0corr = r["S0"] - n * hb(sig(u))                   # the o(1) of the lower end of the bracket
        eps = r["prev_gap"] + 1e-6 if r["prev_gap"] is not None else r["gap"] - 1e-6
        # lower bound side: smallest twin radius with gap > eps is r2 (by construction of the case)
        r2 = r["r2"]
        # algorithm side: largest R with G(R) + s0corr <= eps
        R = r2
        while plateau_ball(n, u, R, r["U0"], lc)[0] - r["lnZ0"] + s0corr > eps:
            R -= 1
        lnM = n * LN2 + math.log(math.log(1 / delta)) - lbt[R]
        lnLB = math.log(1 - 2 * delta) + math.log(1 - 2 / n**2) + n * LN2 - lbt[r2 - 1]
        lnPhit = math.log(math.log(1 / delta)) + lbt[r1 - 1] - lbt[R]
        # expected cost with exhaustive fallback: M + P_hit 2^n
        lnratio_enum = np.logaddexp(0.0, lnPhit + n * LN2 - lnM)
        e1 = eps / n
        expo = hb(r1 / n) - hb(min(0.5, rho0(u) + e1 / u))
        print(f"  {n:5d} {u:4.1f} {eps:8.3f}   {R:5d}         {r2:5d} (ball r2-1)   {r2-1-R:+d}          {lnM-lnLB:6.2f}        "
              f"{math.exp(lnPhit):.2e}            {lnratio_enum:8.1f}                          {expo:+.4f}")
    return True


def part4():
    print("== 4: (iv) the bracket of (ii) as a function of the datum ==")
    ok = True
    for (n, u, Rfrac) in ((2000, 1.0, 0.44), (2000, 2.0, 0.40), (1500, 4.0, 0.30)):
        lc = lnC(n); lbt = np.logaddexp.accumulate(lc)
        R = int(Rfrac * n)
        s = sig(u)
        best = (-1, None)
        print(f"  n={n} u={u} R={R}: e = |U|/(un);  width/n exact, formula min(h(R/n-e)-h(sig), ue+h(R/n-e)-ln2)_+")
        es = np.linspace(0.0, R / n - s - 0.01, 60)
        ws = []
        for e in es:
            U = -u * e * n
            lo = max(float(np.log(-np.expm1(lbt[R] - n * LN2))) + n * LN2, n * hb(s) - U)
            up = plateau_ball(n, u, R, U, lc)[0]
            ws.append((up - lo) / n)
        ws = np.array(ws)
        form = np.maximum(np.minimum([hb(R / n - e) - hb(s) for e in es], [u * e + hb(R / n - e) - LN2 for e in es]), 0)
        k = int(np.argmax(ws))
        print(f"     max |exact - formula| over the datum: {np.max(np.abs(ws-form)):.4f} (o(1) expected: O(ln n / n) = {math.log(n)/n:.4f})")
        print(f"     maximum of the exact width at e = {es[k]:.4f};  rho0 - sigma_u = {rho0(u)-s:.4f} (= a/u = {a_of(u)/u:.4f})")
        ok &= abs(es[k] - (rho0(u) - s)) < 0.02
    return ok


def part5():
    print("== 5: the bracket of (ii) on random members constant outside few points (general members, random gauge) ==")
    rng = np.random.default_rng(5)
    tot = 0; bad = 0; minslack_lo = np.inf; minslack_up = np.inf
    for n in (10, 12):
        N = 1 << n
        x = np.arange(N)
        pc = np.zeros(N, dtype=np.int64)
        for b in range(n):
            pc += (x >> b) & 1
        lc = lnC(n); lbt = np.logaddexp.accumulate(lc)
        for rep in range(150):
            u = float(rng.choice([0.5, 1.0, 2.0, 3.5]))
            Rr = int(rng.integers(1, n // 2))
            Nmax = int(round(math.exp(lbt[Rr])))
            Ns = int(rng.integers(1, Nmax + 1))
            c = int(rng.integers(0, N)); c2 = int(rng.integers(0, N))
            sc = pc[x ^ c] + rng.choice([0.0, 0.6]) * pc[x ^ c2] + 0.3 * rng.random(N)
            D = np.zeros(N, dtype=bool); D[np.argsort(sc)[:Ns]] = True
            # distance to the complement by relaxation
            rho = np.where(D, n + 1, 0).astype(float)
            for _ in range(n):
                for i in range(n):
                    rho = np.minimum(rho, rho[x ^ (1 << i)] + 1)
            psi = rng.normal(0, rng.choice([0.5, 3.0, 10.0]) * u, N) - rng.uniform(0, 4) * u
            for i in range(n):
                psi = np.minimum(psi, psi[x ^ (1 << i)] + u)
            if rng.random() < 0.25:
                psi = -psi
            g = np.maximum(-u * rho, np.minimum(psi, u * rho))
            v = rng.normal(0, 5)
            gg = g + v
            m = gg.min(); w = np.exp(-(gg - m)); Z = w.sum(); lnZ = math.log(Z) - m; U = float((w * gg).sum() / Z)
            Ut = U - v
            lo = max(float(np.log(-np.expm1(lbt[Rr] - n * LN2))) + n * LN2, n * hb(sig(u)) - Ut)
            up = plateau_ball(n, u, Rr, min(Ut, 0.0), lc)[0]
            val = lnZ + v
            tot += 1
            bad += int(not (lo - 1e-9 <= val <= up + 1e-9))
            minslack_lo = min(minslack_lo, val - lo); minslack_up = min(minslack_up, up - val)
    print(f"  members {tot}: bracket fails to contain ln Z + v in {bad} cases; least slack below {minslack_lo:.2e}, above {minslack_up:.2e}")
    return bad == 0


def part6():
    print("== 6: at bounded accuracy 'gap = G(r2-1)' fails (it is an extensive-accuracy statement) ==")
    n, u = 800, 1.0
    r1 = math.ceil((rho0(u) + 0.02) * n)
    lc = lnC(n)
    for k in (1, 2, 3, 5, 8, 12, 20):
        tw = TW.Twin(n, u, r1, r1 + k, n // 2)
        kap, _, _ = tw.root()
        gp = tw.gap(kap)
        G1 = plateau_ball(n, u, r1 + k - 1, tw.U0, lc)[0] - tw.lnZ0
        G0 = plateau_ball(n, u, r1 + k, tw.U0, lc)[0] - tw.lnZ0
        print(f"  r2 = r1+{k:2d}: gap of the twin {gp:8.4f}   G(r2-1) {G1:8.4f}   G(r2) {G0:8.4f}   gap - G(r2-1) = {gp-G1:+.4f}")
    return True


if __name__ == "__main__":
    t0 = time.time()
    ok1 = part1()
    ok2, rows = part2()
    part3(rows)
    ok4 = part4()
    ok5 = part5()
    part6()
    print("SUMMARY table:", ok1, " twins <= G(R) of the lemma:", ok2, " (iv):", ok4, " bracket valid:", ok5, f" time {time.time()-t0:.0f}s")
