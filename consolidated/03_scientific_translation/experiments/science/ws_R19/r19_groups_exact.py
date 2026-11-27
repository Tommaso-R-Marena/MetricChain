#!/usr/bin/env python3
"""R19, item 2 at production size: the five statistics of every group, recomputed EXACTLY with my own code -- no window, no
held-site pass, no code of the division: plain variable elimination on the tables of the ceiling model, keeping the sites
that the items of the group touch.  (The law of S_g under the model needs only the joint marginal of those sites.)

Input: case_*.pkl written by r19_dump_case.py (the tables of the driver's two models, the items, their routes, the group
statistics the driver computed with held_site_laws.py, the two ln Z).
Checks: ln Z(m_+), ln Z(m_-) by my elimination against the driver's transfer matrix; for every group (or the groups named)
the statistics a, e, b, c, cp and the total mass against the driver's numbers; the four bounds from my statistics.
Control that must fail: the same comparison with one item of the group left out.
For wide bands the held site is restricted to one state at a time (memory), which is the only concession to size.

Run: python3 -B r19_groups_exact.py case_K12_m4_w4.pkl [all | N | key,key,...] > r19_groups_exact_K12_m4_w4.log
"""
import os, sys, math, time, pickle, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "NUMEXPR_MAX_THREADS"):
    os.environ[v] = "1"
import numpy as np
t00 = time.time()
C = pickle.load(open(sys.argv[1], "rb")); which = sys.argv[2] if len(sys.argv) > 2 else "all"; FORCE = len(sys.argv) > 3 and sys.argv[3] == "restrict"
n, k, w, beta = C["n"], C["k"], C["w"], C["beta"]


def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


def factors_of(T):
    """the model as a list of (sites, -beta * table); the constant separately."""
    F = [((i,), -beta * T["one"][i]) for i in range(n)]
    F += [(tuple(U), -beta * tab) for U, tab in T["pair"].items()] + [(tuple(U), -beta * tab) for U, tab in T["multi"].items()]
    return F, -beta * T["const"]


def eliminate(F, order, kk):
    """log-domain variable elimination: sum out the sites of `order`, one by one; returns the remaining factors."""
    F = list(F)
    for t in order:
        inv = [f for f in F if t in f[0]]; F = [f for f in F if t not in f[0]]
        scope = sorted({u for f in inv for u in f[0]}); A = np.zeros([kk[u] for u in scope])
        for U, tab in inv:
            A = A + np.asarray(tab).reshape([kk[u] if u in U else 1 for u in scope])
        ax = scope.index(t); mx = A.max(axis=ax); A = A - np.expand_dims(mx, ax); np.exp(A, out=A)
        F.append((tuple(u for u in scope if u != t), mx + np.log(A.sum(axis=ax))))
    return F


def combine(F, scope, kk):
    A = np.zeros([kk[u] for u in scope])
    for U, tab in F:
        A = A + np.asarray(tab).reshape([kk[u] if u in U else 1 for u in scope])
    return A


def order_for(keep, held=None):
    """sites to sum out: left of the kept block ascending, right of it descending, then the sites inside it -- from the held site
    towards the window (ascending if the held site is the leftmost kept site, descending if it is the rightmost), so that no array
    spans more than the held site and w + 1 consecutive sites.  (Version 1 summed the inside sites ascending in both cases and
    built arrays over nine sites for a held site on the right: 4.9 GB at band 4 -- my error, see NOTES.md.)"""
    lo_, hi_ = min(keep), max(keep)
    inside = [t for t in range(lo_, hi_ + 1) if t not in keep]
    if held is not None and held == hi_: inside = inside[::-1]
    return [t for t in range(lo_) if t not in keep] + [t for t in range(n - 1, hi_, -1) if t not in keep] + inside


def restrict(F, site, b):
    out = []
    for U, tab in F:
        if site in U:
            ax = U.index(site); out.append((tuple(u for u in U if u != site), np.take(np.asarray(tab), b, axis=ax)))
        else: out.append((U, tab))
    return out


Fup, cup = factors_of(C["up"]); Flo, clo = factors_of(C["lo"])
t1 = time.time()
lz_up = float(combine(eliminate(Fup, list(range(n)), k), [], k)) + cup; lz_lo = float(combine(eliminate(Flo, list(range(n)), k), [], k)) + clo
print(f"case {C['args']}: n = {n}, k = {k}, band {w}; {len(C['items'])} items, {len(C['GS'][C['last']])} groups; ln Z(m+): mine {lz_up:.10f}, the driver's {C['lnZup']:.10f} (difference {lz_up - C['lnZup']:+.2e}); "
      f"ln Z(m-): mine {lz_lo:.10f}, the driver's {C['lnZlo']:.10f} ({lz_lo - C['lnZlo']:+.2e}) [{time.time() - t1:.0f}s, peak RSS {rss():.0f} MB]", flush=True)
GS = C["GS"][C["last"]]; items, kind, rts = C["items"], C["kind"], C["rts"]
members = {}
for j, r in enumerate(rts):
    if r is not None: members.setdefault(r, []).append(j)
