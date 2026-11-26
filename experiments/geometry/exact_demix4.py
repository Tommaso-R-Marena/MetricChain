"""Computer-assisted proof that the degree-4 certificate of Proposition 6.2 holds generically
(docs/geometry/ENSEMBLE_RIGIDITY.md, section 6.2, Theorem I').

For K conformations of a chain with n atoms (unit bonds, one bond angle), let z be the
unweighted stacked configuration in F^{3K} (the weights only rescale the blocks, which does
not change ranks) and

    L = { (P, c) : P symmetric 3K x 3K,  e^T P e = c * l_e^2  for the 2n - 3 constrained edges }.

L contains the K block identities E_k (with c = 1).  Let J_4 be the span of the 4 x 4 minors
of P, restricted to L, inside the quartic forms on L (dimension nmon = C(m + 3, 4), m = dim L).
All minors vanish at the K linearly independent points E_k, so dim J_4 <= nmon - K, and
Proposition 6.2 says: if dim J_4 = nmon - K ("h_4 = K") then the only matrices of rank <= 3 in
L, real or complex, are the multiples of the E_k, and the K-state mixture is identifiable
among all ensembles -- for this chain and for every chain that extends it.

What this script proves, for each line "PROVED": a witness with rational torsion parameters
at which h_4 = K.  The set of torsions with h_4 = K is then a non-empty Zariski-open subset
of the torus, for this n and (Proposition 6.2 (a')) for every larger n.

Rigour.  The witness has coordinates in Q (bond angle with rational cos and sin) or in
Q(sqrt 2) (tetrahedral angle).  Everything is reduced modulo a prime p < 2^16 (sqrt 2 mapped
to a square root of 2 mod p), and
    rank_p(values of the minors at S points of L_p)
        <= rank_p(coefficients of the minors on L_p)
        <= rank_Q(coefficients of the minors on L)  =  dim J_4  <=  nmon - K.
The second inequality needs dim L_p = dim L, which holds because the constraint matrix has
full row rank 2n - 3 modulo p (checked; then also over Q): a basis of L over the local ring
reduces to a basis of L_p, and a ring homomorphism to a field cannot increase a rank.
So "rank_p = nmon - K" proves h_4 = K at the witness.  Only lower bounds on ranks are used:
unlucky evaluation points or an unlucky prime can make the script fail, never prove a false
statement.

Arithmetic.  All entries are integers in [0, p), p = 65521 or 65519 < 2^16.  Matrix products
are done in float64: every partial sum is an integer below (number of terms) * p^2 < 2^53
for fewer than 2^21 terms, hence exact.  The 4 x 4 minors are computed in int64 by Laplace
expansion along two rows.  `--verify` recomputes the pivot rows with int64 arithmetic only,
at fresh points and a second prime, and finds their rank by an independent elimination.

Usage:
  exact_demix4.py                         K = 2, n = 11 and K = 3, n = 17 (both bond angles; seconds)
  exact_demix4.py K n [geometry [seed]]   one case (geometry: rational | tetrahedral)
  exact_demix4.py --verify K n            with the independent int64 cross-check (slow for K >= 4)
  exact_demix4.py --mutate                two planted errors (structural point ignored; principal minors
                                          only): neither may prove; exit status 1 means both were caught
"""
import itertools
import math
import random
import sys
import time
from fractions import Fraction

import numpy as np

from geomlib import Mod, chain_exact, tonelli

PRIMES = (65521, 65519)           # both are 1 or 7 mod 8, so 2 is a square


def witness(K, n, geometry, seed, p):
    """Unweighted stacked configuration of K exact chains, reduced mod p, and l_2^2 mod p."""
    old_p, Mod.p = Mod.p, p
    try:
        return _witness(K, n, geometry, seed, p)
    finally:
        Mod.p = old_p


