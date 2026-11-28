#!/usr/bin/env python3
"""Phase II -- exact small-cube checks of the statements of docs/phase2/PHASE2_REPORT.md.

Everything here is exact enumeration over {0,1}^n (n <= 10) in double precision, or a
closed-form evaluation; each check prints PASS/FAIL and the script exits non-zero on a
failure.  Sections follow the report: A (noisy observations), B (exact observables),
C (sharpness), D (deterministic algorithms), E (exponent functions).

Run:  python3 -B experiments/phase2/p2_checks.py            (about 20 s, < 300 MB)
"""
import itertools, math, sys
import numpy as np

rng = np.random.default_rng(20261128)
FAILS = []

def check(name, ok, info=""):
    print(("PASS  " if ok else "FAIL  ") + name + ("   " + info if info else ""))
    if not ok:
        FAILS.append(name)

def cube(n):
    N = 1 << n
    idx = np.arange(N)
    D = np.zeros((N, N), dtype=np.int16)
    x = idx[:, None] ^ idx[None, :]
    for i in range(n):
        D += (x >> i) & 1
    return N, idx, D

def weight(idx, n):
    return sum(((idx >> i) & 1) for i in range(n))

def admissible(w, n, u, tol=1e-12):
    """w(x) <= e^u w(y) for all Hamming neighbours (equivalent to the cone condition)."""
    N = len(w); idx = np.arange(N)
    for i in range(n):
        y = idx ^ (1 << i)
        if np.any(w > math.exp(u) * w[y] * (1 + tol)):
            return False
    return True

def random_admissible(n, u, D, k=6):
    """exp(-psi), psi = u * (a random 1-Lipschitz function: min of distances plus offsets)."""
    N = D.shape[0]
    cs = rng.integers(0, N, size=k)
    off = rng.uniform(0, n / 2, size=k)
    f = np.min(D[:, cs] + off[None, :], axis=1)
    sgn = rng.choice([-1.0, 1.0])
    return np.exp(-u * sgn * f)

# ----------------------------------------------------------------------------- A
print("== A. noisy observations: translation averaging and the flat mixture ==")
n, u = 8, 1.0
N, idx, D = cube(n)
pi_u = np.full(N, 1.0 / N)

# A1: cone is convex, translation invariant; averaging preserves A; ensemble = mixture
w = random_admissible(n, u, D)
cs = rng.integers(0, N, size=5)
lam = rng.dirichlet(np.ones(5))
wbar = sum(l * w[idx ^ c] for l, c in zip(lam, cs))
check("A1a admissible weights: random instance, translate, convex combination",
      admissible(w, n, u) and admissible(w[idx ^ cs[0]], n, u) and admissible(wbar, n, u))
A = w.mean()
check("A1b translation average preserves the partition function", abs(wbar.mean() - A) < 1e-12 * A)
phi = rng.uniform(-1, 1, size=N)
lhs = (wbar * phi).mean() / wbar.mean()
rhs = sum(l * (w[idx ^ c] * phi).mean() / A for l, c in zip(lam, cs))
check("A1c ensemble of the average = average of the translated ensembles", abs(lhs - rhs) < 1e-12)
full = sum(w[idx ^ c] for c in range(N)) / N
check("A1d average over all translations is the constant A", np.allclose(full, A, rtol=1e-12))
allmean = np.mean([(w[idx ^ c] * phi).mean() / A for c in range(N)])
check("A1e mean over a uniform translation of E_mu[phi] is the uniform mean of phi",
      abs(allmean - phi.mean()) < 1e-12)

# A2: flat mixture for an ARBITRARY reference measure pi
pi = rng.dirichlet(np.full(N, 0.3))
K = np.exp(-u * D.astype(float))                     # K[x, c] = e^{-u d(x,c)}
S0 = K.sum(axis=1)
check("A2a row sums of the kernel are constant", np.allclose(S0, S0[0], rtol=1e-12),
      "Sigma_0 = (1+e^-u)^n = %.6f" % S0[0])
