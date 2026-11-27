"""r10_11: the small-slope law and its test on other chains.  Own derivation (R10_REPORT 2.9):

   for a finite space (X, pi) and a SYMMETRIC envelope d = u d0,
        F*_X(t) = (t(1-t)/2) u^2 V + O(u^3),   V := max{ Var_pi(f) : f in Lip(d0) },
   hence  E ~ a ~ u^2 V / 2,  h ~ u^2 V / 8;  V is attained at a vertex of the Lipschitz polytope.

 1. binary symmetric chain (ferro p<1/2, antiferro p>1/2): V over ALL vertices, n<=5, against
    (1/4)Var(m) resp. (1/4)Var(staggered m); convergence of F*_4(t;u)/(u^2 t(1-t)/2) to V.
 2. a frustrated binary chain (nn ferro + nnn antiferro): V against the best site-wise label and
    against the zero-wave-vector value (1/4)Var(m).
 3. three-letter Potts chain (n = 2, 3): V over all integer Lipschitz functions of the Hamming
    graph H(n,3), against Var(number of sites in letter a) and the product measure.
 4. helix-coil (Zimm-Bragg) chain, n = 5: V against (1/4)Var(number of helical residues ... ) and
    the thermodynamic factor (1+lam)/(1-lam).
"""
import itertools
import time
import numpy as np
from r10lib import *

t0 = time.time()


def variances(pi, F):
    mean = F @ pi
    return (F * F) @ pi - mean ** 2


# ---------------------------------------------------------------------------------- 1
print("1. binary symmetric chain: V_n = max over ALL vertices of Var_pi(f) (unit slope)")
for p in (0.4, 0.3, 0.1, 0.7):
    lam = 1 - 2 * p
    for n in (3, 4, 5):
        pi = binary_chain_law(n, p)
        V = hom_vertices(n).astype(float)
        var = variances(pi, V)
        k = int(np.argmax(var))
        s = spins(n).astype(float)
        m = s.sum(axis=1)
        mst = (s * ((-1.0) ** np.arange(n))[None, :]).sum(axis=1)
        vm = 0.25 * variances(pi, m[None, :])[0]
        vs = 0.25 * variances(pi, mst[None, :])[0]
        f = V[k] - V[k][0]
        # is the maximiser a site-wise label?
        c = np.array([f[1 << i] for i in range(n)])
        additive = np.allclose(f, bits(n).astype(float) @ c)
        print("   p=%.1f n=%d: V_n = %.6f (maximiser additive: %s, signs %s);  (1/4)Var(m) = %.6f;  (1/4)Var(m_stag) = %.6f;  V_n/(n/4) = %.4f;  chi=(1+|lam|)/(1-|lam|) = %.4f"
              % (p, n, var[k], additive, (-c).astype(int).tolist(), vm, vs, var[k] / (n / 4), (1 + abs(lam)) / (1 - abs(lam))))
print("   convergence of F*_4(t;u) / (u^2 t(1-t)/2) to V_4 (all 990 vertices):")
for p in (0.3, 0.7):
    pi = binary_chain_law(4, p)
    V = hom_vertices(4).astype(float)
    V4 = variances(pi, V).max()
    for t in (0.3, 0.6):
        row = []
        for u in (0.4, 0.2, 0.1, 0.05):
            W, _ = gibbs(pi, u * V)
            br = renyi_bracket(W, t, tol=1e-13, iters=200000)
            row.append("u=%.2f: %.5f" % (u, br["upper"] / (u * u * t * (1 - t) / 2)))
        print("      p=%.1f t=%.1f: %s   -> V_4 = %.5f" % (p, t, "  ".join(row), V4))

# ---------------------------------------------------------------------------------- 2
print("2. frustrated binary chain  pi ~ exp(J1 sum s_i s_{i+1} + J2 sum s_i s_{i+2}),  n = 5, all 395094 vertices")
n = 5
s = spins(n).astype(float)
V5 = hom_vertices(n).astype(float)
for (J1, J2) in ((0.5, 0.0), (0.5, -0.5), (0.3, -0.8), (-0.4, -0.6)):
    en = J1 * (s[:, 1:] * s[:, :-1]).sum(axis=1) + J2 * (s[:, 2:] * s[:, :-2]).sum(axis=1)
    pi = np.exp(en); pi /= pi.sum()
    var = variances(pi, V5)
    k = int(np.argmax(var))
    C = (s * pi[:, None]).T @ s                       # <s_i s_j>  (means vanish by symmetry)
    vals = 0.25 * np.einsum('ki,ij,kj->k', s, C, s)
    best_sw = (float(vals.max()), s[int(np.argmax(vals))])
    vm = 0.25 * np.ones(n) @ C @ np.ones(n)
    f = V5[k] - V5[k][0]
    c = np.array([f[1 << i] for i in range(n)])
    additive = np.allclose(f, bits(n).astype(float) @ c)
    print("   J1=%+.1f J2=%+.1f: V_5 = %.6f (maximiser additive: %s);  best site-wise label %.6f (signs %s);  zero wave vector (1/4)Var(m) = %.6f;  product measure n/4 = %.4f"
          % (J1, J2, var[k], additive, best_sw[0], best_sw[1].astype(int).tolist(), vm, n / 4))

