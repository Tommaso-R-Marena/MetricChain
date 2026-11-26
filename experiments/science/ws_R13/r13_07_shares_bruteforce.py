#!/usr/bin/env python3
"""R13 / item 2, Propositions 11.18b(e), 11.18c(a) and StateShares.lean: brute force of the three explicit instances of the
theory report at 63e36f7, and an own random test of "state-dependent shares exist  <=>  the reference solves the pairwise
(local-polytope) linear relaxation".  Own code; exact rational arithmetic (fractions) for the three instances, scipy/HiGHS
for the linear programmes.  Nothing of the theory division's harness is imported.

Notation.  Sites i with states {0 = reference, 1, ...}.  Lower model relative to the reference:
    L(x) - L(x0) = sum_{i changed} A_i(x_i) + sum_{i<j both changed} [T_ij(x_i, x_j) - c_ij].
State shares: s_ij(a) >= 0, s_ij(a) + s_ji(b) >= c_ij - T_ij(a,b) (a, b changed), sum_{j != i} s_ij(a) <= A_i(a).
Constant shares of deficits: w_ij = max_{a,b}[c_ij - T_ij(a,b)]_+ <= s_ij + s_ji, sum_j s_ij <= Delta_i = min_a A_i(a).

(I)   the "explicit integrality gap" of 11.18b(e): three binary sites, A = (1,1,1), c12 = c13 = 2, T23 = 10
      (c23 = 0 and T12 = T13 = 0 are my reading of the text; both readings c23 in {0, 2} are run).
(II)  the Lean witness (stateShareModel): two sites, three states, A = (1, 10), c12 = 3, T12(1,1) = 2.
(III) the counter-example to completeness on a reset-closed domain, 11.18c(a) (ours, SCI-REV-0012 sec. 3):
      two sites, states {0,1,2}, D = product minus (1,1), A = (1, 10), zero star data, c12 = 3.
(IV)  random instances: equivalence of the two linear programmes; integrality gaps counted.
"""
import itertools, random
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog


def model_values(k, A, c, T):
    """dict config -> L(x) - L(x0), exact.  k[i] = number of states of site i; A[i][a]; c[(i,j)]; T[(i,j)][a][b] (i<j)."""
    n = len(k)
    out = {}
    for x in itertools.product(*[range(ki) for ki in k]):
        v = Fr(0)
        for i in range(n):
            if x[i]:
                v += A[i][x[i]]
        for i in range(n):
            for j in range(i + 1, n):
                if x[i] and x[j]:
                    v += T[(i, j)][x[i]][x[j]] - c[(i, j)]
        out[x] = v
    return out


def lp_relaxation(k, A, c, T):
    """minimum of the local-polytope relaxation (float, HiGHS); returns (value, solution dict)."""
    n = len(k)
    idx = {}
    for i in range(n):
        for a in range(k[i]):
            idx[('s', i, a)] = len(idx)
    for i in range(n):
        for j in range(i + 1, n):
            for a in range(k[i]):
                for b in range(k[j]):
                    idx[('p', i, j, a, b)] = len(idx)
    N = len(idx)
    cost = np.zeros(N)
    for i in range(n):
        for a in range(1, k[i]):
            cost[idx[('s', i, a)]] = float(A[i][a])
    for i in range(n):
        for j in range(i + 1, n):
            for a in range(1, k[i]):
                for b in range(1, k[j]):
                    cost[idx[('p', i, j, a, b)]] = float(T[(i, j)][a][b] - c[(i, j)])
    Aeq, beq = [], []
    for i in range(n):
        row = np.zeros(N)
        for a in range(k[i]):
            row[idx[('s', i, a)]] = 1
        Aeq.append(row); beq.append(1.0)
    for i in range(n):
        for j in range(i + 1, n):
            for a in range(k[i]):
                row = np.zeros(N)
                for b in range(k[j]):
                    row[idx[('p', i, j, a, b)]] = 1
                row[idx[('s', i, a)]] = -1
                Aeq.append(row); beq.append(0.0)
            for b in range(k[j]):
                row = np.zeros(N)
                for a in range(k[i]):
                    row[idx[('p', i, j, a, b)]] = 1
                row[idx[('s', j, b)]] = -1
                Aeq.append(row); beq.append(0.0)
    res = linprog(cost, A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=[(0, None)] * N, method='highs')
    assert res.status == 0
    return res.fun, {key: res.x[v] for key, v in idx.items()}


