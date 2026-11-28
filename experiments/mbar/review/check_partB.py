"""Referee A -- independent exact checks of Theorem B1 / B2 / B3 (MATHEMATICS.md) by full enumeration
on tiny finite models, with adversarial predictors, adversarial adaptive allocation, and the three
'peeking' variants that the theorems do NOT license (they must break).  No import of d9mbar.
"""
import itertools
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(99)


def rand_model(K, J, zero_prob=0.0):
    while True:
        P = rng.dirichlet(np.ones(J), size=K)
        P = np.where(rng.random((K, J)) < zero_prob, 0.0, P)
        if np.all(P.sum(axis=1) > 0):
            return P / P.sum(axis=1, keepdims=True)


def samples(n, J):
    labels = [k for k in range(len(n)) for _ in range(n[k])]
    for xs in itertools.product(range(J), repeat=len(labels)):
        yield labels, xs


def expect(P, n, stat):
    """Exact E[stat(labels, xs)] under stratified sampling with counts n."""
    tot = 0.0
    for labels, xs in samples(n, P.shape[1]):
        pr = np.prod([P[k, x] for k, x in zip(labels, xs)])
        if pr > 0:
            tot += pr * stat(labels, xs)
    return tot


def factor_table(P, s, lam, w):
    """fac[k, x] = lam_k(x) m_w(x) / (s_k p_k(x)) on p_k(x) > 0."""
    mw = w @ P
    with np.errstate(divide="ignore", invalid="ignore"):
        fac = lam * mw[None, :] / (s[:, None] * P)
    return np.where(P > 0, fac, 0.0)


# ------------------------------------------------------------------ B1: arbitrary predictors, tilts
print("== B1: exact enumeration, arbitrary predictors / tilts")
worst = 0.0
nmod = 0
for trial in range(400):
    K, J = int(rng.integers(2, 4)), int(rng.integers(2, 5))
    P = rand_model(K, J, zero_prob=rng.choice([0.0, 0.3]))
    n = [int(rng.integers(1, 4)) for _ in range(K)]
    if sum(n) > 6:
        continue
    s = np.array(n) / sum(n)
    lam = rng.dirichlet(np.ones(K + 1) * rng.choice([0.2, 1.0]), size=J).T[:K]     # sum_k lam_k <= 1
    if rng.random() < 0.3:
        lam = rng.dirichlet(np.ones(K) * 0.2, size=J).T                             # sum = 1, peaky
    w = rng.dirichlet(np.ones(K + 1))[:K] if rng.random() < 0.5 else rng.dirichlet(np.ones(K))
    fac = factor_table(P, s, lam, w)
    E = expect(P, n, lambda lab, xs: np.prod([fac[k, x] for k, x in zip(lab, xs)]))
    worst = max(worst, E)
    nmod += 1
print(f"  {nmod} models: max expectation = {worst:.10f}  (claim: <= 1)")

# adversarial predictor and tilt: maximise the exact expectation prod_k b_k^{n_k}
worst_adv = 0.0
for trial in range(60):
    K, J = int(rng.integers(2, 4)), int(rng.integers(2, 5))
    P = rand_model(K, J, zero_prob=rng.choice([0.0, 0.3]))
    n = np.array([int(rng.integers(1, 5)) for _ in range(K)])
    s = n / n.sum()

    def negE(z):
        lam = np.exp(z[:K * J].reshape(K, J)); lam = lam / lam.sum(axis=0, keepdims=True)
        w = np.exp(z[K * J:]); w = w / w.sum()
        b = (factor_table(P, s, lam, w) * P).sum(axis=1)
        return -float(np.prod(b ** n))
    best = 0.0
    for start in range(4):
        res = minimize(negE, rng.normal(size=K * J + K), method="BFGS")
        best = max(best, -res.fun)
    worst_adv = max(worst_adv, best)
print(f"  adversarially optimised predictor+tilt (60 models): sup of expectation found = {worst_adv:.10f}")

# identity E = exp(-N KL(s || a)) for lam = pi(f'), w = s
worst_id = 0.0
for trial in range(200):
    K, J = int(rng.integers(2, 4)), int(rng.integers(2, 5))
    P = rand_model(K, J, zero_prob=rng.choice([0.0, 0.3]))
    n = [int(rng.integers(1, 3)) for _ in range(K)]
    s = np.array(n) / sum(n)
    d = rng.normal(size=K) * 2                      # f' - f*
    m = s @ P
    num = s[:, None] * np.exp(d)[:, None] * P
    lam = num / num.sum(axis=0, keepdims=True)      # pi(f'; x)
    fac = factor_table(P, s, lam, s)
    E = expect(P, n, lambda lab, xs: np.prod([fac[k, x] for k, x in zip(lab, xs)]))
    a = (lam * m[None, :]).sum(axis=1)
    worst_id = max(worst_id, abs(E - np.exp(-sum(n) * np.sum(s * np.log(s / a)))))
