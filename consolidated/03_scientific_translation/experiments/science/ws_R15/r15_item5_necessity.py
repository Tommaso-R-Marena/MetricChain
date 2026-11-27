#!/usr/bin/env python3
"""R15, Item 5 -- the necessity argument of Proposition 11.113(d) (theory report at f7df44f; THY-RES-0012 section 1.2):
own recomputation of the table (Pinsker bound, N_TV, N_KL at five pairs (Delta, eps)), and brute-force checks of the
two probabilistic steps of the argument.  Written from the statement; nothing imported from the theory harness.

Notation: c = 1/(e^Delta - 1); ln Z = const + ln(c + E_q W); the random two-level member has W = 1_D, D containing every
state independently with probability w;  w' = w + (e^{2 eps} - 1)(c + w)  (so c + w' = e^{2 eps}(c + w));  delta = 0.05.

PART 1  the table.
PART 2  the constants: w* = c/(1 + 2c) maximises w(1 - w)/(c + w)^2 with value sinh^2(Delta/2); either direction of the
        Kullback-Leibler divergence may be used in Pinsker's inequality; when w' <= 1; the best w at finite eps; the
        Bretagnolle-Huber form; the expected-number version.
PART 3  "one fresh bit of probability w whatever the algorithm does": for random adaptive decision trees on a small
        state space the law of the transcript under the prior is exactly Bernoulli(w)^N (enumeration of all D).
PART 4  "q(D) is within o(1) of w with probability 1 - o(1) under max q -> 0": Var q(D) = w(1 - w) sum q^2 <= w(1-w) max q
        (exact, by enumeration on a small space; and the size of sum q^2 needed for the fluctuation of ln Z to be
        small against eps).
PART 5  the exact failure probability of the plug-in estimate on two-level members with N_KL and N_KL/4 evaluations.

Run:  OMP_NUM_THREADS=1 python3 r15_item5_necessity.py > logs/item5_necessity.log
"""
import itertools, math, resource, time
import numpy as np
from scipy import stats, optimize

t0 = time.time()
ok_all = True
DELTA = 0.05
PAIRS = [(0.0605, 0.01), (0.5, 0.03), (1.0, 0.05), (2.0, 0.08), (3.0, 0.1)]
THEIRS = {(0.0605, 0.01): (5.7, 20, 68), (0.5, 0.03): (57, 189, 528), (1.0, 0.05): (89, 289, 815), (2.0, 0.08): (181, 575, 1634),
          (3.0, 0.1): (384, 1209, 3455)}


def check(cond, msg):
    global ok_all
    if not cond:
        ok_all = False
        print("   !!! CHECK FAILED:", msg)


def kl(a, b):
    """KL(Bernoulli(a) || Bernoulli(b)); +inf if a is outside [0, 1]"""
    if a < 0 or a > 1:
        return math.inf
    s = 0.0
    if a > 0:
        s += a * math.log(a / b)
    if a < 1:
        s += (1 - a) * math.log((1 - a) / (1 - b))
    return s


def tv_binom(N, a, b):
    k = np.arange(N + 1)
    return 0.5 * float(np.abs(stats.binom.pmf(k, N, a) - stats.binom.pmf(k, N, b)).sum())


def n_tv(a, b, target):
    """least N with TV(Bin(N, a), Bin(N, b)) >= target (the total variation of product laws is nondecreasing in N)"""
    lo, hi = 1, 1
    while tv_binom(hi, a, b) < target:
        hi *= 2
    while lo < hi:
        mid = (lo + hi) // 2
        if tv_binom(mid, a, b) >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo


def n_kl(Delta, eps, delta, ws):
    """least N with ln(2/delta) <= N min(KL(w + t+ || w), KL(w - t- || w)) for every mean w of the list:
    then the plug-in estimate ln(c + What) is within eps of ln(c + w) with probability >= 1 - delta (Hoeffding 1963, Thm 1)"""
    c = 1 / math.expm1(Delta)
    worst, at = 0.0, None
    for w in ws:
        tp, tm = math.expm1(eps) * (c + w), -math.expm1(-eps) * (c + w)
        need = math.log(2 / delta) / min(kl(w + tp, w), kl(w - tm, w))
        if need > worst:
            worst, at = need, w
    return math.ceil(worst), worst, at


