"""
T4 — which tractable cut families certify how much of the true barrier?

For a local minimum a and its exit target b (the lower state reached with the smallest barrier, so that
H = B(a,b) - E(a) is the depth of a) we compare the exact height H with the best certified wall height
        W_F(a,b) = max_{S in F, a in S, b notin S}  min_{outer boundary of S} E  -  E(a)
over families F whose walls are unions of few boxes or level sets of a counting statistic:

  box      S_I = {x : x_i = a_i for i in I},        wall = union of |I| boxes        (|I| kernel calls)
  sphere   S   = {x : d_H(x,a) < r},                 wall = {d_H(x,a) = r}            (counting constraint)
  count    S   = {x : q_I(x) < r}, q_I = #{i in I : x_i != a_i},  wall = {q_I = r}   (contains both)
  exact    S*  = component of a in {E < B}                                           (= H by duality)

and the LAGRANGIAN relaxation of the counting constraint,
        min_{q=r} E  >=  max_lambda min_x [E(x) + lambda (q(x) - r)]  =  (lower convex envelope of the
        profile m_j = min_{q=j} E)(r),
which is what one gets by handing E + lambda*q to the existing pairwise kernel.

Run:  python3 t4_cut_families.py
"""
import numpy as np
from kcore import (Space, barrier_from, random_pairwise, pairwise_energy, local_minima,
                   ising_chain_energy, curie_weiss_energy)

rng = np.random.default_rng(5)


def convex_envelope_at(levels, vals, r):
    """value at r of the lower convex envelope of the points (levels[j], vals[j])."""
    best = -np.inf
    pts = sorted(zip(levels, vals))
    xs = np.array([p[0] for p in pts], dtype=float)
    ys = np.array([p[1] for p in pts], dtype=float)
    if r in xs:
        best = ys[list(xs).index(r)]
    val = best if best > -np.inf else np.inf
    # the envelope at r is the min over chords through r (and the point itself)
    for i in range(len(xs)):
        for j in range(len(xs)):
            if xs[i] < r < xs[j]:
                t = (r - xs[i]) / (xs[j] - xs[i])
                val = min(val, (1 - t) * ys[i] + t * ys[j])
    return val


def analyse(S, E, a, b, label, verbose=False):
    B = barrier_from(S, E, a)[b]
    H = B - E[a]
    diff = S.cfg[a] != S.cfg[b]
    neq = S.cfg != S.cfg[a][None, :]                 # N x n: site differs from a
    best = dict(box=-np.inf, sphere=-np.inf, count=-np.inf, lagr=-np.inf)
    arg = {}
    for Imask in range(1, 2 ** S.n):
        I = np.array([(Imask >> i) & 1 for i in range(S.n)], dtype=bool)
        if not (I & diff).any():
            continue
        q = neq[:, I].sum(axis=1)
        qb = int((I & diff).sum())
        levels = np.arange(0, I.sum() + 1)
        prof = np.array([E[q == j].min() for j in levels])
        for r in range(1, qb + 1):
            val = prof[r] - E[a]
            if val > best["count"]:
                best["count"] = val
                arg["count"] = (I.copy(), r)
            if r == 1 and val > best["box"]:
                best["box"] = val
                arg["box"] = I.copy()
            if I.all() and val > best["sphere"]:
                best["sphere"] = val
            lag = convex_envelope_at(levels, prof, r) - E[a]
            best["lagr"] = max(best["lagr"], lag)
    triv = max(E[a], E[b]) - E[a]
    out = dict(label=label, H=H, triv=triv, **best)
    if verbose:
        print(f"  {label}: H={H:.3f} trivial={triv:.3f} box={best['box']:.3f} sphere={best['sphere']:.3f} "
              f"count={best['count']:.3f} lagrangian={best['lagr']:.3f}"
              f"  |I_box|={int(arg['box'].sum())} (I_count,r)=({int(arg['count'][0].sum())},{arg['count'][1]})")
    return out


def exit_target(S, E, a):
    Ba = barrier_from(S, E, a)
    lower = np.nonzero(E < E[a])[0]
    if len(lower) == 0:
        return None
    best = Ba[lower].min()
    cands = lower[Ba[lower] <= best + 1e-12]
    return int(cands[np.argmin(E[cands])])


def main():
    rows = []
    print("T4 structured examples")
    S = Space([2] * 10)
    E = ising_chain_energy(S, Jc=1.0, hfield=0.3)
    a, b = 0, S.N - 1
    rows.append(analyse(S, E, a, b, "Ising chain n=10 J=1 h=0.3, all-down -> all-up", verbose=True))
    E = ising_chain_energy(S, Jc=1.0, hfield=0.3, periodic=True)
    rows.append(analyse(S, E, a, b, "Ising ring  n=10 J=1 h=0.3, all-down -> all-up", verbose=True))
    E = curie_weiss_energy(S, Jc=1.0, hfield=0.05)
    rows.append(analyse(S, E, a, b, "Curie-Weiss n=10 J=1 h=0.05, all-down -> all-up", verbose=True))

    print("T4 random pairwise models: every non-global strict local minimum a, b = its exit target")
    summary = {}
    for name, ks, graph, ninst in (("binary n=10 chain+", [2] * 10, "chain+", 12),
                                   ("binary n=10 complete", [2] * 10, "complete", 12),
                                   ("3-state n=6 chain+", [3] * 6, "chain+", 12),
                                   ("3-state n=6 complete", [3] * 6, "complete", 12)):
        S = Space(ks)
        res = []
        for inst in range(ninst):
            h, J = random_pairwise(S, rng, graph=graph, scale_h=0.5, scale_J=1.0)
            E = pairwise_energy(S, h, J)
            mins = local_minima(S, E, strict=True)
            for a in mins:
                b = exit_target(S, E, a)
                if b is None:
                    continue
                r = analyse(S, E, a, b, name)
                if r["H"] > 1e-9:
                    res.append(r)
        H = np.array([r["H"] for r in res])
        line = f"  {name}: {len(res)} minima; "
        for fam in ("box", "sphere", "count", "lagr"):
            v = np.array([max(r[fam], 0.0) for r in res]) / H
            exact = np.mean(v > 1 - 1e-9)
            line += f"{fam}: mean frac {v.mean():.2f}, exact in {exact:.0%}; "
        # Lagrangian never beats the trivial bound
        nolag = all(r["lagr"] <= r["triv"] + 1e-9 for r in res)
        line += f"lagrangian <= trivial bound always: {nolag}"
        print(line)
        summary[name] = res
    return rows, summary


if __name__ == "__main__":
    main()
