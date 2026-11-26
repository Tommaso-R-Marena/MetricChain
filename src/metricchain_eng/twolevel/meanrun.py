"""The run of Algorithm 2L+ with every count replaced by its mean ("mean run"), on an instance
given by the law of the fibre averages W(a), with exact accounting of the evaluations for
two explicit, valid inner oracles.

Why the law is enough.  The outer loop of the algorithm (K_REPORT §2.2, steps 0-3) reads the
instance only through (i) the reference value psi_0, (ii) which sampled points are HIGH at each
level, and (iii) the brackets the inner procedures return.  With counts replaced by their
means, (ii) is a function of p(s) = P(W > s) alone.  (iii) is not determined by the
instance: an inner procedure may return any valid bracket of the promised ratio.  Two
consistent choices are implemented, between which every bracket placement lies:

    oracle "bottom":  rung l >= 1 returns [W, W e^{x_l}]      (the value sits at the lower end)
    oracle "top":     rung l >= 1 returns [W e^{-x_l}, W]     (the value sits at the upper end)

and the trivial bracket of rung 0 is [W e^{-t0}, W e^{x_0 - t0}], x_0 = 2 u n_i, where
t0 = ln(W / lower end) is a property of the fibre (the same for every fibre of a product
instance; u n_i for a flat fibre).  Under "bottom" every point of the tolerance zone
(s e^-b, s] is HIGH, under "top" none is; these are the two extreme trajectories.

General positions and the exact classification (``rung_positions``; added at checkpoint 4b).
Brackets are intersected from rung to rung, so after rung l a point has the bracket
[W e^{-A_l}, W e^{B_l}] with A_0 = t0, B_0 = x_0 - t0, A_l = min(A_{l-1}, alpha_l),
B_l = min(B_{l-1}, beta_l), where (alpha_l, beta_l) is where the rung-l inner bracket puts the
value ("bottom": (0, x_l); "top": (x_l, 0); any pair with alpha_l + beta_l <= x_l is allowed).
A point leaves the refinement loop HIGH at the first rung with L > s e^-b while U > s, and
LOW at the first rung with U <= s; since B_l decreases, it is HIGH iff

    W > s e^{-c},        c = max_{0 <= l <= L} min(b - A_l, B_l)        (0 <= c <= b).

In general (SCI-REV-0018, finding m1, re-derived there and checked on 400 000 random cases)

    c_bottom = max{ min(b - t0, x_0 - t0),  min(b, x_1, x_0 - t0) },      c_top = max{ 0, min(b - t0, x_0 - t0) }.

For "bottom" with x_0 - t0 >= b *and some inner accuracy at least b* (x_1 >= b; in every design
of X-005 the ladder ends at b itself) this is c = b, and for "top" with t0 >= b it is c = 0 -- the
two conventions above.  The rule needs that the levels are visited in increasing order (a point
meets a level at the rung where lower levels left it; finding m2 of the same review).
**They differ from the algorithm in two corners**: "top" with t0 < b
(the value lies within the tolerance of the lower end of the trivial bracket, so points with
W in (s e^{-(b - t0)}, s] are classified HIGH at rung 0 without a call; c = b - t0) and
"bottom" with x_0 - t0 < b (c = x_0 - t0).  The runs of experiment X-005 as published at
checkpoints 3 and 4 used c = b / c = 0 everywhere; ``legacy_classification=True`` reproduces
them.

Evaluations.  A point a_i is moved from rung l to rung l + 1 at level j when it is among the
points used at that level (i <= M_j) and its rung-l bracket [L, U] has U > s_j and
L <= s_j e^-b, i.e. when  s_j  lies in  [L e^b, U).  These windows are nested in l for l >= 1
and contained in the window of rung 0, so the number of calls of I_{l+1} is

    calls_{l+1} = sum over atoms w of  P(W = w) * max{ M_j : j <= j_stop,  w e^{b - alpha_l} <= s_j < w e^{beta_l} },

with (alpha_l, beta_l) the logarithmic distances of the value from the two ends of the rung-l
bracket (after intersection with the trivial bracket).  The number of evaluations is

    1 + max_j M_j + sum_{l=1}^{L} calls_l * C_l .

Ties.  The reference point's own weight lies exactly on the level grid whenever its fibre is
flat and u n / lambda is an integer (s_j = s_0 e^{j lambda}, s_0 = e^{-psi_0 - u n}), so "W > s_j"
with W = s_j is not a rare coincidence, and in floating point ln s_j = (-psi_0 - u n) + j lambda
is off by rounding.  Every comparison of a weight with a level therefore treats values
within TIE = 1e-9 (in the logarithm) as equal, which is what exact arithmetic gives.

"Populated" (SCI-REV-0018, finding m9).  A pass m is counted as populated when
m >= -log2 P(HIGH) - 1e-12, i.e. when 2^m P(HIGH) >= 1 - 6.93e-13, where the mean count alone
would ask for 2^m P(HIGH) >= 1.  The tolerance is part of the definition of this mean run (it
absorbs rounding of -log2 at exact powers of two); with n_o >= 41 the extreme shell has a
probability below it.  In the review's 600 runs the other reading changes ln(cost) by at most
0.0345.  Neither is "the" mean run: a literal run has N = K at such a pass with probability
(1 - eps)^K.

Memory.  The calls of a rung are range maxima of the sample sizes over one window per atom;
``_range_max`` answers them from a sparse table of O(j_stop log j_stop) numbers (it used to keep
one array per distinct window length: 6.4 GB at n = 16 000, finding m8 of the same review).

Nothing here is taken from the workstream's scripts; ``experiments/eng/twolevel/controls.py``
compares the results with the workstream's stored outputs.
"""
from __future__ import annotations

