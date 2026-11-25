"""Step 3(b) -- lower bounds from label laws that are i.i.d. over blocks of L sites (labels of a block: site-wise, with at most
w domain walls), tilted by c_phi^t, with the EXACT boundary correction:

   F_inf(t)  >=  [ G_L(M_L) + Lam_blk(t) - t ln lam_max(B_Q rho0) ] / L,
   G_L(M_L) = -t ln sum_x (sum_phi M_L(phi) pi_{L,phi}(x)^t)^(1/t)        (block of L sites, stationary law, plain slopes u)
   B_phi(a,b) = pi_{L,phi}(first letter a, last letter b),  B_Q the same for the centre Q of M_L,  rho0 = 2 P (transition matrix),
   Lam_blk(t) = moment Lyapunov exponent of order t of the i.i.d. product of the 2x2 matrices B_phi rho0, phi ~ M_L.
(1) validation of the finite-k identity and of the moment Lyapunov routine by brute force; (2) the bounds.
usage: python3 y07_block_labels.py [p ...]"""
import sys, time, math, itertools
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ylib import *
from ylyap import _cheb, _interp, G_inf

t0 = time.time(); u = 1.0; h = u / 2

def moment_lyap_general(mats, probs, r, N=40):
    zc = [0.5 * math.log(A[0, j] / A[1, j]) for A in mats for j in (0, 1)]
    a, b = min(zc), max(zc)
    if b - a < 1e-9: a -= 1e-6; b += 1e-6
    nodes, w = _cheb(N, a, b); ez = np.exp(nodes); T = np.zeros((N, N))
    for A, pr in zip(mats, probs):
        y1 = A[0, 0] * ez + A[0, 1] / ez; y2 = A[1, 0] * ez + A[1, 1] / ez
        T += pr * (np.sqrt(y1 * y2) ** r)[:, None] * _interp(nodes, w, 0.5 * np.log(y1 / y2))
    return math.log(float(np.max(np.linalg.eigvals(T).real)))

def spins(L):
    return np.array([[1.0 - 2 * b for b in bits(x, L)] for x in range(2 ** L)])       # site i = column i; x = 0 is all +

def block_data(L, p, labels, t, M=None, tol=1e-10):
    """labels: array (nl, L) of +-1.  Returns per-site bound pieces."""
    Kp = 0.5 * math.log((1 - p) / p); S = spins(L)
    lpi = Kp * (S[:, :-1] * S[:, 1:]).sum(axis=1) if L > 1 else np.zeros(2 ** L)
    W = lpi[None, :] + h * (labels @ S.T); W -= W.max(axis=1, keepdims=True)
    P = np.exp(W); P /= P.sum(axis=1, keepdims=True)
    if M is None:
        lo, up, M, Q = renyi_F(P, t, tol=tol, itmax=min(40000, 300 + int(3e8 / P.size)))
    s = M @ P ** t; NL = float((s ** (1 / t)).sum()); Q = s ** (1 / t) / NL; GL = -t * math.log(NL)
    fa = (S[:, 0] < 0).astype(int); la = (S[:, -1] < 0).astype(int)                   # letter index 0 = '+', 1 = '-'
    def Bmat(v):
        B = np.zeros((2, 2)); np.add.at(B, (fa, la), v); return B
    rho0 = 2 * np.array([[1 - p, p], [p, 1 - p]])
    keep = M > 1e-12
    mats = [Bmat(P[k]) @ rho0 for k in np.where(keep)[0]]; probs = M[keep] / M[keep].sum()
    lamQ = float(np.max(np.linalg.eigvals(Bmat(Q) @ rho0).real))
    return GL, mats, probs, lamQ, M, P, Q

def bound(L, p, labels, t, M=None):
    GL, mats, probs, lamQ, M, P, Q = block_data(L, p, labels, t, M)
    lam = moment_lyap_general(mats, probs, t)
    return (GL + lam - t * math.log(lamQ)) / L, GL / L, M

def wall_labels(L, w):
    """site-wise labels of a block with at most w domain walls (both signs)"""
    out = []
    for k in range(w + 1):
        for pos in itertools.combinations(range(1, L), k):
            s = np.ones(L); sign = 1.0; j = 0
            for i in range(L):
                if j < len(pos) and i == pos[j]: sign = -sign; j += 1
                s[i] = sign
            out.append(s); out.append(-s)
    return np.array(out)

