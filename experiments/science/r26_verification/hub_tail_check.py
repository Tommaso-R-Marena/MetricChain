#!/usr/bin/env python3
"""Coordinator's check of the finding of workstream R26 that decides most (its F2): on a nearest-neighbour chain
with the dependence between blocks confined to ONE outer site, the outer integrand is outside the class whose
tail function the product-class certificate uses.

Written from the statement in docs/science/workstreams/R26_REPORT.md (F2) and from the definitions it quotes;
it does NOT use the referee's code and does NOT run the nested algorithm.  What it checks is the inequality the
algorithm's upper end rests on:

    (TU)   mu_o(V > s) <= q   ==>   E (V - s)_+  <=  s * Xi(q),

with Xi the exact tail function of an envelope rho (Lemma N.0 as the report quotes it):
    Xi_rho(q) = sup { sum_{x in D} mu_o(x) (e^{rho(x -> D^c)} - 1) :  mu_o(D) <= q },   Xi_rho(1) = +infinity,
    rho(x -> D^c) = min_{z not in D} rho(x, z),
computed here by enumeration of all 2^16 subsets D of the 16 outer points.

Instance (binary sites; 4 outer, k inner):  a_1..a_3 independent uniform;  P(a_4 = 1) = pi_h;
P(b_1 = a_4) = p_x = 1/(1 + e^{cx});  P(b_{j+1} != b_j) = p_in = 1/(1 + e^{cin});
residual psi = u (a_1 + a_2 + a_3) + u |b|  (additive, u-Lipschitz in every site);
V(a) = e^{-u(a_1+a_2+a_3)} E[e^{-u|b|} | a_4].

Envelopes:  (A) product class, rho = u * Hamming on the four outer sites;
            (B) the envelope of the theory division's Theorem N4: u * Hamming on sites 1..3 plus
                iota = ln(V_1/V_0) when x_4 = 1 and z_4 = 0  (the class-relative influence of the boundary site);
controls:   (C) the same chain with no coupling across the cut (p_x = 1/2) and envelope (A): must satisfy (TU);
            (B) must satisfy (TU);  (A) with coupling must NOT.
Run:  python3 -B hub_tail_check.py
"""
import math, resource, time
import numpy as np

resource.setrlimit(resource.RLIMIT_AS, (3 * 1024**3, 3 * 1024**3))
T0 = time.time()
C = 4


def inner_moment(k, p_x, p_in, u):
    """E[e^{-u|b|} | a_4 = h], h = 0, 1, by a backward recursion along the inner chain."""
    w = np.array([1.0, math.exp(-u)])                 # weight of b_j = 0, 1
    f = w.copy()                                      # f[s] = E[prod_{i >= j} w(b_i) | b_j = s]
    for _ in range(k - 1):
        f = w * np.array([(1 - p_in) * f[0] + p_in * f[1], p_in * f[0] + (1 - p_in) * f[1]])
    # b_1 = a_4 with probability p_x (so the common state a_4 = 0 sends the inner chain to 1...1)
    return np.array([p_x * f[0] + (1 - p_x) * f[1], (1 - p_x) * f[0] + p_x * f[1]])


def inner_moment_enum(k, p_x, p_in, u):
    """the same by enumeration of the 2^k inner configurations (control of the recursion)."""
    out = np.zeros(2)
    for h in (0, 1):
        tot = 0.0
        for conf in range(1 << k):
            b = [(conf >> j) & 1 for j in range(k)]
            p = p_x if b[0] == h else 1 - p_x
            for j in range(k - 1):
                p *= p_in if b[j + 1] != b[j] else 1 - p_in
            tot += p * math.exp(-u * sum(b))
        out[h] = tot
    return out


def tail_function(mu, rho):
    """all subsets D: (mu(D), I(D)); returns sorted masses and the running maximum of I."""
    n = len(mu)
    masks = np.arange(1, (1 << n) - 1, dtype=np.int64)                  # proper nonempty subsets
    member = ((masks[:, None] >> np.arange(n)[None, :]) & 1).astype(bool)   # (subsets, points)
    mass = member @ mu
    I = np.zeros(len(masks))
    big = 1e300
    for x in range(n):
        r = np.where(member, big, rho[x][None, :]).min(axis=1)          # rho(x -> D^c)
        I += np.where(member[:, x], mu[x] * np.expm1(r), 0.0)
    order = np.argsort(mass, kind="stable")
    return mass[order], np.maximum.accumulate(I[order])


def xi(masses, runmax, q):
    """Xi(q) = max{I(D): mu(D) <= q}; 0 if no nonempty subset has mass <= q; +inf at q = 1."""
    if q >= 1 - 1e-15:
        return math.inf
    j = np.searchsorted(masses, q * (1 + 1e-12), side="right") - 1
    return runmax[j] if j >= 0 else 0.0


