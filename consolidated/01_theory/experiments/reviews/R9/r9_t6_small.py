# R9 test 6: Theorem F6 and Lemma F5 by brute force on small cubes (own code).
#  n = 3, 4: ALL subsets D (2^8 - 2, 2^16 - 2): mu_H(D), Phi_H(D), Phi_H^+(D);
#     (i)   exact tail function Xi_H(q) against the best ball with type-dependent radii around one centre (all centres,
#           all radius vectors) of measure <= q;
#     (ii)  the F6 statistic: theta = -ln mu_H(D)/n, e = ln Phi_H^+(D)/n, defect(D) = ln Phi_H^+(D) - n (R^max)^{-1}(theta),
#           and the least omega with theta <= R^max(e - omega) + omega;
#     (iii) Lemma F5 for random members of L_u (and fibre averages) against the exact Xi_0 of three references.
#  n = 5, 6: stochastic search (annealing over subsets) for a large defect.
import numpy as np, itertools, sys, time
from math import log, exp
from r9lib import Par
rng = np.random.default_rng(3)
t0 = time.time()

def cube(n):
    X = np.array(list(itertools.product([0, 1], repeat=n)), dtype=np.int64)
    return X, X.sum(axis=1), (X[:, None, :] != X[None, :, :]).sum(axis=2)

class RTab:
    """R^max and its inverse, vectorised (table in t; exact up to the t-grid)"""
    def __init__(self, P):
        self.P = P; self.ts, self.Fs, _ = P.table(); self.a = -P.ec(); self.E = P.E()[0]
        self.eg = np.linspace(-self.a, self.E, 20001); self.Rg = self.R(self.eg)
    def R(self, e):
        e = np.atleast_1d(np.asarray(e, dtype=float)); out = np.empty(e.shape)
        for i in range(0, e.size, 2000):
            ee = e.ravel()[i:i + 2000]
            out.ravel()[i:i + 2000] = np.maximum((self.Fs[None, :] - self.ts[None, :] * ee[:, None]).max(axis=1), np.maximum(0.0, -ee))
        return out
    def Rinv(self, th):
        th = np.atleast_1d(np.asarray(th, dtype=float))
        # R decreasing on [-a, E]: interpolate the inverse
        inv = np.interp(th, self.Rg[::-1], self.eg[::-1])
        return np.where(th >= self.a, -th, inv)
    def omega(self, theta, e):
        """least omega >= 0 with theta <= R(e - omega) + omega (vectorised bisection)"""
        theta = np.atleast_1d(theta); e = np.atleast_1d(e)
        lo = np.zeros(theta.shape); hi = np.full(theta.shape, 10.0)
        ok0 = theta <= self.R(e) + 1e-15
        for _ in range(45):
            mid = 0.5 * (lo + hi); good = theta <= self.R(e - mid) + mid
            hi = np.where(good, mid, hi); lo = np.where(good, lo, mid)
        return np.where(ok0, 0.0, hi)

def reference(P, n, tX, kind, g=0.0):
    if kind == 'H': psi = -n * P.v(tX / n)
    elif kind == 'zero': psi = np.zeros(len(tX))
    else: psi = g * tX.astype(float)
    logw = tX * log(P.p) + (n - tX) * log(P.q) - psi
    lnA = np.log(np.exp(logw).sum())
    return psi, np.exp(logw - lnA)

def all_subsets_stats(n, mu, s):
    """for all masks 1 .. 2^N - 2: mu(D), Phi(D), Phi^+(D).  For every x the points y are scanned in the order of
    increasing slack s(x,y); the first one outside D gives s(x -> D^c)."""
    N = 1 << n; M = 1 << N
    masks = np.arange(1, M - 1, dtype=np.int64)
    muD = np.zeros(masks.size); php = np.zeros(masks.size)
    for x in range(N):
        inx = (masks >> x) & 1 == 1
        order = np.argsort(s[x], kind='stable')
        slack = np.full(masks.size, np.nan)
        todo = inx.copy()
        for y in order:
            out = todo & ((masks >> int(y)) & 1 == 0)
            slack[out] = s[x, y]
            todo &= ~out
        muD += inx * mu[x]
        php += np.where(inx, mu[x] * np.exp(np.where(inx, slack, 0.0)), 0.0)
    return masks, muD, php - muD, php