def _witness(K, n, geometry, seed, p):
    rnd = random.Random(seed)
    if geometry == "rational":            # cos = -5/13, sin = 12/13   (112.62 degrees)
        cth, sth = Mod(Fraction(-5, 13)), Mod(Fraction(12, 13))
    elif geometry == "tetrahedral":       # cos = -1/3, sin = 2 sqrt(2)/3   (109.47 degrees)
        r2 = tonelli(2, p)
        cth, sth = Mod(Fraction(-1, 3)), Mod(2 * r2) / 3
    else:
        raise ValueError(geometry)
    tors = [[Fraction(rnd.randint(-9, 9), rnd.randint(1, 9)) for _ in range(n - 3)]
            for _ in range(K)]
    Xs = [chain_exact(n, t, cth, sth) for t in tors]
    Z = np.array([[Xs[k][i][j].v for k in range(K) for j in range(3)] for i in range(n)],
                 dtype=np.int64)
    ell2 = (2 - 2 * cth).v                # |x_{i+2} - x_i|^2 = 2 - 2 cos(theta)
    return tors, Z, ell2


def nullspace_mod_p(A, p):
    """Rank and a basis of the kernel of the integer matrix A modulo p (reduced echelon form)."""
    A = np.array(A, dtype=np.int64) % p
    nr, nc = A.shape
    piv = []
    r = 0
    for c in range(nc):
        rows = np.flatnonzero(A[r:, c]) + r
        if rows.size == 0:
            continue
        i = rows[0]
        if i != r:
            A[[r, i]] = A[[i, r]]
        A[r] = (A[r] * pow(int(A[r, c]), -1, p)) % p
        for j in np.flatnonzero(A[:, c]):
            if j != r:
                A[j] = (A[j] - A[j, c] * A[r]) % p
        piv.append(c)
        r += 1
        if r == nr:
            break
    free = [c for c in range(nc) if c not in piv]
    basis = np.zeros((len(free), nc), dtype=np.int64)
    for b, f in enumerate(free):
        basis[b, f] = 1
        for i, c in enumerate(piv):
            basis[b, c] = (-A[i, f]) % p
    return r, basis


