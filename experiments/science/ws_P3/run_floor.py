"""
P3 -- certified floor and ceiling of E = f(ff14SB) + g(GBn2) on a fixed backbone, end to end:

  1. anchor x0 (coordinate descent on E);
  2. certified remainder constant Gamma_m of the anchored expansion truncated at order m
     (gfbound, rigorous enclosures) + floating-point allowance;
  3. g on the Hamming ball of radius m-1 about x0 -> anchored terms d_U, |U| <= m-1;
  4. banded pairwise lower / upper models  m_- <= E <= m_+  (pwmodel.build_band_models);
     exact ln Z(m_-), ln Z(m_+) by transfer matrix; rho_cert = max (m_+ - m_-) by max-plus DP;
  5. if the domain is small: enumeration of E, check of m_- <= E <= m_+ at every state, exact ln Z(E),
     exact rho = max(E - m_-), the cost number Z(m_-)/Z(E) - 1 of the theory division;
  6. N exact samples from pi_{m_-}, E at the samples, W = exp(-beta (E - m_-)) in [exp(-beta rho_cert), 1];
     Hoeffding bracket for ln Z(E) = ln Z(m_-) + ln E[W]; Gibbs-Bogoliubov lower bound.

usage: python3 -B run_floor.py SEQ BB TAU m [--w W] [--N N] [--seed S] [--delta D] [--noenum] [--kind gbn2|obc2] [--tag T]
"""
import sys, os, json, time, math
import numpy as np
from p3core import GBModel, KT300, BETA
from encl import EnvelopeSup
from gfbound import GFBound
import pwmodel as pw

EPS_G = 1e-7      # kcal/mol: allowance for the floating-point error of one evaluation of g (see report 2.6)
HERE = os.path.dirname(os.path.abspath(__file__))


def opt(a, key, default, cast=str):
    return cast(a[a.index(key) + 1]) if key in a else default


