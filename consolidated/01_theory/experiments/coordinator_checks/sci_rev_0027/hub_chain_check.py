#!/usr/bin/env python3
"""Coordinator's own check of finding 2.2 of SCI-REV-0027 (the Scientific Discovery Division's review of
theory report 11.33): "a hub is not a counterexample" is false at finite size.

Written from the statement of the instance (a nearest-neighbour chain of binary sites, 4 outer and 16
inner; a_1..a_3 uniform, P(a_4 = 1) = pi_h; b_1 differs from a_4 except with probability 1/(1 + e^14);
neighbouring inner sites differ with probability 1/(1 + e^11); residual u(a_1 + a_2 + a_3) + u|b|, u = 1),
with code of our own; the nested algorithm is not run.  Checked: the inequality (TU) on which the upper
end of a bracket rests,  mu(V > s) <= q  ==>  E(V - s)_+ <= s Xi(q),  for
  (A) the exact tail function of the product-class envelope u * Hamming on the four outer sites,
  (B) the envelope of Theorem 11.119(b): the class-relative influence ln(V_1/V_0) added at the boundary site,
  (C) the chain without the coupling across the cut, envelope (A).
Xi by enumeration of all subsets of the 16 outer points (exit costs by a sweep over the complement).
"""
import math, itertools

def fibre_moment(k, p_keep, p_flip, u):
    """E[e^{-u|b|} | a_4 = h] for h = 0, 1: b_1 = a_4 with probability p_keep, neighbours differ with p_flip."""
    f = [1.0, math.exp(-u)]                       # last site
    for _ in range(k - 1):
        f = [1.0 * ((1 - p_flip) * f[0] + p_flip * f[1]), math.exp(-u) * (p_flip * f[0] + (1 - p_flip) * f[1])]
    return [p_keep * f[0] + (1 - p_keep) * f[1], (1 - p_keep) * f[0] + p_keep * f[1]]

def worst_ratio(mu, V, rho):
    """max over levels s of E(V - s)_+ / (s * Xi(mu(V > s))), Xi exact for the envelope rho (a matrix)."""
    n = len(mu)
    full = (1 << n) - 1
    # for every proper nonempty D: mass and I(D) = sum_{x in D} mu(x)(e^{rho(x -> D^c)} - 1)
    best = {}                                      # mass (rounded) -> max I; then prefix maxima over sorted masses
    recs = []
    for D in range(1, full):
        out = [z for z in range(n) if not (D >> z) & 1]
        mass = 0.0; I = 0.0
        for x in range(n):
            if (D >> x) & 1:
                mass += mu[x]
                I += mu[x] * math.expm1(min(rho[x][z] for z in out))
        recs.append((mass, I))
    recs.sort()
    masses = [r[0] for r in recs]
    run = []; m = 0.0
    for (_, I) in recs:
        m = max(m, I); run.append(m)
    import bisect
    def xi(q):
        if q >= 1 - 1e-15: return math.inf
        i = bisect.bisect_right(masses, q + 1e-15) - 1
        return run[i] if i >= 0 else 0.0
    worst = 0.0
    levels = sorted(set(V))
    for i in range(len(levels) - 1):
        s = levels[i]                               # the excess over s is largest relative to s at the left end
        q = sum(mu[x] for x in range(n) if V[x] > s)
        ex = sum(mu[x] * (V[x] - s) for x in range(n) if V[x] > s)
        X = xi(q)
        if X == math.inf: continue
        worst = max(worst, ex / (s * X) if X > 0 else math.inf)
    return worst

def main():
    u, k = 1.0, 16
    pts = list(itertools.product((0, 1), repeat=4))
    ham = lambda x, z: sum(a != b for a, b in zip(x, z))
    print("chain with one boundary site: largest E(V - s)_+ / (s Xi(q)) over the levels (above 1 = (TU) fails)")
    for pi_h in (0.002, 0.02, 0.2):
        mu = [0.125 * (pi_h if x[3] == 1 else 1 - pi_h) for x in pts]
        res = {}
        for name, cx in (("coupled", 14.0), ("uncoupled", 0.0)):
            p_keep = 1 / (1 + math.exp(cx)); p_flip = 1 / (1 + math.exp(11.0))
            m0, m1 = fibre_moment(k, p_keep, p_flip, u)
            V = [math.exp(-u * (x[0] + x[1] + x[2])) * (m1 if x[3] == 1 else m0) for x in pts]
            iota = math.log(m1 / m0)
            rhoA = [[u * ham(x, z) for z in pts] for x in pts]
            rhoB = [[u * ham(x[:3], z[:3]) + (max(iota, 0.0) if (x[3] == 1 and z[3] == 0) else (max(-iota, 0.0) if (x[3] == 0 and z[3] == 1) else 0.0)) for z in pts] for x in pts]
            res[name] = (iota, worst_ratio(mu, V, rhoA), worst_ratio(mu, V, rhoB))
        iota, a, b = res["coupled"]
        _, c, _ = res["uncoupled"]
        print(f"  pi_h = {pi_h}: ln(V_1/V_0) = {iota:.4f};  (A) product-class envelope: {a:.4g};  (B) with the influence at the boundary site: {b:.6f};  (C) no coupling, envelope (A): {c:.6f}")
        assert a > 1e3 and b <= 1 + 1e-9 and c <= 1 + 1e-9
    print("ALL CHECKS PASSED: (A) fails by four orders of magnitude, (B) and (C) hold")

if __name__ == "__main__":
    main()
