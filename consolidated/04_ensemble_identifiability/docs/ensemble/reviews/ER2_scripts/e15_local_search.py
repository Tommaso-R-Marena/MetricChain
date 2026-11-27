#!/usr/bin/env python3
"""ER2: E15 and E15T on 5 and 6 sites (32 and 64 states) and on larger mixed alphabets, where the exact
maximisation over all subsets is out of reach: adversarial local search.

max over the class of  TV(mu, mu*) - L(mu)  =  max over (S, mu) of  mu(S) - mu*(S) - L(mu),  convex in mu.
Alternate:  S <- {mu > mu*}  (best subset for the current mu),  mu <- LP optimum for the current S;  the value
increases until a vertex that is a local maximum.  Starts: random subsets and random LP vertices.
(For 3 and 4 sites the exact maxima are in e15_union_bound.py and e15t_interacting.py.)
"""
import itertools, sys, time
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(1505)


def climb(R, N, mustar, lin, const, starts):
    A_eq = np.ones((1, N)); bounds = [(0, None)] * N; b_ub = np.zeros(len(R))
    best = -np.inf
    for s in range(starts):
        if s % 2 == 0:
            ind = (rng.random(N) < rng.uniform(0.2, 0.8)).astype(float)
        else:
            mu = linprog(rng.normal(size=N), A_ub=R, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0], bounds=bounds, method="highs").x
            ind = (mu > mustar).astype(float)
        val = -np.inf
        for _ in range(60):
            res = linprog(-(ind + lin), A_ub=R, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0], bounds=bounds, method="highs")
            mu = res.x
            new = 0.5 * np.abs(mu - mustar).sum() + lin @ mu - const
            if new <= val + 1e-13:
                break
            val = new; ind = (mu > mustar).astype(float)
        best = max(best, val)
    return best


def product_case(sizes, binary_form):
    n = len(sizes)
    states = list(itertools.product(*[range(q) for q in sizes])); N = len(states); index = {s: k for k, s in enumerate(states)}
    deltas = []
    for q in sizes:
        p = np.sort(rng.random(q)) * rng.uniform(0.4, 2.5); D = np.abs(p[:, None] - p[None, :])
        if q > 2 and rng.random() < 0.5:                       # a non-line metric
            D = rng.uniform(0.3, 1.0, size=(q, q)) * 2; D = (D + D.T) / 2; np.fill_diagonal(D, 0)
            for k in range(q):
                D = np.minimum(D, D[:, [k]] + D[[k], :])
        deltas.append(D)
    pis = [rng.dirichlet(np.ones(q) * 3) for q in sizes]
    pi = np.array([np.prod([pis[i][s[i]] for i in range(n)]) for s in states])
    rows = []
    for k, s in enumerate(states):
        for i in range(n):
            for t in range(sizes[i]):
                if t != s[i]:
                    y = list(s); y[i] = t; ky = index[tuple(y)]
                    r = np.zeros(N); r[ky] = 1.0 / pi[ky]; r[k] = -np.exp(deltas[i][s[i], t]) / pi[k]; rows.append(r)
    R = np.array(rows)
    a = tuple(int(rng.integers(q)) for q in sizes)
    sl = [pis[i] * np.exp(-deltas[i][a[i]]) for i in range(n)]; sl = [v / v.sum() for v in sl]
    mustar = np.array([np.prod([sl[i][s[i]] for i in range(n)]) for s in states])
    sig = np.array([sl[i][a[i]] for i in range(n)])
    M = np.array([[1.0 if s[i] == a[i] else 0.0 for s in states] for i in range(n)])
    if binary_form:
        return R, N, mustar, M.sum(axis=0), sig.sum()                       # (c): TV - sum (sigma_i - mu_i)
    return R, N, mustar, (M / sig[:, None]).sum(axis=0), float(n)           # (b): TV - sum (1 - mu_i / sigma_i)


def ising_case(n, graph, violate=False):
    E = np.array(list(itertools.product((0, 1), repeat=n))); N = len(E); index = {tuple(e): k for k, e in enumerate(E)}
    K = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            if graph == "complete" or (graph == "chain" and j == i + 1) or (graph == "ring" and (j == i + 1 or (i == 0 and j == n - 1))):
                K[i, j] = abs(rng.normal()) * (1.2 if graph != "complete" else 0.6)
    if violate:
        K[0, 1] = -K[0, 1] - 0.3                               # the centre violates the first bond
    th = rng.normal(size=n); bs = rng.uniform(0.3, 2.2, size=n)
    lp = np.array([e @ K @ e + th @ e for e in E]); pi = np.exp(lp - lp.max()); pi /= pi.sum()
    rows = []
    for k, e in enumerate(E):
        for i in range(n):
            y = e.copy(); y[i] = 1 - y[i]; ky = index[tuple(y)]
            r = np.zeros(N); r[ky] = 1.0 / pi[ky]; r[k] = -np.exp(bs[i]) / pi[k]; rows.append(r)
    R = np.array(rows)
    mustar = pi * np.exp(-(E @ bs)); mustar /= mustar.sum()
    agree = (1 - E).astype(float)
    return R, N, mustar, agree.sum(axis=1), (agree.T @ mustar).sum()


def main():
    t0 = time.time(); worst = {}
    plan = [("E15(c): binary product, 5 sites", lambda: product_case([2] * 5, True), 6, 40),
            ("E15(c): binary product, 6 sites", lambda: product_case([2] * 6, True), 3, 24),
            ("E15(b): alphabets (3,3,3)", lambda: product_case([3, 3, 3], False), 4, 40),
            ("E15(b): alphabets (2,3,2,3)", lambda: product_case([2, 3, 2, 3], False), 3, 30),
            ("E15(b): alphabets (4,4,3)", lambda: product_case([4, 4, 3], False), 3, 24),
            ("E15T(a): Ising chain, 5 sites, bonds satisfied", lambda: ising_case(5, "chain"), 4, 40),
            ("E15T(a): Ising ring, 6 sites, bonds satisfied", lambda: ising_case(6, "ring"), 3, 24),
            ("E15T(a): complete graph, 5 sites, bonds satisfied", lambda: ising_case(5, "complete"), 4, 40),
            ("E15T(a): complete graph, 6 sites, bonds satisfied", lambda: ising_case(6, "complete"), 3, 24)]
    for label, make, reps, starts in plan:
        w = -np.inf
        for _ in range(reps):
            R, N, mustar, lin, const = make()
            w = max(w, climb(R, N, mustar, lin, const, starts))
        print(f"  {label}: {reps} instances x {starts} starts: largest local maximum of the excess = {w:+.2e}   [{time.time() - t0:.0f} s]", flush=True)
        worst[label] = w
    print("LOCAL SEARCH: NO COUNTEREXAMPLE" if max(worst.values()) < 1e-8 else "LOCAL SEARCH: POSITIVE EXCESS FOUND")
    # control: does the search find a positive excess where one exists?  chains of 5 sites with the first bond violated
    found = []
    for _ in range(4):
        R, N, mustar, lin, const = ising_case(5, "chain", violate=True)
        found.append(climb(R, N, mustar, lin, const, 40))
    print("  control (Ising chain, 5 sites, first bond violated by the centre): largest excess found = " + ", ".join(f"{v:+.3f}" for v in found))


if __name__ == "__main__":
    main()
