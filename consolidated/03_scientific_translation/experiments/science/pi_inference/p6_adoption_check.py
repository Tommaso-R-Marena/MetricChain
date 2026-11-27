#!/usr/bin/env python3
"""Coordinator's checks before adopting workstream P6 (pair and triple shares in the certified sandwich), 2026-11-26.

1. THE COUNTING LEMMAS (P6's Lemma A, Lemma A', Lemma B) ON RANDOM DATA, own code: for random non-negative constants on
   the m-subsets of n sites and every 0/1 vector s (exhaustively), with a band / window w:
       envelope <= triple form (window) <= pair form <= banded pair form <= site form,
   the inclusion-exclusion formula for the pair sums, the double-counting identities.
2. THE TRIPLE FORM ON A REAL ENUMERATED INSTANCE, WITHOUT P6'S MODEL CODE: Ace-Val8-NMe on PPII (6 561 states), order 4.
   Inputs taken as given: the enumerated energies (workstream P6's cache of P2/P3 evaluations) and workstream P3's
   certified constants chat_T for the 70 subsets (gfbound.GFBound.total(m, T)).  Mine: the anchored interpolation
   I_{m-1} g by inclusion-exclusion over the three-state grid, the three penalties (all pairs / triples in the window, so
   that no band reduction of P3 is involved), the models m_-/+ = f + I g -/+ penalty by brute force over all states,
   ln Z by enumeration.  Compared with the widths in P6's report (0.425, 0.0717, 0.0123 nats).  Those are for PAIRWISE
   models, in which the evaluated three-site terms d_U are replaced by P3's min/max reductions to pair tables (and which
   carry P3's floating-point allowance); mine keep the evaluated terms exact (possible only by enumeration), so mine must
   be narrower by the slack of those reductions -- the same amount for every penalty form, if both are right.
(The headline bracket of the triple form at twenty residues is re-run separately, from a scratch copy of workstream P6's
directory, so that nothing of the workstream's record is overwritten: see the validation record.)
Run:  python3 -B p6_adoption_check.py > p6_adoption_check.log     (one core, a few minutes)
"""
import os, sys, math, json, time, itertools
import numpy as np
from scipy.special import logsumexp, comb
HERE = os.path.dirname(os.path.abspath(__file__))
P6 = os.path.normpath(os.path.join(HERE, "..", "ws_P6"))
sys.path.insert(0, P6)
t0 = time.time()
def log(s): print(s, flush=True)

log("=== 1. the counting lemmas on random non-negative constants (exhaustive over s in {0,1}^n)")
rng = np.random.default_rng(20261126); ncheck = 0; worst = 0.0
for n, m, w in ((6, 3, 2), (7, 3, 3), (7, 4, 2), (8, 4, 3), (8, 5, 3), (9, 4, 4), (9, 5, 2), (10, 4, 3)):
    for rep in range(6):
        subs = list(itertools.combinations(range(n), m))
        c = rng.random(len(subs)) ** 4 * (rng.random(len(subs)) < 0.7)          # non-negative, many small, some zero
        S1 = np.zeros(n); G = np.zeros((n, n)); H = {}
        for T, v in zip(subs, c):
            for i in T: S1[i] += v
            for i, j in itertools.combinations(T, 2): G[i, j] += v; G[j, i] += v
            for tr in itertools.combinations(T, 3): H[tr] = H.get(tr, 0.0) + v
        Gam = c.sum()
        # Lemma B: inclusion-exclusion and double counting
        def gam_ex(A): return sum(v for T, v in zip(subs, c) if not (set(T) & set(A)))
        for i, j in itertools.combinations(range(n), 2):
            assert abs(G[i, j] - (Gam - gam_ex([i]) - gam_ex([j]) + gam_ex([i, j]))) < 1e-10
        assert np.allclose(G.sum(1), (m - 1) * S1) and all(abs(sum(H.get(tuple(sorted((a, b, cc))), 0.0) for cc in range(n) if cc not in (a, b)) - (m - 2) * G[a, b]) < 1e-10 for a, b in itertools.combinations(range(n), 2))
        g1 = S1 / m; g2 = G / comb(m, 2); eta = {tr: v / comb(m, 3) for tr, v in H.items()}
        inwin = {tr for tr in eta if tr[2] - tr[0] <= w}
        rho = np.zeros((n, n))                                                     # pair part of the windowed triple form
        for tr, v in eta.items():
            if tr not in inwin:
                for a, b in itertools.combinations(tr, 2): rho[a, b] += v / 3.0
        g1b = np.array([0.5 * sum(g2[i, j] for j in range(n) if abs(i - j) > w) for i in range(n)])   # banded pair form: site part
        for bits in itertools.product((0, 1), repeat=n):
            s = np.array(bits); idx = [i for i in range(n) if s[i]]
            env = sum(v for T, v in zip(subs, c) if all(s[i] for i in T))
            tri_full = sum(v for tr, v in eta.items() if s[tr[0]] and s[tr[1]] and s[tr[2]])
            tri_win = sum(eta[tr] for tr in inwin if s[tr[0]] and s[tr[1]] and s[tr[2]]) + sum(rho[a, b] for a, b in itertools.combinations(idx, 2))
            pair = sum(g2[a, b] for a, b in itertools.combinations(idx, 2))
            band = sum(g2[a, b] for a, b in itertools.combinations(idx, 2) if b - a <= w) + g1b[idx].sum()
            site = g1[idx].sum()
            chain = (env, tri_full, tri_win, pair, band, site)
            for x, y in zip(chain, chain[1:]):
                worst = max(worst, x - y); ncheck += 1
                assert x <= y + 1e-9, (n, m, w, bits, chain)
