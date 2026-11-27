"""
Workstream P7 -- library: shares at the leaves of a branching tree.

What is whose code:
  * P4's library `p4lib` (read-only import from ../ws_P4) is used for loading P2's enumerated grids
    (`load_instance`, which calls P2's loaders), for P4's class constants (`c2_matrix`, `c3_dict`) and
    its grid helpers (`star_part`, `interp2`, `pair_penalty`, `site_penalty`, `line`, `second_diff`),
    so that the models are P4's models.  Nothing is written into ws_P4 or ws_P2
    (sys.dont_write_bytecode is set before the import; run with `python3 -B`).
  * Everything else here is written for this workstream: the pairwise model in difference form,
    the linear programmes (shares with slack; the dual of a leaf in the theory kernel's variables;
    the primal local-polytope programme, with optional triplet constraints), the "published"
    integer instance (tables rounded DOWN to multiples of 2^-40 kcal/mol), an integer checker that
    mirrors the theory division's `LeafOK` (proofs/CertificateAlgebra.lean), exact rational
    fractional points, brute force over leaves.

Conventions.
  A model is a pairwise function in DIFFERENCE FORM at a reference r (an index tuple):
      F(x) = sum_{i: x_i != r_i} A_i(x_i) + sum_{i<j: both changed} M_ij(x_i, x_j),     F(r) = 0,
  A_i(a) = F(r; i->a), M_ij = second mixed difference of F at r.  A_i(r_i) = 0 and M_ij has a zero
  row r_i and a zero column r_j.  "x0 minimises the model" <=> F >= 0.
  A domain D is a list (one entry per site) of sorted integer arrays of admissible states.
  Optional `allowed[(i, j)]` (boolean (k_i, k_j)): pairs of states that may occur together
  (non-product domains = a product minus forbidden pairs of states).

  Messages follow the sign convention of the theory kernel's `leaf u p m`:
      u_i  <= A_i(a) + sum_{j != i} m_ij(a)                      (a in D_i)
      P_ij <= M_ij(a, b) - m_ij(a) - m_ji(b)                     (a in D_i, b in D_j, allowed)   [P_ij = 2 p_ij]
      L    <= sum_i u_i + sum_{i<j} P_ij .
  State-dependent shares (Proposition P4.1 / theory report 11.18b(e)) are s_ij(a) = -m_ij(a) with
  m_ij(r_i) = 0, u = 0, P = 0, L = 0.
"""
import sys, os, math, itertools, time
sys.dont_write_bytecode = True
from fractions import Fraction
import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
P4 = os.path.normpath(os.path.join(HERE, "..", "ws_P4"))
if P4 not in sys.path:
    sys.path.insert(0, P4)
import p4lib as L4          # P4 (read-only); it imports P2's anlib / an_main (read-only)

SCALE = 40                  # published instance: integers in units of 2^-SCALE kcal/mol
UNIT = 2.0 ** (-SCALE)
RESIDUALS = L4.RESIDUALS


# =============================================================================== the model
class PM:
    """pairwise model in difference form at the reference r (see module docstring)."""

    def __init__(self, shape, r, A, M, allowed=None, dom=None):
        self.shape = tuple(int(k) for k in shape)
        self.n = len(self.shape)
        self.r = tuple(int(v) for v in r)
        self.A = [np.array(a, dtype=float) for a in A]
        self.M = {key: np.array(v, dtype=float) for key, v in M.items()}
        self.allowed = allowed
        self.dom = [np.arange(k) for k in self.shape] if dom is None else [np.array(d, dtype=int) for d in dom]
        for i in range(self.n):
            assert self.A[i].shape == (self.shape[i],) and self.A[i][self.r[i]] == 0.0
        for (i, j), T in self.M.items():
            assert i < j and T.shape == (self.shape[i], self.shape[j])
            assert not T[self.r[i], :].any() and not T[:, self.r[j]].any()

    # ---- constructors
    @staticmethod
    def from_grid(G, r, mask=None):
        """difference form at r of the function G on a product grid (G must be finite on the lines
        and planes through r).  If G is pairwise, pm.grid() == G - G[r].  mask: domain (boolean grid)
        given by pairwise exclusions; then dom_i = states compatible with the reference, allowed_ij
        = the plane of the mask through r."""
        r = tuple(int(v) for v in r)
        n = G.ndim
        A = []
        for i in range(n):
            a = L4.line(G, r, i) - G[r]
            a[r[i]] = 0.0
            A.append(a)
        M = {}
        for i in range(n):
            for j in range(i + 1, n):
                T = L4.second_diff(G, r, i, j).copy()
                T[r[i], :] = 0.0
                T[:, r[j]] = 0.0
                M[(i, j)] = T
        allowed = None
        dom = None
        if mask is not None and not mask.all():
            assert mask[r]
            dom = [np.flatnonzero(L4.line(mask, r, i)) for i in range(n)]
            allowed = {}
            for i in range(n):
                for j in range(i + 1, n):
                    idx = list(r); idx[i] = slice(None); idx[j] = slice(None)
                    allowed[(i, j)] = mask[tuple(idx)].copy()
            # entries that can never be used (inadmissible states, forbidden pairs) are set to 0, so that
            # clash energies do not enter the published integer instance
            for i in range(n):
                bad = np.ones(G.shape[i], dtype=bool); bad[dom[i]] = False
                A[i][bad] = 0.0
            for key in M:
                M[key][~allowed[key]] = 0.0
        return PM(G.shape, r, A, M, allowed=allowed, dom=dom)

    def pair(self, i, j):
        """M_ij as a (k_i, k_j) array for any ordered pair i != j."""
        return self.M[(i, j)] if i < j else self.M[(j, i)].T

    def ok(self, i, j):
        """allowed_ij as a (k_i, k_j) boolean array, or None."""
        if self.allowed is None:
            return None
        return self.allowed[(i, j)] if i < j else self.allowed[(j, i)].T

    def grid(self):
        """F on the whole product (float); +inf outside a non-product domain."""
        n = self.n
        out = np.zeros(self.shape)
        for i in range(n):
            sh = [1] * n; sh[i] = self.shape[i]
            out = out + self.A[i].reshape(sh)
        for (i, j), T in self.M.items():
            sh = [1] * n; sh[i] = self.shape[i]; sh[j] = self.shape[j]
            out = out + T.reshape(sh)
        m = self.mask()
        if m is not None:
            out = np.where(m, out, np.inf)
        return out

    def mask(self):
        """boolean grid of the domain (None for a full product)."""
        if self.allowed is None and all(len(d) == k for d, k in zip(self.dom, self.shape)):
            return None
        n = self.n
        m = np.ones(self.shape, dtype=bool)
        for i in range(n):
            v = np.zeros(self.shape[i], dtype=bool); v[self.dom[i]] = True
            sh = [1] * n; sh[i] = self.shape[i]
            m = m & v.reshape(sh)
        if self.allowed is not None:
            for (i, j), ok in self.allowed.items():
                sh = [1] * n; sh[i] = self.shape[i]; sh[j] = self.shape[j]
                m = m & ok.reshape(sh)
        return m

    def full_domain(self):
        return [d.copy() for d in self.dom]

    def active(self, D=None):
        D = self.dom if D is None else D
        return [i for i in range(self.n) if len(D[i]) >= 2]


