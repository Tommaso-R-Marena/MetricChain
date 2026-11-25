#!/usr/bin/env python3
"""R8 / script 06 -- the guess for non-adaptive algorithms with the datum,
        theta_na^U(eps1) = theta_na(u (sigma2(eps1) - sigma_u)).              Own code.

Part 1  the pair, exactly.  Centre s, d = d_H(x,s).  Outside the open ball {d < R3} both members
        are the cone u d.  Inside:
            A:  g_A = u max(d, R1)                 (the cone truncated at R1 <= R3: a flat bottom)
            B:  g_B = min(u R3, c2 + u d)          (the cone raised by c2 >= 0 under a plateau ring)
        Both are u-Lipschitz, they differ only inside {d < R3}.  For every R1 there is exactly one
        c2 with the same mean energy (U_B is continuous and increasing in c2).  All sums are
        radial and exact.  Reported: the root, the equality of the mean energies, ln Z_A - ln Z_B,
        and for a target accuracy eps the smallest R3 for which some R1 gives a gap > eps --
        against the radius predicted by the guess,  KL(rho3 || sigma_u) = u (sigma2(eps1) - sigma_u),
        and against the radius without the datum, KL(rho || sigma_u) = eps1 (theory report,
        Theorem 11.45 at the commit of this tree).
        A displaced inner cone  c2 + u d(x,s')  is admissible iff c2 >= u d(s,s'); it changes
        nothing in the count (checked by enumeration at n = 14).
Part 2  the datum-assisted bracket of remark (4) of Lemma A16.5 on radial instances, exactly:
            Z <= min_eta [ sum_{d>r} C(n,d) f_eta(w_d) + sum_{d<=r} C(n,d) H_eta(r+1-d) ],
            H_eta(rho) = max{ f_eta(s) : t <= s <= t e^{u rho} },  f_eta(s) = s (1 - eta (U + ln s)),
        t the weight at d = r+1 (the level of the sample), lower end = the larger of what the sample
        shows, sum_{d>r} C w + t |B(n,r)|, and the entropy bracket e^{n h(sigma_u) - U}.
        For each instance: the largest unexplored radius r at which the bracket is narrower than
        eps  (cost ~ 2^n/|B(n,r)|), over families of radial instances; the worst one against the guess.

Run:  python3 r8_06_nonadaptive.py part1    (part 1 and 1b only: about 1 minute)
      python3 r8_06_nonadaptive.py          (everything; part 2 took 28 minutes on the shared 4-core machine --
                                             longer than intended; its output is in r8_06_nonadaptive.log)
"""
import math, sys, time
import numpy as np
from scipy.special import logsumexp
from r8_lib import *


def klb(a, b):
    return a * math.log(a / b) + (1 - a) * math.log((1 - a) / (1 - b))


def theta_na(u, x):
    """min{ KL(rho||1/2) : KL(rho||sigma_u) <= x }  (theory report 11.44)"""
    s = sig(u)
    if x >= klb(0.5, s):
        return 0.0
    lo, hi = s, 0.5
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if klb(mid, s) <= x:
            lo = mid
        else:
            hi = mid
    return LN2 - hb(lo)


def rho_of_kl(u, x):
    s = sig(u)
    if x >= klb(0.5, s):
        return 0.5
    lo, hi = s, 0.5
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if klb(mid, s) <= x:
            lo = mid
        else:
            hi = mid
    return lo


# ---------------------------------------------------------------- part 1
def gA(n, u, R1):
    d = np.arange(n + 1)
    return u * np.maximum(d, R1).astype(float)


def gB(n, u, R3, c2):
    d = np.arange(n + 1).astype(float)
    g = u * d
    ins = d < R3
    g[ins] = np.minimum(u * R3, c2 + u * d[ins])
    return g


def pair(n, u, R1, R3):
    """exact pair: returns (c2, U_A, U_B, lnZ_A - lnZ_B) or None"""
    lnZA, UA, SA = radial_stats(n, gA(n, u, R1))
    f = lambda c: radial_stats(n, gB(n, u, R3, c))[1] - UA
    lo, hi = 0.0, u * R3
    if f(lo) > 0 or f(hi) < 0:
        return None
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    c2 = 0.5 * (lo + hi)
    lnZB, UB, SB = radial_stats(n, gB(n, u, R3, c2))
    return c2, UA, UB, lnZA - lnZB, SA, SB


