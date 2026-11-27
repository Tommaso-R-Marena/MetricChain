#!/usr/bin/env python3
"""Addendum A17 (14): THE LEUCINE HELIX WITH PAIR SHARES AT ORDERS 5 AND 6 -- coordinator's script, combining two workstreams.

Workstream P5 certified Ace-Leu_n-NMe on the helix (n = 12, 16, 20, 30) with workstream P3's unchanged pipeline at order 6
and SITE penalties (thirty residues: ln Z in [866.6507, 867.3804], 0.73 nats, from the 174 437 evaluations of the ball of
radius 5).  Workstream P6 proved and validated the banded PAIR form of the same penalties and found on the enumerated
Leu16 helix 0.523 -> 0.0150 nats at order 6 and 6.05 -> 0.068 at order 5.  Neither ran the pair form beyond sixteen
residues.  Here: the pair form on P5's cached balls for twenty and thirty residues -- NO new evaluation of the solvent
term for the deterministic brackets (the ball of radius 4 is a prefix of the ball of radius 5).

What is whose.  P3: the certified constants (gfbound, encl), the band models and transfer matrix (pwmodel), the evaluator.
P6: the closed-form sums with excluded sites (GFBound2, GFBatch), the pair allocation (banded_pair_form, build_models).
P5: the evaluated balls (ws_P5/cache/ball_L*_H_*_M5_*.npz), read here and not regenerated.  Mine: this driver, the
comparison with P5's site-form numbers, the sampled checks.  Nothing is written into a workstream directory: the
enclosure cache is redirected to ./helix_pair_form_cache (copies of the workstreams' tables), where the pair sums are
kept as well.
Run:  python3 -B helix_pair_form.py L20 6 19 > helix_pair_form_L20_m6.log     (minutes)
      python3 -B helix_pair_form.py L30 6 20 > helix_pair_form_L30_m6.log     (tens of minutes: 421 closed-form sums)
      python3 -B helix_pair_form.py L30 5 20 > helix_pair_form_L30_m5.log
"""
import os, sys, math, json, time, glob, shutil, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCI = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(SCI, "ws_P6"))
import p6lib as L
pw = L.pw; BETA = L.BETA
CACHE = os.path.join(HERE, "helix_pair_form_cache"); os.makedirs(CACHE, exist_ok=True)
for src in ("ws_P5", "ws_P6", "ws_P3"):
    for fn in glob.glob(os.path.join(SCI, src, "cache", "atom_*.npz")) + glob.glob(os.path.join(SCI, src, "cache", "zeta_*.npz")):
        dst = os.path.join(CACHE, os.path.basename(fn))
        if not os.path.exists(dst): shutil.copy(fn, dst)
L.encl.CACHE = CACHE


def log(s): print(s, flush=True)