def fix(D, i, a):
    """the leaf domain: site i fixed to state a."""
    out = [d.copy() for d in D]
    out[i] = np.array([int(a)])
    return out


def contains_ref(pm, D):
    return all(pm.r[i] in D[i] for i in range(pm.n))


# =============================================================================== published integer instance
def to_int(arr):
    """floor(arr * 2^SCALE) as int64 -- exact: the product with a power of two is exact in binary
    floating point, floor of a float is exact, and the values are below 2^62."""
    v = np.floor(np.asarray(arr, dtype=np.float64) * (2.0 ** SCALE))
    assert np.all(np.abs(v) < 2.0 ** 61), "table entry too large for the integer instance"
    return v.astype(np.int64)


class IPM:
    """published instance: every table entry of the model rounded DOWN to a multiple of 2^-SCALE
    (a termwise lower instance, the hypothesis of the theory division's `verify_sound_real`);
    entries at reference states are exactly 0, so the value at the reference is exactly 0."""

    def __init__(self, pm):
        self.pm = pm
        self.shape = pm.shape; self.n = pm.n; self.r = pm.r
        self.H = [to_int(a) for a in pm.A]
        self.J = {key: to_int(T) for key, T in pm.M.items()}
        bound = sum(int(np.abs(h).max()) for h in self.H) + sum(int(np.abs(T).max()) for T in self.J.values())
        assert bound < 2 ** 62, "sums could overflow int64"
        self.bound = bound

    def pair(self, i, j):
        return self.J[(i, j)] if i < j else self.J[(j, i)].T

    def grid(self):
        """exact integer values of the published instance on the whole product (int64)."""
        n = self.n
        out = np.zeros(self.shape, dtype=np.int64)
        for i in range(n):
            sh = [1] * n; sh[i] = self.shape[i]
            out = out + self.H[i].reshape(sh)
        for (i, j), T in self.J.items():
            sh = [1] * n; sh[i] = self.shape[i]; sh[j] = self.shape[j]
            out = out + T.reshape(sh)
        return out


def zero_messages(pm):
    return {(i, j): np.zeros(pm.shape[i], dtype=np.int64) for i in range(pm.n) for j in range(pm.n) if i != j}


