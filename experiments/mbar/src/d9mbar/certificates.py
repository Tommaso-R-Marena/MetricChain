"""Finite-sample confidence certificates for multistate free energies.  Division 9; float64
(the probability statements are proved for exact arithmetic and independent equilibrium samples).

Main object: the likelihood-ratio e-process region (docs/mbar/MATHEMATICS.md, Theorems B1-B3)

    C = { f :  sum_{b in E} Phi_b(f)  <=  log(1/alpha) + sum_{b in E} Phi_b(f'_b) },
    Phi_b(f) = sum_{n in batch b} [ LSE_j( log beta_{b,j} + f_j - U[n, j] ) - f_{y_n} ],

beta_b = the state proportions of batch b (fixed before the batch is looked at), f'_b = any estimate
computed from earlier batches only.  Under independent equilibrium sampling P(f* not in C) <= alpha
at every sample size, for every K, with no bound on the energies, simultaneously for all contrasts;
C is a sublevel set of a convex function, so the interval of a contrast is two convex programmes.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import brentq
from scipy.special import logsumexp
from scipy.stats import norm

from .estimators import (_validate, fitted_distributions, mbar, minimize_lse, plugin_variance,
                         support_strongly_connected)

__all__ = ["LRRegion", "lr_confidence_region", "restricted_interval", "asymptotic_interval", "bootstrap_interval",
           "make_batches", "kl_interval", "observable_interval", "pmf_difference_interval",
           "classifier_evalue"]


def make_batches(labels, n_batches, rng=None):
    """Batch b = the b-th chunk of every state's samples (in the given order, or permuted within
    states if rng is given).  The composition of every batch is fixed by counts alone."""
    labels = np.asarray(labels, int)
    K = labels.max() + 1
    out = [[] for _ in range(n_batches)]
    for k in range(K):
        idx = np.where(labels == k)[0]
        if rng is not None:
            idx = rng.permutation(idx)
        for b, chunk in enumerate(np.array_split(idx, n_batches)):
            out[b].append(chunk)
    return [np.sort(np.concatenate(c)) for c in out]


@dataclass
class LRRegion:
    A: np.ndarray                 # per-sample logits offset: log beta_{b(n), j} - U[n, j]
    labels: np.ndarray
    level: float                  # Phi(f) <= level
    alpha: float
    status: str = "OK"   # OK | ABSTAIN_SUPPORT | ABSTAIN_NO_DATA | ABSTAIN_PLUGIN | ABSTAIN_NUMERICS | REJECT_MODEL
    meta: dict = field(default_factory=dict)

    def __post_init__(self):
        self.N, self.K = self.A.shape
        if self.status == "OK":
            self.t0 = np.bincount(self.labels, minlength=self.K) / self.N
            self.fhat, v, info = minimize_lse(self.A, self.t0, f0=self.meta.get("start"))
            self.phi_min = self.N * v
            self.meta["fit"] = dict(grad=info["grad"], step=info["step"], iterations=info["iterations"])
            if not info["converged"]:
                # the minimum is not verified: neither an interval nor a rejection is issued
                self.status = "ABSTAIN_NUMERICS"
            elif self.phi_min > self.level:
                self.status = "REJECT_MODEL"       # no f is compatible: evidence against the model
            else:
                Z = self.A + self.fhat
                p = np.exp(Z - logsumexp(Z, axis=1)[:, None])
                self.H = self.N * (np.diag(p.mean(axis=0)) - p.T @ p / self.N)

    def phi(self, f):
        f = np.asarray(f, float)
        return float(np.sum(logsumexp(self.A + f, axis=1) - f[self.labels]))

    def contains(self, f):
        return self.status == "OK" and self.phi(f) <= self.level

    def _profile(self, c, theta, f0):
        """min of Phi over {c.f = theta}.  Returns (value, f, ok).  The computed value of an
        unconverged solve is an UPPER bound of the true minimum and would make the interval too
        narrow; such a point is therefore reported with ok = False and treated as inside the region."""
        f, v, info = minimize_lse(self.A, self.t0, f0=f0, constraint=(c, theta))
        if not info["converged"]:
            f, v, info = minimize_lse(self.A, self.t0, f0=self.fhat, constraint=(c, theta), maxit=500)
        return self.N * v, f, bool(info["converged"])

    def interval(self, c, xtol=1e-6):
        """[inf, sup] of c.f over the region; (-inf, inf) when the certificate abstains.
        If the region is empty (status REJECT_MODEL) the answer is (nan, nan): under the model this
        event has probability at most alpha and is part of the non-coverage budget -- it is a
        rejection of the model, not an interval."""
        c = np.asarray(c, float)
        if c.shape != (self.K,) or abs(c.sum()) > 1e-9 * max(1.0, np.abs(c).max()):
            raise ValueError("a contrast must have one entry per state and sum to zero")
        if self.status != "OK":
            return (-np.inf, np.inf) if self.status != "REJECT_MODEL" else (np.nan, np.nan)
        th = float(c @ self.fhat)
        Jm = np.full((self.K, self.K), 1.0 / self.K)
        try:
            Rc = float(c @ (np.linalg.inv(self.H + Jm) - Jm) @ c)
        except np.linalg.LinAlgError:
            Rc = np.nan
        if not np.isfinite(Rc) or Rc <= 0:               # ill-conditioned curvature: start from a unit step
            Rc = 1.0 / max(2 * (self.level - self.phi_min), 1e-12)
        d0 = np.sqrt(max(2 * (self.level - self.phi_min) * Rc, 1e-300))
        ends = []
        for sgn in (-1.0, 1.0):
            lo_t, f_lo = 0.0, self.fhat
            step, hi_t, f_hi = d0, None, None
            for _ in range(80):
                val, fx, ok = self._profile(c, th + sgn * step, f_lo)
                if ok and val > self.level:
                    hi_t, f_hi = step, fx
                    break
                lo_t = step
                if ok:
                    f_lo = fx
                step *= 1.7
            if hi_t is None:
                ends.append(sgn * np.inf)
                continue
            cache = {"f": f_lo}

            def gap(t):
                val, fx, ok = self._profile(c, th + sgn * t, cache["f"])
                return val - self.level if ok else -1.0      # unconverged: count the point as inside

            root = brentq(gap, lo_t, hi_t, xtol=xtol * max(1.0, d0), rtol=1e-10)
            # outward by more than the root finder's own tolerance (absolute + relative)
            ends.append(th + sgn * (root + 2 * xtol * max(1.0, d0) + 4e-10 * abs(root)))
        return ends[0], ends[1]

    def pair_matrix(self):
        """lower[i, j], upper[i, j] for f_j - f_i over all pairs."""
        lo = np.zeros((self.K, self.K))
        hi = np.zeros((self.K, self.K))
        for i in range(self.K):
            for j in range(i + 1, self.K):
                c = np.zeros(self.K)
                c[i], c[j] = -1.0, 1.0
                a, b = self.interval(c)
                lo[i, j], hi[i, j] = a, b
                lo[j, i], hi[j, i] = -b, -a
        return lo, hi


def lr_confidence_region(U, labels, alpha=0.05, n_batches=8, skip=1, rng=None, plugin=None,
                         batches=None):
    """Prequential likelihood-ratio region (Theorem B2).  Batches follow the sample order within
    each state (pass rng to permute).  Batch b >= skip is evaluated against the MBAR fit of batches
    < b (or against plugin(b, U_prev, labels_prev) if given); a batch whose plug-in cannot be
    computed is left out (its e-value is 1), which keeps the statement valid.

    `batches`: optional explicit list of index arrays (rounds of an adaptive simulation, in time
    order).  The composition of a round may depend on earlier rounds (adaptive allocation) but must
    be fixed before the round is sampled; the statement then holds simultaneously at every round
    (Theorem B3), so the region may be recomputed after each round and sampling may halt at will."""
    U, labels, K = _validate(U, labels)
    if not 0 < alpha < 1:
        raise ValueError("alpha")
    if batches is None:
        batches = make_batches(labels, n_batches, rng)
    else:
        batches = [np.asarray(b, int) for b in batches]
        n_batches = len(batches)
        allidx = np.concatenate(batches) if batches else np.zeros(0, int)
        if len(np.unique(allidx)) != len(allidx):
            # e.g. cumulative prefixes "the data so far" passed as rounds: the plug-in of a round would
            # then have been fitted on samples of that round (REVIEW_A.md, G4: coverage 0.90 at 0.95)
            raise ValueError("batches must be disjoint index sets (rounds), not cumulative prefixes")
    rowsA, rowsy, ref, used, skipped, last_plugin = [], [], 0.0, [], [], None
    for b in range(skip, n_batches):
        prev = np.concatenate(batches[:b])
        cur = batches[b]
        nb = np.bincount(labels[cur], minlength=K)
        if len(cur) == 0 or len(prev) == 0:
            skipped.append(b)
            continue
        try:
            fb = plugin(b, U[prev], labels[prev]) if plugin is not None else mbar(U[prev], labels[prev])[0]
        except (ValueError, RuntimeError, np.linalg.LinAlgError):
            skipped.append(b)
            continue
        with np.errstate(divide="ignore"):
            Ab = np.log(nb / nb.sum())[None, :] - U[cur]
        # Rows are centred on the logit of the sample's own state: Phi_b is then exactly the negative
        # log-likelihood sum_n -log pi_{y_n}(f; x_n), free of large common energies (the centring
        # constant is the same on both sides of the region's inequality).
        Ab = Ab - Ab[np.arange(len(cur)), labels[cur]][:, None]
        fb_use = np.where(np.isfinite(Ab).any(axis=0), fb, 0.0)     # states absent from this batch do not enter
        val = float(np.sum(logsumexp(Ab + fb_use, axis=1) - fb_use[labels[cur]]))
        if not np.isfinite(val):
            # The plug-in gives probability zero to an observed label of THIS batch: the e-value
            # of the batch is 0.  Dropping the batch here would be a decision taken on its own data
            # and is not licensed by Theorem B2; the valid reading is that nothing can be excluded.
            return LRRegion(np.zeros((0, K)), np.zeros(0, int), np.inf, alpha, "ABSTAIN_PLUGIN",
                            dict(n_batches=n_batches, used=used, skipped=skipped, failed_batch=b))
        ref += val
        last_plugin = fb_use
        rowsA.append(Ab)
        rowsy.append(labels[cur])
        used.append(b)
    meta = dict(n_batches=n_batches, used=used, skipped=skipped, reference=ref, start=last_plugin)
    if not used:
        return LRRegion(np.zeros((0, K)), np.zeros(0, int), np.inf, alpha, "ABSTAIN_NO_DATA", meta)
    A = np.vstack(rowsA)
    y = np.concatenate(rowsy)
    if len(np.unique(y)) < K or not support_strongly_connected(-A, y):
        return LRRegion(A, y, np.inf, alpha, "ABSTAIN_SUPPORT", meta)
    reg = LRRegion(A, y, np.log(1 / alpha) + ref, alpha, "OK", meta)
    if reg.status == "OK":
        reg.meta["regret"] = ref - reg.phi_min     # threshold above the minimum, minus log(1/alpha)
    return reg


def restricted_interval(U, labels, c, states, alpha=0.05, **kwargs):
    """Interval for a contrast supported on `states`, from the sub-experiment that keeps only the
    samples and the energy columns of those states (Proposition B2': the sub-experiment is a
    multistate experiment of the same kind, so Theorem B2 applies to it with |states| - 1 nuisance
    directions instead of K - 1).  `states` must be chosen without looking at the samples (by the
    design of the ladder), or the levels of several candidate sets must be added up.
    Returns (lo, hi, region)."""
    U, labels, K = _validate(U, labels)
    states = np.asarray(sorted(set(int(k) for k in states)), int)
    c = np.asarray(c, float)
    if np.any(np.abs(np.delete(c, states)) > 0):
        raise ValueError("the contrast must be supported on the retained states")
    keep = np.isin(labels, states)
    relabel = -np.ones(K, int)
    relabel[states] = np.arange(len(states))
    reg = lr_confidence_region(U[keep][:, states], relabel[labels[keep]], alpha=alpha, **kwargs)
    lo, hi = reg.interval(c[states])
    return lo, hi, reg


def asymptotic_interval(U, labels, c, alpha=0.05):
    """Standard practice: estimate +- z * sqrt(plug-in asymptotic variance).  No finite-sample guarantee."""
    f, _ = mbar(U, labels)
    v = plugin_variance(U, labels, c, f=f)
    half = norm.ppf(1 - alpha / 2) * np.sqrt(max(v, 0.0))
    est = float(np.asarray(c, float) @ f)
    return est - half, est + half


def bootstrap_interval(U, labels, c, alpha=0.05, B=200, rng=None):
    """Percentile bootstrap, resampling within states.  No finite-sample guarantee."""
    rng = rng or np.random.default_rng(0)
    U, labels, K = _validate(U, labels)
    idx = [np.where(labels == k)[0] for k in range(K)]
    c = np.asarray(c, float)
    vals = []
    for _ in range(B):
        take = np.concatenate([rng.choice(i, size=len(i), replace=True) for i in idx])
        try:
            vals.append(c @ mbar(U[take], labels[take])[0])
        except (ValueError, RuntimeError):
            continue
    if len(vals) < B // 2:
        return -np.inf, np.inf
    return float(np.quantile(vals, alpha / 2)), float(np.quantile(vals, 1 - alpha / 2))


def kl_interval(y, n, t):
    """{mu in [0,1] : n kl(y || mu) <= t}: Chernoff interval for a mean of n independent [0,1]
    variables with average expectation mu; failure probability <= 2 exp(-t)."""
    if not (0 <= y <= 1 and n > 0 and t > 0):
        raise ValueError("bad arguments")

    def kl(p, q):
        out = 0.0
        if p > 0:
            out += p * np.log(p / q)
        if p < 1:
            out += (1 - p) * np.log((1 - p) / (1 - q))
        return out

    z = t / n
    lo = 0.0 if y == 0 else brentq(lambda q: kl(y, q) - z, 1e-300, y) if kl(y, 1e-300) > z else 0.0
    hi = 1.0 if y == 1 else brentq(lambda q: kl(y, q) - z, y, 1 - 1e-16) if kl(y, 1 - 1e-16) > z else 1.0
    # outward by more than brentq's default tolerance (absolute 2e-12, relative 8.9e-16)
    return max(0.0, lo * (1 - 1e-9) - 1e-11), min(1.0, hi * (1 + 1e-9) + 1e-11)


def observable_interval(region, U, labels, k, A01, alpha_obs=0.025):
    """Interval for E_k[A], A in [0,1], k a sampled state (handoff G2 with the region of this module
    in place of C1): failure probability <= region.alpha + alpha_obs.

    y(f) = N^-1 sum_n pi_k(f; x_n) A(x_n) has mean s_k E_k[A] at f*, and y(f*)/y(f0) lies in
    [e^-r, e^r] for r = sup_{f in C} osc(f - f0)."""
    U, labels, K = _validate(U, labels)
    A01 = np.asarray(A01, float)
    if A01.min() < 0 or A01.max() > 1:
        raise ValueError("observable must take values in [0, 1]")
    if region.status != "OK":
        return 0.0, 1.0
    n = np.bincount(labels, minlength=K)
    N = n.sum()
    f0, _ = mbar(U, labels)
    lo, hi = region.pair_matrix()
    d0 = f0[None, :] - f0[:, None]
    r = float(max(np.max(hi - d0), np.max(d0 - lo)))
    if not np.isfinite(r):
        return 0.0, 1.0
    Z = np.log(n / N)[None, :] + f0[None, :] - U
    pk = np.exp(Z[:, k] - logsumexp(Z, axis=1))
    y0 = float(np.mean(pk * A01))
    t = np.log(2 / alpha_obs)
    l = kl_interval(min(1.0, np.exp(-r) * y0), N, t)[0]
    u = kl_interval(min(1.0, np.exp(r) * y0), N, t)[1]
    sk = n[k] / N
    return max(0.0, l / sk), min(1.0, u / sk)


def pmf_difference_interval(region, U, labels, k, in_A, in_B, alpha_obs=0.025):
    """Interval for the free-energy difference F_B - F_A = -log(P_k(B)/P_k(A)) between two bins of a
    sampled state k (handoff G2, last paragraph): the two bin probabilities get intervals at level
    alpha_obs/2 each, so the failure probability is <= region.alpha + alpha_obs.  An endpoint is
    infinite when a lower endpoint of a probability is 0 (no finite statement is invented)."""
    lA, uA = observable_interval(region, U, labels, k, np.asarray(in_A, float), alpha_obs / 2)
    lB, uB = observable_interval(region, U, labels, k, np.asarray(in_B, float), alpha_obs / 2)
    lo = np.log(lA) - np.log(uB) if lA > 0 and uB > 0 else -np.inf
    hi = np.log(uA) - np.log(lB) if lB > 0 and uA > 0 else np.inf
    return float(lo), float(hi)


def classifier_evalue(U, labels, prob, n_batches=8, skip=1):
    """Log e-value of the model check (Theorem B5): a label predictor trained on earlier batches
    against the best MBAR classifier in hindsight,

        log E = min_f sum_b sum_n log[ lambda_b,y_n(x_n) / pi^{beta_b}_{y_n}(f; x_n) ]
              = Phi_min - sum_n (-log lambda)          (it is <= the value at the true f).

    Under independent equilibrium sampling P(log E >= log(1/alpha)) <= alpha, whatever the
    predictors.  `prob(b, prev_index, cur_index)` returns an array (len(cur), K) of predicted label
    probabilities for the samples of batch b, using only earlier batches for training."""
    U, labels, K = _validate(U, labels)
    batches = make_batches(labels, n_batches)
    rowsA, rowsy, loss = [], [], 0.0
    for b in range(skip, n_batches):
        prev, cur = np.concatenate(batches[:b]), batches[b]
        nb = np.bincount(labels[cur], minlength=K)
        lam = np.asarray(prob(b, prev, cur), float)
        lam = lam / lam.sum(axis=1, keepdims=True)
        loss += float(-np.sum(np.log(lam[np.arange(len(cur)), labels[cur]])))
        with np.errstate(divide="ignore"):
            Ab = np.log(nb / nb.sum())[None, :] - U[cur]
        rowsA.append(Ab - Ab[np.arange(len(cur)), labels[cur]][:, None])     # own-state logit = 0
        rowsy.append(labels[cur])
    A, y = np.vstack(rowsA), np.concatenate(rowsy)
    t0 = np.bincount(y, minlength=K) / len(y)
    fh, v, info = minimize_lse(A, t0)
    # with centred rows, LSE_j(A_j + f_j) - f_y = -log pi_y(f; x): N * v is the best MBAR log-loss
    # in hindsight.  If that minimisation is not verified the statistic is not defined: no rejection.
    mbar_loss = len(y) * v
    if not info["converged"]:
        return -np.inf, dict(mbar_loss=np.nan, classifier_loss=loss, converged=False)
    return mbar_loss - loss, dict(mbar_loss=mbar_loss, classifier_loss=loss, converged=True)
