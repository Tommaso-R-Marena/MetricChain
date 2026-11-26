#!/usr/bin/env python3
"""R15, Item 2 -- Proposition 11.18f of the theory report at f7df44f ("which shares: the allocation for a law"):
own enumeration, written from the statement.  Nothing imported from the theory harness.

Objects.  n sites; constants c_T >= 0 on the m-subsets T; a law P of the changed set S; a level k.  An allocation is
lam[T][K] >= 0 over the k-subsets K of T with sum_K lam[T][K] = c_T; charge g_K = sum_T lam[T][K]; penalty
pen(S) = sum_{K subset S} g_K;  U = ln E_P e^{pen},  L = -ln E_P e^{-pen}.
(U comes from the floor model m- = A - pen and is the upper end of ln Z; L comes from the ceiling m+ = A + pen.)

PART 1  the "Numbers" of the proposition (six sites, triples, equal constants): eight pairs (U, L).
PART 2  (a) cost number, product formula, mean penalty p^k Gamma;  (b) convexity, gradients, the KKT statement for U,
        vertices and local minima of L, ordering vertices;  (c) first order, the formula gamma_i = Gamma(R_i) - Gamma(R_i \\ {i}),
        ties.
PART 3  the coordinator's question: when the constants are not small, what does the "most frozen site" vertex do to
        the two ends, against equal shares?  Criteria in terms of the penalty at a site against the free-energy cost
        f_i = ln((1 - p_i)/p_i) of changing it; a synthetic family; a random search.

Run:  OMP_NUM_THREADS=1 python3 r15_item2_allocation.py > logs/item2_allocation.log
"""
import itertools, math, resource, time
import numpy as np

t0 = time.time()
ok_all = True


def check(cond, msg):
    global ok_all
    if not cond:
        ok_all = False
        print("   !!! CHECK FAILED:", msg)


# ------------------------------------------------------------------ basic machinery (bit masks)
def masks_of(n):
    return np.arange(1 << n)


def bits(n):
    S = masks_of(n)
    return ((S[:, None] >> np.arange(n)[None, :]) & 1).astype(float)          # 2^n x n


def product_law(p):
    B = bits(len(p))
    p = np.asarray(p, float)
    return np.prod(np.where(B > 0, p[None, :], 1 - p[None, :]), axis=1)


def ksubsets(T, k):
    return [frozenset(K) for K in itertools.combinations(sorted(T), k)]


def contain_matrix(n, Ks):
    """I[S, j] = 1 if K_j is a subset of S"""
    S = masks_of(n)
    out = np.zeros((1 << n, len(Ks)))
    for j, K in enumerate(Ks):
        mk = sum(1 << i for i in K)
        out[:, j] = ((S & mk) == mk)
    return out


def UL(law, pen):
    return math.log(float(law @ np.exp(pen))), -math.log(float(law @ np.exp(-pen)))


class Instance:
    def __init__(self, n, m, k, c, law):
        self.n, self.m, self.k, self.law = n, m, k, np.asarray(law, float)
        self.Ts = [T for T in sorted(c, key=lambda t: sorted(t)) if c[T] > 0]
        self.c = np.array([c[T] for T in self.Ts])
        self.Ks = [frozenset(K) for K in itertools.combinations(range(n), k)]
        self.kidx = {K: j for j, K in enumerate(self.Ks)}
        self.I = contain_matrix(n, self.Ks)
        self.sub = [[self.kidx[K] for K in ksubsets(T, k)] for T in self.Ts]      # for each T the indices of its k-subsets
        self.r = math.comb(m, k)
        self.subarr = np.array(self.sub)                                          # (#T, r)
        self.margK = self.law @ self.I                                            # P(K subset S)

    def charges(self, lam):
        g = np.zeros(len(self.Ks))
        np.add.at(g, self.subarr, lam)
        return g

    def pen(self, lam):
        return self.I @ self.charges(lam)

    def UL(self, lam):
        return UL(self.law, self.pen(lam))

    def tilted(self, lam, sign):
        w = self.law * np.exp(sign * self.pen(lam))
        return (w / w.sum()) @ self.I                                             # tilted P(K subset S)

    def equal(self):
        return np.repeat(self.c[:, None] / self.r, self.r, axis=1)

    def vertex(self, choice):
        lam = np.zeros((len(self.Ts), self.r))
        lam[np.arange(len(self.Ts)), choice] = self.c
        return lam

    def greedy_choice(self, key=None):
        """first order: every constant on its least probable k-subset; ties broken by the index of the subset"""
        key = np.round(self.margK, 12) if key is None else key      # rounding: exact ties must not be decided by the last bit
        return np.array([min(range(self.r), key=lambda a: (key[s[a]], s[a])) for s in self.sub])

    def order_choice(self, order):
        """charge every T to the first of its k-subsets in the given order of the k-subsets"""
        pos = np.empty(len(self.Ks), int)
        pos[np.asarray(order)] = np.arange(len(self.Ks))
        return np.array([min(range(self.r), key=lambda a: pos[s[a]]) for s in self.sub])

    def min_U(self, iters=20000, tol=1e-11):
        """minimise the convex U over the product of simplices by exponentiated gradient; stops when the
        Frank-Wolfe gap <grad, lam - vertex> (an upper bound of U(lam) - min U) is below tol"""
        lam = self.equal()
        eta = 1.0
        gap = math.inf
        for it in range(iters):
            grad = self.tilted(lam, +1)[self.subarr]                              # dU/dlam[T][K] = P+(K subset S)
            best = grad.min(axis=1)
            gap = float((lam * (grad - best[:, None])).sum())
            if gap < tol:
                break
            new = lam * np.exp(-eta * (grad - best[:, None]))
            new *= (self.c / new.sum(axis=1))[:, None]
            if self.UL(new)[0] > self.UL(lam)[0] + 1e-15:
                eta *= 0.5
                continue
            lam = new
            eta *= 1.1
        return lam, gap


