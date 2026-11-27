"""Validation of the geometry builder and the energy evaluators (run: python3 test_build.py)."""
import math, time, sys
import numpy as np
import openmm, openmm.unit as unit
from pepbuild import Peptide, dihedral, KCAL, KT300

rng = np.random.default_rng(0)
for n in (1, 2, 3, 5):
    t0 = time.time()
    P = Peptide(n)
    t1 = time.time()
    M = 200
    phi = rng.uniform(-math.pi, math.pi, (M, n))
    psi = rng.uniform(-math.pi, math.pi, (M, n))
    X = P.coords(phi, psi)
    I = P.idx
    # 1. bond lengths and all force-field angles
    maxb = 0.0
    for (i, j), r in P.r0.items():
        maxb = max(maxb, np.abs(np.linalg.norm(X[:, i] - X[:, j], axis=1) - r).max())
    dev = []
    for (i, j, k), th in P.a0.items():
        u = X[:, i] - X[:, j]; v = X[:, k] - X[:, j]
        ang = np.arccos((u * v).sum(1) / np.linalg.norm(u, axis=1) / np.linalg.norm(v, axis=1))
        dev.append(((ang - th) * 180 / math.pi))
    dev = np.array(dev)
    # 2. torsions
    errs = []
    for k in range(1, n + 1):
        ph = dihedral(X, I[(k - 1, "C")], I[(k, "N")], I[(k, "CA")], I[(k, "C")])
        nxt = I[(k + 1, "N")]
        ps = dihedral(X, I[(k, "N")], I[(k, "CA")], I[(k, "C")], nxt)
        errs.append(np.abs(np.angle(np.exp(1j * (ph - phi[:, k - 1])))).max())
        errs.append(np.abs(np.angle(np.exp(1j * (ps - psi[:, k - 1])))).max())
        # omega
        ca_next = I[(k + 1, "CA")] if k < n else I[(k + 1, "CH3")]
        om = dihedral(X, I[(k, "CA")], I[(k, "C")], nxt, ca_next)
        errs.append(np.abs(np.abs(om) - math.pi).max())
        # chirality: (N-CA).((C-CA)x(CB-CA)) > 0 for L
        a = X[:, I[(k, "N")]] - X[:, I[(k, "CA")]]
        b = X[:, I[(k, "C")]] - X[:, I[(k, "CA")]]
        c = X[:, I[(k, "CB")]] - X[:, I[(k, "CA")]]
        chir = (a * np.cross(b, c)).sum(1)
    E = P.energies(X)
    t2 = time.time()
    print(f"n={n} atoms={P.natoms} setup {t1-t0:.2f}s  energies {1e3*(t2-t1)/M:.3f} ms/conf")
    print(f"   max bond dev {maxb:.2e} A; angle dev (deg): max |dev| {np.abs(dev).max():.3f}, "
          f"angles with |dev|>0.01: {np.sum(np.abs(dev).max(1) > 0.01)} of {dev.shape[0]}; "
          f"spread over conformations {np.ptp(dev,axis=1).max():.2e}")
    print(f"   max torsion error {max(errs):.2e} rad; chiral volume {chir.min():.3f}..{chir.max():.3f} A^3 (L: >0)")
    print(f"   bond energy {E['bond'].min():.6f}..{E['bond'].max():.6f}; angle energy {E['angle'].min():.6f}..{E['angle'].max():.6f} kcal/mol")
    for k in ("tors", "nb", "lj", "gbn2", "gbn2sa", "obc2", "ff99SB", "ff19SB", "ff03", "ff15ipq"):
        print(f"   {k:8s} min {E[k].min():12.3f} median {np.median(E[k]):12.3f} max {E[k].max():14.3f}")
    cs = P.clash_score(X)
    print(f"   clash score quantiles (random torsions): {np.quantile(cs,[0,0.1,0.5,0.9,1])}")
