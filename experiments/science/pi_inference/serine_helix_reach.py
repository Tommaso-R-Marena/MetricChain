#!/usr/bin/env python3
"""Addendum A17 (16): DOES THE CERTIFICATE REACH A NON-FROZEN COMPACT ENSEMBLE BEYOND ENUMERATION?  Serine on the helix at
a length that cannot be enumerated -- coordinator's script.  The design rule of addendum A17 (15) (the bracket of the
k-share form is about 2 p^k Gamma_m) is used as a PREDICTION, printed before any bracket is computed, and then tested;
so is its refinement, which needs no independence: to first order in the band,
      ln Z(m_-) - ln Z(m_+)  =  beta E_E[ m_+ - m_- ]        (E_E: mean under the TRUE ensemble; error at most
                                                               max(E[b^2], e^A E[a^2]) / 2,  a = beta (E - m_-) <= A,  b = beta (m_+ - E)),
i.e. twice the mean penalty when the evaluated terms are exact.  "Refined rule" below: 2 beta x the mean, over the
Gibbs sample, of the penalty each form actually charges (computable before the ball is paid for); after the models
are built the script also prints beta x the mean of m_+ - m_- over the same sample, which contains P3's reductions.

Steps for Ace-X_n-NMe (X = S by default; any sequence name of the workstreams) on a backbone (default: helix), order
m, band w:
  (0) the true ensemble by heat-bath Gibbs sampling of E = f + g (uncertified; 16 chains): the fraction p of side chains
      off the anchor, site by site;
  (1) Gamma_m from workstream P3's certified constants (closed form, no enumeration) and the prediction 2 p^k Gamma_m
      for site (k = 1), pair (k = 2), triple (k = 3) shares and for the envelope (k = m);
  (2) the ball of radius m - 1 around the anchor, evaluated with P3's evaluator (cached in ./serine_helix_reach_cache);
  (3) the pair sums and in-window triple sums of the constants (workstream P6's closed forms);
  (4) the banded sandwiches: site form (P3), pair form and triple form (P6); CERTIFIED brackets of ln Z(E), each
      twice: with P3's reduction of every evaluated term of order >= 3 to a pair table (the workstreams' models), and
      with the evaluated terms that fit a window kept EXACT (window_model.py; checked against enumeration by
      window_model_check.py);
  (5) checks without enumeration on the narrowest sandwich (triple form, exact window terms): exact samples of its
      floor (the sandwich must hold at every one); an uncertified estimate of ln Z by reweighting those samples; the
      theory division's sandwich sampler (a bracket that holds with probability >= 0.95, given the sandwich); p
      re-estimated from the reweighted floor samples.
What is whose: P3 the certified constants, band models, evaluator; P6 the closed-form sums and the pair and triple
forms; mine this driver, the Gibbs sampler, the two rules, the window models and the checks.  Nothing is written into
a workstream directory.  Model-relative; the certified constants are P3's paper proofs; two floating-point allowances
are allowances.
Run:  python3 -B serine_helix_reach.py S6 4 5  > serine_helix_reach_S6_m4.log      (enumerable: the driver against A17 (15))
      python3 -B serine_helix_reach.py S12 5 6 > serine_helix_reach_S12_m5.log     (4.9e9 assignments; minutes)
      python3 -B serine_helix_reach.py S12 4 6 > serine_helix_reach_S12_m4.log
      python3 -B serine_helix_reach.py L12 4 11 > serine_helix_reach_L12_m4.log    (leucine, enumerable: where the rules FAIL)
      python3 -B serine_helix_reach.py L30 5 16 H 8 > serine_helix_reach_L30_m5.log (band 16, triple shares within 8; the
          ball is workstream P5's, copied into this script's cache directory)
Arguments: SEQ m w [backbone [w3]];  w3 = window of the triple shares (default w; window_model.triple_form_two_windows).
History: the first run of S12 at order 5 (before the refined rule and the window models were added to this script)
printed the crude prediction and the three brackets with P3's reductions; the same numbers appear in the present logs.
"""
import os, sys, math, json, time, glob, shutil, importlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCI = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(SCI, "ws_P6"))
import p6lib as L
T9 = importlib.import_module("p6_09_triple")
sys.path.insert(0, HERE)
import window_model
pw = L.pw; BETA = L.BETA
WindowModel, build_window_models, diff_window = window_model.make(pw)
CACHE = os.path.join(HERE, "serine_helix_reach_cache"); os.makedirs(CACHE, exist_ok=True)
for src in ("ws_P5", "ws_P6", "ws_P3"):
    for fn in glob.glob(os.path.join(SCI, src, "cache", "atom_*.npz")) + glob.glob(os.path.join(SCI, src, "cache", "zeta_*.npz")):
        dst = os.path.join(CACHE, os.path.basename(fn))
        if not os.path.exists(dst): shutil.copy(fn, dst)
