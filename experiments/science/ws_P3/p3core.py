"""
Workstream P3 -- core: a table-based evaluator of the GBn2 (and OBC2) polarisation energy on a
fixed backbone with one rotamer variable per residue, written independently of P2's
`fbmodel.gb_energy` (P2's geometry builder `scbuild.SCPeptide` / `fbmodel.FBModel` is re-used for
coordinates, clash scores and the pair tables of the known part; nothing is written into ws_P2).

Mathematical object (what every certified statement of this workstream is about)
---------------------------------------------------------------------------------
Inputs, taken as exact real numbers: the double-precision Cartesian coordinates produced by
the builder for every (site, state) and for the fixed atoms; the per-particle parameters and
the neck tables read from OpenMM's CustomGBForce object (`charge, or, sr, alpha, beta, gamma,
radindex`, `getd0`, `getm0`), and the constants of OpenMM 8.6.1's expressions.  With r in nm:

  H(p <- q; r) = Ivdw + 0.826836 * Ineck
     Ivdw  = [r + sr_q - or_p >= 0] * 0.5*(1/L - 1/U + 0.25*(r - sr_q^2/r)*(1/U^2 - 1/L^2) + 0.5*ln(L/U)/r),
             U = r + sr_q,  L = max(or_p, |r - sr_q|)
     Ineck = [rad_p + rad_q + 0.68 - r >= 0] * m0(p,q) / (1 + 100 (r - d0(p,q))^2 + 0.3e6 (r - d0(p,q))^6),
             rad = or + 0.0195141                                    (GBn2 only; OBC2 has no neck)
  I_p = sum_{q != p} H(p <- q; r_pq)
  psi_p = I_p * or_p,   1/B_p = 1/or_p - tanh(alpha_p psi - beta_p psi^2 + gamma_p psi^3) / rad_p
  g = -KAPPA * [ (1/2) sum_p q_p^2 / B_p + sum_{p<q} q_p q_q / f(r_pq, B_p B_q) ],
      f(r, P) = sqrt(r^2 + P exp(-r^2/(4 P))),   KAPPA = 138.935485 * (1/eps_in - 1/eps_out) kJ nm/mol.

On a fixed backbone every atom belongs to at most one site, hence (P2, Statement 8)
  fixed atom p:          I_p(x) = I0_p + sum_i A_i^p(x_i)
  atom p of side chain i: I_p(x) = S_i^p(x_i) + sum_{j != i} T_ij^p(x_i, x_j).

Units: nm and kJ/mol inside (OpenMM's); energies returned in kcal/mol.
"""
import sys, os, math
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
P2DIR = os.path.normpath(os.path.join(HERE, "..", "ws_P2"))
PDIR = os.path.normpath(os.path.join(HERE, "..", "ws_P"))
for d in (P2DIR, PDIR):
    if d not in sys.path:
        sys.path.insert(0, d)
import numpy as np
import numexpr as ne
import openmm
from fbmodel import FBModel, BACKBONES          # P2's module (read-only)

KCAL = 4.184
KT300 = 0.0019872041 * 300.0                    # kcal/mol
BETA = 1.0 / KT300
COULOMB = 138.935485                            # the constant inside OpenMM's GB expressions
EPS_IN, EPS_OUT = 1.0, 78.5
KAPPA = COULOMB * (1.0 / EPS_IN - 1.0 / EPS_OUT)   # kJ nm / mol
NECK_SCALE, NECK_CUT = 0.826836, 0.68
OFFSET = {"gbn2": 0.0195141, "obc2": 0.009}


