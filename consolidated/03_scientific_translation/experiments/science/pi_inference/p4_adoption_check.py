#!/usr/bin/env python3
"""Coordinator's checks before adopting workstream P4 (SCI-REV-0012).

(1) Counterexample P4.4 (the "iff" of the theory division's Proposition 11.18b(b) fails on a reset-closed domain that
    is not a product): two sites with states {0,1,2}, x0 = (0,0), D = product minus (1,1); additive known part with
    excitation energies (0, 1, 10) at both sites; zero star data; class constant c12 = 3 over the rectangles inside D.
    Checked here by brute force: D is reset-closed; the function -3*[both changed] belongs to the class; every member
    with zero star data is >= -3 where both sites are changed; the reference minimises the lower model on D; no shares
    exist (Delta_1 + Delta_2 = 2 < 3); on the full product the criterion fails, as the "iff" there requires.
(2) The finding about our own workstream P2: for poly-Phe on the strand at tau = 0.60 the minimum of the energy over
    the pair-clash-free domain X_tau is NOT in P2's greedily pruned product X' (on which P2's certificates are stated).
    Recomputed here from P2's stored grids with P2's own domain functions (restrict, s2min, pruned_product) and a
    driver that shares nothing with workstream P4's code.
Run:  python3 p4_adoption_check.py > p4_adoption_check.log
"""
import os, sys, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_P2"))

# ---------------------------------------------------------------- (1)
S = (0, 1, 2); x0 = (0, 0)
D = [(a, b) for a in S for b in S if (a, b) != (1, 1)]
reset_closed = all(((a, 0) in D) and ((0, b) in D) and ((0, 0) in D) for (a, b) in D)
A = (0.0, 1.0, 10.0); c12 = 3.0
gmin = {x: (-c12 if (x[0] != 0 and x[1] != 0) else 0.0) for x in D}
def in_class(g):
    for a, a2 in itertools.combinations(S, 2):
        for b, b2 in itertools.combinations(S, 2):
            corners = [(a, b), (a2, b), (a, b2), (a2, b2)]
            if all(q in D for q in corners):
                if abs(g[(a2, b2)] - g[(a2, b)] - g[(a, b2)] + g[(a, b)]) > c12 + 1e-12: return False
    return True
L = {x: A[x[0]] + A[x[1]] + gmin[x] for x in D}
Delta = min(A[1:]); shares_possible = (2 * Delta >= c12)
print("(1) Counterexample P4.4")
print(f"    D reset-closed: {reset_closed};  -3*[both changed] in the class on D: {in_class(gmin)};  "
      f"anchored rectangles inside D force g' >= -3 at {[x for x in D if x[0] and x[1]]}")
print(f"    L - L(x0) on D: " + ", ".join(f"{x}: {L[x] - L[x0]:g}" for x in D) + f"  -> x0 minimises: {all(L[x] >= L[x0] for x in D)}")
print(f"    shares: need s12 + s21 >= {c12:g} with s12 <= Delta_1 = {Delta:g}, s21 <= Delta_2 = {Delta:g}: possible = {shares_possible}")
print(f"    on the full product the point (1,1) has L - L(x0) = {A[1] + A[1] - c12:g}: criterion fails there, consistent with the 'iff' on products")
assert reset_closed and in_class(gmin) and all(L[x] >= L[x0] for x in D) and not shares_possible and A[1] + A[1] - c12 < 0

# ---------------------------------------------------------------- (2)
import anlib, an_main
print("(2) poly-Phe on the strand, tau = 0.60: minimum of E = f + g_GB (kcal/mol) over the clash-free domain X_tau and over P2's pruned product X'")
tau = 0.60
for n in (4, 5, 6, 7, 8):
    d0 = anlib.load_fb(f"fb_F{n}_E_R3_t0.60"); d = anlib.restrict(d0, tau)
    E = d["tors"] + d["lj"] + d["coul"] + d["gb"]
    mask = d["s2min"] > tau
    keep = an_main.pruned_product(d, tau)
    sub = np.zeros(E.shape, dtype=bool); sub[np.ix_(*keep)] = True
    assert not np.any(sub & ~mask), "the pruned product must lie inside X_tau"
    Emin_tau = float(E[mask].min()); Emin_sub = float(E[sub].min())
    amin = np.unravel_index(np.argmin(np.where(mask, E, np.inf)), E.shape)
    in_sub = bool(sub[amin])
    print(f"    Phe{n}: |X_tau| = {int(mask.sum())}, |X'| = {int(sub.sum())} (shape {tuple(len(k) for k in keep)});  min over X_tau = {Emin_tau:.3f}, "
          f"min over X' = {Emin_sub:.3f}, difference = {Emin_sub - Emin_tau:.2f};  minimiser of X_tau lies in X': {in_sub}")
print("ALL OK")