# ---------------------------------------------------------------------------------- 3
print("3. three-letter Potts chain  pi ~ exp(J sum 1[x_i = x_{i+1}]),  Hamming envelope, unit slope")


def hamming_graph(n, q=3):
    pts = list(itertools.product(range(q), repeat=n))
    idx = {x: i for i, x in enumerate(pts)}
    nb = [[] for _ in pts]
    for x in pts:
        for i in range(n):
            for a in range(q):
                if a != x[i]:
                    y = x[:i] + (a,) + x[i + 1:]
                    nb[idx[x]].append(idx[y])
    return pts, nb


def integer_lipschitz(nb):
    """All integer f with f[0]=0 and |f(x)-f(y)| <= 1 on every edge (DFS in BFS order)."""
    N = len(nb)
    order = [0]; seen = {0}
    for v in order:
        for w in nb[v]:
            if w not in seen:
                seen.add(w); order.append(w)
    pos = {v: i for i, v in enumerate(order)}
    earlier = [[w for w in nb[v] if pos[w] < pos[v]] for v in range(N)]
    out = []
    f = np.zeros(N, dtype=np.int8)

    def rec(i):
        if i == N:
            out.append(f.copy()); return
        v = order[i]
        lo = max(f[w] for w in earlier[v]) - 1
        hi = min(f[w] for w in earlier[v]) + 1
        for val in range(lo, hi + 1):
            f[v] = val
            rec(i + 1)
    rec(1)
    return np.array(out)


for n in (2,):
    pts, nb = hamming_graph(n)
    tt = time.time()
    F = integer_lipschitz(nb).astype(float)
    X = np.array(pts)
    print("   n=%d: %d integer Lipschitz functions of H(%d,3)  (%.1fs)" % (n, len(F), n, time.time() - tt))
    for J in (0.0, 0.7, 1.5, -1.0):
        en = J * (X[:, 1:] == X[:, :-1]).sum(axis=1)
        pi = np.exp(en); pi /= pi.sum()
        var = variances(pi, F)
        k = int(np.argmax(var))
        # candidates: N_a = number of sites in letter 0;  best site-wise label sum_i +-1[x_i = a_i]
        Na = (X == 0).sum(axis=1).astype(float)
        vNa = variances(pi, Na[None, :])[0]
        best_sw = 0.0
        for letters in itertools.product(range(3), repeat=n):
            for sg in itertools.product((1.0, -1.0), repeat=n):
                g = sum(sg[i] * (X[:, i] == letters[i]) for i in range(n)).astype(float)
                best_sw = max(best_sw, variances(pi, g[None, :])[0])
        lam2 = (np.exp(J) - 1) / (np.exp(J) + 2)
        pred = (2 / 9) * (n + 2 * sum((n - k_) * lam2 ** k_ for k_ in range(1, n)))
        print("      J=%+.1f: V_n = %.6f;  Var(N_a) = %.6f (formula (2/9) sum lam2^|i-j| = %.6f);  best site-wise label %.6f;  product measure n*2/9 = %.4f;  V_n/(n 2/9) = %.4f;  (1+lam2)/(1-lam2) = %.4f"
              % (J, var[k], vNa, pred, best_sw, n * 2 / 9, var[k] / (n * 2 / 9), (1 + lam2) / (1 - lam2)))
    if n == 2:
        # small-slope convergence with the true vertex set (connected tight graph)
        def tight_connected(f):
            N = len(f); seen = {0}; st = [0]
            while st:
                v = st.pop()
                for w in nb[v]:
                    if w not in seen and abs(f[v] - f[w]) == 1:
                        seen.add(w); st.append(w)
            return len(seen) == N
        Vx = np.array([f for f in F if tight_connected(f)])
        J = 0.7
        en = J * (X[:, 1:] == X[:, :-1]).sum(axis=1); pi = np.exp(en); pi /= pi.sum()
        Vn = variances(pi, Vx).max()
        row = []
        for u in (0.4, 0.2, 0.1, 0.05):
            W, _ = gibbs(pi, u * Vx)
            br = renyi_bracket(W, 0.4, tol=1e-13, iters=200000)
            row.append("u=%.2f: %.5f" % (u, br["upper"] / (u * u * 0.4 * 0.6 / 2)))
        print("      n=2, J=0.7: %d vertices; F*(0.4;u)/(u^2 t(1-t)/2): %s  -> V = %.5f" % (len(Vx), "  ".join(row), Vn))

