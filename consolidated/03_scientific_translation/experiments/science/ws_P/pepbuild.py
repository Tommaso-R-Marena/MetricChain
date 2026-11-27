"""
Workstream P (science division) -- capped alanine peptides Ace-(Ala)_n-NMe on a torsion grid.

* Topology built by hand (OpenMM app.Topology), atom order = Amber residue templates.
* Geometry: internal-coordinate (NeRF) builder, vectorised over conformations.
  Bond lengths and bond angles = ff14SB equilibrium values read from the OpenMM System;
  omega = 180 deg; methyl groups staggered; substituent dihedral offsets at CA solved from
  three equilibrium angles (so that N-CA-C, N-CA-CB, C-CA-CB are all at equilibrium);
  peptide groups exactly planar.  The only degrees of freedom are phi_k, psi_k.
* Energies: OpenMM (CPU platform, one thread), no cutoff, no constraints.

Units: OpenMM works in nm and kJ/mol; everything returned by this module is in
Angstrom and kcal/mol.
"""
import copy
import math
import numpy as np
import openmm
import openmm.app as app
import openmm.unit as unit

KCAL = 4.184                      # kJ per kcal
KT300 = 0.0019872041 * 300.0      # kcal/mol at 300 K  (= 0.596161)

ACE_ATOMS = [("HH31", "H"), ("CH3", "C"), ("HH32", "H"), ("HH33", "H"), ("C", "C"), ("O", "O")]
ALA_ATOMS = [("N", "N"), ("H", "H"), ("CA", "C"), ("HA", "H"), ("CB", "C"), ("HB1", "H"),
             ("HB2", "H"), ("HB3", "H"), ("C", "C"), ("O", "O")]
NME_ATOMS = [("N", "N"), ("H", "H"), ("CH3", "C"), ("HH31", "H"), ("HH32", "H"), ("HH33", "H")]
ACE_BONDS = [("CH3", "HH31"), ("CH3", "HH32"), ("CH3", "HH33"), ("CH3", "C"), ("C", "O")]
ALA_BONDS = [("N", "H"), ("N", "CA"), ("CA", "HA"), ("CA", "CB"), ("CB", "HB1"), ("CB", "HB2"),
             ("CB", "HB3"), ("CA", "C"), ("C", "O")]
NME_BONDS = [("N", "H"), ("N", "CH3"), ("CH3", "HH31"), ("CH3", "HH32"), ("CH3", "HH33")]


def make_topology(n):
    """Ace-(Ala)_n-NMe.  Returns (topology, index) with index[(res, name)] -> atom index,
    res = 0 for ACE, 1..n for ALA, n+1 for NME."""
    top = app.Topology()
    chain = top.addChain()
    idx = {}
    atoms = {}
    el = {"H": app.element.hydrogen, "C": app.element.carbon, "N": app.element.nitrogen,
          "O": app.element.oxygen}

    def add(resname, r, atomlist, bondlist):
        res = top.addResidue(resname, chain)
        for name, e in atomlist:
            a = top.addAtom(name, el[e], res)
            atoms[(r, name)] = a
            idx[(r, name)] = a.index
        for a, b in bondlist:
            top.addBond(atoms[(r, a)], atoms[(r, b)])

    add("ACE", 0, ACE_ATOMS, ACE_BONDS)
    for k in range(1, n + 1):
        add("ALA", k, ALA_ATOMS, ALA_BONDS)
    add("NME", n + 1, NME_ATOMS, NME_BONDS)
    for k in range(0, n + 1):
        top.addBond(atoms[(k, "C")], atoms[(k + 1, "N")])
    return top, idx


def _system(ffxml, top, **kw):
    ff = app.ForceField(*ffxml)
    return ff.createSystem(top, nonbondedMethod=app.NoCutoff, constraints=None,
                           rigidWater=False, removeCMMotion=False, **kw)