def site_instance(p, m, c_of_T, law=None, k=1):
    n = len(p)
    c = {frozenset(T): float(c_of_T(T)) for T in itertools.combinations(range(n), m)}
    return Instance(n, m, k, c, product_law(p) if law is None else law)


# ------------------------------------------------------------------ PART 1
print("PART 1  'Numbers' of Proposition 11.18f: six sites, triples, equal constants; exact enumeration over the 64 changed sets")
EX = [("four nearly frozen (p = 0.01) and two mobile (p = 0.3), constants 0.1", [0.01] * 4 + [0.3] * 2, 0.1,
       {"equal site shares": (0.240, 0.189), "most frozen site": (0.030, 0.014), "equal pair shares": (0.016, 0.014), "envelope": (0.0004, 0.0004)}),
      ("homogeneous (p = 0.05), constants 0.5", [0.05] * 6, 0.5, {"equal site shares": (1.17, 0.248), "most frozen site": (2.99, 0.159)})]
for name, p, cval, theirs in EX:
    print(f" {name}")
    I1 = site_instance(p, 3, lambda T: cval, k=1)
    I2 = site_instance(p, 3, lambda T: cval, k=2)
    I3 = site_instance(p, 3, lambda T: cval, k=3)
    res = {"equal site shares": I1.UL(I1.equal()), "most frozen site": I1.UL(I1.vertex(I1.greedy_choice())),
           "equal pair shares": I2.UL(I2.equal()), "envelope": I3.UL(I3.equal())}
    for key, (u, l) in res.items():
        th = theirs.get(key)
        s = f"   {key:20s} (U, L) = ({u:.5f}, {l:.5f})"
        if th:
            s += f"   theirs ({th[0]}, {th[1]})"
            tolu = 0.5 * 10 ** (-len(str(th[0]).split(".")[1])) * 1.01
            toll = 0.5 * 10 ** (-len(str(th[1]).split(".")[1])) * 1.01
            check(abs(u - th[0]) <= tolu and abs(l - th[1]) <= toll, f"Numbers: {key}: ({u}, {l}) vs {th}")
        else:
            s += "   (not quoted in the report)"
        print(s)
    ue, le = res["equal site shares"]; ug, lg = res["most frozen site"]
    print(f"   ratios equal/greedy: U {ue / ug:.2f}, L {le / lg:.2f}")
    # more allocations of level 1 for the same instance
    f = np.log((1 - np.array(p)) / np.array(p))
    lamU, gap = I1.min_U()
    uo, lo_ = I1.UL(lamU)
    # ties: split every constant equally among the tied most frozen sites of its T
    lam_t = np.zeros((len(I1.Ts), 3))
    for a, s in enumerate(I1.sub):
        pm = min(I1.margK[j] for j in s)
        tied = [b for b in range(3) if abs(I1.margK[s[b]] - pm) < 1e-15]
        lam_t[a, tied] = I1.c[a] / len(tied)
    ut, lt = I1.UL(lam_t)
    # the best vertex for L among ordering vertices (720 orders of the sites), and the best / worst vertex overall for
    # equal constants through the count vectors of the transportation polytope
    bestL = min((I1.UL(I1.vertex(I1.order_choice(o)))[1], o) for o in itertools.permutations(range(6)))
    print(f"   level 1, other allocations: minimum of U over all allocations {uo:.5f} (Frank-Wolfe gap {gap:.1e}), its L {lo_:.5f};")
    print(f"      equal split among TIED most frozen sites: (U, L) = ({ut:.5f}, {lt:.5f});  best ordering vertex for L: L = {bestL[0]:.5f} (order {bestL[1]});"
          f" greedy L = {lg:.5f}")
    g_gr = I1.charges(I1.vertex(I1.greedy_choice()))
    print(f"      greedy site penalties {np.round(g_gr, 3).tolist()}; free-energy costs f_i = ln((1-p_i)/p_i) = {np.round(f, 3).tolist()}; f - gamma = {np.round(f - g_gr, 3).tolist()}")

