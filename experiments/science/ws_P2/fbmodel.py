"""
Workstream P2 -- fixed-backbone rotamer model of Ace-X_1..X_n-NMe.

Site variables: one site per residue that has side-chain dihedrals; the state of a site is the
tuple of ALL its chi angles (a "rotamer").  On a fixed backbone every atom depends on at most
one site (scbuild.SCPeptide.site_of_atom), so

  * the clash score of P decomposes into a minimum over fixed, one-site and two-site tables;
  * every pair-additive energy (ff14SB vacuum energy, any other fixed-charge force field at the
    same coordinates) is EXACTLY  c0 + sum_i h_i(x_i) + sum_{i<j} J_ij(x_i, x_j); the tables are
    computed here by direct summation of atom-pair terms with the parameters that P's FastFF
    read from the OpenMM System objects, and are checked against FastFF on full conformations;
  * the GBn2 polarisation energy is NOT pairwise in the sites, but its descreening integrals
    I_p = sum_q H(r_pq) are pair sums and are tabulated, so that the energy of an assignment costs
    one pair sum with the exact Born radii.  This is a second implementation of exactly OpenMM's
    GBSAGBn2Force expressions (same formulas as ws_P/fastff.py) and is validated against FastFF
    and OpenMM (test_fbmodel.py).

Units: Angstrom, kcal/mol outside; nm, kJ/mol inside the energy formulas (OpenMM's).
"""
import sys, os, math, itertools
sys.dont_write_bytecode = True
import numpy as np
import numexpr as ne
from scbuild import SCPeptide, NCHI, KT300, KCAL          # also puts ../ws_P on sys.path
from fastff import FastFF, ONE_4PI_EPS0, ONE_4PI_EPS0_NB  # noqa: E402  (P's module, unmodified)

BACKBONES = {            # uniform (phi, psi) in degrees; fixed in NOTES.md before any measurement
    "H": (-57.0, -47.0), "E": (-139.0, 135.0), "P2": (-75.0, 145.0),
    "Hp": (-70.0, -40.0), "Ep": (-150.0, 150.0), "P2p": (-70.0, 150.0),      # P's grid basins
}
STAG = (-60.0, 180.0, 60.0)


def grid_states(resname, grid):
    """list of chi tuples (degrees) for one site."""
    nchi = NCHI[resname]
    if grid == "R3":
        return list(itertools.product(STAG, repeat=nchi))
    if grid == "R2":
        return [(c1,) + (180.0,) * (nchi - 1) for c1 in (-60.0, 180.0)]
    if grid == "R3c":             # chi1, chi2 staggered, further chi trans
        return [c + (180.0,) * (nchi - min(nchi, 2)) for c in itertools.product(STAG, repeat=min(nchi, 2))]
    raise ValueError(grid)


