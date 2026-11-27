#!/usr/bin/env python3
"""R15 -- three small additional checks (own code).

E1 (Item 1, last sentence of Proposition 11.18e(b')(i)).  For grids with k_i states and an order m, the functions of
   order below m restricted to a fixed unisolvent set B (the Hamming ball of radius m - 1 around a reference, or any
   other set of N_ball points with an invertible evaluation matrix) are ALL functions on B: for every a in B there is a
   function h_a of order below m with h_a = 1_a on B.  Hence an algorithm that evaluates only inside B and leaves a
   unevaluated has the same run on g and on g + t h_a, and min(E0 + g + t h_a) <= E0(a) + g(a) + t -> -infinity as
   t -> -infinity: the argument of (i) with h_a in place of a needle.  Checked: unisolvence, h_a|_B = 1_a, agreement of
   g + t h_a with g on B \\ {a}.
E2 (Item 2).  Level 2: the best vertex for L is an ordering vertex of the pairs (n = 4, triples, pairs: 81 vertices,
   720 orders), for product and non-product laws.
E3 (Item 2).  One pair of nearly tied sites, c = 2 ln(1/p): U(most frozen site) ~ ln(1/p) against U(equal) = 2 ln(2 - p):
   no bound of U(greedy) by a multiple of U(equal).

Run:  OMP_NUM_THREADS=1 python3 r15_extras.py > logs/extras.log
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


print("E1  unisolvent sets and their Lagrange functions of order below m")
rng = np.random.default_rng(31)
for ks, m in (((2, 2, 2), 2), ((2, 2, 2), 3), ((2, 2, 3), 2), ((2, 2, 3), 3), ((3, 3, 2), 2), ((3, 3, 2), 3), ((2, 2, 2, 2), 2), ((2, 2, 2, 2), 3),
              ((3, 2, 2, 2), 3), ((4, 3), 2)):
    n = len(ks)
    confs = list(itertools.product(*[range(k) for k in ks]))
    basis = [(U, a) for j in range(m) for U in itertools.combinations(range(n), j) for a in itertools.product(*[range(1, ks[i]) for i in U])]
    M = np.array([[1.0 if all(x[i] == s for i, s in zip(U, a)) else 0.0 for (U, a) in basis] for x in confs])     # |X| x N_ball
    nball = len(basis)
    for ref_trial in range(3):
        ref = confs[int(rng.integers(len(confs)))] if ref_trial else confs[0]
        B = [i for i, x in enumerate(confs) if sum(1 for u, v in zip(x, ref) if u != v) < m]
        check(len(B) == nball, "size of the ball is not the dimension")
        MB = M[B]
        check(np.linalg.matrix_rank(MB) == nball, f"the ball is not unisolvent: {ks}, m = {m}")
        H = M @ np.linalg.inv(MB)                                    # column j: the function of order below m equal to 1 at B[j], 0 on the rest of B
        check(np.abs(H[B] - np.eye(nball)).max() < 1e-9, "Lagrange functions")
        g = rng.normal(0, 1, len(confs)); E0 = rng.normal(0, 1, len(confs))
        j = int(rng.integers(nball))
        for t in (-10.0, -1e3, -1e6):
            g2 = g + t * H[:, j]
            rest = [b for b in B if b != B[j]]
            check(np.abs(g2[rest] - g[rest]).max() < 1e-6 * max(1, abs(t)) * 1e-3 + 1e-9, "g + t h_a differs from g on B without a")
            check((E0 + g2).min() <= E0[B[j]] + g[B[j]] + t + 1e-6, "the minimum does not follow the needle on the ball")
    # another unisolvent set: random points with an invertible evaluation matrix
    for _ in range(200):
        Br = sorted(rng.choice(len(confs), size=nball, replace=False).tolist())
        if abs(np.linalg.det(M[Br])) > 1e-6:
            H = M @ np.linalg.inv(M[Br])
            check(np.abs(H[Br] - np.eye(nball)).max() < 1e-8, "Lagrange functions on a random unisolvent set")
            break
    print(f"   grid {ks}, m = {m}: N_ball = {nball} of {len(confs)} points; balls around 3 references unisolvent; Lagrange functions exist; "
          f"largest |h_a| off the ball {float(np.abs(M @ np.linalg.inv(M[B])).max()):.1f}")

print("E2  level 2: the best vertex for L is an ordering vertex of the pairs (n = 4, m = 3, k = 2)")
n, m, k = 4, 3, 2
Ts = [frozenset(T) for T in itertools.combinations(range(n), m)]
Ks = [frozenset(K) for K in itertools.combinations(range(n), k)]
kidx = {K: j for j, K in enumerate(Ks)}
S = np.arange(1 << n)
I = np.zeros((1 << n, len(Ks)))
for j, K in enumerate(Ks):
    mk = sum(1 << i for i in K)
    I[:, j] = ((S & mk) == mk)
sub = [[kidx[frozenset(K)] for K in itertools.combinations(sorted(T), k)] for T in Ts]
good = 0; tot = 0; nonord = 0
for trial in range(40):
    if trial % 2:
        law = rng.dirichlet(np.ones(1 << n) * 0.5)
    else:
        p = rng.uniform(0.05, 0.6, n)
        Bn = ((S[:, None] >> np.arange(n)[None, :]) & 1)
        law = np.prod(np.where(Bn > 0, p[None, :], 1 - p[None, :]), axis=1)
    c = rng.exponential(float(rng.choice([0.3, 1.0, 4.0])), len(Ts))

    def L_of(choice):
        g = np.zeros(len(Ks))
        for t, a in enumerate(choice):
            g[sub[t][a]] += c[t]
        return -math.log(float(law @ np.exp(-I @ g)))

    allv = {ch: L_of(ch) for ch in itertools.product(range(3), repeat=len(Ts))}
    best = min(allv.values())
    ordv = set()
    for order in itertools.permutations(range(len(Ks))):
        pos = {j: r for r, j in enumerate(order)}
        ordv.add(tuple(min(range(3), key=lambda a: pos[sub[t][a]]) for t in range(len(Ts))))
    best_ord = min(allv[ch] for ch in ordv)
    tot += 1; good += int(abs(best - best_ord) < 1e-12); nonord = len(allv) - len(ordv)
check(good == tot, "level 2: best vertex is not an ordering vertex")
print(f"   {tot} instances (product and non-product laws): the minimum of L over all 81 vertices is attained at an ordering vertex in {good}; "
      f"{81 - nonord} of the 81 vertices are ordering vertices")

print("E3  one pair of nearly tied sites, c = 2 ln(1/p): the most frozen site against equal shares at the upper end")
for p in (0.1, 0.01, 1e-3, 1e-6):
    c = 2 * math.log(1 / p)
    Ug = math.log1p(p * math.expm1(c))
    Ue = 2 * math.log1p(p * math.expm1(c / 2))
    Lg = -math.log1p(-p * (-math.expm1(-c))); Le = -2 * math.log1p(-p * (-math.expm1(-c / 2)))
    print(f"   p = {p:g}: U(vertex) = {Ug:.3f} (ln(1/p) = {math.log(1 / p):.3f}), U(equal) = {Ue:.3f} (2 ln(2 - p) = {2 * math.log(2 - p):.3f}), ratio {Ug / Ue:.2f};"
          f"  L(vertex) = {Lg:.2e}, L(equal) = {Le:.2e}, ratio {Lg / Le:.3f} (bound m = 2 for the lower end)")
    check(Lg <= 2 * Le, "L bound")

print("E4  (THY-RES-0012 section 3.2 item 3) level 2, independent sites: 'the two most frozen sites of T, a second difference'")
worst = 0.0
for trial in range(20):
    n = int(rng.choice([5, 6, 7])); m = int(rng.choice([3, 4]))
    p = rng.uniform(0.02, 0.6, n)
    order = sorted(range(n), key=lambda i: (p[i], i)); pos = {i: r for r, i in enumerate(order)}
    cT = {frozenset(T): float(rng.exponential(1.0)) for T in itertools.combinations(range(n), m)}
    Gam = lambda R: sum(v for T, v in cT.items() if T <= R)
    direct = {}
    for T, v in cT.items():
        two = frozenset(sorted(T, key=lambda i: pos[i])[:2])
        direct[two] = direct.get(two, 0.0) + v
    for i, j in itertools.combinations(range(n), 2):
        a, b = (i, j) if pos[i] < pos[j] else (j, i)                      # a more frozen than b
        after = frozenset(x for x in range(n) if pos[x] > pos[b])
        second = Gam(after | {a, b}) - Gam(after | {a}) - Gam(after | {b}) + Gam(after)
        worst = max(worst, abs(second - direct.get(frozenset((i, j)), 0.0)))
    # the least probable pair of T is the pair of its two most frozen sites
    for T in cT:
        best = min(itertools.combinations(sorted(T), 2), key=lambda K: p[K[0]] * p[K[1]])
        check(frozenset(best) == frozenset(sorted(T, key=lambda i: pos[i])[:2]), "least probable pair is not the two most frozen sites")
    # every allocation of level k has the mean penalty sum_K g_K P(K in S); with a common p it is p^k Gamma whatever the allocation
check(worst < 1e-10, "second difference formula")
print(f"   gamma_ab = Gamma(A + a + b) - Gamma(A + a) - Gamma(A + b) + Gamma(A), A the sites after b in the order: largest error {worst:.1e} over 20 instances")

print("E5  every allocation covers: pen_lam(S) >= sum of c_T over the T inside S, for every changed set S (levels 1, 2, 3)")
worst = math.inf; ncase = 0; eq_full = 0.0
for trial in range(60):
    n = int(rng.choice([5, 6, 7])); m = int(rng.choice([3, 4])); k = int(rng.choice([1, 2, 3]))
    Tsm = [frozenset(T) for T in itertools.combinations(range(n), m)]
    cc = {T: (float(rng.exponential(1.0)) if rng.random() < 0.8 else 0.0) for T in Tsm}
    lam = {}
    for T in Tsm:
        Ksub = [frozenset(K) for K in itertools.combinations(sorted(T), k)]
        wts = rng.dirichlet(np.ones(len(Ksub)) * float(rng.choice([0.1, 1.0])))
        for K, wv in zip(Ksub, wts):
            lam[(T, K)] = cc[T] * float(wv)
    for mask in range(1 << n):
        Sset = frozenset(i for i in range(n) if (mask >> i) & 1)
        pen = sum(v for (T, K), v in lam.items() if K <= Sset)
        env = sum(v for T, v in cc.items() if T <= Sset)
        worst = min(worst, pen - env)
        if mask == (1 << n) - 1:
            eq_full = max(eq_full, abs(pen - env))
    ncase += 1
check(worst > -1e-12 and eq_full < 1e-9, "an allocation does not cover")
print(f"   {ncase} random allocations (n = 5..7, m = 3, 4, k = 1, 2, 3): least pen - envelope over all changed sets {worst:.1e} (zero up to rounding at the set of all sites, positive elsewhere or zero); equality at the set of all sites to {eq_full:.1e}")

print("ALL CHECKS PASSED" if ok_all else "SOME CHECK FAILED")
print(f"seconds {time.time() - t0:.1f}")
print("peak RSS MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
