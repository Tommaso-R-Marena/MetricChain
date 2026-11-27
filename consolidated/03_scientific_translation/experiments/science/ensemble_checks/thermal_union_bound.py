#!/usr/bin/env python3
"""The Ensemble division's Theorem E15 (thermal union bound), checked by independent code, and measured on two rotamer
instances of ours -- for their question E-S3 (ENSEMBLE-MSG-0003 at 1a067b5: is the bound of use as a falsification test?).

Their statement (docs/ensemble/ENSEMBLE_REPORT.md at 1a067b5, l.1036-1099; nothing of their code is used here).
X = prod_i A_i finite, pi = prod_i pi_i > 0, d(x, y) = sum_i delta_i(x_i, y_i), every delta_i a metric;
    class  P(pi, d) = { mu : mu(y) pi(x) <= e^{d(x,y)} mu(x) pi(y) for all x, y }      (a polytope in mu);
    mu*_a = prod_i mu*_{a,i},  mu*_{a,i}(s) ~ pi_i(s) e^{-delta_i(a_i, s)}             (the member most polarised towards a).
(a) mu(x_i = a_i) <= sigma_i := mu*_{a,i}(a_i);   (b) TV(mu, mu*_a) <= sum_i tau_i,  tau_i = 1 - mu(x_i = a_i) / sigma_i;
(c) binary sites: TV(mu, mu*_a) <= sum_i [sigma_i - mu(x_i = a_i)], with equality cases.

PART A -- synthetic classes, EXACT maximisation over the class polytope (one linear programme per subset A of X,
TV = max_A [mu(A) - mu*(A)]; scipy/HiGHS):
  A1  max over the class, all centres, of TV - sum tau                         (the theorem: <= 0, and 0 is attained)
  A2  binary sites: max of TV - sum (sigma - p)                                (<= 0, attained)
  A3  ternary sites: max of TV - sum (sigma - p)                               (expected > 0: (c) is for binary sites only)
  A4  the best constant: sup over the class of TV / sum tau (a linear-fractional programme per subset)
  A5  control: constant 1/2 in (c)                                             (must fail)
  A6  ONE-SIDED envelopes (delta_i not symmetric; triangle inequality kept): (a), (b) with the polarised member
      defined by the cost INTO the centre, w*(x) ~ e^{-d(x, a)}                (claimed here: <= 0);
      control: the member defined with d(a, x)                                 (must fail: it need not be a member)
  A7  control: the class of envelope 2 d against the bound computed for d      (must fail)
  A8  one-body data alone: the one-body marginal vectors of the class are exactly the products of the one-site classes
      (proof in SCI-RES-0032); checked: for marginals drawn from the one-site classes a member exists (the product; verified
      to be a member), and with one one-site constraint violated by 0.01 in the log-ratio the feasibility programme is
      infeasible (control: feasible with the unmodified marginals).

PART B -- an instance of ours by enumeration (argument K5 or LKSE:5):  E on all states; reference = the product of the
anchored one-body weights  pi_i(s) ~ exp(-beta [E(x0 with x_i = s) - E(x0)]);  the rest  g = beta (E - first-order
interpolant around the anchor);  envelope = the LEAST site-additive one, exact by enumeration:
   symmetric  delta_i(s, t) = max over the other sites of |g(s, .) - g(t, .)|      (their theorem as stated)
   one-sided  delta_i(s, t) = max over the other sites of  g(s, .) - g(t, .)       (the class of our Theorem 8; A6)
so the true ensemble is a member and the least scale of the envelope that contains it is exactly 1.  Printed: the size
of the constants, sigma, p, tau, sum tau, TV, the hard limit (union bound), and -- the question E-S3 -- what each test
certifies as a LOWER bound on the scale b of the envelope (class b*d): the one-site ratio test (exact for one-body
data, A8), the caps of (a), and (b) with the most favourable extra datum (the total variation itself).

Run: python3 -B thermal_union_bound.py synthetic > thermal_union_bound_synthetic.log
     python3 -B thermal_union_bound.py K5        > thermal_union_bound_K5.log
     python3 -B thermal_union_bound.py LKSE:5    > thermal_union_bound_LKSEc5.log
"""
import os, sys, math, time, itertools
import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))


