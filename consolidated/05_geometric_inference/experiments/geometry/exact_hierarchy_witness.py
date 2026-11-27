"""Exact witness for Theorem E(d) of docs/geometry/ENSEMBLE_RIGIDITY.md.

Claim proved here, in rational arithmetic: for the six points

    X = (0,0,0), (1,0,0), (1,2,0), (3,1,2), (2,-1,3), (4,2,1)

with E0 = bonds {i,i+1} and 1-3 pairs {i,i+2} (9 pairs) and F = {14, 25, 36, 16} (1-based),
  (1) the rigidity matrix of the 13 bars of F u E0 has rank 12 = 3*6 - 6, so the space of
      equilibrium stresses is one-dimensional;
  (2) the stress matrix has rank 2 = n - 4 and is INDEFINITE (two explicit vectors give the
      quadratic form opposite signs; equivalently the second elementary symmetric function of
      its eigenvalues, the sum of the principal 2x2 minors, is negative);
  (3) the E0 edge vectors of X lie on no conic: the 9 x 6 conic system has rank 6, N(X) = 0;
  (4) X spans space, and no bond angle is 0 or pi.
All four are open conditions on X, so they hold at algebraically generic configurations near
X; for those, (1)-(2) give global rigidity (Connelly 2005; Gortler-Healy-Thurston 2010) and
exclude universal rigidity (Gortler-Thurston 2014: a generic universally rigid framework has
a positive semidefinite stress matrix of rank n - d - 1), and Theorem E(c) (n = 6, so that
realizable data = semidefinite relaxation) turns "not universally rigid" into "not
F-second-moment rigid".

The witness was found by the referee of GEOMETRY-REV-0001 (experiments/geometry/review1/
g_hierarchy.py); this script is an independent implementation of the check.
Exit code 0 iff all four hold.
"""
import sys
from fractions import Fraction as Fr
from itertools import combinations

X = [(0, 0, 0), (1, 0, 0), (1, 2, 0), (3, 1, 2), (2, -1, 3), (4, 2, 1)]
if "--mutate" in sys.argv:              # a positive semidefinite neighbour found by the referee
    X = [(0, 0, 0), (1, 1, 0), (3, 0, 1), (2, 2, 3), (0, 3, 1), (1, 4, 4)]
n = len(X)
X = [tuple(Fr(c) for c in p) for p in X]
E0 = [(i, i + 1) for i in range(n - 1)] + [(i, i + 2) for i in range(n - 2)]
F = [(0, 3), (1, 4), (2, 5), (0, 5)]
G = E0 + F


def rank(rows):
    rows = [list(r) for r in rows]
    rk, col, ncol = 0, 0, len(rows[0])
    while rk < len(rows) and col < ncol:
        piv = next((r for r in range(rk, len(rows)) if rows[r][col] != 0), None)
        if piv is None:
            col += 1
            continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        pv = rows[rk][col]
        rows[rk] = [a / pv for a in rows[rk]]
        for r in range(len(rows)):
            if r != rk and rows[r][col] != 0:
                f = rows[r][col]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[rk])]
        rk += 1
        col += 1
    return rk


def nullvector(cols):
    """A non-zero rational vector w with sum_j w_j cols[j] = 0 (the space is 1-dimensional)."""
    m, k = len(cols[0]), len(cols)
    A = [[cols[j][i] for j in range(k)] for i in range(m)]
    piv_cols, r = [], 0
    for c in range(k):
        piv = next((i for i in range(r, m) if A[i][c] != 0), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        pv = A[r][c]
        A[r] = [a / pv for a in A[r]]
        for i in range(m):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        piv_cols.append(c)
        r += 1
    free = [c for c in range(k) if c not in piv_cols]
    assert len(free) == 1, f"stress space has dimension {len(free)}"
    w = [Fr(0)] * k
    w[free[0]] = Fr(1)
    for i, c in enumerate(piv_cols):
        w[c] = -A[i][free[0]]
    return w


def diff(i, j):
    return [a - b for a, b in zip(X[i], X[j])]


# (1) rigidity matrix: one row per bar, 3n columns
R = []
for (i, j) in G:
    row = [Fr(0)] * (3 * n)
    d = diff(i, j)
    for c in range(3):
        row[3 * i + c] = d[c]
        row[3 * j + c] = -d[c]
    R.append(row)
rk_rig = rank(R)

# (2) the stress: omega with sum_e omega_e R_e = 0
omega = nullvector(R)
Om = [[Fr(0)] * n for _ in range(n)]
for w, (i, j) in zip(omega, G):
    Om[i][i] += w
    Om[j][j] += w
    Om[i][j] -= w
    Om[j][i] -= w
rk_Om = rank(Om)
e2 = sum(Om[i][i] * Om[j][j] - Om[i][j] * Om[j][i] for i, j in combinations(range(n), 2))
diag = [Om[i][i] for i in range(n)]
# equilibrium: Om X = 0 and Om 1 = 0
eq = all(sum(Om[i][j] * X[j][c] for j in range(n)) == 0 for i in range(n) for c in range(3)) \
    and all(sum(Om[i]) == 0 for i in range(n))

# (3) conic system of the E0 edge vectors on Sym(3)
C = []
for (i, j) in E0:
    e = diff(i, j)
    C.append([e[a] * e[b] * (1 if a == b else 2) for a in range(3) for b in range(a, 3)])
rk_conic = rank(C)

# (4) spanning; bond angles
rk_aff = rank([diff(i, 0) for i in range(1, n)])
def cross_nonzero(u, v):
    return any(u[a] * v[b] - u[b] * v[a] != 0 for a, b in ((0, 1), (0, 2), (1, 2)))
angles_ok = all(cross_nonzero(diff(i + 1, i), diff(i + 2, i + 1)) for i in range(n - 2))

indefinite = rk_Om == 2 and e2 < 0
print(f"rank of the rigidity matrix (13 bars): {rk_rig} (want 12)")
print(f"stress (normalised to last free coordinate = 1): {[str(w) for w in omega]}")
print(f"equilibrium checked exactly: {eq}")
print(f"rank of the stress matrix: {rk_Om} (want 2 = n - 4)")
print(f"sum of principal 2x2 minors e2 = {e2} ({'negative: indefinite' if e2 < 0 else 'not negative'})")
print(f"diagonal of the stress matrix: {[str(d) for d in diag]}")
print(f"rank of the E0 conic system: {rk_conic} (want 6)")
print(f"affine rank: {rk_aff} (want 3); bond angles non-degenerate: {angles_ok}")
ok = rk_rig == 12 and eq and indefinite and rk_conic == 6 and rk_aff == 3 and angles_ok
print("WITNESS OK" if ok else "WITNESS FAILED")
sys.exit(0 if ok else 1)
