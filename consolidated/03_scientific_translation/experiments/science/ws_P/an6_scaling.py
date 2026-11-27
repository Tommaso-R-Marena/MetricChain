"""Scaling of the per-torsion constants with position and chain length; extrapolation of the
theory's formulas to 10 and 100 residues.  Reads out/an1_constants.json (exact enumeration)
and out/long_ci_*.json (local-search lower bounds).
usage: python3 an6_scaling.py [residual]   (default GB)"""
import sys, os, json, math, glob
import numpy as np
from analysis_lib import *

rname = sys.argv[1] if len(sys.argv) > 1 else "GB"
TAU = 0.7
J = json.load(open(os.path.join(HERE, "out", "an1_constants.json")))
beta = 1 / KT300
np.set_printoptions(precision=1, suppress=True, linewidth=220)
out = {}
pooled = {}
for alphabet in ("A3", "A2"):
    print(f"\n===== exact constants of {rname}, alphabet {alphabet}, clash-free tau={TAU} (kcal/mol)")
    print(f"{'n':>2s} {'conf.':>8s} {'max c_i':>8s} {'/kT':>6s} {'mean c_i':>8s} {'c_end':>6s} {'c_mid':>6s} {'rms flip':>8s} {'range g':>8s}  c_i by torsion")
    rows = []
    for n in range(1, 12):
        key = f"{alphabet}|{n}|{TAU}|{rname}"
        if key not in J:
            continue
        c = np.array(J[key]["c"]); m = len(c)
        mi = np.minimum(np.arange(1, m + 1), m - np.arange(m))
        cend = c[[0, -1]].mean(); cmid = c[mi >= mi.max() - 0].mean() if m > 2 else c.mean()
        print(f"{n:2d} {J[key]['nconf']:8d} {c.max():8.2f} {c.max()*beta:6.1f} {c.mean():8.2f} {cend:6.2f} {cmid:6.2f} {max(J[key]['rms']):8.2f} {J[key]['range']:8.2f}  {c}")
        rows.append((n, c, mi))
    pooled[alphabet] = rows
    if not rows:
        continue
    ns = np.array([r[0] for r in rows]); cm = np.array([r[1].max() for r in rows]); ca = np.array([r[1].mean() for r in rows])
    if len(ns) >= 3:
        A = np.vstack([np.ones_like(ns), ns]).T.astype(float)
        (a0, b0), *_ = np.linalg.lstsq(A, cm, rcond=None)
        (a1, b1), *_ = np.linalg.lstsq(A, ca, rcond=None)
        sel = ns >= 2
        g0 = np.polyfit(np.log(ns[sel]), np.log(cm[sel]), 1)
        print(f"   max_i c_i vs n: linear fit {a0:.2f} + {b0:.2f} n (kcal/mol); power fit {math.exp(g0[1]):.2f} n^{g0[0]:.2f};  mean_i c_i: {a1:.2f} + {b1:.2f} n")
        out[f"{alphabet}_max_linear"] = (float(a0), float(b0)); out[f"{alphabet}_max_power"] = (float(math.exp(g0[1])), float(g0[0]))
        out[f"{alphabet}_mean_linear"] = (float(a1), float(b1))
    # pooled lever-arm fit c_i ~ a + b m_i + d (2n)
    mm = np.concatenate([r[2] for r in rows]).astype(float); cc = np.concatenate([r[1] for r in rows]); nn = np.concatenate([np.full(len(r[1]), 2.0 * r[0]) for r in rows])
    A = np.vstack([np.ones_like(mm), mm]).T
    (a, b), res, *_ = np.linalg.lstsq(A, cc, rcond=None)
    r1 = cc - A @ np.array([a, b])
    A2 = np.vstack([np.ones_like(mm), mm, nn]).T
    co2, *_ = np.linalg.lstsq(A2, cc, rcond=None)
    r2 = cc - A2 @ co2
    gp = np.polyfit(np.log(mm), np.log(cc), 1)
    r3 = cc - np.exp(gp[1]) * mm ** gp[0]
    print(f"   pooled over all sites and n: c_i = {a:.2f} + {b:.2f} m_i (rms resid {np.sqrt((r1**2).mean()):.2f});  "
          f"c_i = {co2[0]:.2f} + {co2[1]:.2f} m_i + {co2[2]:.2f} (2n) (rms {np.sqrt((r2**2).mean()):.2f});  "
          f"c_i = {math.exp(gp[1]):.2f} m_i^{gp[0]:.2f} (rms {np.sqrt((r3**2).mean()):.2f});   m_i = distance to the nearer chain end in torsions")
    out[f"{alphabet}_lever_linear"] = (float(a), float(b)); out[f"{alphabet}_lever_power"] = (float(math.exp(gp[1])), float(gp[0]))
    out[f"{alphabet}_lever_two"] = [float(v) for v in co2]
    # position dependence within the longest chain
    n, c, mi = rows[-1]
    print(f"   within n={n}: c by distance to the nearer end m: " + "  ".join(f"m={int(v)}: {c[mi == v].mean():.1f}" for v in np.unique(mi)))

