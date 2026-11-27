# b4_identities.py -- REVIEW 6: own checks of the linear identities of CHAIN_GEOMETRY_HARDNESS.md
#  (section 1)  sum_{i<j} c_ij |x_i-x_j|^2 = sum_{k,l} Qt_kl <b_k,b_l>,  Qt_kl = sum_{i<=min} sum_{j>max} c_ij,  and the inverse
#  (Remark of 2a) data with Qt_kl = -1/2 on edges, Qt_kk = deg(k)/2 give sum_E (1 - <b_k,b_l>)
#  (Corollary 5)  G_kl = (m_{k,l+1} + m_{k+1,l} - m_{k,l} - m_{k+1,l+1})/2 is the averaged Gram matrix of the bonds of an
#                 ensemble with data m, and m_ij = sum_{k,l=i}^{j-1} G_kl recovers m;  the cross-polytope is in conv E_1
#  (Theorem 1 proof) |p_v|^2 = (t1^2 + t2^2 - 2 s t1 t2)/(1 - s^2) <= 2 (t1^2 + t2^2) for |s| <= 1/2;  x^2+y^2-xy <= 1 on [0,1]^2
#  (Proposition 4) rotating the tail of a fixed-angle chain about a bond by delta changes every <b_k,b_l> by at most delta,
#                 and <b_k,b_l> depends only on the l-k-1 torsion angles about the bonds strictly between k and l
import itertools, math
import numpy as np
rng = np.random.default_rng(11)
ok = True
for trial in range(200):
    n = int(rng.integers(3, 10))
    c = np.zeros((n + 2, n + 2))
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            c[i, j] = rng.integers(-5, 6)
    Qt = np.zeros((n + 1, n + 1))
    for k in range(1, n):
        for l in range(1, n):
            Qt[k, l] = sum(c[i, j] for i in range(1, min(k, l) + 1) for j in range(max(k, l) + 1, n + 1))
    b = rng.normal(size=(n - 1, 3)); b /= np.linalg.norm(b, axis=1, keepdims=True)
    x = np.vstack([np.zeros(3), np.cumsum(b, axis=0)])
    lhs = sum(c[i, j] * np.sum((x[i - 1] - x[j - 1]) ** 2) for i in range(1, n + 1) for j in range(i + 1, n + 1))
    rhs = np.sum(Qt[1:n, 1:n] * (b @ b.T))
    ok &= abs(lhs - rhs) < 1e-8
    def q(k, l):
        return Qt[k, l] if 1 <= k <= n - 1 and 1 <= l <= n - 1 else 0.0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            ok &= abs(c[i, j] - (q(i, j - 1) - q(i - 1, j - 1) - q(i, j) + q(i - 1, j))) < 1e-9
    # Remark: graph on the bonds
    nb = n - 1
    E = [(k, l) for k in range(nb) for l in range(k + 1, nb) if rng.random() < 0.5]
    Q2 = np.zeros((nb, nb))
    for k, l in E:
        Q2[k, l] = Q2[l, k] = -0.5
        Q2[k, k] += 0.5; Q2[l, l] += 0.5
    ok &= abs(np.sum(Q2 * (b @ b.T)) - sum(1 - b[k] @ b[l] for k, l in E)) < 1e-9
    # Corollary 5
    m = np.array([[np.sum((x[i] - x[j]) ** 2) for j in range(n)] for i in range(n)])
    G = np.eye(nb)
    for k in range(nb):
        for l in range(nb):
            G[k, l] = 0.5 * (m[k, l + 1] + m[k + 1, l] - m[k, l] - m[k + 1, l + 1])
    ok &= np.allclose(G, b @ b.T)
    for i in range(n):
        for j in range(i + 1, n):
            ok &= abs(m[i, j] - G[i:j, i:j].sum()) < 1e-9
    # projection bound and the corner inequality
    z1 = rng.normal(size=3); z1 /= np.linalg.norm(z1)
    s = rng.uniform(-0.5, 0.5)
    w = np.cross(z1, rng.normal(size=3)); w /= np.linalg.norm(w)
    z2 = s * z1 + math.sqrt(1 - s * s) * w
    u = rng.normal(size=3); u /= np.linalg.norm(u)
    t1, t2 = u @ z1, u @ z2
    e = np.cross(z1, z2); e /= np.linalg.norm(e)
    p2 = 1 - (u @ e) ** 2
    ok &= abs(p2 - (t1 * t1 + t2 * t2 - 2 * s * t1 * t2) / (1 - s * s)) < 1e-9 and p2 <= 2 * (t1 * t1 + t2 * t2) + 1e-12
    xx, yy = rng.random(2)
    ok &= xx * xx + yy * yy - xx * yy <= 1 + 1e-15
# cross-polytope vertex as an average of cut matrices
nb = 5
for k, l in itertools.combinations(range(nb), 2):
    for sign in (1, -1):
        M = np.zeros((nb, nb)); cnt = 0
        for xs in itertools.product((1, -1), repeat=nb):
            if xs[k] == sign * xs[l]:
                v = np.array(xs, float); M += np.outer(v, v); cnt += 1
        M /= cnt
        T = np.eye(nb); T[k, l] = T[l, k] = sign
        ok &= np.allclose(M, T)
# Proposition 4: torsion perturbation
def chain_from_torsions(theta, tors):
    b = [np.array([0.0, 0.0, 1.0]), np.array([math.sin(theta), 0.0, math.cos(theta)])]
    for tau in tors:
        a, bb = b[-2], b[-1]
        # next bond: angle theta with bb, dihedral tau relative to a
        e1 = a - (a @ bb) * bb; e1 /= np.linalg.norm(e1)
        e2 = np.cross(bb, e1)
        b.append(math.cos(theta) * bb - math.sin(theta) * (math.cos(tau) * e1 + math.sin(tau) * e2))
    return np.array(b)
worst = 0.0
dep_ok = True
for trial in range(300):
    theta = rng.uniform(0.2, math.pi - 0.2)
    nt = 8
    tors = rng.uniform(0, 2 * math.pi, size=nt)
    B0 = chain_from_torsions(theta, tors)
    ok &= np.allclose([B0[k] @ B0[k + 1] for k in range(len(B0) - 1)], math.cos(theta))
    j = int(rng.integers(0, nt)); delta = rng.uniform(0, 0.5)
    t2 = tors.copy(); t2[j] += delta
    B1 = chain_from_torsions(theta, t2)
    G0, G1 = B0 @ B0.T, B1 @ B1.T
    worst = max(worst, np.abs(G1 - G0).max() / delta)
    # torsion j is the one about bond j+1 (0-based bonds 0..nt+1): only pairs (k,l) with k <= j < j+2 <= l may change
    for k in range(len(B0)):
        for l in range(k + 1, len(B0)):
            if not (k <= j and l >= j + 2):
                dep_ok &= abs(G1[k, l] - G0[k, l]) < 1e-9
print("identities of sections 1, 2a (Remark), 2b and the two elementary bounds of the proof of Theorem 1:", bool(ok))
print(f"Proposition 4: max |change of <b_k,b_l>| / delta over 300 single-torsion perturbations = {worst:.4f} (<= 1); "
      f"only pairs with the torsion strictly between them change: {dep_ok}")