# ------------------------------------------------------------------ PART 2
print("PART 2  the statements (a), (b), (c) on random instances")
rng = np.random.default_rng(1518)
# (a) product formula, mean penalty of level k
worst = 0.0
for trial in range(40):
    n = int(rng.choice([5, 6, 7])); m = int(rng.choice([3, 4]))
    p = rng.uniform(0.02, 0.6, n)
    for k in range(0, m + 1):
        if k == 0:
            continue
        I = site_instance(p, m, lambda T: rng.exponential(0.4), k=k)
        lam = I.equal()
        pen = I.pen(lam)
        # counting form: pen_k(S) = sum_T c_T C(|T & S|, k)/C(m, k)
        cnt = np.zeros(1 << n)
        for T, cT in zip(I.Ts, I.c):
            mk = sum(1 << i for i in T)
            ov = np.array([bin(int(s) & mk).count("1") for s in masks_of(n)])
            cnt += cT * np.array([math.comb(int(t), k) for t in ov]) / math.comb(m, k)
        worst = max(worst, float(np.abs(pen - cnt).max()))
        if k == 1:
            g = I.charges(lam)
            worst = max(worst, abs(float(I.law @ np.exp(pen)) - float(np.prod(1 + p * np.expm1(g)))))
        # common p: mean penalty exactly p^k Gamma
        pc = float(rng.uniform(0.02, 0.6))
        lawc = product_law([pc] * n)
        worst = max(worst, abs(float(lawc @ pen) - pc ** k * float(I.c.sum())))
        # unequal p: mean penalty = sum_K g_K prod_{i in K} p_i
        g = I.charges(lam)
        worst = max(worst, abs(float(I.law @ pen) - float(sum(g[j] * np.prod(p[list(K)]) for j, K in enumerate(I.Ks)))))
check(worst < 1e-10, "(a) identities")
print(f"   (a) counting form of pen_k, product formula of the cost number (k = 1), mean penalty = p^k Gamma for a common p and EVERY 1 <= k <= m"
      f" (random constants), and = sum_K g_K prod p_i for unequal p: largest error {worst:.1e} over 40 instances (k = 0 is trivial: pen_0 = Gamma)")

# (b) convexity, concavity, gradients, for a NON-product law and levels 1, 2
viol = 0; gerr = 0.0
for trial in range(30):
    n = 6; m = 3; k = int(rng.choice([1, 2]))
    law = rng.dirichlet(np.ones(1 << n) * 0.3)
    I = site_instance([0.5] * n, m, lambda T: rng.exponential(0.5), law=law, k=k)

    def rand_alloc():
        return rng.dirichlet(np.ones(I.r), size=len(I.Ts)) * I.c[:, None]

    a, b = rand_alloc(), rand_alloc()
    Ua, La = I.UL(a); Ub, Lb = I.UL(b); Um, Lm = I.UL(0.5 * (a + b))
    viol += int(Um > 0.5 * (Ua + Ub) + 1e-12) + int(Lm < 0.5 * (La + Lb) - 1e-12)
    h = 1e-6
    for _ in range(3):
        ti, ki = int(rng.integers(len(I.Ts))), int(rng.integers(I.r))
        d = np.zeros_like(a); d[ti, ki] = h
        gU = (I.UL(a + d)[0] - I.UL(a - d)[0]) / (2 * h)
        gL = (I.UL(a + d)[1] - I.UL(a - d)[1]) / (2 * h)
        gerr = max(gerr, abs(gU - I.tilted(a, +1)[I.sub[ti][ki]]), abs(gL - I.tilted(a, -1)[I.sub[ti][ki]]))
check(viol == 0 and gerr < 1e-7, "(b) convexity / gradients")
print(f"   (b) midpoint convexity of U and concavity of L violated {viol} times in 30 instances with non-product laws, levels 1 and 2;"
      f" gradients = tilted probabilities P+(K in S), P-(K in S): largest finite-difference error {gerr:.1e}")

# (b) the KKT statement for U
kkt_bad = 0; nonopt_seen = 0; worst_gap = 0.0; rand_below = 0
for trial in range(25):
    n = 6; m = 3; k = int(rng.choice([1, 2]))
    if trial % 2 == 0:
        law = product_law(rng.uniform(0.02, 0.5, n))
    else:
        law = rng.dirichlet(np.ones(1 << n) * 0.3)
    I = site_instance([0.5] * n, m, lambda T: rng.exponential(0.6), law=law, k=k)
    lam, gap = I.min_U()
    worst_gap = max(worst_gap, gap)
    Ustar = I.UL(lam)[0]
    tp = I.tilted(lam, +1)
    for a, s in enumerate(I.sub):
        mn = min(tp[j] for j in s)
        for bidx, j in enumerate(s):
            if lam[a, bidx] > 1e-6 * I.c[a] and tp[j] > mn + 1e-5:
                kkt_bad += 1                      # mass on a subset that is not among the least often changed
    for _ in range(20):
        r_ = rng.dirichlet(np.ones(I.r), size=len(I.Ts)) * I.c[:, None]
        if I.UL(r_)[0] < Ustar - 1e-9:
            rand_below += 1
        tr = I.tilted(r_, +1)
        if any(r_[a, bidx] > 1e-6 * I.c[a] and tr[j] > min(tr[jj] for jj in s) + 1e-5 for a, s in enumerate(I.sub) for bidx, j in enumerate(s)):
            nonopt_seen += 1
