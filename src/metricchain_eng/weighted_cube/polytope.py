"""The Lipschitz polytope of a weighted cube: exact vertex tests, the edges at a vertex, and four independent
exact vertex enumerators.

The polytope.  ``L`` sites, node ``x`` in ``{0, ..., 2^L - 1}`` (bit ``i`` of ``x`` = letter of site ``i``),
positive weights ``w_0, ..., w_{L-1}``:

    P(w) = { phi : nodes -> R :  |phi(x) - phi(x ^ 2^i)| <= w_i  for all x, i } / constants.

It has ``2^L - 1`` dimensions and ``L 2^L`` inequalities (two per edge of the cube): 7 and 24 for ``L = 3``,
15 and 64 for ``L = 4``, 31 and 160 for ``L = 5``.  Because the weighted Hamming distance is the path metric
of the cube graph, the edge inequalities are equivalent to ``|phi(x) - phi(y)| <= d_w(x, y)`` for all pairs.

All functions here take INTEGER weights and return integer vectors normalised by ``phi(0) = 0``: the
constraint matrix is the incidence matrix of the cube graph, which is totally unimodular, so every vertex is
integral.  Rational weights are handled by clearing denominators; the dependence on an irrational slope ratio
is handled in ``chambers``.

Facts used, with proofs.

(V) ``phi`` in ``P(w)`` is a vertex iff the graph of its tight edges (``|difference| = w_i``) is connected.
    Proof: a point of a polytope of dimension ``2^L - 1`` is a vertex iff its tight constraints have rank
    ``2^L - 1``; the constraint rows are ``+-(e_y - e_x)``, and the incidence vectors of a graph with ``c``
    components on ``N`` nodes have rank ``N - c``.  So a vertex is determined by a spanning tree of tight edges
    with a sign for each, and is integral for integer weights.

(E) Orient every tight edge from its lower to its higher end (an acyclic digraph ``T``).  The edges of ``P(w)``
    at the vertex ``phi`` are the directions ``-1_U``, ``U`` a proper non-empty node set that no arc of ``T``
    leaves and such that ``U`` and its complement are connected in ``T``; the adjacent vertex is
    ``phi - s 1_U`` with ``s = min { phi(y) - phi(x) + w_e : e = {x, y} an edge of the cube, x not in U, y in U }``.
    Proof: the cone of feasible directions is ``C = { psi : psi(y) <= psi(x) for every arc x -> y }`` (modulo
    constants; pointed because ``T`` is connected).  (i) A member of ``C`` with values ``c_1 < ... < c_m`` equals
    ``c_m - sum_j (c_{j+1} - c_j) 1_{U_j}``, ``U_j = {psi <= c_j}``, and no arc leaves ``U_j``: ``C`` is generated
    by the vectors ``-1_U``, ``U`` closed under arcs.  (ii) If ``U = U_1 + U_2`` without tight edges between the
    parts, ``-1_U = -1_{U_1} - 1_{U_2}`` with both terms in ``C``; if the complement ``D = D_1 + D_2`` splits,
    ``-1_U = -1_{U + D_1} - 1_{U + D_2}`` modulo constants: not extreme.  (iii) If ``U`` and ``D`` are connected and
    ``-1_U = psi_1 + psi_2`` in ``C``, both ``psi_i`` are constant along every arc inside ``U`` and inside ``D``
    (their sum is, and each difference has a sign), hence constant on ``U`` and on ``D``: non-negative multiples
    of ``-1_U``.  Along an extreme direction the first constraint to become tight is the minimum above.

(C) The graph of a polytope is connected: a set of vertices that contains one vertex and is closed under (E) is
    the vertex set.

Enumerators (each is complete by its own argument; they share no code beyond the edge list):

* ``enumerate_bfs``        breadth-first search over the graph of the polytope, by (E) and (C);
* ``enumerate_bfs_orbits`` the same over orbits of the symmetry group;
* ``enumerate_dfs``        depth-first search over "canonical attachment orders" (uses only (V));
* ``enumerate_bases``      brute force over all sets of ``2^L - 1`` edges with an exact rank test and all sign
                           patterns (uses neither (V) nor (E); ``L <= 3``);
* ``enumerate_ppl``        the double-description code of the Parma Polyhedra Library (exact integers), if the
                           optional package ``pplpy`` is installed.
"""
from __future__ import annotations