def part1():
    print("== 1: the cone with two fillings of its apex ball, exact sums ==")
    ok = True
    for (n, u, f) in ((600, 1.0, 0.3), (1000, 1.0, 0.3), (1000, 1.0, 0.6), (800, 2.0, 0.3), (800, 2.0, 0.6), (600, 4.0, 0.4),
                      (1200, 0.5, 0.4)):
        e1 = f * a_of(u)
        eps = e1 * n
        s = sig(u); s2 = sigma2(u, e1)
        x = u * (s2 - s)
        rho3_pred = rho_of_kl(u, x)
        lbt = ln_ball_table(n)
        found = None
        R3 = max(2, int(rho3_pred * n) - 25)
        while R3 <= n // 2 + 2 and found is None:
            best = None
            for R1 in range(max(1, int(s * n) - 2), R3 + 1):
                p = pair(n, u, R1, R3)
                if p is None:
                    continue
                if best is None or p[3] > best[1][3]:
                    best = (R1, p)
            if best is not None and best[1][3] > eps:
                found = (R3, best)
            else:
                R3 += 1
        if found is None:
            print(f"  n={n} u={u} eps1={e1:.4f}: no pair below n/2 (prediction rho3 = {rho3_pred:.4f})")
            ok = False
            continue
        R3, (R1, (c2, UA, UB, gap, SA, SB)) = found
        # without the datum: smallest R with D_R > eps  (flattening the cone at R lowers ln Z by D_R)
        lnZcone = radial_stats(n, u * np.arange(n + 1).astype(float))[0]
        Rnd = 1
        while lnZcone - radial_stats(n, gA(n, u, Rnd))[0] <= eps and Rnd < n // 2:
            Rnd += 1
        ex = lambda R: (n * LN2 - float(lbt[R - 1])) / n
        print(f"  n={n} u={u} eps1={f}a={e1:.4f} (eps={eps:.2f}): smallest R3 = {R3} (guess: rho3 n = {rho3_pred*n:.1f}), "
              f"R1 = {R1} (sigma2 n = {s2*n:.1f}), c2 = {c2:.4f} (u(sigma2-sigma_u)n = {x*n:.1f})")
        print(f"       U_A = {UA:.10f}  U_B = {UB:.10f}  (difference {UA-UB:+.1e});  S_A - S_B = {SA-SB:.4f};  ln Z_A - ln Z_B = {gap:.4f} > eps")
        print(f"       same values outside the open ball of radius R3: {np.array_equal(gA(n,u,R1)[R3:], gB(n,u,R3,c2)[R3:])};  "
              f"Lipschitz: A {np.max(np.abs(np.diff(gA(n,u,R1))))<=u+1e-12}, B {np.max(np.abs(np.diff(gB(n,u,R3,c2))))<=u+1e-12}")
        print(f"       exponent n^-1 ln(2^n/|B(n,R3-1)|) = {ex(R3):.5f}  [asymptotic guess theta_na(u(sigma2-sigma_u)) = {theta_na(u,x):.5f}];  "
              f"without the datum: R = {Rnd}, {ex(Rnd):.5f}  [theta_na(eps1) = {theta_na(u,e1):.5f}];  adaptive plateau bound theta_pl = {theta_pl(u,e1):.5f}")
        ok &= abs(UA - UB) < 1e-8 and gap > eps
    return ok


def part1b():
    print("== 1b: a displaced inner cone (enumeration, n = 14) ==")
    n, u = 14, 1.0
    N = 1 << n
    x = np.arange(N)
    pc = np.zeros(N, dtype=np.int64)
    for b in range(n):
        pc += (x >> b) & 1
    d = pc.astype(float)
    R3 = 6
    sp = 0b111                        # displaced apex at distance 3
    dp = pc[x ^ sp].astype(float)
    nb = [x ^ (1 << i) for i in range(n)]
    for c2 in (2.0, 3.0, 4.0):
        g = u * d.copy()
        ins = d < R3
        g[ins] = np.minimum(u * R3, c2 + u * dp[ins])
        L = max(np.max(np.abs(g - g[nbr])) for nbr in nb)
        print(f"  c2 = {c2} (u d(s,s') = 3.0): Lipschitz constant of the glued function = {L:.2f}  -> member: {L <= u + 1e-12}")
    return True


