#!/usr/bin/env python3
"""R15, Item 3 -- Proposition 11.113a of the theory report at f7df44f (the nested sampler): own replication on synthetic
boxes, written from the statement.  Nothing of the theory division's or the coordinator's code is imported.

Synthetic instance (mimics the anchored expansion, but everything is random numbers):
  product space of n sites with k_i states, reference state 0 at every site, S(x) = set of changed sites;
  A(x)   = sum_i a_i(x_i)                 additive "evaluated model" (a_i(0) = 0, a_i(s) > 0 random);
  c_T >= 0 on the m-subsets T;  env(x) = sum_{T subset S(x)} c_T   (the envelope: zero with fewer than m changed sites);
  gamma_i = (1/m) sum_{T contains i} c_T;  pen(x) = sum_{i in S(x)} gamma_i >= env(x)   (equal site shares);
  E = A + env * u,  u(x) in [-1, 1]       (the member; several kinds);
  inner sandwich e-/+ = A -/+ env;   outer sandwich m-/+ = A -/+ pen  (product models: exact Z, exact sampling).
PART 1  identities of (a), (b) by enumeration, incl. the rejection sampler of Proposition 11.113(b) and the product form
        of Z(m-/+).
PART 2  coverage of the bracket of (c) in R repetitions, under four sampling schemes
          A  N_f proposals i.i.d. q for the free means; N evaluated draws i.i.d. q_in, an independent stream;
          B  N_f proposals; each accepted with probability rho; ALL accepted are evaluated (N random);
          C  N_f proposals; each accepted with probability rho; the FIRST min(N_cap, #accepted) are evaluated;
          D  proposals until N are accepted (N fixed, N_f random) -- NOT covered by the proof; measured only;
        for four half-widths (in units of A = Z(m-) - Z(m+)):
          thy   2 t_f + rhobar t                      (the proposition)
          one   t_f (1 + |Wbar - 1/2| + t) + rhobar t  (the coordinator's variant, nested_sampler.py)
          two   t_f + rhobar t                         (this review: Hoeffding for beta and for beta + rho)
          nof   rhobar t                               (the free term dropped: must FAIL when N_f is small)
        t_f = sqrt(ln(6/delta)/(2 N_f)), t = sqrt(ln(6/delta)/(2 N)); and the plain sampler of Proposition 11.113(c) with
        the same number of evaluations, half-width sqrt(ln(2/delta)/(2 N)).
        Schemes A-C are simulated exactly through count vectors (multinomial / binomial / multivariate hypergeometric);
        one configuration is repeated with literal streams as a cross-check of that shortcut.
PART 3  when is the nested bound narrower than the plain one at equal N:  2 sqrt(N/N_f) + rhobar < kappa(delta),
        kappa = sqrt(ln(2/delta)/ln(6/delta)); checked on the simulated widths.

Run:  OMP_NUM_THREADS=1 python3 r15_item3_nested.py > logs/item3_nested.log
"""
import itertools, math, resource, sys, time
import numpy as np

t0 = time.time()
ok_all = True
REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 2000


def check(cond, msg):
    global ok_all
    if not cond:
        ok_all = False
        print("   !!! CHECK FAILED:", msg)


def build(seed, ks, m, a_lo, a_hi, c_scale, member):
    rng = np.random.default_rng(seed)
    n = len(ks)
    st = np.array(list(itertools.product(*[range(k) for k in ks])), dtype=np.int64)
    a = [np.concatenate([[0.0], rng.uniform(a_lo, a_hi, k - 1)]) for k in ks]
    A = sum(a[i][st[:, i]] for i in range(n))
    ch = (st != 0)
    subs = list(itertools.combinations(range(n), m))
    c = {T: (float(rng.exponential(c_scale)) if rng.random() < 0.8 else 0.0) for T in subs}
    env = np.zeros(len(st))
    for T, v in c.items():
        if v:
            env += v * ch[:, list(T)].all(axis=1)
    gamma = np.array([sum(v for T, v in c.items() if i in T) / m for i in range(n)])
    pen = ch @ gamma
    if member == "random":
        u = rng.uniform(-1, 1, len(st))
    elif member == "twolevel":
        u = rng.choice([-1.0, 1.0], len(st))
    elif member == "floor":
        u = -np.ones(len(st))
    elif member == "ceiling":
        u = np.ones(len(st))
    else:
        raise ValueError(member)
    E = A + env * u
    return dict(n=n, ks=ks, m=m, st=st, a=a, A=A, ch=ch, c=c, env=env, gamma=gamma, pen=pen, E=E, member=member, seed=seed)


