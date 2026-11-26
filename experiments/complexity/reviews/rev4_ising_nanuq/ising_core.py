"""
Referee's own implementation (review4).  Written from the definitions in
docs/complexity/ISING_GROUND_SETS.md BEFORE reading the author's code.

States: sign vectors x in {+1,-1}^m, identified up to global sign.
E_J(x) = sum_{i<j} J_ij x_i x_j.   V exposed  <=>  exists J with argmin E_J = V.

Exact decision procedure
------------------------
Let B_1..B_r be an integer basis of { J : <J, P(x^k) - P(x^1)> = 0 for all k }  (the J that tie on V).
g(y) = ( <B_b, P(y) - P(x^1)> )_b  in Z^r.
  V exposed      <=>  exists lam in R^r with lam.g(y) > 0 for all y not in V
  V not exposed  <=>  0 in conv{ g(y) : y not in V }        (Gordan / Farkas)
A floating-point LP proposes lam or the convex weights; both are then verified in exact
integer / rational arithmetic.  Nothing is reported without the exact check.
"""
import itertools
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
import sympy


# ---------------------------------------------------------------- basics
def canon(x):
    x = tuple(int(v) for v in x)
    return x if x[0] == 1 else tuple(-v for v in x)


def all_states(m):
    """all 2^(m-1) states with first entry +1, as int8 array"""
    if m == 1:
        return np.ones((1, 1), dtype=np.int8)
    rest = np.array(list(itertools.product([1, -1], repeat=m - 1)), dtype=np.int8)
    return np.hstack([np.ones((rest.shape[0], 1), dtype=np.int8), rest])


def pairs(m):
    return [(i, j) for i in range(m) for j in range(i + 1, m)]


def Pmat(X):
    """rows P(x) for the rows x of X"""
    X = np.asarray(X, dtype=np.int64)
    m = X.shape[1]
    I, Jx = np.triu_indices(m, 1)
    return X[:, I] * X[:, Jx]


