"""R11 / 05 -- an independent certificate of the headline that uses neither Lyapunov exponents
nor Propositions H, I:  exact product structure from (L') + Lemma A + enumeration of ONE block.

Chain of k blocks of L sites separated by gaps of m sites (n = k(L+m) - m).  For labels
   phi_j(x_B) = - sum_{i in block} h_i sigma_i x_i ,   h_i = u/2 inside,  h_i = (u - kappa_m)/2 at the two ends,
the residual  psi = sum_j phi_j(x_{B_j}) + sum_j ln rho_m(x_{e_j}, x_{s_{j+1}})  is a member of C_d
(Theorem Y3) and its Gibbs law restricted to the blocks is the PRODUCT of the block Gibbs laws.
Hence for a label law M_L on one block and M = M_L^{(x)k}:   G_t^{(n)}(M) = k * G_t^{(L)}(M_L)  EXACTLY,
and by Lemma A every algorithm makes >= (1-2 delta) exp(k G_t^{(L)}(M_L) - t eps) evaluations at the
instance gamma*(M), for every k.  Per site:  G_t^{(L)}(M_L) / (L + m).

Part A: the per-site rate for p = 0.4, 0.3 (m = 0), 0.2 (m = 1, 2), 0.1 (m = 3..6), L <= 14 or 16.
Part B: end-to-end brute force on a chain of n = 16 = 2 x 8 sites (p = 0.3): membership of all
        residuals involved, the product structure, the gaps in ln A, the coverage identity.

Run:  python3 r11_05_certificate.py A 0.4 0.3 0.2 0.1   (Part A for the listed p, L <= 14; about 3 min on a free machine)
      python3 r11_05_certificate.py A 0.4 L16          (the same with L = 16 added; several minutes per p)
      python3 r11_05_certificate.py B              (Part B; about 1 min)
"""
import sys, time
import numpy as np
from r11lib import *

T0 = time.time()
u = 1.0
hc, tc, ac, Ec = cube_constants(u)


def walls_labels(L, maxwalls):
    sig = configs(L)
    nw = ((sig[:, :-1] * sig[:, 1:]) == -1).sum(axis=1)
    return sig[nw <= maxwalls]


def kappa(p, m):
    lam = 1 - 2 * p
    return np.log((1 + lam ** (m + 1)) / (1 - lam ** (m + 1)))


def block_logP(L, p, m, labels):
    s, pi = chain_law(L, p)
    hs = np.full(L, u / 2)
    red = (u - kappa(p, m)) / 2
    assert red >= 0, "reduced end slope negative: gap too small"
    if L == 1:
        hs[0] = (u - 2 * kappa(p, m)) / 2
        assert hs[0] >= 0
    else:
        hs[0] = hs[-1] = red
    phis = -(labels.astype(float) * hs[None, :]) @ s.T.astype(float)
    return s, pi, hs, phis, gibbs_logs(np.log(pi), phis)


def rate(L, p, m, t, maxwalls=None):
    labels = configs(L) if maxwalls is None else walls_labels(L, maxwalls)
    s, pi, hs, phis, logP = block_logP(L, p, m, labels)
    lo, up, M = maximise_G_fast(logP, t)
    return lo / (L + m), up / (L + m), M, labels


print("== Part A: per-site rate G_t^(L)(M_L)/(L+m) of the reduced-end block family (exact for every k) ==")
print(f"cube: h = {hc:.6f} (exact exponent of the uniform cube at bounded accuracy, u = 1)")
plan = {0.4: [(0, 0.454)], 0.3: [(0, 0.433)], 0.2: [(1, 0.409), (2, 0.409)], 0.1: [(3, 0.38), (4, 0.38), (5, 0.38)]}
MODE = sys.argv[1] if len(sys.argv) > 1 else 'A'
PS = [float(a) for a in sys.argv[2:] if a != 'L16'] if len(sys.argv) > 2 else [0.4, 0.3, 0.2, 0.1]
LS = (4, 6, 8, 10, 12, 14, 16) if 'L16' in sys.argv else (4, 6, 8, 10, 12, 14)
best_overall = {}
for p, lst in plan.items():
    if MODE != 'A' or p not in PS:
        continue
    for m, t in lst:
        row = []
        best = (0, None)
        for L in LS:
            mw = None if L <= 10 else (3 if L <= 12 else 2)
            lo, up, M, labels = rate(L, p, m, t, mw)
            row.append(f"L={L}: {lo:.6f}")
            if lo > best[0]:
                best = (lo, L, mw)
        # refine t at L = 12 (cheap), then evaluate the best L at that t
        _, L, mw = best
        tt, val = golden_max(lambda x: rate(12, p, m, x, 2)[0], max(0.2, t - 0.06), min(0.8, t + 0.06), tol=4e-3)
        lo, up, M, labels = rate(L, p, m, tt, mw)
        if lo < best[0]:
            tt = t
            lo, up, M, labels = rate(L, p, m, tt, mw)
        best_overall[p] = max(best_overall.get(p, (0,)), (lo, L, m, tt))
        print(f"p={p} m={m} (end slope u-kappa_m = {u-kappa(p,m):.3f}) t={t}: " + "  ".join(row))
        print(f"      best L={L} ({'all 2^L labels' if mw is None else '<= %d walls' % mw}), t refined to {tt:.3f}: rate = {lo:.6f}"
              f" (dual over the label set {up:.6f});  ratio to the cube {lo/hc:.3f};  labels with weight > 1e-5: {(M>1e-5).sum()}   [{time.time()-T0:.0f} s]")
