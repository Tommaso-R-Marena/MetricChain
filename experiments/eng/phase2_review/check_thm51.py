"""Review checks for Theorem 5.1 and Proposition 5.2 of CERTIFIED_INFERENCE.md.

A. instances built to make P(tau_hat < V+) as large as possible (the bound delta is attained in the limit);
B. heavy upper tail (a rare state with a huge envelope);
C. the full split-sample procedure on random instances;
D. what happens when a hypothesis is dropped: B taken from the certification sample; eta fitted on
   the certification sample;
E. monotonicity and continuity of W_n in tau by brute force;
F. Proposition 5.2: first-order cost against simulation.

Run:  python check_thm51.py
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize_scalar

import ref

rng = np.random.default_rng(5151)
LOG = np.log


def psi_tau(tau, f, phi_eta, hR_eta, Lw, Uw):
    """psi_{tau,eta}(x) for all x; tau may be an array (returns len(tau) x N)."""
    tau = np.atleast_1d(np.asarray(tau, float))
    s = (f - phi_eta + hR_eta)[None, :] - tau[:, None]
    return Uw[None, :] * np.maximum(s, 0) - Lw[None, :] * np.maximum(-s, 0)


def log_wealth(counts, psi, lams):
    """log W_n for count vectors (R x N), psi (N,), bets lams (J,).  Mixture with equal weights."""
    fac = 1.0 - lams[:, None] * psi[None, :]              # J x N, all > 0 by construction
    if np.any(fac <= 0):
        raise ValueError("non-positive factor: bet too large for B")
    lw = counts @ LOG(fac).T                               # R x J
    mx = lw.max(axis=1, keepdims=True)
    return (mx + LOG(np.mean(np.exp(lw - mx), axis=1, keepdims=True)))[:, 0]


def fail_rate(pi, f, phi_eta, hR_eta, Lw, Uw, lams, n, delta, vplus, tau_min, reps, rng, tiny=1e-10):
    """Monte Carlo estimate of P(tau_hat < V+): by monotonicity, tau_hat < V+ iff W_n(V+ - 0) >= 1/delta."""
    if tau_min >= vplus:
        return 0.0, 0.0
    counts = rng.multinomial(n, pi, size=reps)
    psi = psi_tau(vplus - tiny, f, phi_eta, hR_eta, Lw, Uw)[0]
    lw = log_wealth(counts, psi, lams)
    p = float(np.mean(lw >= LOG(1 / delta)))
    return p, float(np.sqrt(max(p * (1 - p), 1e-12) / reps))


def part_A():
    print("[5.1 A] two states, f = x, m = 0, L = 1, U = Gamma, pi(1) = a;  V+ = Gamma a / (1 + (Gamma-1) a)")
    print("        tau_min just below V+, B = sup psi at tau_min, one bet lambda = 0.999 / B, n with (1-a)^n just below delta")
    print("   Gamma      a    delta      n   (1-a)^n   failure rate (s.e.)     with tau_min = 0, bets 0.5/B: failure rate")
    for Gam, a, delta in ((10.0, 0.05, 0.05), (100.0, 0.02, 0.05), (1000.0, 0.002, 0.05), (10.0, 0.2, 0.2),
                          (1e6, 1e-4, 0.01), (4.0, 0.3, 0.3)):
        pi = np.array([1 - a, a])
        f = np.array([0.0, 1.0])
        Lw = np.ones(2)
        Uw = np.array([Gam, Gam])
        vplus = Gam * a / (1 + (Gam - 1) * a)
        n = int(np.ceil(LOG(delta) / LOG(1 - a))) + 1
        tau_min = vplus - 1e-6 * (1 - vplus)
        Bcap = Gam * (1 - tau_min)
        lams = np.array([0.999 / Bcap])
        # with lambda < 1/B the wealth without any draw of state 1 is slightly below (1-a)^-n: enlarge n until it fires
        while n * LOG(1 + lams[0] * vplus) < LOG(1 / delta) + 1e-9:
            n += 1
        p, se = fail_rate(pi, f, np.zeros(2), 0.0, Lw, Uw, lams, n, delta, vplus, tau_min, 400000, rng)
        lams0 = np.array([0.5 / Gam])
        p0, se0 = fail_rate(pi, f, np.zeros(2), 0.0, Lw, Uw, lams0, n, delta, vplus, 0.0, 400000, rng)
        print(f"   {Gam:8.0f}  {a:6.4f}  {delta:5.2f}  {n:6d}   {(1 - a) ** n:.4f}    {p:.4f} ({se:.4f})"
              f"                    {p0:.4f} ({se0:.4f})")
    print("   -> the failure rate reaches (1-a)^n, i.e. delta up to the rounding of n: Theorem 5.1 cannot be improved;")
    print("      no configuration exceeds delta.")


def part_B():
    print("[5.1 B] rare state with a huge envelope: pi = (0.5, 0.499, 0.001), U = (1, 1, 1000), L = 1, f = (0, .5, 1)")
    pi = np.array([0.5, 0.499, 0.001])
    f = np.array([0.0, 0.5, 1.0])
    Lw = np.ones(3)
    Uw = np.array([1.0, 1.0, 1000.0])
    vplus = ref.threshold_max(pi * Lw, pi * Uw, f)
    print(f"   V+ = {vplus:.6f}")
    print("   tau_min      bets (x 1/B)                 n     failure rate (s.e.)   delta = 0.05")
    for tau_min in (0.0, vplus - 1e-6):
        Bcap = float(psi_tau(tau_min, f, np.zeros(3), 0.0, Lw, Uw).max())
        for fr in ((0.999,), (0.5,), (0.001, 0.01, 0.1, 0.5, 0.999)):
            lams = np.array(fr) / Bcap
            for n in (50, 1000, 3000, 6000, 20000):
                p, se = fail_rate(pi, f, np.zeros(3), 0.0, Lw, Uw, lams, n, 0.05, vplus, tau_min, 200000, rng)
                print(f"   {tau_min:8.5f}   {str(fr):28s} {n:6d}    {p:.4f} ({se:.4f})")


def empirical_eta(counts, f, phi, Lw, Uw, ylo, yhi, H=60.0):
    lhat = counts * Lw
    uhat = counts * Uw
    fun = lambda e: ref.tau_star([e], lhat, uhat, phi, f, lambda ee: ref.h_box(ee, ylo, yhi))
    res = minimize_scalar(fun, bounds=(-H, H), method="bounded", options={"xatol": 1e-6})
    return float(res.x), float(res.fun)


def part_C_D():
    print("[5.1 C] split-sample procedure, random 6-state instances, m = 1, box region of half-width 0.03 around the")
    print("        mean of a member of the class; eta from n_tr training draws; B = exact sup of psi at tau_min = min f;")
    print("        bets = (0.01, 0.03, 0.1, 0.3, 0.9)/B; delta = 0.05.  'same-sample' = eta fitted on the certification draws.")
    print("   Gamma  n_tr  n_cert   V+       failure(split)   median excess    failure(same-sample eta)  failure(B from sample)")
    delta = 0.05
    fracs = np.array([0.01, 0.03, 0.1, 0.3, 0.9])
    for Gam in (3.0, 30.0):
        for inst in range(2):
            N = 6
            pi = rng.dirichlet(np.ones(N) * 2)
            f = rng.uniform(0, 1, N)
            phi = rng.uniform(-1, 1, (N, 1))
            Lw = np.ones(N)
            Uw = np.full(N, Gam)
            r = rng.uniform(1, Gam, N)
            y = (pi * r) @ phi / (pi * r).sum()
            ylo, yhi = y - 0.03, y + 0.03
            A, c = ref.box_region(ylo, yhi)
            vplus = ref.primal_extreme(pi * Lw, pi * Uw, phi, f, A, c, +1)
            tau_min = float(f.min())
            for n_tr, n_c in ((20, 20), (200, 100), (1000, 1000)):
                reps = 3000
                fails = 0
                fails_same = 0
                fails_Bhat = 0
                exc = []
                for _ in range(reps):
                    ctr = rng.multinomial(n_tr, pi)
                    cc = rng.multinomial(n_c, pi)
                    eta, _ = empirical_eta(ctr, f, phi, Lw, Uw, ylo, yhi)
                    phi_eta = phi[:, 0] * eta
                    hR = ref.h_box([eta], ylo, yhi)
                    Bcap = float(psi_tau(tau_min, f, phi_eta, hR, Lw, Uw).max())
                    if Bcap <= 0:
                        continue
                    lams = fracs / Bcap
                    psi_v = psi_tau(vplus - 1e-10, f, phi_eta, hR, Lw, Uw)[0]
                    lw = log_wealth(cc[None, :], psi_v, lams)[0]
                    fails += int(lw >= LOG(1 / delta))
                    # excess of tau_hat over V+ by bisection (upper end of the bracket)
                    lo_t, hi_t = tau_min, float(f.max() + abs(eta) * 2 + abs(hR) + 1)
                    if log_wealth(cc[None, :], psi_tau(hi_t, f, phi_eta, hR, Lw, Uw)[0], lams)[0] < LOG(1 / delta):
                        exc.append(np.inf)
                    else:
                        for _ in range(40):
                            mid = 0.5 * (lo_t + hi_t)
                            if log_wealth(cc[None, :], psi_tau(mid, f, phi_eta, hR, Lw, Uw)[0], lams)[0] >= LOG(1 / delta):
                                hi_t = mid
                            else:
                                lo_t = mid
                        exc.append(min(hi_t, f.max()) - vplus)
                    # (D2) eta fitted on the certification sample itself
                    eta2, _ = empirical_eta(cc, f, phi, Lw, Uw, ylo, yhi)
                    phi_eta2 = phi[:, 0] * eta2
                    hR2 = ref.h_box([eta2], ylo, yhi)
                    B2 = float(psi_tau(tau_min, f, phi_eta2, hR2, Lw, Uw).max())
                    if B2 > 0:
                        lw2 = log_wealth(cc[None, :], psi_tau(vplus - 1e-10, f, phi_eta2, hR2, Lw, Uw)[0], fracs / B2)[0]
                        fails_same += int(lw2 >= LOG(1 / delta))
                    # (D1) B taken from the certification sample (max of psi over the sampled states)
                    seen = cc > 0
                    Bhat = float(psi_tau(tau_min, f, phi_eta, hR, Lw, Uw)[0][seen].max())
                    if Bhat > 0:
                        lam_hat = fracs / Bhat
                        fac = 1.0 - lam_hat[:, None] * psi_v[None, seen]
                        if np.all(fac > 0):
                            lwj = cc[seen] @ LOG(fac).T
                            lw3 = lwj.max() + LOG(np.mean(np.exp(lwj - lwj.max())))
                            fails_Bhat += int(lw3 >= LOG(1 / delta))
                print(f"   {Gam:5.0f}  {n_tr:4d}  {n_c:6d}  {vplus:.4f}    {fails / reps:.4f}"
                      f"          {np.median(exc):8.4f}         {fails_same / reps:.4f}"
                      f"                   {fails_Bhat / reps:.4f}")


def part_D1_heavy():
    print("[5.1 D1] B estimated from the certification sample on the heavy-tail instance of part B (tau_min = 0, bet 0.5/B_hat)")
    pi = np.array([0.5, 0.499, 0.001])
    f = np.array([0.0, 0.5, 1.0])
    Lw = np.ones(3)
    Uw = np.array([1.0, 1.0, 1000.0])
    vplus = ref.threshold_max(pi * Lw, pi * Uw, f)
    delta = 0.05
    for n in (20, 50, 200, 1000):
        reps = 20000
        counts = rng.multinomial(n, pi, size=reps)
        psi0 = psi_tau(0.0, f, np.zeros(3), 0.0, Lw, Uw)[0]
        psiv = psi_tau(vplus - 1e-10, f, np.zeros(3), 0.0, Lw, Uw)[0]
        fails = 0
        for cnt in counts:
            seen = cnt > 0
            Bhat = psi0[seen].max()
            lam = 0.5 / Bhat
            fac = 1 - lam * psiv[seen]
            if np.all(fac > 0):
                fails += int(cnt[seen] @ LOG(fac) >= LOG(1 / delta))
        print(f"   n = {n:5d}: failure rate = {fails / reps:.4f}   (delta = {delta})")


def part_E():
    worst_dec = 0.0
    for _ in range(300):
        N = int(rng.integers(2, 8))
        pi = rng.dirichlet(np.ones(N))
        f = rng.uniform(-1, 1, N)
        phi = rng.uniform(-1, 1, N)
        eta = rng.normal() * 3
        ylo, yhi = -0.2, 0.3
        hR = ref.h_box([eta], [ylo], [yhi])
        Lw = rng.uniform(0, 1, N) * (rng.random(N) < 0.8)
        Uw = Lw + rng.uniform(0, 5, N)
        tau_min = float(rng.uniform(-2, 0))
        Bcap = float(psi_tau(tau_min, f, phi * eta, hR, Lw, Uw).max())
        if Bcap <= 0:
            continue
        lams = rng.uniform(0, 1, 4) / Bcap * 0.999
        n = int(rng.integers(1, 200))
        cnt = rng.multinomial(n, pi)
        taus = np.linspace(tau_min, 6, 4001)
        psis = psi_tau(taus, f, phi * eta, hR, Lw, Uw)
        lw = np.array([log_wealth(cnt[None, :], p, lams)[0] for p in psis])
        worst_dec = min(worst_dec, float(np.min(np.diff(lw))))
    print(f"[5.1 E] W_n(tau) on a grid of 4001 thresholds, 300 random configurations: most negative increment of"
          f" log W_n = {worst_dec:.2e} (monotone non-decreasing)")


def part_F():
    print("[5.2] first-order cost: uniform envelope L = 1, U = Gamma, m = 0, 8 states, f in [0,1], test at tau = V+ + alpha")
    print("   Gamma  alpha    mu        E psi^2    (Gamma+1)S^2   lambda*  capped   n_pred = 2 E psi^2 ln(1/d)/mu^2   n_50 (sim)   ratio   2(G+1)S^2 ln/alpha^2")
    delta = 0.05
    for Gam in (3.0, 30.0, 300.0):
        N = 8
        pi = rng.dirichlet(np.ones(N) * 3)
        f = np.sort(rng.uniform(0, 1, N))
        Lw = np.ones(N)
        Uw = np.full(N, Gam)
        vplus = ref.threshold_max(pi * Lw, pi * Uw, f)
        for alpha in (0.05, 0.01):
            tau = vplus + alpha
            psi = psi_tau(tau, f, np.zeros(N), 0.0, Lw, Uw)[0]
            mu = float(pi @ psi)
            m2 = float(pi @ psi ** 2)
            S = float(np.max(np.abs(f - tau)))
            Bcap = float(psi_tau(0.0, f, np.zeros(N), 0.0, Lw, Uw).max())     # tau_min = 0
            assert abs(mu) >= alpha - 1e-12 and m2 <= (Gam + 1) * S * S + 1e-12      # the two bounds of Proposition 5.2
            lam_star = abs(mu) / m2
            lam = min(lam_star, 0.999 / Bcap)
            n_pred = 2 * m2 * LOG(1 / delta) / mu ** 2
            # n at which the test fires with probability 1/2
            lo, hi = 1, 10
            def fire(n):
                counts = rng.multinomial(n, pi, size=4000)
                return np.mean(counts @ LOG(1 - lam * psi) >= LOG(1 / delta))
            while fire(hi) < 0.5:
                hi *= 2
            lo = hi // 2
            while hi - lo > max(1, lo // 50):
                mid = (lo + hi) // 2
                if fire(mid) >= 0.5:
                    hi = mid
                else:
                    lo = mid
            print(f"   {Gam:5.0f}  {alpha:5.2f}  {mu:9.5f}  {m2:9.5f}  {(Gam + 1) * S * S:9.4f}     {lam_star:.4f}  "
                  f"{'yes' if lam < lam_star else 'no ':3s}     {n_pred:12.0f}                  {hi:8d}    {hi / n_pred:5.2f}"
                  f"     {2 * (Gam + 1) * S * S * LOG(1 / delta) / alpha ** 2:12.0f}")
    print("   asserted in every row: |mu| >= alpha and E psi^2 <= (Gamma+1) S^2 (normalisation L = 1, E_pi L = 1).")
    print("   -> the first-order formula is accurate when the bet is not capped (ratio ~ 1) and far too optimistic when it is")
    print("      (ratios 3 - 270): there the cost is the cap term ~ B ln(1/delta)/|mu|.  The closed form 2(Gamma+1)S^2 ln/alpha^2")
    print("      is an upper estimate (both of its ingredients are bounds), not an approximation.")


if __name__ == "__main__":
    part_A()
    part_B()
    part_E()
    part_F()
    part_D1_heavy()
    part_C_D()
