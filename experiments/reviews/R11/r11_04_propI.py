"""R11 / 04 -- Proposition I (label laws i.i.d. over blocks, exact boundary term) and the four
headline lower ends 0.034026 (p=0.4), 0.040115 (0.3), 0.044599 (0.2), 0.044378 (0.1).

(1) the formula  G^(kL)(M) = k G^(L)(M_L) + ln E[c^t] - t ln E_{Q x..x Q}[prod rho_0]
    against a direct computation from the definitions on n = 6 (L=3,k=2) and n = 9 (L=3,k=3)
    and n = 8 (L=4, k=2), with random (not symmetric) M_L;
(2) the bound [G^(L)(M_L) + Lambda_blk(t) - t ln lam_max(B_Q rho_0)]/L for site-wise labels with
    at most 2 walls on a block of L sites; M_L = my own optimum of G^(L) on that label set
    (any M_L gives a valid bound);  Lambda_blk by my operator and by exact enumeration k = 2, 3.

Run:  python3 r11_04_propI.py            (about 3-5 minutes)
"""
import sys, time, itertools
import numpy as np
from r11lib import *

T0 = time.time()
u = 1.0
h = u / 2
hc, tc, ac, Ec = cube_constants(u)


def block_objects(L, p, labels):
    """Gibbs laws of the site-wise labels on the L-block (law = stationary L-marginal)."""
    s, pi = chain_law(L, p)
    phis = -h * labels.astype(float) @ s.T.astype(float)
    logP = gibbs_logs(np.log(pi), phis)
    return s, pi, logP


def end_matrix(s, w):
    """B[a, b] = sum of w over configurations with first letter a, last letter b (index 0: +1, 1: -1)."""
    B = np.zeros((2, 2))
    fa = (s[:, 0] == -1).astype(int)
    lb = (s[:, -1] == -1).astype(int)
    np.add.at(B, (fa, lb), w)
    return B


def walls_labels(L, maxwalls):
    sig = configs(L)
    nw = ((sig[:, :-1] * sig[:, 1:]) == -1).sum(axis=1)
    return sig[nw <= maxwalls]


def prop_I_terms(L, p, t, labels, M, N=64):
    s, pi, logP = block_objects(L, p, labels)
    G_L = G_of_M(logP, M, t)
    logQ = centre_of_M(logP, M, t)
    P = np.array([[1 - p, p], [p, 1 - p]])
    rho0 = 2 * P
    Bs = [end_matrix(s, np.exp(logP[k])) for k in range(labels.shape[0])]
    As = [B @ rho0 for B in Bs]
    BQ = end_matrix(s, np.exp(logQ))
    lamQ = float(np.max(np.linalg.eigvals(BQ @ rho0).real))
    sup = M > 1e-300
    Lam = moment_lyapunov([A for A, k in zip(As, sup) if k], M[sup], t, N=N)
    return G_L, Lam, np.log(lamQ), Bs, As, BQ, logP, logQ


# ------------------------------------------------------------------------------------------ (1)
print("== (1) Proposition I against the definitions ==")
rng = np.random.default_rng(7)
worst = 0.0
for (L, k, p, t) in ((3, 2, 0.3, 0.43), (3, 3, 0.3, 0.43), (3, 2, 0.1, 0.7), (4, 2, 0.2, 0.3), (2, 4, 0.4, 0.55)):
    labels = configs(L)                                # all 2^L site-wise labels of the block
    nl = labels.shape[0]
    M = rng.dirichlet(np.ones(nl))                     # random, not symmetric
    G_L, Lam, lnlamQ, Bs, As, BQ, logP_L, logQ = prop_I_terms(L, p, t, labels, M)
    P = np.array([[1 - p, p], [p, 1 - p]])
    rho0 = 2 * P
    one = np.ones(2)
    # exact finite-k terms of the formula
    tuples = list(itertools.product(range(nl), repeat=k))
    lnE = 0.0
    cs = np.empty(len(tuples))
    for idx, tp in enumerate(tuples):
        v = one.copy()
        for j, a in enumerate(tp):
            v = v @ Bs[a]
            if j < k - 1:
                v = v @ rho0
        cs[idx] = v @ one
    wts = np.array([np.prod(M[list(tp)]) for tp in tuples])
    lnEc = np.log((wts * cs ** t).sum())
    v = one.copy()
    for j in range(k):
        v = v @ BQ
        if j < k - 1:
            v = v @ rho0
    lnEQ = np.log(v @ one)
    formula = k * G_L + lnEc - t * lnEQ
    # direct: the chain of n = kL sites, labels = concatenations, M ~ M_L^{(x)k} c^t
    n = k * L
    s, pi = chain_law(n, p)
    biglabels = np.array([np.concatenate([labels[a] for a in tp]) for tp in tuples])
    phis = -h * biglabels.astype(float) @ s.T.astype(float)
    logP = gibbs_logs(np.log(pi), phis)
    # c_phi from the definition: Z_phi / prod_j Z_{L,phi_j}
    sL, piL = chain_law(L, p)
    lnZL = logsumexp(np.log(piL)[None, :] + h * labels.astype(float) @ sL.T.astype(float), axis=1)
    lnZ = logsumexp(np.log(pi)[None, :] - phis, axis=1)
    c_def = np.exp(lnZ - np.array([lnZL[list(tp)].sum() for tp in tuples]))
    Mbig = wts * c_def ** t
    Mbig /= Mbig.sum()
    direct = G_of_M(logP, Mbig, t)
    worst = max(worst, abs(direct - formula), float(np.abs(c_def - cs).max()))
    print(f"L={L} k={k} p={p} t={t}: direct {direct:.12f}  formula {formula:.12f}  |c_def - c_matrix| <= {np.abs(c_def-cs).max():.1e};"
          f"  per block: G_L {G_L:.6f}, ln E[c^t]/(k-1) {lnEc/(k-1):.6f} (operator Lambda_blk {Lam:.6f}), t ln E_Q/(k-1) {t*lnEQ/(k-1):.6f} (t ln lam_Q {t*lnlamQ:.6f})")