def leaf_bound(ipm, D, mI, triple=None):
    """The checker of one leaf, in exact integer arithmetic (unit 2^-SCALE): additions and comparisons.
    Mirrors `LeafOK` of proofs/CertificateAlgebra.lean with the best u, p for the given messages:
        U_i  = min_{a in D_i} [ H_i(a) + sum_{j != i} m_ij(a) ]
        P_ij = min_{a in D_i, b in D_j, allowed} [ J_ij(a, b) - m_ij(a) - m_ji(b) ]     (= 2 p_ij)
        LB   = sum_i U_i + sum_{i<j} P_ij ,
    so that  LB <= (published instance)(x) for every x of the box prod D.
    With triple = (p, q, r): the three pair terms inside the triple are replaced by ONE term, the
    minimum over the joint states of the triple of the sum of the three reparametrised pair tables
    (the dual of the relaxation with the local-consistency constraints of that triple).
    Returns (LB, U, P) as Python ints / dicts."""
    pm = ipm.pm
    n = ipm.n
    U = []
    for i in range(n):
        v = ipm.H[i][D[i]].copy()
        for j in range(n):
            if j != i:
                v = v + mI[(i, j)][D[i]]
        U.append(int(v.min()))
    P = {}
    inT = set()
    if triple is not None:
        p_, q_, r_ = sorted(triple)
        inT = {(p_, q_), (p_, r_), (q_, r_)}
    BIG = np.int64(2 ** 62)
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) in inT:
                continue
            T = ipm.J[(i, j)][np.ix_(D[i], D[j])] - mI[(i, j)][D[i]][:, None] - mI[(j, i)][D[j]][None, :]
            ok = pm.ok(i, j)
            if ok is not None:
                T = np.where(ok[np.ix_(D[i], D[j])], T, BIG)
            P[(i, j)] = int(T.min())
    LB = sum(U) + sum(P.values())
    if triple is not None:
        def tab(i, j):
            T = ipm.J[(i, j)][np.ix_(D[i], D[j])] - mI[(i, j)][D[i]][:, None] - mI[(j, i)][D[j]][None, :]
            ok = pm.ok(i, j)
            if ok is not None:
                T = np.where(ok[np.ix_(D[i], D[j])], T, BIG // 4)
            return T
        S3 = tab(p_, q_)[:, :, None] + tab(p_, r_)[:, None, :] + tab(q_, r_)[None, :, :]
        P[("triple", p_, q_, r_)] = int(S3.min())
        LB += int(S3.min())
    return LB, U, P


# =============================================================================== LP 1: shares with slack (leaf that contains the reference)
def shares_lp(pm, D=None, triple=None):
    """State-dependent shares on the box prod D (which must contain the reference):
         s_ij(a) >= 0,   s_ij(a) + s_ji(b) >= -M_ij(a, b)  (a, b changed, allowed),
         sum_{j != i} s_ij(a) + t <= A_i(a)                  (a changed);     maximise t.
    t > 0  <=>  a certificate with slack exists (x0 minimises F on the box, strictly).
    With triple = (p, q, r): for the three pairs inside the triple the sign and cover constraints
    are replaced by: for every joint state (a, b, c) of the triple, the sum of the three
    reparametrised pair terms is >= 0.
    Returns dict(t, s) with s[(i, j)] a float array over ALL states of i (0 at the reference and
    outside D_i), or t = None if the LP failed."""
    D = pm.dom if D is None else D
    assert contains_ref(pm, D)
    n = pm.n
    act = [i for i in range(n) if len(D[i]) >= 2]
    if not act:
        return dict(t=math.inf, s={(i, j): np.zeros(pm.shape[i]) for i in range(n) for j in range(n) if i != j}, status="trivial")
    off = {}
    nv = 0
    for i in act:
        for j in act:
            if i != j:
                off[(i, j)] = nv
                nv += pm.shape[i]
    tvar = nv
    inT = set()
    if triple is not None:
        p_, q_, r_ = sorted(triple)
        assert p_ in act and q_ in act and r_ in act
        inT = {(p_, q_), (p_, r_), (q_, r_)}
    lb = np.zeros(nv + 1); ub = np.zeros(nv + 1)
    for (i, j), o in off.items():
        ch = np.array([a for a in D[i] if a != pm.r[i]], dtype=int)
        ub[o + ch] = np.inf
        if (min(i, j), max(i, j)) in inT:
            lb[o + ch] = -np.inf
    lb[tvar] = -np.inf; ub[tvar] = np.inf
    rows, cols, vals, rhs = [], [], [], []
    nr = 0
    for i in act:
        for j in act:
            if i < j and (i, j) not in inT:
                T = pm.M[(i, j)]
                ok = pm.ok(i, j)
                ai = np.array([a for a in D[i] if a != pm.r[i]], dtype=int)
                bj = np.array([b for b in D[j] if b != pm.r[j]], dtype=int)
                sub = T[np.ix_(ai, bj)]
                need = sub < 0
                if ok is not None:
                    need = need & ok[np.ix_(ai, bj)]
                ia, ib = np.nonzero(need)
                k = len(ia)
                if k:
                    rr = nr + np.arange(k)
                    rows += [rr, rr]; cols += [off[(i, j)] + ai[ia], off[(j, i)] + bj[ib]]
                    vals += [-np.ones(k), -np.ones(k)]
                    rhs.append(sub[ia, ib]); nr += k
    if triple is not None:
        Dp, Dq, Dr = D[p_], D[q_], D[r_]
        A3, B3, C3 = np.meshgrid(Dp, Dq, Dr, indexing="ij")
        A3 = A3.ravel(); B3 = B3.ravel(); C3 = C3.ravel()
        keep = ~((A3 == pm.r[p_]) & (B3 == pm.r[q_]) & (C3 == pm.r[r_]))
        for (x, y, X, Y) in ((p_, q_, A3, B3), (p_, r_, A3, C3), (q_, r_, B3, C3)):
            ok = pm.ok(x, y)
            if ok is not None:
                keep = keep & ok[X, Y]
        A3 = A3[keep]; B3 = B3[keep]; C3 = C3[keep]
        k = len(A3)
        rr = nr + np.arange(k)
        val3 = pm.M[(p_, q_)][A3, B3] + pm.M[(p_, r_)][A3, C3] + pm.M[(q_, r_)][B3, C3]
        for (x, y, X) in ((p_, q_, A3), (q_, p_, B3), (p_, r_, A3), (r_, p_, C3), (q_, r_, B3), (r_, q_, C3)):
            rows.append(rr); cols.append(off[(x, y)] + X); vals.append(-np.ones(k))
        rhs.append(val3); nr += k
    for i in act:
        ai = np.array([a for a in D[i] if a != pm.r[i]], dtype=int)
        k = len(ai)
        rr = nr + np.arange(k)
        for j in act:
            if j != i:
                rows.append(rr); cols.append(off[(i, j)] + ai); vals.append(np.ones(k))
        rows.append(rr); cols.append(np.full(k, tvar)); vals.append(np.ones(k))
        rhs.append(pm.A[i][ai]); nr += k
    Aub = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(nr, nv + 1))
    cost = np.zeros(nv + 1); cost[tvar] = -1.0
    res = linprog(cost, A_ub=Aub, b_ub=np.concatenate(rhs), bounds=np.c_[lb, ub], method="highs")
    if res.x is None:
        return dict(t=None, s=None, status=res.message)
    s = {(i, j): np.zeros(pm.shape[i]) for i in range(n) for j in range(n) if i != j}
    for (i, j), o in off.items():
        s[(i, j)] = res.x[o:o + pm.shape[i]].copy()
    return dict(t=float(res.x[tvar]), s=s, status="ok", nvar=nv + 1, nrow=nr)


