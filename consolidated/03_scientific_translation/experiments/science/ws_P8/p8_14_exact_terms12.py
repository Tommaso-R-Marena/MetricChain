"""
P8 step 2 -- the EXACT anchored terms of order <= M of a peptide too large to enumerate, in the anchor context, from
the values of g on the Hamming ball of radius M around the anchor.

    d_T(y_T) = Delta_T g(x0; x0_T -> y_T)   (every site outside T at the anchor),      M_T = max_y |d_T(y_T)|.

g(x) = sum_{T subset S(x)} d_T(x_T) (P3's anchored expansion), so M_T is what the TRUTH contributes at the subset T in the
anchor context; it is a LOWER bound of the exact anchored constant c_T^anch(g) (which takes the supremum over all
contexts).  This is the measurement behind "how does the truth fall with the order at twelve residues" (step 2 of the
brief): at five and six residues the fall is known by enumeration (p8_01_measure.py), here it is measured at twelve
for the orders the ball reaches.

The ball is the one p8_12_certificate.py evaluates for order M + 1 (same file in ws_P8/cache, reused if present;
otherwise evaluated here with a checkpoint every minute).  P3's pwmodel.anchored_terms turns the ball values into the
tables d_T (imported read-only).

usage: python3 -B p8_14_exact_terms12.py SEQ BB TAU M [--budget SECONDS] [--resume]
writes logs/exact_<tag>_M<M>.log, out/exact_<tag>_M<M>.npz (T<s>, MT<s> for s = 3..M), out/exact_<tag>_M<M>.json
"""
import sys, os, json, time, hashlib, itertools
import numpy as np
from p8lib import *
import pwmodel as pw                                  # P3 (read-only; no side effects at import)

a = sys.argv[1:]
seq, bb, tau, M = a[0], a[1], float(a[2]), int(a[3])
BUDGET = float(a[a.index("--budget") + 1]) if "--budget" in a else 1e18
tag = tagname(seq, bb, tau)
stem = f"exact_{tag}_M{M}"
if os.path.exists(os.path.join(HERE, "out", stem + ".json")) and "--force" not in a:
    print(f"out/{stem}.json exists: this run is complete; nothing done"); sys.exit(0)
G = GBModel(seq, bb, tau=tau)
n, k = G.ns, list(G.k)
c0, h, J = pw.known_tables(G)
x0, E0, nev = pw.icm_anchor(G, c0, h, J)
x0 = tuple(int(v) for v in x0)
ah = hashlib.sha1(str((x0, [list(map(int, dd)) for dd in G.dom])).encode()).hexdigest()[:10]
ballfile = os.path.join(MYCACHE, f"ball_{tag}_M{M}_{ah}.npz")
ballckpt = os.path.join(MYCACHE, f"ball_{tag}_M{M}_{ah}_ckpt.npz")
resume = os.path.exists(ballckpt) and not os.path.exists(ballfile)
if resume and "--resume" not in a:
    print(f"a checkpoint of this ball exists ({os.path.basename(ballckpt)}): another run may be evaluating it; pass --resume to continue it here"); sys.exit(1)
log = Log(os.path.join(HERE, "logs", stem + ".log"), append=resume)
t0 = time.time()
log(f"=== p8_14_exact_terms12: {seq} on {bb}, tau {tau}: {G.nat} atoms, {n} sites, states per site {k}; anchor (ICM) {x0}; ball of radius {M}" + ("; RESUMING the ball" if resume else ""))
blocks, tot = pw.ball_states(k, x0, M)
allst = np.concatenate([b_ for _, b_ in blocks], axis=0)
if os.path.exists(ballfile):
    z = np.load(ballfile); vals = z["vals"]
    assert z["states"].shape == allst.shape and np.array_equal(z["states"], allst)
    log(f"(1) ball of radius {M}: {tot} values read from cache/{os.path.basename(ballfile)}")
