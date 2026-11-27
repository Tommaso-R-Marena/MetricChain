#!/usr/bin/env python3
"""Coordinator's check of workstream P9's state-resolved bound on ENUMERATED instances: P9's tables (computed here
through P9's own Resolver -- they are P9's numbers), my left side.

For SEQ on the helix and every order m = 3 .. n, at EVERY state x:
     R(x) = | g(x) - I_{m-1} g(x) |      (my evaluation of g at every state; my grid recursion, lys_enum_check.remainder)
     B_s(x) = sum_{T subset S(x), |T| = m} Theta^s_T(x_T)      for P9's stage s = 1 (hosts resolved), 2 (all sites of T resolved)
and R <= B_2 <= B_1 <= B_SAb must hold.  Controls that must fail: C1 every table replaced by its minimum; C2 every
table reversed along each axis.  Also: the Boltzmann means under the true ensemble (what the certificate pays).
Run: python3 -B resolved_enum_check.py K5 > resolved_enum_check_K5.log
"""
import os, sys, math, time, itertools, resource
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCI = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(SCI, "ws_P9"))
import p9lib as P9                                      # P9's library (guards its imports against writing elsewhere)
sys.path.insert(0, os.path.join(SCI, "p8_verification"))
from lys_enum_check import remainder                    # the coordinator's grid recursion
BETA = P9.BETA if hasattr(P9, "BETA") else None


def log(s): print(s, flush=True)


def main():
    seq = sys.argv[1]; bb = "H"; tau = P9.tau_of(seq); t0 = time.time()
    G, c0, h, J, x0, E0 = P9.setup(seq, bb, tau); n, k = G.ns, list(G.k)
    beta = BETA if BETA is not None else 1.0 / 0.596
    grid = np.stack(np.meshgrid(*[np.arange(v) for v in k], indexing="ij"), axis=-1).reshape(-1, n)
    g = np.concatenate([G.bulk_energy(grid[s:s + 256]) for s in range(0, len(grid), 256)])
    E = P9.pw.f_energy(grid, c0, h, J) + g; wB = np.exp(-beta * (E - E.min())); wB /= wB.sum()
    log(f"=== {seq} on {bb}, tau {tau}: {n} sites, states per site {k}, {len(grid)} states; anchor {x0}; beta = {beta:.6f}; g evaluated at every state [{time.time() - t0:.0f}s]")
    SR = P9.ResBound(G, tuple(x0), P9.EnvelopeSup(G), K=n); RES = P9.Resolver(SR)
    non = [[b for b in range(k[i]) if b != x0[i]] for i in range(n)]
    Pm = np.full((len(grid), n), -1)
    for i in range(n):
        mp = np.full(k[i], -1); mp[non[i]] = np.arange(len(non[i])); Pm[:, i] = mp[grid[:, i]]
    F = g.reshape(k)
    log("| m | subsets | states with >= m sites off | violations R > B2 | violations B2 > B1 | violations B1 > B_SAb | smallest B2/R | largest R (kcal/mol) | "
        "Boltzmann means of beta R; beta B2; beta B1; beta B_SAb | B2/R in Boltzmann mean | control C1 (minimum): violations | control C2 (reversed): violations |")
    log("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for m in range(3, n + 1):
        R = np.abs(remainder(F, x0, m)).reshape(-1)
        B1 = np.zeros(len(grid)); B2 = np.zeros(len(grid)); BS = np.zeros(len(grid)); C1 = np.zeros(len(grid)); C2 = np.zeros(len(grid))
        subs = list(itertools.combinations(range(n), m))
        for T in subs:
            t1, t2, sab, sb = RES.theta_both(m, list(T))
            idx = Pm[:, list(T)]; inS = (idx >= 0).all(axis=1); ii = tuple(idx[inS].T)
            B1[inS] += np.broadcast_to(t1, t2.shape)[ii]; B2[inS] += t2[ii]; BS[inS] += sab
            C1[inS] += t2.min(); C2[inS] += t2[tuple(slice(None, None, -1) for _ in range(m))][ii]
        nz = R > 1e-9
        v2 = int((R > B2 * (1 + 1e-12) + 1e-10).sum()); v21 = int((B2 > B1 * (1 + 1e-9) + 1e-12).sum()); v1s = int((B1 > BS * (1 + 1e-9) + 1e-12).sum())
        log(f"| {m} | {len(subs)} | {int((Pm >= 0).sum(1).__ge__(m).sum())} | {v2} | {v21} | {v1s} | {(B2[nz] / R[nz]).min():.3f} | {R.max():.4g} | "
            f"{beta * (wB * R).sum():.3e}; {beta * (wB * B2).sum():.3e}; {beta * (wB * B1).sum():.3e}; {beta * (wB * BS).sum():.3e} | {(wB * B2).sum() / max((wB * R).sum(), 1e-300):.0f} | "
            f"{int((R > C1 + 1e-10).sum())} | {int((R > C2 + 1e-10).sum())} |")
    log(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
