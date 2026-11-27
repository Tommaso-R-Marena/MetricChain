"""R28 — self-test of my own toy library against brute force FROM THE DEFINITIONS (tiny chains),
and per-state checks of (a), (b), (c) of Proposition A17.24.

Checks (each with a control that can fail):
 T1  transfer-matrix values (exact, Jensen, upper for random modes, minima, maxima) == brute force.
 T2  per-state inequalities (b), (c) hold for every state, every tried mode assignment, for
     closed trapezoid cells AND for half-open cells (a genuine partition).
     Control C2: oscillations scaled by 0.3 -> (c) must be violated for some state in some model.
 T3  (a): sum_s v_s <e^{-V}>_s == exact grid value.
     Control C3: closed cells with FULL end-point weights (not a decomposition of nu) -> (a) fails.
 T4  one-body terms kept as terms of V (uniform reference) also satisfy everything.
 T5  correlated (non-product) reference inside a cell: the smallest counterexample to (c):
     two perfectly correlated two-point coordinates, W = a(x1 + x2).
"""
import r28_common as rc
rc.cap()
import sys
import time
import numpy as np
import toy_lib as tl

t0 = time.time()
print("R28 toy_selftest.py  start", rc.utc())
rng = np.random.default_rng(2801)

nviol_T1 = nviol_b = nviol_c = nviol_a = 0
ncheck = 0
ctrl_c_hits = 0
ctrl_a_hits = 0
max_T1 = 0.0
models = 0
for trial in range(60):
    n = int(rng.integers(2, 5))                 # 2, 3, 4 sites
    k = int(rng.integers(2, 4))                 # 2 or 3 cells
    m = int(rng.integers(2, 4))                 # 2 or 3 intervals per cell
    N = k * m
    amp = float(rng.choice([0.3, 1.0, 3.0, 8.0]))
    w = [np.exp(-rng.normal(size=N)) for _ in range(n)]
    pair = [amp * rng.normal(size=(N, N)) for _ in range(n - 1)]
    one = None
    if trial % 3 == 2:
        one = [amp * rng.normal(size=N) for _ in range(n)]
    ch = tl.Chain(w, pair, one)
    ex = ch.lnZ_exact()
    for kind in ("closed", "halfopen"):
        idx, tw = (tl.cell_index(N, k) if kind == "closed" else tl.halfopen_index(N, k))
        cs = tl.Cells(ch, idx, tw)
        for rep in range(3):
            if rep == 0:
                H = cs.all_H()
            elif rep == 1:
                H = cs.all_M()
            else:
                H = [rng.random(k) < 0.5 for _ in range(n)]
            bf = tl.brute_force_check(ch, idx, tw, H)
            models += 1
            # T3 (a)
            ncheck += 1
            if abs(bf["lnZ_cells"] - ex) > 1e-10:
                nviol_a += 1
            # T1
            d = max(abs(bf["lnZ_low"] - cs.lnZ_jensen()), abs(bf["lnZ_up"] - cs.lnZ_upper(H)))
            if rep == 1:
                d = max(d, abs(bf["lnZ_up"] - cs.lnZ_minima()))
            max_T1 = max(max_T1, d)
            if d > 1e-9:
                nviol_T1 += 1
            # T2
            if bf["worst_b"] > 1e-12:
                nviol_b += 1
            if bf["worst_c"] > 1e-12:
                nviol_c += 1
            # C2: too small oscillations
            if rep != 1:
                bf2 = tl.brute_force_check(ch, idx, tw, H, scale=0.3)
                if bf2["worst_c"] > 1e-12:
                    ctrl_c_hits += 1
                # the transfer-matrix code must agree on the scaled quantity too
                d2 = abs(bf2["lnZ_up"] - cs.lnZ_upper(H, scale=0.3))
                max_T1 = max(max_T1, d2)
                if d2 > 1e-9:
                    nviol_T1 += 1
        # maxima are a lower bound, minima an upper bound
        if not (cs.lnZ_maxima() <= ex + 1e-12 <= cs.lnZ_minima() + 2e-12):
            nviol_T1 += 1
    # C3: closed cells with full end-point weights
    idx, tw = tl.cell_index(N, k)
    bf3 = tl.brute_force_check(ch, idx, np.ones_like(tw), [np.ones(k, bool)] * n)
    if abs(bf3["lnZ_cells"] - ex) > 1e-10:
        ctrl_a_hits += 1

print(f"models x modes checked by brute force: {models}")
print(f"T1 transfer matrices vs brute force: violations {nviol_T1}, max |difference| {max_T1:.2e}")
print(f"T2 per-state (b): models with a violated state {nviol_b};  (c): {nviol_c}")
print(f"T3 (a) cell-wise identity: violations {nviol_a} of {ncheck}")
print(f"C2 control (oscillations x 0.3): models with a state violating (c): {ctrl_c_hits}  (must be > 0)")
print(f"C3 control (full end-point weights): (a) fails in {ctrl_a_hits} of 60  (must be > 0)")

# ------------------------------------------------------------------ T5: non-product reference
print()
print("T5  smallest counterexample to (c) without a product reference inside the cell:")
print("    x1 = x2 in {0,1} with probability 1/2 each (perfectly correlated), V = W = a (x1 + x2),")
print("    c_1 = c_2 = a;  ln<e^{-(W-<W>)}> = ln cosh(a);  claimed bound sum c_i^2/8 = a^2/4;")
print("    surviving bound (sum c_i)^2/8 = a^2/2")
for a in (0.1, 0.5, 1.0, 2.0, 4.0):
    lhs = np.log(np.cosh(a))
    print(f"    a = {a:4.1f}   ln cosh a = {lhs:.6f}   a^2/4 = {a*a/4:.6f}   a^2/2 = {a*a/2:.6f}"
          f"   (c) violated: {lhs > a*a/4}   weaker bound holds: {lhs <= a*a/2}")
print("    with a PRODUCT two-point reference: ln<e^{-(W-<W>)}> = 2 ln cosh(a/2):")
for a in (0.1, 0.5, 1.0, 2.0, 4.0):
    lhs = 2 * np.log(np.cosh(a / 2))
    print(f"    a = {a:4.1f}   2 ln cosh(a/2) = {lhs:.6f}   a^2/4 = {a*a/4:.6f}   holds: {lhs <= a*a/4}")

ok = (nviol_T1 == 0 and nviol_b == 0 and nviol_c == 0 and nviol_a == 0 and ctrl_c_hits > 0 and ctrl_a_hits > 0)
print()
print("SELFTEST", "PASSED" if ok else "FAILED")
rc.finish(t0)
