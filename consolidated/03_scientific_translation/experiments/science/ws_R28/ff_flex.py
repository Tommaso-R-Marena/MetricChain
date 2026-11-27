"""R28 — is "rigid bond geometry exaggerates the strain of ideal rotamers" (item 101 (c)) justified by a
measurement?  Nothing in the logs under review measures it.  This script does: the SAME energy
function (ff14SB + GBn2 polar term, OpenMM), capped leucine on the helix or strand backbone, but with
bond lengths and bond angles allowed to relax (energy minimisation) at prescribed side-chain torsions.

Variant A ("side chain flexible"): every atom of ACE, NME and N, H, CA, C, O of the residue frozen at
  the rigid ideal positions (mass 0); HA, CB and the side chain free.
Variant B ("all flexible"): no atom frozen; phi, psi and both omega held by torsion restraints.
In both: chi_1, chi_2 held by stiff restraints  k (1 - cos(theta - theta0)),  k = 20000 kJ/mol
(not counted in the reported energy), or released for the minima of the wells.

Outputs: relaxed energies at the ideal rotamers (300,180), (180,60); relaxed minima of the two wells;
strains; the relaxed CA-CB-CG angle.  Adiabatic: the vibrational free energy of the relaxed
coordinates is NOT included.
Controls (can fail): R1 the restrained torsions end within 0.5 deg of their targets (also checks the
sign convention); R2 relaxation never raises the energy above the rigid one at the same torsions;
R3 with ALL atoms frozen the energy equals the rigid builder's energy; R4 a second minimisation from
a perturbed start reaches the same energy within 0.01 kT.
Usage: python3 -B ff_flex.py H|E [--map STEP_DEG --emax KT]
"""
import r28_common as rc
rc.cap()
import argparse
import sys
import time
import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, "/home/user/MetricChain/experiments/science/ws_P2")
t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("bb")
ap.add_argument("--map", type=float, default=0.0)
ap.add_argument("--emax", type=float, default=25.0)
ap.add_argument("--out", default="")
args = ap.parse_args()
print("R28 ff_flex.py  start", rc.utc(), vars(args))
import scbuild                                   # noqa: E402
import openmm                                    # noqa: E402
import openmm.app as app                         # noqa: E402
import openmm.unit as unit                       # noqa: E402

KT = 0.596
BACKBONE = {"H": (-57.0, -47.0), "E": (-139.0, 135.0)}
phi0, psi0 = np.deg2rad(BACKBONE[args.bb])
pep = scbuild.SCPeptide("L", solvent=True)
I = pep.idx
nat = pep.natoms


def my_dihedral(X, q):
    p0, p1, p2, p3 = [X[a] for a in q]
    b1, b2, b3 = p1 - p0, p2 - p1, p3 - p2
    n1, n2 = np.cross(b1, b2), np.cross(b2, b3)
    return np.degrees(np.arctan2(np.dot(np.cross(n1, n2), b2 / np.linalg.norm(b2)), np.dot(n1, n2)))


def my_angle(X, a, b, c):
    u, v = X[a] - X[b], X[c] - X[b]
    return np.degrees(np.arccos(np.dot(u, v) / np.linalg.norm(u) / np.linalg.norm(v)))


Q = {"chi1": (I[(1, "N")], I[(1, "CA")], I[(1, "CB")], I[(1, "CG")]),
     "chi2": (I[(1, "CA")], I[(1, "CB")], I[(1, "CG")], I[(1, "CD1")]),
     "phi": (I[(0, "C")], I[(1, "N")], I[(1, "CA")], I[(1, "C")]),
     "psi": (I[(1, "N")], I[(1, "CA")], I[(1, "C")], I[(2, "N")]),
     "om1": (I[(0, "CH3")], I[(0, "C")], I[(1, "N")], I[(1, "CA")]),
     "om2": (I[(1, "CA")], I[(1, "C")], I[(2, "N")], I[(2, "CH3")])}
KR = 20000.0


