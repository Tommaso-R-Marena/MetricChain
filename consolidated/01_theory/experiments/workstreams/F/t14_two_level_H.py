"""t14: the two-level bracket RELATIVE TO THE REFERENCE INSTANCE H on a biased cube -- logic test at small size.

Outer block Q_o (n_o = 4, all 2^16 - 2 proper subsets enumerated, so the tail function
    Xi_H(q) = max { sum_{a in D} mu_H(a) (e^{s_H(a -> D^c)} - 1) : D proper subset, mu_H(D) <= q }
is exact), inner block Q_i (n_i = 3..5, fibre averages enumerated; the inner procedure is SIMULATED: a call at
accuracy x returns a valid bracket [L, U], U = L e^x, placed adversarially).  psi is an arbitrary u-Lipschitz
function on Q_o x Q_i, the reference measure is Bernoulli(p)^n.

Checked on every run (the statements of the proof of Theorem F7 of REPORT.md):
  * the bracket contains A = E_pi e^{-psi} and is at most G + ln(4 e J + 3) wide;
  * every certified exceedance probability is valid:  mu_H(What > s_j) <= q_j;
  * every sample size is at most 8 J e^2 M_dagger, M_dagger = 2K/q_dagger (q_dagger from Xi_H), and at most twice
    the negligibility threshold;
  * the count of points close to a level:  M_neg mu_H(What > s e^{-x}) <= 8 K J e^2 e^x.
The reference instance is H (the lower envelope of the normalised additive instances), the zero residual (plain
sampling of pi) or an additive instance: the bracket is valid for every reference in the class (only the cost
depends on it).  Mutations (each must produce invalid brackets, otherwise the test has no power):
  M1 closure also when q = 1;  M3 the weights 1/w_ref forgotten (levels for W instead of W/w_ref).
(The orientation of the slack and the tail function itself are tested directly in t15_tail_lemma_H.py.)
"""
import math, sys, time
import numpy as np
from birad import logw_H

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 14)
REPS = int(sys.argv[2]) if len(sys.argv) > 2 else 40


def cube(n):
    N = 2 ** n
    idx = np.arange(N)
    pop = np.array([bin(x).count("1") for x in range(N)])
    return pop, pop[idx[:, None] ^ idx[None, :]]


def rand_lipschitz(n, u, D, pop, kind):
    N = D.shape[0]
    m = int(rng.integers(1, 7))
    idx = rng.choice(N, size=min(m, N), replace=False)
    scale = u * n * float(rng.choice([0.2, 0.5, 1.0]))
    v = rng.uniform(0, scale, size=len(idx))
    if kind == 0:
        return (v[:, None] + u * D[idx, :]).min(0)
    if kind == 1:
        return (v[:, None] - u * D[idx, :]).max(0)
    if kind == 2:
        return u * D[int(rng.integers(N))].astype(float)                       # cone
    if kind == 3:
        return float(rng.uniform(-u, u)) * pop.astype(float)                   # additive instance
    if kind == 4:
        return -u * np.maximum(int(rng.integers(1, 4)) - D[int(rng.integers(N))], 0).astype(float)   # dip in the flat instance
    z = rng.normal(0, u * n * 0.3, size=N)
    return (z[:, None] + u * D).min(0)