def quantities(I):
    A_, env, pen, E = I["A"], I["env"], I["pen"], I["E"]
    ml, mu, el, eh = A_ - pen, A_ + pen, A_ - env, A_ + env
    check((ml <= el + 1e-12).all() and (el <= E + 1e-12).all() and (E <= eh + 1e-12).all() and (eh <= mu + 1e-12).all(),
          "nesting m- <= e- <= E <= e+ <= m+")
    wq = np.exp(-ml) - np.exp(-mu)
    Zlo, Zhi, ZE, Zel, Zeh = (float(np.exp(-v).sum()) for v in (ml, mu, E, el, eh))
    Aw = Zlo - Zhi
    q = wq / Aw
    pos = wq > 0
    beta = np.zeros_like(q); rho = np.zeros_like(q); W = np.zeros_like(q)
    beta[pos] = (np.exp(-eh[pos]) - np.exp(-mu[pos])) / wq[pos]
    rho[pos] = (np.exp(-el[pos]) - np.exp(-eh[pos])) / wq[pos]
    W[pos] = (np.exp(-E[pos]) - np.exp(-mu[pos])) / wq[pos]
    # rounding: where env = pen (e.g. all sites changed) rho is 1 up to one unit in the last place; clip, after checking
    check(beta.min() > -1e-12 and rho.min() > -1e-12 and rho.max() < 1 + 1e-12 and W.min() > -1e-12 and W.max() < 1 + 1e-12,
          "beta, rho or W outside [0, 1] by more than rounding")
    beta = np.clip(beta, 0.0, 1.0); rho = np.clip(rho, 0.0, 1.0); W = np.clip(W, 0.0, 1.0)
    inner = np.exp(-el) - np.exp(-eh)
    ipos = inner > 0
    Win = np.zeros_like(q)
    Win[ipos] = np.clip((np.exp(-E[ipos]) - np.exp(-eh[ipos])) / inner[ipos], 0.0, 1.0)
    return dict(ml=ml, mu=mu, el=el, eh=eh, q=q, beta=beta, rho=rho, W=W, Win=Win, inner=inner, ipos=ipos, pos=pos,
                Zlo=Zlo, Zhi=Zhi, ZE=ZE, Zel=Zel, Zeh=Zeh, Aw=Aw)


