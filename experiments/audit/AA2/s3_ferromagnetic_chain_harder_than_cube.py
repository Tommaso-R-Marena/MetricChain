#!/usr/bin/env python3
"""AA2 audit, script S3 -- "ferromagnets are never harder than the uniform cube" (theory report
Proposition 11.81(a), Corollary 11.91) is a statement about known parts that are FUNCTIONS OF THE TYPE.

Independent re-computation (own code; nothing imported from the repository) of the block certificate of
theory report Proposition 11.117(a) / referee R11 section 4.4 for the symmetric two-state chain with flip
probability p (a nearest-neighbour FERROMAGNET for p < 1/2), Hamming envelope of slope u:

  * Theorem 11.116(b): blocks of L sites separated by gaps of m sites embed exactly, with the envelope
    reduced by kappa_m = ln[(1 + lam^{m+1})/(1 - lam^{m+1})], lam = 1 - 2p, at the two ends of a block;
  * Theorem 11.116(c) [machine-checked, SoftMinLowerBound.lean]: for any law M on members of the class and
    0 < t < 1 every (eps/2, delta)-correct algorithm makes at least (1 - 2 delta) exp(G_t(M) - t eps)
    evaluations at the soft minimum of the labels, G_t(M) = -t ln sum_x (sum_phi M(phi) pi_phi(x)^t)^{1/t};
  * with labels that are independent over the blocks, G_t adds over the blocks, so
        G_t(M_block) / (L + m)
    is a lower bound on the exponent of EVERY algorithm at EVERY accuracy (per site, n = k(L+m) - m).

The script (1) checks the embedding end to end on a chain of 8 sites, (2) evaluates the bound for
p = 0.3, 0.4 at u = 1 and compares it with the uniform cube's exponent h = KL(Lambda_1/u || 1/2), which by
Theorem 11.58 is the exact exponent of the cube at bounded accuracy.

Run:  python3 experiments/audit/AA2/s3_ferromagnetic_chain_harder_than_cube.py > experiments/audit/AA2/out_s3.txt
"""
import itertools
import math
import numpy as np


def block_law(L, p):
    """marginal of the stationary symmetric chain on L consecutive sites (x as bit string)."""
    out = np.empty(1 << L)
    for x in range(1 << L):
        pr = 0.5
        for i in range(L - 1):
            pr *= (1 - p) if ((x >> i) & 1) == ((x >> (i + 1)) & 1) else p
        out[x] = pr
    return out


def spins(L):
    return np.array([[1.0 if (x >> i) & 1 else -1.0 for i in range(L)] for x in range(1 << L)])


def labels(L, u, end_slope, max_walls=2):
    """members of the block class: phi(x) = -sum_i h_i sig_i s_i, |h_i| = u/2 inside, end_slope/2 at the two
    ends (a flip of s_i changes phi by 2 h_i <= the slope of site i), sig piecewise constant with <= max_walls walls."""
    hs = np.array([end_slope / 2] + [u / 2] * (L - 2) + [end_slope / 2])
    s = spins(L)
    out = []
    for walls in range(max_walls + 1):
        for W in itertools.combinations(range(1, L), walls):
            sig = np.ones(L)
            for wpos in W:
                sig[wpos:] *= -1
            for sgn in (1.0, -1.0):
                out.append(-(s * (hs * sig * sgn)[None, :]).sum(axis=1))
    return np.array(out)


def renyi_G(pi, lab, t, iters=400):
    """G_t(M) for the uniform label law and after an exponentiated-gradient ascent in M (any M gives a valid bound)."""
    P = pi[None, :] * np.exp(-lab)
    P /= P.sum(axis=1, keepdims=True)                 # Gibbs laws of the labels
    Pt = P ** t
    M = np.full(len(lab), 1.0 / len(lab))

    def val(M):
        return -t * math.log(float(((M @ Pt) ** (1.0 / t)).sum()))
    g_unif = val(M)
    best, bestM = g_unif, M.copy()
    eta = 2.0
    for _ in range(iters):
        mix = M @ Pt
        grad = (Pt * (mix ** (1.0 / t - 1.0))[None, :]).sum(axis=1)   # d/dM of sum_x mix^{1/t}, up to 1/t
        M2 = M * np.exp(-eta * (grad - grad.min()) / max(grad.max() - grad.min(), 1e-300))
        M2 /= M2.sum()
        v = val(M2)
        if v > best:
            best, bestM, M = v, M2.copy(), M2
        else:
            eta *= 0.5
            if eta < 1e-6:
                break
    return g_unif, best


