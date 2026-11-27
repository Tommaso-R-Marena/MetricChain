# R9 test 3: Lemma SL by direct (primal) minimisation over kernels, own code.
#   V(P_UX, B) = min{ I(X';U) : u P(X' != X) + v(P_X') <= B },   claim: V <= R^max(B - alpha),  alpha = D(P_X|U || pi | P_U).
# Kernels are parametrised by nu_u = P(X'=1|U=u) (the cheapest coupling has P(X' != X | u) = |nu_u - mu_u|).
# (a) |U| = 2: brute-force grid + zoom (no solver);  (b) |U| <= 4: SLSQP in split variables, several starts;
# (c) equality at the "generalised dip" U = S ~ Bernoulli(m), X|S ~ cone law, maximised over m;
# (d) adversarial ascent over P_UX (random restarts + coordinate perturbations).
import numpy as np, time, sys
from scipy.optimize import minimize, minimize_scalar
from r9lib import Par, h, kl
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
t0 = time.time()

def Ifun(Pu, nu):
    nb = float(np.dot(Pu, nu))
    return float(h(nb) - np.dot(Pu, h(nu)))

def gfun(P, Pu, mu, nu, B):
    return P.u * float(np.dot(Pu, np.abs(nu - mu))) + float(P.v(np.dot(Pu, nu))) - B

def V_grid2(P, Pu, mu, B, N=601, zooms=6):
    lo = np.zeros(2); hi = np.ones(2); best = Ifun(Pu, mu)   # nu = mu is feasible (B >= v(P_X))
    for z in range(zooms):
        a = np.linspace(lo[0], hi[0], N)[:, None]; b = np.linspace(lo[1], hi[1], N)[None, :]
        nb = Pu[0] * a + Pu[1] * b
        I = h(nb) - Pu[0] * h(a) - Pu[1] * h(b)
        g = P.u * (Pu[0] * np.abs(a - mu[0]) + Pu[1] * np.abs(b - mu[1])) + P.v(nb) - B
        I = np.where(g <= 0, I, np.inf)
        k = int(np.argmin(I)); i, j = divmod(k, N)
        if not np.isfinite(I[i, j]): break
        best = min(best, float(I[i, j]))
        w = (hi - lo) / (N - 1) * 5
        c0 = np.array([a[i, 0], b[0, j]])
        lo = np.clip(c0 - w, 0, 1); hi = np.clip(c0 + w, 0, 1)
    return best

def V_slsqp(P, Pu, mu, B, nstart=6):
    k = len(Pu); best = Ifun(Pu, mu)
    def unpack(x): return np.clip(mu + x[:k] - x[k:], 1e-13, 1 - 1e-13)
    fI = lambda x: Ifun(Pu, unpack(x))
    fc = lambda x: B - (P.u * float(np.dot(Pu, x[:k] + x[k:])) + float(P.v(np.dot(Pu, unpack(x)))))
    bnds = [(0, 1 - m) for m in mu] + [(0, m) for m in mu]
    mub = float(np.dot(Pu, mu))
    starts = [np.zeros(2 * k)]
    # move every nu_u a fraction s towards a common value c (feasible if the budget allows)
    for c in (mub, P.kminus, P.kplus, 0.5 * (P.kminus + P.kplus), P.p):
        for s in (0.25, 0.6, 0.95):
            tgt = mu + s * (c - mu)
            starts.append(np.concatenate([np.maximum(tgt - mu, 0), np.maximum(mu - tgt, 0)]))
    for _ in range(nstart):
        tgt = np.clip(mu + rng.normal(0, 0.1, k), 1e-6, 1 - 1e-6)
        starts.append(np.concatenate([np.maximum(tgt - mu, 0), np.maximum(mu - tgt, 0)]))
    for x0 in starts:
        try:
            r = minimize(fI, x0, method='SLSQP', bounds=bnds, constraints=[{'type': 'ineq', 'fun': fc}], options={'ftol': 1e-14, 'maxiter': 400})
        except Exception:
            continue
        if fc(r.x) >= -1e-10 and np.isfinite(r.fun): best = min(best, float(r.fun))
    return best

def alpha_of(P, Pu, mu): return float(np.dot(Pu, kl(mu, P.p)))

def random_law(k):
    Pu = rng.dirichlet(np.ones(k) * rng.choice([0.5, 1.0, 3.0]))
    Pu = np.maximum(Pu, 1e-3); Pu /= Pu.sum()
    mode = rng.integers(0, 3)
    if mode == 0: mu = rng.uniform(0.001, 0.999, k)
    elif mode == 1: mu = rng.beta(0.4, 0.4, k).clip(1e-4, 1 - 1e-4)
    else: mu = np.clip(rng.uniform(0, 1) + rng.normal(0, 0.15, k), 1e-3, 1 - 1e-3)
    return Pu, mu