def part1(I, Q, label):
    q, beta, rho, W, Win = Q["q"], Q["beta"], Q["rho"], Q["W"], Q["Win"]
    tol = 1e-12
    r = dict()
    r["ranges"] = bool(beta.min() >= -tol and rho.min() >= -tol and (beta + rho).max() <= 1 + tol and Win.min() >= -tol
                       and Win.max() <= 1 + tol and W.min() >= -tol and W.max() <= 1 + tol)
    r["W=beta+rho*Win"] = float(np.abs(W - (beta + rho * Win))[Q["pos"]].max())
    r["Z(E)"] = abs(Q["Zhi"] + Q["Aw"] * float(q @ W) - Q["ZE"]) / Q["ZE"]
    r["Z(e+)"] = abs(Q["Zhi"] + Q["Aw"] * float(q @ beta) - Q["Zeh"]) / Q["Zeh"]
    r["Z(e-)-Z(e+)"] = abs(Q["Aw"] * float(q @ rho) - (Q["Zel"] - Q["Zeh"])) / Q["Zel"]
    Eqr = float(q @ rho)
    qin = q * rho / Eqr
    r["accepted law"] = float(np.abs(qin - Q["inner"] / (Q["Zel"] - Q["Zeh"])).max())
    r["Z(E) inner"] = abs(Q["Zeh"] + (Q["Zel"] - Q["Zeh"]) * float(qin @ Win) - Q["ZE"]) / Q["ZE"]
    r["E_q[rho Win]"] = abs(float(q @ (rho * Win)) - Eqr * float(qin @ Win))
    # Proposition 11.113(b): rejection from the Gibbs measure of m- with probability 1 - e^{-(m+ - m-)}
    pi_lo = np.exp(-Q["ml"]) / Q["Zlo"]
    acc = -np.expm1(-(Q["mu"] - Q["ml"]))
    rate = float(pi_lo @ acc)
    r["rejection law"] = float(np.abs(pi_lo * acc / rate - q).max())
    r["rejection rate"] = abs(rate - (1 - Q["Zhi"] / Q["Zlo"]))
    # product form of the outer partition functions (the outer models are solvable without enumeration)
    Zlo_prod = math.prod(float(np.exp(-(I["a"][i] - I["gamma"][i] * (np.arange(I["ks"][i]) > 0))).sum()) for i in range(I["n"]))
    Zhi_prod = math.prod(float(np.exp(-(I["a"][i] + I["gamma"][i] * (np.arange(I["ks"][i]) > 0))).sum()) for i in range(I["n"]))
    r["Z(m-) product"] = abs(Zlo_prod - Q["Zlo"]) / Q["Zlo"]
    r["Z(m+) product"] = abs(Zhi_prod - Q["Zhi"]) / Q["Zhi"]
    nch = I["ch"].sum(axis=1)
    r["rho=0 inside ball"] = bool((rho[nch < I["m"]] == 0).all())
    worst = max(v for k_, v in r.items() if not isinstance(v, bool))
    check(r["ranges"] and r["rho=0 inside ball"] and worst < 1e-9, f"identity failed on {label}: {r}")
    D_out = math.log(Q["Zlo"] / Q["Zhi"]); D_in = math.log(Q["Zel"] / Q["Zeh"])
    mu_in = float(qin @ Win)
    print(f"  [{label}] {len(q)} states; outer bracket of ln Z {D_out:.4f} nats, inner (envelope) {D_in:.4f}; E_q beta = {float(q @ beta):.5f}, "
          f"E_q rho = {Eqr:.5f}, E_in W_in = {mu_in:.4f}, E_q W = {float(q @ W):.5f}; max q = {q.max():.2e}; "
          f"sd_q(beta) {math.sqrt(float(q @ (beta - q @ beta) ** 2)):.3f}, sd_q(rho) {math.sqrt(float(q @ (rho - Eqr) ** 2)):.3f}, "
          f"sd_in(W_in) {math.sqrt(float(qin @ (Win - mu_in) ** 2)):.3f}")
    print(f"      identities: ranges {r['ranges']}; rho = 0 on all states with fewer than m changed sites {r['rho=0 inside ball']}; "
          f"largest error of the {len(r) - 2} numerical identities {worst:.1e}")
    return dict(Eqr=Eqr, qin=qin, mu_in=mu_in, EqW=float(q @ W), Eqb=float(q @ beta))


def halfwidths(bbar, rbar, wbar, Nf, N, delta):
    """the four half-widths in units of A; N may be an array (random), N = 0 handled (t = 1: W_in in [0,1])"""
    Lg = math.log(6 / delta)
    tf = np.sqrt(Lg / (2 * Nf))
    with np.errstate(divide="ignore"):
        t = np.where(N > 0, np.sqrt(Lg / (2 * np.maximum(N, 1))), 1.0)
    t = np.minimum(t, 1.0)
    return dict(thy=2 * tf + rbar * t, one=tf * (1 + np.abs(wbar - 0.5) + t) + rbar * t, two=tf + rbar * t, nof=rbar * t)


