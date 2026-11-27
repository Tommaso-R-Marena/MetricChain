"""R28 — my own energy-grid generator for Ace-X..-NMe blocks, calling workstream P2's builder
(scbuild.SCPeptide, imported unmodified) through a code path different from the script under
review: Peptide.energies() (one OpenMM call per force group) instead of the combined group masks.

Stores per force group: bond, angle, tors, nb, lj, gbn2 (kcal/mol) for every grid point.
Checks (each can fail):
 G1  the built coordinates have the dihedrals they are said to have (phi, psi of every residue,
     chi_1 = N-CA-CB-XG, chi_2 = CA-CB-XG-XD(1)), measured with my own dihedral function;
 G2  bond + angle are constant over the grid (rigid geometry);
 G3  at a few conformations the builder's vacuum + GBn2 energy equals the total energy of a FRESH
     OpenMM system made from amber14/protein.ff14SB.xml + implicit/gbn2.xml (no surface term);
 G4  (optional, --compare CACHE.npy) my grid equals the cache written by the re-run of
     continuous_cells_real.py, entry by entry.
Usage: python3 -B ff_grid.py SEQ BB N OUT.npz [--window a1,b1,a2,b2,step] [--compare CACHE.npy]
"""
import r28_common as rc
rc.cap()
import argparse
import itertools
import os
import sys
import time
import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, "/home/user/MetricChain/experiments/science/ws_P2")
t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("seq")
ap.add_argument("bb")
ap.add_argument("N", type=int)
ap.add_argument("out")
ap.add_argument("--window", default=None, help="deg: lo1,hi1,lo2,hi2,step  (two torsions; a window instead of the full grid)")
ap.add_argument("--compare", default=None)
args = ap.parse_args()
print("R28 ff_grid.py  start", rc.utc(), vars(args))

import scbuild                                   # noqa: E402  (P2's builder, unmodified)
import openmm                                    # noqa: E402
import openmm.app as app                         # noqa: E402
import openmm.unit as unit                       # noqa: E402

BACKBONE = {"H": (-57.0, -47.0), "E": (-139.0, 135.0)}
seq, bb = args.seq, args.bb
pep = scbuild.SCPeptide(seq, solvent=True)
nres, n = pep.n, pep.nchi
phi0, psi0 = np.deg2rad(BACKBONE[bb])
print(f"Ace-{seq}-NMe: {pep.natoms} atoms, {nres} residues, {n} side-chain torsions; backbone {bb} {BACKBONE[bb]}")


def my_dihedral(p0, p1, p2, p3):
    """IUPAC dihedral of four points, radians, own implementation."""
    b1, b2, b3 = p1 - p0, p2 - p1, p3 - p2
    n1, n2 = np.cross(b1, b2), np.cross(b2, b3)
    # test case: p0=(1,0,0), p1=0, p2=(0,0,1), p3=(cos t, sin t, 1) must give +t  (checked by hand;
    # the first version of this function had the sign of the sine reversed — my error, log _01)
    return np.arctan2(np.dot(np.cross(n1, n2), b2 / np.linalg.norm(b2)), np.dot(n1, n2))


def my_angle(p0, p1, p2):
    u, v = p0 - p1, p2 - p1
    return np.degrees(np.arccos(np.dot(u, v) / np.linalg.norm(u) / np.linalg.norm(v)))


I = pep.idx
CHI_NAMES = {"VAL": [("N", "CA", "CB", "CG1")], "LEU": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "CD1")],
             "SER": [("N", "CA", "CB", "OG"), ("CA", "CB", "OG", "HG")], "ALA": []}
chi_quads = []
for k in range(1, nres + 1):
    for q in CHI_NAMES[pep.seq[k - 1]]:
        chi_quads.append(tuple(I[(k, nm)] for nm in q))
assert len(chi_quads) == n

# ------------------------------------------------------------------ G1 geometry
rng = np.random.default_rng(2803)
M = 40
chi_t = rng.uniform(0, 2 * np.pi, size=(M, n))
X = pep.coords(np.full((M, nres), phi0), np.full((M, nres), psi0), chi_t)
worst = 0.0
for m in range(M):
    for k in range(1, nres + 1):
        prevC = I[(k - 1, "C")]
        nxtN = I[(k + 1, "N")]
        ph = my_dihedral(X[m, prevC], X[m, I[(k, "N")]], X[m, I[(k, "CA")]], X[m, I[(k, "C")]])
        ps = my_dihedral(X[m, I[(k, "N")]], X[m, I[(k, "CA")]], X[m, I[(k, "C")]], X[m, nxtN])
        worst = max(worst, abs(np.angle(np.exp(1j * (ph - phi0)))), abs(np.angle(np.exp(1j * (ps - psi0)))))
    for c, q in enumerate(chi_quads):
        d = my_dihedral(*[X[m, a] for a in q])
        worst = max(worst, abs(np.angle(np.exp(1j * (d - chi_t[m, c])))))
print(f"G1 dihedrals of the built coordinates (phi, psi of every residue; every chi; {M} random conformations):"
      f" largest deviation from the requested value {np.degrees(worst):.2e} deg  ->  {'ok' if worst < 1e-8 else 'FAILED'}")
