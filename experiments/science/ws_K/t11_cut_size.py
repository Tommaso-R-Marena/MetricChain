"""
T11 — at what cost?  Size of EXACT decision-tree/box cut certificates on small systems.

For a trap a with exit target b and t = B(a,b), the canonical cut is S* = component of a in {E < t}.
An exact certificate (format K9 of the report) needs a family of boxes, each contained in the high set
{E >= t} (so that a leaf of the min-kernel can certify it), whose union covers the outer boundary of S*.
We report a GREEDY upper bound on the number of such boxes (grow a maximal box inside {E >= t} around an
uncovered wall point, repeat), next to |wall|, |S*| and the number n of boxes of a box cut.

Also: how the count changes if only 90% of the height is to be certified (t' = E(a) + 0.9 H).

Run:  python3 t11_cut_size.py
"""
import numpy as np
from kcore import (Space, barrier_from, random_pairwise, pairwise_energy, local_minima,
                   component_below, outer_boundary)
from t7_chain import ChainSpace

rng = np.random.default_rng(8)


def exit_target(S, E, a):
    Ba = barrier_from(S, E, a)
    lower = np.nonzero(E < E[a])[0]
    if len(lower) == 0:
        return None, None
    best = Ba[lower].min()
    cands = lower[Ba[lower] <= best + 1e-12]
    return int(cands[np.argmin(E[cands])]), best


def greedy_boxes(S, E, a, t):
    comp = component_below(S, E, a, t, strict=True)
    wall = outer_boundary(S, comp)
    high = E >= t - 1e-12
    uncovered = wall.copy()
    nbox = 0
    order = np.argsort(E)
    while uncovered.any():
        y = next(int(u) for u in order if uncovered[u])
        allowed = [{int(S.cfg[y, i])} for i in range(S.n)]
        inbox = np.ones(S.N, dtype=bool)
        for i in range(S.n):
            inbox &= S.cfg[:, i] == S.cfg[y, i]
        improved = True
        while improved:
            improved = False
            for i in rng.permutation(S.n):
                for s in range(S.ks[i]):
                    if s in allowed[i]:
                        continue
                    # candidate box: site i may also take state s
                    cand = np.ones(S.N, dtype=bool)
                    for j in range(S.n):
                        if j == i:
                            cand &= np.isin(S.cfg[:, j], list(allowed[j] | {s}))
                        else:
                            cand &= np.isin(S.cfg[:, j], list(allowed[j]))
                    if high[cand].all():
                        allowed[i].add(s)
                        inbox = cand
                        improved = True
        uncovered &= ~inbox
        nbox += 1
    return nbox, int(wall.sum()), int(comp.sum())


def run(name, S, E):
    rows = []
    for a in local_minima(S, E, strict=False):
        b, B = exit_target(S, E, a)
        if b is None or B - E[a] <= 1e-9:
            continue
        H = B - E[a]
        nb, nw, nc = greedy_boxes(S, E, a, B)
        nb90, nw90, nc90 = greedy_boxes(S, E, a, E[a] + 0.9 * H)
        rows.append((H, nb, nw, nc, nb90, nw90))
    if not rows:
        print(f"  {name}: no traps")
        return
    r = np.array(rows)
    print(f"  {name}: {len(rows)} traps | exact: boxes median {np.median(r[:,1]):.0f} max {r[:,1].max():.0f}; "
          f"|wall| median {np.median(r[:,2]):.0f} max {r[:,2].max():.0f}; |S*| median {np.median(r[:,3]):.0f} "
          f"max {r[:,3].max():.0f}; boxes/n median {np.median(r[:,1]) / S.n:.1f} max {r[:,1].max() / S.n:.1f} "
          f"| 90% of height: boxes median {np.median(r[:,4]):.0f} max {r[:,4].max():.0f}")


def main():
    print("T11: greedy size of exact box-cover cut certificates")
    for n in (6, 8, 10):
        S = Space([2] * n)
        for inst in range(2):
            h, J = random_pairwise(S, rng, graph="chain+", scale_h=0.5, scale_J=1.0)
            run(f"binary n={n} chain+ inst {inst}", S, pairwise_energy(S, h, J))
    for n in (4, 5, 6):
        S = Space([3] * n)
        h, J = random_pairwise(S, rng, graph="chain+", scale_h=0.5, scale_J=1.0)
        run(f"3-state n={n} chain+", S, pairwise_energy(S, h, J))
    for n in (6, 7, 8):
        S = ChainSpace(n)
        run(f"RIS diamond chain n={n} ({S.N} states)", S, S.E)


if __name__ == "__main__":
    main()
