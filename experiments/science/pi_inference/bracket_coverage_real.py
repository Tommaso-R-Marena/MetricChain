#!/usr/bin/env python3
"""Benchmark B10, the baseline that had not been run: how often are error bars wrong? -- coordinator's script.

On the enumerated rotamer instances of workstream P2 (the 45 with a full product domain: Val, Leu, Ser
homopeptides, three backbones; ff14SB vacuum energy f, GBn2 term gb; g = f + gb; 300 K), for the three
surrogates of surrogate_divergence_real.py (m0 = f; m1 = f + one-body fit of gb; m2 = f + pairwise fit of gb),
the exact law of the remainder r = beta (g - m) under pi_m is known.  Target: ln mu, mu = E_{pi_m} e^{-r}
(= ln Z(g) - ln Z(m)).  From N exact samples of pi_m, four brackets for ln mu at confidence 1 - delta:

  naive      mu_hat +- 2 standard errors of the reweighting estimator (the usual uncertified error bar)
  EB         the empirical-Bernstein bracket (Maurer-Pontil; Liu-Fisher-Ihler 2015, Corollary 3.2) for the
             variable X = e^{-(r - lo)} in [0, 1], lo = min r the TRUE floor: certified given the floor
  H3         first-order perturbation theory with Hoeffding's Theorem 3 (addendum A17 (7)):
               -rbar - eta <= ln mu <= -rbar + eta + W(rbar + eta - lo, s2),   eta = sqrt(s2/(N delta)),
             with the TRUE floor lo and the TRUE variance s2 of r: certified given both
  H3-sampled the same formula with the SAMPLED minimum and the SAMPLED variance in place of the true ones
             (what one is tempted to do): not certified

Reported per row: coverage (fraction of repetitions in which the bracket contains the exact ln mu) and the median
width, with D_2(pi_g || pi_m) -- the quantity that, according to the theory, decides whether the naive bar fails.

Run:  python3 bracket_coverage_real.py > bracket_coverage_real.log      (about ten minutes)
"""
import os, sys, math, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_P2"))
import anlib

BETA = anlib.BETA
DELTA = 0.05
NS = (200, 2000, 20000)
REPS = 400
rng = np.random.default_rng(20261126)


def W_sharp(b, s2):
    b = np.asarray(b, dtype=float); s2 = np.asarray(s2, dtype=float)
    out = np.zeros(np.broadcast(b, s2).shape)
    ok = (b > 1e-12) & (s2 > 1e-300)
    bb = np.where(ok, b, 1.0); ss = np.where(ok, s2, 1.0)
    big = bb > 700.0
    safe = np.where(big, 1.0, bb)
    val = np.log1p((safe * safe * np.expm1(-ss / safe) + ss * np.expm1(safe)) / (safe * safe + ss))
    val = np.where(big, bb + np.log(ss / (bb * bb + ss)), val)
    return np.where(ok, val, 0.0)


def gibbs(E):
    w = np.exp(-BETA * (E - E.min())); return w / w.sum()


def analyse(tag):
    d = anlib.load_fb(tag)
    f = d["tors"] + d["lj"] + d["coul"]; gb = d["gb"]; g = f + gb
    pg = gibbs(g)
    rows = []
    for name, fit in (("m0", np.zeros_like(gb)), ("m1", anlib.anova_fit(gb, 1)), ("m2", anlib.anova_fit(gb, 2))):
        m = f + fit
        pm = gibbs(m).ravel()
        r = (BETA * (g - m)).ravel()
        lo = float(r.min())
        mu = float(np.sum(pm * np.exp(-(r - lo)))) * math.exp(-lo) if lo > -700 else float("nan")
        # work with the shifted variable to avoid overflow: X = e^{-(r-lo)} in (0,1], ln mu = -lo + ln E X
        X = np.exp(-(r - lo))
        EX = float(np.sum(pm * X)); lnmu = -lo + math.log(EX)
        Er = float(np.sum(pm * r)); s2 = float(np.sum(pm * (r - Er) ** 2))
        D2 = float(np.log(np.sum(pm * X * X)) - 2 * math.log(EX))
        cdf = np.cumsum(pm); cdf[-1] = 1.0
        res = dict(tag=tag, seq=d["seq"], bb=d["bb"], n=d["n"], surrogate=name, D2=D2, floor_b=Er - lo, sd=math.sqrt(s2), K=lnmu + Er)
        for N in NS:
            cov = dict(naive=0, EB=0, H3=0, H3s=0); wid = dict(naive=[], EB=[], H3=[], H3s=[])
            for start in range(0, REPS, 50):
                R = min(50, REPS - start)
                idx = np.searchsorted(cdf, rng.random((R, N)), side="right")
                idx = np.minimum(idx, len(cdf) - 1)
                rs = r[idx]; xs = X[idx]
                xm = xs.mean(axis=1); xv = xs.var(axis=1, ddof=1)
                # naive: two standard errors
                se = np.sqrt(xv / N)
                lo_n = np.where(xm - 2 * se > 0, np.log(np.maximum(xm - 2 * se, 1e-300)), -np.inf) - lo
                hi_n = np.log(xm + 2 * se) - lo
                # empirical Bernstein, two-sided (delta/2 each side), X in [0,1]
                L = math.log(4.0 / DELTA)
                dlt = np.sqrt(2 * xv * L / N) + 7 * L / (3 * (N - 1))
                lo_e = np.where(xm - dlt > 0, np.log(np.maximum(xm - dlt, 1e-300)), -np.inf) - lo
                hi_e = np.log(np.minimum(xm + dlt, 1.0)) - lo
                # Hoeffding's Theorem 3 with the true floor and variance
                rbar = rs.mean(axis=1)
                eta = math.sqrt(s2 / (N * DELTA))
                lo_h = -rbar - eta
                hi_h = -rbar + eta + W_sharp(np.maximum(rbar + eta - lo, 0.0), s2)
                # the same with the sampled minimum and the sampled variance
                s2s = rs.var(axis=1, ddof=1); los = rs.min(axis=1)
                etas = np.sqrt(s2s / (N * DELTA))
                lo_s = -rbar - etas
                hi_s = -rbar + etas + W_sharp(np.maximum(rbar + etas - los, 0.0), s2s)
                tol = 1e-12
                for key, a, b in (("naive", lo_n, hi_n), ("EB", lo_e, hi_e), ("H3", lo_h, hi_h), ("H3s", lo_s, hi_s)):
                    cov[key] += int(np.sum((a <= lnmu + tol) & (lnmu <= b + tol)))
                    wid[key].extend(np.where(np.isfinite(b - a), b - a, np.inf).tolist())
            for key in cov:
                res[f"cov_{key}_{N}"] = cov[key] / REPS
                res[f"wid_{key}_{N}"] = float(np.median(wid[key]))
        rows.append(res)
    return rows