def make(variant):
    ff = app.ForceField("amber14/protein.ff14SB.xml", "implicit/gbn2.xml")
    sysm = ff.createSystem(pep.top, nonbondedMethod=app.NoCutoff, constraints=None, rigidWater=False,
                           removeCMMotion=False, sasaMethod=None)
    for f in sysm.getForces():
        f.setForceGroup(0)
    rest = openmm.CustomTorsionForce("k*(1-cos(theta-theta0))")
    rest.addPerTorsionParameter("k")
    rest.addPerTorsionParameter("theta0")
    names = ["chi1", "chi2"] + (["phi", "psi", "om1", "om2"] if variant == "B" else [])
    for nm in names:
        rest.addTorsion(*Q[nm], [KR, 0.0])
    rest.setForceGroup(1)
    sysm.addForce(rest)
    frozen = []
    if variant in ("A", "frozen_all"):
        for (r, nm), a in I.items():
            if variant == "frozen_all" or r in (0, 2) or nm in ("N", "H", "CA", "C", "O"):
                sysm.setParticleMass(a, 0.0)
                frozen.append(a)
    integ = openmm.VerletIntegrator(0.001)
    ctx = openmm.Context(sysm, integ, openmm.Platform.getPlatformByName("CPU"), {"Threads": "1"})
    return dict(ctx=ctx, rest=rest, names=names, integ=integ, frozen=frozen, variant=variant)


def set_targets(S, chi1, chi2, hold=True):
    tg = {"chi1": chi1, "chi2": chi2, "phi": np.degrees(phi0), "psi": np.degrees(psi0), "om1": 180.0, "om2": 180.0}
    for t, nm in enumerate(S["names"]):
        k = KR if (hold or nm not in ("chi1", "chi2")) else 0.0
        S["rest"].setTorsionParameters(t, *Q[nm], [k, np.radians(tg[nm])])
    S["rest"].updateParametersInContext(S["ctx"])


def energy(S):
    st = S["ctx"].getState(getEnergy=True, getPositions=True, groups=1)
    e = st.getPotentialEnergy().value_in_unit(unit.kilocalorie_per_mole) / KT
    X = st.getPositions(asNumpy=True).value_in_unit(unit.angstrom)
    er = S["ctx"].getState(getEnergy=True, groups=2).getPotentialEnergy().value_in_unit(unit.kilocalorie_per_mole) / KT
    return e, np.array(X), er


def relax(S, chi1, chi2, hold=True, start=None, jitter=0.0, seed=0):
    """minimise from the rigid geometry at (chi1, chi2) (or from `start`); returns (E kT, X, restraint energy kT)"""
    set_targets(S, chi1, chi2, hold)
    if start is None:
        X0 = pep.coords(np.array([[phi0]]), np.array([[psi0]]), np.radians([[chi1, chi2]]))[0]
    else:
        X0 = start.copy()
    if jitter:
        rng = np.random.default_rng(seed)
        mv = np.array([a not in S["frozen"] for a in range(nat)])
        X0 = X0 + jitter * rng.normal(size=X0.shape) * mv[:, None]
    S["ctx"].setPositions(X0 * 0.1)
    openmm.LocalEnergyMinimizer.minimize(S["ctx"], 1e-4, 0)
    return energy(S)


def rigid_energy(S, chi1, chi2):
    set_targets(S, chi1, chi2, True)
    X0 = pep.coords(np.array([[phi0]]), np.array([[psi0]]), np.radians([[chi1, chi2]]))[0]
    S["ctx"].setPositions(X0 * 0.1)
    return energy(S)[0]


def wrap(d):
    return (d + 180.0) % 360.0 - 180.0


CA, CB, CG = I[(1, "CA")], I[(1, "CB")], I[(1, "CG")]
# ------------------------------------------------------------------ R3: all atoms frozen == rigid builder energy
S0 = make("frozen_all")
e_b = pep.energies(pep.coords(np.array([[phi0]]), np.array([[psi0]]), np.radians([[300.0, 180.0]])))
e_builder = (e_b["bond"][0] + e_b["angle"][0] + e_b["tors"][0] + e_b["nb"][0] + e_b["gbn2"][0]) / KT
e_frozen = relax(S0, 300.0, 180.0)[0]
print(f"R3 all atoms frozen: energy after 'minimisation' {e_frozen:.6f} kT; rigid builder {e_builder:.6f} kT; difference {e_frozen - e_builder:+.1e}"
      f"  -> {'ok' if abs(e_frozen - e_builder) < 1e-6 else 'FAILED'}")
