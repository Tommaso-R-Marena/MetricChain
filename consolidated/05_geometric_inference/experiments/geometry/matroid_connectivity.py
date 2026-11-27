"""Algebraic matroids of distance measurements on the chain variety (answer to the Ensemble
division's questions E-G2, E-G3; Theorem J of docs/geometry/ENSEMBLE_RIGIDITY.md).

Features: squared distances d_ij^2, (i, j) in a pattern F, as functions of the n - 3 torsions of
a chain with fixed bond lengths and angles.  Their algebraic matroid M(F) has rank function
r(J) = generic rank of the Jacobian of (d_ij^2)_{ij in J} with respect to the torsions; it is
the contraction of the rigidity matroid by the constrained edges, for this bond geometry.

The Ensemble division's Theorem E5/Corollary E6 (applied to the chain variety): if M(F) is
connected and no feature is constant, a generic finite ensemble of chains -- any number of
states -- is determined by the one-dimensional laws of the features up to the fibres of the
feature map; if M(F) is not connected there are chimeras.

Rigour.  The Jacobian is evaluated exactly at a rational witness and reduced modulo a prime.
The matroid M_p of the reduced matrix is a weak image of the generic matroid M (independent in
M_p implies independent in M).  Hence: (i) if rank M_p = n - 3 and M_p is connected, M is
connected; (ii) if all features are independent in M_p, M is free (and not connected when
there are at least two features).  Other outcomes are reported as "undetermined by this
witness".  Connectivity of M_p is decided through the fundamental graph of a basis.
"""
import sys
import random
from fractions import Fraction
from geomlib import Mod, chain_exact, cross


def jacobian_rows(n, pairs, seed=0, cth=Fraction(-5, 13), sth=Fraction(12, 13)):
    rnd = random.Random(seed)
    Mod.p = 2147483629
    p = Mod.p
    tors = [Fraction(rnd.randint(-9, 9), rnd.randint(1, 9)) for _ in range(n - 3)]
    X = [[c.v for c in pt] for pt in chain_exact(n, tors, Mod(cth), Mod(sth))]
    rows = []
    for (i, j) in pairs:
        row = []
        for m in range(n - 3):
            if j < m + 3 or i >= m + 3:
                row.append(0)
                continue
            ax = [(X[m + 2][c] - X[m + 1][c]) % p for c in range(3)]
            rel = [(X[j][c] - X[m + 2][c]) % p for c in range(3)]
            dx = cross(ax, rel)
            diff = [(X[j][c] - X[i][c]) % p for c in range(3)]
            row.append(2 * sum(diff[c] * dx[c] for c in range(3)) % p)
        rows.append(row)
    return rows, p


def analyse(rows, p):
    """Row-reduce; return rank, basis (row indices), and for each non-basis row the set of basis
    rows in its fundamental circuit."""
    m = len(rows)
    ncols = len(rows[0]) if rows else 0
    # reduce each row against the current basis, tracking coefficients
    basis = []            # list of (pivot col, reduced row, combination dict over original rows)
    fund = {}
    for r in range(m):
        v = list(rows[r])
        comb = {r: 1}
        for (pc, bv, bc) in basis:
            if v[pc] % p:
                f = v[pc]
                v = [(x - f * y) % p for x, y in zip(v, bv)]
                for k, c in bc.items():
                    comb[k] = (comb.get(k, 0) - f * c) % p
        pc = next((c for c in range(ncols) if v[c] % p), None)
        if pc is None:
            # dependency: sum_k comb[k] * row_k = 0 ; the circuit is the support of comb
            fund[r] = sorted(k for k, c in comb.items() if c % p and k != r)
        else:
            inv = pow(v[pc], -1, p)
            v = [(x * inv) % p for x in v]
            comb = {k: (c * inv) % p for k, c in comb.items()}
            basis.append((pc, v, comb))
    # the "basis rows" are those that entered the basis; comb of a basis vector involves only
    # earlier basis rows and itself, so supports of dependencies are within basis rows + r
    basis_rows = [max(bc.keys()) for (_, _, bc) in basis]
    return len(basis), basis_rows, fund


