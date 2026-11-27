#!/usr/bin/env python3
"""Science division — assumption-audit obligation G-5: what the certificate becomes for CONTINUOUS site variables.

Statement tested (addendum A17 (25), Proposition A17.24).  Site variables x_i in M_i with product reference
probability measures nu_i; cells C_{i,s} (s = 1..k) partitioning M_i; v_{i,s} = nu_i(C_{i,s}); <.>_s the product of
the nu_i conditioned on the cells of the discrete state s.  For an interaction V = sum_T V_T(x_T):

    Z = int e^{-V} d nu = sum_s  prod_i v_{i,s_i}  <e^{-V}>_s                                   (exact)
    <e^{-V}>_s >= exp( - sum_T mean_s V_T )                                                      (Jensen: lower end)
    <e^{-V}>_s <= exp( - sum_T R_T(s_T) + (1/8) sum_{i in H(s)} c_i(s)^2 )                       (upper end)

where every coordinate i is, depending on i and its cell only, in mode H ("bounded differences") or M ("minimum"):
R_T = the minimum of V_T over its M-coordinates in their cells, averaged over its H-coordinates; c_i(s) = the sum
over the terms T containing i of the oscillation of that reduced term in coordinate i inside the cell (the others
anywhere in their cells).  Proof of the upper end: V >= its minimum over the M-coordinates; then the
moment-generating-function bound for functions of independent variables with bounded differences (McDiarmid).
Both ends are discrete models on the interaction graph of V (the penalty couples the terms that share a site).
All M: the bracket from cell minima.  The bracket from cell minima and maxima is first order in the cell size,
Jensen / bounded differences second order.  One-body terms can be put into nu_i ("tilted reference"): they then
cost nothing.

Test model: an open chain of n angles, V = sum_i e_i(x_i) + sum_i V_i(x_i, x_{i+1}),
    e_i = 1.5 (1 + cos(3x + phi_i)),   V_i = J cos(x_i - x_{i+1} - theta_i) + W exp(-(2 - cos(x_i-a_i) - cos(x_{i+1}-b_i))/sigma^2),
energies in kT (beta = 1), random phases with a fixed seed.  The "continuum" is the periodic rectangle rule on Nf
points per angle, written cell by cell as a trapezoid rule on the m + 1 points of each CLOSED cell (end points
with weight one half, shared by two cells) — so the reference measure inside a cell is a probability measure whose
support contains both end points of the cell, and oscillations over its support are those of the closed cell up
to the resolution of the grid.  Every inequality above holds EXACTLY for this grid model (a product measure inside
every cell), so the assertions below test the statement with no quadrature error; the grid model itself is
compared with the grid of 2 Nf points and the difference printed.

Controls that can fail: (1) with every coordinate in mode M the upper end must equal the bracket from cell minima;
(2) the Jensen value used as an UPPER end must be violated in every case with a coupling; (3) the grid of 2 Nf.
Run:  python3 -B continuous_cells.py > continuous_cells.log
"""
import sys, time, resource
import numpy as np
from scipy.special import logsumexp

t0 = time.time()
TOL = 1e-10


def build(n, J, W, sigma, seed, Nf):
    rng = np.random.default_rng(seed)
    phi = rng.uniform(0, 2 * np.pi, n); theta = rng.uniform(0, 2 * np.pi, n - 1)
    a = rng.uniform(0, 2 * np.pi, n - 1); b = rng.uniform(0, 2 * np.pi, n - 1)
    x = np.arange(Nf) * 2 * np.pi / Nf
    e = [1.5 * (1 + np.cos(3 * x + phi[i])) for i in range(n)]

    def pair(i):
        X, Y = np.meshgrid(x, x, indexing="ij")
        v = J * np.cos(X - Y - theta[i])
        if W:
            v = v + W * np.exp(-((1 - np.cos(X - a[i])) + (1 - np.cos(Y - b[i]))) / sigma ** 2)
        return v
    return e, pair