check(kkt_bad == 0 and rand_below == 0 and worst_gap < 1e-6, "(b) KKT for the minimiser of U")
print(f"   (b) minimiser of U (exponentiated gradient, Frank-Wolfe gap <= {worst_gap:.1e}) on 25 instances: constants sitting on a k-subset that is NOT"
      f" among the least often changed under P+ at the minimiser: {kkt_bad}; random allocations below the minimum: {rand_below}; of 500 random allocations"
      f" {nonopt_seen} violate the condition (and none is optimal)")
# exchangeable instance: equal shares satisfy the condition
I = site_instance([0.2] * 5, 3, lambda T: 0.6, k=1)
tp = I.tilted(I.equal(), +1)
check(np.ptp(tp) < 1e-14, "exchangeable instance: tilted probabilities equal")
I2 = site_instance([0.2] * 5, 3, lambda T: 0.6, k=2)
check(np.ptp(I2.tilted(I2.equal(), +1)) < 1e-14, "exchangeable instance, level 2")
print("       exchangeable instance (equal p, equal constants): at equal shares all tilted probabilities coincide, levels 1 and 2 -> equal shares minimise U")

# (b) L on the vertices: all vertices of a small instance
print("   (b) L on ALL vertices (n = 5, triples, level 1: 3^10 = 59049 vertices; a vertex is a strict local minimum if moving any one constant raises L to first order)")


def all_vertices_L(I):
    """L at every vertex, by the site charges: for level 1 the penalty depends on the charges only"""
    nT = len(I.Ts)
    B = bits(I.n)
    choices = np.array(list(itertools.product(range(I.r), repeat=nT)), dtype=np.int16)      # (#V, nT)
    sub = I.subarr                                                                            # (nT, r) -> site index
    site = sub[np.arange(nT)[None, :], choices]                                               # (#V, nT)
    g = np.zeros((len(choices), I.n))
    for t in range(nT):
        np.add.at(g, (np.arange(len(choices)), site[:, t]), I.c[t])
    # L = -ln sum_S law(S) exp(-B g)
    Lv = np.empty(len(choices))
    for s in range(0, len(choices), 8192):
        Lv[s:s + 8192] = -np.log(np.exp(-g[s:s + 8192] @ B.T) @ I.law)
    return choices, g, Lv


stat = dict(inst=0, greedy_is_best=0, best_is_ordering=0, locmin=[], greedy_locmin=0)
for trial, kind in enumerate(["equal constants, product law"] * 3 + ["random constants, product law"] * 4 + ["random constants, non-product law"] * 3):
    n, m = 5, 3
    p = rng.uniform(0.03, 0.5, n)
    law = product_law(p) if "non-product" not in kind else rng.dirichlet(np.ones(1 << n) * 0.4)
    cs = float(rng.choice([0.2, 1.0, 3.0]))
    I = site_instance(p, m, (lambda T: cs) if kind.startswith("equal") else (lambda T: rng.exponential(cs)), law=law, k=1)
    choices, g, Lv = all_vertices_L(I)
    ibest = int(np.argmin(Lv))
    gch = I.greedy_choice()
    Lg = I.UL(I.vertex(gch))[1]
    # ordering vertices
    Lord = min(I.UL(I.vertex(I.order_choice(o)))[1] for o in itertools.permutations(range(n)))
    # strict local minima among ALL vertices: for every T the charged site is the strictly least often changed site
    # of T under the ceiling-tilted law of the vertex itself (then moving any one constant raises L to first order)
    Bm = bits(I.n)
    nloc = 0
    for s0 in range(0, len(choices), 8192):
        gg_ = g[s0:s0 + 8192]
        wts = np.exp(-gg_ @ Bm.T) * I.law[None, :]
        tmv = (wts @ Bm) / wts.sum(axis=1, keepdims=True)                         # (V, n) tilted change probabilities
        okv = np.ones(len(gg_), bool)
        for t in range(len(I.Ts)):
            vals = tmv[:, I.subarr[t]]                                            # (V, r)
            ch_ = choices[s0:s0 + 8192, t].astype(int)
            mine = vals[np.arange(len(gg_)), ch_]
            vals2 = vals.copy(); vals2[np.arange(len(gg_)), ch_] = np.inf
            okv &= mine < vals2.min(axis=1) - 1e-12
        nloc += int(okv.sum())
    lam_g = I.vertex(gch); tm = I.tilted(lam_g, -1)
    g_loc = all(tm[s[gch[a]]] < min(tm[s[b]] for b in range(I.r) if b != gch[a]) - 1e-12 for a, s in enumerate(I.sub))
    stat["inst"] += 1
    stat["greedy_is_best"] += int(Lg <= Lv[ibest] + 1e-12)
    stat["best_is_ordering"] += int(abs(Lord - Lv[ibest]) < 1e-12)
    stat["greedy_locmin"] += int(g_loc)
    print(f"      {kind:36s} scale {cs}: min L over all vertices {Lv[ibest]:.5f}, max {Lv.max():.5f}; best ordering vertex {Lord:.5f}; greedy {Lg:.5f}"
          f" ({'= best' if Lg <= Lv[ibest] + 1e-12 else 'NOT best'}; local minimum: {g_loc}); equal shares {I.UL(I.equal())[1]:.5f};"
          f" strict local minima among all {len(choices)} vertices: {nloc}")
