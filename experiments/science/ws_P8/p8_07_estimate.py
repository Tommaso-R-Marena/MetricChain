"""
P8 step 4 -- first-order estimates of the certified bracket from per-subset constants and a sample of the true ensemble.

Addendum A17 (16), Lemma A17.16 / item 39 ("refined rule"): with exact evaluated terms the bracket of a sandwich
m_-/+ = [f + I_{m-1} g] -/+ pen is  2 beta <pen>  to first order, <.> the mean under the true ensemble (here: the
heat-bath Gibbs sample of p8_05_gibbs.py -- UNCERTIFIED; nothing in this script is a certificate).

Penalty forms built from the per-subset constants chat_T (|T| = m) of out/g12_<tag>_m<m>.npz, for each variant
(P3, S, AH, SA), with s_i = [x_i != x0_i], t = |T n S(x)|:
    site       sum_i gamma_i s_i,                         gamma_i = sum_{T ni i} chat_T / m                      (P3)
    pair       k = 2 shares, all pairs                    sum_T chat_T C(t,2)/C(m,2)                               (P6, Lemma A)
    pair/w     banded: pairs beyond the band w in halves to their sites                                           (P6, Lemma A)
    triple     k = 3 shares, all triples                  sum_T chat_T C(t,3)/C(m,3)                               (P6, Lemma A')
    triple/w   triples with last - first <= w kept; the others in thirds to their pairs, pairs beyond the band in
               halves to their sites                                                                              (P6, Lemma A')
    quad       k = 4 shares, all quadruples               sum_T chat_T C(t,4)/C(m,4)        (the same counting argument, k = 4)
    occ3/w     every T charged in full to ONE sub-tuple U_T of at most three of its sites that fits a window:
               sum_T chat_T prod_{i in U_T} s_i, U_T chosen by the measured site frequencies (valid for every choice)
    occW/w     the same with sub-tuples of any size that fit a window (the coordinator's window model can carry them)
    envelope   sum_{T subset S(x)} chat_T                 (k = m: the pointwise smallest penalty the constants allow)
No floating-point allowance of the evaluated terms is included (the coordinator's "refined rule" numbers include P6's).

usage: python3 -B p8_07_estimate.py SEQ BB TAU BAND
needs out/g12_<tag>_m{4,5,6}.npz and out/gibbs_<tag>.npz; optional: out/dist_<tag>.npz (order 3: variant "exact3", the
exact anchored terms of the triples in the anchor context) and out/exact_<tag>_M*.npz (variants "exact<m>" of the orders
the ball of p8_14_exact_terms12.py reaches).  The "exact" variants are measurements of the truth, not valid constants.
Writes logs/est_<tag>.log, out/est_<tag>.json
"""
import sys, os, json, time, itertools, glob
from math import comb
import numpy as np
from p8lib import *

a = sys.argv[1:]
seq, bb, tau, W = a[0], a[1], float(a[2]), int(a[3])
tag = tagname(seq, bb, tau)
log = Log(os.path.join(HERE, "logs", f"est_{tag}.log"))
Zg = np.load(os.path.join(HERE, "out", f"gibbs_{tag}.npz"))
X = Zg["X"]; x0 = Zg["anchor"]; k = [int(v) for v in Zg["k"]]
n = len(k)
s = (X != x0[None, :]).astype(float)                  # (samples, n)
nsamp = s.shape[0]
chain = Zg["chain"]; nch = int(chain.max()) + 1
psite = s.mean(axis=0)
log(f"=== p8_07_estimate: {seq} on {bb}, tau {tau}, band {W}: {nsamp} Gibbs states ({nch} chains); off the anchor {s.sum(1).mean():.3f} of {n}; by site " + " ".join(f"{v:.3f}" for v in psite))
ref = None
rf = os.path.join(SCI, "pi_inference", "certificate_reach_table_H.json")
if bb == "H" and os.path.exists(rf):
    for r in json.load(open(rf)):
        if r["seq"] == seq:
            ref = r
res = dict(seq=seq, bb=bb, tau=tau, band=W, nsamples=int(nsamp), psite=[float(v) for v in psite], orders={})


def mean_se(v):
    """mean over the sample and the standard error from the chain means."""
    cm = np.array([v[chain == c].mean() for c in range(nch)])
    return float(v.mean()), float(cm.std(ddof=1) / np.sqrt(nch))


