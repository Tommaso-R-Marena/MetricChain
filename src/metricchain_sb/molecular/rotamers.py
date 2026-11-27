"""The synthetic, licence-free "idealised staggered library" (rotamer chi values in degrees).

Rule: an sp3-sp3 chi bond takes the three staggered values (-60, 180, +60).  Chis whose distal
bond atom is sp2 (or whose distal group is planar) take the values in `_SP2` below.  Where the
distal group has a two-fold symmetry under which the ff14SB energy is invariant (PHE/TYR ring
flip, ASP/GLU carboxylate flip: identical atom types and charges on both halves) the values are
chosen distinct modulo 180, so no two library states are related by the symmetry.  No-symmetry
planar groups (ASN/GLN amide, HIS/TRP ring, ARG guanidinium) take values covering the full
circle.  States of a site are the Cartesian product over its chis (in chi order, values in the
order listed here), preceded by the native state (see tables.py).
"""
from __future__ import annotations

from .chi import CHI_ATOMS

STAGGERED = (-60.0, 180.0, 60.0)

# (residue, 0-based chi index) -> values; all other chis are sp3-sp3 -> STAGGERED
_SP2: dict[tuple[str, int], tuple[float, ...]] = {
    ("PHE", 1): (90.0, 0.0),                               # ring flip: period 180
    ("TYR", 1): (90.0, 0.0),                               # ring flip: period 180
    ("TRP", 1): (-90.0, 0.0, 90.0),
    ("HIS", 1): (-90.0, 90.0, 0.0),
    ("ASN", 1): (-120.0, -60.0, 0.0, 60.0, 120.0, 180.0),  # amide, no symmetry
    ("GLN", 2): (-120.0, -60.0, 0.0, 60.0, 120.0, 180.0),  # amide, no symmetry
    ("ASP", 1): (-60.0, 0.0, 60.0),                        # carboxylate: period 180
    ("GLU", 2): (-60.0, 0.0, 60.0),                        # carboxylate: period 180
    ("ARG", 3): (-90.0, 90.0, 180.0),                      # CD-NE (NE sp2)
}


def library_values(resname: str, chi_index: int) -> tuple[float, ...]:
    """Library chi values (degrees) for chi number `chi_index` (0-based) of `resname`."""
    if chi_index >= len(CHI_ATOMS[resname]):
        raise KeyError(f"{resname} has no chi{chi_index + 1}")
    return _SP2.get((resname, chi_index), STAGGERED)


def library_table() -> dict[str, list[list[float]]]:
    """The whole library, for the metadata."""
    return {r: [list(library_values(r, k)) for k in range(len(q))] for r, q in CHI_ATOMS.items() if q}


# ----------------------------------------------------------------------------- wells and cells
# chis under whose half-turn the ff14SB energy is invariant (see the module docstring)
_PERIOD_180 = frozenset({("PHE", 1), ("TYR", 1), ("ASP", 1), ("GLU", 2)})


def chi_period(resname: str, chi_index: int) -> float:
    """Period (degrees) of chi number `chi_index` (0-based): 180 for the symmetric groups, else 360."""
    if chi_index >= len(CHI_ATOMS[resname]):
        raise KeyError(f"{resname} has no chi{chi_index + 1}")
    return 180.0 if (resname, chi_index) in _PERIOD_180 else 360.0


def _circular(a: float, b: float, period: float) -> float:
    d = abs(a - b) % period
    return min(d, period - d)


def well_of(resname: str, chis) -> tuple[int, ...]:
    """The rotamer well of a conformation: per chi, the index of the nearest library value
    (distance on the circle of that chi's period; a tie goes to the value listed first)."""
    well = []
    for k, angle in enumerate(chis):
        values, period = library_values(resname, k), chi_period(resname, k)
        well.append(min(range(len(values)), key=lambda i: (_circular(angle, values[i], period), i)))
    return tuple(well)


def cell_widths(resname: str, chi_index: int) -> tuple[float, ...]:
    """Width (degrees) of the cell of each library value of one chi: the points of the circle
    nearer to it than to any other library value.  The widths add up to the period."""
    values, period = library_values(resname, chi_index), chi_period(resname, chi_index)
    reduced = [v % period for v in values]
    widths = []
    for i, v in enumerate(reduced):
        others = [(w - v) % period for j, w in enumerate(reduced) if j != i]
        if not others:
            widths.append(period)
            continue
        ahead, behind = min(others), period - max(others)
        widths.append((ahead + behind) / 2.0)
    return tuple(widths)


def state_share(resname: str, well) -> float:
    """Share of the residue's torsion space that the library state `well` stands for: the product
    over chis of (cell width / period).  The shares of all library states add up to 1."""
    share = 1.0
    for k, i in enumerate(well):
        share *= cell_widths(resname, k)[i] / chi_period(resname, k)
    return share
