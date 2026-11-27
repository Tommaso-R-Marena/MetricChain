"""The generic (off-lattice) rotamer chain of docs/workstreams/P_REPORT.md section 0 ("gen").

Independent implementation from the definition:

* beads ``0..N-1``, ``N = n+3``; bond length 1, bond angle 111 degrees; ``n`` torsions with states
  ``t, g+, g-`` (180, +60, -60 degrees);
* hard core: squared distance ``s_pq >= 3.0`` for every pair with ``q - p >= 3``;
* pairs ``P = {(p, q) : q - p >= 3}``; truncated squared distances ``min(s_pq, S_c)``, ``S_c = 16``;
* the profile of a conformation is the counting function of its squared distances below the
  cutoff, and ``||N^x - N^y||_1 = || sort(s~^x) - sort(s~^y) ||_{l1}`` (P_REPORT Proposition 2:
  the one-dimensional Wasserstein distance between the multisets of truncated distances).

Distances are irrational, so everything here is floating point: two conformations are put in
the same profile class when their sorted truncated distances agree after rounding to
``ROUND_DECIMALS`` decimals, and cover relations are decided with the tolerance ``TOL``.  The
functions report how close the nearest comparison came to the tolerance, so that a result can
be seen to be insensitive to it (or not).
"""
from __future__ import annotations

import dataclasses
import math
from fractions import Fraction

import numpy as np

ROUND_DECIMALS = 8
TOL = 1e-9


def _place(a: np.ndarray, b: np.ndarray, c: np.ndarray, bond: float, angle: float, dihedral: float) -> np.ndarray:
    """Next atom from the three previous ones and (bond length, bond angle, dihedral angle)."""
    bc = c - b
    bc = bc / np.linalg.norm(bc)
    nrm = np.cross(b - a, bc)
    nrm = nrm / np.linalg.norm(nrm)
    m = np.cross(nrm, bc)
    return (c - bond * math.cos(angle) * bc + bond * math.sin(angle) * math.cos(dihedral) * m
            + bond * math.sin(angle) * math.sin(dihedral) * nrm)


@dataclasses.dataclass
class GenericClassTable:
    n_torsions: int
    s_cut: float
    n_pairs: int                        # |P| = number of pairs with q - p >= 3
    below: list[np.ndarray]             # per class: sorted squared distances below the cutoff
    count: np.ndarray                   # conformations per class
    gmin: np.ndarray                    # fewest gauche torsions per class
    n_conformations: int
    min_core_margin: float              # smallest (s_pq - hard core) among accepted conformations
    min_rejected_margin: float          # smallest (hard core - s_pq) among rejected placements

    @property
    def n_beads(self) -> int:
        return self.n_torsions + 3

    @property
    def n_classes(self) -> int:
        return len(self.below)

    def sorted_truncated(self) -> np.ndarray:
        """(classes, |P|) matrix of sorted truncated squared distances (padded with S_c)."""
        V = np.full((self.n_classes, self.n_pairs), self.s_cut, dtype=np.float64)
        for i, v in enumerate(self.below):
            V[i, : len(v)] = v
        return V

    def l1_matrix(self, chunk: int = 256) -> np.ndarray:
        V = self.sorted_truncated()
        n = V.shape[0]
        D = np.empty((n, n), dtype=np.float64)
        for i in range(0, n, chunk):
            D[i:i + chunk] = np.abs(V[i:i + chunk, None, :] - V[None, :, :]).sum(axis=2)
        return D


def enumerate_generic(n: int, s_cut: float = 16.0, hard_core: float = 3.0, bond: float = 1.0,
                      angle_deg: float = 111.0, mirror: bool = True) -> GenericClassTable:
    """All hard-core conformations of the generic chain with ``n`` torsions, grouped into profile classes."""
    angle = math.radians(angle_deg)
    dih = (math.pi, math.pi / 3.0, -math.pi / 3.0)           # t, g+, g-
    N = n + 3
    pts = np.zeros((N, 3))
    pts[1] = (bond, 0.0, 0.0)
    pts[2] = pts[1] + bond * np.array([-math.cos(angle), math.sin(angle), 0.0])
    classes: dict[bytes, list] = {}
    stats = {"conf": 0, "core": math.inf, "rej": math.inf}
    dist_stack: list[np.ndarray] = []                         # squared distances of bead q to beads 0..q-3

    def leaf(g: int, w: int) -> None:
        d = np.concatenate(dist_stack) if dist_stack else np.empty(0)
        below = np.sort(d[d < s_cut - TOL])
        key = np.round(below, ROUND_DECIMALS).tobytes()
        e = classes.get(key)
        if e is None:
            classes[key] = [below, w, g]
        else:
            e[1] += w
            if g < e[2]:
                e[2] = g
        stats["conf"] += w

    def extend(q: int, g: int, seen_gauche: bool, w: int) -> None:
        if q == N:
            leaf(g, w)
            return
        for state in range(3):
            w2, seen2 = w, seen_gauche
            if state != 0:
                if mirror and not seen_gauche:
                    if state == 2:
                        continue                              # mirror image of the g+ branch
                    w2 = 2 * w
                seen2 = True
            x = _place(pts[q - 3], pts[q - 2], pts[q - 1], bond, angle, dih[state])
            d = ((pts[: q - 2] - x) ** 2).sum(axis=1)         # beads 0..q-3
            margin = float(d.min()) - hard_core
            if margin < -TOL:
                stats["rej"] = min(stats["rej"], -margin)
                continue
            stats["core"] = min(stats["core"], margin)
            pts[q] = x
            dist_stack.append(d)
            extend(q + 1, g + (state != 0), seen2, w2)
            dist_stack.pop()

    extend(3, 0, False, 1)
    keys = sorted(classes, key=lambda k: (len(classes[k][0]), k))
    return GenericClassTable(
        n_torsions=n, s_cut=s_cut, n_pairs=(N - 3) * (N - 2) // 2,
        below=[classes[k][0] for k in keys],
        count=np.array([classes[k][1] for k in keys], dtype=np.int64),
        gmin=np.array([classes[k][2] for k in keys], dtype=np.int64),
        n_conformations=stats["conf"], min_core_margin=stats["core"], min_rejected_margin=stats["rej"])


def cover_matrix_generic(tab: GenericClassTable, L, eps, e=1.0, dist: np.ndarray | None = None
                         ) -> tuple[np.ndarray, float]:
    """``M[a, c]``: an evaluation in class ``a`` covers class ``c`` (``L d(a,c) <= e gmin(c) + eps``).

    Returns the matrix and the smallest absolute distance of any comparison from equality (if it
    is of the order of the tolerance the result depends on rounding and must not be trusted).
    """
    D = tab.l1_matrix() if dist is None else dist
    slack = float(Fraction(e)) * tab.gmin[None, :].astype(np.float64) + float(Fraction(eps)) - float(Fraction(L)) * D
    return slack >= -TOL, float(np.abs(slack).min())
