"""R28 — a RIGID-rotamer model of capped leucine whose bond geometry is not the ff14SB equilibrium one
(CA-CB-CG = 109.5 deg) but the geometry relaxed once in one well and then rotated rigidly — the
situation of a table built by rigid rotation of a deposited or minimised geometry.

For each choice of geometry: the full 2.5-deg grid of (chi_1, chi_2) with every internal coordinate
other than chi_1, chi_2 frozen at the values of the chosen structure; then the reductions of item 100.
Geometries:  g0  the builder's own rigid geometry rebuilt through my Z-matrix extraction (CONTROL: must
                 reproduce the numbers of the original grid);
             g_mt  relaxed (side chain, CB, HA free; backbone frozen) at the relaxed minimum of the mt well;
             g_tp  the same at the relaxed minimum of the tp well.
Usage: python3 -B ff_relaxgeom.py H|E
"""
import r28_common as rc
rc.cap()
import itertools
import math
import sys
import time
import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, "/home/user/MetricChain/experiments/science/ws_P2")
t0 = time.time()
bb = sys.argv[1]
print("R28 ff_relaxgeom.py  start", rc.utc(), "backbone", bb)
import scbuild                                   # noqa: E402
import openmm                                    # noqa: E402
import openmm.app as app                         # noqa: E402
import openmm.unit as unit                       # noqa: E402
import ff_lib as fl                              # noqa: E402

KT = 0.596
BACKBONE = {"H": (-57.0, -47.0), "E": (-139.0, 135.0)}
phi0, psi0 = np.deg2rad(BACKBONE[bb])
pep = scbuild.SCPeptide("L", solvent=True)
I = pep.idx
Z_ORIG = list(pep.Z)
N = 144


def dih(X, a, b, c, d):
    b1, b2, b3 = X[b] - X[a], X[c] - X[b], X[d] - X[c]
    n1, n2 = np.cross(b1, b2), np.cross(b2, b3)
    return math.atan2(np.dot(np.cross(n1, n2), b2 / np.linalg.norm(b2)), np.dot(n1, n2))


def ang(X, a, b, c):
    u, v = X[a] - X[b], X[c] - X[b]
    return math.acos(np.dot(u, v) / np.linalg.norm(u) / np.linalg.norm(v))


QCHI = [(I[(1, "N")], I[(1, "CA")], I[(1, "CB")], I[(1, "CG")]), (I[(1, "CA")], I[(1, "CB")], I[(1, "CG")], I[(1, "CD1")])]


def extract_Z(X):
    """Z-matrix with the bond lengths, bond angles and dihedral offsets of the structure X (Angstrom)."""
    chi = [dih(X, *q) for q in QCHI]
    Znew = []
    for atom, a, b, c, bond, angle, kind, const in Z_ORIG:
        d = dih(X, a, b, c, atom)
        v = 0.0 if kind[0] == "fix" else (phi0 if kind[0] == "phi" else (psi0 if kind[0] == "psi" else chi[kind[1]]))
        Znew.append((atom, a, b, c, float(np.linalg.norm(X[atom] - X[c])), ang(X, b, c, atom), kind, d - v))
    return Znew, chi


def coords(Zm, chi_rad):
    pep.Z = Zm
    M = len(chi_rad)
    return pep.coords(np.full((M, 1), phi0), np.full((M, 1), psi0), chi_rad)


def grid_energy(Zm):
    axv = np.arange(N) * 2 * np.pi / N
    pts = np.array(list(itertools.product(range(N), repeat=2)))
    out = {nm: np.empty(len(pts)) for nm in ("bond", "angle", "tors", "nb", "gbn2")}
    for a in range(0, len(pts), 4000):
        e = pep.energies(coords(Zm, axv[pts[a:a + 4000]]))
        for nm in out:
            out[nm][a:a + 4000] = e[nm]
    for nm in out:
        out[nm] = out[nm].reshape(N, N)
    out["vac"] = out["bond"] + out["angle"] + out["tors"] + out["nb"]
    return out


# ------------------------------------------------------------------ relaxation (variant A of ff_flex.py)
ff = app.ForceField("amber14/protein.ff14SB.xml", "implicit/gbn2.xml")
sysm = ff.createSystem(pep.top, nonbondedMethod=app.NoCutoff, constraints=None, rigidWater=False, removeCMMotion=False, sasaMethod=None)
for (r, nm), a in I.items():
    if r in (0, 2) or nm in ("N", "H", "CA", "C", "O"):
        sysm.setParticleMass(a, 0.0)
ctx = openmm.Context(sysm, openmm.VerletIntegrator(0.001), openmm.Platform.getPlatformByName("CPU"), {"Threads": "1"})


def relax_free(chi_deg):
    pep.Z = Z_ORIG
    X0 = pep.coords(np.array([[phi0]]), np.array([[psi0]]), np.radians([chi_deg]))[0]
    ctx.setPositions(X0 * 0.1)
    openmm.LocalEnergyMinimizer.minimize(ctx, 1e-4, 0)
    st = ctx.getState(getEnergy=True, getPositions=True)
    return np.array(st.getPositions(asNumpy=True).value_in_unit(unit.angstrom)), st.getPotentialEnergy().value_in_unit(unit.kilocalorie_per_mole) / KT


