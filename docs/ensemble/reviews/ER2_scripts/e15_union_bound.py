#!/usr/bin/env python3
"""ER2: attack on Theorem E15 (thermal union bound, product reference, site-additive envelope).

Every maximum below is EXACT up to LP tolerances: max over the class polytope of TV(mu, mu*) - L(mu), with L
linear, is max over all subsets S of the state space of an LP (TV = max_S mu(S) - mu*(S)).

T1  binary sites, heterogeneous slopes b_i, non-uniform product reference: (a), (c), equality cases.
T2  general alphabets (2..4 letters, mixed), random site metrics: (a), (b); the (c)-form for non-binary
    sites (not claimed by the report; is it true?); the best constant in (b).
T3  non-symmetric site envelopes: the report's mu* (built from delta_i(a_i, s)) against the member built
    from delta_i(s, a_i).
T4  edge cases: one site, a one-letter site, a zero slope, zero entries (pseudo-metric), large slopes, ties.
T5  (d): cube, uniform reference: identified by one-body data inside the class <=> at most one unsaturated
    marginal; vertices of the class polytope by brute force (n = 2, 3), LP vertices (n = 4).
"""
import itertools, sys, time
import numpy as np
from scipy.optimize import linprog
from er2_common import product_states, shortest_path_closure, vertices_bruteforce, vertices_bruteforce_fast

rng = np.random.default_rng(1502)


def build(sizes, deltas, pis):
    states = product_states(sizes); N = len(states); index = {s: k for k, s in enumerate(states)}
    pi = np.array([np.prod([pis[i][s[i]] for i in range(len(sizes))]) for s in states])
    rows = []; pairs = []
    for k, s in enumerate(states):
        for i in range(len(sizes)):
            for t in range(sizes[i]):
                if t == s[i]:
                    continue
                y = list(s); y[i] = t; ky = index[tuple(y)]
                r = np.zeros(N); r[ky] = 1.0 / pi[ky]; r[k] = -np.exp(deltas[i][s[i], t]) / pi[k]
                rows.append(r); pairs.append((k, ky))
    return states, pi, np.array(rows).reshape(-1, N), pairs


def star(sizes, deltas, pis, a, convention="report"):
    """Site laws of the 'most polarised member'.  report: prop. to pi_i(s) exp(-delta_i(a_i, s));
    to_centre: prop. to pi_i(s) exp(-delta_i(s, a_i)).  The two coincide for symmetric delta_i."""
    out = []
    for i in range(len(sizes)):
        e = deltas[i][a[i], :] if convention == "report" else deltas[i][:, a[i]]
        v = pis[i] * np.exp(-e); out.append(v / v.sum())
    return out


def product_of(site_laws, states):
    return np.array([np.prod([site_laws[i][s[i]] for i in range(len(site_laws))]) for s in states])


def in_class(mu, R, tol=1e-10):
    return (R @ mu).max() <= tol


def exact_max(R, N, mustar, lin, const):
    best = -np.inf; arg = None
    A_eq = np.ones((1, N)); bounds = [(0, None)] * N; b_ub = np.zeros(len(R))
    for mask in range(1 << N):
        ind = np.array([(mask >> k) & 1 for k in range(N)], dtype=float)
        res = linprog(-(ind + lin), A_ub=R, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0], bounds=bounds, method="highs")
        if res.status != 0:
            raise RuntimeError("LP failed")
        val = -res.fun - ind @ mustar - const
        if val > best:
            best = val; arg = res.x.copy()
    return best, arg


def marg_rows(states, a):
    return np.array([[1.0 if s[i] == a[i] else 0.0 for s in states] for i in range(len(a))])


def max_marginal(R, N, row):
    res = linprog(-row, A_ub=R, b_ub=np.zeros(len(R)), A_eq=np.ones((1, N)), b_eq=[1.0],
                  bounds=[(0, None)] * N, method="highs")
    return -res.fun


def run_case(sizes, deltas, pis, a, convention="report", want=("b",)):
    states, pi, R, _ = build(sizes, deltas, pis); N = len(states)
    sl = star(sizes, deltas, pis, a, convention); mustar = product_of(sl, states)
    sig = np.array([sl[i][a[i]] for i in range(len(sizes))])
    M = marg_rows(states, a)
    out = {"member": in_class(mustar, R), "N": N}
    out["a_excess"] = max(max_marginal(R, N, M[i]) - sig[i] for i in range(len(sizes)))
    if "b" in want:      # TV - sum_i (1 - mu_i(a_i)/sigma_i)
        out["b_excess"], _ = exact_max(R, N, mustar, (M / sig[:, None]).sum(axis=0), len(sizes))
    if "c" in want:      # TV - sum_i (sigma_i - mu_i(a_i))
        out["c_excess"], out["c_arg"] = exact_max(R, N, mustar, M.sum(axis=0), sig.sum())
    return out, (states, pi, R, mustar, sig, M)