def lnZ_grid(e, pair, n):
    Nf = len(e[0]); m = -e[0] - np.log(Nf)
    for i in range(n - 1):
        m = logsumexp(m[:, None] - pair(i), axis=0) - e[i + 1] - np.log(Nf)
    return float(logsumexp(m))


class Cells:
    """cell tables of one instance for k cells per angle; reference 'tilted' (one-body terms in the measure) or 'uniform'"""

    def __init__(self, e, pair, n, k, ref):
        Nf = len(e[0]); assert Nf % k == 0
        m = Nf // k; self.n, self.k, self.ref = n, k, ref
        idx = (np.arange(k)[:, None] * m + np.arange(m + 1)[None, :]) % Nf      # the m + 1 grid points of each closed cell
        trap = np.full(m + 1, 1.0 / m); trap[0] = trap[-1] = 0.5 / m             # trapezoid weights inside a cell (sum 1)
        self.lv, self.P = [], []          # log cell weights; conditional probabilities inside the cells (k, m + 1)
        self.e_mean, self.e_min, self.e_max, self.e_osc = [], [], [], []
        for i in range(n):
            ec = e[i][idx]
            if ref == "tilted":
                lw = -ec + np.log(trap)[None, :] - np.log(k); lvi = logsumexp(lw, axis=1)
                self.lv.append(lvi); self.P.append(np.exp(lw - lvi[:, None]))
                z = np.zeros(k); self.e_mean.append(z); self.e_min.append(z); self.e_max.append(z); self.e_osc.append(z)
            else:
                self.lv.append(np.full(k, -np.log(k))); self.P.append(np.tile(trap, (k, 1)))
                self.e_mean.append(ec @ trap); self.e_min.append(ec.min(axis=1)); self.e_max.append(ec.max(axis=1))
                self.e_osc.append(ec.max(axis=1) - ec.min(axis=1))
        self.T = []
        for i in range(n - 1):
            Vc = pair(i)[idx[:, :, None, None], idx[None, None, :, :]]; P, Q = self.P[i], self.P[i + 1]
            d = {}
            d["mean"] = np.einsum("sa,satb,tb->st", P, Vc, Q)
            d["O1_HH"] = (Vc.max(axis=1) - Vc.min(axis=1)).max(axis=2)          # oscillation in x_i, sup over x_{i+1} in its cell
            d["O2_HH"] = (Vc.max(axis=3) - Vc.min(axis=3)).max(axis=1)          # oscillation in x_{i+1}, sup over x_i in its cell
            Vr = Vc.min(axis=1)                                                   # (s, t, b): minimum over x_i in its cell
            d["R_MH"] = np.einsum("stb,tb->st", Vr, Q); d["O2_MH"] = Vr.max(axis=2) - Vr.min(axis=2)
            Vr2 = Vc.min(axis=3)                                                  # (s, a, t): minimum over x_{i+1} in its cell
            d["R_HM"] = np.einsum("sat,sa->st", Vr2, P); d["O1_HM"] = Vr2.max(axis=1) - Vr2.min(axis=1)
            d["min"] = Vc.min(axis=(1, 3)); d["max"] = Vc.max(axis=(1, 3))
            self.T.append(d)
        # the largest penalty argument a coordinate can meet in its cell (used only to choose modes)
        self.cmax = []
        for i in range(n):
            c = self.e_osc[i].copy()
            if i > 0: c = c + self.T[i - 1]["O2_HH"].max(axis=0)
            if i < n - 1: c = c + self.T[i]["O1_HH"].max(axis=1)
            self.cmax.append(c)

    def chain(self, R, lv_eff, pen0=None, pens=None, penN=None):
        """ln of sum_s exp(sum_i lv_eff_i[s_i] - sum_i R_i[s_i,s_{i+1}] + penalties); penalties: pen0[s0,s1],
        pens[i][s_{i-1}, s_i, s_{i+1}] for 1 <= i <= n-2 (callables, to save memory), penN[s_{n-2}, s_{n-1}]"""
        n = self.n
        F = lv_eff[0][:, None] + lv_eff[1][None, :] - R[0]
        if pen0 is not None: F = F + pen0
        for i in range(1, n - 1):
            if pens is None:
                G = logsumexp(F, axis=0)[:, None]
            else:
                G = logsumexp(F[:, :, None] + pens(i), axis=0)
            F = G + lv_eff[i + 1][None, :] - R[i]
        if penN is not None: F = F + penN
        return float(logsumexp(F))

    def jensen(self):
        return self.chain([d["mean"] for d in self.T], [self.lv[i] - self.e_mean[i] for i in range(self.n)])

    def first_order(self):
        lo = self.chain([d["max"] for d in self.T], [self.lv[i] - self.e_max[i] for i in range(self.n)])
        hi = self.chain([d["min"] for d in self.T], [self.lv[i] - self.e_min[i] for i in range(self.n)])
        return lo, hi

    def upper(self, thr):
        """upper end with coordinate (i, s) in mode M iff cmax_i[s] > thr"""
        n, k = self.n, self.k
        M = [self.cmax[i] > thr for i in range(n)]
        key = b"".join(x.tobytes() for x in M)
        if not hasattr(self, "cache"): self.cache = {}
        if key in self.cache: return self.cache[key]
        R, A, B = [], [None] * n, [None] * n      # A[i+1]: oscillation that term i contributes to site i+1; B[i]: to site i
        for i, d in enumerate(self.T):
            mi, mj = M[i][:, None], M[i + 1][None, :]
            R.append(np.where(mi, np.where(mj, d["min"], d["R_MH"]), np.where(mj, d["R_HM"], d["mean"])))
            A[i + 1] = np.where(mj, 0.0, np.where(mi, d["O2_MH"], d["O2_HH"]))
            B[i] = np.where(mi, 0.0, np.where(mj, d["O1_HM"], d["O1_HH"]))
        lv_eff = [self.lv[i] - np.where(M[i], self.e_min[i], self.e_mean[i]) for i in range(n)]
        H = [(~M[i]).astype(float) for i in range(n)]
        pen0 = H[0][:, None] * (B[0] + self.e_osc[0][:, None]) ** 2 / 8
        penN = H[n - 1][None, :] * (A[n - 1] + self.e_osc[n - 1][None, :]) ** 2 / 8

        def pens(i):
            return H[i][None, :, None] * (A[i][:, :, None] + B[i][None, :, :] + self.e_osc[i][None, :, None]) ** 2 / 8
        self.cache[key] = (self.chain(R, lv_eff, pen0, pens, penN), [int(x.sum()) for x in M])
        return self.cache[key]


