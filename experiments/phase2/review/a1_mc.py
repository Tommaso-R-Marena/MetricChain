#!/usr/bin/env python3
"""a1_mc.py -- referee A1: Monte Carlo for the new Theorem A' at moderate size (n = 16..20).

Written from docs/phase2/PHASE2_REPORT.md (sections 1, 2.3) only; nothing imported from the repo.

For L independent uniform centres c_1..c_L on {0,1}^n and narrow dips of radius r,
    w_c = 1 + max_j e_r(. xor c_j),  e_r(x) = (exp(u(r-|x|)) - 1)_+ ,
the script samples instances and records, for a few FIXED observables phi with values in [-1,1],
    G_psi(c) = E_pi[(w_c - 1) psi]  (psi = phi - E_pi phi),   bias = E_{mu_{w_c}} phi - E_pi phi = G_psi / A(w_c),
    O_c  = sum_{j<j'} E_pi min(e_j, e_j'),   Otilde_c = E_pi(sum_j e_j - max_j e_j) = L m_r - (A - 1),
    C_psi = E_pi[(sum_j e_j - max_j e_j) psi]   (the part of the bias due to the overlaps; the first
            version of the theorem bounded it by Otilde_c ||psi|| and needed Otilde_c << tau).
Compared with:  E G_psi = 0 (Lemma 2.5 (iv));  P(|G_psi| > t) <= 2 exp(-t^2/(8 R m_r)) (the report's
McDiarmid bound, d = 4 m_r) and <= 2 exp(-t^2/(2 R m_r)) (referee's constant, d = 2 m_r);
tau_min = sqrt(8 R m_r ln(2M/eta)) = the least tolerance the theorem allows for M observables in the
text that was reviewed (commit 67956b7); the text as revised after this review (2026-11-28 03:17 UTC)
has the constant 2, i.e. the least tolerance tau2 = tau_min/2: the lines "revised text" report that;
P(O_c >= R/2) <= eta''.  The regimes are chosen so that the overlaps are NOT small compared with
tau_min (there the first version of the theorem is void: eta' > 1), plus one control regime and one
regime with heavy overlaps (eta'' > 1, where only Lemma 2.5 (iv) + McDiarmid are tested).

Usage: python3 a1_mc.py [quick]
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys
import math
import time
import itertools
import numpy as np

ETA = 0.1


def popcount_table(n):
    x = np.arange(1 << n, dtype=np.uint32)
    pc = np.zeros(1 << n, dtype=np.int16)
    for i in range(n):
        pc += ((x >> i) & 1).astype(np.int16)
    return pc


def ball_masks(n, rad):
    masks, wts = [0], [0]
    for k in range(1, rad + 1):
        for comb in itertools.combinations(range(n), k):
            m = 0
            for i in comb:
                m |= 1 << i
            masks.append(m)
            wts.append(k)
    return np.array(masks, dtype=np.int64), np.array(wts, dtype=np.int64)


def make_observables(n, seed=12345):
    N = 1 << n
    x = np.arange(N, dtype=np.int64)
    pc = popcount_table(n).astype(np.int64)
    rng = np.random.default_rng(seed)
    k0 = 0
    while sum(math.comb(n, j) for j in range(k0 + 2)) <= 0.03 * N:     # largest ball below 3% of the cube
        k0 += 1
    obs = [
        ("chi_1", (1 - 2 * (x & 1)).astype(np.float64)),
        ("chi_123", (1 - 2 * (((x & 1) + ((x >> 1) & 1) + ((x >> 2) & 1)) & 1)).astype(np.float64)),
        ("parity", (1 - 2 * (pc & 1)).astype(np.float64)),
        ("majority", np.sign(n - 2 * pc).astype(np.float64)),
        ("linear", 1.0 - 2.0 * pc / n),
        ("cell4", ((x & 15) == 0).astype(np.float64)),
        ("1-2*B(0,%d)" % k0, 1.0 - 2.0 * (pc <= k0)),
        ("rand_pm1", rng.choice(np.array([-1.0, 1.0]), size=N)),
    ]
    return obs


def instance(n, r, exc, masks, mwt, centres, Psi):
    """returns (A-1, O_c, G[K], Gsum[K]) for one tuple of centres (sparse: only the union of the balls)."""
    N = 1 << n
    pts = (centres[:, None] ^ masks[None, :]).ravel()
    key = pts * r + np.tile(mwt, len(centres))      # sort by point, then by decreasing excess
    key.sort()
    spts = key // r
    sk = key % r
    vals = exc[sk]
    first = np.empty(len(key), dtype=bool)
    first[0] = True
    first[1:] = spts[1:] != spts[:-1]
    idx = np.arange(len(key))
    rank = idx - np.maximum.accumulate(np.where(first, idx, 0))      # 0 for the largest value at a point
    Am1 = float(vals[first].sum()) / N
    O = float((rank * vals).sum()) / N
    G = (Psi[:, spts[first]] @ vals[first]) / N
    Gsum = (Psi[:, spts] @ vals) / N
    return Am1, O, G, Gsum


def dense_reference(n, u, r, centres, Phi):
    """direct computation from the definitions on the whole cube (small n only)."""
    N = 1 << n
    x = np.arange(N)
    pc = popcount_table(n).astype(np.int64)
    Ej = np.stack([np.where(pc[x ^ c] < r, np.expm1(u * (r - pc[x ^ c])), 0.0) for c in centres])
    wm1 = Ej.max(axis=0)
    Am1 = wm1.mean()
    O = 0.0
    for j in range(len(centres)):
        for k in range(j + 1, len(centres)):
            O += np.minimum(Ej[j], Ej[k]).mean()
    psi = Phi - Phi.mean(axis=1, keepdims=True)
    G = (psi * wm1[None, :]).mean(axis=1)
    Gsum = (psi * Ej.sum(axis=0)[None, :]).mean(axis=1)
    bias = (Phi * (1 + wm1)[None, :]).mean(axis=1) / (1 + Am1) - Phi.mean(axis=1)
    return Am1, O, G, Gsum, bias


def self_test():
    print("== self-test: sparse instance code against a dense computation from the definitions ==")
    rng = np.random.default_rng(1)
    worst = 0.0
    cases = 0
    for (n, u, r, L) in ((8, 1.0, 2, 6), (8, 1.0, 3, 9), (9, 0.4, 1, 40), (10, 2.0, 3, 30), (7, 1.0, 2, 60)):
        obs = make_observables(n)
        Phi = np.stack([p for _, p in obs])
        Psi = Phi - Phi.mean(axis=1, keepdims=True)
        masks, mwt = ball_masks(n, r - 1)
        exc = np.expm1(u * (r - np.arange(r)))
        for _ in range(5):
            c = rng.integers(0, 1 << n, size=L)
            if _ == 0:
                c[1] = c[0]                      # equal centres
            Am1, O, G, Gsum = instance(n, r, exc, masks, mwt, c, Psi)
            a2, o2, g2, gs2, bias2 = dense_reference(n, u, r, c, Phi)
            worst = max(worst, abs(Am1 - a2), abs(O - o2), float(np.abs(G - g2).max()), float(np.abs(Gsum - gs2).max()),
                        float(np.abs(G / (1 + Am1) - bias2).max()))
            cases += 1
    print("   %d instances (n = 7..10, equal centres included): max |sparse - dense| over (A-1, O_c, G, G_sum, bias) = %.1e %s"
          % (cases, worst, "ok" if worst < 1e-12 else "FAIL"))
    return worst < 1e-12


def run(name, n, u, r, L, n_inst, seed, note):
    t0 = time.time()
    N = 1 << n
    obs = make_observables(n)
    names = [nm for nm, _ in obs]
    Phi = np.stack([p for _, p in obs])
    assert np.all(np.abs(Phi) <= 1)
    K = len(obs)
    Psi = Phi - Phi.mean(axis=1, keepdims=True)
    psi_inf = np.abs(Psi).max(axis=1)
    masks, mwt = ball_masks(n, r - 1)
    V = len(masks)
    exc = np.expm1(u * (r - np.arange(r)))
    m_r = float(sum(math.comb(n, j) * math.expm1(u * (r - j)) for j in range(r))) / N
    assert V == sum(math.comb(n, j) for j in range(r))
    R = L * m_r
    eta2 = L * V / N
    sig0 = math.sqrt(R * m_r)                                  # = sqrt(L) m_r
    tau = math.sqrt(8 * R * m_r * math.log(2 * K / ETA))       # least tolerance allowed by Theorem A' (M = K, eta)
    eps = math.log1p(R / 2)                                    # largest accuracy allowed
    eta_old = (5 * R / (2 * tau)) * eta2                       # eta' of the first version at the same tau
    tau_old = math.sqrt(8 * math.log(2 * K / ETA) / L)         # least tolerance the first version allows (L >= 8 tau^-2 ln(2M/eta))
    eta_old2 = (5 * R / (2 * max(tau, tau_old))) * eta2        # its eta' at max(tau_min, tau_old)
    rng = np.random.default_rng(seed)
    A = np.empty(n_inst)
    O = np.empty(n_inst)
    G = np.empty((n_inst, K))
    Gs = np.empty((n_inst, K))
    for i in range(n_inst):
        c = rng.integers(0, N, size=L, dtype=np.int64)
        A[i], O[i], G[i], Gs[i] = instance(n, r, exc, masks, mwt, c, Psi)
    # one-centre replacements (Lemma 2.5 (iv), bounded differences) on a few instances
    phi_osc = Phi.max(axis=1) - Phi.min(axis=1)
    dmax, dmax_rel, nrep = 0.0, 0.0, 0
    for i in range(8):
        c = rng.integers(0, N, size=L, dtype=np.int64)
        G0 = instance(n, r, exc, masks, mwt, c, Psi)[2]
        for t in range(25):
            c2 = c.copy()
            c2[rng.integers(0, L)] = rng.integers(0, N)
            dG = np.abs(instance(n, r, exc, masks, mwt, c2, Psi)[2] - G0) / m_r
            dmax = max(dmax, float(dG.max()))
            dmax_rel = max(dmax_rel, float((dG / phi_osc).max()))
            nrep += 1
    Ot = R - A                                                 # Otilde_c
    D = G / (1 + A)[:, None]                                   # the actual bias
    C = Gs - G                                                 # part of the bias due to the overlaps
    print("== regime %s: n=%d u=%g r=%d L=%d, %d instances [%.0fs]  -- %s" % (name, n, u, r, L, n_inst, time.time() - t0, note))
    print("   m_r=%.4g  V(n,r-1)=%d  R=L m_r=%.4f  eta''=L V/2^n=%.4f  sigma0=sqrt(R m_r)=%.4g" % (m_r, V, R, eta2, sig0))
    print("   M=%d, eta=%.2f:  least tolerance allowed tau_min=sqrt(8 R m_r ln(2M/eta))=%.4g %s;  largest accuracy eps=ln(1+R/2)=%.4f;  new bound factor 1-eta-eta''=%.3f"
          % (K, ETA, tau, "(<=1)" if tau <= 1 else "(>1: hypotheses not satisfiable)", eps, 1 - ETA - eta2))
    print("   first version (eta' = (5 L m_r/(2 tau)) L V/2^n; needs L >= 8 tau^-2 ln(2M/eta), i.e. tau >= %.4g): eta' = %.3g at tau_min, %.3g at max(tau_min, %.4g)  => %s"
          % (tau_old, eta_old, eta_old2, tau_old, "void in this regime (eta' >= 1 - eta)" if eta_old2 >= 1 - ETA else "usable in this regime"))
    print("   overlaps:  E O_c=%.4g (bound C(L,2) m_r V/2^n=%.4g)  E Otilde_c=%.4g   =>  E O_c/tau_min=%.2f, E Otilde_c/tau_min=%.2f;  first version needs O_c <= tau/5: frequency %.4f"
          % (O.mean(), math.comb(L, 2) * m_r * V / N, Ot.mean(), O.mean() / tau, Ot.mean() / tau, float((O <= tau / 5).mean())))
    lowviol = float(((R - O) - A).max())
    print("   Lemma 2.5(ii): max[(R-O_c)-(A-1)]=%+.1e (<=0 %s), max[(A-1)-R]=%+.1e (<=0 %s);  P(O_c>=R/2)=%.4f <= (L-1)V/2^n=%.4f %s;  P(A-1<=R/2)=%.4f;  (A-1)/R in [%.3f, %.3f]"
          % (lowviol, "ok" if lowviol <= 1e-12 else "FAIL", float((A - R).max()), "ok" if (A - R).max() <= 1e-12 else "FAIL",
             float((O >= R / 2).mean()), (L - 1) * V / N, "ok" if (O >= R / 2).mean() <= (L - 1) * V / N + 3 * math.sqrt(0.25 / n_inst) else "FAIL",
             float((A <= R / 2).mean()), float((A / R).min()), float((A / R).max())))
    print("   bounded differences: %d single-centre replacements: max |G(c)-G(c')|/m_r = %.4f (lemma: <= 2|psi|oo <= 4);  max |G(c)-G(c')|/(osc(phi) m_r) = %.4f (referee: <= 1) %s"
          % (nrep, dmax, dmax_rel, "ok" if dmax <= 4 + 1e-9 and dmax_rel <= 1 + 1e-9 else "FAIL"))
    ks = (1.0, 2.0, 3.0, 4.0)
    print("   McDiarmid at t = k*sigma0, k=%s:  report 2exp(-k^2/8) = %s;  referee 2exp(-k^2/2) = %s"
          % (ks, ["%.3g" % min(1, 2 * math.exp(-k * k / 8)) for k in ks], ["%.3g" % min(1, 2 * math.exp(-k * k / 2)) for k in ks]))
    print("   %-12s %7s | %11s %6s | %9s | %-31s | %-27s %9s | %10s %10s %11s" % (
        "phi", "|psi|oo", "mean G/sig0", "z", "sd G/sig0", "P(|G|>k sig0), k=1,2,3,4", "|b|/tau: q50   q99    max", "P(|b|>tau)", "mean C/tau", "sd C/tau", "max|C|/tau"))
    zmax = 0.0
    viol = 0
    for k in range(K):
        g = G[:, k]
        mean, sd = g.mean(), g.std(ddof=1)
        z = mean / (sd / math.sqrt(n_inst)) if sd > 0 else 0.0
        zmax = max(zmax, abs(z))
        tails = [float((np.abs(g) > kk * sig0).mean()) for kk in ks]
        for kk, tl in zip(ks, tails):                      # empirical tail against the two bounds (3-sigma MC slack)
            for bnd in (2 * math.exp(-kk * kk / 8), 2 * math.exp(-kk * kk / 2)):
                if tl > bnd + 3 * math.sqrt(max(bnd * (1 - min(bnd, 1)), 1e-12) / n_inst) + 1e-12 and bnd < 1:
                    viol += 1
        c = C[:, k]
        ab = np.abs(D[:, k]) / tau
        print("   %-12s %7.3f | %+11.4f %+6.2f | %9.4f | %7.4f %7.4f %7.4f %7.4f |        %6.4f %6.4f %6.4f %9.4f | %+10.4f %10.4f %11.4f" % (
            names[k], psi_inf[k], mean / sig0, z, sd / sig0, tails[0], tails[1], tails[2], tails[3],
            float(np.quantile(ab, 0.5)), float(np.quantile(ab, 0.99)), float(ab.max()), float((ab > 1).mean()),
            c.mean() / tau, c.std(ddof=1) / tau, float(np.abs(c).max()) / tau))
    bad_any = float((np.abs(D).max(axis=1) > tau).mean())
    not_good = float(((np.abs(D).max(axis=1) > tau) | (A <= R / 2)).mean())
    tau2 = tau / 2                                             # least tolerance of the revised text (constant 2)
    bad_any2 = float((np.abs(D).max(axis=1) > tau2).mean())
    not_good2 = float(((np.abs(D).max(axis=1) > tau2) | (A <= R / 2)).mean())
    per_obs2 = float((np.abs(D) > tau2).mean(axis=0).max())
    print("   all %d observables:  P(exists i: |bias_i| > tau_min) = %.4f (theorem: <= eta = %.2f);  P(not good) = %.4f (theorem: <= eta+eta'' = %.3f);  max |z| of the means = %.2f;  tail violations: %d"
          % (K, bad_any, ETA, not_good, ETA + eta2, zmax, viol))
    print("   revised text (2 R m_r ln(2M/eta) <= tau^2): least tolerance tau2 = %.4g %s;  E O_c/tau2 = %.2f, E Otilde_c/tau2 = %.2f;  max |bias|/tau2 = %.4f;  "
          "max_i P(|bias_i| > tau2) = %.4f (theorem: <= eta/M = %.4f);  P(exists i: |bias_i| > tau2) = %.4f (<= eta = %.2f);  P(not good) = %.4f (<= eta+eta'' = %.3f)"
          % (tau2, "(<=1)" if tau2 <= 1 else "(>1)", O.mean() / tau2, Ot.mean() / tau2, float(np.abs(D).max()) / tau2,
             per_obs2, ETA / K, bad_any2, ETA, not_good2, ETA + eta2))
    print()
    sys.stdout.flush()
    return dict(zmax=zmax, viol=viol, bad_any=bad_any, not_good=not_good, eta2=eta2, zs=None)


def main():
    quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
    f = 0.05 if quick else 1.0
    print("a1_mc.py -- referee A1 -- Monte Carlo, numpy %s" % np.__version__)
    print("tau = the LEAST tolerance for which the hypotheses of the new Theorem A' hold (M = 8 observables, eta = %.2f); 'b' = bias = E_mu phi - E_pi phi; 'C' = overlap part of the bias" % ETA)
    print()
    ok = self_test()
    print()
    regimes = [
        ("A (overlaps > tau)", 20, 1.0, 2, 10000, 2000, 101, "narrow dips of radius 2; overlaps comparable with / above tau"),
        ("B (overlaps >> tau)", 20, 1.0, 1, 200000, 2000, 102, "dips = single points; many coincident centres; overlaps ~ 8 tau"),
        ("C", 20, 1.0, 3, 1000, 2000, 103, "radius 3, L = 1000"),
        ("D", 18, 2.0, 2, 3000, 2000, 104, "steeper slope u = 2"),
        ("G (overlaps >> tau)", 20, 0.3, 2, 20000, 1500, 107, "flat slope u = 0.3, radius 2; overlaps ~ 4 tau"),
        ("F (control)", 16, 1.0, 2, 300, 3000, 106, "overlaps small compared with tau: the regime of the first version"),
        ("E (heavy overlap)", 16, 1.0, 3, 1000, 2000, 105, "eta'' > 1: the theorem is void, Lemma 2.5(iv) + McDiarmid still have to hold"),
    ]
    res = []
    for (name, n, u, r, L, n_inst, seed, note) in regimes:
        res.append(run(name, n, u, r, L, max(50, int(n_inst * f)), seed, note))
    nz = sum(1 for _ in res) * 8
    print("summary: self-test %s; regimes %d; largest |z| of a mean of G_psi over all %d (regime, observable) pairs: %.2f; tail violations (beyond 3 sigma MC error): %d"
          % ("ok" if ok else "FAIL", len(res), nz, max(x["zmax"] for x in res), sum(x["viol"] for x in res)))


if __name__ == "__main__":
    main()
