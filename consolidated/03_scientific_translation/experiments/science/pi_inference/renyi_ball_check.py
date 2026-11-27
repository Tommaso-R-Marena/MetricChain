#!/usr/bin/env python3
"""Addendum A17 -- certification of ln Z against a sampleable model when an a-priori bound on a
divergence between the true ensemble and the model is available.  Coordinator's own check script.

Setting: finite X, reference (model) measure pi, remainder r = g - ghat, Boltzmann factor Y = exp(-r),
mu = E_pi Y = Z(g)/Z(ghat).  Classes:
   B_p(B)  = { r : ||Y||_{L^p(pi)} <= B }                (p in (1, inf]; p = inf is a box with floor -ln B)
   D_p(k)  = { r : Renyi divergence D_p(pi_g || pi) <= k } (scale-invariant form; p = 1 is KL)

What is checked (all by exact sums on finite X, no sampling unless stated):
 (1) detection lemma: two members of B_p(B) that differ on D with |ln mu - ln mu'| > eps have
     pi(D) >= ((1 - e^-eps) * max(mu,mu')... precisely  pi(D) >= (|mu - mu'| / B)^{p/(p-1)}.
     Tested against the *extremal* alternative on each D (closed form), i.e. the hardest case.
 (2) the packing alternative of the lower bound is a member and achieves the claimed change.
 (3) KL ball: exact KL of the two-level alternative; detection bound through the binary KL.
 (4) moment bounds on r itself (E_pi r^2 <= s^2) do not bound ln mu on small sets.
 (5) first-order classes on a product measure sit in Renyi balls: D_2 <= sum c_i^2 / 2 (McDiarmid),
     random members of the cube class by enumeration; the additive instance.
 (6) coverage of the Chebyshev bracket [muhat +- B/sqrt(N delta)] on a heavy-tailed instance (simulation).
"""
import math, sys, json
import numpy as np

rng = np.random.default_rng(20261125)
out = {}

def norm_p(pi, Y, p):
    if math.isinf(p):
        return float(Y.max())
    return float((pi @ Y**p) ** (1.0 / p))

def renyi(pi, Y, p):
    """D_p(pi_g || pi), pi_g = pi*Y/mu."""
    mu = float(pi @ Y)
    w = Y / mu
    if p == 1:
        return float(pi @ (w * np.log(w)))
    if math.isinf(p):
        return float(np.log(w.max()))
    return float(np.log(pi @ w**p) / (p - 1))

