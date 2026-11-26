#!/usr/bin/env python3
"""ER2: attack on Theorem E13 (the polytope of a first-order class).

(a) extreme <=> tight graph connected (finite envelopes): vertices by brute force over bases (independent of
    the criterion), then the criterion on vertices, on mixtures, and on members built from spanning trees of
    tight constraints; plus the algebraic test "rank of the active constraints".
(b) identified inside the class <=> an exposed face (exposed by an f in span{1, Phi}) through mu with injective
    data: direct fibre LP against the criterion, computed from the vertex list (smallest exposed face).
(c) flow certificate: feasibility of the dual system at t = max, t = max +- 1e-3.
"""
import itertools, sys
import numpy as np
from scipy.optimize import linprog
from er2_common import (shortest_path_closure, class_rows_mu, is_member, tight_graph_components,
                        vertices_bruteforce)

rng = np.random.default_rng(1302)


def random_envelope(N, kind):
    if kind == "metric":                       # symmetric metric: points on a line
        p = rng.random(N) * rng.uniform(0.5, 3.0)
        return np.abs(p[:, None] - p[None, :]) + 0.0
    if kind == "quasi":                        # asymmetric, triangle inequality by shortest paths
        return shortest_path_closure(rng.uniform(0.1, 2.5, size=(N, N)))
    if kind == "zeros":                        # asymmetric with some zero entries
        D = rng.uniform(0.1, 2.0, size=(N, N))
        D[rng.random((N, N)) < 0.25] = 0.0
        return shortest_path_closure(D)
    if kind == "notriangle":                   # no triangle inequality at all
        D = rng.uniform(0.1, 2.5, size=(N, N)); np.fill_diagonal(D, 0.0)
        return D
    raise ValueError(kind)


def active_rank(mu, R, tol=1e-9):
    act = np.abs(R @ mu) <= tol * np.maximum(1.0, np.abs(R).max(axis=1))
    M = np.vstack([R[act], np.ones((1, len(mu)))])
    return np.linalg.matrix_rank(M, tol=1e-9)


def fibre_is_point(mu, R, Phi, tol=1e-7):
    N = len(mu)
    A_eq = np.vstack([np.ones((1, N)), Phi]); b_eq = A_eq @ mu
    for k in range(N):
        for sgn in (1.0, -1.0):
            c = np.zeros(N); c[k] = -sgn
            res = linprog(c, A_ub=R, b_ub=np.zeros(len(R)), A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * N,
                          method="highs")
            if res.status != 0:
                raise RuntimeError("fibre LP failed")
            if abs(-res.fun * sgn - mu[k]) > tol:
                return False
    return True


def smallest_exposed_face(mu, V, Phi, tol=1e-8):
    """Indices of the vertices of the smallest face of the form argmax_P E f, f in span{1,Phi}, containing mu."""
    m = Phi.shape[0]
    G = (V - mu) @ Phi.T                          # rows: A v - A mu
    keep = []
    for j in range(len(V)):
        res = linprog(G[j], A_ub=G, b_ub=np.zeros(len(V)), bounds=[(-1, 1)] * m, method="highs")
        if res.status != 0:
            raise RuntimeError("normal cone LP failed")
        if res.fun > -tol:
            keep.append(j)
    return keep


def criterion_b(mu, V, Phi):
    keep = smallest_exposed_face(mu, V, Phi)
    F = V[keep]
    rF = np.linalg.matrix_rank(F - F[0], tol=1e-8) if len(F) > 1 else 0
    rA = np.linalg.matrix_rank((F - F[0]) @ Phi.T, tol=1e-8) if len(F) > 1 else 0
    return rF == rA, len(keep)


def flow_feasible(f, t, pi, d):
    """Is there Psi >= 0 with (f(z)-t) pi(z) <= sum_x Psi(x,z) - sum_y e^{d(z,y)} Psi(z,y) for all z ?"""
    N = len(pi)
    pairs = [(x, y) for x in range(N) for y in range(N) if x != y]
    # A_ub Psi <= b_ub :  -(in - out) <= -(f - t) pi
    A = np.zeros((N, len(pairs)))
    for k, (x, y) in enumerate(pairs):
        A[y, k] -= 1.0                          # inflow to y
        A[x, k] += np.exp(d[x, y])              # outflow from x, with gain
    res = linprog(np.zeros(len(pairs)), A_ub=A, b_ub=-(f - t) * pi, bounds=[(0, None)] * len(pairs),
                  method="highs")
    return res.status == 0


