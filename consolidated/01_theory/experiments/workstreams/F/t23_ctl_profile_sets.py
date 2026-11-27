"""t23: Theorem F6 (converse tail lemma for the reference H) tested on profile sets of many shapes, exact sums.

For a centre s (k ones) and a set D that is a union of profile classes (i, j), compute exactly
    theta = -(1/n) ln mu_H(D),      e = (1/n) ln Phi_H^+(D),     Phi_H^+(D) = sum_{x in D} mu_H(x) exp(s_H(x -> D^c)),
and compare with the claimed exponent  chi(theta) = (R^max)^{-1}(theta)  ( = -theta for theta >= a ):
Theorem F6 says e <= chi(theta) + o(1).  Shapes: balls with type-dependent radii, Hamming balls, anisotropic balls
{alpha i + beta j < c}, rectangles, far-side corners, bands that do not contain the centre, random staircases.
The theorem concerns sets of exponentially small measure; at finite n we test it with omega_n = 3 ln(n)/n on the sets with
theta >= 6 ln(n)/n:  e <= chi(theta - omega_n) + omega_n.  Also reported: the raw difference e - chi(theta) (close to 0 from
above for the extremal shapes, by a few ln(n)/n; negative for the others)."""
import math, sys, time
import numpy as np
from flib import *
from birad import *

n = int(sys.argv[1]) if len(sys.argv) > 1 else 600
rng = np.random.default_rng(23)
t0 = time.time()
for p, u in ((0.1, 2.0), (0.3, 1.0), (0.5, 1.0)):
    wp = WorstPair(p, u)
    es = np.linspace(wp.ec - 0.3, wp.E, 20001)
    Rs = wp.R(es)                         # decreasing in e
    def chi(theta):                        # inverse of R^max
        if theta >= Rs[0]:
            return -theta
        if theta <= 0:
            return wp.E
        return float(np.interp(theta, Rs[::-1], es[::-1]))
    tt = np.arange(n + 1)
    lwH_t = logw_H(n, p, u, tt)
    lnZH = float(np.log(np.sum(np.exp(lnC(n, tt) + tt * math.log(p) + (n - tt) * math.log(1 - p) + lwH_t))))
    worst = (-math.inf, None); worst_raw = (-math.inf, None); count = 0; skipped = 0; best_by_shape = {}
    for kfrac in (0.05, 0.2, 0.35, 0.5, 0.65, 0.8, 0.95):
        k = int(round(kfrac * n))
        C = Centre(n, k, p)
        ii, jj = np.broadcast_arrays(C.i, C.j)
        lw0 = lwH_t[C.t]
        shapes = []
        for th in (0.01, 0.03, 0.06, 0.1, 0.2):
            ins, _ = C.density_ball(-n * th); shapes.append(("density ball", ins))
        for rfrac in (0.05, 0.15, 0.25, 0.35, 0.45):
            shapes.append(("Hamming ball", C.dist <= rfrac * n))
        for _ in range(40):
            al, be = rng.uniform(0.2, 3.0, size=2); c = rng.uniform(0.02, 0.6) * n * max(al, be)
            shapes.append(("anisotropic ball", al * ii + be * jj < c))
        for _ in range(25):
            i0, j0 = int(rng.uniform(0, 1) * k), int(rng.uniform(0, 1) * (n - k))
            shapes.append(("rectangle", (ii <= i0) & (jj <= j0)))
            shapes.append(("far corner", (ii >= i0) & (jj >= j0)))
        for _ in range(25):
            al, be = rng.uniform(0.2, 3.0, size=2); c1 = rng.uniform(0.02, 0.4) * n * max(al, be); c2 = c1 + rng.uniform(0.02, 0.3) * n
            shapes.append(("band", (al * ii + be * jj >= c1) & (al * ii + be * jj < c2)))
        for _ in range(25):
            steps = np.sort(rng.integers(0, n - k + 1, size=k + 1))[::-1]          # j < steps[i]: a staircase (down-set of the grid)
            shapes.append(("staircase", jj < steps[:, None]))
        for name, ins in shapes:
            if not ins.any() or ins.all():
                continue
            lw1 = C.lower_envelope_logw(lw0, ins, u)
            mass = C.logmass[ins]
            ln_mu = float(logsumexp(mass + lw0[ins])) - lnZH
            ln_phi = float(logsumexp(mass + lw1[ins])) - lnZH
            theta, e = -ln_mu / n, ln_phi / n
            # the theorem is a statement for theta bounded away from 0 (sets of exponentially small measure); with the
            # o(1) terms of a finite n we compare at theta - slack, slack = 3 ln(n)/n, and only for theta >= 2 slack
            slack = 3 * math.log(n) / n
            if theta < 2 * slack:
                skipped += 1
                continue
            gap = e - chi(theta - slack) - slack
            raw = e - chi(theta)
            count += 1
            best_by_shape[name] = max(best_by_shape.get(name, -math.inf), raw)
            if gap > worst[0]:
                worst = (gap, (name, kfrac, round(theta, 5), round(e, 5), round(chi(theta), 5)))
            if raw > worst_raw[0]:
                worst_raw = (raw, (name, kfrac, round(theta, 5), round(e, 5), round(chi(theta), 5)))
    print(f"p={p} u={u} n={n}: {count} sets with theta >= 6 ln(n)/n = {6*math.log(n)/n:.4f} ({skipped} larger sets skipped);")
    print(f"     largest e - chi(theta - 3 ln n/n) - 3 ln n/n = {worst[0]:+.5f} at {worst[1]}   (Theorem F6 with omega_n = 3 ln n/n: must be <= 0)")
    print(f"     largest raw e - chi(theta) = {worst_raw[0]:+.5f} at {worst_raw[1]}   [{time.time()-t0:.0f}s]")
    print("     raw, by shape: " + ", ".join(f"{k_}: {v_:+.4f}" for k_, v_ in sorted(best_by_shape.items())))
