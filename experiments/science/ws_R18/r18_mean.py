#!/usr/bin/env python3
"""r18_mean.py -- workstream R18 (science division): an own "mean run" of Algorithm 2L+.

Written from the statements only:
  * the algorithm and its constants: K_REPORT.md §2.1-2.2 (theory branch, as in our repository);
  * what a mean run is and how evaluations are counted: ENG-RES-0008 §1 ("every count of the algorithm is
    replaced by its mean"; calls_{l+1} = sum_w P(W = w) max{M_j : j <= j_stop, w e^{b-A_l} <= s_j < w e^{B_l}};
    evaluations = 1 + max_j M_j + sum_l calls_l C_l);
  * the positions and the placement-free bound: ENG-RES-0014 §1 and §4.
No code of the engineering division is imported here, and none of r6lib.

What is exact.  A mean run is a deterministic object, and ties in it are structural (a level set of probability
exactly 1/2; the reference fibre exactly on the level grid).  So:
  - probabilities are integers over a common denominator; "populated" (N = M P(HIGH) >= K), the radii of steps
    (b) and (c) and the comparison q >= 1 are integer comparisons;
  - every logarithm that is compared with a level (ln W, the place t0, the positions, the ladder, b, lambda,
    ln s_0) is a Fraction, so the classification and the windows are exact;
  - magnitudes (ell, tails, thresholds, sums) are mpmath numbers with 50 digits.

An instance is a list of atoms (ln W, weight, place t0, behaviour): a product instance has one place and one
behaviour; an instance that is not a product has several.  The classification shift is computed PER ATOM
(c = max_l min(b - A_l, B_l) with the atom's own A_0 = t0, B_0 = x_0 - t0), so nothing is assumed about it.
"""
import bisect
import math
from fractions import Fraction as Fr

import mpmath as mp

mp.mp.dps = 50


# ---------------------------------------------------------------------------------------------- the cube
class Cube:
    """|B(m,r)| (exact), E_r(m) = sum_{j<=r} C(m,j)(e^{u(r+1-j)} - 1), T_m(k) = sum_j C(m,j) e^{-u (j-k)_+}."""

    def __init__(self, m, u):
        self.m, self.u = m, mp.mpf(u.numerator) / u.denominator if isinstance(u, Fr) else mp.mpf(u)
        eu, emu = mp.e ** self.u, mp.e ** (-self.u)
        self.binom = [math.comb(m, j) for j in range(m + 1)]
        self.ball, s = [], 0
        for c in self.binom:
            s += c
            self.ball.append(s)
        # E_r = sum_{j<=r} C(m,j) e^{u(r+1-j)} - |B(r)|;  with S_r = sum_{j<=r} C(m,j) e^{u(r-j)}:  S_r = e^u S_{r-1} + C(m,r)
        self.E, S = [], mp.mpf(0)
        for r in range(m + 1):
            S = eu * S + self.binom[r]
            self.E.append(eu * S - self.ball[r])
        # T_m(k) = |B(k)| + sum_{j>k} C(m,j) e^{-u(j-k)};  R_k := that sum;  R_{k-1} = e^{-u}(C(m,k) + R_k)
        self.T, R = [None] * (m + 1), mp.mpf(0)
        for k in range(m, -1, -1):
            self.T[k] = self.ball[k] + R
            R = emu * (self.binom[k] + R)

    def largest_ball_le(self, x):
        """largest k >= 0 with |B(m,k)| <= x, for an integer x >= 1."""
        return bisect.bisect_right(self.ball, x) - 1

    def least_ball_ge(self, x):
        """least r >= 0 with |B(m,r)| >= x, for an integer 1 <= x <= 2^m."""
        return bisect.bisect_left(self.ball, x)


