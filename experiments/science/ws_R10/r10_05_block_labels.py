"""r10_05: Proposition I of Y_REPORT 5.3 (label laws i.i.d. over blocks, exact boundary term),
re-derived (R10_REPORT section 2) and re-evaluated with own code.

    F_inf(t) >= [ G_t^(L)(M_L) + Lambda_blk(t) - t ln lam_max(B_Q rho0) ] / L

M_L: a law on labels of an L-block (here: site-wise labels with at most `maxwalls` sign
changes), Q its Renyi centre, B_phi(a,b) = pi_{L,phi}(first letter a, last letter b),
rho0 = 2P, Lambda_blk(t) = moment Lyapunov exponent of order t of the i.i.d. product of the
2x2 matrices B_phi rho0, phi ~ M_L.

 1. the finite-k identity against the definition (brute force, n = 6 and n = 9);
 2. the headline lower ends of h (Y section 6.4, bold) and of a.
usage: python3 r10_05_block_labels.py [check] [h] [a]
"""
import sys
import time
import itertools
import numpy as np
from r10lib import *
from r10_lyap import cheb_nodes, cheb_interp_matrix

u = 1.0
h = u / 2
parts = sys.argv[1:] or ["check", "h", "a"]


def wall_labels(L, maxwalls):
    """sigma in {+-1}^L with at most maxwalls sign changes."""
    out = []
    for k in range(maxwalls + 1):
        for pos in itertools.combinations(range(1, L), k):
            sg = np.ones(L)
            cur = 1.0
            j = 0
            for i in range(L):
                if j < len(pos) and i == pos[j]:
                    cur = -cur
                    j += 1
                sg[i] = cur
            out.append(sg)
            out.append(-sg)
    return np.array(out)


def block_objects(p, L, sig):
    pi = binary_chain_law(L, p)
    s = spins(L).astype(float)
    lab = -h * (sig @ s.T)
    W, _ = gibbs(pi, lab)
    x = bits(L)
    first, last = x[:, 0], x[:, L - 1]
    sel = np.zeros((4, 1 << L))
    for a in (0, 1):
        for b in (0, 1):
            sel[2 * a + b] = (first == a) & (last == b)
    return pi, W, sel


def mom_lyap_matrices(A, m, t, N=64):
    """Moment Lyapunov exponent of order t of the i.i.d. product of the positive 2x2 matrices
    A[k] with weights m[k]: row vectors y = s (w, 1-w);  y A = s g(w) (w', 1-w').
    Chebyshev collocation on w in [0,1]."""
    wn, xn = cheb_nodes(N, 0.0, 1.0)
    T = np.zeros((N, N))
    for k in range(len(A)):
        if m[k] < 1e-300:
            continue
        y0 = wn * A[k][0, 0] + (1 - wn) * A[k][1, 0]
        y1 = wn * A[k][0, 1] + (1 - wn) * A[k][1, 1]
        g = y0 + y1
        w2 = y0 / g
        T += m[k] * (g ** t)[:, None] * cheb_interp_matrix(xn, np.clip(2 * w2 - 1, -1, 1))
    return float(np.log(np.max(np.linalg.eigvals(T).real)))


def exact_log_Ec(Bm, rho0, m, t, kmax):
    """ln E_{M^k}[ c^t ],  c = 1^T B_1 rho0 B_2 rho0 ... B_k 1,  for k = 1..kmax (exact)."""
    out = []
    Y = Bm.sum(axis=1)                 # rows: y = 1^T B_phi   shape (m,2)
    lw = np.log(np.maximum(m, 1e-300))
    out.append(np.log(np.sum(m * Y.sum(axis=1) ** t)))
    A = np.einsum("ab,kbc->kac", rho0, Bm)       # rho0 B_phi
    for k in range(2, kmax + 1):
        Y = np.einsum("ia,kab->ikb", Y, A).reshape(-1, 2)
        lw = (lw[:, None] + np.log(np.maximum(m, 1e-300))[None, :]).reshape(-1)
        out.append(np.log(np.sum(np.exp(lw) * Y.sum(axis=1) ** t)))
    return out


def prop_I(p, L, t, maxwalls=2, M=None, N=64, verbose=False, detail=False):
    P = np.array([[1 - p, p], [p, 1 - p]])
    rho0 = 2 * P
    sig = wall_labels(L, maxwalls)
    pi, W, sel = block_objects(p, L, sig)
    if M is None:
        br = renyi_bracket(W, t, tol=1e-12, iters=100000)
        M = br["M"]
    mix = M @ W ** t
    r = mix ** (1 / t)
    S = r.sum()
    Q = r / S
    GL = -t * np.log(S)
    Bm = (W @ sel.T).reshape(-1, 2, 2)            # B_phi(a,b)
    BQ = (sel @ Q).reshape(2, 2)
    lamQ = np.max(np.linalg.eigvals(BQ @ rho0).real)
    A = np.einsum("kab,bc->kac", Bm, rho0)        # B_phi rho0
    Lam = mom_lyap_matrices(A, M, t, N)
    val = (GL + Lam - t * np.log(lamQ)) / L
    if detail:
        return dict(val=val, GL=GL, Lam=Lam, lamQ=lamQ, M=M, Bm=Bm, rho0=rho0, sig=sig, nlab=len(sig))
    return val