def tail_tables(n_o, p, u, ref="H", mutation=None):
    """exact tail function of the outer block relative to a reference instance psi_ref in L_u:
         mu_ref = pi e^{-psi_ref}/Z_ref,   s_ref(a, a') = u d(a,a') + psi_ref(a) - psi_ref(a') >= 0,
         Xi_ref(q) = max { sum_{a in D} mu_ref(a)(e^{s_ref(a -> D^c)} - 1) : D proper subset, mu_ref(D) <= q }.
    ref = "H" (lower envelope of the normalised additive instances), "zero" (psi_ref = 0: plain sampling of pi),
    or a number gamma (the additive instance gamma|a|).  Returns the sorted table and the reference data."""
    N = 2 ** n_o
    pop, D = cube(n_o)
    if ref == "H":
        logw = logw_H(n_o, p, u, pop)
    elif ref == "zero":
        logw = np.zeros(N)
    else:
        logw = -float(ref) * pop
    psiR = -logw
    pio = p ** pop * (1 - p) ** (n_o - pop)
    ZR = float((pio * np.exp(logw)).sum())
    muR = pio * np.exp(logw) / ZR
    sR = u * D + psiR[:, None] - psiR[None, :]
    assert sR.min() > -1e-12
    if mutation == "M2":
        sR = u * D - psiR[:, None] + psiR[None, :]
    masks = np.arange(1, 2 ** N - 1)                             # all proper nonempty subsets of the 2^{n_o} points
    member = ((masks[:, None] >> np.arange(N)[None, :]) & 1).astype(bool)      # [set, a]
    mu = member @ muR
    phi = np.zeros(len(masks))
    for a in range(N):
        d = np.where(member, np.inf, sR[a][None, :]).min(axis=1)              # min over a' not in D of s_ref(a, a')
        phi += np.where(member[:, a], muR[a] * np.expm1(d), 0.0)
    order = np.argsort(mu, kind="stable")
    return dict(mu=mu[order], pref=np.maximum.accumulate(phi[order]), muH=muR, wH=np.exp(logw), ZH=ZR, sH=sR, pop=pop, D=D, pio=pio,
                masks=masks[order], phi=phi[order])


_CACHE = {}


def tables(n_o, p, u, ref="H", mutation=None):
    key = (n_o, p, u, ref, mutation if mutation == "M2" else None)
    if key not in _CACHE:
        _CACHE[key] = tail_tables(n_o, p, u, ref, mutation)
    return _CACHE[key]


def Xi(tab, q):
    k = int(np.searchsorted(tab["mu"], q * (1 + 1e-12), side="right"))
    return 0.0 if k == 0 else float(tab["pref"][k - 1])


def q_dagger(tab, level):
    """sup{ q0 <= 1 : Xi(q)/q <= level for all q <= q0 } on the breakpoints of Xi"""
    mu, pref = tab["mu"], tab["pref"]
    bad = np.nonzero(pref > level * mu * (1 + 1e-12))[0]
    # Xi jumps at the breakpoints mu_k; between breakpoints Xi is constant and Xi/q decreases
    if len(bad) == 0:
        return 1.0
    return float(mu[bad[0]]) * (1 - 1e-12)


def harper_tail(n_o, u, q):
    """the tail function of the uniform cube (Theorem 11.52): 2^{-n_o} E_r(n_o), r least radius with |B(r)| >= 2^{n_o} q"""
    binom = [math.comb(n_o, j) for j in range(n_o + 1)]
    ball = np.cumsum(binom)
    if 2 ** n_o * q < 1:
        return 0.0
    r = next(rr for rr in range(n_o + 1) if ball[rr] >= 2 ** n_o * q - 1e-9)
    if r >= n_o:
        return math.inf
    return sum(binom[j] * (math.exp(u * (r + 1 - j)) - 1) for j in range(r + 1)) / 2 ** n_o


