#!/usr/bin/env python3
"""Do our window-form penalty tables satisfy the hypothesis of the Complexity division's setting?

Their docs/complexity/PENALTY_THRESHOLD.md (at ff04e5e), section 1: tables gamma_U >= 0 with gamma_U(x_U) = 0 unless EVERY site
of U is off its anchor.  product_threshold.py uses their formula for lambda_0 with the maxima of our tables; this script
checks, per case, on the very tables of the driver (floor_transition.py, run in-process as product_threshold.py does):
  (1) every table is non-negative;
  (2) every table vanishes wherever at least one of its sites is at the anchor  -> the largest entry there (must be 0);
  (3) how far a typical entry is from the maximum: the mean of each table over its all-off entries, divided by its maximum
      (the binary relaxation replaces the table by its maximum on all of them) -- mean over tables, weighted by the maxima.
Control of (2): one entry with one site at the anchor is set to 1e-3 kT in a copy of one table; the test must report it.
Run: python3 -B product_threshold_support.py K12 4 4 > product_threshold_support_K12_m4_w4.log
"""
import sys, time, resource, functools
import numpy as np
import floor_transition as FT
from product_threshold import capture


def on_anchor_part(K, v, x0):
    """the largest |entry| of table v (on the site tuple K) among entries with at least one site at its anchor state"""
    mask = np.zeros(v.shape, dtype=bool)
    for ax, u in enumerate(K):
        sl = [slice(None)] * v.ndim; sl[ax] = x0[u]; mask[tuple(sl)] = True
    return float(np.abs(v[mask]).max()), mask


def main():
    seq, m, w = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); t0 = time.time(); BETA = FT.BETA
    got, text = capture([seq, str(m), str(w), "--grid", "0,0.01", "--N", "4"])
    print([l for l in text.split("\n") if l.startswith("=== ")][0][:300])
    g1, g2, g3, n, x0 = got["g1"], got["g2"], got["g3"], got["n"], [int(v) for v in got["x0"]]
    tabs = [((i,), g1[i]) for i in range(n) if g1[i].any()] + [(tuple(int(u) for u in K), v) for K, v in list(g2.items()) + list(g3.items())]
    neg = min(float(v.min()) for _, v in tabs); worst = 0.0; num = 0.0; den = 0.0; fr = []
    for K, v in tabs:
        a, mask = on_anchor_part(K, v, x0); worst = max(worst, BETA * a); off = v[~mask]; mx = float(v.max())
        if mx > 0: num += float(off.mean()); den += mx; fr.append(float(off.mean()) / mx)
    print(f"(1) {len(tabs)} tables; least entry {BETA * neg:.3g} kT (must be >= 0)")
    print(f"(2) largest entry with at least one site of the table at its anchor: {worst:.3g} kT (must be 0: their hypothesis)")
    K, v = tabs[-1]; v2 = v.copy(); idx = [0 if x0[u] != 0 else 1 for u in K]; idx[0] = x0[K[0]]; v2[tuple(idx)] = 1e-3 / BETA
    print(f"    control: one entry with one site at the anchor set to 1e-3 kT in a copy of the table on {K}: the test reports {BETA * on_anchor_part(K, v2, x0)[0]:.3g} kT (must be 1e-3)")
    assert neg >= 0 and worst == 0.0 and abs(BETA * on_anchor_part(K, v2, x0)[0] - 1e-3) < 1e-12
    print(f"(3) mean of a table over its all-off entries / its maximum: weighted by the maxima {num / den:.3f}; over tables: median {np.median(fr):.3f}, least {min(fr):.3f}, largest {max(fr):.3f}")
    print(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
