#!/usr/bin/env python3
"""P9 step 3 -- the state-resolved bounds of ALL subsets of order m of a twelve-residue peptide (or of a small
instance), both stages, reduced on the fly to everything the later steps need (p9lib.Acc):
  top-level sums S1 (sites), S2 (pairs), S3 (triples) for the share forms; the window form W; the fully resolved
  envelope at the states of the two Gibbs samples; per-subset maxima / minima / typical values.
Per subset: P8's constants 'Sb', 'SAb' (its own code path) are compared with P8's stored files.

usage:  python3 -B p9_03_tables.py SEQ M [--w W] [--part j J] [--keeptabs]
        python3 -B p9_03_tables.py SEQ M [--w W] --merge J
  without --part: all subsets in one run, final file out/tables_<tag>_m<M>_w<W>.npz
  --part j J:     the subsets with index = j mod J (a complete run of its own, own log); then --merge J.
  --keeptabs:     also stores the stage-2 tables Theta_T themselves (cache/theta2_<tag>_m<M>[_pjofJ].npz), for the envelope.
logs: logs/tables_<tag>_m<M>_w<W>[_pjofJ | _merge].log
"""
import sys
from p9lib import *

a = sys.argv[1:]; seq, m = a[0], int(a[1]); bb = "H"; tau = tau_of(seq); tag = tagname(seq, bb, tau)
w = int(a[a.index("--w") + 1]) if "--w" in a else 7
PART = (int(a[a.index("--part") + 1]), int(a[a.index("--part") + 2])) if "--part" in a else None
MERGE = int(a[a.index("--merge") + 1]) if "--merge" in a else None
KEEP = "--keeptabs" in a
stem = f"{tag}_m{m}_w{w}"
suffix = f"_p{PART[0]}of{PART[1]}" if PART else "_merge" if MERGE else ""
log = Log(os.path.join(LOGS, f"tables_{stem}{suffix}.log"))
log(f"=== p9_03_tables {seq} on {bb}, tau {tau}, order {m}, window {w}" + (f", part {PART[0]} of {PART[1]}" if PART else f", merging {MERGE} parts" if MERGE else "") + f"; started {now()}")
final = os.path.join(OUT, f"tables_{stem}.npz")


def summary(d):
    n = int(d["n"]); subs = [tuple(int(v) for v in T) for T in d["s1_subs"]]
    assert subs == list(itertools.combinations(range(n), m)), "subsets missing or out of order"
    sab, sb = d["s1_sab"], d["s1_sb"]
    log(f"--- {len(subs)} subsets of order {m}.  Gamma_{m} in kT:  P8's Sb {BETA * sb.sum():.6g}, P8's SAb {BETA * sab.sum():.6g} | "
        f"stage 1: joint maximum {BETA * d['s1_cJ'].sum():.6g}, median over the states {BETA * d['s1_med'].sum():.6g}, minimum {BETA * d['s1_cmin'].sum():.6g} | "
        f"stage 2: joint maximum {BETA * d['s2_cJ'].sum():.6g}, median {BETA * d['s2_med'].sum():.6g}, minimum {BETA * d['s2_cmin'].sum():.6g}")
    for s in (1, 2):
        r = d[f"s{s}_cJ"] / sab
        log(f"    stage {s}: joint maximum / SAb per subset: min {r.min():.3f}, median {np.median(r):.3f}, max {r.max():.4f}; "
            f"sum over the subsets of E_prod[Theta_T; T off the anchor] (product of the one-site marginals of the guiding sample): {BETA * d[f's{s}_typ'].sum():.4g} kT; "
            f"window form: {len([f for f in d if f.startswith(f's{s}_W_')])} tables, sub-tuples kept by size: "
            + ", ".join(f"{sz}: {c}" for sz, c in sorted({sz: sum(1 for v in d[f's{s}_keep'] if len(str(v).split('_')) == sz) for sz in range(1, m + 1)}.items()) if c))
    f12b = os.path.join(P8DIR, "out", f"g12b_{tag}_m{m}.npz"); fbc = os.path.join(P8DIR, "out", f"bc_{tag}.json")
    if os.path.exists(f12b):
        Zb = np.load(f12b); Vb = [str(v) for v in Zb["variants"]]
        assert [tuple(int(v) for v in T) for T in Zb["T"]] == subs and [int(v) for v in Zb["anchor"]] == [int(v) for v in d["x0"]]
        log(f"    my recorded constants against P8's stored per-subset values (ws_P8/out/g12b_{tag}_m{m}.npz): largest relative deviation "
            f"'Sb' {float(np.abs(sb / Zb['Cb'][:, Vb.index('Sb')] - 1).max()):.1e}, 'SAb' {float(np.abs(sab / Zb['Cb'][:, Vb.index('SAb')] - 1).max()):.1e}")
    elif os.path.exists(fbc):
        Jd = json.load(open(fbc))["per_subset"]
        ref = np.array([float(Jd["SAb"]["-".join(map(str, T))]) for T in subs])
        log(f"    my recorded 'SAb' constants against P8's stored per-subset values (ws_P8/out/bc_{tag}.json): largest relative deviation {float(np.abs(sab / ref - 1).max()):.1e}")
    for sd in sorted(int(f.split('_')[-1]) for f in d if f.startswith("s1_env_")):
        e1, e2 = d[f"s1_env_{sd}"], d[f"s2_env_{sd}"]
        log(f"    Gibbs sample {sd} ({len(e1)} states): mean of beta x envelope: stage 1 {BETA * e1.mean():.4g}, stage 2 {BETA * e2.mean():.4g}; largest: {BETA * e1.max():.4g}, {BETA * e2.max():.4g}; "
            f"states with a non-zero envelope: {int((e1 > 0).sum())}")


