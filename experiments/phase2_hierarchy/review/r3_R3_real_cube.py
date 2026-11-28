"""Review item 2: Algorithm R3 of section 4 implemented LITERALLY on real cubes (n <= 20).

The energy is a table on all 2^n points, psi(x) = F(type of x) for a hidden centre s, a KNOWN partition of
the coordinates into blocks (random, not consecutive) and an admissible profile F.  The algorithm only looks
up psi at points of its choice (every lookup is counted).

Tests
 T0  exhaustive, every point x of the cube and every block j: if the neighbour values in block j are not all
     equal they take exactly two values and c^j := x^{B_j} xor 1_I is s^j or its antipode.
 T1  the same for every candidate that occurs in the runs of R3 (rounds 1 and 2).
 T2  unbiasedness: (a) exact - for the (S_2, candidates) of each run, and for ARBITRARY wrong candidates,
     sum_a prod_j P_j(a_j) * (average of e^{-psi} over the product of spheres) = A by enumeration;
     (b) statistical - the mean of A_hat over many runs against A (z-score), M = 1, 2, 5.
 T3  A_hat = A (to rounding) whenever S_2 is the set of all blocks.
 T4  the path argument: with Theta_1 := the largest budget for which E_1 holds for the realised round-1 sample
     (every type of cost <= Theta_1 was sampled), F sees only S_1 on V_0(Theta_1) (parity version), checked by
     brute force over all pairs; the same for round 2 (E_2, V_{S_1}(Theta_2), S_2).  Also recorded: how often
     the statement WITHOUT the parity qualifier fails (it should fail for 2-periodic profiles).
 T5  number of evaluations <= 3 (n+1)^(m+1) M.

usage: python3 r3_R3_real_cube.py [seed]
"""
import itertools
import math
import sys
import time
import numpy as np
from rv_common import tcost


def popcount(a):
    a = a.astype(np.uint32)
    a = a - ((a >> 1) & 0x55555555)
    a = (a & 0x33333333) + ((a >> 2) & 0x33333333)
    a = (a + (a >> 4)) & 0x0F0F0F0F
    return ((a * 0x01010101) & 0xFFFFFFFF) >> 24


class Instance:
    def __init__(self, ns, F, rng):
        self.ns = list(ns)
        self.m = len(ns)
        self.n = sum(ns)
        perm = rng.permutation(self.n)
        self.blocks = []
        pos = 0
        for nj in ns:
            self.blocks.append(np.sort(perm[pos:pos + nj]).astype(np.int64))   # least index first
            pos += nj
        self.bits = [np.left_shift(np.int64(1), B) for B in self.blocks]
        self.masks = [int(b.sum()) for b in self.bits]
        self.s = int(rng.integers(0, 2 ** self.n))
        self.F = F
        x = np.arange(2 ** self.n, dtype=np.int64)
        self.types = [popcount((x ^ self.s) & mk).astype(np.int64) for mk in self.masks]
        self.psi = F[tuple(self.types)]
        self.A = float(np.mean(np.exp(-self.psi)))
        self.evals = 0
        self.lnP = [np.array([math.log(math.comb(nj, d)) - nj * math.log(2.0) for d in range(nj + 1)]) for nj in ns]

    # the oracle
    def query(self, x):
        self.evals += int(np.size(x))
        return self.psi[x]


def reveal(inst, xs, j):
    """literal reveal step for block j at the points xs; returns (revealed mask, candidates, n_distinct_values)."""
    nb = xs[:, None] ^ inst.bits[j][None, :]
    vals = inst.query(nb)
    first = vals[:, :1]                       # value attained at the least index of B_j
    same = vals == first
    revealed = ~same.all(axis=1)
    onesI = (same * inst.bits[j][None, :]).sum(axis=1)
    cand = (xs & inst.masks[j]) ^ onesI
    srt = np.sort(vals, axis=1)
    ndist = 1 + (np.diff(srt, axis=1) != 0).sum(axis=1)
    return revealed, cand, ndist


def sample_shell(inst, S, cands, a, M, rng):
    """M points: block j in S uniform on the sphere of radius a_j around c^j, the other blocks uniform."""
    xs = np.zeros(M, dtype=np.int64)
    for j in range(inst.m):
        nj = inst.ns[j]
        if j in S:
            r = a[S.index(j)]
            if r == 0:
                flip = np.zeros(M, dtype=np.int64)
            else:
                order = np.argsort(rng.random((M, nj)), axis=1)[:, :r]
                flip = inst.bits[j][order].sum(axis=1)
            xs |= (cands[j] ^ flip)
        else:
            b = rng.integers(0, 2, size=(M, nj))
            xs |= (b * inst.bits[j][None, :]).sum(axis=1)
    return xs


