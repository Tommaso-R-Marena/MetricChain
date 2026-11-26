"""Side-chain chi-angle definitions and rigid rotation about chi bonds.

Standard (IUPAC-IUB 1970) chi definitions with the atom names used by OpenMM's PDB reader
(PDB v3 names; ILE's delta carbon is CD1).  The dihedral sign convention is IUPAC: looking
along b->c, the angle is positive when d is rotated clockwise from a.
"""
from __future__ import annotations

import numpy as np

_X1 = ("N", "CA", "CB")

CHI_ATOMS: dict[str, tuple[tuple[str, str, str, str], ...]] = {
    "ALA": (), "GLY": (),
    "SER": (_X1 + ("OG",),),
    "CYS": (_X1 + ("SG",),),
    "THR": (_X1 + ("OG1",),),
    "VAL": (_X1 + ("CG1",),),
    "PRO": (_X1 + ("CG",), ("CA", "CB", "CG", "CD")),
    "ILE": (_X1 + ("CG1",), ("CA", "CB", "CG1", "CD1")),
    "LEU": (_X1 + ("CG",), ("CA", "CB", "CG", "CD1")),
    "ASP": (_X1 + ("CG",), ("CA", "CB", "CG", "OD1")),
    "ASN": (_X1 + ("CG",), ("CA", "CB", "CG", "OD1")),
    "HIS": (_X1 + ("CG",), ("CA", "CB", "CG", "ND1")),
    "PHE": (_X1 + ("CG",), ("CA", "CB", "CG", "CD1")),
    "TYR": (_X1 + ("CG",), ("CA", "CB", "CG", "CD1")),
    "TRP": (_X1 + ("CG",), ("CA", "CB", "CG", "CD1")),
    "MET": (_X1 + ("CG",), ("CA", "CB", "CG", "SD"), ("CB", "CG", "SD", "CE")),
    "GLU": (_X1 + ("CG",), ("CA", "CB", "CG", "CD"), ("CB", "CG", "CD", "OE1")),
    "GLN": (_X1 + ("CG",), ("CA", "CB", "CG", "CD"), ("CB", "CG", "CD", "OE1")),
    "LYS": (_X1 + ("CG",), ("CA", "CB", "CG", "CD"), ("CB", "CG", "CD", "CE"),
            ("CG", "CD", "CE", "NZ")),
    "ARG": (_X1 + ("CG",), ("CA", "CB", "CG", "CD"), ("CB", "CG", "CD", "NE"),
            ("CG", "CD", "NE", "CZ")),
}


def dihedral_deg(a, b, c, d) -> np.ndarray:
    """Dihedral angle(s) a-b-c-d in degrees in (-180, 180]; arrays broadcast over leading axes."""
    b0, b1, b2 = np.asarray(b) - a, np.asarray(c) - b, np.asarray(d) - c
    n1, n2 = np.cross(b0, b1), np.cross(b1, b2)
    b1hat = b1 / np.linalg.norm(b1, axis=-1, keepdims=True)
    y = np.sum(b1hat * np.cross(n1, n2), axis=-1)
    return np.degrees(np.arctan2(y, np.sum(n1 * n2, axis=-1)))


def rotate_about_axis(points: np.ndarray, origin: np.ndarray, axis_to: np.ndarray, angle_deg: float) -> np.ndarray:
    """Rotate `points` (n,3) by `angle_deg` about the axis origin->axis_to (right-hand rule, Rodrigues)."""
    k = axis_to - origin
    k = k / np.linalg.norm(k)
    t = np.radians(angle_deg)
    v = points - origin
    rot = v * np.cos(t) + np.cross(k, v) * np.sin(t) + np.outer(v @ k, k) * (1.0 - np.cos(t))
    return rot + origin