if __name__ == "__main__":
    t0 = time.time()
    tags = []
    for aa, ns in (("V", (2, 4, 6, 8, 10, 12)), ("L", (2, 4, 6, 8)), ("S", (2, 3, 4, 5, 6))):
        for bb in ("E", "P2", "H"):
            for n in ns:
                t = f"fb_{aa}{n}_{bb}_R3_t0.60"                  # the tags of surrogate_divergence_real.py
                if os.path.exists(os.path.join(HERE, "..", "ws_P2", "data", t + ".npz")):
                    tags.append(t)
    assert len(tags) == 45, len(tags)                            # the 45 product-domain instances of A17 (6)
    allrows = []
    for tag in tags:
        rows = analyse(tag)
        for q in rows:
            q["tag"] = q["seq"][:1] + str(q["n"]) + "_" + q["bb"]
        allrows.extend(rows)
    print(f"# {len(allrows)} rows ({len(allrows)//3} instances x 3 surrogates); delta = {DELTA}; {REPS} repetitions per row and sample size; exact sampling from the enumerated law; {time.time()-t0:.0f} s")
    print("# coverage must be >= 0.95 for EB and H3 (certified, given the true floor / the true floor and variance), up to the simulation error "
          f"{3*math.sqrt(DELTA*(1-DELTA)/REPS):.3f}; naive and H3-sampled carry no guarantee")
    hdr = f"{'instance':10s} {'surr':4s} {'D2':>9s} {'floor b':>8s} {'sd r':>8s} {'gap K':>9s} | " + " | ".join(
        f"N={N}: cov naive / EB / H3 / H3-sampled; width EB / H3" for N in NS)
    print(hdr)
    for q in allrows:
        line = f"{q['tag']:10s} {q['surrogate']:4s} {q['D2']:9.2e} {q['floor_b']:8.3f} {q['sd']:8.4f} {q['K']:9.2e} | "
        line += " | ".join(
            f"{q[f'cov_naive_{N}']:.3f} / {q[f'cov_EB_{N}']:.3f} / {q[f'cov_H3_{N}']:.3f} / {q[f'cov_H3s_{N}']:.3f}; {q[f'wid_EB_{N}']:.3g} / {q[f'wid_H3_{N}']:.3g}"
            for N in NS)
        print(line)
    # summary by class of D2
    print("# summary: smallest coverage over the rows in each class of D2 (and the number of rows)")
    bins = [(0, 1e-3), (1e-3, 0.1), (0.1, 1.0), (1.0, 5.0), (5.0, 1e9)]
    for lo_, hi_ in bins:
        sel = [q for q in allrows if lo_ <= q["D2"] < hi_]
        if not sel:
            continue
        parts = []
        for N in NS:
            parts.append(f"N={N}: naive {min(q[f'cov_naive_{N}'] for q in sel):.3f}, EB {min(q[f'cov_EB_{N}'] for q in sel):.3f}, "
                         f"H3 {min(q[f'cov_H3_{N}'] for q in sel):.3f}, H3-sampled {min(q[f'cov_H3s_{N}'] for q in sel):.3f}")
        print(f"   D2 in [{lo_:g}, {hi_:g}): {len(sel):3d} rows | " + " | ".join(parts))
    worst_cert = min(min(q[f"cov_EB_{N}"] for N in NS) for q in allrows), min(min(q[f"cov_H3_{N}"] for N in NS) for q in allrows)
    print(f"# smallest coverage of the certified brackets over all rows and sample sizes: EB {worst_cert[0]:.3f}, H3 {worst_cert[1]:.3f}")
    json.dump(allrows, open(os.path.join(HERE, "bracket_coverage_real.json"), "w"), indent=1)
    assert worst_cert[0] >= 1 - DELTA - 3 * math.sqrt(DELTA * (1 - DELTA) / REPS)
    assert worst_cert[1] >= 1 - DELTA - 3 * math.sqrt(DELTA * (1 - DELTA) / REPS)
    print(f"ALL OK ({time.time()-t0:.0f} s)")