check(stat["best_is_ordering"] == stat["inst"], "the best vertex for L is not an ordering vertex")
print(f"      -> the best vertex is an ordering vertex ('every constant to the first site of its T in one order of the sites') in {stat['best_is_ordering']} of"
      f" {stat['inst']} instances; greedy (frozen first) is the best vertex in {stat['greedy_is_best']}; greedy is a strict local minimum in {stat['greedy_locmin']}")
# equal constants + independent sites: frozen-first is the best ordering (rearrangement), many random p
okr = 0; nr = 0
for trial in range(200):
    n = int(rng.choice([5, 6])); m = int(rng.choice([2, 3]))
    p = rng.uniform(0.01, 0.6, n)
    I = site_instance(p, m, lambda T: 1.0 * cs, k=1) if False else site_instance(p, m, (lambda cc: (lambda T: cc))(float(rng.choice([0.05, 0.5, 2.0, 8.0]))), k=1)
    Lg = I.UL(I.vertex(I.greedy_choice()))[1]
    Lord = min(I.UL(I.vertex(I.order_choice(o)))[1] for o in itertools.permutations(range(n)))
    nr += 1; okr += int(Lg <= Lord + 1e-12)
check(okr == nr, "equal constants, independent sites: frozen-first is not the best ordering")
print(f"      equal constants on all m-subsets, independent sites, 200 random instances: the frozen-first order is the best of all n! ordering vertices in {okr} of {nr}")

# (c) first order; the formula with nested sets; ties
print("   (c) first order and the formula gamma_i = Gamma(R_i) - Gamma(R_i \\ {i})")
worst = 0.0; ratio_ok = True
for trial in range(20):
    n = 6; m = 3
    p = rng.uniform(0.02, 0.5, n)
    cT = {frozenset(T): float(rng.exponential(1.0)) for T in itertools.combinations(range(n), m)}
    I = Instance(n, m, 1, cT, product_law(p))
    gch = I.greedy_choice()
    g = I.charges(I.vertex(gch))
    order = sorted(range(n), key=lambda i: (p[i], i))
    pos = {i: r for r, i in enumerate(order)}
    Gam = lambda R: sum(v for T, v in cT.items() if T <= R)
    for i in range(n):
        Ri = frozenset(j for j in range(n) if pos[j] >= pos[i])
        worst = max(worst, abs(g[i] - (Gam(Ri) - Gam(Ri - {i}))))
    # first order: scale the constants down
    for scale in (1e-5,):
        lam = I.vertex(gch) * scale
        pen_ = I.pen(lam)
        u, l = math.log1p(float(I.law @ np.expm1(pen_))), -math.log1p(float(I.law @ np.expm1(-pen_)))
        first = float((lam * I.margK[I.subarr]).sum())
        ratio_ok &= abs(u / first - 1) < 1e-3 and abs(l / first - 1) < 1e-3
        fo_g = float(sum(c_ * min(p[list(T)]) for T, c_ in zip(I.Ts, I.c))) * scale
        ratio_ok &= abs(first - fo_g) < 1e-12 * first
        r_ = rng.dirichlet(np.ones(I.r), size=len(I.Ts)) * I.c[:, None] * scale
        ratio_ok &= float((r_ * I.margK[I.subarr]).sum()) >= first * (1 - 1e-12)
check(worst < 1e-12 and ratio_ok, "(c) formula / first order")
print(f"       with a linear order of the sites (ties broken by the order) and R_i = i and the sites after it: gamma_i = Gamma(R_i) - Gamma(R_i \\ {{i}}) is the"
      f" 'most frozen site' allocation exactly (largest error {worst:.1e}, 20 instances); to first order both ends are sum lam P(K in S), least at the greedy vertex: {ratio_ok}")
# ties read as 'p_j >= p_i'
p = [0.01] * 4 + [0.3] * 2; cval = 0.1
cT = {frozenset(T): cval for T in itertools.combinations(range(6), 3)}
Gam = lambda R: sum(v for T, v in cT.items() if T <= R)
g_tie = [Gam(frozenset(j for j in range(6) if p[j] >= p[i])) - Gam(frozenset(j for j in range(6) if p[j] >= p[i]) - {i}) for i in range(6)]
B6 = bits(6)
pen_tie = B6 @ np.array(g_tie)
u_tie, l_tie = UL(product_law(p), pen_tie)
print(f"       TIES: if R_i is read as 'the sites j with p_j >= p_i' on the first example (four tied frozen sites): gamma = {np.round(g_tie, 3).tolist()},"
      f" sum {sum(g_tie):.2f} against Gamma = {Gam(frozenset(range(6))):.2f}: every triple with two or three tied frozen sites is charged two or three times"
      f" (a valid cover, not an allocation): (U, L) = ({u_tie:.5f}, {l_tie:.5f})")