# ---------------------------------------------------------------------------------- 4
print("4. helix-coil chain (Zimm-Bragg weights: coil 1, helix after helix s, helix after coil sigma*s), n = 5, all vertices")
n = 5
x = bits(n)                                           # 1 = helix, 0 = coil
for (sZ, sig) in ((1.0, 1e-2), (1.0, 1e-3), (1.3, 1e-3), (0.7, 1e-2)):
    w = np.ones(1 << n)
    for i in range(n):
        prev = x[:, i - 1] if i > 0 else np.zeros(1 << n, dtype=np.int8)
        w *= np.where(x[:, i] == 1, np.where(prev == 1, sZ, sig * sZ), 1.0)
    pi = w / w.sum()
    var = variances(pi, V5)
    k = int(np.argmax(var))
    nh = x.sum(axis=1).astype(float)
    vNh = variances(pi, nh[None, :])[0]
    theta = float(pi @ nh) / n
    lam_p = ((1 + sZ) + np.sqrt((1 - sZ) ** 2 + 4 * sig * sZ)) / 2
    lam_m = ((1 + sZ) - np.sqrt((1 - sZ) ** 2 + 4 * sig * sZ)) / 2
    r = lam_m / lam_p
    f = V5[k] - V5[k][0]
    c = np.array([f[1 << i] for i in range(n)])
    additive = np.allclose(f, bits(n).astype(float) @ c)
    print("   s=%.1f sigma=%.0e: helicity %.3f; V_5 = %.6f (maximiser additive: %s, signs %s);  Var(N_helix) = %.6f;  bulk factor (1+r)/(1-r) = %.1f  (1/sqrt(sigma) = %.1f)"
          % (sZ, sig, theta, var[k], additive, c.astype(int).tolist(), vNh, (1 + r) / (1 - r), 1 / np.sqrt(sig)))
# ---------------------------------------------------------------------------------- 3b
print("3b. Potts chain, n = 3 and 4: V_n by LP ascent (successive linearisation of the variance over the Lipschitz polytope; local maxima, 40 starts) -- a LOWER estimate of V_n")
from scipy.optimize import linprog
rng = np.random.default_rng(3)
for n in (3, 4):
    pts, nb = hamming_graph(n)
    X = np.array(pts); N = len(pts)
    rows = []; 
    for v in range(N):
        for w in nb[v]:
            r = np.zeros(N); r[v] = 1.0; r[w] = -1.0; rows.append(r)
    A = np.array(rows); b = np.ones(len(rows))
    Aeq = np.zeros((1, N)); Aeq[0, 0] = 1.0
    for J in (0.7, 1.5, -1.0):
        en = J * (X[:, 1:] == X[:, :-1]).sum(axis=1); pi = np.exp(en); pi /= pi.sum()
        best = 0.0
        for start in range(40):
            f = rng.normal(size=N)
            val = -1.0
            for it in range(50):
                g = pi * (f - f @ pi)
                res = linprog(-g, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=[0.0], bounds=[(None, None)] * N, method="highs")
                f2 = res.x
                v2 = float(pi @ f2 ** 2 - (pi @ f2) ** 2)
                if v2 <= val + 1e-12:
                    break
                f, val = f2, v2
            best = max(best, val)
        Na = (X == 0).sum(axis=1).astype(float)
        vNa = float(pi @ Na ** 2 - (pi @ Na) ** 2)
        lam2 = (np.exp(J) - 1) / (np.exp(J) + 2)
        print("   n=%d J=%+.1f: best local maximum of the variance %.6f;  Var(N_a) = %.6f;  ratio to the product measure (n 2/9): %.4f;  finite-n structure-factor sum %.4f;  bulk (1+lam2)/(1-lam2) = %.4f"
              % (n, J, best, vNa, best / (n * 2 / 9), (n + 2 * sum((n - k_) * lam2 ** k_ for k_ in range(1, n))) / n, (1 + lam2) / (1 - lam2)))
print("time %.0fs" % (time.time() - t0))
