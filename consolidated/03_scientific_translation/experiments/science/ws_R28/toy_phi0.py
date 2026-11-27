"""R28 — item 98, slip (1): the text gives the one-body terms as 1.5(1 + cos 3x); the script has random phases phi_i.
Their instance (seed 20261126, their theta) with phi_i = 0 (wells centred in the three 120-degree cells) against
their instance as run: mixed width per angle (best of their nine thresholds) at k = 3, 6, 12."""
import r28_common as rc
rc.cap()
import time
import numpy as np
import toy_lib as tl

t0 = time.time()
print("R28 toy_phi0.py  start", rc.utc())
n, N = 8, 1440
THRS = (np.inf, 6, 4, 3, 2, 1.5, 1, 0.5, -1.0)
x = tl.grid(N)
for label, zero in (("phi_i random (as run)", False), ("phi_i = 0 (as the text reads)", True)):
    rng = np.random.default_rng(20261126)
    phi = rng.uniform(0, 2 * np.pi, n)
    theta = rng.uniform(0, 2 * np.pi, n - 1)
    if zero:
        phi = np.zeros(n)
    e = [1.5 * (1.0 + np.cos(3.0 * x + phi[i])) for i in range(n)]
    pair = [2.0 * np.cos(x[:, None] - x[None, :] - theta[i]) for i in range(n - 1)]
    ch = tl.Chain([np.exp(-ee) for ee in e], pair, None)
    ex = ch.lnZ_exact()
    out = []
    for k in (3, 6, 12, 24, 48):
        idx, tw = tl.cell_index(N, k)
        cs = tl.Cells(ch, idx, tw)
        lj = cs.lnZ_jensen()
        ups = [cs.lnZ_upper(cs.modes_by_threshold(t)) for t in THRS]
        assert lj <= ex + 1e-10 and all(ex <= u + 1e-10 for u in ups)
        out.append(f"k={k}: first-order {(cs.lnZ_minima() - cs.lnZ_maxima())/n:.4g}, all-H {(ups[0] - lj)/n:.4g}, mixed {(min(ups) - lj)/n:.4g}")
    print(f"{label}:  " + ";  ".join(out))
rc.finish(t0)