def main():
    tot = dict(inst=0, verts=0, a_vertex_disconnected=0, a_mixture_connected=0, a_tree_members=0,
               a_tree_not_vertex=0, a_rank_mismatch=0, b_cases=0, b_mismatch=0, b_identified=0,
               b_vertex_cases=0, b_vertex_mismatch=0, c_cases=0, c_fail=0)
    b_by_kind = {}
    for N, kinds, reps in ((4, ("metric", "quasi", "zeros", "notriangle"), 12), (5, ("metric", "quasi", "zeros"), 6)):
        for kind in kinds:
            for rep in range(reps):
                d = random_envelope(N, kind)
                pi = rng.dirichlet(np.ones(N) * 3)
                R, pairs = class_rows_mu(pi, d)
                V = vertices_bruteforce(pi, d)
                tot["inst"] += 1; tot["verts"] += len(V)
                # ---------- (a)
                for v in V:
                    if tight_graph_components(v, pi, d) != 1:
                        tot["a_vertex_disconnected"] += 1
                    if active_rank(v, R) != N:
                        tot["a_rank_mismatch"] += 1
                mixes = []
                for i, j in itertools.combinations(range(len(V)), 2):
                    mixes.append(0.5 * (V[i] + V[j]))
                for _ in range(30):
                    k = rng.integers(2, min(4, len(V)) + 1) if len(V) >= 2 else 1
                    sel = rng.choice(len(V), size=k, replace=False)
                    w = rng.dirichlet(np.ones(k))
                    if k >= 2:
                        mixes.append(w @ V[sel])
                for mu in mixes:
                    conn = tight_graph_components(mu, pi, d) == 1
                    ext = active_rank(mu, R) == N
                    if conn:
                        tot["a_mixture_connected"] += 1
                    if conn != ext:
                        tot["a_rank_mismatch"] += 1
                # members with a connected tight graph built from random spanning trees of tight constraints
                for _ in range(200):
                    order = rng.permutation(N); w = np.zeros(N); w[order[0]] = 1.0
                    for t in range(1, N):
                        y = order[t]; x = order[rng.integers(t)]
                        if rng.random() < 0.5:
                            w[y] = np.exp(d[x, y]) * w[x]           # constraint (x,y) tight
                        else:
                            w[y] = np.exp(-d[y, x]) * w[x]          # constraint (y,x) tight
                    mu = pi * w; mu /= mu.sum()
                    if is_member(mu, pi, d):
                        tot["a_tree_members"] += 1
                        if not any(np.abs(mu - v).max() < 1e-7 for v in V):
                            tot["a_tree_not_vertex"] += 1
                # ---------- (b)
                for m in (1, 2, 3):
                    if m > N - 2:
                        continue
                    for style in ("int", "gauss"):
                        Phi = (rng.integers(0, 3, size=(m, N)).astype(float) if style == "int"
                               else rng.normal(size=(m, N)))
                        pts = [("vertex", v) for v in V]
                        pts += [("mid", mu) for mu in mixes[:12]]
                        pts += [("mix", mu) for mu in mixes[-6:]]
                        pts.append(("centre", V.mean(axis=0)))
                        for tag, mu in pts:
                            direct = fibre_is_point(mu, R, Phi)
                            crit, nface = criterion_b(mu, V, Phi)
                            tot["b_cases"] += 1; tot["b_identified"] += direct
                            key = (tag, direct)
                            b_by_kind[key] = b_by_kind.get(key, 0) + 1
                            if direct != crit:
                                tot["b_mismatch"] += 1
                            if tag == "vertex":
                                tot["b_vertex_cases"] += 1
                                if direct != (nface == 1):
                                    tot["b_vertex_mismatch"] += 1
                # ---------- (c)
                for _ in range(5):
                    f = rng.normal(size=N)
                    res = linprog(-f, A_ub=R, b_ub=np.zeros(len(R)), A_eq=np.ones((1, N)), b_eq=[1.0],
                                  bounds=[(0, None)] * N, method="highs")
                    tmax = -res.fun
                    good = (flow_feasible(f, tmax + 1e-9, pi, d) and flow_feasible(f, tmax + 1e-3, pi, d)
                            and not flow_feasible(f, tmax - 1e-3, pi, d))
                    tot["c_cases"] += 1; tot["c_fail"] += (not good)
    print("E13 attack: random envelopes on 4 and 5 states (symmetric metrics, quasi-metrics, with zero entries, without triangle inequality)")
    print(f"  instances {tot['inst']}, vertices found by brute force over bases {tot['verts']}")
    print(f"  (a) vertices with a DISCONNECTED tight graph: {tot['a_vertex_disconnected']}")
    print(f"  (a) proper mixtures of vertices with a CONNECTED tight graph: {tot['a_mixture_connected']}")
    print(f"  (a) members built from a spanning tree of tight constraints: {tot['a_tree_members']}; of these NOT in the vertex list: {tot['a_tree_not_vertex']}")
    print(f"  (a) disagreements between 'tight graph connected' and 'active constraints have full rank': {tot['a_rank_mismatch']}")
    print(f"  (b) (member, Phi) cases {tot['b_cases']}; identified by the fibre LP {tot['b_identified']}; disagreements with the exposed-face criterion: {tot['b_mismatch']}")
    print(f"      by kind of member (kind, identified): {dict(sorted(b_by_kind.items()))}")
    print(f"  (b) vertices: {tot['b_vertex_cases']} cases; disagreements 'identified <=> unique maximiser of some f in the span': {tot['b_vertex_mismatch']}")
    print(f"  (c) flow certificate feasible at t >= max and infeasible at max - 1e-3: failures {tot['c_fail']} of {tot['c_cases']}")
    # the infinite envelope (simplex): delta_x is extreme with an empty tight graph
    N = 4; pi = np.full(N, 0.25); d = np.full((N, N), np.inf); np.fill_diagonal(d, 0.0)
    mu = np.array([1.0, 0, 0, 0])
    print(f"  infinite envelope (simplex), delta_x: components of the tight graph = {tight_graph_components(mu, pi, d)} (extreme; (a) needs a finite envelope)")
    bad = (tot['a_vertex_disconnected'] + tot['a_mixture_connected'] + tot['a_tree_not_vertex'] + tot['a_rank_mismatch']
           + tot['b_mismatch'] + tot['b_vertex_mismatch'] + tot['c_fail'])
    print("E13: NO COUNTEREXAMPLE" if bad == 0 else "E13: COUNTEREXAMPLE(S) FOUND")


if __name__ == "__main__":
    main()
