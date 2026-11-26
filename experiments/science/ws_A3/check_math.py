#!/usr/bin/env python3
"""Workstream A3 — numerical checks of the identities and inequalities used in A3_REPORT.md.

Nothing here is a literature result; these are the checks behind the statements labelled [P] in the
report (COMMON rule 3: numerics before theory).

  C1  L(w) = ln((e^w-1)/w) - 1 + w/(e^w-1)  ==  ln S(e^w)  (Specht's ratio S(h) = (h-1) h^{1/(h-1)} / (e ln h))
                                            ==  a - 1 - ln a,  a = w/(1-e^{-w})   (bounded-range form)
                                            ==  max_t [ ln(1 - t + t e^w) - t w ]
      and L(w) <= w^2/8, and ln cosh(w/2) <= L(w).
  C2  Random laws on [0, w]:  ln E e^Y - E Y <= L(w)   (never exceeded; two-point law attains it).
  C3  Both Kullback-Leibler divergences between a law and its tilt by a function of oscillation w are <= L(w),
      and the bound is attained (by different two-point pairs for the two directions).
  C4  Tilt lemma: for P = Q e^{-r} / E_Q e^{-r}, osc(r) = w:   D_alpha(P||Q) <= alpha w^2 / 8  (alpha > 1);
      numerical supremum over two-point laws for comparison.
  C5  Product reference, one-site oscillations c_i, K = sum c_i^2:   D_p(pi_g || pi) <= p K / 8
      (random members of bounded-difference classes on {0,1}^n and {0,1,2}^n by exact enumeration, plus a
      hill-climb that tries to violate it), compared with the bound p^2 K / (8 (p-1)) of addendum A17.6.
  C6  The constants connecting T3 to the [0,1]-valued mean-estimation problem: for X in [0,1] with mean m,
      max Var = m(1-m), so (worst-case variance term)/(eps m)^2 = (1-m)/(eps^2 m) and T3's (1/m - 1)/eps
      is exactly eps times it.
  C7  At the centre of a constant box the hint is not needed: the stopping rule "draw N(m) =
      ceil(ln(1/delta) max((1-m)/(eps m), 1/eps)) + 1 samples of X = e^{-(r-lo)}; if they all equal the first
      value m, output m" fails with probability <= delta on every [0,1]-valued law (exact worst case over
      two- and three-level alternatives), and N(m) is the hinted count of T3 up to the factor ln(1/delta).
  C8  Hoeffding's (4.12)-(4.13): ln E e^{Y-EY} <= -w p + ln(1 - p + p e^w), p = (EY - min Y)/w, on random laws;
      it is never larger than L(w) and equals it only at the extremal p.
  C5 also checks the refined bound D_p <= (p-1)K/8 + sum_i L(c_i)   (bounded range => zCDP, composed).
  C5 (last block) checks the same bound for NON-product reference measures with the ranges c~_i of the
      conditional free energy F_i = -ln E_pi[e^{-r} | x_<=i]  (remark after A3.2 in the report).

Run:  python3 check_math.py            (about 40 s; writes check_math.out next to this file when redirected)
"""
import itertools
import math

import numpy as np

rng = np.random.default_rng(20261126)


def dirichlet(k, conc):
    """Dirichlet draw with all masses strictly positive (tiny concentrations can underflow to 0)."""
    p = np.maximum(rng.dirichlet(np.full(k, conc)), 1e-12)
    return p / p.sum()


# ----------------------------------------------------------------------------------------------- C1
def L(w):
    """L(w) in a numerically stable form."""
    if w < 1e-4:
        return w * w / 8.0 - w ** 4 / 576.0
    em1 = math.expm1(w)
    return math.log(em1 / w) - 1.0 + w / em1


def ln_specht(h):
    """ln of Specht's ratio S(h) = (h-1) h^{1/(h-1)} / (e ln h), h > 1."""
    return math.log(h - 1.0) + math.log(h) / (h - 1.0) - 1.0 - math.log(math.log(h))


def L_br(w):
    a = w / (-math.expm1(-w))
    return a - 1.0 - math.log(a)


