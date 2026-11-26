"""(n) The [N] claim added at the third checkpoint (Summary item 7, section 8.2): "instance A",
a 7-atom chain that is second-moment rigid on F = {15,16,25,27,37} but not universally rigid.

The instance is specified in the report by 4-digit torsions in the authors' dihedral convention
(bond angle 111 deg, unit bonds); the convention is re-implemented here from its formula
(x_i = c - b cos(th) bc + b sin(th) (cos t m + sin t nrm)), everything else is the referee's code.

Checks: stress of (F u E0, X) unique, its eigenvalues; H_c = sum_F c_ij |x_i-x_j|^2 with
c = +-omega|_F: X critical, Hessian on the 4 torsions definite; global maximum over the 4-torus
(grid + multi-start); a 4D framework with the same 16 lengths.
"""
import itertools
import numpy as np
from scipy.optimize import minimize, least_squares

TH = np.deg2rad(111.0)
n = 7
E0 = [(i, i + 1) for i in range(n - 1)] + [(i, i + 2) for i in range(n - 2)]
F = [(0, 4), (0, 5), (1, 4), (1, 6), (2, 6)]
G = E0 + F


def chain_dihedral(tors, b=1.0, th=TH):
    X = np.zeros((len(tors) + 3, 3))
    X[1] = [b, 0, 0]
    X[2] = X[1] + b * np.array([-np.cos(th), np.sin(th), 0.0])
    for i in range(3, len(X)):
        a, bb, c = X[i - 3], X[i - 2], X[i - 1]
        bc = (c - bb) / np.linalg.norm(c - bb)
        nrm = np.cross(bb - a, bc)
        nrm /= np.linalg.norm(nrm)
        m = np.cross(nrm, bc)
        t = tors[i - 3]
        X[i] = c - b * np.cos(th) * bc + b * np.sin(th) * (np.cos(t) * m + np.sin(t) * nrm)
    return X


def chains_batch(T, b=1.0, th=TH):
    """Vectorised version: T has shape (N, 4); returns (N, 7, 3)."""
    N = len(T)
    X = np.zeros((N, n, 3))
    X[:, 1] = [b, 0, 0]
    X[:, 2] = X[:, 1] + b * np.array([-np.cos(th), np.sin(th), 0.0])
    for i in range(3, n):
        a, bb, c = X[:, i - 3], X[:, i - 2], X[:, i - 1]
        bc = c - bb
        bc /= np.linalg.norm(bc, axis=1)[:, None]
        nrm = np.cross(bb - a, bc)
        nrm /= np.linalg.norm(nrm, axis=1)[:, None]
        m = np.cross(nrm, bc)
        t = T[:, i - 3][:, None]
        X[:, i] = c - b * np.cos(th) * bc + b * np.sin(th) * (np.cos(t) * m + np.sin(t) * nrm)
    return X


def sq(X, i, j):
    return ((X[..., i, :] - X[..., j, :]) ** 2).sum(-1)


tors = np.array([1.5174, -1.0463, 2.7120, -1.6744])
X = chain_dihedral(tors)
bl = [np.sqrt(sq(X, i, i + 1)) for i in range(n - 1)]
print("bond lengths", np.round(bl, 12).tolist(), "; 1-3 distances^2", np.round([sq(X, i, i + 2) for i in range(n - 2)], 6).tolist())
# stress
R = np.zeros((len(G), 3 * n))
for r, (i, j) in enumerate(G):
    R[r, 3 * i:3 * i + 3] = X[i] - X[j]
    R[r, 3 * j:3 * j + 3] = X[j] - X[i]
U, s, Vt = np.linalg.svd(R.T)
print("singular values of the rigidity matrix (16 bars, 21 coords):", np.round(s[-3:], 6).tolist(), "-> rank", int((s > 1e-9 * s[0]).sum()), "stress dim", 16 - int((s > 1e-9 * s[0]).sum()))
om = Vt[-1]
Om = np.zeros((n, n))
for wgt, (i, j) in zip(om, G):
    Om[i, i] += wgt; Om[j, j] += wgt; Om[i, j] -= wgt; Om[j, i] -= wgt
ev = np.linalg.eigvalsh(Om)
ev_n = ev / np.abs(ev).max()
print("stress matrix eigenvalues (normalised):", np.round(ev_n, 4).tolist())
omF = om[len(E0):]
for sign in (+1, -1):
    c = sign * omF
    # with Om = sum w_e L_e, tr(V^T Om V) = sum_e w_e |v_i - v_j|^2: energy sum_e w_e d_e^2.
    H = lambda t, c=c: float(sum(ci * sq(chain_dihedral(t), i, j) for ci, (i, j) in zip(c, F)))
    g = np.array([(H(tors + 1e-5 * e) - H(tors - 1e-5 * e)) / 2e-5 for e in np.eye(4)])
    Hs = np.zeros((4, 4))
    h = 1e-4
    for a in range(4):
        for b_ in range(4):
            ea, eb = np.eye(4)[a] * h, np.eye(4)[b_] * h
            Hs[a, b_] = (H(tors + ea + eb) - H(tors + ea - eb) - H(tors - ea + eb) + H(tors - ea - eb)) / (4 * h * h)
    hev = np.linalg.eigvalsh(Hs)
    print(f"c = {'+' if sign > 0 else '-'}omega|_F: |grad| = {np.linalg.norm(g):.1e}; Hessian eigenvalues in torsion coordinates {np.round(hev, 5).tolist()}")
    if hev.max() < 0:
        cmax, Hmax = c, H
