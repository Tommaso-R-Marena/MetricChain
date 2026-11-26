#!/usr/bin/env python3
"""R24, item 2 (i)-(ii) on synthetic classes; the referee's own linear programmes (scipy/HiGHS), no code of the division.

Class on a product space X = prod A_i:  P(pi, d) = { mu : mu(y) pi(x) <= e^{d(x,y)} mu(x) pi(y) for all x != y }.
PART A -- the weakest condition for the Ensemble division's E15 (a), (b).  Claim of the referee: with a PRODUCT reference and
   delta_i(s) := max over the other sites of d( (s, x_-i), (a_i, x_-i) )      (single-site moves INTO the centre state only),
   mu*_{a,i}(s) ~ pi_i(s) e^{-delta_i(s)},  sigma_i = mu*_{a,i}(a_i):   mu(x_i = a_i) <= sigma_i  and  TV(mu, prod_i mu*_{a,i}) <= sum_i [1 - mu(x_i = a_i)/sigma_i]
   for EVERY envelope d -- no symmetry, no triangle inequality, no additivity over the sites (mu* need then not be a member).
   Envelope types: T1 site-additive, one-sided, triangle inequality; T2 site-additive, one-sided, NO triangle inequality;
   T3 arbitrary positive d(x, y) (not site-additive); T4 d = c [x != y].  Control: every delta_i(s) halved (must fail).
PART B -- addendum item 87 (c): the one-body marginal vectors of the class = the product of the one-site classes P(pi_i, delta_i).
   Test by support functions: max over the class of a random linear functional of the marginals (one LP) against the sum of
   the one-site maxima.  Site-additive envelopes with and without symmetry / triangle inequality (claimed: equal).
   Controls that must fail: an envelope that is not site-additive (d = c [x != y], one-site constants c); a reference that is
   not a product (one-site classes built on its marginals).
PART C -- the closed form  b_min = max_i max_{s != t} [ln(mu_i(t) pi_i(s) / (mu_i(s) pi_i(t)))]_+ / delta_i(s, t)  for one-body data
   against the feasibility programme "a member of P(pi, b d) with these one-site marginals exists" at b = 1.03 b_min (must be
   feasible) and b = 0.97 b_min (must be infeasible; the violation planted is 3 % of b_min delta, at least 3e-3 in the
   log-ratio, large against the solver's 1e-7); control: the formula with delta_i(t, s) on one-sided envelopes.
   And the explicit flow certificate of INFERENCE_LIMITS.md, Theorem 8 (c), at b = 0.97 b_min: the inequality at every state.
Run: python3 -B r24_item2_synthetic.py > r24_item2_synthetic.log
"""
import os, sys, math, time, itertools
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r24_common as C


def states(k): return list(itertools.product(*[range(v) for v in k]))


def closure(M):
    M = M.copy(); np.fill_diagonal(M, 0.0)
    for c in range(len(M)): M = np.minimum(M, M[:, [c]] + M[[c], :])
    return M


def site_deltas(k, rng, scale, symmetric, triangle):
    out = []
    for kk in k:
        M = rng.uniform(0.15, 1.2, (kk, kk)) * scale
        if symmetric: M = (M + M.T) / 2
        np.fill_diagonal(M, 0.0); out.append(closure(M) if triangle else M)
    return out


def additive(k, X, deltas):
    return np.array([[sum(deltas[i][x[i], y[i]] for i in range(len(k))) for y in X] for x in X])


def polytope(pi, d):
    N = len(pi); rows = []
    for x in range(N):
        for y in range(N):
            if x != y:
                r = np.zeros(N); r[y] = pi[x]; r[x] = -math.exp(d[x, y]) * pi[y]; rows.append(r)
    return np.array(rows)


def lpmax(c, A, N, Aeq=None, beq=None):
    Ae = np.ones((1, N)) if Aeq is None else np.vstack([np.ones((1, N)), Aeq]); be = [1.0] if beq is None else [1.0] + list(beq)
    r = linprog(-np.asarray(c, float), A_ub=A, b_ub=np.zeros(len(A)), A_eq=Ae, b_eq=be, bounds=[(0, None)] * N, method="highs")
    return (None, None, r.status) if r.status != 0 else (-r.fun, r.x, 0)


