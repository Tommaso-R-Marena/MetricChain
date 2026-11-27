"""Exact helpers for GEOMETRY-REQ-0001 (items 1 and 3), written by the Computational Research
Division from the mathematical definitions in docs/geometry/ENSEMBLE_RIGIDITY.md of the Geometric
Inference division (their commit d84a43b).  Nothing here imports or executes their code.

Arithmetic: `fractions.Fraction` / Python integers (exact rationals).  The only optional
dependency is python-flint, used when available for the larger exact ranks (it is a pure
speed-up: the pure-Python fall-back computes the same numbers).

Conventions (ours, chosen to agree with the definitions of the report):

* a chain with n atoms x_0..x_{n-1} in Q^3 has unit bonds u_i = x_{i+1} - x_i (i = 0..n-2), a fixed
  bond angle with cosine COS = -5/13 at every interior atom, i.e. u_{i-1}.u_i = -COS = 5/13, so the
  squared one-three distance is |x_{i+2} - x_i|^2 = 2 - 2 COS = 36/13, and n - 3 torsion angles
  phi_m (m = 0..n-4), the dihedral of the atoms m, m+1, m+2, m+3 (cis = 0);
* a torsion is given by the tangent t of its half angle: cos phi = (1-t^2)/(1+t^2),
  sin phi = 2t/(1+t^2), so that all coordinates are rational when t is;
* the (unweighted) stacked configuration of K chains is z_i = (x_i^(1), ..., x_i^(K)) in Q^{3K};
  the weighted one of the report is z_i D with D = diag(sqrt(w_k) I_3);
* the constrained edge vectors of z are the n-1 bond vectors z_{i+1} - z_i followed by the n-2
  one-three vectors z_{i+2} - z_i;
* a symmetric m x m matrix S is coordinatised by its upper triangle, (i, j) with i <= j in
  lexicographic order; the row of an edge vector e is the vector of coefficients of e^T S e:
  e_i^2 for i = j and 2 e_i e_j for i < j.
"""
from __future__ import annotations

import random
from fractions import Fraction as Fr
from itertools import combinations
from math import gcd

COS = Fr(-5, 13)          # cosine of the bond angle
SIN = Fr(12, 13)          # its sine; COS^2 + SIN^2 = 1
BOND2 = Fr(1)             # squared bond length
ONE3_2 = 2 - 2 * COS      # squared one-three distance, 36/13

try:                      # optional accelerator
    import flint          # type: ignore
    HAVE_FLINT = True
except Exception:         # pragma: no cover - exercised only without python-flint
    flint = None
    HAVE_FLINT = False


# --------------------------------------------------------------------------------- chains
def circle_point(t):
    """(cos, sin) of the angle whose half-angle tangent is the rational t."""
    t = Fr(t)
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def chain_from_tangents(tans, cos=COS, sin=SIN):
    """Atoms of the chain with torsion half-angle tangents `tans` (n = len(tans) + 3 atoms).

    Bond-vector recursion: with p = u_{i-2}, q = u_{i-1} (unit, p.q = -cos) the next bond is
        u_i = -cos q + cos(phi) (-cos q - p) + sin(phi) (p x q).
    (-cos q - p) is orthogonal to q and has length sin; p x q is orthogonal to both and has length
    sin; so |u_i| = 1 and q.u_i = -cos, and phi is the dihedral angle of the four atoms.  No
    division by sin is needed.  x_0 = 0, u_0 = (1, 0, 0), u_1 = (-cos, sin, 0).
    """
    cos, sin = Fr(cos), Fr(sin)
    if cos * cos + sin * sin != 1:
        raise ValueError("cos^2 + sin^2 != 1")
    p = (Fr(1), Fr(0), Fr(0))
    q = (-cos, sin, Fr(0))
    x = [(Fr(0), Fr(0), Fr(0)), p, tuple(p[j] + q[j] for j in range(3))]
    for t in tans:
        c, s = circle_point(t)
        pq = cross(p, q)
        u = tuple(-cos * q[j] + c * (-cos * q[j] - p[j]) + s * pq[j] for j in range(3))
        x.append(tuple(x[-1][j] + u[j] for j in range(3)))
        p, q = q, u
    return x