# ------------------------------------------------------------------ PART 3
print("PART 3  constants that are not small: the 'most frozen site' vertex against equal shares (independent sites, level 1)")
print("   notation: f_i = ln((1 - p_i)/p_i) free-energy cost of changing site i; gamma_i the penalty carried by site i;")
print("   U = sum_i [sp(gamma_i - f_i) - sp(-f_i)],  L = sum_i [sp(-f_i) - sp(-f_i - gamma_i)],  sp(z) = ln(1 + e^z)   (checked below)")
sp = lambda z: np.logaddexp(0.0, z)


def crit(I, p, lam):
    g = I.charges(lam)
    f = np.log((1 - p) / p)
    U_, L_ = I.UL(lam)
    check(abs(U_ - float((sp(g - f) - sp(-f)).sum())) < 1e-9 and abs(L_ - float((sp(-f) - sp(-f - g)).sum())) < 1e-9, "softplus forms of U, L")
    return g, f, U_, L_


print(f"   {'family':34s} {'scale':>6} | {'U equal':>9} {'U greedy':>9} {'U min':>9} | {'L equal':>9} {'L greedy':>9} {'L best ord':>10} | {'max(gamma_gr - f)':>17} {'KKT(U) at greedy':>16} {'cond B(i)':>9} {'cond B(iii)':>11}")
FAM = [("4 frozen (0.01) + 4 mobile (0.3)", np.array([0.01] * 4 + [0.3] * 4)),
       ("graded 0.01 .. 0.4", np.array([0.01, 0.02, 0.04, 0.08, 0.15, 0.25, 0.4, 0.4])),
       ("nearly homogeneous 0.05(1 + i/100)", np.array([0.05 * (1 + i / 100) for i in range(8)]))]
for fname, p in FAM:
    n, m = len(p), 3
    base = {frozenset(T): 1.0 for T in itertools.combinations(range(n), m)}
    for scale in (0.003, 0.01, 0.03, 0.1, 0.3, 1.0):
        I = Instance(n, m, 1, {T: v * scale for T, v in base.items()}, product_law(p))
        lam_e, lam_g = I.equal(), I.vertex(I.greedy_choice())
        ge, f, Ue, Le = crit(I, p, lam_e)
        gg, f, Ug, Lg = crit(I, p, lam_g)
        lamU, gap = I.min_U()
        Umin = I.UL(lamU)[0]
        Lord = min(I.UL(I.vertex(I.order_choice(o)))[1] for o in itertools.permutations(range(n))) if n <= 8 and scale in (0.01, 0.1, 1.0) else float("nan")
        gch = I.greedy_choice()
        kkt = all(f[s[gch[a]]] - gg[s[gch[a]]] >= max(f[j] - gg[j] for j in s) - 1e-12 for a, s in enumerate(I.sub))
        pplus = 1 / (1 + np.exp(f - gg))
        condBi = all(pplus[s[gch[a]]] <= np.mean([pplus[j] for j in s]) + 1e-15 for a, s in enumerate(I.sub))
        condBiii = all(f[s[gch[a]]] + ge[s[gch[a]]] >= max(f[j] + ge[j] for j in s) - 1e-12 for a, s in enumerate(I.sub))
        if kkt:
            check(abs(Ug - Umin) < 1e-7, "KKT holds at greedy but greedy is not the minimiser of U")
        else:
            check(Ug > Umin + 1e-12, "KKT fails at greedy but greedy is the minimiser")
        if condBi:
            check(Ug <= Ue + 1e-12, "condition B(i) holds but U(greedy) > U(equal)")
        if condBiii:
            check(Lg <= Le + 1e-12, "condition B(iii) holds but L(greedy) > L(equal)")
        print(f"   {fname:34s} {scale:>6} | {Ue:>9.5f} {Ug:>9.5f} {Umin:>9.5f} | {Le:>9.5f} {Lg:>9.5f} {Lord:>10.5f} | {float((gg - f).max()):>17.3f} {str(kkt):>16} {str(condBi):>9} {str(condBiii):>11}")
        if scale in (0.1, 0.3) and not fname.startswith("nearly"):
            gU = I.charges(lamU)
            print(f"        at the minimiser of U: penalties {np.round(gU, 2).tolist()}; f - gamma = {np.round(f - gU, 2).tolist()}   (greedy: f - gamma = {np.round(f - gg, 2).tolist()})")

# the star: L(greedy) > L(equal)
print("   a star of pairs (m = 2): d frozen leaves (p = 0.2) around one centre that is slightly more mobile (p = 0.2001); every pair {leaf, centre} has constant c")
for d, cval in ((4, 0.5), (6, 0.5), (12, 0.2), (12, 0.05), (40, 0.05)):
    n = d + 1
    p = np.array([0.2] * d + [0.2001])
    f = np.log((1 - p) / p)
    ell = lambda g, pp: -np.log1p(-pp * (-np.expm1(-g)))
    Lg = float(sum(ell(cval, p[i]) for i in range(d)))
    Le = float(ell(d * cval / 2, p[d]) + sum(ell(cval / 2, p[i]) for i in range(d)))
    Lc = float(ell(d * cval, p[d]))
    u_ = lambda g, pp: np.log1p(pp * np.expm1(g))
    Ug = float(sum(u_(cval, p[i]) for i in range(d))); Ue = float(u_(d * cval / 2, p[d]) + sum(u_(cval / 2, p[i]) for i in range(d)))
    print(f"      d = {d:3d}, c = {cval}: L greedy (all on the leaves) {Lg:.4f}, L equal {Le:.4f}, L all on the centre {Lc:.4f}: L greedy / L equal = {Lg / Le:.3f}"
          f" (bound m = 2);  U greedy {Ug:.4f}, U equal {Ue:.4f}")
    check(Lg <= 2 * Le + 1e-12, "L(vertex) <= m L(equal) violated on the star")
