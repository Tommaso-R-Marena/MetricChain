"""
P4 item 2: the pairwise lower models of third order (Theorem 11.18a of the theory report at 24a3c27)
on P2's enumerated instances, residual g_GB, with P2's measured third-order class constants c_T
(exact maxima of the third mixed difference over all boxes of X'; recomputed here with my own
routine and compared with P2's stored values).  Reference x0 = argmin E over X'.

Models (all of the form  m = f + I_2 g - penalty(changed set S)):
  env3   penalty = sum_{T subset S} c_T                 the exact envelope (three-body; Theorem 11.18)
  site   penalty = sum_{i in S} gamma_i,   gamma_i  = (1/3) sum_{T contains i} c_T          (site form)
  pair   penalty = sum_{i<j in S} gamma_ij, gamma_ij = (1/3) sum_{T contains i,j} c_T        (pair form)
  LP-A   pair shares mu_{T,p} >= 0, sum_p mu_{T,p} = 1, chosen by a linear programme to maximise
         the margin  min_{x != x0} m(x) - m(x0)
  LP-B   the same, chosen to minimise the largest gap max_x (E - m)
  LZ     the same, chosen (L-BFGS on a softmax parametrisation; "best found") to minimise ln Z(m)
  CV-A / CV-B   as LP-A / LP-B over ALL penalties (gamma_i, gamma_ij) that cover the triples in the
         sense of Theorem 11.18a(b) (2^n covering inequalities; not only shares)
For every model:  soundness  min_x (E - m) >= 0 (checked at every state);  margin (>= 0 iff x0
minimises m);  ln Z(m) - ln Z(E) and the cost number Z(m)/Z(E) - 1;  largest gap max_x (E - m).
Share certificates of Proposition 11.18b(c)/(d) for the site and the pair form:
  deficits w_ij = max_{a,b changed} [gamma_ij - T_ij(a,b) - D_ij(a,b)]_+ , loads <= Delta_i - gamma_i.

usage: python3 -B p4_02_third.py [--only SUBSTR] [--maxlp 10] [--nolz]
writes out/p4_02_third.json ; last line "DONE p4_02_third".
"""
import sys, os, re, glob, json, time, math, itertools
import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog, minimize
import p4lib as L4

t00 = time.time()
a = sys.argv[1:]
only = a[a.index("--only") + 1] if "--only" in a else None
MAXLP = int(a[a.index("--maxlp") + 1]) if "--maxlp" in a else 10
DOLZ = "--nolz" not in a
BETA = L4.BETA
TOL = 1e-9


def group_stats(code, nS, arrays_min=(), arrays_max=(), lz=()):
    """per changed-set statistics.  code: flat int array (bit i set iff site i changed)."""
    order = np.argsort(code, kind="stable")
    cs = code[order]
    starts = np.flatnonzero(np.r_[True, cs[1:] != cs[:-1]])
    present = cs[starts]
    out = []
    for arr in arrays_min:
        v = np.full(nS, np.inf); v[present] = np.minimum.reduceat(arr.ravel()[order], starts); out.append(v)
    for arr in arrays_max:
        v = np.full(nS, -np.inf); v[present] = np.maximum.reduceat(arr.ravel()[order], starts); out.append(v)
    for arr in lz:                                     # ln sum exp(-beta arr) per group
        e = arr.ravel()[order]
        m = e.min()
        v = np.full(nS, -np.inf); v[present] = np.log(np.add.reduceat(np.exp(-BETA * (e - m)), starts)) - BETA * m; out.append(v)
    return out