def two_level(tab, What, s0, n, n_i, u, b, G, K, J, mode, mutation=None, step=0.5):
    muH = tab["muH"]
    N = len(muH)
    cdf = np.cumsum(muH)
    xs = np.array(list(np.arange(2 * u * n_i + 1.0, b, -step)) + [b * (1 - 1e-9)])
    Wl = np.zeros(0); L = np.zeros(0); U = np.zeros(0); acc = np.zeros(0, dtype=np.int64); pts = np.zeros(0, dtype=np.int64)
    ell = s0
    levels = []
    for j in range(J + 1):
        s = s0 * math.exp(j)
        ell_in = ell
        Mneg = 2 * K * J * math.e * s / (ell_in * math.exp(b))
        M = K
        while True:
            if len(Wl) < M:
                extra = M - len(Wl)
                new = np.minimum(np.searchsorted(cdf, rng.uniform(size=extra)), N - 1)
                pts = np.concatenate([pts, new])
                Wl = np.concatenate([Wl, What[new]])
                L = np.concatenate([L, np.zeros(extra)]); U = np.concatenate([U, np.full(extra, np.inf)])
                acc = np.concatenate([acc, np.full(extra, -1, dtype=np.int64)])
            while True:
                und = np.nonzero((U[:M] > s) & (L[:M] <= s * math.exp(-b)))[0]
                if len(und) == 0:
                    break
                if np.any(acc[und] >= len(xs) - 1):
                    return dict(error="classification does not end at the last accuracy of the ladder")
                acc[und] += 1
                x = xs[acc[und]]
                t = rng.uniform(size=len(und)) if mode == 0 else (np.ones(len(und)) if mode == 1 else np.zeros(len(und)))
                L[und] = np.maximum(L[und], Wl[und] * np.exp(-t * x))
                U[und] = np.minimum(U[und], Wl[und] * np.exp((1 - t) * x))
            Nh = int((U[:M] > s).sum())
            q = min(1.0, 2 * max(Nh, K) / M)
            if Nh >= K:
                ell = max(ell, s * math.exp(-b) * Nh / (2 * M))
            if mutation == "M4":
                tail = s * harper_tail(int(round(math.log2(N))), u, q)
            elif q < 1 or mutation == "M1":
                tail = s * Xi(tab, min(q, 1 - 1e-9) if mutation == "M1" else q)
            else:
                tail = math.inf
            if tail <= math.exp(G) * ell:
                upper = s0 + sum(lv[0] * math.e * lv[2] for lv in levels) + tail
                return dict(ell=ell, upper=upper, levels=levels, last=(s, M, q, tail), J=J, npts=len(Wl))
            if Nh >= K or M >= Mneg:
                levels.append((s, M, q, Nh >= K, ell_in))
                break
            M *= 2
    return dict(error="no closure within J levels")


def make_instance(kind, n_o, n_i, p, u, tab, pop, D):
    """psi on Q_o x Q_i (outer coordinates = high bits).  kinds 0-5: generic; 6: the reference instance on the outer
    block with the deepest admissible dip on a random outer set (extremal for the tail lemma); 7: a cone centred at
    the least typical corner; 8: the reference on the outer block with the deepest dip at the outer point of smallest
    reference measure (a level that is left as negligible when that measure is small)."""
    n = n_o + n_i
    No = 2 ** n_o
    if kind <= 5:
        return rand_lipschitz(n, u, D, pop, kind)
    outer = np.arange(2 ** n) >> n_i
    psiH = -np.log(tab["wH"])
    if kind == 7:
        corner = (2 ** n - 1) if p < 0.5 else 0
        return u * D[corner].astype(float)
    if kind == 6:
        k = int(rng.integers(1, No - 1))
        Dset = np.zeros(No, dtype=bool); Dset[rng.choice(No, size=k, replace=False)] = True
    else:
        Dset = np.zeros(No, dtype=bool); Dset[int(np.argmin(tab["muH"]))] = True
    Do = tab["D"]
    low = (psiH[~Dset][None, :] - u * Do[np.ix_(np.arange(No), ~Dset)]).max(axis=1)     # lower McShane extension from D^c
    psi_o = np.where(Dset, low, psiH)
    return psi_o[outer]


