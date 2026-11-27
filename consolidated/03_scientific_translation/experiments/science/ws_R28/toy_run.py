"""R28 — replication of the toy chain of item 98 with my own code (toy_lib.py).

Usage:  python3 -B toy_run.py --phases own:<seed> | file:<path.npy>   [--wall SPEC] [--tag TAG]

Stage A (own phases) was run BEFORE the script under review was opened; stage B uses the phases and
the wall formula read from that script (specification only), supplied through files/arguments.

Per angle widths of the bracket for ln Z; one-body terms 1.5(1+cos 3x) in the reference measure
unless stated.  Controls are counted and printed with their violations.
"""
import r28_common as rc
rc.cap()
import argparse
import sys
import time
import numpy as np
import toy_lib as tl

t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("--phases", default="own:28")
ap.add_argument("--n", type=int, default=8)
ap.add_argument("--J", type=float, default=2.0)
ap.add_argument("--N", type=int, default=1440)
ap.add_argument("--ks", default="3,6,12,24,48,96,144,288")
ap.add_argument("--wall", default="none",
                help="none | cos:<W>:<p>  -> W*((1+cos(xi-xj-phi))/2)^p   (phi from --wallphase)")
ap.add_argument("--wallphase", default="0")
ap.add_argument("--reference", default="tilted", choices=["tilted", "uniform"])
ap.add_argument("--search", type=int, default=1, help="local search over modes for k <= 12")
args = ap.parse_args()
print("R28 toy_run.py  start", rc.utc(), " args:", vars(args))

n, J, N = args.n, args.J, args.N
x = tl.grid(N)
if args.phases.startswith("own:"):
    rng = np.random.default_rng(int(args.phases.split(":")[1]))
    theta = rng.uniform(0.0, 2.0 * np.pi, size=n - 1)
else:
    theta = np.load(args.phases.split(":", 1)[1])
    assert len(theta) == n - 1
print("phases theta_i:", np.array2string(theta, precision=6))

e1 = 1.5 * (1.0 + np.cos(3.0 * x))
d = x[:, None] - x[None, :]


def wall_term(i):
    if args.wall == "none":
        return 0.0
    kind, W, p = args.wall.split(":")
    W, p = float(W), float(p)
    ph = np.load(args.wallphase)[i] if args.wallphase.endswith(".npy") else float(args.wallphase)
    return W * ((1.0 + np.cos(d - ph)) / 2.0) ** p


pair = [J * np.cos(d - theta[i]) + wall_term(i) for i in range(n - 1)]
if args.reference == "tilted":
    chain = tl.Chain([np.exp(-e1)] * n, pair, None)
else:
    chain = tl.Chain([np.ones(N)] * n, pair, [e1] * n)
ex = chain.lnZ_exact()
print(f"exact ln of the reference-normalised integral on the {N}-point grid: {ex:.12f}")

ks = [int(a) for a in args.ks.split(",")]
rows = []
viol_bracket = 0          # any bracket that excludes the exact value (must be 0)
n_brackets = 0
ctrl_small_osc = {}       # control: oscillation x f  -> list of k where the exact value is excluded
ctrl_minima_as_lower = 0  # control: cell minima used as a lower end -> must exceed the exact value
ctrl_jensen_as_upper = 0
print()
print(" k   cell   first-order   all-H        all-M(up)/Jensen  best-threshold (tau, #H cells)   "
      "local-search   position(all-H)  position(best)")
