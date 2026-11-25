import time
import numpy as np
from r10lib import *
M = Model(bJ=1.5, bB=0.0, u=1.0)
ref = None
for k in (2, 3, 5):
    for kw in (dict(G=400, zooms=5, ncand=6, nz=41, rounds=8), dict(), dict(G=64, zooms=3, ncand=3), dict(G=96, both=False)):
        t0 = time.time(); n = 60; acc = []
        rng = np.random.default_rng(1)
        for _ in range(n):
            lam = rng.dirichlet(np.ones(k)); mu = rng.random(k)
            acc.append(r_mu(M, lam, mu, 0.0, **kw))
        acc = np.array(acc)
        if kw.get('G') == 400: ref = acc
        print(k, kw, "ms/call %.2f" % (1000 * (time.time() - t0) / n), "max diff to ref %.2e" % np.nanmax(np.abs(acc - ref)), "max over %.2e" % np.nanmax(acc - ref))
