#!/usr/bin/env python3
"""A certified sandwich as a class of ensembles: the Ensemble division's threshold rule (ENSEMBLE-RES-0002 section 4 at
1a067b5) checked and run on our sandwiches; what their Theorem E13 says when the class is a sandwich; a stability bound.

Class.  Weights l <= w <= u on a finite X (l = e^{-m_+}, u = e^{-m_-} for a sandwich m_- <= E <= m_+); members mu ~ w.
(1) THRESHOLD RULE (theirs; "K: DeRobertis-Hartigan 1981" in their message, cited from memory there and here).  The largest
    mean of an observable psi over the class is the unique t with
          sum_x u(x) (psi(x) - t)_+  =  sum_x l(x) (psi(x) - t)_-          (weights u where psi > t, l where psi < t),
    attained by that "threshold member"; the smallest mean symmetrically.
(2) THE SANDWICH IS A FIRST-ORDER CLASS (ours, elementary).  With pi = sqrt(l u) and the "hub" metric
    d(x, y) = (D(x) + D(y)) / 2,  D = ln(u / l) = m_+ - m_-,  the class is exactly their
          P(pi, d) = { mu : mu(y) pi(x) <= e^{d(x,y)} mu(x) pi(y) }  --  so their Theorem E13 applies to it verbatim.
(3) STABILITY (ours, elementary).  With t* the upper end for f, mu_f the threshold member and gamma = min_x |f(x) - t*|:
          TV(mu, mu_f)  <=  (t* - E_mu f) / gamma        for every member mu;
    for a population f = 1_A:  TV(mu, mu_A) <= [mu_A(A) - mu(A)] / min(P, 1 - P),  P = mu_A(A).
(4) SANDWICH + DATA (ours, elementary; exact by LP duality).  For members with E_mu phi = m:  E_mu psi <= t whenever some
    lambda has  sum u (psi - t - lambda (phi - m))_+ <= sum l (psi - t - lambda (phi - m))_- ;  the least such t over lambda
    is the exact upper end of the identified set.

PART S (synthetic, exact):
  S1  (1) against brute force over the 2^N vertices of the box; control: l and u exchanged (must differ)
  S2  (2): max of random linear functionals over the polytope P(pi, d) by LP = the threshold value; members of the box
      satisfy the pair constraints; control: a weight vector outside the box by 1 % violates one
  S3  (3): max over the class of TV(mu, mu_f) - (t* - E_mu f) / gamma by LP over every subset (<= 0); for populations the
      best constant sup TV / Delta against 1 / min(P, 1 - P); control: half the constant (must fail)
  S4  (4): LP value with one datum against the least threshold value over lambda (must agree); soundness at random lambda
PART R (real sandwiches; argument "real"):
  R1  the law of the number of sites off the anchor under floor and ceiling by a transfer matrix WITH A COUNTER
      (count_law below: the model's own arrays, one message per count); validated on Val8/PPII by enumeration
  R2  the exact range of the mean number of sites off the anchor by (1), against the sum of the single-site intervals
      that addendum A17 (13) published -- Val8 (with the exact value), Val20/PPII at orders 4 and 5 (site, pair, triple form)
  R3  Lys5 (order 4, band 2; workstream P9's tables, the sandwich of first_order_recovery.py, by enumeration): the same,
      with the stability bound (3) evaluated at the true ensemble
Run: python3 -B sandwich_class.py synthetic > sandwich_class_synthetic.log
     python3 -B sandwich_class.py real      > sandwich_class_real.log
"""
import os, sys, io, math, time, itertools, contextlib
import numpy as np
from scipy.optimize import linprog, minimize_scalar
from scipy.special import logsumexp

HERE = os.path.dirname(os.path.abspath(__file__))


def log(s): print(s, flush=True)