def main():
    seq, m, w = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); bb, tau = "H", 0.60
    NS = int(sys.argv[4]) if len(sys.argv) > 4 else 1200
    t0 = time.time(); M = m - 1
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k)
    log(f"=== {seq} on the helix, tau {tau}: {G.nat} atoms, {n} sites, states per site {sorted(set(k))}, {float(np.prod([float(v) for v in k])):.6g} assignments; "
        f"anchor E = {E0:.6f} kcal/mol; order m = {m}, band {w} [{time.time() - t0:.0f}s]")
    # ---- P5's numbers (site form, order 6) for comparison
    p5 = None; fn5 = os.path.join(SCI, "ws_P5", "out", f"floor_{seq}_H_t0.60_gbn2_m6_siteres.json")
    if os.path.exists(fn5):
        p5 = json.load(open(fn5)); assert list(p5["anchor"]) == [int(v) for v in x0], "anchor differs from P5's"
    # ---- the ball: P5's cache, prefix of radius M
    blocks, tot = pw.ball_states(k, x0, M); allst = np.concatenate([b for _, b in blocks], axis=0)
    ah = hashlib.sha1(str((tuple(x0), [list(map(int, dd)) for dd in G.dom])).encode()).hexdigest()[:10]
    fb = os.path.join(SCI, "ws_P5", "cache", f"ball_{seq}_H_t0.60_gbn2_M5_{ah}.npz")
    z = np.load(fb); assert z["states"].shape[0] >= tot and np.array_equal(z["states"][:tot], allst), "P5's ball is not a prefix-compatible ball"
    vals = np.array(z["vals"][:tot], dtype=float)
    rng = np.random.default_rng(20261126); chk = rng.choice(tot, 60, replace=False)
    dev = float(np.abs(G.bulk_energy(allst[chk]) - vals[chk]).max())
    log(f"    ball of radius {M}: {tot} values read from workstream P5's cache ({os.path.basename(fb)}, {z['states'].shape[0]} stored); "
        f"60 of them re-evaluated here: largest difference {dev:.1e} kcal/mol [{time.time() - t0:.0f}s]")
    lut = {st.tobytes(): v for st, v in zip(allst.astype(np.int16), vals)}
    d, nb, _ = pw.anchored_terms(G, x0, M, energy=lambda st: np.array([lut[row.tobytes()] for row in np.atleast_2d(st).astype(np.int16)]), cache_file=None)
    assert nb == tot
    # ---- certified constants: closed-form sums with excluded sites (P6), in-band pairs only
    GF = L.GFBound2(G, x0, L.EnvelopeSup(G), K=m)
    fps = os.path.join(CACHE, f"pairsums_{seq}_H_m{m}_w{w}.npz")
    excl = L.exclusion_sets(n, w)
    if os.path.exists(fps) and list(np.load(fps)["anchor"]) == [int(v) for v in x0]:
        tot_ex = np.load(fps)["tot"]; srcp = "read from this script's cache"
    else:
        t1 = time.time()
        se, cr = L.GFBatch(GF).totals(m, excl, progress=max(1, n // 5))
        tot_ex = se + cr
        np.savez(fps, tot=tot_ex, anchor=np.array(x0), excl=np.array([list(e) + [-1] * (2 - len(e)) for e in excl]))
        srcp = f"computed, {time.time() - t1:.0f}s"
    Gam, S, Gp = L.assemble_pair_sums(n, m, excl, tot_ex)
    log(f"    Gamma_{m} = {Gam:.5f} kcal/mol = {BETA * Gam:.3f} kT from {len(excl)} closed-form sums ({srcp}); largest site share S_i/m = {S.max() / m:.4f}, "
        f"largest in-band pair share = {np.nanmax(Gp) / math.comb(m, 2):.5f} kcal/mol [{time.time() - t0:.0f}s]")
    phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
    res = dict(seq=seq, m=m, w=w, n=n, nball=int(tot), Gamma=Gam, forms={})
    models = {}
    for form in ("S", "B"):
        if form == "S": gs, g2 = L.site_form(n, m, S, phi1), np.zeros((n, n))
        else: gs, g2 = L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, 5e-9 * Gam)
        lo, up = L.build_models(k, x0, c0, h, J, d, w, M, gs, g2)
        a, b = up.lnZ(), lo.lnZ(); models[form] = (lo, up)
        res["forms"][form] = dict(lnZ_lo=a, lnZ_hi=b, width=b - a, min_lower=lo.minimum())
        extra = ""
        if form == "S" and p5 is not None and m == 6 and w == p5["w"]:
            extra = f";  workstream P5's run of P3's pipeline: [{p5['lnZ_upper_model']:.6f}, {p5['lnZ_lower_model']:.6f}] (differences {a - p5['lnZ_upper_model']:+.1e}, {b - p5['lnZ_lower_model']:+.1e})"
        log(f"    form {form} ({'site penalties, P3/P5' if form == 'S' else 'banded pair penalties, P6'}): CERTIFIED ln Z(E) in [{a:.6f}, {b:.6f}], width {b - a:.6f} nats; "
            f"min m_- = {lo.minimum():.6f} (anchor E = {E0:.6f}){extra} [{time.time() - t0:.0f}s]")
    # ---- sampled checks on the pair-form sandwich: exact samples of the floor; the theory division's sandwich sampler
    lo, up = models["B"]; a, b = up.lnZ(), lo.lnZ(); D = b - a
    xs = lo.sample(1000, rng); Ex = pw.f_energy(xs, c0, h, J) + G.bulk_energy(xs); ml, mu = lo.energy(xs), up.energy(xs)
    off = float((xs != np.array(x0)[None]).sum(1).mean())
    log(f"    1000 exact samples of the pair-form floor ({len(np.unique(xs, axis=0))} distinct; {off:.2f} sites off the anchor on average): "
        f"m_- > E at {int((ml > Ex + 1e-9).sum())}, m_+ < E at {int((mu < Ex - 1e-9).sum())} [{time.time() - t0:.0f}s]")
    diff = L.diff_model(lo, up); acc = []; nprop = 0
    while sum(len(v) for v in acc) < NS and nprop < 4_000_000:
        P = lo.sample(20000, rng); U = BETA * diff.energy(P); ok = rng.random(len(P)) < -np.expm1(-U); acc.append(P[ok]); nprop += len(P)
    A = np.concatenate(acc)[:NS]
    if len(A) == NS:
        EA = pw.f_energy(A, c0, h, J) + G.bulk_energy(A); r = BETA * (EA - lo.energy(A)); U = BETA * (up.energy(A) - lo.energy(A))
        W = np.expm1(-(r - U)) / np.expm1(U); delta = 0.05; t = math.sqrt(math.log(2 / delta) / (2 * NS))
        lz = lambda v: a + math.log1p(math.expm1(D) * min(max(v, 0.0), 1.0))
        log(f"    sandwich sampler (theory division, Proposition 11.113) on the pair-form sandwich: {NS} accepted of about {nprop} proposals "
            f"(rate 1 - e^-D = {-math.expm1(-D):.4f}), {len(np.unique(A, axis=0))} distinct states evaluated; W in [{W.min():.3f}, {W.max():.3f}], mean {W.mean():.4f}; "
            f"W outside [0, 1]: {int(((W < -1e-9) | (W > 1 + 1e-9)).sum())};  with probability >= {1 - delta}: ln Z(E) in [{lz(W.mean() - t):.6f}, {lz(W.mean() + t):.6f}], "
            f"width {lz(W.mean() + t) - lz(W.mean() - t):.6f}; point estimate {lz(W.mean()):.6f} [{time.time() - t0:.0f}s]")
        res["sampler"] = dict(N=NS, mean_W=float(W.mean()), lo=lz(W.mean() - t), hi=lz(W.mean() + t), outside=int(((W < -1e-9) | (W > 1 + 1e-9)).sum()))
    json.dump(res, open(os.path.join(HERE, f"helix_pair_form_{seq}_m{m}.json"), "w"), indent=1)
    log(f"ALL DONE {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
