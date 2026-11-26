"""
P8 step 2 -- distance laws from the outputs of p8_06_distance.py (no new energy evaluation).

(1) Third-order anchored terms M_T (anchor context) of a twelve-residue peptide against the SPATIAL distances between
    the three side-chain groups in the states y_T at which |d_T| is largest (the "group" of a site: its charged head
    for Lys / Glu, all its moving atoms otherwise; centroids).  With d_AB, d_AC, d_BC the three centroid distances and
    P = min over the three groups of the product of its two distances, least squares for  ln M_T = a ln P + c
    (a = -4 would be: the group in the middle responds to each of the other two through one descreening integral
    ~ r^-4), for all triples and for the triples whose three distances all exceed 0.6 nm.
(2) First-order response R1[A, j] of a rigid group's own solvation energy to a change at another site j against the
    centroid distance (group at the anchor, side chain j in its maximising state), by class of the group; and the same
    normalised by the sensitivity S_A = sum_p |dE_A/d ln B_p| at the anchor (kcal/mol per unit relative change of a Born
    radius) -- not computed here; the classes are compared at equal distance instead.
(3) Second-order response R2[A; j, k] against the product of the two distances.

usage: python3 -B p8_11_distance_fit.py SEQ BB TAU     -> logs/dfit_<tag>.log, out/dfit_<tag>.json
"""
import sys, os, json
import numpy as np
from p8lib import *

seq, bb, tau = sys.argv[1], sys.argv[2], float(sys.argv[3])
tag = tagname(seq, bb, tau)
log = Log(os.path.join(HERE, "logs", f"dfit_{tag}.log"))
Z = np.load(os.path.join(HERE, "out", f"dist_{tag}.npz"))
G = GBModel(seq, bb, tau=tau)
n = G.ns
x0 = [int(v) for v in Z["anchor"]]
cls, letter = atom_classes(G)
restype = [str(v) for v in Z["restype"]]
log(f"=== p8_11_distance_fit: {seq} on {bb}, tau {tau}: {n} sites ({''.join(restype)})")


def group_centroid(i, y):
    """centroid (nm) of the charged head of site i in state y, or of all its moving atoms if the site is neutral."""
    at = G.mov[i]
    sel = np.flatnonzero(cls[at] == 3)
    if len(sel) == 0:
        sel = np.arange(len(at))
    return G.Xm[i][y][sel].mean(axis=0)


def fit(x, y):
    A = np.vstack([np.log(x), np.ones(len(x))]).T
    co = np.linalg.lstsq(A, np.log(y), rcond=None)[0]
    res = np.log(y) - A @ co
    return float(co[0]), float(co[1]), float(res.std())


out = dict(seq=seq, bb=bb, tau=tau)
# ---------------------------------------------------------------- (1) triples
tri = Z["triples"]; MT = Z["MT"]; YT = Z["YT"]
Pm = np.zeros(len(tri)); dmin = np.zeros(len(tri)); dmax = np.zeros(len(tri)); ncharged = Z["chargedT"]
for t, (T, y) in enumerate(zip(tri, YT)):
    c = [group_centroid(int(i), int(v)) for i, v in zip(T, y)]
    d01, d02, d12 = (float(np.linalg.norm(c[0] - c[1])), float(np.linalg.norm(c[0] - c[2])), float(np.linalg.norm(c[1] - c[2])))
    Pm[t] = min(d01 * d02, d01 * d12, d02 * d12)
    dmin[t] = min(d01, d02, d12); dmax[t] = max(d01, d02, d12)
ok = MT > 0
a_all = fit(Pm[ok], MT[ok])
far = ok & (dmin > 0.6)
a_far = fit(Pm[far], MT[far]) if far.sum() >= 8 else None
log(f"(1) {len(tri)} triples: M_T from {MT.min():.2e} to {MT.max():.2e} kcal/mol; smallest group distance in the maximising states from {dmin.min():.2f} to {dmin.max():.2f} nm")
log(f"    all triples: ln M_T = {a_all[0]:.2f} ln P + c, rms residual {a_all[2]:.2f} (a factor {np.exp(a_all[2]):.1f});  P = min over the groups of the product of its two distances")
if a_far:
    log(f"    triples with all three distances > 0.6 nm ({int(far.sum())}): ln M_T = {a_far[0]:.2f} ln P + c, rms residual {a_far[2]:.2f} (a factor {np.exp(a_far[2]):.1f})")
edges = [0.0, 0.4, 0.6, 0.8, 1.0, 1.3, 9.9]
rows = []
log("    by the smallest of the three group distances: triples | median M_T | max M_T | share of the sum")
for lo_, hi_ in zip(edges[:-1], edges[1:]):
    mk = (dmin >= lo_) & (dmin < hi_)
    if mk.any():
        rows.append(dict(lo=lo_, hi=hi_, n=int(mk.sum()), median=float(np.median(MT[mk])), max=float(MT[mk].max()), share=float(MT[mk].sum() / MT.sum())))
        log(f"      {lo_:.1f}-{hi_:.1f} nm: {int(mk.sum()):3d} | {np.median(MT[mk]):.3e} | {MT[mk].max():.3e} | {100 * MT[mk].sum() / MT.sum():.1f} %")