# ------------------------------------------------------------------------------------------------ the rule
def upper_end(psi, u, l):
    """the unique t with sum u (psi - t)_+ = sum l (t - psi)_+ ; returns (t, weights of the threshold member)."""
    psi = np.asarray(psi, float); u = np.asarray(u, float); l = np.asarray(l, float)
    H = lambda t: float((u * np.clip(psi - t, 0, None)).sum() - (l * np.clip(t - psi, 0, None)).sum())
    vals = np.unique(psi)
    if len(vals) == 1: return float(vals[0]), u.copy()
    j = 0
    while j + 1 < len(vals) and H(vals[j + 1]) > 0: j += 1                    # H(vals[j]) > 0 >= H(vals[j+1]) (H decreases; H(min) > 0, H(max) < 0)
    up = psi > vals[j] + 0.0; dn = ~up                                        # above the root: psi >= vals[j+1]; below: psi <= vals[j]
    t = float(((u * psi)[up].sum() + (l * psi)[dn].sum()) / (u[up].sum() + l[dn].sum()))
    assert vals[j] - 1e-12 <= t <= vals[j + 1] + 1e-12 and abs(H(t)) <= 1e-9 * (u.sum() + l.sum()) * max(1.0, float(np.abs(psi).max()))
    return t, np.where(up, u, l)


def lower_end(psi, u, l):
    t, w = upper_end(-np.asarray(psi, float), u, l); return -t, w


def brute(psi, u, l):
    N = len(psi); best = (-1e300, 1e300)
    for bits in itertools.product((0, 1), repeat=N):
        w = np.where(np.array(bits) == 1, u, l); v = float((w * psi).sum() / w.sum()); best = (max(best[0], v), min(best[1], v))
    return best


def hub_polytope(u, l):
    N = len(u); pi = np.sqrt(u * l); D = np.log(u / l); rows = []
    for x in range(N):
        for y in range(N):
            if x != y:
                r = np.zeros(N); r[y] = pi[x]; r[x] = -math.exp(0.5 * (D[x] + D[y])) * pi[y]; rows.append(r)
    return np.array(rows)


def lp(c, A_ub, N, Aeq=None, beq=None):
    Ae = np.ones((1, N)) if Aeq is None else np.vstack([np.ones((1, N)), Aeq]); be = [1.0] if beq is None else [1.0] + list(beq)
    r = linprog(-np.asarray(c, float), A_ub=A_ub, b_ub=np.zeros(len(A_ub)), A_eq=Ae, b_eq=be, bounds=[(0, None)] * N, method="highs")
    return (None, None) if r.status == 2 else (-r.fun, r.x)


