"""
P6 step 2-4: the certified sandwich  m_- <= E <= m_+  of P3 with three penalty forms, for several band widths:

   S (site form, P3):         penalty = sum_i gamma_i s_i,                   gamma_i = (1/m) sum_{T ni i} chat_T
   B (banded pair form):      penalty = sum_{i<j, j-i<=w} gamma_ij s_i s_j + sum_i gamma'_i s_i,
                              gamma_ij = sum_{T contains i,j} chat_T / C(m,2),  gamma'_i = (1/2) sum_{j: |i-j|>w} gamma_ij
   (for w = n-1 the form B is the full pair form P)

with s_i = [x_i != x0_i]; everything else is P3's model unchanged (pwmodel.build_band_models: in-band pairs exact,
far pairs split additively, evaluated terms of order 3..m-1 reduced to an in-band pair by min/max).  Floating-point
allowances as in P3 (EPS_G per evaluated value), allocated to sites (form S, as P3) or to pairs (form B).

For enumerable domains: E, m_-, m_+ at EVERY state (violations counted with tolerance 0 and with P3's 1e-9), exact
ln Z(E), cost numbers, ratios penalty / |exact remainder|, and -- where C(n, m) <= MAXSUB -- the pair sums against
explicit enumeration of the subsets.

usage: python3 -B p6_02_sandwich.py SEQ BB TAU --m 3,4,5 [--bands default|8,2,1] [--noenum] [--kind gbn2|obc2]
"""
import sys, os, time, math, json, itertools
import numpy as np
import p6lib as L
pw = L.pw
BETA = L.BETA
MAXSUB = 500      # explicit enumeration of subsets only where C(n, m) <= MAXSUB (lowered from 1000 at 03:12 UTC, see NOTES)


def opt(a, key, default, cast=str):
    return cast(a[a.index(key) + 1]) if key in a else default


def lnz_enum(v):
    return float(np.log(np.exp(-BETA * (v - v.min())).sum()) - BETA * v.min())


