#!/usr/bin/env python3
"""Workstream R27, Item 1 -- Lemma P (Procrustes-Gram inequality) and Lemma Q (a window with complete distance data).
REPLICATION with own code written from the statements; adversarial search for the supremum of each ratio; the reflection
example of SCI-REV-0023 section 5 in Lemma Q.

  Lemma P:  min_{R in O(r)} ||U - X R||_F^2  <=  ||U U^T - X X^T||_F^2 / (2 (sqrt2 - 1) sigma_r(X)^2)
  Lemma Q:  ||Y_S - X_S R - 1 t^T||_F <= kappa e / s,  kappa = 1/(2 sqrt(sqrt2 - 1)),  e = l2 norm of eta over the pairs of S,
            s = sigma_3 of the centred window.
Controls (must fail): Lemma P without the factor (sqrt2 - 1); Lemma Q with kappa -> 1/2 (the first-order constant);
Lemma Q with proper rotations only; Lemma Q with sigma_2 in place of sigma_3.

Run:  OMP_NUM_THREADS=1 python3 -B item1_lemmas.py > item1_lemmas_<stamp>.log
"""
import os, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import minimize
from r27lib import cap_memory, peak_mb, now, KAPPA, helix, angle_chain, random_unit_chain, procrustes, procrustes_proper, sigma3

cap_memory(2.0)
t0 = time.time()
rng = np.random.default_rng(271)
C_P = 2 * (np.sqrt(2) - 1)
print(f"R27 item1_lemmas.py started {now()}   kappa = {KAPPA:.9f}  (claimed < 0.777: {KAPPA < 0.777});  2(sqrt2-1) = {C_P:.9f}")


# ----------------------------------------------------------------------------------------------------------------------
# Lemma P
# ----------------------------------------------------------------------------------------------------------------------
def proc_general(X, U):
    """min over R in O(r) of ||U - X R||_F (no centring)"""
    A, S, Bt = np.linalg.svd(X.T @ U)
    R = A @ Bt
    return np.linalg.norm(U - X @ R)


def ratio_P(X, U, const=C_P):
    """LHS/RHS of Lemma P (squared form)"""
    sr = np.linalg.svd(X, compute_uv=False)[-1]
    lhs = proc_general(X, U) ** 2
    rhs = np.linalg.norm(U @ U.T - X @ X.T) ** 2 / (const * sr ** 2)
    return lhs, rhs


print("\n[P1] Lemma P on random pairs (m x r), U arbitrary: Gaussian, X + small/large noise, collapsed, rank-deficient, column-reflected,")
print("     orthogonal complement, X ill-conditioned")
nP = 0; worst = 0.0; viol = 0; ctl_viol = 0
for m, r in ((1, 1), (2, 1), (3, 1), (2, 2), (3, 2), (3, 3), (4, 3), (5, 3), (8, 3), (6, 4), (10, 5)):
    for trial in range(2000):
        X = rng.normal(size=(m, r))
        if trial % 5 == 0:
            X = X @ np.diag(10.0 ** rng.uniform(-3, 0, size=r))          # ill-conditioned
        kind = trial % 8
        if kind == 0:
            U = rng.normal(size=(m, r)) * 10.0 ** rng.uniform(-3, 2)
        elif kind == 1:
            U = X + 10.0 ** rng.uniform(-8, -1) * rng.normal(size=(m, r))
        elif kind == 2:
            U = X + 10.0 ** rng.uniform(-1, 1) * rng.normal(size=(m, r))
        elif kind == 3:
            U = np.zeros((m, r))
        elif kind == 4:
            U = np.outer(rng.normal(size=m), rng.normal(size=r))          # rank one
        elif kind == 5:
            U = X @ np.diag(rng.choice([-1.0, 1.0], size=r)) * rng.uniform(0.5, 1.5)
        elif kind == 6:
            # collapse the weakest direction of X (close to the equality case when m > r)
            Us, Ss, Vts = np.linalg.svd(X, full_matrices=True)
            p = Vts[-1]
            U = X - np.outer(X @ p, p)
            if m > r:
                U = U + np.outer(Us[:, -1], p) * Ss[r - 1] * rng.uniform(0.3, 1.0)
        else:
            U = X @ np.linalg.qr(rng.normal(size=(r, r)))[0] + 1e-3 * rng.normal(size=(m, r))
        lhs, rhs = ratio_P(X, U)
        nP += 1
        if rhs > 1e-18:
            worst = max(worst, lhs / rhs)
        if lhs > rhs * (1 + 1e-9) + 1e-18:
            viol += 1
        lhs0, rhs0 = ratio_P(X, U, const=2.0)                              # control: factor (sqrt2 - 1) dropped
        if lhs0 > rhs0 * (1 + 1e-9) + 1e-18:
            ctl_viol += 1