m = pi @ K                                           # m[c] = E_pi K(., c)
q = m / S0[0]
check("A2b the hiding law q = pi * K_u / Sigma_0 is a probability vector", abs(q.sum() - 1) < 1e-12)
eps0 = 0.7
Hc = eps0 / m
flat = (K * (q * Hc)[None, :]).sum(axis=1)
check("A2c flat mixture: sum_c q(c) H(c) e^{-u d(x,c)} = eps0 for every x",
      np.allclose(flat, eps0, rtol=1e-12))
Wc = np.maximum(1.0, K * Hc[None, :])                # Wc[x, c] = w_c(x)
check("A2d every member max(1, H(c) K_c) is admissible",
      all(admissible(Wc[:, c], n, u) for c in range(0, N, 17)))
delta_tr = (np.minimum(1.0, K * Hc[None, :]) * q[None, :]).sum(axis=1)
xi = float(pi @ delta_tr)
winf = (Wc * q[None, :]).sum(axis=1)
check("A2e mixture of the truncated members = 1 + eps0 - delta_tr", np.allclose(winf, 1 + eps0 - delta_tr))
mu_inf = pi * winf / (pi @ winf)
tv = 0.5 * np.abs(mu_inf - pi).sum()
check("A2f TV(ensemble of the full mixture, pi) <= xi/(1+eps0-xi)", tv <= xi / (1 + eps0 - xi) + 1e-12,
      "TV = %.3e, bound = %.3e (this pi is far from uniform; n = 8)" % (tv, xi / (1 + eps0 - xi)))

# A3: Hoeffding for L random translates on the uniform cube (constant baseline versus dip)
n3, u3 = 10, 1.0
N3, idx3, D3 = cube(n3)
r = 5
dip = np.maximum(1.0, np.exp(u3 * (r - D3[:, 0].astype(float))))    # dip of radius r at 0
A3 = dip.mean()
M, L, tau, trials = 40, 300, 0.25, 400
phis = rng.choice([-1.0, 1.0], size=(M, N3))
phis[0] = 1 - 2 * ((idx3 >> 0) & 1)                    # a dictator: the worst kind of observable
phibar = phis.mean(axis=1)
G = np.empty((M, N3))                                  # G[i, c] = E_{mu_{w_c}} phi_i
for c in range(N3):
    G[:, c] = (phis[:, idx3 ^ c] * dip[None, :]).mean(axis=1) / A3
check("A3a E_c E_{mu_c} phi = uniform mean, all observables", np.allclose(G.mean(axis=1), phibar, atol=1e-12))
width = 2 * (1 - 1 / A3)
check("A3b range of E_{mu_c} phi has width <= 2(1 - 1/A)", np.all(G.max(axis=1) - G.min(axis=1) <= width + 1e-12),
      "A = %.4f" % A3)
bad = 0
for _ in range(trials):
    c = rng.integers(0, N3, size=L)
    dev = np.abs(G[:, c].mean(axis=1) - phibar)
    bad += np.any(dev > tau)
bound = 2 * M * math.exp(-2 * L * tau ** 2 / width ** 2)
check("A3c observed failure frequency <= Hoeffding + union bound", bad / trials <= bound + 3 * math.sqrt(bound / trials) + 1e-9,
      "observed %.4f, bound %.4f (L = %d, tau = %.2f, M = %d)" % (bad / trials, bound, L, tau, M))
Lmin = math.ceil(2 * tau ** -2 * math.log(2 * M / 0.1))
check("A3d L >= 2 tau^-2 ln(2M/eta) makes the bound <= eta", 2 * M * math.exp(-Lmin * tau ** 2 / 2) <= 0.1 + 1e-12)

# A4: maximum of narrow dips: admissible, mass >= sum - pair overlaps, expected overlap bound
Lc, rn = 6, 3
cs = rng.integers(0, N3, size=Lc)
E = np.maximum(0.0, np.exp(u3 * (rn - D3[:, cs].astype(float))) - 1.0)    # excesses e_c(x)
wmax = 1.0 + E.max(axis=1)
check("A4a maximum of dips is admissible", admissible(wmax, n3, u3))
pair = sum(np.minimum(E[:, i], E[:, j]).mean() for i in range(Lc) for j in range(i))
check("A4b sum - pair overlaps <= max <= sum (masses)",
      E.sum(axis=1).mean() - pair - 1e-12 <= E.max(axis=1).mean() <= E.sum(axis=1).mean() + 1e-12)