def R3(inst, M, rng, log):
    n, m = inst.n, inst.m
    inst.evals = 0
    # ---- round 1
    X1 = rng.integers(0, 2 ** n, size=M).astype(np.int64)
    inst.query(X1)
    cands = {}
    for j in range(m):
        rev, cand, nd = reveal(inst, X1, j)
        log['T1_total'] += int(rev.sum())
        log['T1_two_values_fail'] += int((nd[rev] != 2).sum())
        sj = inst.s & inst.masks[j]
        log['T1_cand_fail'] += int(((cand[rev] != sj) & (cand[rev] != (sj ^ inst.masks[j]))).sum())
        if rev.any():
            cands[j] = int(cand[np.argmax(rev)])
    S1 = sorted(cands)
    # ---- round 2
    X2 = []
    cands2 = dict(cands)
    rest = [j for j in range(m) if j not in S1]
    for a in itertools.product(*[range(inst.ns[j] + 1) for j in S1]):
        xs = sample_shell(inst, S1, cands, a, M, rng)
        inst.query(xs)
        X2.append((a, xs))
        for j in rest:
            rev, cand, nd = reveal(inst, xs, j)
            log['T1_total'] += int(rev.sum())
            log['T1_two_values_fail'] += int((nd[rev] != 2).sum())
            sj = inst.s & inst.masks[j]
            log['T1_cand_fail'] += int(((cand[rev] != sj) & (cand[rev] != (sj ^ inst.masks[j]))).sum())
            if rev.any() and j not in cands2:
                cands2[j] = int(cand[np.argmax(rev)])
    S2 = sorted(cands2)
    # ---- round 3
    est = 0.0
    for a in itertools.product(*[range(inst.ns[j] + 1) for j in S2]):
        xs = sample_shell(inst, S2, cands2, a, M, rng)
        w = math.exp(sum(inst.lnP[j][a[i]] for i, j in enumerate(S2)))
        est += w * float(np.mean(np.exp(-inst.query(xs))))
    return est, S1, S2, cands2, X1, X2, inst.evals


def exact_conditional_mean(inst, S, cands):
    """sum_a prod_{j in S} P_j(a_j) * average of e^{-psi} over {x : d(x^j, c^j) = a_j, j in S}, by enumeration."""
    x = np.arange(2 ** inst.n, dtype=np.int64)
    if not S:
        return float(np.mean(np.exp(-inst.psi)))
    key = np.zeros(2 ** inst.n, dtype=np.int64)
    lnw = np.zeros(2 ** inst.n)
    for j in S:
        dj = popcount((x ^ cands[j]) & inst.masks[j]).astype(np.int64)
        key = key * (inst.ns[j] + 1) + dj
        lnw += inst.lnP[j][dj]
    val = np.exp(-inst.psi)
    sums = np.bincount(key, weights=val)
    cnts = np.bincount(key)
    wts = np.bincount(key, weights=np.exp(lnw))        # = count * prod P_j(a_j)
    ok = cnts > 0
    return float(np.sum(wts[ok] / cnts[ok] * sums[ok] / cnts[ok]))


def sees_only(F, S, region, parity):
    """does F see only the blocks S on the boolean region (brute force over classes)?"""
    m = F.ndim
    grids = np.meshgrid(*[np.arange(k) for k in F.shape], indexing='ij', sparse=True)
    key = np.zeros(F.shape, dtype=np.int64)
    for j in range(m):
        if j in S:
            key = key * F.shape[j] + grids[j]
        else:
            key = key * 2 + ((grids[j] % 2) if parity else 0)
    k = key[region]
    v = F[region]
    if k.size == 0:
        return True
    order = np.argsort(k, kind='stable')
    k = k[order]
    v = v[order]
    lo = np.minimum.reduceat(v, np.r_[0, np.nonzero(np.diff(k))[0] + 1])
    hi = np.maximum.reduceat(v, np.r_[0, np.nonzero(np.diff(k))[0] + 1])
    return bool(np.all(hi == lo))


def reflectF(F, flips):
    G = F
    for j in flips:
        G = np.flip(G, axis=j)
    return G