def ball_family_masks(n, X, tX, dist):
    """all balls with type-dependent radii around one centre: D cap T_t = {x in T_t: d(x,s) <= r_t}, r_t in {-1,...}"""
    N = 1 << n; out = set()
    for c in range(N):
        per_type = []
        for t in range(n + 1):
            idx = np.where(tX == t)[0]; ds = sorted(set(dist[c, idx].tolist()))
            opts = [0]
            for r in ds:
                m = 0
                for x in idx:
                    if dist[c, x] <= r: m |= (1 << int(x))
                opts.append(m)
            per_type.append(opts)
        for combo in itertools.product(*per_type):
            m = 0
            for c_ in combo: m |= c_
            if 0 < m < (1 << N) - 1: out.add(m)
    return np.array(sorted(out), dtype=np.int64)

def run_exhaustive(n, pairs):
    X, tX, dist = cube(n); N = 1 << n
    fam = ball_family_masks(n, X, tX, dist)
    print(f"n={n}: {2**N - 2} subsets; family of balls with type-dependent radii: {fam.size} sets")
    for (p, u) in pairs:
        P = Par(p, u); T = RTab(P)
        psi, mu = reference(P, n, tX, 'H')
        s = u * dist + psi[:, None] - psi[None, :]
        assert s.min() > -1e-12
        masks, muD, phi, php = all_subsets_stats(n, mu, s)
        # (i) exact tail function against the family
        order = np.argsort(muD, kind='stable'); cummax = np.maximum.accumulate(phi[order]); qs = muD[order]
        fidx = fam - 1                               # index of a mask in the arrays
        fo = np.argsort(muD[fidx], kind='stable'); fq = muD[fidx][fo]; fcm = np.maximum.accumulate(phi[fidx][fo])
        pos = np.searchsorted(fq, qs + 1e-15, side='right') - 1
        ok = pos >= 0
        with np.errstate(divide='ignore', invalid='ignore'):
            ratio = np.where(ok & (fcm[np.maximum(pos, 0)] > 0), cummax / fcm[np.maximum(pos, 0)], 1.0)
        ir = int(np.argmax(ratio))
        # (ii) the F6 statistic
        theta = -np.log(muD) / n; e = np.log(php) / n
        defect = np.log(php) - n * T.Rinv(theta)
        om = T.omega(theta, e)
        i1 = int(np.argmax(defect)); i2 = int(np.argmax(om))
        # the same restricted to the family
        print(f"  p={p} u={u}: max_q Xi_H(q)/[best family set with mu<=q] = {ratio[ir]:.3f} (at q={qs[ir]:.4f});  "
              f"max defect ln Phi+ - n (R^max)^-1(theta) = {defect[i1]:.3f} = {defect[i1]/log(n):.2f} ln n (|D|={bin(int(masks[i1])).count('1')}, theta={theta[i1]:.3f}); "
              f"family only: {defect[fidx].max():.3f};  least omega for all sets = {om[i2]:.4f} (family only: {om[fidx].max():.4f})   [{time.time()-t0:.0f}s]")
        sys.stdout.flush()

def lemma_F5(n, pairs, ntrial=400):
    X, tX, dist = cube(n); N = 1 << n
    print(f"Lemma F5 on Q_{n} (exact Xi_0 from all subsets); random psi in L_u and fibre averages over a second block")
    for (p, u) in pairs:
        P = Par(p, u)
        for kind, g in (('H', 0.0), ('zero', 0.0), ('add', -0.5 * u), ('add', u)):
            psi0, mu0 = reference(P, n, tX, kind, g)
            s0 = u * dist + psi0[:, None] - psi0[None, :]
            masks, muD, phi, php = all_subsets_stats(n, mu0, s0)
            order = np.argsort(muD, kind='stable'); qs = muD[order]; cm = np.maximum.accumulate(phi[order])
            def Xi(q):
                j = np.searchsorted(qs, q * (1 + 1e-12) + 1e-15, side='right') - 1
                return cm[j] if j >= 0 else 0.0
            worst = -np.inf; wrong = 0; nthr = 0; eq = 0.0
            for trial in range(ntrial):
                # a random u-Lipschitz function: lower McShane envelope of random values at random points, or a fibre average
                if trial % 2 == 0:
                    k = int(rng.integers(1, 6)); pts = rng.integers(0, N, k); vals = rng.uniform(-2 * u, 2 * u, k)
                    psi = (vals[None, :] + u * dist[:, pts]).min(axis=1)
                    if trial % 4 == 0: psi = np.maximum(psi, rng.uniform(-u, u))
                    w = np.exp(-psi)
                else:
                    n2 = 2; X2, tX2, d2 = cube(n2); k = int(rng.integers(1, 5))
                    pa = rng.integers(0, N, k); pb = rng.integers(0, 4, k); vals = rng.uniform(-2 * u, 2 * u, k)
                    psi2 = (vals[None, None, :] + u * (dist[:, None, pa] + d2[None, :, pb])).min(axis=2)       # (N, 4)
                    pi2 = np.exp(tX2 * log(P.p) + (n2 - tX2) * log(P.q))
                    w = (np.exp(-psi2) * pi2[None, :]).sum(axis=1)
                wh = w / np.exp(-psi0)
                for t in np.unique(wh)[:-1]:
                    q = mu0[wh > t].sum(); lhs = (mu0 * np.maximum(wh - t, 0)).sum(); rhs = t * Xi(q)
                    worst = max(worst, (lhs - rhs) / max(rhs, 1e-300) if rhs > 0 else (0.0 if lhs <= 1e-15 else np.inf)); nthr += 1
                    eq = max(eq, lhs / rhs if rhs > 0 else 0.0)
                    # mutation: the slack with the wrong orientation  s'(x,y) = u d + psi0(y) - psi0(x)
            print(f"  p={p} u={u} reference {kind}{'' if kind!='add' else f'(gamma={g:+.2f})'}: {nthr} thresholds, max (lhs - rhs)/rhs = {worst:+.2e}, max lhs/rhs = {eq:.4f}")
        sys.stdout.flush()

