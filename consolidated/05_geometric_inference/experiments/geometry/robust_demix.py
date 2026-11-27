"""Robust demixing: computable noise and tolerance bounds (docs/geometry/ROBUST_DEMIXING.md).

Data: a centred symmetric matrix Gt (minus one half of the doubly centred matrix of averaged
squared distances), possibly noisy.  A *reference* is a triple (Z, Q, v): Z an n x 3K matrix
with centred columns (here: the top 3K eigenpairs of Gt), Q = [Q_1 ... Q_K] an orthogonal
matrix cut into K blocks of 3 columns, v_k > 0.  Reference states: Xhat_k = Z Q_k / sqrt(v_k);
reference projectors Phat_k = Q_k Q_k^T / v_k.  Five numbers are computed from the reference:

  sigma_perp  smallest singular value of the conic map S -> (e^T S e)_e on the orthogonal
              complement of span{Phat_k - Phat_1} (Frobenius norm on the left);
  tau_max     largest l2-norm over k of the constraint violations of the reference states;
  ||Z||_op, lambda_m = sigma_m(Z)^2, and tail = trace of Gt off the column space of Z.

Lemma N0, Theorems N1 (all ensembles, square-root law) and N2 (K-state mixtures, linear,
crude constant) bound every ensemble whose data are within eps of Gt in terms of these.
Theorem N3 (reference an exact mixture): the first-order constants C_state, C_w -- block norms
of the pseudo-inverse of the linearised map (weights, tangent displacements) -> G -- hold for
every K-state competitor in a certified range, by bootstrapping from the crude bound; they are
attained to first order.  A posteriori use: DEMIX, then a least-squares polish to an exact
mixture mu_0 with residual eps_0; every competitor within eps of the data is within
eps + eps_0 of G(mu_0).

This file computes the bounds and CHECKS every inequality of the proofs on competitors that
are not chosen to be favourable.  Floating point; the theorems are paper proofs.

Usage: robust_demix.py           checks on five instances, ends with ALL OK
       robust_demix.py --table   the table of constants and certified ranges (section 6)
"""
import itertools
import sys

import numpy as np
from scipy.optimize import least_squares

from geomlib import chain

KAPPA_P = 1.0 / np.sqrt(2.0 * (np.sqrt(2.0) - 1.0))       # Procrustes-Gram constant (Lemma P)
D = 3


# ------------------------------------------------------------------ basic objects
def centre(X):
    return X - X.mean(0)


def chain_edges(n, b=1.0, theta=np.deg2rad(111.0)):
    c = np.sqrt(2 * b * b * (1 - np.cos(theta)))
    edges = [(i, i + 1) for i in range(n - 1)] + [(i, i + 2) for i in range(n - 2)]
    return edges, np.array([b] * (n - 1) + [c] * (n - 2))


def gram(Xs, w):
    return sum(wk * centre(X) @ centre(X).T for wk, X in zip(w, Xs))


def d_procrustes(X, Y):
    """min over orthogonal R (reflections allowed) and translations of ||Y - X R||_F, with the
    residual formed explicitly (no cancellation), and the minimising R."""
    Xc, Yc = centre(X), centre(Y)
    U, _, Vt = np.linalg.svd(Xc.T @ Yc)
    R = U @ Vt
    return float(np.linalg.norm(Yc - Xc @ R)), R


def sym_coords(m):
    """Index pairs of an orthonormal basis of Sym(m) for the Frobenius inner product."""
    return [(i, j) for i in range(m) for j in range(i, m)]


def to_vec(S, idx):
    return np.array([S[i, j] if i == j else np.sqrt(2.0) * S[i, j] for (i, j) in idx])


def conic_rows(Z, edges, idx):
    """Matrix of S -> (e^T S e)_e in orthonormal coordinates of Sym(m)."""
    rows = []
    for (i, j) in edges:
        e = Z[j] - Z[i]
        rows.append([e[a] * e[b] if a == b else np.sqrt(2.0) * e[a] * e[b] for (a, b) in idx])
    return np.array(rows)


def laplacian_max(n, edges):
    L = np.zeros((n, n))
    for (i, j) in edges:
        L[i, i] += 1
        L[j, j] += 1
        L[i, j] -= 1
        L[j, i] -= 1
    return float(np.linalg.eigvalsh(L)[-1])


# ------------------------------------------------------------------ the reference (DEMIX on Gt)
def reference(Gt, edges, lengths, K, rng=None):
    """Top-m eigenpairs of Gt; approximate null space of the conic system (the K - 1 smallest
    right singular vectors); eigenvectors of a combination with well separated eigenvalues;
    weights from the mean of |edge|^2 / l^2."""
    rng = rng or np.random.default_rng(0)
    m = D * K
    ev, Vec = np.linalg.eigh(Gt)
    order = np.argsort(ev)[::-1]
    ev, Vec = ev[order], Vec[:, order]
    Z = Vec[:, :m] * np.sqrt(np.maximum(ev[:m], 0.0))
    idx = sym_coords(m)
    if K == 1:
        Q = np.eye(m)
    else:
        A = conic_rows(Z, edges, idx)
        null = np.linalg.svd(A)[2][len(idx) - (K - 1):]
        best = None
        for _ in range(20):                      # keep the combination with the widest cluster gaps
            cvec = rng.normal(size=K - 1)
            T = np.zeros((m, m))
            for c, vvec in zip(cvec, null):
                for t, (i, j) in enumerate(idx):
                    val = vvec[t] if i == j else vvec[t] / np.sqrt(2.0)
                    T[i, j] += c * val
                    if i != j:
                        T[j, i] += c * val
            tv, Qc = np.linalg.eigh(T)
            centres = tv.reshape(K, D).mean(1)
            gap = np.min(np.diff(centres)) / (np.abs(tv).max() + 1e-300)
            if best is None or gap > best[0]:
                best = (gap, Qc)
        Q = best[1]
    Qs = [Q[:, D * k:D * k + D] for k in range(K)]
    v = []
    for Qk in Qs:
        Yk = Z @ Qk
        v.append(float(np.mean([((Yk[j] - Yk[i]) ** 2).sum() / l ** 2 for (i, j), l in zip(edges, lengths)])))
    v = np.array(v)
    states = [Z @ Qk / np.sqrt(vk) for Qk, vk in zip(Qs, v)]
    return dict(Z=Z, Qs=Qs, v=v, states=states, ev=ev, K=K, m=m)