def int_nullspace(A):
    """integer basis (rows) of the right null space of the integer matrix A (sympy, exact)"""
    A = sympy.Matrix(A.tolist()) if not isinstance(A, sympy.Matrix) else A
    ns = A.nullspace()
    out = []
    for v in ns:
        den = sympy.ilcm(*[sympy.Rational(e).q for e in v]) if len(v) else 1
        w = [int(sympy.Rational(e) * den) for e in v]
        g = 0
        for e in w:
            g = np.gcd(g, abs(e))
        g = int(g) if g else 1
        out.append([e // g for e in w])
    return np.array(out, dtype=np.int64).reshape(len(out), A.shape[1])


# ---------------------------------------------------------------- exact linear algebra
def solve_exact(A, b):
    """Solve A x = b over Q (A: list of rows of ints/Fractions).  Returns (x, unique) or (None, False)
    if inconsistent.  If not unique, free variables are set to 0."""
    nrow = len(A)
    ncol = len(A[0]) if nrow else 0
    M = [[Fraction(v) for v in row] + [Fraction(bb)] for row, bb in zip(A, b)]
    piv = []
    r = 0
    for c in range(ncol):
        p = None
        for i in range(r, nrow):
            if M[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        inv = 1 / M[r][c]
        M[r] = [v * inv for v in M[r]]
        for i in range(nrow):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * bb for a, bb in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == nrow:
            break
    for i in range(r, nrow):
        if M[i][ncol] != 0:
            return None, False
    x = [Fraction(0)] * ncol
    for i, c in enumerate(piv):
        x[c] = M[i][ncol]
    return x, (len(piv) == ncol)


def exact_feasible_nonneg(A, b, maxit=20000):
    """Find x >= 0 with A x = b over Q by an exact phase-1 simplex (Bland's rule).
    A: list of rows (ints), b: list.  Returns list of Fractions or None."""
    nrow = len(A)
    ncol = len(A[0])
    T = []
    for i in range(nrow):
        row = [Fraction(v) for v in A[i]]
        bb = Fraction(b[i])
        if bb < 0:
            row = [-v for v in row]
            bb = -bb
        art = [Fraction(0)] * nrow
        art[i] = Fraction(1)
        T.append(row + art + [bb])
    basis = [ncol + i for i in range(nrow)]
    ntot = ncol + nrow
    # objective: minimise sum of artificials -> reduced costs
    def reduced():
        z = [Fraction(0)] * (ntot + 1)
        for i in range(nrow):
            if basis[i] >= ncol:
                for j in range(ntot + 1):
                    z[j] += T[i][j]
        return z
    for it in range(maxit):
        z = reduced()
        # cost of column j is 1 for artificials, 0 otherwise; reduced cost d_j = c_j - z_j
        enter = None
        for j in range(ncol):
            if z[j] > 0:          # d_j = -z_j < 0
                enter = j
                break
        if enter is None:
            break
        best = None
        leave = None
        for i in range(nrow):
            if T[i][enter] > 0:
                ratio = T[i][ntot] / T[i][enter]
                if best is None or ratio < best or (ratio == best and basis[i] < basis[leave]):
                    best = ratio
                    leave = i
        if leave is None:
            return None
        pv = T[leave][enter]
        T[leave] = [v / pv for v in T[leave]]
        for i in range(nrow):
            if i != leave and T[i][enter] != 0:
                f = T[i][enter]
                T[i] = [a - f * bb for a, bb in zip(T[i], T[leave])]
        basis[leave] = enter
    else:
        raise RuntimeError("simplex iteration limit")
    val = sum(T[i][ntot] for i in range(nrow) if basis[i] >= ncol)
    if val != 0:
        return None
    x = [Fraction(0)] * ncol
    for i in range(nrow):
        if basis[i] < ncol:
            x[basis[i]] = T[i][ntot]
    return x


# ---------------------------------------------------------------- decision
class Result:
    def __init__(self, exposed, **kw):
        self.exposed = exposed
        self.__dict__.update(kw)


def decide(V, candidates=None, want_alpha=True, tol=1e-7):
    """V: list of states (sign tuples, pairwise different up to sign).
    candidates: array of states to be used as V^c (default: all states not in V).
    Returns Result(exposed=True, J=integer matrix (verified on `candidates`))
         or Result(exposed=False, mu={state: Fraction}, alpha=[Fraction]*K)  (verified exactly)."""
    V = [canon(x) for x in V]
    K = len(V)
    m = len(V[0])
    assert len(set(V)) == K, "states not pairwise different"
    Vset = set(V)
    if candidates is None:
        S = all_states(m)
    else:
        S = np.array([canon(x) for x in candidates], dtype=np.int8)
    keep = np.array([tuple(int(v) for v in row) not in Vset for row in S], dtype=bool)
    Y = S[keep]
    if Y.shape[0] == 0:
        return Result(True, J=np.zeros((m, m), dtype=np.int64), trivial=True)
    PV = Pmat(np.array(V))
    D = PV[1:] - PV[0:1]
    npair = PV.shape[1]
    if D.shape[0] == 0 or not D.any():
        B = np.eye(npair, dtype=np.int64)
    else:
        B = int_nullspace(D)
    r = B.shape[0]
    PY = Pmat(Y)
    G = (PY - PV[0:1]) @ B.T          # |Y| x r, integers
    if r == 0:
        # no tying J at all except 0: exposed iff Y empty (handled) -> not exposed; any y is in aff P(V)
        return _certificate(V, Y, np.zeros((Y.shape[0], 0), dtype=np.int64), want_alpha)
    # primal LP: max t, G lam >= t, -1<=lam<=1, t<=1
    c = np.zeros(r + 1)
    c[-1] = -1.0
    A_ub = np.hstack([-G.astype(float), np.ones((G.shape[0], 1))])
    b_ub = np.zeros(G.shape[0])
    bounds = [(-1, 1)] * r + [(None, 1)]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if res.status != 0:
        raise RuntimeError("LP failed: " + res.message)
    t = res.x[-1]
    if t > tol:
        lam = res.x[:r]
        for Q in (10 ** 4, 10 ** 6, 10 ** 8):
            li = [int(round(v * Q)) for v in lam]
            vals = G.astype(object) @ np.array(li, dtype=object)
            if min(vals) > 0:
                Jv = np.array(li, dtype=object) @ B.astype(object)
                J = np.zeros((m, m), dtype=object)
                for (i, j), v in zip(pairs(m), Jv):
                    J[i, j] = J[j, i] = v
                # final exact check straight from the definition
                EV = [energy(J, x) for x in V]
                assert len(set(EV)) == 1
                EY = PY.astype(object) @ Jv
                assert min(EY) > EV[0]
                return Result(True, J=J, E0=EV[0], gap=min(EY) - EV[0], margin=t)
        raise RuntimeError("could not rationalise an exposing J (margin %g)" % t)
    return _certificate(V, Y, G, want_alpha)


def energy(J, x):
    m = len(x)
    return sum(J[i, j] * x[i] * x[j] for i in range(m) for j in range(i + 1, m))


def _certificate(V, Y, G, want_alpha=True):
    """exact mu >= 0 on Y, sum 1, with G^T mu = 0; then alpha with sum_y mu_y P(y) = sum_k alpha_k P(x^k)."""
    nY, r = G.shape
    A_eq = np.vstack([G.T.astype(float), np.ones((1, nY))])
    b_eq = np.zeros(r + 1)
    b_eq[-1] = 1.0
    res = linprog(np.zeros(nY), A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * nY, method="highs-ds")
    if res.status != 0:
        raise RuntimeError("neither exposing J nor certificate found (status %d)" % res.status)
    mu = res.x
    order = np.argsort(-mu)
    supp = [int(i) for i in order if mu[i] > 1e-9]
    sol = None
    A = [[int(G[i, b]) for i in supp] for b in range(r)] + [[1] * len(supp)]
    bvec = [0] * r + [1]
    x, unique = solve_exact(A, bvec)
    if x is not None and unique and all(v > 0 for v in x):
        sol = dict(zip(supp, x))
    else:
        # fall back: exact simplex on an enlarged column set
        extra = [int(i) for i in order[: min(nY, max(4 * (r + 1), len(supp) + 50))]]
        cols = list(dict.fromkeys(supp + extra))
        A = [[int(G[i, b]) for i in cols] for b in range(r)] + [[1] * len(cols)]
        x = exact_feasible_nonneg(A, bvec)
        if x is None:
            cols = list(range(nY))
            A = [[int(G[i, b]) for i in cols] for b in range(r)] + [[1] * len(cols)]
            x = exact_feasible_nonneg(A, bvec)
        if x is None:
            raise RuntimeError("exact certificate not found")
        sol = {i: v for i, v in zip(cols, x) if v != 0}
    mu_exact = {tuple(int(v) for v in Y[i]): w for i, w in sol.items()}
    assert sum(mu_exact.values()) == 1 and all(w > 0 for w in mu_exact.values())
    alpha = None
    if want_alpha:
        alpha = alpha_for(V, mu_exact)
        assert alpha is not None, "certificate does not lie in aff P(V)"
    return Result(False, mu=mu_exact, alpha=alpha)


def alpha_for(V, mu):
    """solve sum_k alpha_k P(x^k) = sum_y mu_y P(y), sum alpha = 1 exactly; None if unsolvable.
    Finally verifies the identity from the definition."""
    m = len(V[0])
    pr = pairs(m)
    rhs = [sum(w * y[i] * y[j] for y, w in mu.items()) for (i, j) in pr] + [Fraction(1)]
    A = [[x[i] * x[j] for x in V] for (i, j) in pr] + [[1] * len(V)]
    alpha, _ = solve_exact(A, rhs)
    if alpha is None:
        return None
    assert verify_certificate(V, mu, alpha)
    return alpha


def verify_certificate(V, mu, alpha):
    """Theorem 1 certificate, checked literally: y not in V, mu>0, sum mu = 1, sum alpha = 1,
    sum mu P(y) = sum alpha P(x)."""
    Vset = set(canon(x) for x in V)
    m = len(V[0])
    if any(canon(y) in Vset for y in mu):
        return False
    if any(w <= 0 for w in mu.values()) or sum(mu.values()) != 1 or sum(alpha) != 1:
        return False
    for i in range(m):
        for j in range(i + 1, m):
            lhs = sum(Fraction(w) * y[i] * y[j] for y, w in mu.items())
            rhs = sum(Fraction(a) * x[i] * x[j] for x, a in zip(V, alpha))
            if lhs != rhs:
                return False
    return True


# ---------------------------------------------------------------- types, twins
def type_of_site(V, i):
    col = tuple(int(x[i]) for x in V)
    return col if col[0] == 1 else tuple(-v for v in col)


def twin_reduce(V):
    """one site per type (first occurrence); returns list of reduced states and the list of kept sites"""
    m = len(V[0])
    seen = {}
    for i in range(m):
        t = type_of_site(V, i)
        if t not in seen:
            seen[t] = i
    T = sorted(seen.values())
    return [tuple(x[i] for i in T) for x in V], T


def states_from_types(types):
    """types: list of K-tuples (columns).  Returns the K states on len(types) sites."""
    K = len(types[0])
    return [tuple(t[k] for t in types) for k in range(K)]


def distinct_states(V):
    return len(set(canon(x) for x in V)) == len(V)


# ---------------------------------------------------------------- sign vectors in the span
def rank_exact(rows):
    return sympy.Matrix(rows).rank()


def sign_vectors_in_span(V):
    """all sign vectors (as canonical states) in the real span of the states V.  Exact.
    Cost 2^(rank-1) * poly."""
    Vl = [list(x) for x in V]
    Mx = sympy.Matrix(Vl)
    m = Mx.shape[1]
    # independent rows
    _, prow = Mx.T.rref()
    R = list(prow)
    MR = Mx.extract(R, list(range(m)))
    _, pcol = MR.rref()
    I = list(pcol)
    rho = len(R)
    Sq = MR.extract(list(range(rho)), I)          # rho x rho invertible
    Sinv = Sq.inv()                                # exact rationals
    den = sympy.ilcm(*[sympy.Rational(e).q for e in Sinv]) if rho else 1
    Sinv_i = np.array((Sinv * den).tolist(), dtype=object)     # integer matrix, Sinv = Sinv_i/den
    MRn = np.array(MR.tolist(), dtype=object)
    # y = MR^T c with (Sq^T) c = b  -> c = Sinv^T b ; y = MR^T Sinv^T b = (Sinv MR)^T b
    Wm = (Sinv_i @ MRn)                            # rho x m integers; y*den = Wm^T b
    Wm = np.array(Wm.tolist(), dtype=np.int64)
    den = int(den)
    out = []
    if rho == 0:
        return out, []
    bs = np.array(list(itertools.product([1, -1], repeat=rho - 1)), dtype=np.int64)
    bs = np.hstack([np.ones((bs.shape[0], 1), dtype=np.int64), bs]) if rho > 1 else np.ones((1, 1), dtype=np.int64)
    Yd = bs @ Wm                                   # candidates * den
    ok = np.all(np.abs(Yd) == abs(den), axis=1)
    coefs = []
    for b, yd in zip(bs[ok], Yd[ok]):
        y = tuple(int(v // den) for v in yd)
        out.append(canon(y))
    return out, (R, I)


def decide_span(V, **kw):
    """FPT algorithm: only sign vectors of span(V) are used as V^c (justified by Proposition 5)."""
    Y, _ = sign_vectors_in_span(V)
    return decide(V, candidates=Y if Y else [V[0]], **kw)


def coefficients(V, y):
    """exact c with sum_k c_k x^k = y  (V linearly independent), or None"""
    A = [[x[i] for x in V] for i in range(len(y))]
    c, unique = solve_exact(A, list(y))
    return c
