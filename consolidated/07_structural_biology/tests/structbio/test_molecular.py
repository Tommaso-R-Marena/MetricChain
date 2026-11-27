"""Tests for the STRUCTBIO molecular model layer (src/metricchain_sb/molecular).

The PDB files are read from benchmarks/structbio/pdb/ (no network access); a test whose file
is absent is skipped with the reason.  The decomposition tests (§6 of the specification) are
the acceptance tests: the pairwise tables must reproduce an independently assembled OpenMM
System to |diff| <= 1e-9*|E| + 1e-6 kcal/mol on random configurations, and to an absolute
1e-6 kcal/mol on clash-free configurations.
"""
import json
import pathlib
import shutil

import numpy as np
import pytest

from metricchain_sb.molecular import (
    EnergyTables, build_energy_tables, load_energy_tables, openmm_reference_energy,
    save_energy_tables)
from metricchain_sb.molecular.chi import CHI_ATOMS, dihedral_deg
from metricchain_sb.molecular.prepare import StructureRejected, prepare_structure
from metricchain_sb.molecular.reference import validate_against_openmm
from metricchain_sb.molecular.rotamers import library_values

ROOT = pathlib.Path(__file__).resolve().parents[2]
PDB_DIR = ROOT / "benchmarks" / "structbio" / "pdb"

TWENTY = ["ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY", "HIS", "ILE",
          "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL"]
N_CHI = {"ALA": 0, "GLY": 0, "SER": 1, "CYS": 1, "THR": 1, "VAL": 1, "PRO": 2, "ILE": 2,
         "LEU": 2, "ASP": 2, "ASN": 2, "HIS": 2, "PHE": 2, "TYR": 2, "TRP": 2, "MET": 3,
         "GLU": 3, "GLN": 3, "LYS": 4, "ARG": 4}


def pdb(name):
    path = PDB_DIR / f"{name}.pdb"
    if not path.exists():
        pytest.skip(f"{path} is not cached (download it, see benchmarks/structbio/pdb/MANIFEST.json)")
    return str(path)


@pytest.fixture(scope="module")
def crn_tables():
    return build_energy_tables(pdb("1CRN"), chain_id="A")


@pytest.fixture(scope="module")
def trp_cage():
    return build_energy_tables(pdb("1L2Y"), chain_id="A")


# ----------------------------------------------------------------------------- chi table
def test_chi_table_covers_twenty_residue_types():
    assert sorted(CHI_ATOMS) == TWENTY
    for res, n in N_CHI.items():
        assert len(CHI_ATOMS[res]) == n, res
        for k, quad in enumerate(CHI_ATOMS[res]):
            assert len(quad) == 4
            if k == 0:
                assert quad[:3] == ("N", "CA", "CB")
            else:  # consecutive chis share three atoms
                assert quad[:3] == CHI_ATOMS[res][k - 1][1:]


def test_dihedral_known_values():
    a, b, c = np.array([1.0, 0, 0]), np.array([0.0, 0, 0]), np.array([0.0, 0, 1])
    for ang in (-170.0, -60.0, 0.0, 60.0, 90.0, 180.0):
        t = np.radians(ang)
        d = np.array([np.cos(t), np.sin(t), 1.0])
        got = dihedral_deg(a, b, c, d)
        assert abs((got - ang + 180) % 360 - 180) < 1e-12


def test_chi_atoms_are_bonded_chains_and_measure_like_independent_formula(trp_cage):
    model = trp_cage.model
    top_atoms = list(model.topology.atoms())
    bonds = {frozenset((a.index, b.index)) for a, b in model.topology.bonds()}
    pos = model.positions
    n_checked = 0
    for res in model.topology.residues():
        names = {a.name: a.index for a in res.atoms()}
        for quad in CHI_ATOMS[res.name]:
            idx = [names[n] for n in quad]
            for u, v in zip(idx, idx[1:]):
                assert frozenset((u, v)) in bonds, (res, quad)
            # independent dihedral: angle between normals, sign from the triple product
            p = pos[idx]
            b0, b1, b2 = p[1] - p[0], p[2] - p[1], p[3] - p[2]
            n1, n2 = np.cross(b0, b1), np.cross(b1, b2)
            ang = np.degrees(np.arccos(np.clip(n1 @ n2 / np.linalg.norm(n1) / np.linalg.norm(n2), -1, 1)))
            ang = ang if np.dot(np.cross(n1, n2), b1) > 0 else -ang
            got = dihedral_deg(*p)
            assert abs((got - ang + 180) % 360 - 180) < 1e-6
            n_checked += 1
    assert n_checked > 20
    assert len(top_atoms) == len(pos)


def test_library_is_symmetry_aware():
    assert library_values("ASP", 1) == library_values("GLU", 2) == (-60.0, 0.0, 60.0)
    assert library_values("PHE", 1) == library_values("TYR", 1) == (90.0, 0.0)
    for res, n in N_CHI.items():
        for k in range(n):
            vals = library_values(res, k)
            assert len(set(vals)) == len(vals)
    with pytest.raises(KeyError):
        library_values("ALA", 0)


