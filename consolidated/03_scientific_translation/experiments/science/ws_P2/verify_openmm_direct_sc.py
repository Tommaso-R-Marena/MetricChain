"""Independent end-to-end check of the central numbers (the analogue of ws_P/verify_openmm_direct.py):
Ace-(Ser)3-NMe on the strand E, all 9^3 = 729 rotamer assignments, GBn2 polarisation energy
from OpenMM's own CustomGBForce on the Reference (double precision) platform and the vacuum
energy from OpenMM's torsion + nonbonded force groups -- no fastff, no fbmodel tables, no anlib;
coordinates from the full internal-coordinate build; constants by explicit loops.
Expected (out/an_fb_S3_E_R3_t0.60_tau0.70.json, i.e. the table-based pipeline):
c_i(g_GB) = 4.81 4.12 4.32; c_12, c_13, c_23 = 1.306 2.426 1.308; c_123(g_GB) = 0.00403;
c_123(f) = 0 to rounding.  Observed with this script: identical (logs/verify_openmm_direct_sc.log)."""
import itertools, math
import numpy as np
from scbuild import SCPeptide

P = SCPeptide("SSS", extra_ffs=(), platform="Reference")
vals = [-60.0, 180.0, 60.0]
rot = list(itertools.product(vals, repeat=2))                 # 9 rotamers (chi1, hydroxyl torsion)
states = list(itertools.product(range(9), repeat=3))
chi = np.deg2rad(np.array([[rot[s[r]][j] for r in range(3) for j in range(2)] for s in states]))
phi = np.full((len(states), 3), math.radians(-139.0)); psi = np.full((len(states), 3), math.radians(135.0))
X = P.coords(phi, psi, chi)
with np.errstate(divide="ignore"):
    clash = P.clash_score(X)
E = P.energies(X)
g = E["gbn2"]; f = E["tors"] + E["nb"]
idx = {s: i for i, s in enumerate(states)}
print("assignments:", len(states), "; clash score min", round(float(clash.min()), 3), "(all > 0.70:", bool((clash > 0.70).all()), ")")
for name, h in (("g_GB", g), ("f", f)):
    c1 = np.zeros(3); c2 = np.zeros((3, 3)); c3 = 0.0
    for s in states:
        for i in range(3):
            for a in range(9):
                if a == s[i]: continue
                t = list(s); t[i] = a
                c1[i] = max(c1[i], abs(h[idx[s]] - h[idx[tuple(t)]]))
                for j in range(i + 1, 3):
                    for b in range(9):
                        if b == s[j]: continue
                        u = list(s); u[j] = b; v = list(t); v[j] = b
                        d2 = h[idx[s]] - h[idx[tuple(t)]] - h[idx[tuple(u)]] + h[idx[tuple(v)]]
                        c2[i, j] = max(c2[i, j], abs(d2))
    for s in states:                      # third order: sites 0, 1, 2
        for a in range(9):
            if a == s[0]: continue
            for b in range(9):
                if b == s[1]: continue
                for c in range(9):
                    if c == s[2]: continue
                    tot = 0.0
                    for bits in itertools.product((0, 1), repeat=3):
                        y = (a if bits[0] else s[0], b if bits[1] else s[1], c if bits[2] else s[2])
                        tot += (-1) ** sum(bits) * h[idx[y]]
                    c3 = max(c3, abs(tot))
    print(f"{name}: c_i = {np.round(c1, 2)}; c_12, c_13, c_23 = {c2[0,1]:.3f} {c2[0,2]:.3f} {c2[1,2]:.3f}; c_123 = {c3:.2e} kcal/mol")
