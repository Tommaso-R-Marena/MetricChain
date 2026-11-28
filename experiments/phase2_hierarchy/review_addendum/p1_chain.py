#!/usr/bin/env python3
"""Reviewer's own re-evaluation of the proof of Theorem P (HIERARCHY_ADDENDUM.md, sections A1-A2) from the definitions.

Nothing is imported from the author's scripts.  Parts:
  C   facts (C1)-(C4) on random data, including boundary values 0/1 and cells with classes on both sides of 1/2
  A   the chain y -> e -> e' -> m' -> p (Steps 1-5) on random and adversarial instances; every intermediate claim is
      evaluated separately
  O   direct maximisation over y of  B(y) := r(p) - r(y) + u||y - e'|| - (h - theta)   (the proof says B <= 0)
  L   theta < h: the inequality of the theorem still holds (either the chain, or s = 1 and (H1) alone)
"""
import sys, time
import numpy as np
from multiprocessing import Pool

LN2 = float(np.log(2.0))
NB = 70          # bisection steps


def f(t):
    t = np.asarray(t, dtype=float)
    a = np.where(t > 0, t, 1.0)
    b = np.where(t < 1, 1.0 - t, 1.0)
    return LN2 + t * np.log(a) + (1.0 - t) * np.log(b)


def consts(u):
    pu = 1.0 / (1.0 + np.exp(u))
    L1 = float(np.log(2.0 / (1.0 + np.exp(-u))))
    kap = L1 / u
    return pu, L1, kap, float(f(kap)), float(f(pu))


def rate(z, w):
    return float(np.dot(w, f(z)))


def avg(z, w, G):
    out = np.array(z, dtype=float)
    for g in G:
        out[g] = np.dot(w[g], z[g]) / np.sum(w[g])
    return out


def cost(z, w, G):
    return rate(z, w) - rate(avg(z, w, G), w)


def dist(z, zz, w):
    return float(np.dot(w, np.abs(z - zz)))


def clip(z, l):
    return np.minimum(np.maximum(z, l), 1.0 - l)


def fill(e, w, g, target, up):
    """max(e, lam) (up) or min(e, lam) (down) on the cell g, lam chosen so that the weighted mean is `target`"""
    lo, hi = 0.0, 1.0
    wg = w[g] / np.sum(w[g])
    eg = e[g]
    for _ in range(NB):
        mid = 0.5 * (lo + hi)
        v = np.maximum(eg, mid) if up else np.minimum(eg, mid)
        if np.dot(wg, v) < target:
            lo = mid
        else:
            hi = mid
    lam = 0.5 * (lo + hi)
    return (np.maximum(eg, lam) if up else np.minimum(eg, lam)), lam