def report(tag, G):
    E = fl.total_kT(G, "total")
    rm = fl.rotamer_models(E)
    ID = (60.0, 180.0, 300.0)
    a = rm["rot_min_state"]
    print(f"[{tag}] rigid table: minimum state ({ID[a[0]]:g}, {ID[a[1]]:g}), gap {rm['rot_gap']:.3f} kT; continuous minimum at ({rm['cont_min_deg'][0]:g}, {rm['cont_min_deg'][1]:g})"
          f" in cell {rm['cont_min_cell']}; same cell: {rm['same_cell']}")
    print(f"      TV(grid cells, rigid) = {rm['tv_r']:.4f}; TV(grid cells, cell-minimised) = {rm['tv_m']:.4f}; ln Z offsets per torsion: rigid {(rm['lnZ_rot'] - rm['lnZ']) / 2:+.4f},"
          f" minimised {(rm['lnZ_min'] - rm['lnZ']) / 2:+.4f}")
    print(f"      cells (2,1) / (1,0): population grid {rm['Pg'][2, 1]:.4f} / {rm['Pg'][1, 0]:.4f}; rigid table {rm['Pr'][2, 1]:.4f} / {rm['Pr'][1, 0]:.4f};"
          f" strain of the ideal rotamer above the cell minimum {rm['Erot'][2, 1] - rm['Emin'][2, 1]:.3f} / {rm['Erot'][1, 0] - rm['Emin'][1, 0]:.3f} kT;"
          f" cell minima {rm['Emin'][2, 1]:.3f} / {rm['Emin'][1, 0]:.3f} kT")
    return rm


# ------------------------------------------------------------------ g0: control
pep.Z = Z_ORIG
Xr = pep.coords(np.array([[phi0]]), np.array([[psi0]]), np.radians([[217.0, 93.0]]))[0]
Z0, chi0 = extract_Z(Xr)
rng = np.random.default_rng(2805)
ct = rng.uniform(0, 2 * np.pi, size=(20, 2))
d = np.abs(coords(Z0, ct) - coords(Z_ORIG, ct)).max()
print(f"control g0: Z-matrix extracted from the builder's own structure reproduces its coordinates at 20 random (chi_1, chi_2): largest difference {d:.1e} A"
      f" -> {'ok' if d < 1e-8 else 'FAILED'}")
G0 = grid_energy(Z0)
ref = np.load(f"/home/user/MetricChain/experiments/science/ws_R28/grid_L_{bb}_144.npz", allow_pickle=True)
dd = (np.abs(G0["vac"] - ref["vac"]) / np.maximum(1.0, np.abs(ref["vac"]))).max()
print(f"control g0: its energy grid against my original grid: largest relative difference {dd:.1e} -> {'ok' if dd < 1e-7 else 'FAILED'}")
report("g0 = builder geometry (CA-CB-CG 109.50)", G0)

for tag, start in (("g_mt", (287.5, 157.5) if bb == "H" else (267.5, 160.0)), ("g_tp", (190.0, 80.0) if bb == "H" else (195.0, 82.5))):
    Xrel, e = relax_free(start)
    Zr, chir = extract_Z(Xrel)
    cacbcg = math.degrees(ang(Xrel, I[(1, "CA")], I[(1, "CB")], I[(1, "CG")]))
    # the rigid model built on this geometry must reproduce the relaxed structure itself at its own chi
    back = np.abs(coords(Zr, np.array([chir]))[0] - Xrel).max()
    print(f"\n{tag}: geometry relaxed from {start}: chi = ({math.degrees(chir[0]) % 360:.2f}, {math.degrees(chir[1]) % 360:.2f}), CA-CB-CG = {cacbcg:.2f} deg,"
          f" N-CA-CB = {math.degrees(ang(Xrel, I[(1, 'N')], I[(1, 'CA')], I[(1, 'CB')])):.2f}, CB-CG-CD1 = {math.degrees(ang(Xrel, I[(1, 'CB')], I[(1, 'CG')], I[(1, 'CD1')])):.2f},"
          f" CB-CG-CD2 = {math.degrees(ang(Xrel, I[(1, 'CB')], I[(1, 'CG')], I[(1, 'CD2')])):.2f}; rebuild error {back:.1e} A")
    Gr = grid_energy(Zr)
    print(f"      bond + angle energy constant over the grid: ranges {np.ptp(Gr['bond']):.1e}, {np.ptp(Gr['angle']):.1e} kcal/mol")
    report(f"{tag}: rigid rotation of the geometry relaxed in the {tag[2:]} well (CA-CB-CG {cacbcg:.2f})", Gr)
    np.savez(f"/home/user/MetricChain/experiments/science/ws_R28/grid_L_{bb}_144_{tag}.npz", **Gr)
rc.finish(t0)