def connected(m, basis_rows, fund):
    """Connectivity of the matroid via the fundamental graph (elements = vertices; a non-basis
    element is joined to the basis elements of its fundamental circuit)."""
    parent = list(range(m))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for e, circ in fund.items():
        for b in circ:
            parent[find(e)] = find(b)
    comps = {}
    for e in range(m):
        comps.setdefault(find(e), []).append(e)
    return list(comps.values())


def pattern(n, seps):
    return [(i, i + s) for s in seps for i in range(n - s)]


def report(name, n, pairs, seeds=(0, 1, 2)):
    best = None
    for seed in seeds:
        rows, p = jacobian_rows(n, pairs, seed)
        rk, basis_rows, fund = analyse(rows, p)
        comps = connected(len(pairs), basis_rows, fund)
        cand = (rk, -len(comps), comps)
        if best is None or cand[:2] > best[:2]:
            best = cand
    rk, _, comps = best
    m = len(pairs)
    if rk == m:
        verdict = "FREE (all features independent): not connected" if m > 1 else "one feature"
    elif rk == n - 3 and len(comps) == 1:
        verdict = "CONNECTED (proved by this witness)"
    else:
        verdict = f"undetermined by these witnesses: rank {rk}, {len(comps)} components of the witness matroid"
    print(f"{name:34s} n={n:2d}  features={m:3d}  rank={rk:2d} (torsions {n-3:2d})  {verdict}")
    return rk, comps


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    print("squared distances at sequence separations S, as functions of the torsions")
    for seps in ([3], [4], [5], [3, 4], [3, 5], [4, 5], [3, 6], [4, 6], [5, 6], [3, 4, 5], [6, 7]):
        report(f"S = {seps}", n, pattern(n, seps))
    report("all pairs", n, [(i, j) for i in range(n) for j in range(i + 3, n)])
    report("S = [3] + end-to-end", n, pattern(n, [3]) + [(0, n - 1)])
    report("end-to-end distances (0,j), j>=3", n, [(0, j) for j in range(3, n)])
    rnd = random.Random(5)
    allp = [(i, j) for i in range(n) for j in range(i + 3, n)]
    for k in (n - 3, n, 2 * n):
        report(f"{k} random pairs", n, sorted(rnd.sample(allp, k)))


# ---------------------------------------------------------------------------------------
# Two rigid bodies and the bars between them (the Ensemble division's smallest case of O3).
# Features: |a_i - g b_j|^2 for g in SE(3); the Jacobian row of a bar at the identity pose is
# the Pluecker vector (direction, moment) of its line, so the matroid is the linear matroid of
# the lines a_i b_j.  Exact rational points, rank modulo a prime.
def two_body(p, q, seed=0, bars=None):
    rnd = random.Random(seed)
    P = 2147483629
    A = [[rnd.randint(-50, 50) for _ in range(3)] for _ in range(p)]
    B = [[rnd.randint(-50, 50) for _ in range(3)] for _ in range(q)]
    bars = bars or [(i, j) for i in range(p) for j in range(q)]
    rows = []
    for (i, j) in bars:
        d = [B[j][c] - A[i][c] for c in range(3)]
        m = cross(A[i], d)
        rows.append([x % P for x in d + m])
    rk, basis_rows, fund = analyse(rows, P)
    comps = connected(len(bars), basis_rows, fund)
    return len(bars), rk, len(comps)


def two_body_report():
    print("two rigid bodies, bars between p points of one and q points of the other (matroid of the bar lines, rank <= 6)")
    for (p, q) in [(1, 3), (2, 2), (2, 3), (3, 3), (2, 4), (3, 4), (4, 4)]:
        m, rk, nc = two_body(p, q)
        verdict = "free: not connected" if rk == m and m > 1 else ("CONNECTED" if nc == 1 and rk == min(6, rk) and rk < m else f"{nc} components in the witness")
        print(f"   p={p} q={q}: bars={m:2d} rank={rk}  {verdict}")


if __name__ == "__main__":
    two_body_report()
