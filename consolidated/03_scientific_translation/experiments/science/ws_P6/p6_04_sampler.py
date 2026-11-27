"""
P6 item 7 (added by the coordinator): the SANDWICH SAMPLER of the theory division (their Proposition 11.113,
THY-RES-0010 section 3; read at theory commit 9408e33) on P3's certified sandwich and on its banded pair form.

For m_- <= E <= m_+ (a = beta m_-, b = beta m_+, e = beta E):
    q(x) ~ exp(-a) - exp(-b),   W(x) = (exp(-e) - exp(-b)) / (exp(-a) - exp(-b)) in [0, 1],
    Z(E) = Z(m_+) + (Z(m_-) - Z(m_+)) E_q[W].
q = law of a draw x ~ pi_{m_-} (exact transfer-matrix sampler of P3) accepted with probability 1 - exp(-(b - a)(x)).
Only accepted points are evaluated.  Hoeffding on [0, 1]: |mean W - E_q W| <= sqrt(ln(2/delta)/(2N)) w.p. >= 1 - delta.

Rounding of an evaluated energy: with r = beta(E - m_-), U = beta(m_+ - m_-), |dW/dr| <= 1/(1 - exp(-U)); every
evaluated W_i is replaced by the interval W_i -/+ beta*EPS_G/(1 - exp(-U_i)) clipped to [0, 1] (EPS_G = P3's
allowance for one evaluated value of g); the Hoeffding interval is taken around the means of the two ends.

modes:
  python3 -B p6_04_sampler.py SEQ BB TAU m FORM w --enumcheck [--reps 400] [--N 1200]     (enumerable instance)
  python3 -B p6_04_sampler.py SEQ BB TAU m FORM w --N 50000 [--N1 1200] [--seed S]        (evaluation at accepted points)
FORM: S (site form, P3) or B (banded pair form).
"""
import sys, os, time, math, json
import numpy as np
import p6lib as L
pw = L.pw
BETA = L.BETA


def opt(a, key, default, cast=str):
    return cast(a[a.index(key) + 1]) if key in a else default


def propose_accept(lo, diff, N, rng, batch):
    """N accepted draws of q by rejection from pi_{m_-}.  Returns (states (N, n), U = beta(m_+ - m_-) at them,
    number of proposals up to and including the one that gave the N-th acceptance)."""
    out = []; outU = []; got = 0; nprop = 0
    while got < N:
        S = lo.sample(batch, rng)
        U = BETA * diff.energy(S)
        acc = rng.random(batch) < -np.expm1(-U)
        idx = np.flatnonzero(acc)
        if got + len(idx) >= N:
            idx = idx[:N - got]
            nprop += int(idx[-1]) + 1
        else:
            nprop += batch
        out.append(S[idx]); outU.append(U[idx]); got += len(idx)
    return np.concatenate(out), np.concatenate(outU), nprop


def w_values(r, U):
    """W = (e^-r - e^-U)/(1 - e^-U) = e^-r * expm1(-(U - r)) / expm1(-U), and the rounding half-width for E."""
    W = np.exp(-r) * np.expm1(-(U - r)) / np.expm1(-U)
    dW = BETA * (L.EPS_G + 1e-10) / (-np.expm1(-U))
    return W, dW


def bracket(W, dW, lnZlo, lnZup, delta):
    """certified bracket of ln Z(E) from the accepted evaluations (Hoeffding on [0,1], rounding intervals)."""
    N = len(W)
    t = math.sqrt(math.log(2.0 / delta) / (2.0 * N))
    Wl = max(0.0, float(np.clip(W - dW, 0.0, 1.0).mean()) - t)
    Wh = min(1.0, float(np.clip(W + dW, 0.0, 1.0).mean()) + t)
    D = lnZlo - lnZup
    eD = math.expm1(D)
    return lnZup + math.log1p(eD * Wl), lnZup + math.log1p(eD * Wh), t, lnZup + math.log1p(eD * float(np.clip(W, 0, 1).mean()))