def L_max(w, grid=200001):
    t = np.linspace(0.0, 1.0, grid)
    v = np.log1p(t * math.expm1(w)) - t * w
    return float(v.max())


print("C1  identities for L(w)")
print("    w        L(w)          ln S(e^w)     a-1-ln a      max_t          L/(w^2/8)   lncosh(w/2)/L")
worst = 0.0
for w in [0.01, 0.1, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0, 30.0]:
    a, b, c, d = L(w), ln_specht(math.exp(w)), L_br(w), L_max(w)
    worst = max(worst, abs(a - b), abs(a - c), abs(a - d))
    lc = math.log(math.cosh(w / 2.0))
    print(f"    {w:6.2f}  {a:.10f}  {b:.10f}  {c:.10f}  {d:.10f}   {a / (w * w / 8):.6f}    {lc / a:.6f}")
print(f"    largest disagreement between the four forms: {worst:.2e}")
ws = np.linspace(1e-3, 60, 6000)
print("    L(w) <= w^2/8 on (0,60]:", all(L(float(w)) <= float(w) ** 2 / 8 + 1e-15 for w in ws),
      "| ln cosh(w/2) <= L(w):", all(math.log(math.cosh(float(w) / 2)) <= L(float(w)) + 1e-12 for w in ws))
print(f"    large w: L(w) - (w - 1 - ln w) at w = 30, 60: {L(30.0) - (29 - math.log(30)):.2e}, "
      f"{L(60.0) - (59 - math.log(60)):.2e}")

# ----------------------------------------------------------------------------------------------- C2
print("C2  random laws on [0,w]: ratio (ln E e^Y - E Y)/L(w)")
mx = 0.0
cnt = 0
for _ in range(40000):
    w = float(rng.choice([0.2, 1.0, 3.0, 6.0, 12.0]))
    k = int(rng.integers(2, 9))
    y = np.sort(rng.uniform(0, w, k))
    if rng.random() < 0.7:
        y[0], y[-1] = 0.0, w
    p = dirichlet(k, float(rng.choice([0.05, 0.3, 1.0])))
    gap = math.log(float(np.dot(p, np.exp(y)))) - float(np.dot(p, y))
    mx = max(mx, gap / L(w))
    cnt += 1
print(f"    {cnt} laws, largest ratio {mx:.6f} (must be <= 1)")
for w in [0.5, 3.0, 10.0]:
    t = 1.0 / w - 1.0 / math.expm1(w)
    val = math.log1p(t * math.expm1(w)) - t * w
    print(f"    two-point law at w={w}: mass t = 1/w - 1/(e^w-1) = {t:.6f} on the top point, value/L = {val / L(w):.12f}")

# ----------------------------------------------------------------------------------------------- C3
print("C3  KL between a law and its tilt by a function of oscillation w")
mx1 = mx2 = 0.0
for _ in range(40000):
    w = float(rng.choice([0.2, 1.0, 3.0, 6.0, 12.0]))
    k = int(rng.integers(2, 7))
    r = rng.uniform(0, w, k)
    r[0], r[1] = 0.0, w
    q = dirichlet(k, float(rng.choice([0.05, 0.3, 1.0])))
    p = q * np.exp(-r)
    p /= p.sum()
    kl_pq = float(np.sum(p * np.log(p / q)))
    kl_qp = float(np.sum(q * np.log(q / p)))
    mx1 = max(mx1, kl_pq / L(w))
    mx2 = max(mx2, kl_qp / L(w))
print(f"    largest KL(tilt||base)/L(w) = {mx1:.6f}, largest KL(base||tilt)/L(w) = {mx2:.6f} (both must be <= 1)")
for w in [1.0, 4.0]:
    # KL(base||tilt): base puts mass t on the point where e^{-r} is largest (Y = -r in {0,w}): the law of C2
    t = 1.0 / w - 1.0 / math.expm1(w)
    q = np.array([1 - t, t])
    p = q * np.exp(np.array([0.0, w]))
    p /= p.sum()
    print(f"    w={w}: KL(base||tilt) at the C2 law = {float(np.sum(q * np.log(q / p))) / L(w):.12f} * L;"
          f"  KL(tilt||base) at the mirrored pair = {float(np.sum(q * np.log(q / p))) / L(w):.12f} * L (same pair, roles swapped)")

