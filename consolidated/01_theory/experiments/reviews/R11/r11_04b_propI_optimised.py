"""R11 / 04b -- the bound of Proposition I maximised over the block label law M_L itself.

The report's M_L is an Arimoto iterate for G_L alone that was stopped by an iteration cap
(y07_block_labels.py, read AFTER my own run of r11_04: itmax = 300 + 3e8/size), so its four
headline numbers are neither the optimum of G_L (r11_04 gives larger G_L) nor the optimum of
the bound.  Any M_L gives a valid bound.  Here: exponentiated-gradient ascent of
      J(M) = [ G_L(M) + Lambda_blk(M) ] / L        (M symmetric under the global flip, so lam_Q = 1)
on the labels with <= 2 walls, started at the G_L-optimum; the final M is re-evaluated from
scratch (G_L from the definition, Lambda_blk with N = 128 and against exact increments).

Run:  python3 r11_04b_propI_optimised.py          (about 2-4 minutes)
"""
import sys, time
import numpy as np
from r11lib import *

T0 = time.time()
u = 1.0
h = u / 2
hc, tc, ac, Ec = cube_constants(u)


def walls_labels(L, maxwalls):
    sig = configs(L)
    nw = ((sig[:, :-1] * sig[:, 1:]) == -1).sum(axis=1)
    return sig[nw <= maxwalls]


def end_matrix(s, w):
    B = np.zeros((2, 2))
    np.add.at(B, ((s[:, 0] == -1).astype(int), (s[:, -1] == -1).astype(int)), w)
    return B


class BlockProblem:
    def __init__(self, p, L, t, maxwalls, N=40):
        self.p, self.L, self.t, self.N = p, L, t, N
        self.labels = walls_labels(L, maxwalls)
        self.s, self.pi = chain_law(L, p)
        phis = -h * self.labels.astype(float) @ self.s.T.astype(float)
        self.logP = gibbs_logs(np.log(self.pi), phis)
        self.A = np.exp(t * self.logP)
        rho0 = 2 * np.array([[1 - p, p], [p, 1 - p]])
        self.rho0 = rho0
        self.Bs = np.array([end_matrix(self.s, np.exp(lp)) for lp in self.logP])
        self.As = np.array([B @ rho0 for B in self.Bs])
        # the flip partner of every label (for symmetrisation)
        key = {tuple(l): i for i, l in enumerate(self.labels)}
        self.partner = np.array([key[tuple(-l)] for l in self.labels])
        # collocation matrices T_phi on a common invariant interval
        lo, hi = 1.0, 0.0
        for A in self.As:
            for x in (0.0, 1.0):
                w0 = x * A[0, 0] + (1 - x) * A[1, 0]
                w1 = x * A[0, 1] + (1 - x) * A[1, 1]
                y = w0 / (w0 + w1)
                lo, hi = min(lo, y), max(hi, y)
        k = np.arange(N)
        z = np.cos(np.pi * (k + 0.5) / N)
        x = 0.5 * (lo + hi) + 0.5 * (hi - lo) * z
        Tx = np.cos(np.outer(np.arccos(z), np.arange(N)))
        c = np.full(N, 2.0 / N)
        c[0] = 1.0 / N
        self.Tphi = np.empty((len(self.As), N, N))
        for a, A in enumerate(self.As):
            w0 = x * A[0, 0] + (1 - x) * A[1, 0]
            w1 = x * A[0, 1] + (1 - x) * A[1, 1]
            sm = w0 + w1
            zy = np.clip((2 * (w0 / sm) - (lo + hi)) / (hi - lo), -1, 1)
            Ty = np.cos(np.outer(np.arccos(zy), np.arange(N)))
            self.Tphi[a] = (sm ** t)[:, None] * (Ty @ (c[:, None] * Tx.T))

    def J(self, M, grad=False):
        t, L = self.t, self.L
        mt = M @ self.A
        m = mt ** (1.0 / t)
        S = m.sum()
        G = -t * np.log(S)
        T = np.tensordot(M, self.Tphi, axes=1)
        ev, VR = np.linalg.eig(T)
        i = int(np.argmax(ev.real))
        lam = ev[i].real
        val = (G + np.log(lam)) / L
        if not grad:
            return val
        r = VR[:, i].real
        evl, VL = np.linalg.eig(T.T)
        j = int(np.argmax(evl.real))
        l = VL[:, j].real
        dG = -(self.A @ (m / mt)) / S
        dLam = np.einsum('i,aij,j->a', l, self.Tphi, r) / (lam * (l @ r))
        return val, (dG + dLam) / L

    def symmetrise(self, M):
        M = 0.5 * (M + M[self.partner])
        return M / M.sum()


targets = {0.4: (12, 0.459, 0.034026), 0.3: (14, 0.434, 0.040115), 0.2: (14, 0.409, 0.044599), 0.1: (14, 0.380, 0.044378)}
ps = [float(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else [0.4, 0.3, 0.2, 0.1]
for p in ps:
    L, t, rep = targets[p]
    t1 = time.time()
    bp = BlockProblem(p, L, t, 2)
    lo, up, M = maximise_G_fast(bp.logP, t)
    M = bp.symmetrise(np.maximum(M, 1e-12))
    v0 = bp.J(M)
    val, g = bp.J(M, grad=True)
    eta = 50.0
    for it in range(3000):
        while True:
            w = np.log(M) + eta * (g - g.max())
            Mn = np.exp(w - w.max())
            Mn = bp.symmetrise(np.maximum(Mn / Mn.sum(), 1e-300))
            vn = bp.J(Mn)
            if vn > val or eta < 1e-3:
                break
            eta /= 2
        if vn <= val:
            break
        gain = vn - val
        M = Mn
        val, g = bp.J(M, grad=True)
        eta = min(eta * 1.5, 1e4)
        if gain < 1e-12 and it > 50:
            break
    # re-evaluation from scratch
    keep = M > 1e-14
    Mk = M[keep] / M[keep].sum()
    G_L = G_of_M(bp.logP[keep], Mk, t)
    Lam = moment_lyapunov(list(bp.As[keep]), Mk, t, N=128)
    logQ = centre_of_M(bp.logP[keep], Mk, t)
    lamQ = float(np.max(np.linalg.eigvals(end_matrix(bp.s, np.exp(logQ)) @ bp.rho0).real))
    final = (G_L + Lam - t * np.log(lamQ)) / L
    # exact increment k = 1 -> 2 of ln E[c^t]
    one = np.ones(2)
    v1 = one @ bp.Bs[keep]
    v2 = np.einsum('ai,ij,bjk->abk', v1, bp.rho0, bp.Bs[keep])
    E2 = float((np.outer(Mk, Mk) * (v2 @ one) ** t).sum())
    print(f"p={p} L={L} t={t}: start (G_L-optimum) {v0:.6f}  ->  optimised bound {final:.6f}  (report {rep:.6f}; cube {hc:.6f}; ratio {final/hc:.3f})")
    print(f"      G_L = {G_L:.9f}, Lambda_blk(N=128) = {Lam:.9f}, exact increment k=1->2 = {np.log(E2):.7f}, ln lam_Q = {np.log(lamQ):.1e},"
          f" labels with weight > 1e-5: {(M>1e-5).sum()}, iterations {it}   [{time.time()-t1:.0f} s]")
    # refine t with the same procedure started at the current M (coarse)
print(f"{time.time()-T0:.1f} s")