import itertools
import sys
from collections import deque
from fractions import Fraction

import numpy as np

# ----------------------------------------------------------------------------- the cube graph


def cube_edges(L: int):
    """Edges ``(x, y, i)`` of the cube, ``y = x | 2^i``, ``x`` with letter 0 at site ``i``."""
    return [(x, x | (1 << i), i) for x in range(1 << L) for i in range(L) if not (x >> i) & 1]


def n_inequalities(L: int) -> int:
    return L * (1 << L)


def dimension(L: int) -> int:
    return (1 << L) - 1


def additive_vertex(wts):
    """``phi(x) = sum_i w_i x_i``: every edge is tight, so it is a vertex."""
    L = len(wts)
    return tuple(sum(wts[i] for i in range(L) if (x >> i) & 1) for x in range(1 << L))


def is_feasible(phi, wts) -> bool:
    L = len(wts)
    return all(abs(phi[y] - phi[x]) <= wts[i] for (x, y, i) in cube_edges(L))


def tight_graph_connected(phi, wts) -> bool:
    L = len(wts)
    n = 1 << L
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for (x, y, i) in cube_edges(L):
        if abs(phi[y] - phi[x]) == wts[i]:
            parent[find(x)] = find(y)
    return len({find(v) for v in range(n)}) == 1


def is_vertex(phi, wts) -> bool:
    """Exact test by (V): feasible and tight graph connected."""
    return is_feasible(phi, wts) and tight_graph_connected(phi, wts)


def is_vertex_by_rank(phi, wts) -> bool:
    """Exact test from the definition of a vertex: feasible, and the tight constraints have rank ``2^L - 1``
    (Gaussian elimination over the rationals; independent of (V))."""
    L = len(wts)
    n = 1 << L
    if not is_feasible(phi, wts):
        return False
    rows = []
    for (x, y, i) in cube_edges(L):
        if abs(phi[y] - phi[x]) == wts[i]:
            r = [Fraction(0)] * (n - 1)
            if x:
                r[x - 1] -= 1
            if y:
                r[y - 1] += 1
            rows.append(r)
    return _rank(rows, n - 1) == n - 1


def _rank(rows, ncol) -> int:
    rows = [r[:] for r in rows]
    rank = 0
    for c in range(ncol):
        piv = next((k for k in range(rank, len(rows)) if rows[k][c] != 0), None)
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        pr = rows[rank]
        for k in range(len(rows)):
            if k != rank and rows[k][c] != 0:
                f = rows[k][c] / pr[c]
                rows[k] = [a - f * b for a, b in zip(rows[k], pr)]
        rank += 1
        if rank == len(rows):
            break
    return rank


# ----------------------------------------------------------------------------- the edges at a vertex (E)


def tight_dag(phi, wts):
    """Bit masks ``up[v]``, ``dn[v]`` of the tight arcs leaving / entering ``v`` (arcs point upwards)."""
    L = len(wts)
    n = 1 << L
    up = [0] * n
    dn = [0] * n
    for (x, y, i) in cube_edges(L):
        d = phi[y] - phi[x]
        if d == wts[i]:
            up[x] |= 1 << y
            dn[y] |= 1 << x
        elif d == -wts[i]:
            up[y] |= 1 << x
            dn[x] |= 1 << y
    return up, dn


def _closures(phi, up, dn):
    n = len(phi)
    order = sorted(range(n), key=lambda v: phi[v])
    upcl = [0] * n
    dncl = [0] * n
    for v in order:
        m = 1 << v
        d = dn[v]
        while d:
            b = d & -d
            d ^= b
            m |= dncl[b.bit_length() - 1]
        dncl[v] = m
    for v in reversed(order):
        m = 1 << v
        u = up[v]
        while u:
            b = u & -u
            u ^= b
            m |= upcl[b.bit_length() - 1]
        upcl[v] = m
    return upcl, dncl


