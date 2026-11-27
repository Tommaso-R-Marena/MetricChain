#!/usr/bin/env python3
"""R9 — second part of r9_sites.py (the tests that follow the data points), run separately with lighter parameters:
the ceiling F*(t) <= t(1-t) D^2/8 on random asymmetric sites, the comparison with the cube for site laws with weight 1/2
on a set of letters, and the chi^2 bound of Theorem 11.97(c).  Uses the class Site of r9_sites.py."""
import math, sys
import numpy as np
from scipy.optimize import minimize
sys.dont_write_bytecode = True
from r9_sites import Site, hamming, cube_values

if __name__ == "__main__":
    P = lambda *a: (print(*a), sys.stdout.flush())
    # ------------------------------------------------------------------ 2(c)(b): the ceiling for every envelope
    rng = np.random.default_rng(20261126)
    worst = 0.0; ncase = 0; worst_h = 0.0
    for trial in range(40):
        q = int(rng.integers(2, 5))
        while True:                                                         # random asymmetric envelope with the triangle inequality
            d = rng.uniform(0.1, 2.5, size=(q, q)); np.fill_diagonal(d, 0)
            for _ in range(q):                                              # shortest-path closure
                for b in range(q):
                    d = np.minimum(d, d[:, [b]] + d[[b], :])
            np.fill_diagonal(d, 0)
            if d.max() > 0:
                break
        pi = rng.dirichlet(np.ones(q))
        s = Site(pi, d)
        for t in (0.05, 0.2, 0.35, 0.5, 0.65, 0.8, 0.95):
            p, du, _ = s.Fstar(t)
            ratio = du / (t * (1 - t) * s.D ** 2 / 8)
            worst = max(worst, ratio); ncase += 1
        worst_h = max(worst_h, s.h(ngrid=39)[2] / (s.D ** 2 / 32))
    P(f"\nceiling F*(t) <= t(1-t) D^2/8, D = max d: {ncase} (site, t) pairs on 40 random sites with asymmetric envelopes, q = 2..4:"
      f" largest ratio (dual value/ceiling) = {worst:.4f};  largest h/(D^2/32) = {worst_h:.4f}")
    for u in (0.1, 0.5, 1.0, 2.0):
        hc, ac, Ec = cube_values(u)
        s3 = Site([1 / 3] * 3, hamming(3, u))
        t, hp, hd = s3.h(ngrid=79)
        P(f"  u = {u}: cube h/(u^2/32) = {hc/(u*u/32):.4f};  uniform three-letter site h/(u^2/32) = {hp/(u*u/32):.4f}  (below the ceiling by {100*(1-hp/(u*u/32)):.1f} %)")
    # weight 1/2 on a set of letters  =>  F* >= F*_cube
    bad = 0; n = 0
    for trial in range(40):
        q = int(rng.integers(3, 5)); u = float(rng.uniform(0.2, 2.5))
        w = rng.dirichlet(np.ones(q - 1)) * 0.5
        k = int(rng.integers(1, q - 1))
        a_ = rng.dirichlet(np.ones(k)) * 0.5; b_ = rng.dirichlet(np.ones(q - k)) * 0.5
        pi = np.concatenate([a_, b_])
        s = Site(pi, hamming(q, u))
        for t in (0.1, 0.3, 0.5, 0.7, 0.9):
            fc = t * math.log(math.cosh(u / 2)) - math.log(math.cosh(t * u / 2))
            p, du, _ = s.Fstar(t); n += 1
            if du < fc - 1e-10: bad += 1
    P(f"site laws with weight 1/2 on a set of letters (Hamming, q = 3, 4, random u): F* >= F*_cube in {n - bad} of {n} (site, t) pairs")

    # ------------------------------------------------------------------ 3(a): the chi^2 bound
    P("\n3(a): (I - v)(P) = min_{gamma in L} KL(P||pi_gamma) <= KL(P||Q) <= chi^2(P||Q) for Q = pi_gamma0 in the window")

    def v_primal(s, Pm):
        """v(P) = min_{P'} [KL(P'||pi) + W(P',P)], W(P',P) = min E d(X',X) over couplings: a convex programme in the coupling K[a',a]"""
        q = len(s.pi)

        def obj(k):
            K = k.reshape(q, q)
            Pp = K.sum(axis=1)
            return float(np.sum(Pp * (np.log(np.maximum(Pp, 1e-300)) - np.log(s.pi))) + np.sum(K * s.d))
        cons = [{"type": "eq", "fun": (lambda k, a=a: k.reshape(q, q)[:, a].sum() - Pm[a])} for a in range(q)]
        best = 1e9
        for start in range(4):
            if start == 0:
                k0 = np.diag(Pm).ravel()
            else:
                R = rng.dirichlet(np.ones(q), size=q).T * Pm[None, :]
                k0 = R.ravel()
            res = minimize(obj, k0, method="SLSQP", bounds=[(0, 1)] * (q * q), constraints=cons, options={"ftol": 1e-15, "maxiter": 3000})
            if res.success or res.status in (0, 9):
                best = min(best, obj(np.clip(res.x, 0, None)))
        return best

    def v_dual(s, Pm):
        """max_{gamma in L} [ -ln E_pi e^{-gamma} - E_P gamma ]  (concave in gamma)"""
        q = len(s.pi)
        cons = [{"type": "ineq", "fun": (lambda g, a=a, b=b: s.d[a][b] - g[a] + g[b])} for a in range(q) for b in range(q) if a != b]

        def obj(g):
            return math.log(np.sum(s.pi * np.exp(-g))) + float(Pm @ g)
        best = (1e9, None)
        for g0 in [np.zeros(q)] + list(s.V):
            res = minimize(obj, g0, method="SLSQP", constraints=cons, options={"ftol": 1e-15, "maxiter": 3000})
            if obj(res.x) < best[0] and all(c["fun"](res.x) >= -1e-9 for c in cons):
                best = (obj(res.x), res.x)
        return -best[0], best[1]

    nt = 0; maxgap = 0.0; worst_ratio = 0.0; viol = 0
    for trial in range(120):
        q = int(rng.integers(2, 5))
        d = rng.uniform(0.1, 2.0, size=(q, q)); np.fill_diagonal(d, 0)
        for _ in range(q):
            for b in range(q):
                d = np.minimum(d, d[:, [b]] + d[[b], :])
        np.fill_diagonal(d, 0)
        pi = rng.dirichlet(np.ones(q) * 2)
        s = Site(pi, d)
        # a window point Q = pi_gamma0 with gamma0 a random point of L (convex combination of vertices), and P near Q
        lam = rng.dirichlet(np.ones(len(s.V)))
        g0 = lam @ s.V
        Q = pi * np.exp(-g0); Q /= Q.sum()
        scale = 10 ** rng.uniform(-3, -0.3)
        Pm = np.clip(Q + scale * rng.normal(size=q) * Q, 1e-9, None); Pm /= Pm.sum()
        I = float(np.sum(Pm * (np.log(Pm) - np.log(pi))))
        vp = v_primal(s, Pm); vd, gopt = v_dual(s, Pm)
        maxgap = max(maxgap, abs(vp - vd))
        ImV = I - vd
        chi2 = float(np.sum((Pm - Q) ** 2 / Q))
        klPQ = float(np.sum(Pm * (np.log(Pm) - np.log(Q))))
        nt += 1
        if ImV > chi2 + 1e-9 or ImV > klPQ + 1e-9 or ImV < -1e-9:
            viol += 1
        if chi2 > 1e-12:
            worst_ratio = max(worst_ratio, ImV / chi2)
        # letter probabilities in the window are at least pi_min e^{-D}
        assert Q.min() >= pi.min() * math.exp(-s.D) - 1e-12
    P(f"  {nt} random (site, window point Q, nearby P), q = 2..4, asymmetric envelopes: |v_primal - v_dual| <= {maxgap:.2e};"
      f" violations of 0 <= I - v <= KL(P||Q) <= chi^2(P||Q): {viol};  largest (I - v)/chi^2 = {worst_ratio:.4f}")

    # the bound on the set G of the proof: |P_j(a) - Q_j(a)| <= kappa2/lambda_j  =>  (I - v)(P) <= omega'
    P("  the bound on G: sum_j lambda_j (I-v)_j(P_j) <= omega' = m kappa2 [q_max e^{D_max}/pi_min + ln(1/pi_min)]")
    worst = 0.0; nt = 0
    for trial in range(300):
        m = int(rng.integers(1, 4))
        sites = []
        for j in range(m):
            q = int(rng.integers(2, 4))
            d = rng.uniform(0.1, 1.5, size=(q, q)); np.fill_diagonal(d, 0)
            for _ in range(q):
                for b in range(q):
                    d = np.minimum(d, d[:, [b]] + d[[b], :])
            np.fill_diagonal(d, 0)
            sites.append(Site(rng.dirichlet(np.ones(q) * 2), d))
        lam = rng.dirichlet(np.ones(m) * rng.choice([0.05, 0.3, 1.0]))
        kappa2 = 10 ** rng.uniform(-3.5, -1)
        qmax = max(len(s.pi) for s in sites); Dmax = max(s.D for s in sites); pmin = min(s.pi.min() for s in sites)
        omega = m * kappa2 * (qmax * math.exp(Dmax) / pmin + math.log(1 / pmin))
        tot = 0.0
        for j, s in enumerate(sites):
            q = len(s.pi)
            g0 = rng.dirichlet(np.ones(len(s.V))) @ s.V
            Q = s.pi * np.exp(-g0); Q /= Q.sum()
            # an adversarial P in the box |P - Q| <= kappa2/lambda_j: move mass between two letters by the full amount allowed
            r = min(kappa2 / lam[j], 1.0)
            a, b = rng.choice(q, 2, replace=False)
            dlt = min(r, Q[a] - 1e-9 if Q[a] > 1e-9 else 0.0, 1 - Q[b])
            Pm = Q.copy(); Pm[a] -= dlt; Pm[b] += dlt
            Pm = np.clip(Pm, 1e-12, None); Pm /= Pm.sum()
            I = float(np.sum(Pm * (np.log(Pm) - np.log(s.pi))))
            vd, _ = v_dual(s, Pm)
            tot += lam[j] * (I - vd)
        nt += 1
        worst = max(worst, tot / omega)
    P(f"  {nt} random chains (m = 1..3 site types, compositions with small fractions, kappa2 in [3e-4, 0.1]): largest (I - v)/omega' = {worst:.4f}  (must be <= 1)")