if "check" in parts:
    t0 = time.time()
    print("=== 1. finite-k identity of Prop. I against the definition ===")
    rng = np.random.default_rng(5)
    worst = 0.0
    for (L, k) in ((3, 2), (3, 3), (2, 4)):
        n = L * k
        for p in (0.4, 0.3, 0.1):
            for t in (0.3, 0.45, 0.8):
                P = np.array([[1 - p, p], [p, 1 - p]]); rho0 = 2 * P
                sig = spins(L).astype(float)                      # all 2^L site-wise labels of the block
                piL, WL, sel = block_objects(p, L, sig)
                ML = rng.dirichlet(np.ones(len(sig)))             # an ARBITRARY (asymmetric) block law
                mixL = ML @ WL ** t
                rL = mixL ** (1 / t); SL = rL.sum(); QL = rL / SL
                GL = -t * np.log(SL)
                Bm = (WL @ sel.T).reshape(-1, 2, 2)
                BQ = (sel @ QL).reshape(2, 2)
                lnEc = exact_log_Ec(Bm, rho0, ML, t, k)[k - 1]
                # E_{Q^k}[prod rho0] = 1^T (B_Q rho0)^(k-1) B_Q 1
                v = np.ones(2) @ BQ
                for _ in range(k - 1):
                    v = v @ rho0 @ BQ
                formula = k * GL + lnEc - t * np.log(v.sum())
                # definition on the n-chain: labels = k-tuples of block labels, M prop. M_L^k c_phi^t
                pin = binary_chain_law(n, p)
                sn = spins(n).astype(float)
                tuples = list(itertools.product(range(len(sig)), repeat=k))
                sigs = np.array([np.concatenate([sig[j] for j in tp]) for tp in tuples])
                Wn, lnZn = gibbs(pin, -h * (sigs @ sn.T))
                # c_phi = Z_phi / prod z_j
                c = np.array([(np.ones(2) @ np.linalg.multi_dot([Bm[tp[0]]] + [rho0 @ Bm[j] for j in tp[1:]])).sum()
                              if k > 1 else Bm[tp[0]].sum() for tp in tuples])
                Mn = np.array([np.prod(ML[list(tp)]) for tp in tuples]) * c ** t
                Mn /= Mn.sum()
                Gdef = -t * np.log(((Mn @ Wn ** t) ** (1 / t)).sum())
                worst = max(worst, abs(Gdef - formula))
    print("   27 cases (L,k) in {(3,2),(3,3),(2,4)}, random asymmetric M_L: largest |definition - formula| = %.2e  (%.1fs)"
          % (worst, time.time() - t0))

if "h" in parts:
    t0 = time.time()
    print("=== 2. lower ends of h from block-wise labels with <= 2 walls per block ===")
    theirs = {0.4: (0.034026, 12, 0.459), 0.3: (0.040115, 14, 0.434), 0.2: (0.044599, 14, 0.409), 0.1: (0.044378, 14, 0.380)}
    hc = cube_exponents(u)[0]
    for p in (0.4, 0.3, 0.2, 0.1):
        v0, L0, t0_ = theirs[p]
        d = prop_I(p, L0, t0_, detail=True)
        d2 = prop_I(p, L0, t0_, N=96, detail=True)
        # exact increments of ln E[c^t] over k = 1,2,3 blocks
        ex = exact_log_Ec(d["Bm"], d["rho0"], d["M"], t0_, 3)
        print("p=%.1f L=%d t=%.3f: %d labels; G_L=%.7f  Lambda_blk=%.7f (N=96: %.7f; exact increments k=2,3: %.7f %.7f)  lam_Q=%.12f"
              % (p, L0, t0_, d["nlab"], d["GL"], d["Lam"], d2["Lam"], ex[1] - ex[0], ex[2] - ex[1], d["lamQ"]))
        # maximise over t at this L
        tb, vb = golden_max(lambda t: prop_I(p, L0, t), max(0.05, t0_ - 0.06), min(0.95, t0_ + 0.06), tol=2e-4)
        print("        bound at Y's (L,t): %.6f (Y: %.6f);  max over t at this L: %.6f at t=%.3f;  ratio to cube %.4f"
              % (d["val"], v0, vb, tb, vb / hc))
        for L in (8, 10, 12, 14):
            if L != L0:
                print("        L=%d, t=%.3f: %.6f" % (L, t0_, prop_I(p, L, t0_)))
    print("time %.1fs" % (time.time() - t0))

if "a" in parts:
    t0 = time.time()
    print("=== 3. lower ends of a = sup_t F_inf(t)/(1-t) from the same family ===")
    theirs_a = {0.4: 0.116817, 0.3: 0.126444, 0.2: 0.129797, 0.1: 0.116632}
    ac = cube_exponents(u)[2]
    for p in (0.4, 0.3, 0.2, 0.1):
        best = (0, None)
        for L in (10, 12, 14):
            for t in (0.9, 0.97, 0.99, 0.997, 0.999):
                v = prop_I(p, L, t) / (1 - t)
                if v > best[0]:
                    best = (v, (L, t))
                print("   p=%.1f L=%d t=%.3f: bound/(1-t) = %.6f" % (p, L, t, v))
        print("p=%.1f  a >= %.6f at (L,t)=%s   (Y: %.6f)   ratio to cube %.4f" % (p, best[0], best[1], theirs_a[p], best[0] / ac))
    print("time %.1fs" % (time.time() - t0))
