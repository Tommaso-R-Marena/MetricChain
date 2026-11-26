"""Computer-assisted proof of identifiability among all ensembles below the conic threshold,
for two states (Theorem I of docs/geometry/ENSEMBLE_RIGIDITY.md; proof obligation O-2).

Setting: K = 2 chains with n atoms, unit bonds, bond-angle cosine -5/13, rational torsion
half-angle tangents; z = (X_1 | X_2) the UNWEIGHTED stacked configuration in Q^6 (weights only
rescale the blocks).  L is the linear space of symmetric 6 x 6 matrices P with
        e^T P e = c * l_e^2      for all 2n - 3 constrained edge vectors e of z,  c a scalar.
L contains the block projectors E_1, E_2.  A chain that is a linear image A z of the stacked
configuration corresponds to P = A^T A in L of rank <= 3 (with c = 1).

For n = 10 the projective space P(L) has dimension 4 and contains three points of rank <= 3:
[E_1], [E_2], and a structural point at infinity (c = 0): the rank-2 quadric
S = a b^T + b a^T, where a is orthogonal to the stacked bond vectors u_1..u_5 and b to
u_5..u_9 -- every constrained edge vector lies in one of the two hyperplanes.  At a point of
rank <= 2 all 4 x 4 minors vanish to second order, so the local length of the scheme there is
at least 1 + 4 = 5.

Claim checked here, in exact arithmetic with Singular (Groebner basis over Q or F_p):
    the projective scheme  { [P] in P(L) : all 4 x 4 minors of P vanish }
    is zero-dimensional of degree 7.
Since 7 = 1 + 1 + 5, it consists of exactly [E_1], [E_2] (each reduced) and [S] (length 5): the
only solutions with c != 0 are the two block projectors -- over the complex numbers.  The
report (Theorem I) derives from this, by semicontinuity, that the same holds for generic pairs
of chains with 10 atoms, and hence with more.

For n = 11, 12 the script checks degree 2 (no structural point: two hyperplanes cannot contain
ten stacked bond vectors).

Usage: python3 exact_nonlinear_threshold.py [n=10] [seed=0] [char=32003]
       (char = 0: over Q, minutes;  char = p: over F_p, a fraction of a second -- the degree
        over Q is at most the degree over F_p when the scheme over F_p is zero-dimensional, and
        it is at least 7 by the three points, so char = p proves the claim over Q as well)
Requires the computer algebra system Singular on the PATH.
"""
import random
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from geomlib import chain_exact


