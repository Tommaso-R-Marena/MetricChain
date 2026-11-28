#!/usr/bin/env python3
"""Algorithm R3(M) of HIERARCHY_REPORT.md section 4, implemented literally on real cubes {0,1}^n (n <= 16 here),
written from the report's text only.  Checks (a) candidates, (b) unbiasedness, (c) exactness when all blocks
are revealed, and the mutation "shell weights P_j(a_j) -> uniform 1/(n_j+1)".

Points are integers in [0, 2^n); block j is a contiguous range of bit positions; psi is a table on all 2^n points.
"""
import argparse
import itertools
import math
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


class Instance:
    def __init__(self, ns, F, centres, u):
        self.ns = ns
        self.m = len(ns)
        self.n = sum(ns)
        self.u = u
        self.F = F
        off = np.cumsum([0] + list(ns))
        self.bits = [np.array([1 << i for i in range(off[j], off[j + 1])], dtype=np.int64) for j in range(self.m)]
        self.bmask = [int(b.sum()) for b in self.bits]
        self.s = centres
        x = np.arange(1 << self.n, dtype=np.int64)
        d = []
        for j in range(self.m):
            y = (x ^ self.s[j]) & self.bmask[j]
            d.append(popcount(y))
        self.types = d
        self.psi = F[tuple(d)]
        self.pc = popcount(x)
        self.allx = x
        self.A = float(np.mean(np.exp(-self.psi)))
        # same value from the types (P(d) = prod C(n_j,d_j) 2^-n_j)
        Pj = [np.array([math.comb(k, a) for a in range(k + 1)], dtype=float) / 2 ** k for k in ns]
        Pd = Pj[0]
        for j in range(1, self.m):
            Pd = np.multiply.outer(Pd, Pj[j])
        self.A_types = float(np.sum(Pd * np.exp(-F)))
        self.Pj = Pj
        # subsets of each block grouped by size, for uniform sampling on spheres
        self.subsets = []
        for j in range(self.m):
            k = ns[j]
            allm = np.arange(1 << k, dtype=np.int64)
            pc = popcount(allm)
            order = np.argsort(pc, kind="stable")
            cnt = np.bincount(pc, minlength=k + 1)
            offs = np.r_[0, np.cumsum(cnt)[:-1]]
            # spread the local bits to the block's global positions
            glob = np.zeros(1 << k, dtype=np.int64)
            for i in range(k):
                glob |= ((allm >> i) & 1) * int(self.bits[j][i])
            self.subsets.append((glob[order], offs, cnt))


def popcount(a):
    a = a.copy()
    c = np.zeros_like(a)
    while np.any(a):
        c += a & 1
        a >>= 1
    return c


def admissible(F, u, tol=1e-12):
    return all(np.max(np.abs(np.diff(F, axis=ax))) <= u + tol for ax in range(F.ndim))


def random_profile(ns, u, rng, family):
    shape = tuple(k + 1 for k in ns)
    grids = np.meshgrid(*[np.arange(s) for s in shape], indexing="ij")
    K = 1 if family == "hidden" else rng.integers(1, 4)
    cones = []
    for _ in range(K):
        if family == "cones":
            v = [rng.integers(0, k + 1) for k in ns]
        else:  # dips at atypical types (near a corner of the type grid), flat elsewhere
            v = [int(rng.choice([0, 1, k - 1, k])) for k in ns]
        w = rng.uniform(0.3, 1.0, size=len(ns))
        b = rng.uniform(-3.0 * u, -0.5 * u) if family != "cones" else rng.uniform(-2.0 * u, 2.0 * u)
        if family == "hidden":  # one small dip at a corner of the type grid: rarely seen by small batches
            v = [int(rng.choice([0, k])) for k in ns]
            w = np.ones(len(ns))
            b = rng.uniform(-1.9 * u, -0.6 * u)
        cones.append(b + u * sum(w[j] * np.abs(grids[j] - v[j]) for j in range(len(ns))))
    Fc = np.minimum.reduce(cones)
    if family == "cones":
        F = Fc
    elif family in ("capped", "hidden"):  # flat at 0 except dips: the hidden-structure shape
        F = np.minimum(0.0, Fc)
    elif family == "parity":  # half-slope cones plus a 2-periodic term in one block (reveal-resistant)
        j = rng.integers(0, len(ns))
        F = 0.5 * np.minimum(0.0, Fc) + 0.5 * u * (grids[j] % 2)
    else:
        raise ValueError(family)
    assert admissible(F, u)
    return F