else:
    if resume:
        z = np.load(ballckpt); vals = z["vals"]; i_next = int(z["i_next"])
        log(f"    ball checkpoint read: {i_next} of {tot} evaluations done")
    else:
        vals = np.zeros(tot); i_next = 0
    tlast = time.time(); stopped = False
    CH = 256
    for s0 in range(i_next, tot, CH):
        vals[s0:s0 + CH] = G.bulk_energy(allst[s0:s0 + CH])
        now = time.time()
        if now - tlast > 60 or now - t0 > BUDGET:
            tmp = ballckpt + ".tmp.npz"
            np.savez(tmp, vals=vals, i_next=min(tot, s0 + CH)); os.replace(tmp, ballckpt); tlast = now
            log(f"    ball: {min(tot, s0 + CH)}/{tot} evaluations, checkpoint written, {now - t0:.0f} s, RSS {rss_mb():.0f} MB")
        if now - t0 > BUDGET and s0 + CH < tot:
            stopped = True
            break
    if stopped:
        log("BUDGET REACHED in the ball: checkpoint on disk, run the same command with --resume to continue (not a complete run)")
        log.f.close(); sys.exit(0)
    np.savez(ballfile, states=allst.astype(np.int16), vals=vals)
    log(f"(1) ball of radius {M}: {tot} evaluations of the solvent term [{time.time() - t0:.0f}s]")
rng = np.random.default_rng(20261126)
pick = rng.choice(tot, size=min(48, tot), replace=False)
devb = float(np.abs(G.energy(allst[pick]) - vals[pick]).max())
log(f"    48 ball values re-evaluated with P3's own evaluator (GBModel.energy): largest deviation {devb:.1e} kcal/mol")
assert devb < 1e-8
pos = [0]


def lookup(st_):
    st_ = np.atleast_2d(st_)
    s0 = pos[0]
    assert np.array_equal(st_, allst[s0:s0 + len(st_)]), "anchored_terms asked for states in an unexpected order"
    pos[0] += len(st_)
    return vals[s0:s0 + len(st_)]


d, nb, _ = pw.anchored_terms(G, x0, M, energy=lookup, cache_file=None)
assert nb == tot and pos[0] == tot
del _
log(f"(2) anchored terms of order <= {M}: {len(d)} tables [{time.time() - t0:.0f}s, RSS {rss_mb():.0f} MB]")
# identity check: g at random ball states = sum of the anchored terms of the changed sites' subsets
chk = rng.choice(tot, size=min(200, tot), replace=False)
dev = 0.0
for i_ in chk:
    x = allst[i_]; S = [j for j in range(n) if x[j] != x0[j]]
    acc = 0.0
    for r in range(len(S) + 1):
        for U in itertools.combinations(S, r):
            acc += float(d[U][tuple(int(x[j]) for j in U)]) if U else float(d[()])
    dev = max(dev, abs(acc - vals[i_]))
