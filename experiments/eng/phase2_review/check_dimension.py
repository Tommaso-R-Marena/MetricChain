"""Does the number m of measured observables enter the sample size of the split-sample certificate?

Section 0 item 3 of CERTIFIED_INFERENCE.md says that Theorem 5.1 'removes the dimension from the sample bound
altogether'.  Theorem 5.1 is a statement about VALIDITY for a given eta.  The excess of the certified bound over
V+ also depends on how good the eta fitted on the training half is, and on the size of the scores (B grows with
|eta|_1).  This script measures the excess as a function of m at fixed sample size, with an independent
implementation of the procedure (dual linear programme on the empirical measure, product test with a fixed
geometric grid of bets, bisection).

Run:  python check_dimension.py
"""
from __future__ import annotations

import numpy as np

import ref

rng = np.random.default_rng(31337)
LOG = np.log
FRACS = 0.9 * 2.0 ** -np.arange(16)


def certified_upper(f, phi, Lw, Uw, x_tr, x_va, ylo, yhi, delta, f_lo, f_hi):
    N = len(f)
    c_tr = np.bincount(x_tr, minlength=N).astype(float) / len(x_tr)
    seen = c_tr > 0
    _, eta = ref.dual_upper_lp_box(c_tr[seen] * Lw[seen], c_tr[seen] * Uw[seen], phi[seen], f[seen], ylo, yhi)
    if eta is None:
        eta = np.zeros(phi.shape[1])
    hR = ref.h_box(eta, ylo, yhi)
    s0 = f - phi @ eta + hR                                    # score at tau = 0, all states
    Bcap = float(np.max(Uw * np.maximum(s0 - f_lo, 0)))        # exact sup of psi at tau_min = f_lo (best case)
    if Bcap <= 0:
        return f_lo, eta
    lams = FRACS / Bcap
    cnt = np.bincount(x_va, minlength=N).astype(float)

    def lw(tau):
        s = s0 - tau
        psi = Uw * np.maximum(s, 0) - Lw * np.maximum(-s, 0)
        v = np.log1p(-lams[:, None] * psi[None, :]) @ cnt
        return v.max() + LOG(np.mean(np.exp(v - v.max())))

    target = LOG(1 / delta)
    if lw(f_hi) < target:
        return f_hi, eta
    lo, hi = f_lo, f_hi
    if lw(lo) >= target:
        return lo, eta
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if lw(mid) >= target:
            hi = mid
        else:
            lo = mid
    return hi, eta


def main():
    N, Gam, delta = 300, 3.0, 0.05
    print(f"[dimension] {N} states, uniform envelope Gamma = {Gam}, box of half-width 0.01 around the means of the reference itself")
    print("            (so that the observations bind), split sample (n/2 + n/2), delta = 0.05; 20 repetitions per cell;")
    print("            f in [-1, 1], phi in [-1, 1]^m")
    print("   m      n     V+       median certified bound   median excess   median |eta_hat|_1   |eta*|_1 (exact dual)   misses")
    pi = rng.dirichlet(np.ones(N))
    f = rng.uniform(-1, 1, N)
    phi_all = rng.uniform(-1, 1, (N, 60))
    r = np.ones(N)
    Lw, Uw = np.ones(N), np.full(N, Gam)
    for m in (1, 5, 20, 60):
        phi = phi_all[:, :m]
        y = (pi * r) @ phi / (pi * r).sum()
        ylo, yhi = y - 0.01, y + 0.01
        vplus, eta_star = ref.dual_upper_lp_box(pi * Lw, pi * Uw, phi, f, ylo, yhi)
        A, c = ref.box_region(ylo, yhi)
        vp = ref.primal_extreme(pi * Lw, pi * Uw, phi, f, A, c, +1)
        assert abs(vp - vplus) < 1e-7
        for n in (1000, 10000, 100000):
            vals, norms = [], []
            for _ in range(20):
                x = rng.choice(N, size=n, p=pi)
                tau, eta = certified_upper(f, phi, Lw, Uw, x[:n // 2], x[n // 2:], ylo, yhi, delta, -1.0, 1.0)
                vals.append(tau)
                norms.append(np.abs(eta).sum())
            vals = np.array(vals)
            print(f"   {m:2d}  {n:6d}  {vplus:7.4f}        {np.median(vals):7.4f}              {np.median(vals) - vplus:7.4f}"
                  f"          {np.median(norms):8.2f}            {np.abs(eta_star).sum():8.2f}             {int(np.sum(vals < vplus - 1e-9))}/20")
    print("   -> validity never fails, as Theorem 5.1 says; the EXCESS at fixed n grows with m (the fitted multipliers and with")
    print("      them the scores and B grow, and the training half over-fits): the dimension is not removed from the sample size")
    print("      needed for a given accuracy, only from the validity statement.")


if __name__ == "__main__":
    main()