print("summary (valid for every number of blocks k, exact, no limit taken):")
for p, (lo, L, m, tt) in best_overall.items():
    print(f"   p={p}: exponent per site >= {lo:.6f}  (L={L}, m={m}, t={tt:.3f})   cube {hc:.6f}   {'ABOVE the cube' if lo > hc else 'not above the cube'}")

# -------------------------------------------------------------------------------------------- Part B
if MODE != 'B':
    print(f"{time.time()-T0:.1f} s")
    sys.exit(0)
print("\n== Part B: end-to-end brute force, n = 16 = 2 blocks of 8, p = 0.3, m = 0 ==")
p, L, k, m, t = 0.3, 8, 2, 0, 0.43
n = k * L
K = np.log((1 - p) / p)
labels = walls_labels(L, 1)                      # 16 labels per block: uniform fields and one wall
s8, pi8, hs, phis8, logP8 = block_logP(L, p, m, labels)
G_L, up_L, M_L = maximise_G_fast(logP8, t)
print(f"block: {labels.shape[0]} labels (<= 1 wall), end slope {u-kappa(p,0):.4f};  G_t^(8)(M_L) = {G_L:.9f};  per site {G_L/L:.6f}")
s, pi = chain_law(n, p)
N = 2 ** n
idx = np.arange(N)
i1 = idx & (2 ** L - 1)          # configuration of block 1 (sites 0..7)
i2 = idx >> L                    # configuration of block 2 (sites 8..15)
# ln rho_0 at the cut (sites 7 and 8)
same = (s[:, L - 1] * s[:, L]) == 1
lnrho = np.where(same, np.log(2 * (1 - p)), np.log(2 * p))
slopes = [u] * n
nl = labels.shape[0]
worst_mem = -np.inf
worst_prod = 0.0
lnA = np.empty((nl, nl))
logpi = np.log(pi)
# m(x)^t = sum_phi M(phi) pi_phi(x)^t accumulated label by label (memory: a few arrays of 65536)
mt = np.zeros(N)
phit = {}
for a in range(nl):
    for b in range(nl):
        psi = phis8[a][i1] + phis8[b][i2] + lnrho
        worst_mem = max(worst_mem, is_lipschitz(psi, n, slopes))
        lw = logpi - psi
        lz = logsumexp(lw)
        lnA[a, b] = lz
        lp = lw - lz
        # product structure: pi_psi = pi_{8,phi_a} x pi_{8,phi_b}
        worst_prod = max(worst_prod, float(np.abs(lp - (logP8[a][i1] + logP8[b][i2])).max()))
        mt += M_L[a] * M_L[b] * np.exp(t * lp)
print(f"all {nl*nl} residuals psi = phi_a + phi_b + ln rho_0 are in C_d: largest edge violation {worst_mem:.2e} (<= 0 admissible)")
print(f"Gibbs laws are products of block Gibbs laws: max |ln pi_psi - ln(pi_a x pi_b)| = {worst_prod:.2e};  A_pi(psi) = A(phi_a) A(phi_b): "
      f"{np.abs(lnA - (logsumexp(np.log(pi8)[None,:]-phis8,axis=1)[:,None] + logsumexp(np.log(pi8)[None,:]-phis8,axis=1)[None,:])).max():.2e}")
lm = np.log(mt) / t
G16 = -t * logsumexp(lm)
print(f"G_t^(16)(M_L x M_L) = {G16:.9f}  =  2 G_t^(8)(M_L) = {2*G_L:.9f};   cube: 16 F_c(t) = {16*cube_F(t):.6f};  ratio {G16/(16*cube_F(t)):.3f}")
# the instance gamma* and the alternatives of Lemma A
lq = lm - logsumexp(lm)                         # ln pi_gamma*
gam_t = logpi - lq                              # gamma~* (normalised: E_pi e^{-gamma~*} = 1)
print(f"gamma* in C_d: largest edge violation {is_lipschitz(gam_t, n, slopes):.2e};  osc gamma* = {gam_t.max()-gam_t.min():.4f}")
eps = 0.5
r = eps + 1e-9
cover = np.zeros(N)                             # sum_phi M(phi) 1[x in D_phi]
expw = np.zeros(N)                              # sum_phi M(phi) exp(-t (Phi_phi(x) - r))
min_gap = np.inf
worst_alt = -np.inf
for a in range(nl):
    for b in range(nl):
        psi_t = phis8[a][i1] + phis8[b][i2] + lnrho + lnA[a, b]      # phi~
        Phi = psi_t - gam_t
        alt = gam_t - np.maximum(r - Phi, 0.0)                         # = min(gamma~*, phi~ - r)
        worst_alt = max(worst_alt, is_lipschitz(alt, n, slopes))
        gap = logsumexp(logpi - alt) - logsumexp(logpi - gam_t)
        min_gap = min(min_gap, gap)
        w = M_L[a] * M_L[b]
        cover += w * (Phi < r)
        expw += w * np.exp(-t * (Phi - r))
print(f"alternatives gamma* - (r - Phi_phi)_+ with r = eps = {eps}: all in C_d (largest edge violation {worst_alt:.2e});"
      f" smallest gain in ln A = {min_gap:.6f} (> eps = {eps}: {min_gap > eps})")
print(f"exponential weights: max_x sum_phi M e^(-t(Phi-r)) = {expw.max():.9f}, min_x = {expw.min():.9f};  e^(t r - G) = {np.exp(t*r-G16):.9f}")
print(f"hard packing with the weights M: max_x sum_phi M 1[x in D_phi] = {cover.max():.6f}  ->  E|Q| >= (1-2 delta) * {1/cover.max():.4f};"
      f"   exponential-weights bound (1-2 delta) * {np.exp(G16 - t*eps):.4f}")
print(f"{time.time()-T0:.1f} s")