e0 = np.maximum(0.0, np.exp(u3 * (rn - D3[:, 0].astype(float))) - 1.0)
m_r, V = e0.mean(), np.count_nonzero(D3[:, 0] < rn)
exp_pair = np.mean([np.minimum(e0, e0[idx3 ^ c]).mean() for c in range(N3)])
check("A4c expected pair overlap <= m(r) V(n,r-1)/2^n", exp_pair <= m_r * V / N3 + 1e-15,
      "%.3e <= %.3e" % (exp_pair, m_r * V / N3))

# A4d-g: Lemma 2.5 (iv) and the two probabilistic steps of Theorem A' (the form with bounded differences),
# by EXACT enumeration of all L-tuples of centres on small cubes: for centred psi the bias functional
# G(c) = E_pi[(w_c - 1) psi] has mean zero (overlaps included); one centre moves it by at most (sup psi - inf psi) m_r;
# its exact tails are below McDiarmid's bound; P(O_c >= R/2) <= (L-1) V / 2^n.
def all_tuples_max(n_, r_, L_, u_):
    N_ = 1 << n_
    wt_ = np.array([bin(x).count("1") for x in range(N_)])
    e_ = np.where(wt_ < r_, np.exp(u_ * (r_ - wt_)) - 1.0, 0.0)
    Em = e_[np.bitwise_xor.outer(np.arange(N_), np.arange(N_))]              # Em[x, c] = e_r(x xor c)
    parts = [Em.reshape((N_,) + tuple(N_ if i == j else 1 for i in range(L_))) for j in range(L_)]
    W = parts[0]
    for q in parts[1:]:
        W = np.maximum(W, q)                                                 # (w_c - 1)(x), all tuples c
    Opair = sum(np.minimum(parts[i], parts[j]).mean(axis=0) for i in range(L_) for j in range(i))
    Opair = np.broadcast_to(Opair, (N_,) * L_)
    return N_, wt_, e_.mean(), int((wt_ < r_).sum()), W, Opair