import math
from bisect import bisect_left, bisect_right
from dataclasses import dataclass, field

import numpy as np

from .alg2l import Constants, Params, constants, inner_costs, lC_max, logsumexp
from .tables import LN2, TIE, TOL, CubeTables

POP, NEG, STOP_POP, STOP_UNPOP = 0, 1, 2, 3


# ---------------------------------------------------------------------------------------------
# Laws of W
# ---------------------------------------------------------------------------------------------
@dataclass
class Law:
    """A discrete law of ln W: atoms ``lw`` (any order) with log-probabilities ``lpr``."""

    lw: np.ndarray
    lpr: np.ndarray
    ltail_ge: np.ndarray = field(init=False, repr=False)
    lA: float = field(init=False)

    def __post_init__(self) -> None:
        order = np.argsort(self.lw, kind="stable")
        self.lw = np.asarray(self.lw, dtype=float)[order]
        self.lpr = np.asarray(self.lpr, dtype=float)[order]
        total = float(np.logaddexp.reduce(self.lpr))
        if abs(total) > 1e-8:
            raise ValueError(f"probabilities sum to exp({total})")
        # Normalise exactly.  A total of 1 - 1e-12 would make the levels below the whole support look
        # "not populated at the first pass" (M p < K by one part in 10^12), which no run does.
        self.lpr = self.lpr - total
        self.ltail_ge = np.concatenate([np.logaddexp.accumulate(self.lpr[::-1])[::-1], [-np.inf]])
        self.ltail_ge[0] = 0.0
        self.lA = float(np.logaddexp.reduce(self.lw + self.lpr))

    def ltail_gt(self, ls, tie: float = TIE):
        """ln P(W > e^ls) (vectorised).  A weight within ``tie`` of the threshold counts as equal to it."""
        return self.ltail_ge[np.searchsorted(self.lw, np.asarray(ls) + tie, side="right")]


def radial_law(F: np.ndarray, tables: CubeTables, shift: float = 0.0) -> Law:
    """Law of W(a) = exp(shift - F(d(a, centre))) for a uniform point of the cube of ``tables``."""
    F = np.asarray(F, dtype=float)
    if F.shape != (tables.m + 1,):
        raise ValueError("profile must have m + 1 values")
    return Law(shift - F, tables.lbinom - tables.m * LN2)


