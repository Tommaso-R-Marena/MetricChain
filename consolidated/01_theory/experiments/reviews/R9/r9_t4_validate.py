# R9 test 4: validation of the profile machinery (r9prof.Grid.stats) against brute force on the full cube, n <= 11:
# random groupings (G = 2, 3, 4), random unions of cells, references H, 0 and additive.
import numpy as np, time, itertools, sys
from math import log
from r9lib import Par
from r9prof import Grid, lse
rng = np.random.default_rng(11)
t0 = time.time()
maxdev = 0.0; ncase = 0
for trial in range(120):
    G = int(rng.choice([2, 3, 4])); sizes = [int(rng.integers(1, 4)) for _ in range(G)]
    n = sum(sizes)
    if n > 11: continue
    p = rng.uniform(0.05, 0.95); u = rng.uniform(0.2, 4.0); P = Par(p, u)
    gr = Grid(P, sizes)
    # all points of the cube; group membership = consecutive coordinates
    X = np.array(list(itertools.product([0, 1], repeat=n)), dtype=np.int64)
    bounds = np.cumsum([0] + sizes)
    W = np.stack([X[:, bounds[g]:bounds[g + 1]].sum(axis=1) for g in range(G)], axis=1)
    tX = X.sum(axis=1)
    dist = (X[:, None, :] != X[None, :, :]).sum(axis=2)
    D = rng.uniform(size=gr.shape) < rng.uniform(0.1, 0.7)
    if D.all() or not D.any(): continue
    inD = D[tuple(W[:, g] for g in range(G))]
    for kind in ('H', 'zero', 'add'):
        if kind == 'H': psi_t = gr.psiH_t
        elif kind == 'zero': psi_t = np.zeros(n + 1)
        else: psi_t = rng.uniform(-u, u) * np.arange(n + 1.0)
        psi = psi_t[tX]
        logw = tX * log(p) + (n - tX) * log(1 - p) - psi
        lnA = lse(logw)
        mu = np.exp(logw - lnA)
        s = u * dist + psi[:, None] - psi[None, :]
        s_out = np.where(inD[None, :], np.inf, s).min(axis=1)       # slack to the complement
        mu_D = mu[inD].sum(); phip = (mu[inD] * np.exp(s_out[inD])).sum(); phi = phip - mu_D
        dens = max(inD[tX == t].mean() for t in range(n + 1))
        a = gr.stats(D, None if kind == 'H' else psi_t)
        dev = max(abs(a[0] - log(mu_D)), abs(a[1] - log(phip)), abs(np.exp(a[2]) - phi) / max(phi, 1e-300) if phi > 1e-12 else 0.0, abs(a[3] - log(dens)))
        maxdev = max(maxdev, dev); ncase += 1
        # the deepest dip really multiplies A by 1 + Phi:  psi^D = max_{y notin D}[psi(y) - u d(.,y)] on D
        psiD = np.where(inD, (np.where(inD[None, :], -np.inf, psi[None, :] - u * dist)).max(axis=1), psi)
        lip = np.max(np.abs(psiD[:, None] - psiD[None, :]) - u * dist)
        ratio = np.exp(lse(tX * log(p) + (n - tX) * log(1 - p) - psiD) - lnA)
        maxdev = max(maxdev, abs(ratio - (1 + phi)) / (1 + phi)); assert lip < 1e-9
print(f"{ncase} (grouping, set, reference) cases, n <= 11: largest deviation between profile sums and brute force = {maxdev:.2e}  (also: deepest dip is u-Lipschitz and A(psi^D)/A(psi) = 1 + Phi)  [{time.time()-t0:.1f}s]")