for d, cval in ((1000, 0.05), (10000, 0.01), (100000, 0.003)):
    ell = lambda g, pp: -np.log1p(-pp * (-np.expm1(-g)))
    Lg = d * float(ell(cval, 0.2)); Le = float(ell(d * cval / 2, 0.2001)) + d * float(ell(cval / 2, 0.2))
    print(f"      d = {d:6d}, c = {cval}: L greedy {Lg:.3f}, L equal {Le:.3f}: ratio {Lg / Le:.4f}  (closed form; the bound m = 2 is approached)")
    check(Lg <= 2 * Le, "L(vertex) <= m L(equal) violated on the large star")
# closed forms for a nearly homogeneous ensemble of n sites (independent, p_i = 0.05 (1 + i/1000)), triples, equal constants:
# greedy gamma_i = c C(n - 1 - i, 2), equal gamma_i = c C(n - 1, 2)/3
print("   nearly homogeneous ensembles, closed forms (p_i = 0.05(1 + i/1000), triples, equal constants c chosen so that U(equal) has the stated value):")
for n in (6, 12, 20, 30):
    pp = np.array([0.05 * (1 + i / 1000) for i in range(n)])
    for target in (0.05, 0.2, 1.0):
        lo_, hi_ = 0.0, 5.0
        for _ in range(200):
            mid = 0.5 * (lo_ + hi_)
            ue = float(np.log1p(pp * np.expm1(mid * math.comb(n - 1, 2) / 3)).sum())
            lo_, hi_ = (mid, hi_) if ue < target else (lo_, mid)
        cc = 0.5 * (lo_ + hi_)
        ge_ = np.full(n, cc * math.comb(n - 1, 2) / 3); gg_ = np.array([cc * math.comb(n - 1 - i, 2) for i in range(n)])
        Ue = float(np.log1p(pp * np.expm1(ge_)).sum()); Ug = float(np.log1p(pp * np.expm1(gg_)).sum())
        Le = float(-np.log1p(-pp * (-np.expm1(-ge_))).sum()); Lg = float(-np.log1p(-pp * (-np.expm1(-gg_))).sum())
        f0 = math.log(0.95 / 0.05)
        print(f"      n = {n:2d}: c = {cc:.5f}: U equal {Ue:.3f}, U greedy {Ug:.3f} (x {Ug / Ue:.2f}); L equal {Le:.4f}, L greedy {Lg:.4f};"
              f" largest greedy penalty {gg_[0]:.2f} against f = {f0:.2f}; equal penalty {ge_[0]:.2f}")

# random search
print("   random search (independent sites and general laws; levels 1 and 2; dense and sparse constants)")
st = dict(n=0, L_gr_gt_eq=0, max_L_ratio=0.0, max_U_ratio=0.0, max_U_diff=0.0, bound_viol=0, kkt_iff_viol=0, Bi_viol=0, Bii_viol=0, Biii_viol=0, Lany_ratio=0.0,
          bounds_viol=0, min_L_ratio=math.inf, kkt_tested=0, kkt_true=0, Bi_true=0, Bii_true=0, Biii_true=0)