def shares_to_messages(ipm, D, s, triple=None):
    """integer messages m = -S from floating-point shares: S = ceil(s * 2^SCALE) (clipped at 0 outside
    a triple), then every cover constraint of the PUBLISHED instance is repaired exactly by raising
    one share (P4's repair).  The result is checked by leaf_bound (LB must be 0)."""
    pm = ipm.pm
    n = ipm.n
    inT = set()
    if triple is not None:
        p_, q_, r_ = sorted(triple)
        inT = {(p_, q_), (p_, r_), (q_, r_)}
    S = {}
    for (i, j), v in s.items():
        w = np.ceil(np.asarray(v, dtype=float) * (2.0 ** SCALE)).astype(np.int64)
        if (min(i, j), max(i, j)) not in inT:
            w = np.maximum(w, 0)
        w[pm.r[i]] = 0
        S[(i, j)] = w
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) in inT or len(D[i]) < 2 or len(D[j]) < 2:
                continue
            ok = pm.ok(i, j)
            T = ipm.J[(i, j)][np.ix_(D[i], D[j])] + S[(i, j)][D[i]][:, None] + S[(j, i)][D[j]][None, :]
            if ok is not None:
                T = np.where(ok[np.ix_(D[i], D[j])], T, 0)
            deficit = np.maximum(-T, 0).max(axis=1)              # per state a of i: the largest violation
            for pos, a in enumerate(D[i]):
                if deficit[pos] > 0 and a != pm.r[i]:
                    S[(i, j)][a] += deficit[pos]
    if triple is not None:
        Dp, Dq, Dr = D[p_], D[q_], D[r_]
        def tab(x, y):
            T = ipm.J[(x, y)][np.ix_(D[x], D[y])] + S[(x, y)][D[x]][:, None] + S[(y, x)][D[y]][None, :]
            ok = pm.ok(x, y)
            if ok is not None:
                T = np.where(ok[np.ix_(D[x], D[y])], T, 2 ** 58)
            return T
        for _ in range(3):
            S3 = tab(p_, q_)[:, :, None] + tab(p_, r_)[:, None, :] + tab(q_, r_)[None, :, :]
            deficit = np.maximum(-S3, 0).max(axis=(1, 2))        # per state a of p
            if not deficit.any():
                break
            for pos, a in enumerate(Dp):
                if deficit[pos] > 0 and a != pm.r[p_]:
                    S[(p_, q_)][a] += deficit[pos]
    return {key: -v for key, v in S.items()}


# =============================================================================== LP 2: the dual of a leaf (any box), kernel variables
def dual_lp(pm, D):
    """max  sum_i u_i + sum_{i<j} P_ij   subject to
         u_i - sum_{j != i} m_ij(a) <= A_i(a)                      (a in D_i)
         P_ij + m_ij(a) + m_ji(b)   <= M_ij(a, b)                  (a in D_i, b in D_j, allowed)
    = the value of the pairwise (local-polytope) relaxation of min F over the box prod D.
    Gauge: m_ij(first state of D_i) = 0.  Returns dict(val, m) with m[(i, j)] over all states of i."""
    n = pm.n
    off = {}
    nv = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                off[(i, j)] = nv
                nv += pm.shape[i]
    uoff = nv; nv += n
    poff = {}
    for i in range(n):
        for j in range(i + 1, n):
            poff[(i, j)] = nv; nv += 1
    lb = np.zeros(nv); ub = np.zeros(nv)
    for (i, j), o in off.items():
        free = np.array(D[i][1:], dtype=int)
        lb[o + free] = -np.inf; ub[o + free] = np.inf
    lb[uoff:] = -np.inf; ub[uoff:] = np.inf
    rows, cols, vals, rhs = [], [], [], []
    nr = 0
    for i in range(n):
        ai = np.asarray(D[i], dtype=int)
        k = len(ai)
        rr = nr + np.arange(k)
        rows.append(rr); cols.append(np.full(k, uoff + i)); vals.append(np.ones(k))
        for j in range(n):
            if j != i:
                rows.append(rr); cols.append(off[(i, j)] + ai); vals.append(-np.ones(k))
        rhs.append(pm.A[i][ai]); nr += k
    for i in range(n):
        for j in range(i + 1, n):
            ai = np.asarray(D[i], dtype=int); bj = np.asarray(D[j], dtype=int)
            Aa, Bb = np.meshgrid(ai, bj, indexing="ij")
            Aa = Aa.ravel(); Bb = Bb.ravel()
            ok = pm.ok(i, j)
            if ok is not None:
                keep = ok[Aa, Bb]
                Aa = Aa[keep]; Bb = Bb[keep]
            k = len(Aa)
            if k == 0:
                ub[poff[(i, j)]] = 0.0; lb[poff[(i, j)]] = 0.0
                continue
            rr = nr + np.arange(k)
            rows += [rr, rr, rr]
            cols += [np.full(k, poff[(i, j)]), off[(i, j)] + Aa, off[(j, i)] + Bb]
            vals += [np.ones(k), np.ones(k), np.ones(k)]
            rhs.append(pm.M[(i, j)][Aa, Bb]); nr += k
    Aub = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(nr, nv))
    cost = np.zeros(nv); cost[uoff:] = -1.0
    res = linprog(cost, A_ub=Aub, b_ub=np.concatenate(rhs), bounds=np.c_[lb, ub], method="highs")
    if res.x is None:
        return dict(val=None, m=None, status=res.message)
    m = {(i, j): res.x[o:o + pm.shape[i]].copy() for (i, j), o in off.items()}
    return dict(val=float(-res.fun), m=m, status="ok", nvar=nv, nrow=nr)


