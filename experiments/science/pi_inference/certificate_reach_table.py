#!/usr/bin/env python3
"""Addendum A17 (16), part C: THE REACH OF THE CERTIFICATE, PREDICTED WITHOUT PAYING FOR IT -- coordinator's script.

For twelve-residue peptides Ace-X12-NMe (and one patterned sequence; serine also at 16 and 20 residues) on a
backbone, at orders m = 4, 5, 6:
  * Gamma_m and the pair and in-window triple sums of workstream P3's certified constants (closed forms, P6; no
    evaluation of the solvent term on a ball);
  * the true ensemble by heat-bath Gibbs sampling (uncertified; 16 chains): the fraction p of side chains off the
    anchor;
  * the crude rule 2 p^k Gamma_m and the refined rule  2 beta E_E[penalty]  for the site, banded pair and banded triple
    forms -- addendum A17 (15) item 35 and A17 (16) part A; the band is the widest one whose transfer arrays stay
    below BUDGET states (all pairs in band for two-state sites, 8 for six-state sites);
  * the size of the ball each order would cost.
Nothing is certified here: the table says which certificates are worth running.  The rules ignore P3's reductions of
the evaluated terms to the band model (they need the ball); where a certificate has been run the two are compared in
the addendum.  Model-relative.
Run:  python3 -B certificate_reach_table.py H  > certificate_reach_table_H.log      (helix; tens of minutes on one core)
      python3 -B certificate_reach_table.py P2 > certificate_reach_table_P2.log
"""
import os, sys, math, json, time, glob, shutil, importlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCI = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(SCI, "ws_P6"))
import p6lib as L
T9 = importlib.import_module("p6_09_triple")
pw = L.pw; BETA = L.BETA
CACHE = os.path.join(HERE, "serine_helix_reach_cache"); os.makedirs(CACHE, exist_ok=True)
for src in ("ws_P5", "ws_P6", "ws_P3"):
    for fn in glob.glob(os.path.join(SCI, src, "cache", "atom_*.npz")) + glob.glob(os.path.join(SCI, src, "cache", "zeta_*.npz")):
        dst = os.path.join(CACHE, os.path.basename(fn))
        if not os.path.exists(dst): shutil.copy(fn, dst)
L.encl.CACHE = CACHE; L.MYCACHE = CACHE
sys.path.insert(0, HERE)
from serine_helix_reach import gibbs
BUDGET = 2.0e7          # largest transfer array (states of a window of w + 1 consecutive sites) the band is allowed to need


def band_for(k):
    """the widest band w <= n - 1 whose windows of w + 1 consecutive sites have at most BUDGET states."""
    n = len(k); best = 1
    for w in range(1, n):
        if max(float(np.prod([float(v) for v in k[i:i + w + 1]])) for i in range(n - w)) <= BUDGET: best = w
    return best


def log(s): print(s, flush=True)


def ball(ks, r):
    e = [1] + [0] * r
    for kk in ks:
        for j in range(r, 0, -1): e[j] += e[j - 1] * (kk - 1)
    return sum(e)


def main():
    bb = sys.argv[1] if len(sys.argv) > 1 else "H"
    insts = [a for a in sys.argv[2:]] or ["S12", "V12", "L12", "F12", "K12", "LKSE:12", "S16", "S20"]
    TAU = dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)
    t0 = time.time(); out = []
    log(f"# backbone {bb}; band for the pair and triple forms: the widest whose windows have at most {BUDGET:.0e} states; widths in nats.  Columns: instance | assignments | p (Gibbs) | then per order m: "
        "Gamma_m (kT) | crude rule 2 p^k Gamma_m, k = 1, 2, 3 | REFINED rule 2 beta E[penalty]: site, banded pair, banded triple | ball of radius m - 1")
    for seq in insts:
        tau = 0.60 if ":" in seq else TAU[seq[0]]
        try:
            G, c0, h, J, x0, E0 = L.setup(seq, bb, tau)
        except Exception as e:
            log(f"{seq}/{bb}: setup failed ({type(e).__name__}: {e}) -- skipped"); continue
        n, k = G.ns, list(G.k); dom = float(np.prod([float(v) for v in k])); rng = np.random.default_rng(20261126)
        nsw = 250 if sum(k) <= 100 else 150; W = band_for(k)
        fr, XG = gibbs(G, c0, h, J, x0, k, rng, nchain=16, nsweep=nsw, burn=50)
        noff = fr.sum(1); p = float(noff.mean() / n)
        log(f"{seq}/{bb} tau {tau}: {G.nat} atoms, states per site {min(k)}..{max(k)}, {dom:.3g} assignments; band {W}; Gibbs ({len(XG)} states): "
            f"{noff.mean():.2f} +- {noff.std(ddof=1) / 4:.2f} of {n} off the anchor, p = {p:.3f} (by site {' '.join(f'{v:.2f}' for v in fr.mean(0))}) [{time.time() - t0:.0f}s]")
        row = dict(seq=seq, bb=bb, tau=tau, n=n, k=k, domain=dom, band=W, p=p, p_site=[float(v) for v in fr.mean(0)], orders={})
        for m in (4, 5, 6):
            t1 = time.time(); M = m - 1
            GF = L.GFBound2(G, x0, L.EnvelopeSup(G), K=m)
            excl = L.exclusion_sets(n, None); se, cr = L.GFBatch(GF).totals(m, excl); tot_ex = se + cr
            Gam, S, Gp = L.assemble_pair_sums(n, m, excl, tot_ex); val = {tuple(e): float(t) for e, t in zip(excl, tot_ex)}
            tris = T9.window_triples(n, W); se, cr = L.GFBatch(GF).totals(m, tris)
            H = {tr: (val[()] - val[(tr[0],)] - val[(tr[1],)] - val[(tr[2],)] + val[(tr[0], tr[1])] + val[(tr[0], tr[2])] + val[(tr[1], tr[2])]) - float(v)
                 for tr, v in zip(tris, se + cr)}
            phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
            gsS = L.site_form(n, m, S, phi1); gsB, g2B = L.banded_pair_form(n, m, W, S, Gp, psi1, psi2, 5e-9 * Gam)
            gsT, g2T, eta = T9.triple_form(n, m, W, Gp, H, psi1, psi2, 5e-9 * Gam, 1e-8 * Gam)
            ref = dict(site=2 * BETA * float(L.penalty_value(XG, x0, gsS, np.zeros((n, n))).mean()),
                       pair=2 * BETA * float(L.penalty_value(XG, x0, gsB, g2B).mean()),
                       triple=2 * BETA * float(T9.penalty_value3(XG, x0, gsT, g2T, eta).mean()))
            crude = [2 * p ** kk * BETA * Gam for kk in (1, 2, 3)]; nb = ball(k, M)
            row["orders"][m] = dict(Gamma_kT=BETA * Gam, crude=crude, refined=ref, ball=nb)
            log(f"    m = {m}: Gamma = {BETA * Gam:10.4g} kT | crude {crude[0]:9.3g} {crude[1]:9.3g} {crude[2]:9.3g} | refined {ref['site']:9.3g} {ref['pair']:9.3g} {ref['triple']:9.3g} "
                f"| ball {nb:.3g} ({100 * nb / dom:.2g} % of the domain) [{time.time() - t1:.0f}s]")
        out.append(row)
        json.dump(out, open(os.path.join(HERE, f"certificate_reach_table_{bb}.json"), "w"), indent=1)
    log(f"ALL DONE {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