def nullspace(rows, ncols):
    """Exact basis of the null space of a rational matrix (list of rows)."""
    A = [list(r) for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        A[r] = [x / A[r][c] for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for fcol in free:
        v = [F(0)] * ncols
        v[fcol] = F(1)
        for i, pc in enumerate(piv):
            v[pc] = -A[i][fcol]
        basis.append(v)
    return basis


def solve_in_basis(basis, target):
    """Coordinates of `target` in `basis` (exact), or None."""
    k = len(basis)
    rows = [[basis[b][i] for b in range(k)] + [target[i]] for i in range(len(target))]
    A = [list(r) for r in rows]
    r = 0
    piv = []
    for c in range(k):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None:
            return None
        A[r], A[p] = A[p], A[r]
        A[r] = [x / A[r][c] for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    if any(A[i][k] != 0 for i in range(r, len(A))):
        return None
    return [A[i][k] for i in range(k)]


def setup(n, seed):
    rnd = random.Random(seed)
    cth, sth = F(-5, 13), F(12, 13)
    tors = [[F(rnd.randint(-9, 9), rnd.randint(1, 9)) for _ in range(n - 3)] for _ in range(2)]
    Xs = [chain_exact(n, t, cth, sth) for t in tors]
    Z = [Xs[0][i] + Xs[1][i] for i in range(n)]                      # rows in Q^6
    edges = [([Z[i + 1][c] - Z[i][c] for c in range(6)], F(1)) for i in range(n - 1)]
    edges += [([Z[i + 2][c] - Z[i][c] for c in range(6)], F(36, 13)) for i in range(n - 2)]
    idx = [(i, j) for i in range(6) for j in range(i, 6)]
    rows = [[e[i] * e[j] * (1 if i == j else 2) for (i, j) in idx] + [-l2] for e, l2 in edges]
    basis = nullspace(rows, len(idx) + 1)                              # vectors (P, c)
    def vec_of_block(k):
        P = [[F(1) if (i == j and i // 3 == k) else F(0) for j in range(6)] for i in range(6)]
        return [P[i][j] for (i, j) in idx] + [F(1)]
    pts = [solve_in_basis(basis, vec_of_block(k)) for k in range(2)]
    assert all(p is not None for p in pts), "block projectors are not in L"
    # the structural rank-2 quadric (exists when the bonds can be covered by two hyperplanes)
    struct = None
    if n == 10:
        U = [e for e, _ in edges[:n - 1]]
        a = nullspace(U[0:5], 6)
        b = nullspace(U[4:9], 6)
        assert len(a) == 1 and len(b) == 1
        a, b = a[0], b[0]
        S = [[a[i] * b[j] + b[i] * a[j] for j in range(6)] for i in range(6)]
        assert all(sum(e[i] * S[i][j] * e[j] for i in range(6) for j in range(6)) == 0 for e, _ in edges), \
            "the pair of hyperplanes does not contain all edge vectors"
        struct = solve_in_basis(basis, [S[i][j] for (i, j) in idx] + [F(0)])
        assert struct is not None
        # exact rank of S is 2: a and b are linearly independent
        assert len(nullspace([a, b], 6)) == 4
    return tors, basis, idx, pts, struct


def singular_script(basis, idx, pts, char):
    k = len(basis)
    def poly(i, j):
        t = idx.index((min(i, j), max(i, j)))
        terms = []
        for b in range(k):
            c = basis[b][t]
            if c != 0:
                terms.append(f"({c.numerator}/{c.denominator})*t({b + 1})")
        return "+".join(terms) if terms else "0"
    lines = [f"ring R = {char},(t(1..{k})),dp;", "matrix P[6][6];"]
    for i in range(6):
        for j in range(6):
            lines.append(f"P[{i + 1},{j + 1}] = {poly(i, j)};")
    lines += ["ideal I = minor(P,4);", "ideal G = std(I);",
              'print("DIM=" + string(dim(G)));', 'print("DEG=" + string(mult(G)));']
    for q, a in enumerate(pts):
        gens = []
        for i in range(k):
            for j in range(i + 1, k):
                gens.append(f"({a[i].numerator}/{a[i].denominator})*t({j + 1})-({a[j].numerator}/{a[j].denominator})*t({i + 1})")
        lines.append(f"ideal Q{q} = {','.join(gens)};")
        lines.append(f"Q{q} = std(Q{q});")
        lines.append(f'print("CONTAINS{q}=" + string(size(reduce(I, Q{q}))));')
        lines.append(f'print("POINTDIM{q}=" + string(dim(Q{q})));')
    lines.append('print("SAMEPOINT=" + string(size(reduce(Q0, Q1))));')
    lines.append("quit;")
    return "\n".join(lines)


def main(n=10, seed=0, char=32003):
    if shutil.which("Singular") is None:
        print("Singular not found on the PATH; this exact computation is skipped")
        return 2
    tors, basis, idx, pts, struct = setup(n, seed)
    print(f"K = 2, n = {n}, seed = {seed}: dim L = {len(basis)} (expected 1 + 21 - (2n - 3) = {22 - (2 * n - 3)}),"
          f" char = {char}; structural rank-2 point at infinity: {'yes' if struct else 'no'}")
    script = singular_script(basis, idx, pts + ([struct] if struct else []), char)
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as f:
        f.write(script)
        path = f.name
    out = subprocess.run(["Singular", "-q", path], capture_output=True, text=True, timeout=7200).stdout
    vals = {}
    for line in out.splitlines():
        if "=" in line:
            a, b = line.split("=", 1)
            vals[a.strip()] = b.strip()
    print("   Singular:", vals)
    want = 7 if struct else 2
    ok = (vals.get("DIM") == "1" and vals.get("DEG") == str(want) and vals.get("CONTAINS0") == "0"
          and vals.get("CONTAINS1") == "0" and vals.get("POINTDIM0") == "1" and vals.get("POINTDIM1") == "1"
          and vals.get("SAMEPOINT") != "0" and (not struct or vals.get("CONTAINS2") == "0"))
    if ok and struct:
        print("   OK: zero-dimensional of degree 7 = 1 + 1 + 5; contains [E_1] != [E_2] and the rank-2 point"
              " at infinity (local length >= 5): no other point, and E_1, E_2 are reduced")
    elif ok:
        print("   OK: zero-dimensional of degree 2 and contains [E_1] != [E_2]: exactly the two block"
              " projectors, each reduced")
    else:
        print("   UNEXPECTED (see the values above)")
    return 0 if ok else 1


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:]]
    sys.exit(main(*a))
