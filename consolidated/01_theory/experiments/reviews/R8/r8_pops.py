#!/usr/bin/env python3
"""Referee R8 -- instances and populations of outer points for the simulations (own code).

  * u-Lipschitz functions on an enumerated cube Q_n = Q_{n_o} x Q_{n_i} (non-radial families), with exact
    fibre averages;
  * radial outer landscapes (law of W exactly binomial), per point (moderate size) or as counts per shell
    and block (medium size, samples up to 2^61 points) with an own tail-safe multinomial sampler.
"""
import math
from fractions import Fraction as Fr
import numpy as np
from r8_core import Block, NEG_INF


# ----------------------------------------------------------------------------------------------
# functions on the enumerated cube
# ----------------------------------------------------------------------------------------------
def popcounts(n):
    x = np.arange(1 << n, dtype=np.int64)
    c = np.zeros(1 << n, dtype=np.int64)
    for i in range(n):
        c += (x >> i) & 1
    return c


def dist_to(n, c):
    x = np.arange(1 << n, dtype=np.int64) ^ int(c)
    d = np.zeros(1 << n, dtype=np.int64)
    for i in range(n):
        d += (x >> i) & 1
    return d


def lipschitz_const(psi, n):
    x = np.arange(1 << n, dtype=np.int64)
    best = 0.0
    for i in range(n):
        best = max(best, float(np.max(np.abs(psi - psi[x ^ (1 << i)]))))
    return best


def infconv(g, n, u):
    """x -> min_y g(y) + u d(x,y): the largest u-Lipschitz minorant (coordinate by coordinate)"""
    psi = g.copy()
    x = np.arange(1 << n, dtype=np.int64)
    for i in range(n):
        psi = np.minimum(psi, psi[x ^ (1 << i)] + u)
    return psi


KINDS = ['flat', 'cone', 'anticone', 'halfcone', 'dip', 'trunc', 'mcshane_min', 'mcshane_max', 'additive',
         'noise_reg', 'mixture', 'dips', 'outer_cone_inner_noise', 'bumpy_cone', 'cliff']


