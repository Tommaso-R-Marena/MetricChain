"""Validate fastff.FastFF against OpenMM's Reference (double precision) platform.
Run: python3 validate_fast.py   (prints max abs deviations per component, kcal/mol)."""
import math, time
import numpy as np
from pepbuild import Peptide
from fastff import FastFF

rng = np.random.default_rng(1)
worst = {}
for n in (1, 2, 3, 5, 8):
    P = Peptide(n, platform="Reference")
    F = FastFF(P)
    M = 150
    phi = rng.uniform(-math.pi, math.pi, (M, n)); psi = rng.uniform(-math.pi, math.pi, (M, n))
    # half random torsions (many clashes), half from the basin grid (few clashes)
    gphi = np.deg2rad(rng.choice([-150.0, -70.0, 60.0], (M // 2, n)))
    gpsi = np.deg2rad(rng.choice([-40.0, 60.0, 150.0], (M // 2, n)))
    phi[: M // 2] = gphi; psi[: M // 2] = gpsi
    X = P.coords(phi, psi)
    t0 = time.time(); E = P.energies(X); t1 = time.time(); Ef = F.energies(X); t2 = time.time()
    cs = P.clash_score(X)
    ok = cs > 0.5          # exclude overlapping atoms, where energies are 1e6+ and abs errors meaningless
    comp = {
        "tors": (E["tors"], Ef["tors"]),
        "lj": (E["lj"], Ef["lj"]),
        "coul": (E["nb"] - E["lj"], Ef["coul"]),
        "gbn2": (E["gbn2"], Ef["gbn2"]),
        "sa": (E["gbn2sa"] - E["gbn2"], Ef["sa"]),
        "obc2": (E["obc2"], Ef["obc2"]),
    }
    for ff in P.extra:
        comp[ff + "_tors"] = (E[ff + "_tors"], Ef[ff + "_tors"])
        comp[ff + "_nb"] = (E[ff + "_nb"], Ef[ff + "_lj"] + Ef[ff + "_coul"])
    print(f"n={n} atoms={P.natoms}  OpenMM(Reference) {1e3*(t1-t0)/M:.2f} ms/conf, numpy {1e6*(t2-t1)/M:.1f} us/conf; "
          f"{ok.sum()} of {M} conformations with clash score > 0.5")
    for k, (a, b) in comp.items():
        d = np.abs(a - b)[ok].max()
        rel = (np.abs(a - b) / np.maximum(1.0, np.abs(a)))[~ok].max() if (~ok).any() else 0.0
        worst[k] = max(worst.get(k, 0.0), d)
        print(f"   {k:14s} max|dev| {d:.2e} kcal/mol (clash-free);  max rel dev on overlapping conformations {rel:.1e}")
print("worst over all sizes:", {k: f"{v:.1e}" for k, v in worst.items()})
