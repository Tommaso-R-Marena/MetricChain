#!/usr/bin/env python3
"""Independent check of Lemma B (HIERARCHY_REPORT.md section 3, branch research/phase2-adaptive-hierarchy).

Written from the mathematical statement only; nothing of the other division's scripts is imported or run.

For blocks n_1..n_m, roles in {P,Q,T}, slope u and budget Theta, compute the pointwise largest
G = -F over all F on the type grid prod_j {0..n_j} such that
  * |F(d) - F(d')| <= u for neighbouring types (differ by 1 in one coordinate),
  * (H1) F "sees only P" on V_0 = {t(d) <= Theta}: F(d) = F(d') when d_P = d'_P and d_j = d'_j mod 2 for j not in P,
  * (H2) F "sees only P u Q" on V_P = {t_Q(d) + t_T(d) <= Theta}: same with P u Q, parities of T,
  * nu(d) = -F(d) - t(d) <= 0 on V_0,
with t_j(d) = ln P_j(floor(n_j/2)) - ln P_j(d), P_j = Binomial(n_j, 1/2) (exact integer binomials).
The largest G is the shortest-path value G(y) = min_{s in V_0} [t(s) + dist(s, y)] in the graph with
edges of length u between neighbouring types and length 0 between members of one class; it is computed
here as the fixed point of (L1 distance transform) o (class minima), and cross-checked by Dijkstra and by
linear programmes in q1_crosscheck.py.

Then V = max_y [ nu(y) - n_P h + min{t_T(y), Theta - (n - n_P) h} ] is compared with m(u + 5 ln(n+1)).
"""
import argparse
import math
import re
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def consts(u):
    lam1 = math.log(2.0 / (1.0 + math.exp(-u)))
    kappa = lam1 / u
    f = lambda r: math.log(2) + (r * math.log(r) if r > 0 else 0) + ((1 - r) * math.log(1 - r) if r < 1 else 0)
    h = f(kappa)
    pu = 1.0 / (1.0 + math.exp(u))
    a = f(pu)
    Nu = math.ceil(5.0 / (1.0 - 2.0 * kappa))
    return dict(lam1=lam1, kappa=kappa, h=h, a=a, pu=pu, Nu=Nu)