print(f"largest deviation: {worst:.2e}")


# ------------------------------------------------------------------------------------------ (2)
def bound(p, L, t, maxwalls, M0=None, tol=1e-10, N=64, full=False):
    labels = walls_labels(L, maxwalls)
    s, pi, logP = block_objects(L, p, labels)
    lo, up, M = maximise_G_fast(logP, t, M0=M0)
    G_L, Lam, lnlamQ, Bs, As, BQ, _, _ = prop_I_terms(L, p, t, labels, M, N=N)
    val = (G_L + Lam - t * lnlamQ) / L
    if full:
        return val, dict(G_L=G_L, up=up, Lam=Lam, lnlamQ=lnlamQ, M=M, As=As, labels=labels, Bs=Bs)
    return val


print("\n== (2) headline lower ends: site-wise labels with <= 2 walls per block ==")
targets = {0.4: (12, 0.459, 0.034026), 0.3: (14, 0.434, 0.040115), 0.2: (14, 0.409, 0.044599), 0.1: (14, 0.380, 0.044378)}
ps = [float(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else [0.4, 0.3, 0.2, 0.1]
for p in ps:
    L, t, rep = targets[p]
    t1 = time.time()
    val, d = bound(p, L, t, 2, full=True)
    M = d['M']
    nl = M.size
    # exact increments of ln E[c^t], k = 1 -> 2 -> 3 (c for k = 1 is 1)
    P = np.array([[1 - p, p], [p, 1 - p]])
    rho0 = 2 * P
    one = np.ones(2)
    Bst = np.array(d['Bs'])                             # (nl, 2, 2)
    v1 = one @ Bst                                      # (nl, 2): 1^T B_a
    E1 = float((M * (v1 @ one) ** t).sum())             # = 1
    v2 = np.einsum('ai,ij,bjk->abk', v1, rho0, Bst)     # 1^T B_a rho0 B_b
    E2 = float((np.outer(M, M) * (v2 @ one) ** t).sum())
    keep = M > 1e-7
    Mk = M[keep] / M[keep].sum()
    v1k = one @ Bst[keep]
    v2k = np.einsum('ai,ij,bjk->abk', v1k, rho0, Bst[keep])
    E2k = float((np.outer(Mk, Mk) * (v2k @ one) ** t).sum())
    v3k = np.einsum('abi,ij,cjk->abck', v2k, rho0, Bst[keep])
    E3k = float((np.einsum('a,b,c->abc', Mk, Mk, Mk) * (v3k @ one) ** t).sum())
    Lam128 = moment_lyapunov([A for A, k in zip(d['As'], M > 1e-300) if k], M[M > 1e-300], t, N=128)
    print(f"p={p} L={L} t={t}: {nl} labels ({(M>1e-5).sum()} with weight > 1e-5);  G_L = [{d['G_L']:.9f}, {d['up']:.9f}] (dual over these labels);"
          f"  Lambda_blk: N=64 {d['Lam']:.9f}, N=128 {Lam128:.9f}; exact increments k=1->2: {np.log(E2)-np.log(E1):.7f},"
          f" k=2->3 (weights > 1e-7): {np.log(E3k)-np.log(E2k):.7f};  ln lam_Q = {d['lnlamQ']:.2e}")
    print(f"      bound per site = {val:.6f}   (report {rep:.6f};  cube {hc:.6f};  ratio {val/hc:.3f})   [{time.time()-t1:.0f} s]")
    # the same at the cube's t* and a small scan in t and L, to see that the maximum is where the report says
    t1 = time.time()
    scan = []
    for tt in (t - 0.02, t - 0.01, t + 0.01, t + 0.02):
        scan.append((tt, bound(p, L, tt, 2, tol=1e-9)))
    print("      t-scan: " + "  ".join(f"t={a:.3f}: {b:.6f}" for a, b in scan) + f"   [{time.time()-t1:.0f} s]")
    t1 = time.time()
    Ls = []
    for LL in (8, 10, 12):
        if LL != L:
            Ls.append((LL, bound(p, LL, t, 2, tol=1e-9)))
    print("      L-scan (<= 2 walls): " + "  ".join(f"L={a}: {b:.6f}" for a, b in Ls) + f"   [{time.time()-t1:.0f} s]")
    w0 = [(LL, bound(p, LL, t, 0, tol=1e-12)) for LL in (3, 4, 5, 6)]
    print("      uniform fields only (0 walls): " + "  ".join(f"L={a}: {b:.6f}" for a, b in w0))
print(f"{time.time()-T0:.1f} s")