# ---------------------------------------------------------------- (1) detection lemma, extremal alternatives
worst = {}
cases = 0
for p in (1.25, 1.5, 2.0, 3.0, 6.0, math.inf):
    wr = math.inf   # smallest value of pi(D) / bound ; must be >= 1
    for trial in range(1500):
        N = int(rng.integers(30, 400))
        pi = rng.dirichlet(np.full(N, rng.choice([0.2, 1.0, 5.0])))
        Y0 = np.exp(-rng.normal(0, rng.choice([0.3, 1.0, 2.5]), N))
        B0 = norm_p(pi, Y0, p)
        B = B0 * (1 + rng.choice([1e-3, 0.1, 1.0, 10.0]))
        k = int(rng.integers(1, max(2, N // 3)))
        D = rng.choice(N, size=k, replace=False)
        q = float(pi[D].sum())
        mu0 = float(pi @ Y0)
        # extremal upward alternative on D: Y' = y (constant) on D, y maximal with ||Y'||_p <= B
        if math.isinf(p):
            y = B
        else:
            T = float(pi @ Y0**p) - float(pi[D] @ Y0[D]**p)
            y = ((B**p - T) / q) ** (1.0 / p)
        Y1 = Y0.copy(); Y1[D] = y
        assert norm_p(pi, Y1, p) <= B * (1 + 1e-9)
        mu1 = float(pi @ Y1)
        if mu1 > mu0:
            bound = ((mu1 - mu0) / B) ** (p / (p - 1)) if not math.isinf(p) else (mu1 - mu0) / B
            wr = min(wr, q / bound)
        # extremal downward alternative: Y' = 0+ on D
        Y2 = Y0.copy(); Y2[D] = 1e-300
        mu2 = float(pi @ Y2)
        bound = ((mu0 - mu2) / B) ** (p / (p - 1)) if not math.isinf(p) else (mu0 - mu2) / B
        wr = min(wr, q / bound)
        cases += 2
    worst[str(p)] = wr
    print(f"(1) p={p}: min over cases of pi(D)/bound = {wr:.6f}  (must be >= 1)")
    assert wr >= 1 - 1e-9
out["detection_min_ratio"] = worst
out["detection_cases"] = cases

# ---------------------------------------------------------------- (2) the packing alternative
for p in (1.5, 2.0, 4.0):
    N = 100000
    pi = np.full(N, 1.0 / N)
    Y0 = np.ones(N)          # the centre: mu0 = 1, ||Y0||_p = 1
    for B, eps in ((3.0, 0.1), (10.0, 0.3), (1.5, 0.05)):
        qlow = ((math.exp(eps) - 1) / (B - 1)) ** (p / (p - 1))
        m = int(math.floor(qlow * N)) + 1          # smallest set with mass > qlow
        q = m / N
        a = (B - 1) * q ** (-1 / p)
        Y1 = Y0.copy(); Y1[:m] += a
        nb = norm_p(pi, Y1, p)
        dln = math.log(float(pi @ Y1))
        k = N // m
        print(f"(2) p={p} B={B} eps={eps}: q_low={qlow:.3e}, |D|/N={q:.3e}, ||Y'||_p={nb:.6f} <= B, "
              f"ln mu'={dln:.4f} > eps, disjoint alternatives k={k}, "
              f"upper bound ln(1/0.05)/q* = {math.log(20) / ((1 - math.exp(-eps)) / B) ** (p / (p - 1)):.3e}")
        assert nb <= B * (1 + 1e-12) and dln > eps

# ---------------------------------------------------------------- (3) KL ball at the centre
print("(3) KL ball D_1(pi_g||pi) <= kappa at the centre (hint r = 0)")
for kappa, eps in ((0.5, 0.1), (1.0, 0.1), (1.0, 0.3), (3.0, 0.5)):
    s = 1 - math.exp(-eps); eta = math.exp(eps) - 1
    N = 10**7
    # smallest q such that the two-level alternative (1 + a on D, a q = eta) is in the ball: solve exactly
    def KL(q):
        return -eps + (q + eta) * math.exp(-eps) * math.log(1 + eta / q)
    lo, hi = 1e-300, 0.5
    for _ in range(300):
        mid = math.sqrt(lo * hi)
        if KL(mid) > kappa: lo = mid
        else: hi = mid
    qmin = hi
    approx = eta * math.exp(-(kappa + eps) / s)
    det = math.exp(-(kappa + math.log(2)) / s)
    print(f"    kappa={kappa} eps={eps}: smallest mass of a hiding set (exact two-level) q={qmin:.4e}; "
          f"formula eta*exp(-(kappa+eps)/s)={approx:.4e}; detection bound exp(-(kappa+ln2)/s)={det:.4e}; "
          f"ratio q/det = {qmin / det:.3f} (>= 1)")
    assert qmin >= det
    # random alternatives in the ball: check pi(D) >= det whenever |ln mu'| > eps
    bad = 0; tested = 0
    for trial in range(4000):
        n = 200
        pi = rng.dirichlet(np.ones(n))
        k = int(rng.integers(1, 40)); D = rng.choice(n, size=k, replace=False)
        Y = np.ones(n); Y[D] = np.exp(rng.normal(0, 3.0, k) + rng.uniform(0, 8))
        if renyi(pi, Y, 1) <= kappa and abs(math.log(float(pi @ Y))) > eps:
            tested += 1
            if pi[D].sum() < det: bad += 1
    print(f"      random alternatives in the ball with |ln mu'|>eps: {tested}, violating the detection bound: {bad}")
    assert bad == 0

# ---------------------------------------------------------------- (4) moments of r do not help
print("(4) class E_pi r^2 <= sigma^2: a dip on one state")
for sigma, q in ((0.1, 1e-6), (0.1, 1e-9), (0.01, 1e-12)):
    d = sigma / math.sqrt(q)                       # depth allowed on a state of mass q
    lnmu = math.log1p(q * math.expm1(min(d, 700)))
    print(f"    sigma={sigma}, mass q={q}: allowed depth {d:.3g} k_BT, ln mu changes by {lnmu:.3g}")
    assert lnmu > 1

# ---------------------------------------------------------------- (5) first-order => Renyi, product measure
print("(5) D_2(pi_g||pi) <= sum_i c_i^2 / 2 for members of the cube class, uniform product measure")
def random_member(n, u):
    """random u-Lipschitz function on {0,1}^n: McShane envelope of random anchors (max of cones)."""
    X = np.arange(2**n)
    bits = ((X[:, None] >> np.arange(n)) & 1)
    m = int(rng.integers(1, 6))
    psi = np.full(2**n, -np.inf)
    for _ in range(m):
        a = bits[rng.integers(2**n)]
        dist = (bits != a).sum(1)
        psi = np.maximum(psi, rng.normal(0, 2.0) - u * dist * rng.uniform(0.3, 1.0))
    return psi, bits
viol = 0; worst5 = 0.0
for trial in range(600):
    n = int(rng.integers(4, 13)); u = float(rng.choice([0.2, 0.5, 1.0, 2.0]))
    psi, bits = random_member(n, u)
    pi = np.full(2**n, 2.0**-n)
    # exact one-site oscillations c_i
    c = np.zeros(n)
    idx = np.arange(2**n)
    for i in range(n):
        c[i] = np.abs(psi - psi[idx ^ (1 << i)]).max()
    assert c.max() <= u + 1e-12
    for p in (1.5, 2.0, 3.0):
        Dp = renyi(pi, np.exp(-psi), p)
        bnd = p * p * (c @ c) / (8 * (p - 1))
        worst5 = max(worst5, Dp / bnd)
        if Dp > bnd + 1e-12: viol += 1
print(f"    600 random members x 3 orders: violations {viol}; largest D_p / bound = {worst5:.4f}")
assert viol == 0
for u in (0.2, 1.0, 2.0):
    n = 12
    idx = np.arange(2**n); w = np.array([bin(i).count('1') for i in idx])
    pi = np.full(2**n, 2.0**-n)
    D2 = renyi(pi, np.exp(-u * w), 2.0)
    print(f"    additive instance u={u}, n={n}: D_2 = {D2:.6f} = n ln(1+tanh^2(u/2)) = {n * math.log(1 + math.tanh(u / 2) ** 2):.6f}"
          f"  (bound n u^2/2 = {n * u * u / 2:.4f})")
out["mcdiarmid_violations"] = viol
out["mcdiarmid_largest_ratio"] = worst5

# ---------------------------------------------------------------- (6) coverage of the Chebyshev bracket
print("(6) Chebyshev bracket mu in [muhat - B2/sqrt(N delta), muhat + B2/sqrt(N delta)], B2 = ||Y||_2")
N = 2000; delta = 0.1
n_states = 200000
pi = np.full(n_states, 1.0 / n_states)
Y = np.exp(rng.normal(0, 1.8, n_states))            # heavy right tail: lognormal Boltzmann factors
mu = float(pi @ Y); B2 = norm_p(pi, Y, 2.0)
miss = 0; reps = 4000
for rep in range(reps):
    xs = rng.integers(0, n_states, N)
    mh = Y[xs].mean()
    if abs(mh - mu) > B2 / math.sqrt(N * delta): miss += 1
print(f"    lognormal(sigma=1.8): mu={mu:.3f}, ||Y||_2={B2:.3f}, D_2={2 * math.log(B2 / mu):.3f}; "
      f"miss rate {miss / reps:.4f} <= delta={delta};  half-width/mu = {B2 / math.sqrt(N * delta) / mu:.3f}")
assert miss / reps <= delta
out["chebyshev_miss_rate"] = miss / reps

# ---------------------------------------------------------------- (7) the theory division's preview (THY-RES-0007 section 4), re-computed
print("(7) statements (a), (b), (e) of the theory division's box-class preview, independently")
def Lw(w): return math.log(math.expm1(w) / w) - 1 + w / math.expm1(w)
worst7 = 0.0
for trial in range(20000):
    w = float(rng.choice([0.1, 0.5, 1.0, 3.0, 8.0]))
    k = int(rng.integers(2, 8))
    y = rng.uniform(0, w, k); pr = rng.dirichlet(np.full(k, rng.choice([0.3, 1.0])))
    if rng.random() < 0.5:                     # two-point laws on the end points, including the optimum
        y = np.array([0.0, w]); t = rng.random(); pr = np.array([1 - t, t])
    gap = math.log(float(pr @ np.exp(y))) - float(pr @ y)
    worst7 = max(worst7, gap / Lw(w))
    assert gap <= Lw(w) * (1 + 1e-12) + 1e-15
for w in (0.1, 1.0, 3.0, 8.0):
    t = 1 / w - 1 / math.expm1(w)
    val = math.log(1 - t + t * math.exp(w)) - t * w
    assert abs(val - Lw(w)) < 1e-12 and Lw(w) <= w * w / 8
print(f"    (a) ln E e^Y - E Y <= L(w): 20 000 laws, largest ratio {worst7:.6f}; two-point optimum = L(w); L(w) <= w^2/8")
for rm, rp, eps in ((3.0, 3.0, 0.2), (1.0, 2.0, 0.1), (5.0, 0.5, 0.5)):
    qs = math.expm1(eps) / (math.exp(rm) - math.exp(eps - rp) + math.expm1(eps))
    up = (1 - qs) + qs * math.exp(rm); lo = (1 - qs) + qs * math.exp(-rp)
    assert abs(math.log(up / lo) - eps) < 1e-12
print("    (b) q* = (e^eps - 1)/(e^rho- - e^(eps - rho+) + e^eps - 1): the bracket off Q has width exactly eps at pi(Q^c) = q*")
def spot(rho_minus, rho_plus, eps, delta):
    eta = eps / 2
    U = math.expm1(rho_minus); V = -math.expm1(-rho_plus)          # in units of Z, at the centre
    p = min(1.0, 0.5 * min(math.expm1(eta) / U, -math.expm1(-eta) / V))
    return math.ceil(math.log(1 / delta) / p)
n1 = spot(3.0, 3.0, 0.2, 0.05)
n2 = spot(3.7, 3.7, 0.1, 0.05); n3 = spot(15.6, 15.6, 0.1, 0.05)
print(f"    (e) spot check at the centre of a constant box: rho=3, eps=0.2, delta=0.05 -> {n1} (theirs: 1088); "
      f"rho=3.7, eps=0.1 -> {n2} (theirs: about 5e3); rho=15.6 -> {n3:.3e} (theirs: about 7e8); "
      f"e^(0.0291391 n) exceeds {n1} from n = {math.ceil(math.log(n1) / 0.0291391)}")
assert n1 == 1088

json.dump(out, open("renyi_ball_check.json", "w"), indent=1)
print("ALL CHECKS PASSED")