def messages_to_int(m):
    return {key: np.rint(np.asarray(v, dtype=float) * (2.0 ** SCALE)).astype(np.int64) for key, v in m.items()}


# =============================================================================== LP 3: the primal relaxation (local polytope, optional triplets)
def primal_lp(pm, D=None, triples=()):
    """min <theta, mu> over the local polytope of the box prod D (pair marginals consistent with the
    site marginals), optionally with the local-consistency constraints of the given triples
    (a joint marginal on the triple that reproduces its three pair marginals).
    Returns dict(val, mu1 (list of arrays), mu2 (dict (i,j) -> array))."""
    D = pm.dom if D is None else D
    n = pm.n
    o1 = []
    nv = 0
    for i in range(n):
        o1.append(nv); nv += pm.shape[i]
    o2 = {}
    for i in range(n):
        for j in range(i + 1, n):
            o2[(i, j)] = nv; nv += pm.shape[i] * pm.shape[j]
    o3 = {}
    for T in triples:
        T = tuple(sorted(T))
        o3[T] = nv; nv += pm.shape[T[0]] * pm.shape[T[1]] * pm.shape[T[2]]
    cost = np.zeros(nv); ub = np.zeros(nv)
    inD = []
    for i in range(n):
        v = np.zeros(pm.shape[i], dtype=bool); v[D[i]] = True
        inD.append(v)
        cost[o1[i]:o1[i] + pm.shape[i]] = pm.A[i]
        ub[o1[i]:o1[i] + pm.shape[i]] = np.where(v, 1.0, 0.0)
    for (i, j), o in o2.items():
        ki, kj = pm.shape[i], pm.shape[j]
        cost[o:o + ki * kj] = pm.M[(i, j)].ravel()
        okm = inD[i][:, None] & inD[j][None, :]
        if pm.allowed is not None:
            okm = okm & pm.allowed[(i, j)]
        ub[o:o + ki * kj] = np.where(okm.ravel(), 1.0, 0.0)
    for T, o in o3.items():
        p_, q_, r_ = T
        okm = inD[p_][:, None, None] & inD[q_][None, :, None] & inD[r_][None, None, :]
        ub[o:o + okm.size] = np.where(okm.ravel(), 1.0, 0.0)
    rows, cols, vals, rhs = [], [], [], []
    nr = 0
    for i in range(n):
        k = pm.shape[i]
        rows.append(np.full(k, nr)); cols.append(o1[i] + np.arange(k)); vals.append(np.ones(k)); rhs.append(1.0); nr += 1
    for (i, j), o in o2.items():
        ki, kj = pm.shape[i], pm.shape[j]
        idx = o + np.arange(ki * kj).reshape(ki, kj)
        # sum_b mu_ij(a, b) - mu_i(a) = 0
        rr = nr + np.arange(ki)
        rows.append(np.repeat(rr, kj)); cols.append(idx.ravel()); vals.append(np.ones(ki * kj))
        rows.append(rr); cols.append(o1[i] + np.arange(ki)); vals.append(-np.ones(ki))
        rhs += [0.0] * ki; nr += ki
        rr = nr + np.arange(kj)
        rows.append(np.tile(rr, ki)); cols.append(idx.ravel()); vals.append(np.ones(ki * kj))
        rows.append(rr); cols.append(o1[j] + np.arange(kj)); vals.append(-np.ones(kj))
        rhs += [0.0] * kj; nr += kj
    for T, o in o3.items():
        p_, q_, r_ = T
        kp, kq, kr = pm.shape[p_], pm.shape[q_], pm.shape[r_]
        idx = o + np.arange(kp * kq * kr).reshape(kp, kq, kr)
        for (x, y, axis_sum) in ((p_, q_, 2), (p_, r_, 1), (q_, r_, 0)):
            kx, ky = pm.shape[x], pm.shape[y]
            pidx = o2[(x, y)] + np.arange(kx * ky).reshape(kx, ky)
            rr = nr + np.arange(kx * ky).reshape(kx, ky)
            R3 = np.expand_dims(rr, axis_sum) + np.zeros((kp, kq, kr), dtype=int)
            rows.append(R3.ravel()); cols.append(idx.ravel()); vals.append(np.ones(idx.size))
            rows.append(rr.ravel()); cols.append(pidx.ravel()); vals.append(-np.ones(kx * ky))
            rhs += [0.0] * (kx * ky); nr += kx * ky
    Aeq = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(nr, nv))
    res = linprog(cost, A_eq=Aeq, b_eq=np.array(rhs), bounds=np.c_[np.zeros(nv), ub], method="highs")
    if res.x is None:
        return dict(val=None, status=res.message)
    mu1 = [res.x[o1[i]:o1[i] + pm.shape[i]].copy() for i in range(n)]
    mu2 = {(i, j): res.x[o:o + pm.shape[i] * pm.shape[j]].reshape(pm.shape[i], pm.shape[j]).copy() for (i, j), o in o2.items()}
    return dict(val=float(res.fun), mu1=mu1, mu2=mu2, status="ok", nvar=nv, nrow=nr)