def run_case(name, n, J, W, sigma, seed, ks, ref, Nf=1440, thrs=(np.inf, 6, 4, 3, 2, 1.5, 1, 0.5, -1.0)):
    e, pair = build(n, J, W, sigma, seed, Nf)
    ex = lnZ_grid(e, pair, n)
    e2, pair2 = build(n, J, W, sigma, seed, 2 * Nf)
    ex2 = lnZ_grid(e2, pair2, n)
    print(f"\n=== {name}: n = {n}, J = {J}, wall W = {W} (sigma {sigma}), reference {ref}, seed {seed}; grid of {Nf} points per angle: ln Z = {ex:.10f}; grid of {2*Nf}: {ex2:.10f} (difference {ex2-ex:+.1e})")
    print("   k  cell   first-order bracket (minima/maxima)   second-order bracket (Jensen / bounded differences)    exact at   mixed rule: best upper end   threshold  M-cells   widths per site: first   second   mixed")
    rows = []
    for k in ks:
        C = Cells(e, pair, n, k, ref)
        lo1, hi1 = C.first_order(); jl = C.jensen()
        ups = {}
        for thr in thrs:
            ups[thr] = C.upper(thr)
        hH = ups[np.inf][0]; hM = ups[-1.0][0]
        # controls and assertions
        assert abs(hM - hi1) < 1e-9 * max(1.0, abs(hi1)), ("control 1: all coordinates in mode M must give the bracket from minima", hM, hi1)
        assert lo1 <= ex + TOL and ex <= hi1 + TOL, ("first-order bracket violated", lo1, ex, hi1)
        assert jl <= ex + TOL, ("Jensen end violated", jl, ex)
        for thr, (val, _) in ups.items():
            assert ex <= val + TOL, ("upper end violated", thr, val, ex)
        assert lo1 <= jl + TOL, "the Jensen end must be at least the end from maxima"
        viol = ex > jl + 1e-12                    # control 2: Jensen value as an upper end
        best_thr = min(ups, key=lambda t: ups[t][0]); best, Mc = ups[best_thr]
        pos = (ex - jl) / (hH - jl) if hH > jl else float("nan")
        rows.append(dict(k=k, w1=hi1 - lo1, w2=hH - jl, wm=best - jl, pos=pos, viol=viol, thr=best_thr, up1=hi1 - ex, upH=hH - ex, upm=best - ex, lo1=ex - lo1, loJ=ex - jl))
        thr_s = "all H" if best_thr == np.inf else ("all M" if best_thr == -1.0 else f"{best_thr:g}")
        print(f"{k:4d} {360/k:5.1f}  [{lo1:12.6f}, {hi1:12.6f}] {hi1-lo1:9.2e}   [{jl:12.6f}, {hH:12.6f}] {hH-jl:9.2e}   {pos:6.3f}    {best:12.6f} {best-jl:9.2e}   {thr_s:>6s}  {sum(Mc):5d}/{n*k:<5d}   {(hi1-lo1)/n:9.2e} {(hH-jl)/n:9.2e} {(best-jl)/n:9.2e}"
              + ("" if viol else "   [control 2 NOT violated]"))
    return dict(name=name, n=n, rows=rows, ex=ex, quad=ex2 - ex)