print(f"     pairs: {nP}   violations: {viol}   max LHS/RHS: {worst:.6f}   CONTROL (factor sqrt2-1 dropped) violated by {ctl_viol} pairs")

print("\n[P2] the equality case derived in the review:  U = X - X p p^T + w p^T,  p = weakest right singular vector of X,")
print("     w orthogonal to the columns of X, |w|^2 = (sqrt2 - 1) sigma_r^2   (needs m >= r + 1)")
worst_eq = 0.0
for m, r in ((2, 1), (3, 1), (4, 3), (5, 3), (4, 2), (9, 4)):
    for trial in range(200):
        X = rng.normal(size=(m, r)) @ np.diag(10.0 ** rng.uniform(-1, 0, size=r))
        Us, Ss, Vts = np.linalg.svd(X, full_matrices=True)
        p = Vts[-1]
        w = Us[:, -1] * np.sqrt(np.sqrt(2) - 1) * Ss[r - 1]
        U = X - np.outer(X @ p, p) + np.outer(w, p)
        lhs, rhs = ratio_P(X, U)
        worst_eq = max(worst_eq, abs(lhs / rhs - 1))
print(f"     max |LHS/RHS - 1| over 1200 instances: {worst_eq:.2e}  -> the constant 2(sqrt2 - 1) is attained: Lemma P is sharp for every X")

print("\n[P3] adversarial: maximise LHS/RHS over U by L-BFGS from random starts, X random (m x r)")
for m, r in ((3, 3), (4, 3), (5, 3)):
    best = 0.0
    for trial in range(40):
        X = rng.normal(size=(m, r))
        f = lambda u: -np.log(max(ratio_P(X, u.reshape(m, r))[0], 1e-300) / max(ratio_P(X, u.reshape(m, r))[1], 1e-300))
        res = minimize(f, rng.normal(size=m * r), method="L-BFGS-B", options=dict(maxiter=400))
        lhs, rhs = ratio_P(X, res.x.reshape(m, r))
        best = max(best, lhs / rhs)
    print(f"     m = {m}, r = {r}: sup found {best:.6f}" + ("   (m = r: U cannot leave the column space of X)" if m == r else ""))


# ----------------------------------------------------------------------------------------------------------------------
# Lemma Q
# ----------------------------------------------------------------------------------------------------------------------
def eta_full(XS, YS):
    m = len(XS)
    iu = np.triu_indices(m, 1)
    dx = XS[iu[0]] - XS[iu[1]]
    dy = YS[iu[0]] - YS[iu[1]]
    return np.einsum("ij,ij->i", dy - dx, dy + dx)


def ratio_Q(XS, YS, kappa=KAPPA, which=2, proper=False):
    """(LHS, RHS) of Lemma Q;  which = index of the singular value used (2 = sigma_3)"""
    sv = np.linalg.svd(XS - XS.mean(0), compute_uv=False)
    s = sv[which]
    e = np.linalg.norm(eta_full(XS, YS))
    res = (procrustes_proper if proper else procrustes)(XS, YS)[2]
    return np.linalg.norm(res), kappa * e / s


