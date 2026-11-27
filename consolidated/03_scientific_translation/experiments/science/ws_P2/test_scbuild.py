"""Validation of scbuild.SCPeptide (run: python3 -B test_scbuild.py).

1. Regression: for poly-Ala the new builder reproduces P's pepbuild.Peptide coordinates exactly.
2. Geometry of every residue type used (homopolymers n = 3 and the heteropolymer LKSE):
   bond lengths against the ff14SB equilibrium values (all bonds of the force field, including
   the ring-closure bond of Phe), bond angles (deviation from equilibrium and -- the important
   property -- constancy over conformations), recovered chi, chirality at CA, constancy of the
   bond and angle energies.
3. Energies: P's numpy evaluator fastff.FastFF against OpenMM's Reference (double precision)
   platform on random states (continuous random chi and grid chi; random and ideal backbones).
"""
import math, time, sys
import numpy as np
from scbuild import SCPeptide, dihedral, NCHI, KCAL
from pepbuild import Peptide
from fastff import FastFF

rng = np.random.default_rng(0)
np.set_printoptions(precision=4, suppress=True, linewidth=200)

# ---------------------------------------------------------------- 1. regression against P
for n in (1, 3):
    P0 = Peptide(n, extra_ffs=(), solvent=False)
    P1 = SCPeptide("A" * n, extra_ffs=(), solvent=False)
    phi = rng.uniform(-math.pi, math.pi, (50, n)); psi = rng.uniform(-math.pi, math.pi, (50, n))
    d = np.abs(P0.coords(phi, psi) - P1.coords(phi, psi)).max()
    same_names = [a.name for a in P0.top.atoms()] == [a.name for a in P1.top.atoms()]
    print(f"regression poly-Ala n={n}: atom names identical {same_names}; max |coordinate difference| = {d:.1e} A")
    assert same_names and d < 1e-12