def numbers(ref, Gt, edges, lengths, delta=None):
    """The computable constants of Lemma N0 and Theorems N1, N2 for a reference."""
    Z, Qs, v, K, m = ref["Z"], ref["Qs"], ref["v"], ref["K"], ref["m"]
    n = Z.shape[0]
    idx = sym_coords(m)
    A = conic_rows(Z, edges, idx)
    Ph = [Qk @ Qk.T / vk for Qk, vk in zip(Qs, v)]
    l2 = np.asarray(lengths) ** 2
    tau = [float(np.linalg.norm(A @ to_vec(P, idx) - l2)) for P in Ph]
    if K > 1:
        Tspan = np.array([to_vec(Ph[k] - Ph[0], idx) for k in range(1, K)]).T        # columns span T'
        Qt, _ = np.linalg.qr(Tspan, mode="complete")
        W = Qt[:, K - 1:]                                                              # basis of its complement
    else:
        W = np.eye(len(idx))
    sigma_perp = float(np.linalg.svd(A @ W, compute_uv=False)[-1]) if A.shape[0] >= W.shape[1] else 0.0
    V = float(v.sum())
    c = [1.0 + np.sqrt(D * (K - 1 + (V / vk - 1.0) ** 2)) for vk in v]
    sv = np.linalg.svd(Z, compute_uv=False)
    Pi = Z @ np.linalg.pinv(Z)
    J = np.eye(n) - np.ones((n, n)) / n
    delta = np.zeros(len(edges)) if delta is None else np.asarray(delta, dtype=float)
    lplus = float(np.sqrt((l2 + delta).max()))
    lbond = float(np.sqrt(max(l2[t] + delta[t] for t, (i, j) in enumerate(edges) if j - i == 1)))
    tau_max = max(tau)
    return dict(n=n, m=m, K=K, sigma_perp=sigma_perp, tau=tau, tau_max=tau_max, V=V, c=c, v=v,
                a=KAPPA_P * sv[0] * max(np.sqrt(vk) * ck for vk, ck in zip(v, c)),
                Znorm=float(sv[0]), lam_m=float(sv[m - 1] ** 2), tail=float(np.trace((J - Pi) @ Gt)),
                Lam0=laplacian_max(n, edges), lplus=lplus, delta_norm=float(np.linalg.norm(delta)),
                sigma_eff=sigma_perp - 2 * tau_max * V, Pi=Pi, J=J, Ph=Ph, A=A, idx=idx, l2=l2,
                D2=lbond ** 2 * n * (n * n - 1) / 12.0)


def rho_of(num, phi):
    return num["delta_norm"] + 2 * num["lplus"] * np.sqrt(num["Lam0"] * phi) + num["Lam0"] * phi


def nu_bar(num, phi):
    """(rho(phi) + tau_max) / (sigma_perp - 2 tau_max V); infinite if the denominator is not positive."""
    return (rho_of(num, phi) + num["tau_max"]) / num["sigma_eff"] if num["sigma_eff"] > 0 else np.inf


def radius(num, phi):
    return np.sqrt(phi) + num["a"] * nu_bar(num, phi)


def phi_max(num, safety=1.0):
    """Largest phi with nu_bar(phi) V <= safety (0 if there is none)."""
    if num["sigma_eff"] <= 0:
        return 0.0
    budget = safety * num["sigma_eff"] / num["V"] - num["tau_max"] - num["delta_norm"]
    if budget <= 0:
        return 0.0
    L, l = num["Lam0"], num["lplus"]
    s = (-2 * l * np.sqrt(L) + np.sqrt(4 * l * l * L + 4 * L * budget)) / (2 * L)     # s = sqrt(phi)
    return float(s * s)


# ------------------------------------------------------------------ Lemma N0 on one chain
def chain_report(ref, num, Y, delta_violation=0.0):
    """All quantities of Lemma N0 and of the first half of Theorem N1 for a chain Y, with the
    inequalities evaluated.  Returns a dict; 'violations' lists the names of failed inequalities
    (empty when the hypotheses do not hold, in which case 'applicable' is False)."""
    Z, Qs, v = ref["Z"], ref["Qs"], ref["v"]
    K = ref["K"]
    Yc = centre(Y)
    At = np.linalg.pinv(Z) @ Yc                      # A_Y^T, m x d
    R = Yc - Z @ At
    phi = float((R ** 2).sum())
    P = At @ At.T
    idx, A, l2, Ph = num["idx"], num["A"], num["l2"], num["Ph"]
    resid = A @ to_vec(P, idx) - l2
    rho_act = float(np.linalg.norm(resid))
    out = dict(phi=phi, rho_actual=rho_act, rho_bound=rho_of(num, phi), violations=[])
    tol = 1e-9
    if rho_act > out["rho_bound"] * (1 + 1e-9) + tol:
        out["violations"].append("rho")
    nb = nu_bar(num, phi)
    out["nu_bar"] = nb
    out["applicable"] = bool(nb * num["V"] < 1)
    dists = [d_procrustes(Xh, Y)[0] for Xh in ref["states"]]
    out["dist"] = min(dists)
    out["nearest"] = int(np.argmin(dists))
    if not out["applicable"]:
        return out
    # decomposition P = sum t_k Phat_k + N with N orthogonal to span{Phat_k - Phat_1}
    if K > 1:
        Tspan = np.array([to_vec(Ph[k] - Ph[0], idx) for k in range(1, K)]).T
        coef = np.linalg.lstsq(Tspan, to_vec(P - Ph[0], idx), rcond=None)[0]
        t = np.concatenate([[1 - coef.sum()], coef])
    else:
        t = np.array([1.0])
    N = P - sum(tk * Pk for tk, Pk in zip(t, Ph))
    nF = float(np.linalg.norm(N))
    out["N_F"] = nF
    if nF > nb * (1 + 1e-9) + tol:
        out["violations"].append("N")
    b = t / v
    nu = float(np.linalg.norm(N, 2))
    big = [k for k in range(K) if b[k] > nu]
    if len(big) != 1:
        out["violations"].append("k0")
        return out
    k0 = big[0]
    dP = float(np.linalg.norm(P - Ph[k0]))
    out["dP"], out["dP_bound"] = dP, num["c"][k0] * nb
    if dP > out["dP_bound"] * (1 + 1e-9) + tol:
        out["violations"].append("dP")
    dk0 = d_procrustes(ref["states"][k0], Y)[0]
    out["bound"] = np.sqrt(phi) + KAPPA_P * num["Znorm"] * np.sqrt(v[k0]) * num["c"][k0] * nb
    if dk0 > out["bound"] * (1 + 1e-9) + tol:
        out["violations"].append("distance")
    if out["bound"] > radius(num, phi) * (1 + 1e-12):
        out["violations"].append("radius")
    return out