def worst_tu(mu, V, masses, runmax):
    """sup over levels s of E(V-s)_+ / (s * Xi(p(s))), p(s) = mu(V > s); levels: every value of V and a fine grid."""
    levels = np.unique(np.concatenate([V, np.exp(np.linspace(math.log(V.min()) - 2, math.log(V.max()), 4000))]))
    worst, where = 0.0, None
    for s in levels:
        p = float(mu[V > s].sum())
        if p <= 0:
            continue
        excess = float((mu * np.clip(V - s, 0, None)).sum())
        x = xi(masses, runmax, p)
        ratio = 0.0 if math.isinf(x) else (math.inf if x == 0 else excess / (s * x))
        if ratio > worst:
            worst, where = ratio, (s, p)
    return worst, where


def instance(k, u, pi_h, cx, cin):
    p_x = 1 / (1 + math.exp(cx)) if cx is not None else 0.5
    p_in = 1 / (1 + math.exp(cin))
    Vh = inner_moment(k, p_x, p_in, u)
    pts = np.arange(1 << C)
    bits = (pts[:, None] >> np.arange(C)[None, :]) & 1
    a4 = bits[:, C - 1]
    rest = bits[:, : C - 1].sum(axis=1)
    mu = np.where(a4 == 1, pi_h, 1 - pi_h) / (1 << (C - 1))
    V = np.exp(-u * rest) * Vh[a4]
    ham3 = (bits[:, None, : C - 1] != bits[None, :, : C - 1]).sum(axis=2).astype(float)
    flip4 = (a4[:, None] != a4[None, :]).astype(float)
    iota = math.log(Vh[1] / Vh[0])
    rhoA = u * (ham3 + flip4)
    rhoB = u * ham3 + max(iota, 0.0) * ((a4[:, None] == 1) & (a4[None, :] == 0))
    return dict(mu=mu, V=V, Vh=Vh, iota=iota, rhoA=rhoA, rhoB=rhoB, a4=a4, p_x=p_x, p_in=p_in)


def main():
    print("hub_tail_check.py   started", time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))
    u = 1.0
    bad = 0
    # control of the recursion against enumeration (k = 12)
    r = inner_moment(12, 1 / (1 + math.exp(10)), 1 / (1 + math.exp(7.6)), u)
    e = inner_moment_enum(12, 1 / (1 + math.exp(10)), 1 / (1 + math.exp(7.6)), u)
    print(f"recursion against enumeration of 2^12 inner configurations: largest relative difference {np.abs(r / e - 1).max():.1e}")
    bad += int(np.abs(r / e - 1).max() > 1e-12)
    for (k, cx, cin, label) in ((16, 14.0, 11.0, "chain of the report: 16 inner sites, couplings 14 kT across the cut, 11 kT inside"),
                                (12, 10.0, 7.6, "the weaker chain: 12 inner sites, couplings 10 and 7.6 kT")):
        print(f"\n== {label}")
        for pi_h in (0.002, 0.02, 0.2):
            I = instance(k, u, pi_h, cx, cin)
            mu, V = I["mu"], I["V"]
            A = float((mu * V).sum())
            share = float((mu * V)[I["a4"] == 1].sum()) / A
            mA, rA = tail_function(mu, I["rhoA"])
            mB, rB = tail_function(mu, I["rhoB"])
            wA, atA = worst_tu(mu, V, mA, rA)
            wB, atB = worst_tu(mu, V, mB, rB)
            # is V inside each envelope?  max over pairs of ln V(x) - ln V(z) - rho(x, z)
            L = np.log(V)
            outA = float((L[:, None] - L[None, :] - I["rhoA"]).max())
            outB = float((L[:, None] - L[None, :] - I["rhoB"]).max())
            print(f"  pi_h = {pi_h}: ln(V_1/V_0) = {I['iota']:.4f}; share of the rare boundary state in A = {100*share:.2f} %")
            print(f"     (A) product-class envelope: V exceeds it by {outA:.3f} nats; worst (TU) ratio {wA:.4g} at level s = {atA[0]:.3g}, p(s) = {atA[1]:.4g}")
            print(f"     (B) envelope with the influence at the boundary site: V exceeds it by {outB:.1e}; worst (TU) ratio {wB:.6f}")
            bad += int(not (wA > 1.0)) + int(wB > 1 + 1e-9) + int(outB > 1e-9)
        # control (C): no coupling across the cut
        I = instance(k, u, 0.02, None, cin)
        mA, rA = tail_function(I["mu"], I["rhoA"])
        wC, _ = worst_tu(I["mu"], I["V"], mA, rA)
        print(f"  control, no coupling across the cut (pi_h = 0.02): ln(V_1/V_0) = {I['iota']:.2e}; worst (TU) ratio with the product-class envelope {wC:.6f} (must be <= 1)")
        bad += int(wC > 1 + 1e-9)
    print(f"\nstatements that must hold and did not: {bad}")
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    print(f"ALL DONE   computed in {time.time() - T0:.1f} s   peak memory {peak:.0f} MB")
    assert bad == 0


if __name__ == "__main__":
    main()