def _component(seed, allowed, adj):
    comp = seed
    frontier = seed
    while frontier:
        b = frontier & -frontier
        frontier ^= b
        new = adj[b.bit_length() - 1] & allowed & ~comp
        comp |= new
        frontier |= new
    return comp


def _union(masks, S):
    s = 0
    while S:
        b = S & -S
        S ^= b
        s |= masks[b.bit_length() - 1]
    return s


def edge_sets(phi, wts):
    """All node sets ``U`` (bit masks) of (E): up-sets of the tight digraph with ``U`` and its complement
    connected.  The search fixes a source ``s`` of the digraph and grows the side that contains it; a branch is
    cut as soon as the nodes forced to the other side fall into two components, and components that cannot
    belong to the other side are absorbed, so that every surviving state leads to at least one solution."""
    n = len(phi)
    full = (1 << n) - 1
    up, dn = tight_dag(phi, wts)
    adj = [up[v] | dn[v] for v in range(n)]
    if _component(1, full, adj) != full:
        raise ValueError("the tight graph is not connected: not a vertex")
    upcl, dncl = _closures(phi, up, dn)
    s = next(v for v in range(n) if dn[v] == 0)
    out = []

    def rec(X, F, grow, close_in, close_out, emit_complement):
        # X: the growing side (contains s); F: nodes forced to the other side
        front = _union(grow, X) & ~X & ~F
        if not front:
            if F:
                out.append(full & ~X if emit_complement else X)
            return
        yb = front & -front
        y = yb.bit_length() - 1
        F2 = F | close_out[y]
        if F:
            rec(X, F2, grow, close_in, close_out, emit_complement)
        else:
            K = _component(yb, full & ~X, adj)
            rec(full & ~K, F2, grow, close_in, close_out, emit_complement)
        X2 = X | close_in[y]
        if F:
            K = _component(F & -F, full & ~X2, adj)
            if F & ~K:
                return
            rec(full & ~K, F, grow, close_in, close_out, emit_complement)
        else:
            rec(X2, 0, grow, close_in, close_out, emit_complement)

    rec(dncl[s], 0, up, dncl, upcl, True)    # s in the lower side D; U = complement of D
    rec(upcl[s], 0, dn, upcl, dncl, False)   # s in U
    return out


def step_length(phi, U, wts):
    L = len(wts)
    n = 1 << L
    s = None
    for x in range(n):
        if (U >> x) & 1:
            continue
        for i in range(L):
            y = x ^ (1 << i)
            if (U >> y) & 1:
                c = phi[y] - phi[x] + wts[i]
                if s is None or c < s:
                    s = c
    if s is None or s <= 0:
        raise AssertionError("no positive step: U is not an edge direction")
    return s


def neighbours(phi, wts):
    """The vertices adjacent to the vertex ``phi`` in the graph of the polytope (normalised, as tuples)."""
    n = len(phi)
    out = []
    for U in edge_sets(phi, wts):
        s = step_length(phi, U, wts)
        new = [phi[v] - s if (U >> v) & 1 else phi[v] for v in range(n)]
        c0 = new[0]
        out.append(tuple(v - c0 for v in new))
    return out


# ----------------------------------------------------------------------------- symmetry


def weight_preserving_perms(wts):
    """All permutations ``s`` of the sites with ``w[s[i]] = w[i]``."""
    L = len(wts)
    return [s for s in itertools.permutations(range(L)) if all(wts[s[i]] == wts[i] for i in range(L))]


def node_perm_table(L: int, perms) -> np.ndarray:
    """``table[k, x]`` = the node obtained from ``x`` by moving bit ``i`` to position ``perms[k][i]``."""
    n = 1 << L
    tab = np.zeros((len(perms), n), dtype=np.uint8)
    for k, s in enumerate(perms):
        for x in range(n):
            y = 0
            for i in range(L):
                if (x >> i) & 1:
                    y |= 1 << s[i]
            tab[k, x] = y
    return tab


