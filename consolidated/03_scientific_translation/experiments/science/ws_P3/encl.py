"""
P3 -- rigorous enclosures of the derivatives of the three univariate functions of dfun.py, by
interval arithmetic (mpmath.iv: arbitrary-precision intervals with outward rounding) on cells,
and range-maximum queries on the resulting tables.

  * For an atom class (or, offset, al, be, ga) and a cell X = [I_a, I_b] of the descreening
    integral: Taylor coefficients of ib(X + t) and ell(X + t) = -ln ib(X + t) in t, computed with
    interval power-series arithmetic.  The k-th coefficient encloses phi^(k)(xi)/k! for EVERY
    xi in X (interval automatic differentiation), so  k! * mag(c_k)  bounds sup_X |phi^(k)|.
  * For the kernel: d^k h/dw^k (w; r) = (2/r) zeta_k(D), zeta_k(D) = sqrt(D) eta_k(D),
    D = r^2 e^{-w}/4 (r > 0); eta_k is the explicit finite sum of monomials
    coef * D^a * exp(-bD) * (4D + exp(-D))^(-c/2) of dfun.ETA_TERMS (exact rational coefficients).
    On a cell of D every monomial is evaluated in interval arithmetic.

Every table entry is an upper bound stored as a double rounded UP.  Queries take the maximum over
all cells that meet the query interval (after widening the query by a relative 1e-9 to absorb the
rounding of the query's own endpoints).
"""
import os, math, hashlib, json
from fractions import Fraction
import numpy as np
import mpmath
from mpmath import iv
from mpmath.libmp import to_float

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
iv.prec = 80
KMAX = 6


# ----------------------------------------------------------------------------- interval series
def s_mul(a, b, K):
    return [sum((a[j] * b[k - j] for j in range(k + 1)), iv.mpf(0)) for k in range(K + 1)]


def s_inv(a, K):
    b = [1 / a[0]]
    for k in range(1, K + 1):
        b.append(-sum((a[j] * b[k - j] for j in range(1, k + 1)), iv.mpf(0)) / a[0])
    return b


def s_exp(a, K):
    e = [iv.exp(a[0])]
    for k in range(1, K + 1):
        e.append(sum((j * a[j] * e[k - j] for j in range(1, k + 1)), iv.mpf(0)) / k)
    return e


def s_log(a, K):
    l = [iv.log(a[0])]
    for k in range(1, K + 1):
        acc = a[k] - sum((j * l[j] * a[k - j] for j in range(1, k)), iv.mpf(0)) / k if k > 1 else a[k]
        l.append(acc / a[0])
    return l


def up(x):
    """double >= the largest magnitude in the interval x (directed rounding of the raw endpoint)."""
    lo, hi = abs(x)._mpi_
    return to_float(hi, rnd="c")


def lo_hi(x):
    """doubles (a, b) with a <= x.a and b >= x.b (directed rounding)."""
    lo, hi = x._mpi_
    return to_float(lo, rnd="f"), to_float(hi, rnd="c")


JT = 2          # order of the Taylor form used on a cell (see atom_cell / zeta tables)


def _atom_series(orr, off, al, be, ga, X, K):
    """interval Taylor coefficients (order 0..K) of ib(X + t) and ell(X + t)."""
    o = iv.mpf(orr)
    rad = o + iv.mpf(off)
    psi = [o * X, o] + [iv.mpf(0)] * (K - 1)
    psi2 = s_mul(psi, psi, K)
    psi3 = s_mul(psi2, psi, K)
    P = [iv.mpf(al) * psi[k] - iv.mpf(be) * psi2[k] + iv.mpf(ga) * psi3[k] for k in range(K + 1)]
    e2 = s_exp([2 * c for c in P], K)
    e2[0] = e2[0] + 1
    inv = s_inv(e2, K)                               # 1/(exp(2P) + 1);  tanh P = 1 - 2/(exp(2P)+1)
    ib = [2 * c / rad for c in inv]                  # -tanh/rad = (2 inv - 1)/rad
    ib[0] = ib[0] + 1 / o - 1 / rad                  # ib = 1/or - (1 - 2 inv)/rad
    ell = [-c for c in s_log(ib, K)]
    return ib, ell


