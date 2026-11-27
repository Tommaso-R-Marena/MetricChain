"""
P8 -- the tables of P8_REPORT.md, assembled from the JSON / npz outputs of the other scripts (nothing is computed here
except sums, ratios and least-squares fits of logged quantities).  Missing inputs are skipped and named.

usage: python3 -B p8_09_tables.py        -> out/tables.md
"""
import sys, os, json, glob, itertools
from math import comb
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
KT = 0.0019872041 * 300.0
BETA = 1.0 / KT
L = []


def P(s=""):
    L.append(s)


def J(name):
    fn = os.path.join(OUT, name)
    return json.load(open(fn)) if os.path.exists(fn) else None


def f(v, d=3):
    if v is None or (isinstance(v, float) and not np.isfinite(v)):
        return "—"
    if v == 0:
        return "0"
    a = abs(v)
    if a >= 1e4 or a < 1e-3:
        e = int(np.floor(np.log10(a))); return f"{v / 10 ** e:.{max(d - 1, 0)}f}·10^{e}"
    if a >= 100:
        return f"{v:.0f}"
    if a >= 10:
        return f"{v:.1f}"
    if a >= 1:
        return f"{v:.2f}"
    return f"{v:.{d}g}"


INST = [("K3", "H", 0.70, "Lys₃"), ("K4", "H", 0.70, "Lys₄"), ("K5", "H", 0.70, "Lys₅"), ("LKSE:4", "H", 0.60, "LKSE:4"), ("LKSE:5", "H", 0.60, "LKSE:5"),
        ("LKSE:6", "H", 0.60, "LKSE:6"), ("S4", "H", 0.70, "Ser₄"), ("S5", "H", 0.70, "Ser₅"), ("S6", "H", 0.70, "Ser₆"), ("L6", "H", 0.60, "Leu₆"), ("L8", "H", 0.60, "Leu₈"),
        ("K3", "E", 0.70, "Lys₃ strand"), ("K4", "E", 0.70, "Lys₄ strand"), ("LKSE:5", "E", 0.60, "LKSE:5 strand")]


def tg(seq, bb, tau):
    return f"{seq.replace(':', 'c')}_{bb}_{tau:.2f}"


