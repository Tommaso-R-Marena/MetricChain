"""
Phase II (adaptive hierarchy) -- type-level simulation of the round-limited algorithms R1, R2, R3
on block-radial instances (blocks known, centres hidden).

For a block-radial energy psi(x) = F(d(x^1,s^1),...,d(x^m,s^m)) every quantity the algorithms use
depends on the sampled points only through their types, and a point of type d has neighbours of the
types d + e_j and d - e_j in block j (both, iff 0 < d_j < n_j).  The simulation is therefore exact at
the level of types: the number of sample points of a type is drawn as a Poisson variable with the right
mean (independent Poisson counts in place of a multinomial sample of size M: 'Poissonisation').

  R1  one round : M uniform points; plain Monte Carlo.
  R2  two rounds: round 1 as R3; round 2: every shell of the revealed blocks, M points each; estimate.
  R3  three rounds (Theorem H1): round 1: M uniform points with neighbours -> S1 (blocks revealed);
      round 2: every shell of S1, M points each, with neighbours in the other blocks -> S2;
      round 3: every shell of S2, M points each; estimate  sum_a P_{S2}(a) * mean(e^{-psi}).

Instances: (I1) the extremal three-block function of Lemma B designed against a budget Theta_c;
(I2) the two-round twins F_D of the archive's Theorem U3; (I3) a cone on two blocks; (I4) random admissible F.
Output: ln(estimate) - ln A for each algorithm (A exact, by summation over types).
"""
import sys, itertools
import numpy as np
from scipy.special import gammaln

LN2 = np.log(2.0)
def f(r):
    r = np.clip(r, 1e-300, 1 - 1e-16); return LN2 + r * np.log(r) + (1 - r) * np.log1p(-r)
def consts(u):
    pu = 1 / (1 + np.exp(u)); L1 = np.log(2 / (1 + np.exp(-u))); return pu, L1, f(pu), f(L1 / u)
def logbinom(n):
    k = np.arange(n + 1); return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1) - n * LN2
def logsumexp(a):
    a = np.asarray(a, float); m = a.max()
    return m + np.log(np.exp(a - m).sum()) if np.isfinite(m) else -np.inf
def lip_pass(U, u):
    for ax in range(U.ndim):
        U = np.moveaxis(U, ax, 0)
        for i in range(1, U.shape[0]): np.minimum(U[i], U[i - 1] + u, out=U[i])
        for i in range(U.shape[0] - 2, -1, -1): np.minimum(U[i], U[i + 1] + u, out=U[i])
        U = np.moveaxis(U, 0, ax)
    return U
def lip_minorant_1d(t, u):
    g = np.array(t, float)
    for i in range(1, len(g)): g[i] = min(g[i], g[i - 1] + u)
    for i in range(len(g) - 2, -1, -1): g[i] = min(g[i], g[i + 1] + u)
    return g

class Instance:
    """U = -F on the grid of types; lp[j] = ln P_j."""
    def __init__(self, ns, U, u):
        self.ns, self.U, self.u, self.m = list(ns), U, u, len(ns)
        self.lp = [logbinom(nj) for nj in ns]
        assert self.max_step() <= u + 1e-9, self.max_step()
    def max_step(self):
        return max(np.abs(np.diff(self.U, axis=ax)).max() for ax in range(self.m))
    def lnP(self, blocks):
        """ln of the product weight on the listed blocks, broadcast to the full grid"""
        out = 0
        for j in blocks:
            sh = [1] * self.m; sh[j] = self.ns[j] + 1
            out = out + self.lp[j].reshape(sh)
        return np.broadcast_to(out, self.U.shape) if blocks else np.zeros(self.U.shape)
    def lnA(self):
        return logsumexp(self.lnP(range(self.m)) + self.U)
    def depends(self, j, tol=1e-9):
        """types d (interior in block j) at which F(d+e_j) != F(d-e_j)"""
        U = np.moveaxis(self.U, j, 0)
        dep = np.zeros(U.shape, bool)
        dep[1:-1] = np.abs(U[2:] - U[:-2]) > tol
        return np.moveaxis(dep, 0, j)

def sampled(rng, lnmean):
    """indicator that a Poisson variable with mean exp(lnmean) is positive"""
    p = -np.expm1(-np.exp(np.minimum(lnmean, 5.0)))
    return rng.random(lnmean.shape) < p
def ln_count(rng, lnmean):
    """ln of a Poisson count with mean exp(lnmean)  (-inf where the count is 0)"""
    mean = np.exp(np.minimum(lnmean, 40.0))
    out = np.full(lnmean.shape, -np.inf)
    small = lnmean < np.log(1e6)
    cnt = rng.poisson(np.where(small, mean, 0.0))
    rel = np.clip(rng.standard_normal(lnmean.shape) * np.exp(-0.5 * np.clip(lnmean, 0.0, 700.0)), -0.5, 0.5)
    with np.errstate(divide='ignore'):
        out = np.where(small, np.log(cnt), lnmean + np.log1p(rel))
    return out

def run(inst, lnM, rng, rounds=3):
    m = inst.m
    S = []                                   # revealed blocks
    for rnd in range(1, rounds):             # the revealing rounds
        rest = [j for j in range(m) if j not in S]
        seen = sampled(rng, lnM + inst.lnP(rest))          # every shell of S, M points: type seen?
        new = [j for j in rest if (inst.depends(j) & seen).any()]
        S = sorted(S + new)
    rest = [j for j in range(m) if j not in S]
    lnN = ln_count(rng, lnM + inst.lnP(rest))               # counts per (shell of S, type of the rest)
    est = logsumexp((inst.lnP(S) + lnN - lnM + inst.U).ravel())
    return est, S