def log(s): print(s, flush=True)


# ------------------------------------------------------------------------------------------------ PART A
def closure(M):
    M = M.copy(); np.fill_diagonal(M, 0.0)
    for c in range(len(M)): M = np.minimum(M, M[:, [c]] + M[[c], :])
    return M


def make_class(k, rng, scale, symmetric):
    deltas = []
    for kk in k:
        M = rng.uniform(0.15, 1.0, (kk, kk)) * scale
        if symmetric: M = (M + M.T) / 2
        deltas.append(closure(M))
    pis = [rng.dirichlet(np.full(kk, 3.0)) for kk in k]
    return deltas, pis


def tables(k, deltas, pis):
    X = list(itertools.product(*[range(v) for v in k])); N = len(X)
    pi = np.array([math.prod(pis[i][x[i]] for i in range(len(k))) for x in X])
    d = np.array([[sum(deltas[i][x[i], y[i]] for i in range(len(k))) for y in X] for x in X])     # d[x, y]
    return X, N, pi, d


def polytope(N, pi, d):
    """rows: mu(y) pi(x) - e^{d(x,y)} mu(x) pi(y) <= 0 for x != y"""
    rows = []
    for x in range(N):
        for y in range(N):
            if x != y:
                r = np.zeros(N); r[y] = pi[x]; r[x] = -math.exp(d[x, y]) * pi[y]; rows.append(r)
    return np.array(rows)


def polarised(k, X, pi, deltas, pis, a, into=True):
    """w*(x) ~ pi(x) e^{-d(x, a)} (into = True: the cost INTO the centre) or e^{-d(a, x)}; the one-site values sigma_i"""
    n = len(k); dd = np.array([sum((deltas[i][x[i], a[i]] if into else deltas[i][a[i], x[i]]) for i in range(n)) for x in X])
    w = pi * np.exp(-dd); mu = w / w.sum()
    sig = [pis[i][a[i]] / sum(pis[i][s] * math.exp(-(deltas[i][s, a[i]] if into else deltas[i][a[i], s])) for s in range(k[i])) for i in range(n)]
    return mu, np.array(sig)


def lp_max(cvec, A_ub, N, const=0.0):
    r = linprog(-cvec, A_ub=A_ub, b_ub=np.zeros(len(A_ub)), A_eq=np.ones((1, N)), b_eq=[1.0], bounds=[(0, None)] * N, method="highs")
    assert r.status == 0, r.message
    return -r.fun + const, r.x


def scan(k, X, N, pi, deltas, pis, A_ub, form, cst=1.0, into=True, centres=None):
    """max over centres a, subsets A and members mu of  mu(A) - mu*(A) - cst * sum_i dev_i(mu);
    form 'ratio': dev_i = 1 - p_i / sigma_i;  form 'diff': dev_i = sigma_i - p_i.  Returns (max, #LPs, where)."""
    n = len(k); best = (-1e9, None); cnt = 0
    for a in (centres if centres is not None else X):
        mus, sig = polarised(k, X, pi, deltas, pis, a, into)
        ind = [np.array([1.0 if x[i] == a[i] else 0.0 for x in X]) for i in range(n)]
        if form == "ratio": lin = sum(ind[i] / sig[i] for i in range(n)); c0 = -cst * n
        else: lin = sum(ind[i] for i in range(n)); c0 = -cst * float(sig.sum())
        for bits in range(1, 2 ** N - 1):
            iA = np.array([(bits >> j) & 1 for j in range(N)], dtype=float)
            val, mu = lp_max(iA + cst * lin, A_ub, N, const=c0 - float(iA @ mus)); cnt += 1
            if val > best[0]: best = (val, (a, bits))
    return best[0], cnt, best[1]


