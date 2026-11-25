# Coordinator's independent spot checks of workstream K (own code).
import math
from fractions import Fraction
from math import comb, exp, log, sqrt

def kl(r, p):
    if r <= 0: return -math.log(1 - p)
    if r >= 1: return -math.log(p)
    return r * math.log(r / p) + (1 - r) * math.log((1 - r) / (1 - p))

def consts(u):
    pu = 1 / (1 + exp(u)); lam1 = log(2 / (1 + exp(-u))); es = log(math.cosh(u / 2))
    return pu, lam1, es, kl(pu, .5), kl(lam1 / u, .5)

def theta_na(e, u):
    pu, lam1, es, a, h = consts(u)
    if e >= es: return 0.0
    lo, hi = pu, .5                      # largest rho in [pu, 1/2] with KL(rho||pu) <= e
    for _ in range(200):
        mid = (lo + hi) / 2
        if kl(mid, pu) <= e: lo = mid
        else: hi = mid
    return kl(lo, .5)

def theta_hint(e, u):
    pu, lam1, es, a, h = consts(u)
    return kl((lam1 + e) / u, .5) if e < es else 0.0

# (1) tau_2 closed form: min_phi max((1-phi) a, phi a + (1-phi) theta_na(phi a/(1-phi)))
for u in (0.5, 1.0, 2.0):
    pu, lam1, es, a, h = consts(u)
    best = min(max((1 - f) * a, f * a + (1 - f) * theta_na(f * a / (1 - f), u)) for f in [i / 20000 for i in range(1, 20000)])
    # sup over gamma in [0, phi a] of gamma + (1-phi) theta_na(gamma/(1-phi)) could exceed the endpoint value: check
    def Rphi(f):
        vals = [(1 - f) * a]
        for i in range(1, 401):
            g = f * a * i / 400
            vals.append(g + (1 - f) * theta_na(g / (1 - f), u))
        return max(vals)
    best2 = min(Rphi(i / 400) for i in range(1, 400))
    print(f"u={u}: h/a={h/a:.4f}  tau2/a closed={best/a:.4f}  tau2/a full sup={best2/a:.4f}")

# (2) necessary condition K5(b): for T = theta_hint, R_phi[T](0) >= h for all phi; and the two-rung bound
for u in (0.5, 1.0, 2.0):
    pu, lam1, es, a, h = consts(u)
    worst = 1e9; worst2 = 1e9
    for i in range(1, 200):
        f = i / 200
        val = max([(1 - f) * h] + [min(g, f * a) + (1 - f) * theta_hint(g / (1 - f), u) for g in [f * a * j / 300 for j in range(0, 301)]])
        worst = min(worst, val)
        for j in range(1, 60):
            xi = es * j / 60
            worst2 = min(worst2, max(f * a + (1 - f) * theta_hint(xi, u), (1 - f) * (xi + h)))
    print(f"u={u}: min_phi R_phi[theta_hint](0)/h = {worst/h:.6f} (must be >= 1);  two-rung min/h = {worst2/h:.6f} (must be >= 1)")

# (3) Lemma K.4(a),(b) in exact arithmetic for m <= 400
def tables(m, u):
    eu = exp(u)
    ball = [0] * (m + 2); s = 0
    for r in range(m + 1):
        s += comb(m, r); ball[r + 1] = s            # ball[r+1] = |B(m,r)|, ball[0] = |B(m,-1)| = 0
    return ball

def E_r(m, r, u):   # sum_{j<=r} C(m,j)(e^{u(r+1-j)} - 1), log-sum for stability via floats of big ints
    return math.fsum(comb(m, j) * (exp(u * (r + 1 - j)) - 1) for j in range(r + 1))
def T_m(m, k, u):
    return math.fsum(comb(m, j) * exp(-u * max(j - k, 0)) for j in range(m + 1))

bad = 0; worstA = 0; worstB = 0
for u in (0.5, 1.0, 2.0):
    pu = 1 / (1 + exp(u))
    for eta in (0.25, 0.5):
        ceta = Fraction(1) * (1 - Fraction(eta)) / (1 + Fraction(eta))
        m0 = math.ceil(log(1 / float(ceta)) / u)
        for m in (20, 57, 150, 400):
            ball = tables(m, u)
            for r in range(0, int(pu * (m + 1)) + 1):
                gam = (exp(u) - 1) if r == 0 else E_r(m, r, u) / ball[r]
                worstA = max(worstA, gam / (2 * exp(u) * m))
                if gam > 2 * exp(u) * m * (1 + 1e-12): bad += 1
            for r in range(0, int(pu * m) + 1):
                target = max(Fraction(1), ceta * ball[r])           # max{1, c_eta |B(m,r-1)|}
                k = max(kk for kk in range(0, m + 1) if ball[kk + 1] <= target)
                if r >= 1 and k < r - 1 - m0: bad += 1
                gam2 = E_r(m, r, u) / T_m(m, k, u)
                binle = math.fsum(comb(m, j) * pu ** j * (1 - pu) ** (m - j) for j in range(r + 1))
                bound = 2 * exp(u * (m0 + 2)) * binle
                worstB = max(worstB, gam2 / bound)
                if gam2 > bound * (1 + 1e-9): bad += 1
print("Lemma K.4(a),(b): violations =", bad, " max ratio (a) =", round(worstA, 3), " max ratio (b) =", round(worstB, 3))

# (4) binomial median fact used: P(Bin(m,p) >= k) >= 1/2 for every integer k <= m p
badm = 0
for m in range(1, 200):
    for p in (0.05, 0.119, 0.2689, 0.3775, 0.5):
        k = math.floor(m * p)
        tail = math.fsum(comb(m, j) * p ** j * (1 - p) ** (m - j) for j in range(k, m + 1))
        if tail < 0.5 - 1e-12: badm += 1
print("binomial median fact: violations =", badm)