for k in ks:
    idx, tw = tl.cell_index(N, k)
    cs = tl.Cells(chain, idx, tw)
    lj = cs.lnZ_jensen()
    lmin = cs.lnZ_minima()
    lmax = cs.lnZ_maxima()
    lH = cs.lnZ_upper(cs.all_H())
    lM = cs.lnZ_upper(cs.all_M())
    assert abs(lM - lmin) < 1e-9 * max(1.0, abs(lM)), (lM, lmin)     # all-M reproduces cell minima
    # thresholds
    q = np.concatenate(cs.cmax_allH())
    taus = np.unique(np.concatenate([[0.0], np.quantile(q, np.linspace(0, 1, 41)), [np.inf]]))
    best = (lM, 0.0, 0)
    for tau in taus:
        H = cs.modes_by_threshold(tau)
        lu = cs.lnZ_upper(H)
        n_brackets += 1
        if not (lj <= ex + 1e-11 and ex <= lu + 1e-11):
            viol_bracket += 1
        if lu < best[0]:
            best = (lu, tau, int(sum(h.sum() for h in H)))
    for lu in (lH, lM):
        n_brackets += 1
        if not (lj <= ex + 1e-11 and ex <= lu + 1e-11):
            viol_bracket += 1
    if not (lmax <= ex + 1e-11):
        viol_bracket += 1
    # local search over modes (coordinate descent), small k only
    ls = float("nan")
    if args.search and k <= 12:
        H = [h.copy() for h in cs.modes_by_threshold(best[1])]
        cur = cs.lnZ_upper(H)
        improved = True
        sweeps = 0
        while improved and sweeps < 6:
            improved = False
            sweeps += 1
            for i in range(n):
                for c in range(k):
                    H[i][c] = not H[i][c]
                    new = cs.lnZ_upper(H)
                    n_brackets += 1
                    if not (ex <= new + 1e-11):
                        viol_bracket += 1
                    if new < cur - 1e-12:
                        cur = new
                        improved = True
                    else:
                        H[i][c] = not H[i][c]
        ls = (cur - lj) / n
    # controls
    for f in (0.5, 0.3, 0.1):
        lu = cs.lnZ_upper(cs.all_H(), scale=f)
        if ex > lu:
            ctrl_small_osc.setdefault(f, []).append(k)
    if lmin > ex:
        ctrl_minima_as_lower += 1
    if lj < ex:
        ctrl_jensen_as_upper += 1
    w1 = (lmin - lmax) / n
    wH = (lH - lj) / n
    wM = (lM - lj) / n
    wB = (best[0] - lj) / n
    posH = (ex - lj) / (lH - lj)
    posB = (ex - lj) / (best[0] - lj)
    rows.append((k, w1, wH, wM, wB, ls, posH, posB, (ex - lj) / n, (lmin - ex) / n))
    print(f"{k:4d} {360.0/k:6.2f}  {w1:11.4g}  {wH:11.4g}  {wM:11.4g}      {wB:11.4g} ({best[1]:.3g}, {best[2]})"
          f"   {ls:11.4g}   {posH:8.4f}   {posB:8.4f}")
    sys.stdout.flush()

rows = np.array(rows)
print()
print("Jensen gap per angle (exact - Jensen end):", " ".join(f"{a:.4g}" for a in rows[:, 8]))
print("minima end above exact per angle        :", " ".join(f"{a:.4g}" for a in rows[:, 9]))


def slope(col, k1, k2, fit=False):
    sel = (rows[:, 0] >= k1) & (rows[:, 0] <= k2)
    if fit:
        return np.polyfit(np.log(rows[sel, 0]), np.log(rows[sel, col]), 1)[0]
    a = rows[rows[:, 0] == k1][0]
    b = rows[rows[:, 0] == k2][0]
    return np.log(b[col] / a[col]) / np.log(k2 / k1)


if set([24, 48, 96]).issubset(set(ks)):
    print(f"exponents between 24 and 96 cells: first-order {slope(1,24,96):.4f} (2-point) "
          f"{slope(1,24,96,True):.4f} (LSQ on 24,48,96);  all-H {slope(2,24,96):.4f} (2-point) "
          f"{slope(2,24,96,True):.4f} (LSQ)")
if set([96, 144, 288]).issubset(set(ks)):
    w = {int(r[0]): r[4] for r in rows}
    s1 = np.log(w[96] / w[144]) / np.log(144 / 96)
    k_ext = 144 * (w[144] / 1e-3) ** (1 / s1)
    s2 = np.log(w[144] / w[288]) / np.log(2)
    k_int = 144 * (w[144] / 1e-3) ** (1 / s2)
    print(f"cells per angle for 1e-3 nats per angle: {k_ext:.1f} (power law through 96 and 144, "
          f"{'EXTRAPOLATED beyond 144' if k_ext > 144 else 'interpolated'}); "
          f"{k_int:.1f} (power law through 144 and 288)")
print(f"brackets checked: {n_brackets};  brackets that exclude the exact value: {viol_bracket}  (must be 0)")
print("CONTROL too-small oscillation (all-H, c_i scaled by f): k where the exact value is EXCLUDED:")
for f in sorted(ctrl_small_osc, reverse=True):
    print(f"    f = {f}: {ctrl_small_osc[f]}")
for f in (0.5, 0.3, 0.1):
    if f not in ctrl_small_osc:
        print(f"    f = {f}: nowhere")
print(f"CONTROL cell minima used as a 'lower end': above the exact value (not a lower bound) in "
      f"{ctrl_minima_as_lower} of {len(ks)}")
print(f"CONTROL Jensen value used as an 'upper end': below the exact value in {ctrl_jensen_as_upper} of {len(ks)}")
rc.finish(t0)