def best_ratio(k, X, N, pi, deltas, pis, A_ub, centres=None):
    """sup over the class, the centres and the subsets of [mu(A) - mu*(A)] / sum_i tau_i(mu)  (Charnes-Cooper)."""
    n = len(k); best = 0.0
    for a in (centres if centres is not None else X):
        mus, sig = polarised(k, X, pi, deltas, pis, a)
        lin = sum(np.array([1.0 if x[i] == a[i] else 0.0 for x in X]) / sig[i] for i in range(n))
        for bits in range(1, 2 ** N - 1):
            iA = np.array([(bits >> j) & 1 for j in range(N)], dtype=float)
            # variables (y, t): maximise iA.y - mu*(A) t  s.t.  n t - lin.y = 1,  sum y = t,  A_ub y <= 0
            c = np.concatenate([-iA, [float(iA @ mus)]])
            Aeq = np.vstack([np.concatenate([-lin, [n]]), np.concatenate([np.ones(N), [-1.0]])])
            r = linprog(c, A_ub=np.hstack([A_ub, np.zeros((len(A_ub), 1))]), b_ub=np.zeros(len(A_ub)), A_eq=Aeq, b_eq=[1.0, 0.0],
                        bounds=[(0, None)] * (N + 1), method="highs")
            if r.status == 0: best = max(best, -r.fun)
            else: assert r.status == 2, r.message                    # infeasible: the denominator vanishes on the whole face
    return best


