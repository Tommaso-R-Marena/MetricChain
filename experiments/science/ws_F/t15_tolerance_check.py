"""Ingredient check of Theorem tau by exhaustive enumeration (n = 12): base  (tau/4) pi_gamma^n + (1 - tau/4) Bern(c_0)^n,
alternative = base + average of N dips at i.i.d. Bern(m) centres, depth e^r = 1 + 8/tau.  Claim checked: every marginal
of order <= 3 of the alternative is within tau of the base's (the proof gives 3 tau/4 for 'good' lists of the size N of
the theorem; here N is much smaller than the theorem's and the list is simply random)."""
import numpy as np, sys, itertools
from sl import *
from t03_enum_adaptive import cube, popcount, in_class
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s); sys.stdout.flush()
rng = np.random.default_rng(7)
for (n, p, u, tau, N) in ((12, 0.3, 1.0, 0.1, 400), (12, 0.1, 2.0, 0.1, 400), (12, 0.3, 1.0, 0.03, 2000)):
    E = E_threshold(p, u); R, t, m, Q, g = Rmax(p, u, 0.0, return_all=True)
    X, bits, wt = cube(n); q = 1 - p
    pi = p ** wt * q ** (n - wt)
    w1 = np.exp(-g * wt); w1 /= (pi * w1).sum()
    c0 = cone_density(p, u, m); gc = gamma_of_density(p, c0)
    wc = np.exp(-gc * wt); wc /= (pi * wc).sum()
    b = 4 / tau - 1
    w0 = w1 + b * wc
    r = np.log(1 + 8 / tau)
    exc = np.zeros(2 ** n)
    for _ in range(N):
        sbits = rng.random(n) < m
        s = int(sum(1 << i for i in range(n) if sbits[i]))
        c = np.exp(-u * popcount(X ^ s)); c /= (pi * c).sum()
        exc += np.maximum(np.exp(r) * c - w1, 0.0) / N
    walt = w0 + exc
    ok0, _ = in_class(w0, n, u); ok1, _ = in_class(walt, n, u)
    mu0 = pi * w0; A0 = mu0.sum(); mu0 /= A0; mu1 = pi * walt; A1 = mu1.sum(); mu1 /= A1
    worst = {}
    B = bits.astype(float)
    for order in (1, 2, 3):
        dev = 0.0
        for S in itertools.combinations(range(n), order):
            for a in itertools.product((0, 1), repeat=order):
                ind = np.ones(2 ** n)
                for i, ai in zip(S, a): ind *= B[:, i] if ai else 1 - B[:, i]
                dev = max(dev, abs((mu1 * ind).sum() - (mu0 * ind).sum()))
        worst[order] = dev
    P(f"n={n} p={p} u={u} tau={tau} N={N}: in class {ok0},{ok1}; separation ln A(alt)/A(base) = {np.log(A1/A0):.4f}; max deviation of marginals: order 1: {worst[1]:.4f}, order 2: {worst[2]:.4f}, order 3: {worst[3]:.4f}  (tolerance tau = {tau})")
open('out/t15_tolerance_check.txt', 'w').write('\n'.join(out) + '\n')