def expand_seq(s):
    import re
    m = re.fullmatch(r"([A-Z])(\d+)", s)
    if m:
        return m.group(1) * int(m.group(2))
    m = re.fullmatch(r"([A-Z]+):(\d+)", s)
    if m:
        pat, n = m.group(1), int(m.group(2))
        return (pat * (n // len(pat) + 1))[:n]
    return s


def read_gb_params(P, kind):
    """Per-particle parameters and neck tables straight from the OpenMM force object."""
    grp = {v: k for k, v in P.group_names.items()}[kind]
    force = [f for f in P.master.getForces() if f.getForceGroup() == grp][0]
    nat = P.natoms
    out = {}
    if isinstance(force, openmm.CustomGBForce):
        names = [force.getPerParticleParameterName(i) for i in range(force.getNumPerParticleParameters())]
        par = np.array([force.getParticleParameters(i) for i in range(nat)], dtype=float)
        for i, nm in enumerate(names):
            out[nm] = par[:, i].copy()
        exprs = " ".join(str(force.getComputedValueParameters(i)[1]) for i in range(force.getNumComputedValues()))
        exprs += " " + " ".join(str(force.getEnergyTermParameters(i)[0]) for i in range(force.getNumEnergyTerms()))
        out["exprs"] = exprs
        for t in range(force.getNumTabulatedFunctions()):
            fn = force.getTabulatedFunction(t)
            nx, ny, vals = fn.getFunctionParameters()
            out[force.getTabulatedFunctionName(t)] = np.array(vals, dtype=float).reshape(ny, nx).T   # [x, y]
    else:
        raise TypeError(f"unexpected force type {type(force)} for {kind}")
    return out


class GBModel:
    """Fixed-backbone rotamer model with table-based GBn2 / OBC2.

    dom: list over sites of state indices (into the R3 grid of that site) that form the domain;
    all tables are restricted to it and every `st` argument below indexes into the domain."""

    def __init__(self, seq, bb, dom=None, tau=None, kind="gbn2", grid="R3", platform="Reference", fb=None):
        self.seq = expand_seq(seq)
        self.bb = bb
        self.kind = kind
        self.fb = fb if fb is not None else FBModel(self.seq, bb, grid=grid, extra_ffs=(), platform=platform)
        fb = self.fb
        self.P = fb.P
        self.nat = fb.P.natoms
        self.ns = fb.ns
        if dom is None:
            dom = pruned_domain(fb, tau) if tau is not None else [np.arange(k) for k in fb.k]
        self.dom = [np.asarray(d, dtype=int) for d in dom]
        self.k = [len(d) for d in self.dom]
        self.fixed = fb.fixed
        self.mov = fb.mov
        self.nf = len(self.fixed)
        par = read_gb_params(fb.P, kind)
        self.par = par
        self.q = par["charge"]
        self.orr = par["or"]
        self.sr = par["sr"]
        self.off = OFFSET[kind]
        self.rad = self.orr + self.off
        ex = par["exprs"]
        if kind == "gbn2":
            assert "neckScale=0.826836" in ex and "neckCut=0.68" in ex and "offset=0.0195141" in ex, ex
            assert "tanh(alpha*psi-beta*psi^2+gamma*psi^3)" in ex
            self.al, self.be, self.ga = par["alpha"], par["beta"], par["gamma"]
            ri = par["radindex"].astype(int)
            assert np.all(ri == par["radindex"])
            self.d0 = par["getd0"][ri[:, None], ri[None, :]]
            self.m0 = par["getm0"][ri[:, None], ri[None, :]]
            self.cut = self.rad[:, None] + self.rad[None, :] + NECK_CUT
        else:
            assert "tanh(psi-0.8*psi^2+4.85*psi^3)" in ex and "offset=0.009" in ex, ex
            self.al = np.ones(self.nat); self.be = np.full(self.nat, 0.8); self.ga = np.full(self.nat, 4.85)
            self.d0 = self.m0 = self.cut = None
        assert "solventDielectric=78.5" in ex and "soluteDielectric=1;" in ex and "138.935485" in ex
        assert "f=sqrt(r^2+B1*B2*exp(-r^2/(4*B1*B2)))" in ex
        # coordinates in nm, restricted to the domain
        self.Xf = fb.X0[self.fixed] * 0.1                                   # (nf, 3)
        self.Xm = [fb.XYZ[i][self.dom[i]] * 0.1 for i in range(self.ns)]   # (k_i, n_i, 3)
        self._tables()

    # ------------------------------------------------------------------ descreening
    def _H(self, r, ip, iq):
        """descreening integral of atoms ip (rows) by atoms iq (columns) at distances r[..., ip, iq] (nm)."""
        or1 = self.orr[ip][:, None]
        sr2 = self.sr[iq][None, :]
        U = r + sr2
        D = np.abs(r - sr2)
        L = np.maximum(or1, D)
        vdw = 0.5 * (1.0 / L - 1.0 / U + 0.25 * (r - sr2 * sr2 / r) * (1.0 / (U * U) - 1.0 / (L * L)) + 0.5 * np.log(L / U) / r)
        out = np.where(r + sr2 - or1 >= 0.0, vdw, 0.0)
        if self.kind == "gbn2":
            sub = np.ix_(ip, iq)
            dr = r - self.d0[sub]
            neck = self.m0[sub] / (1.0 + 100.0 * dr * dr + 0.3e6 * dr ** 6)
            out = out + NECK_SCALE * np.where(self.cut[sub] - r >= 0.0, neck, 0.0)
        return out

    @staticmethod
    def _dist(XA, XB):
        d = XA[..., :, None, :] - XB[..., None, :, :]
        return np.sqrt((d * d).sum(-1))

    def _tables(self):
        f, mov = self.fixed, self.mov
        nf = self.nf
        r = self._dist(self.Xf, self.Xf) + np.eye(nf)
        self.I0 = (self._H(r, f, f) * (1.0 - np.eye(nf))).sum(-1)                       # (nf,)
        self.A, self.S, self.T = [], [], {}
        for i in range(self.ns):
            Xi = self.Xm[i]
            ni = len(mov[i])
            rfi = self._dist(self.Xf[None], Xi)                                         # (k_i, nf, n_i)
            self.A.append(self._H(rfi, f, mov[i]).sum(-1))                              # (k_i, nf): fixed <- side chain i
            rif = np.swapaxes(rfi, -1, -2)
            rii = self._dist(Xi, Xi) + np.eye(ni)
            self.S.append(self._H(rif, mov[i], f).sum(-1)
                          + (self._H(rii, mov[i], mov[i]) * (1.0 - np.eye(ni))).sum(-1))  # (k_i, n_i)
            for j in range(self.ns):
                if j != i:
                    rij = self._dist(Xi[:, None], self.Xm[j][None, :])                  # (k_i, k_j, n_i, n_j)
                    self.T[(i, j)] = self._H(rij, mov[i], mov[j]).sum(-1)               # (k_i, k_j, n_i)

    def descreening(self, st):
        """I_p (nm^-1) for all atoms at the states st (M, ns), by table look-up."""
        st = np.atleast_2d(st)
        M = st.shape[0]
        I = np.empty((M, self.nat))
        If = np.broadcast_to(self.I0, (M, self.nf)).copy()
        for i in range(self.ns):
            If += self.A[i][st[:, i]]
            Ii = self.S[i][st[:, i]].copy()
            for j in range(self.ns):
                if j != i:
                    Ii += self.T[(i, j)][st[:, i], st[:, j]]
            I[:, self.mov[i]] = Ii
        I[:, self.fixed] = If
        return I

    def invB(self, I):
        """1/B_p (nm^-1) from the descreening integrals I (M, nat)."""
        psi = I * self.orr[None]
        th = np.tanh(self.al[None] * psi - self.be[None] * psi ** 2 + self.ga[None] * psi ** 3)
        return 1.0 / self.orr[None] - th / self.rad[None]

    def coords(self, st):
        """coordinates (M, nat, 3) in nm."""
        st = np.atleast_2d(st)
        X = np.empty((st.shape[0], self.nat, 3))
        X[:, self.fixed] = self.Xf[None]
        for i in range(self.ns):
            X[:, self.mov[i]] = self.Xm[i][st[:, i]]
        return X

    # ------------------------------------------------------------------ energies
    def energy(self, st, parts=False, chunk=None, invB=None):
        """GB polarisation energy (kcal/mol) at the states st (M, ns).
        parts=True: (total, self part, cross part).  invB: (nat,) frozen inverse Born radii."""
        st = np.atleast_2d(st)
        M = st.shape[0]
        nat = self.nat
        if not hasattr(self, "_iu"):
            self._iu = np.triu_indices(nat, 1)
            self._qq = (self.q[self._iu[0]] * self.q[self._iu[1]])[None]
        iu0, iu1 = self._iu
        qq = self._qq
        if chunk is None:
            chunk = max(1, int(4e6 // max(len(iu0), 1)))
        eself = np.empty(M); ecross = np.empty(M)
        q2 = (self.q ** 2)[None]
        for s in range(0, M, chunk):
            sub = st[s:s + chunk]
            X = self.coords(sub)
            if invB is None:
                ib = self.invB(self.descreening(sub))
            else:
                ib = np.broadcast_to(invB, (sub.shape[0], nat))
            B = 1.0 / ib
            d = X[:, iu0] - X[:, iu1]
            r2 = (d * d).sum(-1)
            BB = B[:, iu0] * B[:, iu1]
            eself[s:s + chunk] = -0.5 * KAPPA * (q2 * ib).sum(1)
            ecross[s:s + chunk] = -KAPPA * ne.evaluate("sum(qq / sqrt(r2 + BB * exp(-r2 / (4.0 * BB))), axis=1)")
        if parts:
            return (eself + ecross) / KCAL, eself / KCAL, ecross / KCAL
        return (eself + ecross) / KCAL

    def bulk_energy(self, st):
        """Total GB energy (kcal/mol) for bulk evaluation.  GBn2: P2's block evaluator fbmodel.gb_energy (about
        five times faster than `energy` on 300 atoms; checked against `energy` and against OpenMM on fresh states
        in t01_validate.py, and re-checked on a subsample by every script that uses it).  OBC2: `energy`."""
        st = np.atleast_2d(st)
        if self.kind != "gbn2":
            return self.energy(st)
        raw = np.stack([self.dom[i][st[:, i]] for i in range(self.ns)], axis=1)
        return self.fb.gb_energy(raw)

    def energy_direct(self, st):
        """Reference implementation without tables: full distance matrix, descreening integrals summed
        over all ordered atom pairs.  Slow; used only to validate the tables."""
        st = np.atleast_2d(st)
        out = np.empty(st.shape[0])
        allat = np.arange(self.nat)
        eye = np.eye(self.nat)
        for m in range(st.shape[0]):
            X = self.coords(st[m:m + 1])[0]
            r = self._dist(X, X) + eye
            I = (self._H(r, allat, allat) * (1.0 - eye)).sum(-1)
            ib = self.invB(I[None])[0]
            B = 1.0 / ib
            r2 = (r - eye) ** 2
            BB = B[:, None] * B[None, :]
            f = np.sqrt(r2 + BB * np.exp(-r2 / (4.0 * BB)))
            qq = self.q[:, None] * self.q[None, :]
            # diagonal of qq/f is q^2/B: the double sum over all ordered pairs incl. the diagonal is
            # sum_p q_p^2/B_p + 2 sum_{p<q} q_p q_q / f
            out[m] = -0.5 * KAPPA * (qq / f).sum() / KCAL
        return out

    def openmm_energy(self, st):
        """OpenMM's own value (kcal/mol) for the same coordinates (platform chosen at construction)."""
        X = self.coords(st) * 10.0
        return self.P.energies(X)[self.kind]

    def product_states(self):
        grids = np.meshgrid(*[np.arange(k) for k in self.k], indexing="ij")
        return np.stack([g.reshape(-1) for g in grids], axis=1)


def pruned_domain(fb, tau):
    """P2's product domain X' (an_main.pruned_product), recomputed from the clash tables of an
    FBModel without enumeration data: states with one-site score > tau; then repeatedly remove the
    (site, state) taking part in the largest number of two-site clashes (score <= tau) with
    still-present states of other sites (ties: lower one-site score, then lower site, then lower
    position) until no clash is left.  Returns the list over sites of kept state indices."""
    n = fb.ns
    dom = [np.flatnonzero(s > tau) for s in fb.s1]
    s1 = [fb.s1[i][dom[i]] for i in range(n)]
    bad = {}
    for (i, j), tab in fb.s2.items():
        b = tab[np.ix_(dom[i], dom[j])] <= tau
        if b.any():
            bad[(i, j)] = b
    keep = [np.ones(len(dom[i]), dtype=bool) for i in range(n)]
    while True:
        deg = [np.zeros(len(dom[i])) for i in range(n)]
        for (i, j), b in bad.items():
            bb_ = b & keep[i][:, None] & keep[j][None, :]
            deg[i] += bb_.sum(1); deg[j] += bb_.sum(0)
        best = None
        for i in range(n):
            for s in np.flatnonzero(deg[i] > 0):
                key = (-deg[i][s], s1[i][s], i, s)
                if best is None or key < best:
                    best = key
        if best is None:
            break
        keep[best[2]][best[3]] = False
    return [dom[i][keep[i]] for i in range(n)]