# ------------------------------------------------------------------ preparation / sites
def test_native_state_reproduces_input_coordinates(trp_cage):
    model = trp_cage.model
    from openmm.app import PDBFile
    raw = PDBFile(pdb("1L2Y"))
    raw_pos = np.array(raw.getPositions(asNumpy=True, frame=0)._value) * 10.0
    raw_index = {(a.residue.id, a.name): a.index for a in raw.topology.atoms() if a.element.symbol != "H"}
    n = 0
    for a in model.topology.atoms():
        if a.element.symbol != "H":
            assert np.max(np.abs(model.positions[a.index] - raw_pos[raw_index[(a.residue.id, a.name)]])) < 1e-9
            n += 1
    assert n == len(raw_index)
    for site in model.sites:
        assert np.max(np.abs(site.state_coords[0] - model.positions[site.moving])) < 1e-9
        assert site.origins[0] == "native"


def test_rotation_preserves_bonds_angles_and_hits_targets(trp_cage):
    model = trp_cage.model
    bonds = [(a.index, b.index) for a, b in model.topology.bonds()]
    nbr = {}
    for u, v in bonds:
        nbr.setdefault(u, set()).add(v)
        nbr.setdefault(v, set()).add(u)
    angles = [(u, c, v) for c in nbr for u in nbr[c] for v in nbr[c] if u < v]

    def geometry(p):
        bl = np.array([np.linalg.norm(p[u] - p[v]) for u, v in bonds])
        an = []
        for u, c, v in angles:
            x, y = p[u] - p[c], p[v] - p[c]
            an.append(np.arctan2(np.linalg.norm(np.cross(x, y)), x @ y))
        return bl, np.degrees(an)

    bl0, an0 = geometry(model.positions)
    for site in model.sites:
        for a in range(1, site.n_states):
            p = model.positions_for({site.index: a})
            bl, an = geometry(p)
            assert np.max(np.abs(bl - bl0)) < 1e-9
            assert np.max(np.abs(an - an0)) < 1e-7
            names = {at.name: at.index for at in site.residue.atoms()}
            for k, quad in enumerate(CHI_ATOMS[site.resname]):
                got = dihedral_deg(*p[[names[q] for q in quad]])
                assert abs((got - site.chis[a][k] + 180) % 360 - 180) < 1e-9


def test_flexible_site_selection_crambin(crn_tables):
    meta = crn_tables.meta
    names = {s["resname"] for s in meta["sites"]}
    assert not names & {"GLY", "ALA", "PRO"}
    fixed = {(r["resnum"], r["reason"]) for r in meta["fixed_residues"]}
    # crambin: Cys3-Cys40, Cys4-Cys32, Cys16-Cys26 are disulfide bonded
    cyx = sorted(int(n) for n, why in fixed if why == "disulfide-bonded cysteine (CYX)")
    assert cyx == [3, 4, 16, 26, 32, 40]
    for s in meta["sites"]:
        assert s["n_states"] == len(s["chi_angles"]) == len(s["origin"])
        assert s["origin"][0] == "native"
        assert all(o == "library" for o in s["origin"][1:])
        lib = 1
        for k in range(len(s["chi_names"])):
            lib *= len(library_values(s["resname"], k))
        assert s["n_states"] == 1 + lib
    assert len(crn_tables.unary) == len(meta["sites"])
    k = len(meta["sites"])
    assert sorted(crn_tables.pair) == [(i, j) for i in range(k) for j in range(i + 1, k)]


def test_rejects_missing_heavy_atom_and_nonstandard_residue(tmp_path):
    src = pathlib.Path(pdb("1CRN")).read_text().splitlines()
    # 1) delete the side-chain atom CZ of Arg10
    broken = [l for l in src if not (l.startswith("ATOM") and l[17:20] == "ARG" and l[22:26].strip() == "10"
                                     and l[12:16].strip() == "CZ")]
    p1 = tmp_path / "missing.pdb"
    p1.write_text("\n".join(broken) + "\n")
    with pytest.raises(StructureRejected, match="missing heavy atom"):
        prepare_structure(str(p1), "A")
    # 2) rename Asn12 to a non-standard name
    renamed = [l[:17] + "XYZ" + l[20:] if l.startswith("ATOM") and l[22:26].strip() == "12" else l for l in src]
    p2 = tmp_path / "nonstd.pdb"
    p2.write_text("\n".join(renamed) + "\n")
    with pytest.raises(StructureRejected, match="non-standard"):
        prepare_structure(str(p2), "A")


def test_pdbfixer_repair_only_behind_flag_and_recorded(tmp_path):
    pytest.importorskip("pdbfixer")
    src = pathlib.Path(pdb("1CRN")).read_text().splitlines()
    broken = [l for l in src if not (l.startswith("ATOM") and l[22:26].strip() == "10" and l[12:16].strip() == "CZ")]
    path = tmp_path / "missing.pdb"
    path.write_text("\n".join(broken) + "\n")
    fixed = prepare_structure(str(path), "A", repair_with_pdbfixer=True)
    assert fixed.meta["preparation"]["repaired_with_pdbfixer"] is True
    assert fixed.meta["preparation"]["pdbfixer_added_atoms"] == ["ARG10:CZ"]
    ref = prepare_structure(pdb("1CRN"), "A")
    key = lambda s: {(a.residue.id, a.name): s.positions[a.index] for a in s.topology.atoms() if a.element.symbol != "H"}
    k_fixed, k_ref = key(fixed), key(ref)
    for name, xyz in k_fixed.items():
        if name != ("10", "CZ"):
            assert np.max(np.abs(xyz - k_ref[name])) < 1e-9, name