def part_a():
    t0 = time.time(); rng = np.random.default_rng(20261126)
    log("=== PART A: Theorem E15 of the Ensemble division on synthetic classes, by exact maximisation over the class polytope")
    cases = [((2, 2, 2), 0.5), ((2, 2, 2), 1.0), ((2, 2, 2), 2.0), ((2, 2), 1.0), ((3, 2), 1.0), ((3, 3), 1.0), ((3, 3), 2.0), ((4, 2), 1.5), ((3, 2, 2), 1.0)]
    worst_b = -1e9; worst_c = -1e9; best_c3 = -1e9; nlp = 0; ratios = []; fail_half = 0; nbin = 0
    for k, scale in cases:
        deltas, pis = make_class(k, rng, scale, True); X, N, pi, d = tables(k, deltas, pis); A_ub = polytope(N, pi, d)
        cen = X if N <= 9 else [X[j] for j in rng.choice(N, size=3, replace=False)]
        v, c, _ = scan(k, X, N, pi, deltas, pis, A_ub, "ratio", centres=cen); worst_b = max(worst_b, v); nlp += c
        v2, c, _ = scan(k, X, N, pi, deltas, pis, A_ub, "diff", centres=cen); nlp += c
        rt = best_ratio(k, X, N, pi, deltas, pis, A_ub, centres=cen); ratios.append(rt)
        if max(k) == 2:
            worst_c = max(worst_c, v2); nbin += 1
            vh, c, _ = scan(k, X, N, pi, deltas, pis, A_ub, "diff", cst=0.5, centres=cen); nlp += c; fail_half += int(vh > 1e-6)
        else: best_c3 = max(best_c3, v2)
        log(f"  alphabets {k}, scale {scale}: {N} states, {len(A_ub)} constraints, {len(cen)} centres: max [TV - sum tau] = {v:+.2e}; max [TV - sum (sigma - p)] = {v2:+.4f}; "
            f"sup TV / sum tau = {rt:.4f} [{time.time() - t0:.0f}s]")
    log(f"A1  (b): largest value of TV - sum tau over {len(cases)} classes, every subset, every centre tried: {worst_b:+.2e} (must be <= 1e-9; 0 is attained at mu = mu*)")
    log(f"A2  (c), binary sites ({nbin} classes): largest TV - sum (sigma - p) = {worst_c:+.2e} (must be <= 1e-9)")
    log(f"A3  the binary form on sites with three or four states: largest TV - sum (sigma - p) = {best_c3:+.4f} (expected > 0: (c) does not extend; (b) is the form that does)")
    log(f"A4  the best constant in (b): sup TV / sum tau per class: {', '.join(f'{r:.4f}' for r in ratios)} (the theorem: <= 1)")
    log(f"A5  control, constant 1/2 in (c): fails in {fail_half} of {nbin} binary classes (must be all)")
    assert worst_b <= 1e-9 and worst_c <= 1e-9 and fail_half == nbin and best_c3 > 1e-6 and max(ratios) <= 1 + 1e-9
    # ---- A6: one-sided envelopes
    w6 = -1e9; w6a = -1e9; bad_dir = 0; ncl = 0
    for k, scale in [((2, 2, 2), 1.0), ((3, 2), 1.0), ((3, 3), 1.5), ((3, 3), 0.7), ((4, 2), 1.0)]:
        deltas, pis = make_class(k, rng, scale, False); X, N, pi, d = tables(k, deltas, pis); A_ub = polytope(N, pi, d); ncl += 1
        asym = max(float(np.abs(D - D.T).max()) for D in deltas)
        v, c, _ = scan(k, X, N, pi, deltas, pis, A_ub, "ratio", into=True); w6 = max(w6, v); nlp += c
        # (a) for the one-sided class: max over the class of p_i - sigma_i
        for a in X:
            mus, sig = polarised(k, X, pi, deltas, pis, a, True)
            assert (A_ub @ mus <= 1e-12).all(), "the polarised member (cost into the centre) must be a member"
            for i in range(len(k)):
                val, _ = lp_max(np.array([1.0 if x[i] == a[i] else 0.0 for x in X]), A_ub, N, const=-sig[i]); w6a = max(w6a, val); nlp += 1
        # control: the other direction
        notmem = 0
        for a in X:
            mus, sig = polarised(k, X, pi, deltas, pis, a, False); notmem += int((A_ub @ mus > 1e-9).any())
        vb, c, _ = scan(k, X, N, pi, deltas, pis, A_ub, "ratio", into=False); nlp += c; bad_dir += int(vb > 1e-6 or notmem > 0)
        log(f"  one-sided, alphabets {k}, scale {scale} (largest |delta(s,t) - delta(t,s)| = {asym:.2f}): max [TV - sum tau] = {v:+.2e}; with the member defined by d(a, x): "
            f"not a member for {notmem} of {N} centres, max [TV - sum tau] = {vb:+.4f} [{time.time() - t0:.0f}s]")
    log(f"A6  one-sided envelopes ({ncl} classes): (b) with w* ~ e^(-d(x, a)): largest TV - sum tau = {w6:+.2e}; (a): largest p_i - sigma_i = {w6a:+.2e} (both must be <= 1e-9); "
        f"control, the member defined by d(a, x): wrong in {bad_dir} of {ncl} classes (must be positive)")
    assert w6 <= 1e-9 and w6a <= 1e-9 and bad_dir > 0
    # ---- A7: a class that is too large
    f7 = 0
    for k, scale in [((2, 2, 2), 1.0), ((3, 2), 1.0), ((3, 3), 1.0)]:
        deltas, pis = make_class(k, rng, scale, True); X, N, pi, d = tables(k, deltas, pis); A2 = polytope(N, pi, 2 * d)
        v, c, _ = scan(k, X, N, pi, deltas, pis, A2, "ratio", centres=X[:2]); nlp += c; f7 += int(v > 1e-6)
    log(f"A7  control, members of the class of envelope 2d against the bound for d: violated in {f7} of 3 classes (must be all)")
    assert f7 == 3
    # ---- A8: one-body data alone
    ok = 0; infeas = 0; tot = 0; feas_ctrl = 0
    VIOL = 0.01                      # in the log-ratio; 1e-6 was tried first and is inside the LP solver's feasibility tolerance (1e-7 absolute): 30 of 60 came back "feasible"
    for k, scale in [((3, 2), 1.0), ((3, 3), 1.0), ((2, 2, 2), 1.5)]:
        deltas, pis = make_class(k, rng, scale, True); X, N, pi, d = tables(k, deltas, pis); A_ub = polytope(N, pi, d); n = len(k)
        for rep in range(20):
            # a member of each one-site class: w_i = pi_i e^{-h_i}, h_i = inf-convolution of a random function with delta_i (1-Lipschitz)
            ms = []
            for i in range(n):
                u = rng.uniform(0, 2 * scale, k[i]); h = (u[None, :] + deltas[i]).min(axis=1); w = pis[i] * np.exp(-h); ms.append(w / w.sum())
            prod = np.array([math.prod(ms[i][x[i]] for i in range(n)) for x in X]); tot += 1
            ok += int((A_ub @ prod <= 1e-12).all())
            # violate one one-site constraint by 1e-6 in the log-ratio: find the tightest pair of site 0 and push beyond it
            i = 0; lr = np.log(ms[i][None, :] * pis[i][:, None] / (ms[i][:, None] * pis[i][None, :])) - deltas[i]     # [s, t]: ln(m(t) pi(s) / (m(s) pi(t))) - delta(s, t) <= 0
            np.fill_diagonal(lr, -1e9); s, t = np.unravel_index(np.argmax(lr), lr.shape)
            m2 = ms[i].copy(); fac = math.exp(-lr[s, t] + VIOL); m2[t] *= fac; m2 /= m2.sum()                           # now ln(...) - delta = +VIOL for that pair
            marg = [m2] + ms[1:]
            Aeq = [np.ones(N)]; beq = [1.0]
            for j in range(n):
                for s_ in range(k[j] - 1): Aeq.append(np.array([1.0 if x[j] == s_ else 0.0 for x in X])); beq.append(marg[j][s_])
            r = linprog(np.zeros(N), A_ub=A_ub, b_ub=np.zeros(len(A_ub)), A_eq=np.array(Aeq), b_eq=beq, bounds=[(0, None)] * N, method="highs")
            infeas += int(r.status == 2)
            # control of the feasibility programme itself: with the unmodified marginals it must be feasible
            Aeq = [np.ones(N)]; beq = [1.0]
            for j in range(n):
                for s_ in range(k[j] - 1): Aeq.append(np.array([1.0 if x[j] == s_ else 0.0 for x in X])); beq.append(ms[j][s_])
            r = linprog(np.zeros(N), A_ub=A_ub, b_ub=np.zeros(len(A_ub)), A_eq=np.array(Aeq), b_eq=beq, bounds=[(0, None)] * N, method="highs")
            feas_ctrl += int(r.status == 0)
    log(f"A8  one-body data alone: products of one-site members are members: {ok} of {tot}; one one-site constraint violated by {VIOL} in the log-ratio: no member has those marginals in {infeas} of {tot} "
        f"(must be all); the same programme with the unmodified marginals is feasible in {feas_ctrl} of {tot} (must be all) -- so for one-body data the exact falsification test is the one-site ratio test")
    assert ok == tot and infeas == tot and feas_ctrl == tot
    log(f"PART A DONE: {nlp} linear programmes, {time.time() - t0:.0f} s")


