"""
T12 — the "product flow" Thomson certificate (report, Prop. K12, remark).

Binary sites, a and b differ on the site set I (|I| = D); other sites frozen at their common values.
Unit flow: flip the D sites in a uniformly random order.  Flow through the edge (x, x + site i) with x at
level m (m sites already flipped):  1 / ( C(D,m) (D-m) ).   Dissipation (Metropolis conductances
c = exp(-beta max(E_x,E_y)) / Z):

    D(psi) = sum_m [C(D,m)(D-m)]^{-2} sum_{edges at level m} 1/c(e)
           <= Z * sum_m [C(D,m)(D-m)]^{-2} [ (D-m) Zneg_m + (m+1) Zneg_{m+1} ],   Zneg_j = sum_{level j} e^{+beta E}.

So cap(a,b) >= 1/D(psi) >= 1/(bound): a capacity LOWER bound from NEGATIVE-temperature level partition
functions of a subcube (kernel-checkable).  Test: validity and looseness against the exact capacity and
against the single-path / few-path bounds.

Run:  OMP_NUM_THREADS=1 python3 t12_product_flow.py
"""
from math import comb
import numpy as np
from kcore import (Space, random_pairwise, pairwise_energy, curie_weiss_energy, generator, gibbs,
                   conductances, capacity, minimax_path)

rng = np.random.default_rng(31)


def product_flow_bounds(S, E, beta, a, b):
    I = np.nonzero(S.cfg[a] != S.cfg[b])[0]
    D = len(I)
    frozen = np.ones(S.N, dtype=bool)
    for j in range(S.n):
        if j not in I:
            frozen &= S.cfg[:, j] == S.cfg[a, j]
    level = (S.cfg[:, I] != S.cfg[a][I][None, :]).sum(axis=1)
    pi = gibbs(E, beta)
    Q = generator(S, E, beta)
    C = conductances(Q, pi)
    # explicit flow and its exact dissipation; divergence check
    div = np.zeros(S.N)
    diss = 0.0
    for x in np.nonzero(frozen)[0]:
        m = level[x]
        if m == D:
            continue
        for i in I:
            if S.cfg[x, i] == S.cfg[a, i]:
                y = x + (S.cfg[b, i] - S.cfg[a, i]) * S.radix[i]
                fl = 1.0 / (comb(D, m) * (D - m))
                div[x] += fl
                div[y] -= fl
                diss += fl ** 2 / C[x, y]
    assert abs(div[a] - 1) < 1e-12 and abs(div[b] + 1) < 1e-12
    inner = np.ones(S.N, dtype=bool); inner[a] = False; inner[b] = False
    assert np.abs(div[inner]).max() < 1e-12
    # bound from negative-temperature level partition functions
    Emin = E.min()
    Z = np.exp(-beta * (E - Emin)).sum()
    bound = 0.0
    for m in range(D):
        zneg_m = np.exp(beta * (E[frozen & (level == m)] - Emin)).sum()
        zneg_m1 = np.exp(beta * (E[frozen & (level == m + 1)] - Emin)).sum()
        bound += ((D - m) * zneg_m + (m + 1) * zneg_m1) / (comb(D, m) * (D - m)) ** 2
    bound *= Z
    ma = np.zeros(S.N, dtype=bool); ma[a] = True
    mb = np.zeros(S.N, dtype=bool); mb[b] = True
    cap, _ = capacity(Q, pi, ma, mb)
    P, _ = minimax_path(S, E, a, b)
    R1 = sum(1.0 / C[u, v] for u, v in zip(P[:-1], P[1:]))
    return cap, 1.0 / diss, 1.0 / bound, 1.0 / R1


def main():
    print("T12 product (random-order) flow:  ratios to the exact capacity (all must be <= 1)")
    print("   system                          beta  flow/cap   Zneg-bound/cap  one-path/cap")
    bad = 0
    S = Space([2] * 8)
    E = np.zeros(S.N)
    for beta in (1.0,):
        cap, f1, f2, p1 = product_flow_bounds(S, E, beta, 0, S.N - 1)
        print(f"   flat landscape n=8              {beta:<5.1f} {f1 / cap:<10.4f} {f2 / cap:<15.4f} {p1 / cap:.4f}")
        bad += int(f1 > cap * (1 + 1e-9) or f2 > f1 * (1 + 1e-9))
    E = curie_weiss_energy(S, 1.0, 0.05)
    for beta in (0.5, 1.0, 2.0):
        cap, f1, f2, p1 = product_flow_bounds(S, E, beta, 0, S.N - 1)
        print(f"   Curie-Weiss n=8                 {beta:<5.1f} {f1 / cap:<10.4f} {f2 / cap:<15.4f} {p1 / cap:.4f}")
        bad += int(f1 > cap * (1 + 1e-9) or f2 > f1 * (1 + 1e-9))
    for inst in range(3):
        h, J = random_pairwise(S, rng, graph="chain+", scale_h=0.5, scale_J=1.0)
        E = pairwise_energy(S, h, J)
        a = int(np.argmin(E))
        b = S.N - 1 - a                      # the complementary configuration: all sites differ
        for beta in (0.5, 1.0, 2.0):
            cap, f1, f2, p1 = product_flow_bounds(S, E, beta, a, b)
            print(f"   random chain+ n=8 inst {inst}        {beta:<5.1f} {f1 / cap:<10.2e} {f2 / cap:<15.2e} {p1 / cap:.2e}")
            bad += int(f1 > cap * (1 + 1e-9) or f2 > f1 * (1 + 1e-9))
    print(f"T12 summary: violations {bad}")


if __name__ == "__main__":
    main()
