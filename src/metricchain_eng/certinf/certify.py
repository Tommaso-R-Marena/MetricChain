"""Statistical side: certified bounds from samples (Theorem 5.1), S3 as proposed (Theorems 2.2, 3.1), abstention.

A *sample* holds, for independent draws x_1..x_n of a sampling law pi: the target f, the measured observables phi,
and the two density ratios L = l/(c pi), U = u/(c pi) of the envelope against pi (c > 0 any common constant).
Reference sampling of an energy envelope: pi = reference Gibbs law, L = exp(-rho), U = exp(rho).

Everything a certificate needs *beyond* the sample is in ``Declared``: bounds on the ranges and on U.  They are
assumptions about the whole configuration space; a sample cannot verify them, and a certificate is void if a
drawn point violates them.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy.special import logsumexp

from .core import Box, Ellipsoid, Problem, Sum, find_inconsistency, solve_upper, _vec

__all__ = ["Sample", "Declared", "Bound", "certify_upper", "certify_lower", "certified_interval",
           "certify_inconsistent", "certify_upper_gap", "s3_eps_net", "s3_eps_rademacher", "s3_interval",
           "log_wealth", "hoeffding_ucb", "bernstein_ucb"]

BETS = 0.9 * 2.0 ** -np.arange(16)          # fractions of the largest admissible bet 1/B; fixed in advance


@dataclass
class Sample:
    f: np.ndarray
    phi: np.ndarray
    L: np.ndarray
    U: np.ndarray

    def __post_init__(self):
        self.f = _vec(self.f)
        n = self.f.size
        self.phi = np.asarray(self.phi, dtype=float).reshape(n, -1)
        self.L = np.broadcast_to(np.asarray(self.L, dtype=float), (n,)).astype(float).copy()
        self.U = np.broadcast_to(np.asarray(self.U, dtype=float), (n,)).astype(float).copy()

    @property
    def n(self) -> int:
        return self.f.size

    def part(self, idx) -> "Sample":
        return Sample(self.f[idx], self.phi[idx], self.L[idx], self.U[idx])

    def negated(self) -> "Sample":
        return Sample(-self.f, self.phi, self.L, self.U)


@dataclass
class Declared:
    f_lo: float
    f_hi: float
    phi_lo: np.ndarray
    phi_hi: np.ndarray
    U_max: float                 # sup of U over the configuration space
    iid: bool = True             # the draws are independent draws of the sampling law
    beta: float = 1.0            # ... or of a law whose density against it lies in [1/beta, beta]   (section 7.3)
    eps_tv: float = 0.0          # ... or within total-variation distance eps_tv of it
    phi_err: float = 0.0         # evaluation error of the measured observables                          (section 7.4)
    f_err: float = 0.0           # evaluation error of the target

    def __post_init__(self):
        self.phi_lo, self.phi_hi = _vec(self.phi_lo), _vec(self.phi_hi)

    def negated(self) -> "Declared":
        return Declared(-self.f_hi, -self.f_lo, self.phi_lo, self.phi_hi, self.U_max, self.iid, self.beta, self.eps_tv,
                        self.phi_err, self.f_err)

    def violated_by(self, s: Sample) -> str:
        tol = 1e-12
        if np.any(s.f < self.f_lo - tol) or np.any(s.f > self.f_hi + tol):
            return "a drawn target value is outside the declared range"
        if s.phi.shape[1] and (np.any(s.phi < self.phi_lo - tol) or np.any(s.phi > self.phi_hi + tol)):
            return "a drawn observable is outside the declared range"
        if np.any(s.U > self.U_max * (1 + tol)) or np.any(s.L > s.U * (1 + tol)) or np.any(s.L < 0):
            return "a drawn density ratio violates 0 <= L <= U <= U_max"
        return ""


@dataclass
class Bound:
    value: float                 # the bound (the trivial end of the declared range when status is not 'certified')
    status: str                  # 'certified' | 'trivial' (nothing better than the range) | 'abstain' | 'void'
    note: str = ""
    eta: np.ndarray = field(default_factory=lambda: np.zeros(0))
    tau_train: float = math.nan
    n_valid: int = 0


# ---------------------------------------------------------------------------------------------
# One-function tests
# ---------------------------------------------------------------------------------------------
def log_wealth(z: np.ndarray, big: float) -> float:
    """ln of W = mean_k prod_j (1 - lam_k z_j), lam_k = BETS[k] / big, for z_j <= big.  If E z >= 0 then E W <= 1,
    so W >= 1/delta has probability at most delta (Markov): a one-sided test of 'E z < 0' whose power adapts to the
    variance of z.  Only an upper bound of z is used."""
    if big <= 0:
        return math.inf if np.all(z <= 0) and np.any(z < 0) else 0.0
    lam = BETS / big
    return float(logsumexp(np.log1p(-np.outer(lam, z)).sum(axis=1)) - math.log(len(lam)))


def hoeffding_ucb(z: np.ndarray, lo: float, hi: float, delta: float) -> float:
    return float(np.mean(z) + (hi - lo) * math.sqrt(math.log(1 / delta) / (2 * len(z))))


def bernstein_ucb(z: np.ndarray, lo: float, hi: float, delta: float) -> float:
    """Maurer and Pontil (2009), Theorem 4, for values in [lo, hi]."""
    n = len(z)
    return float(np.mean(z) + math.sqrt(2 * np.var(z, ddof=1) * math.log(2 / delta) / n) + 7 * (hi - lo) * math.log(2 / delta) / (3 * (n - 1)))


def _smallest_tau(zfun, big: float, lo: float, hi: float, target: float):
    """Smallest tau in [lo, hi] with log_wealth(zfun(tau)) >= target (the wealth is non-decreasing in tau), or None."""
    if log_wealth(zfun(hi), big) < target:
        return None
    if log_wealth(zfun(lo), big) >= target:
        return lo
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if log_wealth(zfun(mid), big) >= target:
            hi = mid
        else:
            lo = mid
    return hi


def _spread(eta, d: Declared, h: float) -> tuple[float, float]:
    """(inf, sup) over the declared ranges of -eta . phi + h_R(eta)."""
    a, b = eta * d.phi_lo, eta * d.phi_hi
    return h - float(np.maximum(a, b).sum()), h - float(np.minimum(a, b).sum())


def _region(region, d: Declared):
    return region.enlarged(d.phi_err) if d.phi_err > 0 else region


# ---------------------------------------------------------------------------------------------
# Certified ends of the identified interval (reference sampling)
# ---------------------------------------------------------------------------------------------
def certify_upper(train: Sample, valid: Sample, region, d: Declared, delta: float, rigorous: bool = False) -> Bound:
    """An upper bound for E_p f over every ensemble p of the class with measured averages in the region, valid
    with probability at least 1 - delta over the validation draws (Theorem 5.1).  The training draws only choose
    the multipliers eta."""
    if not d.iid:
        return Bound(d.f_hi, "abstain", "the draws are not declared independent: Theorem 5.1 does not apply")
    if not math.isfinite(d.U_max):
        return Bound(d.f_hi, "abstain", "no finite bound on u/pi: no sample certifies anything about unsampled configurations (Theorem 6.1)")
    for s in (train, valid):
        msg = d.violated_by(s)
        if msg:
            return Bound(d.f_hi, "void", msg)
    reg = _region(region, d)
    n = train.n
    lt, ut = train.L / d.beta, train.U * d.beta
    tau_tr, eta = solve_upper(Problem(train.f, train.phi, Lw=lt, Gw=ut - lt, region=reg, wt=np.full(n, 1.0 / n)))
    eta = _vec(eta)
    h = reg.h(eta)
    s_lo, s_hi = _spread(eta, d, h)
    umax = d.U_max * d.beta
    shift = d.eps_tv * umax * ((d.f_hi + s_hi - d.f_lo) + max(d.f_hi - d.f_lo - s_lo, 0.0))
    big = umax * max(d.f_hi + s_hi - d.f_lo, 0.0) + shift
    s0 = valid.f - valid.phi @ eta + h
    lv, uv = valid.L / d.beta, valid.U * d.beta

    def zfun(tau):
        s = s0 - tau
        return uv * np.maximum(s, 0.0) - lv * np.maximum(-s, 0.0) + shift

    target = math.log(1.0 / delta)
    tau = _smallest_tau(zfun, big, d.f_lo, d.f_hi, target)
    if tau is None:
        return Bound(d.f_hi + d.f_err, "trivial", "the validation sample certifies nothing below the declared range", eta, tau_tr, valid.n)
    if rigorous:
        tau = _raise_until_rigorous(valid, lv, uv, eta, reg, shift, big, tau, d.f_hi, target)
        if tau is None:
            return Bound(d.f_hi + d.f_err, "trivial", "not confirmed in interval arithmetic", eta, tau_tr, valid.n)
    return Bound(tau + d.f_err, "certified", "", eta, tau_tr, valid.n)


def certify_lower(train: Sample, valid: Sample, region, d: Declared, delta: float, rigorous: bool = False) -> Bound:
    b = certify_upper(train.negated(), valid.negated(), region, d.negated(), delta, rigorous)
    return Bound(-b.value, b.status, b.note, b.eta, -b.tau_train, b.n_valid)


def certified_interval(sample: Sample, region, d: Declared, delta: float, split: float = 0.5, rigorous: bool = False) -> dict:
    """Both ends, each at level delta/2, from one sample split into a training and a validation part.  If the two
    certified ends cross, no ensemble of the class is compatible with the data (remark (iv) to Theorem 4.1)."""
    k = int(round(split * sample.n))
    train, valid = sample.part(slice(0, k)), sample.part(slice(k, None))
    hi = certify_upper(train, valid, region, d, delta / 2, rigorous)
    lo = certify_lower(train, valid, region, d, delta / 2, rigorous)
    status = "abstain" if "abstain" in (hi.status, lo.status) else "void" if "void" in (hi.status, lo.status) else \
        "inconsistent" if (hi.status == lo.status == "certified" and lo.value > hi.value) else \
        "certified" if "certified" in (hi.status, lo.status) else "trivial"
    return dict(lo=lo.value, hi=hi.value, status=status, lower=lo, upper=hi, n_train=train.n, n_valid=valid.n)


def certify_inconsistent(train: Sample, valid: Sample, region, d: Declared, delta: float) -> Bound:
    """Certificate that NO ensemble of the class has its measured averages in the region (Theorem 4.1(e), tested as
    in Theorem 5.1).  status 'certified' means inconsistency is certified with probability >= 1 - delta."""
    if not d.iid or not math.isfinite(d.U_max):
        return Bound(math.nan, "abstain", "needs independent draws and a finite bound on u/pi")
    for s in (train, valid):
        msg = d.violated_by(s)
        if msg:
            return Bound(math.nan, "void", msg)
    reg = _region(region, d)
    n = train.n
    lt, ut = train.L / d.beta, train.U * d.beta
    val, eta = find_inconsistency(Problem(train.f, train.phi, Lw=lt, Gw=ut - lt, region=reg, wt=np.full(n, 1.0 / n)))
    if not val > 0:
        return Bound(val, "trivial", "the training sample shows no inconsistency", eta, math.nan, valid.n)
    h = reg.h(eta)
    t = valid.phi @ eta - h
    umax = d.U_max * d.beta
    t_lo = float(np.minimum(eta * d.phi_lo, eta * d.phi_hi).sum()) - h          # inf of t over the declared ranges
    t_hi = float(np.maximum(eta * d.phi_lo, eta * d.phi_hi).sum()) - h
    shift = d.eps_tv * umax * (max(-t_lo, 0.0) + max(t_hi, 0.0))
    z = (valid.U * d.beta) * np.maximum(-t, 0.0) - (valid.L / d.beta) * np.maximum(t, 0.0) + shift   # want E z < 0
    lw = log_wealth(z, umax * max(-t_lo, 0.0) + shift)
    ok = lw >= math.log(1.0 / delta)
    return Bound(val, "certified" if ok else "trivial", "" if ok else "the validation sample does not confirm it", eta, math.nan, valid.n)


# ---------------------------------------------------------------------------------------------
# Gap sampling with exact b, G (S3's access model), certified by one function
# ---------------------------------------------------------------------------------------------
def certify_upper_gap(b, G: float, f_tr, phi_tr, f_va, phi_va, region, d: Declared, delta: float) -> Bound:
    """Draws from q = (u - l)/G, with b = sum l v and G exact: Psi = lin + G E_q[s_+].  ``d.U_max`` is not used."""
    b = _vec(b)
    f_tr, f_va = _vec(f_tr), _vec(f_va)
    phi_tr, phi_va = np.asarray(phi_tr, float).reshape(f_tr.size, -1), np.asarray(phi_va, float).reshape(f_va.size, -1)
    P = Problem(f_tr, phi_tr, Lw=0.0, Gw=G, region=region, wt=np.full(f_tr.size, 1.0 / f_tr.size), b=b)
    tau_tr, eta = solve_upper(P)
    eta = _vec(eta)
    h = region.h(eta)
    _, s_hi = _spread(eta, d, h)
    b0, const = b[0], b[-1] - float(eta @ b[1:-1]) + h * b[0]
    s0 = f_va - phi_va @ eta + h

    def zfun(tau):                       # E_q z <= 0  <=>  Psi(tau, eta) <= 0
        return np.maximum(s0 - tau, 0.0) + (const - b0 * tau) / G

    big = max(d.f_hi + s_hi - d.f_lo, 0.0) + (const - b0 * d.f_lo) / G
    tau = _smallest_tau(zfun, big, d.f_lo, d.f_hi, math.log(1.0 / delta))
    if tau is None:
        return Bound(d.f_hi, "trivial", "the validation sample certifies nothing below the declared range", eta, tau_tr, f_va.size)
    return Bound(tau, "certified", "", eta, tau_tr, f_va.size)


# ---------------------------------------------------------------------------------------------
# S3 as proposed: compress the moment body, enlarge the region and the interval by kappa
# ---------------------------------------------------------------------------------------------
def s3_eps_net(n: int, dim: int, delta: float) -> float:
    """The epsilon for which n = (2/eps^2)[dim ln(1 + 8/eps) + ln(2/delta)] (Theorem 2.2)."""
    lo, hi = 1e-12, 1e6
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if (2 / mid ** 2) * (dim * math.log1p(8 / mid) + math.log(2 / delta)) > n:
            lo = mid
        else:
            hi = mid
    return hi


def s3_eps_rademacher(n: int, dim: int, delta: float) -> float:
    """Theorem 3.1."""
    return 2 * math.sqrt(2 * math.log(2 * dim) / n) + math.sqrt(math.log(2 / delta) / (2 * n))


def s3_interval(b, G: float, f_q, phi_q, region, delta: float, bound: str = "net") -> dict:
    """S3 with its own allowance: draws from q, exact b and G, observables in [-1, 1] (assumption H1)."""
    b, f_q = _vec(b), _vec(f_q)
    phi_q = np.asarray(phi_q, dtype=float).reshape(f_q.size, -1)
    if np.any(np.abs(f_q) > 1 + 1e-12) or np.any(np.abs(phi_q) > 1 + 1e-12):
        raise ValueError("S3 assumes observables scaled to [-1, 1] (H1)")
    n, dim = f_q.size, phi_q.shape[1] + 2
    eps = s3_eps_net(n, dim, delta) if bound == "net" else s3_eps_rademacher(n, dim, delta)
    kappa = 2 * eps * G / b[0] if b[0] > 0 else math.inf
    if not math.isfinite(kappa):
        return dict(lo=-1.0, hi=1.0, kappa=kappa, eps=eps, status="abstain")
    P = Problem(f_q, phi_q, Lw=0.0, Gw=G, region=region.enlarged(kappa), wt=np.full(n, 1.0 / n), b=b)
    hi, _ = solve_upper(P)
    lo = -solve_upper(P.negated())[0]
    if hi < lo:
        return dict(lo=lo, hi=hi, kappa=kappa, eps=eps, status="inconsistent")
    return dict(lo=max(lo - kappa, -1.0), hi=min(hi + kappa, 1.0), kappa=kappa, eps=eps, status="certified")


# ---------------------------------------------------------------------------------------------
# Interval-arithmetic confirmation of a wealth certificate (section 7.1: rounding)
# ---------------------------------------------------------------------------------------------
def _h_iv(region, eta, iv):
    if isinstance(region, Box):
        return sum((iv.mpf(float(e)) * iv.mpf(float(c)) + abs(iv.mpf(float(e))) * iv.mpf(float(w)) for e, c, w in zip(eta, region.c, region.e)), iv.mpf(0))
    if isinstance(region, Ellipsoid):
        q = sum((iv.mpf(float(eta[i])) * iv.mpf(float(region.cov[i, j])) * iv.mpf(float(eta[j])) for i in range(len(eta)) for j in range(len(eta))), iv.mpf(0))
        q = iv.mpf([max(q.a, 0), max(q.b, 0)])
        return sum((iv.mpf(float(e)) * iv.mpf(float(c)) for e, c in zip(eta, region.c)), iv.mpf(0)) + iv.mpf(region.radius) * iv.sqrt(q)
    if isinstance(region, Sum):
        return _h_iv(region.a, eta, iv) + _h_iv(region.b, eta, iv)
    raise TypeError("region without an interval-arithmetic support function")


def wealth_lower_bound_iv(valid: Sample, lv, uv, eta, region, shift: float, big: float, tau: float) -> float:
    """A rigorous lower bound of ln W at tau (the same mixture of bets as ``log_wealth``): every operation in
    interval arithmetic on the stored floats."""
    from mpmath import iv
    iv.dps = 30
    h = _h_iv(region, eta, iv)
    z_hi = []
    for j in range(valid.n):
        s = iv.mpf(float(valid.f[j])) - iv.mpf(float(tau)) + h
        for e, p in zip(eta, valid.phi[j]):
            s -= iv.mpf(float(e)) * iv.mpf(float(p))
        z = iv.mpf(float(uv[j])) * max(s.b, 0) - iv.mpf(float(lv[j])) * max(-s.b, 0) + iv.mpf(float(shift))
        z_hi.append(z.b)                                   # z is increasing in s: its value at the upper end of s
    lows = []
    for frac in BETS:
        lam = iv.mpf(float(frac)) / iv.mpf(float(big))
        tot = iv.mpf(0)
        for z in z_hi:
            tot += iv.log(1 - lam * z)
        lows.append(tot.a)
    top = max(lows)
    acc = iv.mpf(0)
    for t in lows:
        acc += iv.exp(iv.mpf(t) - iv.mpf(top))
    res = iv.mpf(top) + iv.log(acc) - iv.log(iv.mpf(len(BETS)))
    return math.nextafter(float(res.a), -math.inf)


def _raise_until_rigorous(valid, lv, uv, eta, region, shift, big, tau, tau_max, target):
    step = 1e-12 * max(1.0, abs(tau))
    for _ in range(40):
        if wealth_lower_bound_iv(valid, lv, uv, eta, region, shift, big, tau) >= target:
            return tau
        tau, step = tau + step, step * 4
        if tau > tau_max:
            return None
    return None