def part_s():
    t0 = time.time(); rng = np.random.default_rng(31415)
    log("=== PART S: the sandwich class on synthetic boxes (exact)")
    # ---- S1
    dev = 0.0; ctrl = 0; n1 = 0
    for N in (3, 5, 8, 10, 12):
        for rep in range(40 if N <= 10 else 8):
            l = rng.uniform(0.05, 1.0, N); u = l * np.exp(rng.uniform(0.0, 2.5, N)); psi = rng.normal(size=N) if rep % 3 else rng.integers(0, 4, N).astype(float)
            hi, _ = upper_end(psi, u, l); lo_, _ = lower_end(psi, u, l); b = brute(psi, u, l); n1 += 1
            dev = max(dev, abs(hi - b[0]), abs(lo_ - b[1]))
            # control: the rule with the roles of l and u exchanged solves a different equation
            H = float((l * np.clip(psi - hi, 0, None)).sum() - (u * np.clip(hi - psi, 0, None)).sum()); ctrl += int(abs(H) > 1e-6)
    log(f"S1  threshold rule against brute force over the vertices of the box: {n1} boxes of 3 to 12 states, both ends: largest deviation {dev:.1e} (must be < 1e-10); "
        f"control, the equation with l and u exchanged at the same t: not satisfied in {ctrl} of {n1} (must be nearly all)")
    assert dev < 1e-10 and ctrl > 0.9 * n1
    # ---- S2
    dev2 = 0.0; inside = 0; outside = 0; n2 = 0
    for N in (4, 6, 8):
        for rep in range(15):
            l = rng.uniform(0.05, 1.0, N); u = l * np.exp(rng.uniform(0.0, 2.0, N)); A = hub_polytope(u, l)
            for q in range(6):
                f = rng.normal(size=N); v, _ = lp(f, A, N); t, _ = upper_end(f, u, l); dev2 = max(dev2, abs(v - t)); n2 += 1
            w = l + (u - l) * rng.random(N); inside += int((A @ (w / w.sum()) <= 1e-12).all())
            # control: a vertex of the box with states at both bounds, one state at its upper bound pushed 1 % beyond: outside for EVERY scaling
            bits = rng.random(N) < 0.5; bits[0] = True; bits[1] = False; w2 = np.where(bits, u, l).astype(float); w2[0] = u[0] * 1.01
            outside += int((A @ (w2 / w2.sum()) > 1e-12).any())
    log(f"S2  the sandwich as the first-order class P(sqrt(l u), hub metric): max of {n2} random functionals over the polytope by LP against the threshold value: "
        f"largest deviation {dev2:.1e} (must be < 1e-8); random members of the box satisfy every pair constraint: {inside} of 45; "
        f"control, one weight 1 % beyond its bound with another state at the opposite bound: a pair constraint is violated in {outside} of 45 (must be all)")
    assert dev2 < 1e-8 and inside == 45 and outside == 45
    # ---- S3
    worst = -1e9; ratio_pop = []; n3 = 0
    for N in (4, 5, 6, 7):
        for rep in range(6):
            l = rng.uniform(0.05, 1.0, N); u = l * np.exp(rng.uniform(0.2, 2.0, N)); A = hub_polytope(u, l)
            f = rng.normal(size=N) if rep % 2 else (rng.random(N) < 0.5).astype(float)
            if len(np.unique(f)) == 1: f[0] = 1 - f[0]
            t, wf = upper_end(f, u, l); muf = wf / wf.sum(); gam = float(np.abs(f - t).min())
            if gam < 1e-6: continue
            n3 += 1
            for bits in range(1, 2 ** N - 1):
                iA = np.array([(bits >> j) & 1 for j in range(N)], dtype=float)
                # maximise mu(A) - mu_f(A) - (t - E_mu f) / gam   and the same with half the constant
                v, _ = lp(iA + f / gam, A, N); worst = max(worst, v - float(iA @ muf) - t / gam)
            if rep % 2 == 0:                                                   # population: best constant by Charnes-Cooper
                P = t; best = 0.0
                for bits in range(1, 2 ** N - 1):
                    iA = np.array([(bits >> j) & 1 for j in range(N)], dtype=float)
                    c = np.concatenate([-iA, [float(iA @ muf)]])               # maximise iA.y - mu_f(A) s  s.t.  P s - f.y = 1, sum y = s
                    Aeq = np.vstack([np.concatenate([-f, [P]]), np.concatenate([np.ones(N), [-1.0]])])
                    r = linprog(c, A_ub=np.hstack([A, np.zeros((len(A), 1))]), b_ub=np.zeros(len(A)), A_eq=Aeq, b_eq=[1.0, 0.0], bounds=[(0, None)] * (N + 1), method="highs")
                    if r.status == 0: best = max(best, -r.fun)
                ratio_pop.append(best * min(P, 1 - P))
    # the control with HALF the constant: maximise TV - 0.5 (t - E f)/gam  (it must be positive somewhere)
    half_fail = 0; nh = 0
    for N in (4, 5, 6):
        for rep in range(6):
            l = rng.uniform(0.05, 1.0, N); u = l * np.exp(rng.uniform(0.2, 2.0, N)); A = hub_polytope(u, l); f = (rng.random(N) < 0.5).astype(float)
            if len(np.unique(f)) == 1: f[0] = 1 - f[0]
            t, wf = upper_end(f, u, l); muf = wf / wf.sum(); gam = float(np.abs(f - t).min()); nh += 1; b = -1e9
            for bits in range(1, 2 ** N - 1):
                iA = np.array([(bits >> j) & 1 for j in range(N)], dtype=float); v, _ = lp(iA + 0.5 * f / gam, A, N); b = max(b, v - float(iA @ muf) - 0.5 * t / gam)
            half_fail += int(b > 1e-6)
    log(f"S3  stability: largest TV(mu, mu_f) - (t* - E_mu f) / gamma over the class, every subset, {n3} cases (random and indicator observables): {worst:+.2e} (must be <= 1e-9); "
        f"populations: sup TV / Delta times min(P, 1 - P): "
        f"{', '.join(f'{r:.3f}' for r in ratio_pop)} (the bound: <= 1); control, half the constant: violated in {half_fail} of {nh} cases (must be positive)")
    assert worst <= 1e-9 and max(ratio_pop) <= 1 + 1e-9 and half_fail > 0
    # ---- S4
    dev4 = 0.0; unsound = 0; n4 = 0; gain = []
    for N in (5, 7, 9):
        for rep in range(10):
            l = rng.uniform(0.05, 1.0, N); u = l * np.exp(rng.uniform(0.2, 2.0, N)); A = hub_polytope(u, l); psi = rng.normal(size=N); phi = rng.normal(size=N)
            w = l + (u - l) * rng.random(N); m = float((w * phi).sum() / w.sum())                       # a datum that some member satisfies
            v, _ = lp(psi, A, N, Aeq=phi[None, :], beq=[m]); assert v is not None
            tl = lambda lam: upper_end(psi - lam * (phi - m), u, l)[0]
            best = min(minimize_scalar(tl, bounds=(-50, 50), method="bounded", options=dict(xatol=1e-12)).fun, tl(0.0)); n4 += 1
            dev4 = max(dev4, abs(best - v)); gain.append((tl(0.0) - v) / max(tl(0.0) - lower_end(psi, u, l)[0], 1e-300))
            for lam in rng.normal(size=5) * 3: unsound += int(tl(lam) < v - 1e-9)
    log(f"S4  sandwich + one datum: least threshold value over the multiplier against the LP: largest deviation {dev4:.1e} over {n4} cases (must be < 1e-6); "
        f"a threshold value below the LP at a random multiplier: {unsound} of {5 * n4} (must be 0); the datum removes {np.median(gain):.2f} (median) of the width of the box's range from above")
    assert dev4 < 1e-6 and unsound == 0
    log(f"PART S DONE {time.time() - t0:.0f} s")


