"""
Workstream P2 (science division) -- capped peptides Ace-X_1...X_n-NMe WITH rotatable side chains.

Extends workstream P's builder (experiments/science/ws_P/pepbuild.py, imported, not modified):
* topology from the residue templates of OpenMM's amber14/protein.ff14SB.xml (atom order and
  bonds are read from the force-field file, nothing is typed by hand except the internal
  coordinates of the side chains below);
* geometry: the same internal-coordinate (NeRF) construction as P -- bond lengths and bond
  angles are the ff14SB equilibrium values read from the OpenMM System, omega = 180 deg,
  methyl / ammonium rotors staggered, substituent offsets at tetrahedral centres solved from
  three equilibrium angles, planar groups exactly planar.  Degrees of freedom: phi_k, psi_k
  (as in P) and the side-chain dihedrals chi_{k,j}.
* energies: P's Peptide._make_contexts / Peptide.energies (OpenMM) are inherited unchanged, so
  P's fastff.FastFF works on these objects without modification.

Side-chain dihedrals (IUPAC): chi1 = N-CA-CB-XG, chi2 = CA-CB-XG-XD, chi3 = CB-XG-XD-XE,
chi4 = XG-XD-XE-XZ.  For SER the hydroxyl torsion CA-CB-OG-HG is treated as chi2.

Units: Angstrom, radians, kcal/mol (as in pepbuild).
"""
import sys, os, math
sys.dont_write_bytecode = True                      # never write into ws_P/__pycache__
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_P"))
import numpy as np
import openmm
import openmm.app as app
import openmm.unit as unit
from pepbuild import Peptide, dihedral, KCAL, KT300, _system      # noqa: E402  (P's module)

THREE = {"A": "ALA", "V": "VAL", "L": "LEU", "S": "SER", "K": "LYS", "F": "PHE", "E": "GLU"}
NCHI = {"ALA": 0, "VAL": 1, "LEU": 2, "SER": 2, "LYS": 4, "PHE": 2, "GLU": 3}
NET_CHARGE = {"ALA": 0, "VAL": 0, "LEU": 0, "SER": 0, "LYS": +1, "PHE": 0, "GLU": -1}

# Internal coordinates of the side-chain atoms beyond CB.  Entry: (atom, (a, b, c), mode, arg):
# the atom is bonded to c, bond angle (b, c, atom), dihedral (a, b, c, atom) =
#   mode "chi": chi_j + const        arg = (j, const in degrees)
#   mode "fix": const                arg = const in degrees
#   mode "sib": dihedral of the sibling `s` (same frame a, b, c) + sign * offset, the offset being
#               solved from the three equilibrium angles (b,c,s), (b,c,atom), (s,c,atom)
#               arg = (s, sign)
_M3 = (180.0, 60.0, -60.0)


def _rotor(names, frame):
    return [(nm, frame, "fix", ang) for nm, ang in zip(names, _M3)]