def main():
    a = sys.argv[1:]
    seq, bb, tau, m = a[0], a[1], float(a[2]), int(a[3])
    N = opt(a, "--N", 20000, int)
    seed = opt(a, "--seed", 1, int)
    delta = opt(a, "--delta", 0.05, float)
    kind = opt(a, "--kind", "gbn2")
    wopt = opt(a, "--w", None, int)
    tag = opt(a, "--tag", "")
    M = m - 1
    t0 = time.time()
    res = dict(seq=seq, bb=bb, tau=tau, m=m, kind=kind, N=N, seed=seed, delta=delta)
    G = GBModel(seq, bb, tau=tau, kind=kind)
    n, k = G.ns, G.k
    if min(k) == 0:
        print(f"{seq} {bb} tau {tau}: EMPTY domain"); return
    size = float(np.prod([float(v) for v in k]))
    c0, h, J = pw.known_tables(G)
    x0, E0, nev = pw.icm_anchor(G, c0, h, J)
    kmax = max(k)
    w = wopt if wopt is not None else max(1, min(n - 1, int(math.floor(math.log(3e6) / math.log(max(kmax, 2)))) - 1))
    res.update(natoms=int(G.nat), n=n, k=[int(v) for v in k], size=size, anchor=list(x0), E_anchor=E0, w=w)
    print(f"=== {seq} on {bb}, tau {tau}, {kind}, truncation order m = {m}: atoms {G.nat}, sites {n}, states/site {k[0]}..{k[-1]}, "
          f"|X| = {size:.3g}; anchor E = {E0:.4f} kcal/mol; band w = {w}", flush=True)
    # ---- 2. certified remainder constant
    t1 = time.time()
    sup = EnvelopeSup(G)
    GF = GFBound(G, x0, sup, K=m)
    gs, gc = GF.total(m) if m <= n else (0.0, 0.0)
    blocks, nball = pw.ball_states(k, x0, M)
    eps_fp = EPS_G * sum((2 ** len(U)) for U, _ in blocks)          # every d_U is an alternating sum of 2^|U| values of g
    Gamma = gs + gc + eps_fp
    gam = None
    if "--siteres" in a and m <= n:
        gam, _ = GF.site_penalties(m)
        res.update(gamma_sites=[float(v) for v in gam], Gamma_const=Gamma)
        print(f"    site penalties gamma_i (kcal/mol) = {np.round(gam, 4)}; sum = {gam.sum():.5e} (= Gamma_{m} up to rounding)", flush=True)
        Gamma = eps_fp                      # the constant part of the remainder bound is then only the fp allowance
    res.update(Gamma_self=gs, Gamma_cross=gc, eps_fp=eps_fp, Gamma=Gamma, nball=int(nball), t_gamma=time.time() - t1)
    print(f"    Gamma_{m} = {gs + gc:.5e} kcal/mol (self {gs:.3e}, cross {gc:.3e}) + floating-point allowance {eps_fp:.2e} "
          f"= {Gamma:.5e} = {Gamma * BETA:.4f} kT   [{time.time() - t1:.1f}s]", flush=True)
    # ---- 3. anchored terms
    t1 = time.time()
    rngc = np.random.default_rng(seed + 1000)
    chk = np.stack([rngc.integers(0, kk, 48) for kk in k], axis=1)
    dev = float(np.abs(G.bulk_energy(chk) - G.energy(chk)).max())
    assert dev < 1e-8, dev
    res["bulk_vs_own_evaluator"] = dev
    d, nb, _ = pw.anchored_terms(G, x0, M, progress=20, energy=G.bulk_energy)
    res.update(t_ball=time.time() - t1)
    for s in range(3, M + 1):
        vals = [np.abs(arr).max() for U, arr in d.items() if len(U) == s]
        neg = [max(0.0, -arr.min()) for U, arr in d.items() if len(U) == s]
        posv = [max(0.0, arr.max()) for U, arr in d.items() if len(U) == s]
        res[f"sum_absd{s}"] = float(np.sum(vals)); res[f"sum_negd{s}"] = float(np.sum(neg)); res[f"sum_posd{s}"] = float(np.sum(posv))
    print(f"    ball of radius {M}: {nb} evaluations of g ({100 * nb / size:.3g} % of the domain) [{time.time() - t1:.1f}s]; "
          + "; ".join(f"sum_T max|d_T| (order {s}) = {res[f'sum_absd{s}']:.3e}" for s in range(3, M + 1)), flush=True)
    # ---- 4. models
    t1 = time.time()
    lo, up = pw.build_band_models(k, x0, c0, h, J, d, w, Gamma, M, gam=gam)
    lnZlo, lnZup = lo.lnZ(), up.lnZ()
    diff = pw.BandModel(k, w)
    diff.const = up.const - lo.const
    diff.one = [up.one[i] - lo.one[i] for i in range(n)]
    for key in set(lo.pair) | set(up.pair):
        diff.pair[key] = up.pair.get(key, 0.0) - lo.pair.get(key, 0.0)
    rho_cert = diff.maximum()
    gap_min = diff.minimum()
    res.update(lnZ_lower_model=lnZlo, lnZ_upper_model=lnZup, rho_cert=rho_cert, min_gap=gap_min, minE_lower=lo.minimum(), minE_upper=up.minimum())
    print(f"    models: ln Z(m_-) = {lnZlo:.6f}, ln Z(m_+) = {lnZup:.6f}: deterministic certified bracket of ln Z(E), width {lnZlo - lnZup:.5f} nats; "
          f"rho_cert = max(m_+ - m_-) = {rho_cert:.5f} kcal/mol = {rho_cert * BETA:.4f} kT (min {gap_min:.2e}); "
          f"min m_- = {res['minE_lower']:.4f}, min m_+ = {res['minE_upper']:.4f} kcal/mol [{time.time() - t1:.1f}s]", flush=True)
    # ---- 5. enumeration (validation)
    if size <= 3.0e6 and "--noenum" not in a:
        t1 = time.time()
        st = G.product_states()
        g = np.empty(len(st))
        for s in range(0, len(st), 16384):
            g[s:s + 16384] = G.bulk_energy(st[s:s + 16384])
        E = pw.f_energy(st, c0, h, J) + g
        ml, mu = lo.energy(st), up.energy(st)
        rem = g - pw.expansion_value(d, st)
        rem2 = g - pw.expansion_value(d, st, M=2)
        res.update(rem2_min=float(rem2.min()), rem2_max=float(rem2.max()))
        bw = np.exp(-BETA * (E - E.min()))
        lnZE = float(np.log(bw.sum()) - BETA * E.min())
        lnZlo_enum = float(np.log(np.exp(-BETA * (ml - ml.min())).sum()) - BETA * ml.min())
        res.update(enum=True, viol_lower=int((ml > E + 1e-9).sum()), viol_upper=int((mu < E - 1e-9).sum()),
                   rem_min=float(rem.min()), rem_max=float(rem.max()), lnZ_E=lnZE, lnZ_lower_enum=lnZlo_enum,
                   rho_exact=float((E - ml).max()), rho_up_exact=float((mu - E).max()), cost=float(np.exp(lnZlo - lnZE) - 1.0),
                   minE=float(E.min()), E_anchor_is_min=bool(abs(E.min() - E0) < 1e-9),
                   mean_gap=float((bw / bw.sum() * (E - ml)).sum()))
        print(f"    ENUMERATION ({len(st)} states, {time.time() - t1:.1f}s): violations m_- > E: {res['viol_lower']}, m_+ < E: {res['viol_upper']}; "
              f"exact remainder g - I_{M} g in [{rem.min():.3e}, {rem.max():.3e}] (certified |.| <= {Gamma:.3e}); "
              f"ln Z(E) = {lnZE:.6f}; |lnZ(m_-) DP - enum| = {abs(lnZlo - lnZlo_enum):.1e}; rho = max(E - m_-) = {res['rho_exact']:.5f} kcal/mol = {res['rho_exact'] * BETA:.4f} kT; "
              f"cost number Z(m_-)/Z(E) - 1 = {res['cost']:.5f}; min E = {E.min():.4f} (anchor is the minimiser: {res['E_anchor_is_min']})", flush=True)
    # ---- 6. sampling
    if N > 0:
        t1 = time.time()
        rng = np.random.default_rng(seed)
        S = lo.sample(N, rng)
        gS = np.empty(N)
        for s in range(0, N, 4096):
            gS[s:s + 4096] = G.bulk_energy(S[s:s + 4096])
        ES = pw.f_energy(S, c0, h, J) + gS
        gap = ES - lo.energy(S)
        assert gap.min() > -1e-9, gap.min()
        Wv = np.exp(-BETA * np.maximum(gap, 0.0))
        wmin = math.exp(-BETA * rho_cert)
        Wbar = float(Wv.mean())
        hoef = (1.0 - wmin) * math.sqrt(math.log(2.0 / delta) / (2.0 * N))
        lo_mu, hi_mu = max(Wbar - hoef, wmin), min(Wbar + hoef, 1.0)
        br = (lnZlo + math.log(lo_mu), lnZlo + math.log(hi_mu))
        # sample-range (zero-failure tolerance) bound: with prob. >= 1 - delta/2 the mass above the sample maximum is
        # <= e_N = 1 - (delta/2)^(1/N), and likewise below the sample minimum (report 2.7, Lemma R)
        eN = 1.0 - (delta / 2.0) ** (1.0 / N)
        Wmin_s, Wmax_s = float(Wv.min()), float(Wv.max())
        rng_lo = Wmin_s - (Wmin_s - wmin) * eN
        rng_hi = Wmax_s + (1.0 - Wmax_s) * eN
        br2 = (lnZlo + math.log(rng_lo), lnZlo + math.log(rng_hi))
        res.update(range_bracket_lo=br2[0], range_bracket_hi=br2[1], W_min_sampled=Wmin_s, W_max_sampled=Wmax_s, eN=eN)
        gbar = float(gap.mean())
        gb = lnZlo - BETA * (gbar + rho_cert * math.sqrt(math.log(1.0 / (delta / 2)) / (2.0 * N)))
        res.update(Wbar=Wbar, Wstd=float(Wv.std(ddof=1)), hoeffding_halfwidth=hoef, bracket_lo=br[0], bracket_hi=br[1],
                   gap_mean=gbar, gap_max_sampled=float(gap.max()), gibbs_bogoliubov_lower=gb,
                   distinct_samples=int(len(np.unique(S, axis=0))), t_sample=time.time() - t1,
                   mean_changed_sites=float((S != np.array(x0)[None]).sum(1).mean()))
        print(f"    SAMPLING: N = {N} exact samples of pi_(m_-) ({res['distinct_samples']} distinct; mean number of sites off the anchor "
              f"{res['mean_changed_sites']:.2f}), E evaluated at each [{time.time() - t1:.1f}s]; W in [{wmin:.4f}, 1], mean {Wbar:.6f}, std {res['Wstd']:.2e}; "
              f"Hoeffding (delta = {delta}, two-sided): ln Z(E) in [{br[0]:.6f}, {br[1]:.6f}] (width {br[1] - br[0]:.5f} nats); "
              f"point estimate {lnZlo + math.log(Wbar):.6f}; Gibbs-Bogoliubov lower bound (same confidence) {gb:.6f}; mean gap {gbar:.4e}, max sampled gap {gap.max():.4e} kcal/mol", flush=True)
        print(f"    sample-range bound (delta = {delta}): ln Z(E) in [{br2[0]:.6f}, {br2[1]:.6f}] (width {br2[1] - br2[0]:.5f} nats); "
              f"W sampled in [{Wmin_s:.6f}, {Wmax_s:.6f}]", flush=True)
        if res.get("enum"):
            res["truth_in_bracket"] = bool(br[0] <= res["lnZ_E"] <= br[1])
            res["truth_in_range_bracket"] = bool(br2[0] <= res["lnZ_E"] <= br2[1])
            print(f"    truth {res['lnZ_E']:.6f} inside the Hoeffding bracket: {res['truth_in_bracket']}; inside the sample-range bracket: {res['truth_in_range_bracket']}", flush=True)
    res["seconds"] = time.time() - t0
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    if gam is not None and not tag:
        tag = "_siteres"
    fn = os.path.join(HERE, "out", f"floor_{seq.replace(':', 'c')}_{bb}_t{tau:.2f}_{kind}_m{m}{tag}.json")
    json.dump(res, open(fn, "w"), indent=1)
    print(f"    [{res['seconds']:.0f}s] -> {os.path.relpath(fn, HERE)}", flush=True)


if __name__ == "__main__":
    main()