def rationalise_point(pm, ipm, mu1, mu2, maxden=5040, tol=1e-7):
    """Try to read the floating-point LP point as an exact rational point of the local polytope:
    find the least common denominator d <= maxden with d*mu within tol of integers, then CHECK in
    integer arithmetic that the numerators are nonnegative, satisfy every normalisation and
    marginalisation constraint exactly, and vanish on forbidden pairs.  Returns None if no such d,
    else dict(den, value_int (exact value of the PUBLISHED instance at the point, a Fraction in
    units of 2^-SCALE), value (exact value of the float-table model, a Fraction in kcal/mol),
    support (number of nonzero site states per site))."""
    n = pm.n
    allv = np.concatenate([m.ravel() for m in mu1] + [m.ravel() for m in mu2.values()])
    den = None
    for d in range(1, maxden + 1):
        if np.abs(allv * d - np.rint(allv * d)).max() < tol:
            den = d
            break
    if den is None:
        return None
    N1 = [np.rint(m * den).astype(np.int64) for m in mu1]
    N2 = {key: np.rint(m * den).astype(np.int64) for key, m in mu2.items()}
    for i in range(n):
        if N1[i].min() < 0 or int(N1[i].sum()) != den:
            return None
    for (i, j), N in N2.items():
        if N.min() < 0 or not np.array_equal(N.sum(axis=1), N1[i]) or not np.array_equal(N.sum(axis=0), N1[j]):
            return None
        if pm.allowed is not None and N[~pm.allowed[(i, j)]].any():
            return None
    vi = sum(int((ipm.H[i].astype(object) * N1[i].astype(object)).sum()) for i in range(n)) \
        + sum(int((ipm.J[key].astype(object) * N2[key].astype(object)).sum()) for key in N2)
    vf = Fraction(0)
    for i in range(n):
        for a in np.flatnonzero(N1[i]):
            vf += Fraction(float(pm.A[i][a])) * int(N1[i][a])
    for (i, j), N in N2.items():
        for a, b in zip(*np.nonzero(N)):
            vf += Fraction(float(pm.M[(i, j)][a, b])) * int(N[a, b])
    return dict(den=den, value_int=Fraction(vi, den), value=vf / den,
                support=[int((N1[i] > 0).sum()) for i in range(n)], N1=N1, N2=N2)


# =============================================================================== certifying one leaf
TOL_T = 1e-9


def certify_leaf(pm, ipm, D):
    """Find and verify EXACTLY a certificate that the published instance is >= 0 on the box prod D.
    kind 'R' (the box contains the reference): shares with slack; kind 'N': the dual of the leaf.
    Returns dict(kind, lp (t of the share LP, or the relaxation value of the leaf, kcal/mol),
    ok (exact acceptance: LB >= 0 in integer arithmetic), LB (int, units of 2^-SCALE), m (integer
    messages or None))."""
    if contains_ref(pm, D):
        res = shares_lp(pm, D)
        if res["t"] is None:
            return dict(kind="R", lp=None, ok=False, LB=None, m=None)
        if res["t"] == math.inf:
            m = zero_messages(pm)
        else:
            m = shares_to_messages(ipm, D, res["s"])
        LB, U, P = leaf_bound(ipm, D, m)
        return dict(kind="R", lp=res["t"], ok=bool(LB >= 0), LB=LB, m=m)
    res = dual_lp(pm, D)
    if res["val"] is None:
        return dict(kind="N", lp=None, ok=False, LB=None, m=None)
    m = messages_to_int(res["m"])
    LB, U, P = leaf_bound(ipm, D, m)
    return dict(kind="N", lp=res["val"], ok=bool(LB >= 0), LB=LB, m=m)


def box_min(grid, D):
    """brute force: minimum of a grid over the box prod D."""
    return grid[np.ix_(*[np.asarray(d, dtype=int) for d in D])].min()


def n_states(D):
    out = 1
    for d in D:
        out *= len(d)
    return out


# =============================================================================== models of P4 (from P2's grids)
def second_order_grid(inst, name):
    """P4's second-order lower model on X' (p4_01_shares.py): L = f + g_star - sum_{i<j changed} c_ij,
    with x0 = argmin E over X', c = P2's measured class constants (recomputed by P4's routine).
    Returns (Lgrid, x0, E, C)."""
    f = inst["f"]; g = inst["R"][name]
    E = f + g
    x0 = L4.argmin_index(E)
    C = L4.c2_matrix(g)
    Lmod = f + L4.star_part(g, x0) - L4.pair_penalty(inst["shape"], x0, C)
    return Lmod, x0, E, C


def third_order_grids(inst):
    """P4's third-order pairwise lower models for g_GB on X' (p4_02_third.py): pair form and site form
    of Theorem 11.18a with P2's measured c_T.  Returns (m_pair, m_site, m_env, x0, E)."""
    f = inst["f"]; g = inst["R"]["GB"]; E = f + g
    shape = inst["shape"]; n = len(shape)
    x0 = L4.argmin_index(E)
    c3 = L4.c3_dict(g)
    gam = np.zeros(n); gam2 = np.zeros((n, n))
    for (i, j, k), v in c3.items():
        for s in (i, j, k):
            gam[s] += v / 3.0
        for (u, w_) in ((i, j), (i, k), (j, k)):
            gam2[u, w_] += v / 3.0; gam2[w_, u] += v / 3.0
    base = f + L4.interp2(g, x0)
    return (base - L4.pair_penalty(shape, x0, gam2), base - L4.site_penalty(shape, x0, gam),
            base - L4.triple_penalty(shape, x0, c3), x0, E)


def instance_files():
    """(tag, family, nres, backbone, tau string, P2 json path) for every analysis file of P2, as P4 lists them."""
    import glob, re
    out = []
    for p in sorted(glob.glob(os.path.join(L4.P2, "out", "an_fb_*_R3_t0.60_tau*.json"))):
        m = re.match(r"an_(fb_([A-Z]+?)c?(\d+)_([A-Za-z0-9]+)_R3_t0\.60)_tau([0-9.]+)\.json", os.path.basename(p))
        if m:
            out.append((m.group(1), m.group(2), int(m.group(3)), m.group(4), m.group(5), p))
    return out


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())