SIDECHAIN = {
    "ALA": _rotor(("HB1", "HB2", "HB3"), ("N", "CA", "CB")),
    "VAL": [("CG1", ("N", "CA", "CB"), "chi", (0, 0.0)),
            ("CG2", ("N", "CA", "CB"), "sib", ("CG1", +1)),
            ("HB", ("N", "CA", "CB"), "sib", ("CG1", -1))]
           + _rotor(("HG11", "HG12", "HG13"), ("CA", "CB", "CG1"))
           + _rotor(("HG21", "HG22", "HG23"), ("CA", "CB", "CG2")),
    "LEU": [("CG", ("N", "CA", "CB"), "chi", (0, 0.0)),
            ("HB2", ("N", "CA", "CB"), "sib", ("CG", +1)),
            ("HB3", ("N", "CA", "CB"), "sib", ("CG", -1)),
            ("CD1", ("CA", "CB", "CG"), "chi", (1, 0.0)),
            ("CD2", ("CA", "CB", "CG"), "sib", ("CD1", +1)),
            ("HG", ("CA", "CB", "CG"), "sib", ("CD1", -1))]
           + _rotor(("HD11", "HD12", "HD13"), ("CB", "CG", "CD1"))
           + _rotor(("HD21", "HD22", "HD23"), ("CB", "CG", "CD2")),
    "SER": [("OG", ("N", "CA", "CB"), "chi", (0, 0.0)),
            ("HB2", ("N", "CA", "CB"), "sib", ("OG", +1)),
            ("HB3", ("N", "CA", "CB"), "sib", ("OG", -1)),
            ("HG", ("CA", "CB", "OG"), "chi", (1, 0.0))],
    "LYS": [("CG", ("N", "CA", "CB"), "chi", (0, 0.0)),
            ("HB2", ("N", "CA", "CB"), "sib", ("CG", +1)),
            ("HB3", ("N", "CA", "CB"), "sib", ("CG", -1)),
            ("CD", ("CA", "CB", "CG"), "chi", (1, 0.0)),
            ("HG2", ("CA", "CB", "CG"), "sib", ("CD", +1)),
            ("HG3", ("CA", "CB", "CG"), "sib", ("CD", -1)),
            ("CE", ("CB", "CG", "CD"), "chi", (2, 0.0)),
            ("HD2", ("CB", "CG", "CD"), "sib", ("CE", +1)),
            ("HD3", ("CB", "CG", "CD"), "sib", ("CE", -1)),
            ("NZ", ("CG", "CD", "CE"), "chi", (3, 0.0)),
            ("HE2", ("CG", "CD", "CE"), "sib", ("NZ", +1)),
            ("HE3", ("CG", "CD", "CE"), "sib", ("NZ", -1))]
           + _rotor(("HZ1", "HZ2", "HZ3"), ("CD", "CE", "NZ")),
    "PHE": [("CG", ("N", "CA", "CB"), "chi", (0, 0.0)),
            ("HB2", ("N", "CA", "CB"), "sib", ("CG", +1)),
            ("HB3", ("N", "CA", "CB"), "sib", ("CG", -1)),
            ("CD1", ("CA", "CB", "CG"), "chi", (1, 0.0)),
            ("CD2", ("CA", "CB", "CG"), "chi", (1, 180.0)),
            ("HD1", ("CB", "CG", "CD1"), "fix", 0.0),
            ("CE1", ("CB", "CG", "CD1"), "fix", 180.0),
            ("HE1", ("CG", "CD1", "CE1"), "fix", 180.0),
            ("CZ", ("CG", "CD1", "CE1"), "fix", 0.0),
            ("HZ", ("CD1", "CE1", "CZ"), "fix", 180.0),
            ("HD2", ("CB", "CG", "CD2"), "fix", 0.0),
            ("CE2", ("CB", "CG", "CD2"), "fix", 180.0),
            ("HE2", ("CG", "CD2", "CE2"), "fix", 180.0)],
    "GLU": [("CG", ("N", "CA", "CB"), "chi", (0, 0.0)),
            ("HB2", ("N", "CA", "CB"), "sib", ("CG", +1)),
            ("HB3", ("N", "CA", "CB"), "sib", ("CG", -1)),
            ("CD", ("CA", "CB", "CG"), "chi", (1, 0.0)),
            ("HG2", ("CA", "CB", "CG"), "sib", ("CD", +1)),
            ("HG3", ("CA", "CB", "CG"), "sib", ("CD", -1)),
            ("OE1", ("CB", "CG", "CD"), "chi", (2, 0.0)),
            ("OE2", ("CB", "CG", "CD"), "chi", (2, 180.0))],
}
# the four atoms that define each chi (for checking)
CHI_ATOMS = {
    "VAL": [("N", "CA", "CB", "CG1")],
    "LEU": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "CD1")],
    "SER": [("N", "CA", "CB", "OG"), ("CA", "CB", "OG", "HG")],
    "LYS": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "CD"), ("CB", "CG", "CD", "CE"), ("CG", "CD", "CE", "NZ")],
    "PHE": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "CD1")],
    "GLU": [("N", "CA", "CB", "CG"), ("CA", "CB", "CG", "CD"), ("CB", "CG", "CD", "OE1")],
    "ALA": [],
}
BACKBONE_NAMES = ("N", "H", "CA", "HA", "CB", "C", "O")       # atoms that do not depend on any chi

_FF14 = None


def _templates():
    global _FF14
    if _FF14 is None:
        _FF14 = app.ForceField("amber14/protein.ff14SB.xml")
    return _FF14._templates


def parse_seq(seq):
    """'LKSE' or ['LEU', 'LYS', ...] -> list of three-letter names."""
    if isinstance(seq, str):
        return [THREE[c] for c in seq]
    return list(seq)