def group_order(L: int, nperm: int) -> int:
    return 2 * nperm * (1 << L)


def image(phi, table_row, t: int, eps: int):
    """The image ``x -> eps * phi[table_row[x] ^ t]`` of a function, normalised by its value at node 0."""
    vals = [eps * phi[int(table_row[x]) ^ t] for x in range(len(phi))]
    c = vals[0]
    return tuple(v - c for v in vals)


def canonical(phi, table):
    """Canonical member of the orbit of ``phi`` and the order of its stabiliser: among the images whose value at
    node 0 is their minimum (shifted to 0) the lexicographically least one; the number of group elements that
    produce it is the order of the stabiliser.  Same convention as ``wcube_kernel.c``."""
    n = len(phi)
    mn, mx = min(phi), max(phi)
    best = None
    count = 0
    for eps, ref in ((1, mn), (-1, mx)):
        for t in range(n):
            if phi[t] != ref:
                continue
            for row in table:
                cand = tuple(eps * (phi[int(row[x]) ^ t] - ref) for x in range(n))
                if best is None or cand < best:
                    best, count = cand, 1
                elif cand == best:
                    count += 1
    return best, count


def orbit(phi, table):
    """All distinct images of ``phi`` under the group (normalised by the value at node 0)."""
    n = len(phi)
    out = set()
    for eps in (1, -1):
        for t in range(n):
            for row in table:
                out.add(image(phi, row, t, eps))
    return out


# ----------------------------------------------------------------------------- enumerator 1: BFS over the graph


def enumerate_bfs(wts, limit: int | None = None, return_degrees: bool = False):
    """All vertices (set of tuples with ``phi(0) = 0``) by breadth-first search from the additive vertex."""
    start = additive_vertex(wts)
    seen = {start}
    queue = deque([start])
    degrees = {}
    while queue:
        phi = queue.popleft()
        nbs = neighbours(phi, wts)
        degrees[phi] = len(nbs)
        for nb in nbs:
            if nb not in seen:
                seen.add(nb)
                queue.append(nb)
        if limit is not None and len(seen) > limit:
            raise RuntimeError("vertex limit exceeded")
    return (seen, degrees) if return_degrees else seen


