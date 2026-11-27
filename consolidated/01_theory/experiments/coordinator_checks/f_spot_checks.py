# Coordinator's independent spot checks of workstream F (biased cube), own code, numpy only.
import math, itertools, random
import numpy as np

def h2(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return -(x * np.log(x) + (1 - x) * np.log1p(-x))
def kl2(x, y):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return x * np.log(x / y) + (1 - x) * np.log((1 - x) / (1 - y))

def setup(p, u):
    q = 1 - p
    L0 = -math.log(q + p * math.exp(-u)); L1 = -math.log(p + q * math.exp(-u))
    eta1 = q * math.exp(-u) / (p + q * math.exp(-u)); eta0 = p * math.exp(-u) / (q + p * math.exp(-u))
    return q, L0, L1, eta0, eta1

def game_value(K):                       # min over mixtures M of centres (columns) of max over rows
    best = 1e300
    for w in np.linspace(0, 1, 200001):
        pass
    w = np.linspace(0, 1, 2000001)
    v = np.maximum(K[0, 0] * w + K[0, 1] * (1 - w), K[1, 0] * w + K[1, 1] * (1 - w))
    return v.min()

def F_closed(p, u, g, t):
    q, L0, L1, _, _ = setup(p, u)
    Zg = q + p * math.exp(-g)
    return -t * math.log(Zg) + math.log((1 - math.exp(-t * (u + g))) * math.exp(-t * L0)
                                         + (1 - math.exp(-t * (u - g))) * math.exp(-t * (L1 + g))) - math.log(1 - math.exp(-2 * t * u))

def F_game(p, u, g, t):
    q, L0, L1, _, _ = setup(p, u)
    Zg = q + p * math.exp(-g)
    Lam = [L0, L1]
    K = np.array([[math.exp(-t * (u * (a != b) - Lam[b] - g * a - math.log(Zg))) for b in (0, 1)] for a in (0, 1)])
    return -math.log(game_value(K))

print("(1) closed form of F(gamma,t) against a numerical 2x2 game value")
worst = 0
rng = random.Random(1)
for _ in range(40):
    p = rng.uniform(0.03, 0.97); u = rng.uniform(0.2, 3.0); g = rng.uniform(-0.95, 0.95) * u; t = rng.uniform(0.05, 0.98)
    worst = max(worst, abs(F_closed(p, u, g, t) - F_game(p, u, g, t)))
print("    max |closed - game| over 40 random cases:", f"{worst:.2e}")

T = np.linspace(1e-4, 1.0, 4001)
def Fstar(p, u, ngam=801):
    gam = np.linspace(-u * (1 - 1e-9), u * (1 - 1e-9), ngam)
    q, L0, L1, _, _ = setup(p, u)
    G, TT = np.meshgrid(gam, T, indexing="ij")
    Zg = q + p * np.exp(-G)
    Fv = -TT * np.log(Zg) + np.log((1 - np.exp(-TT * (u + G))) * np.exp(-TT * L0)
                                   + (1 - np.exp(-TT * (u - G))) * np.exp(-TT * (L1 + G))) - np.log(1 - np.exp(-2 * TT * u))
    i0 = np.argmin(np.abs(gam))
    return Fv.max(axis=0), Fv[i0], gam[Fv.argmax(axis=0)]

def Rfun(Fv, e):                          # max_t [F(t) - t e], including t = 0 (value 0)
    return max(0.0, float((Fv - T * e).max()))

print("(2),(3),(4) R_0 against max_m [h(m) - h((Lam_m+e)/u)]_+ ; p = 1/2 against KL((Lam1+e)/u || 1/2) ; R^max > R_0")
for (p, u) in [(0.5, 1.0), (0.5, 2.0), (0.1, 2.0), (0.3, 1.0), (0.05, 2.0)]:
    q, L0, L1, eta0, eta1 = setup(p, u)
    Fs, F0, gstar = Fstar(p, u)
    E = float((Fs / T).max()); E0 = float((F0 / T).max())
    for frac in (0.0, 0.3, 0.6):
        e = frac * E
        R0 = Rfun(F0, e); Rm = Rfun(Fs, e)
        ms = np.linspace(1e-4, 1 - 1e-4, 200001)
        rho = ((1 - ms) * L0 + ms * L1 + e) / u
        ok = rho <= np.minimum(ms, 1 - ms)
        R0b = float(np.max(np.where(ok, h2(ms) - h2(rho), 0.0)))
        line = f"    p={p} u={u} e={frac}E: R_0(game)={R0:.6f} R_0(ball form)={R0b:.6f} R^max={Rm:.6f}"
        if p == 0.5:
            lam1 = math.log(2 / (1 + math.exp(-u)))
            line += f"  KL((Lam1+e)/u||1/2)={float(kl2((lam1 + e) / u, 0.5)):.6f}"
        print(line)
    print(f"      thresholds: E_0={E0:.5f} E={E:.5f};  gamma* at e=0: {float(gstar[np.argmax(Fs)]):+.3f}")

print("(5) theta_na: max_m min{ I(S;X) : D(P_{X|S}||pi_s|P_S) <= x } against R^max(S^{-1}(x)); the same with R_0 must fail for p != 1/2")
def theta_na_maxmin(p, u, x, nm=121, ng=700):
    q, L0, L1, eta0, eta1 = setup(p, u)
    al = np.linspace(1e-6, 1 - 1e-6, ng); be = np.linspace(1e-6, 1 - 1e-6, ng)
    A, B = np.meshgrid(al, be, indexing="ij")           # A = P(X=0|S=1), B = P(X=1|S=0)
    best = 0.0
    for m in np.linspace(0.005, 0.995, nm):
        kap = m * (1 - A) + (1 - m) * B
        I = h2(kap) - m * h2(A) - (1 - m) * h2(B)
        Ic = m * kl2(A, eta1) + (1 - m) * kl2(B, eta0)
        feas = Ic <= x
        if feas.any():
            best = max(best, float(I[feas].min()))
    return best
def theta_from_pair(Fv, x):
    lo, hi = -5.0, 5.0                                   # solve e + R(e) = x (S nondecreasing)
    for _ in range(80):
        mid = (lo + hi) / 2
        if mid + Rfun(Fv, mid) < x: lo = mid
        else: hi = mid
    return Rfun(Fv, hi)
for (p, u) in [(0.5, 1.0), (0.1, 2.0), (0.3, 1.0)]:
    Fs, F0, _ = Fstar(p, u)
    E = float((Fs / T).max())
    for frac in (0.1, 0.4):
        x = frac * E
        mm = theta_na_maxmin(p, u, x)
        line = f"    p={p} u={u} x={frac}E: max-min={mm:.5f}  R^max(S^-1(x))={theta_from_pair(Fs, x):.5f}  with R_0 instead: {theta_from_pair(F0, x):.5f}"
        if p == 0.5:
            pu = 1 / (1 + math.exp(u)); rr = np.linspace(pu, 0.5, 2000001)
            line += f"  min{{KL(rho||1/2): KL(rho||p_u)<=x}}={float(kl2(rr[kl2(rr, pu) <= x].max(), 0.5)):.5f}"
        print(line)

print("(6) Theorem F4(a): type-wise quantiles of a u-Lipschitz weight are Lipschitz (brute force, n <= 9)")
bad = 0; cases = 0
for n in (5, 7, 9):
    V = list(range(2 ** n)); wt = np.array([bin(v).count("1") for v in V])
    for trial in range(60):
        u = rng.choice([0.5, 1.0, 2.0])
        # random u-Lipschitz function: McShane extension of random data
        k = rng.randint(2, 8); pts = rng.sample(V, k); vals = [rng.uniform(-u * n, u * n) for _ in pts]
        psi = np.array([min(vals[i] + u * bin(v ^ pts[i]).count("1") for i in range(k)) for v in V])
        w = np.exp(-psi)
        for qq in (0.02, 0.1, 0.3, 0.7):
            tk = []
            for kappa in range(n + 1):
                ws = np.sort(w[wt == kappa])[::-1]       # smallest value tau of w on the class with dens{w > tau} <= q
                cand = [tau for tau in ws if (ws > tau).mean() <= qq]
                tk.append(max(cand) if False else min([tau for tau in ws if (ws > tau).mean() <= qq]))
            for kappa in range(n):
                cases += 1
                if tk[kappa + 1] > math.exp(u) * tk[kappa] * (1 + 1e-12) or tk[kappa] > math.exp(u) * tk[kappa + 1] * (1 + 1e-12):
                    bad += 1
print(f"    {cases} adjacent pairs of type classes checked, violations: {bad}")
