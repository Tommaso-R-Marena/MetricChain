"""Tests of the lattice-chain enumerator and of the exact covering computations (THY-REQ-0002).

The C enumerator works with lattice direction indices.  The first test checks it against an
independent construction that never mentions the lattice: Cartesian coordinates built from
internal coordinates (bond length sqrt(3), tetrahedral bond angle, dihedral angles 180 / +60 /
-60 degrees), exactly as the chain is defined in docs/workstreams/P_REPORT.md section 0.
"""
from __future__ import annotations

import itertools
import math
import subprocess
import sys
from collections import defaultdict
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.chains.profile_cover import (  # noqa: E402
    certified_lower_bound, cover_matrix_P, covering_number_P, greedy_cover, min_cover_cpsat, min_cover_highs,
    parse_enum_output, reduce_cover)

C_SOURCE = ROOT / "src" / "metricchain_eng" / "chains" / "dia_enum.c"


@pytest.fixture(scope="session")
def dia_enum(tmp_path_factory) -> Path:
    exe = tmp_path_factory.mktemp("bin") / "dia_enum"
    subprocess.run(["cc", "-O2", "-Wall", "-Wextra", "-Werror", "-o", str(exe), str(C_SOURCE)], check=True)
    return exe


def run(exe: Path, n: int, *extra: str):
    out = subprocess.run([str(exe), "-n", str(n), *extra], check=True, capture_output=True, text=True).stdout
    return parse_enum_output(out)


# ----------------------------------------------------------------------------- independent geometry

def _place(a, b, c, bond, angle, dihedral):
    """Position of the next atom from the three previous ones and internal coordinates."""
    bc = c - b
    bc /= np.linalg.norm(bc)
    nrm = np.cross(b - a, bc)
    nrm /= np.linalg.norm(nrm)
    m = np.cross(nrm, bc)
    d2 = np.array([-bond * math.cos(angle), bond * math.sin(angle) * math.cos(dihedral),
                   bond * math.sin(angle) * math.sin(dihedral)])
    return c + d2[0] * bc + d2[1] * m + d2[2] * nrm


def geometric_class_table(n: int, s_cut: float = 12.0):
    """Class table of the self-avoiding tetrahedral chain from internal coordinates (pure Python)."""
    bond = math.sqrt(3.0)
    angle = math.acos(-1.0 / 3.0)                      # tetrahedral bond angle
    dihedrals = {"t": math.pi, "p": math.pi / 3.0, "m": -math.pi / 3.0}
    a0 = np.array([0.0, 0.0, 0.0])
    a1 = np.array([bond, 0.0, 0.0])
    a2 = a1 + bond * np.array([-math.cos(angle), math.sin(angle), 0.0])
    table: dict[tuple[int, int, int], list[int]] = defaultdict(lambda: [0, 10 ** 9])
    for word in itertools.product("tpm", repeat=n):
        pts = [a0, a1, a2]
        for w in word:
            pts.append(_place(pts[-3], pts[-2], pts[-1], bond, angle, dihedrals[w]))
        P = np.array(pts)
        d2 = ((P[:, None, :] - P[None, :, :]) ** 2).sum(axis=2)
        iu = np.triu_indices(len(pts), k=1)
        if (d2[iu] < 0.5).any():                       # two beads on one site
            continue
        r = np.rint(d2).astype(int)
        assert np.abs(d2 - r).max() < 1e-6, "squared distances of the tetrahedral chain are integers"
        counts = [0, 0, 0]
        for p in range(len(pts)):
            for q in range(p + 3, len(pts)):
                if r[p, q] < s_cut:
                    counts[{3: 0, 8: 1, 11: 2}[int(r[p, q])]] += 1
        g = sum(1 for w in word if w != "t")
        entry = table[tuple(counts)]
        entry[0] += 1
        entry[1] = min(entry[1], g)
    return dict(table)


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6, 7])
def test_enumerator_matches_internal_coordinate_geometry(dia_enum, n):
    tab = run(dia_enum, n)
    ref = geometric_class_table(n)
    got = {tuple(int(v) for v in tab.hist[i]): [int(tab.count[i]), int(tab.gmin[i])] for i in range(tab.n_classes)}
    assert got == ref
    assert tab.distances == (3, 8, 11)


# ----------------------------------------------------------------------------- published values

PUBLISHED = {  # P_REPORT sections 3.2 and 3.3: conformations, profile classes
    5: (233, 22), 6: (683, 37), 7: (2005, 57), 8: (5849, 90), 9: (17107, 129), 10: (49833, 190),
    11: (145379, 258), 12: (422825, 356)}
PUBLISHED_COVER = {5: (5, 3, 2), 6: (6, 5, 2), 7: (10, 5, 2), 8: (10, 5, 2), 9: (13, 5, 3),
                   10: (16, 7, 3), 11: (19, 7, 4)}


@pytest.mark.parametrize("n", sorted(PUBLISHED))
def test_published_counts(dia_enum, n):
    tab = run(dia_enum, n)
    assert (tab.n_conformations, tab.n_classes) == PUBLISHED[n]


@pytest.mark.parametrize("n", sorted(PUBLISHED_COVER))
def test_published_covering_numbers(dia_enum, n):
    tab = run(dia_enum, n)
    got = tuple(covering_number_P(tab, L, eps).size
                for L, eps in ((1, 0), (1, Fr(tab.n_beads, 2)), (Fr(1, 5), 0)))
    assert got == PUBLISHED_COVER[n]