# ---------------------------------------------------------------- 2. + 3.
BB = {"H": (-57.0, -47.0), "E": (-139.0, 135.0), "P2": (-75.0, 145.0)}
worst = {}
for seq in ("VVV", "LLL", "SSS", "FFF", "KKK", "EEE", "LKSE", "LKSELKSE"):
    t0 = time.time()
    P = SCPeptide(seq, extra_ffs=("ff99SB", "ff03", "ff15ipq"), platform="Reference")
    F = FastFF(P, threads=1)
    n = P.n
    M = 120
    # one third: random backbone + random continuous chi; one third: ideal backbones + grid chi;
    # one third: ideal backbones + random chi
    phi = rng.uniform(-math.pi, math.pi, (M, n)); psi = rng.uniform(-math.pi, math.pi, (M, n))
    chi = rng.uniform(-math.pi, math.pi, (M, P.nchi))
    for m in range(M // 3, M):
        b = BB[("H", "E", "P2")[m % 3]]
        phi[m] = math.radians(b[0]); psi[m] = math.radians(b[1])
    chi[M // 3: 2 * M // 3] = np.deg2rad(rng.choice([-60.0, 180.0, 60.0], (2 * M // 3 - M // 3, P.nchi)))
    X = P.coords(phi, psi, chi)
    I = P.idx
    maxb = 0.0
    for (i, j), r in P.r0.items():
        maxb = max(maxb, np.abs(np.linalg.norm(X[:, i] - X[:, j], axis=1) - r).max())
    dev = []
    for (i, j, k), th in P.a0.items():
        u = X[:, i] - X[:, j]; v = X[:, k] - X[:, j]
        ang = np.arccos(np.clip((u * v).sum(1) / np.linalg.norm(u, axis=1) / np.linalg.norm(v, axis=1), -1, 1))
        dev.append((ang - th) * 180 / math.pi)
    dev = np.array(dev)
    errs = []
    for col, q in enumerate(P.chi_quads()):
        got = dihedral(X, *q)
        errs.append(np.abs(np.angle(np.exp(1j * (got - chi[:, col])))).max())
    chir = []
    for k in range(1, n + 1):
        ph = dihedral(X, I[(k - 1, "C")], I[(k, "N")], I[(k, "CA")], I[(k, "C")])
        ps = dihedral(X, I[(k, "N")], I[(k, "CA")], I[(k, "C")], I[(k + 1, "N")])
        errs.append(np.abs(np.angle(np.exp(1j * (ph - phi[:, k - 1])))).max())
        errs.append(np.abs(np.angle(np.exp(1j * (ps - psi[:, k - 1])))).max())
        a = X[:, I[(k, "N")]] - X[:, I[(k, "CA")]]
        b = X[:, I[(k, "C")]] - X[:, I[(k, "CA")]]
        c = X[:, I[(k, "CB")]] - X[:, I[(k, "CA")]]
        chir.append((a * np.cross(b, c)).sum(1))
    chir = np.array(chir)
    t1 = time.time()
    E = P.energies(X)
    t2 = time.time()
    Ef = F.energies(X)
    t3 = time.time()
    with np.errstate(divide="ignore"):
        cs = P.clash_score(X)
    ok = cs > 0.5
    assert np.allclose(cs, Ef["clash"], rtol=1e-9), "FastFF clash score differs from Peptide.clash_score"
    print(f"\n{seq}: atoms={P.natoms} nchi={P.nchi} net charge {P.charges.sum():+.4f}; setup {t1-t0:.1f}s; "
          f"OpenMM Reference {1e3*(t2-t1)/M:.2f} ms/conf; FastFF {1e3*(t3-t2)/M:.3f} ms/conf; "
          f"{int(ok.sum())} of {M} conformations with clash score > 0.5")
    print(f"   max bond dev {maxb:.2e} A (all {len(P.r0)//2} force-field bonds); angle dev from equilibrium (deg): max {np.abs(dev).max():.3f}, "
          f"angles with |dev| > 0.01: {int(np.sum(np.abs(dev).max(1) > 0.01))} of {dev.shape[0]//2*2}; "
          f"spread over conformations {np.ptp(dev, axis=1).max():.2e}")
    print(f"   max dihedral error (phi, psi, chi) {max(errs):.2e} rad; chiral volume at CA {chir.min():.3f}..{chir.max():.3f} A^3 (L: > 0)")
    print(f"   bond energy {E['bond'].min():.3e}..{E['bond'].max():.3e}; angle energy {E['angle'].min():.6f}..{E['angle'].max():.6f} kcal/mol "
          f"(spread {np.ptp(E['angle']):.1e})")
    assert maxb < 1e-9 and np.ptp(dev, axis=1).max() < 1e-8 and max(errs) < 1e-9 and chir.min() > 0
    comp = {"tors": (E["tors"], Ef["tors"]), "lj": (E["lj"], Ef["lj"]), "coul": (E["nb"] - E["lj"], Ef["coul"]),
            "gbn2": (E["gbn2"], Ef["gbn2"]), "sa": (E["gbn2sa"] - E["gbn2"], Ef["sa"]), "obc2": (E["obc2"], Ef["obc2"])}
    for ff in P.extra:
        comp[ff + "_tors"] = (E[ff + "_tors"], Ef[ff + "_tors"])
        comp[ff + "_nb"] = (E[ff + "_nb"], Ef[ff + "_lj"] + Ef[ff + "_coul"])
        # the other force field's total = tors + nb + (bond + angle, which must be constant)
        rest = E[ff] - E[ff + "_tors"] - E[ff + "_nb"]
        # reference = a clash-free conformation (on overlapping conformations the subtraction loses digits)
        comp[ff + "_bonded_const"] = (rest, np.full(M, rest[np.flatnonzero(ok)[0]] if ok.any() else rest[0]))
    line = "   max |FastFF - OpenMM Reference| (kcal/mol, clash-free conformations): "
    for k, (a, b) in comp.items():
        dd = np.abs(a - b)[ok].max() if ok.any() else float("nan")
        worst[k] = max(worst.get(k, 0.0), dd)
        line += f"{k} {dd:.1e}; "
    print(line)
    print(f"   ranges on clash-free conformations: GBn2 {E['gbn2'][ok].min():.1f}..{E['gbn2'][ok].max():.1f}; "
          f"coul {Ef['coul'][ok].min():.1f}..{Ef['coul'][ok].max():.1f}; lj {Ef['lj'][ok].min():.1f}..{Ef['lj'][ok].max():.1f} kcal/mol")
print("\nworst over all systems:", {k: f"{v:.1e}" for k, v in worst.items()})
