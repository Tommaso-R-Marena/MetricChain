"""Deterministic hydrogen placement (model v2), written after the seed measurement SB-X-005.

Model v1 let `openmm.app.Modeller.addHydrogens` place hydrogens from random starts with at most 50
minimiser iterations; the certified minimum of crambin then moved by 15.7 kcal/mol between seeds
(SCI-REV-0026 F1, measured in SB-X-005).  Model v2 places every hydrogen by a geometric rule: a
function of the deposited heavy atoms, the bond graph and the force field's equilibrium bond
lengths and angles — nothing random, no minimiser.
"""
from __future__ import annotations

import pathlib

import numpy as np
import pytest

openmm = pytest.importorskip("openmm")

from metricchain_sb.molecular import build_energy_tables  # noqa: E402
from metricchain_sb.molecular.chi import dihedral_deg  # noqa: E402
from metricchain_sb.molecular.hydrogens import (  # noqa: E402
    UnsupportedHydrogenEnvironment, classify_parent, ideal_hydrogen_positions, place_from_internal)
from metricchain_sb.molecular.prepare import prepare_structure  # noqa: E402
from metricchain_sb.molecular.tables import build_model  # noqa: E402

PDB = pathlib.Path(__file__).resolve().parents[2] / "benchmarks" / "structbio" / "pdb"


def _angle_deg(a, b, c):
    u, v = a - b, c - b
    return float(np.degrees(np.arccos(np.clip(u @ v / np.linalg.norm(u) / np.linalg.norm(v), -1.0, 1.0))))


def test_internal_coordinate_placement_gives_the_requested_bond_angle_and_torsion():
    rng = np.random.default_rng(7)
    for _ in range(50):
        a, b, c = rng.normal(size=(3, 3)) * 2.0
        r, theta, phi = rng.uniform(0.9, 1.5), rng.uniform(95.0, 125.0), rng.uniform(-180.0, 180.0)
        d = place_from_internal(a, b, c, r, theta, phi)
        assert abs(np.linalg.norm(d - c) - r) < 1e-12
        assert abs(_angle_deg(b, c, d) - theta) < 1e-9
        delta = (float(dihedral_deg(a, b, c, d)) - phi + 180.0) % 360.0 - 180.0
        assert abs(delta) < 1e-9


def test_unknown_hydrogen_environment_is_rejected_not_guessed():
    assert classify_parent("C", 3, 1) == "methine"
    assert classify_parent("C", 2, 2) == "methylene"
    assert classify_parent("O", 1, 1) == "hydroxyl"
    with pytest.raises(UnsupportedHydrogenEnvironment):
        classify_parent("C", 4, 1)
    with pytest.raises(UnsupportedHydrogenEnvironment):
        classify_parent("P", 1, 1)


def test_ideal_hydrogens_do_not_depend_on_the_seed():
    a = prepare_structure(str(PDB / "1CRN.pdb"), hydrogens="ideal", seed=0)
    b = prepare_structure(str(PDB / "1CRN.pdb"), hydrogens="ideal", seed=5)
    assert np.array_equal(a.positions, b.positions)
    old_a = prepare_structure(str(PDB / "1CRN.pdb"), hydrogens="openmm-seeded", seed=0)
    old_b = prepare_structure(str(PDB / "1CRN.pdb"), hydrogens="openmm-seeded", seed=5)
    assert not np.array_equal(old_a.positions, old_b.positions)        # the defect this replaces
    assert a.meta["preparation"]["hydrogens"] == "ideal"


def _bond_lengths_nm(system):
    out = {}
    for force in system.getForces():
        if isinstance(force, openmm.HarmonicBondForce):
            for k in range(force.getNumBonds()):
                i, j, r0, _ = force.getBondParameters(k)
                out[(min(i, j), max(i, j))] = r0.value_in_unit(openmm.unit.nanometer)
    return out


def test_ideal_hydrogens_sit_at_force_field_bond_lengths_and_heavy_atoms_do_not_move():
    for pdb_id in ("1L2Y", "1CRN"):
        seeded = prepare_structure(str(PDB / f"{pdb_id}.pdb"), hydrogens="openmm-seeded")
        ideal = prepare_structure(str(PDB / f"{pdb_id}.pdb"), hydrogens="ideal")
        r0 = _bond_lengths_nm(ideal.system)
        n_h = 0
        for bond in ideal.topology.bonds():
            i, j = bond[0].index, bond[1].index
            if "H" in (bond[0].element.symbol, bond[1].element.symbol):
                n_h += 1
                d = np.linalg.norm(ideal.positions[i] - ideal.positions[j])
                assert abs(d - 10.0 * r0[(min(i, j), max(i, j))]) < 1e-9
        assert n_h > 100
        heavy = [a.index for a in ideal.topology.atoms() if a.element.symbol != "H"]
        assert np.array_equal(ideal.positions[heavy], seeded.positions[heavy])


