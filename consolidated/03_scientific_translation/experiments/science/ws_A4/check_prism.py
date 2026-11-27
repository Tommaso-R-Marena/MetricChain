#!/usr/bin/env python3
"""Hand-check of my reading of a printed lower bound (no project data, no project code): for the band graph with
edges |i-j| <= 3 in R^3, the "prism" configurations p_c(u) = (c x_{u mod 3}, u) (x_1,x_2,x_3 the vertices of a unit
equilateral triangle, c large) used in the printed proof have a 7th stiffness eigenvalue of order 1/n^2 —
printed lower bound: 1 - cos( (pi/2) / ceil(n/3) ).  A thin helix of similar bond length is shown for contrast."""
import numpy as np
def lam7(X, K=3):
    n = len(X); rows = []
    for i in range(n):
        for j in range(i + 1, min(n, i + K + 1)):
            e = (X[i] - X[j]) / np.linalg.norm(X[i] - X[j]); r = np.zeros(3 * n)
            r[3 * i:3 * i + 3] = e; r[3 * j:3 * j + 3] = -e; rows.append(r)
    R = np.array(rows); return np.linalg.eigvalsh(R.T @ R)[6]
tri = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) / 2]])
print(" n   prism c=10   prism c=1e3   printed lower bound   n^2*prism(c=1e3)   thin helix   n^4*helix")
for n in (12, 24, 48, 96):
    vals = []
    for c in (10.0, 1e3):
        X = np.array([[c * tri[u % 3][0], c * tri[u % 3][1], float(u)] for u in range(n)])
        vals.append(lam7(X))
    lb = 1 - np.cos((np.pi / 2) / np.ceil(n / 3))
    t = np.arange(n); H = np.c_[np.cos(1.7 * t), np.sin(1.7 * t), 0.6 * t]   # a thin helix, radius 1
    h = lam7(H)
    print(f"{n:3d}   {vals[0]:.3e}    {vals[1]:.3e}     {lb:.3e}            {vals[1]*n*n:7.3f}        {h:.3e}   {h*n**4:9.2f}")
