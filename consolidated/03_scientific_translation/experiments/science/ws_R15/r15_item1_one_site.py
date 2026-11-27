#!/usr/bin/env python3
"""R15, Item 1 -- Proposition 11.18e(b')(i) of the theory report at f7df44f: the randomised count on one site.

Own code, written from the statement (replication).  Three parts.

PART A  The algorithm "skip one uniformly random state with probability k*delta" written out, and its exact failure
        probability on every instance of a grid (ties included), exact arithmetic (integers / Fractions).
        One site, k states, energies E(x); weights z(x) = e^{-E(x)}.
        With probability 1 - k*delta: evaluate all k states, return the exact answer.
        With probability k*delta:     draw a uniformly from the k states, evaluate the other k - 1, and return
            task MIN :  the lower bound  l_a = min_{x != a} E(x) - w              (w >= 0 a slack; also the bracket
                        [l_a, min_{x != a} E(x)], whose upper end is always valid)
            task LNZ :  the bracket [ln Z_a, ln Z_a + W],  Z_a = sum_{x != a} z(x)  (lower end always valid).
        Failure probability on an instance = delta * #{a : the output after skipping a is invalid on that instance}.
            MIN: skipping a is invalid  iff  E(a) < min_{x != a} E(x) - w.
            LNZ: skipping a is invalid  iff  z(a) > tau * Z_a,  tau = e^W - 1   (iff the weight fraction of a exceeds
                 theta = tau/(1 + tau) = 1 - e^{-W}).
        Claim to test (the coordinator's first reading, SCI-RES-0016 section 3): MIN -- at most one invalid skip for
        every w >= 0; LNZ -- at most one invalid skip iff tau >= 1 (W >= ln 2); for tau < 1 the worst number of invalid
        skips is min(k, ceil(1/theta) - 1).
PART B  The trivial algorithm "with probability delta evaluate nothing and return anything; otherwise evaluate
        everything": expected count (1 - delta) k, failure at most delta, for every width -- arithmetic only.
PART C  The lower bound for EVERY randomised adaptive algorithm, in a finite model, by linear programming over
        behavioural strategies (sequence form).  Values on a ladder of L + 1 levels 0 > -s > ... > -L s, task MIN with a
        prescribed width w < s (so an output is valid for exactly one value of the minimum, and the outputs may be
        taken to be levels).  At the instance g0 = (0, ..., 0) a run that leaves a state unevaluated is the same on the
        L + 1 instances that differ from g0 at that state only, and its output is valid for at most one of them; so
        P_{g0}(a not evaluated) <= delta (L + 1)/L and E|Q(g0)| >= k (1 - delta (L + 1)/L)  -- the argument of (b')(i)
        with a ladder in place of the limit D -> infinity; as L -> infinity this is (1 - delta) k.
        The LP minimises E|Q(g0)| over all randomised adaptive algorithms subject to failure <= delta on every
        instance of the ladder; it must return exactly k (1 - delta (L + 1)/L).

Run:  OMP_NUM_THREADS=1 python3 r15_item1_one_site.py > logs/item1_one_site.log
"""
import itertools, math, resource, sys, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix

t0 = time.time()
ok_all = True


def check(cond, msg):
    global ok_all
    if not cond:
        ok_all = False
        print("   !!! CHECK FAILED:", msg)


# ---------------------------------------------------------------------------------------------------------------
print("PART A  skip-one algorithm: exact number of invalid skips on a grid of instances (ties included)")
# weights z = e^{-E}: positive integers, with ties, moderate ratios and needles
ZGRID = [1, 2, 3, 7, 50, 10 ** 4, 10 ** 12]
# energies for the MIN task: Fractions with ties and deep needles
EGRID = [Fr(0), Fr(-1, 5), Fr(-1, 2), Fr(-1), Fr(-2), Fr(-5), Fr(-40)]
TAUS = [(Fr(1, 20), "W=ln(1.05)=0.0488"), (Fr(1, 3), "W=ln(4/3)=0.2877"), (Fr(1, 2), "W=ln(1.5)=0.4055"),
        (Fr(999, 1000), "W=ln(1.999)=0.6926"), (Fr(1), "W=ln 2=0.6931"), (Fr(2), "W=ln 3=1.0986"), (Fr(19), "W=ln 20=2.9957")]