# local-search lower bounds for longer chains
print(f"\n===== lower bounds from local search (every value is attained by an explicit pair of clash-free conformations)")
rk = {"GB": "GB", "ff03-ff14SB": "ff03"}.get(rname, rname)
for path in sorted(glob.glob(os.path.join(HERE, "out", f"long_ci_*_{rk}.json")), key=lambda p: (json.load(open(p))["alphabet"], json.load(open(p))["n"])):
    L = json.load(open(path)); n = L["n"]; m = 2 * n; alphabet = L["alphabet"]
    sites = sorted(int(s) for s in L["sites"])
    lb = np.array([L["sites"][str(s)]["lower_bound"] for s in sites]); med = np.array([L["sites"][str(s)]["sampled_median"] for s in sites])
    mi = np.array([min(s + 1, m - s) for s in sites])
    key = f"{alphabet}|{n}|{TAU}|{rname}"
    ex = ""
    if key in J:
        cex = np.array(J[key]["c"])[sites]
        ex = f"  | exact available: search/exact ratio min {np.min(lb/cex):.2f} mean {np.mean(lb/cex):.2f}"
    a, b = out.get(f"{alphabet}_lever_linear", (float('nan'),) * 2)
    print(f"{alphabet} n={n:2d}: {len(sites)} sites; max lower bound {lb.max():.1f} kcal/mol = {lb.max()*beta:.0f} kT; by m_i: "
          + " ".join(f"{int(v)}:{lb[mi == v].max():.1f}" for v in np.unique(mi)) + f"; median random flip {np.median(med):.1f}" + ex)
    out[f"long_{alphabet}_{n}"] = dict(sites=sites, lb=lb.tolist(), m=mi.tolist())