# ----------------------------------------------------------------------------------------------- C4
print("C4  tilt lemma  D_alpha(P||Q) <= alpha w^2/8  (P = tilt of Q by a function of oscillation w)")


def renyi(p, q, alpha):
    if abs(alpha - 1.0) < 1e-12:
        return float(np.sum(p * np.log(p / q)))
    t = alpha * np.log(p) + (1 - alpha) * np.log(q)
    m = float(t.max())
    return float((m + np.log(np.sum(np.exp(t - m)))) / (alpha - 1))


mx = 0.0
for _ in range(60000):
    w = float(rng.choice([0.2, 1.0, 3.0, 6.0]))
    alpha = float(rng.choice([1.0, 1.01, 1.5, 2.0, 3.0, 5.0, 10.0]))
    k = int(rng.integers(2, 7))
    r = rng.uniform(0, w, k)
    r[0], r[1] = 0.0, w
    q = dirichlet(k, float(rng.choice([0.05, 0.3, 1.0])))
    p = q * np.exp(-r)
    p /= p.sum()
    mx = max(mx, renyi(p, q, alpha) / (alpha * w * w / 8))
print(f"    60000 random tilts, largest D_alpha/(alpha w^2/8) = {mx:.6f} (must be <= 1)")
print("    two-point supremum of D_alpha (numerical, over the mass t of the top point), as a fraction of alpha w^2/8:")
ts = np.linspace(1e-6, 1 - 1e-6, 400001)
for alpha in [1.0, 2.0, 5.0]:
    row = []
    for w in [0.1, 1.0, 3.0, 6.0]:
        if alpha == 1.0:
            # KL(P||Q), P = tilt of Q=(1-t,t) by e^{+w} on the second point
            z = 1 - ts + ts * math.exp(w)
            v = ts * math.exp(w) / z * w - np.log(z)
        else:
            v = (np.log1p(ts * math.expm1(alpha * w)) - alpha * np.log1p(ts * math.expm1(w))) / (alpha - 1)
        row.append(float(v.max()) / (alpha * w * w / 8))
    print(f"      alpha={alpha:4.1f}: " + "  ".join(f"w={w}: {x:.4f}" for w, x in zip([0.1, 1.0, 3.0, 6.0], row)))

# ----------------------------------------------------------------------------------------------- C5
print("C5  product reference: D_p(pi_g||pi) against p K/8 and against p^2 K/(8(p-1))  [K = sum c_i^2]")


def all_states(n, a):
    return np.array(list(itertools.product(range(a), repeat=n)), dtype=np.int64)


def one_site_osc(r, states, n, a):
    """c_i = max |r(x) - r(x')| over pairs differing in coordinate i only (exact, by enumeration)."""
    idx = {tuple(s): j for j, s in enumerate(states)}
    c = np.zeros(n)
    for i in range(n):
        m = 0.0
        for j, s in enumerate(states):
            if s[i] != 0:
                continue
            vals = []
            t = list(s)
            for v in range(a):
                t[i] = v
                vals.append(r[idx[tuple(t)]])
            m = max(m, max(vals) - min(vals))
        c[i] = m
    return c


def product_measure(states, n, a, conc):
    margs = [dirichlet(a, conc) for _ in range(n)]
    w = np.ones(len(states))
    for i in range(n):
        w *= margs[i][states[:, i]]
    return w


def member(states, n, a, kind):
    N = len(states)
    if kind == "additive":
        h = rng.uniform(0, 2.0, (n, a))
        return sum(h[i][states[:, i]] for i in range(n))
    if kind == "infconv":
        # r(x) = min_y [ b(y) + sum_i c_i 1(x_i != y_i) ]  has one-site oscillations <= c_i
        cc = rng.uniform(0.1, 2.0, n)
        b = rng.uniform(0, float(rng.choice([1.0, 5.0, 20.0])), N)
        d = (states[:, None, :] != states[None, :, :]).astype(float) @ cc
        return (b[None, :] + d).min(axis=1)
    if kind == "hockey":
        u = float(rng.uniform(0.2, 2.0))
        thr = float(rng.uniform(0, n))
        s = (states != 0).sum(axis=1)
        return -u * np.maximum(s - thr, 0.0)
    if kind == "dist":
        u = float(rng.uniform(0.2, 2.0))
        centres = states[rng.choice(N, size=int(rng.integers(1, 4)), replace=False)]
        d = np.min((states[:, None, :] != centres[None, :, :]).sum(axis=2), axis=1)
        return (u * d) * float(rng.choice([-1.0, 1.0]))
    raise ValueError(kind)


