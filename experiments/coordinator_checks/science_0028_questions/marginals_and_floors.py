"""Coordinator's checks for the answer to two questions of SCI-MSG-0028 (A19-T2, P9-T2).  Seeded; exact enumeration.

A19-T2.  Laws of S_1..S_G >= 0 known, joint law unknown; S = sum_g S_g, prod_g e^{+-beta S_g} = e^{+-beta S}.
 (1) sup over couplings of E e^{beta S} and of E e^{-beta S}: the comonotone coupling (both are convex functions of the
     sum; products of similarly ordered non-negative sequences are maximal).  Check: equal-weight atoms, random
     permutations never exceed the sorted alignment.
 (2) inf over couplings of E prod_g (1 + y_g), y_g = e^{beta S_g} - 1 >= 0: the bound 1 + sum_g E y_g is attained iff the
     events {S_g > 0} can be made disjoint, i.e. sum_g P(S_g > 0) <= 1.  Check: the mutually exclusive coupling attains
     it; when the sum of probabilities exceeds one, an exhaustive search over couplings (small cases) stays above it.
 (3) With the joint law of some pairs: E prod (1 + y_g) >= 1 + sum E y_g + sum_{pairs} E[y_g y_g'] (all terms >= 0).
P9-T2.  A floor with penalties reduced to fewer sites is pointwise smaller, so its partition function is larger: the
     cheap floor's ln Z bounds the expensive one's from above.  Check on a toy chain: window tables gamma_U(x_U) >= 0
     vanishing when a site of U is at the anchor, reduced to site tables c_i(x_i) = sum_{U ni i} max gamma_U / |U|;
     and the generalised Hoelder (Finner) bound for a product reference measure,
         ln < prod_U e^{beta gamma_U} >  <=  sum_U (1/p_U) ln < e^{p_U beta gamma_U} >   if  sum_{U ni i} 1/p_U <= 1 for all i.
"""
import itertools, math, random
import numpy as np

rng = random.Random(20261126)
nprng = np.random.default_rng(20261126)

# ---------- A19-T2 (1): comonotone alignment maximises E e^{+-beta S}
viol = 0
worst = 0.0
for trial in range(2000):
    G, N = rng.randint(2, 5), rng.randint(3, 7)
    beta = rng.choice([0.3, 1.0, 2.5])
    atoms = [sorted(max(0.0, rng.gauss(0.2, 1.0)) for _ in range(N)) for _ in range(G)]
    for sign in (+1, -1):
        como = sum(math.exp(sign * beta * sum(atoms[g][t] for g in range(G))) for t in range(N)) / N
        for _ in range(60):
            perms = [list(range(N))] + [rng.sample(range(N), N) for _ in range(G - 1)]
            val = sum(math.exp(sign * beta * sum(atoms[g][perms[g][t]] for g in range(G))) for t in range(N)) / N
            if val > como * (1 + 1e-12):
                viol += 1
            worst = max(worst, val / como)
print("(1) comonotone coupling is the maximum of E e^{+-beta S}: violations %d in 240000 couplings; largest ratio %.12f" % (viol, worst))

# ---------- A19-T2 (2): 1 + sum E y_g attained iff sum_g P(S_g > 0) <= 1
def min_coupling_two_point(ps, ys, N):
    """exhaustive minimum of E prod (1 + y_g 1_{A_g}) over couplings of events with P(A_g) = k_g/N on N equally likely atoms."""
    ks = [round(p * N) for p in ps]
    best = float("inf")
    first = tuple(range(ks[0]))
    for rest in itertools.product(*[itertools.combinations(range(N), k) for k in ks[1:]]):
        sets = [set(first)] + [set(r) for r in rest]
        val = 0.0
        for t in range(N):
            pr = 1.0
            for g, A in enumerate(sets):
                if t in A:
                    pr *= 1 + ys[g]
            val += pr
        best = min(best, val / N)
    return best

rows = []
for ks in [(2, 2, 2), (3, 3, 2), (3, 3, 3), (4, 3, 3), (4, 4, 4), (6, 5, 4)]:
    N = 8
    ps = [k / N for k in ks]
    ys = [0.7, 1.3, 0.4]
    lin = 1 + sum(p * y for p, y in zip(ps, ys))
    mn = min_coupling_two_point(ps, ys, N)
    rows.append((ps, sum(ps), lin, mn))
    print("(2) P(S_g>0) = %s  sum = %.3f   1 + sum E y_g = %.6f   exact minimum over couplings = %.6f   %s" %
          (ps, sum(ps), lin, mn, "attained" if abs(mn - lin) < 1e-12 else "NOT attained (minimum is larger by %.4f)" % (mn - lin)))