del S0

# the rigid reference numbers at this backbone, from the 2.5-degree grid of ff_grid.py
G = np.load(f"/home/user/MetricChain/experiments/science/ws_R28/grid_L_{args.bb}_144.npz", allow_pickle=True)
Eg = (G["vac"] + G["gbn2"]) / KT
gi = np.unravel_index(Eg.argmin(), Eg.shape)
cellmin = {"mt": (Eg[96:144, 48:97].min(), np.unravel_index(Eg[96:144, 48:97].argmin(), (48, 49))),
           "tp": (Eg[48:97, 0:49].min(), np.unravel_index(Eg[48:97, 0:49].argmin(), (49, 49)))}
mt_rig = ((96 + cellmin["mt"][1][0]) * 2.5, (48 + cellmin["mt"][1][1]) * 2.5)
tp_rig = ((48 + cellmin["tp"][1][0]) * 2.5, cellmin["tp"][1][1] * 2.5)
print(f"rigid model ({args.bb}): cell minima mt {mt_rig} at {cellmin['mt'][0] - Eg.min():.3f} kT, tp {tp_rig} at {cellmin['tp'][0] - Eg.min():.3f} kT above the grid minimum;"
      f" ideal rotamers: (300,180) {Eg[120, 72] - Eg.min():.3f}, (180,60) {Eg[72, 24] - Eg.min():.3f}")