orders = [1.0, 1.01, 1.5, 2.0, 3.0, 6.0]
best = {p: 0.0 for p in orders}
best_a17 = {p: 0.0 for p in orders if p > 1}
best_ref = {p: 0.0 for p in orders}
ntest = 0
for (n, a) in [(4, 2), (6, 2), (8, 2), (3, 3), (5, 3)]:
    states = all_states(n, a)
    for kind in ["additive", "infconv", "hockey", "dist"]:
        for _ in range(60 if len(states) <= 300 else 25):
            r = member(states, n, a, kind)
            c = one_site_osc(r, states, n, a)
            K = float(np.sum(c ** 2))
            if K < 1e-12:
                continue
            pi = product_measure(states, n, a, float(rng.choice([0.3, 1.0, 5.0])))
            pg = pi * np.exp(-(r - r.min()))
            pg /= pg.sum()
            ntest += 1
            sumL = float(sum(L(float(ci)) for ci in c if ci > 0))
            for p in orders:
                d = renyi(pg, pi, p)
                best[p] = max(best[p], d / (p * K / 8))
                best_ref[p] = max(best_ref[p], d / ((p - 1) * K / 8 + sumL))
                if p > 1:
                    best_a17[p] = max(best_a17[p], d / (p * p * K / (8 * (p - 1))))
print(f"    {ntest} random members; largest D_p/(pK/8):   " + "  ".join(f"p={p}: {best[p]:.4f}" for p in orders))
print("                   largest D_p/(p^2K/(8(p-1))): " + "  ".join(f"p={p}: {best_a17[p]:.4f}" for p in best_a17))
print("       largest D_p/((p-1)K/8 + sum_i L(c_i)): " + "  ".join(f"p={p}: {best_ref[p]:.4f}" for p in orders))

# hill-climb: try to violate D_2 <= K/4 on {0,1}^n with the uniform and with a biased product measure
print("    hill-climb on r (cube), objective D_p/(pK/8):")
for (n, p, bias) in [(3, 2.0, 0.5), (4, 2.0, 0.5), (4, 2.0, 0.2), (5, 2.0, 0.5), (4, 1.0, 0.5), (4, 5.0, 0.3), (6, 2.0, 0.5)]:
    states = all_states(n, 2)
    pi = np.prod(np.where(states == 1, bias, 1 - bias), axis=1)
    flip = [np.array([int("".join(map(str, (lambda t: t[:i] + (1 - t[i],) + t[i + 1:])(tuple(s)))), 2) for s in states])
            for i in range(n)]

    def obj(r):
        c = np.array([np.max(np.abs(r - r[flip[i]])) for i in range(n)])
        K = float(np.sum(c ** 2))
        if K < 1e-3:       # below this, D_p (a difference of nearly equal numbers) is rounding noise:
            return 0.0     # an earlier version without this guard "found" ratios up to 1.16 at K ~ 1e-13
        pg = pi * np.exp(-(r - r.min()))
        pg /= pg.sum()
        return renyi(pg, pi, p) / (p * K / 8)

    def obj_exact(r):
        """The same ratio in 50-digit arithmetic (mpmath), to confirm the best point found."""
        import mpmath as mp
        mp.mp.dps = 50
        rr = [mp.mpf(float(x)) for x in r]
        cs = [max(abs(rr[j] - rr[int(flip[i][j])]) for j in range(len(rr))) for i in range(n)]
        K = sum(x * x for x in cs)
        wts = [mp.mpf(float(pi[j])) * mp.e ** (-rr[j]) for j in range(len(rr))]
        Z = sum(wts)
        pgs = [x / Z for x in wts]
        pis = [mp.mpf(float(x)) for x in pi]
        if p == 1.0:
            D = sum(a * mp.log(a / b) for a, b in zip(pgs, pis))
        else:
            D = mp.log(sum(a ** p * b ** (1 - p) for a, b in zip(pgs, pis))) / (p - 1)
        return float(D / (p * K / 8)), float(K)

    top = 0.0
    top_r = None
    for restart in range(6):
        r = rng.normal(0, 1.0, len(states)) if restart else (states.sum(axis=1) * 0.3).astype(float)
        cur = obj(r)
        step = 0.5
        for it in range(4000):
            cand = r.copy()
            move = it % 3
            if move == 0:      # perturb a few values
                j = rng.integers(0, len(states), size=int(rng.integers(1, 4)))
                cand[j] += rng.normal(0, step, size=len(j))
            elif move == 1:    # rescale the whole function
                cand *= float(rng.uniform(0.6, 1.3))
            else:              # add a random one-site term
                i = int(rng.integers(0, n))
                cand += rng.normal(0, step) * states[:, i]
            v = obj(cand)
            if v > cur:
                r, cur = cand, v
            elif it % 500 == 499:
                step *= 0.7
        if cur > top:
            top, top_r = cur, r.copy()
    ex, Kex = obj_exact(top_r)
    print(f"      n={n}, p={p}, P(x_i=1)={bias}: best ratio found {top:.6f}  (50-digit re-evaluation: {ex:.6f}, K = {Kex:.3g})")
