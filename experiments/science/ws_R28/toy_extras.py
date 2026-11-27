"""R28 — three adversarial extras on the toy chain of item 98 (their instance, my code):

 X1  closed trapezoid cells against half-open cells (a genuine partition of the grid): both must satisfy the
     sandwich; do the widths differ by more than O(1/N)?  (Is the trapezoid form a grid artefact?)
 X2  the bounded-difference constant: c_i as stated (sum over the terms containing i of term-wise oscillations)
     against the tight constant (oscillation of the SUM of the terms containing i, sup over the window) — both
     are functions of the state on the same window.  On a 360-point grid (the triple tables are k^3 (m+1)^3).
 X3  walls: the bump height W = 20, 200, 2000: what happens to the Jensen (lower) end, which mode M does not
     touch, and to the upper end.
Controls: X2 — the tight constant can never exceed the stated one (asserted, counted); the bracket with the
tight constant must still contain the exact value; a constant 'tighter than tight' (x 0.5) must fail somewhere.
"""
import r28_common as rc
rc.cap()
import sys
import time
import numpy as np
from scipy.special import logsumexp
import toy_lib as tl

t0 = time.time()
print("R28 toy_extras.py  start", rc.utc())


def instance(n, J, W, sigma, seed, N):
    rng = np.random.default_rng(seed)
    phi = rng.uniform(0, 2 * np.pi, n)
    theta = rng.uniform(0, 2 * np.pi, n - 1)
    a = rng.uniform(0, 2 * np.pi, n - 1)
    b = rng.uniform(0, 2 * np.pi, n - 1)
    x = tl.grid(N)
    e = [1.5 * (1.0 + np.cos(3.0 * x + phi[i])) for i in range(n)]
    pair = []
    for i in range(n - 1):
        v = J * np.cos(x[:, None] - x[None, :] - theta[i])
        if W:
            v = v + W * np.exp(-((1 - np.cos(x[:, None] - a[i])) + (1 - np.cos(x[None, :] - b[i]))) / sigma ** 2)
        pair.append(v)
    return e, pair


n = 8
# ------------------------------------------------------------------ X1
N = 1440
e, pair = instance(n, 2.0, 0.0, 0.6, 20261126, N)
ch = tl.Chain([np.exp(-ee) for ee in e], pair, None)
ex = ch.lnZ_exact()
print("\nX1 closed trapezoid cells vs half-open cells, case A (N = 1440): width per angle, first-order | all-H ; violations")
viol = 0
for k in (3, 6, 12, 24, 48, 96, 144, 288):
    out = []
    for kind in ("closed", "halfopen"):
        idx, tw = tl.cell_index(N, k) if kind == "closed" else tl.halfopen_index(N, k)
        cs = tl.Cells(ch, idx, tw)
        lj, lH, lmin, lmax = cs.lnZ_jensen(), cs.lnZ_upper(cs.all_H()), cs.lnZ_minima(), cs.lnZ_maxima()
        if not (lmax <= ex + 1e-10 and lj <= ex + 1e-10 and ex <= lH + 1e-10 and ex <= lmin + 1e-10):
            viol += 1
        out.append(((lmin - lmax) / n, (lH - lj) / n))
    print(f"   k = {k:3d}: closed {out[0][0]:.4e} | {out[0][1]:.4e};   half-open {out[1][0]:.4e} | {out[1][1]:.4e};"
          f"   ratio half-open/closed {out[1][0]/out[0][0]:.4f} | {out[1][1]/out[0][1]:.4f}")
print(f"   brackets excluding the exact value: {viol} of 16 (must be 0)")