def slope(rows, key, k1, k2):
    r = {x["k"]: x for x in rows}
    return np.log(r[k2][key] / r[k1][key]) / np.log(k2 / k1)


def k_needed(rows, key, n, target):
    """cells per angle at which the width per site reaches the target: log-log interpolation between computed points; extrapolated if beyond"""
    ks = [x["k"] for x in rows]; w = [x[key] / n for x in rows]
    for j in range(len(ks) - 1):
        if w[j] > target >= w[j + 1]:
            s = np.log(w[j + 1] / w[j]) / np.log(ks[j + 1] / ks[j])
            return ks[j] * (target / w[j]) ** (1 / s), "interpolated"
    if w[-1] > target:
        s = np.log(w[-1] / w[-2]) / np.log(ks[-1] / ks[-2])
        return ks[-1] * (target / w[-1]) ** (1 / s), "EXTRAPOLATED"
    return ks[0], "reached at the coarsest partition"


KS = (3, 6, 12, 24, 48, 96, 144)
out = {}
out["A"] = run_case("A  smooth, tilted reference", 8, 2.0, 0.0, 0.6, 20261126, KS + (288,), "tilted", Nf=1440)
out["Au"] = run_case("Au smooth, uniform reference (one-body terms inside V)", 8, 2.0, 0.0, 0.6, 20261126, KS, "uniform")
out["B"] = run_case("B  wall of 20 kT between neighbours, tilted reference", 8, 2.0, 20.0, 0.6, 20261126, KS, "tilted")
out["B5"] = run_case("B5 wall of 5 kT, tilted reference", 8, 2.0, 5.0, 0.6, 20261126, KS, "tilted")
for J in (0.5, 1.0, 4.0):
    out[f"J{J}"] = run_case(f"coupling scan J = {J}, smooth, tilted reference", 8, J, 0.0, 0.6, 20261126, (24, 48, 96), "tilted")
out["n16"] = run_case("length scan n = 16, smooth, tilted reference", 16, 2.0, 0.0, 0.6, 20261126, (24, 48, 96), "tilted")

