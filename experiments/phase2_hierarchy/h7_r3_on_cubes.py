"""
Phase II (adaptive hierarchy) -- Algorithm R3 of the report (section 4), run literally on real cubes.

The energy is a table on all 2^n points (n <= 18).  The algorithm sees it only through evaluations.
Tests:  (a) every centre candidate is the true centre of its block or the antipode;
        (b) unbiasedness: the mean of the estimate over repeated runs equals A within sampling error,
            for every M (whatever the reveal steps did);
        (c) when every block is revealed the estimate equals A exactly (up to rounding);
        (d) mutation: shell weights replaced by uniform weights -> the estimate is biased (must be caught);
        (e) mutation: the reveal step replaced by "reveal nothing" -> still unbiased (plain Monte Carlo).
Profiles: minimum of random cones and dips in the types; 2-periodic profiles; profiles that depend on a
block only far from its centre.
"""
import sys, itertools, math
import numpy as np

def make_instance(rng, ns, u, kind):
    n = sum(ns); m = len(ns)
    blocks = []; start = 0
    for nj in ns:
        blocks.append(np.arange(start, start + nj)); start += nj
    s = rng.integers(0, 2, n)
    grids = np.meshgrid(*[np.arange(nj + 1) for nj in ns], indexing='ij')
    if kind == 'cones':
        F = np.zeros(grids[0].shape)
        for _ in range(4):
            c = [rng.integers(0, nj + 1) for nj in ns]; w = rng.random(m) < 0.7
            F = np.minimum(F, u * sum(np.abs(g - ci) * wi for g, ci, wi in zip(grids, c, w)) - rng.uniform(0, 0.5) * u * n)
    elif kind == 'periodic':                       # 2-periodic in block 0, a cone in the others
        F = 0.5 * u * (grids[0] % 2) + u * sum(grids[1:])
    elif kind == 'far':                            # depends on block 0 only at distance <= 1 from its centre
        F = -u * np.maximum(2 - grids[0], 0) + 0.3 * u * sum(grids[1:])
    else:
        raise ValueError(kind)
    # table on the cube
    X = ((np.arange(2 ** n)[:, None] >> np.arange(n)[None, :]) & 1).astype(np.int8)
    types = [np.sum(X[:, b] != s[b], axis=1) for b in blocks]
    psi = F[tuple(types)]
    # admissibility on the cube (largest edge difference)
    edge = max(np.abs(psi - psi[np.arange(2 ** n) ^ (1 << i)]).max() for i in range(n))
    assert edge <= u + 1e-9, edge
    return dict(n=n, m=m, blocks=blocks, s=s, psi=psi, A=float(np.mean(np.exp(-psi))), ns=ns)

def idx(x):
    return int(np.dot(x, 1 << np.arange(len(x))))

def reveal(inst, x, block, q):
    """evaluate the neighbours of x in the block; return a centre candidate or None"""
    vals = []
    for i in block:
        y = x.copy(); y[i] ^= 1; vals.append(inst['psi'][idx(y)]); q[0] += 1
    vals = np.array(vals)
    if np.all(np.abs(vals - vals[0]) < 1e-12): return None
    I = np.abs(vals - vals[0]) < 1e-12
    c = x[block].copy(); c[I] ^= 1
    return c

def sample_shell(rng, inst, cand, a):
    """a point whose revealed blocks lie on spheres of radii a_j around the candidates, uniform elsewhere"""
    x = rng.integers(0, 2, inst['n'])
    for j, c in cand.items():
        b = inst['blocks'][j]; y = c.copy()
        flip = rng.choice(len(b), size=a[j], replace=False)
        y[flip] ^= 1; x[b] = y
    return x

def R3(inst, M, rng, mutate=None):
    q = [0]; cand = {}
    for rnd in (1, 2):                                   # the two revealing rounds
        shells = itertools.product(*[range(inst['ns'][j] + 1) for j in sorted(cand)]) if cand else [()]
        new = {}
        keys = sorted(cand)
        for a in shells:
            ad = dict(zip(keys, a))
            for _ in range(M):
                x = sample_shell(rng, inst, cand, ad); q[0] += 1
                for j in range(inst['m']):
                    if j in cand or j in new: continue
                    c = None if mutate == 'no_reveal' else reveal(inst, x, inst['blocks'][j], q)
                    if c is not None: new[j] = c
        cand.update(new)
    keys = sorted(cand); est = 0.0
    shells = itertools.product(*[range(inst['ns'][j] + 1) for j in keys]) if keys else [()]
    for a in shells:
        ad = dict(zip(keys, a))
        if mutate == 'uniform_weights':
            w = 1.0 / np.prod([inst['ns'][j] + 1 for j in keys]) if keys else 1.0
        else:
            w = np.prod([math.comb(inst['ns'][j], ad[j]) / 2.0 ** inst['ns'][j] for j in keys]) if keys else 1.0
        tot = 0.0
        for _ in range(M):
            x = sample_shell(rng, inst, cand, ad); q[0] += 1
            tot += math.exp(-inst['psi'][idx(x)])
        est += w * tot / M
    return est, cand, q[0]

if __name__ == "__main__":
    rng = np.random.default_rng(20261128)
    u = 1.0
    print("Algorithm R3 on real cubes (u = %g).  z = (mean estimate - A)/standard error over the runs." % u)
    bad = 0
    for kind in ('cones', 'periodic', 'far'):
        for ns in ((6, 6), (5, 4, 5), (7, 7)):
            inst = make_instance(rng, ns, u, kind)
            for M in (3, 30):
                ests = []; cand_ok = True; allrev_exact = True; nrev = []
                for _ in range(60):
                    est, cand, q = R3(inst, M, rng)
                    ests.append(est); nrev.append(len(cand))
                    for j, c in cand.items():
                        sj = inst['s'][inst['blocks'][j]]
                        cand_ok &= bool(np.all(c == sj) or np.all(c == 1 - sj))
                    if len(cand) == inst['m']: allrev_exact &= abs(est - inst['A']) <= 1e-9 * inst['A']
                ests = np.array(ests); se = ests.std(ddof=1) / np.sqrt(len(ests))
                relerr = np.abs(ests - inst['A']).max() / inst['A']
                # if every run is exact up to rounding, a z-score is meaningless: report 0 and require exactness
                z = 0.0 if relerr < 1e-9 else (ests.mean() - inst['A']) / se
                mut = np.array([R3(inst, M, rng, mutate='uniform_weights')[0] for _ in range(60)])
                zm = (mut.mean() - inst['A']) / (mut.std(ddof=1) / np.sqrt(60) + 1e-300)
                nr = np.array([R3(inst, M, rng, mutate='no_reveal')[0] for _ in range(60)])
                zn = (nr.mean() - inst['A']) / (nr.std(ddof=1) / np.sqrt(60) + 1e-300)
                ok = cand_ok and allrev_exact and abs(z) < 3.5
                bad += (not ok)
                print("  %-8s blocks %-9s M=%2d  revealed %.1f of %d | candidates ok %s | exact when all revealed %s | max rel. error %.1e | z = %+5.2f | mutation uniform weights: |z| = %.3g | no reveal: z = %+5.2f" % (
                    kind, ns, M, np.mean(nrev), inst['m'], cand_ok, allrev_exact, relerr, z, abs(zm), zn))
                sys.stdout.flush()
    print("failures of (a), (b), (c):", bad)