def enumerate_bfs_orbits(wts, perms=None, limit: int | None = None):
    """Orbit representatives by breadth-first search over orbits.  Returns ``(reps, total)``: ``reps`` maps the
    canonical member of every orbit to ``(stabiliser order, degree)``, ``total`` is the number of vertices."""
    L = len(wts)
    perms = weight_preserving_perms(wts) if perms is None else perms
    table = node_perm_table(L, perms)
    order = group_order(L, len(perms))
    key, stab = canonical(additive_vertex(wts), table)
    reps = {key: [stab, None]}
    queue = deque([key])
    while queue:
        phi = queue.popleft()
        nbs = neighbours(phi, wts)
        reps[phi][1] = len(nbs)
        for nb in nbs:
            k, st = canonical(nb, table)
            if k not in reps:
                reps[k] = [st, None]
                queue.append(k)
        if limit is not None and len(reps) > limit:
            raise RuntimeError("orbit limit exceeded")
    total = sum(order // st for st, _ in reps.values())
    return {k: tuple(v) for k, v in reps.items()}, total


# ----------------------------------------------------------------------------- enumerator 2: DFS over attachment orders


def enumerate_dfs(wts, limit: int | None = None):
    """All vertices by a depth-first search that uses only (V).

    For a vertex ``phi`` let ``S_0 = {0}`` and let ``y_k`` be the least node outside ``S_k`` that has a tight
    edge into ``S_k`` (it exists because the tight graph is connected); ``S_{k+1} = S_k + y_k``.  The search
    builds ``(S_k, phi|S_k)`` step by step: the nodes outside ``S`` that have an edge into ``S`` not yet declared
    slack are tried in increasing order; the node chosen gets a value at distance exactly ``w`` from a neighbour
    in ``S`` along such an edge, and every node passed over has all its current edges into ``S`` declared slack
    (strict inequality, checked when the node finally receives its value).  Every vertex is produced exactly
    once (its own sequence ``y_k`` is the only path that yields it), and every leaf is a vertex.  The search
    has many dead ends and is meant as an independent check for small cases."""
    L = len(wts)
    n = 1 << L
    full = (1 << n) - 1
    nb = [[(x ^ (1 << i), wts[i], i) for i in range(L)] for x in range(n)]
    dist = [[sum(wts[i] for i in range(L) if ((x ^ y) >> i) & 1) for y in range(n)] for x in range(n)]
    phi = [0] * n
    slack = [0] * n   # bit i of slack[z]: the edge of z in direction i is declared slack
    assigned = [0]
    out = []
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old_limit, 10 * n + 1000))

    def rec(S):
        if S == full:
            out.append(tuple(phi))
            if limit is not None and len(out) > limit:
                raise RuntimeError("vertex limit exceeded")
            return
        saved = []
        for z in range(n):
            if (S >> z) & 1:
                continue
            mz = slack[z]
            vals = set()
            for (x, w, i) in nb[z]:
                if (S >> x) & 1 and not (mz >> i) & 1:
                    vals.add(phi[x] + w)
                    vals.add(phi[x] - w)
            if not vals:
                continue
            for v in sorted(vals):
                ok = True
                for (x, w, i) in nb[z]:
                    if (S >> x) & 1:
                        d = abs(v - phi[x])
                        if d > w or (d == w and (mz >> i) & 1):
                            ok = False
                            break
                if ok:
                    dz = dist[z]
                    for x in assigned:      # extendability to a Lipschitz function (pruning only)
                        if abs(v - phi[x]) > dz[x]:
                            ok = False
                            break
                if ok:
                    phi[z] = v
                    assigned.append(z)
                    rec(S | (1 << z))
                    assigned.pop()
            m = mz
            closed = True
            for (x, w, i) in nb[z]:
                if (S >> x) & 1:
                    m |= 1 << i
                else:
                    closed = False
            saved.append((z, mz))
            slack[z] = m
            if closed:          # z can never become tight: no vertex below this state
                break
        for (z, mz) in saved:
            slack[z] = mz

    try:
        rec(1)
    finally:
        sys.setrecursionlimit(old_limit)
    return set(out)


# ----------------------------------------------------------------------------- enumerator 3: brute force over bases


def enumerate_bases(wts):
    """All vertices from the definition: for every set of ``2^L - 1`` edges whose constraint rows are linearly
    independent (exact rank test: Gauss-Jordan elimination over the rationals) and every pattern of signs, solve
    the linear system exactly and keep the solution if it satisfies all inequalities.  ``L <= 3`` (792 edge
    sets, 128 sign patterns)."""
    L = len(wts)
    n = 1 << L
    if L > 3:
        raise ValueError("brute force over bases is limited to L <= 3")
    if max(wts) > 10 ** 6:
        raise ValueError("weights too large for exact 64-bit arithmetic")
    edges = cube_edges(L)
    ea = np.array([e[0] for e in edges])
    eb = np.array([e[1] for e in edges])
    ew = np.array([wts[e[2]] for e in edges], dtype=np.int64)
    signs = np.array(list(itertools.product((1, -1), repeat=n - 1)), dtype=np.int64)
    out = set()
    for comb in itertools.combinations(range(len(edges)), n - 1):
        M = [[Fraction(0)] * (n - 1) for _ in comb]
        for r, k in enumerate(comb):
            x, y, _ = edges[k]
            if x:
                M[r][x - 1] -= 1
            if y:
                M[r][y - 1] += 1
        inv = _inverse(M)
        if inv is None:
            continue
        if any(v.denominator != 1 for row in inv for v in row):
            raise AssertionError("non-integral inverse (contradicts total unimodularity)")
        inv_i = np.array([[int(v) for v in row] for row in inv], dtype=np.int64)     # exact: entries are 0, +-1
        rhs = signs * np.array([wts[edges[k][2]] for k in comb], dtype=np.int64)[None, :]
        sols = rhs @ inv_i.T                                                         # exact integer arithmetic
        phi = np.concatenate([np.zeros((len(sols), 1), dtype=np.int64), sols], axis=1)
        ok = (np.abs(phi[:, eb] - phi[:, ea]) <= ew[None, :]).all(axis=1)
        for row in phi[ok]:
            out.add(tuple(int(v) for v in row))
    return out


