"""Scoring tools: planted answers first, then agreement with independent implementations.

Every test states the answer before computing it.  The cross-checks need biotite / tmtools
(listed in requirements-frontier.txt) and are skipped without them.
"""
import math
from pathlib import Path

import numpy as np
import pytest

from metricchain_fb import scores

DATA = Path(__file__).resolve().parent / "data"


def chain(n, seed, step=3.8):
    """A compact self-avoiding-ish random chain with fixed step length (a chiral object)."""
    rng = np.random.default_rng(seed)
    pts = [np.zeros(3)]
    direction = np.array([1.0, 0.0, 0.0])
    for _ in range(n - 1):
        direction = direction + 0.9 * rng.normal(size=3)
        direction /= np.linalg.norm(direction)
        pts.append(pts[-1] + step * direction)
    return np.array(pts)


def random_rotation(seed):
    q, _ = np.linalg.qr(np.random.default_rng(seed).normal(size=(3, 3)))
    return q * np.sign(np.linalg.det(q))


# ------------------------------------------------------------------ planted answers
@pytest.mark.parametrize("seed", [1, 2, 3])
def test_identity_and_rigid_motion_give_perfect_scores(seed):
    ref = chain(150, seed)
    moved = ref @ random_rotation(seed + 10).T + np.array([12.0, -7.0, 30.0])
    assert scores.rmsd(moved, ref) < 1e-9
    assert scores.lddt(moved, ref) == pytest.approx(1.0, abs=1e-12)
    assert scores.gdt_ts(moved, ref) == pytest.approx(100.0, abs=1e-9)
    assert scores.gdt_ha(moved, ref) == pytest.approx(100.0, abs=1e-9)
    assert scores.tm_score(moved, ref) == pytest.approx(1.0, abs=1e-9)


@pytest.mark.parametrize("seed", [4, 5])
def test_mirror_image_is_invisible_to_distance_scores_and_visible_to_superposition_scores(seed):
    """Planted: a reflection preserves every distance, so lDDT must be exactly 1; a proper
    superposition cannot undo it, so RMSD, GDT and TM-score must see it.  (The blind spot is a
    property of the score, recorded in NEGATIVE_RESULTS.md, not a defect of the code.)"""
    ref = chain(120, seed)
    mirror = ref * np.array([1.0, 1.0, -1.0])
    assert scores.lddt(mirror, ref) == pytest.approx(1.0, abs=1e-12)
    assert scores.rmsd(mirror, ref) > 2.0
    assert scores.gdt_ts(mirror, ref) < 90.0
    assert scores.tm_score(mirror, ref) < 0.9


def test_kabsch_never_returns_a_reflection():
    ref = chain(60, 7)
    R, _ = scores.kabsch(ref * np.array([1.0, 1.0, -1.0]), ref)
    assert np.linalg.det(R) == pytest.approx(1.0, abs=1e-9)


@pytest.mark.parametrize("n1,n2", [(60, 40), (75, 25), (50, 50)])
def test_two_rigid_domains_far_apart_give_exactly_the_larger_fraction(n1, n2):
    """Planted: model = reference with the second domain moved 200 A away as a rigid body.
    No single rigid superposition can bring atoms of both domains within 8 A, so at every
    cut-off the best fraction is max(n1, n2) / (n1 + n2)."""
    ref = chain(n1 + n2, 11)
    model = ref.copy()
    model[n1:] = model[n1:] @ random_rotation(3).T + np.array([200.0, 0.0, 0.0])
    expected = 100.0 * max(n1, n2) / (n1 + n2)
    assert scores.gdt_ts(model, ref) == pytest.approx(expected, abs=1e-9)
    assert scores.gdt_ha(model, ref) == pytest.approx(expected, abs=1e-9)
    # lDDT (cut-off 15 A): every intra-domain distance is preserved, every inter-domain one is lost
    d = np.linalg.norm(ref[:, None] - ref[None, :], axis=2)
    mask = (d < 15.0) & ~np.eye(len(ref), dtype=bool)
    same = np.zeros_like(mask)
    same[:n1, :n1] = True
    same[n1:, n1:] = True
    assert scores.lddt(model, ref) == pytest.approx((mask & same).sum() / mask.sum(), abs=1e-12)


def test_noise_of_known_size_gives_the_expected_rmsd_and_monotone_scores():
    ref = chain(600, 21)
    rng = np.random.default_rng(22)
    previous = (1.01, 100.1)
    for sigma in (0.2, 0.5, 1.0, 2.0):
        model = ref + rng.normal(scale=sigma, size=ref.shape)
        assert scores.rmsd(model, ref) == pytest.approx(sigma * math.sqrt(3.0), rel=0.08)
        current = (scores.lddt(model, ref), scores.gdt_ts(model, ref))
        assert current[0] < previous[0] and current[1] < previous[1]
        previous = current


def test_planted_dihedral_and_sign_convention():
    """Planted: looking from p1 to p2 (here along +z), the bond to p0 must be rotated clockwise by
    phi to eclipse the bond to p3 (IUPAC).  Seen along +z a rotation from +x towards +y is
    clockwise, so p3 at azimuth +phi is the planted positive torsion.  (The first version of this
    test planted the opposite sign; the implementation was right and the test wrong, as the
    agreement with an independent library on a crystal structure showed.)"""
    for phi in (-170.0, -60.0, 0.0, 35.0, 90.0, 179.0):
        a = math.radians(phi)
        p0, p1, p2 = np.array([1.0, 0.0, 0.0]), np.zeros(3), np.array([0.0, 0.0, 1.0])
        p3 = np.array([math.cos(a), math.sin(a), 1.0])
        assert scores.dihedral(p0, p1, p2, p3) == pytest.approx(phi, abs=1e-9)
    assert scores.angular_difference(179.0, -179.0) == pytest.approx(2.0)
    assert scores.angular_difference(170.0, -10.0, period=180.0) == pytest.approx(0.0)


