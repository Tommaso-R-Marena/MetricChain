"""A literal run of Algorithm 2L+ (K_REPORT §2.2) on a radial outer landscape, with the outer sample
drawn at random and the inner procedures replaced by an oracle that returns a valid bracket.

Purpose: an implementation that follows the text step by step (pass by pass, point group by point
group, with the abort rule) and shares no code with the mean-run evaluator except the cube tables
and the constants.  ``tests/eng/test_twolevel.py`` compares the two; ``experiments/eng/twolevel``
uses it for runs with real fluctuations of the counts.

The outer points are i.i.d. uniform in Q_{n_o}; only their distance d from the centre matters, so
the sample is stored as counts per (block, shell): block 0 holds the first K points, block k >= 1
the points K 2^{k-1} + 1 .. K 2^k.  All points of one (block, shell) group receive the same
brackets -- a valid, if correlated, inner behaviour (the device of K_REPORT §6.8).  Oracles:

    "bottom"  [W, W e^x]        "top"  [W e^-x, W]        "random"  [W e^{-t x}, W e^{(1-t) x}], t uniform per call

and one INVALID inner behaviour, for the claim that the cost bound holds in every run (requested by the
Scientific Discovery Division, SCI-REV-0007 R6-E2):

    "dear"    [s_j e^{-(x+b)/2}, s_j e^{(x-b)/2}] at the level s_j at which the point is refined -- a bracket that
              ignores W and straddles the level at every rung, so that every refined point is refined down to the
              last (dearest) rung.  The returned bracket of such a run means nothing; only its cost is examined.

The trivial bracket of rung 0 is [W e^{-t0}, W e^{x_0 - t0}].
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from .alg2l import Constants, Params, logsumexp
from .sampling import stable_multinomial
from .tables import LN2, TIE, CubeTables


@dataclass
class SimResult:
    status: str = ""                    # "closed-populated", "closed-unpopulated", "abort-<reason>"
    j_stop: int = -1
    lL: float = -math.inf
    lU: float = math.inf
    lA: float = 0.0
    valid: bool = False
    width: float = math.inf
    M_max: int = 0
    npop: int = 0
    nneg: int = 0
    calls: list = field(default_factory=list)       # number of calls of I_l, l = 0..L (index 0 unused)
    lqueries: float = -math.inf                      # ln(number of evaluations)
    good_event: bool = True                         # (V2) and (V3) on the realised sample
    last_rung_ties: int = 0                         # points classified by the tie rule at the last rung
    trivial_returned: bool = False                  # the closure test returned L > U and the trivial bracket was returned instead
    violations: list = field(default_factory=list)  # claims of Theorem 11.56 violated by this run
    levels: list = field(default_factory=list)      # per level: (kind, M, N, lq)


def simulate(P: Params, outer: CubeTables, C: Constants, F: np.ndarray, psi0: float, t0: float, shift: float, oracle: str,
             rng: np.random.Generator, lC: np.ndarray | None = None, lCmax: float = math.inf,
             K_override: int | None = None, literal_ties: bool = False, sampler: str = "exact") -> SimResult:
    """One run.  ``F``: radial profile (ln W = shift - F(d)); ``psi0``: reference value; ``t0``: position of W in
    the trivial bracket.  ``K_override`` replaces K (and nu = K nu0, M_dagger, M_bar, cnt) to see where the
    probabilistic events start to fail; the claims are then tested with the constants so changed.

    Ties.  Comparisons of a bracket end with a level treat logarithms within TIE as equal, and a point at the
    last rung is classified by its upper end alone (its bracket has ratio at most e^b, so U > s_j implies
    L > s_j e^-b): this is what exact arithmetic does.  ``literal_ties=True`` switches both off -- plain floating
    point comparisons and the abort of step 3 -- to exhibit the pitfall recorded by referee R8 (m10).

    ``sampler``: "exact" (``sampling.binomial_exact``) or "numpy" (numpy's binomial at every block size -- the
    first version, biased for blocks of 10^15 points and more; kept to reproduce job M-011)."""
    tie = 0.0 if literal_ties else TIE
    n, n_o, n_i, u, b, lam, eta = P.n, P.n_o, P.n_i, P.u, P.b, P.lam, P.eta
    L = P.L
    xs = P.xs
    K = C.K if K_override is None else int(K_override)
    lK = math.log(K)
    lnu = lK + math.log(C.nu0)
    lM_dag = lK - math.log(1 - eta) - C.lpi_dag
    lM_bar = math.log(2 * (1 + eta) * C.nu0) + lam + lM_dag
    lcount_factor = math.log((1 + eta) / (1 - eta)) + lam + lnu
    lcnt_const = math.log(2 * (1 + eta) ** 2 / (1 - eta)) + lam + lnu
    lMneg_cap = math.log((1 + eta) * C.nu0) + lam + lM_dag
    m_max = C.m_max
    m_cap = 61 - math.ceil(math.log2(K))                     # samples are stored as int64 counts: K 2^m < 2^61
    nln2 = n_o * LN2
    lth = math.log(P.theta)
    lpmf = outer.lbinom - nln2
    lpmf = lpmf - float(np.logaddexp.reduce(lpmf))
    lw = shift - np.asarray(F, dtype=float)                  # ln W per shell
    order = np.argsort(lw, kind="stable")
    lw_sorted = lw[order]
    ltail_sorted = np.concatenate([np.logaddexp.accumulate(lpmf[order][::-1])[::-1], [-np.inf]])
    ltail_sorted[0] = 0.0

    def lp_gt(ls: float) -> float:                           # ln P(W > e^ls), exact
        return float(ltail_sorted[np.searchsorted(lw_sorted, ls + TIE, side="right")])

    lA = float(np.logaddexp.reduce(lw + lpmf))
    ls0 = -psi0 - u * n
    lell = -psi0 + n * math.log((1 + math.exp(-u)) / 2)
    R = SimResult(lA=lA, calls=[0] * (L + 1))

    # groups: per block a dict of arrays over shells
    counts: list[np.ndarray] = []
    rung: list[np.ndarray] = []
    glL: list[np.ndarray] = []
    glU: list[np.ndarray] = []
    x0 = xs[0] if n_i > 0 else 0.0

    def draw_block(k: int) -> None:
        size = K if k == 0 else K * 2 ** (k - 1)
        counts.append(stable_multinomial(rng, size, lpmf, sampler))
        rung.append(np.zeros(n_o + 1, dtype=np.int64))
        glL.append(lw - t0)
        glU.append(lw + x0 - t0)

    calls = R.calls
    lcalls_cost = -math.inf                                   # ln of the evaluations spent in inner calls

    def classify_block(k: int, lsj: float) -> int | None:
        """Classify the points of block k at the level e^lsj; returns its number of HIGH points, None on abort.
        (Within one level the blocks classified at earlier passes do not change, so a pass only adds a block.)"""
        nonlocal lcalls_cost
        cnt, rg, gl, gu = counts[k], rung[k], glL[k], glU[k]
        todo = np.flatnonzero((cnt > 0) & (gu > lsj + tie) & (gl <= lsj - b + tie))
        for d in todo.tolist():
            while gu[d] > lsj + tie and gl[d] <= lsj - b + tie:
                if rg[d] == L:
                    if literal_ties:
                        R.status = "abort-unclassified at the last rung"
                        return None
                    R.last_rung_ties += 1
                    break
                l = int(rg[d]) + 1
                if lC is not None:                            # abort test BEFORE the call (R8, m1)
                    new = float(np.logaddexp(lcalls_cost, math.log(int(cnt[d])) + float(lC[l])))
                    if logsumexp([0.0, new, lK + (len(counts) - 1) * LN2]) > lCmax + 1e-9:
                        R.status = "abort-query budget"
                        return None
                    lcalls_cost = new
                rg[d] = l
                calls[l] += int(cnt[d])
                x = xs[l]
                if oracle == "dear":                          # invalid on purpose: straddles the level until the last rung
                    gl[d] = lsj - (x + b) / 2
                    gu[d] = lsj + (x - b) / 2
                    continue
                t = 0.0 if oracle == "bottom" else 1.0 if oracle == "top" else float(rng.random())
                gl[d] = max(gl[d], lw[d] - t * x)
                gu[d] = min(gu[d], lw[d] + (1.0 - t) * x)
        return int(cnt[gu > lsj + tie].sum())

    lsum = -math.inf
    lU_acc = ls0
    records = []                 # per level left: (j, kind, m, N, lq, lpbar, lell_in, lMneg)
    J = C.J
    stopped = False
    for j in range(J + 1):
        lsj = ls0 + lam * j
        lell_in = lell
        lMneg = lnu + lsj - lell_in - b
        m = 0
        N = 0
        while True:
            if m > m_max or m > m_cap:
                R.status = "abort-sample size" if m > m_max else "skipped-sample beyond 2^61"
                stopped = True
                break
            while len(counts) <= m:
                draw_block(len(counts))
            lM = lK + m * LN2
            M = K * 2 ** m
            Nk = classify_block(m, lsj)
            if Nk is None:
                stopped = True
                break
            N += Nk
            lq = min(0.0, math.log(max(N, K)) - math.log(1 - eta) - lM)
            populated = N >= K
            lpbar = math.log(N) - math.log(1 + eta) - lM if populated else -math.inf
            if populated:
                kk = outer.kball(nln2 + lpbar)
                lell = max(lell, lsj - b + lpbar, lsj - b - nln2 + float(outer.lT[kk]))
            if nln2 + lq < 0.0:
                r, ltail = -1, -math.inf
            else:
                # q is a ratio of integers: decide "least r with |B(r)| >= 2^{n_o} q" on the complement when q is near 1
                l1mq = None
                if lq > -LN2 and populated:
                    num = (1 - eta) * M - N
                    l1mq = math.log(num / ((1 - eta) * M)) if num > 0 else -math.inf
                r = outer.radius(lq, l1mq) if lq < 0.0 else n_o
                ltail = lsj - nln2 + float(outer.lE[r]) if r <= n_o - 1 else math.inf
            if ltail <= lth + b + lell:                                              # (c) closure test
                new_sum = float(np.logaddexp(lsum, math.log(-math.expm1(-lam)) - b + lsj + lpbar)) if populated else lsum
                R.lL = max(lell, new_sum)
                R.lU = float(np.logaddexp(lU_acc, ltail))
                R.status = "closed-populated" if populated else "closed-unpopulated"
                records.append((j, 2 if populated else 3, m, N, lq, lpbar, lell_in, lMneg))
                stopped = True
                break
            if populated:                                                            # (d)
                lsum = float(np.logaddexp(lsum, math.log(-math.expm1(-lam)) - b + lsj + lpbar))
                lU_acc = float(np.logaddexp(lU_acc, math.log(math.expm1(lam)) + lsj + lq))
                records.append((j, 0, m, N, lq, lpbar, lell_in, lMneg))
                R.npop += 1
                break
            if lM >= lMneg:                                                          # (e)
                lU_acc = float(np.logaddexp(lU_acc, math.log(math.expm1(lam)) + lsj + lq))
                records.append((j, 1, m, N, lq, lpbar, lell_in, lMneg))
                R.nneg += 1
                break
            m += 1                                                                   # (f)
        if stopped:
            R.j_stop = j
            break
    else:
        R.status = "abort-level J left"
        R.j_stop = J
    R.M_max = K * 2 ** (len(counts) - 1) if counts else 0
    R.levels = [(rec[1], K * 2 ** rec[2], rec[3], rec[4]) for rec in records]
    terms = [0.0, math.log(R.M_max)] if R.M_max else [0.0]
    if lC is not None:
        terms += [math.log(calls[l]) + float(lC[l]) for l in range(1, L + 1) if calls[l] > 0]
    R.lqueries = logsumexp(terms)

    # ---- the good event on the realised sample: (V2), (V3) for all levels reached and all sample sizes drawn ----
    thresholds_x = [0.0, b] + ([xs[l] for l in range(L)] if n_i > 0 else [])
    desc = np.argsort(-lw, kind="stable")
    lw_desc_neg = -lw[desc]                                   # ascending
    cum = np.cumsum(np.array(counts, dtype=np.int64), axis=0)[:, desc]             # blocks 0..m, shells by decreasing W
    prefix = np.concatenate([np.zeros((cum.shape[0], 1), dtype=np.int64), np.cumsum(cum, axis=1)], axis=1)
    j_reached = R.j_stop
    ls_all = ls0 + lam * np.arange(j_reached + 1)

    def X_vec(m: int, ls: np.ndarray) -> np.ndarray:         # number of the first K 2^m points with W > e^ls
        return prefix[m][np.searchsorted(lw_desc_neg, -(ls + TIE), side="left")]

    def lp_vec(ls: np.ndarray) -> np.ndarray:
        return ltail_sorted[np.searchsorted(lw_sorted, ls + TIE, side="right")]

    for m in range(len(counts)):
        Mf = float(K) * 2.0 ** m
        for x in thresholds_x:
            pt = np.exp(lp_vec(ls_all - x))
            Xt = X_vec(m, ls_all - x).astype(float)
            if x == 0.0:
                if np.any((Mf * pt > K / (1 - eta)) & (Xt < (1 - eta) * Mf * pt)):          # (V2)
                    R.good_event = False
            elif np.any((Xt >= K) & (Xt > (1 + eta) * Mf * pt)):                            # (V3)
                R.good_event = False

    def X(m: int, ls: float) -> int:
        return int(X_vec(m, np.array([ls]))[0])

    # ---- claims of Theorem 11.56 --------------------------------------------------------------------------------
    v = R.violations
    closed = R.status.startswith("closed")
    if closed:
        R.width = R.lU - R.lL
        if R.width > C.x_out + 1e-9:
            v.append("width")                                # holds whenever the algorithm stops through the closure test
        if R.lL > R.lU:                                      # possible off the good event only: return the trivial bracket (R8, m1)
            R.lL, R.lU = ls0, ls0 + 2 * u * n
            R.trivial_returned = True
        R.valid = R.lL <= lA + 1e-9 and lA <= R.lU + 1e-9
    if R.good_event:
        if not closed and not R.status.startswith("skipped"):
            v.append("(i) " + R.status)
        if closed and not R.valid:
            v.append("(ii) invalid bracket")
        for (j, kind, m, N, lq, lpbar, lell_in, lMneg) in records:
            lsj = ls0 + lam * j
            if lp_gt(lsj) > lq + 1e-9:
                v.append("(ii) q_j below p(s_j)")
            if kind in (0, 2) and lpbar > lp_gt(lsj - b) + 1e-9:
                v.append("(ii) pbar_j above p(s_j e^-b)")
            if lell_in > lA + 1e-9:
                v.append("(ii) ell above A")
    for (j, kind, m, N, lq, lpbar, lell_in, lMneg) in records:   # (iii), (iv): every run
        lM = lK + m * LN2
        if kind in (0, 1) and lq <= C.lpi_dag + 1e-12:
            v.append("(iii) level left with q_j <= pi_dagger")
        if lM > max(lK, LN2 + lMneg) + 1e-9 or lM > lM_bar + 1e-9:
            v.append("(iv) sample size")
        if R.good_event and lMneg > lMneg_cap + 1e-9:
            v.append("(iv) M_neg")
        if R.good_event and n_i > 0:
            lsj = ls0 + lam * j
            for l in range(L):
                x = xs[l]
                if lMneg + lp_gt(lsj - x) > lcount_factor + x + 1e-9:
                    v.append("(v) count")
                if X(m, lsj - x) > max(K, math.exp(min(700.0, lcnt_const + x))):
                    v.append("(v) sampled count")
    if R.good_event and lC is not None and R.lqueries > lCmax + 1e-9:
        v.append("(vi) queries above C_max")
    R.violations = sorted(set(v))
    return R