def _inverse(M):
    """Exact inverse of a square rational matrix, or None if it is singular."""
    k = len(M)
    A = [row[:] + [Fraction(int(i == j)) for j in range(k)] for i, row in enumerate(M)]
    for c in range(k):
        piv = next((r for r in range(c, k) if A[r][c] != 0), None)
        if piv is None:
            return None
        A[c], A[piv] = A[piv], A[c]
        pv = A[c][c]
        A[c] = [a / pv for a in A[c]]
        for r in range(k):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    return [row[k:] for row in A]


# ----------------------------------------------------------------------------- enumerator 4: Parma Polyhedra Library


# The Parma library switches the floating-point unit of the *whole process* to upward rounding when it is loaded,
# and leaves it there (its checked floating-point number types need that; the integer polyhedra used here do not).
# Everything else in the process -- numpy, the C kernels of this repository, even Python's own parsing and printing
# of floats -- assumes round-to-nearest.  Found on 2026-11-26 when an unrelated test (tie counting on the off-lattice
# chain) failed as soon as this module's tests were collected in the same session.  So: the mode is put back to
# round-to-nearest immediately after the import and after every call into the library, and the library's own mode
# is restored only for the duration of a call.
_FE_TONEAREST = 0                       # the value of FE_TONEAREST on x86-64 and aarch64 (glibc)
_ppl_mode = None                        # the rounding mode the library selected when it was loaded


def _libm():
    import ctypes
    import ctypes.util
    return ctypes.CDLL(ctypes.util.find_library("m") or "libm.so.6")


def rounding_is_to_nearest() -> bool:
    """True iff double arithmetic currently rounds to nearest (1 + 2^-53 == 1 and 1 - 2^-54 == 1)."""
    one, tiny = 1.0, 2.0 ** -53
    return one + tiny == one and one - tiny / 2 == one


def _import_ppl():
    global _ppl_mode
    import ppl
    lib = _libm()
    if _ppl_mode is None:
        _ppl_mode = lib.fegetround()
    lib.fesetround(_FE_TONEAREST)
    return ppl


def ppl_available() -> bool:
    try:
        _import_ppl()
        return True
    except Exception:
        return False


def enumerate_ppl(wts):
    """All vertices with the double-description code of the Parma Polyhedra Library (exact integer
    arithmetic).  Requires the optional package ``pplpy``.  The process's rounding mode is round-to-nearest
    again when this function returns (see the comment above)."""
    ppl = _import_ppl()
    lib = _libm()
    lib.fesetround(_ppl_mode)
    try:
        return _enumerate_ppl(ppl, wts)
    finally:
        lib.fesetround(_FE_TONEAREST)


def _enumerate_ppl(ppl, wts):
    C_Polyhedron, Constraint_System, Linear_Expression, Variable = (ppl.C_Polyhedron, ppl.Constraint_System,
                                                                    ppl.Linear_Expression, ppl.Variable)
    L = len(wts)
    n = 1 << L

    def var(x):
        return Linear_Expression(0) if x == 0 else Linear_Expression(Variable(x - 1))

    cs = Constraint_System()
    for (x, y, i) in cube_edges(L):
        cs.insert(var(y) - var(x) <= wts[i])
        cs.insert(var(x) - var(y) <= wts[i])
    poly = C_Polyhedron(cs)
    out = set()
    for g in poly.minimized_generators():
        if not g.is_point():
            raise AssertionError("the polytope is bounded: no rays or lines expected")
        d = int(g.divisor())
        co = [int(c) for c in g.coefficients()]
        co += [0] * (n - 1 - len(co))
        if any(c % d for c in co):
            raise AssertionError("non-integral vertex (contradicts total unimodularity)")
        out.add((0,) + tuple(c // d for c in co))
    return out
