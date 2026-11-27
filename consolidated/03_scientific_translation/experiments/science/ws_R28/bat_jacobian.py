"""R28 — numerical check of a remark on item 99 (ii): "with [bond lengths, bond angles] free, the 'sites' are
no longer independent under any natural reference".

Claim checked: in bond-angle-torsion coordinates of an unbranched chain of N atoms the Cartesian volume
element is  (external factor) x prod_{i>=2} b_i^2 db_i x prod_{i>=3} sin(theta_i) dtheta_i x prod_{i>=4} dphi_i,
i.e. a PRODUCT measure over the internal coordinates.  Test: |det d(x)/d(q)| by central differences at random
internal coordinates (external coordinates fixed) divided by prod b_i^2 prod sin theta_i must be constant.
Control: the same ratio with the sin(theta) factors left out, or with b instead of b^2, must NOT be constant.
"""
import r28_common as rc
rc.cap()
import sys
import time
import numpy as np

t0 = time.time()
print("R28 bat_jacobian.py  start", rc.utc())
rng = np.random.default_rng(2807)
N = 6


def rot(a, b, g):
    ca, sa, cb, sb, cg, sg = np.cos(a), np.sin(a), np.cos(b), np.sin(b), np.cos(g), np.sin(g)
    Rz1 = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
    Ry = np.array([[cb, 0, sb], [0, 1, 0], [-sb, 0, cb]])
    Rz2 = np.array([[cg, -sg, 0], [sg, cg, 0], [0, 0, 1]])
    return Rz1 @ Ry @ Rz2


def place(A, B, C, bond, angle, dih):
    bc = (C - B) / np.linalg.norm(C - B)
    n = np.cross(B - A, bc)
    n /= np.linalg.norm(n)
    m = np.cross(n, bc)
    return C + bond * (-np.cos(angle) * bc + np.sin(angle) * np.cos(dih) * m + np.sin(angle) * np.sin(dih) * n)


def cart(q):
    """q = (t (3), euler (3), b2, b3, th3, then (b_i, th_i, phi_i) for i = 4..N)"""
    t, eu = q[:3], q[3:6]
    b2, b3, th3 = q[6:9]
    X = np.zeros((N, 3))
    X[1] = [b2, 0, 0]
    X[2] = X[1] + b3 * np.array([-np.cos(th3), np.sin(th3), 0])
    for i in range(3, N):
        b, th, ph = q[9 + 3 * (i - 3): 12 + 3 * (i - 3)]
        X[i] = place(X[i - 3], X[i - 2], X[i - 1], b, th, ph)
    return (X @ rot(*eu).T + t).ravel()


def sample():
    q = np.empty(3 * N)
    q[:3] = [0.3, -0.2, 0.5]
    q[3:6] = [0.7, 1.1, -0.4]                      # external coordinates fixed
    q[6] = rng.uniform(0.9, 1.8)
    q[7] = rng.uniform(0.9, 1.8)
    q[8] = rng.uniform(0.6, 2.6)
    for i in range(3, N):
        q[9 + 3 * (i - 3)] = rng.uniform(0.9, 1.8)
        q[10 + 3 * (i - 3)] = rng.uniform(0.6, 2.6)
        q[11 + 3 * (i - 3)] = rng.uniform(-np.pi, np.pi)
    return q


def jac_det(q, h=1e-6):
    J = np.empty((3 * N, 3 * N))
    for k in range(3 * N):
        e = np.zeros(3 * N)
        e[k] = h
        J[:, k] = (cart(q + e) - cart(q - e)) / (2 * h)
    return abs(np.linalg.det(J))


r_ok, r_nosin, r_b1 = [], [], []
for s in range(200):
    q = sample()
    d = jac_det(q)
    bs = np.array([q[6], q[7]] + [q[9 + 3 * (i - 3)] for i in range(3, N)])
    ths = np.array([q[8]] + [q[10 + 3 * (i - 3)] for i in range(3, N)])
    r_ok.append(d / (np.prod(bs ** 2) * np.prod(np.sin(ths))))
    r_nosin.append(d / np.prod(bs ** 2))
    r_b1.append(d / (np.prod(bs) * np.prod(np.sin(ths))))
r_ok, r_nosin, r_b1 = map(np.array, (r_ok, r_nosin, r_b1))
print(f"chain of {N} atoms, 200 random internal geometries (bonds 0.9-1.8, angles 34-149 deg, torsions free):")
print(f"  |det J| / (prod b^2 prod sin theta): mean {r_ok.mean():.8f}, relative spread (max-min)/mean {np.ptp(r_ok) / r_ok.mean():.2e}"
      f"  -> constant: {np.ptp(r_ok) / r_ok.mean() < 1e-6}")
print(f"  control, sin(theta) left out: relative spread {np.ptp(r_nosin) / r_nosin.mean():.2e};  control, b in place of b^2: {np.ptp(r_b1) / r_b1.mean():.2e}  (both must be large)")
print("  => the Cartesian volume element is a product measure in bond-angle-torsion coordinates (unbranched chain; numerical evidence, N = 6)")
rc.finish(t0)