print("\n=== summary against the predictions of 21:53 UTC (research log)")
A, B = out["A"], out["B"]
s1 = slope(A["rows"], "w1", 24, 96); s2 = slope(A["rows"], "w2", 24, 96)
print(f"(i)   exponents between k = 24 and 96, case A: first-order width {s1:+.3f} (predicted within 0.1 of -1: {'met' if abs(s1+1) <= 0.1 else 'MISSED'}); second-order width {s2:+.3f} (predicted within 0.15 of -2: {'met' if abs(s2+2) <= 0.15 else 'MISSED'})")
pos = [(x["k"], x["pos"]) for x in A["rows"] if x["k"] >= 24]
okp = all(0.15 <= p <= 0.34 for _, p in pos)
print(f"(ii)  position of the exact value in the second-order bracket, k >= 24: " + ", ".join(f"{k}: {p:.3f}" for k, p in pos) + f"  (predicted 0.15 to 0.34: {'met' if okp else 'MISSED'})")
r24 = [x for x in A["rows"] if x["k"] == 24][0]
kn, how = k_needed(A["rows"], "w2", A["n"], 1e-3)
ok3 = (0.02 <= r24["w2"] / A["n"] <= 0.15) and (100 <= kn <= 300)
print(f"(iii) case A at k = 24: second-order width per site {r24['w2']/A['n']:.4f} nats (predicted 0.02 to 0.15); 1e-3 nats per site at k = {kn:.0f} cells per angle [{how}] (predicted 100 to 300): {'met' if ok3 else 'MISSED'}")
bw = {x["k"]: x for x in B["rows"]}; aw = {x["k"]: x for x in A["rows"]}
part1 = all(bw[k]["w2"] > bw[k]["w1"] for k in (3, 6, 12, 24))
ratio = bw[96]["wm"] / aw[96]["w2"]
print(f"(iv)  wall of 20 kT: bounded differences alone wider than minima/maxima at every k <= 24: {part1}; mixed rule at k = 96: width {bw[96]['wm']:.3e} against {aw[96]['w2']:.3e} without the wall, ratio {ratio:.2f} (predicted at most 3): {'met' if (part1 and ratio <= 3) else 'MISSED'}")
print("\n=== scalings (not predicted)")
for J in (0.5, 1.0, 4.0):
    r = {x["k"]: x for x in out[f"J{J}"]["rows"]}
    print(f"coupling J = {J}: second-order width at k = 48: {r[48]['w2']:.3e}; divided by J^2: {r[48]['w2']/J**2:.3e}; position of the exact value {r[48]['pos']:.3f}")
print(f"coupling J = 2.0: second-order width at k = 48: {aw[48]['w2']:.3e}; divided by J^2: {aw[48]['w2']/4:.3e}")
r16 = {x["k"]: x for x in out["n16"]["rows"]}
print(f"length: second-order width per site at k = 48: n = 8: {aw[48]['w2']/8:.3e}; n = 16: {r16[48]['w2']/16:.3e}")
u = {x["k"]: x for x in out["Au"]["rows"]}
print(f"reference: second-order width at k = 48: tilted {aw[48]['w2']:.3e}, uniform {u[48]['w2']:.3e} (ratio {u[48]['w2']/aw[48]['w2']:.2f})")
nv = sum(1 for o in out.values() for x in o["rows"] if not x["viol"]); nt = sum(len(o["rows"]) for o in out.values())
print(f"\ncontrols: (1) all-M equals the bracket from minima in all {nt} partitions (asserted); (2) the Jensen value as an upper end is violated in {nt-nv} of {nt}; (3) largest difference between the grid and the grid of twice as many points: {max(abs(o['quad']) for o in out.values()):.1e}")
print(f"every bracket contains the grid value in all {nt} partitions and for every threshold (asserted)")
print(f"ALL DONE  {time.time()-t0:.1f} s  peak memory {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024:.0f} MB")
