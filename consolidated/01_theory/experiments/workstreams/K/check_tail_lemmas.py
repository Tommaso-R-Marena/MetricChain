"""Workstream K: own check of Lemma K.1 (= Lemma 11.43(b),(c)) on u-Lipschitz functions of small cubes, every threshold:
 (a) |{w > t}| <= |B(m,r)|, r <= m-1   =>   sum_x (w - t)_+ <= t E_r(m)
 (b) |{w >= t}| >= |B(m,k)|            =>   sum_x min(w, t) >= t T_m(k)
and of the equality cases (dip for (a), cone with a flat top for (b))."""
import math, sys
import numpy as np
from sim_outer_loop import Tables, cube_dist, rand_lipschitz

rng = np.random.default_rng(5)
ok = True
stats = dict(functions=0, thresholds=0, worst_a=0.0, worst_b=math.inf)
for m in (4, 6, 8, 10):
    D = cube_dist(m)
    for u in (0.4, 1.0, 2.2):
        tab = Tables(m, u, 0.25)
        for rep in range(40 if m <= 8 else 16):
            psi = rand_lipschitz(rng, m, u, D, rep % 8)
            w = np.exp(-psi)
            stats["functions"] += 1
            ws = np.sort(w)
            for t in np.unique(ws):
                nD = int((w > t).sum()); nS = int((w >= t).sum())
                stats["thresholds"] += 1
                if 0 < nD:
                    r = next(rr for rr in range(m + 1) if tab.ball[rr + 1] >= nD)
                    if r <= m - 1:
                        lhs = float(np.maximum(w - t, 0).sum()); rhs = t * tab.E[r]
                        stats["worst_a"] = max(stats["worst_a"], lhs / rhs)
                        if lhs > rhs * (1 + 1e-9): ok = False; print("(a) violated", m, u, rep, t)
                k = max(kk for kk in range(m + 1) if tab.ball[kk + 1] <= nS)
                lhs = float(np.minimum(w, t).sum()); rhs = t * tab.T[k]
                stats["worst_b"] = min(stats["worst_b"], lhs / rhs)
                if lhs < rhs * (1 - 1e-9): ok = False; print("(b) violated", m, u, rep, t)
        # equality cases
        R = max(1, m // 3)
        dip = np.exp(u * np.maximum(R + 1 - D[0], 0).astype(float))          # w = e^{u (R+1-d)_+}, t = 1: {w > 1} = B(R)
        if abs(np.maximum(dip - 1, 0).sum() / tab.E[R] - 1) > 1e-9: ok = False; print("equality (a) fails")
        top = np.exp(-u * np.maximum(D[0] - R, 0).astype(float))             # w = e^{-u (d-R)_+}, t = 1: {w >= 1} = B(R)
        if abs(np.minimum(top, 1).sum() / tab.T[R] - 1) > 1e-9: ok = False; print("equality (b) fails")
print(stats)
print("Lemma K.1 (a), (b) hold on every threshold of every function; equality cases attained:", ok)
open("out_check_tail_lemmas.txt", "w").write(f"{stats}\nok = {ok}\n")
sys.exit(0 if ok else 1)