def test_wider_cutoff_class_counts(dia_enum):
    assert run(dia_enum, 10, "-c", "28").n_classes == 4646        # P_REPORT section 3.2
    assert run(dia_enum, 10, "-c", "28").distances == (3, 8, 11, 16, 19, 24, 27)


def test_cutoff_below_every_distance_gives_one_class(dia_enum):
    """Negative control of THY-REQ-0002: with no pair inside the cutoff all profiles coincide."""
    tab = run(dia_enum, 9, "-c", "4")                             # only s = 3 is below the cutoff ...
    assert tab.distances == (3,)
    one = parse_enum_output("\n".join(                            # ... and with its column removed: one class
        ["# dia_enum n_torsions=9 n_beads=12 s_cut=4", "# distances 3"]
        + [f"0 {int(c)} {int(g)} {int(cg)} {int(gx)}" for c, g, cg, gx in zip(tab.count, tab.gmin, tab.count_gmin, tab.gmax)]))
    assert one.n_classes == 1 and one.n_conformations == 17107
    assert covering_number_P(one, 1, 0).size == 1


# ----------------------------------------------------------------------------- reductions of the enumeration

def test_mirror_reduction_is_exact(dia_enum):
    a, b = run(dia_enum, 10, "-m", "1"), run(dia_enum, 10, "-m", "0")
    assert (a.hist == b.hist).all() and (a.gmin == b.gmin).all() and (a.gmax == b.gmax).all()
    assert [int(x) for x in a.count] == [int(x) for x in b.count]
    assert [int(x) for x in a.count_gmin] == [int(x) for x in b.count_gmin]


def test_prefix_split_is_a_partition(dia_enum):
    whole = run(dia_enum, 11)
    texts = [subprocess.run([str(dia_enum), "-n", "11", "-k", "4", "-W", "7", "-w", str(w)], check=True,
                            capture_output=True, text=True).stdout for w in range(7)]
    merged = parse_enum_output("\n".join(texts))
    assert (merged.hist == whole.hist).all() and (merged.gmin == whole.gmin).all()
    assert [int(x) for x in merged.count] == [int(x) for x in whole.count]
    assert [int(x) for x in merged.count_gmin] == [int(x) for x in whole.count_gmin]


def test_every_gauche_pattern_is_realised_small(dia_enum, tmp_path):
    for n in (5, 9, 12):
        bm = tmp_path / f"p{n}.bin"
        subprocess.run([str(dia_enum), "-n", str(n), "-b", str(bm)], check=True, capture_output=True)
        bits = np.unpackbits(np.frombuffer(bm.read_bytes(), dtype=np.uint8), bitorder="little")[: 1 << n]
        assert int(bits.sum()) == 1 << n


# ----------------------------------------------------------------------------- exact covering

def _brute_force_cover(M: np.ndarray) -> int:
    nA, nC = M.shape
    for k in range(1, nA + 1):
        for comb in itertools.combinations(range(nA), k):
            if M[list(comb)].any(axis=0).all():
                return k
    raise AssertionError("no cover")


@pytest.mark.parametrize("seed", range(40))
def test_reductions_and_solvers_agree_with_brute_force(seed):
    rng = np.random.default_rng(seed)
    n = int(rng.integers(4, 11))
    M = rng.random((n, n)) < rng.uniform(0.15, 0.5)
    np.fill_diagonal(M, True)                                     # coverable, like "a class covers itself"
    opt = _brute_force_cover(M)
    R, rows, cols = reduce_cover(M)
    assert _brute_force_cover(R) == opt
    assert min_cover_highs(R)[0] == opt
    assert certified_lower_bound(M, R, cols) <= opt
    assert min_cover_cpsat(R, workers=1)[0] == opt
    assert len(greedy_cover(R)) >= opt


def test_cover_relation_uses_exact_rationals(dia_enum):
    tab = run(dia_enum, 8)
    dist = tab.l1_matrix()
    for L, eps in ((Fr(1, 5), Fr(0)), (Fr(1, 5), Fr(9, 10)), (Fr(3, 7), Fr(11, 4)), (Fr(1), Fr(11, 2))):
        M = cover_matrix_P(tab, L, eps)
        for a in range(0, tab.n_classes, 7):
            for c in range(tab.n_classes):
                assert bool(M[a, c]) == (L * int(dist[a, c]) <= int(tab.gmin[c]) + eps)


def test_l1_distance_is_the_integral_of_the_profile_difference(dia_enum):
    """||N^x - N^y||_1 on [0, S_c): direct integration of the step functions."""
    tab = run(dia_enum, 7)
    s_cut, dists = tab.s_cut, tab.distances
    def profile(h, s):                                           # N(s) = number of pairs at squared distance <= s
        return sum(int(hk) for hk, dk in zip(h, dists) if dk <= s)
    D = tab.l1_matrix()
    for a in range(0, tab.n_classes, 5):
        for c in range(0, tab.n_classes, 3):
            integral = sum(abs(profile(tab.hist[a], s) - profile(tab.hist[c], s)) for s in range(s_cut))
            assert integral == int(D[a, c])                      # unit cells [s, s+1), s = 0 .. S_c - 1