# ------------------------------------------------------------------ X2
N = 360
e, pair = instance(n, 2.0, 0.0, 0.6, 20261126, N)
ch = tl.Chain([np.exp(-ee) for ee in e], pair, None)
ex = ch.lnZ_exact()
print(f"\nX2 stated against tight bounded-difference constant, case A on a {N}-point grid (exact ln<e^-V> = {ex:.8f})")
n_exceed = 0
n_trip = 0
for k in (3, 6, 12, 24):
    idx, tw = tl.cell_index(N, k)
    cs = tl.Cells(ch, idx, tw)
    lj = cs.lnZ_jensen()
    lH = cs.lnZ_upper(cs.all_H())
    lv = [np.log(a) for a in cs.v]
    # tight constants for the interior sites: T[i][s_{i-1}, s_i, s_{i+1}]
    Tt = {}
    for i in range(1, n - 1):
        A = pair[i - 1][idx[:, :, None, None], idx[None, None, :, :]]        # (s-, a, s, j)
        B = pair[i][idx[:, :, None, None], idx[None, None, :, :]]            # (s, j, s+, b)
        tab = np.empty((k, k, k))
        for s in range(k):
            S = A[:, :, s, :, None, None] + B[s][None, None, :, :, :]         # (s-, a, j, s+, b)
            osc = S.max(axis=2) - S.min(axis=2)                               # (s-, a, s+, b)
            tab[:, s, :] = osc.max(axis=(1, 3))
        Tt[i] = tab
        stated = cs.oR[i - 1][:, :, None] + cs.oL[i][None, :, :]
        n_trip += tab.size
        n_exceed += int((tab > stated + 1e-12).sum())

    def upper_tight(scale=1.0):
        F = lv[0][:, None] + lv[1][None, :] - cs.A[0] + (scale * cs.oL[0]) ** 2 / 8.0
        for i in range(1, n - 1):
            G = F[:, :, None] + (scale * Tt[i]) ** 2 / 8.0
            F = logsumexp(G, axis=0) + lv[i + 1][None, :] - cs.A[i]
        F = F + (scale * cs.oR[n - 2]) ** 2 / 8.0
        return float(logsumexp(F))
    lT = upper_tight()
    lT_half = upper_tight(0.5)
    lT_03 = upper_tight(0.3)
    ok = lj <= ex + 1e-10 <= lT + 2e-10
    print(f"   k = {k:2d}: all-H width per angle, stated constant {(lH - lj)/n:.4e}; tight constant {(lT - lj)/n:.4e}; ratio {(lT - lj)/(lH - lj):.3f};"
          f" position of the exact value {(ex - lj)/(lH - lj):.3f} -> {(ex - lj)/(lT - lj):.3f}; bracket holds: {ok};"
          f" control (tight x 0.5) excludes the exact value: {ex > lT_half}; control (tight x 0.3): {ex > lT_03}")
print(f"   tight constant larger than the stated one in {n_exceed} of {n_trip} (site, state-triple) entries (must be 0)")

# ------------------------------------------------------------------ X3
N = 1440
print("\nX3 walls: a bump of height W in every neighbour term; per angle: Jensen end below exact | best upper end (9 thresholds) above exact | cell-minima end above exact")
THRS = (np.inf, 6, 4, 3, 2, 1.5, 1, 0.5, -1.0)
for W in (0.0, 20.0, 200.0, 2000.0):
    e, pair = instance(n, 2.0, W, 0.6, 20261126, N)
    ch = tl.Chain([np.exp(-ee) for ee in e], pair, None)
    ex = ch.lnZ_exact()
    row = []
    for k in (3, 12, 48, 144):
        idx, tw = tl.cell_index(N, k)
        cs = tl.Cells(ch, idx, tw)
        lj = cs.lnZ_jensen()
        best = min(cs.lnZ_upper(cs.modes_by_threshold(t)) for t in THRS)
        assert lj <= ex + 1e-9 <= best + 2e-9
        row.append(f"k={k}: {(ex - lj)/n:.3g} | {(best - ex)/n:.3g} | {(cs.lnZ_minima() - ex)/n:.3g}")
    print(f"   W = {W:6g}:  " + ";   ".join(row))
rc.finish(t0)