print(f"R15 item 5; delta = {DELTA}")
print("PART 1  the table of THY-RES-0012 section 1.2, recomputed")
print(f"  {'Delta':>7} {'eps':>5} | {'w*':>7} {'w_prime':>7} {'KL(w||w_)':>10} {'KL(w_||w)':>10} | {'Pinsker':>8} {'theirs':>7} | {'N_TV':>5} {'theirs':>6} | "
      f"{'N_KL grid400':>12} {'theirs':>6} {'N_KL fine':>9} | {'N_TV/Pin':>8} {'N_KL/N_TV':>9} | {'approx (1-2d)^2 sinh^2/eps^2':>28} {'Pin/approx':>10}")
rows = []
for Delta, eps in PAIRS:
    c = 1 / math.expm1(Delta)
    w = c / (1 + 2 * c)
    w2 = w + math.expm1(2 * eps) * (c + w)
    check(abs((math.log(c + w2) - math.log(c + w)) - 2 * eps) < 1e-12, "the two values of ln Z differ by 2 eps")
    check(w2 <= 1, "w' exceeds 1")
    k1, k2 = kl(w, w2), kl(w2, w)
    pin = 2 * (1 - 2 * DELTA) ** 2 / k1
    ntv = n_tv(w, w2, 1 - 2 * DELTA)
    grid = [i / 400 for i in range(1, 400)]
    nkl, raw, at = n_kl(Delta, eps, DELTA, grid)
    fine = [i / 20000 for i in range(1, 20000)]
    nkl_f, raw_f, at_f = n_kl(Delta, eps, DELTA, fine)
    approx = (1 - 2 * DELTA) ** 2 * math.sinh(Delta / 2) ** 2 / eps ** 2
    th = THEIRS[(Delta, eps)]
    rows.append((Delta, eps, pin, ntv, nkl, nkl_f, k1, k2, w, w2))
    print(f"  {Delta:>7} {eps:>5} | {w:>7.4f} {w2:>7.4f} {k1:>10.6f} {k2:>10.6f} | {pin:>8.2f} {th[0]:>7} | {ntv:>5d} {th[1]:>6} | "
          f"{nkl:>12d} {th[2]:>6} {nkl_f:>9d} | {ntv / pin:>8.2f} {nkl / ntv:>9.2f} | {approx:>28.2f} {pin / approx:>10.3f}")
    check(abs(pin - th[0]) <= (0.06 if th[0] < 10 else 0.6), f"Pinsker bound {pin} vs theirs {th[0]}")
    check(ntv == th[1], f"N_TV {ntv} vs theirs {th[1]}")
    check(nkl == th[2], f"N_KL {nkl} vs theirs {th[2]}")
    check(pin <= ntv <= nkl, "ordering Pinsker <= N_TV <= N_KL")
print("  ratios quoted by the theory division:")
for Delta, eps, pin, ntv, nkl, nkl_f, k1, k2, w, w2 in rows:
    closed = 2 * math.log(2 / DELTA) * math.sinh(Delta / 2) ** 2 / eps ** 2
    first = math.log(2 / DELTA) * math.expm1(Delta) ** 2 / (2 * eps ** 2)
    print(f"   Delta = {Delta}, eps = {eps}: N_KL / [2 ln(2/delta) sinh^2(Delta/2)/eps^2] = {nkl / closed:.4f} (they assert 0.95..1.12); "
          f"N_KL e^Delta / first-version count = {nkl * math.exp(Delta) / first:.4f} (they: 1.007..1.033); "
          f"count of (c) x e^-Delta: factor e^-Delta = {math.exp(-Delta):.3f}")
    check(0.95 <= nkl / closed <= 1.12, "N_KL over closed form")
