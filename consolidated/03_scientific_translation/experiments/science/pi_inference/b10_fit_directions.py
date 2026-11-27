#!/usr/bin/env python3
"""Benchmark B10, instance (i), the part that had not been run: WHICH DIVERGENCE DOES A FITTED SURROGATE CONTROL?
-- coordinator's script.

On the 45 enumerated product-domain rotamer instances of workstream P2 (Val, Leu, Ser homopeptides, three backbones;
g = ff14SB vacuum energy + GBn2; 300 K; pi_g the exact Gibbs law), two tractable families
    product   q(x) = prod_i q_i(x_i)                                   (independent residues)
    chain     q(x) proportional to exp(sum_i a_i(x_i) + sum_i b_i(x_i, x_{i+1}))    (nearest-neighbour chain)
are fitted to pi_g in five ways, all with exact sums over the enumerated grid (no sampling):
    LSu   least squares of beta*g under the uniform measure (ANOVA terms of the family) -- what the earlier runs used
    LSs   least squares under the surrogate's own measure (iterated weighted least squares; the fit named in B10)
    VAR   the variational principle: minimal KL(q || pi_g) within the family ("reverse" KL; mean field / Bogoliubov)
    ML    maximum likelihood: minimal KL(pi_g || q) (moment matching; closed form for both families)
    CHI   minimal D_2(pi_g || q) = ln sum pi_g^2/q -- the divergence that the cost of certified reweighting is
          exponential in (addendum A17)
For each fit: the root-mean-square remainder under the surrogate, sd_q(beta g - (-ln q)), the variational gap KL(q || pi_g),
KL(pi_g || q), D_2(pi_g || q), D_inf(pi_g || q) = ln max pi_g/q.

Prediction of the benchmark (refutable): the fits are close in the first two numbers and can differ by orders of
magnitude in exp(D_2) and exp(D_inf); the root-mean-square remainder does not predict the certified cost across fits.
Refutation criterion: a family of instances on which the root-mean-square remainder or the variational gap predicts
exp(D_2) within a constant factor across fits.

VAR and CHI are non-convex in general: L-BFGS from two starts (ML and LSu), the better end point is kept and the
difference between the two is reported.  LSs is iterated at most 40 times; non-convergence is reported.
For the ten instances with more than BIG = 20 000 states (59 049 or 531 441): one start (ML), at most 200 iterations,
and LSs is not run (on every smaller instance its fixed point is the variational fit: the normal equations of a
least-squares fit under the surrogate's own measure are the stationarity conditions of KL(q || pi_g)).

Run:  python3 -u b10_fit_directions.py > b10_fit_directions.log        (one core)
"""
import os, sys, math, json, time
import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp
import scipy.sparse as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_P2"))
import anlib
BETA = anlib.BETA
BIG = 20000


class Family:
    """exponential family on a product grid with site tables and (optionally) nearest-neighbour pair tables"""
    def __init__(self, shape, chain):
        self.shape = shape; self.n = n = len(shape); self.N = N = int(np.prod(shape))
        idx = np.indices(shape).reshape(n, N)
        self.cols = []; self.sizes = []
        for i in range(n):
            self.cols.append(idx[i].astype(np.int64)); self.sizes.append(shape[i])
        if chain:
            for i in range(n - 1):
                self.cols.append((idx[i] * shape[i + 1] + idx[i + 1]).astype(np.int64)); self.sizes.append(shape[i] * shape[i + 1])
        self.off = np.concatenate([[0], np.cumsum(self.sizes)]); self.P = int(self.off[-1])
        self._A = None

    def score(self, th):
        s = np.zeros(self.N)
        for c, o, k in zip(self.cols, self.off, self.sizes):
            s += th[o:o + k][c]
        return s

    def logq(self, th):
        s = self.score(th); return s - logsumexp(s)

    def moments(self, p):
        return np.concatenate([np.bincount(c, weights=p, minlength=k) for c, k in zip(self.cols, self.sizes)])

    def design(self):
        if self._A is None:
            rows = np.tile(np.arange(self.N), len(self.cols))
            colidx = np.concatenate([c + o for c, o in zip(self.cols, self.off)])
            self._A = sp.csr_matrix((np.ones(rows.size), (rows, colidx)), shape=(self.N, self.P))
        return self._A

    def ls(self, y, w):
        """weighted least squares of y on the family's indicator design; returns th with A th ~ y"""
        A = self.design(); WA = A.multiply(w[:, None]).tocsr()
        G = (A.T @ WA).toarray(); b = A.T @ (w * y)
        return np.linalg.lstsq(G, b, rcond=1e-12)[0]


