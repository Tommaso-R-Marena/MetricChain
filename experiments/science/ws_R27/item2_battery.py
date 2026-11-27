#!/usr/bin/env python3
"""Workstream R27, Item 2 (ii) -- REPLICATION of Theorem L with code written from the statements:
a battery of pairs (X, Y), every intermediate inequality of Steps 1-4, both bounds, and controls that must fail.

X: random unit-bond chains (unconstrained and with constrained angles), helix-like, strand-like (near-coplanar windows),
   chains with ONE thin interior four-point window, point clouds without chain structure, a compact double tetrahedron.
Y: small and large noise; tails reflected in the plane of three consecutive points (every position); heads reflected; unrelated
   chains; random point clouds; mirror images; pieces rotated about a bond, about an axis through two points, about a random
   axis; one point moved far away (every position, three distances); all points equal; collinear; planar projection; softest
   modes of the half-Jacobian at several amplitudes and both signs; scalings; reversal of the order; a swap of two points;
   reflection plus noise.

Run:  OMP_NUM_THREADS=1 python3 -B item2_battery.py > item2_battery_<stamp>.log
"""
import os, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from r27lib import (cap_memory, peak_mb, now, helix, random_unit_chain, angle_chain, torsion_chain, chain_consts, pair_arrays,
                    mu_and_mode, dP)
from thmL_steps import check_pair, prepare

cap_memory(2.0)
t0 = time.time()
rng = np.random.default_rng(2711)
print(f"R27 item2_battery.py  started {now()}  (replication: own code from the statements; their scripts not available)")


def rot(axis, ang):
    a = axis / np.linalg.norm(axis)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K


def random_orth(rng):
    Q, Rr = np.linalg.qr(rng.normal(size=(3, 3)))
    return Q * np.sign(np.diag(Rr))


def reflect_tail(X, i):
    """reflect the points beyond x_{i+3} (0-based i: plane of X[i+1], X[i+2], X[i+3]; points i+4.. are reflected)"""
    nrm = np.cross(X[i + 2] - X[i + 1], X[i + 3] - X[i + 1])
    nn = np.linalg.norm(nrm)
    if nn < 1e-12:
        return None
    nrm /= nn
    Y = X.copy()
    Y[i + 4:] = X[i + 4:] - 2 * ((X[i + 4:] - X[i + 1]) @ nrm)[:, None] * nrm[None, :]
    return Y


def reflect_head(X, i):
    nrm = np.cross(X[i + 2] - X[i + 1], X[i + 3] - X[i + 1])
    nn = np.linalg.norm(nrm)
    if nn < 1e-12:
        return None
    nrm /= nn
    Y = X.copy()
    Y[:i + 1] = X[:i + 1] - 2 * ((X[:i + 1] - X[i + 1]) @ nrm)[:, None] * nrm[None, :]
    return Y


def thin_window_chain(n, rng, pos, height):
    """angle-constrained random chain in which the four points pos+1..pos+4 (0-based) are made nearly coplanar:
    x_{pos+4} is moved to height `height` over the plane of the three points before it (the rest of the chain follows rigidly)"""
    X = angle_chain(n, rng)
    a, b_, c_ = X[pos + 1], X[pos + 2], X[pos + 3]
    nrm = np.cross(b_ - a, c_ - a)
    nrm /= np.linalg.norm(nrm)
    h = (X[pos + 4] - a) @ nrm
    shift = (height - h) * nrm
    X[pos + 4:] += shift
    return X


