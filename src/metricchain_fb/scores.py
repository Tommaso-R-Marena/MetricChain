"""Structure-comparison scores written from their published definitions, for cross-checking.

These are this division's *own* implementations.  They exist so that every number we report
about a structure has been computed twice — once here, once by an established package — and
so that their blind spots are known from planted controls (`tests/frontier/test_scores.py`).
They are not a replacement for the community's reference programs (LGA, OpenStructure,
TM-score): `agreement with the official numbers` is an empirical question that protocol
FB-P-10 answers, not an assumption.

Conventions: coordinates are ``(N, 3)`` float arrays in ångström; a *correspondence* is given
by position (row ``i`` of the model corresponds to row ``i`` of the reference) — no sequence
alignment is performed here.

Known blind spot, demonstrated by the tests: every distance-based score (lDDT, and any score
computed from internal distances) is unchanged under reflection, so it cannot distinguish a
structure from its mirror image.
"""
from __future__ import annotations

import math

import numpy as np

__all__ = ["kabsch", "rmsd", "lddt", "gdt", "gdt_ts", "gdt_ha", "tm_score", "dihedral", "angular_difference",
           "CHI_ATOMS", "CHI_PERIOD_180", "chi_angles", "chi_recovery"]


# --------------------------------------------------------------------------- superposition
def kabsch(mobile: np.ndarray, target: np.ndarray, weights: np.ndarray | None = None):
    """Proper rotation ``R`` and translation ``t`` minimising ``sum w |R m + t - x|^2``.

    Returns ``(R, t)`` with ``det R = +1`` (reflections are never used).
    """
    mobile = np.asarray(mobile, dtype=float)
    target = np.asarray(target, dtype=float)
    if mobile.shape != target.shape or mobile.ndim != 2 or mobile.shape[1] != 3:
        raise ValueError("kabsch needs two (N, 3) arrays of equal shape")
    w = np.ones(len(mobile)) if weights is None else np.asarray(weights, dtype=float)
    w = w / w.sum()
    cm, ct = w @ mobile, w @ target
    H = (mobile - cm).T @ ((target - ct) * w[:, None])
    U, _, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1.0, 1.0, d])
    R = Vt.T @ D @ U.T
    return R, ct - R @ cm


def rmsd(model: np.ndarray, reference: np.ndarray, superpose: bool = True) -> float:
    """Root-mean-square deviation, after optimal proper superposition unless ``superpose`` is False."""
    model = np.asarray(model, dtype=float)
    reference = np.asarray(reference, dtype=float)
    if superpose:
        R, t = kabsch(model, reference)
        model = model @ R.T + t
    return float(np.sqrt(np.mean(np.sum((model - reference) ** 2, axis=1))))


# --------------------------------------------------------------------------- lDDT
def lddt(model: np.ndarray, reference: np.ndarray, residue_index=None, cutoff: float = 15.0,
         thresholds=(0.5, 1.0, 2.0, 4.0), per_residue: bool = False):
    """Local distance difference test (Mariani et al. 2013), superposition-free.

    Every pair of atoms from *different residues* whose distance in the reference is below
    ``cutoff`` is a preserved-distance test; a test passes at threshold ``d`` if the model
    distance differs by less than ``d``.  The score is the mean over thresholds of the fraction
    passed.  ``residue_index`` gives the residue of each atom (default: one atom per residue).
    No stereochemistry penalty is applied (the reference implementation can apply one).
    """
    model = np.asarray(model, dtype=float)
    reference = np.asarray(reference, dtype=float)
    n = len(reference)
    res = np.arange(n) if residue_index is None else np.asarray(residue_index)
    dr = np.linalg.norm(reference[:, None, :] - reference[None, :, :], axis=2)
    dm = np.linalg.norm(model[:, None, :] - model[None, :, :], axis=2)
    mask = (dr < cutoff) & (res[:, None] != res[None, :])
    diff = np.abs(dr - dm)
    passed = np.zeros((n, n))
    for d in thresholds:
        passed += (diff < d) & mask
    passed /= len(thresholds)
    total = mask.sum()
    if per_residue:
        uniq = np.unique(res)
        out = {}
        for r in uniq:
            rows = res == r
            denom = mask[rows].sum()
            out[int(r)] = float(passed[rows].sum() / denom) if denom else float("nan")
        return out
    return float(passed.sum() / total) if total else float("nan")


