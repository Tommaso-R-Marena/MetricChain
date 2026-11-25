"""
T1 — cut (separator) duality for minimax barriers, and the corner cases of the brief's sketch 1.

Checks, on random energies over small product spaces (unrestricted single-site moves):
 (a) EXHAUSTIVE over all S with a in S, b not in S:
        B(a,b) = max( E(a), max_S min_{outer boundary of S} E )            [claimed theorem]
     and the symmetric inner-boundary form
        B(a,b) = max( E(b), max_S min_{inner boundary of S} E ).
 (b) how often the unrepaired "iff" of the brief fails (no S at all certifies t = B(a,b)).
 (c) the canonical cut: S* = component of a in {E < t} for t = B(a,b) > E(a).
 (d) coordinate cuts: outer boundary of {x_i in T} is the whole complement (complete site graph),
     so the certified value is <= E(b): never better than the trivial bound.
 (e) box cuts: outer boundary of a box prod T_i is the union over i of the boxes
     {x_i notin T_i, x_j in T_j (j != i)}.
Run:  python3 t1_cut_duality.py
"""
import itertools
import numpy as np
from kcore import Space, barrier_from, component_below, outer_boundary, inner_boundary

rng = np.random.default_rng(20261125)


def exhaustive(S, E, a, b):
    others = [u for u in range(S.N) if u not in (a, b)]
    best_out, best_in = -np.inf, -np.inf
    for r in range(len(others) + 1):
        for T in itertools.combinations(others, r):
            mask = np.zeros(S.N, dtype=bool)
            mask[a] = True
            mask[list(T)] = True
            ob = outer_boundary(S, mask)
            ib = inner_boundary(S, mask)
            # boundaries are non-empty because the graph is connected and b is outside
            best_out = max(best_out, E[ob].min())
            best_in = max(best_in, E[ib].min())
    return best_out, best_in


def main():
    stats = dict(cases=0, formula_out_ok=0, formula_in_ok=0, naive_out_fail=0, naive_in_fail=0,
                 canon_ok=0, canon_cases=0)
    for ks in ([2, 2, 2], [3, 3], [2, 2, 3], [2, 2, 2, 2]):
        S = Space(ks)
        ntrial = 40 if S.N <= 12 else 6
        for trial in range(ntrial):
            # integer energies so that ties and the corner cases E(a)=B, E(b)=B occur often
            E = rng.integers(0, 6, S.N).astype(float)
            a, b = rng.choice(S.N, 2, replace=False)
            B = barrier_from(S, E, a)[b]
            bo, bi = exhaustive(S, E, a, b)
            stats["cases"] += 1
            stats["formula_out_ok"] += int(abs(max(E[a], bo) - B) < 1e-12)
            stats["formula_in_ok"] += int(abs(max(E[b], bi) - B) < 1e-12)
            stats["naive_out_fail"] += int(bo < B - 1e-12)     # brief's iff (outer) fails at t=B
            stats["naive_in_fail"] += int(bi < B - 1e-12)      # brief's iff (inner) fails at t=B
            if B > E[a]:
                stats["canon_cases"] += 1
                comp = component_below(S, E, a, B, strict=True)
                ok = (not comp[b]) and E[outer_boundary(S, comp)].min() >= B
                stats["canon_ok"] += int(ok)
    print("T1(a-c) exhaustive cut duality:", stats)
    assert stats["formula_out_ok"] == stats["cases"] and stats["formula_in_ok"] == stats["cases"]
    assert stats["canon_ok"] == stats["canon_cases"]

    # explicit 2-vertex counterexamples to the unrepaired iff
    S = Space([2])
    E = np.array([5.0, 0.0])
    B = barrier_from(S, E, 0)[1]
    mask = np.array([True, False])
    print("counterexample (outer convention): E=(5,0), a=0,b=1: B =", B,
          " only S={a}: min outer boundary =", E[outer_boundary(S, mask)].min())
    E = np.array([0.0, 5.0])
    B = barrier_from(S, E, 0)[1]
    print("counterexample (inner convention): E=(0,5), a=0,b=1: B =", B,
          " only S={a}: min inner boundary =", E[inner_boundary(S, mask)].min())

    # (d) coordinate cuts
    S = Space([3, 3, 2])
    worse = 0
    tot = 0
    for trial in range(200):
        E = rng.normal(size=S.N)
        a, b = rng.choice(S.N, 2, replace=False)
        for i in range(S.n):
            if S.cfg[a, i] == S.cfg[b, i]:
                continue
            for T in ([S.cfg[a, i]],
                      [s for s in range(S.ks[i]) if s != S.cfg[b, i]]):
                mask = np.isin(S.cfg[:, i], T)
                ob = outer_boundary(S, mask)
                assert np.array_equal(ob, ~mask)          # boundary = whole complement
                tot += 1
                worse += int(E[ob].min() <= E[b] + 1e-12)
    print(f"T1(d) coordinate cuts, complete site graph: boundary = complement in all {tot} cases; "
          f"certified value <= E(b) in {worse}/{tot}")

    # (e) box cuts
    okbox = 0
    nbox = 0
    for trial in range(200):
        Ts = []
        for i in range(S.n):
            r = rng.integers(1, S.ks[i] + 1)
            Ts.append(set(rng.choice(S.ks[i], r, replace=False).tolist()))
        if all(len(T) == S.ks[i] for i, T in enumerate(Ts)):
            continue
        inT = np.array([[S.cfg[u, i] in Ts[i] for i in range(S.n)] for u in range(S.N)])
        mask = inT.all(axis=1)
        ob = outer_boundary(S, mask)
        union = (~inT).sum(axis=1) == 1
        nbox += 1
        okbox += int(np.array_equal(ob, union))
    print(f"T1(e) box cuts: outer boundary == union of n one-defect boxes in {okbox}/{nbox} random boxes")
    assert okbox == nbox


if __name__ == "__main__":
    main()
