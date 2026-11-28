"""Referee A -- tests of the division's CODE (imports d9mbar): pilot_allocation's integer safeguard
(Proposition A9), the e-process region under an adversarial adaptive allocation rule (Theorem B3),
the number of models in the B1 enumeration test, and the abstention on inf - inf.
"""
import sys, re, itertools, warnings
import numpy as np
from scipy.special import logsumexp

sys.path.insert(0, "../src")
from d9mbar.estimators import pilot_allocation, integer_counts, mbar      # noqa: E402
from d9mbar.certificates import lr_confidence_region                       # noqa: E402

warnings.filterwarnings("ignore")
rng = np.random.default_rng(2718)


def V_direct(P, s, nu):
    m = s @ P
    supp = m > 0
    if np.any(np.abs(nu[~supp]) > 1e-12 * max(np.abs(nu).max(), 1e-300)):
        return np.inf
    d = np.sqrt(m[supp])
    Pa = P[:, supp]
    Mt = ((Pa / d).T * s) @ (Pa / d)
    w, E = np.linalg.eigh(np.eye(supp.sum()) - (Mt + Mt.T) / 2)
    pos = w > 1e-9
    coef = E.T @ (nu[supp] / d)
    if np.any(np.abs(coef[~pos]) > 1e-7 * max(np.abs(coef).max(), 1e-300)):
        return np.inf
    return float(np.sum(coef[pos] ** 2 / w[pos]))


# ------------------------------------------------------------------ A9: integer counts
print("== A9 (1): integer_counts vs the coordinatewise domination n0 + counts >= gamma (n0 + u)")
gam = 0.25
viol = {0: 0, 1: 0, 2: 0, 3: 0}
tot = {0: 0, 1: 0, 2: 0, 3: 0}
example = {}
for trial in range(40000):
    K = int(rng.integers(2, 11))
    n0v = int(rng.integers(0, 4))
    n0 = np.full(K, n0v, float)
    rem = float(rng.integers(1, 60))
    u = np.full(K, rem / K)
    plug = rng.dirichlet(np.ones(K) * rng.choice([0.05, 0.3, 1.0])) * rem
    if rng.random() < 0.5:
        plug = np.zeros(K); plug[rng.integers(K)] = rem
    extra = (1 - gam) * plug + gam * u
    cnt = integer_counts(extra, rem, np.ones(K))
    tot[n0v] += 1
    bad = n0 + cnt < gam * (n0 + u) - 1e-9
    if bad.any():
        viol[n0v] += 1
        example.setdefault(n0v, (K, rem, np.round(extra, 3).tolist(), cnt.tolist(), float(gam * (n0v + rem / K))))
for k in sorted(tot):
    print(f"  pilot count per state = {k}: domination violated in {viol[k]} of {tot[k]} random cases", example.get(k, ""))

print("== A9 (2): pilot_allocation itself; true population variance of the returned integer allocation")
nviol, ntot, worst_ratio, ex = 0, 0, 0.0, None
for trial in range(1500):
    K, J = 3, 4
    P = rng.dirichlet(np.ones(J), size=K)
    P[0, 3] = P[1, 3] = 0.0                      # point 3 is private to state 2
    P /= P.sum(axis=1, keepdims=True)
    off = rng.normal(size=K)
    n0 = np.array([int(rng.integers(2, 6)), int(rng.integers(2, 6)), int(rng.integers(0, 2))])
    xs = np.concatenate([rng.choice(J, size=n0[k], p=P[k]) for k in range(K)])
    y = np.repeat(np.arange(K), n0)
    with np.errstate(divide="ignore"):
        U = -np.log(P[:, xs].T) + off[None, :]
    c = np.array([-1.0, 0.0, 1.0])
    rem = float(rng.integers(2, 9))
    try:
        cnt, info = pilot_allocation(U, y, c, n0.sum() + rem, safeguard=gam)
    except Exception as e:
        continue
    ntot += 1
    nfin = n0 + cnt
    nunif = n0 + rem / K
    nu = c @ P
    Vf, Vu = V_direct(P, nfin.astype(float), nu), V_direct(P, nunif, nu)
    if Vf > Vu / gam * (1 + 1e-9):
        nviol += 1
        if ex is None or (np.isfinite(Vf) and Vf / (Vu / gam) > worst_ratio):
            ex = dict(pilot=n0.tolist(), rem=rem, counts=cnt.tolist(), final=nfin.tolist(),
                      unif=np.round(nunif, 3).tolist(), V_final=Vf, bound=Vu / gam, fallback=info["fallback"])
        if np.isfinite(Vf):
            worst_ratio = max(worst_ratio, Vf / (Vu / gam))