# ------------------------------------------------------------------ Theorem N2 on one mixture
def mixture_report(ref, num, Gt, Ys, u, eps=None):
    """Theorem N2 for the K-mixture (Ys, u): eps = ||G(mixture) - Gt||_F unless given.  Checks the
    intermediate inequality ||z' - Z Q0|| <= eps_Z and the conclusions (states, inverse weights)."""
    K, v = ref["K"], ref["v"]
    out = dict(violations=[])
    Gm = gram(Ys, u)
    eps = float(np.linalg.norm(Gm - Gt)) if eps is None else eps
    out["eps"] = eps
    if not eps < num["lam_m"]:
        out["applicable"] = False
        return out
    epsZ = 2 * KAPPA_P * eps / np.sqrt(num["lam_m"])
    zp = np.hstack([np.sqrt(uk) * centre(Y) for uk, Y in zip(u, Ys)])
    U, _, Vt = np.linalg.svd(ref["Z"].T @ zp)
    Q0 = U @ Vt
    actual_epsZ = float(np.linalg.norm(zp - ref["Z"] @ Q0))
    out["epsZ"], out["epsZ_actual"] = epsZ, actual_epsZ
    if actual_epsZ > epsZ * (1 + 1e-9) + 1e-10:
        out["violations"].append("epsZ")
    nbs = [nu_bar(num, epsZ ** 2 / uk) for uk in u]
    out["applicable"] = bool(max(nbs) * num["V"] < 1 and 2 * max(num["c"]) * max(nbs) < np.sqrt(2 * D))
    if not out["applicable"]:
        return out
    best = None
    for perm in itertools.permutations(range(K)):
        errs = [d_procrustes(ref["states"][perm[j]], Ys[j])[0] for j in range(K)]
        if best is None or max(errs) < max(best[1]):
            best = (perm, errs)
    perm, errs = best
    out["state_err"] = max(errs)
    bounds = [epsZ / np.sqrt(u[j]) + KAPPA_P * num["Znorm"] * np.sqrt(v[perm[j]]) * num["c"][perm[j]] * nbs[j]
              for j in range(K)]
    out["state_bound"] = max(bounds)
    if any(e > bd * (1 + 1e-9) + 1e-10 for e, bd in zip(errs, bounds)):
        out["violations"].append("states")
    werr = [abs(1 / u[j] - 1 / v[perm[j]]) for j in range(K)]
    wbd = [num["c"][perm[j]] * nbs[j] for j in range(K)]
    out["invw_err"], out["invw_bound"] = max(werr), max(wbd)
    if any(e > bd * (1 + 1e-9) + 1e-10 for e, bd in zip(werr, wbd)):
        out["violations"].append("weights")
    return out


# ------------------------------------------------------------------ first-order constants (Theorem N3)
def torsions_of(X, theta=np.deg2rad(111.0)):
    """Torsion angles in the convention of geomlib.chain (exact for chains built by it)."""
    t = []
    for i in range(3, len(X)):
        a, bb, c = X[i - 3], X[i - 2], X[i - 1]
        bc = (c - bb) / np.linalg.norm(c - bb)
        nrm = np.cross(bb - a, bc)
        nrm /= np.linalg.norm(nrm)
        mm = np.cross(nrm, bc)
        t.append(np.arctan2((X[i] - c) @ nrm, (X[i] - c) @ mm))
    return np.array(t)


def rigidity_matrix(X, edges):
    n = len(X)
    Rg = np.zeros((len(edges), 3 * n))
    for t, (i, j) in enumerate(edges):
        e = X[j] - X[i]
        Rg[t, 3 * j:3 * j + 3] = e
        Rg[t, 3 * i:3 * i + 3] = -e
    return Rg


def trivial_motions(Xc):
    n = len(Xc)
    triv = []
    for a in range(3):
        t = np.zeros((n, 3))
        t[:, a] = 1
        triv.append(t.ravel())
    for (a, b) in ((0, 1), (0, 2), (1, 2)):
        Xi = np.zeros((3, 3))
        Xi[a, b], Xi[b, a] = 1, -1
        triv.append((Xc @ Xi).ravel())
    return np.linalg.qr(np.array(triv).T)[0]


def tangent_basis(X, edges):
    """Orthonormal basis of the flexes of (E0, X) orthogonal to the infinitesimal isometries,
    and the smallest non-zero singular value of the rigidity matrix."""
    Xc = centre(X)
    Rg = rigidity_matrix(Xc, edges)
    sv, Vt = np.linalg.svd(Rg)[1:]
    rank = int((sv > 1e-9 * sv[0]).sum())
    flex = Vt[rank:].T
    Tq = trivial_motions(Xc)
    flex = flex - Tq @ (Tq.T @ flex)
    Uq, sq, _ = np.linalg.svd(flex, full_matrices=False)
    return Uq[:, sq > 1e-8], float(sv[rank - 1])


def first_order(Xs, w, edges):
    """The linearised map L(a, tau) = sum_k a_k X_k X_k^T + w_k (X_k tau_k^T + tau_k X_k^T) on
    {sum a = 0} x prod T_k, its pseudo-inverse, and the block norms C_state[k], C_w."""
    K, n = len(Xs), len(Xs[0])
    Xc = [centre(X) for X in Xs]
    cols, kinds, bases, sR = [], [], [], []
    for k in range(K - 1):
        cols.append((Xc[k] @ Xc[k].T - Xc[K - 1] @ Xc[K - 1].T).ravel())
        kinds.append(("w", k))
    for k in range(K):
        B, s = tangent_basis(Xs[k], edges)
        bases.append(B)
        sR.append(s)
        for cidx in range(B.shape[1]):
            b = B[:, cidx].reshape(n, 3)
            cols.append((w[k] * (Xc[k] @ b.T + b @ Xc[k].T)).ravel())
            kinds.append(("x", k))
    A = np.array(cols).T
    sv = np.linalg.svd(A, compute_uv=False)
    pinv = np.linalg.pinv(A)
    rows = lambda kind, k=None: [i for i, (t, kk) in enumerate(kinds) if t == kind and (k is None or kk == k)]
    C_state = [float(np.linalg.norm(pinv[rows("x", k)], 2)) for k in range(K)]
    # weights: a_k = c_k (k < K-1), a_{K-1} = -sum c: the map c -> a has matrix Wm
    Wm = np.vstack([np.eye(K - 1), -np.ones((1, K - 1))]) if K > 1 else np.zeros((1, 0))
    C_w = float(np.linalg.norm(Wm @ pinv[rows("w")], 2)) if K > 1 else 0.0
    # tolerance: violations (all states, all constrained pairs) -> displacement of state k, to first
    # order: nu_j = Rig_j^+ (viol_j / 2), (a, tau) = -L^+ L(0, nu), displacement_k = tau_k + nu_k
    ne = len(edges)
    Rp = [np.linalg.pinv(rigidity_matrix(X, edges)) for X in Xc]
    L0 = np.zeros((n * n, K * ne))
    for j in range(K):
        for cidx in range(ne):
            nu = (Rp[j][:, cidx] / 2).reshape(n, 3)
            L0[:, j * ne + cidx] = (w[j] * (Xc[j] @ nu.T + nu @ Xc[j].T)).ravel()
    T_state = []
    for k in range(K):
        Tk = -bases[k] @ (pinv[rows("x", k)] @ L0)
        Tk[:, k * ne:(k + 1) * ne] += Rp[k] / 2
        T_state.append(float(np.linalg.norm(Tk, 2)))
    T_w = float(np.linalg.norm(Wm @ (pinv[rows("w")] @ L0), 2)) if K > 1 else 0.0
    return dict(A=A, pinv=pinv, kinds=kinds, bases=bases, sR=sR, C_state=C_state, C_w=C_w, Wm=Wm,
                injective=bool(sv[-1] > 1e-9 * sv[0]), Xop=[float(np.linalg.norm(X, 2)) for X in Xc], rows=rows,
                T_state=T_state, T_w=T_w)


