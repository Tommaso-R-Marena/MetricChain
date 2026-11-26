#!/usr/bin/env python3
"""R18, item 1 -- the classification rule and the refinement window of ENG-RES-0014 §1 against a literal loop.

Not the engineering division's code and not r6lib: written from the text of the algorithm.

LITERAL LOOP (K_REPORT §2.2, step 1, word for word):
    "A new point gets the trivial bracket ... and rung 0.  Brackets are only ever refined: to classify a_i at
     level j, while U_i > s_j and L_i <= s_j e^{-b} move a_i to the next rung l, call I_l on its fibre and
     intersect; then a_i is low if U_i <= s_j and high otherwise."
The point keeps its bracket and its rung from level to level; the levels are visited in increasing order; the
point is classified only at the levels at which it is "present" (it is among the first M_j points) -- an
arbitrary subset, because M_j is not monotone in j.

CLOSED RULE (ENG-RES-0014 §1), per point:
    A_0 = t0, B_0 = x_0 - t0, A_l = min(A_{l-1}, alpha_l), B_l = min(B_{l-1}, beta_l)   (alpha_l + beta_l <= x_l)
    HIGH at the level s  iff  W > s e^{-c},   c = max_{0<=l<=L} min(b - A_l, B_l)
    the point is moved from rung l to rung l+1 at the level s  iff  W e^{b - A_l} <= s < W e^{B_l}.

ARITHMETIC.  Every logarithm is an integer multiple of a unit (1/4 in the "coarse" regime, where ties are
frequent; 1/64 in the "fine" one).  All comparisons are exact; a tie is a real tie.

CONTROLS (each must produce disagreements, otherwise the test has no power):
    swap     c' = min_l max(b - A_l, B_l)                       (min and max exchanged)
    legacy   c = b for "bottom", c = 0 for "top", whatever t0   (the convention of the runs published before)
    nonstr   HIGH iff W >= s e^{-c}                              (the tie given to HIGH)
    noint    A_l = alpha_l, B_l = beta_l without the running minimum (no intersection)
    winstr   window  W e^{b - A_l} < s <= W e^{B_l}             (strictness exchanged)
    ladder   last accuracy x_L > b                               (hypothesis x_L <= b dropped: unclassified points)

usage: python3 -I -B r18_rule.py [points_per_regime_and_mode] [seed]
"""
import random
import resource
import sys
import time


def literal_history(xs, b, t0, pos, lnW, levels, present, intersect=True):
    """The literal loop for one point.  xs[0..L]; pos[l] = (alpha_l, beta_l) for l = 1..L (pos[0] unused).
    Returns (classes, first_call, events): classes[k] in {None, 'LOW', 'HIGH', 'UNCL'}; first_call[l] = index of the
    level at which rung l was called (l = 1..L) or None; events = counts of exact ties met."""
    L = len(xs) - 1
    lnL, lnU = lnW - t0, lnW + xs[0] - t0          # the trivial bracket [W e^{-t0}, W e^{x0 - t0}]
    rung = 0
    classes = []
    first_call = [None] * (L + 1)
    tie_U = tie_L = 0
    for k, ls in enumerate(levels):
        if not present[k]:
            classes.append(None)
            continue
        stuck = False
        while lnU > ls and lnL <= ls - b:           # "while U_i > s_j and L_i <= s_j e^{-b}"
            if lnL == ls - b:
                tie_L += 1
            if rung == L:
                stuck = True                        # "a point is still unclassified at rung L" (abort of step 3)
                break
            rung += 1                               # "move a_i to the next rung l, call I_l on its fibre ..."
            a, be = pos[rung]
            if intersect:
                lnL = max(lnL, lnW - a)             # "... and intersect"
                lnU = min(lnU, lnW + be)
            else:                                   # (control only) an algorithm that keeps the latest bracket alone
                lnL, lnU = lnW - a, lnW + be
            first_call[rung] = k
        if stuck:
            classes.append("UNCL")
        elif lnU <= ls:                             # "then a_i is low if U_i <= s_j"
            if lnU == ls:
                tie_U += 1
            classes.append("LOW")
        else:                                       # "and high otherwise"
            classes.append("HIGH")
    return classes, first_call, (tie_U, tie_L)


def nested(xs, t0, pos, intersect=True):
    """(A_l, B_l), l = 0..L."""
    A, B = [t0], [xs[0] - t0]
    for l in range(1, len(xs)):
        a, be = pos[l]
        A.append(min(A[-1], a) if intersect else a)
        B.append(min(B[-1], be) if intersect else be)
    return A, B