def chain(y, w, G1, G2, u, theta):
    """the construction of Step 1; returns every quantity the proof makes a claim about"""
    pu, L1, kap, h, a = consts(u)

    def parts(s):
        e = clip(y, s * kap)
        m = avg(e, w, G2)
        mp = clip(m, kap)
        return e, m, mp, cost(e, w, G2) + cost(mp, w, G1)

    Phi0, Phi1 = parts(0.0)[3], parts(1.0)[3]
    lo, hi = 0.0, 1.0
    for _ in range(NB):
        mid = 0.5 * (lo + hi)
        if parts(mid)[3] > theta:
            lo = mid
        else:
            hi = mid
    s = hi
    e, m, mp, Phi = parts(s)
    l = s * kap
    ep = e.copy()
    lam_ok = 0.0
    for g in G2:
        mg = m[g[0]]
        if mg < kap:
            ep[g], lam = fill(e, w, g, kap, True)
            lam_ok = max(lam_ok, lam - kap)                 # claim: lam_g <= kappa
        elif mg > 1 - kap:
            ep[g], lam = fill(e, w, g, 1 - kap, False)
            lam_ok = max(lam_ok, (1 - kap) - lam)
    p = avg(mp, w, G1)
    T = lambda z: cost(z, w, G2)
    Pi1 = rate(e, w) - rate(y, w) + u * dist(y, e, w)
    Pi2 = rate(mp, w) - rate(m, w) + u * dist(m, mp, w)
    chi = lambda t: float(f(t)) + u * min(t, 1 - t) - L1
    cells = -np.inf
    for g in G2:
        Ag = float(np.dot(w[g], f(e[g]) - f(y[g]) + u * np.abs(y[g] - e[g])))
        mg, mpg = m[g[0]], mp[g[0]]
        Ag += float(np.sum(w[g])) * (float(f(mpg)) - float(f(mg)) + u * abs(mg - mpg))
        cells = max(cells, Ag - float(np.sum(w[g])) * h)
    out = dict(
        Phi0=Phi0, Phi1=Phi1,
        root=abs(Phi - theta),                                              # Phi(s) = theta
        mean=float(np.max(np.abs(avg(ep, w, G2) - mp))),                    # avg_2 e' = m'
        norm=abs(dist(e, ep, w) - dist(m, mp, w)),                          # ||e - e'|| = ||m - m'||
        lam=lam_ok,                                                         # lambda_g <= kappa (>= 1-kappa)
        Tfill=T(ep) - T(e),                                                 # (C4):  T(e') <= T(e)
        split=abs(cost(ep, w, G1) - (T(ep) + cost(mp, w, G1))),             # cost_1(e') = T(e') + Q(m')
        vis=cost(ep, w, G1) - theta,                                        # cost_1(e') <= theta   -> (H2) applies
        core=max(float(np.max(kap - mp)), float(np.max(mp - (1 - kap))),    # m', p in K            -> (H1), nu_K apply
                 float(np.max(kap - p)), float(np.max(p - (1 - kap)))),
        ident=abs((rate(p, w) - rate(y, w) + u * dist(y, e, w) + u * dist(m, mp, w))
                  - (Pi1 + Pi2 - T(e) - cost(mp, w, G1))),                  # Step 3 bookkeeping
        tri=dist(y, ep, w) - dist(y, e, w) - dist(m, mp, w),                # triangle inequality used in Step 3
        cells=cells,                                                        # Step 4:  A_g <= phi_g h
        Pi=Pi1 + Pi2 - h,                                                   # Step 5
        B=rate(p, w) - rate(y, w) + u * dist(y, ep, w) - (h - theta),       # the theorem without the profile
        BnoH1=rate(mp, w) - rate(y, w) + u * dist(y, ep, w) - (h - theta),  # what is left if the step F(m') = F(p) is not available
    )
    return out, dict(s=s, l=l, e=e, ep=ep, m=m, mp=mp, p=p)


# ------------------------------------------------------------------ instance generators
def random_partitions(rng, nC):
    lab2 = rng.integers(0, rng.integers(1, nC + 1), size=nC)
    cells2 = [[int(i) for i in np.flatnonzero(lab2 == v)] for v in np.unique(lab2)]
    k = len(cells2)
    lab1 = rng.integers(0, rng.integers(1, k + 1), size=k)
    cells1 = [sum((cells2[i] for i in np.flatnonzero(lab1 == v)), []) for v in np.unique(lab1)]
    return cells1, cells2


def random_weights(rng, nC):
    w = rng.dirichlet(np.full(nC, float(rng.choice([0.3, 1.0, 5.0]))))
    w = np.maximum(w, 1e-6)
    if rng.random() < 0.5:                                   # a class of weight far below 5%
        w[rng.integers(nC)] = 10.0 ** (-rng.uniform(1.4, 5.0)) * w.sum()
    return w / w.sum()


def random_y(rng, nC, u, G2, fam):
    pu, L1, kap, h, a = consts(u)
    special = np.array([0.0, 1.0, pu, 1 - pu, kap, 1 - kap, 0.5, 1e-9, 1 - 1e-9])
    if fam == 0:                                             # uniform
        return rng.random(nC)
    if fam == 1:                                             # boundary and special values
        return rng.choice(special, size=nC)
    if fam == 2:                                             # every cell has classes on both sides of 1/2
        y = np.empty(nC)
        for g in G2:
            for j, c in enumerate(rng.permutation(g)):
                y[c] = rng.uniform(0, 0.3) if j % 2 == 0 else rng.uniform(0.7, 1.0)
        return y
    if fam == 3:                                             # deep cells: all classes low (or all high), unequal
        y = np.empty(nC)
        for g in G2:
            lowside = rng.random() < 0.5
            v = rng.uniform(0, kap, size=len(g)) * rng.choice([1.0, 0.3, 0.05])
            y[g] = v if lowside else 1 - v
        return y
    if fam == 4:                                             # cone points: one class at p_u (or 0), the rest typical
        y = 0.5 + 0.05 * rng.standard_normal(nC)
        k = rng.integers(1, nC + 1)
        idx = rng.choice(nC, size=k, replace=False)
        y[idx] = rng.choice([pu, 1 - pu, 0.0, 1.0, pu / 2], size=k)
        return np.clip(y, 0, 1)
    # fam 5: near the clip levels
    return np.clip(rng.choice([kap, 1 - kap, pu, 1 - pu], size=nC) + 0.02 * rng.standard_normal(nC), 0, 1)


