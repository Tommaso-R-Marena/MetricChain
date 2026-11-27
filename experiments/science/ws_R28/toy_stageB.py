"""R28 — stage B of the toy-chain replication: MY code (toy_lib.py) on THEIR instance.

Only the specification is taken from continuous_cells.py: the instance (seed 20261126; draws in the
order phi (n), theta (n-1), a (n-1), b (n-1), uniform on [0, 2 pi)); one-body terms
1.5 (1 + cos(3x + phi_i)); pair terms J cos(x_i - x_{i+1} - theta_i)
+ W exp(-(2 - cos(x_i - a_i) - cos(x_{i+1} - b_i)) / sigma^2), sigma = 0.6; the threshold rule
"(i, cell) in mode M iff cmax > thr" for thr in (inf, 6, 4, 3, 2, 1.5, 1, 0.5, -1); the eight cases.

Then every number of their log (continuous_cells.log) is compared with mine, entry by entry.
Extras (adversarial): local search over modes; controls.
"""
import r28_common as rc
rc.cap()
import re
import sys
import time
import numpy as np
import toy_lib as tl

t0 = time.time()
print("R28 toy_stageB.py  start", rc.utc())
LOG = "/home/user/MetricChain/experiments/science/pi_inference/continuous_cells.log"
THRS = (np.inf, 6, 4, 3, 2, 1.5, 1, 0.5, -1.0)
N = 1440


def instance(n, J, W, sigma, seed, N, phi_zero=False):
    rng = np.random.default_rng(seed)
    phi = rng.uniform(0, 2 * np.pi, n)
    theta = rng.uniform(0, 2 * np.pi, n - 1)
    a = rng.uniform(0, 2 * np.pi, n - 1)
    b = rng.uniform(0, 2 * np.pi, n - 1)
    if phi_zero:
        phi = np.zeros(n)
    x = tl.grid(N)
    e = [1.5 * (1.0 + np.cos(3.0 * x + phi[i])) for i in range(n)]
    pair = []
    for i in range(n - 1):
        v = J * np.cos(x[:, None] - x[None, :] - theta[i])
        if W:
            v = v + W * np.exp(-((1 - np.cos(x[:, None] - a[i])) + (1 - np.cos(x[None, :] - b[i]))) / sigma ** 2)
        pair.append(v)
    return e, pair


# ------------------------------------------------------------------ their log, parsed
row_re = re.compile(
    r"^\s*(\d+)\s+([\d.]+)\s+\[\s*([-\d.]+),\s*([-\d.]+)\]\s+([\d.e+-]+)\s+\[\s*([-\d.]+),\s*([-\d.]+)\]\s+([\d.e+-]+)"
    r"\s+([\d.]+|nan)\s+([-\d.]+)\s+([\d.e+-]+)\s+(all H|all M|[\d.]+)\s+(\d+)/(\d+)\s+([\d.e+-]+)\s+([\d.e+-]+)\s+([\d.e+-]+)")
theirs = {}
cur = None
for line in open(LOG):
    if line.startswith("==="):
        m = re.match(r"=== (.*?): n = (\d+), J = ([\d.]+), wall W = ([\d.]+) \(sigma ([\d.]+)\), reference (\w+), seed (\d+);"
                     r" grid of (\d+) points per angle: ln Z = ([-\d.]+); grid of (\d+): ([-\d.]+)", line)
        if m:
            cur = (int(m.group(2)), float(m.group(3)), float(m.group(4)), m.group(6))
            theirs[cur] = dict(name=m.group(1), lnZ=float(m.group(9)), rows={})
        else:
            cur = None
        continue
    m = row_re.match(line)
    if m and cur is not None:
        g = m.groups()
        theirs[cur]["rows"][int(g[0])] = dict(lo1=float(g[2]), hi1=float(g[3]), jl=float(g[5]), hH=float(g[6]),
                                              pos=float(g[8]), best=float(g[9]), thr=g[11], Mc=int(g[12]),
                                              w1=float(g[14]), w2=float(g[15]), wm=float(g[16]))
print("cases parsed from their log:", len(theirs), " partitions:", sum(len(v["rows"]) for v in theirs.values()))

cases = [
    ("A  smooth, tilted", 8, 2.0, 0.0, "tilted", (3, 6, 12, 24, 48, 96, 144, 288)),
    ("Au smooth, uniform", 8, 2.0, 0.0, "uniform", (3, 6, 12, 24, 48, 96, 144)),
    ("B  wall 20, tilted", 8, 2.0, 20.0, "tilted", (3, 6, 12, 24, 48, 96, 144)),
    ("B5 wall 5, tilted", 8, 2.0, 5.0, "tilted", (3, 6, 12, 24, 48, 96, 144)),
    ("J = 0.5", 8, 0.5, 0.0, "tilted", (24, 48, 96)),
    ("J = 1.0", 8, 1.0, 0.0, "tilted", (24, 48, 96)),
    ("J = 4.0", 8, 4.0, 0.0, "tilted", (24, 48, 96)),
    ("n = 16", 16, 2.0, 0.0, "tilted", (24, 48, 96)),
]

