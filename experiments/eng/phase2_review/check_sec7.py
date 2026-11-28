"""Review checks for section 7 of CERTIFIED_INFERENCE.md (propagation of uncertainty in the inputs).

7.1 envelope enclosures; 7.2 enclosures of b, G; 7.3 approximate sampling (ratio bound beta; total
variation); 7.4 evaluation errors of the observables.  Each rule is checked as an inequality on random
instances; for 7.3 the monotonicity in tau that Theorem 5.1 needs is examined for a tau-dependent shift.

Run:  python check_sec7.py
"""
from __future__ import annotations

import numpy as np

import ref

rng = np.random.default_rng(7070)


def inst(N, m):
    pi = rng.dirichlet(np.ones(N) * 2)
    Lw = rng.uniform(0.1, 1.0, N) * (rng.random(N) < 0.85)
    Uw = Lw + rng.uniform(0.0, 4.0, N)
    phi = rng.uniform(-1, 1, (N, m))
    f = rng.uniform(-1, 1, N)
    return pi, Lw, Uw, phi, f


def psi_of(tau, eta, f, phi, hR, Lw, Uw):
    s = f - tau - phi @ eta + hR
    return Uw * np.maximum(s, 0) - Lw * np.maximum(-s, 0), s


def check_71():
    bad = 0
    for _ in range(300):
        N = int(rng.integers(3, 8))
        pi, Lw, Uw, phi, f = inst(N, 1)
        l, u = pi * Lw, pi * Uw
        lm = l * rng.uniform(0.5, 1.0, N)
        up = u * rng.uniform(1.0, 2.0, N)
        w = rng.uniform(l, u)
        y = (w @ phi) / w.sum()
        A, c = ref.box_region(y - 0.05, y + 0.05)
        a = ref.primal_interval(l, u, phi, f, A, c)
        b = ref.primal_interval(lm, up, phi, f, A, c)
        if not (b[0] <= a[0] + 1e-10 and a[1] <= b[1] + 1e-10):
            bad += 1
    print(f"[7.1] interval with (l-, u+) contains the interval with (l, u): violations = {bad}/300")


def check_72():
    worst = -np.inf
    for _ in range(2000):
        N = int(rng.integers(3, 8))
        pi, Lw, Uw, phi, f = inst(N, 1)
        l, u = pi * Lw, pi * Uw
        g = u - l
        G = g.sum()
        q = g / G
        V = np.column_stack([np.ones(N), phi, f])
        b = V.T @ l
        eta = rng.normal(size=1) * 3
        tau = rng.uniform(-1, 1)
        hR = ref.h_box(eta, [-0.2], [0.3])
        lam = np.r_[hR - tau, -eta, 1.0]
        s = V @ lam
        Psi = lam @ b + G * (q @ np.maximum(s, 0))
        bm = b - rng.uniform(0, 0.1, 3)
        bp = b + rng.uniform(0, 0.1, 3)
        Gp = G * rng.uniform(1.0, 1.3)
        bound = np.sum(np.maximum(lam * bm, lam * bp)) + Gp * (q @ np.maximum(s, 0))
        worst = max(worst, Psi - bound)
    print(f"[7.2] Psi <= sum_i max(lam_i b_i-, lam_i b_i+) + G+ E_q s_+ : max of (lhs - rhs) = {worst:.2e} (must be <= 0)")