# ------------------------------------------------------------------ extrapolation of the formulas
if rname == "GB" and pooled["A3"]:
    print("\n===== theory formulas with measured numbers, extrapolated chains (A3-type sites, 3 states per torsion)")
    # site tables of the known part: star of f at argmin f in the largest enumerated A3 chain
    nbig = pooled["A3"][-1][0]
    d = load("A3", nbig); R = residuals(d); m = d["m"]; k = d["k"]
    mask = d["clash"] > TAU
    f = np.where(mask, R["f"], np.inf); E = np.where(mask, R["f"] + R["GB"], np.inf)
    x0 = np.unravel_index(np.argmin(f), f.shape); xs = np.unravel_index(np.argmin(E), E.shape)
    def star(h, x):
        tabs = []
        for i in range(m):
            row = []
            for s in range(k):
                y = list(x); y[i] = s
                row.append(h[tuple(y)] - h[x])
            tabs.append(row)
        return np.array(tabs)
    Tf = star(f, x0); TE = star(E, xs)
    print(f"A3 n={nbig}: argmin f = {x0}; argmin E = {xs}")
    print("star of f at argmin f (kcal/mol; rows = torsion sites; inf = clash):"); print(np.round(Tf, 2))
    print("star of E = f + GB at argmin E:"); print(np.round(TE, 2))
    # coil-like scenario: star of f around the all-beta conformation (phi=-150, psi=150), which is the
    # minimum of f for n <= 4 and has clash-free single-flip neighbours at every site
    xb = tuple([0, 2] * (m // 2))
    Tb = star(f, xb)
    print(f"star of f around the all-beta conformation {xb} (f - min f = {f[xb]-f[x0]:.2f} kcal/mol):"); print(np.round(Tb, 2))
    interior = list(range(2, m - 2))
    def med_table(T, par):
        rowsel = [np.sort(T[i]) for i in interior if i % 2 == par]
        return np.median(np.array(rowsel), axis=0)
    tab_phi = med_table(Tb, 0); tab_psi = med_table(Tb, 1)
    print(f"coil-like interior site tables of f (sorted, kcal/mol): phi {np.round(tab_phi,2)}, psi {np.round(tab_psi,2)}")
    cexact = pooled["A3"][-1][1]; mexact = pooled["A3"][-1][2]
    by_m = {int(v): float(cexact[mexact == v].mean()) for v in np.unique(mexact)}
    a, b = out["A3_lever_linear"]; c0, gam = out["A3_lever_power"]
    def profile(nres, scen):
        mtot = 2 * nres; mi = np.minimum(np.arange(1, mtot + 1), mtot - np.arange(mtot))
        if scen == "plateau":       # no growth beyond what was enumerated
            return np.array([by_m[min(int(v), max(by_m))] for v in mi])
        if scen == "linear":
            return a + b * mi
        if scen == "power":
            return c0 * mi ** gam
    def product_bound(tabs, cc, eps):
        best = (0.0, 0.0)
        for t in np.concatenate([[0.0], np.logspace(-4, 2, 600)]):
            val = -t * eps
            for tab, ci in zip(tabs, cc):
                fin = [e for e in tab if np.isfinite(e)]
                val += math.log(sum(math.exp(-t * e) for e in fin)) - math.log(1 + (len(fin) - 1) * math.exp(-t * ci))
            if val > best[0]:
                best = (val, t)
        return best
    for nres in (10, 100):
        mtot = 2 * nres
        print(f"--- {nres} residues = {mtot} torsion sites; grid size 3^{mtot} = 10^{mtot*math.log10(3):.1f}")
        for scen in ("plateau", "linear", "power"):
            c = profile(nres, scen)
            u = beta * c
            tabs = [tab_phi if i % 2 == 0 else tab_psi for i in range(mtot)]
            emin = np.array([np.sort(t)[1] for t in tabs])
            nsharp = int((emin >= c).sum())
            lc = float(np.log(np.cosh(u / 2)).sum())
            res = []
            for eps in (0.0, 1.0 * nres * KT300):
                pb, tb = product_bound(tabs, c, eps)
                res.append(pb)
            # with the measured kappa: the true residual is not the zero residual; lower bound uses (1-kappa) c; here kappa unknown -> zero-residual form
            print(f"   scenario {scen:8s}: c_i from {c.min():.1f} to {c.max():.1f} kcal/mol (beta c: {u.min():.0f}–{u.max():.0f}); sharp sites {nsharp}/{mtot}; "
                  f"sum ln cosh(beta c_i/2) = {lc:.0f} nats = {lc*KT300:.0f} kcal/mol = {lc/nres:.1f} nats/residue; "
                  f"product bound ln N_cov >= {res[0]:.1f} (eps=0) / {res[1]:.1f} (eps = 1 kT per residue) of ln|X| = {mtot*math.log(3):.1f}  -> N >= 10^{res[0]/math.log(10):.1f}")
            out[f"extrap_{nres}_{scen}"] = dict(cmin=float(c.min()), cmax=float(c.max()), sharp=nsharp, lncosh=lc, lnN0=res[0], lnN1=res[1], lnX=mtot * math.log(3))
json.dump(out, open(os.path.join(HERE, "out", f"an6_scaling_{rname}.json"), "w"), indent=0)