n_cmp = 0
n_disagree = 0
maxdiff_ends = 0.0
n_brackets = 0
viol = 0
ctrl_jensen_upper = 0
ctrl_min_lower = 0
ctrl_small = {0.5: 0, 0.3: 0, 0.1: 0}
n_part = 0
mine = {}
for name, n, J, W, ref, ks in cases:
    e, pair = instance(n, J, W, 0.6, 20261126, N)
    if ref == "tilted":
        ch = tl.Chain([np.exp(-ee) for ee in e], pair, None)
        shift = sum(np.log(np.exp(-ee).mean()) for ee in e)     # ln of the normalisation of the tilted reference
    else:
        ch = tl.Chain([np.ones(N)] * n, pair, e)
        shift = 0.0
    ex = ch.lnZ_exact() + shift
    th = theirs[(n, J, W, ref)]
    print(f"\n=== {name}: n = {n}, J = {J}, W = {W}, reference {ref}:  my ln Z = {ex:.10f}   theirs {th['lnZ']:.10f}"
          f"   difference {ex - th['lnZ']:+.1e}")
    n_cmp += 1
    if abs(ex - th["lnZ"]) > 6e-11:
        n_disagree += 1
    print("   k   mine: lo1, hi1 | Jensen, all-H | pos | best (thr, M-cells) | widths per site first, second, mixed"
          "   || max |mine - theirs| over the 5 ends;  thr/M-cells equal;  local search (mixed width per site)")
    mine[(n, J, W, ref)] = {}
    for k in ks:
        idx, tw = tl.cell_index(N, k)
        cs = tl.Cells(ch, idx, tw)
        lj = cs.lnZ_jensen() + shift
        lmin = cs.lnZ_minima() + shift
        lmax = cs.lnZ_maxima() + shift
        ups = {}
        for thr in THRS:
            H = cs.modes_by_threshold(thr)
            ups[thr] = (cs.lnZ_upper(H) + shift, int(sum((~h).sum() for h in H)))
            n_brackets += 1
            if not (lj <= ex + 1e-10 and ex <= ups[thr][0] + 1e-10):
                viol += 1
        lH = ups[np.inf][0]
        lM = ups[-1.0][0]
        assert abs(lM - lmin) < 1e-9 * max(1.0, abs(lmin))
        if not (lmax <= ex + 1e-10 <= lmin + 2e-10):
            viol += 1
        best_thr = min(ups, key=lambda t: ups[t][0])
        best, Mc = ups[best_thr]
        pos = (ex - lj) / (lH - lj)
        thr_s = "all H" if best_thr == np.inf else ("all M" if best_thr == -1.0 else f"{best_thr:g}")
        # local search over modes for small k
        ls = float("nan")
        if k <= 12:
            H = [h.copy() for h in cs.modes_by_threshold(best_thr)]
            curv = cs.lnZ_upper(H)
            improved, sweeps = True, 0
            while improved and sweeps < 6:
                improved = False
                sweeps += 1
                for i in range(n):
                    for c in range(k):
                        H[i][c] = not H[i][c]
                        new = cs.lnZ_upper(H)
                        n_brackets += 1
                        if not (ex <= new + shift + 1e-10):
                            viol += 1
                        if new < curv - 1e-12:
                            curv, improved = new, True
                        else:
                            H[i][c] = not H[i][c]
            ls = (curv + shift - lj) / n
        # controls
        n_part += 1
        if lj < ex - 1e-12:
            ctrl_jensen_upper += 1
        if lmin > ex + 1e-12:
            ctrl_min_lower += 1
        for f in ctrl_small:
            if ex > cs.lnZ_upper(cs.all_H(), scale=f) + shift:
                ctrl_small[f] += 1
        # comparison with their row
        t = th["rows"][k]
        dends = max(abs(lmax - t["lo1"]), abs(lmin - t["hi1"]), abs(lj - t["jl"]), abs(lH - t["hH"]), abs(best - t["best"]))
        maxdiff_ends = max(maxdiff_ends, dends)
        same_thr = (thr_s == t["thr"]) and (Mc == t["Mc"])
        wd = [(lmin - lmax) / n, (lH - lj) / n, (best - lj) / n]
        rel = max(abs(wd[0] / t["w1"] - 1), abs(wd[1] / t["w2"] - 1), abs(wd[2] / t["wm"] - 1))
        okrow = dends < 1.0e-6 and same_thr and rel < 6e-3 and abs(pos - t["pos"]) < 6e-4
        n_cmp += 1
        if not okrow:
            n_disagree += 1
        mine[(n, J, W, ref)][k] = dict(w1=wd[0], w2=wd[1], wm=wd[2], pos=pos, ls=ls, jl=lj, ex=ex, lH=lH, best=best)
        print(f"{k:4d}  [{lmax:.6f}, {lmin:.6f}] | [{lj:.6f}, {lH:.6f}] | {pos:.3f} | {best:.6f} ({thr_s}, {Mc}/{n*k}) |"
              f" {wd[0]:.3e} {wd[1]:.3e} {wd[2]:.3e}   || {dends:.1e};  {same_thr};  {ls:.4g}"
              + ("" if okrow else "   <-- DISAGREES with their row"))
        sys.stdout.flush()

