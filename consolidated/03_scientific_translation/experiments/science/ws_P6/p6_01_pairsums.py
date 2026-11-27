"""
P6 step 1: pair sums  G_ij = sum_{T contains i, j, |T| = m} chat_T  of P3's certified tail constants WITHOUT
enumerating subsets, from P3's closed form (Proposition 4) with one and two sites excluded:
    G_ij = Gamma - Gamma^(-i) - Gamma^(-j) + Gamma^(-i,-j),      S_i = sum_{T ni i} chat_T = Gamma - Gamma^(-i).
Output: out/pairsums_<tag>_m<m>.npz  (Gamma, S, G, exclusion totals, anchor, time).

With --check: validation against (a) P3's own total(m, exclude=i), (b) the simple subclass GFBound2.total_ex
(P3's loop, a set of excluded sites) for every single and pair, (c) EXPLICIT ENUMERATION of all subsets T by P3's
per-subset evaluation total(m, T).  Reports the largest differences.

usage: python3 -B p6_01_pairsums.py SEQ BB TAU m [--check] [--w W] [--kind gbn2|obc2]
       (--w W: only the pair exclusions with j - i <= W -- enough for the banded pair form with band W)
"""
import sys, os, time, itertools, json
import numpy as np
import p6lib as L

a = sys.argv[1:]
seq, bb, tau, m = a[0], a[1], float(a[2]), int(a[3])
check = "--check" in a
wopt = int(a[a.index("--w") + 1]) if "--w" in a else None
kind = a[a.index("--kind") + 1] if "--kind" in a else "gbn2"
t0 = time.time()
G, c0, h, J, x0, E0 = L.setup(seq, bb, tau, kind)
n = G.ns
print(f"=== pair sums: {seq} on {bb}, tau {tau}, {kind}, order m = {m}: atoms {G.nat}, sites {n}, states/site {min(G.k)}..{max(G.k)}; "
      f"anchor {''.join(map(str, x0))}, E = {E0:.6f} kcal/mol [{time.time() - t0:.1f}s]", flush=True)
if m > n:
    print("m > n: no subset of order m; nothing to do"); print("DONE"); sys.exit(0)
