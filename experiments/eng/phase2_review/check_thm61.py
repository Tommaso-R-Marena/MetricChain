"""Review checks for Theorem 6.1 of CERTIFIED_INFERENCE.md (lower bound proportional to Gamma).

1. All the arithmetic of parts (a) and (b) on grids of (Gamma, theta), with the instance values of V+
   recomputed by brute force.
2. The access model: on the instances of the proof, one evaluation of the envelope (or of the
   unnormalised reference weight) reveals the hidden parameter.
3. The bound is a statement about the sampling law: with draws from the extremal (tilted) law of the
   SAME instance the same certificate has no factor Gamma.

Run:  python check_thm61.py
"""
from __future__ import annotations

import numpy as np

import ref

rng = np.random.default_rng(6161)
LOG = np.log


def kl(p, q):
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    m = p > 0
    return float(np.sum(p[m] * LOG(p[m] / q[m])))


def chi2(p, q):
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    return float(np.sum((p - q) ** 2 / q))


def part_a():
    worst = dict(gap_ratio=np.inf, chi_ratio=0.0, formula=0.0, kl_over_chi=0.0)
    for Gam in np.concatenate([np.linspace(4, 10, 25), np.logspace(1, 7, 61)]):
        for theta in np.linspace(1e-3, 1.0, 200):
            a0, a1 = 1 / Gam, (1 + theta) / Gam
            V = lambda a: ref.threshold_max(np.array([1 - a, a]), Gam * np.array([1 - a, a]), np.array([0.0, 1.0]))
            closed = lambda a: Gam * a / (1 + (Gam - 1) * a)
            worst["formula"] = max(worst["formula"], abs(V(a0) - closed(a0)), abs(V(a1) - closed(a1)))
            gap = closed(a1) - closed(a0)
            gap_formula = Gam ** 2 * theta / ((2 * Gam - 1) * (2 * Gam - 1 + theta * (Gam - 1)))
            worst["formula"] = max(worst["formula"], abs(gap - gap_formula))
            worst["gap_ratio"] = min(worst["gap_ratio"], gap / (theta / 6))
            c2 = chi2([1 - a0, a0], [1 - a1, a1])
            c2_formula = (theta / Gam) ** 2 / (a1 * (1 - a1))
            worst["formula"] = max(worst["formula"], abs(c2 - c2_formula) / c2)
            worst["chi_ratio"] = max(worst["chi_ratio"], c2 / (2 * theta ** 2 / Gam))
            worst["kl_over_chi"] = max(worst["kl_over_chi"], kl([1 - a0, a0], [1 - a1, a1]) / c2)
    print("[6.1 a] Gamma in [4, 1e7], theta in (0, 1]:")
    print(f"   formulas (V+, gap, chi^2) against brute force: max discrepancy {worst['formula']:.2e}")
    print(f"   min of gap / (theta/6)             = {worst['gap_ratio']:.4f}   (claim: >= 1)")
    print(f"   max of chi^2 / (2 theta^2 / Gamma) = {worst['chi_ratio']:.4f}   (claim: <= 1)")
    print(f"   max of KL / chi^2                  = {worst['kl_over_chi']:.4f}   (claim: <= 1)")


