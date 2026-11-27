import time, sys
import numpy as np
from r10lib import *
from r10search import *
from r10slp import *
t0 = time.time()
bJ = 1.5
M = Model(bJ=bJ, bB=0.0, u=1.0)
phip = lambda k: -2 * bJ * (2 * k - 1)
# start: binary optimum at e = 0.02, expect ascent towards the free-block optimum (0.0161548)
for e, start in ((0.02, binary(0.5, 0.3055, 0.3055)), (0.0, binary(0.5, 0.29803, 0.29803)), (0.02, (np.array([0.3, 0.3, 0.4]), np.array([0.2, 0.5, 0.8])))):
    lam, mu = start
    print("start", e, fmt(lam, mu), r_mu(M, lam, mu, e))
    val, lam, mu, hist = slp(M, lam, mu, e, phip, verbose=True)
    print("  end", val, fmt(lam, mu), "time", time.time() - t0, flush=True)