# ------------------------------------------------------------------------------------------------ PART R
def count_law(model, anchor, beta):
    """ln sum over the states with exactly c sites off the anchor of exp(-beta model(x)), c = 0..n: the model's own
    transfer matrix (its arrays _A), one message per count."""
    n = model.n; msgs = {0: None}
    for i in range(n):
        new = {}
        for c, msg in msgs.items():
            A = model._A(i, msg, -beta); on = A[anchor[i]]; rest = [b for b in range(model.k[i]) if b != anchor[i]]
            cand = [(c, on)]
            if rest: cand.append((c + 1, logsumexp(A[rest], axis=0)))
            for c2, arr in cand: new[c2] = arr if c2 not in new else np.logaddexp(new[c2], arr)
        msgs = new
    return np.array([float(msgs[c]) - beta * model.const if c in msgs else -np.inf for c in range(n + 1)])


def site_sum_interval(lo, up, x0, beta):
    """the sum over the sites of the exact single-site intervals of P(x_i != a_i) -- what A17 (13) published"""
    BIG = 1.0e5; a = b = 0.0
    for i in range(lo.n):
        if lo.k[i] == 1: continue
        z = {}
        for nm, mdl in (("lo", lo), ("up", up)):
            old = mdl.one[i]; pen = np.full(len(old), BIG); pen[x0[i]] = 0.0; mdl.one[i] = old + pen; on = mdl.lnZ(beta)
            pen = np.zeros(len(old)); pen[x0[i]] = BIG; mdl.one[i] = old + pen; off = mdl.lnZ(beta); mdl.one[i] = old; z[nm] = (on, off)
        # P(off) in [ Z+(off) / (Z+(off) + Z-(on)),  Z-(off) / (Z-(off) + Z+(on)) ]
        a += 1.0 / (1.0 + math.exp(z["lo"][0] - z["up"][1])); b += 1.0 / (1.0 + math.exp(z["up"][0] - z["lo"][1]))
    return a, b


def count_range(lzl, lzu):
    """exact range of the mean count over the sandwich from the two laws (ln Z-_c of the floor, ln Z+_c of the ceiling)"""
    sh = max(lzl.max(), lzu.max()); u = np.exp(lzl - sh); l = np.exp(lzu - sh); c = np.arange(len(u), dtype=float)
    assert (u >= l * (1 - 1e-9)).all(), "the floor's sum must dominate the ceiling's at every count"
    return lower_end(c, u, l)[0], upper_end(c, u, l)[0]