def crude_bounds(num, eta, ulow, factor=1.0):
    """Theorem N2 with lower bounds ulow[k] on the weight of the competitor state matched to the
    reference state k: eta_Z and the nu_bar_k, or None if the hypotheses fail.  factor = 1 for
    an exact reference (||z'z'^T - Z Z^T|| <= eta), 2 for a reference cut from noisy data."""
    if not eta < num["lam_m"]:
        return None
    etaZ = factor * KAPPA_P * eta / np.sqrt(num["lam_m"])
    nbs = np.array([nu_bar(num, etaZ ** 2 / uk) for uk in ulow])
    if not (nbs.max() * num["V"] < 1 and 2 * max(num["c"]) * nbs.max() < np.sqrt(2 * D)):
        return None
    return etaZ, nbs


def theorem_N2(num, eta, u0=None, factor=1.0, iterations=200):
    """Bounds for every K-mixture on C_delta with ||G - Gt||_F <= eta (weights >= u0; default:
    the automatic bound (lambda_m - eta) / D_n^2), after renumbering: B[k] >= d_P(Y_k, Xhat_k),
    I[k] >= |1/u_k - 1/v_k|, and lower bounds ulow[k] <= u_k.  The lower bounds are improved by
    the weight bound itself (each step is an implication for the same competitor).  None
    outside the certified range."""
    K, v, c = num["K"], num["v"], num["c"]
    start = (num["lam_m"] - eta) / num["D2"] if u0 is None else u0
    if not start > 0:
        return None
    ulow = np.full(K, float(start))
    cb = crude_bounds(num, eta, ulow, factor)
    if cb is None:
        return None
    for _ in range(iterations):
        etaZ, nbs = cb
        new = np.maximum(ulow, 1.0 / (1.0 / v + np.array(c) * nbs))
        if np.allclose(new, ulow, rtol=1e-13, atol=0):
            break
        ulow = new
        cb = crude_bounds(num, eta, ulow, factor)
    etaZ, nbs = cb
    B = etaZ / np.sqrt(ulow) + KAPPA_P * num["Znorm"] * np.sqrt(v) * np.array(c) * nbs
    return dict(B=B, I=np.array(c) * nbs, ulow=ulow, etaZ=etaZ, nbs=nbs)


def theorem_N3(num, fo, eta, u0=None, iterations=200):
    """Exact reference with constants num (reference built by exact_reference) and first-order
    data fo.  For every K-mixture on C_delta with ||G - G(reference)||_F <= eta (weights >= u0,
    default automatic): after renumbering, B[k] >= d_P(Y_k, X_k) and Aw >= ||u - w||_2, obtained
    from the crude bounds by iterating the second-order inequality.  None outside the range."""
    K, v = num["K"], num["v"]
    cr = theorem_N2(num, eta, u0)
    if cr is None:
        return None
    B = cr["B"].copy()
    A = v * cr["I"]                                    # |u_k - w_k| = u_k w_k |1/u_k - 1/w_k| <= w_k I_k
    sR, Xop, Cs, Ts = np.array(fo["sR"]), np.array(fo["Xop"]), np.array(fo["C_state"]), np.array(fo["T_state"])
    viol = np.sqrt(K) * num["delta_norm"]              # l2 norm of all violations of the competitor
    L0 = num["Lam0"]

    def second(B, A):
        nu1 = L0 * B ** 2 / (2 * sR)                   # the part of nu that comes from |Delta e|^2
        return nu1, eta + float(np.sum(2 * v * Xop * nu1 + 2 * A * Xop * B + (v + A) * B ** 2))

    for _ in range(iterations):
        nu1, E = second(B, A)
        Bn = np.minimum(B, Ts * viol + Cs * E + nu1)
        An = np.minimum(A, fo["T_w"] * viol + fo["C_w"] * E)
        done = np.allclose(Bn, B, rtol=1e-14, atol=0) and np.allclose(An, A, rtol=1e-14, atol=0)
        B, A = Bn, An
        if done:
            break
    nu1, E = second(B, A)
    return dict(B=B, Aw=min(float(np.linalg.norm(A)), fo["T_w"] * viol + fo["C_w"] * E), crude=cr["B"], E=E,
                ulow=cr["ulow"])


def exact_reference(w, Xs):
    """The reference of an exact mixture: its centred stack, coordinate blocks, its weights."""
    K = len(Xs)
    Xc = [centre(X) for X in Xs]
    Z = np.hstack([np.sqrt(wk) * X for wk, X in zip(w, Xc)])
    Qs = [np.eye(D * K)[:, D * k:D * k + D] for k in range(K)]
    return dict(Z=Z, Qs=Qs, v=np.asarray(w, dtype=float), states=Xc, K=K, m=D * K)


def polish(Gt, states, weights, n):
    """Least squares over exact K-mixtures of chains (weights on the simplex, torsions), started
    at the DEMIX output: returns (weights, torsions, chains, residual ||G(mixture) - Gt||_F)."""
    K = len(states)
    x0 = np.concatenate([np.asarray(weights[:K - 1]) / np.sum(weights)] + [torsions_of(X) for X in states])

    def unpack(x):
        wfree = x[:K - 1]
        w = np.concatenate([wfree, [1 - wfree.sum()]])
        tors = [x[K - 1 + k * (n - 3):K - 1 + (k + 1) * (n - 3)] for k in range(K)]
        return w, tors

    def res(x):
        w, tors = unpack(x)
        return (gram([chain(n, t) for t in tors], w) - Gt).ravel()

    sol = least_squares(res, x0, xtol=1e-15, ftol=1e-15, gtol=1e-15)
    w, tors = unpack(sol.x)
    Xs = [chain(n, t) for t in tors]
    return w, tors, Xs, float(np.linalg.norm(gram(Xs, w) - Gt))