KEYS = ('root', 'mean', 'norm', 'lam', 'Tfill', 'split', 'vis', 'core', 'ident', 'tri', 'cells', 'Pi', 'B')


def structured(rng, kind):
    """the structures named in the review brief"""
    if kind == 'three-in-one-cell':
        return 3, [[0, 1, 2]], [[0, 1, 2]]
    if kind == 'split-into-three':
        nC = int(rng.integers(4, 8))
        cut = sorted(rng.choice(np.arange(1, nC), size=2, replace=False))
        return nC, [list(range(nC))], [list(range(0, cut[0])), list(range(cut[0], cut[1])), list(range(cut[1], nC))]
    nC = int(rng.integers(2, 9))
    G1, G2 = random_partitions(rng, nC)
    return nC, G1, G2


def worker_A(seed):
    rng = np.random.default_rng(seed)
    worst = {k: (-np.inf, None) for k in KEYS}
    worst['BnoH1'] = (-np.inf, None)
    count = {}
    tried = 0
    done = 0
    t0 = time.time()
    while done < 1500 and time.time() - t0 < 200:
        tried += 1
        u = float(rng.choice([0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 6.0, 10.0]))
        pu, L1, kap, h, a = consts(u)
        kind = str(rng.choice(['random', 'random', 'three-in-one-cell', 'split-into-three']))
        nC, G1, G2 = structured(rng, kind)
        w = random_weights(rng, nC)
        fam = int(rng.integers(0, 6))
        y = random_y(rng, nC, u, G2, fam)
        Ty = cost(y, w, G2)
        if Ty <= h * (1 + 1e-6):
            continue
        cand = [t for t in (h, 1.001 * h, 1.05 * h, 1.3 * h, 2 * h, 3 * h, Ty * (1 - 1e-3), 0.5 * (h + Ty)) if h <= t < Ty * (1 - 1e-9)]
        theta = float(rng.choice(cand))
        out, _ = chain(y, w, G1, G2, u, theta)
        done += 1
        tag = "%s/fam%d" % (kind, fam)
        count[tag] = count.get(tag, 0) + 1
        info = "u=%g theta=%.4fh %d classes |G1|=%d |G2|=%d min w=%.1e fam%d %s" % (u, theta / h, nC, len(G1), len(G2), w.min(), fam, kind)
        for k in list(worst):
            v = out[k] / h                                   # everything in units of h
            if v > worst[k][0]:
                worst[k] = (v, info)
    return worst, count, tried, done


def part_A():
    print("PART A: the chain of Steps 1-5, own implementation; all quantities in units of h; each must be <= 0 (or = 0) up to rounding")
    with Pool(4) as pool:
        res = pool.map(worker_A, [1000 + i for i in range(8)])
    worst = {}
    count = {}
    tried = done = 0
    for wst, cnt, tr, dn in res:
        tried += tr
        done += dn
        for k, v in wst.items():
            if k not in worst or v[0] > worst[k][0]:
                worst[k] = v
        for k, v in cnt.items():
            count[k] = count.get(k, 0) + v
    print("  %d hidden instances (%d draws).  by structure/family: %s" % (done, tried, ", ".join("%s:%d" % kv for kv in sorted(count.items()))))
    names = dict(root="|Phi(s) - theta|  (existence of s)", mean="|avg_2 e' - m'|", norm="| ||e-e'|| - ||m-m'|| |",
                 lam="lambda_g beyond kappa", Tfill="T(e') - T(e)                 [(C4)]", split="|cost_1(e') - T(e') - Q(m')|  [(C1)]",
                 vis="cost_1(e') - theta           [(H2) applicable]", core="m', p outside K              [(H1), nu_K applicable]",
                 ident="Step 3 bookkeeping identity", tri="||y-e'|| - ||y-e|| - ||m-m'||", cells="max_g A_g - phi_g h         [Step 4]",
                 Pi="Pi_1 + Pi_2 - h              [Step 5]", B="B = r(p)-r(y)+u||y-e'||-(h-theta)  [conclusion]",
                 BnoH1="(for information) same without the step F(m')=F(p)")
    ok = True
    for k in KEYS + ('BnoH1',):
        v, info = worst[k]
        if k != 'BnoH1':
            ok &= v <= 1e-7
        print("   %-52s max %+.3e   at %s" % (names[k], v, info))
    print("  all claims hold: %s" % ok)
    return ok