# ------------------------------------------------------------------ instances
def extremal_three(u, ns, Theta):
    """deepest admissible function with: on V0(Theta) F depends on d1 only and has mass <= that of the
    typical type; on V_P(Theta) F depends on (d1,d2) only (Lemma B's hypotheses with P={1},Q={2},T={3})"""
    lp = [logbinom(nj) for nj in ns]
    t = [l.max() - l for l in lp]
    INF = 1e18
    cap1 = lip_minorant_1d(t[0], u)
    U1 = np.where(t[0] <= Theta, cap1, INF)
    T12 = t[0][:, None] + t[1][None, :]
    inV0 = T12 <= Theta
    U2 = np.where(inV0, np.broadcast_to(U1[:, None], T12.shape), INF).astype(float)
    U2 = lip_pass(U2, u); U2 = np.where(inV0, np.minimum(U2, U1[:, None]), U2)
    U2 = np.where((t[1] <= Theta)[None, :], U2, INF)
    T23 = t[1][:, None] + t[2][None, :]
    U = np.where((T23 <= Theta)[None, :, :], np.broadcast_to(U2[:, :, None], (ns[0] + 1, ns[1] + 1, ns[2] + 1)), INF).astype(float)
    return Instance(ns, lip_pass(U, u), u)

def u3_twin(u, ns, Theta):
    """the deep twin of the two-round separation: flat histogram of block 1 on W1, capped envelope on V2,
    deepest extension beyond"""
    lp = [logbinom(nj) for nj in ns]; t = [l.max() - l for l in lp]
    INF = 1e18
    cap1 = lip_minorant_1d(t[0], u); capB = lip_minorant_1d(t[1], u)
    T12 = t[0][:, None] + t[1][None, :]
    W1 = T12 <= Theta; W2 = t[1] <= Theta
    U = np.where(W1, np.broadcast_to(cap1[:, None], T12.shape), INF).astype(float)
    U = lip_pass(U, u)
    U = np.where(W2[None, :], np.minimum(U, cap1[:, None] + capB[None, :]), INF)
    return Instance(ns, lip_pass(U, u), u)

def cone(u, ns):
    grids = np.meshgrid(*[np.arange(nj + 1) for nj in ns], indexing='ij')
    return Instance(ns, -u * sum(grids).astype(float), u)

def random_admissible(u, ns, rng, K=6):
    """minimum of K random cones and dips with random offsets, in the types (admissible by construction)"""
    grids = np.meshgrid(*[np.arange(nj + 1) for nj in ns], indexing='ij')
    F = np.zeros(grids[0].shape)
    for _ in range(K):
        c = [rng.integers(0, nj + 1) for nj in ns]
        w = rng.random(len(ns)) < 0.7
        dist = sum(np.abs(g - ci) * wi for g, ci, wi in zip(grids, c, w))
        F = np.minimum(F, u * dist - rng.uniform(0, 0.6) * u * sum(ns))
    return Instance(ns, -F, u)

def report(name, inst, lnMs, rng, reps=5):
    lnA = inst.lnA()
    for lnM in lnMs:
        row = []
        for rounds in (1, 2, 3):
            errs = []; Ss = set()
            for _ in range(reps):
                est, S = run(inst, lnM, rng, rounds)
                errs.append(est - lnA); Ss.add(tuple(S))
            row.append("R%d: %+8.3f..%+8.3f %s" % (rounds, min(errs), max(errs), sorted(Ss)[-1]))
        print("  %-34s ln M = %6.1f   %s" % (name, lnM, "   ".join(row)))
    sys.stdout.flush()

if __name__ == "__main__":
    rng = np.random.default_rng(20261128)
    u = 2.0; pu, L1, a, h = consts(u)
    print("u = %g: a = %.4f, h = %.4f, theta2*/h = 1.328" % (u, a, h))
    print("columns: range over the runs of ln(estimate) - ln A, and the blocks revealed before the last round")
    print("NOTE: an instance designed against a budget Theta_c hides its structure from M points only if")
    print("      ln M is below Theta_c by a margin of order ln(number of types); the sweeps show both sides.")
    n = 300
    print("(I3) cone on two blocks, n = %d (n a = %.1f, n h = %.1f)" % (n, n * a, n * h))
    report("cone (150,150)", cone(u, (150, 150)), [0.5 * n * h, n * h, 1.2 * n * h], rng)
    n = 1200
    Tc = 1.15 * n * h
    print("(I2) deep twin of the two-round separation, blocks (720,480), n h = %.1f, designed against Theta_c = 1.15 n h = %.1f" % (n * h, Tc))
    inst = u3_twin(u, (720, 480), Tc)
    report("U3 twin", inst, [Tc - 24, Tc - 16, Tc - 8, Tc, Tc + 8], rng, reps=3)
    n = 480
    print("(I1) extremal three-block function of Lemma B, blocks (96,192,192), n h = %.1f" % (n * h))
    for mult in (0.7, 1.15, 1.3):
        Tc = mult * n * h
        inst = extremal_three(u, (96, 192, 192), Tc)
        report("extremal, Theta_c = %.2f n h = %.1f" % (mult, Tc), inst, [Tc - 16, Tc - 8, Tc, Tc + 8], rng, reps=3)
    print("(I4) random admissible functions on three blocks (100,100,100), n h = %.1f" % (300 * h))
    for i in range(4):
        report("random #%d" % i, random_admissible(u, (100, 100, 100), rng), [1.2 * 300 * h], rng, reps=3)
