"""Ideal hydrogen placement (rule 1 of model v2): a deterministic function of the heavy atoms.

WHY.  Model v1 took hydrogen positions from `openmm.app.Modeller.addHydrogens`, which starts
every new hydrogen at a random position and runs at most 50 minimiser iterations.  A seed made
that reproducible, not meaningful: between seeds 0..9 the certified minimum of the crambin table
moved by 15.7 kcal/mol and up to 4 of 26 sites changed state (experiment SB-X-005, asked for by
the science division, SCI-REV-0026 F1).  Here nothing is random and nothing is minimised.

THE RULE.  Every hydrogen H is placed from its parent heavy atom P, the heavy atoms bonded to P
and, for a group that can turn about a bond, one reference atom.  The bond length is the force
field's equilibrium length r0(P, H); angles named theta0 are the force field's equilibrium
angles (HarmonicBondForce / HarmonicAngleForce of the OpenMM system — for Amber ff14SB).  The
class of P is decided by (element of P, number of heavy atoms bonded to P, number of H on P):

  methine    (C,3,1)            H opposite to the sum of the unit vectors P->A1, P->A2, P->A3
  methylene  (C,2,2), (N,2,2)   b = -(u1+u2)/|u1+u2|, n = (u1 x u2)/|u1 x u2|, a = theta0(H,P,H)/2:
                                H = P + r0 (cos a * b +- sin a * n)
  planar     (C,2,1), (N,2,1)   H = P + r0 b   (aromatic C-H, amide and ring N-H)
  methyl     (C,1,3)            angle A-P-H = theta0(A,P,H); torsions B-A-P-H = 60, 180, -60
  ammonium   (N,1,3)            as methyl
  amide      (N,1,2)            A must have three bonded atoms (sp2); angle theta0(A,P,H);
                                torsions B-A-P-H = 0, 180
  hydroxyl   (O,1,1), (S,1,1)   angle theta0(A,P,H); torsion B-A-P-H = 180 (anti)

where, for the last four, A is the one heavy atom bonded to P and the reference B is the heavy
atom bonded to A, other than P, that is nearest to CA in the bond graph of A's residue (ties:
smallest atom name).  Hydrogens of one parent are assigned to the positions in the order of
their names; this choice has no effect on any energy because it is checked that hydrogens on
one parent carry identical nonbonded parameters (else `UnsupportedHydrogenEnvironment`).  Any
other environment is rejected, never guessed.

CONSEQUENCES, stated so that nobody has to discover them.  (1) Polar hydrogens do not look for
partners: a hydroxyl hydrogen is anti to the atom towards the backbone whatever its
surroundings (the science division's finding F3 stands; it is a property of the model).
(2) The placement commutes with the rigid chi rotations that generate the states: every atom
a rule uses lies on the rotation axis or turns with the hydrogen (a side chain is a tree, apart
from rings that turn as one body), so every state of a table has ideal hydrogens — tested.
(3) Histidine tautomers and termini are those chosen by `addHydrogens` from heavy atoms alone
(pH 7: HID unless only NE2 would donate a hydrogen bond; NH3+ / COO-); that choice does not
depend on the seed.
"""
from __future__ import annotations

import numpy as np
import openmm

_CLASSES = {
    ("C", 3, 1): "methine",
    ("C", 2, 2): "methylene", ("N", 2, 2): "methylene",
    ("C", 2, 1): "planar", ("N", 2, 1): "planar",
    ("C", 1, 3): "methyl",
    ("N", 1, 3): "ammonium",
    ("N", 1, 2): "amide",
    ("O", 1, 1): "hydroxyl", ("S", 1, 1): "hydroxyl",
}
_TORSIONS = {"methyl": (60.0, 180.0, -60.0), "ammonium": (60.0, 180.0, -60.0), "amide": (0.0, 180.0),
             "hydroxyl": (180.0,)}


class UnsupportedHydrogenEnvironment(ValueError):
    """A hydrogen whose parent is in none of the classes of the rule (fail closed)."""


def classify_parent(element: str, n_heavy: int, n_hydrogen: int) -> str:
    try:
        return _CLASSES[(element, n_heavy, n_hydrogen)]
    except KeyError:
        raise UnsupportedHydrogenEnvironment(
            f"no rule for {n_hydrogen} hydrogen(s) on {element} with {n_heavy} heavy neighbour(s)") from None


def _unit(v: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(v))
    if not norm > 1e-9:
        raise UnsupportedHydrogenEnvironment("degenerate geometry: a direction of the rule has zero length")
    return v / norm


def place_from_internal(a, b, c, r: float, theta_deg: float, phi_deg: float) -> np.ndarray:
    """The point d with |d - c| = r, angle b-c-d = theta and dihedral a-b-c-d = phi (IUPAC sign)."""
    a, b, c = (np.asarray(v, dtype=float) for v in (a, b, c))
    bc = _unit(c - b)
    n = _unit(np.cross(b - a, bc))
    m = np.cross(n, bc)
    theta, phi = np.radians(theta_deg), np.radians(phi_deg)
    return c + r * (-np.cos(theta) * bc + np.sin(theta) * np.cos(phi) * m + np.sin(theta) * np.sin(phi) * n)