log(f"   {ncheck} inequalities of the chain envelope <= triples <= triples in a window <= pairs <= banded pairs <= sites: no violation "
    f"(largest excess {worst:.1e}); inclusion-exclusion and both double-counting identities hold")

log("=== 2. Val8 on PPII, order 4: site, pair and triple forms built here from P3's constants and the enumerated energy")
import p6lib as L
from gfbound import GFBound
from encl import EnvelopeSup
pw = L.pw; BETA = L.BETA
seq, bb, tau, m = "V8", "P2", 0.70, 4
G_, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n = G_.ns; k = list(G_.k); x0 = [int(v) for v in x0]
st, g, src = L.enumerate_g(G_, seq, bb, tau, verbose=False)
shape = tuple(k); gt = g.reshape(shape); f = pw.f_energy(st, c0, h, J); E = f + g
GF = GFBound(G_, x0, EnvelopeSup(G_), K=m)
chat = {T: float(sum(GF.total(m, T=list(T)))) for T in itertools.combinations(range(n), m)}
log(f"   {len(st)} states ({src}); anchor {x0}; {len(chat)} subsets, Gamma_{m} = {sum(chat.values()):.5f} kcal/mol = {BETA * sum(chat.values()):.4f} kT")
# anchored interpolation I_{m-1} g by inclusion-exclusion (own code)
Ig = np.empty(len(st)); pen = {key: np.zeros(len(st)) for key in ("env", "site", "pair", "triple")}
S1 = np.zeros(n); Gp = np.zeros((n, n)); Ht = {}
for T, v in chat.items():
    for i in T: S1[i] += v
    for i, j in itertools.combinations(T, 2): Gp[i, j] += v
    for tr in itertools.combinations(T, 3): Ht[tr] = Ht.get(tr, 0.0) + v
x0a = np.array(x0)
dcache = {}
def d_U(U, xU):
    key = (U, xU)
    if key not in dcache:
        val = 0.0
        for r in range(len(U) + 1):
            for V in itertools.combinations(range(len(U)), r):
                y = list(x0)
                for q in V: y[U[q]] = xU[q]
                val += (-1) ** (len(U) - r) * gt[tuple(y)]
        dcache[key] = val
    return dcache[key]
for a, x in enumerate(st):
    S = tuple(i for i in range(n) if x[i] != x0[i])
    Ig[a] = sum(d_U(U, tuple(int(x[i]) for i in U)) for r in range(m) for U in itertools.combinations(S, r))
    sset = set(S)
    pen["env"][a] = sum(v for T, v in chat.items() if sset.issuperset(T))
    pen["site"][a] = sum(S1[i] for i in S) / m
    pen["pair"][a] = sum(Gp[i, j] for i, j in itertools.combinations(S, 2)) / comb(m, 2)
    pen["triple"][a] = sum(Ht.get(tr, 0.0) for tr in itertools.combinations(S, 3)) / comb(m, 3)
rem = g - Ig
lnZE = float(logsumexp(-BETA * E))
log(f"   remainder g - I_{m - 1} g: range [{rem.min():.5f}, {rem.max():.5f}] kcal/mol; exact ln Z(E) = {lnZE:.6f}")
ref = dict(site=0.425, pair=0.0717, triple=0.0123)
for key in ("env", "triple", "pair", "site"):
    p = pen[key]
    viol = int((np.abs(rem) > p + 1e-10).sum())
    lo = float(logsumexp(-BETA * (f + Ig + p))); hi = float(logsumexp(-BETA * (f + Ig - p)))
    log(f"   {key:6s} form: |remainder| > penalty at {viol} of {len(st)} states;  ln Z in [{lo:.6f}, {hi:.6f}], width {hi - lo:.5f} nats"
        + (f" (P6's pairwise model with reduced three-site terms: {ref[key]}; difference {ref[key] - (hi - lo):+.4f})" if key in ref else " (the envelope itself: the best any share allocation can do)")
        + f";  exact inside: {lo <= lnZE <= hi}")
    assert viol == 0 and lo <= lnZE <= hi
assert (pen["env"] <= pen["triple"] + 1e-12).all() and (pen["triple"] <= pen["pair"] + 1e-12).all() and (pen["pair"] <= pen["site"] + 1e-12).all()

log(f"ALL DONE {time.time() - t0:.0f} s")