print()
print(f"ENTRY-BY-ENTRY: {n_cmp} items compared (8 exact values + 41 rows); disagreements: {n_disagree};"
      f" largest |mine - theirs| over the 205 bracket ends: {maxdiff_ends:.1e} (their print has 6 decimals)")
print(f"brackets checked {n_brackets}; excluding the exact value: {viol} (must be 0)")
print(f"CONTROL Jensen value as an upper end: violated in {ctrl_jensen_upper} of {n_part}")
print(f"CONTROL cell minima as a lower end: violated (above exact) in {ctrl_min_lower} of {n_part}")
for f in (0.5, 0.3, 0.1):
    print(f"CONTROL all-H with oscillations x {f}: exact value excluded in {ctrl_small[f]} of {n_part} partitions")

A = mine[(8, 2.0, 0.0, "tilted")]
B = mine[(8, 2.0, 20.0, "tilted")]
s1 = np.log(A[96]["w1"] / A[24]["w1"]) / np.log(4)
s2 = np.log(A[96]["w2"] / A[24]["w2"]) / np.log(4)
print(f"\nderived numbers of item 98 from MY values:")
print(f"  exponents 24..96: {s1:+.4f} and {s2:+.4f}   (text: -1.005 and -2.148)")
print("  position of the exact value, k = 24..288: " + ", ".join(f"{k}: {A[k]['pos']:.4f}" for k in (24, 48, 96, 144, 288))
      + "   (text: 0.14 to 0.21)")
sa = np.log(A[96]["w2"] / A[144]["w2"]) / np.log(144 / 96)
kext = 144 * (A[144]["w2"] / 1e-3) ** (1 / sa)
sb = np.log(A[144]["w2"] / A[288]["w2"]) / np.log(2)
kint = 144 * (A[144]["w2"] / 1e-3) ** (1 / sb)
print(f"  cells for 1e-3 nats per angle: {kint:.1f} by log-log interpolation between 144 and 288 (what their script does);"
      f" {kext:.1f} by the power law through 96 and 144 (an extrapolation beyond 144); width at 144 = {A[144]['w2']:.4e} > 1e-3")
n16 = mine[(16, 2.0, 0.0, "tilted")]
print(f"  length: width per angle at 48 cells: n = 8: {A[48]['w2']:.4e}; n = 16: {n16[48]['w2']:.4e}  (text: 0.0103, 0.0097)")
for J in (0.5, 1.0, 2.0, 4.0):
    r = A if J == 2.0 else mine[(8, J, 0.0, "tilted")]
    print(f"  J = {J}: all-H width PER ANGLE at 48 cells {r[48]['w2']:.4e}; per angle / J^2 = {r[48]['w2']/J**2:.4e};"
          f" TOTAL (8 angles) / J^2 = {8*r[48]['w2']/J**2:.4e}")
print("  (text: 'width over J^2: 0.027, 0.025, 0.021, 0.015' in a sentence whose subject is the width per angle)")
Au = mine[(8, 2.0, 0.0, "uniform")]
print(f"  uniform / tilted reference at 48 cells: {Au[48]['w2']/A[48]['w2']:.3f}  (text: 4.7);"
      f" at other k: " + ", ".join(f"{k}: {Au[k]['w2']/A[k]['w2']:.2f}" for k in (3, 6, 12, 24, 96, 144)))
print("  wall 20 kT, all-H width per angle at 3, 6, 12, 24: " + ", ".join(f"{B[k]['w2']:.3g}" for k in (3, 6, 12, 24))
      + ";  first-order: " + ", ".join(f"{B[k]['w1']:.3g}" for k in (3, 6, 12, 24)) + "  (text: 80, 38, 7.7 useless; false at 24)")
print(f"  wall / no wall, mixed width at 96 cells: {B[96]['wm']/A[96]['w2']:.3f}  (text: 1.31)")
print("  local search over modes against the threshold rule (mixed width per angle):")
for key, lab in (((8, 2.0, 0.0, "tilted"), "A"), ((8, 2.0, 0.0, "uniform"), "Au"), ((8, 2.0, 20.0, "tilted"), "B"), ((8, 2.0, 5.0, "tilted"), "B5")):
    r = mine[key]
    print(f"    case {lab}: " + ", ".join(f"k = {k}: threshold {r[k]['wm']:.4g} -> local search {r[k]['ls']:.4g}" for k in (3, 6, 12)))
rc.finish(t0)