def part_r():
    P6 = os.path.normpath(os.path.join(HERE, "..", "ws_P6")); PI = os.path.normpath(os.path.join(HERE, "..", "pi_inference"))
    sys.path.insert(0, P6); sys.path.insert(0, PI)
    import p6lib as L
    pw = L.pw; BETA = L.BETA; t0 = time.time()
    log("=== PART R: real sandwiches (workstreams P3, P6, P9); model-relative, as everything in addendum A17")

    def triple(seq, bb, tau, m, w, sd):                    # as in certified_populations.triple_models (the coordinator's; P6's functions are called, not copied)
        import importlib
        T9 = importlib.import_module("p6_09_triple"); G, c0, h, J, x0, E0 = sd; n, k = G.ns, G.k
        GF = L.GFBound2(G, x0, L.EnvelopeSup(G), K=m); fn = os.path.join(P6, "out", f"pairsums_{L.tagname(seq, bb, tau)}_m{m}.npz")
        if not os.path.exists(fn): return None
        z = np.load(fn)
        if list(z["anchor"]) != list(x0) or not np.isfinite(z["G"][~np.eye(n, dtype=bool)]).all(): return None
        Gam, S, Gp = float(z["Gamma"]), z["S"], z["G"]; val = {tuple(int(v) for v in e if v >= 0): float(t) for e, t in zip(z["excl"], z["tot"])}
        tris = T9.window_triples(n, w); se, cr = L.GFBatch(GF).totals(m, tris)
        H = {tr: (val[()] - val[(tr[0],)] - val[(tr[1],)] - val[(tr[2],)] + val[(tr[0], tr[1])] + val[(tr[0], tr[2])] + val[(tr[1], tr[2])]) - float(t3) for tr, t3 in zip(tris, se + cr)}
        d, nball, srcb = L.ball_terms(G, x0, m - 1, seq, bb, tau, verbose=False); phi1, psi1, psi2 = L.fp_tables(n, k, x0, m - 1)
        gsT, g2T, eta = T9.triple_form(n, m, w, Gp, H, psi1, psi2, 5e-9 * Gam, 1e-8 * Gam)
        lo, up = T9.build_triple_models(k, x0, c0, h, J, d, w, m - 1, gsT, g2T, eta); return lo, up

    def line(tag, lo, up, x0, exact=None):
        t1 = time.time(); lzl = count_law(lo, x0, BETA); lzu = count_law(up, x0, BETA)
        defect = max(abs(logsumexp(lzl) - lo.lnZ(BETA)), abs(logsumexp(lzu) - up.lnZ(BETA)))
        a, b = site_sum_interval(lo, up, x0, BETA); tl, th = count_range(lzl, lzu)
        s = (f"  {tag}: ln Z width {lo.lnZ(BETA) - up.lnZ(BETA):.3g}; sum of the single-site intervals [{a:.5f}, {b:.5f}] (width {b - a:.3g}); "
             f"**exact range over the sandwich [{tl:.5f}, {th:.5f}] (width {th - tl:.3g})**: narrower by a factor **{(b - a) / (th - tl):.2f}**; "
             f"the counts of the two laws sum to the models' ln Z within {defect:.1e}")
        if exact is not None: s += f"; exact value {exact:.5f}: inside both: {a <= exact <= b and tl <= exact <= th}"
        log(s + f" [{time.time() - t1:.1f}s]")
        assert defect < 1e-8 and a - 1e-9 <= tl and th <= b + 1e-9
        return (b - a) / (th - tl)

    # ---- R1/R2: Val8 on PPII by enumeration
    seq, bb, tau = "V8", "P2", 0.70; sd = L.setup(seq, bb, tau); G, c0, h, J, x0, E0 = sd; x0 = [int(v) for v in x0]; w = min(8, G.ns - 1)
    st, g, src = L.enumerate_g(G, seq, bb, tau, verbose=False); E = pw.f_energy(st, c0, h, J) + g; p = np.exp(-BETA * (E - E.min())); p /= p.sum()
    cnt = (st != np.array(x0)[None]).sum(axis=1); ex = float((p * cnt).sum())
    log(f"R1  {seq}/{bb}: {len(st)} states enumerated; exact mean number of sites off the anchor {ex:.5f}")
    for m in (3, 4):
        for form in ("S", "B"):
            try: lo, up, info = L.make_models(seq, bb, tau, m, w, form, setup_data=sd)
            except Exception as e: log(f"  order {m} form {form}: not available ({type(e).__name__})"); continue
            ml, mu = lo.energy(st), up.energy(st); assert int((ml > E + 1e-9).sum() + (mu < E - 1e-9).sum()) == 0
            # the counter pass against enumeration
            for mdl, en in ((lo, ml), (up, mu)):
                law = count_law(mdl, x0, BETA); ref = np.array([logsumexp(-BETA * en[cnt == c]) if (cnt == c).any() else -np.inf for c in range(G.ns + 1)])
                assert np.abs(law - ref)[np.isfinite(ref)].max() < 1e-9, "counter pass against enumeration"
            # the exact range by enumeration with the rule applied to the states themselves
            sh = (-BETA * ml).max(); u = np.exp(-BETA * ml - sh); l = np.exp(-BETA * mu - sh); th2 = upper_end(cnt.astype(float), u, l)[0]; tl2 = lower_end(cnt.astype(float), u, l)[0]
            f = line(f"{seq}/{bb} order {m} form {form}", lo, up, x0, exact=ex)
            tl, th = count_range(count_law(lo, x0, BETA), count_law(up, x0, BETA)); assert abs(tl - tl2) < 1e-9 and abs(th - th2) < 1e-9
    log("    (the counter pass equals enumeration to 1e-9 for both models of every case; the rule on the law of the count equals the rule on the states)")
    # ---- R2: Val20 on PPII
    seq, bb, tau = "V20", "P2", 0.70; sd = L.setup(seq, bb, tau); G, c0, h, J, x0, E0 = sd; x0 = [int(v) for v in x0]
    log(f"R2  {seq}/{bb}: {G.ns} sites, 10^{sum(math.log10(k) for k in G.k):.2f} assignments (no enumeration)")
    for m in (4, 5):
        for form in ("S", "B"):
            lo, up, info = L.make_models(seq, bb, tau, m, 8, form, setup_data=sd); line(f"{seq}/{bb} order {m} form {form}", lo, up, x0)
        tm = triple(seq, bb, tau, m, 8, sd)
        if tm is not None: line(f"{seq}/{bb} order {m} form T", tm[0], tm[1], x0)
    # ---- R3: Lys5, the sandwich of first_order_recovery.py, by enumeration (its locals are taken from its frame)
    import first_order_recovery as FR
    got = {}

    def prof(frame, event, arg):
        if event == "return" and frame.f_code is FR.main.__code__: got.update(frame.f_locals)
    old = sys.argv; sys.argv = ["first_order_recovery.py", "K5", "4", "2", "--enum"]; buf = io.StringIO(); sys.setprofile(prof)
    try:
        with contextlib.redirect_stdout(buf): FR.main()
    finally:
        sys.setprofile(None); sys.argv = old
    st, EE, eu, el, x0 = got["st"], got["EE"], got["eu"], got["el"], np.array(got["x0"]); B2 = FR.BETA
    assert int((el > EE + 1e-9).sum() + (eu < EE - 1e-9).sum()) == 0
    cnt = (st != x0[None]).sum(axis=1).astype(float); p = np.exp(-B2 * (EE - EE.min())); p /= p.sum(); ex = float((p * cnt).sum())
    sh = (-B2 * el).max(); u = np.exp(-B2 * el - sh); l = np.exp(-B2 * eu - sh); th, wth = upper_end(cnt, u, l); tl, wtl = lower_end(cnt, u, l)
    a = b = 0.0
    for i in range(st.shape[1]):
        off = st[:, i] != x0[i]; a += l[off].sum() / (l[off].sum() + u[~off].sum()); b += u[off].sum() / (u[off].sum() + l[~off].sum())
    D = B2 * (eu - el)
    log(f"R3  Lys5, order 4, band 2 (the sandwich of first_order_recovery.py; ln Z width {math.log(u.sum() / l.sum()):.4g}; D(x) = beta (m_+ - m_-): max {D.max():.3g}, Gibbs mean {float((p * D).sum()):.3g}): "
        f"exact mean number of sites off the anchor {ex:.5f}; sum of the single-site intervals [{a:.5f}, {b:.5f}] (width {b - a:.3g}); "
        f"**exact range over the sandwich [{tl:.5f}, {th:.5f}] (width {th - tl:.3g})**: narrower by a factor **{(b - a) / (th - tl):.2f}**; the exact value inside both: {a <= ex <= b and tl <= ex <= th}")
    for nm, t, wv, sgn in (("upper", th, wth, 1.0), ("lower", tl, wtl, -1.0)):
        muf = wv / wv.sum(); TV = 0.5 * float(np.abs(p - muf).sum()); gam = float(np.abs(cnt - t).min()); bound = sgn * (t - ex) / gam
        log(f"    stability (3) at the true ensemble, {nm} end: TV(mu, threshold member) = {TV:.4g} <= (distance of the mean from the end) / gamma = {abs(t - ex):.4g} / {gam:.4g} = {bound:.4g}: {TV <= bound + 1e-12}")
        assert TV <= bound + 1e-12
    log(f"PART R DONE {time.time() - t0:.0f} s")


if __name__ == "__main__":
    part_s() if sys.argv[1] == "synthetic" else part_r()