# ------------------------------------------------------------------ competitors
def random_mixture(K, n, seed):
    rng = np.random.default_rng(seed)
    w = rng.dirichlet(np.ones(K) * 4)
    tors = [rng.uniform(-np.pi, np.pi, n - 3) for _ in range(K)]
    return w, tors, [chain(n, t) for t in tors]


def far_near_affine(ref, num, n, rng, starts=12):
    """Chains that are nearly affine images of the stack: local minima of phi over the torsions
    from random starts.  Returns (phi, distance to the nearest reference state) pairs."""
    Pi, J = num["Pi"], num["J"]
    out = []
    for _ in range(starts):
        t0 = rng.uniform(-np.pi, np.pi, n - 3)
        res = least_squares(lambda t: ((J - Pi) @ chain(n, t)).ravel(), t0, xtol=1e-12, ftol=1e-12)
        Y = chain(n, res.x)
        rep = chain_report(ref, num, Y)
        out.append((rep["phi"], rep["dist"], rep))
    return out


# ------------------------------------------------------------------ checks
def check_instance(K, n, seed, noise=0.0, verbose=True):
    rng = np.random.default_rng(1000 + seed)
    w, tors, Xs = random_mixture(K, n, seed)
    edges, lengths = chain_edges(n)
    G = gram(Xs, w)
    Nz = rng.normal(size=G.shape)
    Nz = (Nz + Nz.T) / 2
    Jn = np.eye(n) - np.ones((n, n)) / n
    Nz = Jn @ Nz @ Jn
    Gt = G + noise * Nz / np.linalg.norm(Nz)                 # ||Gt - G||_F = noise exactly
    ref = reference(Gt, edges, lengths, K, rng)
    num = numbers(ref, Gt, edges, lengths)
    bad = []
    stats = dict(K=K, n=n, noise=noise, sigma_perp=num["sigma_perp"], tau_max=num["tau_max"],
                 lam_m=num["lam_m"], a=num["a"], phi_max=phi_max(num))
    # (1) Lemma N0 / Theorem N1(b) on chains: near the true states, random, and near-affine far chains
    applicable = 0
    worst_ratio = 0.0
    for k in range(K):
        for scale in (1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1):
            for _ in range(6):
                Y = chain(n, tors[k] + scale * rng.normal(size=n - 3))
                rep = chain_report(ref, num, Y)
                bad += [("chain", v_) for v_ in rep["violations"]]
                if rep["applicable"]:
                    applicable += 1
                    worst_ratio = max(worst_ratio, rep["dist"] / rep["bound"])
    for _ in range(40):
        rep = chain_report(ref, num, chain(n, rng.uniform(-np.pi, np.pi, n - 3)))
        bad += [("random chain", v_) for v_ in rep["violations"]]
        applicable += rep["applicable"]
    far = far_near_affine(ref, num, n, rng)
    for phi, dist, rep in far:
        bad += [("near-affine chain", v_) for v_ in rep["violations"]]
        applicable += rep["applicable"]
    far_phi = min([phi for phi, dist, rep in far if dist > 1.0], default=np.inf)
    stats.update(chains_applicable=applicable, chain_ratio=worst_ratio, far_phi=far_phi)
    # (2) Theorem N1(a): ensembles (split states, an extra state of small weight)
    for trial in range(6):
        t = 10.0 ** rng.uniform(-5, -2)
        Ys, u = [], []
        for k in range(K):
            dirn = rng.normal(size=n - 3)
            Ys += [chain(n, tors[k] + t * dirn), chain(n, tors[k] - t * dirn)]
            u += [w[k] / 2, w[k] / 2]
        if trial % 2:
            extra = 10.0 ** rng.uniform(-8, -5)
            Ys.append(chain(n, rng.uniform(-np.pi, np.pi, n - 3)))
            u = [x * (1 - extra) for x in u] + [extra]
        u = np.array(u)
        eps = float(np.linalg.norm(gram(Ys, u) - Gt))
        Phi = np.sqrt(n - 1 - num["m"]) * eps + num["tail"]
        mean_phi = sum(uk * float((((num["J"] - num["Pi"]) @ Y) ** 2).sum()) for uk, Y in zip(u, Ys))
        if mean_phi > Phi * (1 + 1e-9) + 1e-12:
            bad.append(("ensemble", "mean phi"))
        phi1 = phi_max(num, 0.5)
        if phi1 > 0:
            far_mass = sum(uk for uk, Y in zip(u, Ys) if chain_report(ref, num, Y)["dist"] > radius(num, phi1))
            if far_mass > Phi / phi1 * (1 + 1e-9) + 1e-12:
                bad.append(("ensemble", "enclosure"))
    # (3) Theorem N2: the truth and perturbed K-mixtures
    reports = [mixture_report(ref, num, Gt, Xs, w)]
    for trial in range(8):
        t = 10.0 ** rng.uniform(-8, -4)
        Ys = [chain(n, tors[k] + t * rng.normal(size=n - 3)) for k in range(K)]
        u = w * (1 + t * rng.normal(size=K))
        u = u / u.sum()
        reports.append(mixture_report(ref, num, Gt, Ys, u))
    n2_app = 0
    n2_ratio = 0.0
    for rep in reports:
        bad += [("mixture", v_) for v_ in rep["violations"]]
        if rep.get("applicable"):
            n2_app += 1
            n2_ratio = max(n2_ratio, rep["state_err"] / rep["state_bound"])
    stats.update(n2_applicable=n2_app, n2_ratio=n2_ratio, truth=reports[0])
    if verbose:
        tr = reports[0]
        print(f"K = {K}, n = {n}, noise {noise:.0e}: sigma_perp {num['sigma_perp']:.3e}, tau_max {num['tau_max']:.1e}, "
              f"phi_max {stats['phi_max']:.2e}; chains with the hypothesis {applicable} (worst distance/bound "
              f"{worst_ratio:.3f}); smallest phi of a far near-affine chain {far_phi:.2e}; "
              f"K-mixtures with the hypothesis {n2_app} of {len(reports)} (worst error/bound {n2_ratio:.4f}); "
              + (f"truth: state error {tr['state_err']:.2e} <= {tr['state_bound']:.2e}; " if tr.get("applicable")
                 else "truth outside the certified range; ")
              + ("OK" if not bad else "VIOLATIONS " + str(sorted(set(bad)))))
    stats["bad"] = bad
    return stats