def lipschitz_violation(F: np.ndarray, u: float) -> float:
    """max |F(d+1) - F(d)| - u  (<= 0 for a u-Lipschitz radial profile)."""
    return float(np.max(np.abs(np.diff(F)))) - u if len(F) > 1 else -u


@dataclass
class Instance:
    """Everything the mean run needs to know about the instance.

    law   law of the fibre averages W(a), a uniform in the outer cube
    psi0  the value of psi at the reference point 0^n
    t0    ln(W(a) / lower end of the trivial bracket) = psi(a, 0) + u n_i + ln W(a), taken equal
          for all a (true for product instances psi(a, b) = F_o(a) + F_i(b));
          admissible range: n_i (u - Lambda_1) <= t0 <= n_i (2u - Lambda_1)
    """

    law: Law
    psi0: float
    t0: float = 0.0


# ---------------------------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------------------------
@dataclass
class Run:
    status: str = ""             # "closed-populated", "closed-unpopulated", "abort-levels", "abort-sample"
    j_stop: int = -1
    r_close: int = -2            # closing radius (-1: empty tail)
    lM_last: float = -math.inf   # ln of the sample size at the closing pass
    lM_max: float = -math.inf    # ln of the largest sample used (= number of outer points drawn)
    lL: float = -math.inf
    lU: float = math.inf
    lA: float = 0.0
    width: float = math.inf      # ln(U/L)
    npop: int = 0
    nneg: int = 0
    min_pop_radius: float = math.inf   # least closing radius r(q_j) over populated levels that were left
    # claims of Theorem 11.56 (each "slack" must be <= 0, "margin" must be > 0)
    slack_valid_lower: float = -math.inf     # ln L - ln A
    slack_valid_upper: float = -math.inf     # ln A - ln U
    slack_width: float = -math.inf           # ln(U/L) - x_out
    margin_iii: float = math.inf             # min over levels left of ln q_j - ln pi_dagger
    slack_iv_M: float = -math.inf            # max_j ln M_j - max(ln K, ln 2 + ln M_j^neg)
    slack_iv_Mneg: float = -math.inf         # max_j ln M_j^neg - ln((1+eta) e^lam nu0 M_dagger)
    slack_iv_Mbar: float = -math.inf         # max_j ln M_j - ln M_bar
    slack_v: float = -math.inf               # max_{j,x} ln(M_j^neg p(s_j e^-x)) - ln((1+eta)/(1-eta) e^lam nu e^x)
    slack_vi: float = -math.inf              # max_{j,l} ln(M_j p(s_j e^-x_{l-1})) - ln cnt(x_{l-1})   (mean count per level)
    # evaluations
    lcalls: np.ndarray | None = None         # ln calls_l, l = 0..L (index 0 unused)
    lcost: float = math.inf                  # ln(number of evaluations)
    lCmax: float = math.inf
    # per-level record (kept when record=True)
    lM: np.ndarray | None = None
    kind: np.ndarray | None = None
    lq: np.ndarray | None = None
    lMneg: np.ndarray | None = None

    @property
    def closed(self) -> bool:
        return self.status.startswith("closed")

    def violations(self, tol: float = 1e-7) -> list[str]:
        """Names of the claims of Theorem 11.56 that this run violates."""
        out = []
        if not self.closed:
            out.append("(i) " + self.status)
        for name in ("slack_valid_lower", "slack_valid_upper", "slack_width", "slack_iv_M", "slack_iv_Mneg",
                     "slack_iv_Mbar", "slack_v", "slack_vi"):
            if getattr(self, name) > tol:
                out.append(name)
        if self.margin_iii <= -tol:
            out.append("margin_iii")
        if self.lcost > self.lCmax + tol:
            out.append("cost > C_max")
        return out


# ---------------------------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------------------------
def _forward_window_max(arr: np.ndarray, w: int) -> np.ndarray:
    """out[j] = max(arr[j : j + w]) (shorter windows at the end), by the van Herk / Gil-Werman scheme."""
    n = arr.size
    if w <= 1:
        return arr.copy()
    if w >= n:
        return np.maximum.accumulate(arr[::-1])[::-1]
    pad = (-n) % w + w                      # one extra block, so that j + w - 1 always exists
    a = np.concatenate([arr, np.full(pad, -np.inf)]).reshape(-1, w)
    pre = np.maximum.accumulate(a, axis=1).ravel()
    suf = np.maximum.accumulate(a[:, ::-1], axis=1)[:, ::-1].ravel()
    idx = np.arange(n)
    return np.maximum(suf[idx], pre[idx + w - 1])


