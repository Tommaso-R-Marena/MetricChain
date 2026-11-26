#!/usr/bin/env python3
"""Coordinator's re-run of workstream P8's twelve-residue certificate (its request P8-E1) and checks of its constants
at that size that P8 did not make.

P8 fed the certificate pipeline (P3's band models, P6's share forms, my window models) with per-subset constants
chat_T of its own ('Sb': workstream P3's theorem with the maximum over host rotamers taken state-wise; 'SAb': the
same with P8's Theorem AH) and a driver of its own.  Here:
  (1) the constants are READ from ws_P8/out/g12_*.npz, g12b_*.npz -- they are P8's; nothing below recomputes them;
  (1a) P8's per-subset decomposition of workstream P3's closed form ('P3' variant) is compared with P3's closed-form
       sums as MY driver computes them (totals over exclusion sets): Gamma, every site sum S_i, every pair sum G_ij;
  (2) the ball is P8's cached file; its states are compared with pwmodel.ball_states and a random sample of its
      values is re-evaluated here;
  (3) NEW CHECK: |g(x) - I_{m-1} g(x)| <= sum_{T subset S(x), |T| = m} chat_T at uniformly random states with
      s = m .. n sites off the anchor (P8 checked the sandwich at Gibbs states and at samples of the floor, i.e. at
      low-energy states); I_{m-1} g by my own formula from the raw ball values,
            I_{m-1} g(x) = sum_{v < m} (-1)^{m-1-v} C(s-v-1, m-1-v) sum_{U subset S(x), |U| = v} g(x_U, x0),
      self-tested below against the grid recursion of lys_enum_check.py;
  (4) the brackets with MY assembly of S_i, G_ij, H_ijk from the constants, for 'Sb' and 'SAb', compared digit by
      digit with P8's JSON; the sandwich at my own Gibbs states (another seed than P8's and mine of the reach table),
      at the random states of (3) and at exact samples of the floor.
What is whose: constants P8; band models, anchored terms, evaluator P3; share forms P6; window models, this driver,
the remainder formula and the checks mine.

Run: python3 -B lys12_rerun.py K12 0.70 5 7 > lys12_rerun_K12_m5_w7.log
"""
import os, sys, math, json, time, itertools, importlib, resource
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCI = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(SCI, "ws_P6"))
import p6lib as L
T9 = importlib.import_module("p6_09_triple")
sys.path.insert(0, os.path.join(SCI, "pi_inference"))
import window_model
pw = L.pw; BETA = L.BETA
WindowModel, build_window_models, diff_window = window_model.make(pw)
CACHE = os.path.join(SCI, "pi_inference", "serine_helix_reach_cache")
L.encl.CACHE = CACHE; L.MYCACHE = CACHE
P8 = os.path.join(SCI, "ws_P8")


def log(s): print(s, flush=True)


def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


def interp(x, x0, m, lookup):
    """I_{m-1} g at the rows of x (N, n) from ball values: lookup(states) -> g."""
    out = np.empty(len(x))
    for a, row in enumerate(x):
        S = [i for i in range(len(row)) if row[i] != x0[i]]; s = len(S)
        if s <= m - 1:
            out[a] = lookup(row[None])[0]; continue
        tot = 0.0
        for v in range(0, m):
            c = (-1) ** (m - 1 - v) * math.comb(s - v - 1, m - 1 - v)
            sts = np.tile(np.asarray(x0), (math.comb(s, v), 1))
            for b, U in enumerate(itertools.combinations(S, v)):
                sts[b, list(U)] = row[list(U)]
            tot += c * float(lookup(sts).sum())
        out[a] = tot
    return out


def self_test(rng):
    sys.path.insert(0, HERE)
    from lys_enum_check import remainder
    shape = (3, 2, 4, 3, 2, 3); x0 = [1, 0, 2, 1, 1, 0]; F = rng.standard_normal(shape)
    grid = np.stack(np.meshgrid(*[np.arange(v) for v in shape], indexing="ij"), axis=-1).reshape(-1, len(shape))
    lut = lambda st: F[tuple(st.T)]
    dev = 0.0
    for m in (2, 3, 4, 5):
        R = remainder(F, x0, m).reshape(-1)
        dev = max(dev, float(np.abs((F.reshape(-1) - interp(grid, x0, m, lut)) - R).max()))
    return dev