SLACKS = [Fr(0), Fr(1, 10), Fr(1), Fr(3)]
for k in (2, 3, 4):
    print(f" k = {k}: {len(ZGRID) ** k} instances (LNZ), {len(EGRID) ** k} instances (MIN)")
    for tau, name in TAUS:
        theta = tau / (1 + tau)
        hist = {}
        worst = None
        for z in itertools.product(ZGRID, repeat=k):
            Z = sum(z)
            bad = sum(1 for a in range(k) if z[a] > tau * (Z - z[a]))
            # the same through the weight fraction, as a cross-check of the algebra
            bad2 = sum(1 for a in range(k) if Fr(z[a], Z) > theta)
            check(bad == bad2, "invalid-skip criterion vs weight fraction")
            hist[bad] = hist.get(bad, 0) + 1
            if worst is None or bad > worst[0]:
                worst = (bad, z)
        pred = min(k, math.ceil(1 / theta) - 1)
        # the needle instance: exactly one invalid skip, whatever tau on this grid
        needle = tuple([10 ** 12] + [1] * (k - 1))
        nb = sum(1 for a in range(k) if needle[a] > tau * (sum(needle) - needle[a]))
        flat = sum(1 for a in range(k) if 1 > tau * (k - 1))
        check(worst[0] == pred, f"LNZ worst number of invalid skips {worst[0]} != predicted {pred} (k={k}, {name})")
        check(nb == 1, "needle instance: exactly one invalid skip")
        print(f"   LNZ {name:22s} theta=1-e^-W={float(theta):.4f}: invalid skips per instance {dict(sorted(hist.items()))}; "
              f"worst {worst[0]} at z={worst[1]} (predicted min(k, ceil(1/theta)-1) = {pred}); needle: {nb}; flat instance: {flat}"
              f"  => worst failure = {worst[0]} x delta")
    for w in SLACKS:
        hist = {}
        worst = 0
        for E in itertools.product(EGRID, repeat=k):
            m = min(E)
            bad = 0
            for a in range(k):
                seen = min(E[x] for x in range(k) if x != a)
                lower = seen - w
                if not (lower <= m):
                    bad += 1
                check(seen >= m, "upper end min-of-seen is always a valid upper bound")
            hist[bad] = hist.get(bad, 0) + 1
            worst = max(worst, bad)
        check(worst == 1, f"MIN worst number of invalid skips {worst} != 1 (k={k}, w={w})")
        print(f"   MIN slack w={str(w):5s}: invalid skips per instance {dict(sorted(hist.items()))}; worst {worst}"
              f"  => worst failure = {worst} x delta")

# ---------------------------------------------------------------------------------------------------------------
print("PART B  the trivial mixture: with probability delta evaluate nothing; otherwise everything")
for k in (2, 3, 4, 10):
    for delta in (Fr(1, 20), Fr(3, 10), Fr(9, 10)):
        count = (1 - delta) * k          # every state is evaluated with probability 1 - delta
        fail_max = delta                  # a wrong output only in the branch of probability delta
        check(count == (1 - delta) * k and fail_max <= delta, "trivial mixture")
print("   expected count (1 - delta) k and failure <= delta on every instance, for every width, every k, every delta in [0, 1]"
      " -- needs neither k delta <= 1 nor a width >= ln 2")
print("   (skip-one needs k delta <= 1: e.g. k = 4, delta = 0.3 gives k delta = 1.2, not a probability)")

# ---------------------------------------------------------------------------------------------------------------
print("PART C  LP over all randomised adaptive algorithms (sequence form), task MIN, prescribed width, ladder of L+1 levels")


