"""w04: the worked example (W5) -- single-letter numbers.

Chains (wsites.py): 'path' (three states on a path with steps 0.8, 1.6; pi = (0.5, 0.3, 0.2)), 'tri' (triangle with
sides 1, 1.5, 2; pi = (0.2, 0.5, 0.3)), 'asym' (asymmetric three-state envelope), 'bin' (binary, p = 0.3, u = 1),
'mix' (half binary, half path), 'mix2' (0.4 binary, 0.6 triangle).

For every chain: thresholds E = sum lam_j E_j, a = sum lam_j a_j, h = R(0); the table of
  R^max(e)   adaptive without a hint = hinted at the hardest additive instance   (max_t [F*(t) - t e]),
  theta_na(e) non-adaptive                                                       (R^max o S^{-1}),
  t*(e), the hardest additive instance gamma*(e), the label weights M*(e),
  R_0(e)     the zero residual (hint at g = 0),
  R^dip(e)   single dips only (distance-function vertices), hardest additive instance,
  R^cut(e)   'worst binary reduction' by coarse-graining {a} | rest (a subclass: a proved lower bound),
  R^pair(e)  'worst binary reduction' by deleting a state (not a subclass: a heuristic, not a bound),
and for chains with two site types: sum_j lam_j R_j(e) (average at a common accuracy) and the best split
min_{sum lam_j e_j = e} sum_j lam_j R_j(e_j).
Every optimum is certified by the bracket [F, upper] of Site.renyi (and was re-evaluated with the primal solver
in w02).  usage: python3 w04_example.py
"""
import math
import sys
import time

import numpy as np
from scipy.optimize import minimize_scalar, brentq

from wlib import *
from wsites import *

np.set_printoptions(precision=4, suppress=True, linewidth=170)
t00 = time.time()
C = chains()
FR = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]


def cut_sites(s):
    out = []
    for a in range(s.q):
        rest = [b for b in range(s.q) if b != a]
        out.append(Site([s.pi[a], 1 - s.pi[a]], [[0, min(s.d[a, b] for b in rest)], [min(s.d[b, a] for b in rest), 0]],
                        f"cut{{{a}}}|rest"))
    return out


def pair_sites(s):
    out = []
    for a in range(s.q):
        for b in range(a + 1, s.q):
            w = s.pi[a] + s.pi[b]
            out.append(Site([s.pi[a] / w, s.pi[b] / w], [[0, s.d[a, b]], [s.d[b, a], 0]], f"pair{{{a},{b}}}"))
    return out


def R_of_table(ts, F, e):
    obj = F - ts * e
    return float(obj.max())


def variants(ch, nt=401):
    """tables of the game functions of the variants on a t-grid"""
    ts = np.linspace(0, 1, nt)
    tab = lambda fun: np.array([fun(t) if 0 < t < 1 else 0.0 for t in ts])
    out = {"ts": ts}
    out["zero"] = sum(l * tab(lambda t, s=s: s.F(np.zeros(s.q), t)) for l, s in zip(ch.lam, ch.sites))
    out["dip"] = sum(l * tab(lambda t, s=s: s.Fstar(t, cols=np.where(s.is_dist)[0])) for l, s in zip(ch.lam, ch.sites))
    cut = np.zeros(nt)
    pair = np.zeros(nt)
    for l, s in zip(ch.lam, ch.sites):
        if s.q == 2:
            f = tab(lambda t, s=s: s.Fstar(t))
            cut += l * f
            pair += l * f
        else:
            cut += l * np.max([tab(lambda t, r=r: r.Fstar(t)) for r in cut_sites(s)], axis=0)
            pair += l * np.max([tab(lambda t, r=r: r.Fstar(t)) for r in pair_sites(s)], axis=0)
    out["cut"], out["pair"] = cut, pair
    return out