def part_C():
    print("PART C: facts (C1)-(C4)")
    rng = np.random.default_rng(7)
    w1 = w2 = w4 = -np.inf
    c1eq = 0.0
    special = np.array([0.0, 1.0, 0.5, 1e-12, 1 - 1e-12])
    for it in range(8000):
        nC = int(rng.integers(2, 9))
        G1, G2 = random_partitions(rng, nC)
        w = random_weights(rng, nC)
        z = rng.random(nC)
        zz = rng.random(nC)
        mask = rng.random(nC) < 0.3
        z[mask] = rng.choice(special, size=int(mask.sum()))
        c1eq = max(c1eq, abs(cost(z, w, G1) - cost(avg(z, w, G2), w, G1) - cost(z, w, G2)))
        w1 = max(w1, cost(z, w, G2) - cost(z, w, G1), rate(avg(z, w, G1), w) - rate(z, w), -cost(z, w, G2))
        w2 = max(w2, dist(avg(z, w, G1), avg(zz, w, G1), w) - dist(z, zz, w))
        # (C4): T_g(max(z, lam)) nonincreasing in lam; T_g(min(z, lam)) nondecreasing in lam
        g = list(range(nC))
        lams = np.sort(np.concatenate([np.linspace(0, 1, 41), z]))
        Tup = np.array([cost(np.maximum(z, lam), w, [g]) for lam in lams])
        Tdn = np.array([cost(np.minimum(z, lam), w, [g]) for lam in lams])
        w4 = max(w4, float(np.max(np.diff(Tup))), float(np.max(-np.diff(Tdn))))
    print("   (C1) |cost_1(z) - cost_1(avg_2 z) - cost_2(z)|        max %.2e" % c1eq)
    print("   (C1) cost_2 - cost_1, r(avg z) - r(z), -cost           max %+.2e" % w1)
    print("   (C2) ||avg z - avg z'|| - ||z - z'||                   max %+.2e" % w2)
    print("   (C4) increase of T_g(max(z,lam)) in lam / of T_g(min(z,lam)) as lam decreases   max %+.2e" % w4)
    w3 = 0.0
    for u in (0.01, 0.1, 0.25, 0.5, 1, 2, 4, 6, 10, 20, 40):
        pu, L1, kap, h, a = consts(u)
        t = np.linspace(0, 1, 200001)
        chi = f(t) + u * np.minimum(t, 1 - t) - L1
        left = t <= pu
        mid = (t >= pu) & (t <= 0.5)
        v = [-(chi.min()), abs(float(f(pu)) + u * pu - L1), abs(float(f(kap)) + u * kap - L1 - h),
             float(np.max(np.diff(chi[left]))) if left.sum() > 1 else 0.0, float(np.max(-np.diff(chi[mid]))),
             float(np.max(np.abs(chi - chi[::-1]))), pu - kap, kap - 0.5]
        # the identity for t' between t and 1/2
        tt = rng.random(2000)
        tp = tt + rng.random(2000) * (0.5 - tt)
        chi_ = lambda x: f(x) + u * np.minimum(x, 1 - x) - L1
        v.append(float(np.max(np.abs(f(tp) - f(tt) + u * np.abs(tp - tt) - (chi_(tp) - chi_(tt))))))
        w3 = max(w3, max(v))
    print("   (C3) chi >= 0, chi(p_u) = 0, chi(kappa) = h, monotonicity, symmetry, p_u < kappa < 1/2, step identity; worst defect %+.2e (11 slopes 0.01..40)" % w3)
    ok = c1eq < 1e-12 and w1 < 1e-12 and w2 < 1e-12 and w4 < 1e-12 and w3 < 1e-9
    print("   all facts hold: %s" % ok)
    return ok


# ------------------------------------------------------------------ direct maximisation of B over y
STRUCT_O = [
    ("two classes, one cell (tight case of Remark 4)", np.array([0.5, 0.5]), [[0, 1]], [[0, 1]]),
    ("two classes 1:9, one cell", np.array([0.1, 0.9]), [[0, 1]], [[0, 1]]),
    ("three classes (3%,47%,50%) in one cell", np.array([0.03, 0.47, 0.5]), [[0, 1, 2]], [[0, 1, 2]]),
    ("four classes, cell split into {0},{1},{2,3}", np.array([0.2, 0.3, 0.1, 0.4]), [[0, 1, 2, 3]], [[0], [1], [2, 3]]),
    ("four classes, one cell -> pairs", np.array([0.25, 0.25, 0.25, 0.25]), [[0, 1, 2, 3]], [[0, 1], [2, 3]]),
    ("nested {0,1},{2,3} -> {0,1},{2},{3}", np.array([0.3, 0.2, 0.25, 0.25]), [[0, 1], [2, 3]], [[0, 1], [2], [3]]),
    ("five classes -> {0,1},{2,3},{4}", np.array([0.2, 0.2, 0.25, 0.15, 0.2]), [[0, 1, 2, 3, 4]], [[0, 1], [2, 3], [4]]),
    ("three hidden classes after split {0,1,2},{3}", np.array([0.02, 0.38, 0.3, 0.3]), [[0, 1, 2, 3]], [[0, 1, 2], [3]]),
]


