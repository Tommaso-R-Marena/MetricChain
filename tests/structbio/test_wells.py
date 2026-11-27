"""Rotamer wells and the share of torsion space of a library state.

Why (SCI-REV-0026): a flip between two states of one well — the deposited conformation and the
library point a few degrees away — is not a change of conformation, and a sum over a state set is
not a quadrature of torsion space unless each state stands for a stated share of it.
"""
from __future__ import annotations

import itertools

import pytest

from metricchain_sb.molecular.chi import CHI_ATOMS
from metricchain_sb.molecular.rotamers import cell_widths, chi_period, library_values, state_share, well_of


def test_periods():
    assert chi_period("PHE", 1) == chi_period("TYR", 1) == chi_period("ASP", 1) == chi_period("GLU", 2) == 180.0
    assert chi_period("LEU", 0) == chi_period("ASN", 1) == chi_period("HIS", 1) == chi_period("GLU", 1) == 360.0


def test_a_library_point_is_its_own_well():
    for resname, quads in CHI_ATOMS.items():
        values = [library_values(resname, k) for k in range(len(quads))]
        for idx in itertools.product(*[range(len(v)) for v in values]):
            assert well_of(resname, [values[k][i] for k, i in enumerate(idx)]) == idx


def test_a_deposited_angle_belongs_to_the_nearest_library_value():
    assert well_of("THR", [-59.34]) == (0,)
    assert well_of("THR", [56.10]) == (2,)
    assert well_of("ILE", [-74.07, 172.83]) == (0, 1)
    assert well_of("SER", [179.0]) == well_of("SER", [-179.0]) == (1,)          # across the cut at 180


def test_symmetric_groups_are_compared_modulo_180():
    assert well_of("PHE", [-60.0, -85.0]) == (0, 0)       # -85 is 95 modulo 180: the value 90
    assert well_of("ASP", [180.0, 170.0]) == (1, 1)       # 170 is -10 modulo 180: the value 0
    assert well_of("ASN", [180.0, 170.0]) == (1, 5)       # no symmetry: the value 180


def test_a_tie_goes_to_the_value_listed_first():
    assert well_of("SER", [0.0]) == (0,)                  # 60 degrees from -60 and from +60


def test_cells_tile_the_period():
    for resname, quads in CHI_ATOMS.items():
        for k in range(len(quads)):
            assert sum(cell_widths(resname, k)) == pytest.approx(chi_period(resname, k))
    assert cell_widths("LEU", 0) == pytest.approx((120.0, 120.0, 120.0))
    assert cell_widths("HIS", 1) == pytest.approx((135.0, 135.0, 90.0))          # values -90, 90, 0
    assert cell_widths("ARG", 3) == pytest.approx((135.0, 135.0, 90.0))          # values -90, 90, 180
    assert cell_widths("TRP", 1) == pytest.approx((135.0, 90.0, 135.0))          # values -90, 0, 90
    assert cell_widths("PHE", 1) == pytest.approx((90.0, 90.0))
    assert cell_widths("ASP", 1) == pytest.approx((60.0, 60.0, 60.0))


def test_shares_of_the_states_of_a_residue_sum_to_one():
    for resname, quads in CHI_ATOMS.items():
        if not quads:
            continue
        sizes = [len(library_values(resname, k)) for k in range(len(quads))]
        total = sum(state_share(resname, idx) for idx in itertools.product(*[range(s) for s in sizes]))
        assert total == pytest.approx(1.0)
    assert state_share("HIS", (0, 2)) == pytest.approx((1 / 3) * (90 / 360))


def test_table_metadata_names_the_well_of_every_state_and_of_the_deposited_conformation():
    import pathlib

    pytest.importorskip("openmm")
    from metricchain_sb.molecular import build_energy_tables

    pdb = str(pathlib.Path(__file__).resolve().parents[2] / "benchmarks" / "structbio" / "pdb" / "1L2Y.pdb")
    library_only = build_energy_tables(pdb, include_native=False)
    for site in library_only.meta["sites"]:
        assert len(site["wells"]) == site["n_states"]
        assert len(site["deposited_chi_angles"]) == len(site["chi_names"])
        assert site["deposited_well"] == list(well_of(site["resname"], site["deposited_chi_angles"]))
        assert sum(site["state_shares"]) == pytest.approx(1.0)
        assert site["deposited_well"] in site["wells"]
    with_deposited = build_energy_tables(pdb, include_native=True)
    for site, lib in zip(with_deposited.meta["sites"], library_only.meta["sites"]):
        assert site["wells"][0] == site["deposited_well"] == lib["deposited_well"]
        assert site["wells"][1:] == lib["wells"]
        assert site["state_shares"][0] is None and site["state_shares"][1:] == lib["state_shares"]
