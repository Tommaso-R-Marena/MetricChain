"""
P5 -- (a) numerical check of Proposition 10 of the report (remainder identity for an arbitrary
down-closed family D of evaluated subsets), and of the bound it gives with exact anchored
constants, at EVERY state of enumerated instances; (b) the test that killed "banded exactness":
exact anchored constants and P3's certified bound of the subsets that are NOT inside a window,
by sequence diameter.

Proposition 10.  D down-closed family of subsets of the sites (contains the empty set).  For every g,
anchor x0 and state x, with S = S(x) = {i : x_i != x0_i}:
    g(x) - sum_{U in D, U subset S} d_U(x_U)  =  sum_{T in Thr(D), T subset S} Delta_T g(z^{T,x}; x_T),
    Thr(D) = { T not in D : T minus {min T} in D },   z^{T,x}_i = x_i (i < min T), x0_i (otherwise).

usage: python3 -B s3_locality.py        (log: logs/s3_locality.log; about 3 min)
"""
import sys, os, json, itertools, time
import numpy as np
from p5lib import *

log = Tee(os.path.join(HERE, "logs", "s3_locality.log"))
rng = np.random.default_rng(7)


def d_term(g, x0, x, U):
    """anchored term d_U(x_U) by inclusion-exclusion."""
    tot = 0.0
    for r in range(len(U) + 1):
        for V in itertools.combinations(U, r):
            y = list(x0)
            for i in V:
                y[i] = x[i]
            tot += (-1) ** (len(U) - r) * g[tuple(y)]
    return tot


def delta_T(g, x0, x, T):
    """Delta_T g(z^{T,x}; x_T): context = x before min T, anchor elsewhere."""
    lo = min(T)
    base = [x[i] if i < lo else x0[i] for i in range(len(x0))]
    tot = 0.0
    for r in range(len(T) + 1):
        for V in itertools.combinations(T, r):
            y = list(base)
            for i in V:
                y[i] = x[i]
            tot += (-1) ** (len(T) - r) * g[tuple(y)]
    return tot


def families(n):
    fams = {}
    for w in range(1, n):
        fams[f"window w={w} (all subsets of diameter <= w, and all pairs)"] = lambda U, w=w: len(U) <= 2 or (max(U) - min(U) <= w)
    for m in (2, 3, 4):
        fams[f"ball m-1={m} (P3's family: |U| <= {m})"] = lambda U, m=m: len(U) <= m
    fams["window 2 and order <= 3, plus pairs"] = lambda U: len(U) <= 2 or (len(U) <= 3 and max(U) - min(U) <= 2)
    return fams


def check_identity(g, x0, name, consts=None):
    """identity at every state for several families; with consts (dict T -> exact c_T^anch): also the bound."""
    n = g.ndim
    shape = g.shape
    nst = nviol = nb = nbviol = 0
    worst = 0.0
    rmin, rmax = np.inf, 0.0
    for fname, inD in families(n).items():
        for x in itertools.product(*[range(k) for k in shape]):
            S = [i for i in range(n) if x[i] != x0[i]]
            lhs = g[x]
            rhs = 0.0
            bound = 0.0
            for r in range(len(S) + 1):
                for U in itertools.combinations(S, r):
                    if inD(U):
                        lhs -= d_term(g, x0, x, U)
                    elif inD(U[1:]):                       # U not in D, U minus its smallest element in D
                        rhs += delta_T(g, x0, x, U)
                        if consts is not None:
                            bound += consts[U]
            nst += 1
            err = abs(lhs - rhs)
            worst = max(worst, err)
            if err > 1e-9 * (1 + abs(g).max()):
                nviol += 1
            if consts is not None:
                nb += 1
                if abs(lhs) > bound + 1e-9:
                    nbviol += 1
                if abs(lhs) > 1e-12:
                    rmin = min(rmin, bound / abs(lhs)); rmax = max(rmax, bound / abs(lhs))
    log(f"    {name}: identity checked at {nst} (state, family) pairs, largest deviation {worst:.2e}, violations {nviol}"
        + (f"; bound |remainder| <= sum of exact c_T^anch over threshold sets: {nb} checks, {nbviol} violations, ratio bound/|remainder| in [{rmin:.3g}, {rmax:.3g}]" if consts is not None else ""))
    return nst, nviol, nb, nbviol


log("=== (a) Proposition 10: remainder identity for down-closed families")
tot = [0, 0, 0, 0]
gr = rng.normal(size=(3, 2, 4, 2, 3))
res = check_identity(gr, (1, 0, 2, 1, 0), "random function on a 3x2x4x2x3 grid")
tot = [a + b for a, b in zip(tot, res)]
for seq, bb, tau in (("L6", "H", 0.60), ("S4", "H", 0.70)):
    G, st, shape, f, g, E, x0 = build(seq, bb, tau)
    n = G.ns
    c = anch_consts(g, x0, n, n, minorder=1)
    consts = {T: float(v) for T, v in c.items()}
    for T in [T for m in range(1, n + 1) for T in itertools.combinations(range(n), m)]:
        consts.setdefault(T, 0.0)
    res = check_identity(g, x0, f"GBn2 of {seq}/{bb} tau {tau} ({g.size} states)", consts)
    tot = [a + b for a, b in zip(tot, res)]
log(f"    totals: identity {tot[0]} checks, {tot[1]} violations; bound {tot[2]} checks, {tot[3]} violations")

log("=== (b) are the subsets outside a window small?  Leu on the helix, tau 0.60; kcal/mol")
t0 = time.time()
out = {}
for seq, maxo, dop3 in (("L8", 4, True), ("L12", 4, True), ("L16", 3, True)):
    G, st, shape, f, g, E, x0 = build(seq, "H", 0.60)
    n = G.ns
    c = anch_consts(g, x0, n, maxo)
    sup = EnvelopeSup(G)
    GF = GFBound(G, x0, sup, K=maxo)
    log(f"  {seq}/H: {G.nat} atoms, {g.size} states enumerated, anchor {x0}; {time.time() - t0:.0f} s")
    for m in range(3, maxo + 1):
        rows = {}
        for T in itertools.combinations(range(n), m):
            d = T[-1] - T[0]
            b = sum(GF.total(m, T)) if dop3 else np.nan
            if float(c[T]) > b + 1e-9:
                log(f"    VIOLATION of P3's bound at T = {T}")
            rows.setdefault(d, []).append((float(c[T]), b))
        tail_e = 0.0; tail_b = 0.0
        tab = []
        for d in sorted(rows, reverse=True):
            a = np.array(rows[d])
            tail_e += a[:, 0].sum(); tail_b += a[:, 1].sum()
            tab.append((d, len(a), a[:, 0].sum(), a[:, 0].max(), a[:, 1].sum(), a[:, 1].min(), a[:, 1].max(), tail_e, tail_b))
        out[f"{seq}_{m}"] = tab
        log(f"    order {m}: diameter | subsets | exact: sum, max | P3 bound: sum, min, max | all subsets of diameter >= d: exact sum, P3 sum")
        for r in sorted(tab):
            log(f"      {r[0]:3d} | {r[1]:4d} | {r[2]:.3e}, {r[3]:.2e} | {r[4]:.3e}, {r[5]:.2e}, {r[6]:.2e} | {r[7]:.3e}, {r[8]:.3e}")
    log(f"  {seq}/H done, {time.time() - t0:.0f} s")
with open(os.path.join(HERE, "out", "s3_locality.json"), "w") as fh:
    json.dump(out, fh, indent=1)
log.done()