def test_preparation_is_reproducible_and_replaces_input_hydrogens():
    # 5PTI is a joint X-ray/neutron model with H and D atoms: all are deleted and re-added
    a = prepare_structure(pdb("5PTI"), "A", seed=0)
    b = prepare_structure(pdb("5PTI"), "A", seed=0)
    assert np.array_equal(a.positions, b.positions)
    assert {at.element.symbol for at in a.topology.atoms()} <= {"C", "N", "O", "S", "H"}
    assert a.topology.getNumResidues() == 58


# ----------------------------------------------------------------------- tables / io
def test_table_api_and_clipping(crn_tables):
    t = crn_tables
    n_clip = 0
    for u, uu in zip(t.unary, t.unary_unclipped):
        assert u.dtype == np.float64 and u.shape == uu.shape
        assert np.array_equal(u, np.minimum(uu, 1000.0))
        n_clip += int(np.sum(uu > 1000.0))
    for key, p in t.pair.items():
        assert p.shape == (len(t.unary[key[0]]), len(t.unary[key[1]]))
        assert np.array_equal(p, np.minimum(t.pair_unclipped[key], 1000.0))
        n_clip += int(np.sum(t.pair_unclipped[key] > 1000.0))
    assert t.meta["clipping"]["n_clipped_entries"] == n_clip
    assert t.meta["e_const"] == 0.0
    x = [0] * len(t.unary)
    manual = sum(u[0] for u in t.unary_unclipped) + sum(p[0, 0] for p in t.pair_unclipped.values())
    assert abs(t.table_energy(x, clipped=False) - manual) < 1e-9
    json.dumps(t.meta)


def test_save_load_roundtrip(crn_tables, tmp_path):
    prefix = str(tmp_path / "crn")
    save_energy_tables(crn_tables, prefix)
    meta = json.loads(pathlib.Path(prefix + ".json").read_text())
    assert meta["format"] == "structbio-energy-tables/1"
    t2 = load_energy_tables(prefix)
    assert isinstance(t2, EnergyTables)
    for a, b in zip(crn_tables.unary + crn_tables.unary_unclipped, t2.unary + t2.unary_unclipped):
        assert np.array_equal(a, b)
    for key in crn_tables.pair:
        assert np.array_equal(crn_tables.pair[key], t2.pair[key])
        assert np.array_equal(crn_tables.pair_unclipped[key], t2.pair_unclipped[key])
    rng = np.random.default_rng(1)
    x = [int(rng.integers(len(u))) for u in t2.unary]
    assert crn_tables.table_energy(x) == t2.table_energy(x)


def test_max_states_per_site_keeps_native_and_lowest_self_energy(crn_tables):
    t = build_energy_tables(pdb("1CRN"), chain_id="A", max_states_per_site=4)
    assert t.meta["max_states_per_site"] == 4
    for i, s in enumerate(t.meta["sites"]):
        full = crn_tables.meta["sites"][i]
        assert s["n_states"] == min(4, full["n_states"])
        assert s["origin"][0] == "native"
        if full["n_states"] > 4:
            u_full = crn_tables.unary_unclipped[i]
            kept = sorted(u_full[1:])[:3]
            assert np.allclose(sorted(t.unary_unclipped[i][1:]), kept, rtol=0, atol=1e-12)


# ------------------------------------------------------------- §6 acceptance validation
def _check_validation(t, n_random, seed):
    rep = validate_against_openmm(t, n_random=n_random, seed=seed)
    # random full configurations (clash-prone): relative + absolute tolerance
    for d, e in zip(rep["random"]["diff"], rep["random"]["e_openmm"]):
        assert abs(d) <= 1e-9 * abs(e) + 1e-6, (d, e)
    # clash-free configurations (ICM descents on the tables): absolute agreement
    assert rep["clash_free"]["n"] >= 2
    assert rep["clash_free"]["max_abs_diff"] < 1e-6
    # bonds and angles are invariant under chi rotation
    assert rep["bonded_constant_max_spread"] < 1e-6
    return rep


def test_decomposition_matches_openmm_crambin(crn_tables):
    rep = _check_validation(crn_tables, n_random=20, seed=0)
    assert rep["random"]["n"] == 21  # 20 random + all-native


def test_reference_energy_is_deterministic(crn_tables):
    x0 = [0] * len(crn_tables.unary)
    e = openmm_reference_energy(crn_tables.model, [x0, x0])
    assert e.shape == (2,) and e[0] == e[1]


@pytest.mark.slow
def test_decomposition_matches_openmm_ubiquitin():
    t = build_energy_tables(pdb("1UBQ"), chain_id="A")
    _check_validation(t, n_random=20, seed=0)