# general (non-product) reference: the same bound with c~_i = sup_{x_<i} osc_{x_i} F_i(x_<=i),
# F_i = -ln E_pi[e^{-r} | x_<=i]  (remark after A3.2); random pi, random r, exact enumeration
print("    non-product reference pi (random), ranges c~_i of the conditional free energy of the remainder:")
worst_np = {p: 0.0 for p in orders}
cnt_np = 0
for n in [3, 4, 5, 6]:
    states = all_states(n, 2)
    N = len(states)
    for _ in range(60):
        pi = dirichlet(N, float(rng.choice([0.3, 1.0, 5.0])))
        r = rng.normal(0, float(rng.choice([0.3, 1.0, 3.0])), N)
        y = np.exp(-(r - r.min()))
        ct = []
        for i in range(n):
            # group states by the prefix x_<=i  (states are in lexicographic order: prefix = index >> (n-i-1))
            key = np.arange(N) >> (n - i - 1)
            num = np.bincount(key, weights=pi * y, minlength=2 ** (i + 1))
            den = np.bincount(key, weights=pi, minlength=2 ** (i + 1))
            F = -np.log(num / den)                       # F_i(x_<=i), length 2^(i+1)
            ct.append(float(np.max(np.abs(F[0::2] - F[1::2]))))   # osc over x_i at fixed x_<i
        pg = pi * y
        pg /= pg.sum()
        K_t = sum(c * c for c in ct)
        sumL = sum(L(c) for c in ct if c > 0)
        cnt_np += 1
        for p in orders:
            d = renyi(pg, pi, p)
            worst_np[p] = max(worst_np[p], d / ((p - 1) * K_t / 8 + sumL))
print(f"      {cnt_np} instances; largest D_p/((p-1)K~/8 + sum_i L(c~_i)): "
      + "  ".join(f"p={p}: {worst_np[p]:.4f}" for p in orders))
u = 0.3
for n in [4, 12]:
    exact = n * math.log(1 + math.tanh(u / 2) ** 2)
    print(f"    additive cube instance r = u|x|, u={u}, n={n}: D_2 = n ln(1+tanh^2(u/2)) = {exact:.6f};"
          f"  K/4 = {n * u * u / 4:.6f};  K/2 = {n * u * u / 2:.6f}")

# ----------------------------------------------------------------------------------------------- C6
print("C6  T3 against the [0,1]-valued mean-estimation problem (X = e^{-(r-lo)} under the floor measure, mean m = Z(g)/Z(lo))")
for m, eps in [(0.5, 0.1), (math.exp(-3.0), 0.2), (math.exp(-3.7), 0.1), (math.exp(-15.6), 0.1)]:
    hinted = (1 / m - 1) / eps
    var_term = (1 - m) / (eps * eps * m)
    second = 1 / (eps * m)
    print(f"    m={m:.3e}, eps={eps}: (1/m-1)/eps = {hinted:.4g};  1/(eps m) = {second:.4g};"
          f"  max-variance term (1-m)/(eps^2 m) = {var_term:.4g};  ratio var/hinted = {var_term / hinted:.4g} = 1/eps")
