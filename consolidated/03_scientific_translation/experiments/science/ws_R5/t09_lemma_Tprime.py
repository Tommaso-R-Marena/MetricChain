"""t09_lemma_Tprime.py -- Lemma 11.96 (= Lemma T' of W_REPORT: inherently typical subsets for a fixed sequence of site
types), by exact enumeration: 2 three-letter sites and 3 two-letter sites in the order (A, B, A, B, B), 72 points,
a product measure rho = prod rho_{tau(i)}, random nonempty sets, M in {1, 2, 3, 5}.

Checked, as stated:
 (2) rho(A~) >= rho(A) * prod_j (n_j+1)^(-q_j (M+1)^q_j)
 (3) alpha_A - q_max/M <= alpha := D(P_{X|UT} || rho_T | P_UT) <= alpha_{A~}
 (4) I(X_I; V | U_I, T_I) = alpha_{A~} - alpha   (computed directly from the conditional laws of rho(.|A~))
"""
import itertools, math, time
from collections import defaultdict
import numpy as np

rng = np.random.default_rng(99)
types = [0, 1, 0, 1, 1]
qs = [3, 2]
n = len(types)
nj = [types.count(0), types.count(1)]
rho_site = [np.array([0.5, 0.3, 0.2]), np.array([0.65, 0.35])]
X = list(itertools.product(*[range(qs[t]) for t in types]))
rho = np.array([np.prod([rho_site[types[i]][x[i]] for i in range(n)]) for x in X])
index = {x: k for k, x in enumerate(X)}


def conditional_laws(members):
    """members: list of points with their rho-weights -> dict prefix -> law of the next letter under rho(.|set)."""
    mass = defaultdict(float)
    for x in members:
        w = rho[index[x]]
        for i in range(n + 1):
            mass[x[:i]] += w
    def law(prefix):
        i = len(prefix)
        q = qs[types[i]]
        v = np.array([mass.get(prefix + (a,), 0.0) for a in range(q)])
        return v / v.sum()
    return law, mass


def kl(p, q):
    m = p > 0
    return float(np.sum(p[m] * (np.log(p[m]) - np.log(q[m]))))


def check(A, M):
    law, mass = conditional_laws(A)
    def label(prefix):
        p = law(prefix)
        c = np.ceil(M * p - 1e-12)
        return tuple(int(v) for v in c)             # the label is the vector of ceilings (normalised law = c / sum c)
    # joint type of (tau(i), u_i(x^{i-1}), x_i)
    def jt(x):
        cnt = defaultdict(int)
        for i in range(n):
            cnt[(types[i], label(x[:i]), x[i])] += 1
        return tuple(sorted(cnt.items()))
    classes = defaultdict(list)
    for x in A:
        classes[jt(x)].append(x)
    best = max(classes.values(), key=lambda c: sum(rho[index[x]] for x in c))
    At = best
    rA = sum(rho[index[x]] for x in A)
    rAt = sum(rho[index[x]] for x in At)
    # (2)
    ok2 = rAt >= rA * np.prod([(nj[j] + 1.0) ** (-qs[j] * (M + 1) ** qs[j]) for j in range(2)]) * (1 - 1e-12)
    # the labelled profile P_TUX from any member of A~
    x0 = At[0]
    cnt = defaultdict(float)
    for i in range(n):
        cnt[(types[i], label(x0[:i]), x0[i])] += 1.0 / n
    PTU = defaultdict(float)
    for (t, u, a), w in cnt.items():
        PTU[(t, u)] += w
    alpha = 0.0
    cond = {}
    for (t, u), w in PTU.items():
        p = np.array([cnt.get((t, u, a), 0.0) for a in range(qs[t])]) / w
        cond[(t, u)] = p
        alpha += w * kl(p, rho_site[t])
    aA, aAt = -math.log(rA) / n, -math.log(rAt) / n
    ok3 = (aA - max(qs) / M <= alpha + 1e-12) and (alpha <= aAt + 1e-12)
    # (4): I(X_I; V | U_I, T_I) under rho(.|A~), with the labels u_i defined from A
    law_t, mass_t = conditional_laws(At)
    cmi = 0.0
    for i in range(n):
        prefixes = {x[:i] for x in At}
        for pre in prefixes:
            ppre = mass_t[pre] / rAt
            cmi += (1.0 / n) * ppre * kl(law_t(pre), cond[(types[i], label(pre))])
    ok4 = abs(cmi - (aAt - alpha)) < 1e-10
    eta = max(qs) / M + sum(qs[j] * (M + 1) ** qs[j] for j in range(2)) * math.log(n + 1) / n
    ok4b = cmi <= eta + 1e-12
    return ok2, ok3, ok4, ok4b, aA, alpha, aAt, cmi


if __name__ == "__main__":
    t0 = time.time()
    tot = 0
    bad = [0, 0, 0, 0]
    tight3 = (np.inf, np.inf)
    for rep in range(160):
        kind = rep % 4
        if kind == 0:      # random subset
            A = [x for x in X if rng.random() < rng.choice([0.1, 0.3, 0.6])]
        elif kind == 1:    # Hamming-type ball around a random centre
            c = X[rng.integers(len(X))]; r = rng.integers(1, 4)
            A = [x for x in X if sum(a != b for a, b in zip(x, c)) <= r]
        elif kind == 2:    # super-level set of a random additive function
            f = [rng.normal(size=qs[t]) for t in types]
            vals = np.array([sum(f[i][x[i]] for i in range(n)) for x in X])
            A = [x for x, v in zip(X, vals) if v >= np.quantile(vals, rng.uniform(0.3, 0.9))]
        else:              # union of two type-like classes
            A = [x for x in X if (x.count(0) + rng.integers(2)) % 3 == 0]
        if not A:
            continue
        for M in (1, 2, 3, 5):
            r = check(A, M)
            tot += 1
            for k in range(4):
                bad[k] += (not r[k])
            tight3 = (min(tight3[0], r[5] - (r[4] - max(qs) / M)), min(tight3[1], r[6] - r[5]))
    print(f"{tot} cases (sets of four kinds x M in 1,2,3,5) on {len(X)} points, site types {types}:")
    print(f"   violations of (2): {bad[0]};  of (3): {bad[1]};  of the identity (4): {bad[2]};  of the bound in (4): {bad[3]}")
    print(f"   smallest slack in (3): alpha - (alpha_A - q_max/M) = {tight3[0]:.3e},  alpha_A~ - alpha = {tight3[1]:.3e}")
    print(f"[{time.time()-t0:.1f} s]")