def state_shares_feasible(k, A, c, T, slack=False):
    """LP feasibility of state-dependent shares (float, HiGHS).  With slack=True: returns the largest uniform margin
    m such that the cover holds with '>= c - T + m' (m >= 0 <=> feasible), which is robust to rounding."""
    n = len(k)
    idx = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                for a in range(1, k[i]):
                    idx[(i, j, a)] = len(idx)
    N = len(idx) + 1                      # last variable: margin m
    Aub, bub = [], []
    for i in range(n):
        for j in range(i + 1, n):
            for a in range(1, k[i]):
                for b in range(1, k[j]):
                    row = np.zeros(N)
                    row[idx[(i, j, a)]] = -1
                    row[idx[(j, i, b)]] = -1
                    row[-1] = 1
                    Aub.append(row); bub.append(-float(c[(i, j)] - T[(i, j)][a][b]))
    for i in range(n):
        for a in range(1, k[i]):
            row = np.zeros(N)
            for j in range(n):
                if j != i:
                    row[idx[(i, j, a)]] = 1
            Aub.append(row); bub.append(float(A[i][a]))
    cost = np.zeros(N); cost[-1] = -1.0
    bounds = [(0, None)] * (N - 1) + [(None, 1.0)]
    res = linprog(cost, A_ub=np.array(Aub), b_ub=np.array(bub), bounds=bounds, method='highs')
    if res.status == 2:
        return -np.inf
    assert res.status == 0, res.message
    return res.x[-1]


def const_shares_feasible(k, A, c, T):
    n = len(k)
    w = {}
    for i in range(n):
        for j in range(i + 1, n):
            w[(i, j)] = max([Fr(0)] + [c[(i, j)] - T[(i, j)][a][b] for a in range(1, k[i]) for b in range(1, k[j])])
    Delta = [min(A[i][a] for a in range(1, k[i])) for i in range(n)]
    idx = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                idx[(i, j)] = len(idx)
    N = len(idx) + 1
    Aub, bub = [], []
    for (i, j), wij in w.items():
        row = np.zeros(N); row[idx[(i, j)]] = -1; row[idx[(j, i)]] = -1; row[-1] = 1
        Aub.append(row); bub.append(-float(wij))
    for i in range(n):
        row = np.zeros(N)
        for j in range(n):
            if j != i:
                row[idx[(i, j)]] = 1
        Aub.append(row); bub.append(float(Delta[i]))
    cost = np.zeros(N); cost[-1] = -1.0
    res = linprog(cost, A_ub=np.array(Aub), b_ub=np.array(bub), bounds=[(0, None)] * (N - 1) + [(None, 1.0)], method='highs')
    if res.status == 2:
        return -np.inf, w, Delta
    return res.x[-1], w, Delta


def zeroT(k):
    return {(i, j): [[Fr(0)] * k[j] for _ in range(k[i])] for i in range(len(k)) for j in range(i + 1, len(k))}