print(f"  {ntot} runs with a pilot count of 0 or 1 in one state: V_true(final) > V_true(n0+u)/gamma in {nviol}; example: {ex}")
# the same with every pilot count >= 2
nviol2, ntot2 = 0, 0
for trial in range(600):
    K, J = 3, 4
    P = rng.dirichlet(np.ones(J), size=K)
    off = rng.normal(size=K)
    n0 = rng.integers(2, 7, K)
    xs = np.concatenate([rng.choice(J, size=n0[k], p=P[k]) for k in range(K)])
    y = np.repeat(np.arange(K), n0)
    U = -np.log(P[:, xs].T) + off[None, :]
    c = np.array([-1.0, 0.0, 1.0])
    rem = float(rng.integers(2, 30))
    try:
        cnt, info = pilot_allocation(U, y, c, n0.sum() + rem, safeguard=gam)
    except Exception:
        continue
    ntot2 += 1
    nu = c @ P
    if V_direct(P, (n0 + cnt).astype(float), nu) > V_direct(P, n0 + rem / K, nu) / gam * (1 + 1e-9):
        nviol2 += 1
print(f"  {ntot2} runs with every pilot count >= 2: violations {nviol2}")

# ------------------------------------------------------------------ B3 through the code
print("== B3 through lr_confidence_region(batches=...): adversarial adaptive allocation, stop at first exclusion")


def phi_def(A, y, f):
    return float(np.sum(logsumexp(A + f, axis=1) - f[y]))


def run_adaptive(overlap, rounds, per_round, alpha, adversary, trials, seed):
    r = np.random.default_rng(seed)
    K = 3
    P = np.full((K, K), overlap / (K - 1)); np.fill_diagonal(P, 1 - overlap)
    ftrue = np.array([0.0, 1.0, -0.5])
    with np.errstate(divide="ignore"):
        Ut = -np.log(P).T + ftrue[None, :]          # Ut[x, k] = -log q_k(x), q_k = P_k e^{-f_k}

    def draw(comp):
        xs = np.concatenate([r.choice(K, size=comp[k], p=P[k]) for k in range(K)])
        return Ut[xs], np.repeat(np.arange(K), comp)
    ever, statuses = 0, {}
    for tr in range(trials):
        comp = np.full(K, per_round // K)
        U, y = draw(comp)
        batches = [np.arange(len(y))]
        excluded = False
        logLam = 0.0
        for b in range(1, rounds + 1):
            if adversary == "gambler":
                # knows the truth and the current value of the e-process: bet big when behind
                if logLam < 0:
                    comp = np.array([per_round - 2, 1, 1])[r.permutation(K)]
                else:
                    comp = np.full(K, per_round // K)
            elif adversary == "random":
                comp = r.multinomial(per_round - K, r.dirichlet(np.ones(K) * 0.3)) + 1
            else:
                comp = np.full(K, per_round // K)
            Ub, yb = draw(comp)
            batches.append(np.arange(len(y), len(y) + len(yb)))
            U, y = np.vstack([U, Ub]), np.concatenate([y, yb])
            reg = lr_confidence_region(U, y, alpha=alpha, batches=batches)
            statuses[reg.status] = statuses.get(reg.status, 0) + 1
            if reg.status == "REJECT_MODEL":
                excluded = True
            elif reg.A.size:
                val = phi_def(reg.A, reg.labels, ftrue)
                logLam = val - reg.meta["reference"]
                if reg.status == "OK" and val > reg.level:
                    excluded = True
            if excluded:
                break
        ever += excluded
    return ever / trials, statuses


for overlap, adv in ((0.05, "gambler"), (0.3, "gambler"), (0.05, "random"), (0.3, "fixed")):
    frac, st = run_adaptive(overlap, rounds=8, per_round=12, alpha=0.05, adversary=adv, trials=1200, seed=5)
    print(f"  overlap {overlap}, rule {adv}: P(truth ever excluded) = {frac:.4f} (claim <= 0.05; MC s.e. ~0.006); statuses {st}")

# ------------------------------------------------------------------ B1 test: how many models?
src = open("../tests/test_certificates.py").read()
m = re.search(r"def test_evalue_exact_enumeration\(\):.*?return maxE, worst\n", src, re.S)
code = m.group(0).replace("maxE = max(maxE, tot)", "maxE = max(maxE, tot); COUNT[0] += 1")
ns = dict(np=np, itertools=itertools, COUNT=[0])
exec(code, ns)
maxE, worst = ns["test_evalue_exact_enumeration"]()
print(f"== B1 enumeration test of the division: models enumerated = {ns['COUNT'][0]}, max E = {maxE:.9f}, identity error = {worst:.2e}")

# ------------------------------------------------------------------ inf - inf
print("== numerical trap: a state absent from prev and from the current batch, with no finite energy on prev")
K = 3
U0 = np.array([[0.0, 1.0, np.inf], [0.5, 0.0, np.inf], [0.2, 0.3, np.inf], [1.0, 0.1, np.inf],
               [0.0, 1.0, np.inf], [0.5, 0.0, np.inf], [0.2, 0.3, np.inf], [1.0, 0.1, np.inf],
               [0.3, 0.2, 0.0], [np.inf, np.inf, 0.0], [0.1, 0.4, 0.3], [0.6, 0.0, 0.2]])
y0 = np.array([0, 1, 0, 1, 0, 1, 0, 1, 2, 2, 0, 1])
reg = lr_confidence_region(U0, y0, batches=[np.arange(0, 4), np.arange(4, 8), np.arange(8, 12)])
print("  status:", reg.status, reg.meta)