def part_a(rng, t0):
    print("=== PART A: E15 (a), (b) with delta_i(s) = the worst single-site cost into the centre state; no other condition on d")
    cases = [((2, 2, 2), "T1"), ((3, 2), "T1"), ((3, 3), "T1"), ((2, 2, 2), "T2"), ((3, 2), "T2"), ((3, 3), "T2"), ((2, 3, 2), "T2"),
             ((2, 2, 2), "T3"), ((3, 2), "T3"), ((3, 3), "T3"), ((2, 3, 2), "T3"), ((2, 2, 2), "T4"), ((3, 3), "T4")]
    worst_a = -1e9; worst_b = -1e9; nlp = 0; notmem = 0; ncen = 0; fail_half = 0; tri_viol = 0
    for k, typ in cases:
        X = states(k); N = len(X); n = len(k); pis = [rng.dirichlet(np.full(kk, 3.0)) for kk in k]
        pi = np.array([math.prod(pis[i][x[i]] for i in range(n)) for x in X])
        if typ in ("T1", "T2"): d = additive(k, X, site_deltas(k, rng, 1.0, False, typ == "T1"))
        elif typ == "T3": d = rng.uniform(0.1, 1.5, (N, N)); np.fill_diagonal(d, 0.0)
        else: d = 0.8 * (1.0 - np.eye(N))
        tri = float((d[:, None, :] - d[:, :, None] - d[None, :, :]).max()); tri_viol += int(tri > 1e-9)
        A = polytope(pi, d); idx = {x: j for j, x in enumerate(X)}
        cen = X if N <= 9 else [X[j] for j in rng.choice(N, size=2, replace=False)]
        wa = -1e9; wb = -1e9; wh = -1e9
        for a in cen:
            ncen += 1
            for half in (False, True):
                dl = [np.array([max(d[idx[x[:i] + (s,) + x[i + 1:]], idx[x[:i] + (a[i],) + x[i + 1:]]] for x in X if x[i] == a[i]) if s != a[i] else 0.0 for s in range(k[i])]) for i in range(n)]
                if half: dl = [0.5 * v for v in dl]
                ms = [pis[i] * np.exp(-dl[i]) for i in range(n)]; ms = [v / v.sum() for v in ms]; sig = [ms[i][a[i]] for i in range(n)]
                mstar = np.array([math.prod(ms[i][x[i]] for i in range(n)) for x in X])
                ind = [np.array([1.0 if x[i] == a[i] else 0.0 for x in X]) for i in range(n)]
                va = max(lpmax(ind[i], A, N)[0] - sig[i] for i in range(n)); nlp += n
                if half: wh = max(wh, va); continue
                notmem += int((A @ mstar > 1e-10).any()); wa = max(wa, va)
                lin = sum(ind[i] / sig[i] for i in range(n))
                for bits in range(1, 2 ** N - 1):
                    iA = np.array([(bits >> j) & 1 for j in range(N)], dtype=float)
                    v, _, _ = lpmax(iA + lin, A, N); nlp += 1; wb = max(wb, v - n - float(iA @ mstar))
        worst_a = max(worst_a, wa); worst_b = max(worst_b, wb); fail_half += int(wh > 1e-6)
        print(f"  {typ} alphabets {k}: {N} states, {len(cen)} centres; triangle inequality of d violated by {max(tri, 0):.2f}; max [p_i - sigma_i] = {wa:+.1e}; max [TV - sum tau] = {wb:+.1e}; "
              f"control (delta halved): max [p_i - sigma_i] = {wh:+.3f} [{time.time() - t0:.0f}s]", flush=True)
    print(f"A   {len(cases)} classes ({tri_viol} of them violate the triangle inequality), {ncen} centres, {nlp} linear programmes: largest p_i - sigma_i = {worst_a:+.1e}, largest TV - sum tau = {worst_b:+.1e} (both must be <= 1e-9); "
          f"the product mu* is NOT a member of the class at {notmem} of {ncen} centres (the bound holds all the same); control, delta halved: (a) fails in {fail_half} of {len(cases)} classes (must be positive)")
    assert worst_a <= 1e-9 and worst_b <= 1e-9 and fail_half > 0


def one_site_max(c, pi_i, delta_i):
    kk = len(pi_i); A = polytope(pi_i, delta_i); v, x, s = lpmax(c, A, kk); return v