pairs = [(0.1, 2.0), (0.3, 1.0), (0.2, 4.0), (0.5, 1.0), (0.85, 2.5)]
print("(a),(b) random laws: V - R^max(B - alpha) must be <= 0")
glob = -1e9
for (p, u) in pairs:
    P = Par(p, u); E = P.E()[0]; a = -P.ec()
    worst = -1e9; wrec = None; cnt = 0; dgrid = 0.0; npos = 0; nneg = 0
    for trial in range(160):
        k = int(rng.choice([1, 2, 2, 2, 3, 4]))
        Pu, mu = random_law(k)
        al = alpha_of(P, Pu, mu); vP = float(P.v(np.dot(Pu, mu)))
        # B >= v(P_X); choose e = B - alpha in an interesting range of both signs when possible
        emin = vP - al
        e = emin + rng.choice([0.0, 0.02, 0.1, 0.3, 0.6, 1.0]) * rng.uniform(0, 1) * (E + a) + (0 if rng.uniform() < 0.3 else rng.uniform(0, max(0.0, -emin)))
        B = al + e
        Vs = V_slsqp(P, Pu, mu, B)
        if k == 2:
            Vg = V_grid2(P, Pu, mu, B); dgrid = max(dgrid, abs(Vg - Vs)); V = min(Vs, Vg)
        else: V = Vs
        R = P.Rmax(e); cnt += 1; npos += e > 0; nneg += e < 0
        if V - R > worst: worst = V - R; wrec = (k, Pu.round(4), mu.round(4), round(e, 5), V, R)
    glob = max(glob, worst)
    print(f"  p={p} u={u}: {cnt} laws (e>0: {npos}, e<0: {nneg}); max(V - R^max) = {worst:+.3e} at k={wrec[0]} P(u)={wrec[1]} mu={wrec[2]} e={wrec[3]} V={wrec[4]:.6f} R^max={wrec[5]:.6f}; |U|=2: max|grid - SLSQP| = {dgrid:.1e}   [{time.time()-t0:.0f}s]")
    sys.stdout.flush()
print(f"  overall max(V - R^max) = {glob:+.3e}")

print("(c) the generalised dip: U = S ~ Bernoulli(m), X|S ~ cone law; max_m V(m; alpha(m)+e) against R^max(e)")
for (p, u) in pairs[:4]:
    P = Par(p, u); E = P.E()[0]; a = -P.ec()
    for e in (-0.6 * a, -0.2 * a, 0.0, 0.3 * E, 0.7 * E):
        def Vm(m):
            Pu = np.array([1 - m, m]); mu = np.array([P.eta0, 1 - P.eta1])
            al = alpha_of(P, Pu, mu); B = al + e
            if B < float(P.v(np.dot(Pu, mu))): return -1.0      # the lemma does not apply (B < v(P_X))
            return min(V_slsqp(P, Pu, mu, B, nstart=2), V_grid2(P, Pu, mu, B, N=301, zooms=5))
        ms = np.linspace(0.03, 0.97, 48); vals = np.array([Vm(m) for m in ms]); i = int(np.argmax(vals))
        r = minimize_scalar(lambda m: -Vm(m), bounds=(ms[max(i - 1, 0)], ms[min(i + 1, 47)]), method='bounded', options={'xatol': 1e-6})
        best = max(-r.fun, vals[i]); mbest = r.x if -r.fun >= vals[i] else ms[i]
        print(f"  p={p} u={u} e={e:+.5f}: max_m V = {best:.8f} (m={mbest:.4f}), R^max(e) = {P.Rmax(e):.8f}, diff = {best-P.Rmax(e):+.2e}")
    sys.stdout.flush()

print("(d) adversarial ascent over P_UX (|U| = 2, 3), objective V - R^max(B - alpha)")
for (p, u) in pairs[:3]:
    P = Par(p, u); E = P.E()[0]; a = -P.ec()
    bestall = -1e9
    for rs in range(6):
        k = 2 if rs % 2 == 0 else 3
        Pu, mu = random_law(k)
        if rs < 2:   # start at the generalised dip
            m = rng.uniform(0.3, 0.7); Pu = np.array([1 - m, m] + [1e-3] * (k - 2)); Pu /= Pu.sum(); mu = np.array([P.eta0, 1 - P.eta1] + [0.5] * (k - 2))
        slack = rng.uniform(0, 1) * 0.5 * E     # B = v(P_X) + something, re-derived at every step from e
        e = rng.choice([-0.5 * a, -0.1 * a, 0.0, 0.3 * E])
        def obj(Pu, mu):
            al = alpha_of(P, Pu, mu); B = al + e
            if B < float(P.v(np.dot(Pu, mu))): return -9.0
            V = V_slsqp(P, Pu, mu, B, nstart=1)
            if len(Pu) == 2: V = min(V, V_grid2(P, Pu, mu, B, N=201, zooms=4))
            return V - P.Rmax(e)
        cur = obj(Pu, mu); step = 0.08
        for it in range(60):
            Pu2 = np.maximum(Pu * np.exp(rng.normal(0, step, k)), 1e-4); Pu2 /= Pu2.sum()
            mu2 = np.clip(mu + rng.normal(0, step, k) * (rng.uniform(size=k) < 0.7), 1e-4, 1 - 1e-4)
            val = obj(Pu2, mu2)
            if val > cur: Pu, mu, cur = Pu2, mu2, val
            else: step = max(step * 0.93, 0.004)
        bestall = max(bestall, cur)
        print(f"  p={p} u={u} restart {rs} (k={k}, e={e:+.4f}): best V - R^max = {cur:+.3e} at P(u)={Pu.round(4)} mu={mu.round(4)}   [{time.time()-t0:.0f}s]")
        sys.stdout.flush()
    print(f"  p={p} u={u}: best over restarts = {bestall:+.3e}")
print(f"[{time.time()-t0:.1f}s]")