print(f"  identity E = exp(-N KL(s||a)): max abs error = {worst_id:.2e}")

# what the theorem does NOT license (1): proportions in pi different from the batch composition
P = rand_model(2, 3)
n = [1, 3]
s_true = np.array(n) / 4
s_wrong = np.array([0.5, 0.5])
lam = np.tile(s_true[:, None], (1, 3))             # constant predictor
fac = factor_table(P, s_wrong, lam, s_wrong)
E = expect(P, n, lambda lab, xs: np.prod([fac[k, x] for k, x in zip(lab, xs)]))
print(f"  wrong proportions in the statistic (s'=(.5,.5), counts (1,3)): E = {E:.4f} "
      f"(= exp(N KL(s||s')) = {np.exp(4 * np.sum(s_true * np.log(s_true / s_wrong))):.4f} > 1)")

# ------------------------------------------------------------------ B3: adaptive rounds, exact
print("== B3: two rounds, adversarial adaptive composition and plug-in (exact enumeration)")


def lr_stat(P, s, d, lab, xs):
    """prod_n pi_y(f')/pi_y(f*) with proportions s, d = f' - f*."""
    val = 1.0
    for k, x in zip(lab, xs):
        if s[k] == 0:
            return np.nan
        val *= np.exp(d[k]) * (s @ P[:, x]) / (s @ (np.exp(d) * P[:, x]))
    return val


def round_expect(P, n, d):
    s = np.array(n) / sum(n)
    return expect(P, n, lambda lab, xs: lr_stat(P, s, d, lab, xs))


worst_seq = 0.0
worst_peek_plug = 0.0
worst_peek_incl = 0.0
worst_peek_comp = 0.0
menu_comp = [(1, 1), (2, 1), (1, 2), (3, 1), (1, 3)]
menu_d = [np.array([0.0, t]) for t in (-3, -1.5, -0.5, 0.5, 1.5, 3)]
for trial in range(40):
    P = rand_model(2, 3, zero_prob=rng.choice([0.0, 0.2]))
    n1 = (1, 1)
    s1 = np.array(n1) / 2
    d1 = menu_d[rng.integers(len(menu_d))]
    # adversary: after seeing round 1, picks composition and plug-in of round 2 that maximise the
    # conditional expectation of the round-2 factor
    best2 = max(round_expect(P, c, d) for c in menu_comp for d in menu_d)
    E1 = expect(P, n1, lambda lab, xs: lr_stat(P, s1, d1, lab, xs))
    worst_seq = max(worst_seq, E1 * best2)       # E[Lambda_2] <= E[Lambda_1] * sup conditional factor
    # peeking 1: plug-in chosen after seeing the batch (best d in the menu for the realised batch)
    Epeek = expect(P, (2, 2), lambda lab, xs: max(lr_stat(P, np.array([.5, .5]), d, lab, xs) for d in menu_d))
    worst_peek_plug = max(worst_peek_plug, Epeek)
    # peeking 2: the batch is included only if its e-value exceeds 1 (data-dependent set E)
    Eincl = expect(P, (2, 2), lambda lab, xs: max(1.0, lr_stat(P, np.array([.5, .5]), d1, lab, xs)))
    worst_peek_incl = max(worst_peek_incl, Eincl)
    # peeking 3: composition decided after seeing the data: draw (2,2); analyse either the full batch
    # (2,2) or only the first draw of each state (1,1), whichever gives the larger statistic
    def comp_peek(lab, xs):
        full = lr_stat(P, np.array([.5, .5]), d1, lab, xs)
        sub = lr_stat(P, np.array([.5, .5]), d1, [0, 1], [xs[0], xs[2]])
        return max(full, sub)
    worst_peek_comp = max(worst_peek_comp, expect(P, (2, 2), comp_peek))
print(f"  adversarial adaptive rule (licensed):      sup E[Lambda_2] = {worst_seq:.6f}  (claim <= 1)")
print(f"  plug-in peeks at its own batch (unlicensed): sup E = {worst_peek_plug:.4f}")
print(f"  data-dependent inclusion of a batch (unlicensed): sup E = {worst_peek_incl:.4f}")
print(f"  data-dependent sub-batch (unlicensed): sup E = {worst_peek_comp:.4f}")

# single-state round contributes factor 1; single factors are not e-values
P = rand_model(2, 3)
s = np.array([0.5, 0.5]); d = np.array([0.0, 2.0])
m = s @ P
lamk = s[:, None] * np.exp(d)[:, None] * P / (s @ (np.exp(d)[:, None] * P))
ak = (lamk * m[None, :]).sum(axis=1)
print("  per-state factor expectations a_k/s_k:", np.round(ak / s, 4), "(one exceeds 1; product over the batch <= 1)")