t1 = time.time()
sup = L.EnvelopeSup(G)
GF = L.GFBound2(G, x0, sup, K=m)
print(f"    enclosures and instances [{time.time() - t1:.1f}s]", flush=True)
excl = L.exclusion_sets(n, wopt)
t1 = time.time()
GB = L.GFBatch(GF)
se, cr = GB.totals(m, excl, progress=max(1, n // 5))
tot = se + cr
t_batch = time.time() - t1
Gam, S, Gp = L.assemble_pair_sums(n, m, excl, tot)
c2 = m * (m - 1) // 2
print(f"    {len(excl)} exclusion sets (1 + {n} + {len(excl) - n - 1} pairs) by the batched closed form [{t_batch:.1f}s]: "
      f"Gamma_{m} = {Gam:.6e} kcal/mol (self {se[0]:.3e}, cross {cr[0]:.3e})", flush=True)
fin = np.isfinite(Gp) & ~np.eye(n, dtype=bool)
print(f"    S_i = sum_(T ni i): min {S.min():.4e}, max {S.max():.4e}; sum_i S_i / m = {S.sum() / m:.6e} (must equal Gamma: rel. dev. {abs(S.sum() / m - Gam) / Gam:.1e})")
if wopt is None:
    print(f"    G_ij: min {Gp[fin].min():.4e}, max {Gp[fin].max():.4e}; sum_(i<j) G_ij / C(m,2) = {Gp[fin].sum() / 2 / c2:.6e} "
          f"(must equal Gamma: rel. dev. {abs(Gp[fin].sum() / 2 / c2 - Gam) / Gam:.1e}); "
          f"row identity sum_j G_ij = (m-1) S_i: max abs dev {np.abs(np.where(fin, Gp, 0).sum(1) - (m - 1) * S).max():.2e}", flush=True)
    off = [float(np.mean([Gp[i, i + s] for i in range(n - s)])) for s in range(1, n)]
    print("    mean G_ij by separation |i-j| = 1.." + str(n - 1) + ": " + " ".join(f"{v:.2e}" for v in off), flush=True)
res = dict(seq=seq, bb=bb, tau=tau, m=m, kind=kind, n=n, anchor=list(x0), E_anchor=E0, Gamma=Gam, t_batch=t_batch, n_excl=len(excl))
if check:
    # (a) P3's own single exclusions
    t1 = time.time()
    dev_a = 0.0
    for i in range(n):
        ref = sum(GF.total(m, exclude=i))
        dev_a = max(dev_a, abs(ref - tot[1 + i]) / ref)
    ref0 = sum(GF.total(m))
    dev_a = max(dev_a, abs(ref0 - tot[0]) / ref0)
    print(f"    CHECK (a) batched closed form vs P3's total(m) and total(m, exclude=i), {n + 1} values: max rel. dev. {dev_a:.2e} [{time.time() - t1:.1f}s]", flush=True)
    # (b) simple subclass for all exclusion sets
    t1 = time.time()
    dev_b = 0.0
    for e, v in zip(excl, tot):
        ref = sum(GF.total_ex(m, e))
        dev_b = max(dev_b, abs(ref - v) / max(ref, 1e-300))
    print(f"    CHECK (b) batched closed form vs P3's loop with a set of excluded sites (GFBound2.total_ex), {len(excl)} values: max rel. dev. {dev_b:.2e} [{time.time() - t1:.1f}s]", flush=True)
    # (c) explicit enumeration of subsets
    t1 = time.time()
    chat = L.enum_chat(GF, m)
    Gam_e, S_e, Gp_e = L.pair_sums_from_chat(n, chat)
    dS = np.abs(S - S_e); dG = np.abs(np.where(fin, Gp - Gp_e, 0.0))
    relG = np.where(fin & (Gp_e > 0), dG / np.maximum(Gp_e, 1e-300), 0.0)
    print(f"    CHECK (c) EXPLICIT ENUMERATION of the {len(chat)} subsets of order {m} (P3's total(m, T)) [{time.time() - t1:.1f}s]: "
          f"Gamma: gf {Gam:.12e} enum {Gam_e:.12e} (rel. dev. {abs(Gam - Gam_e) / Gam_e:.1e}); "
          f"S_i: max abs dev {dS.max():.2e} (rel. to Gamma {dS.max() / Gam_e:.1e}); "
          f"G_ij ({int(fin.sum() // 2)} pairs): max abs dev {dG.max():.2e} kcal/mol (rel. to Gamma {dG.max() / Gam_e:.1e}; "
          f"largest dev. relative to G_ij itself {relG.max():.1e}; smallest G_ij {Gp_e[fin].min():.3e})", flush=True)
    res.update(check=dict(dev_a=dev_a, dev_b=dev_b, n_subsets=len(chat), Gamma_enum=Gam_e, dS_max=float(dS.max()),
                          dG_max=float(dG.max()), dG_rel_to_Gamma=float(dG.max() / Gam_e), dG_rel_max=float(relG.max()),
                          G_min=float(Gp_e[fin].min()), n_pairs=int(fin.sum() // 2)))
    assert dev_a < 1e-9 and dev_b < 1e-9 and dG.max() <= 1e-9 * Gam_e and dS.max() <= 1e-9 * Gam_e, "pair sums disagree with enumeration"
os.makedirs(os.path.join(L.HERE, "out"), exist_ok=True)
tag = L.tagname(seq, bb, tau, kind)
fn = os.path.join(L.HERE, "out", f"pairsums_{tag}_m{m}" + (f"_w{wopt}" if wopt is not None else "") + ".npz")
np.savez(fn, Gamma=Gam, S=S, G=Gp, tot=tot, se=se, cr=cr, excl=np.array([list(e) + [-1] * (2 - len(e)) for e in excl]),
         anchor=np.array(x0), m=m, w=-1 if wopt is None else wopt)
json.dump(res, open(fn.replace(".npz", ".json"), "w"), indent=1)
print(f"    -> {os.path.relpath(fn, L.HERE)}")
print(f"DONE p6_01_pairsums {seq} {bb} {tau} {m} [{time.time() - t0:.0f}s]", flush=True)