assert all((abs(mn - lin) < 1e-12) == (sp <= 1 + 1e-12) for _, sp, lin, mn in rows)

# ---------- A19-T2 (3): second-order terms from pairs with known joint law
bad = 0
for trial in range(20000):
    G = rng.randint(2, 6)
    N = 12
    y = nprng.exponential(0.5, size=(G, N)) * (nprng.random((G, N)) < 0.4)
    full = float(np.mean(np.prod(1 + y, axis=0)))
    known = [(g, g2) for g in range(G) for g2 in range(g + 1, G) if rng.random() < 0.5]
    lb = 1 + float(np.sum(np.mean(y, axis=1))) + sum(float(np.mean(y[g] * y[g2])) for g, g2 in known)
    if lb > full * (1 + 1e-12):
        bad += 1
print("(3) 1 + sum E y_g + sum_{known pairs} E[y_g y_g'] <= E prod (1 + y_g): violations %d in 20000" % bad)

# ---------- P9-T2: reduced floors bound the window floor; Finner bound for a product reference
def toy(n, q, w, m, scale):
    """n sites, q states (0 = anchor), product reference pi_i; window tables on m-subsets of diameter <= w."""
    pi = nprng.dirichlet(np.ones(q) * 0.7, size=n)
    pi[:, 0] += 1.0
    pi /= pi.sum(axis=1, keepdims=True)
    Us = [U for U in itertools.combinations(range(n), m) if U[-1] - U[0] <= w]
    tabs = {}
    for U in Us:
        t = nprng.exponential(scale, size=(q,) * m)
        idx = np.indices((q,) * m)
        t[np.any(idx == 0, axis=0)] = 0.0                   # zero when a site of U is at the anchor
        tabs[U] = t
    return pi, Us, tabs

def exact_ln_mean(pi, Us, tabs, beta, n, q):
    tot = 0.0
    for x in itertools.product(range(q), repeat=n):
        wgt = 1.0
        for i in range(n):
            wgt *= pi[i, x[i]]
        tot += wgt * math.exp(beta * sum(tabs[U][tuple(x[i] for i in U)] for U in Us))
    return math.log(tot)

viol_site = viol_fin = 0
print("(P9-T2) toy chains, product reference:  beta  ln<e^{beta sum gamma}> exact   site-reduced floor   Finner bound   first order beta<sum gamma>")
for trial in range(12):
    n, q, w, m = 7, 3, 3, 3
    scale = [0.05, 0.2, 0.6, 1.5][trial % 4]
    pi, Us, tabs = toy(n, q, w, m, scale)
    beta = 1.0
    ex = exact_ln_mean(pi, Us, tabs, beta, n, q)
    # site reduction: c_i(x_i) = sum_{U ni i} max_{y: y_i = x_i} gamma_U(y) / |U|
    c = np.zeros((n, q))
    for U in Us:
        for pos, i in enumerate(U):
            mx = np.max(np.moveaxis(tabs[U], pos, 0).reshape(q, -1), axis=1)
            c[i] += mx / m
    site = sum(math.log(sum(pi[i, s] * math.exp(beta * c[i, s]) for s in range(q))) for i in range(n))
    # Finner with p_U = d = the largest number of tables through one site
    d = max(sum(1 for U in Us if i in U) for i in range(n))
    fin = 0.0
    first = 0.0
    for U in Us:
        mean_p = 0.0
        mean_1 = 0.0
        for xs in itertools.product(range(q), repeat=m):
            wgt = 1.0
            for pos, i in enumerate(U):
                wgt *= pi[i, xs[pos]]
            mean_p += wgt * math.exp(d * beta * tabs[U][xs])
            mean_1 += wgt * tabs[U][xs]
        fin += math.log(mean_p) / d
        first += beta * mean_1
    viol_site += ex > site + 1e-12
    viol_fin += ex > fin + 1e-12
    print("        scale %.2f  %4.1f   %10.5f   %10.5f   %10.5f   %10.5f" % (scale, beta, ex, site, fin, first))
print("(P9-T2) exact <= site-reduced floor: violations %d of 12;  exact <= Finner bound: violations %d of 12" % (viol_site, viol_fin))