# control for G1: the wrong fourth atom (CD2 for chi_2 of Leu / CG2 for Val) must NOT reproduce the requested angle
for k in range(1, nres + 1):
    r = pep.seq[k - 1]
    alt = {"LEU": ("CA", "CB", "CG", "CD2"), "VAL": ("N", "CA", "CB", "CG2")}.get(r)
    if alt:
        col = pep.chi_col[(k, 1 if r == "LEU" else 0)]
        d = [np.degrees(np.angle(np.exp(1j * (my_dihedral(*[X[m, I[(k, nm)]] for nm in alt]) - chi_t[m, col])))) for m in range(M)]
        print(f"   control: residue {k} {r}: dihedral to the sibling atom {alt[-1]} minus chi = {np.mean(d):+.2f} deg (spread {np.ptp(d):.1e}) — not zero, as it must be")
    if r == "LEU":
        print(f"   LEU bond angles of the rigid geometry [deg]: N-CA-CB {my_angle(X[0, I[(k,'N')]], X[0, I[(k,'CA')]], X[0, I[(k,'CB')]]):.2f}, "
              f"CA-CB-CG {my_angle(X[0, I[(k,'CA')]], X[0, I[(k,'CB')]], X[0, I[(k,'CG')]]):.2f}, "
              f"CB-CG-CD1 {my_angle(X[0, I[(k,'CB')]], X[0, I[(k,'CG')]], X[0, I[(k,'CD1')]]):.2f}, "
              f"CB-CG-CD2 {my_angle(X[0, I[(k,'CB')]], X[0, I[(k,'CG')]], X[0, I[(k,'CD2')]]):.2f}, "
              f"CD1-CG-CD2 {my_angle(X[0, I[(k,'CD1')]], X[0, I[(k,'CG')]], X[0, I[(k,'CD2')]]):.2f}")

# ------------------------------------------------------------------ G3 fresh OpenMM system
ff = app.ForceField("amber14/protein.ff14SB.xml", "implicit/gbn2.xml")
fresh = ff.createSystem(pep.top, nonbondedMethod=app.NoCutoff, constraints=None, rigidWater=False,
                        removeCMMotion=False, sasaMethod=None)
integ = openmm.VerletIntegrator(0.001)
ctx = openmm.Context(fresh, integ, openmm.Platform.getPlatformByName("CPU"), {"Threads": "1"})
en = pep.energies(X[:8])
worst3 = 0.0
for m in range(8):
    ctx.setPositions(X[m] * 0.1)
    tot = ctx.getState(getEnergy=True).getPotentialEnergy().value_in_unit(unit.kilocalorie_per_mole)
    mine = en["bond"][m] + en["angle"][m] + en["tors"][m] + en["nb"][m] + en["gbn2"][m]
    worst3 = max(worst3, abs(tot - mine) / max(1.0, abs(tot)))
print(f"G3 builder (bond+angle+tors+nb+gbn2) against a fresh ff14SB + GBn2 system, 8 conformations:"
      f" largest relative difference {worst3:.1e}  ->  {'ok' if worst3 < 1e-6 else 'FAILED'}")
wrong = max(abs(en["bond"][m] + en["angle"][m] + en["tors"][m] + en["nb"][m] + en["obc2"][m]
                - (en["bond"][m] + en["angle"][m] + en["tors"][m] + en["nb"][m] + en["gbn2"][m])) for m in range(8))
print(f"   control: with the OBC2 solvent term in place of GBn2 the totals differ by up to {wrong:.3f} kcal/mol (so G3 can fail)")
del ctx, integ

# ------------------------------------------------------------------ the grid
if args.window:
    lo1, hi1, lo2, hi2, step = [float(a) for a in args.window.split(",")]
    assert n == 2
    ax = [np.arange(lo1, hi1 + 1e-9, step), np.arange(lo2, hi2 + 1e-9, step)]
else:
    ax = [np.arange(args.N) * 360.0 / args.N for _ in range(n)]
shape = tuple(len(a) for a in ax)
pts = np.array(list(itertools.product(*[range(s) for s in shape])))
chi = np.stack([np.deg2rad(ax[d][pts[:, d]]) for d in range(n)], axis=1)
names = ["bond", "angle", "tors", "nb", "lj", "gbn2"]
out = {nm: np.empty(len(pts)) for nm in names}
CH = 4000
for a in range(0, len(pts), CH):
    Xc = pep.coords(np.full((len(chi[a:a + CH]), nres), phi0), np.full((len(chi[a:a + CH]), nres), psi0), chi[a:a + CH])
    e = pep.energies(Xc)
    for nm in names:
        out[nm][a:a + CH] = e[nm]
for nm in names:
    out[nm] = out[nm].reshape(shape)
vac = out["bond"] + out["angle"] + out["tors"] + out["nb"]
print(f"grid {shape}: vacuum {vac.min():.2f} .. {vac.max():.4g} kcal/mol; GBn2 {out['gbn2'].min():.2f} .. {out['gbn2'].max():.2f}")
print(f"G2 rigid geometry: bond energy range over the grid {np.ptp(out['bond']):.2e}, angle energy range {np.ptp(out['angle']):.2e} kcal/mol"
      f"  ->  {'ok' if max(np.ptp(out['bond']), np.ptp(out['angle'])) < 1e-6 else 'FAILED'}")
np.savez(args.out, axes=np.array(ax, dtype=object), vac=vac, **out)

if args.compare:
    EE = np.load(args.compare)
    d0 = np.abs(EE[..., 0] - vac)
    d1 = np.abs(EE[..., 1] - out["gbn2"])
    rel0 = (d0 / np.maximum(1.0, np.abs(vac))).max()
    print(f"G4 my grid against the cache of the re-run ({os.path.basename(args.compare)}): vacuum largest relative difference {rel0:.1e},"
          f" GBn2 largest absolute difference {d1.max():.1e} kcal/mol  ->  {'ok' if rel0 < 1e-9 and d1.max() < 1e-9 else 'DIFFERENT'}")
    # control: transposed axes must not agree (unless the block is symmetric)
    if n == 2:
        dT = (np.abs(EE[..., 0].T - vac) / np.maximum(1.0, np.abs(vac))).max()
        print(f"   control: with the two torsion axes exchanged the largest relative difference is {dT:.2e} (must be large)")
rc.finish(t0)
