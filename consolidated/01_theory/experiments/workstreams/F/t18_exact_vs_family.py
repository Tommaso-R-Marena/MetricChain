"""t18: exact tail function of the reference H on the 4-cube (all 65534 subsets) against the best set of the
bi-radial family (largest dip effect among 'density balls' {x : d(x,s) <= r_type(x)} around a centre s with the same
bound on mu_H(D)).  At n = 4 exponents cannot be read off; the test only looks for a gross gap between the family used
for the explicit formulas and the true extremal sets."""
import math, itertools, numpy as np
import t14_two_level_H as T

n = 4
N = 16
pop, D = T.cube(n)
for p in (0.1, 0.3, 0.5):
    for u in (0.6, 1.0, 2.0):
        tab = T.tables(n, p, u, "H")
        mu, sH = tab["muH"], tab["sH"]
        # family: for a centre s and radii (r_t) per type, D = {x : d(x,s) <= r_|x|}
        fam = []
        for s in (0, 1, 3, 7, 15):                      # one centre per weight (the instance is permutation symmetric)
            ds = D[s]
            for radii in itertools.product(range(-1, n + 1), repeat=n + 1):
                Dset = ds <= np.array(radii)[pop]
                if Dset.all() or not Dset.any():
                    continue
                dep = np.where(Dset[None, :], np.inf, sH).min(axis=1)
                phi = float((mu[Dset] * np.expm1(dep[Dset])).sum())
                fam.append((float(mu[Dset].sum()), phi))
        fam.sort()
        fm = np.array([f[0] for f in fam]); fp = np.maximum.accumulate(np.array([f[1] for f in fam]))
        worst = 1.0; at = None
        for q in np.unique(np.round(tab["mu"], 12)):
            ex = T.Xi(tab, q)
            k = int(np.searchsorted(fm, q * (1 + 1e-9), side="right"))
            fa = fp[k - 1] if k > 0 else 0.0
            if ex > 1e-9 and fa > 0 and ex / fa > worst:
                worst, at = ex / fa, (q, ex, fa)
            if ex > 1e-9 and fa == 0:
                worst, at = math.inf, (q, ex, fa)
        print(f"p={p} u={u}: largest ratio exact Xi_H(q) / best family set with mu_H <= q : {worst:.3f}  at (q, exact, family) = {at}")