def atom_cell(orr, off, al, be, ga, Ia, Ib, K=KMAX):
    """Upper bounds (doubles rounded up) of sup_{[Ia,Ib]} |ib^(k)| and |ell^(k)|, k = 0..K, and an
    enclosure of the values of ell on the cell.  Taylor form of order JT about the midpoint c:
        sup |phi^(k)| <= sum_{j<JT} sigma^j/j! |phi^(k+j)(c)| + sigma^JT/JT! * sup_cell |phi^(k+JT)|,
    sigma >= half the cell width; the point values come from the interval series at the (thin)
    midpoint interval, the last supremum from the interval series over the whole cell."""
    X = iv.mpf([Ia, Ib])
    c = (iv.mpf(Ia) + iv.mpf(Ib)) / 2
    sigma = abs(X - c)
    ib_c, ell_c = _atom_series(orr, off, al, be, ga, c, K + JT)
    ib_X, ell_X = _atom_series(orr, off, al, be, ga, X, K + JT)
    fact = [math.factorial(k) for k in range(K + JT + 1)]

    def sups(sc, sX):
        out = []
        for k in range(K + 1):
            acc = iv.mpf(0)
            for j in range(JT):
                acc += sigma ** j / fact[j] * abs(sc[k + j] * fact[k + j])
            acc += sigma ** JT / fact[JT] * abs(sX[k + JT] * fact[k + JT])
            out.append(up(acc))
        return out
    return sups(ib_c, ib_X), sups(ell_c, ell_X), lo_hi(ell_X[0]), lo_hi(ib_X[0])


def _eta_terms(K):
    import dfun
    T = [dict(t) for t in dfun.ETA_TERMS]
    while len(T) <= K:
        T.append(dfun._L(T[-1]))
    return T


def _zeta_iv(terms, D):
    """interval value of sqrt(D) * sum of monomials at the interval D."""
    E = iv.exp(-D)
    u = 4 * D + E
    sq = iv.sqrt(D)
    us = iv.sqrt(u)
    acc = iv.mpf(0)
    for (a, b, c2), v in terms.items():
        acc += iv.mpf(v.numerator) / iv.mpf(v.denominator) * (sq * D ** a * E ** b / us ** c2)
    return acc


def zeta_cell(T, k, Da, Db, J=3):
    """Upper bound (double) of sup over D in [Da, Db] (Da > 0) of |zeta_k(D)|, zeta_k = sqrt(D) eta_k(D).
    In the variable s = ln D:  d zeta_k / ds = -zeta_{k+1}   (because eta_{k+1} = -eta_k/2 - D eta_k').
    Taylor form about the centre s_c with half-width sigma:
        sup |zeta_k| <= sum_{j<J} sigma^j/j! |zeta_{k+j}(D_c)| + sigma^J/J! * sup_cell |zeta_{k+J}|,
    the last supremum by plain interval evaluation of the monomials over the cell.  T: list of
    monomial dictionaries up to order k + J."""
    la, lb = iv.log(iv.mpf(Da)), iv.log(iv.mpf(Db))
    sc = (la + lb) / 2
    sigma = iv.mpf(up((lb - la) / 2))                # >= half-width of the cell in s
    Dc = iv.exp(sc)
    acc = iv.mpf(0)
    fact = 1
    for j in range(J):
        if j:
            fact *= j
        acc += sigma ** j / fact * abs(_zeta_iv(T[k + j], Dc))
    fact *= J
    acc += sigma ** J / fact * abs(_zeta_iv(T[k + J], iv.mpf([Da, Db])))
    return up(acc)


def zeta_cell0(terms, Db):
    """plain interval bound of sup_{[0, Db]} |zeta_k| (first cell, D down to 0)."""
    return up(_zeta_iv(terms, iv.mpf([0.0, Db])))


