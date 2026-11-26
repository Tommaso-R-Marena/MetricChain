"""Structure preparation (rule 1 of the model): read, select one protein chain, validate, add H.

Fail-closed policy: the prepared structure must be exactly the deposited heavy atoms of one
chain (first model, first alternate location) plus hydrogens placed by OpenMM's
`Modeller.addHydrogens(forcefield, pH=7.0)` with Amber ff14SB.  The structure is rejected
(`StructureRejected`) on any of: a non-standard residue in the chain (an ATOM-record residue
that is not one of the 20 standard amino acids, or a SEQRES residue that is not standard),
missing residues (SEQRES length differs from the observed residue count, or a C(i)-N(i+1)
distance > 2.0 A), a missing or unexpected heavy atom (backbone N CA C O, the standard side
chain, and OXT on the C-terminal residue), a heavy-atom coordinate changed by preparation.
Hydrogens (and deuteriums) present in the input are deleted before `addHydrogens` so that all
structures, X-ray, neutron and NMR, receive the same hydrogen placement protocol.  Note that
addHydrogens itself starts the new H from random positions and minimises them (heavy atoms
immobile); we seed Python's `random` with `seed` and use the Reference platform so that the
prepared structure is reproducible.
`repair_with_pdbfixer=True` (off by default) lets PDBFixer add missing heavy atoms (never
residues, never replacements); the added atoms are listed in the metadata.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import pathlib
import random

import numpy as np
import openmm
from openmm import app

FORCEFIELD_FILES = ("amber14-all.xml",)

SIDE_CHAIN_HEAVY = {
    "ALA": "CB", "ARG": "CB CG CD NE CZ NH1 NH2", "ASN": "CB CG OD1 ND2", "ASP": "CB CG OD1 OD2",
    "CYS": "CB SG", "GLN": "CB CG CD OE1 NE2", "GLU": "CB CG CD OE1 OE2", "GLY": "",
    "HIS": "CB CG ND1 CD2 CE1 NE2", "ILE": "CB CG1 CG2 CD1", "LEU": "CB CG CD1 CD2",
    "LYS": "CB CG CD CE NZ", "MET": "CB CG SD CE", "PHE": "CB CG CD1 CD2 CE1 CE2 CZ",
    "PRO": "CB CG CD", "SER": "CB OG", "THR": "CB OG1 CG2",
    "TRP": "CB CG CD1 CD2 NE1 CE2 CE3 CZ2 CZ3 CH2", "TYR": "CB CG CD1 CD2 CE1 CE2 CZ OH",
    "VAL": "CB CG1 CG2",
}
STANDARD = frozenset(SIDE_CHAIN_HEAVY)
WATER = frozenset({"HOH", "WAT", "DOD", "H2O", "TIP3"})


class StructureRejected(ValueError):
    """The input structure cannot be prepared under rule 1 without repair."""


@dataclasses.dataclass
class PreparedStructure:
    topology: app.Topology
    positions: np.ndarray          # (n_atoms, 3) float64, Angstrom
    system: openmm.System          # ff14SB, NoCutoff, no constraints
    forcefield: app.ForceField
    meta: dict


def _sha256(path) -> str:
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def _record_lines(path, chain_id):
    """Residue names of ATOM records and SEQRES of `chain_id` (light parse, first model only)."""
    atom_res, seqres = {}, []
    for line in pathlib.Path(path).read_text().splitlines():
        rec = line[:6]
        if rec == "ENDMDL":
            break
        if rec == "SEQRES" and line[11] == chain_id:
            seqres += line[19:].split()
        if rec == "ATOM  " and line[21] == chain_id:
            atom_res[line[22:27]] = line[17:20].strip()
    return atom_res, seqres


def _source_meta(path) -> dict:
    path = pathlib.Path(path)
    meta = {"file": path.name, "pdb_id": path.stem.upper(), "sha256": _sha256(path), "url": None}
    manifest = path.parent / "MANIFEST.json"
    if manifest.exists():
        for entry in json.loads(manifest.read_text()).get("entries", []):
            if entry.get("file") == path.name:
                meta.update(pdb_id=entry["pdb_id"], url=entry["url"], manifest_sha256=entry["sha256"])
                if entry["sha256"] != meta["sha256"]:
                    raise StructureRejected(f"{path}: sha256 differs from MANIFEST.json")
    return meta


def prepare_structure(pdb_path: str, chain_id: str | None = None, ph: float = 7.0,
                      repair_with_pdbfixer: bool = False, seed: int = 0) -> PreparedStructure:
    pdb = app.PDBFile(str(pdb_path))          # first model, first alternate location
    topology, positions = pdb.topology, pdb.getPositions(asNumpy=True, frame=0)
    chains = [c for c in topology.chains() if any(r.name in STANDARD for r in c.residues())]
    if chain_id is None:
        chain_id = chains[0].id
    chains = [c for c in chains if c.id == chain_id]
    if len(chains) != 1:
        raise StructureRejected(f"{pdb_path}: expected one protein chain '{chain_id}', found {len(chains)}")
    chain = chains[0]

    atom_res, seqres = _record_lines(pdb_path, chain_id)
    bad = sorted({n for n in atom_res.values() if n not in STANDARD} | {n for n in seqres if n not in STANDARD})
    if bad:
        raise StructureRejected(f"{pdb_path}: non-standard residue(s) in chain {chain_id}: {bad}")
    protein = [r for r in chain.residues() if r.name in STANDARD]
    if seqres and len(seqres) != len(protein):
        raise StructureRejected(f"{pdb_path}: missing residues: SEQRES has {len(seqres)}, "
                                f"{len(protein)} observed in chain {chain_id}")

    modeller = app.Modeller(topology, positions)
    keep = {r.index for r in protein}
    modeller.delete([r for r in modeller.topology.residues() if r.index not in keep])
    modeller.delete([a for a in modeller.topology.atoms() if a.element.symbol in ("H", "D")])
    added = []
    if repair_with_pdbfixer:
        modeller, added = _repair(modeller)
    _check_heavy_atoms(modeller.topology, pdb_path)
    residues = list(modeller.topology.residues())
    pos_a = np.array(modeller.getPositions().value_in_unit(openmm.unit.angstrom))
    for r0, r1 in zip(residues, residues[1:]):
        c = next(a.index for a in r0.atoms() if a.name == "C")
        n = next(a.index for a in r1.atoms() if a.name == "N")
        if np.linalg.norm(pos_a[c] - pos_a[n]) > 2.0:
            raise StructureRejected(f"{pdb_path}: chain break between residues {r0.id} and {r1.id}")
    heavy_before = {(a.residue.index, a.name): pos_a[a.index] for a in modeller.topology.atoms()}

    forcefield = app.ForceField(*FORCEFIELD_FILES)
    state = random.getstate()      # addHydrogens draws initial H positions from Python's `random`
    try:
        random.seed(seed)
        modeller.addHydrogens(forcefield, pH=ph, platform=openmm.Platform.getPlatformByName("Reference"))
    finally:
        random.setstate(state)
    pos = np.array(modeller.getPositions().value_in_unit(openmm.unit.angstrom), dtype=np.float64)
    for a in modeller.topology.atoms():
        if a.element.symbol != "H" and np.any(pos[a.index] != heavy_before[(a.residue.index, a.name)]):
            raise StructureRejected(f"{pdb_path}: heavy atom {a} moved during preparation")
    system = forcefield.createSystem(modeller.topology, nonbondedMethod=app.NoCutoff,
                                     constraints=None, rigidWater=False, removeCMMotion=False)
    meta = {
        "source": dict(_source_meta(pdb_path), chain=chain_id),
        "preparation": {
            "reader": "openmm.app.PDBFile (first model, first alternate location)",
            "dropped": "all residues outside the chain or not standard amino acids (waters, ligands, ions)",
            "input_hydrogens": "deleted, then re-added by openmm.app.Modeller.addHydrogens",
            "hydrogen_placement": ("openmm Modeller.addHydrogens: random initial H positions (Python random "
                                   "seeded with `seed`), then LocalEnergyMinimizer(tol 1.0 kJ/mol/nm, 50 iter) of "
                                   "the added H only (heavy atoms immobile; ff14SB, CutoffNonPeriodic), Reference platform"),
            "seed": seed,
            "ph": ph, "forcefield": list(FORCEFIELD_FILES), "minimisation": "none",
            "repaired_with_pdbfixer": bool(repair_with_pdbfixer), "pdbfixer_added_atoms": added,
            "n_residues": len(residues), "n_atoms": modeller.topology.getNumAtoms(),
            "histidine_protonation": {r.id: _his_variant(r) for r in modeller.topology.residues() if r.name == "HIS"},
        },
    }
    return PreparedStructure(modeller.topology, pos, system, forcefield, meta)


def _his_variant(res) -> str:
    names = {a.name for a in res.atoms()}
    return {(True, False): "HID", (False, True): "HIE", (True, True): "HIP"}[("HD1" in names, "HE2" in names)]


def _check_heavy_atoms(topology, pdb_path):
    residues = list(topology.residues())
    for k, res in enumerate(residues):
        want = {"N", "CA", "C", "O"} | set(SIDE_CHAIN_HEAVY[res.name].split())
        if k == len(residues) - 1:
            want.add("OXT")
        have = {a.name for a in res.atoms()}
        if want - have:
            raise StructureRejected(f"{pdb_path}: missing heavy atom(s) {sorted(want - have)} in {res.name}{res.id}")
        if have - want:
            raise StructureRejected(f"{pdb_path}: unexpected heavy atom(s) {sorted(have - want)} in {res.name}{res.id}")


def _repair(modeller):
    try:
        from pdbfixer import PDBFixer
    except ImportError as exc:  # pragma: no cover
        raise StructureRejected("repair_with_pdbfixer=True but pdbfixer is not installed") from exc
    import io
    buf = io.StringIO()
    app.PDBFile.writeFile(modeller.topology, modeller.positions, buf, keepIds=True)
    fixer = PDBFixer(pdbfile=io.StringIO(buf.getvalue()))
    fixer.missingResidues = {}
    fixer.findMissingAtoms()
    added = [f"{r.name}{r.id}:{a.name}" for r, atoms in fixer.missingAtoms.items() for a in atoms]
    added += [f"{r.name}{r.id}:{name}" for r, names in fixer.missingTerminals.items() for name in names]
    fixer.addMissingAtoms()
    return app.Modeller(fixer.topology, fixer.positions), added
