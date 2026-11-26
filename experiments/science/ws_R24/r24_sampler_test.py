#!/usr/bin/env python3
"""R24: the referee's own elimination and exact sampler (r24_common) against enumeration on random models with tables on
overlapping scopes.  Control: the sampler run at 1.05 beta must fail the same chi-square test.
(A first, unpooled chi-square gave 579 for 431 degrees of freedom: 273 of the 432 cells had an expected count below 20 --
an error in the design of the test, not of the sampler; cells with an expected count below 20 are pooled here.)
Run: python3 -B r24_sampler_test.py > r24_sampler_test.log
"""
import sys, math, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r24_common as C


def test(seed, mult=1.0, N=400000):
    rng = np.random.default_rng(seed)
    k = [3, 4, 2, 3, 3, 2]
    fac = [((i,), rng.normal(size=k[i])) for i in range(6)] + [((i, j), rng.normal(size=(k[i], k[j]))) for i in range(6) for j in range(i + 1, min(i + 3, 6))] \
        + [((1, 2, 3), rng.normal(size=(4, 2, 3))), ((0, 2), rng.normal(size=(3, 2))), ((2, 4, 5), rng.normal(size=(2, 3, 2)))]
    E = C.energy_all(0.3, fac, k); beta = 1.3
    lz = math.log(np.exp(-beta * E).sum()); p = np.exp(-beta * E - lz).ravel()
    d_sum = abs(C.eliminate(fac, k, "sum", -beta) - beta * 0.3 - lz)
    mx, x = C.eliminate(fac, k, "max", -beta, want_arg=True); d_max = abs(mx - float((-beta * (E - 0.3)).max())); arg_ok = int(np.ravel_multi_index(x, k)) == int(np.argmax(-beta * E))
    S = C.OwnSampler(fac, k, -mult * beta); X = S.sample(N, rng); emp = np.bincount(np.ravel_multi_index(X.T, k), minlength=p.size)
    big = p * N >= 20; O = np.concatenate([emp[big], [emp[~big].sum()]]); Ex = np.concatenate([p[big] * N, [p[~big].sum() * N]])
    chi = ((O - Ex) ** 2 / Ex).sum(); dof = len(O) - 1
    return d_sum, d_max, arg_ok, chi, dof, (chi - dof) / math.sqrt(2 * dof)


worst = 0.0; zs = []; zc = []
for seed in range(5, 17):
    d_sum, d_max, arg_ok, chi, dof, z = test(seed); _, _, _, _, _, z2 = test(seed, 1.05); worst = max(worst, d_sum, d_max); zs.append(z); zc.append(z2)
    print(f"seed {seed}: ln Z by elimination - enumeration {d_sum:.1e}; max {d_max:.1e}; arg-max equal: {arg_ok}; sampler: pooled chi2 {chi:.1f} for {dof} dof (z = {z:+.2f}); control at 1.05 beta: z = {z2:+.1f}")
print(f"12 random models: largest deviation of the eliminations {worst:.1e}; z-scores of the sampler between {min(zs):+.2f} and {max(zs):+.2f} (must be within about 3); control between {min(zc):+.1f} and {max(zc):+.1f} (must be far above 3)")
print(f"ALL DONE; peak RSS {C.rss():.0f} MB")