if MERGE:
    files = [os.path.join(OUT, f"tabpart_{stem}_p{j}of{MERGE}.npz") for j in range(MERGE)]
    d = merge_parts(files)
    np.savez(final, **d)
    log(f"    merged {len(files)} part files into out/{os.path.basename(final)}")
    summary(d)
    log.done(); sys.exit(0)

G, c0, h, J, x0, E0 = setup(seq, bb, tau); n, k = G.ns, list(G.k)
samples = {sd: load_gibbs(tag, sd)[0] for sd in (4242, 777)}
subs = list(itertools.combinations(range(n), m))
todo = [i for i in range(len(subs)) if (PART is None or i % PART[1] == PART[0])]
log(f"    {G.nat} atoms, {n} sites, states per site {k}, anchor {x0}; {len(subs)} subsets of order {m}, {len(todo)} in this run; "
    f"sum over them of the number of states of T: {sum(int(np.prod([k[i] - 1 for i in subs[j]])) for j in todo):.4g}")
SR = ResBound(G, tuple(x0), EnvelopeSup(G), K=m); RES = Resolver(SR)
acc = Acc(n, k, x0, m, w, samples)
t0 = time.time(); tl = t0; viol = 0
for c, j in enumerate(todo):
    T = subs[j]
    th1, th2, sab, sb = RES.theta_both(m, T)
    viol += int((th2 > th1 * (1 + 1e-12)).sum())
    acc.add(j, T, th1, th2, sab, sb, keeptabs=KEEP)
    if time.time() - tl > 120 or c == len(todo) - 1:
        tl = time.time()
        log(f"    subset {c + 1}/{len(todo)} done, {time.time() - t0:.0f} s ({(time.time() - t0) / (c + 1):.2f} s per subset), RSS now {P8L.rss_mb():.0f} MB")
log(f"    stage 2 > stage 1 at {viol} table entries (must be 0)")
d = acc.to_dict()
if PART:
    np.savez(os.path.join(OUT, f"tabpart_{stem}_p{PART[0]}of{PART[1]}.npz"), **d)
    log(f"    part file written: out/tabpart_{stem}_p{PART[0]}of{PART[1]}.npz ({len(todo)} subsets); run the other parts, then --merge {PART[1]}")
else:
    np.savez(final, **d)
    summary(d)
if KEEP:
    fn = os.path.join(MYCACHE, f"theta2_{tag}_m{m}{suffix}.npz")
    np.savez(fn, idx=np.array(acc.idx), **{f"t{j}": t for j, t in zip(acc.idx, acc.tabs2)})
    log(f"    stage-2 tables Theta_T of {len(acc.tabs2)} subsets stored in cache/{os.path.basename(fn)}")
log.done()
