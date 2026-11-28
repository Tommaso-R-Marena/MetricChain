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

__all__ = ["LRRegion", "lr_confidence_region", "asymptotic_interval", "bootstrap_interval",
           "make_batches", "kl_interval", "observable_interval", "classifier_evalue"]


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
    status: str = "OK"            # OK | ABSTAIN_SUPPORT | ABSTAIN_NO_DATA | REJECT_MODEL
    meta: dict = field(default_factory=dict)

    def __post_init__(self):
        self.N, self.K = self.A.shape if self.A.size else (0, 0)
        if self.status == "OK":
            self.t0 = np.bincount(self.labels, minlength=self.K) / self.N
            self.fhat, v, info = minimize_lse(self.A, self.t0)
            self.phi_min = self.N * v
            if not info["converged"]:
                self.status = "ABSTAIN_SUPPORT"
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
        f, v, info = minimize_lse(self.A, self.t0, f0=f0, constraint=(c, theta))
        return self.N * v, f

    def interval(self, c, xtol=1e-6):
        """[inf, sup] of c.f over the region; (-inf, inf) when the certificate abstains."""
        c = np.asarray(c, float)
        if self.status != "OK":
            return (-np.inf, np.inf) if self.status != "REJECT_MODEL" else (np.nan, np.nan)
        th = float(c @ self.fhat)
        Jm = np.full((self.K, self.K), 1.0 / self.K)
        Rc = float(c @ (np.linalg.inv(self.H + Jm) - Jm) @ c)
        d0 = np.sqrt(max(2 * (self.level - self.phi_min) * Rc, 1e-300))
        ends = []
        for sgn in (-1.0, 1.0):
            lo_t, f_lo = 0.0, self.fhat
            step, hi_t, f_hi = d0, None, None
            for _ in range(80):
                val, fx = self._profile(c, th + sgn * step, f_lo)
                if val > self.level:
                    hi_t, f_hi = step, fx
                    break
                lo_t, f_lo = step, fx
                step *= 1.7
            if hi_t is None:
                ends.append(sgn * np.inf)
                continue
            cache = {"f": f_lo}

            def gap(t):
                val, fx = self._profile(c, th + sgn * t, cache["f"])
                return val - self.level

            root = brentq(gap, lo_t, hi_t, xtol=xtol * max(1.0, d0), rtol=1e-10)
            ends.append(th + sgn * (root + xtol * max(1.0, d0)))     # outward by the tolerance
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


def lr_confidence_region(U, labels, alpha=0.05, n_batches=8, skip=1, rng=None, plugin=None):
    """Prequential likelihood-ratio region (Theorem B2).  Batches follow the sample order within
    each state (pass rng to permute).  Batch b >= skip is evaluated against the MBAR fit of batches
    < b (or against plugin(b, U_prev, labels_prev) if given); a batch whose plug-in cannot be
    computed is left out (its e-value is 1), which keeps the statement valid."""
    U, labels, K = _validate(U, labels)
    if not 0 < alpha < 1:
        raise ValueError("alpha")
    batches = make_batches(labels, n_batches, rng)
    rowsA, rowsy, ref, used, skipped = [], [], 0.0, [], []
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
        val = float(np.sum(logsumexp(Ab + fb, axis=1) - fb[labels[cur]]))
        if not np.isfinite(val):          # the plug-in gives probability zero to an observed label
            skipped.append(b)
            continue
        ref += val
        rowsA.append(Ab)
        rowsy.append(labels[cur])
        used.append(b)
    meta = dict(n_batches=n_batches, used=used, skipped=skipped, reference=ref)
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
    return max(0.0, lo * (1 - 1e-12)), min(1.0, hi * (1 + 1e-12))


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
            rowsA.append(np.log(nb / nb.sum())[None, :] - U[cur])
        rowsy.append(labels[cur])
    A, y = np.vstack(rowsA), np.concatenate(rowsy)
    t0 = np.bincount(y, minlength=K) / len(y)
    fh, v, info = minimize_lse(A, t0)
    return len(y) * v - loss, dict(mbar_loss=len(y) * v, classifier_loss=loss, converged=info["converged"])
