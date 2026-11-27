#!/usr/bin/env python3
"""ER3 review, Theorem E19(e),(f): the cutting-plane face decision of experiments/ensemble/kbody_capacity.py and the
numbers 76/152/233 (cube) and 78/142/214 (Gaussian control).  Reviewer's own code; the division's module is
imported read-only (its linprog is wrapped to record what the solver returned; no file is modified).

V.  Instance by instance, on the same supports: the division's is_face against the reviewer's two independent
    certificates:
      face     <=  a q with q.psi = 0 on S and q.psi >= 1 on every other state (one LP over ALL states, no margin
                   normalisation, no cutting planes);
      non-face <=  a Stiemke certificate: h >= 0 on the other states, sum h = 1, with sum_y h(y) psi(y) in the span
                   of psi(S) (so no q can be positive off S); residual reported.
    Also recorded from inside is_face: LP statuses other than 0 (the script counts them as "not a face"), and the
    final margins t (the script declares "not a face" when t <= 1e-7).
T.  Thresholds with more trials (n = 8: 200 per K; n = 10: 80 per K), cube and Gaussian clouds (several independent
    clouds, which the division's control does not have: it draws one cloud per run), by the reviewer's full LP.
    The point of frequency one half by linear interpolation, with a binomial bootstrap interval.
usage: er3_kbody.py V8 | V10 | V12pair | V12 | T8 | T10
"""
import itertools, os, sys, time
from math import comb
import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "experiments", "ensemble")))
sys.dont_write_bytecode = True
import kbody_capacity as KB                                   # noqa: E402

rng = np.random.default_rng(31107)
LOG = {"status": [], "t": []}
_orig = KB.linprog


def _wrapped(*a, **k):
    res = _orig(*a, **k)
    LOG["status"].append(res.status)
    LOG["t"].append(res.x[-1] if res.status == 0 else np.nan)
    return res


KB.linprog = _wrapped


def my_face(G, idx):
    """(is_face, kind, quality): independent decision with a certificate in either direction."""
    N, D = G.shape; K = len(idx)
    GS = G[idx].astype(float)
    if K > D or np.linalg.matrix_rank(GS, tol=1e-9) < K:
        return False, "dependent", 0.0
    _, _, Vt = np.linalg.svd(GS, full_matrices=True)
    B = Vt[K:].T
    if B.shape[1] == 0:
        return False, "full", 0.0
    H = G.astype(float) @ B
    mask = np.ones(N, bool); mask[idx] = False
    Ho = H[mask]
    r = B.shape[1]
    res = linprog(np.zeros(r), A_ub=-Ho, b_ub=-np.ones(len(Ho)), bounds=[(None, None)] * r, method="highs")
    if res.status == 0:
        e = Ho @ res.x
        return True, "certificate", float(e.min() / np.abs(res.x).max())       # margin relative to |y|_inf = 1
    # Stiemke certificate of infeasibility: h >= 0, sum h = 1, Ho^T h = 0
    res2 = linprog(np.zeros(len(Ho)), A_eq=np.vstack([Ho.T, np.ones((1, len(Ho)))]),
                   b_eq=np.concatenate([np.zeros(r), [1.0]]), bounds=[(0, None)] * len(Ho), method="highs")
    if res2.status == 0:
        return False, "stiemke", float(np.abs(Ho.T @ res2.x).max())
    return None, f"undecided ({res.status},{res2.status})", np.nan


def setup(n, d, gaussian=False, seed=None):
    m = n - 1
    Z = KB.zstates(m); G = KB.monomials(Z, 2 * d)
    if gaussian:
        g = np.random.default_rng(seed)
        G = g.normal(size=G.shape).astype(np.float32); G[:, 0] = 1.0
    return G


def validate(n, d, Ks, trials):
    G = setup(n, d); N = G.shape[0]
    print(f"V. n = {n}, even order <= {2 * d}: {N} states, {G.shape[1]} features")
    for K in Ks:
        agree = dis = und = 0; margins = []; resid = []; t0 = time.time()
        LOG["status"].clear(); LOG["t"].clear(); tiny = 0; freq_div = freq_mine = 0
        for _ in range(trials):
            idx = rng.choice(N, size=K, replace=False)
            n_before = len(LOG["t"])
            ans, it = KB.is_face(G, idx)
            last_t = LOG["t"][-1] if len(LOG["t"]) > n_before else np.nan
            mine, kind, qual = my_face(G, idx)
            if mine is None or ans is None:
                und += 1; continue
            agree += ans == mine; dis += ans != mine
            freq_div += bool(ans); freq_mine += bool(mine)
            if mine:
                margins.append(qual)
            elif kind == "stiemke":
                resid.append(qual)
            if (not ans) and np.isfinite(last_t) and 0 < last_t <= 1e-7:
                tiny += 1
        bad_status = sum(s != 0 for s in LOG["status"])
        print(f"   K = {K}: {trials} supports; division's is_face = reviewer's decision in {agree}, different in {dis}, "
              f"undecided {und}; face frequency {freq_div / trials:.3f} (division) / {freq_mine / trials:.3f} (reviewer); "
              f"faces: smallest margin (|y| <= 1) {min(margins) if margins else float('nan'):.2e}; non-faces: largest "
              f"Stiemke residual {max(resid) if resid else float('nan'):.1e}; inside is_face: {len(LOG['status'])} LPs, "
              f"status != 0 in {bad_status}, 'not a face' with 0 < t <= 1e-7 in {tiny}   ({time.time() - t0:.0f} s)", flush=True)