if __name__ == '__main__':
    print("# r13_07_shares_bruteforce.py")
    print("## (I) three binary sites, A = (1,1,1), c12 = c13 = 2, T23(1,1) = 10")
    for c23 in (Fr(0), Fr(2)):
        k = [2, 2, 2]
        A = [[Fr(0), Fr(1)]] * 3
        c = {(0, 1): Fr(2), (0, 2): Fr(2), (1, 2): c23}
        T = zeroT(k); T[(1, 2)][1][1] = Fr(10)
        vals = model_values(k, A, c, T)
        print(f"   c23 = {c23}: L(x) - L(x0) over the 8 configurations (changed sites -> value): " +
              ", ".join(f"{''.join(str(i+1) for i in range(3) if x[i]) or '-'}:{v}" for x, v in sorted(vals.items())))
        print(f"      minimum over configurations = {min(vals.values())} (attained at {[x for x, v in vals.items() if v == min(vals.values())]}) -> x0 minimises L: {min(vals.values()) == 0}")
        lpv, sol = lp_relaxation(k, A, c, T)
        print(f"      local-polytope relaxation (HiGHS): value {lpv:.12f};  site marginals of 'changed': "
              f"{[round(sol[('s', i, 1)], 6) for i in range(3)]};  pair marginals of 'both changed' (12, 13, 23): "
              f"{[round(sol[('p', i, j, 1, 1)], 6) for (i, j) in ((0, 1), (0, 2), (1, 2))]}")
        # the fractional point of the text, exactly
        p = [Fr(1, 2)] * 3
        q = {(0, 1): Fr(1, 2), (0, 2): Fr(1, 2), (1, 2): Fr(0)}
        val = sum(A[i][1] * p[i] for i in range(3)) + sum((T[e][1][1] - c[e]) * q[e] for e in q)
        feas = all(max(Fr(0), p[i] + p[j] - 1) <= q[(i, j)] <= min(p[i], p[j]) for (i, j) in q)
        print(f"      the point of the text (every site changed with weight 1/2; 12 and 13 always together, 23 never): locally consistent {feas}, value {val}")
        # exact lower bound of the relaxation: reduce to p's (q12 = min(p1,p2), q13 = min(p1,p3), q23 = max(0,p2+p3-1)) on a rational grid
        best = min((p1 + p2 + p3 - c[(0, 1)] * min(p1, p2) - c[(0, 2)] * min(p1, p3) + (Fr(10) - c23) * max(Fr(0), p2 + p3 - 1), (p1, p2, p3))
                   for p1 in [Fr(i, 20) for i in range(21)] for p2 in [Fr(i, 20) for i in range(21)] for p3 in [Fr(i, 20) for i in range(21)])
        print(f"      exact minimum of the reduced objective on the grid {{0, 1/20, ..., 1}}^3: {best[0]} at p = {tuple(str(v) for v in best[1])}")
        m = state_shares_feasible(k, A, c, T)
        print(f"      state shares: largest uniform cover margin {m:.6f} (feasible iff >= 0): exist = {m >= -1e-9};"
              f"  exact reason: covers of 12 and 13 need s12+s21+s13+s31 >= {c[(0,1)] + c[(0,2)]}, loads allow at most {A[0][1] + A[1][1] + A[2][1]}")
        # no joint distribution has these pair marginals
        ok = False
        for w8 in itertools.product([Fr(0), Fr(1, 2), Fr(1)], repeat=8):
            if sum(w8) != 1:
                continue
            X = list(itertools.product((0, 1), repeat=3))
            if all(sum(wt for x, wt in zip(X, w8) if x[i] and x[j]) == q[(i, j)] for (i, j) in q) and \
               all(sum(wt for x, wt in zip(X, w8) if x[i]) == Fr(1, 2) for i in range(3)):
                ok = True
        print(f"      a joint distribution with weights in {{0, 1/2, 1}} that has these marginals exists: {ok}  "
              f"(in general: x1 = x2 and x1 = x3 almost surely force x2 = x3)")

    print("## (II) the Lean witness: two sites, three states, A = (1, 10) at both, c12 = 3, T12(1,1) = 2")
    k = [3, 3]
    A = [[Fr(0), Fr(1), Fr(10)]] * 2
    c = {(0, 1): Fr(3)}
    T = zeroT(k); T[(0, 1)][1][1] = Fr(2)
    vals = model_values(k, A, c, T)
    print("   L - L(x0): " + ", ".join(f"{x}:{v}" for x, v in sorted(vals.items())) + f";  min = {min(vals.values())}")
    s = {1: Fr(1, 2), 2: Fr(5, 2)}
    cover = all(s[a] + s[b] >= c[(0, 1)] - T[(0, 1)][a][b] for a in (1, 2) for b in (1, 2))
    load = all(s[a] <= A[0][a] for a in (1, 2))
    mconst, w, Delta = const_shares_feasible(k, A, c, T)
    print(f"   shares s(1) = 1/2, s(2) = 5/2: cover {cover}, load {load};  deficit w12 = {w[(0,1)]}, Delta = {Delta}: "
          f"constant shares exist: {w[(0,1)] <= Delta[0] + Delta[1]} (LP margin {mconst:.3f})")
    print(f"   where the deficit is realised: {[(a, b) for a in (1, 2) for b in (1, 2) if c[(0,1)] - T[(0,1)][a][b] == w[(0,1)]]} "
          f"(the pair of cheapest states (1,1) has deficit {c[(0,1)] - T[(0,1)][1][1]})")

    print("## (III) 11.18c(a): D = {0,1,2}^2 minus (1,1); additive known part, A = (1, 10); zero star data; c12 = 3")
    D = [x for x in itertools.product(range(3), repeat=2) if x != (1, 1)]
    # the class on D: g = 0 on the star; |mixed difference| <= 3 over every rectangle {a,a'} x {b,b'} with four corners in D
    inner = [x for x in D if x[0] and x[1]]          # (1,2), (2,1), (2,2)
    rects = []
    for a, a2 in itertools.combinations(range(3), 2):
        for b, b2 in itertools.combinations(range(3), 2):
            corners = [(a, b), (a, b2), (a2, b), (a2, b2)]
            if all(cn in D for cn in corners):
                rects.append(corners)
    print(f"   rectangles inside D: {len(rects)} of 9")
    # least value of g at each inner point over the class: LP in the 3 unknowns g(1,2), g(2,1), g(2,2)
    Aub, bub = [], []
    pos = {x: i for i, x in enumerate(inner)}
    for (p00, p01, p10, p11) in rects:
        row = np.zeros(3)
        for cn, sg in ((p00, 1), (p01, -1), (p10, -1), (p11, 1)):
            if cn in pos:
                row[pos[cn]] += sg
        Aub.append(row); bub.append(3.0)
        Aub.append(-row); bub.append(3.0)
    Aexc = {0: 0, 1: 1, 2: 10}
    least = {}
    for x in inner:
        cost = np.zeros(3); cost[pos[x]] = 1
        res = linprog(cost, A_ub=np.array(Aub), b_ub=np.array(bub), bounds=[(None, None)] * 3, method='highs')
        least[x] = res.fun
    print("   least value over the class of the energy difference to the reference: " +
          ", ".join(f"{x}: {Aexc[x[0]] + Aexc[x[1]]} + ({least[x]:.6f}) = {Aexc[x[0]] + Aexc[x[1]] + least[x]:.6f}" for x in inner) +
          ";  star points: 1, 10, 1, 10")
    print(f"   x0 certified for every member: {all(Aexc[x[0]] + Aexc[x[1]] + least[x] >= 0 for x in inner)};  "
          f"over-dense: c12 = 3 > Delta1 + Delta2 = 2: no shares (constant, additive known part)")

    print("## (IV) random instances: state shares exist <=> the relaxation is solved by the reference")
    random.seed(20261126)
    stats = dict(n=0, shares=0, lp0=0, agree=0, intmin=0, gap=0, const=0, const_not_state=0, ambiguous=0)
    for trial in range(400):
        n = random.choice([2, 3, 3, 4])
        k = [random.choice([2, 3]) for _ in range(n)]
        A = [[Fr(0)] + [Fr(random.randint(0, 40), 10) for _ in range(k[i] - 1)] for i in range(n)]
        c = {(i, j): Fr(random.randint(0, 30), 10) for i in range(n) for j in range(i + 1, n)}
        T = {(i, j): [[Fr(0) if (a == 0 or b == 0) else Fr(random.randint(-20, 20), 10) for b in range(k[j])] for a in range(k[i])]
             for i in range(n) for j in range(i + 1, n)}
        vals = model_values(k, A, c, T)
        intmin = min(vals.values()) == 0
        lpv, _ = lp_relaxation(k, A, c, T)
        m = state_shares_feasible(k, A, c, T)
        mc, _, _ = const_shares_feasible(k, A, c, T)
        if abs(lpv) < 1e-7 and lpv != 0 or abs(m) < 1e-7:
            stats['ambiguous'] += 1          # a tie within rounding; counted separately, not used in the verdict
            continue
        sh, lp0 = m > 0, lpv > -1e-7
        stats['n'] += 1
        stats['shares'] += sh; stats['lp0'] += lp0; stats['agree'] += (sh == lp0); stats['intmin'] += intmin
        stats['gap'] += (intmin and not lp0); stats['const'] += (mc > 1e-9); stats['const_not_state'] += (mc > 1e-9 and not sh)
    print(f"   instances decided (ties within 1e-7 set aside: {stats['ambiguous']}): {stats['n']};  reference minimises the model: {stats['intmin']};  "
          f"relaxation solved by the reference: {stats['lp0']};  state shares exist: {stats['shares']};  the two agree in {stats['agree']} of {stats['n']};  "
          f"integrality gaps (reference optimal, relaxation below): {stats['gap']};  constant shares of deficits: {stats['const']} (of which without state shares: {stats['const_not_state']})")
    print("# END")
