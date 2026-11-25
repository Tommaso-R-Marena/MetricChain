"""
T3b — query complexity of exact barrier certification in the large-envelope regime (report, Cor. K7.2).

If the slack between distinct points exceeds the whole energy range (here: uniform Hamming envelope with
c much larger than max E - min E, true residual g = 0) and eps is below the energy resolution, then by
Theorem K7
   W_eps(A) = A ∩ {E >= B - eps},      V_eps(A) = A ∩ {E <= B + eps},
so that
   N_low = minimum number of vertices of the ridge set R = {E >= B} whose removal separates p from q
         = maximum number of p-q paths that are pairwise disjoint on R            (Menger / max-flow),
   N_up  = number of vertices of a hop-shortest p-q path inside {E <= B}.
Test: brute force over anchor sets (N = 16, 18) against a max-flow computation and a BFS.

Run:  python3 t3b_menger.py
"""
import itertools
from collections import deque
import numpy as np
import networkx as nx
from kcore import Space, barrier_from, mcshane

rng = np.random.default_rng(77)


def menger_ridge(S, E, p, q, B):
    """min number of ridge vertices (E >= B) separating p from q; inf-capacity elsewhere."""
    G = nx.DiGraph()
    big = 10 ** 6
    for u in range(S.N):
        cap = 1 if E[u] >= B - 1e-12 else big
        G.add_edge(("in", u), ("out", u), capacity=cap)
        for v in S.nbrs[u]:
            G.add_edge(("out", u), ("in", int(v)), capacity=big)
    val, _ = nx.maximum_flow(G, ("in", p), ("out", q))
    return val


def bfs_len(S, ok, p, q):
    dist = {p: 0}
    dq = deque([p])
    while dq:
        u = dq.popleft()
        if u == q:
            return dist[u] + 1          # number of vertices on the path
        for v in S.nbrs[u]:
            v = int(v)
            if ok[v] and v not in dist:
                dist[v] = dist[u] + 1
                dq.append(v)
    return None


def main():
    nlow_ok = nup_ok = ncase = 0
    for ks in ([2] * 4, [2, 3, 3], [4, 4]):
        S = Space(ks)
        D = S.hamming_env(np.full(S.n, 1000.0))
        g = np.zeros(S.N)
        for trial in range(8):
            # generic values; keep drawing until the pair has a genuine barrier B > max(E(p), E(q))
            while True:
                E = rng.integers(0, 5, S.N).astype(float) + rng.uniform(0, 0.01, S.N)
                p, q = rng.choice(S.N, 2, replace=False)
                B = barrier_from(S, E, p)[q]
                if B > max(E[p], E[q]) + 0.5:
                    break
            eps = 1e-6
            pred_low = menger_ridge(S, E, p, q, B)
            pred_up = bfs_len(S, E <= B + 1e-12, p, q)
            nl = nu = None
            for size in range(1, S.N + 1):
                for A in itertools.combinations(range(S.N), size):
                    A = np.array(A)
                    L, U = mcshane(D, A, g[A])
                    if nl is None and barrier_from(S, E + L, p)[q] >= B - eps:
                        nl = size
                    if nu is None and barrier_from(S, E + U, p)[q] <= B + eps:
                        nu = size
                    if nl is not None and nu is not None:
                        break
                if nl is not None and nu is not None:
                    break
                if size >= 9:
                    break
            ncase += 1
            nlow_ok += int(nl == pred_low)
            nup_ok += int(nu == pred_up)
            print(f"  ks={ks} trial {trial}: N_low brute {nl} vs Menger {pred_low};  "
                  f"N_up brute {nu} vs shortest optimal path {pred_up}")
    print(f"T3b summary: {ncase} instances; N_low = Menger number in {nlow_ok}; N_up = path length in {nup_ok}")


if __name__ == "__main__":
    main()
