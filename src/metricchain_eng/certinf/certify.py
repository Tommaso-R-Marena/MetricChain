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
from scipy.optimize import minimize
from scipy.special import logsumexp

from .core import Box, Ellipsoid, Problem, Sum, find_inconsistency, solve_upper, _vec

__all__ = ["Sample", "Declared", "Bound", "certify_upper", "certify_lower", "certified_interval",
           "certify_inconsistent", "certify_upper_gap", "s3_eps_net", "s3_eps_rademacher", "s3_interval",
           "log_wealth", "hoeffding_ucb", "bernstein_ucb", "range_excludes_region", "train_multipliers",
           "tilt_indicator", "tilted_score", "tilted_root", "certify_upper_tilted", "certify_lower_tilted"]

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

    def invalid(self) -> str:
        """A message if the declaration itself cannot be used, else ''."""
        nums = (self.f_lo, self.f_hi, self.beta, self.eps_tv, self.phi_err, self.f_err)
        if not all(math.isfinite(v) for v in nums) or not np.all(np.isfinite(self.phi_lo)) or not np.all(np.isfinite(self.phi_hi)):
            return "a declared number is not finite"
        if self.f_lo > self.f_hi or self.phi_lo.shape != self.phi_hi.shape or np.any(self.phi_lo > self.phi_hi):
            return "a declared range is empty"
        if self.beta < 1 or not 0 <= self.eps_tv < 1 or self.phi_err < 0 or self.f_err < 0 or not self.U_max >= 0:
            return "the declaration needs beta >= 1, 0 <= eps_tv < 1, non-negative errors and U_max >= 0"
        return ""

    def violated_by(self, s: Sample) -> str:
        """A message if a draw contradicts the declaration or is not a finite number (REVIEW_A, K1), else ''."""
        tol = 1e-12
        msg = _range_violation(s.f, s.phi, self)
        if msg:
            return msg
        if not (np.all(np.isfinite(s.L)) and np.all(np.isfinite(s.U))):
            return "a drawn density ratio is not finite"
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
    if not (lo <= hi and log_wealth(zfun(hi), big) >= target):       # also when the wealth is not a number (K1)
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


def _bad_delta(delta: float) -> str:
    return "" if 0.0 < delta < 1.0 else "the level delta must lie strictly between 0 and 1"


def _range_violation(f, phi, d: Declared) -> str:
    """A message if drawn values of the target or the observables are not finite or leave the declared ranges."""
    tol = 1e-12
    if not (np.all(np.isfinite(f)) and np.all(np.isfinite(phi))):
        return "a drawn value is not a finite number"
    if phi.shape[1] != d.phi_lo.size:
        return "the declared ranges do not match the number of observables"
    if np.any(f < d.f_lo - tol) or np.any(f > d.f_hi + tol):
        return "a drawn target value is outside the declared range"
    if phi.shape[1] and (np.any(phi < d.phi_lo - tol) or np.any(phi > d.phi_hi + tol)):
        return "a drawn observable is outside the declared range"
    return ""


def _train(train: Sample, reg, d: Declared) -> tuple[float, np.ndarray]:
    """Multipliers from the training draws.  Any choice is sound; a failed optimisation falls back to eta = 0."""
    m, n = train.phi.shape[1], train.n
    if n == 0:
        return math.nan, np.zeros(m)
    lt, ut = train.L / d.beta, train.U * d.beta
    tau, eta = solve_upper(Problem(train.f, train.phi, Lw=lt, Gw=ut - lt, region=reg, wt=np.full(n, 1.0 / n)))
    eta = _vec(eta)
    return (float(tau), eta) if np.all(np.isfinite(eta)) else (math.nan, np.zeros(m))