def check_chain(x, cos=COS):
    """True iff the chain has unit bonds and bond-angle cosine `cos` exactly."""
    n = len(x)
    u = [tuple(x[i + 1][j] - x[i][j] for j in range(3)) for i in range(n - 1)]
    return (all(dot(v, v) == 1 for v in u)
            and all(dot(u[i], u[i + 1]) == -Fr(cos) for i in range(n - 2)))


def dihedral_cos_sin(x, m):
    """The dihedral angle of atoms m..m+3 from the coordinates (independent of the construction).
    With bonds a, b, c (|b| = 1), n1 = a x b, n2 = b x c:
        cos = n1.n2 / (|n1||n2|),   sin = a.n2 / (|n1||n2|).
    Returns the triple (n1.n2, a.n2, |n1|^2 |n2|^2); for our chains |n1||n2| = SIN^2."""
    a = tuple(x[m + 1][j] - x[m][j] for j in range(3))
    b = tuple(x[m + 2][j] - x[m + 1][j] for j in range(3))
    c = tuple(x[m + 3][j] - x[m + 2][j] for j in range(3))
    n1, n2 = cross(a, b), cross(b, c)
    den2 = dot(n1, n1) * dot(n2, n2)          # = sin^4 for our chains
    return dot(n1, n2), dot(a, n2), den2      # caller divides (den2 is a rational square here)


def geometry_witness_tangents(K, n, seed):
    """The torsion half-angle tangents of `witness(K, n, "rational", seed)` of the Geometric
    Inference division's experiments/geometry/exact_conic_rank.py at commit d84a43b, RE-DERIVED
    here (their file was read as text, never executed): a Mersenne-twister `random.Random(seed)`,
    and for each state k = 0..K-1, for each torsion m = 0..n-4, the fraction
    randint(-9, 9) / randint(1, 9) (numerator drawn first)."""
    rnd = random.Random(seed)
    out = []
    for _ in range(K):
        row = []
        for _ in range(n - 3):
            num = rnd.randint(-9, 9)
            den = rnd.randint(1, 9)
            row.append(Fr(num, den))
        out.append(row)
    return out


ENG_SMALL_POOL = 40      # largest number of torsions served by the "distinct values" rule below


def eng_witness_tangents(K, n, index):
    """Witnesses of our own choosing, from a Mersenne twister seeded with the string
    "eng-geometry-req1/K/n/index".

    * If the ensemble has at most ENG_SMALL_POOL = 40 torsions (K (n-3) <= 40): tangents a/b with
      a in {-12..12} except 0, b in {1..7}, |a| != b (no torsion equal to 0, +-90 or 180 degrees),
      no value repeated up to sign inside the ensemble (there are 56 such values up to sign).
    * Otherwise: tangents a/b with a in {-30..30} except 0, b in {1..11}, |a| != b, drawn
      independently (repetitions allowed)."""
    rnd = random.Random(f"eng-geometry-req1/{K}/{n}/{index}")
    out = []
    if K * (n - 3) <= ENG_SMALL_POOL:
        used = set()
        for _ in range(K):
            row = []
            while len(row) < n - 3:
                a = rnd.randint(-12, 12)
                b = rnd.randint(1, 7)
                if a == 0 or abs(a) == b:
                    continue
                t = Fr(a, b)
                if abs(t) in used:
                    continue
                used.add(abs(t))
                row.append(t)
            out.append(row)
        return out
    for _ in range(K):
        row = []
        while len(row) < n - 3:
            a = rnd.randint(-30, 30)
            b = rnd.randint(1, 11)
            if a == 0 or abs(a) == b:
                continue
            row.append(Fr(a, b))
        out.append(row)
    return out