def zeta_tail(terms, D0):
    """bound of sup_{D >= D0} |sqrt(D) eta_k(D)| for k >= 1: every monomial has b >= 1 and u >= 1,
    so |mono| <= D^(a+1/2) exp(-D), which decreases for D >= a + 1/2."""
    D = iv.mpf(D0)
    acc = iv.mpf(0)
    for (a, b, c2), v in terms.items():
        assert b >= 1 and D0 >= a + 0.5
        acc += abs(iv.mpf(v.numerator) / iv.mpf(v.denominator)) * iv.sqrt(D) * D ** a * iv.exp(-D)
    return up(acc)


# ----------------------------------------------------------------------------- range maximum
class RangeMax:
    def __init__(self, v):
        v = np.asarray(v, dtype=float)
        self.n = len(v)
        self.tab = [v]
        j = 1
        while 2 * j <= self.n:
            prev = self.tab[-1]
            self.tab.append(np.maximum(prev[:-j], prev[j:]))
            j *= 2

    def query(self, lo, hi):
        """max of v[lo..hi] inclusive (integer arrays, lo <= hi)."""
        lo = np.asarray(lo); hi = np.asarray(hi)
        ln = hi - lo + 1
        lev = np.floor(np.log2(ln)).astype(int)
        out = np.empty(lo.shape)
        for L in np.unique(lev):
            m = lev == L
            t = self.tab[L]
            out[m] = np.maximum(t[lo[m]], t[hi[m] - (1 << int(L)) + 1])
        return out