def path_argument_test(inst, S1, S2, cands2, X1, X2, log):
    m = inst.m
    ts = [tcost(nj) for nj in inst.ns]
    grids = np.meshgrid(*[np.arange(nj + 1) for nj in inst.ns], indexing='ij', sparse=True)
    shape = tuple(nj + 1 for nj in inst.ns)
    # types relative to the candidates on revealed blocks (reflect F where the candidate is the antipode)
    flips = [j for j in S2 if cands2[j] != (inst.s & inst.masks[j])]
    Fc = reflectF(inst.F, flips)

    def types_of(xs):
        out = []
        for j in range(m):
            cj = cands2[j] if j in S2 else (inst.s & inst.masks[j])
            out.append(popcount((xs ^ cj) & inst.masks[j]).astype(np.int64))
        return tuple(out)

    tall = np.zeros(shape) + sum(ts[j][grids[j]] for j in range(m))
    # round 1: E_1 holds for every Theta < Theta_1 := min cost of a type that was not sampled
    hit = np.zeros(shape, dtype=bool)
    hit[types_of(X1)] = True
    Theta1 = float(tall[~hit].min()) if (~hit).any() else float('inf')
    V0 = tall < Theta1
    ok_par = sees_only(Fc, S1, V0, True)
    ok_nopar = sees_only(Fc, S1, V0, False)
    log['T4_r1_cases'] += 1
    log['T4_r1_fail'] += (not ok_par)
    log['T4_r1_fail_without_parity'] += (not ok_nopar)
    log['T4_r1_V0_sizes'].append(int(V0.sum()))
    log['T4_r1_nonvacuous'] += int(len(S1) < m and V0.sum() >= 20)
    # round 2: E_2 holds for every Theta < Theta_2
    rest1 = [j for j in range(m) if j not in S1]
    tS1c = np.zeros(shape) + (sum(ts[j][grids[j]] for j in rest1) if rest1 else 0.0)
    hit2 = np.zeros(shape, dtype=bool)
    for a, xs in X2:
        ty = types_of(xs)
        for i, j in enumerate(S1):
            assert np.all(ty[j] == a[i])       # the shell really is the sphere around the candidate
        hit2[ty] = True
    Theta2 = float(tS1c[~hit2].min()) if (~hit2).any() else float('inf')
    VP = tS1c < Theta2
    ok2 = sees_only(Fc, S2, VP, True)
    ok2n = sees_only(Fc, S2, VP, False)
    log['T4_r2_cases'] += 1
    log['T4_r2_fail'] += (not ok2)
    log['T4_r2_fail_without_parity'] += (not ok2n)
    log['T4_r2_VP_sizes'].append(int(VP.sum()))
    log['T4_r2_nonvacuous'] += int(len(S2) < m and VP.sum() >= 20)


