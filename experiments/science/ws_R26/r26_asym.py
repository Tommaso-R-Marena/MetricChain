#!/usr/bin/env python3
"""r26_asym.py -- workstream R26: the influence is not symmetric -- one explicit example (a nearest-neighbour
chain with clashes: model of table T2, seed 2000), and the triangle inequality of the exact influences.
Usage: python3 -B r26_asym.py"""
import resource
import sys

import numpy as np

import r26_band as B

q, n, c = 3, 10, 5
base = B.make_base(n, q, 1, np.random.default_rng(2000), clash_frac=0.15)
print("model: T2, seed 2000, q = 3, n = 10, cut after site 5, J = 1, clash 20; clash entries on the cross-cut pair:")
print(base["mask"][(c - 1, c)].astype(int))
model = B.energies(base, 1.0, 20.0)
alphas, bconf, logmu = B.brute_conditionals(model, c)
_, betas, Ex, logR, logpi = B.boundary_layer(model, c)
pt = B.iota_pointwise_brute(logmu)
A_ub = B.lipschitz_constraints(q, n - c, 1.0)
lip = B.iota_lipschitz_lp(logmu, A_ub)
box = B.iota_box_levelset(logpi, 5.0)
np.set_printoptions(precision=3, suppress=True)
print("pointwise influence iota_pt[a, a'] (rows a, columns a'):")
print(pt)
print("Lipschitz influence, u = 1:")
print(lip)
print("box influence, D = 5:")
print(box)
asym = np.abs(pt - pt.T).max(), np.abs(lip - lip.T).max(), np.abs(box - box.T).max()
print(f"largest |iota(a,a') - iota(a',a)|: pointwise {asym[0]:.3f}, Lipschitz {asym[1]:.3f}, box {asym[2]:.3f}")
viol = 0
for M in (pt, lip, box):
    for a in range(q):
        for b in range(q):
            for d in range(q):
                if M[a, d] > M[a, b] + M[b, d] + 1e-6:
                    viol += 1
print(f"triangle inequality iota(a,a'') <= iota(a,a') + iota(a',a''): violations {viol}")
print(f"peak memory {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")
sys.exit(1 if viol else 0)