for trial in range(600):
    n = int(rng.choice([5, 6, 7])); m = int(rng.choice([2, 3])); k = 1 if trial % 3 else 2
    if k >= m:
        k = 1                                                                     # k = m has one subset per T: nothing to allocate
    indep = (trial % 2 == 0)
    p = np.exp(rng.uniform(math.log(0.005), math.log(0.6), n))
    law = product_law(p) if indep else rng.dirichlet(np.ones(1 << n) * float(rng.choice([0.05, 0.3, 2.0])))
    scale = float(np.exp(rng.uniform(math.log(0.01), math.log(5.0))))
    dens = float(rng.choice([1.0, 0.5, 0.25]))
    cT = {frozenset(T): (float(rng.exponential(scale)) if rng.random() < dens else 0.0) for T in itertools.combinations(range(n), m)}
    if sum(cT.values()) == 0:
        continue
    I = Instance(n, m, k, cT, law)
    lam_e, lam_g = I.equal(), I.vertex(I.greedy_choice())
    Ue, Le = I.UL(lam_e); Ug, Lg = I.UL(lam_g)
    st["n"] += 1
    st["L_gr_gt_eq"] += int(Lg > Le * (1 + 1e-9))
    st["max_L_ratio"] = max(st["max_L_ratio"], Lg / Le); st["min_L_ratio"] = min(st["min_L_ratio"], Lg / Le)
    st["max_U_ratio"] = max(st["max_U_ratio"], Ug / Ue); st["max_U_diff"] = max(st["max_U_diff"], Ug - Ue)
    # L(any allocation) <= C(m, k) L(equal): any law, any level
    for _ in range(5):
        r_ = rng.dirichlet(np.ones(I.r) * float(rng.choice([0.1, 1.0])), size=len(I.Ts)) * I.c[:, None]
        Lr = I.UL(r_)[1]
        st["Lany_ratio"] = max(st["Lany_ratio"], Lr / Le / I.r)
        st["bound_viol"] += int(Lr > I.r * Le * (1 + 1e-9))
    st["bound_viol"] += int(Lg > I.r * Le * (1 + 1e-9))
    # first-order comparison conditions (any law): B(i), B(ii), B(iii) through the tilted probabilities
    gch = I.greedy_choice()
    tpg = I.tilted(lam_g, +1); tpe = I.tilted(lam_e, +1); tme = I.tilted(lam_e, -1)
    Bi = all(tpg[s[gch[a]]] <= np.mean([tpg[j] for j in s]) + 1e-15 for a, s in enumerate(I.sub))
    Bii = sum(I.c[a] * (tpe[s[gch[a]]] - np.mean([tpe[j] for j in s])) for a, s in enumerate(I.sub)) >= -1e-15
    Biii = all(tme[s[gch[a]]] <= min(tme[j] for j in s) + 1e-15 for a, s in enumerate(I.sub))
    st["Bi_true"] += int(Bi); st["Bii_true"] += int(bool(Bii)); st["Biii_true"] += int(Biii)
    st["Bi_viol"] += int(Bi and Ug > Ue + 1e-10)
    st["Bii_viol"] += int(Bii and Ug < Ue - 1e-10)
    st["Biii_viol"] += int(Biii and Lg > Le + 1e-10)
    if indep and k == 1:
        g = I.charges(lam_g); f = np.log((1 - p) / p)
        kkt = all(f[s[gch[a]]] - g[s[gch[a]]] >= max(f[j] - g[j] for j in s) - 1e-10 for a, s in enumerate(I.sub))
        lamU, gap = I.min_U()
        Umin = I.UL(lamU)[0]
        st["kkt_tested"] += 1; st["kkt_true"] += int(kkt)
        if kkt and abs(Ug - Umin) > 1e-6 * max(1, Ug):
            st["kkt_iff_viol"] += 1
        if (not kkt) and Ug <= Umin + 1e-10 and gap < 1e-9:
            # KKT can fail by a margin too small to matter numerically only if the gap is tiny; count otherwise
            margin = max(max(f[j] - g[j] for j in s) - (f[s[gch[a]]] - g[s[gch[a]]]) for a, s in enumerate(I.sub))
            st["kkt_iff_viol"] += int(margin > 1e-6)
        # site-wise bounds
        u = np.log1p(p * np.expm1(g)); l = -np.log1p(-p * (-np.expm1(-g)))
        okb = (u >= np.maximum(p * g, g - np.log(1 / p)) - 1e-12).all() and (u <= p * np.expm1(g) + 1e-12).all() and (l <= np.minimum(p * g, -np.log1p(-p)) + 1e-12).all()
        st["bounds_viol"] += int(not okb)
check(st["bound_viol"] == 0 and st["kkt_iff_viol"] == 0 and st["Bi_viol"] == 0 and st["Bii_viol"] == 0 and st["Biii_viol"] == 0 and st["bounds_viol"] == 0,
      f"random search: {st}")
print(f"      {st['n']} instances: L(greedy) > L(equal) in {st['L_gr_gt_eq']}; L(greedy)/L(equal) between {st['min_L_ratio']:.4f} and {st['max_L_ratio']:.4f};"
      f" largest L(random allocation)/(C(m,k) L(equal)) = {st['Lany_ratio']:.4f} (bound 1; violations {st['bound_viol']})")
print(f"      U(greedy)/U(equal) up to {st['max_U_ratio']:.2f}, U(greedy) - U(equal) up to {st['max_U_diff']:.2f} nats (no bound exists)")
print(f"      violations: KKT-iff for U at the greedy vertex {st['kkt_iff_viol']}; condition B(i) => U(gr) <= U(eq): {st['Bi_viol']}; B(ii) => U(gr) >= U(eq): {st['Bii_viol']};"
      f" B(iii) => L(gr) <= L(eq): {st['Biii_viol']}; site-wise bounds on u_i, l_i: {st['bounds_viol']}")
print(f"      how often the tests were non-vacuous: the KKT-iff and the site-wise bounds were tested on the {st['kkt_tested']} instances with independent sites and level 1"
      f" (the condition held in {st['kkt_true']} of them); the hypotheses of B(i), B(ii), B(iii) held in {st['Bi_true']}, {st['Bii_true']}, {st['Biii_true']} of the {st['n']} instances")

print("ALL CHECKS PASSED" if ok_all else "SOME CHECK FAILED")
print(f"seconds {time.time() - t0:.1f}")
print("peak RSS MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
