#!/usr/bin/env python3
"""G5 (estimates, not bounds): covering problem of the best available INNER model of the limit object:
   profile body = hull of the periodic chain systems with cell index <= KMAX,
   gamma(p) = lower envelope of the 4D hull of (p, gmin/n)  (an upper estimate of the true gamma on that body).
For a grid of the body in u-coordinates:
   'packing' = greedy set of clients with L|u_i-u_j|_1 > gamma_i + gamma_j + 2 eps1  (a lower bound for the covering
               number of the model),
   'net'     = greedy set cover with internal centres on the grid (at each step the centre covering most uncovered
               clients): an upper estimate for the covering number of the model on the grid (-1: grid too large).
Also the same for the model with gamma = 0 (covering numbers of the body with balls of radius eps1/L).
usage: g5_estimate.py OUT_DIR KMAX
"""
import sys, os
import numpy as np
from scipy.spatial import ConvexHull
from g5_bounds import to_u

out, kmax = sys.argv[1], int(sys.argv[2])
pts = {}
for K in range(1, kmax + 1):
    p = f"{out}/pchain_K{K}.txt"
    if not os.path.exists(p): continue
    for line in open(p):
        if line.startswith('#'): continue
        n, e3, e8, e11, gmin, gmax = map(int, line.split())
        key = (round(e3 / n - 1, 9), round(e8 / n - 1, 9), round(e11 / n, 9))
        g = gmin / n
        if key not in pts or g < pts[key]: pts[key] = g
P = np.array(list(pts)); G = np.array([pts[tuple(k)] for k in P])
U = to_u(P)
h3 = ConvexHull(U)
h4 = ConvexHull(np.column_stack([U, G]))
low = h4.equations[h4.equations[:, 3] < -1e-9]
def gamma(X):
    return np.maximum(0.0, ((X @ low[:, :3].T + low[:, 4]) / (-low[:, 3])).max(axis=1))
print(f"# inner model: {len(P)} periodic chain systems (index <= {kmax}); body volume {h3.volume:.2f} (u-coordinates)")

def grid(step):
    lo = U.min(axis=0); hi = U.max(axis=0)
    ax = [np.arange(lo[k], hi[k] + step, step) for k in range(3)]
    X = np.array(np.meshgrid(*ax, indexing="ij")).reshape(3, -1).T
    keep = np.ones(len(X), bool)
    for s0 in range(0, len(X), 200000):
        keep[s0:s0+200000] = ((X[s0:s0+200000] @ h3.equations[:, :3].T + h3.equations[:, 3]) <= 1e-9).all(axis=1)
    return X[keep]

def greedy(X, gam, L, e1):
    n = len(X)
    order = np.lexsort((X[:, 2], X[:, 1], X[:, 0]))
    # packing
    alive = np.ones(n, bool); pack = 0
    for i in order:
        if not alive[i]: continue
        pack += 1
        d = np.abs(X - X[i]).sum(axis=1)
        alive &= (L * d > gam + gam[i] + 2 * e1 + 1e-9)
    # greedy set cover with internal centres: centre i covers client j iff L d(i,j) <= gam_j + e1;
    # at each step take the centre that covers the largest number of uncovered clients
    if n > 20000:
        return pack, -1
    C = np.zeros((n, n), dtype=bool)
    for i in range(n):
        C[i] = L * np.abs(X - X[i]).sum(axis=1) <= gam + e1 + 1e-9
    unc = np.ones(n, bool); net = 0
    cnt = C.sum(axis=1).astype(np.int64)
    while unc.any():
        i = int(cnt.argmax())
        newly = C[i] & unc
        net += 1
        unc &= ~newly
        cnt -= C[:, newly].sum(axis=1)
    return pack, net

print("#  L    eps1 | grid step, points | with gamma of the model: packing, net | gamma = 0: packing, net | volume fraction with gamma > 0.02")
for L, e1 in ((1.0, 0.5), (1.0, 0.25), (0.2, 0.5), (0.2, 0.25)):
    r = e1 / L
    step = max(r / 3.2, 0.125)
    X = grid(step)
    gam = gamma(X)
    a = greedy(X, gam, L, e1)
    b = greedy(X, np.zeros(len(X)), L, e1)
    print(f"  {L:4.2f} {e1:5.2f} |  {step:5.3f} {len(X):7d}   |        {a[0]:6d} {a[1]:6d}            |   {b[0]:6d} {b[1]:6d}      | {(gam > 0.02).mean():.3f}")
