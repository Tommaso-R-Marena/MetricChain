#!/usr/bin/env python3
"""Coordinator's own check of the deciding points of referee R28's finding F1 (the leucine example of addendum
A17 (26), item 100 (ii), is a knife-edge instance whose strain numbers belong to the builder's bond angles).

Independent of the referee's code and data: only workstream P2's builder (imported, not modified) and OpenMM.
The referee relaxed the geometry by Cartesian minimisation with torsion restraints; here ONE internal
coordinate is relaxed, the bond angle CA-CB-CG of the leucine (the builder sets it to the force field's
equilibrium value), by a scan in the builder's own Z-matrix -- a different method, and a weaker relaxation.

Model: Ace-Leu-NMe, ideal helix backbone (-57, -47), ff14SB vacuum terms + GBn2 polarisation energy, 300 K
(kT = 0.596 kcal/mol), all other bond lengths and angles as built.  Angles in degrees; chi in [0, 360).

PREDICTIONS (written before the first run):
  (A) knife edge: E(180, 60 + d) - E(300, 180 + d) = -1.56, -0.61, +0.35 kT at d = 0, -1, -2 (the referee's
      numbers); I expect to reproduce them to 0.01 kT, the builder and the energy being the same.
  (B) vacuum part alone, on a 2.5 degree grid computed here: the grid minimum lies in the cell of the table's
      minimum (chi_1 near 180, chi_2 near 60), i.e. the "wrong well" disappears without the solvent term; the
      bottoms of the two wells differ by about -0.06 kT (vacuum) against +0.55 kT (total).  Reproduction to 0.01.
  (C) one bond angle relaxed (CA-CB-CG scanned over 105..121 degrees, 5 degree torsion grid): the strain of the
      two ideal rotamers -- 5.9 and 3.8 kT with the angle at its built value -- falls below 1.5 kT each, with the
      best angle between 112 and 117 degrees.  Less sure (I put it at two in three): with the angle relaxed the
      table (energies at the ideal torsions) and the relaxed map put their minimum in the same well.
FIRST RUN (kept as r28_leucine_check_01_cellbug.log): my function `cell_of` shifted the cells by one (it sent
the rotamer 60 to cell 1), so every quantity "of its own well" and the flag "same well" of that log are wrong;
the quantities that do not use cells (part (A); the grid minima; strains above the map minimum) are unaffected
and are the same in the second run.  Found from a control: a strain "above the bottom of its own well" came out
negative.  Corrected, with an assertion.

Controls that can fail: with the scan restricted to the built angle, (C) must return the unrelaxed numbers
(strains 5.9 / 3.8 kT, the table's minimum at (180, 60), the map's minimum near (287.5, 157.5)); the built
angle must be 109.5 degrees; exchanging the two torsion axes must change the answer of (A).
"""
import os
import resource
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(HERE, "..", "ws_P2"))
KT = 0.596
PHI, PSI = np.deg2rad(-57.0), np.deg2rad(-47.0)