def main():
    a = sys.argv[1:]
    seq, bb, tau = a[0], a[1], float(a[2])
    orders = [int(v) for v in opt(a, "--m", "3,4,5").split(",")]
    kind = opt(a, "--kind", "gbn2")
    bands_opt = opt(a, "--bands", "default")
    t0 = time.time()
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau, kind)
    n, k = G.ns, G.k
    if min(k) == 0:
        print(f"{seq} {bb} tau {tau}: EMPTY domain"); print("DONE"); return
    size = float(np.prod([float(v) for v in k]))
    kmax = max(k)
    w_p3 = max(1, min(n - 1, int(math.floor(math.log(3e6) / math.log(max(kmax, 2)))) - 1))     # P3's default band
    enum = (size <= 3.0e6) and ("--noenum" not in a)
    if bands_opt == "default":
        bands = sorted(({w_p3, n - 1, 1, 2} if enum else {w_p3}) & set(range(1, n)), reverse=True)
    else:
        bands = [int(v) for v in bands_opt.split(",")]
    tag = L.tagname(seq, bb, tau, kind)
    print(f"=== sandwich: {seq} on {bb}, tau {tau}, {kind}: atoms {G.nat}, sites {n}, states/site {min(k)}..{max(k)}, |X| = {size:.6g}; "
          f"anchor {''.join(map(str, x0))} E = {E0:.6f} kcal/mol; orders {orders}; bands {bands} (P3's default band: {w_p3}); "
          f"enumeration: {enum} [{time.time() - t0:.1f}s]", flush=True)
    res = dict(seq=seq, bb=bb, tau=tau, kind=kind, n=n, k=[int(v) for v in k], size=size, natoms=int(G.nat), anchor=list(x0),
               E_anchor=E0, w_p3=w_p3, bands=bands, enum=enum, orders={})
    sup = L.EnvelopeSup(G)
    # ---------------------------------------------------------------- enumeration of E (once per instance)
    if enum:
        t1 = time.time()
        st, g, src = L.enumerate_g(G, seq, bb, tau, kind)
        rngc = np.random.default_rng(12345)
        pick = rngc.integers(0, len(st), min(48, len(st)))
        dev = float(np.abs(g[pick] - G.energy(st[pick])).max())          # P3's own evaluator at 48 random states
        assert dev < 1e-8, dev
        E = pw.f_energy(st, c0, h, J) + g
        lnZE = lnz_enum(E)
        sx = (st != np.array(x0)[None])
        nch = sx.sum(1)
        res.update(lnZ_E=lnZE, minE=float(E.min()), anchor_is_min=bool(abs(E.min() - E0) < 1e-9), enum_src=src, bulk_vs_own=dev)
        print(f"    enumeration of g on {len(st)} states ({src}) [{time.time() - t1:.1f}s]; bulk evaluator vs P3's own at 48 states: {dev:.1e}; "
              f"ln Z(E) = {lnZE:.6f}; min E = {E.min():.6f} (anchor is the minimiser: {res['anchor_is_min']})", flush=True)
    nchecks = 0; nviol = 0          # model checks: m_- <= E and E <= m_+ (two inequalities per state, form and band)
    nchk_rem = 0; nviol_rem = 0     # remainder checks: |g - I_(m-1) g| <= penalty (one per state and penalty function)
    for m in orders:
        if m > n:
            print(f"  -- m = {m} > n = {n}: skipped"); continue
        M = m - 1
        tm = time.time()
        R = dict(m=m)
        # ------------------------------------------------------------ pair sums (closed form, no subset enumerated)
        fn = os.path.join(L.HERE, "out", f"pairsums_{tag}_m{m}.npz")
        Gam = None
        if os.path.exists(fn):
            z = np.load(fn)
            if list(z["anchor"]) == list(x0) and int(z["w"]) == -1:
                Gam, S, Gp = float(z["Gamma"]), z["S"], z["G"]
                srcp = "read from " + os.path.basename(fn)
        GF = L.GFBound2(G, x0, sup, K=m)
        if Gam is None:
            t1 = time.time()
            excl = L.exclusion_sets(n)
            se, cr = L.GFBatch(GF).totals(m, excl)
            Gam, S, Gp = L.assemble_pair_sums(n, m, excl, se + cr)
            os.makedirs(os.path.join(L.HERE, "out"), exist_ok=True)
            np.savez(fn, Gamma=Gam, S=S, G=Gp, tot=se + cr, se=se, cr=cr, anchor=np.array(x0), m=m, w=-1,
                     excl=np.array([list(e) + [-1] * (2 - len(e)) for e in excl]))
            srcp = f"computed, {len(excl)} exclusion sets, {time.time() - t1:.1f}s"
        absallow = 5e-9 * Gam
        c2 = math.comb(m, 2)
        print(f"  -- m = {m}: Gamma_{m} = {Gam:.6e} kcal/mol = {Gam * BETA:.4f} kT; pair sums {srcp}; max G_ij/C(m,2) = {np.nanmax(Gp) / c2:.4e}, "
              f"max S_i/m = {S.max() / m:.4e}", flush=True)
        R.update(Gamma=Gam, max_gamma_site=float(S.max() / m), max_gamma_pair=float(np.nanmax(Gp) / c2))
        # ------------------------------------------------------------ explicit enumeration of subsets (validation of item 1)
        chat = None
        if enum and math.comb(n, m) <= MAXSUB:
            t1 = time.time()
            chat = L.enum_chat(GF, m)
            Gam_e, S_e, Gp_e = L.pair_sums_from_chat(n, chat)
            offd = ~np.eye(n, dtype=bool)
            dG = float(np.abs(Gp - Gp_e)[offd].max()); dS = float(np.abs(S - S_e).max())
            R.update(pairsum_check=dict(n_subsets=len(chat), dG_max=dG, dS_max=dS, dGamma=abs(Gam - Gam_e), rel_to_Gamma=max(dG, dS) / Gam_e,
                                        G_min=float(Gp_e[offd].min()), n_pairs=n * (n - 1) // 2))
            print(f"     pair sums vs EXPLICIT ENUMERATION of {len(chat)} subsets [{time.time() - t1:.1f}s]: max |G_ij - enum| = {dG:.2e}, "
                  f"max |S_i - enum| = {dS:.2e}, |Gamma - enum| = {abs(Gam - Gam_e):.2e} kcal/mol (relative to Gamma: {max(dG, dS) / Gam_e:.1e}); "
                  f"smallest G_ij = {Gp_e[offd].min():.3e}", flush=True)
            assert max(dG, dS) <= 1e-9 * Gam_e, "closed-form pair sums disagree with enumeration"
        # ------------------------------------------------------------ ball
        t1 = time.time()
        d, nball, srcb = L.ball_terms(G, x0, M, seq, bb, tau, kind)
        R.update(nball=int(nball))
        print(f"     ball of radius {M}: {nball} values of g ({srcb if 'evaluated' in srcb else 'prefix of ' + os.path.relpath(srcb, os.path.dirname(L.HERE))}) [{time.time() - t1:.1f}s]", flush=True)
        phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
        # ------------------------------------------------------------ exact remainder and the penalties as functions (enumeration)
        if enum:
            rem = g - pw.expansion_value(d, st)
            R.update(rem_min=float(rem.min()), rem_max=float(rem.max()))
            big = (nch >= m) & (np.abs(rem) > 1e-9)
            sf = sx.astype(float)
            pure_site = sf @ (S / m)
            pure_pair = 0.5 * np.einsum("ni,ij,nj->n", sf, np.where(np.eye(n, dtype=bool), 0.0, Gp) / c2, sf)
            env = L.envelope_value(st, x0, chat) if chat is not None else None
            tol = 1e-12 * max(Gam, 1.0)
            chain_ok = bool((pure_pair <= pure_site + tol).all()) and (env is None or bool((env <= pure_pair + tol).all()))
            rr = {}
            for nm, pv in (("envelope", env), ("pair", pure_pair), ("site", pure_site)):
                if pv is None:
                    continue
                viol_r = int((np.abs(rem) > pv + 1e-9).sum())
                rat = pv[big] / np.abs(rem[big]) if big.any() else np.array([np.nan])
                rr[nm] = dict(viol=viol_r, ratio_min=float(rat.min()), ratio_max=float(rat.max()), ratio_median=float(np.median(rat)))
                nchk_rem += len(st); nviol_rem += viol_r
            R.update(remainder=rr, chain_ok=chain_ok, n_states_ratio=int(big.sum()))
            print(f"     exact remainder g - I_{M} g in [{rem.min():.3e}, {rem.max():.3e}] kcal/mol; |remainder| <= penalty at every state: "
                  + "; ".join(f"{nm}: violations {v['viol']}, ratio penalty/|remainder| min {v['ratio_min']:.3g} median {v['ratio_median']:.3g} max {v['ratio_max']:.3g}" for nm, v in rr.items())
                  + f" ({int(big.sum())} states with >= {m} changed sites and |remainder| > 1e-9); pointwise envelope <= pair <= site: {chain_ok}", flush=True)
            assert chain_ok
        # ------------------------------------------------------------ models
        R["bands"] = {}
        for w in bands:
            RW = {}
            gs_S = L.site_form(n, m, S, phi1); g2_S = np.zeros((n, n))
            gs_B, g2_B = L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, absallow)
            if enum:
                # the banded penalty as a function: between the pair form and the site form (pure parts, no allowances)
                gsb0, g2b0 = L.banded_pair_form(n, m, w, S, Gp, np.zeros(n), np.zeros((n, n)), 0.0)
                pure_band = L.penalty_value(st, x0, gsb0, g2b0)
                tolb = 3e-9 * max(Gam, 1.0)          # the banded form carries P3's outward-rounding factor (1 + 1e-9)
                RW["chain_banded_ok"] = bool((pure_pair <= pure_band + tolb).all() and (pure_band <= pure_site + tolb).all())
                viol_b = int((np.abs(rem) > pure_band + 1e-9).sum())
                ratb = pure_band[big] / np.abs(rem[big]) if big.any() else np.array([np.nan])
                RW["remainder_banded"] = dict(viol=viol_b, ratio_min=float(ratb.min()), ratio_max=float(ratb.max()), ratio_median=float(np.median(ratb)))
                nchk_rem += len(st); nviol_rem += viol_b
                assert RW["chain_banded_ok"]
            for form, gs, g2 in (("S", gs_S, g2_S), ("B", gs_B, g2_B)):
                t1 = time.time()
                lo, up = L.build_models(k, x0, c0, h, J, d, w, M, gs, g2)
                lnZlo, lnZup = lo.lnZ(), up.lnZ()
                diff = L.diff_model(lo, up)
                rho_cert = diff.maximum(); gap_min = diff.minimum()
                Eu, Eu2 = lo.moments(diff)
                F = dict(lnZ_lo=lnZlo, lnZ_up=lnZup, width=lnZlo - lnZup, rho_cert=rho_cert, min_gap_models=gap_min,
                         min_lo=lo.minimum(), min_up=up.minimum(), mean_u=BETA * Eu, mean_u2=BETA * BETA * Eu2,
                         max_gs=float(np.max(gs)), max_g2=float(np.max(g2)))
                msg = (f"     w = {w:2d} form {form}: ln Z(m_-) = {lnZlo:.6f}, ln Z(m_+) = {lnZup:.6f}, width {lnZlo - lnZup:.6f} nats; "
                       f"rho_cert = {rho_cert * BETA:.4f} kT; E_(pi-) u = {BETA * Eu:.4e}; min m_- = {F['min_lo']:.6f}")
                if enum:
                    ml, mu = lo.energy(st), up.energy(st)
                    v0l = int((ml > E).sum()); v0u = int((mu < E).sum())
                    v9l = int((ml > E + 1e-9).sum()); v9u = int((mu < E - 1e-9).sum())
                    nchecks += 2 * len(st); nviol += v9l + v9u
                    lz_lo_e, lz_up_e = lnz_enum(ml), lnz_enum(mu)
                    F.update(viol_lower=v9l, viol_upper=v9u, viol_lower_strict=v0l, viol_upper_strict=v0u,
                             min_E_minus_lo=float((E - ml).min()), min_up_minus_E=float((mu - E).min()),
                             rho_exact=float((E - ml).max()), rho_up_exact=float((mu - E).max()),
                             cost_lower=float(math.expm1(min(lnZlo - lnZE, 700.0))), cost_upper=float(-math.expm1(lnZup - lnZE)),     # capped at e^700
                             dlnZ_lo=lnZlo - lnZE, dlnZ_up=lnZE - lnZup, dp_vs_enum=max(abs(lnZlo - lz_lo_e), abs(lnZup - lz_up_e)),
                             truth_inside=bool(lnZup <= lnZE <= lnZlo), states=int(len(st)))
                    msg += (f" | ENUM {len(st)} states: violations m_- > E: {v9l} (strict {v0l}), m_+ < E: {v9u} (strict {v0u}); "
                            f"min(E - m_-) = {F['min_E_minus_lo']:.2e}, min(m_+ - E) = {F['min_up_minus_E']:.2e}; "
                            f"ln Z(m_-) - ln Z(E) = {F['dlnZ_lo']:.3e}, ln Z(E) - ln Z(m_+) = {F['dlnZ_up']:.3e}; cost number {F['cost_lower']:.4g}; "
                            f"|DP - enum| = {F['dp_vs_enum']:.1e}; truth inside: {F['truth_inside']}")
                RW[form] = F
                print(msg + f" [{time.time() - t1:.1f}s]", flush=True)
            # reproduction of P3's site-form run where its output file exists for this band
            p3fn = os.path.join(L.P3, "out", f"floor_{tag}_m{m}_siteres" + ("" if w in (8, w_p3) else f"_w{w}") + ".json")
            for cand in (p3fn, os.path.join(L.P3, "out", f"floor_{tag}_m{m}_siteres_w{w}.json")):
                if os.path.exists(cand):
                    p3 = json.load(open(cand))
                    if p3.get("w") == w and list(p3.get("anchor", [])) == list(x0):
                        dlo = abs(p3["lnZ_lower_model"] - RW["S"]["lnZ_lo"]); dup = abs(p3["lnZ_upper_model"] - RW["S"]["lnZ_up"])
                        RW["p3_repro"] = dict(file=os.path.basename(cand), dlo=dlo, dup=dup, p3_width=p3["lnZ_lower_model"] - p3["lnZ_upper_model"])
                        print(f"     w = {w:2d} form S against P3's own run ({os.path.basename(cand)}): |ln Z(m_-) - P3| = {dlo:.1e}, |ln Z(m_+) - P3| = {dup:.1e}", flush=True)
                        break
            R["bands"][str(w)] = RW
        R["seconds"] = time.time() - tm
        res["orders"][str(m)] = R
    res.update(state_checks=int(nchecks), violations=int(nviol), remainder_checks=int(nchk_rem), remainder_violations=int(nviol_rem), seconds=time.time() - t0)
    os.makedirs(os.path.join(L.HERE, "out"), exist_ok=True)
    bt = "" if bands_opt == "default" else "_b" + bands_opt.replace(",", "-")
    fn = os.path.join(L.HERE, "out", f"sandwich_{tag}{bt}.json")
    json.dump(res, open(fn, "w"), indent=1)
    print(f"    checks of m_- <= E and of E <= m_+ in this run: {nchecks}, violations: {nviol}; checks of |remainder| <= penalty: {nchk_rem}, violations: {nviol_rem}  -> {os.path.relpath(fn, L.HERE)}")
    print(f"DONE p6_02_sandwich {seq} {bb} {tau} {kind} [{time.time() - t0:.0f}s]", flush=True)


if __name__ == "__main__":
    main()