# ---------------------------------------------------------------- profiles
def profiles(ns, u, rng):
    """a list of (name, admissible profile F on the type grid)."""
    shape = tuple(nj + 1 for nj in ns)
    m = len(ns)
    grids = np.meshgrid(*[np.arange(k) for k in shape], indexing='ij', sparse=True)
    out = []

    def l1(p):
        return sum(np.abs(grids[j] - p[j]) for j in range(m))

    # 1 random lower envelopes of cones (McShane type)
    for rep in range(2):
        F = np.full(shape, np.inf)
        for _ in range(4):
            p = [int(rng.integers(0, k)) for k in shape]
            F = np.minimum(F, rng.uniform(-2, 2) + u * rng.uniform(0.3, 1.0) * l1(p))
        out.append(('cones-min-%d' % rep, F))
    # 2 separable random walks
    F = np.zeros(shape)
    for j in range(m):
        g = np.concatenate([[0.0], np.cumsum(rng.uniform(-u, u, size=shape[j] - 1))])
        F = F + g[grids[j]]
    out.append(('separable-walk', F))
    # 3 two-periodic in every block (never revealed, yet depends on every block)
    F = np.zeros(shape)
    for j in range(m):
        F = F + rng.uniform(0.3, 1.0) * u * (grids[j] % 2) / m
    out.append(('2-periodic-all', F))
    # 4 two-periodic in the last block + cone in the first
    F = u * np.abs(grids[0] - shape[0] // 3) + 0.9 * u * (grids[m - 1] % 2)
    out.append(('cone(1)+2-periodic(last)', F + np.zeros(shape)))
    # 5 constant except a dip at a rare type (revealed only at rare types)
    p = [1] * m
    F = -u * np.maximum(0, 3 - l1(p)) + np.zeros(shape)
    out.append(('flat+dip-at-rare-type', F))
    # 6 radial dip around the centre (constant on a large region)
    F = -u * np.maximum(0, 4 - sum(grids[j] for j in range(m))) + np.zeros(shape)
    out.append(('radial-dip', F))
    # 7 first block visible everywhere, second only deep inside the first (rare)
    F = 0.7 * u * np.abs(grids[0] - shape[0] // 2) + u * np.minimum(grids[m - 1], 2) * (grids[0] <= 1) + np.zeros(shape)
    # make it admissible by taking the largest u-Lipschitz minorant (a few sweeps of the l1 inf-convolution)
    for _ in range(sum(shape)):
        G = F.copy()
        for j in range(m):
            sl = [slice(None)] * m
            sl2 = [slice(None)] * m
            sl[j] = slice(1, None); sl2[j] = slice(0, -1)
            G[tuple(sl)] = np.minimum(G[tuple(sl)], F[tuple(sl2)] + u)
            G[tuple(sl2)] = np.minimum(G[tuple(sl2)], F[tuple(sl)] + u)
        if np.array_equal(G, F):
            break
        F = G
    out.append(('block2-only-deep-in-block1', F))
    # 8 symmetric profile (centre / antipode ambiguous)
    F = 0.8 * u * sum(np.abs(grids[j] - (shape[j] - 1) / 2.0) for j in range(m)) + np.zeros(shape)
    out.append(('symmetric-cones', F))
    # 9 parity of the sum (2-periodic, couples the blocks) plus a rare dip
    F = 0.5 * u * (sum(grids[j] for j in range(m)) % 2) - 0.5 * u * np.maximum(0, 2 - l1([k - 1 for k in shape])) + np.zeros(shape)
    out.append(('parity-of-sum+rare-dip', F))
    # 10 constant
    out.append(('constant', np.zeros(shape)))
    for name, F in out:
        for j in range(m):
            assert np.abs(np.diff(F, axis=j)).max() <= u + 1e-9, name
    return out


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20261128
    rng = np.random.default_rng(seed)
    t_start = time.time()
    # (block sizes, slope, runs per M for the structural tests, list of M)
    configs = [((10, 10), 4.0), ((8, 12), 1.0), ((7, 7, 6), 2.0), ((9, 5), 0.5), ((6, 6, 6), 1.0), ((11, 9), 2.0)]
    small_configs = [((4, 4), 1.0), ((3, 3, 2), 1.0), ((5, 4), 2.0)]
    log = dict(T1_total=0, T1_two_values_fail=0, T1_cand_fail=0, T4_r1_cases=0, T4_r1_fail=0,
               T4_r1_fail_without_parity=0, T4_r2_cases=0, T4_r2_fail=0, T4_r2_fail_without_parity=0,
               T4_r1_V0_sizes=[], T4_r2_VP_sizes=[], T4_r1_nonvacuous=0, T4_r2_nonvacuous=0)
    T0_points = 0
    T0_fail = 0
    T2a_max = 0.0
    T2a_cases = 0
    T3_cases = 0
    T3_max = 0.0
    T5_fail = 0
    runs_total = 0
    S2_hist = {}

    def one_run(inst, M, do_exact, do_path):
        nonlocal runs_total, T5_fail, T3_cases, T3_max, T2a_max, T2a_cases
        est, S1, S2, cands2, X1, X2, ev = R3(inst, M, rng, log)
        runs_total += 1
        key = (len(S1), len(S2), inst.m)
        S2_hist[key] = S2_hist.get(key, 0) + 1
        if ev > 3 * (inst.n + 1) ** (inst.m + 1) * M:
            T5_fail += 1
        if len(S2) == inst.m:
            T3_cases += 1
            T3_max = max(T3_max, abs(est / inst.A - 1.0))
        if do_exact:
            T2a_max = max(T2a_max, abs(exact_conditional_mean(inst, S2, cands2) / inst.A - 1.0))
            T2a_cases += 1
        if do_path:
            path_argument_test(inst, S1, S2, cands2, X1, X2, log)
        return est

    # ---------------- structural tests on cubes with n = 14 .. 20
    for ns, u in configs:
        for name, F in profiles(ns, u, rng):
            inst = Instance(ns, F, rng)
            n, m = inst.n, inst.m
            x = np.arange(2 ** n, dtype=np.int64)
            for j in range(m):                                  # T0, exhaustive
                nb = x[:, None] ^ inst.bits[j][None, :]
                vals = inst.psi[nb]
                same = vals == vals[:, :1]
                rev = ~same.all(axis=1)
                srt = np.sort(vals[rev], axis=1)
                nd = 1 + (np.diff(srt, axis=1) != 0).sum(axis=1)
                cand = (x[rev] & inst.masks[j]) ^ (same[rev] * inst.bits[j][None, :]).sum(axis=1)
                sj = inst.s & inst.masks[j]
                bad = (nd != 2) | ((cand != sj) & (cand != (sj ^ inst.masks[j])))
                T0_points += int(rev.sum())
                T0_fail += int(bad.sum())
            for _ in range(3):                                  # T2a with arbitrary (wrong) candidates
                S = sorted(rng.choice(m, size=int(rng.integers(0, m + 1)), replace=False).tolist())
                c = {j: int(rng.integers(0, 2 ** n)) & inst.masks[j] for j in S}
                T2a_max = max(T2a_max, abs(exact_conditional_mean(inst, S, c) / inst.A - 1.0))
                T2a_cases += 1
            for M, R in ((1, 30), (5, 30), (300, 6), (3000, 4), (30000, 1)):
                for r in range(R):
                    one_run(inst, M, do_exact=(r < 3), do_path=True)
        print('config %s u=%g done (%.0f s)' % (ns, u, time.time() - t_start), flush=True)

    # ---------------- statistical unbiasedness on small cubes (every point is sampled often: no rare-event artefact)
    zrows = []
    for ns, u in small_configs:
        for name, F in profiles(ns, u, rng):
            inst = Instance(ns, F, rng)
            for M in (1, 2, 5):
                ests = np.array([one_run(inst, M, do_exact=False, do_path=False) for _ in range(500)])
                sd = ests.std(ddof=1)
                z = (ests.mean() - inst.A) / (sd / math.sqrt(len(ests))) if sd > 1e-12 * inst.A else float('nan')
                zrows.append((ns, u, name, M, inst.A, ests.mean(), z, sd / inst.A))
        print('small config %s u=%g done (%.0f s)' % (ns, u, time.time() - t_start), flush=True)

    print()
    print('T0 exhaustive reveal test: %d revealing (point, block) pairs, failures (not two values / candidate not centre or antipode): %d'
          % (T0_points, T0_fail))
    print('T1 candidates inside R3: %d revealing points, "exactly two values" failures %d, candidate failures %d'
          % (log['T1_total'], log['T1_two_values_fail'], log['T1_cand_fail']))
    print('T2a exact unbiasedness identity (realised and arbitrary candidates): %d cases, max |E/A - 1| = %.2e' % (T2a_cases, T2a_max))
    degenerate = [r for r in zrows if r[6] != r[6]]
    zr = [r for r in zrows if r[6] == r[6]]
    zs = np.array([r[6] for r in zr])
    print('T2b statistical unbiasedness on small cubes: %d (instance, M) cells with 500 runs each (%d further cells have A_hat = A in every run);'
          % (len(zs), len(degenerate)))
    print('     z-scores of the mean of A_hat against A: max |z| = %.2f, mean z = %+.3f, rms z = %.3f, cells with |z| > 3: %d'
          % (np.abs(zs).max(), zs.mean(), math.sqrt((zs ** 2).mean()), int((np.abs(zs) > 3).sum())))
    for r in sorted(zr, key=lambda r: -abs(r[6]))[:4]:
        print('     largest |z|: ns=%s u=%g %-28s M=%d A=%.6g mean=%.6g z=%+.2f (sd/A=%.3g)' % r)
    print('T3 runs with S_2 = all blocks: %d, max |A_hat/A - 1| = %.2e' % (T3_cases, T3_max))
    print('T4 path argument, round 1: %d samples (%d with an unrevealed block and |V_0| >= 20), "F sees only S_1 on V_0(Theta_1)" failed %d times (without the parity qualifier it would fail %d times); |V_0| between %d and %d types, median %d'
          % (log['T4_r1_cases'], log['T4_r1_nonvacuous'], log['T4_r1_fail'], log['T4_r1_fail_without_parity'], min(log['T4_r1_V0_sizes']), max(log['T4_r1_V0_sizes']), int(np.median(log['T4_r1_V0_sizes']))))
    print('T4 path argument, round 2: %d samples (%d with an unrevealed block and |V_{S_1}| >= 20), "F sees only S_2 on V_{S_1}(Theta_2)" failed %d times (without parity: %d); |V_{S_1}| between %d and %d types, median %d'
          % (log['T4_r2_cases'], log['T4_r2_nonvacuous'], log['T4_r2_fail'], log['T4_r2_fail_without_parity'], min(log['T4_r2_VP_sizes']), max(log['T4_r2_VP_sizes']), int(np.median(log['T4_r2_VP_sizes']))))
    print('T5 evaluation count above 3 (n+1)^(m+1) M: %d of %d runs' % (T5_fail, runs_total))
    print('(|S_1|, |S_2|, m) histogram over runs:', dict(sorted(S2_hist.items())))
    print('total time %.0f s, seed %d' % (time.time() - t_start, seed))


if __name__ == '__main__':
    main()
