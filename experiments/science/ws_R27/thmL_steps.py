#!/usr/bin/env python3
"""Workstream R27 -- every intermediate inequality of the proof of Theorem L (Steps 1-4) for one pair (X, Y),
written from the statement and the proof text of the note (section 3).  Returns the ratio LHS/RHS of each inequality
(<= 1 means the inequality holds) and the residuals of the two identities.

A ratio is recorded only when its right-hand side is above `floor` (otherwise both sides are rounding noise and the check
is LHS <= atol).  Nothing here is fitted: every quantity is computed as the note defines it.
"""
import numpy as np
from r27lib import (KAPPA, chain_consts, pair_arrays, eta_vec, window_pair_index, procrustes, procrustes_proper)

SQ3 = np.sqrt(3.0)


def check_pair(X, Y, cache=None, want_controls=True):
    n = len(X)
    if cache is None:
        cache = prepare(X)
    tau, s, b = cache["tau"], cache["s"], cache["b"]
    J, Kk, widx = cache["J"], cache["K"], cache["widx"]
    cW = cache["cW"]
    scale = max(1.0, np.abs(X - X.mean(0)).max(), np.abs(Y - Y.mean(0)).max())
    atol = 1e-9 * scale
    floor = 1e-7 * scale
    out = {}
    viol = []

    def rec(name, lhs, rhs):
        """record inequality lhs <= rhs"""
        if rhs > floor:
            r = lhs / rhs
            out[name] = max(out.get(name, 0.0), r)
            if lhs > rhs * (1 + 1e-9) + atol:
                viol.append((name, lhs, rhs))
        else:
            out.setdefault(name, 0.0)
            if lhs > rhs + atol * max(1.0, scale):
                viol.append((name, lhs, rhs))

    eta = eta_vec(X, Y, J, Kk)
    eta_norm = np.linalg.norm(eta)
    e = np.array([np.linalg.norm(eta[ix]) for ix in widx])
    delta = KAPPA * e / s

    # ---- Step 1: Lemma Q on every five-point window -------------------------------------------------------------
    R, t, eps = [], [], []
    for i in range(n - 4):
        Ri, ti, res = procrustes(X[i:i + 5], Y[i:i + 5])
        R.append(Ri); t.append(ti); eps.append(res)
        rec("S1  ||eps_i|| <= kappa e_i/s_i", np.linalg.norm(res), delta[i])
    # ---- Step 2: consecutive frames ------------------------------------------------------------------------------
    m = []
    id2a = id2b = 0.0
    for j in range(n - 5):
        XW = X[j + 1:j + 5]
        c = cW[j + 1]
        dR = R[j] - R[j + 1]
        ej = eps[j][1:5]            # residual of window j on the shared rows
        ej1 = eps[j + 1][0:4]       # residual of window j+1 on the shared rows
        lhs_mat = (XW - c) @ dR
        rhs_mat = (ej1 - ej) - (ej1 - ej).mean(0)
        id2a = max(id2a, np.abs(lhs_mat - rhs_mat).max())
        rec("S2a ||(X_W-1c)(R_j-R_j+1)|| <= d_j+d_j+1", np.linalg.norm(lhs_mat), delta[j] + delta[j + 1])
        rec("S2b ||R_j-R_j+1||_F <= (d_j+d_j+1)/tau_j+1", np.linalg.norm(dR), (delta[j] + delta[j + 1]) / tau[j + 1])
        mj = ej.mean(0) - ej1.mean(0)
        m.append(mj)
        id2b = max(id2b, np.abs((t[j + 1] - t[j]) - (c @ dR + mj)).max())
        rec("S2c |m_j| <= (d_j+d_j+1)/2", np.linalg.norm(mj), (delta[j] + delta[j + 1]) / 2)
    out["ID2a centred identity (abs residual / scale)"] = id2a / scale
    out["ID2b translation identity (abs residual / scale)"] = id2b / scale
    # ---- Step 3: telescoping and (local) --------------------------------------------------------------------------
    g_res = Y - X @ R[0] - t[0]
    dist = np.linalg.norm(g_res, axis=1)
    local = np.zeros(n)
    id3 = 0.0
    for k in range(n):
        i = min(k, n - 5)
        acc = eps[i][k - i].copy()
        bound = delta[i]
        for j in range(i):
            acc += (X[k] - cW[j + 1]) @ (R[j + 1] - R[j]) + m[j]
            bound += (delta[j] + delta[j + 1]) * (np.linalg.norm(X[k] - cW[j + 1]) / tau[j + 1] + 0.5)
        id3 = max(id3, np.abs(acc - g_res[k]).max())
        local[k] = bound
        rec("S3  (local) |y_k - g x_k| <= local_k", dist[k], bound)
    out["ID3 telescoping identity (abs residual / scale)"] = id3 / scale
    # ---- Step 4: uniform constants ---------------------------------------------------------------------------------
    ts, ss = tau.min(), s.min()
    for k in range(n):
        i = min(k, n - 5)
        for j in range(i):
            # 1-based: |x_k - c_{j+1}| <= b (k - j + 1/2); 0-based k0 - j0 is the same difference
            rec("S4a |x_k - c_j+1| <= b(k-j+1/2)", np.linalg.norm(X[k] - cW[j + 1]), b * (k - j + 0.5))
    rec("S4b sum e_j^2 <= 4 ||eta||^2", float((e ** 2).sum()), 4 * eta_norm ** 2)
    if n > 5:
        rec("S4c sum (d_j+d_j+1)^2 <= (4 kappa ||eta||/s*)^2", float(((delta[:-1] + delta[1:]) ** 2).sum()),
            (4 * KAPPA * eta_norm / ss) ** 2)
    k1 = np.arange(1, n + 1)
    pt = (KAPPA * eta_norm / ss) * (4 * b * (k1 + 0.5) ** 1.5 / (SQ3 * ts) + 2 * np.sqrt(k1) + 1)
    for k in range(n):
        rec("S4d per-point uniform bound", dist[k], pt[k])
        rec("S4d' local_k <= per-point uniform bound", local[k], pt[k])
    frob_g = np.linalg.norm(g_res)
    U118 = 1.18 * b / (ss * ts) * (n + 1.5) ** 2 * eta_norm
    U12 = 1.2 * b / (ss * ts) * (n + 2) ** 2 * eta_norm
    rec("S4e ||Y - gX||_F <= 1.18 (b/(s*tau*)) (n+3/2)^2 ||eta||", frob_g, U118)
    rec("S4e' ||pt||_2 <= 1.18 (...)", np.linalg.norm(pt), U118)
    rec("S4f tau* <= 1.3 b", ts, 1.3 * b)
    R0, t0, res0 = procrustes(X, Y)
    d_p = np.linalg.norm(res0)
    rec("FIN d_P <= ||Y - g1 X||_F", d_p, frob_g)
    rec("FIN d_P <= ||local||_2", d_p, np.linalg.norm(local))
    rec("FIN d_P <= uniform (1.2 (b/(s*tau*)) (n+2)^2 ||eta||)", d_p, U12)
    out["_dP"] = d_p
    out["_eta"] = eta_norm
    out["_local_frob"] = np.linalg.norm(local)
    out["_uniform"] = U12
    out["_frob_g1"] = frob_g
    out["_perpoint_max_ratio"] = out.get("S3  (local) |y_k - g x_k| <= local_k", 0.0)
    out["_det_changes"] = int(sum(1 for j in range(n - 5) if np.linalg.det(R[j]) * np.linalg.det(R[j + 1]) < 0))
    out["_det_first"] = float(np.sign(np.linalg.det(R[0])))
    # ---- controls (inequalities that are NOT claimed; each must be violated by some pair of the battery) ----------
    ctl = {}
    if want_controls:
        sep = Kk - J
        eta3 = np.linalg.norm(eta[sep <= 3])
        C = 1.2 * b / (ss * ts) * (n + 2) ** 2
        tolc = 1e-6 * scale
        ctl["C1 uniform bound with the separation-4 errors left out of eta"] = bool(d_p > C * eta3 * (1 + 1e-9) + tolc)
        for F in (10.0, 100.0, 1000.0, 1e4):
            ctl[f"C2 uniform constant divided by {F:g}"] = bool(d_p > C / F * eta_norm * (1 + 1e-9) + tolc)
        ctl["C3 Lemma Q with the first-order constant 1/2 in place of kappa"] = bool(any(
            np.linalg.norm(eps[i]) > 0.5 * e[i] / s[i] * (1 + 1e-9) + tolc for i in range(n - 4)))
        bad = False
        for i in range(n - 4):
            _, _, resp = procrustes_proper(X[i:i + 5], Y[i:i + 5])
            if np.linalg.norm(resp) > delta[i] * (1 + 1e-9) + tolc:
                bad = True
                break
        ctl["C4 Lemma Q with proper rotations only"] = bad
        ctl["C5 Step 2 with the five-point thickness s_j in place of tau_j+1"] = bool(any(
            np.linalg.norm(R[j] - R[j + 1]) > (delta[j] + delta[j + 1]) / s[j] * (1 + 1e-9) + tolc for j in range(n - 5)))
        ctl["C6 Step 4 with 'a pair lies in at most THREE windows'"] = bool((e ** 2).sum() > 3 * eta_norm ** 2 * (1 + 1e-9) + tolc ** 2)
        # (local) with the lever-arm term dropped: delta_i + sum (d_j + d_j+1)/2
        loc_nolever = np.array([delta[min(k, n - 5)] + sum((delta[j] + delta[j + 1]) * 0.5 for j in range(min(k, n - 5)))
                                for k in range(n)])
        ctl["C7 (local) without the lever-arm term |x_k - c|/tau"] = bool(np.any(dist > loc_nolever * (1 + 1e-9) + tolc))
        ctl["C8 (local) divided by 10"] = bool(np.any(dist > local / 10 * (1 + 1e-9) + tolc))
    return out, viol, ctl


def prepare(X):
    n = len(X)
    tau, s, b = chain_consts(X)
    J, Kk = pair_arrays(n)
    return dict(tau=tau, s=s, b=b, J=J, K=Kk, widx=window_pair_index(n, J, Kk),
                cW=np.array([X[i:i + 4].mean(0) for i in range(n - 3)]))