# ---------------------------------------------------------------- part 2
def bracket_width(n, u, g, r, lp):
    """width of the datum-assisted bracket for the radial instance g (values g[d]) when the
    unexplored set is the ball of radius r.  lp = ln( C(n,d)/2^n ).  Works with g - min g."""
    g = g - g.min()
    lw = lp - g
    lnA = float(logsumexp(lw))                       # ln (Z/2^n)
    p = np.exp(lw - lnA)
    U = float((p * g).sum())
    d = np.arange(n + 1)
    out = d > r
    gt = g[r + 1]                                    # energy level of the threshold t
    rho = np.maximum(r + 1 - d, 0)
    # lower end
    low_s = float(np.logaddexp(logsumexp(lw[out]), logsumexp(lp[~out]) - gt))
    low_e = n * hb(sig(u)) - U - n * LN2
    low = max(low_s, low_e)
    # upper end: minimise over eta.  In energies: f_eta(e^{-v}) = e^{-v}(1 - eta (U - v));
    # best level v* = U + 1 - 1/eta, clipped to [gt - u rho, gt] inside the ball.
    def upper(eta):
        vstar = U + 1.0 - 1.0 / eta
        v_in = np.clip(vstar, gt - u * rho[~out], gt)
        terms_in = np.exp(lp[~out] - v_in + 0.0) * (1 - eta * (U - v_in))
        terms_out = np.exp(lw[out]) * (1 - eta * (U - g[out]))
        tot = terms_in.sum() + terms_out.sum()
        return tot
    # eta = 0 gives the unconstrained tail lemma
    cands = [0.0] + list(np.exp(np.linspace(math.log(1e-4), math.log(50.0), 400)))
    vals = []
    for eta in cands:
        if eta == 0.0:
            v_in = gt - u * rho[~out]
            tot = np.exp(lp[~out] - v_in).sum() + np.exp(lw[out]).sum()
        else:
            tot = upper(eta)
        vals.append(tot)
    vals = np.array(vals)
    k = int(np.argmin(np.where(vals > 0, vals, np.inf)))
    best = vals[k]
    # refine around the best eta
    if 0 < k < len(cands) - 1:
        lo, hi = cands[k - 1] if cands[k - 1] > 0 else 1e-6, cands[k + 1]
        for _ in range(60):
            m1 = lo + (hi - lo) * 0.382; m2 = lo + (hi - lo) * 0.618
            if upper(m1) < upper(m2): hi = m2
            else: lo = m1
        best = min(best, upper(0.5 * (lo + hi)))
    up = math.log(best)
    return up - low, lnA, up, low, U


def needed_radius(n, u, g, eps, lp, rmin=0):
    """largest r < n/2 such that the bracket at unexplored radius r is narrower than eps"""
    best = None
    for r in range(rmin, n // 2):
        w, lnA, up, low, U = bracket_width(n, u, g, r, lp)
        if not (low - 1e-7 <= lnA <= up + 1e-7):
            raise RuntimeError(f"bracket does not contain the truth: r={r} low={low} lnA={lnA} up={up}")
        if w <= eps:
            best = r
    return best


def part2():
    print("== 2: the datum-assisted bracket on radial instances (exact) ==")
    ok = True
    for (n, u, f) in ((400, 1.0, 0.3), (400, 1.0, 0.6), (400, 2.0, 0.4), (300, 4.0, 0.4)):
        e1 = f * a_of(u); eps = e1 * n
        s = sig(u); s2 = sigma2(u, e1); x = u * (s2 - s)
        lp = lnC(n) - n * LN2
        lbt = ln_ball_table(n)
        d = np.arange(n + 1).astype(float)
        fam = {}
        fam["cone"] = [u * d]
        fam["truncated cones (A)"] = [u * np.maximum(d, R1) for R1 in range(int(s * n), n // 2, max(1, n // 100))]
        fam["raised cones (B)"] = [gB(n, u, R3, c2) for R3 in range(int(s * n) + 5, n // 2, max(2, n // 40))
                                   for c2 in np.linspace(0.0, u * R3, 7)[1:-1]]
        fam["flat + plateau basin"] = [-np.minimum(c, u * np.maximum(R + 1 - d, 0)) for R in range(int(0.2 * n), n // 2, max(2, n // 25))
                                       for c in np.linspace(0.0, u * (R + 1), 6)[1:]]
        fam["soft cones v<u"] = [v * d for v in (0.25 * u, 0.5 * u, 0.75 * u)]
        fam["two-slope cones"] = [np.where(d < k, 0.5 * u * d, 0.5 * u * k + u * (d - k)) for k in range(int(0.1 * n), n // 2, max(2, n // 12))]
        print(f"  n={n} u={u} eps1={f}a={e1:.4f}: guess: unexplored radius rho3 n = {rho_of_kl(u, x)*n:.1f} "
              f"(exponent {theta_na(u,x):.4f}); no datum: {rho_of_kl(u,e1)*n:.1f} ({theta_na(u,e1):.4f})")
        worst = (n, None)
        for name, insts in fam.items():
            rs = []
            for g in insts:
                r = needed_radius(n, u, g, eps, lp)
                rs.append(r if r is not None else -1)
            rmin = min(rs)
            print(f"     {name:24s}: {len(insts):3d} instances, smallest needed unexplored radius {rmin:4d}  "
                  f"(exponent {(n*LN2 - float(lbt[max(rmin,0)]))/n:.4f})")
            if rmin < worst[0]:
                worst = (rmin, name)
        print(f"     worst family: {worst[1]} at r = {worst[0]};  guess rho3 n = {rho_of_kl(u, x)*n:.1f}")
    return ok


if __name__ == "__main__":
    t0 = time.time()
    ok1 = part1()
    part1b()
    if not (len(sys.argv) > 1 and sys.argv[1] == "part1"):
        ok2 = part2()
    print("SUMMARY pair exists with equal energies and gap > eps:", ok1, f"  time {time.time()-t0:.0f}s")
