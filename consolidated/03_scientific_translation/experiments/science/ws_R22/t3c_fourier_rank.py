#!/usr/bin/env python3
"""R22: what M sees of a distribution of h differing torsions (long segments) -- take the coordinator's item (5) further.
Every squared distance is multilinear in (1, cos, sin) of the torsions between the two atoms (3^h product functions).
Paper count (R22): M depends on them only through E[rho_a ... rho_b] for runs of consecutive hinges, which gives
rank 2 h^2 + 1 on the proper component (9, 19, 33 for h = 2, 3, 4) -- for h >= 3 fewer than 3^h = 27, 81.
Check: sample random torsion tuples, fit D on the 3^h product functions (residual must be ~1e-13; control: without
the top-degree products the residual must be large), rank of the coefficient map.
Run: OMP_NUM_THREADS=1 python3 -B t3c_fourier_rank.py > t3c_fourier_rank.log
"""
import itertools, time
import numpy as np
import r22lib as L
t0 = time.time(); rng = np.random.default_rng(2270); viol = 0
print("| h | n | hinge torsions | samples | 3^h | residual of the fit on all product functions | control: residual without the degree-h products | rank of the map coefficients -> M | predicted 2h^2+1 |")
print("|---|---|---|---|---|---|---|---|---|")
for h, n, hinges in ((1, 16, [6]), (2, 20, [5, 12]), (2, 26, [7, 16]), (3, 26, [5, 12, 19]), (3, 34, [7, 15, 23]), (4, 34, [5, 12, 19, 26]), (4, 44, [8, 16, 24, 32])):
    tors = rng.uniform(-np.pi, np.pi, n - 3); ns = 6 * 3 ** h
    iu = [(i, j) for i in range(n) for j in range(i + 3, n)]
    B, Y = [], []
    for s in range(ns):
        t = tors.copy(); ang = rng.uniform(-np.pi, np.pi, h); t[hinges] = ang
        D = L.sqdist(L.chain(t)); Y.append([D[i, j] for i, j in iu])
        f = [[1.0, np.cos(a), np.sin(a)] for a in ang]
        B.append([np.prod([f[k][c[k]] for k in range(h)]) for c in itertools.product(range(3), repeat=h)])
    B, Y = np.array(B), np.array(Y)
    coef = np.linalg.lstsq(B, Y, rcond=None)[0]; res = np.abs(B @ coef - Y).max()
    top = [i for i, c in enumerate(itertools.product(range(3), repeat=h)) if all(ci > 0 for ci in c)]
    keep = [i for i in range(3 ** h) if i not in top]
    res2 = np.abs(B[:, keep] @ np.linalg.lstsq(B[:, keep], Y, rcond=None)[0] - Y).max()
    sv = np.linalg.svd(coef, compute_uv=False); rank = int((sv > 1e-9 * sv[0]).sum())
    ok = res < 1e-9 and res2 > 1e-2 and rank == 2 * h * h + 1
    viol += int(not ok)
    print(f"| {h} | {n} | {hinges} | {ns} | {3 ** h} | {res:.1e} | {res2:.1e} | {rank} | {2 * h * h + 1} |" + ("" if ok else "  <-- differs"))
print(f"violations of the prediction: {viol}")
print(f"ALL DONE {time.time() - t0:.1f} s")