def rotate_about_axis(points, origin, axis, degrees):
    axis = axis / np.linalg.norm(axis)
    a = math.radians(degrees)
    p = points - origin
    return origin + p * math.cos(a) + np.cross(axis, p) * math.sin(a) + np.outer(p @ axis, axis) * (1 - math.cos(a))


@pytest.mark.parametrize("delta", [10.0, 30.0, -75.0, 180.0])
def test_planted_side_chain_rotation_changes_chi1_by_exactly_delta(delta):
    atoms = {"N": np.array([1.46, 0.0, 0.0]), "CA": np.zeros(3), "CB": np.array([-0.53, 1.43, 0.0]),
             "CG": np.array([-2.05, 1.52, 0.31]), "CD1": np.array([-2.46, 2.98, 0.52]),
             "CD2": np.array([-2.83, 0.77, -0.78])}
    before = scores.chi_angles("LEU", atoms)
    moved = dict(atoms)
    names = ["CG", "CD1", "CD2"]
    rotated = rotate_about_axis(np.array([atoms[n] for n in names]), atoms["CA"], atoms["CB"] - atoms["CA"], delta)
    moved.update(dict(zip(names, rotated)))
    after = scores.chi_angles("LEU", moved)
    assert scores.angular_difference(after[0], before[0]) == pytest.approx(abs(delta) % 360 if abs(delta) <= 180 else 360 - abs(delta), abs=1e-9)
    assert scores.angular_difference(after[1], before[1]) == pytest.approx(0.0, abs=1e-9)   # chi2 untouched
    assert scores.chi_recovery("LEU", after, before, tolerance=20.0) is (abs(delta) <= 20.0)


def test_symmetric_terminal_groups_and_missing_atoms():
    assert scores.chi_recovery("PHE", [-60.0, 95.0], [-60.0, -85.0]) is True        # ring flip: same conformation
    assert scores.chi_recovery("LEU", [-60.0, 95.0], [-60.0, -85.0]) is False       # not symmetric for leucine
    assert scores.chi_recovery("ASP", [-60.0, 10.0], [-60.0, -170.0]) is True
    assert scores.chi_recovery("LYS", [-60.0, 180.0, None, None], [-60.0, 180.0, 175.0, 60.0]) is False   # missing in model
    assert scores.chi_recovery("LYS", [-60.0, 180.0, 60.0, 60.0], [-60.0, 180.0, 175.0, 60.0], upto=2) is True
    assert scores.chi_recovery("GLY", [], []) is None and scores.chi_angles("ALA", {}) == []


# ------------------------------------------------------------------ independent implementations
def test_lddt_agrees_with_biotite():
    struc = pytest.importorskip("biotite.structure")
    for seed, sigma in ((31, 0.3), (32, 1.0), (33, 3.0)):
        ref = chain(140, seed)
        model = ref + np.random.default_rng(seed).normal(scale=sigma, size=ref.shape)
        arr = struc.AtomArray(len(ref))
        arr.coord = ref.astype(np.float32)
        arr.res_id = np.arange(1, len(ref) + 1)
        arr.chain_id = np.array(["A"] * len(ref))
        arr.atom_name = np.array(["CA"] * len(ref))
        arr.res_name = np.array(["GLY"] * len(ref))
        arr.element = np.array(["C"] * len(ref))
        theirs = float(struc.lddt(arr, model.astype(np.float32)))
        assert scores.lddt(model, ref) == pytest.approx(theirs, abs=2e-3)


def test_tm_score_agrees_with_tm_align_on_a_fixed_correspondence():
    tmtools = pytest.importorskip("tmtools")
    for seed, sigma in ((41, 0.5), (42, 1.5)):
        ref = chain(160, seed)
        model = ref + np.random.default_rng(seed).normal(scale=sigma, size=ref.shape)
        seq = "A" * len(ref)
        res = tmtools.tm_align(model, ref, seq, seq)
        assert scores.tm_score(model, ref) == pytest.approx(res.tm_norm_chain2, abs=0.02)


def test_side_chain_torsions_of_a_public_crystal_structure_agree_with_biotite():
    """Public reference material: crambin, PDB 1CRN (0.945 A; PDB data are CC0)."""
    struc = pytest.importorskip("biotite.structure")
    pdbx = pytest.importorskip("biotite.structure.io.pdbx")
    arr = pdbx.get_structure(pdbx.CIFFile.read(str(DATA / "1crn.cif")), model=1)
    arr = arr[struc.filter_amino_acids(arr)]
    theirs = np.degrees(struc.dihedral_side_chain(arr))
    starts = struc.get_residue_starts(arr, add_exclusive_stop=True)
    compared = 0
    for k in range(len(starts) - 1):
        res = arr[starts[k]:starts[k + 1]]
        atoms = {name: coord for name, coord in zip(res.atom_name, res.coord)}
        ours = scores.chi_angles(res.res_name[0], atoms)
        for j, value in enumerate(ours[:4]):
            if value is None or np.isnan(theirs[k, j]):
                continue
            period = 180.0 if (res.res_name[0], j + 1) in scores.CHI_PERIOD_180 else 360.0
            assert scores.angular_difference(value, float(theirs[k, j]), period) < 0.01, (res.res_name[0], res.res_id[0], j + 1)
            compared += 1
    assert compared >= 60, compared
