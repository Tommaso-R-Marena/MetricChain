"""N4 + N8 — Bayesian certificates on the cube with non-adaptive linear designs.

N4.  Prior: isotropic ANOVA spectrum, sigma_m^2 = n*s_m for m = 1,2,3.  Known part f = e|x|.
     Designs: dual BCH codes, m = 1 (learn main effects) and m = 2 (main effects + pairs).
     For R prior draws: posterior mean (coset formula), then
       ln Z :  analytic interval of Theorem C
                 [ lnZ(f+ghat) - beta s z ,  lnZ(f+ghat) + a + beta s z ],  z = sqrt(2 ln(2/delta)),
                 s = max_x P_A(x),  a = ln E_pihat exp(beta^2 P_A^2 / 2);
               sampled interval: (delta/2, 1-delta/2) quantiles of posterior samples (Matheron).
       min  :  analytic interval [ min_x (f+ghat - zX P_A),  (f+g)(xhat) ],  zX = sqrt(2 ln(|X|/delta));
               sampled interval as above.
     Reported: coverage and mean width.

N8.  REM tail: prior = main effects (n*s1) + white noise of variance tw2 at every configuration.
     Design m = 1 only.  The white part cannot be learned.  Second-moment certificate of
     Theorem C(iv):  ln Z = lnZ(f+ghat) + a + ln(1 +- eta),  eta = sqrt(rho2/delta),
        rho2 = E_{nu x nu} exp(beta^2 K_A(x,y)) - 1,   nu ~ pihat * exp(beta^2 P_A^2/2).
     Reported: coverage and width against beta (annealed vs frozen), and the true posterior
     spread of ln Z.

Run: OMP_NUM_THREADS=1 python3 n4_bayes.py
"""
import json
import math

import numpy as np

import cube as cb

DELTA = 0.05
rng = np.random.default_rng(424242)


class LinearPosterior:
    def __init__(self, v, rows, n):
        self.v, self.n, self.size = v, n, 1 << n
        self.syn = cb.syndromes(rows, n)
        self.ncos = 1 << len(rows)
        self.V = np.bincount(self.syn, weights=v, minlength=self.ncos)
        Vs = self.V[self.syn]
        self.ratio = np.where(Vs > 0, v / np.where(Vs > 0, Vs, 1.0), 0.0)
        self.N = len(cb.span(rows, n))
        self.kappa_T = None
        var = np.full(self.size, float(v.sum()))
        self._sT = []
        for T in range(self.ncos):
            if self.V[T] <= 0:
                continue
            sT = cb.fwht(np.where(self.syn == T, v, 0.0))
            var -= sT ** 2 / self.V[T]
            self._sT.append((sT, self.V[T]))
        self.var = np.maximum(var, 0.0)
        self.P = np.sqrt(self.var)

    def mean_from_ghat(self, ghat):
        G = np.bincount(self.syn, weights=ghat, minlength=self.ncos)
        return cb.fwht(self.ratio * G[self.syn])

    def sample_prior(self):
        ghat = rng.standard_normal(self.size) * np.sqrt(self.v)
        return ghat, cb.fwht(ghat)

    def posterior_residual(self):
        ghat, g = self.sample_prior()
        return g - self.mean_from_ghat(ghat)

    def full_cov(self):
        """K_A(x,y) = k(x xor y) - sum_T s_T(x) s_T(y)/V_T  (dense; only for n <= 12)."""
        kap = cb.fwht(self.v)
        idx = np.arange(self.size)
        K = kap[idx[:, None] ^ idx[None, :]]
        for sT, VT in self._sT:
            K -= np.outer(sT, sT) / VT
        return K


