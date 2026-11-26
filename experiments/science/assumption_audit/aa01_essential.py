#!/usr/bin/env python3
"""Assumption audit, part A (the certificate calculus of the science division): four assumptions classified as
"its removal makes the statement false", each with a counterexample that is run here and a control.

(1) A bound on the order-m part of g is needed (statement A3 of docs/science/ASSUMPTION_AUDIT.md).  Two functions that
    agree on the whole Hamming ball of radius m - 1 around the anchor -- so every evaluation the certificate makes,
    and every evaluated term, is the same -- with ln Z as far apart as one likes.  Control: with a pointwise bound
    on the remainder g - I_{m-1} g in force (|lambda| at the one state, zero elsewhere: valid for both functions) the
    sandwich built from it contains both.
(2) Non-negative group slacks are needed for the product inequality of Proposition A17.19 (LP).  Two groups whose
    slacks cancel pointwise: the hypothesis sum_g S_g <= m_+ - E holds, (LP) as a formula exceeds the exact ln Z.
    (LJ) uses Jensen only and stays valid.  Control: the same slack in one group, where (LP) is attained.
(3) The floor must hold on ALL of the space; the ceiling need not.  A landscape with two modes and models built
    around one of them: the ceiling restricted to that mode still gives a valid lower end, the floor that is valid
    on that mode only gives a false upper end.  Control: the floor repaired on the second mode.
(4) One site may not be given two roles in the remainder identity without the hypothesis on hosts: not re-run here --
    machine-checked by the theory division (term_orders_sharp, TermOrders.lean at dd067f1; file not read by us).

Run: python3 -B aa01_essential.py > aa01_essential.log
"""
import itertools, math
import numpy as np


def lnZ(E, beta=1.0):
    E = np.asarray(E, dtype=float); m = E[np.isfinite(E)].min()
    return float(-beta * m + math.log(np.exp(-beta * (E[np.isfinite(E)] - m)).sum()))


def main():
    fails = 0
    # ---------------------------------------------------------------- (1)
    n, k, m, beta = 6, 3, 3, 1.0
    X = np.array(list(itertools.product(range(k), repeat=n))); off = (X != 0).sum(1)
    ystar = np.array([1, 2, 1, 0, 0, 0]); spike = (X == ystar).all(1); assert off[spike][0] == m
    ball = off <= m - 1
    print(f"(1) {n} sites, {k} states per site, anchor (0,...,0), order m = {m}: the ball of radius {m - 1} has {int(ball.sum())} of {len(X)} states; g_a = 0, g_b = lambda at one state with exactly {m} sites off")
    for lam in (-2.0, -5.0, -10.0, -20.0):
        ga = np.zeros(len(X)); gb = np.where(spike, lam, 0.0)
        same = bool(np.array_equal(ga[ball], gb[ball]))
        d = lnZ(gb, beta) - lnZ(ga, beta)
        # control: a pointwise bound pen >= |g - I_{m-1} g| for both functions (I_{m-1} g = 0 for both: all evaluated terms vanish): floor and ceiling
        pen = np.where(spike, abs(lam), 0.0); lo, hi = lnZ(pen, beta), lnZ(-pen, beta)       # ceiling energy 0 + pen, floor energy 0 - pen
        ok = lo <= min(lnZ(ga), lnZ(gb)) and max(lnZ(ga), lnZ(gb)) <= hi
        print(f"    lambda = {lam:6.1f}: equal on the ball: {same}; ln Z(g_b) - ln Z(g_a) = {d:.4f} nats; control, the sandwich with the pointwise remainder bound {abs(lam):.0f} at that state: "
              f"[{lo:.4f}, {hi:.4f}] contains both: {ok}")
        fails += int(not same) + int(not ok)
    print("    => from the ball alone no finite bracket is valid on the class of all functions with those evaluations: the difference is unbounded in lambda")
    # ---------------------------------------------------------------- (2)
    beta = 1.0; mhi = np.zeros(2); E = np.zeros(2)                                          # two states, E = m_+
    S1 = np.array([0.0, math.log(2.0)]); S2 = -S1
    hyp = bool((S1 + S2 <= mhi - E + 1e-15).all())
    w = np.exp(-beta * mhi); w /= w.sum()
    LP = lnZ(mhi) + math.log(1.0 + float((w * (np.exp(beta * S1) - 1)).sum()) + float((w * (np.exp(beta * S2) - 1)).sum()))
    LJ = lnZ(mhi) + beta * float((w * (S1 + S2)).sum())
    print(f"(2) two states, E = m_+ = 0, groups S_1 = (0, ln 2), S_2 = -S_1: hypothesis sum_g S_g <= m_+ - E holds: {hyp}; exact ln Z(E) = {lnZ(E):.6f}; "
          f"(LP) as a formula = {LP:.6f} ({'VIOLATED' if LP > lnZ(E) + 1e-12 else 'holds'}: a group slack is negative); (LJ) = {LJ:.6f} ({'holds' if LJ <= lnZ(E) + 1e-12 else 'VIOLATED'})")
    fails += int(not (LP > lnZ(E) + 1e-12)) + int(not (LJ <= lnZ(E) + 1e-12))
    E2 = mhi - S1                                                                           # control: the slack S_1 alone, E = m_+ - S_1
    LP2 = lnZ(mhi) + math.log(1.0 + float((w * (np.exp(beta * S1) - 1)).sum()))
    print(f"    control, one non-negative group S_1 and E = m_+ - S_1: exact ln Z(E) = {lnZ(E2):.6f}, (LP) = {LP2:.6f} (attained: {abs(LP2 - lnZ(E2)) < 1e-12})")
    fails += int(abs(LP2 - lnZ(E2)) > 1e-12)
    # ---------------------------------------------------------------- (3)
    # ten states; mode A at state 0, mode B at state 9; models built around A: exact on states 0..4, the rest treated as "high" (energy 5)
    E = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 5.0, 5.0, 5.0, 0.2]); A = np.arange(10) <= 4
    ceil_A = np.where(A, E, np.inf)                                                          # ceiling: exact on A, +infinity elsewhere (a restriction)
    floor_A = np.where(A, E, 5.0)                                                            # "floor" from the picture of one mode: wrong at state 9
    floor_ok = np.where(A, E, np.minimum(E, 5.0))                                            # control: a floor that holds everywhere
    z = lnZ(E)
    print(f"(3) two modes (states 0 and 9), models built around the first: exact ln Z = {z:.6f}; ceiling restricted to the first mode: ln Z(m_+) = {lnZ(ceil_A):.6f} <= ln Z: {lnZ(ceil_A) <= z}; "
          f"a floor valid on that mode only: ln Z(m_-) = {lnZ(floor_A):.6f} >= ln Z: {lnZ(floor_A) >= z} (the upper end is FALSE: the second mode is missing from the floor); "
          f"control, the floor repaired at the second mode: ln Z(m_-) = {lnZ(floor_ok):.6f} >= ln Z: {lnZ(floor_ok) >= z}")
    fails += int(not lnZ(ceil_A) <= z) + int(lnZ(floor_A) >= z) + int(not lnZ(floor_ok) >= z)
    print(f"(4) not re-run: the hypothesis 'at most m hosts' of the remainder identity with one order per term is sharp -- machine-checked by the theory division (term_orders_sharp)")
    print(f"ALL DONE; examples that did not behave as stated: {fails}")
    assert fails == 0


if __name__ == "__main__":
    main()
