"""(l) Independent replication of the computation behind Theorem I (second checkpoint of the
report): for K = 2 and n atoms, V = { [P] in P(L) : rank P <= 3 },
L = { P in Sym(6) : e^T P e = c l_e^2 on the constrained edge vectors of the unweighted stack }.

Referee's own exact witness (own chain builder, rational torsions), two methods:
 (1) Hilbert function of the ideal of 4x4 minors by Macaulay matrices over F_p (own code):
     HF(d) = #monomials of degree d - rank(Macaulay matrix in degree d); for a finite scheme it
     stabilises at deg V;
 (2) Singular (std, dim, mult) on an input file generated here, over F_32003 and over Q.
Also: Jacobian ranks at [E_1], [E_2] (reduced points) and at the rank-2 point [S] = [ab^T+ba^T].

usage: python3 l_theoremI.py n [seed] [dmax]
"""
import sys
import random
import subprocess
import itertools
from fractions import Fraction as Fr
import numpy as np
from j_exact import exact_chain, to_mod, P as PRIME

p = PRIME


def inv(a):
    return pow(int(a) % p, -1, p)


def nullspace_mod(A):
    """Basis of the right null space over F_p of an integer matrix (list of rows)."""
    A = np.array(A, dtype=np.int64) % p
    nr, nc = A.shape
    piv = []
    r = 0
    for c in range(nc):
        nz = np.nonzero(A[r:, c])[0]
        if len(nz) == 0:
            continue
        q = nz[0] + r
        if q != r:
            A[[r, q]] = A[[q, r]]
        A[r] = A[r] * inv(A[r, c]) % p
        for i in np.nonzero(A[:, c])[0]:
            if i != r:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        piv.append(c)
        r += 1
        if r == nr:
            break
    free = [c for c in range(nc) if c not in piv]
    basis = []
    for f in free:
        v = np.zeros(nc, dtype=np.int64)
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-A[i, f]) % p
        basis.append(v)
    return basis, r


def rank_mod_big(A):
    A = np.array(A, dtype=np.int64) % p
    nr, nc = A.shape
    r = 0
    for c in range(nc):
        nz = np.nonzero(A[r:, c])[0]
        if len(nz) == 0:
            continue
        q = nz[0] + r
        if q != r:
            A[[r, q]] = A[[q, r]]
        A[r] = A[r] * inv(A[r, c]) % p
        rows = np.nonzero(A[r + 1:, c])[0] + r + 1
        if len(rows):
            A[rows] = (A[rows] - np.outer(A[rows, c], A[r])) % p
        r += 1
        if r == nr:
            break
    return r


def det_mod(M):
    M = [[int(x) % p for x in row] for row in M]
    n = len(M)
    d = 1
    for c in range(n):
        q = next((i for i in range(c, n) if M[i][c]), None)
        if q is None:
            return 0
        if q != c:
            M[c], M[q] = M[q], M[c]
            d = -d
        d = d * M[c][c] % p
        iv = inv(M[c][c])
        for i in range(c + 1, n):
            f = M[i][c] * iv % p
            if f:
                M[i] = [(x - f * y) % p for x, y in zip(M[i], M[c])]
    return d % p


def monomials(nv, d):
    """exponent tuples of degree d in nv variables."""
    out = []
    for c in itertools.combinations_with_replacement(range(nv), d):
        e = [0] * nv
        for i in c:
            e[i] += 1
        out.append(tuple(e))
    return out


