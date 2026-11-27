"""w05: exact finite-n sums over joint types -- certified lower bounds for EVERY algorithm at an invariant
instance (the hardest additive instance gamma*, and the flat-histogram instance H), compared with the
single-letter exponent R^max(eps_1).

For a chain with n_j sites of type j, accuracy eps = eps_1 n + eps_0:
  * centre class C: label blocks of sizes round(n_j M*_j(phi)), block types round(n_ju pi_phi)   (the
    generalised-dip profile of the single-letter optimum, rounded to the lattice);
  * Phi(y) = min_{x in C} [ d(y,x) - psi(y) + psi(x) ],  generalised dip (r - Phi)_+  (admissible);
  * r* = the least r with E(r) = ln E_mu exp((r - Phi)_+) > eps  (bisection; E is exact for every r);
  * maxdens = the largest density of {Phi < r*} in a joint-type class (exact).
Then every randomised algorithm that is (eps/2, delta)-correct on the class makes at least
(1 - 2 delta)/maxdens evaluations at the instance (GroupSampling.lean, group_queries_ge); the table reports
theta_n = -ln(maxdens)/n.

usage: python3 w05_finite.py <chain> <e_frac> <n1,n2,...> [eps0]
"""
import math
import sys
import time

import numpy as np

from wlib import *
from wfin import *
from wprimal import dip_profile, alpha, Profile
from wsites import chains

UNITS = {"path(0.8,1.6)": 0.8, "tri(1,1.5,2)": 0.5, "asym": 0.5, "bin(0.3,1)": 1.0}


def setup(ch, nvec, prof, gam, instance, eps, slack_extra=6.0):
    """build the parts and the dip table for the centre class of the (rounded) profile"""
    parts, deltas, lmasses, PCs, info = [], [], [], [], []
    # an upper estimate of the dip parameter: r <= eps + n * alpha_g(C) + const
    for j, s in enumerate(ch.sites):
        nj = int(nvec[j])
        sz = round_counts(nj, prof.P[j])
        p = Part(s, sz, unit=UNITS[s.name])
        ms = [round_counts(int(nu), prof.mu[j][u]) for u, nu in enumerate(sz)]
        PC = sum(ms)
        if instance == "gamma":
            g, lm = p.g_additive(gam[j])
        else:
            g, lm, lZ = p.g_flat()
        dl = g[PC @ p.stride] - g
        parts.append(p)
        deltas.append(dl)
        lmasses.append(lm)
        PCs.append(PC)
        info.append((sz, ms))
    # ln mu_g(C) = sum_j [ln mu_g(T_PC) + ln(|C_j|/|T_PC|)]
    lmuC = 0.0
    for j, p in enumerate(parts):
        sz, ms = info[j]
        lC = sum(float(lmult(np.array([m]))[0]) for m in ms)
        lmuC += lmasses[j][PCs[j] @ p.stride] + lC - p.lTP[PCs[j] @ p.stride]
    r_est = eps - lmuC + slack_extra                     # effect >= mu(C) e^r, so r* <= eps - ln mu(C)
    for j, p in enumerate(parts):
        sz, ms = info[j]
        negd = float(np.max(-deltas[j][p.Pidx]))
        cmax = int(math.ceil((r_est + negd) / p.unit)) + 2
        blks = [p.transport_costs(int(nu), ms[u]) for u, nu in enumerate(sz)]
        p.build(blks, cmax)
    dt = DipTable(parts, deltas, lmasses)
    return dt, parts, info, r_est, lmuC


def certified(dt, eps, r_hi):
    lo, hi = 0.0, r_hi
    assert dt.effect(hi) > eps, "r_est too small"
    for it in range(60):
        mid = 0.5 * (lo + hi)
        if dt.effect(mid) > eps:
            hi = mid
        else:
            lo = mid
    r = hi
    dens, arg, need = dt.maxdens(r)
    return r, dens, arg, dt.effect(r)


if __name__ == "__main__":
    name = sys.argv[1]
    e_frac = float(sys.argv[2])
    ns = [int(x) for x in sys.argv[3].split(",")]
    eps0 = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    t00 = time.time()
    ch = chains()[name]
    E = ch.E()
    e1 = e_frac * E
    R, ts = ch.R(e1, return_t=True)
    prof, phis, Ms, gam = dip_profile(ch, ts)
    # single-letter exponent of the additive instance gamma* (equal to R by construction) and of H (= R)
    print(f"=== w05 finite-n: chain {ch.name}, fractions {ch.lam}; eps = {e_frac} E n + {eps0} (E = {E:.6f}); "
          f"single-letter R^max(eps_1) = {R:.6f} at t* = {ts:.4f} ===")
    for j, s in enumerate(ch.sites):
        print(f"  type {j} ({s.name}): gamma* = {np.round(gam[j], 5)}, labels (vertices) {np.round(phis[j], 3).tolist()} with weights {np.round(prof.P[j], 4)}")
    rows = {"gamma": [], "H": []}
    for n in ns:
        nvec = np.rint(ch.lam * n).astype(int)
        assert nvec.sum() == n, "n must be compatible with the fractions"
        eps = e1 * n + eps0
        for inst in ("gamma", "H"):
            t0 = time.time()
            dt, parts, info, r_est, lmuC = setup(ch, nvec, prof, gam, inst, eps)
            r, dens, arg, eff = certified(dt, eps, r_est)
            th = -math.log(dens) / n
            rows[inst].append((n, th))
            blocks = "; ".join(f"type {j}: sizes {info[j][0].tolist()}, centre counts {[m.tolist() for m in info[j][1]]}" for j in range(len(parts)))
            print(f"  n = {n:4d} [{inst:5s}] eps = {eps:8.3f}: r* = {r:8.3f}, E(r*) = {eff:8.3f}, maxdens = {dens:.4e}  ->  theta_n = {th:.6f}"
                  f"  (R = {R:.6f}; (theta_n - R) n / ln n = {(th - R) * n / math.log(n):+.3f}); densest joint type {arg if not isinstance(arg, tuple) else [a.tolist() for a in arg]}; {time.time()-t0:.1f} s")
            if n == ns[0]:
                print(f"         {blocks}")
    # extrapolation a + b ln n / n from the two largest sizes
    for inst in ("gamma", "H"):
        if len(rows[inst]) >= 2:
            (n1, t1), (n2, t2) = rows[inst][-2], rows[inst][-1]
            b = (t1 - t2) / (math.log(n1) / n1 - math.log(n2) / n2)
            a0 = t2 - b * math.log(n2) / n2
            print(f"  [{inst}] two-point extrapolation theta_n = a + b ln n/n from n = {n1}, {n2}: a = {a0:.6f}, b = {b:.3f}   (R = {R:.6f})")
    print(f"time {time.time()-t00:.0f} s")