r1 = [nkl * math.exp(D) / (math.log(2 / DELTA) * math.expm1(D) ** 2 / (2 * e ** 2)) for D, e, _, _, nkl, *_ in rows]
print(f"   range of N_KL e^Delta / first-version count over the five pairs: {min(r1):.4f} .. {max(r1):.4f}")
print(f"   largest N_TV / Pinsker: {max(r[3] / r[2] for r in rows):.3f}; largest N_KL / N_TV: {max(r[4] / r[3] for r in rows):.3f} (they: 'within a factor 3.5')")

print("PART 2  constants")
# (a) the maximiser of w(1-w)/(c+w)^2
for Delta in (0.0605, 0.5, 1.0, 2.0, 3.0, 6.0):
    c = 1 / math.expm1(Delta)
    f = lambda w: -w * (1 - w) / (c + w) ** 2
    res = optimize.minimize_scalar(f, bounds=(1e-9, 1 - 1e-9), method="bounded", options=dict(xatol=1e-12))
    check(abs(res.x - c / (1 + 2 * c)) < 1e-6 and abs(-res.fun - math.sinh(Delta / 2) ** 2) < 1e-9 * max(1, math.sinh(Delta / 2) ** 2),
          "maximiser of w(1-w)/(c+w)^2")
print("   w(1 - w)/(c + w)^2 is largest at w = c/(1 + 2c), where it equals 1/(4c(1 + c)) = sinh^2(Delta/2): confirmed numerically at six widths")
# (b) w' <= 1 needs e^{2 eps} <= (e^Delta + 1)/2
for Delta, eps in PAIRS:
    c = 1 / math.expm1(Delta)
    w = c / (1 + 2 * c)
    lim = 0.5 * math.log((math.exp(Delta) + 1) / 2)
    w2 = w + math.expm1(2 * lim) * (c + w)
    check(abs(w2 - 1) < 1e-9, "threshold for w' = 1")
    print(f"   Delta = {Delta}: w' <= 1 at w* needs eps <= (1/2) ln((e^Delta + 1)/2) = {lim:.5f}; table eps = {eps} ({'ok' if eps <= lim else 'VIOLATED'}); "
          f"'small eps' for the approximation means eps << (1 - e^-Delta)/4 = {(-math.expm1(-Delta)) / 4:.4f}")
# (c) the best w at finite eps, both directions of KL, Bretagnolle-Huber
print("   best two-point bound over w at finite eps (Pinsker with the smaller of the two divergences; Bretagnolle-Huber: N >= ln(1/(4 delta))/KL):")
for Delta, eps in PAIRS:
    c = 1 / math.expm1(Delta)
    best = (0, None)
    bestbh = (0, None)
    for i in range(1, 2000):
        w = i / 2000
        w2 = w + math.expm1(2 * eps) * (c + w)
        if w2 >= 1:
            break
        m = min(kl(w, w2), kl(w2, w))
        b = 2 * (1 - 2 * DELTA) ** 2 / m
        bh = math.log(1 / (4 * DELTA)) / m
        if b > best[0]:
            best = (b, w)
        if bh > bestbh[0]:
            bestbh = (bh, w)
    wstar = c / (1 + 2 * c)
    w2s = wstar + math.expm1(2 * eps) * (c + wstar)
    print(f"   Delta = {Delta}, eps = {eps}: at w*: Pinsker with KL(w||w') {2 * (1 - 2 * DELTA) ** 2 / kl(wstar, w2s):.2f}, with KL(w'||w) "
          f"{2 * (1 - 2 * DELTA) ** 2 / kl(w2s, wstar):.2f}; best over w: {best[0]:.2f} at w = {best[1]:.4f} (w* = {wstar:.4f}); "
          f"N_TV at that w: {n_tv(best[1], best[1] + math.expm1(2 * eps) * (c + best[1]), 1 - 2 * DELTA)}; Bretagnolle-Huber at w*: "
          f"{math.log(1 / (4 * DELTA)) / min(kl(wstar, w2s), kl(w2s, wstar)):.2f}")