def gen_psi(kind, n, n_o, u, rng):
    """a u-Lipschitz function on Q_n (array of length 2^n; the outer coordinates are the high bits)"""
    N = 1 << n
    rc = lambda: int(rng.integers(0, N))
    if kind == 'flat':
        psi = np.zeros(N)
    elif kind == 'cone':
        psi = u * dist_to(n, rc()).astype(float)
    elif kind == 'anticone':
        psi = -u * dist_to(n, rc()).astype(float)
    elif kind == 'halfcone':
        psi = 0.5 * u * dist_to(n, rc()).astype(float)
    elif kind == 'dip':
        R = int(rng.integers(1, max(2, n // 2)))
        psi = -u * np.maximum(R + 1 - dist_to(n, rc()), 0).astype(float)
    elif kind == 'trunc':
        R = int(rng.integers(1, max(2, n // 2)))
        psi = u * np.maximum(dist_to(n, rc()), R).astype(float)
    elif kind == 'mcshane_min':
        k = int(rng.integers(2, 9))
        psi = np.full(N, np.inf)
        for _ in range(k):
            psi = np.minimum(psi, rng.uniform(0, u * n / 2) + u * dist_to(n, rc()))
    elif kind == 'mcshane_max':
        k = int(rng.integers(2, 9))
        psi = np.full(N, -np.inf)
        for _ in range(k):
            psi = np.maximum(psi, rng.uniform(0, u * n / 2) - u * dist_to(n, rc()))
    elif kind == 'additive':
        c = rng.uniform(-u, u, n)
        x = np.arange(N, dtype=np.int64)
        psi = np.zeros(N)
        for i in range(n):
            psi += c[i] * ((x >> i) & 1)
    elif kind == 'noise_reg':
        psi = infconv(rng.normal(0, rng.uniform(0.5, 3) * u, N), n, u)
    elif kind == 'mixture':
        k = int(rng.integers(2, 6))
        acc = np.zeros(N)
        for _ in range(k):
            sl = rng.uniform(0.2, 1.0) * u * rng.choice([-1, 1])
            acc += math.exp(rng.uniform(-3, 3)) * np.exp(-sl * dist_to(n, rc()))
        psi = -np.log(acc)
    elif kind == 'dips':
        k = int(rng.integers(2, 7))
        psi = np.zeros(N)
        for _ in range(k):
            R = int(rng.integers(0, max(1, n // 3)))
            psi = np.minimum(psi, -u * np.maximum(R + 1 - dist_to(n, rc()), 0))
    elif kind == 'outer_cone_inner_noise':
        n_i = n - n_o
        x = np.arange(N, dtype=np.int64)
        a = x >> n_i
        bidx = x & ((1 << n_i) - 1)
        ca = int(rng.integers(0, 1 << n_o))
        da = np.zeros(N, dtype=np.int64)
        for i in range(n_o):
            da += ((a ^ ca) >> i) & 1
        g = infconv(rng.normal(0, u, 1 << n_i), n_i, u)
        psi = rng.choice([-1, 1]) * u * da + g[bidx]
    elif kind == 'bumpy_cone':
        base = u * dist_to(n, rc()).astype(float) * rng.uniform(0.3, 1.0)
        psi = infconv(base + rng.normal(0, 0.7 * u, N), n, u)
    elif kind == 'cliff':
        # a deep well around one point of the outer cube, flat elsewhere, in the inner cube a moving centre
        n_i = n - n_o
        x = np.arange(N, dtype=np.int64)
        a = x >> n_i
        ca = int(rng.integers(0, 1 << n_o))
        da = np.zeros(N, dtype=np.int64)
        for i in range(n_o):
            da += ((a ^ ca) >> i) & 1
        R = int(rng.integers(1, max(2, n_o // 2)))
        psi = infconv(-u * np.maximum(R + 1 - da, 0).astype(float) * 1.0 + 0.3 * u * (popcounts(n) % 2), n, u)
    else:
        raise ValueError(kind)
    assert lipschitz_const(psi, n) <= u * (1 + 1e-9) + 1e-12, (kind, lipschitz_const(psi, n), u)
    return psi


class PopEnum:
    """outer points drawn uniformly from an enumerated outer cube; psi on Q_{n_o} x Q_{n_i}"""

    def __init__(self, psi, n, n_o, u, rng):
        self.n, self.n_o, self.n_i, self.u = n, n_o, n - n_o, u
        w = np.exp(-psi.reshape(1 << n_o, 1 << self.n_i))
        self.w = w                                           # fibre weights
        self.lW_outer = np.log(w.mean(axis=1))
        self.lA = math.log(w.mean())
        self.psi0 = float(psi[0])
        self.ls0 = -self.psi0 - u * n
        lpsi_a0 = -psi.reshape(1 << n_o, 1 << self.n_i)[:, 0]
        self.triv_lo = lpsi_a0 - u * self.n_i
        self.triv_hi = lpsi_a0 + u * self.n_i
        assert np.all(self.triv_lo <= self.lW_outer + 1e-12) and np.all(self.lW_outer <= self.triv_hi + 1e-12)
        self.sorted = np.sort(self.lW_outer)
        self.rng = rng
        self.size = 1 << n_o

    def new_block(self, size):
        b = Block()
        a = self.rng.integers(0, self.size, size)
        b.aidx = a
        b.cnt = np.ones(size, dtype=np.int64)
        b.lW = self.lW_outer[a]
        b.lL = self.triv_lo[a].copy()
        b.lU = self.triv_hi[a].copy()
        b.rung = np.zeros(size, dtype=np.int16)
        return b

    def p_exceed(self, lt):
        c = self.size - int(np.searchsorted(self.sorted, lt, side='right'))
        return Fr(c, self.size)

    def lp_exceed(self, lts):
        c = self.size - np.searchsorted(self.sorted, np.asarray(lts, dtype=float), side='right')
        with np.errstate(divide='ignore'):
            return np.log(c) - self.n_o * math.log(2)


# ----------------------------------------------------------------------------------------------
# radial outer landscapes:  psi(a,b) = f(d(a,c)) + g(b),  W(a) = e^{-f(d)} E_b e^{-g(b)}
# ----------------------------------------------------------------------------------------------
PROFILES = ['flat', 'cone', 'halfcone', 'anticone', 'dip', 'mesa', 'flatbottom', 'walk', 'periodic', 'staircase',
            'critical', 'dip_at_hint']


def gen_profile(kind, n_o, u, rng):
    d = np.arange(n_o + 1, dtype=float)
    pu = 1 / (1 + math.exp(u))
    if kind == 'flat':
        f = np.zeros(n_o + 1)
    elif kind == 'cone':
        f = u * d
    elif kind == 'halfcone':
        f = rng.uniform(0.2, 0.8) * u * d
    elif kind == 'anticone':
        f = -u * d
    elif kind == 'dip':
        R = int(rng.integers(0, max(1, int(0.45 * n_o))))
        f = -u * np.maximum(R + 1 - d, 0)
    elif kind == 'dip_at_hint':
        lam1 = math.log(2 / (1 + math.exp(-u)))
        R = max(0, int(round(lam1 / u * n_o + rng.integers(-3, 4))))
        f = -u * np.maximum(R + 1 - d, 0)
    elif kind == 'mesa':                       # truncated cone: flat near the centre, cone outside
        R = int(rng.integers(1, max(2, int(0.5 * n_o))))
        f = u * np.maximum(d, R)
    elif kind == 'flatbottom':                 # cone near the centre, flat outside
        R = int(rng.integers(1, max(2, int(0.5 * n_o))))
        f = u * np.minimum(d, R)
    elif kind == 'walk':
        f = np.concatenate(([0.0], np.cumsum(rng.uniform(-u, u, n_o))))
    elif kind == 'periodic':
        f = 0.5 * u * (-1.0) ** d
    elif kind == 'staircase':                  # W proportional to 1/|B(n_o,d)| as far as the slope allows
        lb = np.log(np.cumsum([float(math.comb(n_o, j)) for j in range(n_o + 1)]))
        st = np.clip(np.diff(lb), -u, u)
        f = np.concatenate(([0.0], np.cumsum(st)))
    elif kind == 'critical':                   # slope ln((n_o-d)/(d+1)) clipped: makes s p(s) flat
        st = np.clip(np.log((n_o - d[:-1]) / (d[:-1] + 1)), -u, u) * rng.choice([1.0, 0.5])
        f = np.concatenate(([0.0], np.cumsum(st)))
    else:
        raise ValueError(kind)
    assert np.max(np.abs(np.diff(f))) <= u * (1 + 1e-9) + 1e-12
    return f


class RadialBase:
    def __init__(self, f, n_o, n_i, u, rng, inner='zero', d0=None):
        self.n_o, self.n_i, self.n, self.u = n_o, n_i, n_o + n_i, u
        self.rng = rng
        self.f = np.asarray(f, dtype=float)
        # inner function g: 'zero', 'cone' (g = u|b|), 'anticone' (g = -u|b|); g(0) = 0
        if inner == 'zero':
            lEg = 0.0
        elif inner == 'cone':
            lEg = n_i * math.log((1 + math.exp(-u)) / 2)
        else:
            lEg = n_i * math.log((1 + math.exp(u)) / 2)
        self.lW_shell = -self.f + lEg
        if d0 is None:
            d0 = int(rng.integers(0, n_o + 1))
        self.d0 = d0                                   # distance of the reference point from the centre
        self.psi0 = float(self.f[d0])
        self.ls0 = -self.psi0 - u * self.n
        self.triv_lo = -self.f - u * n_i               # e^{-psi(a,0) - u n_i},  psi(a,0) = f(d)
        self.triv_hi = -self.f + u * n_i
        self.C = [math.comb(n_o, j) for j in range(n_o + 1)]
        lC = np.array([math.log(c) for c in self.C])
        m = float(np.max(lC + self.lW_shell))
        self.lA = m + math.log(float(np.sum(np.exp(lC + self.lW_shell - m)))) - n_o * math.log(2)
        order = np.argsort(self.lW_shell, kind='stable')
        self.sorted = self.lW_shell[order]
        cum = [0]
        for i in order:
            cum.append(cum[-1] + self.C[int(i)])
        self.cum = cum                                 # exact ints: number of outer points with lW <= sorted[k-1]
        self.lcum_top = None
        self.two = 1 << n_o

    def p_exceed(self, lt):
        k = int(np.searchsorted(self.sorted, lt, side='right'))
        return Fr(self.two - self.cum[k], self.two)

    def lp_exceed(self, lts):
        ks = np.searchsorted(self.sorted, np.asarray(lts, dtype=float), side='right')
        if self.lcum_top is None:
            self.lcum_top = np.array([math.log(self.two - c) if self.two - c > 0 else NEG_INF for c in self.cum])
        return self.lcum_top[ks] - self.n_o * math.log(2)


class PopRadialPoints(RadialBase):
    """every outer point is a group of its own"""

    def new_block(self, size):
        b = Block()
        d = self.rng.binomial(self.n_o, 0.5, size)
        b.aidx = d
        b.cnt = np.ones(size, dtype=np.int64)
        b.lW = self.lW_shell[d]
        b.lL = self.triv_lo[d].copy()
        b.lU = self.triv_hi[d].copy()
        b.rung = np.zeros(size, dtype=np.int16)
        return b


# ----------------------------------------------------------------------------------------------
# tail-safe binomial / multinomial for sample sizes up to 2^62
# ----------------------------------------------------------------------------------------------
def binom_safe(rng, N, p):
    """Bin(N, p), N a python int < 2^63, 0 <= p <= 1/2.  Inversion with log1p for small means, numpy's
    sampler for p >= 1e-7, and a Poisson variable for p < 1e-7 with a large mean (total variation <= p)."""
    if N <= 0 or p <= 0.0:
        return 0
    mean = N * p
    if mean < 40.0:
        uu = rng.random()
        pk = math.exp(N * math.log1p(-p))
        cdf = pk
        k = 0
        ratio = p / (1.0 - p)
        while uu > cdf and k < N:
            pk *= (N - k) / (k + 1.0) * ratio
            k += 1
            cdf += pk
            if pk < 1e-300:
                break
        return k
    if p >= 1e-7:
        return int(rng.binomial(N, p))
    return min(N, int(rng.poisson(mean)))


def multinomial_shells(rng, N, ball, lo, hi, out):
    """counts of N points over the shells lo..hi of Q_m with probabilities C(m,d)/2^m, by binary splitting
    with exact conditional probabilities (ball[r+1] = |B(m,r)| exact ints)."""
    stack = [(lo, hi, N)]
    while stack:
        lo, hi, N = stack.pop()
        if N == 0:
            continue
        if lo == hi:
            out[lo] = N
            continue
        mid = (lo + hi) // 2
        pl = ball[mid + 1] - ball[lo]
        pt = ball[hi + 1] - ball[lo]
        if 2 * pl <= pt:
            nl = binom_safe(rng, N, float(Fr(pl, pt)))
        else:
            nl = N - binom_safe(rng, N, float(Fr(pt - pl, pt)))
        stack.append((lo, mid, nl))
        stack.append((mid + 1, hi, N - nl))


class PopRadialGroups(RadialBase):
    """the points of one block that lie in one shell form a group (same bracket for all of them)"""

    def __init__(self, f, n_o, n_i, u, rng, inner='zero', d0=None):
        super().__init__(f, n_o, n_i, u, rng, inner, d0)
        s = 0
        self.ball = [0]
        for c in self.C:
            s += c
            self.ball.append(s)

    def new_block(self, size):
        out = {}
        multinomial_shells(self.rng, int(size), self.ball, 0, self.n_o, out)
        ds = np.array(sorted(out.keys()), dtype=np.int64)
        b = Block()
        b.aidx = ds
        b.cnt = np.array([out[int(d)] for d in ds], dtype=np.int64)
        b.lW = self.lW_shell[ds]
        b.lL = self.triv_lo[ds].copy()
        b.lU = self.triv_hi[ds].copy()
        b.rung = np.zeros(ds.shape[0], dtype=np.int16)
        return b
