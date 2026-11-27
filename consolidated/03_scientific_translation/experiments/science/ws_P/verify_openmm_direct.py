"""Independent end-to-end check: constants c_i of g_GB on the A3 grid of the tripeptide,
computed with OpenMM itself (CPU platform, CustomGBForce) and a brute-force double loop,
without fastff.py and without analysis_lib.py.  Expected (report, Statement 1):
16.09 12.41 18.63 16.43 15.14 11.19 kcal/mol."""
import itertools, math
import numpy as np
from pepbuild import Peptide

n = 3
P = Peptide(n, extra_ffs=(), platform="CPU")
PH = [-150.0, -70.0, 60.0]; PS = [-40.0, 60.0, 150.0]
states = list(itertools.product(range(3), repeat=2 * n))
phi = np.deg2rad(np.array([[PH[s[2 * r]] for r in range(n)] for s in states]))
psi = np.deg2rad(np.array([[PS[s[2 * r + 1]] for r in range(n)] for s in states]))
X = P.coords(phi, psi)
E = P.energies(X)
g = E["gbn2"]; ok = P.clash_score(X) > 0.70
index = {s: i for i, s in enumerate(states)}
c = np.zeros(2 * n)
for s in states:
    i0 = index[s]
    if not ok[i0]:
        continue
    for site in range(2 * n):
        for a in range(3):
            if a != s[site]:
                t = list(s); t[site] = a; j = index[tuple(t)]
                if ok[j]:
                    c[site] = max(c[site], abs(g[i0] - g[j]))
print("clash-free conformations:", int(ok.sum()), "of", len(states))
print("c_i (OpenMM direct, kcal/mol):", np.round(c, 2))