def torsion_direction(n, tors, tau, h=1e-6):
    """Torsion velocities whose chain displacement, modulo isometries, is closest to tau."""
    X0 = chain(n, tors)
    Tq = trivial_motions(centre(X0))
    cols = []
    for i in range(n - 3):
        tp, tm = tors.copy(), tors.copy()
        tp[i] += h
        tm[i] -= h
        dX = (centre(chain(n, tp)) - centre(chain(n, tm))).ravel() / (2 * h)
        cols.append(dX - Tq @ (Tq.T @ dX))
    return np.linalg.lstsq(np.array(cols).T, tau, rcond=None)[0]


def sharp_report(num, fo, w, Xs, edges, Ys, u, delta_norm_used=0.0):
    """Theorem N3 for the competitor (Ys, u) against the exact reference (Xs, w): every step of
    the proof with the actual quantities, then the conclusions with the certified bounds."""
    K, n = len(Xs), len(Xs[0])
    out = dict(violations=[])
    eta = float(np.linalg.norm(gram(Ys, u) - gram(Xs, w)))
    out["eta"] = eta
    best = None
    for perm in itertools.permutations(range(K)):
        errs = [d_procrustes(Xs[k], Ys[perm[k]])[0] for k in range(K)]
        if best is None or max(errs) < max(best[1]):
            best = (perm, errs)
    perm, errs = best
    out["errs"] = errs
    a = np.array([u[perm[k]] - w[k] for k in range(K)])
    # steps of the proof with actual quantities
    Lsum = np.zeros((n, n))
    second = 0.0
    lin_nu = 0.0
    for k in range(K):
        Xc = centre(Xs[k])
        Yal = centre(Ys[perm[k]]) @ d_procrustes(Xs[k], Ys[perm[k]])[1].T
        Dl = Yal - Xc
        Bk = fo["bases"][k]
        tau = Bk @ (Bk.T @ Dl.ravel())
        nu = Dl.ravel() - tau
        nu_bound = (delta_norm_used + num["Lam0"] * (Dl ** 2).sum()) / (2 * fo["sR"][k])
        if np.linalg.norm(nu) > nu_bound * (1 + 1e-9) + 1e-11:
            out["violations"].append("nu")
        taum = tau.reshape(n, 3)
        Lsum += a[k] * Xc @ Xc.T + w[k] * (Xc @ taum.T + taum @ Xc.T)
        lin_nu += 2 * w[k] * fo["Xop"][k] * np.linalg.norm(nu)
        dn = np.linalg.norm(Dl)
        second += 2 * abs(a[k]) * fo["Xop"][k] * dn + (w[k] + abs(a[k])) * dn ** 2
    if np.linalg.norm(Lsum) > (eta + lin_nu + second) * (1 + 1e-9) + 1e-11:
        out["violations"].append("linear part")
    res = theorem_N3(num, fo, eta)
    out["applicable"] = res is not None
    if res is None:
        return out
    out["bounds"] = res["B"]
    out["crude"] = res["crude"]
    if any(e > bd * (1 + 1e-9) + 1e-11 for e, bd in zip(errs, res["B"])):
        out["violations"].append("states")
    out["w_err"], out["w_bound"] = float(np.linalg.norm(a)), res["Aw"]
    if out["w_err"] > res["Aw"] * (1 + 1e-9) + 1e-11:
        out["violations"].append("weights")
    out["ratio"] = max(e / bd for e, bd in zip(errs, res["B"]))
    out["first_order_ratio"] = max(e / (cs * eta) for e, cs in zip(errs, fo["C_state"]))
    return out


def check_sharp(K, n, seed, verbose=True):
    """Theorem N3 at an exact mixture: random K-state competitors at several scales, and the
    competitor along the direction that attains C_state for the first state."""
    rng = np.random.default_rng(2000 + seed)
    w, tors, Xs = random_mixture(K, n, seed)
    edges, lengths = chain_edges(n)
    ref = exact_reference(w, Xs)
    num = numbers(ref, gram(Xs, w), edges, lengths)
    fo = first_order(Xs, w, edges)
    bad, app, ratio = [], 0, 0.0
    for scale in (1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3):
        for _ in range(3):
            Ys = [chain(n, tors[k] + scale * rng.normal(size=n - 3)) for k in range(K)]
            u = w * (1 + scale * rng.normal(size=K))
            u = u / u.sum()
            rep = sharp_report(num, fo, w, Xs, edges, Ys, u)
            bad += rep["violations"]
            if rep["applicable"]:
                app += 1
                ratio = max(ratio, rep["ratio"])
    # the direction attaining C_state[0]
    rows = fo["rows"]("x", 0)
    y = np.linalg.svd(fo["pinv"][rows])[2][0]             # data direction with the largest response of state 0
    x = fo["pinv"] @ y
    attained = None
    for t in (1e-9, 1e-8, 1e-7):
        Ys, u = [], np.array(w, dtype=float)
        for k in range(K):
            coef = x[fo["rows"]("x", k)]
            tau = fo["bases"][k] @ coef
            Ys.append(chain(n, tors[k] + t * torsion_direction(n, tors[k], tau)))
        if K > 1:
            u = u + t * (fo["Wm"] @ x[fo["rows"]("w")])
        rep = sharp_report(num, fo, w, Xs, edges, Ys, u)
        bad += rep["violations"]
        if rep["applicable"]:
            attained = rep["errs"][0] / (fo["C_state"][0] * rep["eta"])
            ratio = max(ratio, rep["ratio"])
    stats = dict(K=K, n=n, applicable=app, ratio=ratio, attained=attained, bad=bad, C_state=fo["C_state"],
                 C_w=fo["C_w"], injective=fo["injective"])
    if verbose:
        print(f"K = {K}, n = {n}: first-order constants C_state {[round(c, 2) for c in fo['C_state']]}, C_w {fo['C_w']:.3f}; "
              f"competitors in the certified range {app}; worst error/bound {ratio:.3f}; along the extremal direction "
              f"displacement/(C_state eta) = {attained if attained is None else round(attained, 4)}; "
              + ("OK" if not bad and fo["injective"] else "VIOLATIONS " + str(sorted(set(bad)))))
    return stats