def fit_min(fam, lpg, kind, th0, maxiter=400):
    pg = np.exp(lpg)
    mg = fam.moments(pg)
    def fun(th):
        lq = fam.logq(th); q = np.exp(lq); mq = fam.moments(q)
        if kind == "VAR":
            h = lq - lpg; val = float(q @ h)
            grad = fam.moments(q * h) - mq * val
        elif kind == "ML":
            val = float(pg @ (lpg - lq)); grad = mq - mg
        else:  # CHI
            a = 2 * lpg - lq; val = float(logsumexp(a)); w = np.exp(a - val)
            grad = mq - fam.moments(w)
        return val, grad
    res = minimize(fun, th0, jac=True, method="L-BFGS-B", options=dict(maxiter=maxiter, maxfun=int(1.5 * maxiter), ftol=1e-13, gtol=1e-9))
    return res.x, float(res.fun), int(res.nit)


def metrics(fam, lpg, th, betag):
    lq = fam.logq(th); q = np.exp(lq); pg = np.exp(lpg)
    r = betag + lq                      # beta g - (-ln q): the remainder up to a constant
    Er = float(q @ r); sd = math.sqrt(max(float(q @ (r - Er) ** 2), 0.0))
    return dict(rms=sd, floor=Er - float(r.min()), KLvar=float(q @ (lq - lpg)), KLml=float(pg @ (lpg - lq)),
                D2=float(logsumexp(2 * lpg - lq)), Dinf=float(np.max(lpg - lq)))


def analyse(tag):
    d = anlib.load_fb(tag)
    g = (d["tors"] + d["lj"] + d["coul"] + d["gb"]).ravel()
    betag = BETA * (g - g.min()); lpg = -betag - logsumexp(-betag)
    out = []
    for famname, chain in (("product", False), ("chain", True)):
        fam = Family(d["shape"], chain)
        fits = {}
        uni = np.full(fam.N, 1.0 / fam.N)
        th_lsu = -fam.ls(betag, uni); fits["LSu"] = th_lsu
        # closed-form ML
        pg = np.exp(lpg); mg = fam.moments(pg); th_ml = np.zeros(fam.P)
        eps = 1e-300
        n = fam.n
        if not chain:
            for i in range(n):
                th_ml[fam.off[i]:fam.off[i + 1]] = np.log(np.maximum(mg[fam.off[i]:fam.off[i + 1]], eps))
        else:
            for e in range(n - 1):
                o = fam.off[n + e]; th_ml[o:o + fam.sizes[n + e]] = np.log(np.maximum(mg[o:o + fam.sizes[n + e]], eps))
            for i in range(1, n - 1):
                th_ml[fam.off[i]:fam.off[i + 1]] = -np.log(np.maximum(mg[fam.off[i]:fam.off[i + 1]], eps))
        fits["ML"] = th_ml
        # LSs: iterate weighted least squares under the surrogate's own measure
        th = th_lsu.copy(); conv = None; big = fam.N > BIG
        for it in range(0 if big else 40):
            q = np.exp(fam.logq(th)); th_new = -fam.ls(betag, q)
            dlt = float(np.max(np.abs(fam.logq(th_new) - fam.logq(th))[q > 1e-12])) if np.any(q > 1e-12) else 0.0
            th = th_new
            if dlt < 1e-8: conv = it + 1; break
        fits["LSs"] = None if big else th; lss_conv = conv
        notes = {}
        for kind in ("VAR", "CHI"):
            best = None; vals = []
            for start in (("ML",) if big else ("ML", "LSu")):
                x, v, nit = fit_min(fam, lpg, kind, np.clip(fits[start], -60, 60), 200 if big else 400)
                vals.append(v)
                if best is None or v < best[1]: best = (x, v, nit)
            fits[kind] = best[0]; notes[kind] = abs(vals[0] - vals[1]) if len(vals) == 2 else float("nan")
        for kind in ("LSu", "LSs", "VAR", "ML", "CHI"):
            if fits[kind] is None: continue
            m = metrics(fam, lpg, fits[kind], betag)
            m.update(tag=tag, seq=d["seq"], bb=d["bb"], n=d["n"], N=fam.N, family=famname, fit=kind, P=fam.P,
                     lss_iterations=lss_conv, two_start_gap=notes.get(kind))
            out.append(m)
    return out