def part_b(rng, t0):
    print("=== PART B: item 87 (c) -- marginal vectors of the class = product of the one-site classes (support functions)")
    dev = 0.0; nfun = 0; ctrl_add = 0.0; ctrl_ref = 0.0; cases = [((3, 2), True, True), ((3, 3), True, True), ((2, 2, 2), False, True), ((3, 3), False, True), ((3, 2), False, False), ((3, 3), False, False), ((2, 3, 2), False, False), ((4, 2), False, False)]
    for k, sym, tri in cases:
        X = states(k); N = len(X); n = len(k); pis = [rng.dirichlet(np.full(kk, 3.0)) for kk in k]; pi = np.array([math.prod(pis[i][x[i]] for i in range(n)) for x in X])
        deltas = site_deltas(k, rng, 1.0, sym, tri); d = additive(k, X, deltas); A = polytope(pi, d); dv = 0.0
        for rep in range(20):
            cs = [rng.normal(size=kk) for kk in k]; c = np.array([sum(cs[i][x[i]] for i in range(n)) for x in X])
            v, _, _ = lpmax(c, A, N); v1 = sum(one_site_max(cs[i], pis[i], deltas[i]) for i in range(n)); dv = max(dv, abs(v - v1)); nfun += 1
        dev = max(dev, dv)
        # control 1: not site-additive -- d = c [x != y]; the one-site constants are c
        cc = 0.9; A4 = polytope(pi, cc * (1.0 - np.eye(N))); d1 = [cc * (1.0 - np.eye(kk)) for kk in k]; g1 = 0.0
        # control 2: a reference that is not a product (same site-additive envelope; one-site classes on the marginals of the reference)
        pr = rng.dirichlet(np.full(N, 1.0)); Ar = polytope(pr, d); prm = [np.array([sum(pr[j] for j, x in enumerate(X) if x[i] == s) for s in range(k[i])]) for i in range(n)]; g2 = 0.0
        for rep in range(20):
            cs = [rng.normal(size=kk) for kk in k]; c = np.array([sum(cs[i][x[i]] for i in range(n)) for x in X])
            g1 = max(g1, sum(one_site_max(cs[i], pis[i], d1[i]) for i in range(n)) - lpmax(c, A4, N)[0])
            g2 = max(g2, abs(sum(one_site_max(cs[i], prm[i], deltas[i]) for i in range(n)) - lpmax(c, Ar, N)[0]))
        ctrl_add = max(ctrl_add, g1); ctrl_ref = max(ctrl_ref, g2)
        print(f"  alphabets {k}, {'symmetric' if sym else 'one-sided'}, triangle inequality {'kept' if tri else 'NOT imposed'}: |class maximum - sum of one-site maxima| over 20 functionals: {dv:.1e}; "
              f"control, d = c [x != y]: one-site sum exceeds the class maximum by up to {g1:.3f}; control, non-product reference: differs by up to {g2:.3f} [{time.time() - t0:.0f}s]", flush=True)
    print(f"B   site-additive envelopes, product reference: largest deviation of the support functions over {nfun} functionals in {len(cases)} classes: {dev:.1e} (must be < 1e-8); "
          f"controls: envelope not site-additive: up to {ctrl_add:.3f}; reference not a product: up to {ctrl_ref:.3f} (both must be clearly positive: the statement needs both hypotheses)")
    assert dev < 1e-8 and ctrl_add > 1e-3 and ctrl_ref > 1e-3