def random_Y(XS, rng, kind):
    m = len(XS)
    if kind == 0:
        return XS + 10.0 ** rng.uniform(-8, -2) * rng.normal(size=XS.shape)
    if kind == 1:
        return XS + 10.0 ** rng.uniform(-2, 1) * rng.normal(size=XS.shape)
    if kind == 2:
        return rng.normal(size=XS.shape) * 10.0 ** rng.uniform(-2, 2)
    if kind == 3:
        return np.zeros_like(XS)
    if kind == 4:
        u = rng.normal(size=3); u /= np.linalg.norm(u)
        return (XS - XS.mean(0)) @ (np.eye(3) - np.outer(u, u))            # planar projection
    if kind == 5:
        return (XS @ np.diag([1, 1, -1.0])) @ np.linalg.qr(rng.normal(size=(3, 3)))[0] + rng.normal(size=3)   # mirror image
    if kind == 6:
        Y = XS.copy(); k = rng.integers(m); Y[k] += rng.normal(size=3) * 10.0 ** rng.uniform(-1, 3); return Y
    if kind == 7:
        u = rng.normal(size=3); u /= np.linalg.norm(u)
        return np.outer(rng.normal(size=m), u)                              # collinear
    # collapse the thin direction of the window (the equality case of Lemma P transplanted)
    Xc = XS - XS.mean(0)
    Us, Ss, Vts = np.linalg.svd(Xc, full_matrices=True)
    p = Vts[2]
    w = Us[:, 3] if m >= 5 else np.zeros(m)
    return Xc - np.outer(Xc @ p, p) + np.outer(w, p) * Ss[2] * rng.uniform(0.2, 1.2)


print("\n[Q1] Lemma Q on random windows (|S| = 4, 5, 6, 8) of several kinds, Y arbitrary (9 kinds)")
nQ = 0; viol = 0; worstQ = {}; c_half = 0; c_proper = 0; c_s2 = 0
for m in (4, 5, 6, 8):
    for trial in range(3000):
        kx = trial % 5
        if kx == 0:
            XS = rng.normal(size=(m, 3))
        elif kx == 1:
            XS = random_unit_chain(m, rng)
        elif kx == 2:
            XS = helix(m, 2.3, 1.5, 100.0)
        elif kx == 3:
            XS = helix(m, 0.94, 3.3, rng.choice([160.0, 170.0, 175.0, 179.0]))
        else:
            XS = rng.normal(size=(m, 3)) @ np.diag([1.0, 1.0, 10.0 ** rng.uniform(-4, -1)])      # thin window
        YS = random_Y(XS, rng, trial % 9)
        lhs, rhs = ratio_Q(XS, YS)
        nQ += 1
        sc = max(1.0, np.abs(YS).max(), np.abs(XS).max())
        if rhs > 1e-7 * sc:
            worstQ[m] = max(worstQ.get(m, 0.0), lhs / rhs)
        if lhs > rhs * (1 + 1e-9) + 1e-9 * sc * sc:
            viol += 1
        l1, r1 = ratio_Q(XS, YS, kappa=0.5)
        c_half += int(l1 > r1 * (1 + 1e-9) + 1e-6 * sc)
        l2, r2 = ratio_Q(XS, YS, proper=True)
        c_proper += int(l2 > r2 * (1 + 1e-9) + 1e-6 * sc)
        l3, r3 = ratio_Q(XS, YS, which=1)
        c_s2 += int(l3 > r3 * (1 + 1e-9) + 1e-6 * sc)
print(f"     windows: {nQ}   violations: {viol}   max LHS/RHS by |S|: " + ", ".join(f"{m}: {v:.4f}" for m, v in worstQ.items()))
print(f"     CONTROLS violated by: kappa -> 1/2: {c_half} pairs;  proper rotations only: {c_proper} pairs;  sigma_2 in place of sigma_3: {c_s2} pairs")

print("\n[Q2] adversarial: supremum of ||eps|| s / (kappa e) over BOTH the window X_S and Y_S (L-BFGS, numerical gradient, random starts)")


def negQ(z, m):
    XS = z[:3 * m].reshape(m, 3); YS = z[3 * m:].reshape(m, 3)
    lhs, rhs = ratio_Q(XS, YS)
    if rhs < 1e-14 or lhs < 1e-14:
        return 50.0
    return -np.log(lhs / rhs)