def witness(n, seed):
    rnd = random.Random(1000 + seed)
    c, s = Fr(5, 13), Fr(12, 13)
    bonds = [Fr(1)] * (n - 1)
    Xs = [exact_chain([Fr(rnd.randint(-9, 9), rnd.randint(1, 7)) for _ in range(n - 3)], c, s, bonds) for _ in range(2)]
    Zq = [[Xs[k][i][j] for k in range(2) for j in range(3)] for i in range(n)]     # unweighted stack, exact
    return Zq


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    dmax = int(sys.argv[3]) if len(sys.argv) > 3 else 9
    Zq = witness(n, seed)
    pairs = [(a, a + 1) for a in range(n - 1)] + [(a, a + 2) for a in range(n - 2)]
    idx = [(a, b) for a in range(6) for b in range(a, 6)]
    # linear system for (vech P, c):  e^T P e - c * l_e^2 = 0,  l_e^2 = |e_block1|^2 (exact)
    rows = []
    for (i, j) in pairs:
        e = [Zq[j][t] - Zq[i][t] for t in range(6)]
        l2 = sum(x * x for x in e[:3])
        assert l2 == sum(x * x for x in e[3:])
        rows.append([to_mod(e[a] * e[b] * (1 if a == b else 2)) for (a, b) in idx] + [(-to_mod(l2)) % p])
    basis, rk = nullspace_mod(rows)
    nv = len(basis)
    print(f"n={n} seed={seed}: {len(pairs)} conditions of rank {rk} on (P, c); dim L = {nv} (expected 25 - 2n = {25 - 2*n}); P(L) = P^{nv-1}")
    Bm = []
    cvals = []
    for v in basis:
        M = np.zeros((6, 6), dtype=np.int64)
        for t, (a, b) in enumerate(idx):
            M[a, b] = M[b, a] = v[t]
        Bm.append(M)
        cvals.append(int(v[-1]))
    # 4x4 minors as quartic forms in t_1..t_nv by interpolation
    mons4 = monomials(nv, 4)
    rnd = random.Random(5)
    npts = len(mons4) + 10
    pts = [[rnd.randrange(p) for _ in range(nv)] for _ in range(npts)]
    V = np.array([[int(np.prod([pow(pt[i], e[i], p) for i in range(nv)], dtype=object) % p) for e in mons4] for pt in pts], dtype=object)
    subsets = list(itertools.combinations(range(6), 4))
    minors_idx = [(I, J) for a, I in enumerate(subsets) for J in subsets[a:]]
    vals = np.zeros((npts, len(minors_idx)), dtype=object)
    for r_, pt in enumerate(pts):
        Pm = sum(int(t) * Bm[a].astype(object) for a, t in enumerate(pt)) % p
        for c_, (I, J) in enumerate(minors_idx):
            vals[r_, c_] = det_mod([[Pm[i][j] for j in J] for i in I])
    # solve V * coef = vals  (mod p) by elimination on the augmented matrix
    aug = np.hstack([V, vals]).astype(np.int64) % p
    nm = len(mons4)
    r = 0
    for c_ in range(nm):
        nz = np.nonzero(aug[r:, c_])[0]
        assert len(nz), "interpolation matrix singular"
        q = nz[0] + r
        if q != r:
            aug[[r, q]] = aug[[q, r]]
        aug[r] = aug[r] * inv(aug[r, c_]) % p
        others = [i for i in np.nonzero(aug[:, c_])[0] if i != r]
        if others:
            aug[others] = (aug[others] - np.outer(aug[others, c_], aug[r])) % p
        r += 1
    assert not aug[nm:, nm:].any(), "minors are not quartic forms (interpolation inconsistent)"
    coef = aug[:nm, nm:].T                                     # minors x monomials(4)
    gens = [cf for cf in coef if cf.any()]
    print(f"   {len(minors_idx)} minors (up to symmetry), {len(gens)} non-zero, spanning a space of dimension {rank_mod_big(np.array(gens))} of quartic forms ({nm} monomials)")
    # Hilbert function via Macaulay matrices
    hf = {}
    for d in range(0, 4):
        hf[d] = len(monomials(nv, d))
    for d in range(4, dmax + 1):
        monsd = monomials(nv, d)
        col = {m: i for i, m in enumerate(monsd)}
        mult = monomials(nv, d - 4)
        rows_ = []
        for g in gens:
            nzg = [(mons4[i], int(g[i])) for i in np.nonzero(g)[0]]
            for mm in mult:
                row = np.zeros(len(monsd), dtype=np.int64)
                for e, cval in nzg:
                    row[col[tuple(a + b for a, b in zip(e, mm))]] = cval
                rows_.append(row)
        A = np.array(rows_)
        # random row compression (keeps the rank with overwhelming probability over F_p)
        if len(A) > 3 * len(monsd):
            rng = np.random.default_rng(d)
            R = rng.integers(0, p, size=(2 * len(monsd) + 50, len(A)), dtype=np.int64)
            # (R @ A) mod p without overflow: process in chunks with object fallback via splitting
            Ahi, Alo = A >> 16, A & 0xFFFF
            Rhi, Rlo = R >> 16, R & 0xFFFF
            comp = np.zeros((R.shape[0], A.shape[1]), dtype=np.int64)
            for (Rp, sh1) in ((Rhi, 16), (Rlo, 0)):
                for (Ap, sh2) in ((Ahi, 16), (Alo, 0)):
                    # entries < 2^16 * 2^16 * rows: accumulate in float-safe chunks
                    part = np.zeros_like(comp)
                    for s0 in range(0, A.shape[0], 16384):
                        part = (part + Rp[:, s0:s0 + 16384] @ Ap[s0:s0 + 16384]) % p
                    comp = (comp + part * pow(2, sh1 + sh2, p)) % p
            A = comp
        hf[d] = len(monsd) - rank_mod_big(A)
        print(f"   degree {d}: {len(monsd)} monomials, Hilbert function of R/I = {hf[d]}", flush=True)
    print("   Hilbert function:", [hf[d] for d in sorted(hf)])
    # points E_1, E_2 (c = 1) and S = ab^T + ba^T (n = 10 only), Jacobian ranks
    # coordinates of a matrix in the basis: solve sum t_a B_a = M mod p
    def coords(M):
        Arows = [[int(Bm[a][i][j]) for a in range(nv)] for (i, j) in idx]
        rhs = [int(M[i][j]) % p for (i, j) in idx]
        aug_ = np.array([r_ + [b_] for r_, b_ in zip(Arows, rhs)], dtype=np.int64)
        ns, rr = nullspace_mod(aug_)
        sol = [v for v in ns if v[-1] != 0]
        if not sol:
            return None
        v = sol[0] * inv(-sol[0][-1]) % p
        return [int(x) for x in v[:-1]]
    E1 = np.diag([1, 1, 1, 0, 0, 0]); E2 = np.diag([0, 0, 0, 1, 1, 1])
    def jac_rank(t0):
        # gradient of each quartic generator at t0
        G = []
        for g in gens:
            grad = [0] * nv
            for i in np.nonzero(g)[0]:
                e = mons4[i]
                for v_ in range(nv):
                    if e[v_]:
                        term = int(g[i]) * e[v_]
                        for u in range(nv):
                            term = term * pow(t0[u], e[u] - (1 if u == v_ else 0), p) % p
                        grad[v_] = (grad[v_] + term) % p
            G.append(grad)
        return rank_mod_big(np.array(G))
    for name, M in (("E_1", E1), ("E_2", E2)):
        t0 = coords(M)
        print(f"   {name} in L: {t0 is not None}; rank of the Jacobian of the minors there = {jac_rank(t0) if t0 else None} (reduced point iff = {nv - 1})")
    if n == 10:
        U = [[to_mod(Zq[a + 1][t] - Zq[a][t]) for t in range(6)] for a in range(9)]
        a_, _ = nullspace_mod(U[:5]); b_, _ = nullspace_mod(U[4:])
        a_, b_ = a_[0], b_[0]
        S = (np.outer(a_, b_) + np.outer(b_, a_)) % p
        t0 = coords(S)
        print(f"   S = ab^T + ba^T in L: {t0 is not None}; Jacobian rank there = {jac_rank(t0) if t0 else None} (0 => local length >= {nv})")
    # Singular cross-check
    def singular(char):
        names = ",".join(f"t{i+1}" for i in range(nv))
        ent = []
        for i in range(6):
            for j in range(6):
                terms = [f"{int(Bm[a][i][j])}*t{a+1}" for a in range(nv) if Bm[a][i][j]]
                ent.append("+".join(terms) if terms else "0")
        code = (f"ring r = {char},({names}),dp;\nmatrix P[6][6] = {','.join(ent)};\nideal I = minor(P,4);\n"
                f"ideal G = std(I);\nprint(\"dim=\"+string(dim(G)));\nprint(\"mult=\"+string(mult(G)));\nquit;\n")
        try:
            out = subprocess.run(["Singular", "-q"], input=code, capture_output=True, text=True, timeout=1200)
            return out.stdout.strip().replace("\n", " ")
        except Exception as e:
            return f"Singular failed: {e}"
    print(f"   Singular over F_{p} (basis of L computed mod p here): {singular(p)}  [affine cone: dim 1 <=> finite scheme; mult = degree]")
    # affine chart c = 1: number of solutions (with multiplicity, over the algebraic closure)
    names = ",".join(f"t{i+1}" for i in range(nv))
    ent = []
    for i in range(6):
        for j in range(6):
            terms = [f"{int(Bm[a][i][j])}*t{a+1}" for a in range(nv) if Bm[a][i][j]]
            ent.append("+".join(terms) if terms else "0")
    cform = "+".join(f"{c_}*t{a+1}" for a, c_ in enumerate(cvals) if c_)
    code = (f"ring r = {p},({names}),dp;\nmatrix P[6][6] = {','.join(ent)};\nideal I = minor(P,4), {cform}-1;\n"
            f"ideal G = std(I);\nprint(\"affine: dim=\"+string(dim(G))+\" vdim=\"+string(vdim(G)));\nquit;\n")
    out = subprocess.run(["Singular", "-q"], input=code, capture_output=True, text=True, timeout=3000)
    print("   Singular, chart c = 1:", out.stdout.strip().replace("\n", " "), " [vdim = number of (complex) rank<=3 points with c != 0, with multiplicity]")


if __name__ == "__main__":
    main()