def a_posteriori(K, n, seed, noise, verbose=True):
    """From noisy data alone: DEMIX, polish to an exact mixture mu_0 with residual eps_0, then
    Theorem N3 at mu_0 with eta = eps + eps_0.  The truth is one of the competitors."""
    rng = np.random.default_rng(3000 + seed)
    w, tors, Xs = random_mixture(K, n, seed)
    edges, lengths = chain_edges(n)
    G = gram(Xs, w)
    Nz = rng.normal(size=G.shape)
    Nz = (Nz + Nz.T) / 2
    Jn = np.eye(n) - np.ones((n, n)) / n
    Nz = Jn @ Nz @ Jn
    Gt = G + noise * Nz / np.linalg.norm(Nz)
    ref = reference(Gt, edges, lengths, K, rng)
    w0, tors0, X0, eps0 = polish(Gt, ref["states"], ref["v"], n)
    num = numbers(exact_reference(w0, X0), gram(X0, w0), edges, lengths)
    fo = first_order(X0, w0, edges)
    res = theorem_N3(num, fo, noise + eps0)
    best = None
    for perm in itertools.permutations(range(K)):
        errs = [d_procrustes(X0[k], Xs[perm[k]])[0] for k in range(K)]
        if best is None or max(errs) < max(best[1]):
            best = (perm, errs)
    perm, errs = best
    werr = float(np.linalg.norm([w[perm[k]] - w0[k] for k in range(K)]))
    out = dict(noise=noise, eps0=eps0, errs=errs, werr=werr, certified=res is not None, bad=[])
    if res is not None:
        out["bounds"], out["w_bound"] = res["B"], res["Aw"]
        if any(e > bd * (1 + 1e-9) + 1e-11 for e, bd in zip(errs, res["B"])) or werr > res["Aw"] * (1 + 1e-9) + 1e-11:
            out["bad"].append("a posteriori")
    if verbose:
        print(f"K = {K}, n = {n}, noise {noise:.0e}: residual of the polished mixture {eps0:.2e}; truth within "
              f"{max(errs):.2e} of it (weights {werr:.1e}); "
              + (f"certified bound {max(res['B']):.2e} (weights {res['Aw']:.1e}); " if res is not None
                 else "outside the certified range; ")
              + ("OK" if not out["bad"] else "VIOLATION"))
    return out


def tolerance_constant(w, Xs, edges, lengths):
    """Exact data, statewise constraints known only within a tolerance.  The K-state mixtures
    with the same data are the blocks of z Q, Q orthogonal, with any weights; to first order
    Q = exp(t Xi) with Xi skew (off-diagonal blocks free), u = w + t a (sum a = 0).  Returns
    c_tol[k] = max ||displacement of state k modulo isometries||_F / ||all violations||_2,
    the extremal parameter for state 0, and a function building the finite-t competitor."""
    from scipy.linalg import expm
    K, n = len(Xs), len(Xs[0])
    Xc = [centre(X) for X in Xs]
    l2 = np.asarray(lengths) ** 2
    pairs = [(k, l) for k in range(K) for l in range(k + 1, K)]
    p = 9 * len(pairs) + (K - 1)

    def unpack(x):
        Xi = np.zeros((D * K, D * K))
        for t, (k, l) in enumerate(pairs):
            Bm = x[9 * t:9 * t + 9].reshape(3, 3)
            Xi[D * k:D * k + D, D * l:D * l + D] = Bm
            Xi[D * l:D * l + D, D * k:D * k + D] = -Bm.T
        c = x[9 * len(pairs):]
        a = np.concatenate([c, [-c.sum()]])
        return Xi, a

    Dk = [np.zeros((3 * n, p)) for _ in range(K)]
    Vm = np.zeros((K * len(edges), p))
    Tq = [trivial_motions(X) for X in Xc]
    for col in range(p):
        x = np.zeros(p)
        x[col] = 1
        Xi, a = unpack(x)
        for k in range(K):
            Yd = sum(np.sqrt(w[l] / w[k]) * Xc[l] @ Xi[D * l:D * l + D, D * k:D * k + D] for l in range(K) if l != k)
            Yd = Yd - a[k] / (2 * w[k]) * Xc[k]
            for t, (i, j) in enumerate(edges):
                Vm[k * len(edges) + t, col] = 2 * (Xc[k][j] - Xc[k][i]) @ (Yd[j] - Yd[i])
            yd = Yd.ravel()
            Dk[k][:, col] = yd - Tq[k] @ (Tq[k].T @ yd)
    sv = np.linalg.svd(Vm, compute_uv=False)
    injective = bool(sv[-1] > 1e-9 * sv[0])
    Vp = np.linalg.pinv(Vm)
    c_tol = [float(np.linalg.norm(Dk[k] @ Vp, 2)) for k in range(K)]
    y = np.linalg.svd(Dk[0] @ Vp)[2][0]
    x_ext = Vp @ y

    def competitor(x, t):
        Xi, a = unpack(x)
        Z = np.hstack([np.sqrt(wk) * X for wk, X in zip(w, Xc)]) @ expm(t * Xi)
        u = np.asarray(w) + t * a
        Ys = [Z[:, D * k:D * k + D] / np.sqrt(u[k]) for k in range(K)]
        viol = np.array([[((Y[j] - Y[i]) ** 2).sum() - l2[tt] for tt, (i, j) in enumerate(edges)] for Y in Ys])
        return Ys, u, viol

    return dict(c_tol=c_tol, x_ext=x_ext, competitor=competitor, injective=injective, dim=p)


def check_tolerance(K, n, seed, verbose=True):
    """Tolerance on the statewise constraints with exact data: the explicit family of competitors,
    the first-order constant c_tol (attained), and Theorem N3 with the tolerance in its bounds."""
    rng = np.random.default_rng(4000 + seed)
    w, tors, Xs = random_mixture(K, n, seed)
    edges, lengths = chain_edges(n)
    G = gram(Xs, w)
    fo = first_order(Xs, w, edges)
    tc = tolerance_constant(w, Xs, edges, lengths)
    bad, app, attained, worst = [], 0, None, 0.0
    trials = [(tc["x_ext"], t) for t in (1e-8, 1e-7, 1e-6)] + \
             [(rng.normal(size=tc["dim"]), 10.0 ** rng.uniform(-9, -4)) for _ in range(8)]
    for idx, (x, t) in enumerate(trials):
        Ys, u, viol = tc["competitor"](x / np.linalg.norm(x), t)
        same_data = float(np.linalg.norm(gram(Ys, u) - G))
        if same_data > 1e-10:
            bad.append("the family changes the data")
        delta = np.abs(viol).max(0)
        num = numbers(exact_reference(w, Xs), G, edges, lengths, delta)
        errs = [d_procrustes(Xs[k], Ys[k])[0] for k in range(K)]
        allnorm = float(np.linalg.norm(viol))
        if any(e > c * allnorm * (1 + 1e-3) + 1e-11 for e, c in zip(errs, tc["c_tol"])) and t <= 1e-6:
            bad.append("first-order tolerance constant exceeded")
        if idx < 3:
            attained = errs[0] / (tc["c_tol"][0] * allnorm)
        res = theorem_N3(num, fo, max(same_data, 1e-15))
        if res is not None:
            app += 1
            worst = max(worst, max(e / bd for e, bd in zip(errs, res["B"])))
            if any(e > bd * (1 + 1e-9) + 1e-11 for e, bd in zip(errs, res["B"])):
                bad.append("Theorem N3 with tolerance")
    C_up = np.array(fo["T_state"])                     # certified first-order constants (all-violation norm)
    if any(cu < ct * (1 - 1e-6) for cu, ct in zip(C_up, tc["c_tol"])):
        bad.append("certified tolerance constant below the attained one")
    if verbose:
        print(f"K = {K}, n = {n}: tolerance constants c_tol {[round(c, 2) for c in tc['c_tol']]} (attained: ratio "
              f"{attained:.4f}); certified first-order constants of Theorem N3 {[round(float(c), 2) for c in C_up]}; "
              f"competitors in the certified range {app}, worst error/bound {worst:.3f}; "
              + ("OK" if not bad and tc["injective"] else "VIOLATIONS " + str(sorted(set(bad)))))
    return dict(bad=bad, c_tol=tc["c_tol"], C_up=C_up, attained=attained, applicable=app, injective=tc["injective"])


