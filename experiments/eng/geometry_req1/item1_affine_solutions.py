"""GEOMETRY-REQ-0001, item 1, validation: the AFFINE solutions of
    rank P <= 3,  e^T P e = |e|^2 on the constrained edge vectors
for two-state ensembles, with the same pipeline at n = 9 (where further solutions must appear) and
at n = 10, 11 (where only the two forced points remain).

Run from the repository root:

    python experiments/eng/geometry_req1/item1_affine_solutions.py           # about 12 min
    python experiments/eng/geometry_req1/item1_affine_solutions.py --quick   # main witness, 3 min

Output: experiments/eng/geometry_req1/results/item1_affine_solutions.json

Three layers, kept apart in the output:

 A. MODULAR (exact arithmetic in F_p, 61..63-bit primes).  With J the ideal of the 4 x 4 minors
    on the pencil (v homogeneous variables, h = x_0 + x_1), A_7 = S_7 / J_7 from the Macaulay matrix
    of degree 7.  The image of h^k S_{7-k} in A_7 stabilises (k = 3, 4) at a space V whose
    dimension m is the number of affine solutions counted with multiplicity (the part of the scheme
    at infinity is killed by a power of h, on the affine part h is invertible).  On V the operators
    "multiplication by x_i / h" are computed, checked to commute, and the characteristic polynomial
    of a random combination is factored: it is squarefree iff the affine scheme over F_p is reduced.
    A random combination of 3 x 3 minors is checked to be invertible on V: every affine point has
    rank exactly 3.
    What this proves about Q: see the report; in short, an upper bound on affine solutions over Q
    does NOT follow from a modular count alone, a lower bound follows from layer C.

 B. NUMERICAL (float64): the same construction in floating point (SVD null space of the Macaulay
    matrix, eigenvalues of the multiplication operators), for several scalings of h, followed by
    Newton polishing.  This only produces candidates.

 C. CERTIFIED (ball arithmetic, python-flint / Arb, 400 bits): each candidate is refined and
    proved to be a genuine solution by the Krawczyk test on the square system
        F_e(S, B) = (a_e + B b_e)^T S (a_e + B b_e) - l_e^2 = 0,   e = (a_e, b_e) the 15 edges,
    in the unknowns S (symmetric 3 x 3) and B (3 x 3), which parametrises the symmetric matrices
    P = [[S, S B], [B^T S, B^T S B]] of rank <= 3 (chart "12"), or the same with the two blocks
    exchanged (chart "21").  The data a_e, b_e, l_e^2 are the exact rationals.  K(X) inside the
    interior of the box X proves: exactly one solution in X.  Real solutions are certified with
    real-centred boxes (the system is real, so the unique solution in a conjugation-invariant box
    is real).  Signs of tr S, e_2(S), det S on the box decide semidefiniteness rigorously
    (P = [I, B]^T S [I, B] has the inertia of S); det S != 0 on the box certifies rank 3; an entry
    of P with imaginary part bounded away from 0 certifies a non-real solution.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402

import enslib as el  # noqa: E402

try:
    import flint  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit("this script needs python-flint (pip install python-flint): %s" % exc)

PRIMES = [2305843009213693951, 4611686018427387847, 9223372036854775783]
PIN = "d84a43b"
D = 7


# ============================================================================== A. modular
def unit(v, i):
    return tuple(1 if a == i else 0 for a in range(v))


def affine_part_mod_p(polys, v, p, rng_seed=7):
    red = [{e: c % p for e, c in f.items()} for f in polys]
    mons4 = el.monomials(v, 4)
    R4, r4 = flint.nmod_mat(el.dense_rows(red, v, 4), p).rref()
    R4l = R4.tolist()
    basis4 = [{mons4[j]: int(c) for j, c in enumerate(R4l[i]) if int(c)} for i in range(r4)]
    monsD = el.monomials(v, D)
    posD = {e: i for i, e in enumerate(monsD)}
    rows = el.dense_rows(el.macaulay_rows(basis4, v, 4, D), v, D)
    R, r = flint.nmod_mat(rows, p).rref()
    Rl = R.tolist()[:r]
    piv = []
    for row in Rl:
        for j, c in enumerate(row):
            if int(c):
                piv.append(j)
                break
    pivset = set(piv)
    nonpiv = [j for j in range(len(monsD)) if j not in pivset]
    RD = flint.nmod_mat([[int(c) for c in row] for row in Rl], p)
    out = {"HF_degree_7": len(monsD) - r}

    def reduce(vecs):
        T = flint.nmod_mat(vecs, p)
        Tp = flint.nmod_mat([[row[j] for j in piv] for row in vecs], p)
        Tl = (T - Tp * RD).tolist()
        return [[int(row[j]) for j in nonpiv] for row in Tl]

    def dense(f):
        row = [0] * len(monsD)
        for e, c in f.items():
            row[posD[e]] = c % p
        return row

    def pw(f, k):
        g = {tuple([0] * v): 1}
        for _ in range(k):
            g = {e: c % p for e, c in el.pmul(g, f).items()}
        return g

    h = {unit(v, 0): 1, unit(v, 1): 1}
    ranks = {}
    for k in range(1, 5):
        hk = pw(h, k)
        redk = reduce([dense(el.pmul(hk, {m: 1})) for m in el.monomials(v, D - k)])
        ranks[k] = int(flint.nmod_mat(redk, p).rank())
    out["rank_of_h^k_S_(7-k)_in_A_7"] = {str(k): ranks[k] for k in ranks}
    m = ranks[4]
    out["affine_degree_m"] = m
    out["stable"] = ranks[3] == ranks[4]

    mons3 = el.monomials(v, 3)
    h4, h3 = pw(h, 4), pw(h, 3)
    Hc = reduce([dense(el.pmul(h4, {mm: 1})) for mm in mons3])
    # a basis of V among the classes of h^4 g, g a cubic monomial
    Rt, rk = flint.nmod_mat(Hc, p).transpose().rref()
    bcols = []
    for row in Rt.tolist()[:rk]:
        for j, c in enumerate(row):
            if int(c):
                bcols.append(j)
                break
    Hb = flint.nmod_mat([Hc[j] for j in bcols], p)
    Rb, rk2 = Hb.rref()
    ccols = []
    for row in Rb.tolist()[:rk2]:
        for j, c in enumerate(row):
            if int(c):
                ccols.append(j)
                break
    Hinv = flint.nmod_mat([[Hc[j][c] for c in ccols] for j in bcols], p).inv()

    def operator(ell):
        Lc = reduce([dense(el.pmul(h3, el.pmul(ell, {mons3[j]: 1}))) for j in bcols])
        M = flint.nmod_mat([[row[c] for c in ccols] for row in Lc], p) * Hinv
        ok = (M * Hb).tolist() == flint.nmod_mat(Lc, p).tolist()
        return M, ok

    ops, oks = [], []
    for i in range(v):
        M, ok = operator({unit(v, i): 1})
        ops.append(M)
        oks.append(ok)
    out["operators_well_defined"] = all(oks)
    out["operators_commute"] = all((ops[i] * ops[j]).tolist() == (ops[j] * ops[i]).tolist()
                                   for i in range(v) for j in range(i))
    ident = flint.nmod_mat([[1 if a == b else 0 for b in range(m)] for a in range(m)], p)
    out["h_acts_as_identity"] = (ops[0] + ops[1]).tolist() == ident.tolist()
    rnd = random.Random(rng_seed)
    coeffs = [rnd.randrange(1, p) for _ in range(v)]
    Mc = flint.nmod_mat(m, m, p)
    for c, M in zip(coeffs, ops):
        Mc = Mc + M * flint.nmod_mat([[c if a == b else 0 for b in range(m)] for a in range(m)], p)
    cp = Mc.charpoly()
    fac = cp.factor()[1]
    out["charpoly_degree"] = int(cp.degree())
    out["charpoly_factor_degrees_with_multiplicity"] = sorted([int(f.degree()), int(e)] for f, e in fac)
    out["affine_scheme_reduced_mod_p"] = all(int(e) == 1 for _, e in fac)
    out["forced_points_among_roots"] = (int(cp(coeffs[0])) == 0 and int(cp(coeffs[1])) == 0)
    return out, ops


def rank3_check_mod_p(mats, ops, p, rng_seed=11):
    """A random combination of the 20 principal 3 x 3 minors of the pencil, evaluated on the
    operators, is invertible on V  =>  no affine point has rank <= 2.  (A symmetric matrix of rank
    r over a field of characteristic != 2 has a non-zero principal minor of order r, so the
    principal minors of order 3 vanish simultaneously exactly on the matrices of rank <= 2.)"""
    from itertools import combinations
    m = ops[0].nrows()
    v = len(ops)
    rnd = random.Random(rng_seed)

    def scal(c):
        return flint.nmod_mat([[c % p if a == b else 0 for b in range(m)] for a in range(m)], p)

    ent = {}

    def entry(i, j):
        if (i, j) not in ent:
            tot = flint.nmod_mat(m, m, p)
            for a in range(v):
                c = mats[a][i][j] % p
                if c:
                    tot = tot + ops[a] * scal(c)
            ent[(i, j)] = ent[(j, i)] = tot
        return ent[(i, j)]

    tot = flint.nmod_mat(m, m, p)
    for I in combinations(range(6), 3):
        a = [[entry(i, j) for j in I] for i in I]
        det = (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
               - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
               + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
        tot = tot + det * scal(rnd.randrange(1, p))
    return int(tot.det()) != 0


# ============================================================================== B. numerical
IU = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]


def numeric_candidates(z, m_expected, taus=(1, 3, 10, 30, 100, 300, 1000, 3000, 1e4, 3e4, 1e5), combos=4):
    """Candidate affine solutions (6 x 6 complex matrices) by the floating-point eigenvalue
    method; candidates only."""
    A, b = el.linear_system(z)
    Af = np.array([[float(x) for x in r] for r in A])
    idx = el.sym_index(6)
    _, _, Vt = np.linalg.svd(Af)
    ker = Vt[len(A):]

    def tomat(vec):
        S = np.zeros((6, 6))
        for t, (i, j) in enumerate(idx):
            S[i, j] = S[j, i] = vec[t]
        return S

    E1 = np.diag([1, 1, 1, 0, 0, 0.0])
    Nk = [tomat(k) for k in ker]
    Nk = [M / np.linalg.norm(M) for M in Nk]
    v = 1 + len(Nk)
    mons = el.monomials(v, D)
    pos = {e: i for i, e in enumerate(mons)}
    mons3 = el.monomials(v, 3)
    un = [unit(v, a) for a in range(v)]

    def shift(mexp, add):
        return tuple(a + b for a, b in zip(mexp, add))

    # The minors in the coordinates P = x_0 E_1 + sum_k x_k N_k, once; with E_1 replaced by
    # E_1 / tau the coefficient of a monomial x^beta is multiplied by tau^(-beta_0).
    mons4 = el.monomials(v, 4)
    pos4 = {e: i for i, e in enumerate(mons4)}
    polys1 = [f for _, f in el.all_4x4_minors([E1] + Nk)]
    C1 = np.zeros((len(polys1), len(mons4)))
    for r, f in enumerate(polys1):
        for e, c in f.items():
            C1[r, pos4[e]] = c
    deg0 = np.array([e[0] for e in mons4], dtype=float)
    # column of (cubic monomial) * (quartic monomial) among the septic monomials
    col = np.array([[pos[shift(m3, m4)] for m4 in mons4] for m3 in mons3])
    nf = len(polys1)

    out = []
    for tau in taus:
        # coordinates: P = x_0 E_1 / tau + sum_k x_k N_k, so h = x_0 / tau
        Ct = C1 * (float(tau) ** (-deg0))[None, :]
        M = np.zeros((len(mons3) * nf, len(mons)))
        for a in range(len(mons3)):
            M[a * nf:(a + 1) * nf, col[a]] = Ct
        M /= np.linalg.norm(M, axis=1)[:, None]
        Rq = np.linalg.qr(M, mode="r")
        _, s2, Vt2 = np.linalg.svd(Rq)
        tol = 1e-9 * s2[0]
        nullity = int((s2 < tol).sum())
        K = Vt2[len(mons) - nullity:].T
        h4 = (4,) + (0,) * (v - 1)
        h3 = (3,) + (0,) * (v - 1)
        T4 = np.array([K[pos[shift(mm, h4)], :] for mm in mons3])
        Ut, st, Vtt = np.linalg.svd(T4)
        r = min(m_expected, len(st))
        Ti = [np.array([K[pos[shift(shift(mm, h3), un[i])], :] for mm in mons3]) for i in range(v)]
        Ur, Vr, Sr = Ut[:, :r], Vtt[:r].T, st[:r]
        Mi = [(Ur.T @ T @ Vr) / Sr[:, None] for T in Ti]
        rng = np.random.default_rng(0)
        for _ in range(combos):
            c = rng.normal(size=v)
            w, V = np.linalg.eig(sum(ci * Mm for ci, Mm in zip(c, Mi)))
            try:
                Vinv = np.linalg.inv(V)
            except np.linalg.LinAlgError:
                continue
            coords = np.array([np.diag(Vinv @ Mm @ V) for Mm in Mi]).T
            for row in coords:
                P = E1.astype(complex).copy()
                for k in range(1, v):
                    P = P + tau * row[k] * Nk[k - 1]
                if np.isfinite(P).all():
                    out.append((P, nullity))
    return out


def edge_arrays(z, chart):
    ev = el.edge_vectors(z)
    a = [[x for x in e[:3]] for e, _ in ev]
    b = [[x for x in e[3:]] for e, _ in ev]
    if chart == "21":
        a, b = b, a
    return a, b, [l for _, l in ev]


def FJ_float(S, B, Aa, Bb, L2):
    g = Aa + Bb @ B.T
    Sg = g @ S.T
    F = np.einsum("ei,ei->e", g, Sg) - L2
    J = np.zeros((15, 15), dtype=complex)
    for t, (i, j) in enumerate(IU):
        J[:, t] = g[:, i] * g[:, j] * (1 if i == j else 2)
    J[:, 6:] = 2 * np.einsum("ei,ej->eij", Sg, Bb).reshape(15, 9)
    return F, J


def polish_float(P, z, chart):
    """Newton in float64 in the given chart; returns (x, cond) with x = (S upper triangle, B)."""
    a, b, l2 = edge_arrays(z, chart)
    Aa = np.array([[float(x) for x in r] for r in a])
    Bb = np.array([[float(x) for x in r] for r in b])
    L2 = np.array([float(x) for x in l2])
    if chart == "12":
        S = P[:3, :3].astype(complex)
        B = np.linalg.solve(S, P[:3, 3:])
    else:
        S = P[3:, 3:].astype(complex)
        B = np.linalg.solve(S, P[3:, :3])
    for _ in range(60):
        F, J = FJ_float(S, B, Aa, Bb, L2)
        try:
            dx = np.linalg.solve(J, F)
        except np.linalg.LinAlgError:
            return None
        if not np.isfinite(dx).all():
            return None
        for t, (i, j) in enumerate(IU):
            S[i, j] -= dx[t]
            if i != j:
                S[j, i] -= dx[t]
        B -= dx[6:].reshape(3, 3)
        if np.abs(dx).max() < 1e-13 * (1 + max(np.abs(S).max(), np.abs(B).max())):
            break
    F, J = FJ_float(S, B, Aa, Bb, L2)
    if not np.isfinite(F).all() or np.abs(F).max() > 1e-7 * (1 + np.abs(S).max()):
        return None
    x = np.concatenate([[S[i, j] for (i, j) in IU], B.reshape(9)])
    return x, np.linalg.cond(J)


def P_from_x_float(x, chart):
    S = np.zeros((3, 3), dtype=complex)
    for t, (i, j) in enumerate(IU):
        S[i, j] = S[j, i] = x[t]
    B = x[6:].reshape(3, 3)
    top = np.hstack([S, S @ B])
    bot = np.hstack([B.T @ S, B.T @ S @ B])
    P = np.vstack([top, bot])
    if chart == "21":
        perm = [3, 4, 5, 0, 1, 2]
        P = P[np.ix_(perm, perm)]
    return P


# ============================================================================== C. certified
def arb_q(x):
    return flint.arb(flint.fmpq(x.numerator, x.denominator))


class Certifier:
    """Krawczyk test for the square system in one chart, in ball arithmetic."""

    def __init__(self, z, chart, prec=400):
        flint.ctx.prec = prec
        a, b, l2 = edge_arrays(z, chart)
        assert len(a) == 15, "the square system exists for n = 9 only (15 edges, 15 unknowns)"
        self.chart = chart
        self.a = [[flint.acb(arb_q(x)) for x in r] for r in a]
        self.b = [[flint.acb(arb_q(x)) for x in r] for r in b]
        self.l2 = [flint.acb(arb_q(x)) for x in l2]

    def FJ(self, x):
        """x: list of 15 acb.  Returns (F list, J as list of lists)."""
        S = [[None] * 3 for _ in range(3)]
        for t, (i, j) in enumerate(IU):
            S[i][j] = S[j][i] = x[t]
        B = [[x[6 + 3 * i + j] for j in range(3)] for i in range(3)]
        F, J = [], []
        for e in range(15):
            g = [self.a[e][i] + sum(B[i][j] * self.b[e][j] for j in range(3)) for i in range(3)]
            Sg = [sum(S[i][j] * g[j] for j in range(3)) for i in range(3)]
            F.append(sum(g[i] * Sg[i] for i in range(3)) - self.l2[e])
            row = [g[i] * g[j] * (1 if i == j else 2) for (i, j) in IU]
            row += [2 * Sg[i] * self.b[e][j] for i in range(3) for j in range(3)]
            J.append(row)
        return F, J

    def refine(self, x0, steps=12):
        """Newton iteration on midpoints at working precision."""
        x = [flint.acb(complex(c).real, complex(c).imag) for c in x0]
        for _ in range(steps):
            F, J = self.FJ(x)
            dx = flint.acb_mat(J).solve(flint.acb_mat([[f] for f in F]))
            x = [flint.acb((x[i] - dx[i, 0]).real.mid(), (x[i] - dx[i, 0]).imag.mid()) for i in range(15)]
        return x

    def krawczyk(self, xmid, real, rad_exp=-60):
        """Returns (ok, box) where box is the list of 15 acb balls X; ok means K(X) is contained
        in the interior of X, hence exactly one solution of the system lies in X."""
        if real:
            xmid = [flint.acb(c.real.mid(), 0) for c in xmid]
        scale = max(1.0, max(float(abs(c.real.mid())) + float(abs(c.imag.mid())) for c in xmid))
        r = flint.arb(scale) * flint.arb(2) ** rad_exp
        rball = flint.arb(0, r)
        X = [flint.acb(c.real + rball, c.imag + rball) for c in xmid]
        F0, J0 = self.FJ(xmid)
        Y = flint.acb_mat(J0).inv()
        Y = flint.acb_mat([[flint.acb(Y[i, j].real.mid(), Y[i, j].imag.mid()) for j in range(15)]
                           for i in range(15)])
        _, JX = self.FJ(X)
        ident = flint.acb_mat([[1 if i == j else 0 for j in range(15)] for i in range(15)])
        Cm = ident - Y * flint.acb_mat(JX)
        YF = Y * flint.acb_mat([[f] for f in F0])
        dX = flint.acb_mat([[flint.acb(rball, rball)] for _ in range(15)])
        corr = Cm * dX
        ok = True
        for i in range(15):
            ki = -YF[i, 0] + corr[i, 0]            # K(X)_i - xmid_i
            for part in (ki.real, ki.imag):
                if not (abs(part.mid()) + part.rad() < r):
                    ok = False
        return ok, X

    def P_balls(self, X):
        S = [[None] * 3 for _ in range(3)]
        for t, (i, j) in enumerate(IU):
            S[i][j] = S[j][i] = X[t]
        B = [[X[6 + 3 * i + j] for j in range(3)] for i in range(3)]
        SB = [[sum(S[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
        BSB = [[sum(B[k][i] * SB[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
        P = [[None] * 6 for _ in range(6)]
        for i in range(3):
            for j in range(3):
                P[i][j] = S[i][j]
                P[i][3 + j] = SB[i][j]
                P[3 + j][i] = SB[i][j]
                P[3 + i][3 + j] = BSB[i][j]
        if self.chart == "21":
            perm = [3, 4, 5, 0, 1, 2]
            P = [[P[perm[i]][perm[j]] for j in range(6)] for i in range(6)]
        return P, S


def sign_of(ball):
    if ball > 0:
        return 1
    if ball < 0:
        return -1
    return 0


def certify_all(z, candidates, prec=400, rad_exp=-60):
    """Polish (float64 Newton, in the better conditioned of the two charts), refine (Newton at
    `prec` bits) and certify (Krawczyk) the candidates; duplicates are removed on the polished
    floats.  Returns one record per distinct candidate."""
    sols = []
    certs = {"12": Certifier(z, "12", prec), "21": Certifier(z, "21", prec)}
    seen = []
    E = [np.diag([1, 1, 1, 0, 0, 0]), np.diag([0, 0, 0, 1, 1, 1])]
    # stage 1: polish every candidate in both charts, keep the distinct limits
    for P0, _ in candidates:
        for chart in ("12", "21"):
            blk = P0[:3, :3] if chart == "12" else P0[3:, 3:]
            if abs(np.linalg.det(blk)) < 1e-14 * max(1.0, np.abs(blk).max()) ** 3:
                continue
            pol = polish_float(P0, z, chart)
            if pol is None:
                continue
            Pf = P_from_x_float(pol[0], chart)
            if not any(np.abs(Pf - Q).max() < 1e-6 * (1 + np.abs(Q).max()) for Q in seen):
                seen.append(Pf)
    # stage 2: certify each distinct limit in its better conditioned chart
    for Pf0 in seen:
        best = None
        for chart in ("12", "21"):
            blk = Pf0[:3, :3] if chart == "12" else Pf0[3:, 3:]
            if abs(np.linalg.det(blk)) < 1e-14 * max(1.0, np.abs(blk).max()) ** 3:
                continue
            pol = polish_float(Pf0, z, chart)
            if pol is None:
                continue
            x, cond = pol
            if np.abs(P_from_x_float(x, chart) - Pf0).max() > 1e-6 * (1 + np.abs(Pf0).max()):
                continue
            if best is None or cond < best[2]:
                best = (chart, x, cond)
        if best is None:
            continue
        chart, x, cond = best
        Pf = P_from_x_float(x, chart)
        C = certs[chart]
        flint.ctx.prec = prec
        xr = C.refine(x)
        is_real = all(float(abs(c.imag.mid())) < 1e-30 * (1 + float(abs(c.real.mid()))) for c in xr)
        ok, X = C.krawczyk(xr, is_real, rad_exp=rad_exp)
        Pb, Sb = C.P_balls(X)
        detS = (Sb[0][0] * (Sb[1][1] * Sb[2][2] - Sb[1][2] * Sb[2][1])
                - Sb[0][1] * (Sb[1][0] * Sb[2][2] - Sb[1][2] * Sb[2][0])
                + Sb[0][2] * (Sb[1][0] * Sb[2][1] - Sb[1][1] * Sb[2][0]))
        forced = None
        if ok:
            for k, Ek in enumerate(E):
                if all(Pb[i][j].contains(flint.acb(int(Ek[i][j]))) for i in range(6) for j in range(6)):
                    forced = "E_%d" % (k + 1)        # the unique solution in the box is E_k
        entry = {"chart": chart, "certified": bool(ok), "forced_point": forced, "real": bool(is_real),
                 # rank P = rank S in the chart; det S != 0 on the whole box: rank exactly 3
                 "rank_3_certified": bool(ok and not detS.contains(flint.acb(0))),
                 # some entry of P has an imaginary part bounded away from 0 on the whole box
                 "non_real_certified": bool(ok and not is_real and any(
                     not Pb[i][j].imag.contains(flint.arb(0)) for i in range(6) for j in range(6))),
                 "cond_jacobian_float": float(cond),
                 "box_radius_log2": rad_exp + float(np.log2(max(1.0, np.abs(x).max()))),
                 "max_abs_entry": float(np.abs(Pf).max())}
        if is_real:
            S = [[Sb[i][j].real for j in range(3)] for i in range(3)]
            tr = S[0][0] + S[1][1] + S[2][2]
            e2 = (S[0][0] * S[1][1] - S[0][1] ** 2 + S[0][0] * S[2][2] - S[0][2] ** 2
                  + S[1][1] * S[2][2] - S[1][2] ** 2)
            det = (S[0][0] * (S[1][1] * S[2][2] - S[1][2] ** 2)
                   - S[0][1] * (S[0][1] * S[2][2] - S[1][2] * S[0][2])
                   + S[0][2] * (S[0][1] * S[1][2] - S[1][1] * S[0][2]))
            sg = (sign_of(tr), sign_of(e2), sign_of(det))
            entry["signs_tr_e2_det_of_S"] = list(sg)
            # S is real symmetric 3 x 3 with characteristic polynomial t^3 - tr t^2 + e2 t - det;
            # all roots are real, so by Descartes' rule the number of positive roots is the number
            # of sign changes of (1, -tr, e2, -det) when no coefficient vanishes.
            if 0 in sg:
                entry["definiteness"] = "undecided"
            else:
                seq = [1, -sg[0], sg[1], -sg[2]]
                npos = sum(1 for u, w in zip(seq, seq[1:]) if u != w)
                entry["positive_eigenvalues_of_S"] = npos
                entry["definiteness"] = ("positive semidefinite, rank 3" if npos == 3 else
                                         "not semidefinite (%d positive, %d negative eigenvalues)"
                                         % (npos, 3 - npos))
            entry["eigenvalues_float"] = [float(t) for t in np.linalg.eigvalsh(Pf.real)]
        entry["P"] = [[(Pb[i][j].real.mid().str(30, radius=False) if is_real else
                        Pb[i][j].real.mid().str(30, radius=False) + " + "
                        + Pb[i][j].imag.mid().str(30, radius=False) + "*I")
                       for j in range(6)] for i in range(6)]
        entry["_balls"] = Pb
        sols.append(entry)
    return sols


def pairwise_disjoint(sols):
    """True iff the certified boxes are pairwise disjoint as sets of matrices P."""
    good = [s for s in sols if s["certified"]]
    for a in range(len(good)):
        for b in range(a):
            if all(good[a]["_balls"][i][j].overlaps(good[b]["_balls"][i][j])
                   for i in range(6) for j in range(6)):
                return False
    return True


# ============================================================================== driver
def run(name, tangents, n, primes, do_numeric):
    t0 = time.time()
    chains, z = el.ensemble(tangents)
    first = []
    if n == 10:
        fam = el.rank2_families_at_infinity(z)[0]
        first = [el.sym_outer(fam["ann_lambda"][0], fam["ann_mu"][0])]
    mats, rank, dimN = el.pencil_basis(z, first=first)
    v = len(mats)
    polys = [f for _, f in el.all_4x4_minors(mats)]
    res = {"witness": name, "n": n, "tangents": [[str(t) for t in row] for row in tangents],
           "linear_rank": rank, "pencil_dimension_v": v, "modular": {}}
    m = None
    for p in primes:
        info, ops = affine_part_mod_p(polys, v, p)
        info["all_affine_points_have_rank_3"] = rank3_check_mod_p(mats, ops, p)
        res["modular"][str(p)] = info
        m = info["affine_degree_m"]
    res["affine_solutions_mod_p"] = m
    res["non_forced_affine_solutions_mod_p"] = m - 2
    if do_numeric and m > 2:
        cands = numeric_candidates(z, m)
        sols = certify_all(z, cands)
        cert = [s for s in sols if s["certified"] and s["forced_point"] is None]
        res["certified"] = {
            "numerical_candidates": len(cands),
            "distinct_after_polishing": len(sols),
            "certified_boxes": sum(1 for s in sols if s["certified"]),
            "forced_points_recovered": sorted(s["forced_point"] for s in sols if s["forced_point"]),
            "non_forced_certified": len(cert),
            "matches_modular_count": len(cert) == m - 2,
            "boxes_pairwise_disjoint": pairwise_disjoint(sols),
            "all_of_rank_3": all(s["rank_3_certified"] for s in cert),
            "real": sum(1 for s in cert if s["real"]),
            "non_real": sum(1 for s in cert if s["non_real_certified"]),
            "neither_certified_real_nor_non_real": sum(1 for s in cert if not s["real"]
                                                       and not s["non_real_certified"]),
            "real_positive_semidefinite": sum(1 for s in cert if s["real"]
                                              and s.get("definiteness", "").startswith("positive")),
            "real_not_semidefinite": sum(1 for s in cert if s["real"]
                                         and s.get("definiteness", "").startswith("not")),
            "real_undecided": sum(1 for s in cert if s["real"] and s.get("definiteness") == "undecided"),
        }
        for s in sols:
            s.pop("_balls", None)
        res["solutions"] = sorted([s for s in sols if s["forced_point"] is None],
                                  key=lambda s: s["max_abs_entry"])
    res["seconds"] = round(time.time() - t0, 1)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    jobs = [("geometry_seed_0", el.geometry_witness_tangents, 0, (9, 10, 11), PRIMES, True)]
    if not args.quick:
        jobs += [("geometry_seed_1", el.geometry_witness_tangents, 1, (9, 10), PRIMES[:1], True),
                 ("geometry_seed_2", el.geometry_witness_tangents, 2, (9, 10), PRIMES[:1], True),
                 ("eng_0", el.eng_witness_tangents, 0, (9, 10), PRIMES[:1], True),
                 ("eng_1", el.eng_witness_tangents, 1, (9, 10), PRIMES[:1], True)]
    out = {"request": "GEOMETRY-REQ-0001 item 1 (validation: affine solutions)", "geometry_commit": PIN,
           "macaulay_degree": D, "primes": [str(p) for p in PRIMES],
           "python_flint": flint.__version__, "numpy": np.__version__, "results": []}
    for name, fn, idx, ns, primes, numeric in jobs:
        for n in ns:
            r = run(name, fn(2, n, idx), n, primes, numeric)
            out["results"].append(r)
            line = (f"{name:16s} n={n:2d} affine solutions mod p: {r['affine_solutions_mod_p']} "
                    f"(reduced: {[i['affine_scheme_reduced_mod_p'] for i in r['modular'].values()]}, "
                    f"ranks h^k: {list(r['modular'].values())[0]['rank_of_h^k_S_(7-k)_in_A_7']})")
            if "certified" in r:
                c = r["certified"]
                line += (f" | certified non-forced {c['non_forced_certified']}: real {c['real']} "
                         f"(PSD {c['real_positive_semidefinite']}, not PSD {c['real_not_semidefinite']}), "
                         f"non-real {c['non_real']}, disjoint {c['boxes_pairwise_disjoint']}, "
                         f"count matches mod p: {c['matches_modular_count']}")
            print(line + f" [{r['seconds']}s]", flush=True)
    path = HERE / "results" / ("item1_affine_solutions_quick.json" if args.quick
                               else "item1_affine_solutions.json")
    path.write_text(json.dumps(out, indent=1) + "\n")
    print("wrote", path.relative_to(HERE.parents[2]))


if __name__ == "__main__":
    main()