def stack(chains):
    """Unweighted stacked configuration: z_i = concatenation of the i-th atoms."""
    n = len(chains[0])
    assert all(len(c) == n for c in chains)
    return [tuple(v for c in chains for v in c[i]) for i in range(n)]


def edge_vectors(z):
    """Constrained edge vectors (bonds, then one-three vectors) with their squared lengths."""
    n, m = len(z), len(z[0])
    out = [(tuple(z[i + 1][c] - z[i][c] for c in range(m)), BOND2) for i in range(n - 1)]
    out += [(tuple(z[i + 2][c] - z[i][c] for c in range(m)), ONE3_2) for i in range(n - 2)]
    return out


def sym_index(m):
    return [(i, j) for i in range(m) for j in range(i, m)]


def quad_row(e):
    """Coefficients of e^T S e in the coordinates S_ij, i <= j."""
    m = len(e)
    return [e[i] * e[j] * (1 if i == j else 2) for i in range(m) for j in range(i, m)]


def conic_matrix(z):
    """One row per constrained edge vector: the linear form S -> e^T S e on Sym(3K)."""
    return [quad_row(e) for e, _ in edge_vectors(z)]


def integer_configuration(z):
    """Scale each coordinate (column) of the stacked configuration by the least common multiple
    of its denominators: an integer configuration z D, D diagonal and invertible.  The conic
    spaces satisfy N(z D) = D^{-1} N(z) D^{-1}, so the conic matrices of z and z D have the same
    rank; the integer one has much smaller entries after row scaling.  Returns (z D, D)."""
    m = len(z[0])
    dens = []
    for c in range(m):
        d = 1
        for p in z:
            den = Fr(p[c]).denominator
            d = d * den // gcd(d, den)
        dens.append(d)
    return [tuple(int(Fr(p[c]) * dens[c]) for c in range(m)) for p in z], dens


def sym_from_vec(vec, m):
    S = [[0] * m for _ in range(m)]
    for t, (i, j) in enumerate(sym_index(m)):
        S[i][j] = S[j][i] = vec[t]
    return S


