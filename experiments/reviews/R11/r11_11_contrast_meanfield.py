"""R11 / 11 -- task C, a consistency check with section 11.25 of the theory report, by the SAME code:
the game function over all site-wise labels (cones), exact enumeration, for
  (i)  a nearest-neighbour chain (flip probability p),
  (ii) known parts that are functions of the type (Curie-Weiss, pi ~ exp((bJ/2n) m^2), ferro- and
       antiferromagnetic), chosen with a comparable or larger variance of the magnetisation,
against the uniform cube n F_c(t).  Section 11.25 says (asymptotically, for symmetric instances
and fixed samples) that (ii) is never above the cube; workstream Y says that (i) is.
Also: the Renyi centre for (ii) is a function of the type (the optimal Q is exchangeable).

Run:  python3 r11_11_contrast_meanfield.py     (about 1 minute)
"""
import time
import numpy as np
from r11lib import *

T0 = time.time()
u = 1.0
h = u / 2
t = 0.45
print(f"u = 1, t = {t};  cube per site F_c(t) = {cube_F(t):.6f}")
for n in (8, 10, 12):
    s, _ = chain_law(n, 0.5)
    sf = s.T.astype(float)
    m = s.sum(axis=1).astype(float)
    labels = configs(n).astype(float)
    phis = -h * labels @ sf
    rows = []
    cases = [("cube", np.zeros(2 ** n))]
    for p in (0.4, 0.3):
        nfl = ((s[:, :-1] * s[:, 1:]) == -1).sum(axis=1)
        cases.append((f"chain p={p}", nfl * np.log(p) + (n - 1 - nfl) * np.log(1 - p)))
    for bJ in (0.5, 0.9, 1.5, -1.0, -4.0):
        cases.append((f"Curie-Weiss bJ={bJ}", (bJ / (2 * n)) * m ** 2))
    for name, logw in cases:
        logpi = logw - logsumexp(logw)
        pi = np.exp(logpi)
        logP = gibbs_logs(logpi, phis)
        lo, up, M = maximise_G_fast(logP, t)
        Q = np.exp(centre_of_M(logP, M, t))
        # is the centre a function of the type?  spread of ln Q within type classes
        spread = max((np.log(Q[m == k]).max() - np.log(Q[m == k]).min()) for k in np.unique(m))
        var_m = float(pi @ m ** 2 - (pi @ m) ** 2) / n
        rows.append(f"   {name:22s}: G/n = {lo/n:.6f} (dual over site-wise labels {up/n:.6f});  ratio to the cube {lo/(n*cube_F(t)):.3f};"
                    f"  Var(m)/n = {var_m:.3f};  spread of ln Q* within type classes {spread:.1e}")
    print(f"n = {n}:   [{time.time()-T0:.0f} s]")
    print("\n".join(rows), flush=True)
print(f"{time.time()-T0:.1f} s")