def space_L(Z, ell2, p):
    """Basis of L mod p as symmetric matrices; checks full row rank and that the K block
    identities lie in L (which also checks the witness: unit bonds, equal bond angles)."""
    n, N = Z.shape
    idx = [(i, j) for i in range(N) for j in range(i, N)]
    E = [(Z[i + 1] - Z[i]) % p for i in range(n - 1)] + [(Z[i + 2] - Z[i]) % p for i in range(n - 2)]
    ell = [1] * (n - 1) + [ell2] * (n - 2)
    A = [[int(e[i] * e[j] * (1 if i == j else 2) % p) for (i, j) in idx] + [(-l) % p]
         for e, l in zip(E, ell)]
    rank, ker = nullspace_mod_p(A, p)
    assert rank == 2 * n - 3, f"constraint matrix has rank {rank} < 2n - 3 = {2 * n - 3} mod p"
    A = np.array(A, dtype=np.int64)
    for k in range(N // 3):
        v = np.array([1 if (i == j and i // 3 == k) else 0 for (i, j) in idx] + [1], dtype=np.int64)
        assert not ((A @ v) % p).any(), "a block identity is not in L: the witness is not a chain ensemble"
    B = np.zeros((len(ker), N, N), dtype=np.int64)
    for a, v in enumerate(ker):
        for t, (i, j) in enumerate(idx):
            B[a, i, j] = B[a, j, i] = v[t]
    return B, ker


def coordinates_in_L(Q, c, ker, p):
    """Coordinates of (Q, c) in the basis `ker` of L (rows of the reduced kernel basis have a 1
    in their own free column and 0 in the other free columns).  Asserts that (Q, c) is in L."""
    N = len(Q)
    v = np.array([Q[i, j] for i in range(N) for j in range(i, N)] + [c], dtype=np.int64) % p
    free = FREE_COLUMNS(ker)
    q = v[free]
    assert not ((q @ ker - v) % p).any(), "the matrix is not in L"
    return q


def FREE_COLUMNS(ker):
    """The free column of each kernel basis vector: the columns where the basis restricts to
    the identity."""
    nb, nc = ker.shape
    cols = []
    for b in range(nb):
        for c in range(nc):
            if ker[b, c] == 1 and not ker[:, c].sum() - 1:
                if c not in cols:
                    cols.append(c)
                    break
        else:
            raise AssertionError("kernel basis is not in reduced form")
    sub = ker[:, cols]
    assert (sub == np.eye(nb, dtype=np.int64)).all()
    return cols


def structural_points(Z, p, samples=6, max_runs=5, seed=0):
    """Matrices Q = a b^T + b a^T of rank 2 in L with c = 0 ("structural points"): the bonds
    are covered by runs R_1, R_2, ... of consecutive bonds, consecutive runs sharing one bond,
    with a orthogonal to the bonds of the odd runs and b to those of the even runs.  Then every
    constrained edge vector (bond or sum of two consecutive bonds) is orthogonal to a or to b,
    so e^T Q e = 0.  Such runs exist iff n <= 6K - 2.  Returns a list of (a, b)."""
    n, N = Z.shape
    U = [(Z[i + 1] - Z[i]) % p for i in range(n - 1)]
    nb = n - 1
    rng = np.random.default_rng(4000 + seed)
    out = []

    def perp(indices):
        _, ker = nullspace_mod_p([U[i] for i in indices], p)
        return ker

    def rec(breaks):
        # breaks = [0, j_1, ..., j_r = nb - 1]: runs [breaks[i], breaks[i + 1]]
        runs = [list(range(breaks[i], breaks[i + 1] + 1)) for i in range(len(breaks) - 1)]
        ia = sorted(set(i for r in runs[0::2] for i in r))
        ib = sorted(set(i for r in runs[1::2] for i in r))
        if len(ia) <= N - 1 and len(ib) <= N - 1 and len(runs) >= 2:
            A, Bk = perp(ia), perp(ib)
            if len(A) and len(Bk):
                k = 1 if len(A) == 1 and len(Bk) == 1 else samples * (len(A) + len(Bk))
                for _ in range(k):
                    a = (rng.integers(1, p, size=len(A)) @ A) % p
                    b = (rng.integers(1, p, size=len(Bk)) @ Bk) % p
                    out.append((a, b))

    def extend(breaks):
        if breaks[-1] == nb - 1:
            rec(breaks)
            return
        if len(breaks) - 1 >= max_runs:
            return
        for j in range(breaks[-1] + 1, nb):
            # prune: conditions already imposed on a and on b must stay below N
            trial = breaks + [j]
            runs = [range(trial[i], trial[i + 1] + 1) for i in range(len(trial) - 1)]
            if len(set(i for r in runs[0::2] for i in r)) > N - 1:
                continue
            if len(set(i for r in runs[1::2] for i in r)) > N - 1:
                continue
            extend(trial)

    extend([0])
    return out


def jet_rank(points, ker, p, D):
    """Rank modulo p of the functionals f -> d_v f(Q) (v in L) on forms of degree D on L, for
    the structural points Q = a b^T + b a^T given by `points`; monomial coordinates."""
    if not points:
        return 0
    m = len(ker)
    Ex = np.array([[mono.count(i) for i in range(m)]
                   for mono in itertools.combinations_with_replacement(range(m), D)], dtype=np.int64)
    rows = []
    for a, b in points:
        Q = (np.outer(a, b) + np.outer(b, a)) % p
        assert rank_int64(Q, p) == 2
        q = coordinates_in_L(Q, 0, ker, p)                      # c(Q) = 0
        pw = np.ones((m, D + 1), dtype=np.int64)
        for k in range(1, D + 1):
            pw[:, k] = (pw[:, k - 1] * q) % p
        for v in range(m):
            val = Ex[:, v].copy()                               # factor alpha_v
            for i in range(m):
                e = Ex[:, i] - (1 if i == v else 0)
                val = (val * pw[i, np.maximum(e, 0)]) % p
            rows.append(val)                                    # zero where alpha_v = 0
    return rank_int64(np.array(rows), p)


# ---- 4 x 4 minors by Laplace expansion along the first two rows of the row set --------------
SPLITS = (((0, 1), (2, 3), 1), ((0, 2), (1, 3), -1), ((0, 3), (1, 2), 1),
          ((1, 2), (0, 3), 1), ((1, 3), (0, 2), -1), ((2, 3), (0, 1), 1))


class Minors:
    def __init__(self, B, T, p):
        """B: basis of L (m, N, N); T: evaluation points (S, m).  Precomputes all 2 x 2 minors
        of P(t_s) = sum_a T[s, a] B[a] modulo p."""
        self.p = p
        m, N, _ = B.shape
        S = len(T)
        P = (T @ B.reshape(m, N * N)) % p                    # (S, N*N), entries < p, sums < m p^2
        P = np.ascontiguousarray(P.T).reshape(N, N, S)
        self.N, self.S = N, S
        self.pairs = list(itertools.combinations(range(N), 2))
        self.pair_index = {pr: i for i, pr in enumerate(self.pairs)}
        c1 = np.array([a for a, b in self.pairs])
        c2 = np.array([b for a, b in self.pairs])
        self.m2 = np.empty((len(self.pairs), len(self.pairs), S), dtype=np.int32)
        for i, (r1, r2) in enumerate(self.pairs):
            self.m2[i] = (P[r1][c1] * P[r2][c2] - P[r1][c2] * P[r2][c1]) % p
        self.combos = list(itertools.combinations(range(N), 4))
        nb = len(self.combos)
        self.idx1 = np.empty((nb, 6), dtype=np.int64)
        self.idx2 = np.empty((nb, 6), dtype=np.int64)
        for b, Bset in enumerate(self.combos):
            for j, (u, v, _) in enumerate(SPLITS):
                self.idx1[b, j] = self.pair_index[(Bset[u[0]], Bset[u[1]])]
                self.idx2[b, j] = self.pair_index[(Bset[v[0]], Bset[v[1]])]

    def rows(self, ia, cols=None):
        """Values (mod p, int64) of the minors with row set combos[ia] and column sets
        combos[b], b in cols (default: all b >= ia), at the S points."""
        A = self.combos[ia]
        cols = np.arange(ia, len(self.combos)) if cols is None else np.asarray(cols)
        R12 = self.m2[self.pair_index[(A[0], A[1])]].astype(np.int64)
        R34 = self.m2[self.pair_index[(A[2], A[3])]].astype(np.int64)
        out = np.zeros((len(cols), self.S), dtype=np.int64)
        for j, (_, _, sign) in enumerate(SPLITS):
            out += sign * ((R12[self.idx1[cols, j]] * R34[self.idx2[cols, j]]) % self.p)
        return out % self.p


def det_mod_p(Mx, p):
    """Determinant of a small integer matrix modulo p (Python integers; for self-tests)."""
    Mx = [[int(x) % p for x in r] for r in Mx]
    n = len(Mx)
    det = 1
    for c in range(n):
        piv = next((r for r in range(c, n) if Mx[r][c]), None)
        if piv is None:
            return 0
        if piv != c:
            Mx[c], Mx[piv] = Mx[piv], Mx[c]
            det = -det
        det = det * Mx[c][c] % p
        inv = pow(Mx[c][c], -1, p)
        for r in range(c + 1, n):
            f = Mx[r][c] * inv % p
            if f:
                Mx[r] = [(x - f * y) % p for x, y in zip(Mx[r], Mx[c])]
    return det % p


# ---- streaming reduced row echelon form modulo p, exact in float64 ---------------------------
class Echelon:
    def __init__(self, ncols, p, capacity):
        assert p < 2 ** 16 and max(ncols, capacity) < 2 ** 21      # exactness of float64 products
        self.p = p
        self.E = np.zeros((capacity, ncols))
        self.piv = np.zeros(capacity, dtype=np.int64)
        self.rank = 0

    def add(self, R):
        """Reduce the rows R (float64 integers in [0, p)) against the basis; append what is new.
        Returns the indices (within R) of the rows that produced new pivots."""
        p, r = self.p, self.rank
        R = np.array(R, dtype=np.float64)
        if r:
            R -= R[:, self.piv[:r]] @ self.E[:r]
            np.mod(R, p, out=R)
        new_piv, new_rows = [], []
        for i in range(len(R)):
            nz = np.flatnonzero(R[i])
            if nz.size == 0:
                continue
            c = int(nz[0])
            R[i] = np.mod(R[i] * pow(int(R[i, c]), -1, p), p)
            col = R[:, c].copy()
            col[i] = 0
            rows = np.flatnonzero(col)
            if rows.size:
                R[rows] = np.mod(R[rows] - np.outer(col[rows], R[i]), p)
            new_piv.append(c)
            new_rows.append(i)
            if r + len(new_piv) == len(self.E):
                break
        k = len(new_piv)
        if k == 0:
            return []
        Nw = R[new_rows]
        for s in range(0, r, 2048):                              # keep the old rows reduced
            blk = slice(s, min(s + 2048, r))
            C = self.E[blk][:, new_piv]
            if C.any():
                self.E[blk] = np.mod(self.E[blk] - C @ Nw, p)
        self.E[r:r + k] = Nw
        self.piv[r:r + k] = new_piv
        self.rank += k
        return new_rows


def rank_int64(A, p):
    """Rank modulo p by plain elimination in int64 (independent of the float64 path)."""
    A = np.array(A, dtype=np.int64) % p
    nr, nc = A.shape
    r = 0
    for c in range(nc):
        rows = np.flatnonzero(A[r:, c]) + r
        if rows.size == 0:
            continue
        i = rows[0]
        if i != r:
            A[[r, i]] = A[[i, r]]
        A[r] = (A[r] * pow(int(A[r, c]), -1, p)) % p
        rows = rows[rows != r]
        A[rows] = (A[rows] - np.outer(A[rows, c], A[r])) % p
        r += 1
        if r == nr:
            break
    return r


def certify(K, n, geometry="rational", seed=0, p=PRIMES[0], chunk=128, principal_only=False,
            verbose=False, order_seed=1, structural=True):
    """Returns (proved, info).  proved = True means: at this witness
        rank_p(minors) + rank_p(first-order jets at the structural points) = nmon - K,
    which proves that the matrices of rank <= 3 in L with c != 0 are the multiples of the K
    block identities (Proposition 6.2 (b) if there are no structural points, (h) otherwise)."""
    t0 = time.time()
    tors, Z, ell2 = witness(K, n, geometry, seed, p)
    B, ker = space_L(Z, ell2, p)
    m, N = len(B), 3 * K
    nmon = math.comb(m + 3, 4)
    pts = structural_points(Z, p) if structural else []
    jets = jet_rank(pts, ker, p, 4)
    target = nmon - K - jets
    S = nmon + 8
    rng = np.random.default_rng(1000 + seed)
    T = rng.integers(0, p, size=(S, m), dtype=np.int64)
    mn = Minors(B, T, p)
    ech = Echelon(S, p, target)
    order = np.random.default_rng(order_seed).permutation(len(mn.combos))
    selected, done = [], 0
    for ia in order:
        cols = np.array([ia]) if principal_only else np.arange(ia, len(mn.combos))
        rows = mn.rows(ia, cols)
        for s in range(0, len(rows), chunk):
            new = ech.add(rows[s:s + chunk])
            selected += [(int(ia), int(cols[s + i])) for i in new]
            if ech.rank == target:
                break
        done += len(rows)
        if verbose:
            print(f"   {done} minors, rank {ech.rank} of {target} [{time.time() - t0:.0f}s]", flush=True)
        if ech.rank == target:
            break
    info = {"K": K, "n": n, "geometry": geometry, "seed": seed, "p": p, "dim_L": m, "nmon": nmon,
            "rank": ech.rank, "target": target, "minors_used": done, "selected": selected,
            "tors": tors, "time": time.time() - t0, "jets": jets, "structural_points": len(pts)}
    return ech.rank == target, info


def verify(info, p2=PRIMES[1]):
    """Independent check of a positive result: the pivot rows, recomputed with int64 arithmetic
    at fresh points and another prime, have rank nmon - K by an int64 elimination."""
    K, n = info["K"], info["n"]
    tors, Z, ell2 = witness(K, n, info["geometry"], info["seed"], p2)
    assert tors == info["tors"]
    B, ker = space_L(Z, ell2, p2)
    m = len(B)
    nmon = math.comb(m + 3, 4)
    jets = jet_rank(structural_points(Z, p2), ker, p2, 4)
    assert jets == info["jets"]
    S = nmon + 8
    T = np.random.default_rng(77).integers(0, p2, size=(S, m), dtype=np.int64)
    mn = Minors(B, T, p2)
    by_a = {}
    for ia, ib in info["selected"]:
        by_a.setdefault(ia, []).append(ib)
    A = np.vstack([mn.rows(ia, ibs) for ia, ibs in by_a.items()])
    return rank_int64(A, p2) == nmon - K - jets


def self_test(p=PRIMES[0]):
    """The Laplace minors agree with determinants computed with Python integers."""
    rng = np.random.default_rng(5)
    N, m, S = 7, 4, 5
    B = rng.integers(0, p, size=(m, N, N), dtype=np.int64)
    B = (B + B.transpose(0, 2, 1)) % p
    T = rng.integers(0, p, size=(S, m), dtype=np.int64)
    mn = Minors(B, T, p)
    P = (np.einsum("sa,aij->sij", T, B)) % p
    for ia in (0, 7, 20, 34):
        vals = mn.rows(ia)
        for off, ib in enumerate(range(ia, len(mn.combos))):
            for s in (0, 3):
                sub = P[s][np.ix_(mn.combos[ia], mn.combos[ib])]
                assert det_mod_p(sub, p) == int(vals[off, s]), (ia, ib, s)
    return True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    assert self_test()
    if "--mutate" in flags:
        # two planted errors, each of which must fail to prove
        ok1, i1 = certify(2, 10, structural=False)          # ignore the structural point
        ok2, i2 = certify(3, 17, principal_only=True)       # principal minors only
        print(f"mutation 1 (structural point ignored), K = 2, n = 10: rank {i1['rank']}, needed {i1['target']}: "
              f"{'PROVED (not caught)' if ok1 else 'not proved, as it should be'}")
        print(f"mutation 2 (principal minors only), K = 3, n = 17: rank {i2['rank']}, needed {i2['target']}: "
              f"{'PROVED (not caught)' if ok2 else 'not proved, as it should be'}")
        sys.exit(0 if (ok1 or ok2) else 1)                  # exit 1 = both planted errors were caught
    if args:
        K, n = int(args[0]), int(args[1])
        geoms = [args[2]] if len(args) > 2 else ["rational"]
        seed = int(args[3]) if len(args) > 3 else 0
        cases = [(K, n, g, seed) for g in geoms]
    else:
        cases = [(2, 10, "rational", 0), (2, 10, "tetrahedral", 0),
                 (2, 11, "rational", 0), (2, 11, "tetrahedral", 0),
                 (3, 16, "rational", 0), (3, 16, "tetrahedral", 0),
                 (3, 17, "rational", 0), (3, 17, "tetrahedral", 0)]
    all_ok = True
    for K, n, g, seed in cases:
        ok, info = certify(K, n, g, seed, verbose=(K >= 4))
        line = (f"{g:11s} K = {K}, n = {n}: dim L = {info['dim_L']}, quartic forms {info['nmon']}, "
                f"rank_p = {info['rank']}, jets at {info['structural_points']} structural points: {info['jets']} "
                f"(p = {info['p']}; {info['minors_used']} minors read) [{info['time']:.0f}s]")
        if ok and "--verify" in flags:
            t0 = time.time()
            v = verify(info)
            line += f"; int64 cross-check at p = {PRIMES[1]}: {'agrees' if v else 'DISAGREES'} [{time.time() - t0:.0f}s]"
            ok &= v
        print(line + (f"   PROVED: h_4 = K + {info['jets']}" if ok else "   not proved"), flush=True)
        all_ok &= ok
    print("ALL PROVED" if all_ok else "SOME NOT PROVED")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