def gibbs(G, c0, h, J, x0, k, rng, nchain, nsweep, burn):
    n = len(k); X = np.tile(np.array(x0, dtype=np.int64), (nchain, 1)); keep = []
    for sw in range(nsweep):
        for i in range(n):
            C = np.repeat(X, k[i], axis=0); C[:, i] = np.tile(np.arange(k[i]), nchain)
            E = (pw.f_energy(C, c0, h, J) + G.bulk_energy(C)).reshape(nchain, k[i])
            P = np.exp(-BETA * (E - E.min(1, keepdims=True))); P /= P.sum(1, keepdims=True)
            u = rng.random(nchain); X[:, i] = np.minimum((P.cumsum(1) < u[:, None]).sum(1), k[i] - 1)
        if sw >= burn: keep.append(X.copy())
    return np.concatenate(keep, axis=0)


def main():
    seq, tau, m, w = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); bb = "H"; M = m - 1
    t0 = time.time(); rng = np.random.default_rng(777)
    tag = f"{seq.replace(':', 'c')}_{bb}_{tau:.2f}"
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = [int(v) for v in x0]
    dom = float(np.prod([float(v) for v in k]))
    log(f"=== {seq} on {bb}, tau {tau}: {G.nat} atoms, {n} sites, states per site {k}, {dom:.6g} assignments; anchor {x0}, E = {E0:.6f} kcal/mol; order m = {m}, band {w}")
    log(f"(0) self-test of the interpolation formula against the grid recursion (random table, m = 2..5): largest deviation {self_test(rng):.1e}")
    # ---- (1) P8's constants
    Z = np.load(os.path.join(P8, "out", f"g12_{tag}_m{m}.npz")); Zb = np.load(os.path.join(P8, "out", f"g12b_{tag}_m{m}.npz"))
    assert [int(v) for v in Z["anchor"]] == x0 and [int(v) for v in Zb["anchor"]] == x0 and np.array_equal(Z["T"], Zb["T"])
    Ts = [tuple(int(v) for v in T) for T in Z["T"]]; assert Ts == list(itertools.combinations(range(n), m))
    V = [str(v) for v in Z["variants"]]; Vb = [str(v) for v in Zb["variants"]]
    chat = {v: Z["C"].sum(axis=2)[:, V.index(v)] for v in V}; chat.update({v: Zb["Cb"][:, Vb.index(v)] for v in Vb})
    log(f"(1) {len(Ts)} constants per variant read from ws_P8/out/g12_{tag}_m{m}.npz and g12b_...: Gamma_{m} (kT): "
        + ", ".join(f"{v} {BETA * chat[v].sum():.4g}" for v in ("P3", "AH", "S", "SA", "Sb", "SAb"))
        + f"; chains SAb <= SA <= S <= P3, SAb <= Sb <= S, SA <= AH <= P3 for every subset: "
        f"{bool(np.all(chat['SAb'] <= chat['SA'] * (1 + 1e-12)) and np.all(chat['SA'] <= chat['S'] * (1 + 1e-12)) and np.all(chat['S'] <= chat['P3'] * (1 + 1e-12)) and np.all(chat['SAb'] <= chat['Sb'] * (1 + 1e-12)) and np.all(chat['Sb'] <= chat['S'] * (1 + 1e-12)) and np.all(chat['SA'] <= chat['AH'] * (1 + 1e-12)) and np.all(chat['AH'] <= chat['P3'] * (1 + 1e-12)))}")

    def sums(c):
        S = np.zeros(n); Gp = np.zeros((n, n))
        for T, v in zip(Ts, c):
            for i in T: S[i] += v
            for i, j in itertools.combinations(T, 2): Gp[i, j] += v; Gp[j, i] += v
        return float(c.sum()), S, Gp
    # ---- (1a) P8's decomposition of P3's closed form against the closed-form sums of my driver
    t1 = time.time(); GF = L.GFBound2(G, x0, L.EnvelopeSup(G), K=m); excl = L.exclusion_sets(n, None)
    se, cr = L.GFBatch(GF).totals(m, excl); Gam_c, S_c, Gp_c = L.assemble_pair_sums(n, m, excl, se + cr)
    Gam_p, S_p, Gp_p = sums(chat["P3"]); iu = np.triu_indices(n, 1)
    log(f"(1a) workstream P3's closed form by my driver's route ({len(excl)} closed-form sums over exclusion sets, {time.time() - t1:.0f}s): Gamma_{m} = {BETA * Gam_c:.6g} kT; "
        f"P8's per-subset 'P3' variant summed: {BETA * Gam_p:.6g} kT; relative deviations: Gamma {abs(Gam_p / Gam_c - 1):.1e}, "
        f"site sums S_i at most {float(np.abs(S_p / S_c - 1).max()):.1e}, pair sums G_ij at most {float(np.abs(Gp_p[iu] / Gp_c[iu] - 1).max()):.1e} "
        f"(the closed-form route obtains S_i and G_ij by inclusion-exclusion over exclusion sets, the other by plain sums over the subsets)")
    # ---- (2) the ball
    blocks, tot = pw.ball_states(k, x0, M); allst = np.concatenate([b for _, b in blocks], axis=0)
    fb = [f for f in os.listdir(os.path.join(P8, "cache")) if f.startswith(f"ball_{tag}_M") and f.endswith(".npz") and "ckpt" not in f]
    zb = None
    for f in sorted(fb):
        z = np.load(os.path.join(P8, "cache", f))
        if z["states"].shape[0] >= tot and np.array_equal(z["states"][:tot], allst): zb = z; fbn = f; break
    assert zb is not None, "no cached ball of P8 with these states"
    vals = np.array(zb["vals"][:tot], dtype=float)
    pick = rng.choice(tot, size=3000, replace=False); re = np.empty(len(pick))
    for s in range(0, len(pick), 250): re[s:s + 250] = G.bulk_energy(allst[pick[s:s + 250]])
    log(f"(2) ball of radius {M}: {tot} values from ws_P8/cache/{fbn}; its states equal pwmodel.ball_states row by row; 3000 random values re-evaluated here: "
        f"largest deviation {float(np.abs(re - vals[pick]).max()):.1e} kcal/mol [{time.time() - t0:.0f}s]")
    radix = np.array([int(np.prod(k[i + 1:])) for i in range(n)], dtype=np.int64)
    code = allst.astype(np.int64) @ radix; order = np.argsort(code); code_s = code[order]; vals_s = vals[order]

    def lookup(st):
        c = np.atleast_2d(st).astype(np.int64) @ radix; p = np.searchsorted(code_s, c)
        assert np.array_equal(code_s[p], c), "state outside the ball"
        return vals_s[p]
    # ---- (3) the hypothesis of the pipeline at uniformly random states
    mob = [i for i in range(n) if k[i] > 1]; XR = []
    NR = 250
    for s in range(m, n + 1):
        for _ in range(NR):
            x = np.array(x0); S = rng.choice(mob, size=s, replace=False)
            for i in S:
                x[i] = rng.choice([v for v in range(k[i]) if v != x0[i]])
            XR.append(x)
    XR = np.array(XR); gR = np.empty(len(XR))
    for s in range(0, len(XR), 250): gR[s:s + 250] = G.bulk_energy(XR[s:s + 250])
    IR = interp(XR, x0, m, lookup); R = np.abs(gR - IR); sR = (XR != np.array(x0)[None])
    log(f"(3) |g - I_{M} g| against sum of constants over the {m}-subsets of the changed set, at {NR} uniformly random states for each number s of sites off the anchor [{time.time() - t0:.0f}s]:")
    log("| s | states | largest |g - I g| (kcal/mol) | median | variant | violations | smallest bound/|g - I g| | median bound (kcal/mol) |")
    log("|---|---|---|---|---|---|---|---|")
    res3 = {}
    for s in range(m, n + 1):
        sel = sR.sum(1) == s
        for var in ("P3", "Sb", "SAb"):
            B = np.zeros(len(XR))
            for T, v in zip(Ts, chat[var]): B += v * sR[:, list(T)].all(axis=1)
            viol = int((R[sel] > B[sel] * (1 + 1e-12) + 1e-9).sum())
            res3[f"{s}_{var}"] = dict(viol=viol, min_ratio=float((B[sel] / np.maximum(R[sel], 1e-300)).min()), maxR=float(R[sel].max()))
            log(f"| {s} | {int(sel.sum())} | {R[sel].max():.4g} | {np.median(R[sel]):.3g} | {var} | {viol} | {(B[sel] / np.maximum(R[sel], 1e-300)).min():.2f} | {np.median(B[sel]):.3g} |")
    # ---- (4) brackets with my assembly
    XG = gibbs(G, c0, h, J, x0, k, rng, 8, 150, 30); EG = pw.f_energy(XG, c0, h, J) + G.bulk_energy(XG)
    ER = pw.f_energy(XR, c0, h, J) + gR
    log(f"(4) my Gibbs sample (8 chains, 120 sweeps each after 30, seed 777): {len(XG)} states, {float((XG != np.array(x0)[None]).sum(1).mean()):.2f} sites off the anchor on average; "
        f"by site: " + " ".join(f"{v:.2f}" for v in (XG != np.array(x0)[None]).mean(0)) + f" [{time.time() - t0:.0f}s]")

    def lookup_seq(st):
        return lookup(st)
    d, nb, _ = pw.anchored_terms(G, x0, M, energy=lookup_seq, cache_file=None); assert nb == tot
    tris = T9.window_triples(n, w); phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
    out = dict(seq=seq, tau=tau, m=m, w=w, random_states=res3, forms={})
    ref = None; fj = os.path.join(P8, "out", f"cert_{tag}_m{m}_w{w}_SAb.json")
    if os.path.exists(fj): ref = json.load(open(fj))
    models = {}
    for var in ("Sb", "SAb"):
        Gam, S, Gp = sums(chat[var]); H = {tr: 0.0 for tr in tris}
        for T, v in zip(Ts, chat[var]):
            for tr in itertools.combinations(T, 3):
                if tr in H: H[tr] += v
        absA = 1e-12 * Gam                      # plain sums of at most C(n, m) positive doubles (P8 uses the same allowance)
        tabs = {"S": (L.site_form(n, m, S, phi1), np.zeros((n, n)), None), "B": L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, absA) + (None,),
                "T": window_model.triple_form_two_windows(T9.window_triples, L.RND, n, m, w, w, Gp, H, psi1, psi2, absA, absA)}
        for form in "SBT":
            t1 = time.time(); lo, up, info = build_window_models(k, x0, c0, h, J, d, w, L.EPS_G, M, *tabs[form]); a, b = up.lnZ(), lo.lnZ()
            vg = int((lo.energy(XG) > EG + 1e-9).sum() + (up.energy(XG) < EG - 1e-9).sum())
            vr = int((lo.energy(XR) > ER + 1e-9).sum() + (up.energy(XR) < ER - 1e-9).sum())
            cmp = ""
            if var == "SAb" and ref is not None:
                r = ref["forms"][form]; cmp = f"; P8's run: [{r['lnZ_lo']:.6f}, {r['lnZ_hi']:.6f}], differences {a - r['lnZ_lo']:+.1e}, {b - r['lnZ_hi']:+.1e}"
            out["forms"][f"{var}_{form}"] = dict(lnZ_lo=a, lnZ_hi=b, width=b - a, viol_gibbs=vg, viol_random=vr, info=info)
            log(f"    constants '{var}' (Gamma_{m} = {BETA * Gam:.4g} kT), form {form}, exact window terms ({info['exact']} exact, {info['reduced']} reduced, {info['far_pairs']} pairs beyond the band): "
                f"ln Z(E) in [{a:.6f}, {b:.6f}], width {b - a:.6g} nats; sandwich violated at {vg} of my {len(XG)} Gibbs states and at {vr} of the {len(XR)} random states{cmp} "
                f"[{time.time() - t1:.0f}s, peak RSS {rss():.0f} MB]")
            if form == "T": models[var] = (lo, up)
            else: del lo, up
    lo, up = models["SAb"]; a, b = up.lnZ(), lo.lnZ()
    xs = lo.sample(2000, rng); Ex = pw.f_energy(xs, c0, h, J) + G.bulk_energy(xs); ml, mu = lo.energy(xs), up.energy(xs)
    wts = np.exp(-BETA * (Ex - ml)); est = b + math.log(wts.mean()); se_est = float(wts.std(ddof=1) / math.sqrt(len(wts)) / wts.mean())
    log(f"(5) 2000 exact samples of the floor of the triple form ('SAb'; my seed): {float((xs != np.array(x0)[None]).sum(1).mean()):.2f} sites off the anchor on average; "
        f"m_- > E at {int((ml > Ex + 1e-9).sum())}, m_+ < E at {int((mu < Ex - 1e-9).sum())}; uncertified estimate by reweighting: ln Z(E) = {est:.6f} +- {se_est:.6f} "
        f"(inside the bracket: {a <= est <= b})")
    out["floor"] = dict(viol_lo=int((ml > Ex + 1e-9).sum()), viol_up=int((mu < Ex - 1e-9).sum()), est=est, se=se_est)
    json.dump(out, open(os.path.join(HERE, f"lys12_rerun_{seq.replace(':', 'c')}_m{m}_w{w}.json"), "w"), indent=1)
    log(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {rss():.0f} MB")


if __name__ == "__main__":
    main()