log(f"    identity g(x) = sum of the anchored terms over the subsets of S(x), at {len(chk)} ball states: largest deviation {dev:.1e} kcal/mol")
assert dev < 1e-7
res = dict(seq=seq, bb=bb, tau=tau, M=M, n=n, nball=int(tot), orders={})
save = {}
log("(3) the truth in the anchor context, by order: M_T = max_y |d_T(y_T)| (kcal/mol; kT in brackets)")
prev = None
for s in range(1, M + 1):
    Ts = [U for U in d if len(U) == s]
    MT = np.array([float(np.abs(d[U]).max()) for U in Ts])
    ssum = float(MT.sum())
    # root-mean-square over the states of T (how typical the maximum is)
    rms = np.array([float(np.sqrt((d[U] ** 2).sum() / max(1, np.prod([k[i] - 1 for i in U])))) for U in Ts])
    row = dict(nsub=len(Ts), sum=ssum, sum_kT=BETA * ssum, max=float(MT.max()), median=float(np.median(MT)), sum_rms=float(rms.sum()))
    res["orders"][str(s)] = row
    log(f"    order {s}: {len(Ts):4d} subsets: sum {ssum:.4e} [{BETA * ssum:.4g} kT], largest {MT.max():.3e}, median {np.median(MT):.3e}; sum of the rms over the states of T {rms.sum():.4e}"
        + (f";  fall of the sum from order {s - 1}: {prev / ssum:.1f}-fold" if prev else ""))
    prev = ssum
    if s >= 3:
        save[f"T{s}"] = np.array(Ts, dtype=np.int16); save[f"MT{s}"] = MT
        # by span (last - first site) and the share of the subsets of span <= 7 (two turns of the helix)
        span = np.array([U[-1] - U[0] for U in Ts])
        row["by_span"] = {int(v): float(MT[span == v].sum()) for v in sorted(set(span.tolist()))}
        log("        by span (last - first site): " + ", ".join(f"{v}: {100 * MT[span == v].sum() / ssum:.1f} %" for v in sorted(set(span.tolist()))))
        # NECESSARY condition for every bound of this order, testable at this size: the anchor context is one of the
        # contexts every variant covers (all sites outside T at the anchor, in particular the hosts outside T), so
        # M_T <= chat_T must hold for every subset and every variant (P3, S, AH, SA, Sb, SAb).
        fb = os.path.join(HERE, "out", f"g12b_{tag}_m{s}.npz"); fg = os.path.join(HERE, "out", f"g12_{tag}_m{s}.npz")
        if os.path.exists(fb) and os.path.exists(fg):
            Zb = np.load(fb); Zc = np.load(fg)
            assert tuple(int(v) for v in Zb["anchor"]) == x0 and tuple(int(v) for v in Zc["anchor"]) == x0 and np.array_equal(Zb["T"], Zc["T"])
            idx = {tuple(int(v) for v in T_): i_ for i_, T_ in enumerate(Zb["T"])}
            od = np.array([idx[tuple(int(v) for v in U)] for U in Ts])
            vb = [str(v) for v in Zb["variants"]]; vg = [str(v) for v in Zc["variants"]]
            cols = [(v, Zc["C"].sum(axis=2)[od, vg.index(v)]) for v in vg] + [(v, Zb["Cb"][od, vb.index(v)]) for v in vb]
            row["against_bounds"] = {}
            for name, arr in cols:
                viol = int((arr < MT - 1e-12).sum()); ratio = arr / np.maximum(MT, 1e-300)
                row["against_bounds"][name] = dict(n=int(len(MT)), violations=viol, min_ratio=float(ratio.min()), median_ratio=float(np.median(ratio)), ratio_of_sums=float(arr.sum() / ssum))
            log(f"        bound >= exact anchor-context term, subset by subset ({len(MT)} comparisons per variant): violations " + ", ".join(f"{nm} {row['against_bounds'][nm]['violations']}" for nm, _ in cols)
                + ";  ratio bound/exact: " + "; ".join(f"{nm} min {row['against_bounds'][nm]['min_ratio']:.2f}, median {row['against_bounds'][nm]['median_ratio']:.1f}, of the sums {row['against_bounds'][nm]['ratio_of_sums']:.1f}" for nm, _ in cols))
            assert all(v_["violations"] == 0 for v_ in row["against_bounds"].values()), "a bound is below an exact anchor-context term"
fd = os.path.join(HERE, "out", f"dist_{tag}.npz")
if M >= 3 and os.path.exists(fd):
    Zd = np.load(fd)
    if tuple(int(v) for v in Zd["anchor"]) == x0:
        mt = {tuple(int(v) for v in T): float(v_) for T, v_ in zip(Zd["triples"], Zd["MT"])}
        devd = max(abs(mt[tuple(int(v) for v in T)] - v_) for T, v_ in zip(save["T3"], save["MT3"]))
        log(f"(4) cross-check: M_T of the {len(mt)} triples against p8_06_distance.py (direct evaluation on the grid of the three sites): largest deviation {devd:.1e} kcal/mol")
        res["dev_vs_dist"] = devd
        assert devd < 1e-7
np.savez(os.path.join(HERE, "out", stem + ".npz"), anchor=np.array(x0), **save)
with open(os.path.join(HERE, "out", stem + ".json"), "w") as fh:
    json.dump(res, fh, indent=1)
log.done()
