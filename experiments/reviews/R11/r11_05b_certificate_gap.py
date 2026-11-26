"""R11 / 05b -- the certificate of r11_05 with a GAP, end to end by brute force:
two blocks of L sites separated by m gap sites (n = 2L + m), reduced end slopes u - kappa_m.
Checks: the embedded residuals are members of C_d (all edges), their Gibbs laws restricted to the
blocks are products, and G_t^{(n)}(M x M) on the FULL chain (gap letters included) = 2 G_t^{(L)}(M).

Run:  python3 r11_05b_certificate_gap.py     (seconds)
"""
import numpy as np
from r11lib import *

u = 1.0
t = 0.41
for p, L, m in ((0.2, 4, 1), (0.2, 4, 2), (0.1, 4, 3), (0.3, 5, 1)):
    lam = 1 - 2 * p
    kap = np.log((1 + lam ** (m + 1)) / (1 - lam ** (m + 1)))
    assert u - kap >= 0
    n = 2 * L + m
    s, pi = chain_law(n, p)
    N = 2 ** n
    sL, piL = chain_law(L, p)
    labels = configs(L).astype(float)
    hs = np.full(L, u / 2)
    hs[0] = hs[-1] = (u - kap) / 2
    phisL = -(labels * hs[None, :]) @ sL.T.astype(float)
    logPL = gibbs_logs(np.log(piL), phisL)
    G_L, up, M = maximise_G_fast(logPL, t)
    idx = np.arange(N)
    i1 = idx & (2 ** L - 1)                       # block 1 = sites 0..L-1
    i2 = idx >> (L + m)                           # block 2 = sites L+m..n-1
    e, st = L - 1, L + m
    same = (s[:, e] * s[:, st]) == 1
    lnrho = np.where(same, np.log(1 + lam ** (m + 1)), np.log(1 - lam ** (m + 1)))
    logpi = np.log(pi)
    worst_mem = -np.inf
    worst_prod = 0.0
    mt = np.zeros(N)
    nl = labels.shape[0]
    # marginal of the chain on the two blocks
    keyB = i1 + (i2 << L)
    for a in range(nl):
        if M[a] < 1e-12:
            continue
        for b in range(nl):
            if M[b] < 1e-12:
                continue
            psi = phisL[a][i1] + phisL[b][i2] + lnrho
            worst_mem = max(worst_mem, is_lipschitz(psi, n, [u] * n))
            lw = logpi - psi
            lp = lw - logsumexp(lw)
            margB = np.bincount(keyB, weights=np.exp(lp), minlength=2 ** (2 * L))
            prod = np.exp(logPL[a])[np.arange(2 ** (2 * L)) & (2 ** L - 1)] * np.exp(logPL[b])[np.arange(2 ** (2 * L)) >> L]
            worst_prod = max(worst_prod, float(np.abs(margB - prod).max()))
            mt += M[a] * M[b] * np.exp(t * lp)
    Gn = -t * logsumexp(np.log(mt) / t)
    print(f"p={p} L={L} m={m} (n={n}, end slope {u-kap:.3f}): members: largest edge violation {worst_mem:.1e};  block marginal = product: {worst_prod:.1e};"
          f"  G^(n)(M x M) = {Gn:.10f},  2 G^(L)(M) = {2*G_L:.10f}")