def worker_O(args):
    from scipy.optimize import minimize
    name, w, G1, G2, u, thr, seed = args
    pu, L1, kap, h, a = consts(u)
    theta = thr * h
    rng = np.random.default_rng(seed)

    def obj(x):
        y = np.clip(x, 0.0, 1.0)
        if cost(y, w, G2) <= theta * (1 + 1e-9):
            return 1.0 + (theta - cost(y, w, G2))            # not hidden: push outwards
        return -chain(y, w, G1, G2, u, theta)[0]['B'] / h
    best = (-np.inf, None)
    for start in range(5):
        x0 = rng.random(len(w))
        if start % 3 == 1:
            x0 = rng.choice([pu, 1 - pu, 0.0, 1.0, kap, 1 - kap], size=len(w)) + 0.01 * rng.standard_normal(len(w))
        r = minimize(obj, x0, method='Nelder-Mead', options=dict(maxiter=200 * len(w), xatol=1e-10, fatol=1e-13))
        if r.fun < 1.0 and -r.fun > best[0]:
            best = (-r.fun, np.clip(r.x, 0, 1))
    return name, u, thr, best


def part_O():
    print("PART O: sup over hidden y of B(y)/h by Nelder-Mead (5 starts per case); the proof says sup <= 0")
    cases = []
    for i, (name, w, G1, G2) in enumerate(STRUCT_O):
        for u in (1.0, 4.0):
            for thr in (1.0, 1.2):
                cases.append((name, w, G1, G2, u, thr, 50 + i))
    with Pool(4) as pool:
        res = pool.map(worker_O, cases, chunksize=1)
    top = -np.inf
    for name, u, thr, (val, y) in res:
        top = max(top, val)
        print("   %-48s u=%g theta=%.1fh : sup B/h = %+.6f at y = %s" % (name, u, thr, val, None if y is None else np.round(y, 4)))
    print("   largest value found: %+.3e h   (0 is attained in the two-class case at theta = h, y = (p_u, 1-p_u))" % top)
    return top <= 1e-7


def part_L():
    print("PART L: theta < h.  If Phi(1) <= theta the chain applies verbatim; otherwise s = 1, e = clip_kappa(y) in K and (H1) alone give")
    print("        -F(y) - r(y) <= nu_K + [r(avg_1 e) - r(y) + u||y - e||] <= nu_K + h - cost_1(e) < nu_K + h - theta.")
    rng = np.random.default_rng(11)
    worst = -np.inf
    n1 = n2 = 0
    while n1 + n2 < 4000:
        u = float(rng.choice([0.25, 1.0, 2.0, 4.0, 6.0]))
        pu, L1, kap, h, a = consts(u)
        nC = int(rng.integers(2, 7))
        G1, G2 = random_partitions(rng, nC)
        w = random_weights(rng, nC)
        y = random_y(rng, nC, u, G2, int(rng.integers(0, 6)))
        theta = h * rng.uniform(0.05, 1.0)
        if cost(y, w, G2) <= theta * (1 + 1e-9):
            continue
        e = clip(y, kap)
        if cost(e, w, G1) > theta:
            n1 += 1
            worst = max(worst, (rate(avg(e, w, G1), w) - rate(y, w) + u * dist(y, e, w) - (h - theta)) / h)
        else:
            n2 += 1
            worst = max(worst, chain(y, w, G1, G2, u, theta)[0]['B'] / h)
    print("   %d instances with theta in (0.05h, h): %d by (H1) alone, %d by the chain; max of [bound - (h - theta)]/h = %+.3e" % (n1 + n2, n1, n2, worst))
    return worst <= 1e-7


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "CAOL"
    ok = True
    if "C" in which:
        ok &= part_C()
    if "A" in which:
        ok &= part_A()
    if "O" in which:
        ok &= part_O()
    if "L" in which:
        ok &= part_L()
    print("OVERALL: %s" % ("no violation found" if ok else "VIOLATION FOUND"))