# ------------------------------------------------------------------------------------------------ PART B
def part_b(seq):
    sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "pi_inference")))
    import nested_sampler as NS
    L, pw = NS.L, NS.pw; BETA = L.BETA; t0 = time.time(); bb = "H"
    tau = 0.60 if ":" in seq else dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)[seq[0]]
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = [int(v) for v in x0]
    st = np.stack(np.meshgrid(*[np.arange(v) for v in k], indexing="ij"), axis=-1).reshape(-1, n)
    E = pw.f_energy(st, c0, h, J) + np.concatenate([G.bulk_energy(st[s:s + 256]) for s in range(0, len(st), 256)])
    E = (BETA * (E - E[np.ravel_multi_index(x0, k)])).reshape(k)                                   # beta (E - E(x0)), shape k
    log(f"=== PART B: {seq} on {bb}, tau {tau}: {n} sites, states per site {k}, {E.size} states (all evaluated), anchor {x0}, beta = {BETA:.4f} per kcal/mol [{time.time() - t0:.0f}s]")
    w = np.exp(-(E - E.min())); mu = w / w.sum(); lnZ = float(-E.min() + math.log(w.sum()))
    one = []                                                                                       # anchored one-body terms
    for i in range(n):
        ix = tuple(x0[j] if j != i else slice(None) for j in range(n)); one.append(np.array(E[ix]))
    I1 = np.zeros(k)
    for i in range(n): I1 = I1 + one[i].reshape([k[i] if j == i else 1 for j in range(n)])
    g = E - I1                                                                                     # the rest; zero on the ball of radius 1
    assert abs(g[tuple(x0)]) < 1e-12 and all(np.abs(g[tuple(x0[j] if j != i else slice(None) for j in range(n))]).max() < 1e-9 for i in range(n))
    pis = [np.exp(-(o - o.min())) / np.exp(-(o - o.min())).sum() for o in one]
    marg = [mu.sum(axis=tuple(j for j in range(n) if j != i)) for i in range(n)]
    off = float(sum(1 - marg[i][x0[i]] for i in range(n)))
    log(f"(0) exact ln Z - (-beta E(x0)) = {lnZ:.6f}; population of the anchor conformation {float(mu[tuple(x0)]):.4f}; mean number of sites off the anchor {off:.4f}; "
        f"the rest g = beta (E - first-order interpolant): range [{g.min():.2f}, {g.max():.2f}] kT, Gibbs mean {float((mu * g).sum()):+.3f}, Gibbs mean of |g| {float((mu * np.abs(g)).sum()):.3f}")

    def envelopes(sym):
        out = []
        for i in range(n):
            gi = np.moveaxis(g, i, 0).reshape(k[i], -1); D = (gi[:, None, :] - gi[None, :, :])
            out.append(np.abs(D).max(axis=2) if sym else D.max(axis=2))                            # delta_i[s, t] = max over the others of g(s, .) - g(t, .)
        return out

    def report(name, deltas, a):
        # the class b * d: polarised member w*(x) ~ pi(x) exp(-b d(x, a)); sigma_i(b)
        def member(b):
            ms = [pis[i] * np.exp(-b * deltas[i][:, a[i]]) for i in range(n)]; ms = [m / m.sum() for m in ms]
            mm = np.ones(k)
            for i in range(n): mm = mm * ms[i].reshape([k[i] if j == i else 1 for j in range(n)])
            return ms, mm
        ms, mstar = member(1.0); sig = np.array([ms[i][a[i]] for i in range(n)]); p = np.array([marg[i][a[i]] for i in range(n)])
        tauv = 1 - p / sig; TV = 0.5 * float(np.abs(mu - mstar).sum())
        # membership of the truth (b = 1 must be the least scale): the one-step constraints g(s, .) - g(t, .) <= delta_i(s, t) hold by construction
        log(f"--- {name} envelope, centre {list(a)}: constants delta_i(s, a_i) (kT): per site max {', '.join(f'{float(deltas[i][:, a[i]].max()):.1f}' for i in range(n))}; "
            f"median over s != a_i {', '.join(f'{float(np.median(np.delete(deltas[i][:, a[i]], a[i]))):.1f}' for i in range(n))}; largest delta_i(s, t) over all pairs {max(float(D.max()) for D in deltas):.1f}")
        log(f"    sigma_i = polarised member's population of a_i: {', '.join(f'{v:.4f}' for v in sig)}; p_i = true population: {', '.join(f'{v:.4f}' for v in p)}; "
            f"(a) p_i <= sigma_i: {bool((p <= sig + 1e-12).all())}")
        log(f"    tau_i = 1 - p_i / sigma_i: {', '.join(f'{v:.4f}' for v in tauv)}; **sum tau = {float(tauv.sum()):.4f}**; the binary form sum (sigma_i - p_i) = {float((sig - p).sum()):.4f}; "
            f"**TV(mu, mu*_a) = {TV:.4f}** (exact); (b) holds: {TV <= float(tauv.sum()) + 1e-12}; the bound is {'EMPTY (>= 1)' if tauv.sum() >= 1 else f'{float(tauv.sum()) / TV:.2f} times the truth'}")
        log(f"    hard limit (union bound): 1 - mu(a) = {1 - float(mu[tuple(a)]):.4f} <= sum_i mu(x_i != a_i) = {float((1 - p).sum()):.4f}")
        # what each test certifies as a lower bound on the scale b
        b1 = 0.0; arg = None
        for i in range(n):
            lr = np.log(marg[i][None, :] * pis[i][:, None] / (marg[i][:, None] * pis[i][None, :]))  # [s, t] = ln(mu_i(t) pi_i(s) / (mu_i(s) pi_i(t))) <= b delta_i(s, t)
            with np.errstate(divide="ignore", invalid="ignore"): q = np.where(deltas[i] > 1e-12, lr / deltas[i], 0.0)
            np.fill_diagonal(q, 0.0)
            if q.max() > b1: b1 = float(q.max()); arg = (i,) + tuple(int(v) for v in np.unravel_index(np.argmax(q), q.shape))
        # caps of (a) at scale b, any centre state s of any site: violated iff marg_i(s) > sigma_{i,s}(b)
        b2 = 0.0
        for i in range(n):
            for s in range(k[i]):
                f = lambda b: pis[i][s] / float((pis[i] * np.exp(-b * deltas[i][:, s])).sum()) - marg[i][s]      # sigma(b) - p: negative = violated
                if f(0.0) < 0:
                    lo_, hi_ = 0.0, 1.0
                    if f(1.0) < -1e-12: hi_ = 1.0; lo_ = 1.0
                    else:
                        for _ in range(60):
                            mid = 0.5 * (lo_ + hi_); lo_, hi_ = (mid, hi_) if f(mid) < 0 else (lo_, mid)
                    b2 = max(b2, lo_)
        # (b) with the total variation itself as the extra datum, at this centre: the largest b of the grid at which the caps of this
        # centre hold and TV(mu, mu*_{a,b}) > sum tau(b)  (b3); the largest b at which a cap of this centre fails (b3c)
        grid = np.linspace(0.005, 1.0, 200); b3 = 0.0; b3c = 0.0
        for b in grid:
            msb, mb = member(b); sg = np.array([msb[i][a[i]] for i in range(n)])
            if (p > sg).any(): b3c = max(b3c, b); continue
            if 0.5 * float(np.abs(mu - mb).sum()) > float((1 - p / sg).sum()) + 1e-12: b3 = max(b3, b)
        log(f"    as a falsification test of the class b*d (the truth needs b = 1): one-site ratio test certifies b >= **{b1:.4f}** (site {arg[0]}, states {arg[1]} -> {arg[2]}); "
            f"the caps of (a), any centre: b >= {b2:.4f}; at this centre: a cap fails up to b = {b3c:.4f}, and (b) with the total variation as the extra datum certifies b >= **{b3:.4f}** (grid of 200)")
        return member, b1, b2

    def many_centres(name, deltas):
        # (b) at many centres: every combination of the two most populated states of each site, and 200 random centres; grid of 40
        rng = np.random.default_rng(11); top = [list(np.argsort(-marg[i])[:2]) for i in range(n)]
        cen = [tuple(int(v) for v in c) for c in itertools.product(*top)] + [tuple(int(rng.integers(kk)) for kk in k) for _ in range(200)]
        grid = np.linspace(0.025, 1.0, 40); best = (0.0, None); bestc = (0.0, None); least = (9.0, None)
        for a in cen:
            p = np.array([marg[i][a[i]] for i in range(n)])
            for b in grid:
                ms = [pis[i] * np.exp(-b * deltas[i][:, a[i]]) for i in range(n)]; ms = [m / m.sum() for m in ms]; sg = np.array([ms[i][a[i]] for i in range(n)])
                if (p > sg).any():
                    if b > bestc[0]: bestc = (float(b), a)
                    continue
                mm = np.ones(k)
                for i in range(n): mm = mm * ms[i].reshape([k[i] if j == i else 1 for j in range(n)])
                tv = 0.5 * float(np.abs(mu - mm).sum()); st_ = float((1 - p / sg).sum())
                if tv > st_ + 1e-12 and b > best[0]: best = (float(b), a)
                if b == grid[-1] and st_ / max(tv, 1e-300) < least[0]: least = (st_ / tv, a)
        log(f"    {name}: (b) at {len(cen)} centres (the {2 ** n} combinations of the two most populated states of each site, 200 random), grid of 40: the largest b at which (b) is violated "
            f"with every cap of that centre satisfied: **{best[0]:.3f}**{'' if best[1] is None else ' (centre ' + str(list(best[1])) + ')'}; the largest b at which a cap of the centre fails: {bestc[0]:.3f}; "
            f"at b = 1 the least ratio (sum tau) / TV over these centres: {least[0]:.2f}")

    for sym in (True, False):
        deltas = envelopes(sym); nm = "symmetric" if sym else "one-sided"
        # the truth is a member: check the pair constraints along single-site moves at 20000 random pairs, and the triangle inequality of the delta_i
        rng = np.random.default_rng(7); viol = 0
        for _ in range(20000):
            x = [int(rng.integers(kk)) for kk in k]; i = int(rng.integers(n)); t = int(rng.integers(k[i])); y = list(x); y[i] = t
            viol += int(g[tuple(x)] - g[tuple(y)] > deltas[i][x[i], t] + 1e-9)
        tri = -1e9
        for D in deltas:
            tri = max(tri, float((D[:, None, :] - (D[:, :, None] + D[None, :, :])).max()))                 # delta(s,u) - delta(s,t) - delta(t,u)
        rng = np.random.default_rng(7); viol_half = 0                                                     # control of the membership test: the same pairs against d/2
        for _ in range(20000):
            x = [int(rng.integers(kk)) for kk in k]; i = int(rng.integers(n)); t = int(rng.integers(k[i])); y = list(x); y[i] = t
            viol_half += int(g[tuple(x)] - g[tuple(y)] > 0.5 * deltas[i][x[i], t] + 1e-9)
        log(f"=== {nm} envelope: single-site constraints violated at {viol} of 20000 random pairs (must be 0; control, the same pairs against half the envelope: {viol_half}, must be positive); "
            f"triangle inequality violated by at most {tri:.1e} (must be <= 0)")
        assert viol == 0 and tri <= 1e-9 and viol_half > 0
        res = report(nm, deltas, tuple(x0)); many_centres(nm, deltas)
        # the best centre: tau_i(s) is separate in the sites
        best = []
        for i in range(n):
            tv = [1 - marg[i][s] / (pis[i][s] / float((pis[i] * np.exp(-deltas[i][:, s])).sum())) for s in range(k[i])]; best.append(int(np.argmin(tv)))
        if best != x0: report(nm + " (centre with the least sum tau)", deltas, tuple(best))
        else: log("    the anchor is also the centre with the least sum tau")
        # control: the bound must fail for a class that is too small: scale 1/2
        ms = [pis[i] * np.exp(-0.5 * deltas[i][:, x0[i]]) for i in range(n)]; ms = [m / m.sum() for m in ms]; sg = np.array([ms[i][x0[i]] for i in range(n)])
        p = np.array([marg[i][x0[i]] for i in range(n)]); mm = np.ones(k)
        for i in range(n): mm = mm * ms[i].reshape([k[i] if j == i else 1 for j in range(n)])
        log(f"    at half the envelope (the truth is NOT a member of that class; a finding, not a control): (a) notices it at {int((p > sg).sum())} of {n} sites of this centre; (b): TV - sum tau = {0.5 * float(np.abs(mu - mm).sum()) - float((1 - p / sg).sum()):+.4f} (negative = not noticed)")
    log(f"ALL DONE {time.time() - t0:.0f} s")


if __name__ == "__main__":
    if sys.argv[1] == "synthetic": part_a()
    else: part_b(sys.argv[1])