def _sparse_table(arr: np.ndarray) -> list[np.ndarray]:
    """levels[k][i] = max(arr[i : i + 2**k]) for every i with i + 2**k <= len(arr)."""
    levels = [np.asarray(arr)]
    n, w = levels[0].size, 1
    while 2 * w <= n:
        prev = levels[-1]
        levels.append(np.maximum(prev[:n - 2 * w + 1], prev[w:n - w + 1]))
        w *= 2
    return levels


def _range_max(arr: np.ndarray, lo: np.ndarray, hi: np.ndarray, cache: dict) -> np.ndarray:
    """max(arr[lo..hi]) for index arrays lo, hi (inclusive); -inf where lo > hi.  ``cache`` belongs to ``arr``:
    it keeps the sparse table between calls."""
    out = np.full(lo.shape, -np.inf)
    ok = hi >= lo
    if not ok.any():
        return out
    if "sparse" not in cache:
        cache["sparse"] = _sparse_table(arr)
    levels = cache["sparse"]
    l_, h_ = lo[ok], hi[ok]
    k = np.frexp((h_ - l_ + 1).astype(np.float64))[1] - 1          # floor(log2(length)), exact below 2^53
    res = np.empty(l_.shape)
    for kk in np.unique(k):
        sel = k == kk
        t = levels[int(kk)]
        res[sel] = np.maximum(t[l_[sel]], t[h_[sel] - (1 << int(kk)) + 1])
    out[ok] = res
    return out