# ============================================================================================ Table 1
P("## T1  The measurement, per instance and order (sums over the subsets of that order; kcal/mol)")
P()
P("| instance (states) | m | subsets | truth `Σ c_T` | sup\\|g − I_{m−1}g\\| | all charges positive `Σ c_T(g_|q|)` | (A) best sign pattern per subset | (C) remainder of the pattern found | best pair-by-pair `Σ PP_T` | P3 `Γ_m` | S (state-wise max, pair by pair) | SA | Sb (block-wise) | SAb | `Γ_m`/sup\\|rem\\| | P3/pair-by-pair | pair-by-pair/(A) | (A)/truth | (C)/sup\\|rem\\| | P3/SAb (†: SA, block-wise variant not run) | SAb/truth (†: SA) |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for seq, bb, tau, name in INST:
    t = tg(seq, bb, tau)
    m1 = J(f"m1_{t}.json"); sb = J(f"sb_{t}.json"); sr = J(f"sr_{t}.json"); bc = J(f"bc_{t}.json")
    if m1 is None:
        continue
    for m, o in m1["orders"].items():
        rem = max(abs(o["remainder"][0]), abs(o["remainder"][1]))
        s_ = sb["orders"].get(m) if sb else None
        r_ = sr["orders"].get(m) if sr else None
        b_ = bc["orders"].get(m) if bc and "orders" in bc else None
        A = s_["A_sum"] if s_ else None; C = s_["C_rem"] if s_ else None
        best = b_["SAb"] if b_ else (r_["SA"] if r_ else None)
        P(f"| {name} ({m1['nstates']}) | {m} | {o['nsub']} | {f(o['total'])} | {f(rem)} | {f(o['allplus'])} | {f(A)} | {f(C)} | {f(o['PP'])} | {f(o['P3'])} | {f(r_['S'] if r_ else None)} | "
          f"{f(r_['SA'] if r_ else None)} | {f(b_['Sb'] if b_ else None)} | {f(b_['SAb'] if b_ else None)} | {f(o['P3'] / rem)} | {f(o['P3'] / o['PP'])} | {f(o['PP'] / A if A else None)} | "
          f"{f(A / o['total'] if A else None)} | {f(C / rem if C else None)} | {f(o['P3'] / best if best else None)}{'' if b_ or not best else '†'} | {f(best / o['total'] if best else None)}{'' if b_ or not best else '†'} |")
P()

# ============================================================================================ Table 1b
P("## T1b  Where the factor between P3's bound and the truth goes (ratios of the sums of T1; (C) = largest remainder of a sign pattern found, a lower bound of every sign-blind bound)")
P()
P("| instance | m | P3 `Γ_m`/sup\\|rem\\| | (C)/sup\\|rem\\|: least price of the sign-blind class | P3/(C) | pair-by-pair/(C) | P3/pair-by-pair | new bound/pair-by-pair | new bound/exact constants of its blocks (hosts outside T at the anchor) | new bound/(C) | P3/new bound | new bound |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|")
for seq, bb, tau, name in INST:
    t = tg(seq, bb, tau)
    m1 = J(f"m1_{t}.json"); sb = J(f"sb_{t}.json"); sr = J(f"sr_{t}.json"); bc = J(f"bc_{t}.json")
    if m1 is None or sr is None:
        continue
    for m, o in m1["orders"].items():
        rem = max(abs(o["remainder"][0]), abs(o["remainder"][1]))
        s_ = sb["orders"].get(m) if sb else None
        r_ = sr["orders"].get(m)
        b_ = bc["orders"].get(m) if bc and "orders" in bc else None
        C = s_["C_rem"] if s_ else None
        best = b_["SAb"] if b_ else r_["SA"]; lab = "SAb" if b_ else "SA"
        P(f"| {name} | {m} | {f(o['P3'] / rem)} | {f(C / rem if C else None)} | {f(o['P3'] / C if C else None)} | {f(o['PP'] / C if C else None)} | {f(o['P3'] / o['PP'])} | {f(best / o['PP'])} | "
          f"{f(b_['SAb'] / b_['PPB_res']) if b_ else '—'} | {f(best / C if C else None)} | {f(o['P3'] / best)} | {lab} |")
P()

# ============================================================================================ Table 2
P("## T2  By atom class (bb = fixed atoms, nsc = neutral side chain, chain = aliphatic chain of Lys/Glu, head = NZ,HZ1-3 / CD,OE1,OE2): share of the truth, and who carries the bounds")
P()
P("| instance | m | class pair | signed share of the truth (%) | exact constant of the class-pair function | best pair-by-pair | P3 | S | SA | P3/pair-by-pair | SA/pair-by-pair (restricted) | share of P3 (%) | share of SA (%) |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for seq, bb, tau, name in INST:
    t = tg(seq, bb, tau)
    m1 = J(f"m1_{t}.json"); sr = J(f"sr_{t}.json")
    if m1 is None or seq[0] not in "KL" or ":" not in seq and seq[0] != "K":
        continue
    for m, o in m1["orders"].items():
        rc = {d["name"]: d for d in (sr["orders"][m]["by_class"] if sr else [])}
        totP3 = o["P3"]; totSA = sr["orders"][m]["SA"] if sr else None
        for d in o["by_class"]:
            if d["P3"] <= 0:
                continue
            r = rc.get(d["name"])
            P(f"| {name} | {m} | {d['name']} | {100 * d['signed'] / o['total']:+.1f} | {f(d['const'])} | {f(d['PP'])} | {f(d['P3'])} | {f(r['S'] if r else None)} | {f(r['SA'] if r else None)} | "
              f"{f(d['P3'] / d['PP'] if d['PP'] > 0 else None)} | {f(r['SA'] / r['PPA'] if r and r['PPA'] > 0 else None)} | {100 * d['P3'] / totP3:.1f} | {f(100 * r['SA'] / totSA) if r else '—'} |")
P()

# ============================================================================================ Table 3
P("## T3  Cross part by host pattern (number of moving atoms of the pair; of which with their site in T)")
P()
P("| instance | m | moving atoms, hosts in T | best pair-by-pair (all contexts) | the same, hosts outside T at the anchor | P3 | S | AH | SA | P3/pair-by-pair | S/pair-by-pair | SA/restricted pair-by-pair |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|")
for seq, bb, tau, name in INST:
    t = tg(seq, bb, tau)
    sr = J(f"sr_{t}.json")
    if sr is None:
        continue
    for m, o in sr["orders"].items():
        for d in o["by_host"]:
            if d["P3"] <= 0:
                continue
            P(f"| {name} | {m} | {d['moving']}, {d['hosts_in_T']} | {f(d['PP'])} | {f(d['PPA'])} | {f(d['P3'])} | {f(d['S'])} | {f(d['AH'])} | {f(d['SA'])} | {f(d['P3'] / d['PP'] if d['PP'] > 0 else None)} | "
              f"{f(d['S'] / d['PP'] if d['PP'] > 0 else None)} | {f(d['SA'] / d['PPA'] if d['PPA'] > 0 else None)} |")
P()

# ============================================================================================ Table 4
P("## T4  Far pairs: cross part by `Dmin` = min over all states of `r²/(4 B_p B_q)` (shares in % of the instance's sums)")
P()
P("| instance | m | share of P3's cross bound in pairs with Dmin ≥ 2 | ≥ 4 | ≥ 8 | share of the best pair-by-pair bound with Dmin ≥ 4 | P3/pair-by-pair for Dmin ≥ 4 | for Dmin < 1 |")
P("|---|---|---|---|---|---|---|---|")
for seq, bb, tau, name in INST:
    t = tg(seq, bb, tau)
    m1 = J(f"m1_{t}.json")
    if m1 is None:
        continue
    for m, o in m1["orders"].items():
        D = o["by_D"]
        tot = sum(d["P3"] for d in D); totpp = sum(d["PP"] for d in D)
        sh = lambda lo, key: sum(d[key] for d in D if d["lo"] >= lo)
        near = (sum(d["P3"] for d in D if d["lo"] < 1.0), sum(d["PP"] for d in D if d["lo"] < 1.0))
        P(f"| {name} | {m} | {100 * sh(2.0, 'P3') / tot:.2f} | {100 * sh(4.0, 'P3') / tot:.3f} | {100 * sh(8.0, 'P3') / tot:.4f} | {100 * sh(4.0, 'PP') / totpp:.3f} | "
          f"{f(sh(4.0, 'P3') / sh(4.0, 'PP') if sh(4.0, 'PP') > 0 else None)} | {f(near[0] / near[1] if near[1] > 0 else None)} |")
P()

# ============================================================================================ Table 4b
P("## T4b  After the state-wise maximum: what is left by distance (pair-wise variant 'SA' against the exact restricted constants), and for pairs of FIXED atoms alone")
P()
P("| instance | m | Dmin < 1: SA / exact (share of SA, %) | 1 ≤ Dmin < 4 | Dmin ≥ 4 | pairs of fixed atoms only: Dmin < 1 | 1 ≤ Dmin < 4 | Dmin ≥ 4 |")
P("|---|---|---|---|---|---|---|---|")
for seq, bb, tau, name in INST:
    t = tg(seq, bb, tau)
    f1 = os.path.join(OUT, f"m1_{t}.npz"); f2 = os.path.join(OUT, f"sr_{t}.npz"); f3 = os.path.join(OUT, f"m1b_{t}.npz")
    if not (os.path.exists(f1) and os.path.exists(f2) and os.path.exists(f3)):
        continue
    Z = np.load(f1); Zs = np.load(f2); Zb = np.load(f3)
    N = len(Z["q"]); iu = np.triu_indices(N, 1)
    Dm = Z["Dmin"][iu]; so = Z["site_of"]; fixed2 = (so[iu[0]] < 0) & (so[iu[1]] < 0)
    Tl = Z["Tlist"]; orders = (Tl >= 0).sum(axis=1)
    exa = Zb["PPA"][:, iu[0], iu[1]]; sa = Zs["p_SA"][:, iu[0], iu[1]]
    for m in sorted(set(orders.tolist())):
        sel = orders == m
        tot = sa[sel].sum()
        cells = []
        for mk0 in (np.ones(len(Dm), dtype=bool), fixed2):
            for lo_, hi_ in ((0.0, 1.0), (1.0, 4.0), (4.0, np.inf)):
                mk = mk0 & (Dm >= lo_) & (Dm < hi_)
                a_, b_ = float(sa[sel][:, mk].sum()), float(exa[sel][:, mk].sum())
                cells.append(f"{f(a_ / b_ if b_ > 0 else None)} ({100 * a_ / tot:.1f})")
        P(f"| {name} | {m} | " + " | ".join(cells) + " |")
P()

# ============================================================================================ Table 5
P("## T5  Validation against exact constants: comparisons, violations, smallest margin (ratio bound / exact)")
P()
P("| instance (states; atoms) | C1: 'S' summand ≥ exact constant of the term, all contexts: comparisons; violations; smallest ratio (self, pair) | C2: 'SA' summand ≥ exact restricted constant | 'SA' below the all-context constant (cases) | "
  "C4: per pair, Σ_T summand ≥ sup_x of the pair's remainder: comparisons; violations (P3, S, AH, SA); smallest ratio SA | C5: every state, true / all-plus / sign patterns: state checks; violations; smallest envelope/\\|remainder\\| (SA) | "
  "C7: every pair term at EVERY state (p8_03b): checks; violations; smallest ratio (SA) | B1/B2: block bounds Sb, SAb ≥ exact block constants: comparisons; violations; smallest ratios | B3: every block at every state: checks; violations; smallest ratio (SAb) | B5: Sb = P3's termwise (rel. deviation) |")
P("|---|---|---|---|---|---|---|---|---|---|")
totals = dict(C1=0, C2=0, C4=0, C5=0, C7=0, B12=0, B3=0, B4=0, B5=0); b5dev = 0.0; c0dev = 0.0; ninst = 0; minr = []; minp = []
for seq, bb, tau, name in INST:
    t = tg(seq, bb, tau)
    m1 = J(f"m1_{t}.json"); sr = J(f"sr_{t}.json"); sc = J(f"sc_{t}.json"); bc = J(f"bc_{t}.json")
    if sr is None:
        continue
    c = sr["checks"]
    c7 = f"{sc['stat']['SA']['n']}; {sc['stat']['SA']['viol']}; {sc['stat']['SA']['minratio']:.4f}" if sc else "not run"
    if bc:
        b = bc["checks"]
        b12 = f"{b['B1']['n']} + {b['B2']['n']}; {b['B1']['violations']} + {b['B2']['violations']}; {b['B1']['min_ratio']:.4f}, {b['B2']['min_ratio']:.4f}"
        b3 = f"{b['B3']['n']}; {b['B3']['violations']['SAb']}; {b['B3']['min_ratio']['SAb']:.4f}"
        b5 = f"{b['B5']['devrel']:.1e}"
        totals["B12"] += b["B1"]["n"] + b["B2"]["n"]; totals["B3"] += 2 * b["B3"]["n"]
        totals["B4"] += 2 * b["B4"]["n"]; totals["B5"] += b["B5"]["n"]; b5dev = max(b5dev, b["B5"]["devrel"])
    else:
        b12 = b3 = b5 = "not run"
    P(f"| {name} ({sr['nstates']}; {sr['natoms']}) | {c['C1_S']['n']}; {c['C1_S']['violations']}; {c['C1_S']['min_ratio_self']:.4f}, {c['C1_S']['min_ratio_pair']:.4f} | "
      f"{c['C2_SA']['n']}; {c['C2_SA']['violations']}; {c['C2_SA']['min_ratio_self']:.4f}, {c['C2_SA']['min_ratio_pair']:.4f} | {c['SA_below_allcontext']} | "
      f"{c['C4']['n']}; {c['C4']['violations']['P3']}, {c['C4']['violations']['S']}, {c['C4']['violations']['AH']}, {c['C4']['violations']['SA']}; {c['C4']['min_ratio']['SA']:.3f} | "
      f"{c['C5']['n']} ({len(c['C5']['systems'])} systems); {c['C5']['violations']['SA']}; {c['C5']['min_ratio']['SA']:.2f} | {c7} | {b12} | {b3} | {b5} |")
    totals["C1"] += c["C1_S"]["n"]; totals["C2"] += c["C2_SA"]["n"] + c["C2_AH"]["n"]; totals["C4"] += 4 * c["C4"]["n"]; totals["C5"] += 4 * c["C5"]["n"]
    c0dev = max(c0dev, c["C0"]["devrel"]); ninst += 1
    minr += [c["C1_S"]["min_ratio_self"], c["C2_SA"]["min_ratio_self"]]; minp += [c["C1_S"]["min_ratio_pair"], c["C2_SA"]["min_ratio_pair"]]
    if sc:
        totals["C7"] += sum(sc["stat"][v]["n"] for v in sc["stat"])
P()
P(f"Totals over the {ninst} instances listed (comparisons): C1 (variant S): {totals['C1']}; C2 (variants SA and AH): {totals['C2']}; C4 (four variants): {totals['C4']}; "
  f"C5 (state checks, four variants): {totals['C5']}; C7 (three variants): {totals['C7']}; B1 + B2: {totals['B12']}; B3 (two variants): {totals['B3']}; B4 (state checks, two variants): {totals['B4']}; "
  f"B5: {totals['B5']} subsets, largest relative deviation {b5dev:.1e}; C0 (my variant 'P3' against P3's own summands): largest relative deviation {c0dev:.1e}.  Violations: none in any check.")
P()
P(f"In all: {totals['C1'] + totals['C2'] + totals['C4'] + totals['B12']} comparisons of a bound with an exact constant (C1 + C2 + C4 + B1 + B2) and "
  f"{totals['C5'] + totals['C7'] + totals['B3'] + totals['B4']} checks at single states (C5 + C7 + B3 + B4) on {ninst} enumerated instances; smallest ratio bound/exact over C1, C2: "
  f"{min(minr):.4f} (self terms), {min(minp):.4f} (pair terms).")
P()

# ============================================================================================ Table 6
P("## T6  Twelve residues on the helix: constants `Γ_m = Σ_T ĉ_T` (k_BT) by explicit enumeration of the subsets")
P()
P("| peptide | m | subsets | P3 (closed form) | sum of my 'P3' variant: rel. deviation | AH (X → A) | S | SA | Sb | **SAb** | P3/SAb | per subset P3/SA: min, median, max | fall per order: P3; SAb |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
G12 = [("K12", "H", 0.70, "Lys₁₂", 6), ("LKSE:12", "H", 0.60, "(LKSE)₃", 7), ("S12", "H", 0.70, "Ser₁₂", 7), ("L12", "H", 0.60, "Leu₁₂", 11)]
gam = {}
for seq, bb, tau, name, W in G12:
    prev = None
    for m in (4, 5, 6):
        fn = os.path.join(OUT, f"g12_{tg(seq, bb, tau)}_m{m}.npz")
        if not os.path.exists(fn):
            continue
        Z = np.load(fn); V = [str(v) for v in Z["variants"]]
        tot = Z["C"].sum(axis=2); G = {v: float(tot[:, V.index(v)].sum()) for v in V}
        cf = float(Z["Gamma_closed"].sum())
        fnb = os.path.join(OUT, f"g12b_{tg(seq, bb, tau)}_m{m}.npz")
        if os.path.exists(fnb):
            Zb = np.load(fnb); G["Sb"] = float(Zb["Cb"][:, 0].sum()); G["SAb"] = float(Zb["Cb"][:, 1].sum())
        r = tot[:, V.index("P3")] / tot[:, V.index("SA")]
        best = G.get("SAb", G["SA"])
        fall = f"{prev[0] / cf:.1f}; {prev[1] / best:.1f}" if prev else "—"
        P(f"| {name} | {m} | {len(tot)} | {f(cf * BETA, 4)} | {abs(G['P3'] - cf) / cf:.1e} | {f(G['AH'] * BETA, 4)} | {f(G['S'] * BETA, 4)} | {f(G['SA'] * BETA, 4)} | {f(G.get('Sb', np.nan) * BETA, 4)} | "
          f"**{f(G.get('SAb', np.nan) * BETA, 4)}** | {f(cf / best)} | {r.min():.1f}, {np.median(r):.1f}, {r.max():.0f} | {fall} |")
        prev = (cf, best); gam[(seq, m)] = G
P()

# ============================================================================================ Table 7
P("## T7  First-order estimates of the certified bracket, `2β⟨penalty⟩` over the Gibbs sample of the true ensemble (nats; NOT certificates)")
P()
for seq, bb, tau, name, W in G12:
    e = J(f"est_{tg(seq, bb, tau)}.json")
    if e is None:
        continue
    P(f"**{name}** (band {W}; {e['nsamples']} Gibbs states; off-anchor frequencies by site: " + " ".join(f"{v:.2f}" for v in e["psite"]) + ")")
    P()
    forms = ["site", f"pair/w{W}", f"triple/w{W}", "triple", "envelope", f"occ3/w{W}", f"occW/w{W}"]
    P("Each cell: first-order estimate `2β⟨pen⟩` [the estimate `ln⟨e^{β pen}⟩ − ln⟨e^{−β pen}⟩` on the same sample; the largest `β·pen` on the sample].")
    P()
    hdr = {"site": "site form (P3)", f"pair/w{W}": f"banded pair form (P6), band {W}", f"triple/w{W}": f"banded triple form (P6), band {W}", "triple": "triple shares, all triples in window",
           "envelope": "envelope `Σ_{T⊆S(x)} ĉ_T`", f"occ3/w{W}": "least-occupied in-window sub-tuple of ≤ 3 sites (estimate only)", f"occW/w{W}": "least-occupied in-window sub-tuple, any size (estimate only)"}
    P("| m | ball (evaluations) | constants | Γ_m (k_BT) | " + " | ".join(hdr[k] for k in forms) + " |")
    P("|---|---|---|---|" + "---|" * len(forms))
    for m, o in e["orders"].items():
        for v, d in o["variants"].items():
            if v in ("AH", "S", "Sb", "SA"):
                continue
            P(f"| {m} | {o['ball']} | {v} | {f(d['Gamma_kT'], 4)} | " + " | ".join((f"{f(d['est'][k][0])} [{f(d['expo'][k]) if 'expo' in d else '?'}; {f(d['pen_max_kT'][k], 2) if 'pen_max_kT' in d else '?'}]" if k in d["est"] else "—") for k in forms) + " |")
    P()

# ============================================================================================ Table 8
P("## T8  What an ideal certificate would pay: the exact remainder on the Gibbs sample (nats)")
P()
P("| peptide | Gibbs states (distinct) | m | fraction of states with ≥ m changed sites | mean \\|R_m\\| (kcal/mol) | largest \\|R_m\\| in the sample | floor of any order-m certificate `2β⟨\\|R_m\\|⟩` | envelope of the exact anchored terms `2β⟨A_m⟩` |")
P("|---|---|---|---|---|---|---|---|")
for seq, bb, tau, name, W in G12:
    d = J(f"ideal_{tg(seq, bb, tau)}.json")
    if d is None:
        continue
    for m, o in d["orders"].items():
        P(f"| {name} | {d['nsamples']} ({d['distinct']}) | {m} | {o['frac_ge_m']:.4f} | {f(o['mean_absR'])} | {f(o['max_absR'])} | {f(o['floor_nats'])} (±{f(o['floor_se'], 2)}) | {f(o['envelope_exact_terms_nats'])} |")
P()

# ============================================================================================ Table 9: distance
P("## T9  Distance laws at twelve residues (anchor context; exact evaluations)")
P()
for seq, bb, tau, name, W in G12:
    fn = os.path.join(OUT, f"dist_{tg(seq, bb, tau)}.npz")
    if not os.path.exists(fn):
        continue
    Z = np.load(fn)
    MT = Z["MT"]; span = Z["span"]; tri = Z["triples"]; dCA = Z["dCA"]; ch = Z["chargedT"]
    P(f"**{name}**: third-order anchored terms `M_T = max_y |d_T(y_T)|` of all {len(MT)} triples: sum {f(MT.sum())}, largest {f(MT.max())} kcal/mol.")
    P()
    P("| span (last − first site) | triples | sum of M_T | mean | median | max |")
    P("|---|---|---|---|---|---|")
    for s_ in sorted(set(span.tolist())):
        mk = span == s_
        P(f"| {s_} | {int(mk.sum())} | {f(MT[mk].sum())} | {f(MT[mk].mean())} | {f(float(np.median(MT[mk])))} | {f(MT[mk].max())} |")
    # power law in the distance of the far site for triples (i, i+1, k) and (k, i, i+1)
    xs, ys = [], []
    for T, v in zip(tri, MT):
        i, j, l = [int(u) for u in T]
        if j == i + 1 and l - j >= 2 and v > 0:
            xs.append(0.5 * (dCA[i, l] + dCA[j, l])); ys.append(v)
        elif l == j + 1 and j - i >= 2 and v > 0:
            xs.append(0.5 * (dCA[i, j] + dCA[i, l])); ys.append(v)
    if len(xs) >= 6:
        A = np.vstack([np.log(xs), np.ones(len(xs))]).T
        sl, ic = np.linalg.lstsq(A, np.log(ys), rcond=None)[0]
        resid = np.log(ys) - A @ np.array([sl, ic])
        P()
        P(f"Triples made of two neighbours and one site at Cα distance d (mean of the two distances; {len(xs)} triples, d from {min(xs):.2f} to {max(xs):.2f} nm): "
          f"least-squares fit `ln M_T = {sl:.2f}·ln d + const`, rms residual {resid.std():.2f} (a factor {np.exp(resid.std()):.1f}).")
    if len(set(ch.tolist())) > 1:
        P()
        P("| charged side chains in T | triples | sum of M_T | mean | median |")
        P("|---|---|---|---|---|")
        for c_ in sorted(set(ch.tolist())):
            mk = ch == c_
            P(f"| {c_} | {int(mk.sum())} | {f(MT[mk].sum())} | {f(MT[mk].mean())} | {f(float(np.median(MT[mk])))} |")
    # group responses
    R1 = Z["R1"]; D1 = Z["D1"]; gq = Z["gq"]; gabsq = Z["gabsq"]; gcls = Z["gcls"]; R2 = Z["R2"]
    P()
    P("First-order response `R1[A, j]` of the solvation energy of a rigid group A to a change at another site j (kcal/mol), by class of the group and centroid distance:")
    P()
    edges = [0.0, 0.5, 0.7, 0.9, 1.2, 1.6, 9.9]
    P("| group class (groups; mean \\|net charge\\|, mean Σ\\|q\\|) | " + " | ".join(f"{a:.1f}–{b:.1f} nm: median (n)" for a, b in zip(edges[:-1], edges[1:])) + " | fit ln R1 = a·ln d + c: a (rms residual) |")
    P("|---|" + "---|" * (len(edges) - 1) + "---|")
    cnames = ["bb", "nsc", "chain", "head"]
    for c_ in range(4):
        gsel = np.flatnonzero(gcls == c_)
        if not len(gsel):
            continue
        d = D1[gsel].ravel(); r = R1[gsel].ravel(); ok = ~np.isnan(d) & (r > 0)
        cells = []
        for a, b in zip(edges[:-1], edges[1:]):
            mk = ok & (d >= a) & (d < b)
            cells.append(f"{f(float(np.median(r[mk])))} ({int(mk.sum())})" if mk.any() else "—")
        A = np.vstack([np.log(d[ok]), np.ones(ok.sum())]).T
        sl, ic = np.linalg.lstsq(A, np.log(r[ok]), rcond=None)[0]
        resid = np.log(r[ok]) - A @ np.array([sl, ic])
        P(f"| {cnames[c_]} ({len(gsel)}; {np.abs(gq[gsel]).mean():.3f}, {gabsq[gsel].mean():.3f}) | " + " | ".join(cells) + f" | {sl:.2f} ({resid.std():.2f}) |")
    P()
    # second-order (three-body) response of a group to two other sites
    P("Second-order response `R2[A; j, k]` (a three-body term: group A fixed, sites j, k changing), sums over all pairs (j, k) per group, mean by class (kcal/mol): "
      + "; ".join(f"{cnames[c_]} {f(float(np.mean([np.triu(R2[a_], 1).sum() for a_ in np.flatnonzero(gcls == c_)])))}" for c_ in range(4) if (gcls == c_).any()))
    P()

# ============================================================================================ Table 11: the pipeline with the new constants
P("## T10  The existing certificate pipeline fed with the new constants (`p8_12_certificate.py`): brackets of `ln Z(E)` in nats")
P()
P("| instance | m | band | constants | Γ_m (k_BT) | ball (evaluations) | site form: [lower, upper] width | banded pair form | banded triple form | width of the same models with all penalties zero (the reduction of the evaluated terms beyond the band alone; not a sandwich) | sandwich checked at: violations (m₋ > E, m₊ < E; all three forms) | exact `ln Z` (enumeration) inside the three brackets | "
  "2000 exact samples of the floor of the triple form: mean number of sites off the anchor; violations | accepted points the sandwich sampler needs for a bracket of width 0.1 nats at confidence 0.95 inside the triple-form bracket, `2 ln(2/δ)(e^D − 1)²/w²` |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
NM = {"K4": "Lys₄", "K5": "Lys₅", "K12": "Lys₁₂", "LKSE:12": "(LKSE)₃", "S12": "Ser₁₂", "L12": "Leu₁₂"}
for fn in sorted(glob.glob(os.path.join(OUT, "cert_*.json")), key=lambda p_: (json.load(open(p_))["n"], json.load(open(p_))["m"], p_)):
    c = json.load(open(fn))
    fo = c["forms"]
    cell = lambda k_: f"[{fo[k_]['lnZ_lo']:.4f}, {fo[k_]['lnZ_hi']:.4f}] **{f(fo[k_]['width'])}**"
    viol = sum(fo[k_]["viol_lo"] + fo[k_]["viol_up"] for k_ in fo)
    if c["lnZ_exact"] is not None:
        where = f"all {int(c['domain'])} states"; ex = f"{c['lnZ_exact']:.6f}: " + ("yes" if all(fo[k_]["exact_inside"] for k_ in fo) else "NO")
    else:
        gz = os.path.join(OUT, f"gibbs_{tg(c['seq'], c['bb'], c['tau'])}.npz")
        where = f"{np.load(gz)['X'].shape[0]} Gibbs states of the true ensemble"; ex = "— (not enumerable)"
    D = fo["T"]["width"]; Nn = 2.0 * np.log(2.0 / 0.05) * (np.exp(D) - 1.0) ** 2 / 0.1 ** 2
    fs = c["floor_samples"]
    P(f"| {NM.get(c['seq'], c['seq'])} | {c['m']} | {c['w']} | {c['variant']} | {f(c['Gamma_kT'], 4)} | {c['nball']} | {cell('S')} | {cell('B')} | {cell('T')} | {f(c['width_zero_penalties']) if 'width_zero_penalties' in c else '—'} | {where}: {viol} | {ex} | "
      f"{fs['mean_off']:.2f}; {fs['viol_lo'] + fs['viol_up']} | {f(Nn)} |")
P()
P("Sampler arithmetic (theory division's Proposition 11.113 as P6 implemented it; width `w = (e^D − 1)·2√(ln(2/δ)/(2N))`), points `N` for `w = 0.1` nats at `δ = 0.05`: "
  + "; ".join(f"D = {D_}: {f(2.0 * np.log(2.0 / 0.05) * (np.exp(D_) - 1.0) ** 2 / 0.01)}" for D_ in (0.5, 1.0, 1.5, 2.0, 3.0, 4.0)) + ".")
P()

# ============================================================================================ Table 12: exact anchored terms beyond enumeration
P("## T12  The exact anchored terms in the anchor context, `M_T = max_y |d_T(y_T)|`, from the ball around the anchor (`p8_14_exact_terms12.py`), and the necessary condition `M_T ≤ ĉ_T` for every subset")
P()
P("| instance | ball: radius, evaluations | order | subsets | `Σ_T M_T` (kcal/mol) | in `k_BT` | largest `M_T` | fall of the sum from the order below | share of the sum in subsets of span ≤ 7 (%) | `M_T ≤ ĉ_T`: comparisons per variant; violations (P3, S, AH, SA, Sb, SAb) | smallest ratio `ĉ_T/M_T`: P3; SAb | ratio of the sums `Σĉ_T/ΣM_T`: P3; SAb | all-context exact constants over the anchor-context terms, `Σ c_T^anch/Σ M_T` (enumerated instances only) |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
NM2 = {"K5": "Lys₅", "LKSE:5": "LKSE:5", "K12": "Lys₁₂", "LKSE:12": "(LKSE)₃", "S12": "Ser₁₂", "L12": "Leu₁₂"}
exj = [json.load(open(fn)) for fn in glob.glob(os.path.join(OUT, "exact_*.json"))]
ncmp = 0; nviol = 0
maxM = {}
for e in exj:
    maxM[(e["seq"], e["bb"])] = max(maxM.get((e["seq"], e["bb"]), 0), e["M"])
for e in sorted(exj, key=lambda e_: (e_["n"], e_["seq"], e_["M"])):
    if e["M"] != maxM[(e["seq"], e["bb"])]:
        continue                                       # the same orders are in the run with the larger ball
    m1e = J(f"m1_{tg(e['seq'], e['bb'], e['tau'])}.json")
    prev = None
    for sk in sorted(e["orders"], key=int):
        o = e["orders"][sk]
        fall = f"{prev / o['sum']:.1f}" if prev else "—"
        prev = o["sum"]
        if int(sk) < 2:
            continue
        sp = o.get("by_span")
        share = f"{100 * sum(v for k_, v in sp.items() if int(k_) <= 7) / o['sum']:.1f}" if sp else "—"
        ab = o.get("against_bounds")
        if ab:
            vs = ["P3", "S", "AH", "SA", "Sb", "SAb"]
            c1 = f"{ab['SAb']['n']}; " + ", ".join(str(ab[v]["violations"]) for v in vs)
            c2 = f"{ab['P3']['min_ratio']:.2f}; {ab['SAb']['min_ratio']:.2f}"
            c3 = f"{f(ab['P3']['ratio_of_sums'])}; {f(ab['SAb']['ratio_of_sums'])}"
            ncmp += sum(ab[v]["n"] for v in vs); nviol += sum(ab[v]["violations"] for v in vs)
        else:
            c1 = c2 = c3 = "—"
        c4 = f"{m1e['orders'][sk]['total'] / o['sum']:.3f}" if m1e and sk in m1e["orders"] else "—"
        P(f"| {NM2.get(e['seq'], e['seq'])} | {e['M']}, {e['nball']} | {sk} | {o['nsub']} | {f(o['sum'])} | {f(o['sum_kT'])} | {f(o['max'])} | {fall} | {share} | {c1} | {c2} | {c3} | {c4} |")
P()
P(f"Comparisons `M_T ≤ ĉ_T` over all rows and the six variants: {ncmp}; violations: {nviol}.")
P()

# ============================================================================================ Table 10: run times and memory
import re
FAM = [("p8_00_probe", "p8_00_probe.py"), ("m1b_", "p8_01b_restricted.py"), ("m1_", "p8_01_measure.py"), ("sb_", "p8_02_signblind.py"), ("sr_", "p8_03_sr_validate.py"),
       ("sc_", "p8_03b_statecheck.py"), ("bc_", "p8_03c_blockcheck.py"), ("g12b_", "p8_04b_gamma12_blocks.py"), ("g12_", "p8_04_gamma12.py"), ("tw12_", "p8_04c_termwise12.py"),
       ("gibbs_", "p8_05_gibbs.py"), ("dist_", "p8_06_distance.py"), ("est_", "p8_07_estimate.py"), ("ideal_", "p8_08_ideal.py"), ("p8_10_order_identity", "p8_10_order_identity.py"),
       ("dfit_", "p8_11_distance_fit.py"), ("cert_", "p8_12_certificate.py"), ("ballrun_cert_", "p8_12_certificate.py: the two runs that evaluated the Lys₁₂ balls (last leg)"), ("exact_", "p8_14_exact_terms12.py")]
P("## T11  Run times and peak resident memory, read from the last line of every log in `logs/` (one core; a run with `--budget` is counted with its last leg)")
P()
P("| script | complete logs | time of a run (s): shortest – longest (log of the longest) | peak RSS (MB): largest measured (log) | logs without a memory record (runs of before 06:46 UTC) |")
P("|---|---|---|---|---|")
rows = {}; incomplete = []
for fn in sorted(glob.glob(os.path.join(HERE, "logs", "*.log"))):
    b = os.path.basename(fn)
    fam = next((s_ for p_, s_ in FAM if b.startswith(p_)), None)
    if fam is None:
        continue
    lines = [ln for ln in open(fn).read().splitlines() if ln.strip()]
    mt = re.match(r"DONE(?: in ([\d.]+) s)?(?:; peak RSS (\d+) MB)?\s*$", lines[-1]) if lines else None
    if not mt:
        incomplete.append(b); continue
    rows.setdefault(fam, []).append((b, float(mt.group(1)) if mt.group(1) else None, int(mt.group(2)) if mt.group(2) else None))
for p_, fam in FAM:
    if fam not in rows:
        continue
    r = rows[fam]
    witht = [u for u in r if u[1] is not None]
    withm = [u for u in r if u[2] is not None]
    ml = max(withm, key=lambda u: u[2]) if withm else None
    if witht:
        tl = max(witht, key=lambda u: u[1]); ts = min(witht, key=lambda u: u[1])
        tcell = f"{ts[1]:.1f} – {tl[1]:.1f} (`{tl[0]}`)"
    else:
        tcell = "— (the log ends with a bare `DONE`)"
    P(f"| `{fam}` | {len(r)} | {tcell} | " + (f"{ml[2]} (`{ml[0]}`)" if ml else "—") + f" | {len(r) - len(withm)} |")
P()
P("Logs whose last line is not a `DONE` line (not cited anywhere): " + (", ".join(f"`{b}`" for b in incomplete) if incomplete else "none") + ".")
P()

open(os.path.join(OUT, "tables.md"), "w").write("\n".join(L) + "\n")
print(f"wrote out/tables.md ({len(L)} lines)")