if __name__ == "__main__":
    t0 = time.time()
    only = sys.argv[1:]
    tags = []
    for aa, ns in (("V", (2, 4, 6, 8, 10, 12)), ("L", (2, 4, 6, 8)), ("S", (2, 3, 4, 5, 6))):
        for bb in ("E", "P2", "H"):
            for n in ns:
                t = f"fb_{aa}{n}_{bb}_R3_t0.60"
                if os.path.exists(os.path.join(HERE, "..", "ws_P2", "data", t + ".npz")): tags.append(t)
    assert len(tags) == 45, len(tags)
    if only: tags = [t for t in tags if any(o in t for o in only)]
    rows = []
    print("# instance  states  family  fit | rms remainder (kT) | KL(q||pi_g) variational gap | KL(pi_g||q) | D_2(pi_g||q) | D_inf(pi_g||q) | floor b | notes", flush=True)
    for tag in tags:
        t1 = time.time(); rs = analyse(tag); rows.extend(rs)
        for q in rs:
            name = q["seq"][:1] + str(q["n"]) + "_" + q["bb"]
            note = ""
            if q["fit"] == "LSs": note = f"LSs iterations: {q['lss_iterations']}" if q["lss_iterations"] else "LSs NOT converged in 40 iterations"
            if q["two_start_gap"] is not None: note = (f"two starts differ by {q['two_start_gap']:.1e}" if q["two_start_gap"] == q["two_start_gap"] else "one start (ML)")
            print(f"{name:8s} {q['N']:7d}  {q['family']:7s} {q['fit']:3s} | {q['rms']:9.4f} | {q['KLvar']:10.3e} | {q['KLml']:10.3e} | {q['D2']:10.3e} | {q['Dinf']:9.3f} | {q['floor']:8.3f} | {note}", flush=True)
        print(f"#   {tag}: {time.time()-t1:.0f} s", flush=True)
    # ---- summaries
    def key(q): return (q["tag"], q["family"])
    groups = {}
    for q in rows: groups.setdefault(key(q), {})[q["fit"]] = q
    print("# summary 1: for every (instance, family) with D_2 of the worst fit above 1e-3 -- the spread across the five fits")
    print("#   instance family | rms: min..max (ratio) | variational gap: min..max | D_2: min..max  -> exp(D_2) ratio worst/best | fit with smallest rms / its rank in D_2 (1 = best) | fit with smallest variational gap / its rank in D_2")
    nontriv = 0; rms_best_is_d2_worst = 0; var_best_is_d2_worst = 0; ratio_list = []; rank_rms = []; rank_var = []
    for (tag, fam), fs in groups.items():
        d2 = {k: v["D2"] for k, v in fs.items()}
        if max(d2.values()) < 1e-3: continue
        nontriv += 1
        fs = {k: v for k, v in fs.items() if k != "LSs"}          # LSs coincides with VAR wherever it was run (summary 4)
        d2 = {k: v["D2"] for k, v in fs.items()}
        order = sorted(d2, key=d2.get)
        krms = min(fs, key=lambda k: fs[k]["rms"]); kvar = min(fs, key=lambda k: fs[k]["KLvar"])
        r1 = order.index(krms) + 1; r2 = order.index(kvar) + 1; rank_rms.append(r1); rank_var.append(r2)
        rms_best_is_d2_worst += (r1 == 4); var_best_is_d2_worst += (r2 == 4)
        ratio = max(d2.values()) - min(d2.values()); ratio_list.append(ratio)
        q0 = fs["ML"]; name = q0["seq"][:1] + str(q0["n"]) + "_" + q0["bb"]
        rm = [v["rms"] for v in fs.values()]; kv = [v["KLvar"] for v in fs.values()]
        print(f"#   {name:8s} {fam:7s} | {min(rm):.3f}..{max(rm):.3f} ({max(rm)/max(min(rm),1e-300):.2f}) | {min(kv):.2e}..{max(kv):.2e} | {min(d2.values()):.3e}..{max(d2.values()):.3e} -> e^{ratio:.2f} | {krms} / {r1} | {kvar} / {r2}")
    print(f"# summary 2: {nontriv} non-trivial (instance, family) pairs.  exp(D_2) worst/best across fits: median e^{np.median(ratio_list):.2f}, max e^{max(ratio_list):.2f}.")
    print(f"#   among LSu, VAR, ML, CHI the fit with the smallest rms remainder has D_2-rank (1 best .. 4 worst): " + ", ".join(f"rank {r}: {rank_rms.count(r)}" for r in range(1, 5)))
    print(f"#   the fit with the smallest variational gap (VAR by construction, unless a start failed) has D_2-rank: " + ", ".join(f"rank {r}: {rank_var.count(r)}" for r in range(1, 5)))
    print("# summary 3: D_2 by fit, over the non-trivial pairs: how often each fit is the best / the worst, and the median of D_2(fit) - D_2(CHI)")
    for kind in ("LSu", "VAR", "ML", "CHI"):
        best = worst = 0; diffs = []
        for (tag, fam), fs in groups.items():
            d2 = {k: v["D2"] for k, v in fs.items() if k != "LSs"}
            if max(d2.values()) < 1e-3: continue
            best += (d2[kind] <= min(d2.values()) + 1e-9); worst += (d2[kind] >= max(d2.values()) - 1e-9); diffs.append(d2[kind] - d2["CHI"])
        print(f"#   {kind}: best in {best}, worst in {worst} of {nontriv}; D_2 - D_2(CHI): median {np.median(diffs):.3e}, max {max(diffs):.3e}")
    dl = [abs(fs["LSs"]["KLvar"] - fs["VAR"]["KLvar"]) for fs in groups.values() if "LSs" in fs]
    dq = [abs(fs["LSs"]["D2"] - fs["VAR"]["D2"]) for fs in groups.values() if "LSs" in fs]
    nconv = sum(1 for fs in groups.values() if "LSs" in fs and fs["LSs"]["lss_iterations"])
    print(f"# summary 4: LSs against VAR on the {len(dl)} (instance, family) pairs where LSs was run: LSs converged in {nconv}; "
          f"largest |KL(q||pi_g)(LSs) - (VAR)| = {max(dl):.1e}, largest |D_2(LSs) - D_2(VAR)| = {max(dq):.1e}")
    json.dump(rows, open(os.path.join(HERE, "b10_fit_directions.json" if not only else "b10_fit_directions_partial.json"), "w"))
    print(f"ALL DONE  {len(rows)} rows, {time.time()-t0:.0f} s")