# ---------------------------------------------------------------------------------------------
# The mean run
# ---------------------------------------------------------------------------------------------
def rung_positions(P: Params, t0: float, oracle: str = "bottom", positions: tuple | None = None,
                   legacy_classification: bool = False) -> tuple[np.ndarray, np.ndarray, float]:
    """(A, B, c): the nested logarithmic distances A_l, B_l (l = 0..L) of a fibre average from the two ends of
    its bracket after rung l, and the classification shift c -- a sample point is HIGH at the level s iff
    W > s e^{-c} (module docstring).  ``positions = (alpha, beta)`` gives the rung brackets for l = 1..L
    explicitly (each alpha_l, beta_l >= 0 with alpha_l + beta_l <= x_l); otherwise they come from ``oracle``.
    For n_i = 0 (outer loop alone) the conventions c = b ("bottom") and c = 0 ("top") are returned.

    ``t0`` may be a pair (lo, hi): then A_0 = hi and B_0 = x_0 - lo, the *union* over t0 in [lo, hi] of the
    refinement windows of every rung (with the running minima of the rung positions).  The mean run with these
    positions counts, for every atom of the law, at least as many calls at every rung as the mean run of any
    instance with this law of fibre averages *and this reference value* whose fibres have t0 in [lo, hi] and
    whose inner behaviour is the same for all fibres, product or not: an upper bound on the **mean-run**
    evaluations of every such instance (single literal runs can exceed it; SCI-REV-0018, finding m4).
    **Condition (the range condition; finding m3 of that review).**  The sample sizes depend on the law and on
    the shift c only, so the statement needs the shift to be the same for every placement in [lo, hi].  c is
    nonincreasing in t0, so that holds iff it is the same at lo and at hi; for the two oracles this means
    lo >= b ("top") and x_0 - hi >= b with x_1 >= b ("bottom").  Outside this range the union is the shift of no
    fibre and bounds nothing (a product instance can cost e^{6.83} times what it returns: the review's example
    is the unit test), so a pair with different shifts at its two ends raises ``ValueError``."""
    if oracle not in ("bottom", "top"):
        raise ValueError("oracle must be 'bottom' or 'top'")
    L, b = P.L, P.b
    if P.n_i == 0:
        return np.zeros(L + 1), np.zeros(L + 1), (b if oracle == "bottom" else 0.0)
    x0 = P.xs[0]
    t0_lo, t0_hi = (t0, t0) if np.isscalar(t0) else (float(t0[0]), float(t0[1]))
    if positions is None:
        alpha = [0.0 if oracle == "bottom" else P.xs[l] for l in range(1, L + 1)]
        beta = [P.xs[l] if oracle == "bottom" else 0.0 for l in range(1, L + 1)]
    else:
        alpha, beta = (list(map(float, v)) for v in positions)
        if len(alpha) != L or len(beta) != L:
            raise ValueError("positions must give (alpha_l, beta_l) for l = 1..L")
        for l in range(1, L + 1):
            if alpha[l - 1] < 0 or beta[l - 1] < 0 or alpha[l - 1] + beta[l - 1] > P.xs[l] + 1e-9:
                raise ValueError("a rung bracket must contain the value and have ratio at most e^{x_l}")
    def shift(t: float) -> float:
        """c for a fibre whose value sits at t above the lower end of its trivial bracket."""
        a_, b_ = float(t), float(x0 - t)
        best = min(b - a_, b_)
        for l in range(1, L + 1):
            a_, b_ = min(a_, alpha[l - 1]), min(b_, beta[l - 1])
            best = max(best, min(b - a_, b_))
        return best

    A, B = [float(t0_hi)], [float(x0 - t0_lo)]
    for l in range(1, L + 1):
        A.append(min(A[-1], alpha[l - 1]))
        B.append(min(B[-1], beta[l - 1]))
    if legacy_classification:
        if positions is not None:
            raise ValueError("the legacy classification exists for the two oracles only")
        c = b if oracle == "bottom" else 0.0
    elif t0_lo == t0_hi:
        c = shift(t0_lo)
    else:
        c_lo, c_hi = shift(t0_lo), shift(t0_hi)
        if abs(c_lo - c_hi) > 1e-12:
            raise ValueError(f"the classification shift differs over the range of placements ({c_lo:.6g} at t0 = {t0_lo:.6g}, "
                             f"{c_hi:.6g} at t0 = {t0_hi:.6g}): the union of the windows is not a bound here")
        c = c_lo
    return np.array(A), np.array(B), float(c)