def random_metric(q, scale):
    p = np.sort(rng.random(q)) * scale
    return np.abs(p[:, None] - p[None, :])


def random_metric_general(q, scale):
    D = rng.uniform(0.2, 1.0, size=(q, q)) * scale; D = (D + D.T) / 2; np.fill_diagonal(D, 0)
    return shortest_path_closure(D)


def T1():
    print("T1  binary sites, heterogeneous slopes, non-uniform product reference (exact)")
    worst_a = worst_c = -np.inf; lowest_c = np.inf; eq_gap = 0.0; cnt = 0
    for n, reps in ((1, 20), (2, 40), (3, 25), (4, 2)):
        for _ in range(reps):
            sizes = [2] * n
            bs = rng.uniform(0.05, 3.0, size=n)
            deltas = [np.array([[0, b], [b, 0.0]]) for b in bs]
            pis = [rng.dirichlet(np.ones(2) * rng.uniform(0.5, 4)) for _ in range(n)]
            a = tuple(rng.integers(2, size=n))
            out, (states, pi, R, mustar, sig, M) = run_case(sizes, deltas, pis, a, want=("c",))
            assert out["member"]
            worst_a = max(worst_a, out["a_excess"]); worst_c = max(worst_c, out["c_excess"])
            lowest_c = min(lowest_c, out["c_excess"]); cnt += 1
            # equality for mu = mu*_{a'} with a' one flip away
            for j in range(n):
                a2 = list(a); a2[j] = 1 - a2[j]
                mu = product_of(star(sizes, deltas, pis, tuple(a2)), states)
                assert in_class(mu, R)
                tv = 0.5 * np.abs(mu - mustar).sum(); rhs = (sig - M @ mu).sum()
                eq_gap = max(eq_gap, abs(tv - rhs))
    print(f"    {cnt} instances (n = 1..4): max over the class of TV - sum_i [sigma_i - mu_i(a_i)]: largest {worst_c:+.2e}, smallest {lowest_c:+.2e}")
    print(f"    (a): largest of max_mu mu_i(a_i) - sigma_i = {worst_a:+.2e};  equality at mu*_(a'), a' one flip from a: largest |TV - rhs| = {eq_gap:.2e}")
    return worst_c < 1e-8 and worst_a < 1e-8 and eq_gap < 1e-10


def best_constant_b(sizes, deltas, pis, a):
    states, pi, R, _ = build(sizes, deltas, pis); N = len(states)
    sl = star(sizes, deltas, pis, a); mustar = product_of(sl, states)
    sig = np.array([sl[i][a[i]] for i in range(len(sizes))]); M = marg_rows(states, a)
    lo, hi = 0.0, 1.0
    for _ in range(22):
        c = 0.5 * (lo + hi)
        val, _ = exact_max(R, N, mustar, c * (M / sig[:, None]).sum(axis=0), c * len(sizes))
        if val > 1e-9:
            lo = c
        else:
            hi = c
    return hi, sig