# =============================================================================== several triples (which may share pairs)
def _pairs_of(T):
    p_, q_, r_ = sorted(T)
    return [(p_, q_), (p_, r_), (q_, r_)]


def multi_triple_lp(pm, triples, D=None):
    """Shares with slack for the relaxation with the local-consistency constraints of SEVERAL triples.
    Certificate data: shares s_ij(a) (free in sign for a pair that lies in a triple), and for every
    triple T and each of its three pairs a table lam_{T,pq}(a, b) (the part of the reparametrised pair
    table that is handed to the triple), with
        loads    sum_{j != i} s_ij(a) + t <= A_i(a)                                            (a changed)
        pairs    M_ij(a,b) + s_ij(a) + s_ji(b) - sum_{T contains i,j} lam_{T,ij}(a,b) >= 0     (all a, b)
        triples  lam_{T,pq}(a,b) + lam_{T,pr}(a,c) + lam_{T,qr}(b,c) >= 0                      (all a, b, c)
    (s = 0 at reference states, lam = 0 at pairs of reference states).  t > 0 <=> certified with slack.
    Returns dict(t, s, lam) with lam[(T, (p, q))] a (k_p, k_q) array."""
    D = pm.dom if D is None else D
    assert contains_ref(pm, D) and pm.allowed is None
    n = pm.n
    triples = [tuple(sorted(T)) for T in triples]
    act = [i for i in range(n) if len(D[i]) >= 2]
    inT = {}
    for T in triples:
        for pq in _pairs_of(T):
            inT.setdefault(pq, []).append(T)
    off = {}
    nv = 0
    for i in act:
        for j in act:
            if i != j:
                off[(i, j)] = nv; nv += pm.shape[i]
    loff = {}
    for T in triples:
        for (p_, q_) in _pairs_of(T):
            loff[(T, (p_, q_))] = nv; nv += pm.shape[p_] * pm.shape[q_]
    tvar = nv
    lb = np.zeros(nv + 1); ub = np.zeros(nv + 1)
    inD = []
    for i in range(n):
        v = np.zeros(pm.shape[i], dtype=bool); v[D[i]] = True
        inD.append(v)
    for (i, j), o in off.items():
        ch = np.array([a for a in D[i] if a != pm.r[i]], dtype=int)
        ub[o + ch] = np.inf
        if (min(i, j), max(i, j)) in inT:
            lb[o + ch] = -np.inf
    for (T, (p_, q_)), o in loff.items():
        okm = inD[p_][:, None] & inD[q_][None, :]
        okm[pm.r[p_], pm.r[q_]] = False
        idx = o + np.flatnonzero(okm.ravel())
        lb[idx] = -np.inf; ub[idx] = np.inf
    lb[tvar] = -np.inf; ub[tvar] = np.inf
    rows, cols, vals, rhs = [], [], [], []
    nr = 0
    for i in act:
        for j in act:
            if i >= j:
                continue
            ai = np.asarray(D[i], dtype=int); bj = np.asarray(D[j], dtype=int)
            if (i, j) not in inT:
                ai = ai[ai != pm.r[i]]; bj = bj[bj != pm.r[j]]
                sub = pm.M[(i, j)][np.ix_(ai, bj)]
                ia, ib = np.nonzero(sub < 0)
                k = len(ia)
                if k:
                    rr = nr + np.arange(k)
                    rows += [rr, rr]; cols += [off[(i, j)] + ai[ia], off[(j, i)] + bj[ib]]; vals += [-np.ones(k), -np.ones(k)]
                    rhs.append(sub[ia, ib]); nr += k
            else:
                Aa, Bb = np.meshgrid(ai, bj, indexing="ij")
                Aa = Aa.ravel(); Bb = Bb.ravel()
                keep = ~((Aa == pm.r[i]) & (Bb == pm.r[j]))
                Aa = Aa[keep]; Bb = Bb[keep]
                k = len(Aa)
                rr = nr + np.arange(k)
                rows += [rr, rr]; cols += [off[(i, j)] + Aa, off[(j, i)] + Bb]; vals += [-np.ones(k), -np.ones(k)]
                for T in inT[(i, j)]:
                    rows.append(rr); cols.append(loff[(T, (i, j))] + Aa * pm.shape[j] + Bb); vals.append(np.ones(k))
                rhs.append(pm.M[(i, j)][Aa, Bb]); nr += k
    for T in triples:
        p_, q_, r_ = T
        A3, B3, C3 = np.meshgrid(D[p_], D[q_], D[r_], indexing="ij")
        A3 = A3.ravel(); B3 = B3.ravel(); C3 = C3.ravel()
        keep = ~((A3 == pm.r[p_]) & (B3 == pm.r[q_]) & (C3 == pm.r[r_]))
        A3 = A3[keep]; B3 = B3[keep]; C3 = C3[keep]
        k = len(A3)
        rr = nr + np.arange(k)
        rows += [rr, rr, rr]
        cols += [loff[(T, (p_, q_))] + A3 * pm.shape[q_] + B3, loff[(T, (p_, r_))] + A3 * pm.shape[r_] + C3, loff[(T, (q_, r_))] + B3 * pm.shape[r_] + C3]
        vals += [-np.ones(k), -np.ones(k), -np.ones(k)]
        rhs.append(np.zeros(k)); nr += k
    for i in act:
        ai = np.array([a for a in D[i] if a != pm.r[i]], dtype=int)
        k = len(ai)
        rr = nr + np.arange(k)
        for j in act:
            if j != i:
                rows.append(rr); cols.append(off[(i, j)] + ai); vals.append(np.ones(k))
        rows.append(rr); cols.append(np.full(k, tvar)); vals.append(np.ones(k))
        rhs.append(pm.A[i][ai]); nr += k
    Aub = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(nr, nv + 1))
    cost = np.zeros(nv + 1); cost[tvar] = -1.0
    res = linprog(cost, A_ub=Aub, b_ub=np.concatenate(rhs), bounds=np.c_[lb, ub], method="highs")
    if res.x is None:
        return dict(t=None, s=None, lam=None, status=res.message)
    s = {(i, j): np.zeros(pm.shape[i]) for i in range(n) for j in range(n) if i != j}
    for (i, j), o in off.items():
        s[(i, j)] = res.x[o:o + pm.shape[i]].copy()
    lam = {key: res.x[o:o + pm.shape[key[1][0]] * pm.shape[key[1][1]]].reshape(pm.shape[key[1][0]], pm.shape[key[1][1]]).copy() for key, o in loff.items()}
    return dict(t=float(res.x[tvar]), s=s, lam=lam, status="ok", nvar=nv + 1, nrow=nr)