def part_b():
    worst = dict(gap1=np.inf, gap2=np.inf, chi1=0.0, chi2=0.0, formula=0.0, b=0.0, opt=0.0, kl=0.0)
    f = np.array([0.0, 0.5, 1.0])
    for Gam in np.concatenate([np.linspace(4, 10, 25), np.logspace(1, 7, 61)]):
        m = 1 / Gam
        pi_t = lambda t: np.array([1 - 2 * m + t, 2 * (m - t), t])
        closed = lambda t: 1 / (1 + (Gam - 1) * (2 / Gam - t))
        for theta in np.linspace(1e-3, 1.0, 120):
            t0 = 1 / (4 * Gam)
            t1 = (1 + theta) * t0
            for t in (t0, t1, 0.0, m / 2):
                p = pi_t(t)
                assert np.all(p >= 0) and abs(p.sum() - 1) < 1e-12
                # S3's inputs with l = pi_t, u = Gamma pi_t:  b = (sum l, sum l f), G, Z_l, q
                b = np.array([p.sum(), p @ f])
                worst["b"] = max(worst["b"], abs(b[0] - 1), abs(b[1] - m))
                V = ref.threshold_max(p, Gam * p, f)
                worst["formula"] = max(worst["formula"], abs(V - closed(t)))
                worst["opt"] = max(worst["opt"], V - 0.5)            # the optimal threshold is <= 1/2
            gap = closed(t1) - closed(t0)
            worst["gap1"] = min(worst["gap1"], gap / ((Gam - 1) * theta * t0 / 9))
            worst["gap2"] = min(worst["gap2"], gap / (theta / 48))
            c2 = chi2(pi_t(t0), pi_t(t1))
            worst["chi1"] = max(worst["chi1"], c2 / (theta ** 2 * t0 * (2 + 2 * t0)))
            worst["chi2"] = max(worst["chi2"], c2 / (theta ** 2 / Gam))
            worst["kl"] = max(worst["kl"], kl(pi_t(t0), pi_t(t1)) / c2)
    print("[6.1 b] Gamma in [4, 1e7], theta in (0, 1], t0 = 1/(4 Gamma), t1 = (1+theta) t0:")
    print(f"   b = (1, 1/Gamma) for every t: max deviation {worst['b']:.2e};  G = Gamma-1, Z_l = 1, q = pi_t by construction")
    print(f"   V+(t) = 1/(1+(Gamma-1)(2/Gamma - t)) against threshold enumeration: max discrepancy {worst['formula']:.2e};"
          f" max of V+ - 1/2 = {worst['opt']:.3f} (<= 0: both upper states are up-weighted)")
    print(f"   min of gap / ((Gamma-1) theta t0 / 9) = {worst['gap1']:.4f}   (claim: >= 1)")
    print(f"   min of gap / (theta/48)               = {worst['gap2']:.4f}   (claim: >= 1)")
    print(f"   max of chi^2 / (theta^2 t0 (2+2 t0))  = {worst['chi1']:.4f}   (claim: <= 1)")
    print(f"   max of chi^2 / (theta^2 / Gamma)      = {worst['chi2']:.4f}   (claim: <= 1)")
    print(f"   max of KL / chi^2                     = {worst['kl']:.4f}")


def access_model():
    print("[6.1 access] what one evaluation of the inputs reveals on the instances of the proof")
    Gam = 100.0
    m = 1 / Gam
    for t in (1 / (4 * Gam), 1.5 / (4 * Gam)):
        l = np.array([1 - 2 * m + t, 2 * (m - t), t])
        print(f"   (b) t = {t:.6f}: S3's input l(x) = pi_t(x) at the state with f = 1 is {l[2]:.6f} = t;"
              f" V+(t) = {1 / (1 + (Gam - 1) * (2 / Gam - l[2])):.6f} follows with no draw at all")
    for a in (1 / Gam, 1.5 / Gam):
        w0 = np.array([1 - a, a]) * 7.3                 # unnormalised reference weight, any constant
        print(f"   (a) a = {a:.4f}: w0(1)/(w0(0)+w0(1)) = {w0[1] / w0.sum():.4f} = a from two evaluations of the unnormalised reference")
    print("   -> the theorem holds for procedures whose only information about the instance is the n draws and the values of")
    print("      f, L, U at them; this has to be said, or each atom replaced by a cell of equal-weight configurations of unknown size.")


def wealth_tau_hat(counts, psi_fun, lams, delta, tau_lo, tau_hi, iters=50):
    """tau_hat = inf{tau >= tau_lo : W(tau) >= 1/delta} by bisection (upper end); inf if never."""
    def lw(tau):
        psi = psi_fun(tau)
        v = counts @ LOG(1 - lams[:, None] * psi[None, :]).T
        mx = v.max()
        return mx + LOG(np.mean(np.exp(v - mx)))
    if lw(tau_hi) < LOG(1 / delta):
        return np.inf
    if lw(tau_lo) >= LOG(1 / delta):
        return tau_lo
    lo, hi = tau_lo, tau_hi
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if lw(mid) >= LOG(1 / delta):
            hi = mid
        else:
            lo = mid
    return hi