def lp_count(k, L, delta, objective="g0"):
    """minimum over randomised adaptive algorithms of E|Q(g0)| (g0 = top level everywhere), subject to failure <= delta
    on every instance g in {0..L}^k (level j means the value -j s).  Outputs: a level (valid iff it is the minimum's
    level, i.e. the deepest level of g).  Sequence form: variables y[(h, act)], h a tuple of (state, level) pairs."""
    levels = list(range(L + 1))
    var = {}

    def v(key):
        if key not in var:
            var[key] = len(var)
        return var[key]

    # enumerate histories
    hists = [()]
    frontier = [()]
    for t in range(1, k):
        new = []
        for h in frontier:
            used = {a for a, _ in h}
            for b in range(k):
                if b in used:
                    continue
                for lev in levels:
                    new.append(h + ((b, lev),))
        hists += new
        frontier = new
    # variables: at each history (fewer than k states evaluated): stop with guess j, or query b
    for h in hists:
        used = {a for a, _ in h}
        for j in levels:
            v((h, ("guess", j)))
        for b in range(k):
            if b not in used:
                v((h, ("query", b)))
    nv = len(var)
    Aeq = lil_matrix((len(hists), nv))
    beq = np.zeros(len(hists))
    for r, h in enumerate(hists):
        used = {a for a, _ in h}
        for j in levels:
            Aeq[r, var[(h, ("guess", j))]] = 1.0
        for b in range(k):
            if b not in used:
                Aeq[r, var[(h, ("query", b))]] = 1.0
        if len(h) == 0:
            beq[r] = 1.0
        else:
            parent, (b, lev) = h[:-1], h[-1]
            Aeq[r, var[(parent, ("query", b))]] = -1.0
    insts = list(itertools.product(levels, repeat=k))
    Aub = lil_matrix((len(insts), nv))
    bub = np.full(len(insts), float(delta))
    cost = {}
    for gi, g in enumerate(insts):
        deepest = max(g)
        c = np.zeros(nv)
        for h in hists:
            if any(g[a] != lev for a, lev in h):
                continue                                    # history not consistent with this instance
            used = {a for a, _ in h}
            for j in levels:
                idx = var[(h, ("guess", j))]
                if j != deepest:
                    Aub[gi, idx] = 1.0                      # a wrong guess
                c[idx] += len(h)
            if len(h) == k - 1:                             # querying the last state: k evaluations, exact answer
                for b in range(k):
                    if b not in used:
                        c[var[(h, ("query", b))]] += k
        cost[g] = c
    g0 = tuple([0] * k)
    res = linprog(cost[g0], A_ub=Aub.tocsr(), b_ub=bub, A_eq=Aeq.tocsr(), b_eq=beq, bounds=(0, None), method="highs")
    assert res.status == 0, res.message
    y = res.x
    worst_fail = float((Aub.tocsr() @ y).max())
    return res.fun, nv, len(insts), worst_fail


print(f"   {'k':>2} {'L':>2} {'delta':>6} {'variables':>9} {'instances':>9} {'LP value E|Q(g0)|':>18} {'k(1-delta(L+1)/L)':>18} {'(1-delta)k':>11} {'worst failure':>13}")
for k in (2, 3, 4):
    for L in (1, 2, 3, 5):
        if k == 4 and L == 5:
            continue                                        # 6^4 instances x many histories: skipped to stay small
        for delta in (0.05, 0.2):
            val, nv, ni, wf = lp_count(k, L, delta)
            pred = k * (1 - delta * (L + 1) / L)
            check(abs(val - pred) < 1e-7, f"LP value {val} != ladder bound {pred} (k={k}, L={L}, delta={delta})")
            check(wf <= delta + 1e-9, "LP solution violates the failure constraint")
            print(f"   {k:>2} {L:>2} {delta:>6} {nv:>9} {ni:>9} {val:>18.9f} {pred:>18.9f} {(1 - delta) * k:>11.4f} {wf:>13.9f}")
print("   => in the finite model the least expected count at g0 over ALL randomised adaptive algorithms is exactly the ladder bound,")
print("      which tends to (1 - delta) k as the ladder grows: the limit D -> infinity of (b')(i) is a ladder of depths")

# the Gaussian-prior arithmetic quoted in (b')(ii)(1): average failure Phi(-a)^2/2, early stop Phi(-a): count 2 - sqrt(2 delta)
for delta in (0.05, 0.01):
    cnt = 2 - math.sqrt(2 * delta)
    check(cnt < 2 * (1 - delta), "Gaussian-prior count below the instance-wise bound")
    print(f"PART D  (b')(ii)(1) arithmetic: delta = {delta}: average count under the Gaussian prior 2 - sqrt(2 delta) = {cnt:.4f} < 2(1 - delta) = {2 * (1 - delta):.4f}")

print("ALL CHECKS PASSED" if ok_all else "SOME CHECK FAILED")
print(f"seconds {time.time() - t0:.1f}")
print("peak RSS MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