results = {}
for variant in ("A", "B"):
    S = make(variant)
    print(f"\n=== variant {variant}: " + ("backbone, ACE, NME frozen; HA, CB and the side chain relax" if variant == "A"
                                         else "all atoms relax; phi, psi, omega restrained"))
    worst_fid = 0.0
    viol_R2 = 0
    out = {}
    pts = {"ideal mt (300,180)": (300.0, 180.0), "ideal tp (180,60)": (180.0, 60.0),
           "rigid mt minimum": mt_rig, "rigid tp minimum": tp_rig}
    for nm, (c1, c2) in pts.items():
        e, X, er = relax(S, c1, c2, hold=True)
        d1, d2 = my_dihedral(X, Q["chi1"]), my_dihedral(X, Q["chi2"])
        fid = max(abs(wrap(d1 - c1)), abs(wrap(d2 - c2)))
        worst_fid = max(worst_fid, fid)
        er_rigid = rigid_energy(S, c1, c2)
        if e > er_rigid + 1e-6:
            viol_R2 += 1
        out[nm] = (e, X)
        print(f"   {nm:22s}: relaxed E = {e:10.4f} kT (rigid at the same torsions {er_rigid:10.4f}; relaxation {er_rigid - e:7.3f} kT);"
              f" chi = ({d1 % 360:.2f}, {d2 % 360:.2f}); CA-CB-CG = {my_angle(X, CA, CB, CG):.2f} deg; restraint energy {er:.4f} kT")
    # R4: perturbed start
    e2 = relax(S, 300.0, 180.0, hold=True, start=out["ideal mt (300,180)"][1], jitter=0.02, seed=1)[0]
    print(f"   R4 second minimisation of (300,180) from a perturbed start: {e2:.4f} kT (difference {e2 - out['ideal mt (300,180)'][0]:+.1e})"
          f" -> {'ok' if abs(e2 - out['ideal mt (300,180)'][0]) < 1e-2 else 'DIFFERENT'}")
    # minima of the two wells with chi released (start: relaxed geometry at the rigid minima)
    mins = {}
    for nm, key in (("mt", "rigid mt minimum"), ("tp", "rigid tp minimum")):
        e, X, er = relax(S, 0.0, 0.0, hold=False, start=out[key][1])
        d1, d2 = my_dihedral(X, Q["chi1"]) % 360, my_dihedral(X, Q["chi2"]) % 360
        mins[nm] = (e, d1, d2, my_angle(X, CA, CB, CG))
        fb = [wrap(my_dihedral(X, Q[q]) - t) for q, t in (("phi", np.degrees(phi0)), ("psi", np.degrees(psi0)), ("om1", 180.0), ("om2", 180.0))]
        print(f"   relaxed minimum of the {nm} well (chi free): E = {e:10.4f} kT at chi = ({d1:.2f}, {d2:.2f}); CA-CB-CG = {mins[nm][3]:.2f} deg;"
              f" backbone torsions off target by {max(abs(v) for v in fb):.2e} deg")
    e_mt, e_tp = out["ideal mt (300,180)"][0], out["ideal tp (180,60)"][0]
    print(f"   SUMMARY variant {variant}: strain of the ideal rotamers above the relaxed well minima: (300,180): {e_mt - mins['mt'][0]:.3f} kT, (180,60): {e_tp - mins['tp'][0]:.3f} kT")
    print(f"      relaxed two-state table: E(300,180) - E(180,60) = {e_mt - e_tp:+.3f} kT   (rigid: {Eg[120, 72] - Eg[72, 24]:+.3f});"
          f"  well bottoms: E(tp) - E(mt) = {mins['tp'][0] - mins['mt'][0]:+.3f} kT   (rigid: {cellmin['tp'][0] - cellmin['mt'][0]:+.3f})")
    wrong = (e_tp < e_mt) != (mins["tp"][0] < mins["mt"][0])
    print(f"      the two-state table with relaxed geometry names the well of the relaxed minimum: {not wrong}")
    print(f"   R1 restraint fidelity: largest |chi - target| = {worst_fid:.3f} deg -> {'ok' if worst_fid < 0.5 else 'FAILED'};"
          f"  R2 relaxed energy above the rigid one at the same torsions: {viol_R2} of {len(pts)} (must be 0)")
    results[variant] = (S, mins, out)

    # ------------------------------------------------------------------ optional adiabatic map
    if args.map:
        stp = args.map
        ax = np.arange(0.0, 360.0, stp)
        Em = np.full((len(ax), len(ax)), np.inf)
        ndone = 0
        for x, c1 in enumerate(ax):
            for y, c2 in enumerate(ax):
                er_ = Eg[int(round(c1 / 2.5)) % 144, int(round(c2 / 2.5)) % 144] - Eg.min()
                if er_ > args.emax:
                    continue
                Em[x, y] = relax(S, c1, c2, hold=True)[0]
                ndone += 1
        Em0 = Em - Em[np.isfinite(Em)].min()
        w = np.exp(-Em0)
        w[~np.isfinite(Em0)] = 0.0
        # the same mask applied to the rigid energies on the same coarse grid, for a like-for-like comparison
        Er = np.array([[Eg[int(round(c1 / 2.5)) % 144, int(round(c2 / 2.5)) % 144] for c2 in ax] for c1 in ax]) - Eg.min()
        wr = np.where(np.isfinite(Em0), np.exp(-Er), 0.0)
        def cellpop(wt):
            c = lambda a: int(a // 120)
            P = np.zeros((3, 3))
            for x, c1 in enumerate(ax):
                for y, c2 in enumerate(ax):
                    P[c(c1), c(c2)] += wt[x, y]
            return P / P.sum()
        Pf, Prg = cellpop(w), cellpop(wr)
        am = np.unravel_index(np.where(np.isfinite(Em0), Em0, np.inf).argmin(), Em0.shape)
        print(f"   adiabatic map, step {stp:g} deg, {ndone} points with rigid energy below {args.emax:g} kT: minimum at ({ax[am[0]]:g}, {ax[am[1]]:g});"
              f" half-open 120-deg cell populations (map points only): relaxed mt-cell {Pf[2, 1]:.3f}, tp-cell {Pf[1, 0]:.3f} | rigid energies on the same points: {Prg[2, 1]:.3f}, {Prg[1, 0]:.3f}")
        i300, i180, i60 = int(round(300 / stp)), int(round(180 / stp)), int(round(60 / stp))
        pt2 = np.exp(-np.array([Em0[i300, i180], Em0[i180, i60]]))
        pt2 /= pt2.sum()
        pc = np.array([Pf[2, 1], Pf[1, 0]]) / (Pf[2, 1] + Pf[1, 0])
        print(f"      two-state comparison (mt : tp): relaxed continuous cells {pc[0]:.3f} : {pc[1]:.3f}; relaxed ideal-rotamer table {pt2[0]:.3f} : {pt2[1]:.3f}")
        if args.out:
            np.savez(args.out + f"_{variant}.npz", ax=ax, Em=Em)
rc.finish(t0)