def half_point(Ks, freqs, trials, boot=2000):
    Ks = np.array(Ks, float); f = np.array(freqs, float)
    def cross(ff):
        ff = np.minimum.accumulate(ff)                       # enforce monotone decrease
        for i in range(len(Ks) - 1):
            if ff[i] >= 0.5 > ff[i + 1]:
                return Ks[i] + (Ks[i + 1] - Ks[i]) * (ff[i] - 0.5) / (ff[i] - ff[i + 1])
        return np.nan
    est = cross(f.copy())
    g = np.random.default_rng(1)
    bs = [cross(g.binomial(trials, f) / trials) for _ in range(boot)]
    bs = np.array([b for b in bs if np.isfinite(b)])
    return est, np.percentile(bs, 2.5), np.percentile(bs, 97.5)


def thresholds(n, d, Ks, trials, clouds, Ks_g, per_cloud):
    G = setup(n, d); N = G.shape[0]
    print(f"T. n = {n}, even order <= {2 * d}: {N} states, {G.shape[1]} features (affine dimension {G.shape[1] - 1})")
    fr = []
    for K in Ks:
        c = 0
        for _ in range(trials):
            mine, kind, _ = my_face(G, rng.choice(N, size=K, replace=False)); c += bool(mine)
        fr.append(c / trials)
    est, lo, hi = half_point(Ks, fr, trials)
    print("   cube:     " + ", ".join(f"K={K}: {f:.3f}" for K, f in zip(Ks, fr)))
    print(f"   cube: frequency one half at K = {est:.1f}  (95% bootstrap interval {lo:.1f} .. {hi:.1f}; {trials} supports per K)")
    frg = np.zeros((clouds, len(Ks_g)))
    for c in range(clouds):
        Gg = setup(n, d, gaussian=True, seed=900 + c)
        for j, K in enumerate(Ks_g):
            frg[c, j] = np.mean([bool(my_face(Gg, rng.choice(N, size=K, replace=False))[0]) for _ in range(per_cloud)])
    fg = frg.mean(axis=0)
    estg, log_, hig = half_point(Ks_g, fg, clouds * per_cloud)
    per = [half_point(Ks_g, frg[c], per_cloud, boot=200)[0] for c in range(clouds)]
    print("   Gaussian: " + ", ".join(f"K={K}: {f:.3f}" for K, f in zip(Ks_g, fg)))
    print(f"   Gaussian: frequency one half at K = {estg:.1f}  (95% interval {log_:.1f} .. {hig:.1f}; {clouds} independent clouds x "
          f"{per_cloud} supports per K; single clouds give {np.nanmin(per):.1f} .. {np.nanmax(per):.1f})")
    print(f"   ratio cube / Gaussian = {est / estg:.3f}   (interval roughly {lo / hig:.3f} .. {hi / log_:.3f})")
    D = G.shape[1] - 1
    print(f"   Donoho-Tanner: delta = D/N = {D / N:.3f}; asymptotic formula D/(2 ln(N/D)) = {D / (2 * np.log(N / D)):.1f} "
          f"(the small-delta asymptote; at delta = 1/2 the exact weak threshold is 0.5581 D = {0.5581 * D:.1f})")


if __name__ == "__main__":
    what = sys.argv[1]
    if what == "V8":
        validate(8, 2, (65, 70, 75, 80, 85, 90), 60)
    elif what == "V10":
        validate(10, 2, (140, 150, 160, 170), 25)
    elif what == "V12pair":
        validate(12, 1, (10, 12, 13, 14, 16), 60)
    elif what == "V14pair":
        validate(14, 1, (13, 15, 17, 19), 25)
    elif what == "V12":
        validate(12, 2, (int(sys.argv[2]),), int(sys.argv[3]))
    elif what == "T8":
        thresholds(8, 2, list(range(66, 90, 2)), 200, 10, list(range(68, 92, 2)), 20)
    elif what == "T10":
        thresholds(10, 2, list(range(140, 168, 4)), 80, 6, list(range(130, 158, 4)), 14)