def simulate(Q, P1, scheme, Nf, N, delta, reps, rng, chunk=200):
    """returns per-repetition arrays: err (estimate - truth, units of A), the four half-widths, number of evaluations,
    and the plain sampler's error and half-width with the same number of evaluations"""
    q, beta, rho, Win, W = Q["q"], Q["beta"], Q["rho"], Q["Win"], Q["W"]
    qin = P1["qin"]
    truth = P1["EqW"]
    out = dict(err=[], n=[], perr=[], phw=[], Nf=[], rbar=[])
    hws = {k: [] for k in ("thy", "one", "two", "nof")}
    done = 0
    while done < reps:
        R = min(chunk, reps - done)
        if scheme in ("A", "B", "C"):
            cnt = rng.multinomial(Nf, q, size=R)                       # proposals by state
            bbar = cnt @ beta / Nf
            rbar = cnt @ rho / Nf
            Nf_arr = np.full(R, Nf)
            if scheme == "A":
                ev = rng.multinomial(N, qin, size=R)                   # an independent stream of accepted draws
                nev = np.full(R, N)
            else:
                acc = rng.binomial(cnt, rho[None, :])                  # accepted proposals by state
                if scheme == "B":
                    ev = acc
                else:
                    ev = np.empty_like(acc)
                    for j in range(R):                                 # the first N accepted: exchangeable => hypergeometric
                        tot = int(acc[j].sum())
                        ev[j] = acc[j] if tot <= N else rng.multivariate_hypergeometric(acc[j], N, method="marginals")
                nev = ev.sum(axis=1)
            wbar = np.where(nev > 0, ev @ Win / np.maximum(nev, 1), 0.5)
            # the plain sampler: nev evaluated draws of q (the first nev proposals; for scheme A an independent stream)
            pl = np.empty(R)
            for j in range(R):
                pl[j] = rng.multinomial(max(int(nev[j]), 1), q) @ W / max(int(nev[j]), 1)
        else:                                                          # scheme D: literal streams until N acceptances
            bbar = np.empty(R); rbar = np.empty(R); wbar = np.empty(R); Nf_arr = np.empty(R); nev = np.full(R, N); pl = np.empty(R)
            for j in range(R):
                xs = []; accs = []
                na = 0
                while na < N:
                    blk = rng.choice(len(q), size=max(64, int(2 * (N - na) / max(P1["Eqr"], 1e-3))), p=q)
                    ab = rng.random(len(blk)) < rho[blk]
                    if na + ab.sum() >= N:
                        last = np.flatnonzero(ab)[N - na - 1]
                        blk, ab = blk[:last + 1], ab[:last + 1]
                    xs.append(blk); accs.append(ab); na += int(ab.sum())
                xs = np.concatenate(xs); accs = np.concatenate(accs)
                bbar[j] = beta[xs].mean(); rbar[j] = rho[xs].mean(); wbar[j] = Win[xs[accs]].mean(); Nf_arr[j] = len(xs)
                pl[j] = W[rng.choice(len(q), size=N, p=q)].mean()
        est = bbar + rbar * wbar
        h = halfwidths(bbar, rbar, wbar, Nf_arr, nev, delta)
        out["err"].append(est - truth); out["n"].append(nev); out["Nf"].append(Nf_arr); out["rbar"].append(rbar)
        for k in hws:
            hws[k].append(h[k])
        out["perr"].append(pl - truth)
        out["phw"].append(np.sqrt(math.log(2 / delta) / (2 * np.maximum(nev, 1))))
        done += R
    res = {k: np.concatenate(v) for k, v in out.items()}
    res.update({k: np.concatenate(v) for k, v in hws.items()})
    return res


def report(tag, res, delta, sd_pred=None):
    err = np.abs(res["err"])
    s = f"   {tag}: evals {res['n'].mean():8.1f}"
    if sd_pred is not None:
        s += f" | sd(err) {res['err'].std():.5f} (predicted {sd_pred:.5f}), mean err {res['err'].mean():+.5f}"
    miss = {}
    for k in ("thy", "one", "two", "nof"):
        miss[k] = int((err > res[k] * (1 + 1e-12)).sum())
        s += f" | {k}: hw {res[k].mean():.5f}, miss {miss[k]:4d}, max|err|/hw {float((err / res[k]).max()):.2f}"
    pmiss = int((np.abs(res["perr"]) > res["phw"] * (1 + 1e-12)).sum())
    s += f" | plain: hw {res['phw'].mean():.5f}, miss {pmiss}"
    print(s)
    return miss, pmiss


# ---------------------------------------------------------------------------------------------------------------
print(f"R15 item 3: nested sampler, own replication; repetitions per configuration {REPS}")
print("PART 1  identities by enumeration")
INST = [
    ("I1 12 binary sites, mobile, random member", dict(seed=11, ks=(2,) * 12, m=3, a_lo=0.2, a_hi=1.5, c_scale=0.02, member="random")),
    ("I2 12 binary sites, nearly frozen, random member", dict(seed=12, ks=(2,) * 12, m=3, a_lo=1.5, a_hi=3.5, c_scale=0.03, member="random")),
    ("I3 8 ternary sites, two-level member", dict(seed=13, ks=(3,) * 8, m=3, a_lo=0.3, a_hi=2.0, c_scale=0.03, member="twolevel")),
    ("I4 12 binary sites, mobile, two-level member", dict(seed=14, ks=(2,) * 12, m=3, a_lo=0.2, a_hi=1.5, c_scale=0.02, member="twolevel")),
    ("I5 12 binary sites, member at the floor e-", dict(seed=15, ks=(2,) * 12, m=3, a_lo=0.2, a_hi=1.5, c_scale=0.02, member="floor")),
    ("I6 12 binary sites, member at the ceiling e+", dict(seed=16, ks=(2,) * 12, m=3, a_lo=0.2, a_hi=1.5, c_scale=0.02, member="ceiling")),
    ("I7 12 binary sites, m = 2, wide inner bracket", dict(seed=17, ks=(2,) * 12, m=2, a_lo=0.2, a_hi=1.0, c_scale=0.05, member="twolevel")),
]
built = []
for label, kw in INST:
    I = build(**kw)
    Q = quantities(I)
    P1 = part1(I, Q, label)
    built.append((label, I, Q, P1))