def T2():
    print("T2  general alphabets, random symmetric site metrics, non-uniform product reference (exact)")
    worst_a = worst_b = -np.inf; cnt = 0; cform = []
    shapes = [(3,), (4,), (2, 3), (3, 2), (3, 3), (2, 4), (2, 2, 3), (3, 2, 2), (2, 3, 2)]
    for sizes in shapes:
        for rep in range(4 if np.prod(sizes) <= 9 else 2):
            n = len(sizes)
            gen = random_metric if rep % 2 == 0 else random_metric_general
            deltas = [gen(q, rng.uniform(0.5, 2.5)) for q in sizes]
            pis = [rng.dirichlet(np.ones(q) * 3) for q in sizes]
            a = tuple(int(rng.integers(q)) for q in sizes)
            out, _ = run_case(list(sizes), deltas, pis, a, want=("b", "c"))
            assert out["member"]
            worst_a = max(worst_a, out["a_excess"]); worst_b = max(worst_b, out["b_excess"]); cnt += 1
            cform.append(out["c_excess"])
    print(f"    {cnt} instances with 3..12 states: max over the class of TV - sum_i [1 - mu_i(a_i)/sigma_i]: largest {worst_b:+.2e}")
    print(f"    (a): largest of max_mu mu_i(a_i) - sigma_i = {worst_a:+.2e}")
    print(f"    the (c)-form TV - sum_i [sigma_i - mu_i(a_i)] for NON-binary sites (not claimed): max over the class ranges from "
          f"{min(cform):+.3f} to {max(cform):+.3f}; positive in {sum(c > 1e-6 for c in cform)}/{len(cform)} instances")
    # explicit one-site three-letter example for the failure of the (c)-form
    sizes = [3]; deltas = [np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0.0]])]; pis = [np.full(3, 1 / 3)]
    out, (states, pi, R, mustar, sig, M) = run_case(sizes, deltas, pis, (0,), want=("b", "c"))
    print(f"    one site, three letters, uniform reference, discrete metric (delta = 1), a = 0: sigma = {sig[0]:.4f}; "
          f"max (b)-excess = {out['b_excess']:+.2e}; max (c)-form excess = {out['c_excess']:+.4f} at mu = {np.round(out['c_arg'], 4)}")
    # best constants
    for sizes, label in (((2, 2), "two binary sites"), ((3,), "one ternary site"), ((3, 3), "two ternary sites"), ((2, 3), "binary x ternary")):
        deltas = [random_metric_general(q, 1.5) for q in sizes]
        pis = [rng.dirichlet(np.ones(q) * 3) for q in sizes]
        a = tuple(int(rng.integers(q)) for q in sizes)
        c, sig = best_constant_b(list(sizes), deltas, pis, a)
        print(f"    best constant c in TV <= c * sum_i [1 - mu_i(a_i)/sigma_i], {label}: {c:.4f}  (sigma_i = {np.round(sig, 4)})")
    return worst_b < 1e-8 and worst_a < 1e-8


def T3():
    print("T3  NON-symmetric site envelopes (the theorem assumes symmetry: is it needed?)")
    res = {"report": dict(member=0, a=-np.inf, b=-np.inf), "to_centre": dict(member=0, a=-np.inf, b=-np.inf)}
    cnt = 0; first = None
    for sizes in ((2,), (2, 2), (3,), (2, 3), (3, 3), (2, 2, 2)):
        for rep in range(5):
            deltas = []
            for q in sizes:
                D = shortest_path_closure(rng.uniform(0.1, 2.5, size=(q, q)))
                deltas.append(D)
            pis = [rng.dirichlet(np.ones(q) * 3) for q in sizes]
            a = tuple(int(rng.integers(q)) for q in sizes)
            cnt += 1
            for conv in ("report", "to_centre"):
                out, _ = run_case(list(sizes), deltas, pis, a, convention=conv, want=("b",))
                res[conv]["member"] += out["member"]
                res[conv]["a"] = max(res[conv]["a"], out["a_excess"])
                res[conv]["b"] = max(res[conv]["b"], out["b_excess"])
                if conv == "report" and first is None and (not out["member"] or out["a_excess"] > 1e-6):
                    first = (sizes, deltas, pis, a, out)
    for conv, label in (("report", "mu* from delta_i(a_i, s) (as written in the report)"),
                        ("to_centre", "mu* from delta_i(s, a_i)")):
        r = res[conv]
        print(f"    {label}: member of the class in {r['member']}/{cnt}; largest (a)-excess {r['a']:+.3e}; largest (b)-excess {r['b']:+.3e}")
    # an explicit binary example
    b_up, b_down = 2.0, 0.5       # delta(0,1) = 2 (bound on log w(1)/w(0)), delta(1,0) = 0.5
    deltas = [np.array([[0, b_up], [b_down, 0.0]])]; pis = [np.array([0.5, 0.5])]
    for conv in ("report", "to_centre"):
        out, (states, pi, R, mustar, sig, M) = run_case([2], deltas, pis, (0,), convention=conv, want=("b",))
        print(f"    one binary site, delta(0,1) = 2, delta(1,0) = 0.5, a = 0, {conv}: mu*(a) = {sig[0]:.4f}, member = {out['member']}, "
              f"max_mu mu(a) = {sig[0] + out['a_excess']:.4f}")
    return res["to_centre"]["member"] == cnt and res["to_centre"]["a"] < 1e-8 and res["to_centre"]["b"] < 1e-8


