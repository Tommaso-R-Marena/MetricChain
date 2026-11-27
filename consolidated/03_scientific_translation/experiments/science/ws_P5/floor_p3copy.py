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
# --- P5: this file is a VERBATIM COPY of experiments/science/ws_P3/run_floor.py (workstream P3's pipeline) except for
# --- the next line, which puts ws_P3 on sys.path and redirects the enclosure cache to ws_P5/cache, so that nothing is
# --- written into ws_P3.  Outputs go to ws_P5/out/floor_*.json and ws_P5/cache/ball_*.npz (HERE is this directory).
import p5lib  # noqa: F401
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
        # floating-point allowance, site-resolved as well: d_U is exactly zero (also in floating point) unless U is
        # inside the changed set, so the rounding error of the model at x is at most
        # eps_g * sum_{U subset S(x)} 2^|U| <= eps_g + sum_{i in S(x)} eps_i,  eps_i = eps_g * sum_{U ni i} 2^|U| / |U|
        eps_site = np.zeros(n)
        for U, _b in blocks:
            for i in U:
                eps_site[i] += EPS_G * (2 ** len(U)) / len(U)
        res.update(gamma_sites=[float(v) for v in gam], Gamma_const=Gamma, eps_sites=[float(v) for v in eps_site])
        print(f"    site penalties gamma_i (kcal/mol) = {np.round(gam, 4)}; sum = {gam.sum():.5e} (= Gamma_{m} up to rounding); "
              f"floating-point allowance per site <= {eps_site.max():.2e}", flush=True)
        gam = gam + eps_site
        Gamma = EPS_G                       # the constant part of the remainder bound is then only the allowance for g(x0)
        eps_fp = EPS_G
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
    import hashlib
    ah = hashlib.sha1(str((tuple(x0), [list(map(int, dd)) for dd in G.dom])).encode()).hexdigest()[:10]
    cache_file = os.path.join(HERE, "cache", f"ball_{seq.replace(':', 'c')}_{bb}_t{tau:.2f}_{kind}_M{M}_{ah}.npz")
    d, nb, _ = pw.anchored_terms(G, x0, M, progress=20, energy=G.bulk_energy, cache_file=cache_file)
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
    # ---- 4b. certified inputs of the Bennett bracket (coordinator's addition; report 2.10): for the model m and
    # r = beta (E - m): a one-sided floor of r, an upper bound of its mean and of its variance under pi_m, all from the
    # certified sandwich m_- <= E <= m_+ and exact transfer-matrix moments of the explicit function u = beta (m_+ - m_-).
    t1 = time.time()
    Eu, Eu2 = lo.moments(diff)                                   # under pi_{m_-}
    b0, s20 = BETA * Eu, BETA * BETA * Eu2                       # model m_-: 0 <= r <= u, so E r - inf r <= E u, Var r <= E u^2
    W0 = pw.bennett_W(b0, s20)
    mid = pw.BandModel(k, w)
    mid.const = 0.5 * (lo.const + up.const)
    mid.one = [0.5 * (lo.one[i] + up.one[i]) for i in range(n)]
    for key in set(lo.pair) | set(up.pair):
        mid.pair[key] = 0.5 * (up.pair.get(key, 0.0) + lo.pair.get(key, 0.0))
    lnZmid = mid.lnZ()
    Eum, Eu2m = mid.moments(diff)                                # under pi_{m_0}, m_0 = (m_- + m_+)/2: |r_0| <= u/2
    bh, s2h = 0.5 * BETA * Eum + 0.5 * BETA * rho_cert, 0.25 * BETA * BETA * Eu2m
    Wh = pw.bennett_W(bh, s2h)
    res.update(bennett=dict(lower=dict(b_cert=b0, s2_cert=s20, W_cert=W0, mean_u=BETA * Eu),
                            mid=dict(b_cert=bh, s2_cert=s2h, W_cert=Wh, lnZ_mid=lnZmid, mean_u=BETA * Eum)))
    print(f"    BENNETT inputs, certified (kT units): model m_-: floor lo = 0 of r = beta(E - m_-), b_cert = E u = {b0:.4e}, "
          f"s2_cert = E u^2 = {s20:.4e}, W(b, s2) = {W0:.4e} nats | midpoint model m_0: b_cert = {bh:.4e}, s2_cert = {s2h:.4e}, W = {Wh:.4e} nats "
          f"(ln Z(m_0) = {lnZmid:.6f}) [{time.time() - t1:.1f}s]", flush=True)
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
        lnZE = float(np.log(np.exp(-BETA * (E - E.min())).sum()) - BETA * E.min())
        for nm, mm, lz in (("lower", ml, lnZlo), ("mid", 0.5 * (ml + mu), lnZmid)):
            rr = BETA * (E - mm)
            pm = np.exp(-BETA * (mm - mm.min())); pm /= pm.sum()
            Er = float((pm * rr).sum()); var = float((pm * (rr - Er) ** 2).sum())
            be = Er - float(rr.min())
            K = lnZE - lz + Er
            We = pw.bennett_W(be, var)
            bd = res["bennett"][nm]
            bd.update(b_enum=be, s2_enum=var, W_enum=We, K_true=K, Er=Er)
            uu = BETA * (mu - ml)                    # the transfer-matrix moments of u against direct sums
            dev1 = abs(float((pm * uu).sum()) - bd["mean_u"]); dev2 = abs(float((pm * uu * uu).sum()) - (bd["s2_cert"] if nm == "lower" else 4.0 * bd["s2_cert"]))
            assert dev1 < 1e-9 * (1.0 + bd["mean_u"]) and dev2 < 1e-9 * (1.0 + float((pm * uu * uu).sum())), (nm, dev1, dev2)
            bd["moments_dev"] = max(dev1, dev2)
            assert be <= bd["b_cert"] * (1 + 1e-9) + 1e-9 and var <= bd["s2_cert"] * (1 + 1e-9) + 1e-12, (nm, be, var, bd)
            assert -1e-9 <= K <= We + 1e-9 and K <= bd["W_cert"] + 1e-9, (nm, K, We, bd["W_cert"])
        bl, bm = res["bennett"]["lower"], res["bennett"]["mid"]
        print(f"    BENNETT, enumerated (kT): m_-: b = {bl['b_enum']:.4e} (cert {bl['b_cert']:.4e}), s2 = {bl['s2_enum']:.4e} (cert {bl['s2_cert']:.4e}), "
              f"true Jensen gap K = {bl['K_true']:.4e}, W(enum) = {bl['W_enum']:.4e}, W(cert) = {bl['W_cert']:.4e} | m_0: b = {bm['b_enum']:.4e} (cert {bm['b_cert']:.4e}), "
              f"s2 = {bm['s2_enum']:.4e} (cert {bm['s2_cert']:.4e}), K = {bm['K_true']:.4e}, W(enum) = {bm['W_enum']:.4e}, W(cert) = {bm['W_cert']:.4e}", flush=True)
        remg = rem.reshape(k)
        res["osc_rem"] = [float(np.ptp(remg, axis=i).max()) for i in range(n)]      # exact one-site oscillations of g - I_M g
        bw = np.exp(-BETA * (E - E.min()))
        lnZE = float(np.log(bw.sum()) - BETA * E.min())
        lnZlo_enum = float(np.log(np.exp(-BETA * (ml - ml.min())).sum()) - BETA * ml.min())
        res.update(enum=True, viol_lower=int((ml > E + 1e-9).sum()), viol_upper=int((mu < E - 1e-9).sum()),
                   rem_min=float(rem.min()), rem_max=float(rem.max()), lnZ_E=lnZE, lnZ_lower_enum=lnZlo_enum,
                   rho_exact=float((E - ml).max()), rho_up_exact=float((mu - E).max()), cost=float(np.exp(lnZlo - lnZE) - 1.0),
                   minE=float(E.min()), E_anchor_is_min=bool(abs(E.min() - E0) < 1e-9),
                   mean_gap=float((bw / bw.sum() * (E - ml)).sum()))
        print(f"    ENUMERATION ({len(st)} states, {time.time() - t1:.1f}s): violations m_- > E: {res['viol_lower']}, m_+ < E: {res['viol_upper']}; "
              f"exact remainder g - I_{M} g in [{rem.min():.3e}, {rem.max():.3e}] (certified: |.| <= {res['Gamma_self'] + res['Gamma_cross'] + eps_fp:.3e}"
              + (", and <= sum of gamma_i over the changed sites" if gam is not None else "") + "); "
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
        tiny = 1e-300                      # e^{-beta rho_cert} underflows for absurdly loose floors (Leu helix, m = 3)
        br = (lnZlo + math.log(max(lo_mu, tiny)), lnZlo + math.log(max(hi_mu, tiny)))
        # sample-range (zero-failure tolerance) bound: with prob. >= 1 - delta/2 the mass above the sample maximum is
        # <= e_N = 1 - (delta/2)^(1/N), and likewise below the sample minimum (report 2.7, Lemma R)
        eN = 1.0 - (delta / 2.0) ** (1.0 / N)
        Wmin_s, Wmax_s = float(Wv.min()), float(Wv.max())
        rng_lo = Wmin_s - (Wmin_s - wmin) * eN
        rng_hi = Wmax_s + (1.0 - Wmax_s) * eN
        br2 = (lnZlo + math.log(max(rng_lo, 1e-300)), lnZlo + math.log(max(rng_hi, 1e-300)))
        res.update(range_bracket_lo=br2[0], range_bracket_hi=br2[1], W_min_sampled=Wmin_s, W_max_sampled=Wmax_s, eN=eN)
        # Bennett bracket with the certified (b, s2) of the model m_-: ln Z(E) = ln Z(m_-) - E r + K, 0 <= K <= W_cert;
        # the mean E r from the samples with Chebyshev's inequality and the CERTIFIED variance bound
        rS = BETA * gap
        res.update(r_mean=float(rS.mean()), r_var=float(rS.var(ddof=1)), r_min=float(rS.min()), r_max=float(rS.max()))
        print(f"    sampled remainder r = beta(E - m_-) under pi_(m_-): mean {rS.mean():.4e}, variance {rS.var(ddof=1):.4e}, min {rS.min():.4e}, max {rS.max():.4e} kT "
              f"(certified: 0 <= r <= u, E u = {b0:.4e}, E u^2 = {s20:.4e})", flush=True)
        rbar = BETA * float(gap.mean())
        tch = math.sqrt(s20 / (N * delta))
        br3 = (lnZlo - rbar - tch, lnZlo - rbar + tch + W0)
        res.update(bennett_bracket_lo=br3[0], bennett_bracket_hi=br3[1], cheb_halfwidth=tch)
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
        print(f"    Bennett bracket (certified b, s2; mean by Chebyshev, delta = {delta}): ln Z(E) in [{br3[0]:.6f}, {br3[1]:.6f}] "
              f"(width {br3[1] - br3[0]:.5f} nats = W_cert {W0:.2e} + 2 x {tch:.2e})", flush=True)
        if res.get("enum"):
            res["truth_in_bennett_bracket"] = bool(br3[0] <= res["lnZ_E"] <= br3[1])
            res["truth_in_bracket"] = bool(br[0] <= res["lnZ_E"] <= br[1])
            res["truth_in_range_bracket"] = bool(br2[0] <= res["lnZ_E"] <= br2[1])
            print(f"    truth {res['lnZ_E']:.6f} inside the Hoeffding bracket: {res['truth_in_bracket']}; inside the sample-range bracket: {res['truth_in_range_bracket']}", flush=True)
    res["seconds"] = time.time() - t0
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    if gam is not None and not tag:
        tag = "_siteres"
    if wopt is not None and wopt != 8:
        tag += f"_w{wopt}"
    fn = os.path.join(HERE, "out", f"floor_{seq.replace(':', 'c')}_{bb}_t{tau:.2f}_{kind}_m{m}{tag}.json")
    json.dump(res, open(fn, "w"), indent=1)
    print(f"    [{res['seconds']:.0f}s] -> {os.path.relpath(fn, HERE)}", flush=True)


if __name__ == "__main__":
    main()