norm = np.abs(cmax).max()
cmax = cmax / norm * 1.0
Hx = float(sum(ci * sq(X, i, j) for ci, (i, j) in zip(cmax, F)))
print("couplings c (max |c| = 1):", np.round(cmax, 5).tolist(), " H_c(X) =", round(Hx, 6))


def Hbatch(T):
    Xb = chains_batch(T)
    return sum(ci * sq(Xb, i, j) for ci, (i, j) in zip(cmax, F))


# grid search 40^4
g1 = np.linspace(-np.pi, np.pi, 40, endpoint=False)
best_grid = -np.inf
tops = []
for t0 in g1:
    T = np.array([(t0, a, b_, c_) for a in g1 for b_ in g1 for c_ in g1])
    v = Hbatch(T)
    k = np.argsort(v)[-20:]
    tops += [(v[i], T[i]) for i in k]
    best_grid = max(best_grid, v.max())
print(f"grid 40^4: max H_c = {best_grid:.6f}  (H_c(X) = {Hx:.6f})")
# local maximisation from the best grid points and from random starts
rng = np.random.default_rng(0)
tops.sort(key=lambda p: -p[0])
starts = [p[1] for p in tops[:300]] + [rng.uniform(-np.pi, np.pi, 4) for _ in range(3000)]
maxima = []
negH = lambda t: -float(Hbatch(t[None, :])[0])
for t0 in starts:
    sol = minimize(negH, t0, method="BFGS", options=dict(gtol=1e-10))
    t = (sol.x + np.pi) % (2 * np.pi) - np.pi
    maxima.append((-sol.fun, t))
maxima.sort(key=lambda p: -p[0])
DX = np.array([[sq(X, i, j) for j in range(n)] for i in range(n)])
distinct = []
for val, t in maxima:
    Y = chain_dihedral(t)
    DY = np.array([[sq(Y, i, j) for j in range(n)] for i in range(n)])
    if not any(abs(val - v2) < 1e-7 and np.abs(DY - D2).max() < 1e-5 for v2, D2, _ in distinct):
        distinct.append((val, DY, t))
print(f"{len(starts)} local maximisations: {len(distinct)} distinct local maxima (up to congruence); the top five:")
for val, DY, t in distinct[:5]:
    same = np.abs(DY - DX).max()
    print(f"   H_c = {val:.6f}  torsions {np.round(t, 4).tolist()}  max|D - D(X)| = {same:.2e} {'<- X (or its mirror image)' if same < 1e-5 else ''}")
gap = distinct[0][0] - distinct[1][0]
print(f"margin between the best and the second local maximum: {gap:.5f}; the global maximiser is X: {np.abs(distinct[0][1] - DX).max() < 1e-5}")
# a 4D framework with the same 16 lengths
target = np.array([DX[i, j] for (i, j) in G])
lam, vec = np.linalg.eigh(Om)
pos, neg = vec[:, lam > 1e-9 * np.abs(lam).max()], vec[:, lam < -1e-9 * np.abs(lam).max()]
found = None
for trial in range(200):
    # isotropic vector of Omega as 4th coordinate, then solve
    a = rng.normal(size=pos.shape[1]); bq = rng.normal(size=neg.shape[1])
    qp, qn = pos @ a, neg @ bq
    ep, en = qp @ Om @ qp, -(qn @ Om @ qn)
    q = qp / np.sqrt(ep) + qn / np.sqrt(en)
    hgt = rng.uniform(0.1, 0.6)
    def res(y):
        Y = y.reshape(n, 4)
        r = [((Y[i] - Y[j]) ** 2).sum() - t for (i, j), t in zip(G, target)]
        return np.array(r + list(Y[0]) + [np.std(Y[:, 3]) - hgt * np.std(q)])
    sol = least_squares(res, np.hstack([X, hgt * q[:, None]]).ravel(), xtol=1e-15, ftol=1e-15, gtol=1e-15)
    Y = sol.x.reshape(n, 4)
    sv = np.linalg.svd(Y - Y.mean(0), compute_uv=False)
    if np.abs(sol.fun).max() < 1e-12 and sv[3] > 0.05:
        found = (Y, sv, np.abs(sol.fun).max())
        break
if found:
    Y, sv, r_ = found
    DY = np.array([[((Y[i] - Y[j]) ** 2).sum() for j in range(n)] for i in range(n)])
    print(f"4D framework with the 16 lengths of X: residual {r_:.1e}, singular values {np.round(sv, 3).tolist()}, "
          f"max |D(Y) - D(X)| on unmeasured pairs {max(abs(DY[i,j]-DX[i,j]) for i in range(n) for j in range(i+1,n) if (i,j) not in G):.3f} -> not universally rigid")
else:
    print("no 4D framework found in 200 trials")