def make_points(inst, S, cand, shells, M, rng):
    """For each shell (tuple of radii over sorted S), M points; returns points and shell index per point."""
    K = len(shells)
    x = np.zeros(K * M, dtype=np.int64)
    sh = np.repeat(np.arange(K), M)
    Ssorted = sorted(S)
    for j in range(inst.m):
        if j in S:
            col = Ssorted.index(j)
            a = np.array([s[col] for s in shells], dtype=np.int64)[sh]
            glob, offs, cnt = inst.subsets[j]
            idx = offs[a] + (rng.random(K * M) * cnt[a]).astype(np.int64)
            x |= cand[j] ^ glob[idx]
        else:
            r = rng.integers(0, 1 << inst.ns[j], size=K * M)
            glob, _, _ = inst.subsets[j]
            # glob is ordered by popcount; use the unordered spread instead
            spread = np.zeros(K * M, dtype=np.int64)
            for i in range(inst.ns[j]):
                spread |= ((r >> i) & 1) * int(inst.bits[j][i])
            x |= spread
    return x, sh


def reveal(inst, X, blocks, cand, stats):
    """Neighbours in `blocks`; update cand (first revealing point) and check every candidate (check (a))."""
    newly = set()
    for j in blocks:
        vals = inst.psi[X[:, None] ^ inst.bits[j][None, :]]
        rev = np.any(vals != vals[:, :1], axis=1)
        if not rev.any():
            continue
        Xr, vr = X[rev], vals[rev]
        I = (vr == vr[:, :1])
        Imask = (I * inst.bits[j][None, :]).sum(axis=1)
        c = (Xr & inst.bmask[j]) ^ Imask
        sj = inst.s[j] & inst.bmask[j]
        good = (c == sj) | (c == (sj ^ inst.bmask[j]))
        stats["cand_checked"] += int(len(c))
        stats["cand_bad"] += int((~good).sum())
        # two values exactly?
        stats["two_values_bad"] += int(sum(len(np.unique(row)) != 2 for row in vr[:50]))
        newly.add(j)
        cand[j] = int(c[0])
    return newly