def T4():
    print("T4  edge cases (exact)")
    ok = True
    cases = []
    cases.append(("one binary site, b = 0", [2], [np.zeros((2, 2))], (1,)))
    cases.append(("one binary site, b = 30", [2], [np.array([[0, 30.0], [30.0, 0]])], (0,)))
    cases.append(("binary x one-letter site", [2, 1], [np.array([[0, 1.0], [1.0, 0]]), np.zeros((1, 1))], (0, 0)))
    cases.append(("three binary sites, slopes (0, 1, 12)", [2, 2, 2],
                  [np.zeros((2, 2)), np.array([[0, 1.0], [1.0, 0]]), np.array([[0, 12.0], [12.0, 0]])], (1, 0, 1)))
    Dz = np.array([[0, 0, 1.0], [0, 0, 1.0], [1.0, 1.0, 0]])                 # pseudo-metric: letters 0 and 1 tied
    cases.append(("ternary site with a zero distance (pseudo-metric) x binary", [3, 2], [Dz, np.array([[0, 0.7], [0.7, 0]])], (0, 1)))
    cases.append(("the same, centre at the far letter", [3, 2], [Dz, np.array([[0, 0.7], [0.7, 0]])], (2, 0)))
    Dt = np.array([[0, 1.0, 1.0, 2.0], [1.0, 0, 2.0, 1.0], [1.0, 2.0, 0, 1.0], [2.0, 1.0, 1.0, 0]])  # 4-cycle metric, ties
    cases.append(("four-letter site (4-cycle metric, ties) x binary", [4, 2], [Dt, np.array([[0, 1.0], [1.0, 0]])], (0, 0)))
    for label, sizes, deltas, a in cases:
        pis = [np.full(q, 1.0 / q) for q in sizes]
        binary = all(q <= 2 for q in sizes)
        out, _ = run_case(sizes, deltas, pis, a, want=("b", "c") if binary else ("b",))
        line = f"    {label}: member {out['member']}; (a)-excess {out['a_excess']:+.1e}; (b)-excess {out['b_excess']:+.1e}"
        if binary:
            line += f"; (c)-excess {out['c_excess']:+.1e}"
            ok &= out["c_excess"] < 1e-7
        print(line)
        ok &= out["member"] and out["a_excess"] < 1e-7 and out["b_excess"] < 1e-7
    # the limit b -> infinity: the union bound over the whole simplex (no class constraint), mu* = delta_a
    n = 3; states = product_states([2] * n); N = len(states)
    worst = -np.inf
    for mask in range(1 << N):
        ind = np.array([(mask >> k) & 1 for k in range(N)], dtype=float)
        # maximise mu(S) - 1[a in S] - sum_i mu(x_i != a_i), a = 0...0 ; linear over the simplex: max over point masses
        vals = ind - ind[0] - np.array([sum(s) for s in states])
        worst = max(worst, vals.max())
    print(f"    b = infinity (simplex, mu* = delta_a, n = 3): max of TV(mu, delta_a) - sum_i mu(x_i != a_i) = {worst:+.1f}")
    return ok and worst <= 1e-12


def cube_states(n):
    return np.array(list(itertools.product((-1, 1), repeat=n)))


def cube_rows(n, b):
    X = cube_states(n); N = len(X); index = {tuple(x): k for k, x in enumerate(X)}
    rows = []; pairs = []
    for k, x in enumerate(X):
        for i in range(n):
            y = x.copy(); y[i] = -y[i]; ky = index[tuple(y)]
            r = np.zeros(N); r[ky] = 1.0; r[k] = -np.exp(b); rows.append(r); pairs.append((k, ky))
    return X, np.array(rows), pairs


def fibre_point(mu, R, onebody, tol=1e-7):
    N = len(mu); A_eq = np.vstack([np.ones((1, N)), onebody]); b_eq = A_eq @ mu
    for k in range(N):
        for sgn in (1.0, -1.0):
            c = np.zeros(N); c[k] = -sgn
            res = linprog(c, A_ub=R, b_ub=np.zeros(len(R)), A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * N, method="highs")
            if res.status != 0:
                raise RuntimeError("fibre LP failed")
            if abs(-res.fun * sgn - mu[k]) > tol:
                return False
    return True