out["triples"] = dict(n=int(len(tri)), sum=float(MT.sum()), fit_all=a_all, fit_far=a_far, nfar=int(far.sum()), by_dmin=rows)
if len(set(ncharged.tolist())) > 1:
    byc = []
    log("    by the number of charged side chains in the triple, at comparable smallest distance (0.6-1.0 nm): triples | median M_T")
    for c_ in sorted(set(ncharged.tolist())):
        mk = (ncharged == c_) & (dmin >= 0.6) & (dmin < 1.0)
        mk2 = ncharged == c_
        byc.append(dict(ncharged=int(c_), n=int(mk2.sum()), sum=float(MT[mk2].sum()), median=float(np.median(MT[mk2])),
                        n_mid=int(mk.sum()), median_mid=float(np.median(MT[mk])) if mk.any() else None))
        log(f"      {c_} charged: {int(mk.sum()):3d} | {np.median(MT[mk]) if mk.any() else float('nan'):.3e}   (all distances: {int(mk2.sum())} triples, sum {MT[mk2].sum():.3e}, median {np.median(MT[mk2]):.3e})")
    out["triples"]["by_charged"] = byc
# ---------------------------------------------------------------- (2), (3) group responses
R1 = Z["R1"]; D1 = Z["D1"]; R2 = Z["R2"]; gcls = Z["gcls"]; gq = Z["gq"]; gabsq = Z["gabsq"]; ghost = Z["ghost"]
cn = ["bb", "nsc", "chain", "head"]
out["R1"] = {}
log("(2) first-order response R1 of a group's own solvation energy to another site, by class: fit ln R1 = a ln d + c, and medians at 0.6-0.8, 0.9-1.2, 1.4-1.8 nm (kcal/mol)")
for c_ in range(4):
    gs = np.flatnonzero(gcls == c_)
    if not len(gs):
        continue
    d = D1[gs].ravel(); r = R1[gs].ravel(); okk = ~np.isnan(d) & (r > 0)
    a_ = fit(d[okk], r[okk])
    okf = okk & (d > 0.8)
    a_f = fit(d[okf], r[okf]) if okf.sum() >= 8 else None
    med = []
    for lo_, hi_ in ((0.6, 0.8), (0.9, 1.2), (1.4, 1.8)):
        mk = okk & (d >= lo_) & (d < hi_)
        med.append(float(np.median(r[mk])) if mk.any() else None)
    out["R1"][cn[c_]] = dict(ngroups=int(len(gs)), mean_abs_net=float(np.abs(gq[gs]).mean()), mean_sum_abs=float(gabsq[gs].mean()), fit=a_, fit_beyond_0p8=a_f, medians=med, n=int(okk.sum()))
    log(f"    {cn[c_]:5s} ({len(gs)} groups, mean |net charge| {np.abs(gq[gs]).mean():.3f} e, mean sum|q| {gabsq[gs].mean():.3f} e; {int(okk.sum())} (group, site) pairs): "
        f"a = {a_[0]:.2f} (rms residual {a_[2]:.2f})" + (f"; beyond 0.8 nm a = {a_f[0]:.2f} ({a_f[2]:.2f})" if a_f else "") + "; medians " + ", ".join("—" if v is None else f"{v:.2e}" for v in med))
log("(3) second-order response R2[A; j, k] (group fixed, two other sites change): ln R2 = a ln(d_Aj d_Ak) + c")
out["R2"] = {}
for c_ in range(4):
    gs = np.flatnonzero(gcls == c_)
    xs, ys = [], []
    for a_ in gs:
        for j in range(n):
            for k_ in range(j + 1, n):
                v = R2[a_, j, k_]
                if v > 0 and not np.isnan(D1[a_, j]) and not np.isnan(D1[a_, k_]):
                    xs.append(D1[a_, j] * D1[a_, k_]); ys.append(v)
    if len(xs) >= 8:
        a2 = fit(np.array(xs), np.array(ys))
        out["R2"][cn[c_]] = dict(fit=a2, n=len(xs), median=float(np.median(ys)), sum_per_group=float(np.sum(ys) / len(gs)))
        log(f"    {cn[c_]:5s}: a = {a2[0]:.2f} (rms residual {a2[2]:.2f}; {len(xs)} cases); median R2 {np.median(ys):.2e}; sum over (j, k) per group {np.sum(ys) / len(gs):.3e} kcal/mol")
with open(os.path.join(HERE, "out", f"dfit_{tag}.json"), "w") as fh:
    json.dump(out, fh, indent=1)
log.done()