def part_c(rng, t0):
    print("=== PART C: the closed form of b_min for one-body data against the feasibility programme; the explicit flow of Theorem 8 (c)")
    ok_hi = 0; ok_lo = 0; tot = 0; ctrl_bad = 0; ctrl_n = 0; flow_ok = 0; flow_ctrl = 0; skipped = 0
    for k, sym, tri in [((3, 2), False, True), ((3, 3), False, True), ((2, 2, 2), False, False), ((3, 3), True, True), ((2, 3, 2), False, False), ((4, 2), False, True)]:
        X = states(k); N = len(X); n = len(k)
        for rep in range(10):
            pis = [rng.dirichlet(np.full(kk, 3.0)) for kk in k]; pi = np.array([math.prod(pis[i][x[i]] for i in range(n)) for x in X])
            deltas = site_deltas(k, rng, 1.0, sym, tri); d = additive(k, X, deltas); A = polytope(pi, d)
            _, mu, _ = lpmax(rng.normal(size=N), A, N)                                   # a member: a vertex of the class at scale 1
            marg = [np.array([sum(mu[j] for j, x in enumerate(X) if x[i] == s) for s in range(k[i])]) for i in range(n)]
            if min(float(v.min()) for v in marg) < 1e-6: skipped += 1; continue

            def bmin(dl):
                best = (0.0, None)
                for i in range(n):
                    for s in range(k[i]):
                        for t in range(k[i]):
                            if s != t:
                                q = max(math.log(marg[i][t] * pis[i][s] / (marg[i][s] * pis[i][t])), 0.0) / dl[i][s, t]
                                if q > best[0]: best = (q, (i, s, t))
                return best
            b0, arg = bmin(deltas)
            if arg is None or b0 * deltas[arg[0]][arg[1], arg[2]] < 0.1: skipped += 1; continue
            Aeq = []; beq = []
            for i in range(n):
                for s in range(k[i] - 1): Aeq.append([1.0 if x[i] == s else 0.0 for x in X]); beq.append(marg[i][s])

            def feasible(b):
                r = linprog(np.zeros(N), A_ub=polytope(pi, b * d), b_ub=np.zeros(N * (N - 1)), A_eq=np.vstack([np.ones((1, N)), np.array(Aeq)]), b_eq=[1.0] + beq, bounds=[(0, None)] * N, method="highs")
                return r.status == 0
            tot += 1; ok_hi += int(feasible(1.03 * b0)); ok_lo += int(not feasible(0.97 * b0))
            if not sym:
                br, _ = bmin([D.T for D in deltas]); ctrl_n += 1; ctrl_bad += int(abs(br - b0) > 0.05 * b0 and (feasible(1.03 * br) != True or feasible(0.97 * br) != False))
            # the explicit flow certificate at b = 0.97 b0 (INFERENCE_LIMITS.md, Theorem 8 (c)): data  E 1[x_i = t] >= p_t,  E 1[x_i = s] <= p_s
            i, s, t = arg; b = 0.97 * b0; e = math.exp(b * deltas[i][s, t]); ps, pt = marg[i][s], marg[i][t]; den = pis[i][s] * pt - e * pis[i][t] * ps
            for bb, counter in ((b, "ok"), (1.03 * b0, "ctrl")):
                e = math.exp(bb * deltas[i][s, t]); den = pis[i][s] * pt - e * pis[i][t] * ps
                if den <= 0:
                    if counter == "ctrl": flow_ctrl += 1                                    # no such certificate above b_min: the construction breaks down
                    continue
                gam = pis[i][t] * e / den; alp = (1 + gam * ps) / pt; theta = pis[i][t] * alp; slack = 1e9
                for z in X:
                    lam = gam * ((1.0 if z[i] == s else 0.0) - ps) - alp * ((1.0 if z[i] == t else 0.0) - pt); piz = math.prod(pis[j][z[j]] for j in range(n)); rest = piz / pis[i][z[i]]
                    rhs = theta * rest if z[i] == t else (-e * theta * rest if z[i] == s else 0.0)      # inflow from (s, z_-i) into (t, z_-i); outflow e^{b delta} F out of (s, z_-i)
                    slack = min(slack, rhs - (1.0 - lam) * piz)
                if counter == "ok": flow_ok += int(slack >= -1e-12)
        print(f"  alphabets {k} ({'symmetric' if sym else 'one-sided'}, triangle {'kept' if tri else 'not imposed'}) done [{time.time() - t0:.0f}s]", flush=True)
    print(f"C   {tot} members (vertices of the class at scale 1; {skipped} skipped: a vanishing marginal or b_min delta < 0.1): a member with the same one-site marginals exists at 1.03 b_min in {ok_hi} of {tot} (must be all) "
          f"and at 0.97 b_min in {tot - ok_lo} of {tot} (must be 0); control, the formula with delta_i(t, s) on one-sided envelopes: contradicted by the programme in {ctrl_bad} of {ctrl_n} cases (must be positive); "
          f"the explicit flow certificate of Theorem 8 (c) at 0.97 b_min satisfies its inequality at every state in {flow_ok} of {tot} cases (must be all); above b_min the construction is impossible in {flow_ctrl} of {tot} (must be all)")
    assert ok_hi == tot and ok_lo == tot and ctrl_bad > 0 and flow_ok == tot and flow_ctrl == tot


def main():
    t0 = time.time(); rng = np.random.default_rng(2402)
    part_a(rng, t0); part_b(rng, t0); part_c(rng, t0)
    print(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {C.rss():.0f} MB")


if __name__ == "__main__":
    main()