def anneal(n, pairs, iters, restarts):
    X, tX, dist = cube(n); N = 1 << n
    print(f"n={n}: stochastic search over subsets ({restarts} restarts x {iters} steps) for a large omega(D) (least omega with theta <= R^max(e-omega)+omega)")
    for (p, u) in pairs:
        P = Par(p, u); T = RTab(P)
        psi, mu = reference(P, n, tX, 'H'); s = u * dist + psi[:, None] - psi[None, :]
        def stat(mem):
            so = np.where(mem[None, :], np.inf, s).min(axis=1)
            m = mu[mem].sum(); pp = (mu[mem] * np.exp(so[mem])).sum()
            th = -log(m) / n; e = log(pp) / n
            return float(T.omega(np.array([th]), np.array([e]))[0]), th, e
        best = (-np.inf, None)
        # the ball family for comparison: Hamming balls and single points
        fam = -np.inf
        for c in range(N):
            for r in range(0, n):
                mem = dist[c] <= r
                if mem.all(): continue
                fam = max(fam, stat(mem)[0])
        for r in range(restarts):
            kind = r % 3
            if kind == 0: mem = rng.uniform(size=N) < rng.uniform(0.05, 0.5)
            elif kind == 1: c = rng.integers(0, N); mem = dist[c] <= rng.integers(0, max(1, n // 2))
            else:
                c1, c2 = rng.integers(0, N, 2); mem = (dist[c1] <= rng.integers(0, 2)) | (dist[c2] <= rng.integers(0, 2))
            if mem.all() or not mem.any(): continue
            cur = stat(mem); Tm = 0.05
            for it in range(iters):
                j = rng.integers(0, N); mem2 = mem.copy(); mem2[j] = ~mem2[j]
                if rng.uniform() < 0.3:
                    j2 = rng.integers(0, N); mem2[j2] = ~mem2[j2]
                if mem2.all() or not mem2.any(): continue
                new = stat(mem2)
                if new[0] > cur[0] or rng.uniform() < exp((new[0] - cur[0]) / Tm): mem, cur = mem2, new
                Tm = max(Tm * 0.999, 0.002)
                if cur[0] > best[0]: best = (cur[0], mem.copy(), cur[1], cur[2])
        om, mem, th, e = best
        print(f"  p={p} u={u}: largest omega found = {om:.4f} at |D|={int(mem.sum())}, theta={th:.3f}, e={e:.3f};  Hamming balls only: {fam:.4f}   [{time.time()-t0:.0f}s]")
        sys.stdout.flush()

pairs = [(0.1, 2.0), (0.3, 1.0), (0.2, 4.0), (0.5, 1.0), (0.5, 2.0), (0.3, 3.0), (0.2, 6.0), (0.5, 4.0), (0.5, 6.0)]
mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
if mode in ('all', 'exh'):
    run_exhaustive(3, pairs)
    run_exhaustive(4, pairs)
if mode == 'exhA':            # the same in two halves (each well under ten minutes)
    run_exhaustive(3, pairs[:5]); run_exhaustive(4, pairs[:5])
if mode == 'exhB':
    run_exhaustive(3, pairs[5:]); run_exhaustive(4, pairs[5:])
if mode in ('all', 'f5'):
    lemma_F5(4, pairs[:3], ntrial=300)
if mode in ('all', 'anneal'):
    anneal(5, pairs[:5], 3000, 9)
    anneal(6, pairs[:3], 3000, 6)
print(f"[{time.time()-t0:.0f}s]")