def _force_field_geometry(system: openmm.System):
    nm, rad = openmm.unit.nanometer, openmm.unit.radian
    bonds, angles, nonbonded = {}, {}, None
    for force in system.getForces():
        if isinstance(force, openmm.HarmonicBondForce):
            for k in range(force.getNumBonds()):
                i, j, r0, _ = force.getBondParameters(k)
                bonds[(min(i, j), max(i, j))] = 10.0 * r0.value_in_unit(nm)
        elif isinstance(force, openmm.HarmonicAngleForce):
            for k in range(force.getNumAngles()):
                i, j, l, t0, _ = force.getAngleParameters(k)
                angles[(min(i, l), j, max(i, l))] = float(np.degrees(t0.value_in_unit(rad)))
        elif isinstance(force, openmm.NonbondedForce):
            nonbonded = force
    if nonbonded is None:
        raise UnsupportedHydrogenEnvironment("the system has no NonbondedForce")
    return bonds, angles, nonbonded


def _reference_atom(a, p, bonded, heavy):
    """The heavy neighbour of `a`, other than `p`, nearest to CA in the bond graph of a's residue."""
    residue = a.residue
    ca = [x for x in residue.atoms() if x.name == "CA"]
    if len(ca) != 1:
        raise UnsupportedHydrogenEnvironment(f"residue {residue.name}{residue.id} has no unique CA")
    dist, frontier = {ca[0].index: 0}, [ca[0]]
    while frontier:
        nxt = []
        for x in frontier:
            for y in bonded[x.index]:
                if y.residue is residue and y.index not in dist:
                    dist[y.index] = dist[x.index] + 1
                    nxt.append(y)
        frontier = nxt
    candidates = [y for y in bonded[a.index] if y.index in heavy and y.index != p.index and y.index in dist]
    if not candidates:
        raise UnsupportedHydrogenEnvironment(f"no reference atom for the hydrogens of {p.name} in "
                                             f"{residue.name}{residue.id}")
    return min(candidates, key=lambda y: (dist[y.index], y.name))


def ideal_hydrogen_positions(topology, positions: np.ndarray, system: openmm.System, return_rules: bool = False):
    """Positions (Angstrom) with every hydrogen replaced by its ideal position; heavy atoms untouched."""
    atoms = list(topology.atoms())
    bonded = {a.index: [] for a in atoms}
    for b0, b1 in topology.bonds():
        bonded[b0.index].append(b1)
        bonded[b1.index].append(b0)
    heavy = {a.index for a in atoms if a.element is not None and a.element.symbol != "H"}
    r0, theta0, nonbonded = _force_field_geometry(system)
    out = np.array(positions, dtype=np.float64, copy=True)
    rules: dict[str, str] = {}

    def bond_length(p, h):
        try:
            return r0[(min(p.index, h.index), max(p.index, h.index))]
        except KeyError:
            raise UnsupportedHydrogenEnvironment(f"no equilibrium bond length for {p.name}-{h.name}") from None

    def angle(i, j, l):
        try:
            return theta0[(min(i.index, l.index), j.index, max(i.index, l.index))]
        except KeyError:
            raise UnsupportedHydrogenEnvironment(f"no equilibrium angle for {i.name}-{j.name}-{l.name}") from None

    for h in atoms:
        if h.index in heavy:
            continue
        if len(bonded[h.index]) != 1 or bonded[h.index][0].index not in heavy:
            raise UnsupportedHydrogenEnvironment(f"hydrogen {h.name} of {h.residue.name}{h.residue.id} "
                                                 "is not bonded to exactly one heavy atom")
    for p in atoms:
        if p.index not in heavy:
            continue
        hydrogens = sorted((x for x in bonded[p.index] if x.index not in heavy), key=lambda x: x.name)
        if not hydrogens:
            continue
        neighbours = sorted((x for x in bonded[p.index] if x.index in heavy), key=lambda x: x.index)
        try:
            rule = classify_parent(p.element.symbol, len(neighbours), len(hydrogens))
        except UnsupportedHydrogenEnvironment as exc:
            raise UnsupportedHydrogenEnvironment(f"{p.name} of {p.residue.name}{p.residue.id}: {exc}") from None
        if len({tuple(q.value_in_unit(q.unit) for q in nonbonded.getParticleParameters(x.index)) for x in hydrogens}) != 1:
            raise UnsupportedHydrogenEnvironment(
                f"hydrogens on {p.name} of {p.residue.name}{p.residue.id} carry different nonbonded parameters; "
                "their assignment to positions would matter")
        pp = out[p.index]
        units = [_unit(out[x.index] - pp) for x in neighbours]
        if rule == "methine":
            out[hydrogens[0].index] = pp - bond_length(p, hydrogens[0]) * _unit(units[0] + units[1] + units[2])
        elif rule == "planar":
            out[hydrogens[0].index] = pp - bond_length(p, hydrogens[0]) * _unit(units[0] + units[1])
        elif rule == "methylene":
            bis, normal = -_unit(units[0] + units[1]), _unit(np.cross(units[0], units[1]))
            half = np.radians(angle(hydrogens[0], p, hydrogens[1]) / 2.0)
            for sign, h in zip((1.0, -1.0), hydrogens):
                out[h.index] = pp + bond_length(p, h) * (np.cos(half) * bis + sign * np.sin(half) * normal)
        else:                                               # methyl, ammonium, amide, hydroxyl: a torsion about A-P
            a = neighbours[0]
            if rule == "amide" and len(bonded[a.index]) != 3:
                raise UnsupportedHydrogenEnvironment(
                    f"NH2 on {a.name} of {p.residue.name}{p.residue.id}, which is not planar (a neutral amine?)")
            b = _reference_atom(a, p, bonded, heavy)
            for phi, h in zip(_TORSIONS[rule], hydrogens):
                out[h.index] = place_from_internal(out[b.index], out[a.index], pp, bond_length(p, h),
                                                   angle(a, p, h), phi)
        for h in hydrogens:
            rules[str(h.index)] = rule
    return (out, rules) if return_rules else out