# ---------------------------------------------------------------------------------------------
# Certified ends of the identified interval (reference sampling)
# ---------------------------------------------------------------------------------------------
def certify_upper(train: Sample, valid: Sample, region, d: Declared, delta: float, rigorous: bool = False) -> Bound:
    """An upper bound for E_p f over every ensemble p of the class with measured averages in the region, valid
    with probability at least 1 - delta over the validation draws (Theorem 5.1).  The training draws only choose
    the multipliers eta."""
    msg = d.invalid() or _bad_delta(delta)
    if msg:
        return Bound(d.f_hi, "void", msg)
    if not d.iid:
        return Bound(d.f_hi, "abstain", "the draws are not declared independent: Theorem 5.1 does not apply")
    if not math.isfinite(d.U_max):
        return Bound(d.f_hi, "abstain", "no finite bound on u/pi: reference draws certify nothing about unsampled configurations (section 6, (iv))")
    for s in (train, valid):
        msg = d.violated_by(s)
        if msg:
            return Bound(d.f_hi, "void", msg)
    reg = _region(region, d)
    tau_tr, eta = _train(train, reg, d)
    h = reg.h(eta)
    s_lo, s_hi = _spread(eta, d, h)
    umax = d.U_max * d.beta
    shift = d.eps_tv * umax * (max(d.f_hi + s_hi - d.f_lo, 0.0) + max(d.f_hi - d.f_lo - s_lo, 0.0))   # one constant for the whole bracket (7.3)
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
    in Theorem 5.1).  status 'certified' means inconsistency is certified with probability >= 1 - delta - or with
    certainty, and for every class, when the declared range of the observables alone excludes the region (the note
    says so).  For a class with l = 0 a sample can certify nothing of the kind, because an unsampled configuration
    can have any value of phi: 'abstain' (REVIEW_A, findings C2 and K3)."""
    msg = d.invalid() or _bad_delta(delta)
    if msg:
        return Bound(math.nan, "void", msg)
    for s in (train, valid):
        msg = d.violated_by(s)
        if msg:
            return Bound(math.nan, "void", msg)
    sep = range_excludes_region(region, d)
    if sep is not None:
        return Bound(math.inf, "certified", "deterministic: the region is disjoint from the declared range of the observables", sep, math.nan, 0)
    if not d.iid or not math.isfinite(d.U_max):
        return Bound(math.nan, "abstain", "needs independent draws and a finite bound on u/pi")
    if not np.any(valid.L > 0):
        return Bound(math.nan, "abstain", "l = 0 at every validation draw: for a class with l = 0 inconsistency concerns every "
                                          "configuration and cannot be certified from a sample (Theorem 4.1(e))")
    if train.n == 0:
        return Bound(math.nan, "trivial", "no training draw")
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
    """Draws from q = (u - l)/G, with b = sum l v and G exact: Psi = lin + G E_q[s_+].  ``d.U_max`` is not used.
    The declaration is honoured as in ``certify_upper`` (sections 7.3-7.5; REVIEW_A, findings C1 and K2): abstention
    for dependent draws, a void certificate for a draw outside the declared ranges, the allowances beta, eps_tv,
    phi_err and f_err; and for G = 0, where q does not exist, the exact value from b."""
    b = _vec(b)
    f_tr, f_va = _vec(f_tr), _vec(f_va)
    phi_tr, phi_va = np.asarray(phi_tr, float).reshape(f_tr.size, -1), np.asarray(phi_va, float).reshape(f_va.size, -1)
    m = phi_va.shape[1]
    msg = d.invalid() or _bad_delta(delta)
    if not msg and (b.size != m + 2 or not np.all(np.isfinite(b)) or not (math.isfinite(G) and G >= 0) or not b[0] >= 0):
        msg = "b = (Z_l, sum l phi, sum l f) and G must be finite, with Z_l >= 0 and G >= 0"
    if msg:
        return Bound(d.f_hi, "void", msg)
    if G == 0:
        if not b[0] > 0:
            return Bound(d.f_hi, "abstain", "G = 0 and Z_l = 0: the class contains no ensemble")
        val = float(b[-1] / b[0])
        return Bound(val + d.f_err, "certified", "G = 0: the class is the one ensemble l/Z_l and its average is exact from b; no draw is used, "
                                                 "and consistency with the region is not examined", np.zeros(m), val, 0)
    if not d.iid:
        return Bound(d.f_hi, "abstain", "the draws are not declared independent: Theorem 5.1 does not apply")
    msg = _range_violation(f_tr, phi_tr, d) or _range_violation(f_va, phi_va, d)
    if msg:
        return Bound(d.f_hi, "void", msg)
    reg = _region(region, d)
    tau_tr, eta = math.nan, np.zeros(m)
    if f_tr.size:
        tau_tr, eta = solve_upper(Problem(f_tr, phi_tr, Lw=0.0, Gw=G, region=reg, wt=np.full(f_tr.size, 1.0 / f_tr.size), b=b))
        eta = _vec(eta)
        if not np.all(np.isfinite(eta)):
            tau_tr, eta = math.nan, np.zeros(m)
    h = reg.h(eta)
    _, s_hi = _spread(eta, d, h)
    b0, const = b[0], b[-1] - float(eta @ b[1:-1]) + h * b[0]
    top = max(d.f_hi + s_hi - d.f_lo, 0.0)                    # sup of s_+ over the declared ranges and the bracket
    shift = d.eps_tv * d.beta * top
    s0 = f_va - phi_va @ eta + h

    def zfun(tau):                       # E_q z <= 0  =>  Psi(tau, eta) <= 0
        return d.beta * np.maximum(s0 - tau, 0.0) + shift + (const - b0 * tau) / G

    big = d.beta * top + shift + (const - b0 * d.f_lo) / G
    tau = _smallest_tau(zfun, big, d.f_lo, d.f_hi, math.log(1.0 / delta))
    if tau is None:
        return Bound(d.f_hi + d.f_err, "trivial", "the validation sample certifies nothing below the declared range", eta, tau_tr, f_va.size)
    return Bound(tau + d.f_err, "certified", "", eta, tau_tr, f_va.size)


# ---------------------------------------------------------------------------------------------
# Draws from the extremal ensemble of the class (Theorem 5.4): the envelope ratio does not enter
# ---------------------------------------------------------------------------------------------
def range_excludes_region(region, d: Declared):
    """A unit direction eta with  h_R(eta) < min{eta . y : y in the declared range of phi}, or None if none is found.
    When one exists the region (enlarged by the declared evaluation error) is disjoint from the declared range, so no
    probability whatever on configurations obeying the declaration has its measured averages in the region:
    inconsistency with certainty, for every class, the one with l = 0 included."""
    m = d.phi_lo.size
    if m == 0:
        return None
    reg = _region(region, d)

    def gap(e):                                                # negative  <=>  separated along e
        nrm = float(np.linalg.norm(e))
        if nrm == 0:
            return 0.0
        e = np.asarray(e, dtype=float) / nrm
        return reg.h(e) - float(np.minimum(e * d.phi_lo, e * d.phi_hi).sum())

    best = min((v for i in range(m) for v in (np.eye(m)[i], -np.eye(m)[i])), key=gap)
    if gap(best) >= 0:
        best = minimize(gap, best, method="Nelder-Mead", options=dict(xatol=1e-9, fatol=1e-13, maxiter=2000 * m)).x
    return best / np.linalg.norm(best) if gap(best) < -1e-12 else None


def train_multipliers(train: Sample, region, d: Declared) -> tuple[float, np.ndarray, float]:
    """(tau, eta, se) from draws of the sampling law: the multipliers and the root of the empirical dual, as in
    ``certify_upper``, and a plug-in standard error of that root (delta method).  For choosing a pilot of
    Theorem 5.4; nothing here is certified."""
    reg = _region(region, d)
    tau, eta = _train(train, reg, d)
    if not math.isfinite(tau) or train.n < 2:
        return tau, eta, math.inf
    s = train.f - train.phi @ eta + reg.h(eta) - tau
    om = np.where(s > 0, train.U * d.beta, train.L / d.beta)
    slope = float(om.mean())
    return tau, eta, float((om * s).std(ddof=1) / (math.sqrt(train.n) * slope)) if slope > 0 else math.inf


def tilt_indicator(f, phi, region, eta, tau0: float, d: Declared | None = None) -> np.ndarray:
    """Where the extremal ensemble of Theorem 5.4 carries the upper weight: {s_{tau0,eta} > 0}.  Its unnormalised
    weight is u there and l elsewhere - with energies, a Boltzmann weight of E_min there and E_max elsewhere.
    Pass the declaration if it has an evaluation error of phi (the region is enlarged by it, as in the certificate)."""
    f, eta = _vec(f), _vec(eta)
    reg = region if d is None else _region(region, d)
    return f - np.asarray(phi, dtype=float).reshape(f.size, -1) @ eta + reg.h(eta) - tau0 > 0


def tilted_score(f, phi, ratio, region, eta, tau0: float, tau: float, d: Declared | None = None) -> np.ndarray:
    """The variable whose mean under the extremal ensemble at the pilot (tau0, eta) is Psi(tau, eta) up to a positive
    factor (Theorem 5.4(i)): the score s_tau; times l/u (``ratio``) where the pilot gave the upper weight and
    s_tau <= 0; times u/l where the pilot gave the lower weight and s_tau > 0 (possible only for tau < tau0;
    infinite where l = 0)."""
    f, eta = _vec(f), _vec(eta)
    reg = region if d is None else _region(region, d)
    s0 = f - np.asarray(phi, dtype=float).reshape(f.size, -1) @ eta + reg.h(eta)
    ratio = np.broadcast_to(np.asarray(ratio, dtype=float), (f.size,))
    up, s = s0 - tau0 > 0, s0 - tau
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(up & (s <= 0), ratio * s, np.where(~up & (s > 0), s / ratio, s))


def tilted_root(f, phi, ratio, region, eta, tau0: float, d: Declared | None = None) -> tuple[float, float]:
    """(root, sd): the level at which the sample mean of ``tilted_score`` changes sign - an estimate of the root
    T(eta) from draws of the extremal ensemble at the pilot - and the standard deviation of the score there.  For
    choosing the next pilot; nothing here is certified."""
    f, eta = _vec(f), _vec(eta)
    if f.size == 0:
        return math.nan, math.nan
    reg = region if d is None else _region(region, d)
    s0 = f - np.asarray(phi, dtype=float).reshape(f.size, -1) @ eta + reg.h(eta)
    lo, hi = float(s0.min()) - 1.0, float(s0.max())            # all scores positive at lo, none at hi
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if np.mean(tilted_score(f, phi, ratio, region, eta, tau0, mid, d)) > 0:
            lo = mid
        else:
            hi = mid
    return hi, float(np.std(tilted_score(f, phi, ratio, region, eta, tau0, hi, d)))


def certify_upper_tilted(f_va, phi_va, ratio_va, region, eta, tau0: float, d: Declared, delta: float) -> Bound:
    """Theorem 5.4: an upper bound tau >= tau0 for the whole identified set from independent draws of the extremal
    ensemble of the class at a pilot (tau0, eta) fixed before the draws - proportional to u on ``tilt_indicator``
    and to l elsewhere.  ``ratio_va`` is l/u at the draws.  The tested variable is the score itself (times l/u where
    its sign has changed since the pilot), bounded by the range of the score: neither ``d.U_max`` nor the envelope
    ratio enters.  Valid with probability >= 1 - delta whatever the pilot; a bad pilot only costs width."""
    f_va = _vec(f_va)
    phi_va = np.asarray(phi_va, dtype=float).reshape(f_va.size, -1)
    eta = _vec(eta)
    msg = d.invalid() or _bad_delta(delta)
    if msg:
        return Bound(d.f_hi, "void", msg)
    if not d.iid:
        return Bound(d.f_hi, "abstain", "the draws are not declared independent: Theorem 5.4 does not apply")
    if not (math.isfinite(tau0) and np.all(np.isfinite(eta))) or eta.size != phi_va.shape[1]:
        return Bound(d.f_hi, "void", "the pilot is not finite or has the wrong dimension")
    ratio = np.broadcast_to(np.asarray(ratio_va, dtype=float), (f_va.size,))
    msg = _range_violation(f_va, phi_va, d)
    if not msg and (not np.all(np.isfinite(ratio)) or np.any(ratio < 0) or np.any(ratio > 1 + 1e-12)):
        msg = "a drawn ratio l/u is outside [0, 1]"
    if msg:
        return Bound(d.f_hi, "void", msg)
    if tau0 > d.f_hi:
        return Bound(d.f_hi + d.f_err, "trivial", "the pilot is above the declared range", eta, tau0, f_va.size)
    reg = _region(region, d)
    h = reg.h(eta)
    s_lo, s_hi = _spread(eta, d, h)
    top = max(d.f_hi + s_hi - tau0, 0.0)                       # sup of the tested variable for tau >= tau0
    bot = max(d.f_hi - d.f_lo - s_lo, 0.0)                     # minus its inf over the bracket
    shift = d.eps_tv * (d.beta * top + bot)
    big = d.beta * top + shift
    s0 = f_va - phi_va @ eta + h
    up = s0 - tau0 > 0

    def zfun(tau):                                             # non-increasing in tau >= tau0
        s = s0 - tau
        z = np.where(up & (s <= 0), ratio * s, s)
        return d.beta * np.maximum(z, 0.0) - np.maximum(-z, 0.0) / d.beta + shift

    lo = max(tau0, d.f_lo)
    tau = _smallest_tau(zfun, big, lo, d.f_hi, math.log(1.0 / delta))
    if tau is None:
        return Bound(d.f_hi + d.f_err, "trivial", "the draws certify nothing below the declared range", eta, tau0, f_va.size)
    note = "certified at the pilot level: the bound cannot be below the pilot, and a lower pilot might certify less" if tau <= lo else ""
    return Bound(tau + d.f_err, "certified", note, eta, tau0, f_va.size)


def certify_lower_tilted(f_va, phi_va, ratio_va, region, eta, tau0: float, d: Declared, delta: float) -> Bound:
    """The lower end by the same theorem for -f: the draws come from the ensemble proportional to u where
    f - tau0 + eta . phi - h_R(eta) < 0 and to l elsewhere; the certified bound is <= tau0."""
    b = certify_upper_tilted(-_vec(f_va), phi_va, ratio_va, region, eta, -tau0, d.negated(), delta)
    return Bound(-b.value, b.status, b.note, b.eta, -b.tau_train, b.n_valid)


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
    if n == 0 or not (math.isfinite(G) and G > 0):             # the proposal is stated for G > 0 (REVIEW_A, K2)
        return dict(lo=-1.0, hi=1.0, kappa=math.inf, eps=math.inf, status="abstain",
                    note="S3 needs G > 0 and draws from q = (u - l)/G; for G = 0 the class is one ensemble (section 7.5)")
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