def make_topology_seq(seq):
    """Ace-seq-NMe.  Atoms in the order of the ff14SB residue templates.  Returns (topology, idx)
    with idx[(res, name)] -> atom index; res = 0 (ACE), 1..n, n+1 (NME)."""
    T = _templates()
    top = app.Topology()
    chain = top.addChain()
    idx, atoms = {}, {}
    names = ["ACE"] + list(seq) + ["NME"]
    for r, resname in enumerate(names):
        t = T[resname]
        res = top.addResidue(resname, chain)
        for a in t.atoms:
            at = top.addAtom(a.name, a.element, res)
            atoms[(r, a.name)] = at
            idx[(r, a.name)] = at.index
        for i, j in t.bonds:
            top.addBond(atoms[(r, t.atoms[i].name)], atoms[(r, t.atoms[j].name)])
    for k in range(len(names) - 1):
        top.addBond(atoms[(k, "C")], atoms[(k + 1, "N")])
    return top, idx


class SCPeptide(Peptide):
    """Geometry builder + energy evaluators for Ace-X_1..X_n-NMe with side chains."""

    def __init__(self, seq, extra_ffs=(), solvent=True, threads=1, platform="CPU"):
        self.seq = parse_seq(seq)
        self.n = len(self.seq)
        self.top, self.idx = make_topology_seq(self.seq)
        self.natoms = self.top.getNumAtoms()
        self.elements = np.array([a.element.symbol for a in self.top.atoms()])
        self.names = [a.name for a in self.top.atoms()]
        self.resid = np.array([a.residue.index for a in self.top.atoms()])
        self.threads = threads
        self.platform = platform
        # chi bookkeeping: column of chi_{k,j} (k = 1..n, j = 0..) in the chi array
        self.chi_col = {}
        for k in range(1, self.n + 1):
            for j in range(NCHI[self.seq[k - 1]]):
                self.chi_col[(k, j)] = len(self.chi_col)
        self.nchi = len(self.chi_col)
        base = _system(("amber14/protein.ff14SB.xml",), self.top)
        self._read_internal(base)
        self._zmatrix()
        self._bond_graph()
        self._make_contexts(base, extra_ffs, solvent)
        # Atoms without Lennard-Jones interaction (epsilon = 0: the hydroxyl hydrogen, Amber type HO)
        # carry a placeholder sigma = 1 nm in OpenMM's file (R_min/2 = 5.61 A); the Amber parameter
        # file has R = 0 for them.  P's clash score is defined with the Amber radii, so use 0.
        self.rmin_half = np.where(self.eps == 0.0, 0.0, self.rmin_half)
        # which site (residue 1..n; 0 = none, i.e. fixed on a fixed backbone) each atom depends on
        dep = np.zeros(self.natoms, dtype=int)
        for (k, nm), a in self.idx.items():
            if 1 <= k <= self.n and nm not in BACKBONE_NAMES and NCHI[self.seq[k - 1]] > 0:
                dep[a] = k
        self.site_of_atom = dep

    # ------------------------------------------------------------------ Z-matrix
    def _zmatrix(self):
        """As pepbuild.Peptide._zmatrix, with the side chains appended residue by residue.
        Entry: (atom, a, b, c, bond, angle, kind, const), dihedral (a, b, c, atom) = const + v,
        v = 0 for kind ('fix',), phi_k for ('phi', k), psi_k for ('psi', k), chi[col] for ('chi', col)."""
        I = self.idx
        n = self.n
        Z = []

        def add(atom, a, b, c, kind, const):
            Z.append((atom, a, b, c, self.r0[(c, atom)], self.a0[(b, c, atom)], kind, const))

        ace_c, ace_ch3, ace_o = I[(0, "C")], I[(0, "CH3")], I[(0, "O")]
        self.first3 = (ace_ch3, ace_c, I[(1, "N")])
        pi = math.pi
        self.dCB, self.dHA = {}, {}
        for k in range(1, n + 2):
            prevC = I[(k - 1, "C")]
            prevCA = I[(k - 1, "CA")] if k >= 2 else ace_ch3
            N = I[(k, "N")]
            if k >= 2:
                add(N, I[(k - 1, "N")], prevCA, prevC, ("psi", k - 1), 0.0)
                add(I[(k - 1, "O")], I[(k - 1, "N")], prevCA, prevC, ("psi", k - 1), pi)
            add(I[(k, "H")], prevCA, prevC, N, ("fix",), 0.0)
            CAname = "CA" if k <= n else "CH3"
            CA = I[(k, CAname)]
            add(CA, prevCA, prevC, N, ("fix",), pi)
            if k <= n:
                C = I[(k, "C")]
                add(C, prevC, N, CA, ("phi", k), 0.0)
                tNC = self.a0[(N, CA, C)]
                CB, HA = I[(k, "CB")], I[(k, "HA")]
                dCB = self._offset(tNC, self.a0[(N, CA, CB)], self.a0[(C, CA, CB)])
                dHA = self._offset(tNC, self.a0[(N, CA, HA)], self.a0[(C, CA, HA)])
                add(CB, prevC, N, CA, ("phi", k), -dCB)       # L-amino acid (chiral volume checked)
                add(HA, prevC, N, CA, ("phi", k), +dHA)
                self.dCB[k], self.dHA[k] = dCB, dHA
                placed = {}
                for name, (an, bn, cn), mode, arg in SIDECHAIN[self.seq[k - 1]]:
                    a, b, c, at = I[(k, an)], I[(k, bn)], I[(k, cn)], I[(k, name)]
                    if mode == "fix":
                        kind, const = ("fix",), math.radians(arg)
                    elif mode == "chi":
                        kind, const = ("chi", self.chi_col[(k, arg[0])]), math.radians(arg[1])
                    elif mode == "sib":
                        sib, sign = arg
                        skind, sconst, sframe = placed[sib]
                        assert sframe == (an, bn, cn), (name, sib)
                        s = I[(k, sib)]
                        off = self._offset(self.a0[(b, c, s)], self.a0[(b, c, at)], self.a0[(s, c, at)])
                        kind, const = skind, sconst + sign * off
                    else:
                        raise ValueError(mode)
                    placed[name] = (kind, const, (an, bn, cn))
                    add(at, a, b, c, kind, const)
            else:
                for name, ang in (("HH31", pi), ("HH32", pi / 3), ("HH33", -pi / 3)):
                    add(I[(k, name)], prevC, N, CA, ("fix",), ang)
        self.Z = Z
        self.ace = (ace_ch3, ace_c, ace_o, I[(1, "N")], I[(1, "CA")],
                    [I[(0, "HH31")], I[(0, "HH32")], I[(0, "HH33")]])
        placed_atoms = sorted([z[0] for z in Z] + list(self.first3) + [ace_o] + self.ace[5])
        assert placed_atoms == list(range(self.natoms)), "every atom must be placed exactly once"

    # ------------------------------------------------------------------ coordinates
    def coords(self, phi, psi, chi=None):
        """phi, psi: (M, n) radians; chi: (M, nchi) radians (columns: self.chi_col).
        Returns positions (M, natoms, 3) in Angstrom."""
        phi = np.atleast_2d(np.asarray(phi, dtype=float))
        psi = np.atleast_2d(np.asarray(psi, dtype=float))
        M = phi.shape[0]
        if chi is None:
            chi = np.zeros((M, max(self.nchi, 1)))
        chi = np.atleast_2d(np.asarray(chi, dtype=float))
        X = np.zeros((M, self.natoms, 3))
        ch3, c, n1 = self.first3
        rb = self.r0[(ch3, c)]
        rn = self.r0[(c, n1)]
        th = self.a0[(ch3, c, n1)]
        X[:, ch3] = 0.0
        X[:, c] = np.array([rb, 0.0, 0.0])
        X[:, n1] = np.array([rb - rn * math.cos(th), rn * math.sin(th), 0.0])
        for atom, a, b, cc, bond, angle, kind, const in self.Z:
            if kind[0] == "fix":
                dih = np.full(M, const)
            elif kind[0] == "phi":
                dih = phi[:, kind[1] - 1] + const
            elif kind[0] == "psi":
                dih = psi[:, kind[1] - 1] + const
            else:
                dih = chi[:, kind[1]] + const
            X[:, atom] = self._place(X[:, a], X[:, b], X[:, cc], bond, angle, dih)
        ch3, c, o, n1, ca1, hs = self.ace
        X[:, o] = self._place(X[:, ca1], X[:, n1], X[:, c], self.r0[(c, o)], self.a0[(n1, c, o)],
                              np.zeros(M))
        for h, ang in zip(hs, (math.pi, math.pi / 3, -math.pi / 3)):
            X[:, h] = self._place(X[:, n1], X[:, c], X[:, ch3], self.r0[(ch3, h)],
                                  self.a0[(c, ch3, h)], np.full(M, ang))
        return X

    def chi_quads(self):
        """list over chi columns of the four atom indices that define the dihedral."""
        out = [None] * self.nchi
        for (k, j), col in self.chi_col.items():
            out[col] = tuple(self.idx[(k, nm)] for nm in CHI_ATOMS[self.seq[k - 1]][j])
        return out