supQ = {}
for m, nstart in ((4, 60), (5, 150), (6, 40)):
    best = (0.0, None)
    for trial in range(nstart):
        XS = rng.normal(size=(m, 3))
        if trial % 3 == 0:
            YS = random_Y(XS, rng, 8) + 0.05 * rng.normal(size=(m, 3))
        elif trial % 3 == 1:
            YS = rng.normal(size=(m, 3))
        else:
            YS = XS + 0.3 * rng.normal(size=(m, 3))
        z0 = np.concatenate([XS.ravel(), YS.ravel()])
        res = minimize(negQ, z0, args=(m,), method="L-BFGS-B", options=dict(maxiter=600))
        val = np.exp(-res.fun)
        if val > best[0]:
            best = (val, res.x.copy())
    supQ[m] = best
    XS = best[1][:3 * m].reshape(m, 3); YS = best[1][3 * m:].reshape(m, 3)
    sv = np.linalg.svd(XS - XS.mean(0), compute_uv=False)
    svy = np.linalg.svd(YS - YS.mean(0), compute_uv=False)
    print(f"     |S| = {m}: sup found {best[0]:.6f}   (window singular values {np.round(sv / sv[0], 4)}, of Y {np.round(svy / sv[0], 4)})")
np.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "item1_supQ5_XY.npy"), supQ[5][1])
print("     -> Lemma Q holds with room; with kappa replaced by 1/2 it is violated by the maximiser if sup > 0.5/kappa = "
      f"{0.5 / KAPPA:.4f}: {supQ[5][0] > 0.5 / KAPPA}")

print("\n[Q2'] for a FIXED window the supremum over Y (how sharp is the lemma on a given window?)")
for name, XS in (("helix-like window (2.3, 1.5, 100)", helix(5, 2.3, 1.5, 100.0)), ("strand-like 160", helix(5, 0.94, 3.3, 160.0)),
                 ("strand-like 175", helix(5, 0.94, 3.3, 175.0)), ("double regular tetrahedron", None),
                 ("random unit chain", random_unit_chain(5, rng)), ("thin Gaussian window (1,1,1e-3)", rng.normal(size=(5, 3)) @ np.diag([1, 1, 1e-3]))):
    if XS is None:
        a = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
        XS = np.vstack([a[0], a[1], a[2], a[3], 2 * a[1:].mean(0) - a[0]])
    best = 0.0
    sv = np.linalg.svd(XS - XS.mean(0), compute_uv=False)
    f = lambda y: (lambda lr: 50.0 if (lr[0] < 1e-14 or lr[1] < 1e-14) else -np.log(lr[0] / lr[1]))(ratio_Q(XS, y.reshape(5, 3)))
    for trial in range(40):
        if trial % 2 == 0:
            Y0 = random_Y(XS, rng, 8) + 0.05 * sv[2] * rng.normal(size=(5, 3))
        else:
            Y0 = XS + sv[2] * 10.0 ** rng.uniform(-1, 1) * rng.normal(size=(5, 3))
        res = minimize(f, Y0.ravel(), method="L-BFGS-B", options=dict(maxiter=500))
        best = max(best, np.exp(-res.fun))
    print(f"     {name:36s} s/sigma_1 = {sv[2] / sv[0]:.2e}   sup_Y ||eps|| s/(kappa e) = {best:.4f}")


# ----------------------------------------------------------------------------------------------------------------------
# the reflection example of SCI-REV-0023 section 5 in Lemma Q
# ----------------------------------------------------------------------------------------------------------------------
print("\n[Q3] the reflection example: mirror the end point x_5 of a five-point window in the plane of its three middle points")
print("     columns: h-, h+ | changed squared distances (count), the change, 4h-h+ | d_P of the window, 2 min(|h-|,|h+|) | s, sqrt2 max|h| |"
      " Lemma Q bound 4 kappa |h-h+|/s | d_P/bound")