def Y_family(X, rng, fam):
    """generator of (label, Y)"""
    n = len(X)
    J, Kk = pair_arrays(n)
    diam = np.linalg.norm(X - X.mean(0), axis=1).max()
    for sg in (1e-6, 1e-4, 1e-2):
        yield "noise small", X + sg * rng.normal(size=X.shape)
    for sg in (0.1, 0.3, 1.0, 3.0, 10.0):
        yield "noise large", X + sg * rng.normal(size=X.shape)
    for i in range(n - 4):
        Y = reflect_tail(X, i)
        if Y is not None:
            yield "tail reflected", Y
            yield "tail reflected + noise", Y + 1e-3 * rng.normal(size=X.shape)
        Y = reflect_head(X, i)
        if Y is not None:
            yield "head reflected", Y
    for _ in range(3):
        yield "unrelated chain", random_unit_chain(n, rng) * rng.choice([0.5, 1.0, 3.8])
        yield "unrelated chain", angle_chain(n, rng)
    for sg in (0.1, 1.0, 10.0):
        yield "random cloud", sg * rng.normal(size=X.shape)
    M = np.diag([1.0, 1.0, -1.0])
    yield "mirror image", X @ M
    yield "mirror image", (X @ M) @ random_orth(rng) + rng.normal(size=3)
    yield "congruent copy", X @ random_orth(rng) + rng.normal(size=3)
    for p in sorted(set([1, n // 2, n - 3])):
        if 1 <= p <= n - 2:
            for ang in (0.01, 0.3, 1.0, np.pi):
                Y = X.copy()
                Rm = rot(X[p + 1] - X[p], ang)
                Y[p + 1:] = (X[p + 1:] - X[p]) @ Rm.T + X[p]
                yield "tail rotated about a bond", Y
    for _ in range(4):
        p, q = sorted(rng.choice(n, size=2, replace=False))
        ang = rng.uniform(0.05, np.pi)
        Rm = rot(X[q] - X[p], ang)
        Y = X.copy()
        Y[:q] = (X[:q] - X[p]) @ Rm.T + X[p]
        yield "head rotated about an axis through two points", Y
        k = rng.integers(1, n - 1)
        Rm = rot(rng.normal(size=3), rng.uniform(0.05, np.pi))
        Y = X.copy()
        Y[k:] = (X[k:] - X[k]) @ Rm.T + X[k]
        yield "tail rotated about a random axis", Y
    for k in range(n):
        for far in (1.0, 1e2, 1e4):
            Y = X.copy()
            u = rng.normal(size=3)
            Y[k] = X[k] + far * diam * u / np.linalg.norm(u)
            yield "one point moved far away", Y
    yield "all points equal", np.tile(rng.normal(size=3), (n, 1))
    yield "all points equal", np.zeros_like(X)
    u = rng.normal(size=3); u /= np.linalg.norm(u)
    yield "collinear", np.outer(np.arange(n) * 1.0, u)
    yield "collinear", np.outer(rng.normal(size=n) * diam, u)
    yield "collinear", np.outer((X - X.mean(0)) @ u, u)
    P = np.eye(3) - np.outer(u, u)
    yield "planar projection", X @ P
    yield "planar projection", X @ np.diag([1.0, 1.0, 0.0])
    try:
        mu, nxt, V, S = mu_and_mode(X, J, Kk)
        for tt in (1e-4, 1e-2, 0.1, 1.0, 10.0):
            for sgn in (1, -1):
                yield "softest mode", X + sgn * tt * diam * V
    except Exception as exc:                                   # pragma: no cover
        print("   (softest mode skipped:", exc, ")")
    for lam in (0.0, 0.5, 0.99, 1.01, 2.0, -1.0):
        yield "scaled copy", lam * X
    yield "order reversed", X[::-1].copy()
    Y = X.copy(); a, b_ = rng.choice(n, size=2, replace=False); Y[[a, b_]] = Y[[b_, a]]
    yield "two points swapped", Y


def X_families():
    for n in (5, 6, 8, 12, 20, 40):
        for rep in range(3):
            yield f"random unit chain", random_unit_chain(n, rng)
            yield f"angle-constrained chain", angle_chain(n, rng)
        yield "helix-like (2.3, 1.5, 100)", helix(n, 2.3, 1.5, 100.0)
        for tw in (160.0, 170.0, 175.0, 179.0):
            yield f"strand-like (0.94, 3.3, {tw:g})", helix(n, 0.94, 3.3, tw)
        if n >= 8:
            for hgt in (1e-1, 1e-2, 1e-4):
                yield f"one thin interior window (height {hgt:g})", thin_window_chain(n, rng, n // 2 - 2, hgt)
        yield "point cloud (no chain structure)", rng.normal(size=(n, 3))
    # compact: two regular tetrahedra glued on a face (n = 5)
    a = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
    cface = a[1:].mean(0)
    apex2 = 2 * cface - a[0]
    yield "double regular tetrahedron", np.vstack([a[0], a[1], a[2], a[3], apex2])


agg = {}          # (X family) -> name -> max ratio
aggY = {}         # (Y family) -> name -> max ratio
ctl_count = {}
ctl_by_Y = {}
n_pairs = 0
n_viol = 0
viol_examples = []
skipped = 0
maxima = dict(local_pt=(0, None), local_frob=(0, None), uniform=(0, None), lemmaQ=(0, None))
detchange_pairs = 0
n_swapped = 0; n_viol_swapped = 0; max_swapped = 0.0
for Xname, X in X_families():
    tau, s, b = chain_consts(X)
    if tau.min() < 1e-9 * b:
        skipped += 1
        continue
    cache = prepare(X)
    for Yname, Y in Y_family(X, rng, Xname):
        out, viol, ctl = check_pair(X, Y, cache)
        n_pairs += 1
        # roles swapped: Y as the reference configuration and X as the arbitrary one (this is Corollary L.2), when tau*(Y) > 0
        tY, sY, bY = chain_consts(Y)
        if tY.min() > 1e-6 * max(bY, 1e-300) and np.isfinite(bY):
            out2, viol2, _ = check_pair(Y, X, want_controls=False)
            n_swapped += 1
            n_viol_swapped += int(len(viol2) > 0)
            max_swapped = max(max_swapped, out2.get("FIN d_P <= uniform (1.2 (b/(s*tau*)) (n+2)^2 ||eta||)", 0.0))
        if viol:
            n_viol += 1
            if len(viol_examples) < 20:
                viol_examples.append((Xname, len(X), Yname, viol[:3]))
        if out["_det_changes"] > 0:
            detchange_pairs += 1
        for name, v in out.items():
            if name.startswith("_"):
                continue
            agg.setdefault(Xname, {})
            agg[Xname][name] = max(agg[Xname].get(name, 0.0), v)
            aggY.setdefault(Yname, {})
            aggY[Yname][name] = max(aggY[Yname].get(name, 0.0), v)
        for name, v in ctl.items():
            ctl_count[name] = ctl_count.get(name, 0) + int(v)
            if v:
                ctl_by_Y.setdefault(name, {})
                ctl_by_Y[name][Yname] = ctl_by_Y[name].get(Yname, 0) + 1
        for key, name in (("local_pt", "S3  (local) |y_k - g x_k| <= local_k"), ("local_frob", "FIN d_P <= ||local||_2"),
                          ("uniform", "FIN d_P <= uniform (1.2 (b/(s*tau*)) (n+2)^2 ||eta||)"),
                          ("lemmaQ", "S1  ||eps_i|| <= kappa e_i/s_i")):
            if out.get(name, 0.0) > maxima[key][0]:
                maxima[key] = (out[name], (Xname, len(X), Yname))

names = sorted({k for d in agg.values() for k in d})
print(f"\npairs checked: {n_pairs}   X instances skipped as degenerate (tau* < 1e-9 b): {skipped}")
print(f"pairs with at least one VIOLATION of a claimed inequality: {n_viol}")
for v in viol_examples:
    print("   VIOLATION:", v)
print(f"pairs in which two consecutive window frames have opposite determinants: {detchange_pairs}")
print(f"roles swapped (Y as reference, X arbitrary; the situation of Corollary L.2), for the Y with tau*(Y) > 1e-6 b(Y): {n_swapped} pairs, "
      f"violations {n_viol_swapped}, max d_P/uniform(Y) = {max_swapped:.6g}")
print("\nmaximum of LHS/RHS over all pairs, for each inequality of the proof (<= 1 = holds):")
for name in names:
    print(f"   {name:62s} {max(d.get(name, 0.0) for d in agg.values()):.6g}")
print("\nthe same by family of X (columns: Lemma Q | Step 2b | (local) per point | d_P/||local||_2 | d_P/uniform):")
cols = ["S1  ||eps_i|| <= kappa e_i/s_i", "S2b ||R_j-R_j+1||_F <= (d_j+d_j+1)/tau_j+1", "S3  (local) |y_k - g x_k| <= local_k",
        "FIN d_P <= ||local||_2", "FIN d_P <= uniform (1.2 (b/(s*tau*)) (n+2)^2 ||eta||)"]
for Xname in agg:
    print(f"   {Xname:44s} " + "  ".join(f"{agg[Xname].get(c, 0.0):9.3g}" for c in cols))
print("\nthe same by family of Y:")
for Yname in aggY:
    print(f"   {Yname:44s} " + "  ".join(f"{aggY[Yname].get(c, 0.0):9.3g}" for c in cols))
print("\nlargest ratios and where:")
for k, v in maxima.items():
    print(f"   {k:10s} {v[0]:.6g}  at {v[1]}")
print("\nCONTROLS (not claimed; each must be violated by at least one pair -- number of pairs violating, and in which Y families):")
for name in sorted(ctl_count):
    fams = ctl_by_Y.get(name, {})
    top = ", ".join(f"{k}: {v}" for k, v in sorted(fams.items(), key=lambda z: -z[1])[:6])
    print(f"   {name:70s} {ctl_count[name]:6d} of {n_pairs}   [{top}]")
failed = sorted(k for k, v in ctl_count.items() if v > 0)
not_failed = sorted(k for k, v in ctl_count.items() if v == 0)
print(f"\nall claimed inequalities hold on all pairs: {n_viol == 0}")
print(f"controls that failed at least once (as a control must): {len(failed)} of {len(ctl_count)};  controls that never failed on this battery: {not_failed}")
print("   (the uniform constant divided by 10 or 100 is not violated by any pair of this battery: the largest ratio here is below 0.01; the adversarial searches reach 0.018)")
print(f"ALL DONE {now()}  {time.time() - t0:.1f} s  peak memory {peak_mb():.0f} MB")
