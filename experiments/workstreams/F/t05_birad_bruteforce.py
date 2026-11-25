"""t05: the bi-radial machinery (birad.py) against brute force on the full cube, n <= 12:
profile counts, type densities, McShane envelopes, partition sums, Lipschitz property of psi_H."""
import math, itertools, numpy as np
from birad import *

rng = np.random.default_rng(5)
bad = 0; checks = 0
for n in (6, 9, 12):
    N = 2 ** n
    xs = np.arange(N)
    bits = ((xs[:, None] >> np.arange(n)[None, :]) & 1)
    pop = bits.sum(1)
    Dm = None
    if n <= 12:
        Dm = np.array([[bin(a ^ b).count("1") for b in range(N)] for a in range(N)], dtype=np.int16) if n <= 9 else None
    for trial in range(6):
        p = float(rng.uniform(0.05, 0.6)); u = float(rng.uniform(0.3, 2.5))
        k = int(rng.integers(0, n + 1))
        s = sum(1 << b for b in rng.choice(n, size=k, replace=False))
        sb = ((s >> np.arange(n)) & 1)
        i_of = ((sb[None, :] == 1) & (bits == 0)).sum(1)
        j_of = ((sb[None, :] == 0) & (bits == 1)).sum(1)
        C = Centre(n, k, p)
        # counts
        cnt = np.zeros((k + 1, n - k + 1))
        np.add.at(cnt, (i_of, j_of), 1)
        if np.abs(cnt - np.exp(C.logcount)).max() > 1e-6: bad += 1
        checks += 1
        logpi = pop * math.log(p) + (n - pop) * math.log(1 - p)
        # a density ball
        logq = math.log(float(rng.uniform(0.02, 0.9)))
        inside, mx = C.density_ball(logq)
        ins_pt = inside[i_of, j_of]
        dens = [ins_pt[pop == t].mean() if (pop == t).any() else 0 for t in range(n + 1)]
        if abs(max(dens) - (math.exp(mx) if mx > -700 else 0.0)) > 1e-9 or max(dens) > math.exp(logq) + 1e-9: bad += 1
        if abs(math.exp(C.max_logdens(inside)) - max(dens)) > 1e-9 and max(dens) > 0: bad += 1
        checks += 2
        # maximality: adding the next shell of any type violates the density bound
        # instance: psi_H
        lwH_t = logw_H(n, p, u, np.arange(n + 1))
        psiH = -lwH_t[pop]
        if Dm is not None:
            if not (np.abs(psiH[:, None] - psiH[None, :]) <= u * Dm + 1e-9).all(): bad += 1
            checks += 1
            for name, lw_pt in (("flat", np.zeros(N)), ("H", lwH_t[pop]), ("add", -0.37 * u * pop), ("cone", -u * (i_of + j_of).astype(float))):
                lw_grid = np.zeros((k + 1, n - k + 1)); lw_grid[i_of, j_of] = lw_pt
                out = ~ins_pt
                if out.all() or (~out).all():
                    continue
                lo_b = (lw_pt[out][None, :] + u * Dm[np.ix_(~out, out)]).min(1)     # largest weight on D
                up_b = (lw_pt[out][None, :] - u * Dm[np.ix_(~out, out)]).max(1)     # smallest weight on D
                lo_g = C.lower_envelope_logw(lw_grid, inside, u)[i_of, j_of][~out]
                up_g = C.upper_envelope_logw(lw_grid, inside, u)[i_of, j_of][~out]
                if np.abs(lo_b - lo_g).max() > 1e-9 or np.abs(up_b - up_g).max() > 1e-9: bad += 1
                A_b = math.log(np.exp(logpi + lw_pt).sum())
                if abs(A_b - C.logA(lw_grid)) > 1e-9: bad += 1
                checks += 2
print(f"checks: {checks}, failures: {bad}")