def model_stats(E, m, x0, lnZE):
    gap = E - m
    xg = np.unravel_index(int(np.argmax(gap)), gap.shape)          # a state of largest gap: how many of the multi-state sites are changed there
    nact = sum(1 for k in gap.shape if k >= 2)
    nch = sum(1 for i, k in enumerate(gap.shape) if k >= 2 and xg[i] != x0[i])
    return dict(sound=float(gap.min()), margin=L4.margin_at(m, x0), dlnZ=L4.lnZ(m) - lnZE, maxgap=float(gap.max()),
                cost=float(math.expm1(L4.lnZ(m) - lnZE)), maxgap_all_changed=bool(nch == nact), maxgap_nchanged=int(nch))


P2OUT = os.path.join(L4.P2, "out")
rows = []
for p in sorted(glob.glob(os.path.join(P2OUT, "an_fb_*_R3_t0.60_tau*.json"))):
    mm = re.match(r"an_(fb_([A-Z]+?)c?(\d+)_([A-Za-z0-9]+)_R3_t0\.60)_tau([0-9.]+)\.json", os.path.basename(p))
    if not mm:
        continue
    tag, res, nres, bb, taus = mm.group(1), mm.group(2), int(mm.group(3)), mm.group(4), mm.group(5)
    if only and only not in tag:
        continue
    J = json.load(open(p))
    if J.get("empty") or "iface|GB" not in J:
        continue
    if len(J["shape_pruned"]) < 3:
        continue
    t0 = time.time()
    inst = L4.load_instance(tag, float(taus))
    shape = inst["shape"]; n = len(shape)
    act = [i for i in range(n) if shape[i] >= 2]
    if len(act) < 3:
        continue
    f = inst["f"]; g = inst["R"]["GB"]; E = f + g
    x0 = L4.argmin_index(E)
    assert list(x0) == list(J["iface|GB"]["argmin_E"])
    # ---- constants
    c3 = L4.c3_dict(g)
    c3max = max(c3.values()); c3sum = sum(c3.values())
    P = J["Xp|GB"]
    dmax = abs(c3max - P["c3max"]) if "c3max" in P else None
    dsum = abs(c3sum - P["c3sum"]) if "c3sum" in P else None
    dall = max(abs(c3[tuple(int(t) for t in k.split(","))] - v) for k, v in P["c3"].items()) if P.get("c3") else None
    gam = np.zeros(n); gam2 = np.zeros((n, n))
    for (i, j, k), v in c3.items():
        for s in (i, j, k):
            gam[s] += v / 3.0
        for (u, w_) in ((i, j), (i, k), (j, k)):
            gam2[u, w_] += v / 3.0; gam2[w_, u] += v / 3.0
    # ---- models on the full grid
    I2 = L4.interp2(g, x0)
    base = f + I2
    lnZE = L4.lnZ(E)
    rem = g - I2
    models = {}
    m_env = base - L4.triple_penalty(shape, x0, c3)
    m_site = base - L4.site_penalty(shape, x0, gam)
    m_pair = base - L4.pair_penalty(shape, x0, gam2)
    models["env3"] = model_stats(E, m_env, x0, lnZE)
    models["site"] = model_stats(E, m_site, x0, lnZE)
    models["pair"] = model_stats(E, m_pair, x0, lnZE)
    # pointwise order claimed by Theorem 11.18a(c):  site <= pair <= env3 <= E
    order_ok = bool((m_site <= m_pair + 1e-10).all() and (m_pair <= m_env + 1e-10).all())
    A = L4.excitations(E, x0)
    Delta = L4.min_excitation(A, x0)
    # ---- share certificates of Prop. 11.18b(c)/(d) for the two forms
    ME = lambda i, j: L4.second_diff(E, x0, i, j)            # T_ij + D_ij = second difference of the full energy at x0
    cert = {}
    for form, gs, gp in (("site", gam, np.zeros((n, n))), ("pair", np.zeros(n), gam2)):
        w = L4.deficits(gp, ME, x0, shape)
        Dl = [d - gs[i] if d != math.inf else math.inf for i, d in enumerate(Delta)]
        fl = L4.share_flow(w, Dl)
        if fl["ok"]:
            assert L4.verify_shares(w, Dl, fl["s"])
            assert models[form]["margin"] >= -TOL, (tag, form, "shares exist but x0 does not minimise the model")
        else:
            assert L4.verify_overdense(w, Dl, fl["S"])
        # state-dependent shares (my refinement) on the same model
        tss = None; sl = None
        if models[form]["margin"] >= -TOL and not fl["ok"]:
            Ared = [A[i] - gs[i] for i in range(n)]
            tss, ss = L4.state_shares_lp(gp, ME, Ared, x0, shape)
            if ss is not None:
                v = L4.verify_state_shares(gp, ME, Ared, x0, shape, ss)
                sl = float(v) if v is not None else None
        cert[form] = dict(shares=fl["ok"], rowsum=L4.rowsum_ok(w, Dl), overdense=fl["S"], excess=(float(fl["excess"]) if fl["excess"] is not None else None),
                          wmax=float(w.max()), sshares_slack=sl)
    # ---- allocations by linear programming (per changed-set statistics)
    lp = {}
    if len(act) <= MAXLP:
        ch = L4.changed(shape, x0)
        code = np.zeros(shape, dtype=np.int64)
        for b_, i in enumerate(act):
            code = code + (ch[i].astype(np.int64) << b_)
        m_ = len(act); nS = 1 << m_
        Bm = base - base[x0]
        minB, minR, maxR, lzB = group_stats(code.ravel(), nS, arrays_min=(Bm, rem), arrays_max=(rem,), lz=(Bm,))
        bits = ((np.arange(nS)[:, None] >> np.arange(m_)[None, :]) & 1).astype(float)
        pos = {s: b_ for b_, s in enumerate(act)}
        trip = [(T, v) for T, v in c3.items() if all(s in pos for s in T) and v > 0]
        CS = np.zeros(nS)
        for (T, v) in trip:
            CS += v * bits[:, pos[T[0]]] * bits[:, pos[T[1]]] * bits[:, pos[T[2]]]
        # share matrix: rows S, columns (triple, pair p in T): entry c_T if T cap S = p exactly
        rws, cls, vls = [], [], []
        col = 0
        colinfo = []
        for (T, v) in trip:
            bT = [pos[s] for s in T]
            inT = bits[:, bT].sum(1)
            for (u, w_) in ((0, 1), (0, 2), (1, 2)):
                sel = np.flatnonzero((inT == 2) & (bits[:, bT[u]] == 1) & (bits[:, bT[w_]] == 1))
                rws.append(sel); cls.append(np.full(sel.size, col)); vls.append(np.full(sel.size, v))
                colinfo.append((T, (T[u], T[w_])))
                col += 1
        nv = col
        if nv:
            M = sp.csr_matrix((np.concatenate(vls), (np.concatenate(rws), np.concatenate(cls))), shape=(nS, nv))
            real = np.isfinite(minB); real[0] = False            # realisable non-empty changed sets
            Aeq = sp.csr_matrix((np.ones(nv), (np.repeat(np.arange(nv // 3), 3), np.arange(nv))), shape=(nv // 3, nv))
            beq = np.ones(nv // 3)

            def model_from_mu(mu):
                g2 = np.zeros((n, n))
                for cidx, (T, (u, w_)) in enumerate(colinfo):
                    g2[u, w_] += c3[T] * mu[cidx]; g2[w_, u] += c3[T] * mu[cidx]
                return base - L4.pair_penalty(shape, x0, g2), g2

            # LP-A: maximise the margin
            idx = np.flatnonzero(real)
            Aub = sp.hstack([M[idx], sp.csr_matrix(np.ones((idx.size, 1)))]).tocsr()
            r = linprog(np.r_[np.zeros(nv), -1.0], A_ub=Aub, b_ub=minB[idx] - CS[idx], A_eq=sp.hstack([Aeq, sp.csr_matrix((nv // 3, 1))]).tocsr(), b_eq=beq,
                        bounds=[(0, None)] * nv + [(None, None)], method="highs")
            if r.x is not None:
                mA, _ = model_from_mu(np.clip(r.x[:nv], 0, None))
                lp["LP-A"] = dict(model_stats(E, mA, x0, lnZE), lp_value=float(r.x[-1]))
            # LP-B: minimise the largest gap
            idxb = np.flatnonzero(np.isfinite(maxR))
            Aub = sp.hstack([M[idxb], -sp.csr_matrix(np.ones((idxb.size, 1)))]).tocsr()
            r = linprog(np.r_[np.zeros(nv), 1.0], A_ub=Aub, b_ub=-(maxR[idxb] + CS[idxb]), A_eq=sp.hstack([Aeq, sp.csr_matrix((nv // 3, 1))]).tocsr(), b_eq=beq,
                        bounds=[(0, None)] * nv + [(None, None)], method="highs")
            if r.x is not None:
                mB, _ = model_from_mu(np.clip(r.x[:nv], 0, None))
                lp["LP-B"] = dict(model_stats(E, mB, x0, lnZE), lp_value=float(r.x[-1]))
            # LZ: minimise ln Z(m) over pair shares (softmax parametrisation, L-BFGS; "best found")
            if DOLZ:
                idz = np.flatnonzero(np.isfinite(lzB))
                Mz = M[idz]; a0 = lzB[idz] + BETA * CS[idz]

                def obj(theta):
                    th = theta.reshape(-1, 3)
                    th = th - th.max(1, keepdims=True)
                    mu = np.exp(th); mu /= mu.sum(1, keepdims=True)
                    v = a0 + BETA * (Mz @ mu.ravel())
                    vm = v.max()
                    wgt = np.exp(v - vm); Zs = wgt.sum(); wgt /= Zs
                    gmu = (BETA * (Mz.T @ wgt)).reshape(-1, 3)
                    gth = mu * (gmu - (mu * gmu).sum(1, keepdims=True))
                    return vm + math.log(Zs), gth.ravel()

                r = minimize(obj, np.zeros(nv), jac=True, method="L-BFGS-B", options=dict(maxiter=500))
                th = r.x.reshape(-1, 3); th = th - th.max(1, keepdims=True)
                mu = np.exp(th); mu /= mu.sum(1, keepdims=True)
                mZ, _ = model_from_mu(mu.ravel())
                lp["LZ"] = dict(model_stats(E, mZ, x0, lnZE), iters=int(r.nit))
            # CV-A / CV-B: all covering penalties (gamma_i >= 0, gamma_ij free), 2^m covering inequalities
            prs = [(u, w_) for u in range(m_) for w_ in range(u + 1, m_)]
            Q = np.hstack([bits] + [(bits[:, u] * bits[:, w_])[:, None] for (u, w_) in prs])        # Gamma(S) = Q @ (gamma_i, gamma_ij)
            nq = Q.shape[1]
            allS = np.arange(1, nS)

            def model_from_cover(z):
                gs = np.zeros(n); g2 = np.zeros((n, n))
                for b_, s in enumerate(act):
                    gs[s] = z[b_]
                for q_, (u, w_) in enumerate(prs):
                    g2[act[u], act[w_]] = g2[act[w_], act[u]] = z[m_ + q_]
                return base - L4.site_penalty(shape, x0, gs) - L4.pair_penalty(shape, x0, g2)

            cover_A = -Q[allS]; cover_b = -CS[allS]
            for nmv, sel, rhs, sign in (("CV-A", idx, minB[idx], +1.0), ("CV-B", idxb, -maxR[idxb], -1.0)):
                if nmv == "CV-A":
                    Aub = np.vstack([np.hstack([cover_A, np.zeros((allS.size, 1))]), np.hstack([Q[sel], np.ones((sel.size, 1))])])
                    bub = np.r_[cover_b, rhs]
                    cst = np.r_[np.zeros(nq), -1.0]
                else:
                    Aub = np.vstack([np.hstack([cover_A, np.zeros((allS.size, 1))]), np.hstack([Q[sel], -np.ones((sel.size, 1))])])
                    bub = np.r_[cover_b, rhs]
                    cst = np.r_[np.zeros(nq), 1.0]
                r = linprog(cst, A_ub=Aub, b_ub=bub, bounds=[(0, None)] * m_ + [(None, None)] * (nq - m_) + [(None, None)], method="highs")
                if r.x is not None:
                    z = r.x[:nq].copy()
                    # exact-ish repair of the covering inequalities against rounding: add the largest violation to every site penalty is not needed if the violation is below 1e-9
                    viol = float((CS[allS] - Q[allS] @ z).max())
                    mC = model_from_cover(z)
                    lp[nmv] = dict(model_stats(E, mC, x0, lnZE), lp_value=float(r.x[-1]), cover_violation=viol)
    row = dict(tag=tag, res=res, nres=nres, bb=bb, tau=taus, shape=list(shape), size=int(np.prod(shape)), n=n, nact=len(act), x0=list(x0),
               c3max=c3max, c3sum=c3sum, d_c3max_P2=dmax, d_c3sum_P2=dsum, d_c3_P2=dall, ntriples=len(c3),
               rem_max=float(np.abs(rem).max()), gam_max=float(gam.max()), gam2_max=float(gam2.max()),
               Delta=[d if d != math.inf else None for d in Delta], order_ok=order_ok,
               P2_ball_eps=(J["iface|GB"].get("ball2") or {}).get("eps"), models=models, cert=cert, lp=lp)
    rows.append(row)
    ms = models
    print(f"[{time.time() - t00:6.0f}s] {res}{nres}/{bb} tau {taus} X' {list(shape)}: c3max {c3max:.4f} sum {c3sum:.4f} | margin env3/site/pair "
          f"{ms['env3']['margin']:.4f}/{ms['site']['margin']:.4f}/{ms['pair']['margin']:.4f} | dlnZ {ms['env3']['dlnZ']:.2e}/{ms['site']['dlnZ']:.2e}/{ms['pair']['dlnZ']:.2e} "
          f"| maxgap {ms['env3']['maxgap']:.3f}/{ms['site']['maxgap']:.3f}/{ms['pair']['maxgap']:.3f} | sound {min(ms[k]['sound'] for k in ms):.1e} "
          f"| shares site/pair {cert['site']['shares']}/{cert['pair']['shares']} ({time.time() - t0:.1f}s)", flush=True)

os.makedirs(os.path.join(L4.HERE, "out"), exist_ok=True)
outname = "p4_02_third.json" if not only else f"p4_02_third_{only}.json"
json.dump(rows, open(os.path.join(L4.HERE, "out", outname), "w"), indent=0)
allm = [(r, k, v) for r in rows for k, v in list(r["models"].items()) + list(r["lp"].items())]
print(f"\n{len(rows)} instances; {len(allm)} (instance, model) pairs; smallest min_x (E - m) over all of them: {min(v['sound'] for (_, _, v) in allm):.3e} kcal/mol")
print(f"pointwise order site <= pair <= env3 holds in {sum(r['order_ok'] for r in rows)} of {len(rows)} instances")
dd = [r["d_c3_P2"] for r in rows if r["d_c3_P2"] is not None]
print(f"largest |c_T(mine) - c_T(P2 stored)| over {len(dd)} instances with stored triples: {max(dd):.2e}; "
      f"largest |c3max - P2| {max(r['d_c3max_P2'] for r in rows if r['d_c3max_P2'] is not None):.2e}, |c3sum - P2| {max(r['d_c3sum_P2'] for r in rows if r['d_c3sum_P2'] is not None):.2e}")
print(f"[{time.time() - t00:.0f}s] wrote out/{outname}")
print("DONE p4_02_third")