def mean_run(P: Params, outer: CubeTables, inst: Instance, oracle: str = "bottom", *, C: Constants | None = None,
             lC: np.ndarray | None = None, harper: bool = True, record: bool = False,
             count_grid: tuple = (), enforce_abort: bool = True, tie: float = TIE,
             positions: tuple | None = None, legacy_classification: bool = False) -> Run:
    """Run Algorithm 2L+ on ``inst`` with counts replaced by their means.

    oracle   "bottom" or "top" (see the module docstring)
    positions  (alpha, beta) for the rungs l = 1..L instead of an oracle (``rung_positions``)
    legacy_classification  True: c = b / c = 0 regardless of t0 (X-005 as published; module docstring)
    lC       ln C_l, l = 0..L (default: the base family inside); ignored when n_i = 0
    harper   False removes the Harper term from the lower bound (a mutation, for controls)
    enforce_abort  False lets the sample grow beyond K 2^{m_max} (only for comparison with scripts
             that do not implement the abort rule; the claims then report by how much)
    tie      tolerance of the comparisons of weights with levels (module docstring, "Ties"); 0 gives plain
             floating-point comparisons
    count_grid  extra values of x at which claim (v) is tested (the ladder is always tested)
    """
    if oracle not in ("bottom", "top"):
        raise ValueError("oracle must be 'bottom' or 'top'")
    if C is None:
        C = constants(P, outer)
    n, n_o, n_i, u, b, lam, eta = P.n, P.n_o, P.n_i, P.u, P.b, P.lam, P.eta
    law = inst.law
    J = C.J
    lK, lnu = C.lK, C.lnu
    lth = P.lth
    l1me, l1pe = math.log(1 - eta), math.log(1 + eta)
    nln2 = n_o * LN2
    ls0 = -inst.psi0 - u * n
    lell = -inst.psi0 + n * math.log((1 + math.exp(-u)) / 2)
    if law.lw[0] < ls0 - 1e-9 or law.lw[-1] > ls0 + 2 * u * n + 1e-9:
        raise ValueError("the law is not supported in [s_0, s_0 e^{2un}]: psi0 does not belong to this instance")

    A_pos, B_pos, c_class = rung_positions(P, inst.t0, oracle, positions, legacy_classification)
    ls = ls0 + lam * np.arange(J + 1)
    ph = law.ltail_gt(ls - c_class, tie)                        # ln P(HIGH) at each level
    with np.errstate(divide="ignore", invalid="ignore"):
        m_pop = np.where(ph >= 0.0, 0.0, np.ceil(-ph / LN2 - 1e-12))
    m_pop_l = m_pop.tolist()
    ph_l = ph.tolist()
    ls_l = ls.tolist()
    lE = outer.lE[:n_o].tolist()                                # radii 0 .. n_o - 1 only: no closure at radius n_o
    lball = outer.lball
    lT = outer.lT
    m_empty = math.floor(n_o - l1me / LN2 + 1e-12) + 1          # least m with 2^{n_o} q_m < 1, q_m = 1/((1-eta) 2^m)
    l_e_lam_m1 = math.log(math.expm1(lam))
    l_1_m_e = math.log(-math.expm1(-lam))

    R = Run(lA=law.lA)
    lM_rec = np.full(J + 1, -np.inf)
    kind_rec = np.full(J + 1, -1, dtype=np.int8)
    lq_rec = np.full(J + 1, np.nan)
    lMneg_rec = np.full(J + 1, np.nan)
    lsum = -math.inf            # ln Sigma
    lU_acc = ls0                # ln(s_0 + sum_{i<j} (s_{i+1} - s_i) q_i)
    j_stop = -1
    for j in range(J + 1):
        lsj = ls_l[j]
        lell_in = lell
        lMneg = lnu + lsj - lell_in - b
        lMneg_rec[j] = lMneg
        m_neg = max(0, math.ceil((lMneg - lK) / LN2 - 1e-12))
        # closure at an unpopulated pass m: q_m = min(1, 1/((1-eta) 2^m)), tail nonincreasing in m
        m_close = m_empty
        r_ok = bisect_right(lE, lth + b + lell_in - lsj + nln2 + TOL) - 1
        if r_ok >= 0:
            m2 = max(0, math.ceil((nln2 - l1me - float(lball[r_ok])) / LN2 - 1e-12))
            if m2 < m_close:
                m_close = m2
        mp = m_pop_l[j]
        m_end = min(mp, m_neg, m_close)
        if m_end > C.m_max and enforce_abort:
            R.status = "abort-sample"
            j_stop = j
            lM_rec[j] = lK + C.m_max * LN2
            kind_rec[j] = NEG
            break
        lM = lK + m_end * LN2
        lM_rec[j] = lM
        if mp == m_end:                                          # populated at this pass
            lph = ph_l[j]
            lpbar = lph - l1pe
            lell = max(lell, lsj - b + lpbar)
            if harper:
                k = outer.kball(nln2 + lpbar)
                lell = max(lell, lsj - b - nln2 + float(lT[k]))
            lq = min(0.0, lph - l1me)
            if nln2 + lq < 0.0:
                r, ltail = -1, -math.inf
            else:
                r = outer.radius(lq)
                ltail = lsj - nln2 + float(outer.lE[r]) if r <= n_o - 1 else math.inf
            lq_rec[j] = lq
            new_sum = float(np.logaddexp(lsum, l_1_m_e - b + lsj + lpbar))
            if ltail <= lth + b + lell:
                R.status, R.r_close, R.lM_last = "closed-populated", r, lM
                R.lL = max(lell, new_sum)
                R.lU = float(np.logaddexp(lU_acc, ltail))
                kind_rec[j] = STOP_POP
                j_stop = j
                break
            lsum = new_sum
            lU_acc = float(np.logaddexp(lU_acc, l_e_lam_m1 + lsj + lq))
            kind_rec[j] = POP
            R.npop += 1
            R.min_pop_radius = min(R.min_pop_radius, r)
        elif m_close == m_end:                                   # closure at an unpopulated pass
            lq = min(0.0, -l1me - m_end * LN2)
            if nln2 + lq < 0.0:
                r, ltail = -1, -math.inf
            else:
                r = outer.radius(lq)
                ltail = lsj - nln2 + float(outer.lE[r]) if r <= n_o - 1 else math.inf
            lq_rec[j] = lq
            R.status, R.r_close, R.lM_last = "closed-unpopulated", r, lM
            R.lL = max(lell, lsum)
            R.lU = float(np.logaddexp(lU_acc, ltail))
            kind_rec[j] = STOP_UNPOP
            j_stop = j
            break
        else:                                                    # left as negligible
            lq = min(0.0, -l1me - m_end * LN2)
            lq_rec[j] = lq
            lU_acc = float(np.logaddexp(lU_acc, l_e_lam_m1 + lsj + lq))
            kind_rec[j] = NEG
            R.nneg += 1
    else:
        R.status = "abort-levels"
        j_stop = J
    R.j_stop = j_stop
    used = slice(0, j_stop + 1)
    lMj = lM_rec[used]
    R.lM_max = float(np.max(lMj))

    # ---- claims of Theorem 11.56 ---------------------------------------------------------
    if R.closed:
        R.width = R.lU - R.lL
        R.slack_valid_lower = R.lL - law.lA
        R.slack_valid_upper = law.lA - R.lU
        R.slack_width = R.width - C.x_out
    left = kind_rec[used] <= NEG                                  # levels left without stopping
    if left.any():
        R.margin_iii = float(np.min(lq_rec[used][left] - C.lpi_dag))
    R.slack_iv_M = float(np.max(lMj - np.maximum(lK, LN2 + lMneg_rec[used])))
    R.slack_iv_Mneg = float(np.max(lMneg_rec[used])) - C.lMneg_cap
    R.slack_iv_Mbar = R.lM_max - C.lM_bar
    xs_v = sorted(set(list(P.xs[:-1]) + list(count_grid))) if n_i > 0 else sorted(set(count_grid))
    for x in xs_v:
        if x <= 0:
            continue
        lp_x = law.ltail_gt(ls[used] - x, tie)
        R.slack_v = max(R.slack_v, float(np.max(lMneg_rec[used] + lp_x)) - (C.lcount_factor + x))
        if n_i > 0:
            R.slack_vi = max(R.slack_vi, float(np.max(lMj + lp_x)) - C.lcnt(x, P))

    # ---- evaluations -----------------------------------------------------------------------
    if n_i > 0:
        if lC is None:
            lC = inner_costs(P, C)
        R.lCmax = lC_max(P, C, lC)
        x0 = P.xs[0]
        t0 = inst.t0
        if not (-1e-9 <= t0 <= x0 + 1e-9):
            raise ValueError("t0 must lie in [0, x_0]")
        cache: dict = {}
        lcalls = np.full(P.L + 1, -np.inf)
        for l in range(P.L):                                     # calls of I_{l+1}: windows of the rung-l bracket
            alpha, beta = float(A_pos[l]), float(B_pos[l])
            lo = np.ceil((law.lw + b - alpha - ls0) / lam - 1e-12).astype(np.int64)
            hi = np.ceil((law.lw + beta - ls0) / lam - 1e-12).astype(np.int64) - 1
            lo = np.maximum(lo, 0)
            hi = np.minimum(hi, j_stop)
            mx = _range_max(lMj, lo, np.maximum(hi, lo - 1), cache)
            lcalls[l + 1] = float(np.logaddexp.reduce(law.lpr + mx))
        R.lcalls = lcalls
        R.lcost = logsumexp([0.0, R.lM_max] + [lcalls[l] + lC[l] for l in range(1, P.L + 1)])
    if record:
        R.lM, R.kind, R.lq, R.lMneg = lMj, kind_rec[used], lq_rec[used], lMneg_rec[used]
    return R