# ---------------------------------------------------------------------------------------------------------------
print("PART 2  coverage (half-widths and errors in units of A = Z(m-) - Z(m+); 'miss' = number of repetitions with the truth outside)")
rng = np.random.default_rng(20261126)
total = dict(thy=0, one=0, two=0, nof=0, plain=0, runs=0, nof_few=0, runs_few=0)
worst_ratio = dict(thy=0.0, one=0.0, two=0.0)
for delta in (0.05, 0.3):
    print(f" delta = {delta}: t_f, t with ln(6/delta) = {math.log(6 / delta):.4f}; plain with ln(2/delta) = {math.log(2 / delta):.4f}")
    for label, I, Q, P1 in built:
        rho0 = P1["Eqr"]
        N = 300
        bal = int(round(4 * N / rho0 ** 2))
        configs = [("A", max(50, int(N / rho0 / 4)), N), ("A", min(bal, 2_000_000), N), ("B", max(200, int(N / rho0)), None),
                   ("C", max(400, int(4 * N / rho0)), N), ("C", min(4 * bal, 4_000_000), N), ("A", 40, 2000)]
        print(f"  [{label}]  E_q rho = {rho0:.4f}; 4N/rho^2 = {bal}")
        for scheme, Nf, Nc in configs:
            res = simulate(Q, P1, scheme, Nf, Nc if Nc is not None else 0, delta, REPS, rng)
            # delta-method standard deviation of the estimate: Var_q(beta + rho mu)/N_f + (E rho)^2 Var_in(W_in)/N
            vfree = float(Q["q"] @ (Q["beta"] + Q["rho"] * P1["mu_in"] - (P1["Eqb"] + rho0 * P1["mu_in"])) ** 2)
            vin = float(P1["qin"] @ (Q["Win"] - P1["mu_in"]) ** 2)
            sd_pred = math.sqrt(vfree / Nf + rho0 ** 2 * vin / max(float(res["n"].mean()), 1.0))
            miss, pmiss = report(f"scheme {scheme}, N_f = {Nf:8d}, N {'= ' + str(Nc) if Nc is not None else 'random'}", res, delta, sd_pred)
            for k in ("thy", "one", "two", "nof"):
                total[k] += miss[k]
            total["plain"] += pmiss; total["runs"] += REPS
            for k in worst_ratio:
                worst_ratio[k] = max(worst_ratio[k], float((np.abs(res["err"]) / res[k]).max()))
            check(miss["thy"] <= delta * REPS and miss["one"] <= delta * REPS and miss["two"] <= delta * REPS,
                  f"coverage below 1 - delta: {label} {scheme} {Nf} {Nc} {miss}")
            if Nf == 40:
                total["nof_few"] += miss["nof"]; total["runs_few"] += REPS
print(f" totals over {total['runs']} runs: misses thy {total['thy']}, one {total['one']}, two {total['two']}, plain {total['plain']}; "
      f"without the free term {total['nof']} (of which {total['nof_few']} in the {total['runs_few']} runs with N_f = 40, N = 2000)")
print(f" largest |error|/half-width over all runs: thy {worst_ratio['thy']:.3f}, one {worst_ratio['one']:.3f}, two {worst_ratio['two']:.3f}")
check(total["nof_few"] > 0.3 * total["runs_few"], "the free term was never needed")

# cross-check of the count-vector shortcut against literal streams (scheme C), one configuration
label, I, Q, P1 = built[0]
q, beta, rho, Win = Q["q"], Q["beta"], Q["rho"], Q["Win"]
Nf, Ncap, delta = 4000, 300, 0.05
est_s = []
nev_s = []
for j in range(600):
    xs = rng.choice(len(q), size=Nf, p=q)
    acc = np.flatnonzero(rng.random(Nf) < rho[xs])[:Ncap]
    est_s.append(beta[xs].mean() + rho[xs].mean() * (Win[xs[acc]].mean() if len(acc) else 0.5)); nev_s.append(len(acc))