def multi_triple_bound(ipm, D, mI, lamI, triples):
    """Exact integer checker of a certificate with several triples:
        U_i  = min_a [H_i(a) + sum_j m_ij(a)]
        R_ij = min_{a,b} [J_ij(a,b) - m_ij(a) - m_ji(b) - sum_{T contains i,j} lam_{T,ij}(a,b)]
        Q_T  = min_{a,b,c} [lam_{T,pq}(a,b) + lam_{T,pr}(a,c) + lam_{T,qr}(b,c)]
        LB   = sum U + sum R + sum Q   <=  (published instance)(x) for every x of the box.
    Returns (LB, U, R, Q)."""
    n = ipm.n
    triples = [tuple(sorted(T)) for T in triples]
    U = []
    for i in range(n):
        v = ipm.H[i][D[i]].copy()
        for j in range(n):
            if j != i:
                v = v + mI[(i, j)][D[i]]
        U.append(int(v.min()))
    R = {}
    for i in range(n):
        for j in range(i + 1, n):
            Tt = ipm.J[(i, j)][np.ix_(D[i], D[j])] - mI[(i, j)][D[i]][:, None] - mI[(j, i)][D[j]][None, :]
            for T in triples:
                if (i, j) in _pairs_of(T):
                    Tt = Tt - lamI[(T, (i, j))][np.ix_(D[i], D[j])]
            R[(i, j)] = int(Tt.min())
    Q = {}
    for T in triples:
        p_, q_, r_ = T
        S3 = (lamI[(T, (p_, q_))][np.ix_(D[p_], D[q_])][:, :, None] + lamI[(T, (p_, r_))][np.ix_(D[p_], D[r_])][:, None, :]
              + lamI[(T, (q_, r_))][np.ix_(D[q_], D[r_])][None, :, :])
        Q[T] = int(S3.min())
    return sum(U) + sum(R.values()) + sum(Q.values()), U, R, Q


def multi_triple_to_int(ipm, D, s, lam, triples):
    """integer certificate from the floating-point LP solution, with exact repairs: first the triple
    conditions (by raising lam), then the pair conditions (by raising shares)."""
    pm = ipm.pm
    n = ipm.n
    triples = [tuple(sorted(T)) for T in triples]
    inT = {}
    for T in triples:
        for pq in _pairs_of(T):
            inT.setdefault(pq, []).append(T)
    lamI = {}
    for key, v in lam.items():
        w = np.rint(np.asarray(v, dtype=float) * (2.0 ** SCALE)).astype(np.int64)
        (T, (p_, q_)) = key
        w[pm.r[p_], pm.r[q_]] = 0
        lamI[key] = w
    for T in triples:
        p_, q_, r_ = T
        Lpq, Lpr, Lqr = lamI[(T, (p_, q_))], lamI[(T, (p_, r_))], lamI[(T, (q_, r_))]
        S3 = Lpq[:, :, None] + Lpr[:, None, :] + Lqr[None, :, :]
        d = np.maximum(-S3, 0).max(axis=2)                      # per (a, b)
        d[pm.r[p_], pm.r[q_]] = 0
        Lpq += d
        S3 = Lpq[:, :, None] + Lpr[:, None, :] + Lqr[None, :, :]
        d = np.maximum(-S3, 0).max(axis=1)                      # per (a, c): what is left sits at (ref, ref, c)
        d[pm.r[p_], pm.r[r_]] = 0
        Lpr += d
        S3 = Lpq[:, :, None] + Lpr[:, None, :] + Lqr[None, :, :]
        d = np.maximum(-S3, 0).max(axis=0)
        d[pm.r[q_], pm.r[r_]] = 0
        Lqr += d
    S = {}
    for (i, j), v in s.items():
        w = np.ceil(np.asarray(v, dtype=float) * (2.0 ** SCALE)).astype(np.int64)
        if (min(i, j), max(i, j)) not in inT:
            w = np.maximum(w, 0)
        w[pm.r[i]] = 0
        S[(i, j)] = w
    for i in range(n):
        for j in range(i + 1, n):
            if len(D[i]) < 2 or len(D[j]) < 2:
                continue
            Tt = ipm.J[(i, j)] + S[(i, j)][:, None] + S[(j, i)][None, :]
            for T in inT.get((i, j), []):
                Tt = Tt - lamI[(T, (i, j))]
            d = np.maximum(-Tt, 0).max(axis=1)                  # per state a of i
            d[pm.r[i]] = 0
            S[(i, j)] += d
            Tt = Tt + d[:, None]
            d = np.maximum(-Tt, 0).max(axis=0)                  # what is left sits in the reference row of i
            d[pm.r[j]] = 0
            S[(j, i)] += d
    return {key: -v for key, v in S.items()}, lamI