# --------------------------------------------------------------------------- GDT and TM-score
def _seed_windows(n: int):
    lengths = sorted({n, max(n // 2, 4), max(n // 4, 4), 4} & set(range(3, n + 1)) or {min(n, 3)}, reverse=True)
    for length in lengths:
        step = max(1, length // 2)
        for start in range(0, n - length + 1, step):
            yield np.arange(start, start + length)
        if (n - length) % step:
            yield np.arange(n - length, n)


def _search_superpositions(model, reference, objective, cut_schedule):
    """Heuristic search over superpositions used by GDT and TM-score: seed on contiguous
    windows, then iterate "superpose on the atoms currently within the cut-off" to convergence.
    Returns the best objective value found (a lower bound on the true maximum)."""
    n = len(reference)
    best = -1.0
    for seed in _seed_windows(n):
        if len(seed) < 3:
            continue
        subset = seed
        for cut in cut_schedule:
            for _ in range(20):
                R, t = kabsch(model[subset], reference[subset])
                dist = np.linalg.norm(model @ R.T + t - reference, axis=1)
                best = max(best, objective(dist))
                new = np.nonzero(dist < cut)[0]
                if len(new) < 3 or np.array_equal(new, subset):
                    break
                subset = new
    return best


def gdt(model: np.ndarray, reference: np.ndarray, cutoffs=(1.0, 2.0, 4.0, 8.0)) -> dict:
    """For each cut-off, the largest fraction of reference positions that can be brought within
    it by one proper rigid superposition (heuristic search: values are lower bounds)."""
    model = np.asarray(model, dtype=float)
    reference = np.asarray(reference, dtype=float)
    out = {}
    for c in cutoffs:
        schedule = (c + 1.0, c + 0.5, c)
        out[c] = _search_superpositions(model, reference, lambda d, c=c: float(np.mean(d <= c)), schedule)
    return out


def gdt_ts(model, reference) -> float:
    """GDT_TS in percent: mean of the fractions at 1, 2, 4 and 8 Å."""
    g = gdt(model, reference, (1.0, 2.0, 4.0, 8.0))
    return 100.0 * sum(g.values()) / 4.0


def gdt_ha(model, reference) -> float:
    """GDT_HA in percent: mean of the fractions at 0.5, 1, 2 and 4 Å."""
    g = gdt(model, reference, (0.5, 1.0, 2.0, 4.0))
    return 100.0 * sum(g.values()) / 4.0


def tm_score(model: np.ndarray, reference: np.ndarray, length: int | None = None) -> float:
    """TM-score (Zhang & Skolnick 2004) for a fixed correspondence, normalised by ``length``
    (default: the number of reference positions).  Heuristic search: a lower bound."""
    model = np.asarray(model, dtype=float)
    reference = np.asarray(reference, dtype=float)
    L = len(reference) if length is None else int(length)
    d0 = max(0.5, 1.24 * (L - 15) ** (1.0 / 3.0) - 1.8) if L > 15 else 0.5
    objective = lambda d: float(np.sum(1.0 / (1.0 + (d / d0) ** 2)) / L)
    return _search_superpositions(model, reference, objective, (d0 * 2 + 4.0, d0 + 2.0, max(d0, 1.0), 8.0, 4.0))


# --------------------------------------------------------------------------- torsion angles
def dihedral(p0, p1, p2, p3) -> float:
    """Signed dihedral angle in degrees (IUPAC convention) of four points."""
    p0, p1, p2, p3 = (np.asarray(p, dtype=float) for p in (p0, p1, p2, p3))
    b0, b1, b2 = p0 - p1, p2 - p1, p3 - p2
    b1n = b1 / np.linalg.norm(b1)
    v = b0 - np.dot(b0, b1n) * b1n
    w = b2 - np.dot(b2, b1n) * b1n
    return math.degrees(math.atan2(np.dot(np.cross(b1n, v), w), np.dot(v, w)))


def angular_difference(a: float, b: float, period: float = 360.0) -> float:
    """Smallest absolute difference of two angles in degrees modulo ``period``."""
    d = (a - b) % period
    return min(d, period - d)


#: Side-chain torsions chi1..chi4 by residue (IUPAC atom names).
CHI_ATOMS = {
    "ARG": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "CD"), ("CB", "CG", "CD", "NE"), ("CG", "CD", "NE", "CZ")],
    "ASN": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "OD1")],
    "ASP": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "OD1")],
    "CYS": [("N", "CA", "CB", "SG")],
    "GLN": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "CD"), ("CB", "CG", "CD", "OE1")],
    "GLU": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "CD"), ("CB", "CG", "CD", "OE1")],
    "HIS": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "ND1")],
    "ILE": [("N", "CA", "CB", "CG1"), ("CA", "CB", "CG1", "CD1")],
    "LEU": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "CD1")],
    "LYS": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "CD"), ("CB", "CG", "CD", "CE"), ("CG", "CD", "CE", "NZ")],
    "MET": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "SD"), ("CB", "CG", "SD", "CE")],
    "PHE": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "CD1")],
    "PRO": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "CD")],
    "SER": [("N", "CA", "CB", "OG")],
    "THR": [("N", "CA", "CB", "OG1")],
    "TRP": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "CD1")],
    "TYR": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "CD1")],
    "VAL": [("N", "CA", "CB", "CG1")],
}
#: (residue, chi number) whose terminal group is symmetric, so the angle is defined modulo 180 degrees.
CHI_PERIOD_180 = {("ASP", 2), ("GLU", 3), ("PHE", 2), ("TYR", 2)}


def chi_angles(resname: str, atoms: dict) -> list:
    """chi1.. of one residue from a mapping atom name -> coordinates; ``None`` where an atom is missing."""
    out = []
    for names in CHI_ATOMS.get(resname.upper(), []):
        if all(a in atoms for a in names):
            out.append(dihedral(*(atoms[a] for a in names)))
        else:
            out.append(None)
    return out


def chi_recovery(resname: str, model_chis, reference_chis, tolerance: float = 20.0, upto: int | None = None):
    """Is the side chain "recovered"?  True iff every chi up to ``upto`` (default: all defined in
    the reference) differs by at most ``tolerance`` degrees, with 180-degree periodicity for
    symmetric terminal groups.  Returns ``None`` if nothing can be compared."""
    resname = resname.upper()
    count = len(reference_chis) if upto is None else min(upto, len(reference_chis))
    compared = False
    for k in range(count):
        ref, mod = reference_chis[k], model_chis[k] if k < len(model_chis) else None
        if ref is None:
            continue
        if mod is None:
            return False
        compared = True
        period = 180.0 if (resname, k + 1) in CHI_PERIOD_180 else 360.0
        if angular_difference(mod, ref, period) > tolerance:
            return False
    return True if compared else None