# ----------------------------------------------------------------------------------------------- C7
print("C7  no-hint stopping rule at the centre of a constant box (exact failure probabilities)")
for (m, eps, delta) in [(math.exp(-3.0), 0.2, 0.05), (math.exp(-3.7), 0.1, 0.05), (0.5, 0.1, 0.01)]:
    N = math.ceil(math.log(1 / delta) * max((1 - m) / (eps * m), 1 / eps)) + 1
    worst = 0.0
    # alternatives: X = m with prob 1-q-q2, X = 1 with prob q (dip), X = 0 with prob q2 (bump)
    for q in np.linspace(0, 1, 2001):
        for q2 in np.linspace(0, 1 - q, 41):
            mean = (1 - q - q2) * m + q
            if not ((1 - eps) * m <= mean <= (1 + eps) * m):
                # the rule outputs m only if the first sample is m and the next N-1 agree with it
                worst = max(worst, (1 - q - q2) ** N)
    hinted = (1 / m - 1) / eps
    print(f"    m={m:.4f}, eps={eps}, delta={delta}: N = {N}; worst failure probability over alternatives = {worst:.4f}"
          f" (<= delta: {worst <= delta});  N / (hinted count (1/m-1)/eps) = {N / hinted:.2f}  [ln(1/delta) = {math.log(1 / delta):.2f}]")

# the theory division's own example (rho_- = rho_+ = 3, eps = 0.2 i.e. detection threshold eta = 0.1, delta = 0.05)
rho, eta, delta = 3.0, 0.1, 0.05
U, V = math.expm1(rho), -math.expm1(-rho)
p_thy = 0.5 * min(math.expm1(eta) / U, -math.expm1(-eta) / V)
N_thy = math.ceil(math.log(1 / delta) / p_thy)
m = math.exp(-rho)
q_dip = math.expm1(eta) * m / (1 - m)          # least pi-mass of a dip that raises ln Z by more than eta
q_bump = -math.expm1(-eta)                     # least pi-mass of a bump that lowers ln Z by more than eta
N_nohint = math.ceil(math.log(1 / delta) / min(q_dip, q_bump)) + 1
print(f"    theory division's example: hinted spot check with the half-half sampler: N = {N_thy} (they state 1088);"
      f" no-hint rule 'all N samples of pi agree': N = {N_nohint}"
      f"  [least detectable masses: dip {q_dip:.6f}, bump {q_bump:.6f}]")

# ----------------------------------------------------------------------------------------------- C8
print("C8  Hoeffding (4.12)-(4.13) with the mean position p: gap <= -w p + ln(1-p+p e^w) <= L(w)")
mxh = 0.0
ratios = []
skipped = 0
for _ in range(20000):
    w = float(rng.choice([0.5, 2.0, 6.0]))
    k = int(rng.integers(2, 8))
    y = np.sort(rng.uniform(0, w, k))
    y[0], y[-1] = 0.0, w
    pr = dirichlet(k, float(rng.choice([0.1, 1.0])))
    gap = math.log(float(np.dot(pr, np.exp(y)))) - float(np.dot(pr, y))
    p = float(np.dot(pr, y)) / w
    hb = -w * p + math.log1p(p * math.expm1(w))
    if hb < 1e-6:          # nearly degenerate law: gap and bound are both rounding noise
        skipped += 1       # (an unguarded first version reported a ratio 1.001 from such a case)
        continue
    mxh = max(mxh, gap / hb)
    ratios.append(hb / L(w))
print(f"    {20000 - skipped} laws ({skipped} nearly degenerate ones skipped): largest gap/Hoeffding bound = {mxh:.6f} (<= 1);"
      f" Hoeffding bound / L(w): median {float(np.median(ratios)):.3f}, max {max(ratios):.6f} (<= 1)")
print("done")
