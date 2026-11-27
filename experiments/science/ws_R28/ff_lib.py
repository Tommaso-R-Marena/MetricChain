"""R28 — my own reductions of a two-torsion energy grid (written from the text of items 100–101 and
from Proposition A17.24; n = 2 sites only, explicit code, no general-n machinery).

E[i, j] : energy in kT on an N x N periodic grid (torsion 1 = axis 0), zero at its minimum.
"""
import itertools
import numpy as np
from scipy.special import logsumexp

KT = 0.596          # kcal/mol, the value the text uses
THRS = (np.inf, 12, 8, 6, 4, 3, 2, 1.5, 1, 0.5, -1.0)     # the threshold rule of the script under review


def total_kT(npz, part="total"):
    if part == "total":
        e = npz["vac"] + npz["gbn2"]
    elif part == "vac":
        e = npz["vac"].copy()
    elif part == "gb":
        e = npz["gbn2"].copy()
    else:
        raise ValueError(part)
    e = e / KT
    return e - e.min()


def closed_cells(N, k, shift_pts=0):
    """idx[c, a] (k, m+1): grid indices of the closed cell c; boundaries at shift_pts + c*m; trapezoid weights."""
    assert N % k == 0
    m = N // k
    idx = (shift_pts + np.arange(k)[:, None] * m + np.arange(m + 1)[None, :]) % N
    tw = np.ones(m + 1)
    tw[0] = tw[-1] = 0.5
    return idx, tw


def lnZ_grid(E):
    return float(logsumexp(-E) - np.log(E.size))