# Bretagnolle-Huber checked numerically on the binomial pairs of the table: 1 - TV >= (1/2) exp(-N KL)
viol = 0
for Delta, eps, pin, ntv, nkl, nkl_f, k1, k2, w, w2 in rows:
    for N in (1, 2, 5, ntv // 2, ntv, 2 * ntv, nkl):
        if N < 1:
            continue
        tv = tv_binom(N, w, w2)
        if 1 - tv < 0.5 * math.exp(-N * min(k1, k2)) - 1e-12:
            viol += 1
        if tv > math.sqrt(-math.expm1(-N * min(k1, k2))) + 1e-12:          # the form TV <= sqrt(1 - e^{-KL})
            viol += 1
        if tv > math.sqrt(N * min(k1, k2) / 2) + 1e-12:
            viol += 1
check(viol == 0, "Pinsker or Bretagnolle-Huber violated numerically")
print(f"   Pinsker (TV <= sqrt(KL/2)) and Bretagnolle-Huber (TV <= sqrt(1 - exp(-KL)), hence 1 - TV >= exp(-KL)/2) hold on all binomial pairs tried (violations: {viol})")
print("   Bretagnolle-Huber with TV >= 1 - 2 delta:  N >= ln(1/(4 delta (1 - delta)))/KL  (>= ln(1/(4 delta))/KL, the form printed as 'Bretagnolle-Huber' in this log)")
for Delta, eps, pin, ntv, nkl, nkl_f, k1, k2, w, w2 in rows:
    print(f"      Delta = {Delta}, eps = {eps}: ln(1/(4 delta (1 - delta)))/min KL = {math.log(1 / (4 * DELTA * (1 - DELTA))) / min(k1, k2):.2f}  (Pinsker with the same divergence {2 * (1 - 2 * DELTA) ** 2 / min(k1, k2):.2f})")
for dl in (0.05, 0.01, 0.001, 1e-6):
    Delta, eps = 1.0, 0.05
    c = 1 / math.expm1(Delta); w = c / (1 + 2 * c); w2 = w + math.expm1(2 * eps) * (c + w)
    m = min(kl(w, w2), kl(w2, w))
    ntv = n_tv(w, w2, 1 - 2 * dl) if dl >= 1e-3 else None
    grid = [i / 400 for i in range(1, 400)]
    print(f"   delta = {dl}: (Delta, eps) = (1, 0.05): Pinsker {2 * (1 - 2 * dl) ** 2 / m:.1f}, Bretagnolle-Huber {math.log(1 / (4 * dl)) / m:.1f}, "
          f"N_TV {ntv}, N_KL {n_kl(Delta, eps, dl, grid)[0]}  -- Pinsker saturates at 2/KL = {2 / m:.1f} as delta -> 0, the other two grow like ln(1/delta)")
# (d) expected-number version
u = 1 - 2 * DELTA
K = 4 / u
check(abs((2 * (u - 2 / K) ** 2 / K) - u ** 3 / 8) < 1e-15, "expected-number constant")
Kopt = 6 / u
print(f"   expected number: truncating at K times the expectation gives N_exp >= 2 (1 - 2 delta - 2/K)^2 / (K KL); K = 4/(1 - 2 delta): (1 - 2 delta)^3/(8 KL) [confirmed]; "
      f"the best K is 6/(1 - 2 delta): 4 (1 - 2 delta)^3/(27 KL), larger by the factor {(2 * (u - 2 / Kopt) ** 2 / Kopt) / (u ** 3 / 8):.4f}")

print("PART 3  the transcript of an adaptive algorithm under the prior is a string of independent Bernoulli(w) bits (exact enumeration)")
rng = np.random.default_rng(5)
worst = 0.0
ntrees = 0
for M, N in ((5, 3), (6, 4), (7, 4), (8, 5)):
    for trial in range(20):
        w = float(rng.uniform(0.1, 0.9))
        # a random adaptive deterministic rule: the next state is a function of the bits seen so far (never a state already evaluated)
        rule = {}

        def next_state(bits, seen):
            key = bits
            if key not in rule:
                rule[key] = int(rng.choice([x for x in range(M) if x not in seen]))
            return rule[key]

        law = {}
        for D in itertools.product((0, 1), repeat=M):
            pD = math.prod(w if d else 1 - w for d in D)
            bits, seen = (), []
            for _ in range(N):
                x = next_state(bits, seen)
                seen.append(x)
                bits = bits + (D[x],)
            law[bits] = law.get(bits, 0.0) + pD
        for bits in itertools.product((0, 1), repeat=N):
            prod = math.prod(w if b else 1 - w for b in bits)
            worst = max(worst, abs(law.get(bits, 0.0) - prod))
        ntrees += 1
check(worst < 1e-12, "transcript law is not the product law")
print(f"   {ntrees} random adaptive rules on 5 to 8 states, 3 to 5 evaluations: largest deviation of the transcript law from Bernoulli(w)^N: {worst:.1e}")

print("PART 4  fluctuation of q(D)")
rng = np.random.default_rng(7)
for M in (10, 14):
    q = rng.dirichlet(np.ones(M) * 0.7)
    w = 0.3
    mean = var = 0.0
    for D in itertools.product((0, 1), repeat=M):
        pD = math.prod(w if d else 1 - w for d in D)
        qd = float(np.dot(q, D))
        mean += pD * qd; var += pD * qd * qd
    var -= mean ** 2
    check(abs(mean - w) < 1e-12 and abs(var - w * (1 - w) * float((q ** 2).sum())) < 1e-12, "moments of q(D)")
    print(f"   M = {M}: E q(D) = {mean:.6f} (w = {w}); Var q(D) = {var:.6f} = w(1-w) sum q^2 = {w * (1 - w) * float((q ** 2).sum()):.6f} <= w(1-w) max q = {w * (1 - w) * q.max():.6f}")
print("   the fluctuation of ln Z is sd(q(D))/(c + w); against eps it needs  sum_x q(x)^2  <<  eps^2 (c + w)^2 / (w(1 - w))  =  eps^2 / sinh^2(Delta/2) at w*:")
for Delta, eps in PAIRS:
    print(f"      Delta = {Delta}, eps = {eps}: sum q^2 << {eps ** 2 / math.sinh(Delta / 2) ** 2:.3e}, i.e. many more than {math.sinh(Delta / 2) ** 2 / eps ** 2:.0f} effective states "
          f"(the count itself is of that order: {(1 - 2 * DELTA) ** 2 * math.sinh(Delta / 2) ** 2 / eps ** 2:.0f} .. {2 * math.log(2 / DELTA) * math.sinh(Delta / 2) ** 2 / eps ** 2:.0f})")

print("PART 5  exact failure probability of the plug-in estimate on two-level members")


def plugin_failure(Delta, eps, N, w):
    c = 1 / math.expm1(Delta)
    k = np.arange(N + 1)
    pm = stats.binom.pmf(k, N, w)
    dev = k / N - w
    return float(pm[(dev > math.expm1(eps) * (c + w) + 1e-15) | (dev < math.expm1(-eps) * (c + w) - 1e-15)].sum())


wf, qf = [], []
for Delta, eps, pin, ntv, nkl, *_ in rows:
    g60 = [i / 60 for i in range(1, 60)]
    g600 = [i / 600 for i in range(1, 600)]
    a = max(plugin_failure(Delta, eps, nkl, w) for w in g60)
    a2 = max(plugin_failure(Delta, eps, nkl, w) for w in g600)
    b = max(plugin_failure(Delta, eps, max(nkl // 4, 1), w) for w in g60)
    wf.append(a); qf.append(b)
    print(f"   Delta = {Delta}, eps = {eps}: N_KL = {nkl}: worst failure on the grid i/60: {a:.5f} (grid i/600: {a2:.5f}); with N_KL // 4 = {nkl // 4}: {b:.4f}")
    check(a2 <= DELTA, "plug-in fails with probability above delta at N_KL")
print(f"   largest over the five pairs with N_KL: {max(wf):.4f} (they: at most 0.0072); least over the five pairs with a quarter: {min(qf):.3f} (they: at least 0.16)")
check(max(wf) <= 0.0072 + 5e-5 and min(qf) >= 0.16 - 5e-3, "their two numbers")

print("ALL CHECKS PASSED" if ok_all else "SOME CHECK FAILED")
print(f"seconds {time.time() - t0:.1f}")
print("peak RSS MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