class FBModel:
    def __init__(self, seq, bb, grid="R3", extra_ffs=("ff03",), platform="CPU", threads=1):
        self.P = P = SCPeptide(seq, extra_ffs=extra_ffs, platform=platform)
        self.F = F = FastFF(P, threads=threads)
        F._prepare()
        self.n = n = P.n
        self.bbname = bb if isinstance(bb, str) else None
        bbv = BACKBONES[bb] if isinstance(bb, str) else bb
        self.phi = np.full((1, n), math.radians(bbv[0]))
        self.psi = np.full((1, n), math.radians(bbv[1]))
        self.grid = grid
        self.sites = [k for k in range(1, n + 1) if NCHI[P.seq[k - 1]] > 0]       # residue numbers
        self.ns = len(self.sites)
        self.states = [grid_states(P.seq[k - 1], grid) for k in self.sites]
        self.k = [len(s) for s in self.states]
        self.fixed = np.flatnonzero(P.site_of_atom == 0)
        self.mov = [np.flatnonzero(P.site_of_atom == k) for k in self.sites]
        self._coords()
        self._clash_tables()
        self.tables = {}

    # ------------------------------------------------------------------ coordinates
    def _chi_rows(self, i, base):
        """chi array (k_i, nchi) with site i running over its states, the rest as in `base`."""
        P = self.P
        k = self.sites[i]
        chi = np.repeat(base, self.k[i], axis=0)
        st = np.deg2rad(np.array(self.states[i], dtype=float)).reshape(self.k[i], -1)
        for j in range(NCHI[P.seq[k - 1]]):
            chi[:, P.chi_col[(k, j)]] = st[:, j]
        return chi

    def chi_of(self, st):
        """state indices (M, ns) -> chi array (M, nchi) in radians."""
        P = self.P
        st = np.atleast_2d(st)
        chi = np.zeros((st.shape[0], max(P.nchi, 1)))
        for i, k in enumerate(self.sites):
            vals = np.deg2rad(np.array(self.states[i], dtype=float)).reshape(self.k[i], -1)
            for j in range(NCHI[P.seq[k - 1]]):
                chi[:, P.chi_col[(k, j)]] = vals[st[:, i], j]
        return chi

    def _coords(self):
        P = self.P
        base = self.chi_of(np.zeros((1, self.ns), dtype=int))
        self.X0 = P.coords(self.phi, self.psi, base)[0]
        self.XYZ = []
        for i in range(self.ns):
            ki = self.k[i]
            X = P.coords(np.repeat(self.phi, ki, 0), np.repeat(self.psi, ki, 0), self._chi_rows(i, base))
            other = np.setdiff1d(np.arange(P.natoms), self.mov[i])
            assert np.abs(X[:, other] - self.X0[other][None]).max() < 1e-10, "an atom depends on two sites"
            self.XYZ.append(X[:, self.mov[i]].copy())

    def assemble(self, st):
        """state indices (M, ns) -> coordinates (M, natoms, 3) in Angstrom."""
        st = np.atleast_2d(st)
        X = np.broadcast_to(self.X0, (st.shape[0],) + self.X0.shape).copy()
        for i in range(self.ns):
            X[:, self.mov[i]] = self.XYZ[i][st[:, i]]
        return X

    # ------------------------------------------------------------------ clash tables
    def _clash_tables(self):
        P = self.P
        R, td = P.rmin_half, P.topdist

        def score(XA, ia, XB, ib):
            d = np.sqrt(((XA[..., :, None, :] - XB[..., None, :, :]) ** 2).sum(-1))
            rs = R[ia][:, None] + R[ib][None, :]
            ok = (td[np.ix_(ia, ib)] >= 4) & (rs > 0)
            with np.errstate(divide="ignore", invalid="ignore"):
                ratio = np.where(ok, d / np.where(rs > 0, rs, 1.0), np.inf)
            return ratio.min(axis=(-1, -2))

        Xf = self.X0[self.fixed]
        self.s_fixed = float(score(Xf, self.fixed, Xf, self.fixed))
        self.s1 = []
        for i in range(self.ns):
            a = score(self.XYZ[i], self.mov[i], Xf[None], self.fixed)
            b = score(self.XYZ[i], self.mov[i], self.XYZ[i], self.mov[i])
            self.s1.append(np.minimum(a, b))
        self.s2 = {}
        for i in range(self.ns):
            for j in range(i + 1, self.ns):
                self.s2[(i, j)] = score(self.XYZ[i][:, None], self.mov[i], self.XYZ[j][None, :], self.mov[j])

    def clash_of(self, st):
        st = np.atleast_2d(st)
        s = np.full(st.shape[0], self.s_fixed)
        for i in range(self.ns):
            s = np.minimum(s, self.s1[i][st[:, i]])
        for (i, j), tab in self.s2.items():
            s = np.minimum(s, tab[st[:, i], st[:, j]])
        return s

    def pair_clash_of(self, st):
        """min over i<j of the two-site scores only."""
        st = np.atleast_2d(st)
        s = np.full(st.shape[0], np.inf)
        for (i, j), tab in self.s2.items():
            s = np.minimum(s, tab[st[:, i], st[:, j]])
        return s

    # ------------------------------------------------------------------ pair-additive energies
    def _nb_matrices(self, name):
        nbp = self.F.ff[name]["nb"]
        nat = self.P.natoms
        iu = self.F.iu
        out = []
        for v in (ONE_4PI_EPS0_NB * nbp["qq"], nbp["e4"] * nbp["s6"] ** 2, nbp["e4"] * nbp["s6"]):
            Mx = np.zeros((nat, nat))
            Mx[iu] = v
            out.append(Mx + Mx.T)
        return out

    def pair_tables(self, name="ff14SB"):
        """Exact one-site and two-site tables of the vacuum energy of force field `name`
        (components: coul, lj, tors), kcal/mol:
            E(x) = c0 + sum_i h[i][x_i] + sum_{i<j} J[(i,j)][x_i, x_j]   for each component."""
        if name in self.tables:
            return self.tables[name]
        QQ, A12, A6 = self._nb_matrices(name)

        def block(XA, ia, XB, ib, same=False):
            r2 = ((XA[..., :, None, :] - XB[..., None, :, :]) ** 2).sum(-1) * 0.01      # nm^2
            w = 1.0
            if same:
                w = np.triu(np.ones((len(ia), len(ib))), 1)
                r2 = r2 + np.eye(len(ia))
            inv2 = 1.0 / r2
            inv6 = inv2 * inv2 * inv2
            sub = np.ix_(ia, ib)
            coul = (w * QQ[sub] * np.sqrt(inv2)).sum(axis=(-1, -2))
            lj = (w * (A12[sub] * inv6 * inv6 - A6[sub] * inv6)).sum(axis=(-1, -2))
            return coul / KCAL, lj / KCAL

        Xf = self.X0[self.fixed]
        c0 = {}
        c0["coul"], c0["lj"] = [float(v) for v in block(Xf, self.fixed, Xf, self.fixed, same=True)]
        h = {"coul": [], "lj": [], "tors": []}
        J = {"coul": {}, "lj": {}}
        for i in range(self.ns):
            a = block(self.XYZ[i], self.mov[i], Xf[None], self.fixed)
            b = block(self.XYZ[i], self.mov[i], self.XYZ[i], self.mov[i], same=True)
            h["coul"].append(a[0] + b[0])
            h["lj"].append(a[1] + b[1])
            for j in range(i + 1, self.ns):
                cj = block(self.XYZ[i][:, None], self.mov[i], self.XYZ[j][None, :], self.mov[j])
                J["coul"][(i, j)], J["lj"][(i, j)] = cj
        # torsions: every torsion term involves atoms of at most one site (asserted)
        t = self.F.ff[name]["tors"]
        tsite = self.P.site_of_atom[t["idx"]]
        nsite = np.array([len(set(row[row > 0])) for row in tsite])
        assert nsite.max() <= 1, "a torsion term couples two sites"
        owner = tsite.max(axis=1)

        def tors_energy(X, sel):
            if not sel.any():
                return np.zeros(X.shape[0])
            th = FastFF._dihedrals(X * 0.1, t["idx"][sel])
            return (t["k"][sel][None] * (1.0 + np.cos(t["per"][sel][None] * th - t["phase"][sel][None]))).sum(1) / KCAL

        c0["tors"] = float(tors_energy(self.X0[None], owner == 0)[0])
        for i, k in enumerate(self.sites):
            st = np.zeros((self.k[i], self.ns), dtype=int)
            st[:, i] = np.arange(self.k[i])
            h["tors"].append(tors_energy(self.assemble(st), owner == k))
        self.tables[name] = dict(c0=c0, h=h, J=J)
        return self.tables[name]

    def table_energy(self, st, name="ff14SB", comps=("tors", "lj", "coul")):
        """sum of the requested components at the states st (M, ns)."""
        T = self.pair_tables(name)
        st = np.atleast_2d(st)
        e = np.zeros(st.shape[0])
        for c in comps:
            e += T["c0"][c]
            for i in range(self.ns):
                e += T["h"][c][i][st[:, i]]
            if c in T["J"]:
                for (i, j), tab in T["J"][c].items():
                    e += tab[st[:, i], st[:, j]]
        return e

    def site_tables(self, name="ff14SB", comps=("tors", "lj", "coul")):
        """(c0, [h_i], {(i,j): J_ij}) summed over the components."""
        T = self.pair_tables(name)
        c0 = sum(T["c0"][c] for c in comps)
        h = [sum(T["h"][c][i] for c in comps) for i in range(self.ns)]
        J = {key: sum(T["J"][c][key] for c in comps if c in T["J"]) for key in T["J"]["coul"]}
        return c0, h, J

    # ------------------------------------------------------------------ GBn2
    def _gb_tables(self):
        if hasattr(self, "gbT"):
            return self.gbT
        g = self.F.gb["gbn2"]
        orr, sr = g["or"], g["sr"]
        d0, m0, cut = g["_d0"][0], g["_m0"][0], g["_cut"][0]

        def H(XA, ia, XB, ib, same=False):
            """descreening integral of the atoms ia (at XA) by the atoms ib (at XB), summed over ib."""
            r = np.sqrt(((XA[..., :, None, :] - XB[..., None, :, :]) ** 2).sum(-1)) * 0.1      # nm
            if same:
                r = r + np.eye(len(ia))
            or1 = orr[ia][:, None]
            sr2 = sr[ib][None, :]
            sub = np.ix_(ia, ib)
            U = r + sr2
            L = np.maximum(or1, np.abs(r - sr2))
            t1 = np.where(r + sr2 - or1 >= 0.0,
                          0.5 * (1.0 / L - 1.0 / U + 0.25 * (r - sr2 * sr2 / r) * (1.0 / (U * U) - 1.0 / (L * L))
                                 + 0.5 * np.log(L / U) / r), 0.0)
            t2 = np.where(cut[sub] - r >= 0.0,
                          0.826836 * m0[sub] / (1.0 + 100.0 * (r - d0[sub]) ** 2 + 0.3e6 * (r - d0[sub]) ** 6), 0.0)
            tot = t1 + t2
            if same:
                tot = tot * (1.0 - np.eye(len(ia)))
            return tot.sum(-1)

        Xf = self.X0[self.fixed]
        T = dict(I0=H(Xf, self.fixed, Xf, self.fixed, same=True), A=[], S=[], T={})
        for i in range(self.ns):
            T["A"].append(H(Xf[None], self.fixed, self.XYZ[i], self.mov[i]))
            T["S"].append(H(self.XYZ[i], self.mov[i], Xf[None], self.fixed)
                          + H(self.XYZ[i], self.mov[i], self.XYZ[i], self.mov[i], same=True))
            for j in range(self.ns):
                if j != i:
                    T["T"][(i, j)] = H(self.XYZ[i][:, None], self.mov[i], self.XYZ[j][None, :], self.mov[j])
        self.gbT = T
        iu = self.F.iu
        self._qq = (g["charge"][iu[0]] * g["charge"][iu[1]])[None]
        return T

    def born_radii(self, st):
        """exact GBn2 effective Born radii (nm) of all atoms at the states st (M, ns)."""
        T = self._gb_tables()
        g = self.F.gb["gbn2"]
        st = np.atleast_2d(st)
        I = np.empty((st.shape[0], self.P.natoms))
        If = np.broadcast_to(T["I0"], (st.shape[0], len(self.fixed))).copy()
        for i in range(self.ns):
            If += T["A"][i][st[:, i]]
            Ii = T["S"][i][st[:, i]].copy()
            for j in range(self.ns):
                if j != i:
                    Ii += T["T"][(i, j)][st[:, i], st[:, j]]
            I[:, self.mov[i]] = Ii
        I[:, self.fixed] = If
        orr = g["or"][None]
        psi = I * orr
        rad = orr + 0.0195141
        th = np.tanh(g["alpha"][None] * psi - g["beta"][None] * psi ** 2 + g["gamma"][None] * psi ** 3)
        return 1.0 / (1.0 / orr - th / rad)

    def gb_energy(self, st, chunk=512, parts=False):
        """GBn2 polarisation energy (kcal/mol) at the states st (M, ns).  parts=True returns
        (total, self-energy part, cross part)."""
        self._gb_tables()
        g = self.F.gb["gbn2"]
        st = np.atleast_2d(st)
        M = st.shape[0]
        q2 = (g["charge"] ** 2)[None]
        pref = ONE_4PI_EPS0 * (1.0 / self.F.eps_in - 1.0 / self.F.eps_out)
        i, j = self.F.iu
        qq = self._qq
        e_self = np.empty(M)
        e_pair = np.empty(M)
        for s in range(0, M, chunk):
            sub = st[s:s + chunk]
            B = self.born_radii(sub)
            X = self.assemble(sub) * 0.1
            r2 = np.zeros((sub.shape[0], len(i)))
            for ax in range(3):
                xa = X[:, :, ax]
                dlt = xa[:, i] - xa[:, j]
                r2 += dlt * dlt
            BB = B[:, i] * B[:, j]
            e_self[s:s + chunk] = -0.5 * pref * (q2 / B).sum(1)
            e_pair[s:s + chunk] = -pref * ne.evaluate("sum(qq / sqrt(r2 + BB * exp(-r2 / (4.0 * BB))), axis=1)")
        if parts:
            return (e_self + e_pair) / KCAL, e_self / KCAL, e_pair / KCAL
        return (e_self + e_pair) / KCAL

    # ------------------------------------------------------------------ domains and enumeration
    def domain(self, tau=0.70):
        """list over sites of the state indices with one-site clash score > tau."""
        return [np.flatnonzero(s > tau) for s in self.s1]

    def product_states(self, dom):
        """all assignments of the product of the per-site state lists `dom`, C order, as (M, ns) ints."""
        grids = np.meshgrid(*dom, indexing="ij")
        return np.stack([gx.reshape(-1) for gx in grids], axis=1)