def n4():
    rows_out = []
    z = math.sqrt(2 * math.log(2 / DELTA))
    for n, e, s in [(7, 0.5, (0.04, 0.02, 0.0)), (7, 0.5, (0.04, 0.02, 0.004)),
                    (10, 0.5, (0.04, 0.02, 0.0)), (10, 0.5, (0.04, 0.02, 0.004)),
                    (12, 0.5, (0.04, 0.02, 0.004)), (15, 0.5, (0.04, 0.02, 0.004))]:
        size = 1 << n
        v = cb.iso_spectrum(n, [0.0] + [n * sj for sj in s])
        f = e * cb.weights(n).astype(float)
        zX = math.sqrt(2 * math.log(size / DELTA))
        for m in (1, 2):
            post = LinearPosterior(v, cb.bch_rows(n, m), n)
            smax = float(post.P.max())
            R = 300 if n <= 12 else 120
            RS = 400 if n <= 12 else 150
            # posterior residual samples (shared across draws: the posterior covariance does not
            # depend on the data)
            res = np.stack([post.posterior_residual() for _ in range(RS)])
            for beta in (0.5, 2.0):
                cov_a = cov_s = covm_a = covm_s = 0
                w_a, w_s, wm_a, wm_s = [], [], [], []
                for _ in range(R):
                    ghat, g = post.sample_prior()
                    mean = post.mean_from_ghat(ghat)
                    base = cb.logZ(f + mean, beta)
                    truth = cb.logZ(f + g, beta)
                    a0 = -beta * (f + mean)
                    pih = np.exp(a0 - a0.max())
                    pih /= pih.sum()
                    a = math.log(float(np.sum(pih * np.exp(beta ** 2 * post.var / 2))))
                    lo, hi = base - beta * smax * z, base + a + beta * smax * z
                    cov_a += lo - 1e-9 <= truth <= hi + 1e-9
                    w_a.append(hi - lo)
                    samp = np.array([cb.logZ(f + mean + r, beta) for r in res])
                    ql, qh = np.quantile(samp, [DELTA / 2, 1 - DELTA / 2])
                    cov_s += ql - 1e-9 <= truth <= qh + 1e-9
                    w_s.append(qh - ql)
                    if beta == 0.5:   # the minimum does not depend on beta: do it once
                        tm = float(np.min(f + g))
                        xhat = int(np.argmin(f + mean))
                        lo_m = float(np.min(f + mean - zX * post.P))
                        hi_m = float(f[xhat] + g[xhat])
                        covm_a += lo_m - 1e-12 <= tm <= hi_m + 1e-12
                        wm_a.append(hi_m - lo_m)
                        sm = np.min(f[None, :] + mean[None, :] + res, axis=1)
                        ql, qh = np.quantile(sm, [DELTA / 2, 1 - DELTA / 2])
                        covm_s += ql - 1e-12 <= tm <= qh + 1e-12
                        wm_s.append(qh - ql)
                rec = {"n": n, "s": s, "m": m, "N": post.N, "beta": beta, "sup_P": smax,
                       "tau_m": math.sqrt(float(v[cb.weights(n) > m].sum())),
                       "lnZ_cov_analytic": cov_a / R, "lnZ_width_analytic": float(np.mean(w_a)),
                       "lnZ_cov_sampled": cov_s / R, "lnZ_width_sampled": float(np.mean(w_s))}
                if beta == 0.5:
                    rec.update({"min_cov_analytic": covm_a / R, "min_width_analytic": float(np.mean(wm_a)),
                                "min_cov_sampled": covm_s / R, "min_width_sampled": float(np.mean(wm_s))})
                rows_out.append(rec)
                print(rec, flush=True)
    return rows_out


def n8():
    rows_out = []
    for n, tw2, m in [(10, 1.0, 1), (10, 1.0, 2), (12, 0.25, 2), (12, 1.0, 1), (12, 1.0, 2)]:
        size = 1 << n
        s1 = 0.04
        v = cb.iso_spectrum(n, [0.0, n * s1]) + tw2 / size       # main effects + white noise
        f = 0.5 * cb.weights(n).astype(float)
        post = LinearPosterior(v, cb.bch_rows(n, m), n)
        K = post.full_cov()
        res = np.stack([post.posterior_residual() for _ in range(100)])
        beta_c = math.sqrt(2 * n * math.log(2) / tw2)
        for beta in (0.5, 1.0, 2.0, 4.0):
            R = 100
            EK = np.expm1(beta ** 2 * K)                 # entrywise, once per (design, beta)
            cov2 = 0
            w2, spread, rho2s, h2s = [], [], [], []
            for _ in range(R):
                ghat, g = post.sample_prior()
                mean = post.mean_from_ghat(ghat)
                base = cb.logZ(f + mean, beta)
                truth = cb.logZ(f + g, beta)
                a0 = -beta * (f + mean)
                pih = np.exp(a0 - a0.max())
                pih /= pih.sum()
                wgt = pih * np.exp(beta ** 2 * post.var / 2)
                a = math.log(float(wgt.sum()))
                nu = wgt / wgt.sum()
                rho2 = float(nu @ (EK @ nu))             # = Var(W)/(E W)^2 given the data
                eta = math.sqrt(max(rho2, 0.0) / DELTA)
                if eta < 1:
                    lo, hi = base + a + math.log(1 - eta), base + a + math.log(1 + eta)
                    cov2 += lo <= truth <= hi
                    w2.append(hi - lo)
                else:
                    w2.append(math.inf)
                    cov2 += 1                                        # vacuous interval
                rho2s.append(rho2)
                h2s.append(-math.log(float(np.sum(nu ** 2))))
                samp = np.array([cb.logZ(f + mean + r, beta) for r in res])
                spread.append(float(np.quantile(samp, 1 - DELTA / 2) - np.quantile(samp, DELTA / 2)))
            del EK
            rec = {"n": n, "tw2": tw2, "m": m, "N": post.N, "beta": beta, "beta_c_REM": beta_c,
                   "beta2_tw2": beta ** 2 * tw2, "max_P2": float(post.var.max()),
                   "median_H2_nu": float(np.median(h2s)),
                   "median_rho2": float(np.median(rho2s)),
                   "frac_nonvacuous": float(np.mean(np.isfinite(w2))),
                   "second_moment_width_median": float(np.median(w2)),
                   "coverage": cov2 / R,
                   "true_posterior_95_spread_median": float(np.median(spread)),
                   "sup_norm_width": beta ** 2 * float(post.var.max()) / 2
                                     + 2 * beta * float(post.P.max()) * math.sqrt(2 * math.log(2 / DELTA))}
            rows_out.append(rec)
            print(rec, flush=True)
        del K
    return rows_out


if __name__ == "__main__":
    out = {"delta": DELTA}
    out["n4"] = n4()
    with open("n4_bayes.json", "w") as fh:
        json.dump(out, fh, indent=1)
    out["n8"] = n8()
    with open("n4_bayes.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("N4/N8 done")