res = simulate(Q, P1, "C", Nf, Ncap, delta, 600, rng)
est_c = res["err"] + P1["EqW"]
print(f" cross-check streams vs counts (scheme C, {label}, N_f = {Nf}, cap {Ncap}, 600 runs each): mean estimate {np.mean(est_s):.6f} vs {est_c.mean():.6f} "
      f"(truth {P1['EqW']:.6f}); sd {np.std(est_s):.6f} vs {est_c.std():.6f}; mean evaluations {np.mean(nev_s):.1f} vs {res['n'].mean():.1f}")
se = math.sqrt(np.var(est_s) / 600 + est_c.var() / 600)
check(abs(np.mean(est_s) - est_c.mean()) < 4 * se and 0.8 < np.std(est_s) / est_c.std() < 1.25, "streams and counts disagree")

# scheme D: N fixed, N_f random (stop at the N-th acceptance): the free means are taken at a stopping time
print(" scheme D (proposals until N acceptances; N_f random -- not covered by the proof): bias of rhobar and coverage, delta = 0.05")
for label, I, Q, P1 in (built[0], built[1]):
    for N in (1, 3, 10, 100):
        res = simulate(Q, P1, "D", 0, N, 0.05, 1500, rng)
        err = np.abs(res["err"])
        print(f"   [{label[:2]}] N = {N:4d}: mean N_f {res['Nf'].mean():9.1f}; mean rhobar {res['rbar'].mean():.5f} against E_q rho {P1['Eqr']:.5f} "
              f"(relative bias {res['rbar'].mean() / P1['Eqr'] - 1:+.3f}); misses thy {int((err > res['thy']).sum())}, two {int((err > res['two']).sum())} of 1500")

# ---------------------------------------------------------------------------------------------------------------
print("PART 3  nested against plain at equal N: nested (thy) narrower iff 2 sqrt(N/N_f) + rhobar < kappa(delta); with the two-event form: sqrt(N/N_f) + rhobar < kappa")
for delta in (0.1, 0.05, 0.01, 0.001):
    kap = math.sqrt(math.log(2 / delta) / math.log(6 / delta))
    print(f"   delta = {delta}: kappa = {kap:.4f}; thy: needs rho < {kap:.4f} and N_f > 4N/(kappa - rho)^2 (N_f > {4 / kap ** 2:.2f} N as rho -> 0); "
          f"scheme B (N = rho N_f): rho < (sqrt(1 + kappa) - 1)^2 = {(math.sqrt(1 + kap) - 1) ** 2:.4f}; "
          f"two-event form in scheme B: rho < {((-1 + math.sqrt(1 + 4 * kap)) / 2) ** 2:.4f}")
delta = 0.05
kap = math.sqrt(math.log(2 / delta) / math.log(6 / delta))
agree = 0; tot = 0
for label, I, Q, P1 in built[:4]:
    rho0 = P1["Eqr"]
    for N in (100, 1000):
        for mult in (0.25, 0.8, 1.25, 4.0):
            if rho0 >= kap:
                continue
            Nf_star = 4 * N / (kap - rho0) ** 2
            Nf = int(round(mult * Nf_star))
            if Nf > 3_000_000 or Nf < N:
                continue
            res = simulate(Q, P1, "A", Nf, N, delta, 300, rng)
            nested, plain = float(res["thy"].mean()), float(res["phw"].mean())
            pred = (2 * math.sqrt(N / Nf) + rho0) < kap
            tot += 1; agree += int((nested < plain) == pred)
            print(f"   [{label[:2]}] rho = {rho0:.4f}, N = {N:5d}, N_f = {Nf:8d} = {mult:4.2f} x 4N/(kappa-rho)^2: nested {nested:.5f}, plain {plain:.5f} "
                  f"-> nested narrower: {nested < plain} (criterion: {pred})")
print(f"   criterion agreed with the simulated mean widths in {agree} of {tot} configurations")
check(agree == tot, "criterion for nested narrower than plain")
print("   arithmetic of (d): balance 2 t_f = rho t  <=>  N_f = 4 N / rho^2 ; two-event form: t_f = rho t  <=>  N_f = N / rho^2")

print("ALL CHECKS PASSED" if ok_all else "SOME CHECK FAILED")
print(f"seconds {time.time() - t0:.1f}")
print("peak RSS MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