assert set(members) == set(GS)
keys = sorted(GS)
if which != "all":
    if which.isdigit(): keys = keys[::max(1, len(keys) // int(which))][:int(which)]
    else:
        want = {tuple((p.split("@")[0][:3], int(p.split("@")[0][3:]), int(p.split("@")[1]))) for p in which.split(",")}; keys = [g for g in keys if g in want]
mine = {}; worst = 0.0; worst_mass = 0.0; ctrl = 0; nctrl = 0; nst = 0
for gk in keys:
    t1 = time.time(); d, held, s = gk; js = members[gk]
    used = sorted({u for j in js for u in items[j][0]}); assert held in used
    other = [u for u in used if u != held]; big = FORCE or np.prod([float(k[u]) for u in range(min(used), min(used) + w + 2) if u < n]) > 3e7
    st = dict(a=0.0, e=0.0, b=0.0, c=0.0, cp=0.0, mass=0.0); st_c = dict(a=0.0)
    blocks = [(None, Fup)] if not big else [(b, restrict(Fup, held, b)) for b in range(k[held])]
    for b, F in blocks:
        keep = used if b is None else other
        ordr = [t for t in order_for(keep, held if b is None else None) if b is None or t != held]
        lg = combine(eliminate(F, ordr, k), keep, k) + cup - C["lnZup"]; P = np.exp(lg)                 # the law of the kept sites (times [x_held = b])
        Sp = np.zeros(P.shape); Sm = np.zeros(P.shape); Sp_c = np.zeros(P.shape)
        for q, j in enumerate(js):
            U, tab = items[j]
            if b is not None: tab = np.take(tab, b, axis=U.index(held)); U = tuple(u for u in U if u != held)
            v = np.asarray(tab).reshape([k[u] if u in U else 1 for u in keep])
            if kind[j][1] in (+1, 0):
                Sp = Sp + v
                if q > 0: Sp_c = Sp_c + v
            if kind[j][1] in (-1, 0): Sm = Sm + v
        Ep = np.exp(beta * Sp)
        st["mass"] += float(P.sum()); st["a"] += float((P * Sp).sum()); st["e"] += float((P * np.expm1(beta * Sp)).sum()); st["b"] += float((P * Sm).sum())
        st["c"] += float((P * Sm * Ep).sum()); st["cp"] += float((P * np.expm1(beta * Sm) * Ep).sum()); st_c["a"] += float((P * Sp_c).sum())
    mine[gk] = st; dv = 0.0
    for q in ("a", "e", "b", "c", "cp"):
        ex = GS[gk][q]; nst += 1
        dv = max(dv, abs(st[q] - ex) / abs(ex) if abs(ex) > 1e-300 else abs(st[q] - ex))
    worst = max(worst, dv); worst_mass = max(worst_mass, abs(st["mass"] - 1.0))
    if kind[js[0]][1] in (+1, 0) and abs(st["a"] - st_c["a"]) > 1e-7 * abs(st["a"]):
        nctrl += 1; ctrl += int(abs(st_c["a"] - GS[gk]["a"]) > 1e-8 * abs(GS[gk]["a"]))
    print(f"  group {d}{held}@{s}: {len(js)} items on the sites {used}{' (held site restricted state by state)' if big else ''}: a = {st['a']:.6e}, e = {st['e']:.6e}, b = {st['b']:.6e}, c = {st['c']:.6e}, cp = {st['cp']:.6e}; "
          f"largest relative deviation from the driver's five numbers {dv:.1e}; mass - 1 = {st['mass'] - 1.0:+.1e} [{time.time() - t1:.1f}s]", flush=True)
print(f"{len(keys)} of {len(GS)} groups recomputed, {nst} statistics: largest relative deviation from the held-site passes {worst:.2e}; largest |mass - 1| {worst_mass:.1e}; "
      f"control (the first item of the group left out of <S+_g>): detected in {ctrl} of {nctrl} groups; peak RSS {rss():.0f} MB")
if len(keys) == len(GS):
    a_, e_, c_, cp_ = (sum(v[q] for v in mine.values()) for q in ("a", "e", "c", "cp")); L, U = lz_lo, lz_up
    LJ = U + beta * a_; LP = U + math.log1p(e_); u = v = L
    for _ in range(200):
        u = L - beta * c_ * math.exp(U - u); v = L - math.log1p(cp_ * math.exp(U - v))
    lo_d, up_d = C["res"][C["last"]]
    print(f"the four bounds from my ln Z and my statistics (no safety factor): LJ {LJ:.9f}, LP {LP:.9f}, UE {u:.9f}, UP {v:.9f}: bracket [{max(LJ, LP):.9f}, {min(u, v):.9f}], width {min(u, v) - max(LJ, LP):.4g}; "
          f"the driver's [{lo_d:.9f}, {up_d:.9f}], width {up_d - lo_d:.4g}; differences {max(LJ, LP) - lo_d:+.2e}, {min(u, v) - up_d:+.2e}")
print(f"ALL DONE {time.time() - t00:.0f} s; peak RSS {rss():.0f} MB")