def count_states(Gt, eps):
    """Proposition N5: the number of eigenvalues of Gt above eps, divided by three (None if it
    is not a multiple of three)."""
    r = int((np.linalg.eigvalsh(Gt) > eps).sum())
    return r // D if r % D == 0 else None


def check_count(K, n, seed, verbose=True):
    """Noise of operator norm eps for eps up to just below lambda_m / 2: the count is K."""
    rng = np.random.default_rng(5000 + seed)
    w, tors, Xs = random_mixture(K, n, seed)
    G = gram(Xs, w)
    lam = np.sort(np.linalg.eigvalsh(G))[::-1][D * K - 1]
    Jn = np.eye(n) - np.ones((n, n)) / n
    wrong, fixed_rule_wrong = 0, 0
    for frac in (1e-6, 1e-4, 1e-2, 0.1, 0.3, 0.49):
        for _ in range(5):
            Nz = rng.normal(size=G.shape)
            Nz = Jn @ (Nz + Nz.T) @ Jn
            eps = frac * lam
            Gt = G + eps * Nz / np.linalg.norm(Nz, 2)            # operator norm of the error = eps
            wrong += count_states(Gt, eps) != K
            ev = np.linalg.eigvalsh(Gt)
            fixed_rule_wrong += int((ev > 1e-8 * ev[-1]).sum()) != D * K
    if verbose:
        print(f"K = {K}, n = {n}: lambda_m = {lam:.3f}; count with threshold eps wrong in {wrong} of 30 "
              f"(errors up to 0.49 lambda_m); the fixed relative threshold 1e-8 wrong in {fixed_rule_wrong} of 30; "
              + ("OK" if wrong == 0 else "VIOLATION"))
    return dict(bad=["count"] * wrong, fixed_rule_wrong=fixed_rule_wrong)


def table_row(K, n, seed):
    w, tors, Xs = random_mixture(K, n, seed)
    edges, lengths = chain_edges(n)
    G = gram(Xs, w)
    num = numbers(exact_reference(w, Xs), G, edges, lengths)
    fo = first_order(Xs, w, edges)

    def largest(pred, hi):
        lo = 0.0
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if pred(mid) else (lo, mid)
        return lo

    cs = max(fo["C_state"])
    eta_crude = largest(lambda e: theorem_N2(num, e) is not None, num["lam_m"])
    eta_half = largest(lambda e: theorem_N2(num, e, u0=w.min() / 2) is not None, num["lam_m"])

    def sharp(e):
        r = theorem_N3(num, fo, e)
        return r is not None and max(r["B"]) <= 1.5 * cs * e

    eta_sharp = largest(sharp, num["lam_m"])
    tiny = eta_crude * 1e-6
    r2 = theorem_N2(num, tiny)
    C_crude = max(r2["B"]) / tiny if r2 is not None else np.inf
    ph = phi_max(num, 0.5)
    kappa = min(ph / radius(num, ph) ** 2, ph / (2 * num["D2"])) if ph > 0 else 0.0
    return dict(K=K, n=n, sigma=num["sigma_perp"], lam_m=num["lam_m"], normG=float(np.linalg.norm(G)), cs=cs,
                cw=fo["C_w"], C_crude=C_crude, eta_crude=eta_crude, eta_half=eta_half, eta_sharp=eta_sharp,
                phi_max=phi_max(num), kappa=kappa)


def main():
    if "--table" in sys.argv:
        print(" K   n   sigma_c   lambda_m  ||G||   C_state  C_w     C_crude   eta_crude  (w>=wmin/2)  eta_sharp  "
              "phi_max   kappa >=")
        for K, n in ((2, 12), (2, 16), (2, 24), (2, 40), (3, 23), (3, 30), (3, 45), (4, 39), (4, 48)):
            r = table_row(K, n, seed=7)
            print(f"{K:2d} {n:3d}   {r['sigma']:.1e}   {r['lam_m']:.1e}   {r['normG']:5.1f}   {r['cs']:5.2f}   {r['cw']:.3f}   "
                  f"{r['C_crude']:.1e}   {r['eta_crude']:.1e}    {r['eta_half']:.1e}     {r['eta_sharp']:.1e}    "
                  f"{r['phi_max']:.1e}   {r['kappa']:.1e}")
        return 0
    ok = True
    print("Lemma N0, Theorems N1, N2 (reference cut from the data, possibly noisy)")
    for K, n, seed, noise in ((2, 16, 3, 0.0), (2, 16, 3, 1e-7), (2, 24, 5, 1e-6), (3, 30, 7, 1e-7), (2, 40, 11, 1e-5)):
        st = check_instance(K, n, seed, noise)
        ok &= not st["bad"]
    print("Theorem N3 (reference an exact mixture)")
    for K, n, seed in ((2, 16, 3), (2, 24, 5), (3, 30, 7)):
        st = check_sharp(K, n, seed)
        ok &= not st["bad"] and st["injective"] and st["applicable"] > 0
    print("A posteriori (DEMIX, polish, Theorem N3 at the polished mixture)")
    for K, n, seed, noise in ((2, 16, 3, 1e-9), (2, 24, 5, 1e-8), (2, 24, 5, 1e-4), (3, 30, 7, 1e-9)):
        st = a_posteriori(K, n, seed, noise)
        ok &= not st["bad"]
    print("Number of states (Proposition N5)")
    for K, n, seed in ((2, 16, 3), (3, 30, 7)):
        st = check_count(K, n, seed)
        ok &= not st["bad"] and st["fixed_rule_wrong"] > 0
    print("Tolerance on the statewise constraints (exact data)")
    for K, n, seed in ((2, 16, 3), (2, 24, 5), (3, 30, 7)):
        st = check_tolerance(K, n, seed)
        ok &= not st["bad"] and st["injective"] and st["applicable"] > 0 and abs(st["attained"] - 1) < 1e-2
    print("ALL OK" if ok else "SOME FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