def R3(inst, M, rng, stats):
    m = inst.m
    cand = {}
    # round 1
    X1 = rng.integers(0, 1 << inst.n, size=M)
    S1 = reveal(inst, X1, range(m), cand, stats)
    # round 2
    S1s = sorted(S1)
    shells1 = list(itertools.product(*[range(inst.ns[j] + 1) for j in S1s]))
    X2, _ = make_points(inst, S1, cand, shells1, M, rng)
    S2 = S1 | reveal(inst, X2, [j for j in range(m) if j not in S1], cand, stats)
    # round 3
    S2s = sorted(S2)
    shells2 = list(itertools.product(*[range(inst.ns[j] + 1) for j in S2s]))
    X3, sh = make_points(inst, S2, cand, shells2, M, rng)
    e = np.exp(-inst.psi[X3])
    means = np.bincount(sh, weights=e, minlength=len(shells2)) / M
    Wb = np.array([np.prod([inst.Pj[j][a[c]] for c, j in enumerate(S2s)]) for a in shells2])
    Wu = np.array([np.prod([1.0 / (inst.ns[j] + 1) for j in S2s]) for a in shells2])
    # exact conditional expectation of the round-3 estimate given rounds 1-2 (all 2^n points grouped by shell)
    if S2s:
        key = np.zeros(1 << inst.n, dtype=np.int64)
        for j in S2s:
            key = key * (inst.ns[j] + 1) + inst.pc[(inst.allx ^ cand[j]) & inst.bmask[j]]
        tot = np.bincount(key, weights=np.exp(-inst.psi), minlength=len(shells2))
        cnt = np.bincount(key, minlength=len(shells2))
        exact_means = tot / cnt
    else:
        exact_means = np.array([inst.A])
    stats["cond_err_max"] = max(stats["cond_err_max"], abs(float(Wb @ exact_means) / inst.A - 1))
    if len(S2) > 0:
        stats["cond_mut_runs"] += 1
        if abs(float(Wu @ exact_means) / inst.A - 1) > 1e-9:
            stats["cond_mut_biased"] += 1
    return float(Wb @ means), float(Wu @ means), S1, S2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261128)
    ap.add_argument("--instances", type=int, default=32)
    ap.add_argument("--Ms", default="100:1000,1000:200,10000:20")
    ap.add_argument("--bigM", default="100000:4", help="M:reps, for the two-block instances of the family hidden")
    ap.add_argument("--out", default=str(HERE / "out" / "q2_r3.txt"))
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    Ms = [tuple(int(v) for v in s.split(":")) for s in args.Ms.split(",")]
    bigM = tuple(int(v) for v in args.bigM.split(":")) if args.bigM else None
    lines = []
    pr = lambda s: (print(s, flush=True), lines.append(s))
    configs = [((8, 8), 1.0), ((7, 7), 2.0), ((8, 8), 2.0), ((6, 6), 1.0), ((6, 5, 5), 1.0), ((5, 5, 5), 2.0),
               ((6, 6, 4), 0.5), ((6, 5, 5), 4.0)]
    families = ["hidden", "capped", "cones", "parity"]
    tests = []  # (instance, M, z, zmut, full_reveal_frac)
    stats = dict(cand_checked=0, cand_bad=0, two_values_bad=0, full_runs=0, full_bad=0, runs=0,
                 cond_err_max=0.0, cond_mut_runs=0, cond_mut_biased=0)
    t0 = time.time()
    for k in range(args.instances):
        ns, u = configs[k % len(configs)]
        fam = families[(k // len(configs)) % len(families)]
        F = random_profile(ns, u, rng, fam)
        centres = [int(rng.integers(0, 1 << sum(ns))) for _ in ns]
        inst = Instance(ns, F, centres, u)
        assert abs(inst.A - inst.A_types) <= 1e-12 * inst.A
        plan = list(Ms) + ([bigM] if (bigM and fam == "hidden" and len(ns) == 2) else [])
        for M, R in plan:
            est, estu, sizes1, sizes2 = [], [], [], []
            for _ in range(R):
                ab, au, S1, S2 = R3(inst, M, rng, stats)
                stats["runs"] += 1
                est.append(ab); estu.append(au); sizes1.append(len(S1)); sizes2.append(len(S2))
                if len(S2) == inst.m:
                    stats["full_runs"] += 1
                    if abs(ab - inst.A) > 1e-12 * inst.A:
                        stats["full_bad"] += 1
            est, estu = np.array(est), np.array(estu)
            se = est.std(ddof=1) / math.sqrt(R)
            seu = estu.std(ddof=1) / math.sqrt(R)
            dev = est.mean() - inst.A
            # an SE below float resolution means every run returned A up to rounding: compare deviations directly
            z = dev / se if se > 1e-12 * inst.A else (0.0 if abs(dev) <= 1e-12 * inst.A else math.inf)
            devu = estu.mean() - inst.A
            zu = devu / seu if seu > 1e-12 * inst.A else (0.0 if abs(devu) <= 1e-12 * inst.A else math.inf)
            full = float(np.mean(np.array(sizes2) == inst.m))
            tests.append((k, M, z, zu, full))
            pr(f"inst {k:2d} {fam:6s} ns={ns} u={u} M={M:6d} R={R:3d} A={inst.A:.6e} mean/A-1={dev / inst.A:+.2e} "
               f"z={z:+6.2f} | |S1| mean={np.mean(sizes1):.2f} |S2| mean={np.mean(sizes2):.2f} full={full:.2f} "
               f"| uniform-weights: mean/A-1={devu / inst.A:+.3e} z={zu:+8.2f}  [{time.time() - t0:.0f}s]")
    nz = len(tests)
    within = sum(abs(t[2]) <= 3 for t in tests)
    mut_caught = sum(abs(t[3]) > 3 for t in tests)
    pr(f"# SUMMARY instances={args.instances} tests(instance,M)={nz} runs={stats['runs']}")
    pr(f"# (a) candidates checked={stats['cand_checked']} not centre/antipode={stats['cand_bad']} "
       f"(rows with != 2 values among checked samples: {stats['two_values_bad']})")
    pr(f"# (b) |z|<=3 in {within}/{nz} = {within / nz:.1%} of tests; max |z| = {max(abs(t[2]) for t in tests):.2f}")
    pr(f"# (c) runs with all blocks revealed={stats['full_runs']}, of which A_hat != A (rel 1e-12): {stats['full_bad']}")
    pr(f"# mutation (uniform shell weights): |z|>3 in {mut_caught}/{nz} tests; "
       f"tests where all runs fully revealed: {sum(t[4] == 1.0 for t in tests)} (there the error is deterministic)")
    pr(f"# (b, exact) max over all runs of |E[A_hat | rounds 1,2]/A - 1| (exact, all 2^n points): {stats['cond_err_max']:.2e}")
    pr(f"# mutation, exact conditional mean: biased (|rel err|>1e-9) in {stats['cond_mut_biased']}/{stats['cond_mut_runs']} runs with S2 non-empty")
    pr(f"# time {time.time() - t0:.0f}s")
    Path(args.out).write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
