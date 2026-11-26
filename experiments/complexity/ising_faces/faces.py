"""Are K given sign vectors exactly the ground states of some Ising pair energy?   (question E-C1 of the
Ensemble division, ENSEMBLE-MSG-0003 section 4)

Setting.  Sites 1..n, states x in {+1,-1}^n up to a global sign, energies E_J(x) = sum_{i<j} J_ij x_i x_j with
arbitrary real couplings (all pairs).  V = {x^1,...,x^K} (distinct up to sign) is *exposed* if some J has
E_J(x^k) = E0 for all k and E_J(y) > E0 for every other state y; equivalently the matrices x^k x^k^T are the
vertices of a face of the cut polytope.

Facts used (proved in docs/complexity/ISING_GROUND_SETS.md):
  (1) exposed  <=>  aff(V) does not meet conv(all other vertices);
  (2) the answer depends only on the SET of column types  T = { (x^1_i,...,x^K_i) up to sign : i a site }
      (merge sites with equal or opposite columns);
so for a fixed K the problem is a finite table indexed by subsets of the 2^(K-1) types.

Both answers come with exact certificates, verified in rational arithmetic:
  YES: an integer matrix J; the K states tie and every other state is strictly higher (full enumeration);
  NO:  rationals mu_y >= 0 (sum 1) on other states and alpha_k (sum 1) with  sum mu_y yy^T = sum alpha_k x^k x^k^T.
The linear programmes are solved in floating point (scipy/HiGHS) only to *find* the certificates.
"""
import itertools
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog


def reduce_types(vectors):
    """vectors: list of K sign tuples of equal length.  Returns the list of distinct column types, each
    normalised to have first entry +1 (a column and its negative are the same type)."""
    K, n = len(vectors), len(vectors[0])
    types = []
    for i in range(n):
        col = tuple(v[i] for v in vectors)
        if col[0] < 0:
            col = tuple(-c for c in col)
        if col not in types:
            types.append(col)
    return types


def states(m):
    """all sign vectors of length m with first entry +1 (one per class up to global sign)."""
    for rest in itertools.product((1, -1), repeat=m - 1):
        yield (1,) + rest


def pair_vector(x):
    m = len(x)
    return [x[i] * x[j] for i in range(m) for j in range(i + 1, m)]


def decide(types, max_den=10 ** 6):
    """types: list of distinct columns (tuples of length K, first entry +1).  The K states on the reduced
    system are the rows of the matrix whose columns are the types.
    Returns ('degenerate', None) if two of the K states coincide up to sign on these sites,
            ('yes', J) with J an integer dict {(i,j): J_ij},
            ('no', (mu, alpha)) with exact rational certificates."""
    m, K = len(types), len(types[0])
    V = []
    for k in range(K):
        row = tuple(t[k] for t in types)
        if row[0] < 0:
            row = tuple(-r for r in row)
        V.append(row)
    if len(set(V)) < K:
        return "degenerate", None
    if m == 1:
        return "degenerate", None
    others = [y for y in states(m) if y not in set(V)]
    if not others:
        return "yes", {}
    P = m * (m - 1) // 2
    PV = np.array([pair_vector(v) for v in V], dtype=float)
    PO = np.array([pair_vector(y) for y in others], dtype=float)
    # primal: maximise t  s.t.  J.(v_k - v_1) = 0,  J.(y - v_1) >= t,  -1 <= J <= 1,  t <= 1
    c = np.zeros(P + 1); c[-1] = -1.0
    A_eq = np.hstack([PV[1:] - PV[0], np.zeros((K - 1, 1))]) if K > 1 else None
    b_eq = np.zeros(K - 1) if K > 1 else None
    A_ub = np.hstack([-(PO - PV[0]), np.ones((len(others), 1))])
    b_ub = np.zeros(len(others))
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                  bounds=[(-1, 1)] * P + [(0, 1)], method="highs")
    if res.status == 0 and res.x[-1] > 1e-7:
        # exact certificate: rationalise J and verify; try increasing denominators
        for den in (1, 2, 3, 4, 6, 12, 24, 60, 120, 720, 5040, max_den):
            J = [Fraction(float(v) / res.x[-1]).limit_denominator(den) for v in res.x[:-1]]
            e = [sum(Jp * xp for Jp, xp in zip(J, pair_vector(v))) for v in V]
            if len(set(e)) != 1:
                continue
            if all(sum(Jp * xp for Jp, xp in zip(J, pair_vector(y))) > e[0] for y in others):
                L = 1
                for q in J:
                    L = L * q.denominator // np.gcd(L, q.denominator)
                Jint = {}
                idx = 0
                for i in range(m):
                    for j in range(i + 1, m):
                        Jint[(i, j)] = int(J[idx] * L); idx += 1
                return "yes", Jint
        raise RuntimeError("could not rationalise a primal certificate")
    # dual: mu >= 0 on others, alpha free on V:  sum mu_y y = sum alpha_k v_k,  sum mu = 1, sum alpha = 1
    nO = len(others)
    A_eq = np.vstack([np.hstack([PO.T, -PV.T]),
                      np.hstack([np.ones((1, nO)), np.zeros((1, K))]),
                      np.hstack([np.zeros((1, nO)), np.ones((1, K))])])
    b_eq = np.concatenate([np.zeros(P), [1.0, 1.0]])
    res2 = linprog(np.zeros(nO + K), A_eq=A_eq, b_eq=b_eq,
                   bounds=[(0, None)] * nO + [(None, None)] * K, method="highs")
    if res2.status != 0:
        raise RuntimeError("neither certificate found")
    for den in (1, 2, 3, 4, 6, 8, 12, 24, 60, 120, 720, 5040, max_den):
        mu = [Fraction(float(v)).limit_denominator(den) for v in res2.x[:nO]]
        al = [Fraction(float(v)).limit_denominator(den) for v in res2.x[nO:]]
        if any(q < 0 for q in mu) or sum(mu) != 1 or sum(al) != 1:
            continue
        ok = True
        for p in range(P):
            lhs = sum(q * int(PO[r, p]) for r, q in enumerate(mu) if q)
            rhs = sum(q * int(PV[k, p]) for k, q in enumerate(al))
            if lhs != rhs:
                ok = False; break
        if ok:
            return "no", ({others[r]: q for r, q in enumerate(mu) if q}, al)
    raise RuntimeError("could not rationalise a dual certificate")


def is_exposed(vectors):
    """the general problem: exponential only in the number of distinct column types (<= 2^(K-1))."""
    return decide(reduce_types(vectors))