for name in ("bin", "path", "tri", "asym", "mix", "mix2"):
    ch = C[name]
    E, a = ch.E(), ch.a()[0]
    h, th = ch.R(0.0, return_t=True)
    print(f"\n================ chain {ch.name}: fractions {ch.lam} ================")
    for j, s in enumerate(ch.sites):
        Ed = s.Estar(full=True)
        cap = s.capacity(full=True)
        print(f" site type {j}: {s.name}; pi = {s.pi}; envelope d =\n{s.d}")
        print(f"   vertices of the Lipschitz polytope (rows, normalised phi[0] = 0; * = distance function d(., b) - d(0, b)):")
        for k in range(s.nv):
            print(f"     {k}{'*' if s.is_dist[k] else ' '} {s.V[k]}   Gibbs law {np.round(s.gibbs(s.V[k]), 4)}")
        print(f"   E_j = {Ed['E']:.6f} (certificate {Ed['upper']:.6f}; reverse-KL centre {np.round(Ed['Q'], 4)}, weights {np.round(Ed['M'], 4)});"
              f" a_j = {cap['a']:.6f} (certificate {cap['upper']:.6f}; capacity-achieving weights {np.round(cap['M'], 4)})")
        if s.q == 3:
            for r in cut_sites(s) + pair_sites(s):
                c1 = Chain([r], [1.0])
                print(f"   binary reduction {r.name:12s}: pi = {np.round(r.pi, 4)}, d01 = {r.d[0,1]:.2f}, d10 = {r.d[1,0]:.2f}: E = {c1.E():.6f}, a = {c1.a()[0]:.6f}, h = {c1.R(0.0):.6f}")
    print(f" chain: E = {E:.6f}, a = theta_na(0+) = {a:.6f}, h = R^max(0) = {h:.6f} (t* = {th:.4f}), h/a = {h/a:.4f}, theta_na(h) = {ch.theta_na_direct(h)[0]:.6f}")
    var = variants(ch)
    ts = var["ts"]
    print(f" variants at e = 0:  zero residual {R_of_table(ts, var['zero'], 0):.6f};  dips only {R_of_table(ts, var['dip'], 0):.6f};"
          f"  worst cut {R_of_table(ts, var['cut'], 0):.6f};  worst pair {R_of_table(ts, var['pair'], 0):.6f};"
          f"  thresholds: zero {np.max(var['zero'][1:]/ts[1:]):.6f}, dips {np.max(var['dip'][1:]/ts[1:]):.6f}, cut {np.max(var['cut'][1:]/ts[1:]):.6f}, pair {np.max(var['pair'][1:]/ts[1:]):.6f}")
    print("   e/E      e        R^max      (cert.gap)  t*      theta_na(e)   R_0       R^dip      R^cut      R^pair   | hardest additive instance gamma* (per type) and label weights M*")
    for fr in FR:
        e = fr * E
        R, tt = ch.R(e, return_t=True)
        gap = ch.Fstar_upper(tt) - ch.Fstar(tt)
        thna = ch.theta_na_direct(e)[0] if e > 0 else a
        extra = "; ".join(f"g*={np.round(ch.gammas(tt)[j][1:], 4)} M*={np.round(ch.Ms(tt)[j], 3)}" for j in range(len(ch.sites)))
        print(f"   {fr:4.2f}  {e:8.5f}  {R:9.6f}   ({gap:7.1e})  {tt:6.4f}  {thna:9.6f}   {R_of_table(ts, var['zero'], e):9.6f}  {R_of_table(ts, var['dip'], e):9.6f}"
              f"  {R_of_table(ts, var['cut'], e):9.6f}  {R_of_table(ts, var['pair'], e):9.6f} | {extra}")
    # corners of R^max: non-concavity of F*
    tsf, Fs = ch.table(801)
    d2 = Fs[:-2] - 2 * Fs[1:-1] + Fs[2:]
    if d2.max() > 1e-10:
        tk = tsf[1:-1][np.argmax(d2)]
        # the accuracy at which the two branches tie: scan e for a jump of t*
        es = np.linspace(0.0, E, 2001)
        tstar = np.array([tsf[np.argmax(Fs - tsf * e_)] for e_ in es])
        jump = np.argmax(np.abs(np.diff(tstar)))
        e_lo, e_hi = es[jump], es[jump + 1]
        for it in range(40):
            em = 0.5 * (e_lo + e_hi)
            tm = ch.R(em, return_t=True)[1]
            if tm > tk:
                e_lo = em
            else:
                e_hi = em
        Rl, tl = ch.R(e_lo, return_t=True)
        Rh, t_h = ch.R(e_hi, return_t=True)
        print(f" F* is NOT concave: convex kink at t_c = {tk:.4f}; label switch (corner of R^max) at e_c = {e_hi:.6f} = {e_hi/E:.4f} E: R = {Rh:.6f};")
        print(f"     for e < e_c: t* = {tl:.4f}, M* = " + "; ".join(str(np.round(m, 3)) for m in ch.Ms(tl)) + f";  for e > e_c: t* = {t_h:.4f}, M* = " + "; ".join(str(np.round(m, 3)) for m in ch.Ms(t_h)))
        print(f"     slope of R^max jumps from {-tl:.4f} to {-t_h:.4f}; gamma* is continuous: {np.round(ch.gammas(tl)[-1], 4)} -> {np.round(ch.gammas(t_h)[-1], 4)} (last site type)")
    else:
        print(f" F* is concave on a grid of 801 points (largest second difference {d2.max():.1e})")
    # several site types: the exponents do not add
    if len(ch.sites) > 1:
        singles = [Chain([s], [1.0]) for s in ch.sites]
        print(" several site types: R^max(e) = max_t[sum_j lam_j F*_j(t) - t e]  against the average at a common accuracy and the best split of the accuracy")
        print("   e/E      R^max      sum_j lam_j R_j(e)   min over splits   (split e_j)                        common t*    t*_j at the common accuracy")
        for fr in (0.0, 0.1, 0.3, 0.5, 0.7, 0.9):
            e = fr * E
            R, tt = ch.R(e, return_t=True)
            avg = sum(l * c.R(e) for l, c in zip(ch.lam, singles))
            tj = [c.R(e, return_t=True)[1] for c in singles]
            # best split for two types: minimise lam_0 R_0(e_0) + lam_1 R_1((e - lam_0 e_0)/lam_1)
            l0, l1 = ch.lam
            lo0 = (e - l1 * singles[1].E()) / l0
            hi0 = min(singles[0].E(), (e + l1 * singles[1].a()[0]) / l0)
            f = lambda e0: l0 * singles[0].R(e0) + l1 * singles[1].R((e - l0 * e0) / l1)
            grid = np.linspace(-singles[0].a()[0], singles[0].E(), 241)
            vals = [f(x) for x in grid]
            k = int(np.argmin(vals))
            res = minimize_scalar(f, bounds=(grid[max(k - 1, 0)], grid[min(k + 1, 240)]), method="bounded", options={"xatol": 1e-10})
            e0 = res.x
            print(f"   {fr:4.2f}  {R:9.6f}   {avg:9.6f} (+{100*(avg/R-1):5.2f}%)   {res.fun:9.6f} (+{100*(res.fun/R-1):6.3f}%)  e_j = ({e0:+.5f}, {(e - l0*e0)/l1:+.5f}), E_j = ({singles[0].E():.5f}, {singles[1].E():.5f})"
                  f"   {tt:6.4f}    ({tj[0]:.4f}, {tj[1]:.4f})")
print(f"\ntime {time.time()-t00:.0f} s")
