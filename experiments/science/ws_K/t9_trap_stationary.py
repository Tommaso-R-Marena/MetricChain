"""
T9 — numerical reading of the machine-checked `trap_survival` / `trap_certificate`
(KineticsCertificates.lean): for ANY stochastic kernel P with stationary law pi (reversible or not)
whose steps are single-site moves,

    P_{pi_A}(tau_{A^c} > T)  >=  1 - T * Q(A^c, A) / pi(A)  >=  1 - T * pi(wall) / pi(A),

wall = outer boundary of A.  Tested for (a) discrete-time Metropolis with uniform (site,state) proposals,
(b) a NON-REVERSIBLE single-site kernel with the same stationary law (Metropolis plus divergence-free
circulations around 4-cycles), (c) heat-bath (Glauber) with random site.

Run:  OMP_NUM_THREADS=1 python3 t9_trap_stationary.py
"""
import numpy as np
from kcore import (Space, random_pairwise, pairwise_energy, local_minima, barrier_from,
                   component_below, outer_boundary, generator, gibbs)

rng = np.random.default_rng(23)


def exit_target(S, E, a):
    Ba = barrier_from(S, E, a)
    lower = np.nonzero(E < E[a])[0]
    if len(lower) == 0:
        return None
    best = Ba[lower].min()
    cands = lower[Ba[lower] <= best + 1e-12]
    return int(cands[np.argmin(E[cands])])


def nonreversible(S, P, pi, rng, strength=0.9):
    """add circulations around random 4-cycles x -> x^i -> x^{ij} -> x^j -> x, keeping P >= 0 and pi P = pi."""
    P = P.copy()
    F = pi[:, None] * P                      # stationary flows
    for trial in range(4 * S.N):
        x = int(rng.integers(S.N))
        i, j = rng.choice(S.n, 2, replace=False)
        si = (S.cfg[x, i] + 1 + rng.integers(S.ks[i] - 1)) % S.ks[i]
        sj = (S.cfg[x, j] + 1 + rng.integers(S.ks[j] - 1)) % S.ks[j]
        xi = x + (si - S.cfg[x, i]) * S.radix[i]
        xj = x + (sj - S.cfg[x, j]) * S.radix[j]
        xij = xi + (sj - S.cfg[x, j]) * S.radix[j]
        cyc = [x, xi, xij, xj]
        back = [(cyc[(m + 1) % 4], cyc[m]) for m in range(4)]
        gam = strength * min(F[u, v] for u, v in back)
        for m in range(4):
            u, v = cyc[m], cyc[(m + 1) % 4]
            F[u, v] += gam
            F[v, u] -= gam
    Pn = F / pi[:, None]
    np.fill_diagonal(Pn, 0.0)
    np.fill_diagonal(Pn, 1.0 - Pn.sum(axis=1))
    return Pn


def survival(P, pi, A, Ts):
    idx = np.nonzero(A)[0]
    PA = P[np.ix_(idx, idx)]
    u = np.ones(len(idx))
    out = {}
    Tmax = max(Ts)
    for t in range(1, Tmax + 1):
        u = PA @ u
        if t in Ts:
            out[t] = (pi[idx] * u).sum() / pi[idx].sum()
    return out


def main():
    nbad = 0
    ncase = 0
    for name, ks in (("binary n=8", [2] * 8), ("3-state n=5", [3] * 5)):
        S = Space(ks)
        deg = sum(k - 1 for k in ks)
        for inst in range(4):
            h, J = random_pairwise(S, rng, graph="chain+", scale_h=0.5, scale_J=1.0)
            E = pairwise_energy(S, h, J)
            best = None
            for a in local_minima(S, E, strict=True):
                b = exit_target(S, E, a)
                if b is None:
                    continue
                H = barrier_from(S, E, a)[b] - E[a]
                if best is None or H > best[0]:
                    best = (H, a, b)
            if best is None:
                print(f"  {name} inst {inst}: no non-global strict local minimum; skipped")
                continue
            H, a, b = best
            A = component_below(S, E, a, E[a] + H, strict=True)
            wall = outer_boundary(S, A)
            for beta in (2.0, 4.0):
                pi = gibbs(E, beta)
                Pm = np.eye(S.N) + generator(S, E, beta, "metropolis") / deg
                Ph = np.eye(S.N) + generator(S, E, beta, "heatbath") / S.n
                Pn = nonreversible(S, Pm, pi, rng)
                for label, P in (("metropolis", Pm), ("non-reversible", Pn), ("heat-bath", Ph)):
                    assert P.min() >= -1e-14 and np.allclose(P.sum(axis=1), 1) and np.allclose(pi @ P, pi, atol=1e-13)
                    rev_defect = np.abs(pi[:, None] * P - (pi[:, None] * P).T).max() / (pi[:, None] * P).max()
                    flux = (pi[:, None] * P)[np.ix_(~A, A)].sum()
                    piA = pi[A].sum()
                    r1 = flux / piA
                    r2 = pi[wall].sum() / piA
                    Ts = sorted({1, 2, 5, 10, 30, 100, 300, 1000, max(1, int(0.5 / r1)), max(1, int(1.0 / r1))})
                    sv = survival(P, pi, A, Ts)
                    ok = all(sv[T] >= 1 - T * r1 - 1e-12 and 1 - T * r1 >= 1 - T * r2 - 1e-12 for T in Ts)
                    ncase += 1
                    nbad += int(not ok)
                    Th = max(1, int(0.5 / r1))
                    print(f"  {name} inst {inst} beta={beta} {label:15s} rev.defect={rev_defect:.1e} |A|={A.sum():3d} "
                          f"flux/pi(A)={r1:.3e} pi(wall)/pi(A)={r2:.3e}  T={Th}: surv={sv[Th]:.4f} >= "
                          f"{1 - Th * r1:.4f} >= {1 - Th * r2:.4f}   ok={ok}")
    print(f"T9 summary: {ncase} (instance, beta, kernel) cases, violations: {nbad}")


if __name__ == "__main__":
    main()