class EnvelopeSup:
    """Rigorous derivative suprema for a GBModel (provider for termwise / gf bounds)."""

    def __init__(self, G, K=KMAX, ncell_I=1200, ncell_D=2400, Imax=24.0, verbose=False):
        self.G = G
        self.K = K
        os.makedirs(CACHE, exist_ok=True)
        # atom classes
        keys = [(float(G.orr[p]), float(G.off), float(G.al[p]), float(G.be[p]), float(G.ga[p])) for p in range(G.nat)]
        self.classes = sorted(set(keys))
        self.cls = np.array([self.classes.index(k) for k in keys])
        self.Imax = Imax
        self.edges = np.linspace(0.0, Imax, ncell_I + 1)
        self.atab = []
        for c in self.classes:
            self.atab.append(self._atom_table(c, verbose))
        self._zeta_table(ncell_D, verbose)

    # -- atom tables
    def _atom_table(self, c, verbose):
        tag = hashlib.sha1(json.dumps(["atom2", c, self.K, list(self.edges[[0, -1]]), len(self.edges), iv.prec, JT]).encode()).hexdigest()[:16]
        fn = os.path.join(CACHE, f"atom_{tag}.npz")
        if os.path.exists(fn):
            z = np.load(fn)
            d = dict(supB=z["supB"], supL=z["supL"], ell_lo=z["ell_lo"], ell_hi=z["ell_hi"])
        else:
            n = len(self.edges) - 1
            supB = np.zeros((self.K + 1, n)); supL = np.zeros((self.K + 1, n))
            ell_lo = np.zeros(n); ell_hi = np.zeros(n)
            for m in range(n):
                sb, sl, el, _ = atom_cell(*c, self.edges[m], self.edges[m + 1], self.K)
                supB[:, m] = sb; supL[:, m] = sl
                ell_lo[m], ell_hi[m] = el
            np.savez(fn, supB=supB, supL=supL, ell_lo=ell_lo, ell_hi=ell_hi)
            d = dict(supB=supB, supL=supL, ell_lo=ell_lo, ell_hi=ell_hi)
            if verbose:
                print(f"   enclosure table for atom class {c}: {n} cells -> {fn}", flush=True)
        d["rmB"] = [RangeMax(d["supB"][k]) for k in range(self.K + 1)]
        d["rmL"] = [RangeMax(d["supL"][k]) for k in range(self.K + 1)]
        d["rm_ehi"] = RangeMax(d["ell_hi"])
        d["rm_elo"] = RangeMax(-d["ell_lo"])
        return d

    def _cells(self, Ilo, Ihi):
        w = 1e-9 * (1.0 + np.abs(Ihi))
        a = np.searchsorted(self.edges, Ilo - w, side="right") - 1
        b = np.searchsorted(self.edges, Ihi + w, side="left") - 1
        if (a < 0).any() or (b >= len(self.edges) - 1).any():
            raise ValueError(f"descreening integral outside the enclosure grid [0, {self.Imax}]: {Ilo.min()}, {Ihi.max()}")
        return a, np.maximum(a, b)

    def _per_class(self, atoms, Ilo, Ihi, name, k=None):
        a, b = self._cells(np.asarray(Ilo), np.asarray(Ihi))
        out = np.empty(len(atoms))
        cl = self.cls[atoms]
        for c in np.unique(cl):
            m = cl == c
            rm = self.atab[c][name] if k is None else self.atab[c][name][k]
            out[m] = rm.query(a[m], b[m])
        return out

    def sup_ib(self, k, atoms, Ilo, Ihi):
        return self._per_class(atoms, Ilo, Ihi, "rmB", k)

    def sup_ell(self, k, atoms, Ilo, Ihi):
        return self._per_class(atoms, Ilo, Ihi, "rmL", k)

    def ell_range(self, atoms, Ilo, Ihi):
        """rigorous enclosure [lo, hi] of ell over [Ilo, Ihi]."""
        hi = self._per_class(atoms, Ilo, Ihi, "rm_ehi")
        lo = -self._per_class(atoms, Ilo, Ihi, "rm_elo")
        return lo, hi

    # -- kernel table
    def _zeta_table(self, ncell, verbose):
        self.Dmin, self.Dmax = 1e-5, 80.0
        tag = hashlib.sha1(json.dumps(["zeta2", self.K, self.Dmin, self.Dmax, ncell, iv.prec]).encode()).hexdigest()[:16]
        fn = os.path.join(CACHE, f"zeta_{tag}.npz")
        self.ledges = np.linspace(math.log(self.Dmin), math.log(self.Dmax), ncell + 1)
        self.Dedges = np.exp(self.ledges)
        if os.path.exists(fn):
            tab = np.load(fn)["tab"]
        else:
            JZ = 3
            terms = _eta_terms(self.K + JZ)
            tab = np.zeros((self.K + 1, ncell + 2))       # cell 0: [0, Dmin]; cells 1..ncell; last: [Dmax, inf)
            for k in range(1, self.K + 1):
                tab[k, 0] = zeta_cell0(terms[k], math.nextafter(self.Dedges[0], math.inf))
                for m in range(ncell):
                    tab[k, m + 1] = zeta_cell(terms, k, math.nextafter(self.Dedges[m], 0.0), math.nextafter(self.Dedges[m + 1], math.inf), JZ)
                tab[k, ncell + 1] = zeta_tail(terms[k], math.nextafter(self.Dedges[-1], 0.0))
            np.savez(fn, tab=tab)
            if verbose:
                print(f"   enclosure table for zeta_k: {ncell} cells -> {fn}", flush=True)
        self.ztab = tab
        self.rmZ = [None] + [RangeMax(tab[k]) for k in range(1, self.K + 1)]

    def sup_h(self, k, r, wlo, whi):
        """upper bound of sup_{w in [wlo, whi]} |d^k h/dw^k (w; r)| for r > 0 (arrays)."""
        r = np.asarray(r, dtype=float)
        Dlo = r * r * np.exp(-whi) / 4.0 * (1.0 - 1e-9)
        Dhi = r * r * np.exp(-wlo) / 4.0 * (1.0 + 1e-9)
        a = np.clip(np.searchsorted(self.Dedges, Dlo, side="right"), 0, len(self.Dedges))
        b = np.clip(np.searchsorted(self.Dedges, Dhi, side="left"), 0, len(self.Dedges))
        b = np.maximum(a, b)
        z = self.rmZ[k].query(a.ravel(), b.ravel()).reshape(r.shape)
        return 2.0 / r * z * (1.0 + 1e-12)