def run_suite(mutation=None, reps=REPS, verbose=False, lowK=False, refs=None):
    stats = dict(runs=0, invalid=0, too_wide=0, bad_q=0, bad_M=0, bad_count=0, errors=0, populated=0, negligible=0,
                 closed_q_lt_1=0, widest=-math.inf, largest_M=0.0, tightest_count=0.0)
    n_o = 4
    for rep in range(reps):
        n_i = int(rng.choice([2, 3, 4]))
        n = n_o + n_i
        p = float(rng.choice([0.05, 0.15, 0.3, 0.5, 0.7]))
        u = float(rng.choice([0.6, 1.0, 2.0]))
        ref = ["H", "zero", "H", round(float(rng.uniform(-u, u)), 3)][rep % 4] if refs is None else refs[rep % len(refs)]
        tab = tables(n_o, p, u, ref, mutation)
        pop, D = cube(n)
        kind = (6 + rep % 3) if lowK else rep % 9
        psi = make_instance(kind, n_o, n_i, p, u, tab, pop, D) + float(rng.uniform(-3, 3))
        assert (np.abs(psi[:, None] - psi[None, :]) <= u * D + 1e-9).all()
        popi = pop[: 2 ** n_i]
        pii = p ** popi * (1 - p) ** (n_i - popi)
        W = (np.exp(-psi).reshape(2 ** n_o, 2 ** n_i) * pii[None, :]).sum(axis=1)
        A = float((tab["pio"] * W).sum())
        What = W.copy() if mutation == "M3" else W / tab["wH"]
        psi_ref = float(psi[int(rng.integers(2 ** n))])
        s0 = math.exp(-psi_ref - u * n) / float(tab["wH"].max())
        if mutation != "M3":
            assert s0 <= What.min() * (1 + 1e-12)
        b = float(rng.choice([1.0, 2.0, 3.0])) if not lowK else float(rng.choice([3.0, 4.0]))
        G = b + float(rng.choice([0.3, 0.7, 1.5, 3.0]))
        K = 60 if lowK else math.ceil(24 * math.log(2 ** (n + 6) * n ** 3 / 0.05))
        c1 = math.log(1 / float(tab["muH"].min()))
        J = math.ceil(3 * u * n + b + c1 + 10)
        run = two_level(tab, What, s0, n, n_i, u, b, G, K, J, mode=rep % 3, mutation=mutation)
        stats["runs"] += 1
        if "error" in run:
            stats["errors"] += 1
            continue
        lowA, upA = tab["ZH"] * run["ell"], tab["ZH"] * run["upper"]
        if not (lowA <= A * (1 + 1e-12) and A <= upA * (1 + 1e-12)):
            stats["invalid"] += 1
            if verbose:
                print("   invalid bracket:", dict(kind=kind, p=p, u=u, n_i=n_i, low=lowA, A=A, up=upA, last=run["last"]))
            continue
        width = math.log(run["upper"] / run["ell"])
        stats["widest"] = max(stats["widest"], width - G - math.log(4 * math.e * J + 3))
        if width > G + math.log(4 * math.e * J + 3) + 1e-9:
            stats["too_wide"] += 1
        if mutation is not None:
            continue
        muH = tab["muH"]
        exceed = lambda thr: float(muH[What > thr].sum())
        qd = q_dagger(tab, math.exp(G - b) / 4)
        Mdag = 2 * K / qd
        seq = run["levels"] + [(run["last"][0], run["last"][1], run["last"][2], None, run["ell"])]
        for jj, (s, M, q, pop_, ell_in) in enumerate(seq):
            if exceed(s) > q + 1e-12:
                stats["bad_q"] += 1
            if M > 8 * J * math.e ** 2 * Mdag * (1 + 1e-9):
                stats["bad_M"] += 1
            stats["largest_M"] = max(stats["largest_M"], M / (8 * J * math.e ** 2 * Mdag))
            Mneg = 2 * K * J * math.e * s / (ell_in * math.exp(b))
            if M > max(K, 2 * Mneg):
                stats["bad_M"] += 1
            x = b
            while s * math.exp(-x) >= s0 * (1 - 1e-12):
                bound = 8 * K * J * math.e ** 2 * math.exp(x)
                lhs = Mneg * exceed(s * math.exp(-x))
                if lhs > bound * (1 + 1e-9):
                    stats["bad_count"] += 1
                stats["tightest_count"] = max(stats["tightest_count"], lhs / bound)
                x += 1.0
            if pop_ is not None:
                stats["populated" if pop_ else "negligible"] += 1
        if run["last"][2] < 1:
            stats["closed_q_lt_1"] += 1
    return stats