# ---------------------------------------------------------------------------------------------- the design
class Design:
    """Parameters and constants of Algorithm 2L+ (K_REPORT §2.1-2.2).  u, lam, b, eta and the ladder are Fractions."""

    def __init__(self, n, n_o, u, lam, eta, etap, theta, nu1, b, delta, xs, lC=None, K_override=None):
        self.n, self.n_o, self.n_i = n, n_o, n - n_o
        assert 1 <= n_o <= n - 1
        self.u, self.lam, self.b, self.eta = Fr(u), Fr(lam), Fr(b), Fr(eta)
        assert 0 < self.lam and 0 < self.eta <= Fr(1, 2) and self.b > 0
        self.xs = [Fr(x) for x in xs]
        self.L = len(self.xs) - 1
        assert self.L >= 1 and all(self.xs[i] > self.xs[i + 1] for i in range(self.L)), "ladder must decrease strictly"
        assert self.xs[0] == 2 * self.u * self.n_i, "x_0 = 2 u n_i"
        assert self.xs[-1] <= self.b, "x_L <= b"
        f = lambda q: mp.mpf(q.numerator) / q.denominator                      # noqa: E731
        self.f = f
        um, lamm, bm, etam = f(self.u), f(self.lam), f(self.b), f(self.eta)
        self.etap, self.theta, self.nu1, self.delta = mp.mpf(etap), mp.mpf(theta), mp.mpf(nu1), mp.mpf(delta)
        cube = self.cube = Cube(n_o, self.u)
        m = n_o
        c_eta = (1 - self.eta) / (1 + self.eta)                                 # Fraction
        self.J = int(mp.ceil((2 * um * n + bm + m * mp.log(2)) / lamm))
        self.nu0 = max((self.J + 1) * (mp.e ** lamm - 1) / self.etap, self.nu1) / (1 - etam)
        # r-dagger: the largest r in {0..m-1} such that for every r' <= r:  Gt(r') <= theta (1-eta) nu0  and
        #           min{Gt(r')/c_eta, G2(r')} <= theta;   Gt(0) = e^u - 1, Gt(r) = E_r/|B(r-1)|;  G2(r) = E_r/T(kappa(r)),
        #           kappa(r) = the largest k >= 0 with |B(k)| <= max{1, c_eta |B(r-1)|}
        rd = -1
        for r in range(m):
            gt = (mp.e ** um - 1) if r == 0 else cube.E[r] / cube.ball[r - 1]
            bound = max(1, (c_eta.numerator * (cube.ball[r - 1] if r >= 1 else 0)) // c_eta.denominator)
            kap = cube.largest_ball_le(bound)
            g2 = cube.E[r] / cube.T[kap]
            if gt <= self.theta * (1 - etam) * self.nu0 and min(gt / f(c_eta), g2) <= self.theta:
                rd = r
            else:
                break
        self.r_dag = rd
        self.pi_dag = mp.mpf(cube.ball[rd]) / (1 << m) if rd >= 0 else mp.mpf(1) / (1 << (m + 1))
        self.m_max = int(mp.ceil(mp.log(2 * (1 + etam) * mp.e ** lamm * self.nu0 / ((1 - etam) * self.pi_dag), 2)))
        self.K_theorem = int(mp.ceil(3 * (1 + etam) / etam ** 2 * mp.log(2 * (self.J + 1) * (self.m_max + 1) * (self.L + 2) / self.delta)))
        self.K = self.K_theorem if K_override is None else int(K_override)
        self.nu = self.K * self.nu0
        self.M_dag = self.K / ((1 - etam) * self.pi_dag)
        self.M_bar = 2 * (1 + etam) * mp.e ** lamm * self.nu0 * self.M_dag
        self.x_out = mp.log((2 / (1 + mp.e ** um)) ** n + mp.e ** bm * (mp.e ** lamm * (1 + etam) / (1 - etam) + self.etap + self.theta))
        self.lC = None if lC is None else [None] + [mp.mpf(x) for x in lC[1:]]   # ln C_l, l = 1..L
        self.lCmax = None
        if self.lC is not None:
            tot = 1 + 2 * self.M_bar
            for l in range(1, self.L + 1):
                tot += min(2 * self.M_bar, (self.J + 1) * self.cnt(self.xs[l - 1])) * mp.e ** self.lC[l]
            self.lCmax = mp.log(tot)

    def cnt(self, x):
        etam = self.f(self.eta)
        return max(mp.mpf(self.K), 2 * (1 + etam) ** 2 / (1 - etam) * mp.e ** self.f(self.lam) * self.nu * mp.e ** self.f(Fr(x)))


# ---------------------------------------------------------------------------------------------- positions
def nested_positions(D, t0, pos):
    """(A_l, B_l) for l = 0..L: A_0 = t0, B_0 = x_0 - t0, running minima with the rung positions pos[l-1] = (alpha_l, beta_l)."""
    A, B = [Fr(t0)], [D.xs[0] - Fr(t0)]
    for (a, be) in pos:
        A.append(min(A[-1], a))
        B.append(min(B[-1], be))
    return A, B


def shift_c(D, A, B):
    """c = max_l min(b - A_l, B_l)."""
    return max(min(D.b - a, be) for a, be in zip(A, B))


def uniform_positions(D, kind):
    """rung positions (alpha_l, beta_l), l = 1..L, for a uniform behaviour: 'bottom', 'top', or a share t in [0,1]
    (value at W e^{-t x_l} above the lower end: t = 0 is bottom, 1 is top, 1/2 the centre)."""
    if kind == "bottom":
        t = Fr(0)
    elif kind == "top":
        t = Fr(1)
    else:
        t = Fr(kind)
    return [(t * x, (1 - t) * x) for x in D.xs[1:]]


# ---------------------------------------------------------------------------------------------- the mean run
class MeanRun:
    """Result of mean_run: status, j_stop, per-level kind / pass index m / P(HIGH), calls per rung, cost."""


def _ceil(q):
    return -((-q.numerator) // q.denominator)


POP_TOL_THEIRS = (10 ** 18 - 693147, 10 ** 18)       # 2^{-1e-12} = 1 - 6.93147e-13: the tolerance of their test "populated"


def mean_run(D, atoms, den, psi0, harper=True, union=None, c_force=None, record_levels=True, pop_tol=None):
    """Algorithm 2L+ with every count replaced by its mean.

    atoms : list of (lnW: Fraction, wt: int, t0: Fraction, pos: list of (alpha_l, beta_l) Fractions for l = 1..L)
            P(atom) = wt/den.  Atoms with equal ln W and different places/behaviours are allowed (not a product).
    psi0  : Fraction, the value at the reference point (s_0 = e^{-psi0 - u n}).
    union : None, or (lo, hi): the refinement windows are replaced by their union over places t0 in [lo, hi]
            (ENG-RES-0014 §4: A_0 = hi, B_0 = x_0 - lo), THE CLASSIFICATION IS LEFT AS IT IS (each atom's own c).
    c_force : None, or a Fraction: every atom is classified with this shift (to reproduce a convention).
    pop_tol : None: a pass is populated iff N = M P(HIGH) >= K exactly.  (num, dn): iff M P(HIGH) >= K num/dn -- to
              reproduce the engineering reference, whose test is  m >= -log2 P(HIGH) - 1e-12  (POP_TOL_THEIRS).
    """
    cube, m = D.cube, D.n_o
    lam, b = D.lam, D.b
    f = D.f
    lamm, bm, etam = f(lam), f(b), f(D.eta)
    eta_n, eta_d = D.eta.numerator, D.eta.denominator
    two_m = 1 << m
    assert sum(a[1] for a in atoms) == den, "weights must sum to the denominator"
    q0, rem = divmod(den, two_m)
    assert rem == 0, "denominator must be a multiple of 2^{n_o}"
    ls0 = -Fr(psi0) - D.u * D.n
    J = D.J
    # ---- classification: atom HIGH at level j  iff  lnW > ls0 + j lam - c  iff  j <= jH := ceil((lnW + c - ls0)/lam) - 1
    pos_cache = {}
    jH, AB = [], []
    for (lnW, wt, t0, pos) in atoms:
        key = (t0, id(pos))
        if key not in pos_cache:
            A, B = nested_positions(D, t0, pos)
            pos_cache[key] = (A, B, shift_c(D, A, B))
        A, B, c = pos_cache[key]
        if c_force is not None:
            c = Fr(c_force)
        jH.append(_ceil((lnW + c - ls0) / lam) - 1)
        AB.append((A, B))
    # numerator of P(HIGH at level j) over den: sum of wt over atoms with jH >= j
    order = sorted(range(len(atoms)), key=lambda i: -jH[i])
    thr = [-jH[i] for i in order]                 # ascending
    cum, s = [], 0
    for i in order:
        s += atoms[i][1]
        cum.append(s)

    def high_num(j):
        k = bisect.bisect_right(thr, -j)          # atoms with jH >= j
        return cum[k - 1] if k else 0

    R = MeanRun()
    e_lam, e_b = mp.e ** lamm, mp.e ** bm
    um = f(D.u)
    ell = ((1 + mp.e ** (-um)) / 2) ** D.n * mp.e ** (um * D.n)       # units of s_0:  e^{-psi0}((1+e^{-u})/2)^n / s_0
    Sigma, upper = mp.mpf(0), mp.mpf(0)
    sj = mp.mpf(1)
    ms, kinds, phs = [], [], []
    R.status, R.j_stop = None, None
    npop = nneg = 0
    for j in range(J + 1):
        if j:
            sj = sj * e_lam
        hn = high_num(j)                                              # P(HIGH) = hn/den
        Mneg = D.nu * sj / (ell * e_b)                                # with ell at the entry of the level
        mm = 0
        while True:
            M_over_K = 1 << mm
            populated = (M_over_K * hn >= den)                        # N = K 2^m hn/den >= K
            if not populated and pop_tol is not None and M_over_K * hn * pop_tol[1] >= den * pop_tol[0]:
                populated = True
                R.n_pop_by_tolerance = getattr(R, "n_pop_by_tolerance", 0) + 1
            if populated:
                # q = min{1, P/(1-eta)};  p_low = P/(1+eta)
                q_is_one = (hn * eta_d >= den * (eta_d - eta_n))
                plow = mp.mpf(hn * eta_d) / (den * (eta_d + eta_n))
                kH = cube.largest_ball_le(max(1, (hn * eta_d) // (q0 * (eta_d + eta_n))))
                ell = max(ell, sj / e_b * plow)
                if harper:
                    ell = max(ell, sj / e_b * cube.T[kH] / two_m)
                if q_is_one:
                    q, tail, r = mp.mpf(1), mp.inf, m
                else:
                    q = mp.mpf(hn * eta_d) / (den * (eta_d - eta_n))
                    num, dn = hn * eta_d, q0 * (eta_d - eta_n)        # 2^m q = num/dn
                    if num < dn:
                        tail, r = mp.mpf(0), -1
                    else:
                        r = cube.least_ball_ge(-((-num) // dn))
                        tail = sj * cube.E[r] / two_m if r <= m - 1 else mp.inf
            else:
                # q = min{1, K/((1-eta) M)} = min{1, eta_d/((eta_d - eta_n) 2^mm)}
                num, dn = two_m * eta_d, (eta_d - eta_n) * M_over_K   # 2^m q = num/dn  (if q < 1)
                if eta_d >= (eta_d - eta_n) * M_over_K:
                    q, tail, r = mp.mpf(1), mp.inf, m
                else:
                    q = mp.mpf(eta_d) / ((eta_d - eta_n) * M_over_K)
                    if num < dn:
                        tail, r = mp.mpf(0), -1
                    else:
                        r = cube.least_ball_ge(-((-num) // dn))
                        tail = sj * cube.E[r] / two_m if r <= m - 1 else mp.inf
            if tail <= D.theta * e_b * ell:                           # (c) the closure test
                Lo = max(ell, Sigma + ((1 - 1 / e_lam) / e_b * sj * plow if populated else 0))
                Up = 1 + upper + tail
                R.status = "closed-populated" if populated else "closed-unpopulated"
                R.j_stop, R.r_close = j, r
                R.lnL_rel, R.lnU_rel = mp.log(Lo), mp.log(Up)         # relative to s_0
                ms.append(mm); kinds.append("STOP"); phs.append(hn)
                break
            if populated:                                             # (d)
                Sigma += (1 - 1 / e_lam) / e_b * sj * plow
                upper += (e_lam - 1) * sj * q
                ms.append(mm); kinds.append("POP"); phs.append(hn); npop += 1
                break
            if D.K * M_over_K >= Mneg:                                # (e)
                upper += (e_lam - 1) * sj * q
                ms.append(mm); kinds.append("NEG"); phs.append(hn); nneg += 1
                break
            if mm + 1 > D.m_max:                                      # (f) would exceed K 2^m_max
                R.status, R.j_stop = "abort-sample", j
                ms.append(mm); kinds.append("ABORT"); phs.append(hn)
                break
            mm += 1
        if R.status is not None:
            break
    else:
        R.status, R.j_stop = "abort-levels", J
    R.ms, R.kinds, R.high_num, R.den = ms, kinds, phs, den
    R.npop, R.nneg = npop, nneg
    R.m_top = max(ms)
    R.lM_max = mp.log(D.K) + R.m_top * mp.log(2)
    R.ls0 = ls0
    # ---- evaluations: calls of I_{l+1} = sum over atoms of P(atom) max{M_j : j <= j_stop, lnW + b - A_l <= ls_j < lnW + B_l}
    jstop = R.j_stop
    # sparse table for range maxima of ms
    table = [ms[:]]
    k = 1
    while (1 << k) <= len(ms):
        prev = table[-1]
        half = 1 << (k - 1)
        table.append([max(prev[i], prev[i + half]) for i in range(len(ms) - (1 << k) + 1)])
        k += 1

    def range_max(lo, hi):
        kk = (hi - lo + 1).bit_length() - 1
        return max(table[kk][lo], table[kk][hi - (1 << kk) + 1])

    L = D.L
    calls_num = [0] * (L + 1)                      # calls_l = K * calls_num[l] / den
    if union is not None:
        ulo, uhi = Fr(union[0]), Fr(union[1])
    win_cache = {}
    for i, (lnW, wt, t0, pos) in enumerate(atoms):
        if union is None:
            A, B = AB[i]
        else:
            key = id(pos)
            if key not in win_cache:
                A_, B_ = [uhi], [D.xs[0] - ulo]
                for (a, be) in pos:
                    A_.append(min(A_[-1], a))
                    B_.append(min(B_[-1], be))
                win_cache[key] = (A_, B_)
            A, B = win_cache[key]
        base = lnW - ls0
        for l in range(L):
            lo = max(_ceil((base + b - A[l]) / lam), 0)
            hi = min(_ceil((base + B[l]) / lam) - 1, jstop)
            if lo <= hi:
                calls_num[l + 1] += wt << range_max(lo, hi)
    R.calls = [None] + [mp.mpf(D.K * calls_num[l]) / den for l in range(1, L + 1)]
    R.lcalls = [None] + [(mp.log(c) if c > 0 else -mp.inf) for c in R.calls[1:]]
    R.calls_num = calls_num
    if D.lC is not None:
        tot = 1 + mp.mpf(D.K) * (1 << R.m_top)
        for l in range(1, L + 1):
            tot += R.calls[l] * mp.e ** D.lC[l]
        R.lcost = mp.log(tot)
    else:
        R.lcost = None
    return R


# ---------------------------------------------------------------------------------------------- instances
def radial_atoms(D, F, c_in, t0=None, pos=None):
    """Atoms of the product instance  psi(a, b) = F(d(a)) + F_i(b):  ln W = c_in - F(d), P = C(n_o, d)/2^{n_o},
    place t0 = u n_i + c_in (unless given).  F: list of Fractions of length n_o + 1."""
    t0 = D.u * D.n_i + Fr(c_in) if t0 is None else Fr(t0)
    return [(Fr(c_in) - F[d], D.cube.binom[d], t0, pos) for d in range(D.n_o + 1)], 1 << D.n_o


if __name__ == "__main__":
    import resource
    # smoke: flat product instance, bottom
    u, n, n_o = Fr(1), 60, 40
    xs = [2 * u * (n - n_o), Fr(7), Fr(3), Fr(1), Fr(1, 2)]
    D = Design(n, n_o, u, Fr(1, 5), Fr(1, 20), 0.05, 0.05, 2 * math.e * n_o / 0.05, Fr(1, 2), 0.05, xs, lC=[None, 3.0, 6.0, 9.0, 12.0])
    pos = uniform_positions(D, "bottom")
    atoms, den = radial_atoms(D, [Fr(0)] * (n_o + 1), 0, pos=pos)
    R = mean_run(D, atoms, den, Fr(0))
    print("smoke: J", D.J, "K", D.K, "r_dag", D.r_dag, "m_max", D.m_max, "status", R.status, "j_stop", R.j_stop, "m_top", R.m_top,
          "lcost", mp.nstr(R.lcost, 12), "lCmax", mp.nstr(D.lCmax, 12), "calls", [mp.nstr(c, 6) for c in R.calls[1:]])
    print("peak RSS MB: %.1f" % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024))
