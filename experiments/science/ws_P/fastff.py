"""
Vectorised numpy evaluator of exactly the energy terms that OpenMM computes for the
systems of pepbuild.Peptide.  All parameters (charges, Lennard-Jones, exceptions, torsions,
GB per-particle parameters and the GBn2 neck tables) are read from the OpenMM System
objects; nothing is re-typed.  Functional forms: OpenMM NonbondedForce (NoCutoff),
PeriodicTorsionForce, and openmm.app.internal.customgbforces.GBSAGBn2Force / GBSAOBC2Force
(Amber igb=8 / igb=5).  validate_fast.py compares every component with OpenMM's Reference
(double precision) platform.

Units inside: nm, kJ/mol (OpenMM's).  Returned energies: kcal/mol.  Input coordinates:
Angstrom.
"""
import math
import numpy as np
import numexpr as ne
import openmm
import openmm.unit as unit

KCAL = 4.184
ONE_4PI_EPS0 = 138.935485      # kJ nm / (mol e^2), the constant used inside OpenMM's GB code
ONE_4PI_EPS0_NB = 138.93545764438198   # constant used by NonbondedForce (OpenMM SimTKOpenMMRealType.h)


def _nb_params(nb, nat):
    q = np.zeros(nat); sig = np.zeros(nat); eps = np.zeros(nat)
    for i in range(nat):
        a, b, c = nb.getParticleParameters(i)
        q[i] = a.value_in_unit(unit.elementary_charge)
        sig[i] = b.value_in_unit(unit.nanometer)
        eps[i] = c.value_in_unit(unit.kilojoule_per_mole)
    QQ = np.outer(q, q)
    SIG = 0.5 * (sig[:, None] + sig[None, :])
    EPS = np.sqrt(eps[:, None] * eps[None, :])
    for x in range(nb.getNumExceptions()):
        i, j, qq, s, e = nb.getExceptionParameters(x)
        qq = qq.value_in_unit(unit.elementary_charge ** 2)
        s = s.value_in_unit(unit.nanometer); e = e.value_in_unit(unit.kilojoule_per_mole)
        QQ[i, j] = QQ[j, i] = qq
        SIG[i, j] = SIG[j, i] = s
        EPS[i, j] = EPS[j, i] = e
    iu = np.triu_indices(nat, 1)
    return dict(q=q, sig=sig, eps=eps, qq=QQ[iu], s6=SIG[iu] ** 6, e4=4.0 * EPS[iu])


def _torsions(system):
    out = []
    for f in system.getForces():
        if isinstance(f, openmm.PeriodicTorsionForce):
            for t in range(f.getNumTorsions()):
                i, j, k, l, per, ph, kk = f.getTorsionParameters(t)
                out.append((i, j, k, l, per, ph.value_in_unit(unit.radian),
                            kk.value_in_unit(unit.kilojoule_per_mole)))
    arr = np.array(out, dtype=float)
    return dict(idx=arr[:, :4].astype(int), per=arr[:, 4], phase=arr[:, 5], k=arr[:, 6])


def _gb_params(gbf, nat):
    names = [gbf.getPerParticleParameterName(i) for i in range(gbf.getNumPerParticleParameters())]
    P = np.array([gbf.getParticleParameters(i) for i in range(nat)], dtype=float)
    d = {n: P[:, i] for i, n in enumerate(names)}
    tabs = {}
    for t in range(gbf.getNumTabulatedFunctions()):
        fn = gbf.getTabulatedFunction(t)
        nx, ny, vals = fn.getFunctionParameters()
        tabs[gbf.getTabulatedFunctionName(t)] = np.array(vals).reshape(ny, nx).T   # [x, y]
    d["tabs"] = tabs
    d["exprs"] = [gbf.getComputedValueParameters(i) for i in range(gbf.getNumComputedValues())] + \
                 [gbf.getEnergyTermParameters(i) for i in range(gbf.getNumEnergyTerms())]
    return d