def run_negligible(reps=6):
    """engineered case in which a level is left as negligible: strong field (p = 0.09), steep envelope (u = 8),
    reference = zero residual (plain sampling of pi), instance = flat + the deepest dip at the outer point 1111
    (pi-measure 6.6e-5, excess 0.195), accuracy G - b = 0.02, so that the closure test fails down to the negligibility
    threshold while fewer than K sampled points are high; closure comes only when q < pi(1111) (about 2-4 million
    outer points)."""
    stats = dict(runs=0, invalid=0, too_wide=0, bad_q=0, bad_M=0, bad_count=0, errors=0, populated=0, negligible=0)
    n_o, n_i, p, u, b, K = 4, 2, 0.09, 8.0, 3.0, 60
    n = n_o + n_i
    tab = tables(n_o, p, u, "zero", None)
    pop, D = cube(n)
    No = 2 ** n_o
    Dset = tab["pop"] >= 4
    Do = tab["D"]
    low = (0.0 - u * Do[np.ix_(np.arange(No), ~Dset)]).max(axis=1)
    psi_o = np.where(Dset, low, 0.0)
    psi = psi_o[np.arange(2 ** n) >> n_i]
    assert (np.abs(psi[:, None] - psi[None, :]) <= u * D + 1e-9).all()
    popi = pop[: 2 ** n_i]
    pii = p ** popi * (1 - p) ** (n_i - popi)
    W = (np.exp(-psi).reshape(No, 2 ** n_i) * pii[None, :]).sum(axis=1)
    A = float((tab["pio"] * W).sum())
    G = b + 0.02
    c1 = math.log(1 / float(tab["muH"].min()))
    J = math.ceil(3 * u * n + b + c1 + 10)
    for rep in range(reps):
        s0 = math.exp(-0.0 - u * n) * math.exp(-float(rng.uniform(0.0, 0.9)))
        run = two_level(tab, W, s0, n, n_i, u, b, G, K, J, mode=rep % 3)
        stats["runs"] += 1
        if "error" in run:
            stats["errors"] += 1
            continue
        if not (run["ell"] <= A * (1 + 1e-12) and A <= run["upper"] * (1 + 1e-12)):
            stats["invalid"] += 1
            continue
        if math.log(run["upper"] / run["ell"]) > G + math.log(4 * math.e * J + 3) + 1e-9:
            stats["too_wide"] += 1
        exceed = lambda thr: float(tab["muH"][W > thr].sum())
        qd = q_dagger(tab, math.exp(G - b) / 4)
        Mdag = 2 * K / qd
        for (s, M, q, pop_, ell_in) in run["levels"] + [(run["last"][0], run["last"][1], run["last"][2], None, run["ell"])]:
            if exceed(s) > q + 1e-12:
                stats["bad_q"] += 1
            Mneg = 2 * K * J * math.e * s / (ell_in * math.exp(b))
            if M > 8 * J * math.e ** 2 * Mdag * (1 + 1e-9) or M > max(K, 2 * Mneg):
                stats["bad_M"] += 1
            x = b
            while s * math.exp(-x) >= s0 * (1 - 1e-12):
                if Mneg * exceed(s * math.exp(-x)) > 8 * K * J * math.e ** 2 * math.exp(x) * (1 + 1e-9):
                    stats["bad_count"] += 1
                x += 1.0
            if pop_ is not None:
                stats["populated" if pop_ else "negligible"] += 1
    return stats


if __name__ == "__main__":
    t0 = time.time()
    st = run_suite(None)
    print("correct algorithm, K of the proof, references H / zero / additive:", st)
    ok = st["invalid"] == 0 and st["too_wide"] == 0 and st["bad_q"] == 0 and st["bad_M"] == 0 and st["bad_count"] == 0 and st["errors"] == 0
    st2 = run_suite(None, lowK=True, refs=["zero", "H", "zero"])
    print("correct algorithm, K = 60 (events of the proof only with overwhelming probability), extremal instances:", st2)
    ok2 = st2["invalid"] == 0 and st2["too_wide"] == 0 and st2["bad_M"] == 0 and st2["bad_count"] == 0 and st2["errors"] == 0
    print("  -> all statements hold:", ok and ok2, "  (power: populated levels", st["populated"] + st2["populated"], ", negligible levels",
          st["negligible"] + st2["negligible"], ", closures with q < 1:", st["closed_q_lt_1"] + st2["closed_q_lt_1"], ")")
    st3 = run_negligible()
    print("engineered case with negligible levels (reference = zero residual, K = 60):", st3)
    print("  -> valid and within the bounds:", st3["invalid"] == 0 and st3["too_wide"] == 0 and st3["bad_M"] == 0 and st3["bad_count"] == 0 and st3["errors"] == 0,
          "; negligible levels:", st3["negligible"])
    for mut in ("M1", "M3"):
        sm = run_suite(mut, reps=max(REPS, 72))
        print(f"mutation {mut}: runs {sm['runs']}, invalid brackets {sm['invalid']}, too wide {sm['too_wide']}, errors {sm['errors']}")
    print("time %.0fs" % (time.time() - t0))