def main():
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))
    t0 = time.time()
    print("r28_leucine_check.py   started", time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))
    import scbuild
    import openmm.unit as unit
    pep = scbuild.SCPeptide("L", solvent=True)
    kj = unit.kilojoule_per_mole
    I = pep.idx
    cg, cb, ca = I[(1, "CG")], I[(1, "CB")], I[(1, "CA")]
    zpos = [q for q, z in enumerate(pep.Z) if z[0] == cg]
    assert len(zpos) == 1
    zpos = zpos[0]
    z_built = pep.Z[zpos]
    built = float(np.degrees(z_built[5]))
    assert z_built[3] == cb and z_built[2] == ca, "the frame of CG is not (.., CA, CB)"
    print(f"builder: CA-CB-CG = {built:.2f} degrees (control: must be 109.50); {pep.natoms} atoms; chi columns {pep.nchi}")
    assert abs(built - 109.5) < 0.01

    def energies(chi_deg, theta_deg=None):
        """(vacuum, GBn2) in kT at the torsions chi_deg (M, 2), with CA-CB-CG set to theta_deg (None: as built)."""
        pep.Z[zpos] = z_built if theta_deg is None else z_built[:5] + (np.radians(theta_deg),) + z_built[6:]
        chi = np.radians(np.atleast_2d(np.asarray(chi_deg, dtype=float)))
        X = pep.coords(np.full((len(chi), 1), PHI), np.full((len(chi), 1), PSI), chi)
        out = np.empty((len(chi), 2))
        for m in range(len(chi)):
            pep.ctx.setPositions(X[m] * 0.1)
            out[m, 0] = pep.ctx.getState(getEnergy=True, groups=0b1111).getPotentialEnergy().value_in_unit(kj)
            out[m, 1] = pep.ctx.getState(getEnergy=True, groups=1 << 5).getPotentialEnergy().value_in_unit(kj)
        pep.Z[zpos] = z_built
        return out / scbuild.KCAL / KT

    def grid(step, theta_deg=None):
        a = np.arange(0.0, 360.0, step)
        chi = np.array([(x, y) for x in a for y in a])
        e = energies(chi, theta_deg).reshape(len(a), len(a), 2)
        return a, e

    # ------------------------------------------------------------------ (A) knife edge
    print("(A) the table's order under a uniform shift d of the chi_2 positions: E(180, 60+d) - E(300, 180+d), total energy, kT")
    row = []
    for d in (0.0, -1.0, -1.6, -2.0, 1.0, 2.0):
        e = energies([(180.0, 60.0 + d), (300.0, 180.0 + d)]).sum(axis=1)
        row.append((d, e[0] - e[1]))
    print("    " + ";  ".join(f"d = {d:+.1f}: {v:+.4f}" for d, v in row))
    sign_change = [d for d, v in row if v > 0]
    print(f"    the order is reversed (difference > 0) at d in {sign_change}")
    e = energies([(60.0, 180.0), (180.0, 300.0)]).sum(axis=1)
    print(f"    control (axes exchanged, d = 0): {e[0] - e[1]:+.4f} (must differ from {row[0][1]:+.4f})")

    # ------------------------------------------------------------------ (B) vacuum alone
    a, e = grid(2.5)
    tot = e.sum(axis=2)
    vac = e[..., 0]

    def cell_of(x):               # thirds of the circle centred on the rotamers 60, 180, 300
        return int((x % 360.0) // 120.0)                 # 0: [0,120) -> rotamer 60; 1: [120,240) -> 180; 2: [240,360) -> 300
    assert (cell_of(60.0), cell_of(180.0), cell_of(300.0)) == (0, 1, 2)

    def bottoms(E):
        """location of the grid minimum; bottom of the well of (180, 60) minus bottom of the well of (300, 180)"""
        i, j = np.unravel_index(np.argmin(E), E.shape)
        c1 = np.array([cell_of(x) for x in a])
        b_tab = E[np.ix_(c1 == 1, c1 == 0)].min()          # chi_1 in the cell of 180, chi_2 in the cell of 60
        b_oth = E[np.ix_(c1 == 2, c1 == 1)].min()          # chi_1 in the cell of 300, chi_2 in the cell of 180
        return (a[i], a[j]), b_tab - b_oth

    (m1, m2), dtot = bottoms(tot)
    (v1, v2), dvac = bottoms(vac)
    print(f"(B) 2.5 degree grid ({len(a)}^2 points).  Total energy: grid minimum at ({m1:g}, {m2:g}); bottom of the well of (180, 60) "
          f"minus bottom of the well of (300, 180): {dtot:+.4f} kT")
    print(f"    vacuum part alone: grid minimum at ({v1:g}, {v2:g}); the same difference: {dvac:+.4f} kT")
    i180, i60, i300 = int(round(180 / 2.5)), int(round(60 / 2.5)), int(round(300 / 2.5))
    s_tab = tot[i180, i60] - tot.min()
    s_oth = tot[i300, i180] - tot.min()
    print(f"    strain of the ideal rotamers above the grid minimum (total energy): (180, 60): {s_tab:.3f} kT; (300, 180): {s_oth:.3f} kT; "
          f"table's order E(180,60) - E(300,180) = {tot[i180, i60] - tot[i300, i180]:+.4f} kT")

    # ------------------------------------------------------------------ (C) one bond angle relaxed
    step = 5.0
    thetas = np.arange(105.0, 121.01, 1.0)

    def relaxed(theta_list):
        best = None
        arg = None
        for th in theta_list:
            a5, e5 = grid(step, th)
            E = e5.sum(axis=2)
            if best is None:
                best, arg = E.copy(), np.full(E.shape, th)
            else:
                upd = E < best
                best[upd] = E[upd]
                arg[upd] = th
        return a5, best, arg

    def report(tag, a5, E, arg):
        j180, j60, j300 = int(round(180 / step)), int(round(60 / step)), int(round(300 / step))
        i, j = np.unravel_index(np.argmin(E), E.shape)
        c1 = np.array([cell_of(x) for x in a5])
        b_tab = E[np.ix_(c1 == 1, c1 == 0)].min()
        b_oth = E[np.ix_(c1 == 2, c1 == 1)].min()
        tab = E[np.ix_([j60, j180, j300], [j60, j180, j300])]
        ti, tj = np.unravel_index(np.argmin(tab), tab.shape)
        rot = (60, 180, 300)
        same = (cell_of(a5[i]) == cell_of(rot[ti])) and (cell_of(a5[j]) == cell_of(rot[tj]))
        print(f"    {tag}: map minimum at ({a5[i]:g}, {a5[j]:g}) with angle {arg[i, j]:g}; "
              f"strain of (180, 60) above the bottom of its own well: {E[j180, j60] - b_tab:.3f} kT (angle {arg[j180, j60]:g}); "
              f"of (300, 180): {E[j300, j180] - b_oth:.3f} kT (angle {arg[j300, j180]:g})")
        print(f"       above the map minimum: {E[j180, j60] - E.min():.3f} and {E[j300, j180] - E.min():.3f} kT; table's minimum at "
              f"({rot[ti]}, {rot[tj]}); table and map in the same well: {same}; bottoms (180,60)-well minus (300,180)-well: {b_tab - b_oth:+.3f} kT")
        return same

    print(f"(C) CA-CB-CG relaxed by a scan ({thetas[0]:g} .. {thetas[-1]:g} degrees in steps of 1), {step:g} degree torsion grid, total energy")
    a5, E0, arg0 = relaxed([built])
    report("control, angle as built (109.5)", a5, E0, arg0)
    a5, E1, arg1 = relaxed(list(thetas))
    same = report("angle relaxed", a5, E1, arg1)
    hist = np.bincount(np.round(arg1[E1 < E1.min() + 5.0]).astype(int))
    best_angles = [(th, int(c)) for th, c in enumerate(hist) if c > 0]
    print(f"    best angle at the grid points within 5 kT of the relaxed minimum (angle, count): {best_angles}")
    print(f"    relaxation never raises the energy: max over the grid of (relaxed - built) = {float((E1 - E0).max()):+.3e} kT (must be <= 0)")
    assert float((E1 - E0).max()) <= 1e-9
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    print(f"ALL DONE   {time.time() - t0:.1f} s   peak memory {peak:.0f} MB")


if __name__ == "__main__":
    main()