def reflection_case(XS):
    a, b_, c_ = XS[1], XS[2], XS[3]
    nrm = np.cross(b_ - a, c_ - a); nrm /= np.linalg.norm(nrm)
    hm = (XS[0] - a) @ nrm; hp = (XS[4] - a) @ nrm
    YS = XS.copy(); YS[4] = XS[4] - 2 * hp * nrm
    et = eta_full(XS, YS)
    changed = np.abs(et) > 1e-9 * np.abs(XS - XS.mean(0)).max() ** 2
    s = sigma3(XS)
    d = np.linalg.norm(procrustes(XS, YS)[2])
    bound = KAPPA * np.linalg.norm(et) / s
    return hm, hp, int(changed.sum()), et[np.argmax(np.abs(et))], 4 * hm * hp, d, 2 * min(abs(hm), abs(hp)), s, np.sqrt(2) * max(abs(hm), abs(hp)), bound


rows = []
cases = [("helix-like (2.3, 1.5, 100)", helix(5, 2.3, 1.5, 100.0))]
for tw in (150.0, 160.0, 170.0, 175.0, 179.0):
    cases.append((f"strand-like (0.94, 3.3, {tw:g})", helix(5, 0.94, 3.3, tw)))
a = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
cases.append(("double regular tetrahedron", np.vstack([a[0], a[1], a[2], a[3], 2 * a[1:].mean(0) - a[0]])))
cases.append(("ends on the same side, big middle triangle", np.array([[0.3, 0.2, 1.0], [5, 0, 0], [-2.5, 4.3, 0], [-2.5, -4.3, 0], [-0.2, 0.1, 1.0]])))
cases.append(("h- = 0.01 h+", np.array([[0.3, 0.2, 0.01], [1, 0, 0], [-0.5, 0.87, 0], [-0.5, -0.87, 0], [-0.2, 0.1, 1.0]])))
for eps_ in (1e-1, 1e-2, 1e-3):
    cases.append((f"thin middle triangle (width {eps_:g})", np.array([[0.0, 1.0, 0.3], [eps_, 0, -1.0], [0, 0, 0.0], [eps_ * 0.5, 0, 1.0], [0.0, 1.0, -0.4]])))
min_ratio = 1e9; max_ratio = 0
for name, XS in cases:
    hm, hp, cnt, chg, four, d, two, s, s2, bound = reflection_case(XS)
    assert cnt == 1 and abs(chg - four) < 1e-9 * max(1, abs(four)), (name, cnt, chg, four)
    assert d <= two * (1 + 1e-9) and s <= s2 * (1 + 1e-9) and d <= bound * (1 + 1e-9)
    print(f"     {name:42s} {hm:8.4f} {hp:8.4f} | {cnt} {chg:9.4f} {four:9.4f} | {d:7.4f} {two:7.4f} | {s:8.5f} {s2:7.4f} | {bound:9.4f} | {d / bound:.4f}")
    min_ratio = min(min_ratio, d / bound); max_ratio = max(max_ratio, d / bound)
for trial in range(2000):
    XS = random_unit_chain(5, rng) if trial % 2 else angle_chain(5, rng)
    if np.linalg.norm(np.cross(XS[2] - XS[1], XS[3] - XS[1])) < 1e-6:
        continue
    hm, hp, cnt, chg, four, d, two, s, s2, bound = reflection_case(XS)
    if abs(four) < 1e-8:
        continue
    assert abs(chg - four) < 1e-8 * max(1, abs(four))
    assert d <= two * (1 + 1e-9) + 1e-12 and s <= s2 * (1 + 1e-9) and d <= bound * (1 + 1e-9) + 1e-12
    rows.append((d / bound, d / two, s / s2))
rows = np.array(rows)
print(f"     2000 random five-point chains: d_P/bound in [{rows[:, 0].min():.4f}, {rows[:, 0].max():.4f}] (median {np.median(rows[:, 0]):.4f});"
      f"  d_P/(2 min|h|) in [{rows[:, 1].min():.4f}, {rows[:, 1].max():.4f}];  s/(sqrt2 max|h|) in [{rows[:, 2].min():.2e}, {rows[:, 2].max():.4f}]")
print("     asserted on every case: exactly one squared distance changes, by 4 h- h+;  d_P <= 2 min(|h-|,|h+|);  s <= sqrt2 max(|h-|,|h+|);  d_P <= bound")
print(f"ALL DONE {now()}  {time.time() - t0:.1f} s  peak memory {peak_mb():.0f} MB")