L.encl.CACHE = CACHE; L.MYCACHE = CACHE


def log(s): print(s, flush=True)


def gibbs(G, c0, h, J, x0, k, rng, nchain=16, nsweep=250, burn=50):
    """heat-bath Gibbs sampling of exp(-beta (f + g)); returns the per-site off-anchor frequencies per chain and the
    states of all chains after every sweep past the burn-in."""
    n = len(k); X = np.tile(np.array(x0, dtype=np.int64), (nchain, 1)); cnt = np.zeros((nchain, n)); ns = 0; keep = []
    for sw in range(nsweep):
        for i in range(n):
            C = np.repeat(X, k[i], axis=0); C[:, i] = np.tile(np.arange(k[i]), nchain)
            E = (pw.f_energy(C, c0, h, J) + G.bulk_energy(C)).reshape(nchain, k[i])
            P = np.exp(-BETA * (E - E.min(1, keepdims=True))); P /= P.sum(1, keepdims=True)
            u = rng.random(nchain); X[:, i] = np.minimum((P.cumsum(1) < u[:, None]).sum(1), k[i] - 1)
        if sw >= burn:
            cnt += (X != np.array(x0)[None]); ns += 1; keep.append(X.copy())
    return cnt / ns, np.concatenate(keep, axis=0)