class FastFF:
    def __init__(self, P, threads=2):
        ne.set_num_threads(threads)
        self.P = P
        nat = P.natoms
        self.nat = nat
        self.iu = np.triu_indices(nat, 1)
        self.ff = {}
        nbs = [f for f in P.master.getForces() if isinstance(f, openmm.NonbondedForce)]
        self.ff["ff14SB"] = dict(nb=_nb_params(nbs[0], nat), tors=_torsions(P.master))
        self.gb = {}
        for f in P.master.getForces():
            if isinstance(f, openmm.CustomGBForce):
                self.gb[P.group_names[f.getForceGroup()]] = _gb_params(f, nat)
        self.cmap = {}
        for name, (ctx, _) in P.extra.items():
            s = ctx.getSystem()
            nb = [f for f in s.getForces() if isinstance(f, openmm.NonbondedForce)][0]
            self.ff[name] = dict(nb=_nb_params(nb, nat), tors=_torsions(s))
            cm = [f for f in s.getForces() if isinstance(f, openmm.CMAPTorsionForce)]
            if cm:
                self.cmap[name] = cm[0]
        self.eps_in, self.eps_out = 1.0, 78.5
        # sanity: the expressions hard-coded below are the ones in the OpenMM objects
        if "gbn2" in self.gb:
            ex = " ".join(str(v) for e in self.gb["gbn2"]["exprs"] for v in e)
            assert "neckScale=0.826836" in ex and "neckCut=0.68" in ex and "offset=0.0195141" in ex
            assert "solventDielectric=78.5" in ex and "soluteDielectric=1" in ex
        if "obc2" in self.gb:
            ex = " ".join(str(v) for e in self.gb["obc2"]["exprs"] for v in e)
            assert "tanh(psi-0.8*psi^2+4.85*psi^3)" in ex and "offset=0.009" in ex

    # ------------------------------------------------------------------
    @staticmethod
    def _dihedrals(X, idx):
        a, b, c, d = idx[:, 0], idx[:, 1], idx[:, 2], idx[:, 3]
        b0 = X[:, a] - X[:, b]
        b1 = X[:, c] - X[:, b]
        b2 = X[:, d] - X[:, c]
        b1n = b1 / np.linalg.norm(b1, axis=2, keepdims=True)
        v = b0 - (b0 * b1n).sum(2, keepdims=True) * b1n
        w = b2 - (b2 * b1n).sum(2, keepdims=True) * b1n
        x = (v * w).sum(2)
        y = (np.cross(b1n, v) * w).sum(2)
        return np.arctan2(y, x)

    def _born(self, r, g, kind):
        """r: (M, nat, nat) distances in nm with the diagonal set to a dummy value.
        Returns Born radii (M, nat) in nm and the radii or+offset."""
        orr = g["or"]; sr = g["sr"]
        or1 = orr[None, :, None]
        sr2 = sr[None, None, :]
        off = self._offdiag
        U = ne.evaluate("r + sr2")
        L = ne.evaluate("where(or1 > abs(r - sr2), or1, abs(r - sr2))")
        if kind == "gbn2":
            offset = 0.0195141
            d0, m0, cut = g["_d0"], g["_m0"], g["_cut"]
            I = ne.evaluate("off * (where(r + sr2 - or1 >= 0.0, 0.5*(1.0/L - 1.0/U + 0.25*(r - sr2*sr2/r)*(1.0/(U*U) - 1.0/(L*L)) + 0.5*log(L/U)/r), 0.0)"
                            " + where(cut - r >= 0.0, 0.826836*m0/(1.0 + 100.0*(r-d0)**2 + 0.3e6*(r-d0)**6), 0.0))").sum(axis=2)
        else:
            offset = 0.009
            I = ne.evaluate("off * where(r + sr2 - or1 >= 0.0, 0.5*(1.0/L - 1.0/U + 0.25*(r - sr2*sr2/r)*(1.0/(U*U) - 1.0/(L*L)) + 0.5*log(L/U)/r), 0.0)").sum(axis=2)
        psi = I * orr[None]
        rad = (orr + offset)[None]
        if kind == "gbn2":
            th = np.tanh(g["alpha"][None] * psi - g["beta"][None] * psi ** 2 + g["gamma"][None] * psi ** 3)
        else:
            th = np.tanh(psi - 0.8 * psi ** 2 + 4.85 * psi ** 3)
        B = 1.0 / (1.0 / orr[None] - th / rad)
        return B, rad

    def _gb_energy(self, r, r2u, g, kind, want_born=False):
        B, rad = self._born(r, g, kind)
        q = g["charge"]
        pref = ONE_4PI_EPS0 * (1.0 / self.eps_in - 1.0 / self.eps_out)
        e_self = -0.5 * pref * (q[None] ** 2 / B).sum(1)
        i, j = self.iu
        BB = B[:, i] * B[:, j]
        qq = (q[i] * q[j])[None]
        e_pair = -pref * ne.evaluate("qq / sqrt(r2u + BB * exp(-r2u / (4.0 * BB)))").sum(axis=1)
        rb = rad / B
        e_sa = (28.3919551 * (rad + 0.14) ** 2 * (rb * rb * rb) ** 2).sum(1)
        if want_born:
            return e_self + e_pair, e_sa, B
        return e_self + e_pair, e_sa

    def _prepare(self):
        nat = self.nat
        self._offdiag = (1.0 - np.eye(nat))[None]
        if "gbn2" in self.gb:
            g = self.gb["gbn2"]
            ri = g["radindex"].astype(int)
            g["_d0"] = g["tabs"]["getd0"][ri[:, None], ri[None, :]][None]
            g["_m0"] = g["tabs"]["getm0"][ri[:, None], ri[None, :]][None]
            rad = g["or"] + 0.0195141
            g["_cut"] = (rad[:, None] + rad[None, :] + 0.68)[None]
        # unique torsion quadruples over all force fields
        quads = {}
        for k, p in self.ff.items():
            t = p["tors"]
            pos = np.empty(len(t["idx"]), dtype=int)
            for m, q in enumerate(map(tuple, t["idx"])):
                pos[m] = quads.setdefault(q, len(quads))
            t["upos"] = pos
        self._quads = np.array(list(quads.keys()), dtype=int)
        self._prepared = True

    def energies(self, X, chunk=256, extra=True, born=False, gb=("gbn2", "obc2"), clash=True):
        """X: (M, nat, 3) in Angstrom.  Returns dict of (M,) arrays in kcal/mol:
        tors, lj, coul (ff14SB); gbn2, sa (ACE term with GBn2 radii), obc2;
        <ff>_tors, <ff>_lj, <ff>_coul for the extra force fields (CMAP not included, see
        pepbuild.Peptide.cmap_energy).  born=True adds 'born' (M, nat) GBn2 Born radii in A."""
        if not getattr(self, "_prepared", False):
            self._prepare()
        M = X.shape[0]
        names = ["tors", "lj", "coul"]
        do_gbn2 = "gbn2" in self.gb and "gbn2" in gb
        do_obc2 = "obc2" in self.gb and "obc2" in gb
        if do_gbn2:
            names += ["gbn2", "sa"]
        if do_obc2:
            names += ["obc2"]
        if clash:
            names += ["clash"]
            sel = self.P.topdist[self.iu] >= 4
            rs = self.P.rmin_half[self.iu[0]] + self.P.rmin_half[self.iu[1]]
            cw = np.where(sel, 100.0 / rs ** 2, 1e30)[None]      # nm^-2 -> ratio^2 (r in nm, rs in A)
        if extra is True:
            ffs = ["ff14SB"] + [k for k in self.ff if k != "ff14SB"]
        elif extra:
            ffs = ["ff14SB"] + list(extra)
        else:
            ffs = ["ff14SB"]
        for k in ffs[1:]:
            names += [k + "_tors", k + "_lj", k + "_coul"]
        out = {k: np.empty(M) for k in names}
        if born:
            out["born"] = np.empty((M, self.nat))
        i, j = self.iu
        eye = np.eye(self.nat)[None]
        for s in range(0, M, chunk):
            x = X[s:s + chunk] * 0.1
            sl = slice(s, s + x.shape[0])
            xa = x[:, :, None, 0]; xb = x[:, None, :, 0]
            ya = x[:, :, None, 1]; yb = x[:, None, :, 1]
            za = x[:, :, None, 2]; zb = x[:, None, :, 2]
            r2 = ne.evaluate("(xa-xb)**2 + (ya-yb)**2 + (za-zb)**2")
            r2u = r2[:, i, j]
            inv2 = 1.0 / r2u
            inv1 = np.sqrt(inv2)
            inv6 = inv2 * inv2 * inv2
            inv12 = inv6 * inv6
            if clash:
                out["clash"][sl] = np.sqrt((r2u * cw).min(axis=1))
            th = self._dihedrals(x, self._quads)
            for k in ffs:
                p = self.ff[k]
                pre = "" if k == "ff14SB" else k + "_"
                nbp = p["nb"]
                out[pre + "coul"][sl] = ONE_4PI_EPS0_NB * (inv1 @ nbp["qq"])
                out[pre + "lj"][sl] = inv12 @ (nbp["e4"] * nbp["s6"] ** 2) - inv6 @ (nbp["e4"] * nbp["s6"])
                t = p["tors"]
                tt = th[:, t["upos"]]
                out[pre + "tors"][sl] = (t["k"][None] * (1.0 + np.cos(t["per"][None] * tt - t["phase"][None]))).sum(1)
            if do_gbn2 or do_obc2:
                r = ne.evaluate("sqrt(r2 + eye)")      # dummy 1 on the diagonal
                if do_gbn2:
                    res = self._gb_energy(r, r2u, self.gb["gbn2"], "gbn2", want_born=born)
                    out["gbn2"][sl], out["sa"][sl] = res[0], res[1]
                    if born:
                        out["born"][sl] = res[2] * 10.0
                if do_obc2:
                    out["obc2"][sl], _ = self._gb_energy(r, r2u, self.gb["obc2"], "obc2")
        for k in out:
            if k not in ("born", "clash"):
                out[k] /= KCAL
        return out