# ------------------------------------------------------------------ (1) validation
print("(1) validation")
p = 0.3; t = 0.43; L = 3
labels = np.array(list(itertools.product((1.0, -1.0), repeat=L)))
GL, mats, probs, lamQ, M, P, Q = block_data(L, p, labels, t)
nl = len(labels); S1 = spins(L); Kp = 0.5 * math.log((1 - p) / p)
for k in (2, 3):
    n = k * L; S = spins(n)
    lpi = Kp * (S[:, :-1] * S[:, 1:]).sum(axis=1)
    idx = list(itertools.product(range(nl), repeat=k))
    lab = np.array([np.concatenate([labels[i] for i in tup]) for tup in idx])
    W = lpi[None, :] + h * (lab @ S.T); W -= W.max(axis=1, keepdims=True); Pn = np.exp(W); Pn /= Pn.sum(axis=1, keepdims=True)
    # c_phi by matrices
    rho0 = 2 * np.array([[1 - p, p], [p, 1 - p]])
    fa = (S1[:, 0] < 0).astype(int); la = (S1[:, -1] < 0).astype(int)
    def Bm(v):
        B = np.zeros((2, 2)); np.add.at(B, (fa, la), v); return B
    Bs = [Bm(P[i]) for i in range(nl)]; BQ = Bm(Q)
    cphi = []
    for tup in idx:
        x = Bs[tup[-1]] @ np.ones(2)
        for i in tup[-2::-1]: x = Bs[i] @ (rho0 @ x)
        cphi.append(x.sum())
    cphi = np.array(cphi); Mprod = np.array([math.prod(M[i] for i in tup) for tup in idx])
    Mn = Mprod * cphi ** t; Nprime = Mn.sum(); Mn /= Nprime
    brute = -t * math.log(float(((Mn @ Pn ** t) ** (1 / t)).sum()))
    x = BQ @ np.ones(2)
    for _ in range(k - 1): x = BQ @ (rho0 @ x)
    formula = k * GL + math.log(Nprime) - t * math.log(x.sum())
    print("  L=%d, k=%d (n=%d, %d labels): brute-force Renyi form %.12f; formula k G_L + ln E[c^t] - t ln E_Q[R] = %.12f" % (L, k, n, len(idx), brute, formula))
# the Lyapunov routine against exact growth for a few matrices
mats2 = mats[:4]; pr2 = np.array(probs[:4]) / sum(probs[:4]); r = t
ex = []
for k in (9, 10):
    tot = 0.0
    for tup in itertools.product(range(4), repeat=k):
        x = np.ones(2)
        for i in tup: x = mats2[i] @ x
        tot += math.prod(pr2[i] for i in tup) * x.sum() ** r
    ex.append(math.log(tot))
print("  moment Lyapunov, 4 matrices, order %.2f: operator %.10f; exact increment k=9->10: %.10f" % (r, moment_lyap_general(mats2, pr2, r), ex[1] - ex[0]))

# ------------------------------------------------------------------ (2) bounds
PS = [float(x) for x in sys.argv[1:]] or [0.4, 0.3, 0.2, 0.1]
TSTAR = {0.4: 0.458, 0.3: 0.431, 0.2: 0.402, 0.1: 0.364}
hc, ac, Ec = cube_numbers(u)
print("\n(2) bounds per site (cube h = %.6f, a = %.6f)" % (hc, ac))
for p in PS:
    t = TSTAR[p]
    gm = max(G_inf(t, c, p, u) for c in np.linspace(0, 2, 41))
    print("p=%.1f, t=%.3f: tilted Markov (Lyapunov) %.6f" % (p, t, gm))
    best = (0, None)
    for w, Ls in ((0, range(2, 19)), (1, range(4, 17, 2)), (2, range(6, 15, 2))):
        row = []
        for L in Ls:
            b, g, M = bound(L, p, wall_labels(L, w), t)
            row.append("L=%d: %.6f" % (L, b))
            if b > best[0]: best = (b, (w, L))
        print("   <=%d walls per block: %s" % (w, "  ".join(row)))
    w, L = best[1]
    # refine t at the best structure
    f = lambda tt: bound(L, p, wall_labels(L, w), tt)[0]
    tt, hb = golden_max(f, max(t - 0.08, 0.05), min(t + 0.08, 0.95), it=18)
    print("   best: <=%d walls, L=%d: %.6f at t=%.3f;  after refining t: h >= %.6f at t=%.3f   (x%.3f of the cube)  [%.0f s]" % (w, L, best[0], t, hb, tt, hb / hc, time.time() - t0))
    # a: (bound at t)/(1-t) for t near 1
    arow = []
    for tt in (0.9, 0.97, 0.99):
        ab = max((bound(LL, p, wall_labels(LL, ww), tt)[0] / (1 - tt), ww, LL) for ww, LLs in ((0, (2, 3, 4, 6, 8)), (1, (4, 6, 8, 10)), (2, (6, 8, 10))) for LL in LLs)
        arow.append("t=%.2f: %.6f (<=%d walls, L=%d)" % (tt, ab[0], ab[1], ab[2]))
    print("   a >= " + ";  ".join(arow) + "   [%.0f s]" % (time.time() - t0))
print("%.1f s" % (time.time() - t0))