def block_projection(K, k):
    """E_k: the orthogonal projection of Q^{3K} onto block k (0-based), as a list of lists."""
    m = 3 * K
    return [[Fr(1) if (i == j and i // 3 == k) else Fr(0) for j in range(m)] for i in range(m)]


def quad_form(S, e):
    m = len(e)
    return sum(S[i][j] * e[i] * e[j] for i in range(m) for j in range(m))


# --------------------------------------------------------------------------------- linear algebra
def integer_rows(rows):
    """Scale each rational row to a primitive integer row (the rank is unchanged)."""
    out = []
    for r in rows:
        r = [Fr(x) for x in r]
        den = 1
        for x in r:
            den = den * x.denominator // gcd(den, x.denominator)
        ints = [int(x * den) for x in r]
        g = 0
        for v in ints:
            g = gcd(g, v)
        out.append([v // g for v in ints] if g > 1 else ints)
    return out


def rref_fraction(rows):
    """Reduced row echelon form over Q (Fractions).  Returns (rref rows, pivot columns)."""
    A = [[Fr(x) for x in r] for r in rows]
    nr = len(A)
    nc = len(A[0]) if A else 0
    piv = []
    r = 0
    for c in range(nc):
        p = next((i for i in range(r, nr) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = 1 / A[r][c]
        A[r] = [x * inv for x in A[r]]
        for i in range(nr):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
        if r == nr:
            break
    return A[:r], piv


def rank_bareiss(rows):
    """Rank over Q of a rational matrix by fraction-free (Bareiss) elimination on integer rows.
    Pure Python integers; exact."""
    A = integer_rows(rows)
    nr = len(A)
    nc = len(A[0]) if A else 0
    r = 0
    prev = 1
    for c in range(nc):
        p = next((i for i in range(r, nr) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        piv = A[r][c]
        Ar = A[r]
        for i in range(r + 1, nr):
            f = A[i][c]
            Ai = A[i]
            A[i] = [(piv * Ai[j] - f * Ar[j]) // prev for j in range(nc)]
        prev = piv
        r += 1
        if r == nr:
            break
    return r


def rank_exact(rows):
    """Rank over Q.  python-flint (fraction-free / multimodular inside FLINT, exact) when
    available, otherwise Bareiss in pure Python.  Both are exact; they are compared in the tests."""
    if not rows:
        return 0
    if HAVE_FLINT:
        return int(flint.fmpz_mat(integer_rows(rows)).rank())
    return rank_bareiss(rows)


def rank_mod_p(rows, p):
    """Rank over F_p of the reduction of a rational matrix whose denominators are prime to p
    (a ZeroDivisionError/ValueError is raised otherwise).  rank_p <= rank_Q always."""
    A = []
    for r in rows:
        A.append([(Fr(x).numerator * pow(Fr(x).denominator, -1, p)) % p for x in r])
    nr = len(A)
    nc = len(A[0]) if A else 0
    r = 0
    for c in range(nc):
        piv = next((i for i in range(r, nr) if A[i][c]), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], -1, p)
        Ar = [(x * inv) % p for x in A[r]]
        A[r] = Ar
        for i in range(r + 1, nr):
            f = A[i][c]
            if f:
                Ai = A[i]
                A[i] = [(Ai[j] - f * Ar[j]) % p for j in range(nc)]
        r += 1
        if r == nr:
            break
    return r


def nullspace_fraction(rows, ncols=None):
    """A basis of the right kernel over Q (from the RREF: one vector per free column, with a 1 in
    its free column).  Returns (basis, pivot columns, free columns)."""
    R, piv = rref_fraction(rows)
    nc = ncols if ncols is not None else len(rows[0])
    free = [c for c in range(nc) if c not in piv]
    basis = []
    for f in free:
        v = [Fr(0)] * nc
        v[f] = Fr(1)
        for r, pc in enumerate(piv):
            v[pc] = -R[r][f]
        basis.append(v)
    return basis, piv, free


def primitive_integer_vector(v):
    return integer_rows([v])[0]


# --------------------------------------------------------------------------------- the pencil of item 1
def ensemble(tangents):
    """Chains and unweighted stacked configuration of the ensemble with the given tangents."""
    chains = [chain_from_tangents(t) for t in tangents]
    return chains, stack(chains)


def linear_system(z):
    """The linear equations e^T P e = |e|^2 of item 1 in UNWEIGHTED coordinates:
    rows A (one per constrained edge vector, 21 = dim Sym(6) columns for K = 2) and right-hand
    sides b (1 for bonds, 36/13 for one-three vectors).

    Relation to the weighted formulation of the request: with D = diag(sqrt(w_k) I_3) the weighted
    stack is zD, its edge vectors are De, and e_w^T P e_w = e^T (D P D) e, |e_w|^2 = sum_k w_k
    |e^(k)|^2 = l_e^2 because every state has the same constrained lengths and sum w_k = 1.  So
    P solves the weighted system iff Pt = D P D solves  e^T Pt e = l_e^2;  P -> D P D is a linear
    isomorphism of Sym(3K) preserving rank, reality and semidefiniteness, and it maps E_k / w_k to
    E_k.  The solution scheme therefore does not depend on the weights."""
    ev = edge_vectors(z)
    return [quad_row(e) for e, _ in ev], [l2 for _, l2 in ev]


def bond_vectors(z):
    """Stacked bond vectors e_i = z_{i+1} - z_i, i = 0..n-2."""
    n, m = len(z), len(z[0])
    return [tuple(z[i + 1][c] - z[i][c] for c in range(m)) for i in range(n - 1)]


def annihilator(vectors, m):
    """Primitive integer basis of {lam in Q^m : lam . v = 0 for all v in vectors}."""
    if not vectors:
        return [[1 if i == j else 0 for j in range(m)] for i in range(m)]
    ker, _, _ = nullspace_fraction([list(v) for v in vectors], ncols=m)
    return [primitive_integer_vector(v) for v in ker]


def sym_outer(lam, mu):
    """lam mu^T + mu lam^T: the quadric (lam . v)(mu . v) up to the factor 2; rank 2 when lam, mu
    are independent."""
    m = len(lam)
    return [[lam[i] * mu[j] + mu[i] * lam[j] for j in range(m)] for i in range(m)]


def in_conic_space(S, z):
    """True iff e^T S e = 0 for every constrained edge vector e of z (S in N(z)), exactly."""
    return all(quad_form(S, e) == 0 for e, _ in edge_vectors(z))


def rank2_families_at_infinity(z):
    """All quadrics of rank 2 in N(z) of the form (lam . v)(mu . v), for the given configuration,
    by exhaustion (exact).

    A rank-2 symmetric matrix over C is lam mu^T + mu lam^T with lam, mu independent, and
    e^T S e = 2 (lam.e)(mu.e).  It vanishes on all constrained edge vectors (bonds e_i and
    one-three vectors e_i + e_{i+1}) iff every pair of consecutive bonds {e_i, e_{i+1}} lies in
    ker(lam) or in ker(mu) (if e_i is killed by lam only and e_{i+1} by mu only, then
    (lam.(e_i+e_{i+1}))(mu.(e_i+e_{i+1})) = (lam.e_{i+1})(mu.e_i) != 0).  So the rank-2 locus of
    P(N(z)) is the union, over the assignments of the n-2 consecutive pairs to lam or mu, of the
    images of P(Ann(Lambda)) x P(Ann(M)), Lambda / M the sets of bonds in the pairs assigned to
    lam / mu.  Returns the non-empty families as dicts with the bond sets, the integer bases of the
    two annihilators and the dimension of the family; assignments are taken up to exchanging lam
    and mu (first pair assigned to lam).  Families contained in a larger listed family are not
    removed.  The list is the whole locus of rank <= 2 in P(N(z)) provided the bond vectors span
    Q^m (bonds_span(z)); otherwise there are, in addition, the quadrics (lam.v)(mu.v) with lam
    orthogonal to every bond and mu arbitrary."""
    m = len(z[0])
    bonds = bond_vectors(z)
    npairs = len(bonds) - 1
    # Shortcut, rigorous: if the bond vectors of a set have rank m modulo a prime they have rank m
    # over Q (rank_p <= rank_Q <= m) and their annihilator is zero.  Otherwise the annihilator is
    # computed exactly.  Both are memoised by bond set.
    p = 2305843009213693951
    bonds_p = [[x % p for x in row] for row in integer_rows(bonds)]
    memo = {}

    def ann(bset):
        key = tuple(bset)
        if key not in memo:
            if len(bset) >= m and _rank_int_mod_p([bonds_p[i] for i in bset], p) == m:
                memo[key] = []
            else:
                memo[key] = annihilator([bonds[i] for i in bset], m)
        return memo[key]

    out = []
    for mask in range(1 << (npairs - 1)):
        assign = [0] + [(mask >> i) & 1 for i in range(npairs - 1)]
        if all(a == 0 for a in assign):
            # all pairs assigned to lam: lam would have to kill every bond (and mu would be
            # arbitrary; this case contains the quadrics of rank 1).  It is empty exactly when
            # the bonds span Q^m, which callers check with bonds_span(z); it is not listed here.
            continue
        Lam = sorted({j for i, a in enumerate(assign) if a == 0 for j in (i, i + 1)})
        Mu = sorted({j for i, a in enumerate(assign) if a == 1 for j in (i, i + 1)})
        annL = ann(Lam)
        if not annL:
            continue
        annM = ann(Mu)
        if annL and annM:
            out.append({"lambda_bonds": Lam, "mu_bonds": Mu, "ann_lambda": annL, "ann_mu": annM,
                        "dimension": len(annL) + len(annM) - 2})
    return out


def bonds_span(z):
    """True iff the stacked bond vectors span Q^m (the configuration spans Q^m affinely); exact."""
    return rank_bareiss([list(b) for b in bond_vectors(z)]) == len(z[0])


def _rank_int_mod_p(rows, p):
    """Rank over F_p of a matrix of integers already reduced modulo p."""
    A = [list(r) for r in rows]
    nr = len(A)
    nc = len(A[0]) if A else 0
    r = 0
    for c in range(nc):
        piv = next((i for i in range(r, nr) if A[i][c]), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], -1, p)
        Ar = [(x * inv) % p for x in A[r]]
        A[r] = Ar
        for i in range(r + 1, nr):
            f = A[i][c]
            if f:
                Ai = A[i]
                A[i] = [(Ai[j] - f * Ar[j]) % p for j in range(nc)]
        r += 1
        if r == nr:
            break
    return r


def pencil_basis(z, K=2, first=()):
    """Integer basis (B_0, B_1, ..., B_r) of the linear span  L = Q E_1 + N(z)  with
    B_0 = E_1 and B_1 = E_2 (the forced points; B_1 - B_0 is the trivial quadric), then the
    matrices of `first` (elements of N(z), e.g. the rank-2 quadric at infinity), then further
    elements of N(z) completing a basis, each scaled to a primitive integer matrix.
    Returns (basis as list of 3K x 3K integer matrices, rank of the linear system, dim N(z)).

    Coordinates: P = sum_i x_i B_i satisfies  e^T P e = (x_0 + x_1) |e|^2  on every constrained
    edge vector.  So h = x_0 + x_1 is the homogenising coordinate: the affine solution space of
    the linear equations is {h = 1} and the hyperplane at infinity is {h = 0} = P(N(z))."""
    m = 3 * K
    A, b = linear_system(z)
    ker, piv, free = nullspace_fraction(A)
    rank = len(piv)
    E = [block_projection(K, k) for k in range(K)]
    idx = sym_index(m)
    # the forced points solve the system exactly
    for k in range(K):
        vec = [E[k][i][j] for (i, j) in idx]
        assert all(sum(a * v for a, v in zip(row, vec)) == rhs for row, rhs in zip(A, b))
    chosen = [[Fr(E[1][i][j] - E[0][i][j]) for (i, j) in idx]]
    for S in first:
        v = [Fr(S[i][j]) for (i, j) in idx]
        assert all(sum(a * x for a, x in zip(row, v)) == 0 for row in A), "not in N(z)"
        assert rank_bareiss(chosen + [v]) == len(chosen) + 1, "prescribed elements dependent"
        chosen.append(v)
    for v in ker:
        if len(chosen) == len(ker):
            break
        if rank_bareiss(chosen + [v]) == len(chosen) + 1:
            chosen.append(v)
    assert len(chosen) == len(ker), "could not complete the basis of N(z)"
    mats = [[[int(x) for x in row] for row in E[0]], [[int(x) for x in row] for row in E[1]]]
    for v in chosen[1:]:
        mats.append(sym_from_vec(primitive_integer_vector(v), m))
    return mats, rank, len(ker)


def forced_point_tangent_ranks(z, K=2):
    """Reducedness of the forced points by the tangent-space criterion.  The rank-<=3 locus of
    Sym(6) is smooth at a rank-3 point P with tangent space {Q : u^T Q v = 0 for u, v in ker P}.
    At E_1 the kernel is block 2, so the Zariski tangent space of the affine solution scheme at
    E_1 is {N in N(z) : N_22 = 0}; it is zero iff N -> N_22 is injective on N(z).  Returns
    (dim N(z), rank of N -> N_22, rank of N -> N_11); the two points are reduced iff both ranks
    equal dim N(z)."""
    m = 3 * K
    A, _ = linear_system(z)
    ker, _, _ = nullspace_fraction(A)
    idx = sym_index(m)
    blocks = []
    for blk in range(K):
        sel = [t for t, (i, j) in enumerate(idx) if i // 3 == blk and j // 3 == blk]
        blocks.append(rank_bareiss([[v[t] for t in sel] for v in ker]) if ker else 0)
    # the tangent space at E_1 uses the block of E_2 and conversely
    return len(ker), blocks[1], blocks[0]


# --------------------------------------------------------------------------------- polynomials
# A homogeneous polynomial in v variables is a dict {exponent tuple: integer coefficient}.
def monomials(v, d):
    """All exponent vectors of degree d in v variables, in a fixed (lexicographic) order."""
    if v == 1:
        return [(d,)]
    out = []
    for a in range(d, -1, -1):
        for rest in monomials(v - 1, d - a):
            out.append((a,) + rest)
    return out


def pmul(f, g):
    h = {}
    for ea, ca in f.items():
        for eb, cb in g.items():
            e = tuple(x + y for x, y in zip(ea, eb))
            h[e] = h.get(e, 0) + ca * cb
    return {e: c for e, c in h.items() if c != 0}


def padd(f, g, sg=1):
    h = dict(f)
    for e, c in g.items():
        h[e] = h.get(e, 0) + sg * c
    return {e: c for e, c in h.items() if c != 0}


def peval(f, point):
    tot = 0
    for e, c in f.items():
        term = c
        for x, a in zip(point, e):
            if a:
                term = term * x ** a
        tot += term
    return tot


def pencil_entries(mats):
    """Entries of the generic matrix sum_i x_i B_i as linear forms (dicts)."""
    v = len(mats)
    m = len(mats[0])
    unit = [tuple(1 if a == b else 0 for b in range(v)) for a in range(v)]
    return [[{unit[a]: mats[a][i][j] for a in range(v) if mats[a][i][j] != 0} for j in range(m)]
            for i in range(m)]


def all_4x4_minors(mats):
    """The 4 x 4 minors of the pencil sum_i x_i B_i (B_i symmetric), as quartic forms in the x_i.
    Returns a list of ((rows, cols), polynomial) for row sets <= column sets (the pencil is
    symmetric, so the minor (I, J) equals the minor (J, I)): 120 minors for 6 x 6."""
    m = len(mats[0])
    ent = pencil_entries(mats)
    sets4 = list(combinations(range(m), 4))
    # 2 x 2 minors, cached
    two = {}

    def minor2(r, c):
        key = (r, c)
        if key not in two:
            two[key] = padd(pmul(ent[r[0]][c[0]], ent[r[1]][c[1]]),
                            pmul(ent[r[0]][c[1]], ent[r[1]][c[0]]), -1)
        return two[key]

    out = []
    for a, I in enumerate(sets4):
        for J in sets4[a:]:
            # Laplace expansion along the first two rows of the minor
            tot = {}
            top, bot = (I[0], I[1]), (I[2], I[3])
            for (p, q) in combinations(range(4), 2):
                rest = [k for k in range(4) if k not in (p, q)]
                sign = -1 if (p + q + 1) % 2 else 1          # (-1)^(0+1+p+q)
                term = pmul(minor2(top, (J[p], J[q])), minor2(bot, (J[rest[0]], J[rest[1]])))
                tot = padd(tot, term, sign)
            out.append(((I, J), tot))
    return out


def macaulay_rows(polys, v, d_from, d_to):
    """Rows of the Macaulay matrix: all products (monomial of degree d_to - d_from) * f as
    coefficient dicts of degree d_to."""
    mons = monomials(v, d_to - d_from)
    rows = []
    for f in polys:
        for mexp in mons:
            rows.append({tuple(a + b for a, b in zip(e, mexp)): c for e, c in f.items()})
    return rows


def dense_rows(rows, v, d):
    mons = monomials(v, d)
    pos = {e: i for i, e in enumerate(mons)}
    out = []
    for f in rows:
        r = [0] * len(mons)
        for e, c in f.items():
            r[pos[e]] = c
        out.append(r)
    return out