def shift(A, B, b):
    return max(min(b - a, be) for a, be in zip(A, B))


def shift_swapped(A, B, b):
    return min(max(b - a, be) for a, be in zip(A, B))


def draw_case(rng, unit, mode, ladder_ok=True):
    """One point with its ladder, positions, place and levels; all in integer multiples of 1/unit."""
    b = rng.choice([2, 4, 6, 8]) * unit // 4                     # b in {1/2, 1, 3/2, 2}
    lam = rng.choice([1, 2, 3, 4]) * unit // 4                   # lambda in {1/4, ..., 1}
    L = rng.randint(1, 5)
    if ladder_ok:
        xL = b if rng.random() < 0.5 else 2 * rng.randint(1, max(1, b // 2))     # x_L <= b (half of the cases: = b), even
    else:
        xL = b + 2 * rng.randint(1, 4)                                             # control: x_L > b
    xs = [xL]
    for _ in range(L):
        xs.append(xs[-1] + 2 * rng.randint(1, max(1, 3 * unit // 4)))             # strictly decreasing ladder, even entries
    xs = xs[::-1]                                                                   # x_0 > x_1 > ... > x_L
    x0 = xs[0]
    r = rng.random()
    if r < 0.15:
        t0 = rng.choice([0, x0])                                                    # the value at an end of the trivial bracket
    elif r < 0.45:
        t0 = rng.randint(0, min(x0, b + 1))                                         # corner: within the tolerance of the lower end
    elif r < 0.75:
        t0 = x0 - rng.randint(0, min(x0, b + 1))                                    # corner: within the tolerance of the upper end
    else:
        t0 = rng.randint(0, x0)
    pos = [None]
    for l in range(1, L + 1):
        x = xs[l]
        if mode == "bottom":
            pos.append((0, x))
        elif mode == "top":
            pos.append((x, 0))
        elif mode == "centre":
            pos.append((x // 2, x // 2))
        else:                                                                        # any admissible pair, also narrower than x_l
            a = rng.randint(0, x)
            pos.append((a, rng.randint(0, x - a)))
    lnW = rng.randint(-3 * unit, 3 * unit)
    lo = lnW - x0 - b - 2 * lam - rng.randint(0, lam)                               # levels from below every bracket end ...
    nlev = (2 * x0 + 2 * b + 6 * lam) // lam + 2                                    # ... to above every bracket end
    levels = [lo + k * lam for k in range(nlev)]
    r = rng.random()
    if r < 0.4:
        present = [True] * nlev
    elif r < 0.7:
        p = rng.random()
        present = [rng.random() < p for _ in range(nlev)]
    else:                                                                            # present from some level on, with gaps
        k0 = rng.randint(0, nlev - 1)
        present = [k >= k0 and rng.random() < 0.8 for k in range(nlev)]
    return xs, b, lam, t0, pos, lnW, levels, present


def run(npts, seed):
    rng = random.Random(seed)
    tot = {}
    for unit, regime in ((4, "coarse (unit 1/4)"), (64, "fine (unit 1/64)")):
        for mode in ("bottom", "top", "centre", "general"):
            c = dict(points=0, decisions=0, rule_bad=0, uncl=0, ties_rule=0, ties_U=0, ties_L=0, c_out_of_range=0,
                     swap_bad=0, legacy_bad=0, legacy_tested=0, legacy_bad_in_range=0, legacy_in_range=0, nonstr_bad=0,
                     noint_bad=0, win_checks=0, win_bad=0, winstr_bad=0, closed_form_bad=0,
                     bottom_range_c_ne_b=0, bottom_range_cases=0, bottom_range_xLb_c_ne_b=0, top_range_c_ne_0=0, top_range_cases=0,
                     corner_cases=0, calls=0)
            for _ in range(npts):
                xs, b, lam, t0, pos, lnW, levels, present = draw_case(rng, unit, mode)
                Lr = len(xs) - 1
                x0 = xs[0]
                classes, first_call, (tU, tL) = literal_history(xs, b, t0, pos, lnW, levels, present)
                A, B = nested(xs, t0, pos)
                cc = shift(A, B, b)
                c_sw = shift_swapped(A, B, b)
                A2, B2 = nested(xs, t0, pos, intersect=False)
                c_ni = shift(A2, B2, b)
                c["points"] += 1
                c["ties_U"] += tU
                c["ties_L"] += tL
                c["c_out_of_range"] += not (0 <= cc <= b)
                if mode in ("bottom", "top"):
                    c_leg = b if mode == "bottom" else 0
                    in_range = (t0 >= b and x0 - t0 >= b)
                    c["corner_cases"] += not in_range
                    # the closed forms I derived for the two uniform behaviours (NOTES.md)
                    if mode == "bottom":
                        cf = max(min(b - t0, x0 - t0), min(b, x0 - t0, xs[1]))
                        if in_range:
                            c["bottom_range_cases"] += 1
                            c["bottom_range_c_ne_b"] += (cc != b)
                            c["bottom_range_xLb_c_ne_b"] += (cc != b and xs[-1] == b)
                    else:
                        cf = max(0, min(b - t0, x0 - t0))
                        if in_range:
                            c["top_range_cases"] += 1
                            c["top_range_c_ne_0"] += (cc != 0)
                    c["closed_form_bad"] += (cf != cc)
                for k, cls in enumerate(classes):
                    if cls is None:
                        continue
                    ls = levels[k]
                    c["decisions"] += 1
                    if cls == "UNCL":
                        c["uncl"] += 1
                        continue
                    high = (cls == "HIGH")
                    c["rule_bad"] += ((lnW > ls - cc) != high)
                    c["ties_rule"] += (lnW == ls - cc)
                    c["swap_bad"] += ((lnW > ls - c_sw) != high)
                    c["nonstr_bad"] += ((lnW >= ls - cc) != high)
                    c["noint_bad"] += ((lnW > ls - c_ni) != high)
                    if mode in ("bottom", "top"):
                        bad = ((lnW > ls - c_leg) != high)
                        if in_range:
                            c["legacy_in_range"] += 1
                            c["legacy_bad_in_range"] += bad
                        else:
                            c["legacy_tested"] += 1
                            c["legacy_bad"] += bad
                # the refinement windows: the first level at which rung l+1 is called
                for l in range(Lr):
                    want = next((k for k, ls in enumerate(levels) if present[k] and lnW + b - A[l] <= ls < lnW + B[l]), None)
                    want_s = next((k for k, ls in enumerate(levels) if present[k] and lnW + b - A[l] < ls <= lnW + B[l]), None)
                    c["win_checks"] += 1
                    c["win_bad"] += (want != first_call[l + 1])
                    c["winstr_bad"] += (want_s != first_call[l + 1])
                    c["calls"] += first_call[l + 1] is not None
            tot[(regime, mode)] = c
    # control "ladder": x_L > b
    ctl = dict(points=0, decisions=0, uncl=0)
    for _ in range(npts):
        xs, b, lam, t0, pos, lnW, levels, present = draw_case(rng, 4, "general", ladder_ok=False)
        classes, _, _ = literal_history(xs, b, t0, pos, lnW, levels, present)
        ctl["points"] += 1
        ctl["decisions"] += sum(x is not None for x in classes)
        ctl["uncl"] += sum(x == "UNCL" for x in classes)
    # block D: "bottom" INSIDE the range t0 >= b, x0 - t0 >= b, but with every inner accuracy below the tolerance
    # (x_1 < b, allowed by Theorem 11.56, which asks for x_L <= b only): the message says c = b there.
    D = dict(points=0, c_eq_b=0, c_eq_x1=0, decisions=0, legacy_bad=0, rule_bad=0)
    for _ in range(npts):
        unit = 4
        b = rng.choice([4, 6, 8])
        lam = rng.choice([1, 2, 3, 4])
        L = rng.randint(1, 2)
        x1 = 2 * rng.randint(1, b // 2 - 1) if L == 1 else 2 * rng.randint(2, b // 2 - 1) if b > 4 else None
        if x1 is None:
            L, x1 = 1, 2
        xs = [2 * b + 2 * rng.randint(1, 6), x1] + ([2 * rng.randint(1, x1 // 2 - 1)] if L == 2 and x1 > 2 else [])
        x0 = xs[0]
        t0 = rng.randint(b, x0 - b)
        pos = [None] + [(0, x) for x in xs[1:]]
        lnW = rng.randint(-12, 12)
        lo = lnW - x0 - b - 2 * lam
        nlev = (2 * x0 + 2 * b + 6 * lam) // lam + 2
        levels = [lo + k * lam for k in range(nlev)]
        present = [True] * nlev
        classes, _, _ = literal_history(xs, b, t0, pos, lnW, levels, present)
        A, B = nested(xs, t0, pos)
        cc = shift(A, B, b)
        D["points"] += 1
        D["c_eq_b"] += (cc == b)
        D["c_eq_x1"] += (cc == max(b - t0, min(b, x0 - t0, xs[1])) and cc == xs[1])
        for k, cls in enumerate(classes):
            high = (cls == "HIGH")
            D["decisions"] += 1
            D["rule_bad"] += ((lnW > levels[k] - cc) != high)
            D["legacy_bad"] += ((lnW > levels[k] - b) != high)
    # block E: which hypotheses on the positions does the rule itself need?
    #   wide     intermediate rungs with any non-negative positions (ratio e^{x_l} NOT respected); last rung within x_L <= b
    #   invalid  positions of either sign (the value outside the bracket), 0 <= alpha_l + beta_l <= x_l
    #   nointer  CONTROL: an algorithm that does not intersect, against the rule written with the raw positions
    #   descend  CONTROL: the same algorithm with the levels visited in DECREASING order (brackets kept), against the rule
    E = {k: dict(points=0, decisions=0, rule_bad=0, uncl=0, c_out=0, win_bad=0, win_checks=0) for k in ("wide", "invalid", "nointer", "descend")}
    for kind in ("wide", "invalid", "nointer", "descend"):
        for _ in range(npts):
            xs, b, lam, t0, pos, lnW, levels, present = draw_case(rng, 4, "general")
            Lr = len(xs) - 1
            if kind == "wide":
                pos = [None] + [(rng.randint(0, 2 * xs[0]), rng.randint(0, 2 * xs[0])) for _ in range(1, Lr)] + [pos[Lr]]
            elif kind == "invalid":
                pos = [None]
                for l in range(1, Lr + 1):
                    wdt = rng.randint(0, xs[l])
                    a = rng.randint(-xs[0], xs[0])
                    pos.append((a, wdt - a))
                t0 = rng.randint(-xs[0], 2 * xs[0])               # an invalid trivial bracket as well
            if kind == "descend":
                levels, present = levels[::-1], present[::-1]
            classes, first_call, _ = literal_history(xs, b, t0, pos, lnW, levels, present, intersect=(kind != "nointer"))
            A, B = nested(xs, t0, pos, intersect=(kind != "nointer"))
            cc = shift(A, B, b)
            e = E[kind]
            e["points"] += 1
            e["c_out"] += not (0 <= cc <= b)
            for k, cls in enumerate(classes):
                if cls is None:
                    continue
                e["decisions"] += 1
                if cls == "UNCL":
                    e["uncl"] += 1
                    continue
                e["rule_bad"] += ((lnW > levels[k] - cc) != (cls == "HIGH"))
            if kind in ("wide", "invalid"):
                for l in range(Lr):
                    want = next((k for k, ls in enumerate(levels) if present[k] and lnW + b - A[l] <= ls < lnW + B[l]), None)
                    e["win_checks"] += 1
                    e["win_bad"] += (want != first_call[l + 1])
    return tot, ctl, D, E


def main():
    npts = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 18
    t = time.time()
    print(f"r18_rule.py  points per (regime, mode) = {npts}  seed = {seed}  start {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    tot, ctl, D, E = run(npts, seed)
    keys = ["points", "decisions", "calls", "ties_rule", "ties_U", "ties_L", "corner_cases"]
    print("\nA. THE RULE AND THE WINDOW AGAINST THE LITERAL LOOP (every number in the columns 'bad' must be 0)")
    print(f"{'regime':18s} {'positions':8s} " + " ".join(f"{k:>12s}" for k in keys) + "   rule_bad  unclassified  c_outside_[0,b]  window_bad (of checks)")
    S = dict(decisions=0, rule_bad=0, uncl=0, win_bad=0, win_checks=0, c_out=0, ties=0)
    for (regime, mode), c in tot.items():
        print(f"{regime:18s} {mode:8s} " + " ".join(f"{c[k]:12d}" for k in keys) +
              f"   {c['rule_bad']:8d}  {c['uncl']:12d}  {c['c_out_of_range']:15d}  {c['win_bad']:6d} ({c['win_checks']})")
        S["decisions"] += c["decisions"]; S["rule_bad"] += c["rule_bad"]; S["uncl"] += c["uncl"]; S["win_bad"] += c["win_bad"]
        S["win_checks"] += c["win_checks"]; S["c_out"] += c["c_out_of_range"]; S["ties"] += c["ties_rule"]
    print(f"TOTAL decisions {S['decisions']}  (of them exactly on the threshold W = s e^-c: {S['ties']})  rule violations {S['rule_bad']}  "
          f"unclassified {S['uncl']}  c outside [0,b] {S['c_out']}  window checks {S['win_checks']}  window violations {S['win_bad']}")
    print("\nB. CONTROLS (each must be > 0)")
    print(f"{'regime':18s} {'positions':8s} {'swap':>10s} {'nonstrict':>10s} {'no-intersect':>12s} {'window-strictness':>18s} {'legacy outside range (of decisions)':>36s} {'legacy INSIDE range (must be 0 if x_L = b ...)':>48s}")
    for (regime, mode), c in tot.items():
        leg = f"{c['legacy_bad']} ({c['legacy_tested']})" if mode in ("bottom", "top") else "-"
        legin = f"{c['legacy_bad_in_range']} ({c['legacy_in_range']})" if mode in ("bottom", "top") else "-"
        print(f"{regime:18s} {mode:8s} {c['swap_bad']:10d} {c['nonstr_bad']:10d} {c['noint_bad']:12d} {c['winstr_bad']:18d} {leg:>36s} {legin:>48s}")
    print(f"control 'ladder' (x_L > b, general positions, coarse): points {ctl['points']}  decisions {ctl['decisions']}  UNCLASSIFIED at the last rung {ctl['uncl']}")
    print("\nC. THE TWO UNIFORM BEHAVIOURS: my closed forms  c_bottom = max(min(b-t0, x0-t0), min(b, x0-t0, x_1)),  c_top = max(0, min(b-t0, x0-t0))")
    for (regime, mode), c in tot.items():
        if mode == "bottom":
            print(f"{regime:18s} bottom: closed form wrong in {c['closed_form_bad']} of {c['points']};  cases with t0 >= b and x0-t0 >= b: {c['bottom_range_cases']}, "
                  f"of them with c != b: {c['bottom_range_c_ne_b']} (all have x_1 < b; with x_L = b: {c['bottom_range_xLb_c_ne_b']})")
        if mode == "top":
            print(f"{regime:18s} top:    closed form wrong in {c['closed_form_bad']} of {c['points']};  cases with t0 >= b and x0-t0 >= b: {c['top_range_cases']}, "
                  f"of them with c != 0: {c['top_range_c_ne_0']}")
    print("\nD. \"BOTTOM GIVES c = b AS LONG AS t0 >= b AND x0 - t0 >= b\": ladders with every inner accuracy below the tolerance (x_1 < b), place inside the range")
    print(f"points {D['points']}:  c = b in {D['c_eq_b']};  c = x_1 (< b) in {D['c_eq_x1']};  literal decisions {D['decisions']}: against the exact rule {D['rule_bad']}, "
          f"against the convention c = b: {D['legacy_bad']}")
    print("\nE. WHICH HYPOTHESES ON THE POSITIONS DOES THE RULE NEED?  (coarse grid, positions of any admissible kind)")
    for kind, txt in (("wide", "intermediate rungs wider than x_l (any non-negative positions), last rung within x_L <= b: must hold"),
                      ("invalid", "positions of either sign (value outside the bracket; trivial bracket too), widths within x_l: must hold"),
                      ("nointer", "CONTROL an algorithm WITHOUT intersection against the rule with raw positions: must fail"),
                      ("descend", "CONTROL the levels visited in DECREASING order (brackets kept), against the rule: must fail")):
        e = E[kind]
        print(f"  {kind:8s} {txt}\n           points {e['points']}  decisions {e['decisions']}  rule violations {e['rule_bad']}  unclassified {e['uncl']}  "
              f"c outside [0, b] in {e['c_out']} points  window violations {e['win_bad']} of {e['win_checks']}")
    ok = (S["rule_bad"] == 0 and S["uncl"] == 0 and S["win_bad"] == 0 and S["c_out"] == 0 and D["rule_bad"] == 0
          and E["wide"]["rule_bad"] == 0 and E["wide"]["win_bad"] == 0 and E["invalid"]["rule_bad"] == 0 and E["invalid"]["win_bad"] == 0)
    powers = all(c["swap_bad"] > 0 and c["nonstr_bad"] > 0 and c["winstr_bad"] > 0 for c in tot.values()) and ctl["uncl"] > 0 \
        and all(c["legacy_bad"] > 0 for (r, m), c in tot.items() if m in ("bottom", "top")) \
        and all(c["noint_bad"] > 0 for (r, m), c in tot.items() if m == "general") and E["nointer"]["rule_bad"] > 0 and E["descend"]["rule_bad"] > 0
    print(f"\nVERDICT: rule and window {'HOLD' if ok else 'FAIL'} on every decision;  every control {'FAILED as it must' if powers else 'DID NOT ALL FAIL (test without power)'}")
    print(f"end {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}  wall {time.time() - t:.1f} s  peak RSS MB: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.1f}")


if __name__ == "__main__":
    main()