def tcost(nj):
    """t_j(d) = ln C(nj, floor(nj/2)) - ln C(nj, d), from exact integers."""
    lc = np.array([math.log(math.comb(nj, d)) for d in range(nj + 1)])
    return lc[nj // 2] - lc


def group_min(G, members, keys):
    """Replace G on `members` (flat indices) by the minimum of G over each key class.

    `keys` is sorted-order data prepared by prepare_classes."""
    order, starts = keys
    idx = members[order]
    vals = G[idx]
    mins = np.minimum.reduceat(vals, starts)
    counts = np.diff(np.append(starts, len(idx)))
    G[idx] = np.repeat(mins, counts)


def prepare_classes(shape, mask, exact_axes, parity_axes, use_parity=True):
    """Classes of `mask` (bool array): equal exact_axes coordinates and (if use_parity) equal parities on
    parity_axes.  Returns (members, (order, starts))."""
    members = np.flatnonzero(mask.ravel())
    coords = np.unravel_index(members, shape)
    key = np.zeros(len(members), dtype=np.int64)
    for ax in range(len(shape)):
        if ax in exact_axes:
            key = key * (shape[ax]) + coords[ax]
        elif ax in parity_axes and use_parity:
            key = key * 2 + (coords[ax] & 1)
    order = np.argsort(key, kind="stable")
    ks = key[order]
    starts = np.flatnonzero(np.r_[True, ks[1:] != ks[:-1]])
    return members, (order, starts)


def l1_transform(G, u):
    """In place: G <- min_{d'} G(d') + u |d - d'|_1 (exact, by forward/backward passes along each axis)."""
    for ax in range(G.ndim):
        Gs = np.moveaxis(G, ax, 0)
        for i in range(1, Gs.shape[0]):
            np.minimum(Gs[i], Gs[i - 1] + u, out=Gs[i])
        for i in range(Gs.shape[0] - 2, -1, -1):
            np.minimum(Gs[i], Gs[i + 1] + u, out=Gs[i])


def solve(ns, roles, u, Theta, use_h1=True, use_h2=True, use_parity=True, tol=1e-11, maxit=500):
    m = len(ns)
    shape = tuple(n + 1 for n in ns)
    tj = [tcost(n) for n in ns]
    grids = np.meshgrid(*[np.arange(s) for s in shape], indexing="ij", sparse=True)

    def tsum(sel):
        out = np.zeros(shape)
        for j in sel:
            out = out + tj[j][grids[j]]
        return out

    P = [j for j in range(m) if roles[j] == "P"]
    Q = [j for j in range(m) if roles[j] == "Q"]
    T = [j for j in range(m) if roles[j] == "T"]
    t = tsum(range(m))
    tT = tsum(T)
    tQT = tsum(Q + T)
    V0 = t <= Theta
    VP = tQT <= Theta
    classes = []
    if use_h1:
        classes.append(prepare_classes(shape, V0, set(P), set(Q + T), use_parity))
    if use_h2:
        classes.append(prepare_classes(shape, VP, set(P + Q), set(T), use_parity))
    G = np.full(shape, np.inf)
    G[V0] = t[V0]
    Gf = G.reshape(-1)
    it = 0
    while True:
        it += 1
        old = G.copy()
        l1_transform(G, u)
        for members, keys in classes:
            group_min(Gf, members, keys)
        diff = np.max(np.abs(G - old)[np.isfinite(old)]) if np.isfinite(old).any() else np.inf
        if np.all(np.isfinite(G)) and diff <= tol:
            break
        if it >= maxit:
            raise RuntimeError("no convergence")
    return dict(G=G, t=t, tT=tT, V0=V0, VP=VP, P=P, Q=Q, T=T, classes=classes, iters=it, shape=shape)


def verify(sol, u, tol=1e-9):
    """Independent check of the constraints on the computed G (admissibility, classes, nu<=0 on V0)."""
    G = sol["G"]
    lip = max(np.max(np.abs(np.diff(G, axis=ax))) for ax in range(G.ndim))
    ok_lip = lip <= u + tol
    ok_cls = True
    Gf = G.reshape(-1)
    for members, (order, starts) in sol["classes"]:
        v = Gf[members[order]]
        mx = np.maximum.reduceat(v, starts)
        mn = np.minimum.reduceat(v, starts)
        ok_cls &= bool(np.max(mx - mn) <= tol)
    nu = G - sol["t"]
    ok_nu = bool(np.max(nu[sol["V0"]]) <= tol)
    return bool(ok_lip), ok_cls, ok_nu


def evaluate(ns, roles, u, theta_over_h, **kw):
    c = consts(u)
    n = sum(ns)
    m = len(ns)
    Theta = theta_over_h * n * c["h"]
    t0 = time.time()
    sol = solve(ns, roles, u, Theta, **kw)
    G, t, tT = sol["G"], sol["t"], sol["tT"]
    nu = G - t
    nu0 = float(np.max(nu[sol["V0"]]))
    nP = sum(ns[j] for j in sol["P"])
    bracket = nu - nP * c["h"] + np.minimum(tT, Theta - (n - nP) * c["h"])
    Vval = float(np.max(bracket))
    hid = tT > Theta
    Vhid = float(np.max(bracket[hid])) if hid.any() else -np.inf
    # the lemma's own left side, with nu0 subtracted (nu0 = 0 expected)
    Vlemma = Vval - nu0
    allowance = m * (u + 5 * math.log(n + 1))
    ok = verify(sol, u)
    yarg = np.unravel_index(int(np.argmax(bracket)), sol["shape"])
    return dict(ns=ns, roles=roles, u=u, th=theta_over_h, n=n, m=m, Theta=Theta, V=Vval, Vlemma=Vlemma,
                Vhid=Vhid, nu0=nu0, allowance=allowance, iters=sol["iters"], ok=ok,
                hyp_Theta=Theta >= n * c["h"] + 2 * m * math.log(n + 1),
                hyp_Nu=min(ns) >= c["Nu"], argmax=tuple(int(x) for x in yarg),
                secs=time.time() - t0)


LINE = re.compile(r"u=([\d.]+) ns=\(([\d, ]+)\) roles=(\w+) theta/h=([\d.]+) .*viol=\s*([-+\d.inf]+) .*hidden max=\s*([-+\d.inf]+) vs n h - Theta=\s*([-+\d.]+)")


def their_cases(path):
    rows = []
    for line in Path(path).read_text().splitlines():
        mm = LINE.search(line)
        if mm:
            rows.append(dict(u=float(mm.group(1)), ns=tuple(int(x) for x in mm.group(2).split(",")),
                             roles=mm.group(3), th=float(mm.group(4)), viol=float(mm.group(5)),
                             hidden=float(mm.group(6)), nhT=float(mm.group(7))))
    return rows


def fmt(r, their=None):
    s = (f"u={r['u']:<4} ns={str(r['ns']):<22} roles={r['roles']:<5} th/h={r['th']:.2f} | V={r['V']:+9.4f} "
         f"allow={r['allowance']:7.2f} Vhid={r['Vhid']:+10.4f} nu0={r['nu0']:+.1e} it={r['iters']:3d} "
         f"checks(lip,cls,nu)={''.join('Y' if x else 'N' for x in r['ok'])} hypTheta={'Y' if r['hyp_Theta'] else 'N'} "
         f"hypNu={'Y' if r['hyp_Nu'] else 'N'}")
    if their is not None:
        s += f" | theirs viol={their['viol']:+9.3f} diff={r['V'] - their['viol']:+.4f}"
        # their 'hidden max' is max nu over t_T > Theta; mine Vhid = that + Theta - n h
        if math.isfinite(their["hidden"]):
            mine_h = r["Vhid"] - (r["Theta"] - r["n"] * consts(r["u"])["h"])
            s += f" hidden(theirs)={their['hidden']:+9.3f} hidden(mine)={mine_h:+9.3f}"
        else:
            s += f" hidden(theirs)=-inf hidden(mine)={r['Vhid']:+.3f}"
    return s + f" [{r['secs']:.1f}s]"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--their-output", help="their stored h1_relaxation_lemma_check.txt (read as data: parameters, numbers)")
    ap.add_argument("--extra", action="store_true", help="run my own extra grid (Theta in {1.0,1.1,1.3} nh, n<=400)")
    ap.add_argument("--out", default=str(HERE / "out" / "q1_main.txt"))
    ap.add_argument("--no-parity", action="store_true",
                    help="alternative reading: 'sees only S' without the parity allowance (stronger hypotheses)")
    args = ap.parse_args()
    kw = dict(use_parity=not args.no_parity)
    lines = [f"# reading of 'sees only S': {'WITHOUT parities' if args.no_parity else 'with parities (report section 3)'}"]
    allres = []
    if args.their_output:
        cases = their_cases(args.their_output)
        lines.append(f"# their cases: {len(cases)} parsed")
        for cs in cases:
            r = evaluate(cs["ns"], cs["roles"], cs["u"], cs["th"], **kw)
            r["their"] = cs
            allres.append(r)
            lines.append(fmt(r, cs))
            print(lines[-1], flush=True)
    if args.extra:
        extra = []
        for u in (0.5, 1.0, 2.0, 4.0):
            for ns, roles in [((100, 150, 150), "TQP"), ((200, 100, 100), "QPT"), ((60, 60, 280), "PQT"),
                              ((130, 130, 130), "TTQ"), ((40, 40, 40, 40), "QTPT"), ((30, 40, 50, 60), "TQPT"),
                              ((30, 30, 50, 70), "QQTT"), ((40, 40, 40, 40), "PTTT")]:
                for th in (1.0, 1.1, 1.3):
                    extra.append((ns, roles, u, th))
        lines.append(f"# my extra cases: {len(extra)}")
        for ns, roles, u, th in extra:
            r = evaluate(ns, roles, u, th, **kw)
            allres.append(r)
            lines.append(fmt(r))
            print(lines[-1], flush=True)
    # summary
    V = max(r["V"] for r in allres)
    worst = max(allres, key=lambda r: r["V"])
    exceed = [r for r in allres if r["V"] > r["allowance"]]
    hid = [r for r in allres if r["th"] >= 1.1 - 1e-9 and math.isfinite(r["Vhid"])]
    Vh = max((r["Vhid"] for r in hid), default=-np.inf)
    allok = all(all(r["ok"]) for r in allres)
    lines.append(f"# SUMMARY cases={len(allres)} max V={V:+.4f} at {worst['u']} {worst['ns']} {worst['roles']} th/h={worst['th']} y*={worst['argmax']}")
    lines.append(f"# cases with V > allowance m(u+5L): {len(exceed)}")
    lines.append(f"# cases with V > 5: {sum(r['V'] > 5 for r in allres)}")
    lines.append(f"# max over Theta>=1.1nh of bracket over hidden types (t_T>Theta): {Vh:+.5f} (cases with hidden types: {len(hid)}); > 0.01: {sum(r['Vhid'] > 0.01 for r in hid)}")
    lines.append(f"# max |nu0|: {max(abs(r['nu0']) for r in allres):.2e}; all constraint checks pass: {allok}")
    lines.append(f"# cases violating the lemma's own hypotheses: Theta<nh+2mL: {sum(not r['hyp_Theta'] for r in allres)}, min n_j<N_u: {sum(not r['hyp_Nu'] for r in allres)}")
    if any("their" in r for r in allres):
        d = [abs(r["V"] - r["their"]["viol"]) for r in allres if "their" in r]
        lines.append(f"# max |mine - theirs| (viol column): {max(d):.4f}")
    for l in lines[-8:]:
        print(l)
    Path(args.out).write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