class Peptide:
    """Geometry builder + energy evaluators for Ace-(Ala)_n-NMe."""

    def __init__(self, n, extra_ffs=("ff99SB", "ff19SB", "ff03", "ff15ipq"), solvent=True,
                 threads=1, platform="CPU"):
        self.n = n
        self.top, self.idx = make_topology(n)
        self.natoms = self.top.getNumAtoms()
        self.elements = np.array([a.element.symbol for a in self.top.atoms()])
        self.names = [a.name for a in self.top.atoms()]
        self.resid = np.array([a.residue.index for a in self.top.atoms()])
        self.threads = threads
        self.platform = platform
        base = _system(("amber14/protein.ff14SB.xml",), self.top)
        self._read_internal(base)
        self._zmatrix()
        self._bond_graph()
        self._make_contexts(base, extra_ffs, solvent)

    # ------------------------------------------------------------------ geometry inputs
    def _read_internal(self, system):
        self.r0 = {}
        self.a0 = {}
        for f in system.getForces():
            if isinstance(f, openmm.HarmonicBondForce):
                for b in range(f.getNumBonds()):
                    i, j, r, k = f.getBondParameters(b)
                    r = r.value_in_unit(unit.angstrom)
                    self.r0[(i, j)] = r
                    self.r0[(j, i)] = r
            if isinstance(f, openmm.HarmonicAngleForce):
                for a in range(f.getNumAngles()):
                    i, j, k, th, kk = f.getAngleParameters(a)
                    th = th.value_in_unit(unit.radian)
                    self.a0[(i, j, k)] = th
                    self.a0[(k, j, i)] = th

    @staticmethod
    def _offset(t1, t2, t3):
        """Dihedral offset between substituents X and Y about an axis A-B, given the angles
        t1 = A-B-X, t2 = A-B-Y, t3 = X-B-Y (spherical law of cosines)."""
        c = (math.cos(t3) - math.cos(t1) * math.cos(t2)) / (math.sin(t1) * math.sin(t2))
        return math.acos(max(-1.0, min(1.0, c)))

    def _zmatrix(self):
        """Each entry: (atom, a, b, c, bond, angle, kind, const) meaning
        atom is bonded to c, angle (b, c, atom), dihedral (a, b, c, atom) =
        const + {0, phi_k, psi_k} depending on kind = ('fix',), ('phi', k), ('psi', k)."""
        I = self.idx
        n = self.n
        Z = []

        def add(atom, a, b, c, kind, const):
            Z.append((atom, a, b, c, self.r0[(c, atom)], self.a0[(b, c, atom)], kind, const))

        ace_c, ace_ch3, ace_o = I[(0, "C")], I[(0, "CH3")], I[(0, "O")]
        # first three atoms (CH3, C of ACE, N of residue 1) are placed explicitly
        self.first3 = (ace_ch3, ace_c, I[(1, "N")])
        pi = math.pi
        for k in range(1, n + 2):          # residues 1..n (ALA) and n+1 (NME)
            prevC = I[(k - 1, "C")]
            prevCA = I[(k - 1, "CA")] if k >= 2 else ace_ch3
            N = I[(k, "N")]
            if k >= 2:
                # N_k from (N_{k-1}, CA_{k-1}, C_{k-1}) with psi_{k-1}
                add(N, I[(k - 1, "N")], prevCA, prevC, ("psi", k - 1), 0.0)
            # carbonyl O of the previous residue: planar, trans to N_k about CA-C
            if k >= 2:
                add(I[(k - 1, "O")], I[(k - 1, "N")], prevCA, prevC, ("psi", k - 1), pi)
            else:
                # ACE: O placed from (N1?, ...) -- N1 is one of the first three atoms.
                # dihedral (N1, CH3, C, O) is not a chain dihedral; place O in the plane of
                # CH3, C, N1 by an improper-style construction below (special-cased).
                pass
            # amide H: cis to the previous CA about C-N (dihedral 0); next heavy atom: trans
            add(I[(k, "H")], prevCA, prevC, N, ("fix",), 0.0)
            CAname = "CA" if k <= n else "CH3"
            CA = I[(k, CAname)]
            add(CA, prevCA, prevC, N, ("fix",), pi)
            if k <= n:
                C = I[(k, "C")]
                add(C, prevC, N, CA, ("phi", k), 0.0)
                # substituents on CA: offsets about the N-CA axis from three equilibrium angles
                tNC = self.a0[(N, CA, C)]
                CB, HA = I[(k, "CB")], I[(k, "HA")]
                dCB = self._offset(tNC, self.a0[(N, CA, CB)], self.a0[(C, CA, CB)])
                dHA = self._offset(tNC, self.a0[(N, CA, HA)], self.a0[(C, CA, HA)])
                # L-amino acid: CB at phi - dCB, HA at phi + dHA  (checked by chiral volume)
                add(CB, prevC, N, CA, ("phi", k), -dCB)
                add(HA, prevC, N, CA, ("phi", k), +dHA)
                self.dCB, self.dHA = dCB, dHA
                for name, ang in (("HB1", pi), ("HB2", pi / 3), ("HB3", -pi / 3)):
                    add(I[(k, name)], N, CA, CB, ("fix",), ang)
            else:
                for name, ang in (("HH31", pi), ("HH32", pi / 3), ("HH33", -pi / 3)):
                    add(I[(k, name)], prevC, N, CA, ("fix",), ang)
        self.Z = Z
        # ACE specials: O and methyl hydrogens, placed after the backbone start
        self.ace = (ace_ch3, ace_c, ace_o, I[(1, "N")], I[(1, "CA")],
                    [I[(0, "HH31")], I[(0, "HH32")], I[(0, "HH33")]])

    def _bond_graph(self):
        nat = self.natoms
        adj = [[] for _ in range(nat)]
        for b in self.top.bonds():
            adj[b[0].index].append(b[1].index)
            adj[b[1].index].append(b[0].index)
        # topological distance (number of bonds) by BFS
        D = np.full((nat, nat), 99, dtype=np.int16)
        for s in range(nat):
            D[s, s] = 0
            frontier = [s]
            d = 0
            while frontier:
                d += 1
                new = []
                for u in frontier:
                    for v in adj[u]:
                        if D[s, v] == 99:
                            D[s, v] = d
                            new.append(v)
                frontier = new
        self.topdist = D

    # ------------------------------------------------------------------ coordinates
    @staticmethod
    def _place(A, B, C, bond, angle, dih):
        """NeRF: positions of D with |CD| = bond, angle(B,C,D) = angle, dihedral(A,B,C,D) = dih.
        A, B, C: (M,3); dih: (M,) or scalar."""
        bc = C - B
        bc /= np.linalg.norm(bc, axis=1, keepdims=True)
        nrm = np.cross(B - A, bc)
        nrm /= np.linalg.norm(nrm, axis=1, keepdims=True)
        m = np.cross(nrm, bc)
        d2 = np.stack([-bond * np.cos(angle) * np.ones_like(dih),
                       bond * np.sin(angle) * np.cos(dih),
                       bond * np.sin(angle) * np.sin(dih)], axis=1)
        return C + d2[:, 0:1] * bc + d2[:, 1:2] * m + d2[:, 2:3] * nrm

    def coords(self, phi, psi):
        """phi, psi: arrays (M, n) in radians.  Returns positions (M, natoms, 3) in Angstrom."""
        phi = np.atleast_2d(np.asarray(phi, dtype=float))
        psi = np.atleast_2d(np.asarray(psi, dtype=float))
        M = phi.shape[0]
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
            else:
                dih = psi[:, kind[1] - 1] + const
            X[:, atom] = self._place(X[:, a], X[:, b], X[:, cc], bond, angle, dih)
        # ACE: O in the peptide plane, cis to CA1 about C-N (dihedral (CA1, N1, C, O) = 0);
        # methyl H: dihedral (N1, C, CH3, H) = 180, +60, -60
        ch3, c, o, n1, ca1, hs = self.ace
        X[:, o] = self._place(X[:, ca1], X[:, n1], X[:, c], self.r0[(c, o)], self.a0[(n1, c, o)],
                              np.zeros(M))
        for h, ang in zip(hs, (math.pi, math.pi / 3, -math.pi / 3)):
            X[:, h] = self._place(X[:, n1], X[:, c], X[:, ch3], self.r0[(ch3, h)],
                                  self.a0[(c, ch3, h)], np.full(M, ang))
        return X

    # ------------------------------------------------------------------ energies
    def _ctx(self, system):
        integ = openmm.VerletIntegrator(0.001)
        plat = openmm.Platform.getPlatformByName(self.platform)
        props = {"Threads": str(self.threads)} if self.platform == "CPU" else {}
        return openmm.Context(system, integ, plat, props), integ

    def _make_contexts(self, base, extra_ffs, solvent):
        """Master system (ff14SB): force groups
        0 bonds, 1 angles, 2 torsions (proper+improper), 3 nonbonded (LJ + Coulomb, incl. 1-4),
        4 LJ only (copy with charges zeroed), 5 GBn2 polar, 6 GBn2 polar + ACE surface term,
        7 OBC2 polar."""
        top = self.top
        master = base
        nb = None
        for f in master.getForces():
            if isinstance(f, openmm.HarmonicBondForce):
                f.setForceGroup(0)
            elif isinstance(f, openmm.HarmonicAngleForce):
                f.setForceGroup(1)
            elif isinstance(f, openmm.PeriodicTorsionForce):
                f.setForceGroup(2)
            elif isinstance(f, openmm.NonbondedForce):
                f.setForceGroup(3)
                nb = f
        self.charges = np.array([nb.getParticleParameters(i)[0].value_in_unit(unit.elementary_charge)
                                 for i in range(self.natoms)])
        sig = np.array([nb.getParticleParameters(i)[1].value_in_unit(unit.angstrom)
                        for i in range(self.natoms)])
        self.rmin_half = sig * 2 ** (1.0 / 6.0) / 2.0
        self.eps = np.array([nb.getParticleParameters(i)[2].value_in_unit(unit.kilocalorie_per_mole)
                             for i in range(self.natoms)])
        lj = copy.deepcopy(nb)
        for i in range(self.natoms):
            q, s, e = lj.getParticleParameters(i)
            lj.setParticleParameters(i, 0.0, s, e)
        for x in range(lj.getNumExceptions()):
            i, j, qq, s, e = lj.getExceptionParameters(x)
            lj.setExceptionParameters(x, i, j, 0.0, s, e)
        lj.setForceGroup(4)
        master.addForce(lj)
        self.group_names = {0: "bond", 1: "angle", 2: "tors", 3: "nb", 4: "lj"}
        if solvent:
            specs = [(5, "gbn2", ("amber14/protein.ff14SB.xml", "implicit/gbn2.xml"), None),
                     (6, "gbn2sa", ("amber14/protein.ff14SB.xml", "implicit/gbn2.xml"), "ACE"),
                     (7, "obc2", ("amber14/protein.ff14SB.xml", "implicit/obc2.xml"), None)]
            for g, name, xml, sa in specs:
                s = _system(xml, top, sasaMethod=sa)
                gb = [f for f in s.getForces() if isinstance(f, (openmm.CustomGBForce, openmm.GBSAOBCForce))]
                assert len(gb) == 1, [type(f) for f in s.getForces()]
                gbf = copy.deepcopy(gb[0])
                gbf.setForceGroup(g)
                master.addForce(gbf)
                self.group_names[g] = name
        self.master = master
        self.ctx, self._integ = self._ctx(master)
        self.extra = {}
        xmls = {"ff99SB": ("amber99sb.xml",), "ff19SB": ("amber19/protein.ff19SB.xml",),
                "ff03": ("amber03.xml",), "ff15ipq": ("amber14/protein.ff15ipq.xml",),
                "ff96": ("amber96.xml",), "ff99SBildn": ("amber99sbildn.xml",)}
        for name in extra_ffs:
            s = _system(xmls[name], top)
            for f in s.getForces():
                if isinstance(f, openmm.NonbondedForce):
                    f.setForceGroup(3)
                elif isinstance(f, openmm.PeriodicTorsionForce):
                    f.setForceGroup(2)
                elif isinstance(f, openmm.CMAPTorsionForce):
                    f.setForceGroup(4)
                else:
                    f.setForceGroup(0)
            self.extra[name] = self._ctx(s)

    def energies(self, X):
        """X: (M, natoms, 3) Angstrom.  Returns dict name -> (M,) array, kcal/mol.
        keys: bond, angle, tors, nb, lj, [gbn2, gbn2sa, obc2], and for each extra force field
        '<ff>' (total), '<ff>_tors' (periodic torsions), '<ff>_cmap', '<ff>_nb'."""
        M = X.shape[0]
        out = {v: np.empty(M) for v in self.group_names.values()}
        for name in self.extra:
            out[name] = np.empty(M)
            out[name + "_tors"] = np.empty(M)
            out[name + "_nb"] = np.empty(M)
            out[name + "_cmap"] = np.empty(M)
        Xnm = X * 0.1
        kj = unit.kilojoule_per_mole
        for m in range(M):
            p = Xnm[m]
            self.ctx.setPositions(p)
            for g, name in self.group_names.items():
                out[name][m] = self.ctx.getState(getEnergy=True, groups=1 << g).getPotentialEnergy().value_in_unit(kj)
            for name, (ctx, _) in self.extra.items():
                ctx.setPositions(p)
                out[name][m] = ctx.getState(getEnergy=True).getPotentialEnergy().value_in_unit(kj)
                out[name + "_tors"][m] = ctx.getState(getEnergy=True, groups=1 << 2).getPotentialEnergy().value_in_unit(kj)
                out[name + "_nb"][m] = ctx.getState(getEnergy=True, groups=1 << 3).getPotentialEnergy().value_in_unit(kj)
                out[name + "_cmap"][m] = ctx.getState(getEnergy=True, groups=1 << 4).getPotentialEnergy().value_in_unit(kj)
        for k in out:
            out[k] /= KCAL
        return out

    def cmap_energy(self, X, name="ff19SB"):
        """CMAP energy (kcal/mol) of the extra force field `name` from OpenMM."""
        ctx = self.extra[name][0]
        out = np.empty(X.shape[0])
        kj = unit.kilojoule_per_mole
        for m in range(X.shape[0]):
            ctx.setPositions(X[m] * 0.1)
            out[m] = ctx.getState(getEnergy=True, groups=1 << 4).getPotentialEnergy().value_in_unit(kj)
        return out / KCAL

    # ------------------------------------------------------------------ geometry diagnostics
    def clash_score(self, X, minsep=4):
        """min over atom pairs separated by >= minsep bonds of r_ij / (Rmin_i/2 + Rmin_j/2)
        (Amber ff14SB Lennard-Jones radii).  Returns (M,) array."""
        if not hasattr(self, "_clash_pairs") or self._clash_minsep != minsep:
            iu = np.triu_indices(self.natoms, 1)
            sel = self.topdist[iu] >= minsep
            self._clash_pairs = (iu[0][sel], iu[1][sel])
            self._clash_rsum = self.rmin_half[iu[0][sel]] + self.rmin_half[iu[1][sel]]
            self._clash_minsep = minsep
        i, j = self._clash_pairs
        out = np.empty(X.shape[0])
        step = 4096
        for s in range(0, X.shape[0], step):
            d = np.linalg.norm(X[s:s + step, i] - X[s:s + step, j], axis=2)
            out[s:s + step] = (d / self._clash_rsum).min(axis=1)
        return out


def dihedral(X, a, b, c, d):
    b0 = X[:, a] - X[:, b]
    b1 = X[:, c] - X[:, b]
    b2 = X[:, d] - X[:, c]
    b1n = b1 / np.linalg.norm(b1, axis=1, keepdims=True)
    v = b0 - (b0 * b1n).sum(1, keepdims=True) * b1n
    w = b2 - (b2 * b1n).sum(1, keepdims=True) * b1n
    x = (v * w).sum(1)
    y = (np.cross(b1n, v) * w).sum(1)
    return np.arctan2(y, x)