for m in (3, 4, 5, 6):
    if m == 3:
        # order 3: the EXACT third-order anchored terms in the anchor context, M_T = max_y |d_T(y_T)| (p8_06_distance.py) --
        # lower bounds of the exact anchored constants c_T^anch: what an ideal certificate of order 3 would have as constants
        fn = os.path.join(HERE, "out", f"dist_{tag}.npz")
        if not os.path.exists(fn):
            log(f"--- order 3 (exact anchor-context terms): {fn} missing, skipped"); continue
        Z = np.load(fn)
        assert list(Z["anchor"]) == list(x0)
        Ts = Z["triples"]; C = Z["MT"][:, None]; variants = ["exact3"]
    else:
        fn = os.path.join(HERE, "out", f"g12_{tag}_m{m}.npz")
        if not os.path.exists(fn):
            log(f"--- order {m}: {fn} missing, skipped"); continue
        Z = np.load(fn)
        assert list(Z["anchor"]) == list(x0), "anchor of the constants differs from the anchor of the Gibbs sample"
        Ts = Z["T"]; C = Z["C"].sum(axis=2); variants = [str(v) for v in Z["variants"]]
        fnb = os.path.join(HERE, "out", f"g12b_{tag}_m{m}.npz")
        if os.path.exists(fnb):                             # block-wise variants (p8_04b_gamma12_blocks.py)
            Zb = np.load(fnb)
            assert np.array_equal(Zb["T"], Ts)
            C = np.concatenate([C, Zb["Cb"]], axis=1); variants += [str(v) for v in Zb["variants"]]
        # the EXACT anchored terms of this order in the anchor context (p8_14_exact_terms12.py), where the ball reaches:
        # variant "exact<m>" -- NOT valid constants (lower bounds of the exact anchored constants); what an ideal
        # certificate of this order would have, to leading order
        for fe in sorted(glob.glob(os.path.join(HERE, "out", f"exact_{tag}_M*.npz"))):
            Ze = np.load(fe)
            if f"T{m}" in Ze.files and list(Ze["anchor"]) == list(x0) and f"exact{m}" not in variants:
                mt_ = {tuple(int(v_) for v_ in T_): float(c_) for T_, c_ in zip(Ze[f"T{m}"], Ze[f"MT{m}"])}
                C = np.concatenate([C, np.array([mt_[tuple(int(v_) for v_ in T_)] for T_ in Ts])[:, None]], axis=1); variants.append(f"exact{m}")
    nT = len(Ts)
    inT = np.zeros((nT, n))
    inT[np.arange(nT)[:, None], Ts] = 1.0
    tcount = s @ inT.T                                 # (samples, nT): |T n S(x)|
    ball = ball_size(k, m - 1)
    row = dict(nsub=int(nT), ball=int(ball), variants={})
    log(f"--- order {m}: {nT} subsets; ball of radius {m - 1}: {ball} evaluations ({100 * ball / np.prod([float(v) for v in k]):.2g} % of the domain).  "
        f"First-order bracket 2 beta <penalty> (nats; standard error from the 16 chains in brackets)")
    if ref is not None and str(m) in ref["orders"]:
        o = ref["orders"][str(m)]
        log(f"    coordinator's table (P3's constants, band {ref['band']}, with fp allowances, own Gibbs sample): Gamma = {o['Gamma_kT']:.4g} kT; refined rule site {o['refined']['site']:.4g}, "
            f"banded pair {o['refined']['pair']:.4g}, banded triple {o['refined']['triple']:.4g}")
    for vi, v in enumerate(variants):
        c = C[:, vi]
        Gam = float(c.sum())
        # share sums
        S_i = inT.T @ c                                # (n,)
        Gp = (inT * c[:, None]).T @ inT                # (n, n): G_ij (diagonal = S_i)
        forms = {}
        forms["site"] = s @ (S_i / m)
        for kk, name in ((2, "pair"), (3, "triple"), (4, "quad")):
            if kk <= m:
                wts = np.array([comb(t, kk) for t in range(m + 1)], dtype=float) / comb(m, kk)
                forms[name] = wts[tcount.astype(int)] @ c
        forms["envelope"] = (tcount == m).astype(float) @ c
        # banded pair form
        g2 = Gp / comb(m, 2); np.fill_diagonal(g2, 0.0)
        band = np.abs(np.arange(n)[:, None] - np.arange(n)[None, :]) <= W
        gs = 0.5 * (g2 * (~band)).sum(axis=1)
        g2b = g2 * band
        forms[f"pair/w{W}"] = s @ gs + 0.5 * np.einsum("ni,ij,nj->n", s, g2b, s)
        # windowed triple form
        H = np.einsum("ti,tj,tk,t->ijk", inT, inT, inT, c)        # H_ijk for all ordered triples
        eta = H / comb(m, 3)
        pen3 = np.zeros(nsamp); rho = np.zeros((n, n))
        for (i, j, l) in itertools.combinations(range(n), 3):
            if l - i <= W:
                pen3 += eta[i, j, l] * s[:, i] * s[:, j] * s[:, l]
            else:
                for (a_, b_) in ((i, j), (i, l), (j, l)):
                    rho[a_, b_] += eta[i, j, l] / 3.0; rho[b_, a_] += eta[i, j, l] / 3.0
        rs = 0.5 * (rho * (~band)).sum(axis=1); rb = rho * band
        forms[f"triple/w{W}"] = pen3 + s @ rs + 0.5 * np.einsum("ni,ij,nj->n", s, rb, s)
        # occupancy-aware allocation: every T is charged in full, chat_T prod_{i in U_T} s_i, to ONE sub-tuple U_T of T that
        # fits a window (last - first <= W); valid for every choice ([T subset S] <= prod_{i in U} s_i); U_T is chosen to
        # minimise the product of the site frequencies measured on the OTHER half of the chains (two-fold: no state is
        # used both to choose and to evaluate).  occ3: |U_T| <= 3 (P6's model class); occW: any size (window model).
        for name, kmax in ((f"occ3/w{W}", 3), (f"occW/w{W}", m)):
            pen = np.zeros(nsamp)
            for half in (0, 1):
                tr = (chain % 2) != half; ev = ~tr
                pfr = np.clip(s[tr].mean(axis=0), 1.0 / (2 * tr.sum()), 1.0)
                for ti in range(nT):
                    T = [int(v_) for v_ in Ts[ti]]
                    best = None
                    for r_ in range(1, kmax + 1):
                        for U in itertools.combinations(T, r_):
                            if U[-1] - U[0] <= W:
                                pr = float(np.prod(pfr[list(U)]))
                                if best is None or pr < best[0]:
                                    best = (pr, U)
                    pen[ev] += c[ti] * s[ev][:, list(best[1])].prod(axis=1)
            forms[name] = pen
        # pointwise order of the forms (Lemma A, A'): envelope <= triple <= pair <= site, triple <= triple/w <= pair/w <= site
        tol = 1e-9 * (1.0 + forms["site"])
        assert np.all(forms["envelope"] <= forms["triple"] + tol) and np.all(forms["triple"] <= forms["pair"] + tol) and np.all(forms["pair"] <= forms["site"] + tol)
        assert np.all(forms["triple"] <= forms[f"triple/w{W}"] + tol) and np.all(forms[f"triple/w{W}"] <= forms[f"pair/w{W}"] + tol) and np.all(forms[f"pair/w{W}"] <= forms["site"] + tol)
        if m >= 4:
            assert np.all(forms["envelope"] <= forms["quad"] + tol) and np.all(forms["quad"] <= forms["triple"] + tol)
        est = {name: mean_se(2.0 * BETA * arr) for name, arr in forms.items()}
        # beyond first order (Lemma A17.16: ln Z(m_-) - ln Z(m_+) = ln<e^{beta pen}> - ln<e^{-beta pen}> when the evaluated terms are
        # exact): the same two means over the sample.  A LOWER estimate when the sample misses rare states with large penalties.
        expo = {name: float(np.log(np.mean(np.exp(BETA * arr))) - np.log(np.mean(np.exp(-BETA * arr)))) for name, arr in forms.items()}
        pmax = {name: float(BETA * arr.max()) for name, arr in forms.items()}
        # independent sites with the measured frequencies (for comparison with the sample means)
        ind = {}
        for kk, name in ((1, "site"), (2, "pair"), (3, "triple"), (4, "quad"), (m, "envelope")):
            if kk <= m:
                ek = np.array([sum(np.prod(psite[list(U)]) for U in itertools.combinations(T, kk)) for T in Ts])
                ind[name] = float(2.0 * BETA * (c * ek).sum() / comb(m, kk))
        row["variants"][v] = dict(Gamma_kT=Gam * BETA, est={kname: list(val) for kname, val in est.items()}, independent=ind, expo=expo, pen_max_kT=pmax)
        assert np.all(forms["envelope"] <= forms[f"occW/w{W}"] + tol) and np.all(forms[f"occW/w{W}"] <= forms["site"] * m + tol)
        order_ = ["site", f"pair/w{W}", "pair", f"triple/w{W}", f"occ3/w{W}", f"occW/w{W}", "triple", "quad", "envelope"]
        log(f"    {v:6s}: Gamma = {Gam * BETA:10.4g} kT | " + " | ".join(f"{nm} {est[nm][0]:.3g} ({est[nm][1]:.2g})" for nm in order_ if nm in est))
        log(f"        independent sites: " + " | ".join(f"{nm} {ind[nm]:.3g}" for nm in ("site", "pair", "triple", "quad", "envelope") if nm in ind))
        log(f"        ln<e^(beta pen)> - ln<e^(-beta pen)> on the sample [largest beta*pen on the sample]: " + " | ".join(f"{nm} {expo[nm]:.3g} [{pmax[nm]:.2g}]" for nm in order_ if nm in expo))
    res["orders"][str(m)] = row
with open(os.path.join(HERE, "out", f"est_{tag}.json"), "w") as fh:
    json.dump(res, fh, indent=1)
log.done()