def T5():
    print("T5  (d): identified by one-body marginals inside the cube class <=> at most one unsaturated marginal")
    ok = True
    for n, b in ((2, 0.3), (2, 1.0), (2, 2.5), (3, 0.4), (3, 1.0), (3, 2.0), (4, 1.0)):
        X, R, pairs = cube_rows(n, b); N = len(X); th = np.tanh(b / 2)
        onebody = X.T.astype(float)
        if n <= 3:
            d = b * (X[:, None, :] != X[None, :, :]).sum(axis=2).astype(float)
            V = vertices_bruteforce_fast(np.full(N, 1.0 / N), d, pairs=pairs)
            src = f"{len(V)} vertices (brute force over bases)"
        else:
            vs = {}
            for _ in range(250):
                res = linprog(rng.normal(size=N), A_ub=R, b_ub=np.zeros(len(R)), A_eq=np.ones((1, N)), b_eq=[1.0],
                              bounds=[(0, None)] * N, method="highs")
                vs.setdefault(tuple(np.round(res.x, 9)), res.x)
            V = np.array(list(vs.values())); src = f"{len(V)} distinct LP vertices"
        pts = [("vertex", v) for v in V]
        pair_idx = list(itertools.combinations(range(len(V)), 2))
        sel = pair_idx if len(pair_idx) <= 400 else [pair_idx[k] for k in rng.choice(len(pair_idx), size=400, replace=False)]
        pts += [("mid", 0.5 * (V[i] + V[j])) for i, j in sel]
        for _ in range(150):
            k = int(rng.integers(2, 5)); s = rng.choice(len(V), size=min(k, len(V)), replace=False)
            pts.append(("mix", rng.dirichlet(np.ones(len(s))) @ V[s]))
        # products with k saturated sites, the others free in the open interval
        sig = 1 / (1 + np.exp(-b))
        for _ in range(120):
            k = int(rng.integers(0, n + 1)); sat = rng.permutation(n)[:k]
            p = rng.uniform(1 - sig + 0.02 * (2 * sig - 1), sig - 0.02 * (2 * sig - 1), size=n)
            for i in sat:
                p[i] = sig if rng.random() < 0.5 else 1 - sig
            pts.append(("product", np.prod(np.where(X == 1, p, 1 - p), axis=1)))
        # (saturated sites) x (a correlated vertex of the class on the remaining sites)
        if n >= 3:
            X2, R2, _ = cube_rows(n - 1, b)
            for _ in range(60):
                res = linprog(rng.normal(size=len(X2)), A_ub=R2, b_ub=np.zeros(len(R2)), A_eq=np.ones((1, len(X2))),
                              b_eq=[1.0], bounds=[(0, None)] * len(X2), method="highs")
                m = res.x; s0 = sig if rng.random() < 0.5 else 1 - sig
                site = int(rng.integers(n)); rest = [j for j in range(n) if j != site]
                idx2 = {tuple(x): k for k, x in enumerate(X2)}
                mu = np.array([(s0 if x[site] == 1 else 1 - s0) * m[idx2[tuple(x[rest])]] for x in X])
                pts.append(("sat x vertex", mu))
        agree = 0; tot = 0; ident = 0; table = {}; nonproduct_identified = 0
        for tag, mu in pts:
            if (R @ mu).max() > 1e-9:
                continue
            ex = onebody @ mu
            unsat = int(np.sum(np.abs(np.abs(ex) - th) > 1e-8))
            direct = fibre_point(mu, R, onebody)
            tot += 1; agree += (direct == (unsat <= 1)); ident += direct
            table[(tag, unsat)] = table.get((tag, unsat), 0) + 1
            if direct:
                p1 = (1 + ex) / 2
                prod = np.prod(np.where(X == 1, p1, 1 - p1), axis=1)
                nonproduct_identified += np.abs(prod - mu).max() > 1e-8
        print(f"    n = {n}, b = {b}: {src}; {tot} members tested; identified {ident}; criterion agrees in {agree}/{tot}; "
              f"identified members that are not product measures: {nonproduct_identified}")
        print(f"        members by (kind, number of unsaturated marginals): {dict(sorted(table.items()))}")
        ok &= agree == tot
    return ok


def main():
    t0 = time.time(); allok = True
    sel = sys.argv[1:]
    for fn in (T1, T2, T3, T4, T5):
        if sel and fn.__name__ not in sel:
            continue
        ok = fn(); allok &= ok
        print(f"    -> {'no counterexample' if ok else 'COUNTEREXAMPLE / FAILURE'}   [{time.time() - t0:.0f} s]", flush=True)
    if not sel:
        print("E15: NO COUNTEREXAMPLE to the statements as written (symmetric site metrics)" if allok else "E15: SEE FAILURES ABOVE")


if __name__ == "__main__":
    main()