def cube_h(u):
    lam1 = math.log(2 / (1 + math.exp(-u)))
    rho = lam1 / u
    return math.log(2) + rho * math.log(rho) + (1 - rho) * math.log(1 - rho)


print("AA2 / S3: a nearest-neighbour ferromagnet that is harder than the uniform cube")
print()

# ---------------------------------------------------------------- (1) the embedding, end to end
p, u, L = 0.3, 1.0, 4
lam = 1 - 2 * p
K = math.log((1 + lam) / (1 - lam))                   # kappa_0 = ln((1-p)/p)
lab = labels(L, u, u - K)
n = 2 * L
pi_n, pi_L = block_law(n, p), block_law(L, p)
xs = np.arange(1 << n)
lo, hi = xs & ((1 << L) - 1), xs >> L
same = ((lo >> (L - 1)) & 1) == (hi & 1)
lnrho = np.where(same, math.log(2 * (1 - p)), math.log(2 * p))
rng = np.random.default_rng(20261126)
worst_lip, worst_part, worst_gibbs = 0.0, 0.0, 0.0
for _ in range(60):
    a, b = rng.integers(len(lab), size=2)
    psi = lab[a][lo] + lab[b][hi] + lnrho
    for i in range(n):
        worst_lip = max(worst_lip, float(np.abs(psi[xs ^ (1 << i)] - psi).max()))
    A_chain = float(pi_n @ np.exp(-psi))
    A_prod = float(pi_L @ np.exp(-lab[a])) * float(pi_L @ np.exp(-lab[b]))
    worst_part = max(worst_part, abs(A_chain / A_prod - 1))
    gib = pi_n * np.exp(-psi) / A_chain
    ga = pi_L * np.exp(-lab[a]); ga /= ga.sum()
    gb = pi_L * np.exp(-lab[b]); gb /= gb.sum()
    worst_gibbs = max(worst_gibbs, float(np.abs(gib - ga[lo] * gb[hi]).max()))
print(f"(1) two blocks of {L} sites, no gap, p = {p}, u = {u}, end slope u - K = {u - K:.4f}; 60 random pairs of labels")
print(f"    largest single-flip change of psi = phi_a + phi_b + ln rho_0 on the chain of {n} sites: {worst_lip:.6f}  (must be <= u = {u})")
print(f"    largest |A_chain(psi)/(A_block(phi_a) A_block(phi_b)) - 1|: {worst_part:.2e};  largest deviation of the Gibbs law from the product: {worst_gibbs:.2e}")
assert worst_lip <= u + 1e-9 and worst_part < 1e-12 and worst_gibbs < 1e-12
print()

# ---------------------------------------------------------------- (2) the bound
print("(2) lower bound per site for every algorithm, max over t of G_t(M)/(L + m)")
hc = cube_h(1.0)
print(f"    uniform cube at u = 1: h = {hc:.6f}  (theory report: 0.029139; exact exponent of the cube at bounded accuracy, Theorem 11.58)")
ts = [0.35, 0.40, 0.45, 0.50, 0.55]
for p in (0.3, 0.4):
    lam = 1 - 2 * p
    best_all = (0.0, None)
    for L in (6, 8, 10, 12):
        pi = block_law(L, p)
        for m in (0, 1, 2):
            kap = math.log((1 + lam ** (m + 1)) / (1 - lam ** (m + 1)))
            if kap >= u:
                continue
            lab = labels(L, u, u - kap)
            row = []
            for t in ts:
                g_unif, g_opt = renyi_G(pi, lab, t)
                row.append((g_opt / (L + m), g_unif / (L + m), t))
            b = max(row)
            print(f"    p={p} L={L:2d} gap m={m} (end slope {u - kap:.4f}, {len(lab)} labels): bound = {b[0]:.6f} at t={b[2]:.2f}"
                  f"  (uniform label law: {max(r[1] for r in row):.6f})   ratio to cube h: {b[0] / hc:.4f}")
            if b[0] > best_all[0]:
                best_all = (b[0], (L, m, b[2]))
    print(f"    => p={p}: best bound {best_all[0]:.6f} at (L, m, t) = {best_all[1]}, i.e. {100 * (best_all[0] / hc - 1):.1f} % above the cube's exponent")
print()
print("    Reading: at slope u = 1 the symmetric ferromagnetic chain needs at least (1 - 2 delta) exp(n * bound - O(1)) evaluations")
print("    of every algorithm at every bounded accuracy, more than the uniform cube's exp(n h + o(n)).  So the comparison")
print("    'a ferromagnetic interaction never makes the problem harder than no interaction' is FALSE outside the class of")
print("    known parts that are functions of the type (mean-field models), for which it is proved.")