def eb_bracket(W, dW, lnZlo, lnZup, delta):
    """NOT used for any certified statement: the same bracket with an empirical Bernstein half-width in the form
    sqrt(2 V ln(4/delta)/N) + 7 ln(4/delta)/(3(N-1))  (V = sample variance; two-sided; the inequality of Maurer and
    Pontil for variables in [0, 1], QUOTED FROM MEMORY, not checked against the source)."""
    N = len(W)
    V = float(np.clip(W, 0.0, 1.0).var(ddof=1)); L4 = math.log(4.0 / delta)
    t = math.sqrt(2.0 * V * L4 / N) + 7.0 * L4 / (3.0 * (N - 1))
    Wl = max(0.0, float(np.clip(W - dW, 0.0, 1.0).mean()) - t)
    Wh = min(1.0, float(np.clip(W + dW, 0.0, 1.0).mean()) + t)
    eD = math.expm1(lnZlo - lnZup)
    return lnZup + math.log1p(eD * Wl), lnZup + math.log1p(eD * Wh), t


def main():
    a = sys.argv[1:]
    seq, bb, tau, m, form, w = a[0], a[1], float(a[2]), int(a[3]), a[4], int(a[5])
    delta = opt(a, "--delta", 0.05, float)
    seed = opt(a, "--seed", 2026112600 + 10 * m + (1 if form == "B" else 0), int)
    t0 = time.time()
    lo, up, info = L.make_models(seq, bb, tau, m, w, form)
    G, c0, h, J, x0, E0 = info["setup"]
    n, k = G.ns, G.k
    lnZlo, lnZup = lo.lnZ(), up.lnZ()
    D = lnZlo - lnZup
    diff = L.diff_model(lo, up)
    acc_rate = -math.expm1(-D)
    print(f"=== sandwich sampler (theory division, Prop. 11.113): {seq} on {bb}, tau {tau}, m = {m}, form {form}, band {w}; ball {info['nball']} values; "
          f"ln Z(m_-) = {lnZlo:.6f}, ln Z(m_+) = {lnZup:.6f}, deterministic width D = {D:.6f} nats; exact acceptance rate 1 - e^-D = {acc_rate:.5f}; "
          f"seed {seed}; delta {delta} [{time.time() - t0:.1f}s]", flush=True)
    res = dict(seq=seq, bb=bb, tau=tau, m=m, form=form, w=w, seed=seed, delta=delta, lnZ_lo=lnZlo, lnZ_up=lnZup, D=D, acc_rate_exact=acc_rate,
               nball=info["nball"])
    rng = np.random.default_rng(seed)
    batch = int(min(400000, max(20000, 2000 / max(acc_rate, 1e-6))))
    tagf = f"{L.tagname(seq, bb, tau)}_m{m}_{form}_w{w}"
    if "--enumcheck" in a:
        reps = opt(a, "--reps", 400, int); N = opt(a, "--N", 1200, int)
        st, g, src = L.enumerate_g(G, seq, bb, tau)
        E = pw.f_energy(st, c0, h, J) + g
        ml, mu = lo.energy(st), up.energy(st)
        Emin = E.min()
        lnZE = float(np.log(np.exp(-BETA * (E - Emin)).sum()) - BETA * Emin)
        r = BETA * (E - ml); U = BETA * (mu - ml)
        pos = U > 0
        W, dW = w_values(r[pos], U[pos])
        # exact identity: q, E_q W, Z(E) = Z+ + (Z- - Z+) E_q W
        qw = np.exp(-BETA * (ml[pos] - Emin)) * (-np.expm1(-U[pos]))
        q = qw / qw.sum()
        EqW = float((q * W).sum())
        lnZ_id = lnZup + math.log1p(math.expm1(D) * EqW)
        acc_enum = float(qw.sum() / np.exp(-BETA * (ml - Emin)).sum())
        res.update(enum=dict(states=int(len(st)), W_min=float(W.min()), W_max=float(W.max()), n_outside=int(((W < 0) | (W > 1)).sum()),
                             n_zero_width=int((~pos).sum()), EqW=EqW, lnZ_E=lnZE, lnZ_identity=lnZ_id, identity_dev=abs(lnZ_id - lnZE),
                             acc_rate_enum=acc_enum))
        print(f"    ENUMERATION ({len(st)} states): W in [{W.min():.6g}, {W.max():.6g}], states with W outside [0, 1]: {int(((W < 0) | (W > 1)).sum())} "
              f"(states with m_+ = m_-: {int((~pos).sum())}); exact E_q W = {EqW:.8f}; identity: ln[Z(m_+) + (Z(m_-) - Z(m_+)) E_q W] = {lnZ_id:.10f}, "
              f"ln Z(E) = {lnZE:.10f}, difference {abs(lnZ_id - lnZE):.1e}; acceptance rate: enumerated {acc_enum:.6f}, 1 - e^-D = {acc_rate:.6f}", flush=True)
        # coverage over `reps` repetitions of the actual algorithm (rejection from the transfer-matrix sampler)
        idx_of = lambda S: np.ravel_multi_index(tuple(S.T), k)
        inside = 0; widths = []; errs = []; props = []; wout = 0
        t1 = time.time()
        for rep in range(reps):
            S, Us, nprop = propose_accept(lo, diff, N, rng, batch)
            ii = idx_of(S)
            Wi, dWi = w_values(BETA * (E[ii] - ml[ii]), BETA * (mu[ii] - ml[ii]))
            wout += int(((Wi < 0) | (Wi > 1)).sum())
            b0, b1, t, pt = bracket(Wi, dWi, lnZlo, lnZup, delta)
            inside += int(b0 <= lnZE <= b1); widths.append(b1 - b0); errs.append(pt - lnZE); props.append(nprop)
        errs = np.array(errs)
        res.update(coverage=dict(reps=reps, N=N, inside=inside, mean_width=float(np.mean(widths)), rms_err=float(np.sqrt((errs ** 2).mean())),
                                 max_abs_err=float(np.abs(errs).max()), mean_proposals=float(np.mean(props)), emp_acc=float(N / np.mean(props)),
                                 W_outside=wout))
        print(f"    COVERAGE: {reps} repetitions with N = {N} accepted evaluations each [{time.time() - t1:.1f}s]: truth inside the bracket in {inside} of {reps}; "
              f"mean bracket width {np.mean(widths):.3e} nats (deterministic {D:.3e}); point estimate: rms error {np.sqrt((errs ** 2).mean()):.2e}, max |error| {np.abs(errs).max():.2e}; "
              f"mean proposals {np.mean(props):.0f} (empirical acceptance {N / np.mean(props):.5f}); sampled W outside [0,1]: {wout}", flush=True)
        fn = os.path.join(L.HERE, "out", f"sampler_enum_{tagf}.json")
    else:
        N = opt(a, "--N", 50000, int); N1 = opt(a, "--N1", 1200, int)
        t1 = time.time()
        S, U, nprop = propose_accept(lo, diff, N, rng, batch)
        t_prop = time.time() - t1
        uniq, inv = np.unique(S, axis=0, return_inverse=True)
        inv = np.asarray(inv).reshape(-1)
        print(f"    {N} accepted of {nprop} proposals (empirical acceptance {N / nprop:.5f}; exact {acc_rate:.5f}) [{t_prop:.1f}s]; {len(uniq)} distinct states to evaluate; "
              f"mean number of sites off the anchor among accepted points {float((S != np.array(x0)[None]).sum(1).mean()):.2f}", flush=True)
        t1 = time.time()
        # values of g already on disk are not evaluated again: P3's / my ball caches and the caches of earlier sampler runs
        import glob
        known = {}
        tg = L.tagname(seq, bb, tau)
        for cf in sorted(glob.glob(os.path.join(L.P3, "cache", f"ball_{tg}_M*.npz")) + glob.glob(os.path.join(L.MYCACHE, f"ball_{tg}_M*.npz"))
                         + glob.glob(os.path.join(L.MYCACHE, f"evalcache_{tg}_*.npz"))):
            z = np.load(cf)
            for row, v in zip(z["states"].astype(np.int8), z["vals"]):
                known[row.tobytes()] = float(v)
        u8 = uniq.astype(np.int8)
        gU = np.array([known.get(row.tobytes(), np.nan) for row in u8])
        todo = np.flatnonzero(np.isnan(gU))
        print(f"      {len(uniq) - len(todo)} of the {len(uniq)} distinct states already have a value of g on disk (ball caches, earlier runs); {len(todo)} new evaluations", flush=True)
        for s in range(0, len(todo), 4096):
            ii = todo[s:s + 4096]
            gU[ii] = G.bulk_energy(uniq[ii])
            if (s // 4096) % 3 == 0:
                print(f"      evaluations {min(len(todo), s + 4096)}/{len(todo)}  {time.time() - t1:.0f}s", flush=True)
        if len(todo):
            np.savez(os.path.join(L.MYCACHE, f"evalcache_{tg}_m{m}_{form}_w{w}_seed{seed}.npz"), states=u8[todo], vals=gU[todo])
        res_new_evals = int(len(todo))
        chk = np.random.default_rng(seed + 7).integers(0, len(uniq), 24)
        dev = float(np.abs(gU[chk] - G.energy(uniq[chk])).max())
        assert dev < 1e-8, dev
        EU = pw.f_energy(uniq, c0, h, J) + gU
        ES = EU[inv]
        t_eval = time.time() - t1
        mlS, muS = lo.energy(S), up.energy(S)
        r = BETA * (ES - mlS); Us = BETA * (muS - mlS)
        viol_lo = int((ES < mlS - 1e-9).sum()); viol_up = int((ES > muS + 1e-9).sum())
        W, dW = w_values(r, Us)
        res.update(N=N, proposals=nprop, emp_acc=N / nprop, distinct=int(len(uniq)), new_evals=res_new_evals, t_prop=t_prop, t_eval=t_eval, bulk_vs_own=dev,
                   sandwich_checks=2 * N, viol_lower=viol_lo, viol_upper=viol_up, W_min=float(W.min()), W_max=float(W.max()),
                   W_outside=int(((W < 0) | (W > 1)).sum()), dW_mean=float(dW.mean()), brackets={})
        print(f"    E evaluated at the accepted points [{t_eval:.1f}s]; m_- <= E <= m_+ at all {N} accepted points: violations below {viol_lo}, above {viol_up}; "
              f"W in [{W.min():.6f}, {W.max():.6f}] (outside [0,1]: {res['W_outside']}); mean rounding half-width of W {dW.mean():.1e}", flush=True)
        for NN in sorted({min(N1, N), N}):
            b0, b1, t, pt = bracket(W[:NN], dW[:NN], lnZlo, lnZup, delta)
            res["brackets"][str(NN)] = dict(lo=b0, hi=b1, width=b1 - b0, t=t, point=pt, Wmean=float(W[:NN].mean()), Wstd=float(W[:NN].std(ddof=1)),
                                            predicted_width_bound=math.expm1(D) * 2 * t)
            print(f"    N = {NN:6d} (the first {NN} accepted points): mean W = {W[:NN].mean():.6f} (std {W[:NN].std(ddof=1):.4f}); Hoeffding half-width t = {t:.6f}; "
                  f"CERTIFIED (prob. >= {1 - delta}): ln Z(E) in [{b0:.6f}, {b1:.6f}], width {b1 - b0:.3e} nats (bound (e^D - 1) 2t = {math.expm1(D) * 2 * t:.3e}); "
                  f"point estimate {pt:.6f}", flush=True)
            e0, e1, te = eb_bracket(W[:NN], dW[:NN], lnZlo, lnZup, delta)
            res["brackets"][str(NN)].update(eb_lo=e0, eb_hi=e1, eb_t=te)
            print(f"               [not certified here -- empirical Bernstein half-width (formula quoted from memory) t_EB = {te:.6f}: "
                  f"ln Z(E) in [{e0:.6f}, {e1:.6f}], width {e1 - e0:.3e}]", flush=True)
        np.savez(os.path.join(L.HERE, "out", f"sampler_{tagf}.npz"), states=S.astype(np.int8), E=ES, m_lo=mlS, m_up=muS, proposals=nprop, seed=seed)
        fn = os.path.join(L.HERE, "out", f"sampler_{tagf}.json")
    res["seconds"] = time.time() - t0
    json.dump(res, open(fn, "w"), indent=1)
    print(f"    -> {os.path.relpath(fn, L.HERE)}")
    print(f"DONE p6_04_sampler {seq} {bb} {tau} m={m} {form} w={w} [{time.time() - t0:.0f}s]", flush=True)


if __name__ == "__main__":
    main()