def tilted_law():
    print("[6.1 tilt] instance of part (a) (two states, pi(1) = 1/Gamma, f = x): the same certificate E_pi psi <= 0")
    print("           tested (i) with n draws from pi, (ii) with n draws from the tilted law p0 ~ pi * omega,")
    print("           omega = (1, Gamma), using psi/omega = f - tau (Theorem 5.1 with reference p0, envelope (L/omega, U/omega)).")
    print("           delta = 0.05, bets (0.02, 0.05, 0.1, 0.2, 0.4, 0.8)/B, tau_min = 0; n_alpha = least n with median excess <= 0.05")
    delta = 0.05
    fr = np.array([0.02, 0.05, 0.1, 0.2, 0.4, 0.8])
    print("   Gamma     V+      n_alpha(reference)  misses   n_alpha(tilted)  misses    lower bound Gamma ln(1/4d)/(72 a^2)")
    for Gam in (10.0, 100.0, 1000.0, 10000.0):
        a = 1 / Gam
        vplus = Gam * a / (1 + (Gam - 1) * a)
        alpha = 0.05
        out = []
        for mode in ("ref", "tilt"):
            if mode == "ref":
                p = np.array([1 - a, a])
                psi_fun = lambda tau: np.array([-tau, Gam * (1 - tau)])
                Bcap = Gam
            else:
                p = np.array([1 - vplus, vplus])
                psi_fun = lambda tau: np.array([-tau, 1 - tau])
                Bcap = 1.0
            lams = fr / Bcap
            def med_excess(n, reps=300):
                cs = rng.multinomial(n, p, size=reps)
                th = np.array([wealth_tau_hat(c, psi_fun, lams, delta, 0.0, 1.0) for c in cs])
                th = np.minimum(th, 1.0)
                return np.median(th) - vplus, np.mean(th < vplus)
            n = 8
            while med_excess(n)[0] > alpha:
                n *= 2
            lo, hi = n // 2, n
            while hi - lo > max(1, lo // 20):
                mid = (lo + hi) // 2
                if med_excess(mid)[0] <= alpha:
                    hi = mid
                else:
                    lo = mid
            miss = med_excess(hi, reps=2000)[1]
            out.append((hi, miss))
        lb = Gam * LOG(1 / (4 * delta)) / (72 * alpha ** 2)
        print(f"   {Gam:7.0f}  {vplus:.4f}   {out[0][0]:10d}        {out[0][1]:.4f}   {out[1][0]:10d}     {out[1][1]:.4f}       {lb:12.0f}")
    print("   -> with reference draws n grows in proportion to Gamma (consistent with Theorem 6.1 and Proposition 5.2);")
    print("      with draws from the tilted law it does not depend on Gamma.  Theorem 6.1 is a statement about sampling from")
    print("      pi or q, not about the class.")

    # a multi-state instance with one observable: pilot (tau0, eta) = exact optimum + 0.02; tilt by the extremal weights at the pilot
    print("[6.1 tilt] 8 states (4 bulk states with f <= 0.3, 4 rare states with f >= 0.7 of total reference mass 2/Gamma),")
    print("           m = 1, uniform envelope; pilot threshold tau0 = V+ + 0.02 with the optimal eta; single test of")
    print("           E psi_{tau0} <= 0 with n draws: first-order cost 2 ln(1/delta) E z^2/(E z)^2 and simulated power,")
    print("           z = psi under pi (reference) and z = psi/omega = s under p0 ~ pi*omega (tilted, omega = U on {s>0}, L elsewhere)")
    N = 8
    f = np.r_[rng.uniform(0, 0.3, 4), rng.uniform(0.7, 1.0, 4)]
    phi = rng.uniform(-1, 1, (N, 1))
    bulk = rng.dirichlet(np.ones(4) * 2)
    rare = rng.dirichlet(np.ones(4) * 2)
    print("   Gamma   V+      margin E z (ref, tilted)   cost index (ref, tilted)      n      power(ref)  power(tilted)"
          "   false certification at V+ - 0.02 (ref, tilted)")
    for Gam in (10.0, 100.0, 1000.0):
        pi = np.r_[bulk * (1 - 2 / Gam), rare * (2 / Gam)]
        Lw, Uw = np.ones(N), np.full(N, Gam)
        r = np.r_[np.ones(4), np.full(4, 0.5 * Gam)]
        y = (pi * r) @ phi / (pi * r).sum()
        ylo, yhi = y - 0.03, y + 0.03
        vplus, eta = ref.dual_upper_lp_box(pi * Lw, pi * Uw, phi, f, ylo, yhi)
        hR = ref.h_box(eta, ylo, yhi)
        def psi_at(tau):
            s = f - tau - phi @ eta + hR
            return Uw * np.maximum(s, 0) - Lw * np.maximum(-s, 0), s
        psi, s = psi_at(vplus + 0.02)
        omega = np.where(s > 0, Uw, Lw)
        p0 = pi * omega / (pi * omega).sum()
        mu_r, mu_t = float(pi @ psi), float(p0 @ s)
        ci_r = 2 * LOG(1 / delta) * float(pi @ psi ** 2) / mu_r ** 2
        ci_t = 2 * LOG(1 / delta) * float(p0 @ s ** 2) / mu_t ** 2
        print(f"   {Gam:6.0f}  {vplus:.4f}   {mu_r:9.5f}, {mu_t:9.5f}       {ci_r:10.0f}, {ci_t:8.0f}")
        for n in (200, 2000, 20000):
            res = {}
            for tau, key in ((vplus + 0.02, "power"), (vplus - 0.02, "false")):
                psi, s = psi_at(tau)
                omega = np.where(s > 0, Uw, Lw)
                p0 = pi * omega / (pi * omega).sum()
                for mode in ("ref", "tilt"):
                    if mode == "ref":
                        p, z = pi, psi
                    else:
                        p, z = p0, psi / omega          # = s
                    Bcap = max(z.max(), 1e-12)
                    lams = fr / Bcap
                    cs = rng.multinomial(n, p, size=4000)
                    v = cs @ LOG(1 - lams[:, None] * z[None, :]).T
                    mx = v.max(axis=1, keepdims=True)
                    lw = (mx + LOG(np.mean(np.exp(v - mx), axis=1, keepdims=True)))[:, 0]
                    res[(key, mode)] = float(np.mean(lw >= LOG(1 / delta)))
            print(f"   {'':6s}  {'':6s}   {'':52s} {n:6d}      {res[('power', 'ref')]:.3f}       {res[('power', 'tilt')]:.3f}"
                  f"            {res[('false', 'ref')]:.4f}, {res[('false', 'tilt')]:.4f}")
    print("   -> margin under the tilted law is at least the excess (0.02) and |z| <= S: cost of order S^2 ln(1/delta)/alpha^2, no Gamma.")


def instance_94():
    """Section 9.4 says of the uniform cube with target x_1 and the box of ratio Gamma = e^{un}:
    'by Theorem 6.1 any sampled certificate over that box needs e^{un} draws'.  Theorem 6.1 is a worst case over
    instances of ratio Gamma (its hard instance has pi(f = 1) = 1/Gamma); here pi(x_1 = 1) = 1/2."""
    print("[9.4 / 6.1] uniform cube, f = x_1, box of ratio Gamma = e^{un}: V+ = 1 - 1/(1+Gamma).  Reference draws, Theorem 5.1 with")
    print("            tau_min = 1 - 2/(1+Gamma) (so B < 2), bets (0.1, 0.2, 0.4, 0.8)/B, delta = 0.05; certify tau = V+ + c/(1+Gamma), c = 0.5")
    print("   un     Gamma        n      P(certified)    P(certified at V+ - c/(1+Gamma))  [must be <= delta]")
    delta = 0.05
    c = 0.5
    for un in (5.0, 10.0, 20.0, 30.0):
        Gam = np.exp(un)
        gap = 1.0 / (1.0 + Gam)                       # 1 - V+
        one_minus_tau_min = 2 * gap
        Bcap = Gam * one_minus_tau_min
        lams = np.array([0.1, 0.2, 0.4, 0.8]) / Bcap
        for n in (50, 100, 200, 400):
            k = rng.binomial(n, 0.5, size=20000)      # draws with x_1 = 1
            res = []
            for sign in (+1, -1):
                one_minus_tau = gap * (1 - sign * c)  # tau = V+ + sign*c*gap
                psiA = Gam * one_minus_tau
                psiAc = -(1 - one_minus_tau)
                v = np.outer(k, np.log1p(-lams * psiA)) + np.outer(n - k, np.log1p(-lams * psiAc))
                mx = v.max(axis=1, keepdims=True)
                lw = (mx + LOG(np.mean(np.exp(v - mx), axis=1, keepdims=True)))[:, 0]
                res.append(np.mean(lw >= LOG(1 / delta)))
            print(f"   {un:4.0f}  {Gam:10.3g}  {n:5d}      {res[0]:.3f}            {res[1]:.4f}")
    print("   -> a few hundred reference draws certify a bound within half of the (exponentially small) distance between V+ and the")
    print("      trivial bound, for every system size.  The interval of this box is useless because it is within e^{-un} of trivial,")
    print("      not because certifying it is expensive; Theorem 6.1 does not apply to a given instance.")


if __name__ == "__main__":
    part_a()
    part_b()
    access_model()
    instance_94()
    tilted_law()