def main():
    seq, m, w = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); bb = sys.argv[4] if len(sys.argv) > 4 else "H"
    w3 = int(sys.argv[5]) if len(sys.argv) > 5 else w                                     # window of the triple shares (<= w)
    tau = 0.60 if ":" in seq else dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)[seq[0]]     # the workstreams' pruning thresholds
    t0 = time.time(); M = m - 1; rng = np.random.default_rng(20261126)
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k)
    dom = float(np.prod([float(v) for v in k]))
    log(f"=== {seq} on {bb}, tau {tau}: {G.nat} atoms, {n} sites, states per site {k}, {dom:.6g} assignments; anchor {''.join(map(str, x0))}, "
        f"E = {E0:.6f} kcal/mol; order m = {m}, band {w}" + (f", triple shares within {w3}" if w3 != w else "") + f" [{time.time() - t0:.0f}s]")
    # ---- (0) the true ensemble, uncertified
    fr, XG = gibbs(G, c0, h, J, x0, k, rng)
    pi = fr.mean(0); noff = fr.sum(1); p = float(noff.mean() / n); se_off = float(noff.std(ddof=1) / math.sqrt(len(noff)))
    log(f"(0) Gibbs sampling of the true ensemble (16 chains, 200 sweeps each after 50): {noff.mean():.3f} +- {se_off:.3f} of {n} side chains off the anchor, "
        f"p = {p:.4f}; by site: " + " ".join(f"{v:.2f}" for v in pi) + f" [{time.time() - t0:.0f}s]")
    # ---- (1) the constant and the prediction
    GF = L.GFBound2(G, x0, L.EnvelopeSup(G), K=m)
    excl = L.exclusion_sets(n, None)
    fps = os.path.join(CACHE, f"pairsums_{seq}_{bb}_m{m}.npz")
    if os.path.exists(fps) and list(np.load(fps)["anchor"]) == [int(v) for v in x0]:
        tot_ex = np.load(fps)["tot"]; srcp = "read from this script's cache"
    else:
        t1 = time.time(); se, cr = L.GFBatch(GF).totals(m, excl); tot_ex = se + cr
        np.savez(fps, tot=tot_ex, anchor=np.array(x0)); srcp = f"computed, {time.time() - t1:.0f}s"
    Gam, S, Gp = L.assemble_pair_sums(n, m, excl, tot_ex)
    val = {tuple(e): float(t) for e, t in zip(excl, tot_ex)}
    pred = {name: 2 * p ** kk * BETA * Gam for name, kk in (("site", 1), ("pair", 2), ("triple", 3), ("envelope", m))}
    log(f"(1) Gamma_{m} = {Gam:.5e} kcal/mol = {BETA * Gam:.4f} kT ({len(excl)} closed-form sums, {srcp}).  PREDICTION by the rule 2 p^k Gamma_m, written before any "
        f"bracket is computed: site {pred['site']:.4g}, pair {pred['pair']:.4g}, triple {pred['triple']:.4g}, envelope {pred['envelope']:.4g} nats "
        f"(the rule knows nothing of the band, of P3's reductions of the evaluated terms, or of the two allowances: the brackets can only be wider) [{time.time() - t0:.0f}s]")
    # ---- (1b) in-window triple sums, the penalty tables of the three forms, and the refined rule -- all before the ball
    tris = T9.window_triples(n, w3); t1 = time.time()
    fpt = os.path.join(CACHE, f"triplesums_{seq}_{bb}_m{m}_w{w3}.npz")
    if os.path.exists(fpt) and list(np.load(fpt)["anchor"]) == [int(v) for v in x0]:
        t3 = np.load(fpt)["tot"]
    else:
        se, cr = L.GFBatch(GF).totals(m, tris); t3 = se + cr; np.savez(fpt, tot=t3, anchor=np.array(x0))
    H = {tr: (val[()] - val[(tr[0],)] - val[(tr[1],)] - val[(tr[2],)] + val[(tr[0], tr[1])] + val[(tr[0], tr[2])] + val[(tr[1], tr[2])]) - float(v)
         for tr, v in zip(tris, t3)}
    phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
    tabs = {"S": (L.site_form(n, m, S, phi1), np.zeros((n, n)), None)}
    tabs["B"] = L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, 5e-9 * Gam) + (None,)
    tabs["T"] = window_model.triple_form_two_windows(T9.window_triples, L.RND, n, m, w, w3, Gp, H, psi1, psi2, 5e-9 * Gam, 1e-8 * Gam)
    pen = {f: (L.penalty_value(XG, x0, tabs[f][0], tabs[f][1]) if f != "T" else T9.penalty_value3(XG, x0, *tabs[f])) for f in "SBT"}
    ref = {f: 2 * BETA * float(pen[f].mean()) for f in "SBT"}
    log(f"(1b) {len(tris)} in-window triple sums [{time.time() - t1:.0f}s]; mean pair sum G_ij by separation 1..{n - 1}: "
        + " ".join(f"{float(np.mean([Gp[i, i + s] for i in range(n - s)])):.2e}" for s in range(1, n)))
    log(f"     REFINED RULE, also before any bracket: 2 beta x mean over the {len(XG)} Gibbs states of the penalty each form charges (band {w}): "
        f"site {ref['S']:.4g}, pair {ref['B']:.4g}, triple {ref['T']:.4g} nats; largest penalty on the sample: "
        + ", ".join(f"{BETA * float(pen[f].max()):.3g}" for f in "SBT") + " kT")
    # ---- (2) the ball
    EG = pw.f_energy(XG, c0, h, J) + G.bulk_energy(XG)          # the true energy at the Gibbs states, for the sandwich checks of (4)
    d, nball, srcb = L.ball_terms(G, x0, M, seq, bb, tau, verbose=False)
    log(f"(2) ball of radius {M}: {nball} evaluations of the solvent term ({100 * nball / dom:.2g} % of the domain; "
        f"{'evaluated now' if srcb == 'evaluated now' else 'read from ' + os.path.basename(srcb)}) [{time.time() - t0:.0f}s]")
    # ---- (4) the three sandwiches
    res = dict(seq=seq, bb=bb, m=m, w=w, n=n, domain=dom, nball=int(nball), Gamma_kT=BETA * Gam, p_gibbs=p, p_site=[float(v) for v in pi], pred=pred, refined=ref, forms={})
    models = {}
    for form, name in (("S", "site penalties (P3)"), ("B", "banded pair penalties (P6)"), ("T", "banded triple penalties (P6)")):
        t1 = time.time()
        if form != "T": lo0, up0 = L.build_models(k, x0, c0, h, J, d, w, M, tabs[form][0], tabs[form][1])
        else: lo0, up0 = T9.build_triple_models(k, x0, c0, h, J, d, w, M, *tabs[form])
        a0, b0 = up0.lnZ(), lo0.lnZ(); l0, u0 = lo0.energy(XG), up0.energy(XG); band0 = BETA * float((u0 - l0).mean())
        v0 = int((l0 > EG + 1e-9).sum() + (u0 < EG - 1e-9).sum())
        lo, up, info = build_window_models(k, x0, c0, h, J, d, w, L.EPS_G, M, *tabs[form])
        a, b = up.lnZ(), lo.lnZ(); models[form] = (lo, up); l1, u1 = lo.energy(XG), up.energy(XG); band = BETA * float((u1 - l1).mean())
        v1 = int((l1 > EG + 1e-9).sum() + (u1 < EG - 1e-9).sum())
        res["forms"][form] = dict(reduced=dict(lnZ_lo=a0, lnZ_hi=b0, width=b0 - a0, mean_band=band0, viol_gibbs=v0),
                                  window=dict(lnZ_lo=a, lnZ_hi=b, width=b - a, mean_band=band, viol_gibbs=v1), info=info)
        log(f"(4) form {form}, {name}; crude rule {pred[dict(S='site', B='pair', T='triple')[form]]:.4g}, refined rule {ref[form]:.4g}:")
        log(f"      with P3's reductions (the workstreams' models): CERTIFIED ln Z(E) in [{a0:.6f}, {b0:.6f}], width {b0 - a0:.6g} nats "
            f"(beta x mean of m_+ - m_- over the Gibbs states: {band0:.4g}; sandwich violated at {v0} of the {len(XG)} Gibbs states)")
        log(f"      with EXACT window terms ({info['exact']} terms of order >= 3 exact, {info['reduced']} reduced, {info['far_pairs']} pairs beyond the band): "
            f"CERTIFIED ln Z(E) in [{a:.6f}, {b:.6f}], width {b - a:.6g} nats (beta x mean of m_+ - m_-: {band:.4g}; sandwich violated at {v1} of the Gibbs states) [{time.time() - t1:.0f}s]")
    # ---- (5) checks on the triple-form sandwich with exact window terms
    lo, up = models["T"]; a, b = up.lnZ(), lo.lnZ(); D = b - a
    xs = lo.sample(4000, rng); Ex = pw.f_energy(xs, c0, h, J) + G.bulk_energy(xs); ml, mu = lo.energy(xs), up.energy(xs)
    wts = np.exp(-BETA * (Ex - ml)); est = b + math.log(wts.mean()); se_est = float(wts.std(ddof=1) / math.sqrt(len(wts)) / wts.mean())
    offx = (xs != np.array(x0)[None]).sum(1)
    p_rw = float((wts * offx).sum() / wts.sum() / n)
    log(f"(5) 4000 exact samples of the floor of the triple form with exact window terms ({len(np.unique(xs, axis=0))} distinct; {offx.mean():.2f} sites off the anchor on average): "
        f"m_- > E at {int((ml > Ex + 1e-9).sum())}, m_+ < E at {int((mu < Ex - 1e-9).sum())}; largest E - m_- = {float((Ex - ml).max()):.4f}, largest m_+ - E = {float((mu - Ex).max()):.4f} kcal/mol")
    log(f"    uncertified estimate by reweighting the floor's samples: ln Z(E) = {est:.6f} +- {se_est:.6f} (inside the certified bracket: {a <= est <= b}); "
        f"p re-estimated from the reweighted samples: {p_rw:.4f} (Gibbs: {p:.4f}) [{time.time() - t0:.0f}s]")
    res["checks"] = dict(viol_lo=int((ml > Ex + 1e-9).sum()), viol_up=int((mu < Ex - 1e-9).sum()), est=est, se=se_est, p_reweighted=p_rw)
    NS = 2000; diff = diff_window(lo, up); acc = []; nprop = 0
    while sum(len(v) for v in acc) < NS and nprop < 2_000_000:
        P = lo.sample(20000, rng); U = BETA * diff.energy(P); ok = rng.random(len(P)) < -np.expm1(-U); acc.append(P[ok]); nprop += len(P)
    A = np.concatenate(acc)[:NS]
    if len(A) == NS:
        EA = pw.f_energy(A, c0, h, J) + G.bulk_energy(A); r = BETA * (EA - lo.energy(A)); U = BETA * (up.energy(A) - lo.energy(A))
        W = np.expm1(-(r - U)) / np.expm1(U); delta = 0.05; t = math.sqrt(math.log(2 / delta) / (2 * NS))
        lz = lambda v: a + math.log1p(math.expm1(D) * min(max(v, 0.0), 1.0))
        log(f"    sandwich sampler (theory division, Proposition 11.113) on that sandwich: {NS} accepted of about {nprop} proposals, "
            f"{len(np.unique(A, axis=0))} distinct states evaluated; W in [{W.min():.3f}, {W.max():.3f}], mean {W.mean():.4f}; W outside [0, 1]: "
            f"{int(((W < -1e-9) | (W > 1 + 1e-9)).sum())};  with probability >= {1 - delta}: ln Z(E) in [{lz(W.mean() - t):.6f}, {lz(W.mean() + t):.6f}], "
            f"width {lz(W.mean() + t) - lz(W.mean() - t):.6f}; point estimate {lz(W.mean()):.6f} [{time.time() - t0:.0f}s]")
        res["sampler"] = dict(N=NS, mean_W=float(W.mean()), lo=lz(W.mean() - t), hi=lz(W.mean() + t), point=lz(W.mean()), outside=int(((W < -1e-9) | (W > 1 + 1e-9)).sum()))
    res["w3"] = w3
    json.dump(res, open(os.path.join(HERE, f"serine_helix_reach_{seq.replace(':', 'c')}_{bb}_m{m}_w{w}.json"), "w"), indent=1)
    log(f"ALL DONE {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