okd = oke = okf = okg = True
worst_ratio = 0.0
for (n4, r4, L4, u4) in [(5, 2, 3, 1.0), (6, 2, 2, 1.0), (4, 3, 4, 1.5), (5, 3, 3, 0.7)]:
    N4, wt4, m4, V4, W4, O4 = all_tuples_max(n4, r4, L4, u4)
    R4 = L4 * m4
    okg &= (O4 >= R4 / 2 - 1e-15).mean() <= (L4 - 1) * V4 / N4 + 1e-12
    okg &= bool(np.all(W4.mean(axis=0) >= R4 - O4 - 1e-12))                  # A(w_c) - 1 >= R - O_c for EVERY tuple
    for phi4 in (rng.choice([-1.0, 1.0], size=N4), rng.uniform(-1, 1, size=N4),
                 np.array([1.0 if x & 1 else -1.0 for x in range(N4)]), np.where(wt4 <= n4 // 2 - 1, 1.0, -1.0)):
        psi4 = phi4 - phi4.mean()
        G4 = np.tensordot(psi4, W4, axes=(0, 0)) / N4                        # G(c) for all tuples
        d4 = (psi4.max() - psi4.min()) * m4                                  # the oscillation of the observable times m_r
        okd &= abs(G4.mean()) < 1e-12 * max(1.0, m4)
        osc = (G4.max(axis=-1) - G4.min(axis=-1)).max()                      # one centre (the last; symmetric)
        oke &= osc <= d4 + 1e-12
        worst_ratio = max(worst_ratio, osc / d4)
        for t4 in (0.5, 1.0, 1.5, 2.0, 3.0):
            tt = t4 * math.sqrt(L4) * d4 / 2
            okf &= (np.abs(G4) >= tt - 1e-15).mean() <= 2 * math.exp(-2 * tt * tt / (L4 * d4 * d4)) + 1e-12
check("A4d Lemma 2.5(iv): E_c E_pi[(w_c - 1) psi] = 0 for centred psi, all tuples of centres, overlaps included", okd)
check("A4e Lemma 2.5(iv): one centre moves E_pi[(w_c - 1) psi] by at most (sup psi - inf psi) m_r", oke,
      "largest observed change / bound = %.3f" % worst_ratio)
check("A4f exact tails of the bias functional are below the bounded-differences (McDiarmid) bound", okf)
check("A4g A(w_c) - 1 >= R - O_c for every tuple, and P(O_c >= R/2) <= (L-1) V(n,r-1)/2^n", okg)

# A4h: Theorem A' at finite n beyond the side condition of its first version (u = 1, eps = 1, M = 100, eta = 0.1):
# the recipe of Corollary A' (largest r with 2 (2e^eps - 1) m_r ln(2M/eta) <= tau^2, L = ceil(2(e^eps - 1)/m_r)).
def log_binom_row(n_):
    lg = [math.lgamma(n_ + 1) - math.lgamma(j + 1) - math.lgamma(n_ - j + 1) for j in range(n_ + 1)]
    return np.array(lg)
def lse(v):
    mx = np.max(v)
    return mx + math.log(np.sum(np.exp(v - mx)))
okh = True
print("   Theorem A' at finite n (u = 1, eps = 1, M = 100, eta = 0.1): n, gamma, r/n, L m_r, exponents")
u7, eps7, M7, eta7 = 1.0, 1.0, 100, 0.1
pu7 = 1 / (1 + math.exp(u7)); rho07 = math.log(2 / (1 + math.exp(-u7))) / u7
kl7 = lambda x, p_: x * math.log(x / p_) + (1 - x) * math.log((1 - x) / (1 - p_))
hbar7 = lambda lam: kl7(rho07 - lam / u7, 0.5) - lam
for n7, gam7 in [(2000, 0.005), (2000, 0.03), (20000, 0.03), (20000, 0.045), (200000, 0.03), (200000, 0.045)]:
    lb = log_binom_row(n7) - n7 * math.log(2)
    ltau2 = -2 * gam7 * n7
    lthr = ltau2 - math.log(2 * (2 * math.exp(eps7) - 1) * math.log(2 * M7 / eta7))
    def log_m(r_):                                                    # ln m_r
        j = np.arange(r_)
        x_ = u7 * (r_ - j)
        return lse(lb[:r_] + x_ + np.log1p(-np.exp(-x_)))              # ln(e^x - 1) without overflow
    lo_, hi_ = 1, n7 // 2
    while hi_ - lo_ > 1:                                              # largest r with ln m_r <= lthr
        mid = (lo_ + hi_) // 2
        if log_m(mid) <= lthr: lo_ = mid
        else: hi_ = mid
    r7 = lo_
    lm = log_m(r7)
    lL = math.log(2 * (math.exp(eps7) - 1)) - lm                      # ln L (L = ceil(...): the ceiling changes ln L by < e^{lm})
    lV = lse(lb[:r7]) + n7 * math.log(2)                              # ln V(n, r-1)
    expo = (n7 * math.log(2) - lL - lV) / n7                          # n^-1 ln(2^n / (L V))
    leta2 = lL + lV - n7 * math.log(2)                                # ln eta''
    leta1 = math.log(5 * 2 * (math.exp(eps7) - 1) / 2) + gam7 * n7 + leta2    # ln eta' of the first version
    okh &= lm <= lthr and log_m(r7 + 1) > lthr and leta2 < math.log(1e-3) and abs(r7 / n7 - (rho07 - 2 * gam7 / u7)) < 0.02
    okh &= expo > 0 and abs(expo - hbar7(2 * gam7)) < 0.004
    print("          n = %6d gamma = %.3f: r/n = %.4f (limit %.4f), n^-1 ln(2^n/(L V)) = %.5f (limit hbar(2 gamma) = %.5f), ln eta'' = %.1f, ln eta' (first version) = %+.1f"
          % (n7, gam7, r7 / n7, rho07 - 2 * gam7 / u7, expo, hbar7(2 * gam7), leta2, leta1))
check("A4h the recipe of Corollary A' at n = 2000, 20000, 200000: hypotheses hold, eta'' < 1e-3, the exponent of the bound is positive "
      "and within 0.004 of hbar(2 gamma) (also where eta' of the first version exceeds one)", okh)

# A5: Lemma 5.1 (attenuated bias): E_a (E_{nu_{Gamma+a}} phi - mean phi)^2 = sum_{s != 0} phihat^2 rhotilde^2 nutilde^2
n5a, u5a = 8, 1.0
N5a, idx5a, D5a = cube(n5a)
par = lambda a_, b_: bin(int(a_) & int(b_)).count("1") & 1
CH = np.array([[1 - 2 * par(s_, x_) for x_ in range(N5a)] for s_ in range(N5a)], dtype=float)   # CH[s, x]
e5 = np.maximum(0.0, np.exp(u5a * (4 - D5a[:, 0].astype(float))) - 1.0)
nu0 = e5 / e5.sum()
okA5 = True
for _ in range(3):
    Gam = rng.integers(0, N5a, size=int(rng.integers(2, 9)))
    phi5 = rng.uniform(-1, 1, size=N5a)
    devs = []
    for a_ in range(N5a):
        nuG = sum(nu0[idx5a ^ int(c) ^ a_] for c in Gam) / len(Gam)
        devs.append(nuG @ phi5 - phi5.mean())
    lhs = np.mean(np.square(devs))
    phihat = CH @ phi5 / N5a
    rho_t = CH[:, Gam].mean(axis=1)
    nu_t = CH @ nu0
    rhs = np.sum((phihat ** 2 * rho_t ** 2 * nu_t ** 2)[1:])
    okA5 &= abs(lhs - rhs) < 1e-12 and rhs <= np.mean(phi5 ** 2) * np.max((np.abs(rho_t) * np.abs(nu_t))[1:]) ** 2 + 1e-12
check("A5 attenuated bias: E_a(dev^2) = sum_{s != 0} phihat(s)^2 rho~(s)^2 nu~(s)^2 <= E phi^2 max (|rho~| |nu~|)^2", okA5)

# A6: Proposition 2.7 (absorption): a kappa-Lipschitz known energy f moves the slope by at most kappa
kap, uu = 0.3, 1.0
okA6 = True
for _ in range(5):
    cs6 = rng.integers(0, N, size=4); off6 = rng.uniform(0, 3, size=4)
    f6 = kap * np.min(D[:, cs6] + off6[None, :], axis=1) * float(rng.choice([-1.0, 1.0]))   # kappa-Lipschitz
    Zf = np.exp(-f6).mean()
    pi6 = np.exp(-f6) / np.exp(-f6).sum()
    v6 = random_admissible(n, uu - kap, D)                    # instance of P(uniform, u - kappa)
    w6 = v6 * np.exp(f6)                                      # instance of P(pi, u)
    okA6 &= admissible(v6, n, uu - kap) and admissible(w6, n, uu)
    okA6 &= abs((pi6 @ w6) - v6.mean() / Zf) < 1e-12 * v6.mean() / Zf
    okA6 &= np.allclose(pi6 * w6 / (pi6 @ w6), v6 / v6.sum(), rtol=1e-11, atol=0)
    w7 = random_admissible(n, uu, D)                          # instance of P(pi, u)
    v7 = w7 * np.exp(-f6)                                     # instance of P(uniform, u + kappa)
    okA6 &= admissible(v7, n, uu + kap) and abs(v7.mean() - Zf * (pi6 @ w7)) < 1e-12 * v7.mean()
check("A6 absorption: v e^{f} in W_u for v in W_{u-kappa}, w e^{-f} in W_{u+kappa}; same ensembles; targets differ by ln Z_f", okA6)

# ----------------------------------------------------------------------------- B
print("== B. exact observables: subgroup averaging ==")
nb = 8
Nb, idxb, Db = cube(nb)
def dot(s, x):
    return np.array([bin(int(s) & int(v)).count("1") & 1 for v in np.atleast_1d(x)])
def span(gens):
    C = {0}
    for g in gens:
        C |= {c ^ int(g) for c in C}
    return sorted(C)
wb = random_admissible(nb, 1.0, Db)
what = np.array([(wb * (1 - 2 * dot(s, idxb))).mean() for s in range(Nb)])
ok_all, sizes = True, []
for M in (1, 3, 7, 12, 30):
    Sset = rng.choice(np.arange(1, Nb), size=M, replace=False)
    rr = math.ceil(math.log2(M + 1))
    found = None
    for _ in range(4000):
        gens = rng.integers(0, Nb, size=rr)
        if all(any(bin(int(s) & int(g)).count("1") & 1 for g in gens) for s in Sset):
            found = gens; break
    if found is None:
        ok_all = False; break
    C = span(found)
    sizes.append((M, len(C)))
    wC = sum(wb[idxb ^ c] for c in C) / len(C)
    coef = np.array([(wC * (1 - 2 * dot(s, idxb))).mean() for s in range(Nb)])
    inperp = np.array([all((bin(s & c).count("1") & 1) == 0 for c in C) for s in range(Nb)])
    ok_all &= np.allclose(coef, what * inperp, atol=1e-12) and not inperp[Sset].any() \
        and len(C) < 2 * (M + 1) and admissible(wC, nb, 1.0) and abs(wC.mean() - wb.mean()) < 1e-12
check("B1 a subgroup C with |C| < 2(M+1) kills M prescribed Walsh coefficients; averaging multiplies "
      "the coefficients by 1[s in C-perp]", ok_all, "(M, |C|): " + str(sizes))
# B2: counting identity behind the union bound: for s != 0, #{(g_1..g_r): s.g_i = 0 all i} = 2^{(n-1) r}
n2, r2, s2 = 5, 2, 0b10110
cnt = sum(1 for g in itertools.product(range(1 << n2), repeat=r2)
          if all((bin(s2 & gi).count("1") & 1) == 0 for gi in g))
check("B2 number of generator tuples orthogonal to a fixed s != 0 is 2^{(n-1)r}", cnt == 2 ** ((n2 - 1) * r2))
# B3: tightness: S = W \ {0}, W a subspace of dimension mm: every C with C-perp cap S empty has |C| >= 2^mm
def all_subspaces(nn):
    seen = set()
    for k in range(nn + 1):
        for gens in itertools.combinations(range(1, 1 << nn), k):
            C = tuple(span(gens))
            if len(C) == 1 << k:
                seen.add(C)
    return seen
n5, mm = 4, 2
Wsp = span([0b0001, 0b0010]); Sw = [s for s in Wsp if s]
best = min(len(C) for C in all_subspaces(n5)
           if not any(all((bin(s & c).count("1") & 1) == 0 for c in C) for s in Sw))
check("B3 tightness: for S = W minus 0 (dim W = 2, M = 3) the least |C| is M + 1 = 4", best == 4, "least |C| = %d" % best)
# B4: exact joint law of b coordinates: cylinder instances are invisible; zoom identity
b = 3
cell = idxb & ((1 << b) - 1)
v = random_admissible(nb - b, 1.0, cube(nb - b)[2])
wcyl = v[idxb >> b]
mu = wcyl / wcyl.sum()
cellmass = np.bincount(cell, weights=mu, minlength=1 << b)
check("B4a a cylinder instance has exactly uniform cell masses", np.allclose(cellmass, 2.0 ** -b, atol=1e-14)
      and admissible(wcyl, nb, 1.0))
mu = wb / wb.sum(); cellmass = np.bincount(cell, weights=mu, minlength=1 << b)
zoom = [wb[cell == s].mean() * 2.0 ** -b / cellmass[s] for s in range(1 << b)]
check("B4b zoom identity A = E_S[w] 2^-b / mu(S) for every cell S", np.allclose(zoom, wb.mean(), rtol=1e-12))
z = int(rng.integers(0, Nb))
check("B4c one exact point observable: A = w(z) 2^-n / mu(z)", abs(wb[z] / Nb / mu[z] - wb.mean()) < 1e-12 * wb.mean())

# ----------------------------------------------------------------------------- C
print("== C. sharpness: partition oracles and the full oracle ==")
worst = 0.0
for trial in range(200):
    wt = random_admissible(nb, 1.0, Db)
    mu = wt / wt.sum()
    nu = np.bincount(cell, weights=mu, minlength=1 << b)
    tau_c = 0.05
    # adversarial report: move l1-mass tau_c between cells
    order = rng.permutation(1 << b)
    nuh = nu.copy(); d = min(tau_c / 2, nuh[order[0]] * 0.9)
    nuh[order[0]] -= d; nuh[order[1]] += d
    est = np.array([wt[cell == s].mean() * 2.0 ** -b / nuh[s] for s in range(1 << b)])
    for kappa in (0.1, 0.3, 0.6):
        badp = nuh[np.abs(nu / nuh - 1) > kappa].sum()
        worst = max(worst, badp - np.abs(nu - nuh).sum() / kappa)
    relerr = np.abs(est / wt.mean() - 1)
    assert np.allclose(relerr, np.abs(nu / nuh - 1), atol=1e-12)
check("C1 random-cell estimator: P_{S ~ nu-hat}(|nu(S)/nu-hat(S) - 1| > kappa) <= ||nu - nu-hat||_1 / kappa",
      worst <= 1e-12, "largest (probability - bound) = %.2e" % worst)
worst = 0.0
for trial in range(200):
    wt = random_admissible(nb, 1.0, Db)
    mu = wt / wt.sum()
    noise = rng.dirichlet(np.ones(Nb))
    t = 0.04
    muh = (1 - t) * mu + t * noise                    # TV(muh, mu) <= t
    for kappa in (0.1, 0.3):
        badp = muh[np.abs(mu / muh - 1) > kappa].sum()
        worst = max(worst, badp - np.abs(mu - muh).sum() / kappa)
check("C2 full oracle: one evaluation at x ~ mu-hat fails with probability <= ||mu - mu-hat||_1 / kappa",
      worst <= 1e-12)

# ----------------------------------------------------------------------------- D
print("== D. deterministic algorithms: wells at the query points ==")
Delta = 0.9
ok = True; worst = 0.0
for trial in range(50):
    Q = rng.integers(0, Nb, size=int(rng.integers(1, 12)))
    dQ = Db[:, Q].min(axis=1).astype(float)
    wel = np.minimum(math.exp(Delta), np.exp(1.0 * dQ))
    ok &= admissible(wel, nb, 1.0) and np.all(wel[Q] == 1.0)
    mu = wel / wel.sum()
    tv = 0.5 * np.abs(mu - 1.0 / Nb).sum()
    p = np.count_nonzero(wel < math.exp(Delta)) / Nb
    ok &= tv <= p + 1e-12 and wel.mean() >= math.exp(Delta) * (1 - p) - 1e-12
    worst = max(worst, tv / p)
check("D1 wells min(e^Delta, e^{u d(x,Q)}): admissible, = 1 on Q, A >= e^Delta (1-p), TV(mu, pi) <= p",
      ok, "largest TV/p = %.3f" % worst)

# ----------------------------------------------------------------------------- E
print("== E. exponent functions ==")
def h2(x):
    return 0.0 if x <= 0 or x >= 1 else -x * math.log(x) - (1 - x) * math.log(1 - x)
def kl(x, p):
    s = 0.0
    if x > 0: s += x * math.log(x / p)
    if x < 1: s += (1 - x) * math.log((1 - x) / (1 - p))
    return s
def consts(u):
    pu = 1 / (1 + math.exp(u)); a = kl(pu, 0.5)
    rho0 = math.log(2 / (1 + math.exp(-u))) / u
    h = kl(rho0, 0.5); ell = math.log((1 - rho0) / rho0) / u
    return pu, a, rho0, h, ell
def hbar(lmb, u):
    pu, a, rho0, h, ell = consts(u)
    return kl(rho0 - lmb / u, 0.5) - lmb if lmb < a else 0.0
def bisect(f, lo, hi):
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(lo) * f(mid) <= 0: hi = mid
        else: lo = mid
    return 0.5 * (lo + hi)
print("   u      p_u       a         rho_0     h         ell     2(1-ell)  h/ln2   gamma_max(S1) gamma_1 (first version of A') a/2 (A')  alpha_0   alpha_1   nu*      nu*/h")
okE = True
for u in (0.5, 1.0, 2.0):
    pu, a, rho0, h, ell = consts(u)
    okE &= abs(kl(rho0, pu) - h) < 1e-12                       # Chernoff point: KL(rho0||1/2) = KL(rho0||p_u)
    okE &= abs(rho0 - (pu + a / u)) < 1e-12
    okE &= abs(hbar(0, u) - h) < 1e-12 and abs(hbar(a * (1 - 1e-12), u)) < 1e-9
    d = (hbar(1e-6, u) - h) / 1e-6
    okE &= abs(d + (1 - ell)) < 1e-4                            # slope of hbar at 0 is -(1 - ell)
    okE &= all(hbar(x, u) + hbar(x + 2e-3, u) - 2 * hbar(x + 1e-3, u) >= -1e-12
               for x in np.linspace(0, a * 0.95, 50))           # convex
    g1 = bisect(lambda g: hbar(2 * g, u) - g, 0.0, a / 2)       # hbar(2 gamma) = gamma: the side condition of the FIRST version of Theorem A'
    a0 = bisect(lambda al: h2(al) - h, 1e-9, 0.4)
    a1 = bisect(lambda al: h2(al) - a, 1e-9, 0.4)
    nu = bisect(lambda v: hbar(v, u) - 2 * v, 0.0, a)
    print("   %.1f  %.6f  %.6f  %.6f  %.6f  %.4f  %.4f    %.4f  %.6f      %.6f                     %.6f  %.6f  %.6f  %.6f %.4f"
          % (u, pu, a, rho0, h, ell, 2 * (1 - ell), h / math.log(2), h / 2, g1, a / 2, a0, a1, nu, nu / h))
check("E1 identities: rho_0 = p_u + a/u, KL(rho_0||1/2) = KL(rho_0||p_u) = h, hbar(0) = h, hbar(a) = 0, "
      "hbar' (0) = -(1 - ell), hbar convex", okE)
u = 1.0; pu, a, rho0, h, ell = consts(u)
tab = [(g, max(0.0, h - 2 * g), hbar(2 * g, u), (1 - g / math.log(2)) * h) for g in (0.0, 0.002, 0.005, 0.01, 0.0145, 0.02, 0.03, 0.04, 0.05, a / 2)]
print("   u = 1: gamma, S1 bound max(0, h-2gamma), refined hbar(2gamma), upper (1-gamma/ln2)h")
for row in tab:
    print("          %.4f   %.6f   %.6f   %.6f" % row)
check("E2 refined bound dominates h - 2 gamma and stays below the zoom upper bound",
      all(r[2] >= r[1] - 1e-15 and r[2] <= r[3] + 1e-15 for r in tab))
okE3 = True
for u in (0.5, 1.0, 2.0):
    pu, a, rho0, h, ell = consts(u)
    okE3 &= all(hbar(x, u) > 0 for x in np.linspace(0, a * (1 - 1e-6), 400))             # positive on [0, a)
    okE3 &= all(hbar(x, u) >= max(0.0, h - x) - 1e-15 for x in np.linspace(0, a * (1 - 1e-6), 400))
    for x in (1e-2 * a, 1e-3 * a):                                                         # double zero at a
        okE3 &= abs(hbar(a - x, u) / (x * x / (2 * u * u * pu * (1 - pu))) - 1) < 0.05
check("E3 hbar > 0 on [0, a), hbar >= h - lambda, and hbar(a - x) ~ x^2/(2 u^2 p_u (1 - p_u)) (double zero at a)", okE3)

print()
print("ALL CHECKS PASS" if not FAILS else "FAILED: " + ", ".join(FAILS))
sys.exit(1 if FAILS else 0)