def _minimise_hydrogens(prepared):
    """Converged minimisation of the hydrogens alone (heavy atoms massless), full ff14SB, no cutoff."""
    system = openmm.XmlSerializer.deserialize(openmm.XmlSerializer.serialize(prepared.system))
    for atom in prepared.topology.atoms():
        if atom.element.symbol != "H":
            system.setParticleMass(atom.index, 0.0)
    context = openmm.Context(system, openmm.VerletIntegrator(0.001), openmm.Platform.getPlatformByName("Reference"))
    context.setPositions(prepared.positions * 0.1)
    openmm.LocalEnergyMinimizer.minimize(context, 0.5, 0)
    return np.array(context.getState(getPositions=True).getPositions().value_in_unit(openmm.unit.angstrom))


def test_ideal_hydrogens_are_near_a_minimum_of_the_force_field():
    """A wrong rule (wrong side of a plane, eclipsed methyl, bent bisector) puts a hydrogen far from
    every minimum.  Rotors (methyl, ammonium, hydroxyl) may turn towards partners in vacuo; the rest
    may not move appreciably."""
    prepared = prepare_structure(str(PDB / "1L2Y.pdb"), hydrogens="ideal")
    rules = prepared.meta["preparation"]["hydrogen_rules"]          # atom index (str) -> rule name
    relaxed = _minimise_hydrogens(prepared)
    moved = {int(i): float(np.linalg.norm(relaxed[int(i)] - prepared.positions[int(i)])) for i in rules}
    rigid = [d for i, d in moved.items() if rules[str(i)] not in ("methyl", "ammonium", "hydroxyl")]
    assert len(rigid) > 60
    assert max(rigid) < 0.35, sorted(rigid)[-5:]
    assert float(np.median(list(moved.values()))) < 0.10
    assert sum(1 for d in moved.values() if d > 0.5) < 0.10 * len(moved)


def test_ideal_hydrogens_follow_rigid_chi_rotations():
    """Placing hydrogens on a rotated side chain gives the rotated hydrogens: every state of the
    table has ideal hydrogens, not only the deposited one."""
    model, _ = build_model(str(PDB / "1L2Y.pdb"), hydrogens="ideal")
    prepared = model.prepared
    rng = np.random.default_rng(3)
    for _ in range(5):
        x = [int(rng.integers(site.n_states)) for site in model.sites]
        rotated = model.positions_for(x)
        placed = ideal_hydrogen_positions(prepared.topology, rotated, prepared.system)
        assert np.max(np.abs(placed - rotated)) < 1e-8


def test_tables_do_not_depend_on_the_seed_with_ideal_hydrogens():
    a = build_energy_tables(str(PDB / "1L2Y.pdb"), hydrogens="ideal", seed=0)
    b = build_energy_tables(str(PDB / "1L2Y.pdb"), hydrogens="ideal", seed=3)
    assert all(np.array_equal(u, v) for u, v in zip(a.unary, b.unary))
    assert all(np.array_equal(a.pair[k], b.pair[k]) for k in a.pair)
    assert a.meta["model"] != build_energy_tables(str(PDB / "1L2Y.pdb"), hydrogens="openmm-seeded").meta["model"]


def test_hydroxyl_hydrogens_are_anti_to_the_atom_towards_the_backbone():
    """The stated reference atom, not just any: Thr HG1 is anti to CA (not to CG2), Ser HG to CA,
    Tyr HH to CE1."""
    prepared = prepare_structure(str(PDB / "1CRN.pdb"), hydrogens="ideal")
    quads = {"THR": ("CA", "CB", "OG1", "HG1"), "SER": ("CA", "CB", "OG", "HG"), "TYR": ("CE1", "CZ", "OH", "HH")}
    seen = set()
    for res in prepared.topology.residues():
        if res.name in quads:
            idx = {a.name: a.index for a in res.atoms()}
            a, b, c, d = (prepared.positions[idx[name]] for name in quads[res.name])
            assert abs(abs(float(dihedral_deg(a, b, c, d))) - 180.0) < 1e-6, (res.name, res.id)
            seen.add(res.name)
    assert seen == {"THR", "SER", "TYR"}