# ------------------------------------------------------------------------------- rotamer models
def rotamer_models(E, rot_deg=((60, 180, 300), (60, 180, 300)), shift_deg=0.0):
    """Rigid-rotamer model (rotamers at rot_deg, each a third of the circle), cell-minimised model, and the
    populations of the nine 120-degree cells (boundaries at shift_deg + 0, 120, 240)."""
    N = E.shape[0]
    step = 360.0 / N
    r_idx = []
    for d in range(2):
        ii = [int(round(a / step)) % N for a in rot_deg[d]]
        assert all(abs(((i * step - a + 180) % 360) - 180) < 1e-9 for i, a in zip(ii, rot_deg[d])), "rotamer angles must be grid points"
        r_idx.append(ii)
    sp = int(round(shift_deg / step))
    assert abs(sp * step - shift_deg) < 1e-9
    idx, tw = closed_cells(N, 3, sp)
    Erot = E[np.ix_(r_idx[0], r_idx[1])]
    B = E[idx[:, :, None, None], idx[None, None, :, :]]              # (3, m+1, 3, m+1)
    Emin = B.min(axis=(1, 3))
    W = np.einsum('a,b,cadb->cd', tw, tw, np.exp(-B))
    Pg = W / W.sum()
    Pr = np.exp(-(Erot - Erot.min()))
    Pr /= Pr.sum()
    Pm = np.exp(-(Emin - Emin.min()))
    Pm /= Pm.sum()
    lz = lnZ_grid(E)
    out = dict(Erot=Erot, Emin=Emin, Pg=Pg, Pr=Pr, Pm=Pm, lnZ=lz,
               lnZ_rot=float(logsumexp(-Erot) - 2 * np.log(3)), lnZ_min=float(logsumexp(-Emin) - 2 * np.log(3)),
               tv_r=0.5 * np.abs(Pg - Pr).sum(), tv_m=0.5 * np.abs(Pg - Pm).sum(),
               max_r=np.abs(Pg - Pr).max(), max_m=np.abs(Pg - Pm).max())
    # which cell (of the shifted partition) holds each rigid rotamer state
    cell_of_rot = []
    for d in range(2):
        cc = []
        for i in r_idx[d]:
            hit = [c for c in range(3) if ((i - sp - c * (N // 3)) % N) <= N // 3]
            # a rotamer exactly on a boundary belongs to two closed cells: take the first, flag it
            cc.append(hit[0])
        cell_of_rot.append(cc)
    out["cell_of_rot"] = cell_of_rot
    a = np.unravel_index(Erot.argmin(), Erot.shape)
    out["rot_min_state"] = (int(a[0]), int(a[1]))
    out["rot_min_cell"] = (cell_of_rot[0][a[0]], cell_of_rot[1][a[1]])
    srt = np.sort(Erot.ravel())
    out["rot_gap"] = float(srt[1] - srt[0])
    g = np.unravel_index(E.argmin(), E.shape)
    out["cont_min_deg"] = (g[0] * step, g[1] * step)
    c = np.unravel_index(Emin.argmin(), Emin.shape)
    out["cont_min_cell"] = (int(c[0]), int(c[1]))
    out["same_cell"] = out["rot_min_cell"] == out["cont_min_cell"]
    out["rigid_cell_min_above_global"] = float(Emin[out["rot_min_cell"]] - Emin.min())
    out["width_term"] = -np.log(W / (tw.sum() ** 2)) - Emin          # -ln <exp(-(E - E_cellmin))>_cell
    out["W"] = W
    return out


# ------------------------------------------------------------------------------- Proposition A17.24, two sites
class Bracket2:
    """One term V(x1, x2) on an N x N grid; product reference with log-weights lw1, lw2 on the grid
    (None = uniform); k closed cells per site.  ln of  int exp(-V) d nu  is bracketed."""

    def __init__(self, V, k, lw1=None, lw2=None):
        N = V.shape[0]
        self.N, self.k = N, k
        idx, tw = closed_cells(N, k)
        lw1 = np.zeros(N) if lw1 is None else lw1
        lw2 = np.zeros(N) if lw2 is None else lw2
        self.lv, self.P = [], []
        for lw in (lw1, lw2):
            lp = lw - logsumexp(lw)                       # log nu on the grid
            lc = lp[idx] + np.log(tw)[None, :]
            lv = logsumexp(lc, axis=1)
            self.lv.append(lv)
            self.P.append(np.exp(lc - lv[:, None]))
        V4 = V[idx[:, :, None, None], idx[None, None, :, :]]       # (k, m+1, k, m+1): c, a, d, b
        P1, P2 = self.P
        self.R_HH = np.einsum('ca,db,cadb->cd', P1, P2, V4, optimize=True)
        self.o1_HH = (V4.max(axis=1) - V4.min(axis=1)).max(axis=2)
        self.o2_HH = (V4.max(axis=3) - V4.min(axis=3)).max(axis=1)
        Vm2 = V4.min(axis=3)                                       # c, a, d   (site 2 minimised)
        self.R_HM = np.einsum('ca,cad->cd', P1, Vm2)
        self.o1_HM = Vm2.max(axis=1) - Vm2.min(axis=1)
        Vm1 = V4.min(axis=1)                                       # c, d, b   (site 1 minimised)
        self.R_MH = np.einsum('db,cdb->cd', P2, Vm1)
        self.o2_MH = Vm1.max(axis=2) - Vm1.min(axis=2)
        self.R_MM = V4.min(axis=(1, 3))
        self.R_max = V4.max(axis=(1, 3))
        self.lvs = self.lv[0][:, None] + self.lv[1][None, :]

    def jensen(self):
        return float(logsumexp(self.lvs - self.R_HH))

    def minima(self):
        return float(logsumexp(self.lvs - self.R_MM))

    def maxima(self):
        return float(logsumexp(self.lvs - self.R_max))

    def upper(self, h1, h2, scale=1.0):
        """h1[c], h2[d]: True = mode H.  scale < 1: deliberately too small oscillations (control)."""
        H1, H2 = h1[:, None], h2[None, :]
        with np.errstate(over="ignore"):
            eHH = -self.R_HH + ((scale * self.o1_HH) ** 2 + (scale * self.o2_HH) ** 2) / 8.0
            eHM = -self.R_HM + (scale * self.o1_HM) ** 2 / 8.0
            eMH = -self.R_MH + (scale * self.o2_MH) ** 2 / 8.0
        eMM = -self.R_MM
        expo = np.where(H1 & H2, eHH, np.where(H1 & ~H2, eHM, np.where(~H1 & H2, eMH, eMM)))
        return float(logsumexp(self.lvs + expo))

    def cmax(self):
        return self.o1_HH.max(axis=1), self.o2_HH.max(axis=0)

    def upper_threshold(self, thr, scale=1.0):
        c1, c2 = self.cmax()
        return self.upper(c1 <= thr, c2 <= thr, scale)

    def best_threshold(self):
        vals = {thr: self.upper_threshold(thr) for thr in THRS}
        thr = min(vals, key=lambda t: vals[t])
        return vals[thr], thr, vals

    def best_exhaustive(self):
        """minimum of the upper end over ALL assignments of modes to (site, cell) — 4^k of them."""
        k = self.k
        best = np.inf
        arg = None
        for bits in itertools.product([False, True], repeat=2 * k):
            h1 = np.array(bits[:k])
            h2 = np.array(bits[k:])
            u = self.upper(h1, h2)
            if u < best:
                best, arg = u, (h1, h2)
        return best, arg

    def best_local(self, h1, h2, sweeps=8):
        h1, h2 = h1.copy(), h2.copy()
        cur = self.upper(h1, h2)
        for _ in range(sweeps):
            improved = False
            for h in (h1, h2):
                for c in range(self.k):
                    h[c] = not h[c]
                    new = self.upper(h1, h2)
                    if new < cur - 1e-13:
                        cur, improved = new, True
                    else:
                        h[c] = not h[c]
            if not improved:
                break
        return cur, (h1, h2)


def tilted_parts(E):
    """One-site slices through the grid minimum and the remainder  V = E - e1 - e2  (E zero at its minimum)."""
    i0, j0 = np.unravel_index(E.argmin(), E.shape)
    e1 = E[:, j0].copy()
    e2 = E[i0, :].copy()
    V = E - e1[:, None] - e2[None, :]
    N = E.shape[0]
    lz = (float(logsumexp(-e1) - np.log(N)), float(logsumexp(-e2) - np.log(N)))
    return e1, e2, V, lz, (i0, j0)