def check_73():
    worst_beta = -np.inf
    worst_tv = -np.inf
    for _ in range(3000):
        N = int(rng.integers(3, 8))
        pi, Lw, Uw, phi, f = inst(N, 1)
        beta = float(rng.uniform(1.0, 3.0))
        # a sampler law with ratio in [1/beta, beta]
        ratio = np.exp(rng.uniform(-np.log(beta), np.log(beta), N))
        pip = pi * ratio
        Zr = pip.sum()
        pip = pip / Zr
        # after normalisation the ratio pip/pi lies in [min ratio/Zr, max ratio/Zr]; keep only valid cases
        rr = pip / pi
        if rr.max() > beta or rr.min() < 1 / beta:
            continue
        eta = rng.normal(size=1) * 2
        tau = rng.uniform(-1.5, 1.5)
        hR = ref.h_box(eta, [-0.2], [0.3])
        psi, s = psi_of(tau, eta, f, phi, hR, Lw, Uw)
        adj = beta * Uw * np.maximum(s, 0) - (Lw / beta) * np.maximum(-s, 0)
        worst_beta = max(worst_beta, pi @ psi - pip @ adj)
        tv = 0.5 * np.abs(pi - pip).sum()
        worst_tv = max(worst_tv, pi @ psi - (pip @ psi + tv * (psi.max() - psi.min())))
    print(f"[7.3] ratio rule: E_pi psi <= E_pi'[beta U s_+ - (L/beta) s_-]: max of (lhs - rhs) = {worst_beta:.2e} (must be <= 0)")
    print(f"[7.3] TV rule:    E_pi psi <= E_pi' psi + eps_TV (sup psi - inf psi): max of (lhs - rhs) = {worst_tv:.2e} (must be <= 0)")

    # monotonicity in tau of the shifted test function z_tau(y) = psi_tau(y) + eps_TV * (sup_x psi_tau - inf_x psi_tau)
    # (Theorem 5.1 needs every factor 1 - lambda z_tau(Y_j) to be non-decreasing in tau)
    worst_inc = 0.0
    example = None
    for _ in range(2000):
        N = int(rng.integers(2, 7))
        pi, Lw, Uw, phi, f = inst(N, 1)
        eps_tv = float(rng.uniform(0.0, 0.3))
        eta = rng.normal(size=1)
        hR = ref.h_box(eta, [-0.2], [0.3])
        taus = np.linspace(-2, 4, 1201)
        Z = []
        for t in taus:
            psi, _ = psi_of(t, eta, f, phi, hR, Lw, Uw)
            Z.append(psi + eps_tv * (psi.max() - psi.min()))
        Z = np.array(Z)
        inc = np.max(np.diff(Z, axis=0))
        if inc > worst_inc:
            worst_inc = float(inc)
            example = (N, round(eps_tv, 3), np.round(Lw, 3).tolist(), np.round(Uw, 3).tolist())
    print(f"[7.3] tau-dependent TV shift: largest INCREASE of z_tau(y) between neighbouring thresholds (grid step 0.005)"
          f" = {worst_inc:.4f}")
    print(f"      example (N, eps_TV, L, U) = {example}")
    print("      -> with the shift eps_TV*(sup psi_tau - inf psi_tau) evaluated at each tau the test function is NOT monotone in tau;")
    print("         the proof of Theorem 5.1 then does not go through.  A constant shift (a bound on the range over the whole")
    print("         bracket of thresholds) restores it.")

    # necessity of the correction: certificate computed from pi' without any correction
    N = 2
    f = np.array([0.0, 1.0])
    Gam = 20.0
    a = 0.05
    pi = np.array([1 - a, a])
    beta = 2.0
    pip = np.array([1 - a / beta, a / beta])        # the sampler under-represents the up-weighted state
    vplus = Gam * a / (1 + (Gam - 1) * a)
    delta = 0.05
    for n in (200, 1000, 5000):
        counts = rng.multinomial(n, pip, size=20000)
        out = []
        for corr in (False, True):
            Uw = np.full(2, Gam * (beta if corr else 1.0))
            Lw = np.full(2, 1.0 / (beta if corr else 1.0))
            s = f - (vplus - 1e-9)
            psi = Uw * np.maximum(s, 0) - Lw * np.maximum(-s, 0)
            Bcap = Uw[1] * 1.0
            lams = np.array([0.02, 0.05, 0.1, 0.2, 0.4, 0.8]) / Bcap
            v = counts @ np.log(1 - lams[:, None] * psi[None, :]).T
            mx = v.max(axis=1, keepdims=True)
            lw = (mx + np.log(np.mean(np.exp(v - mx), axis=1, keepdims=True)))[:, 0]
            out.append(np.mean(lw >= np.log(1 / delta)))
        print(f"[7.3] sampler off by a factor beta = 2 on the rare state, n = {n:5d}: failure rate without correction"
              f" = {out[0]:.4f}, with (L/beta, beta U) = {out[1]:.4f}   (delta = {delta})")


def check_74():
    bad = 0
    for _ in range(300):
        N = int(rng.integers(3, 8))
        pi, Lw, Uw, phi, f = inst(N, 2)
        l, u = pi * Lw, pi * Uw
        e_phi = rng.uniform(0, 0.1, 2)
        e_f = float(rng.uniform(0, 0.1))
        phit = phi + rng.uniform(-1, 1, (N, 2)) * e_phi
        ft = f + rng.uniform(-1, 1, N) * e_f
        w = rng.uniform(l, u)
        y = (w @ phi) / w.sum()
        A, c = ref.box_region(y - 0.03, y + 0.03)
        true = ref.primal_interval(l, u, phi, f, A, c)
        A2, c2 = ref.box_region(y - 0.03 - e_phi, y + 0.03 + e_phi)
        comp = ref.primal_interval(l, u, phit, ft, A2, c2)
        if comp is None or not (comp[0] - e_f <= true[0] + 1e-10 and true[1] <= comp[1] + e_f + 1e-10):
            bad += 1
    print(f"[7.4] interval from perturbed observables, region enlarged by e_phi, widened by e_f, contains the true one:"
          f" violations = {bad}/300")


if __name__ == "__main__":
    check_71()
    check_72()
    check_73()
    check_74()
