#!/usr/bin/env python3
"""P9 step 5 -- CERTIFIED BRACKETS of ln Z(E) with the state-resolved penalty tables.

Models: the coordinator's window models with exact in-window evaluated terms, occupancy-aware reductions and the
split of the far pairs around the anchor (pi_inference/window_model_occ.build_window_models_occ, rule "occ+" of
occ_reduction_test.py: guiding Gibbs sample seed 4242), built with ZERO penalties plus workstream P6's
floating-point allowances (p6lib.fp_tables, allocated as in the state-independent forms: site form phi1; pair and
triple forms psi1 + in-band psi2 + halves of the out-of-band psi2); then my tables are ADDED: site tables to
lo.one[i] / up.one[i], pair tables with add_pair, window tables (three or more sites) with add_multi.
Hypothesis used:  |g - I_{m-1} g|(x) <= pen(x) pointwise  (P9_REPORT, Theorem R and Proposition P).

Sources of the penalty (--sources):
  ref   the coordinator's own recipe with workstream P8's stored 'SAb' constants (p6lib.site_form / banded_pair_form /
        window_model.triple_form_two_windows) -- must reproduce the brackets of occ_reduction_test_*.log, rule occ+;
  sab   P8's constants through MY chains (form_tables with state-independent constants): a check of my chain code;
  cJ1, cJ2   the joint maxima over the states of T of the stage-1 / stage-2 bound, as state-independent constants;
  s1, s2     the state-resolved tables of stage 1 (hosts) / stage 2 (hosts and non-host sites).
Forms (--forms): S site, B banded pair, T banded triple (equal shares, as P3 / P6); W window form: every subset charged
in full to one sub-tuple of its sites that fits a window (resolved tables: p9lib.Acc; constants: p9lib.window_form_const).
Checks: the sandwich m_- <= E <= m_+ at the 960 Gibbs states of the check sample (seed 777); for --floor F
"source:form,..." at N exact samples of the floor; with --enum at EVERY state, with the exact ln Z inside.

usage: python3 -B p9_05_brackets.py SEQ M W [--sources ref,s1,s2] [--forms S,B,T,W] [--pairs s2:T,sab:W,...] [--floor s2:T,s2:W] [--nfloor 2000] [--enum] [--label X]
       (--pairs lists the (source, form) pairs explicitly and overrides --sources / --forms)
writes logs/brackets_<tag>_m<M>_w<W>[_<label>].log and out/brackets_....json
"""
import sys
from p9lib import *

a = sys.argv[1:]; seq, m, w = a[0], int(a[1]), int(a[2]); bb = "H"; tau = tau_of(seq); tag = tagname(seq, bb, tau); M = m - 1


def opt(key, default):
    return a[a.index(key) + 1] if key in a else default


SOURCES = opt("--sources", "ref,s1,s2").split(","); FORMS = opt("--forms", "S,B,T,W").split(",")
FLOOR = [tuple(v.split(":")) for v in opt("--floor", "").split(",") if v]; NFLOOR = int(opt("--nfloor", "2000")); ENUM = "--enum" in a
label = opt("--label", ""); stem = f"{tag}_m{m}_w{w}" + (f"_{label}" if label else "")
log = Log(os.path.join(LOGS, f"brackets_{stem}.log"))
log(f"=== p9_05_brackets {seq} on {bb}, tau {tau}: order m = {m}, band {w}; sources {SOURCES}, forms {FORMS}; started {now()}")
t0 = time.time()
G, c0, h, J, x0, E0 = setup(seq, bb, tau); n, k = G.ns, list(G.k)
subs = list(itertools.combinations(range(n), m)); tris = T9.window_triples(n, w)
phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
LD = Loaded(os.path.join(OUT, f"tables_{tag}_m{m}_w{w}.npz")); assert LD.x0 == x0 and LD.k == k and LD.TB[1].subs == subs
# ---- P8's stored constants (for 'ref')
f12b = os.path.join(P8DIR, "out", f"g12b_{tag}_m{m}.npz"); fbc = os.path.join(P8DIR, "out", f"bc_{tag}.json")
if os.path.exists(f12b):
    Zb = np.load(f12b); Vb = [str(v) for v in Zb["variants"]]; assert [int(v) for v in Zb["anchor"]] == x0 and [tuple(int(v) for v in T) for T in Zb["T"]] == subs
    chat = np.array(Zb["Cb"][:, Vb.index("SAb")], dtype=float); srcc = f"ws_P8/out/g12b_{tag}_m{m}.npz"
elif os.path.exists(fbc):
    Jd = json.load(open(fbc))["per_subset"]["SAb"]; chat = np.array([float(Jd["-".join(map(str, T))]) for T in subs]); srcc = f"ws_P8/out/bc_{tag}.json"
else:                                                    # P8 stored no constants for this instance and order (twelve residues, order 3)
    chat = np.array(LD.TB[1].sab, dtype=float); srcc = "P8's code path, re-computed here (workstream P8 stored no per-subset constants for this instance at this order)"
log(f"    {n} sites, states per site {k}, {float(np.prod([float(v) for v in k])):.6g} assignments, anchor {x0}; P8's 'SAb' constants from {srcc}: Gamma_{m} = {BETA * chat.sum():.4g} kT; "
    f"my recorded ones differ by at most {float(np.abs(LD.TB[1].sab / chat - 1).max()):.1e} (relative)")
# ---- the ball and the anchored terms (as the coordinator's drivers: P8's cached ball, read-only; a sample re-evaluated)
blocks, tot = pw.ball_states(k, x0, M); allst = np.concatenate([b for _, b in blocks], axis=0); vals = None; srcb = None
for fcache in sorted(os.listdir(os.path.join(P8DIR, "cache"))):
    if fcache.startswith(f"ball_{tag}_M") and fcache.endswith(".npz") and "ckpt" not in fcache:
        z = np.load(os.path.join(P8DIR, "cache", fcache))
        if z["states"].shape[0] >= tot and np.array_equal(z["states"][:tot], allst):
            vals = np.array(z["vals"][:tot], dtype=float)
            pick = np.random.default_rng(11).choice(tot, size=min(tot, 1000), replace=False)
            dev = float(np.abs(np.concatenate([G.bulk_energy(allst[pick[s:s + 250]]) for s in range(0, len(pick), 250)]) - vals[pick]).max()); assert dev < 1e-8, dev
            srcb = f"ws_P8/cache/{fcache} (states equal pwmodel.ball_states row by row; {len(pick)} random values re-evaluated here: largest deviation {dev:.1e} kcal/mol)"; break
        del z
if vals is None:
    vals = np.concatenate([G.bulk_energy(allst[s:s + 256]) for s in range(0, tot, 256)]); srcb = "evaluated now with P3's bulk evaluator"
radix = np.array([int(np.prod(k[i + 1:])) for i in range(n)], dtype=np.int64)
code = allst.astype(np.int64) @ radix; order = np.argsort(code); code_s = code[order]; vals_s = vals[order]


def lookup(st):
    c = np.atleast_2d(st).astype(np.int64) @ radix; p = np.searchsorted(code_s, c); assert np.array_equal(code_s[p], c)
    return vals_s[p]


d, nb, _ = pw.anchored_terms(G, x0, M, energy=lookup, cache_file=None); assert nb == tot
del allst, code, order
log(f"    ball of radius {M}: {tot} values, {srcb} [{time.time() - t0:.0f}s]")
XGo = load_gibbs(tag, 4242)[0]; XGc, gGc, fGc = load_gibbs(tag, 777); EGc = fGc + gGc
log(f"    Gibbs samples of ws_P9/cache (coordinator's sampler): seed 4242 guides the reductions, seed 777 is the check sample ({len(XGc)} states, {float((XGc != np.array(x0)[None]).sum(1).mean()):.2f} sites off the anchor on average)")
if ENUM:
    st, gE, _ = enumerate_g(G, tag); EE = pw.f_energy(st, c0, h, J) + gE
    lnZ = float(-BETA * EE.min() + math.log(np.exp(-BETA * (EE - EE.min())).sum()))
    log(f"    enumeration: {len(st)} states, exact ln Z = {lnZ:.6f}")
zn, znn = np.zeros(n), np.zeros((n, n))


def base(gs, g2, eta=None):
    return build_window_models_occ(WindowModel, k, x0, c0, h, J, d, w, EPS_G, M, gs, g2, eta, XG=XGo, far_pairs="anchored")


def add_tables(lo, up, g1, g2, g3):
    for key, tab in (list(enumerate(g1)) if isinstance(g1, list) else list(g1.items())):
        i = key if isinstance(key, int) else key[0]
        lo.one[i] = lo.one[i] - tab; up.one[i] = up.one[i] + tab
    for (i, j), tab in g2.items():
        assert j - i <= w
        lo.add_pair(i, j, -tab); up.add_pair(i, j, tab)
    for U, tab in g3.items():
        lo.add_multi(U, -tab); up.add_multi(U, tab)


def fp_parts(form):
    """P6's floating-point allowances alone, allocated as in the state-independent form of the same name."""
    if form == "S":
        return phi1.copy(), znn
    return L.banded_pair_form(n, m, w, zn, znn, psi1, psi2, 0.0)


def make(source, form):
    if source == "ref":
        Gam = float(chat.sum()); S = np.zeros(n); Gp = np.zeros((n, n)); H = {tr: 0.0 for tr in tris}
        for T, v in zip(subs, chat):
            for i in T: S[i] += v
            for i, j in itertools.combinations(T, 2): Gp[i, j] += v; Gp[j, i] += v
            for tr in itertools.combinations(T, 3):
                if tr in H: H[tr] += v
        absA = 1e-12 * Gam
        tabs = (L.site_form(n, m, S, phi1), znn, None) if form == "S" else L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, absA) + (None,) if form == "B" \
            else window_model.triple_form_two_windows(T9.window_triples, L.RND, n, m, w, w, Gp, H, psi1, psi2, absA, absA)
        return base(*tabs)
    lo, up, info = base(*fp_parts(form))
    if source in ("s1", "s2"):
        s = int(source[1])
        add_tables(lo, up, *(window_form(LD.W[s]) if form == "W" else form_tables(LD.TB[s], form, w)))
    else:
        const = dict(sab=LD.TB[1].sab, cJ1=LD.TB[1].cJ, cJ2=LD.TB[2].cJ)[source]
        add_tables(lo, up, *(window_form_const(subs, const, k, x0, w, off_frequencies(XGo, k, x0)) if form == "W" else form_tables(LD.TB[1], form, w, resolved=False, const=const)))
    return lo, up, info


t1 = time.time(); lo0, up0, info0 = base(zn, znn, None); w0 = lo0.lnZ() - up0.lnZ(); del lo0, up0
log(f"(0) the models with ALL penalties zero (not a sandwich: what the reductions of the evaluated terms cost): width {w0:.6g} nats; {info0['exact']} evaluated terms exact in the window, "
    f"{info0['reduced']} reduced, {info0['far_pairs']} pairs beyond the band ({', '.join(f'{v} {kk}' for kk, v in info0['far_kind'].items())}) [{time.time() - t1:.0f}s, peak RSS {peak_rss():.0f} MB]")
res = dict(seq=seq, m=m, w=w, width_zero=w0, rows={})
log("| source | form | certified bracket of ln Z | width (nats) | beta x mean of m_+ - m_- on the check sample | sandwich violated at Gibbs states | "
    + ("violated at any state; exact ln Z inside | " if ENUM else "") + "exact samples of the floor: sites off the anchor (mean); violations | seconds |")
log("|---|---|---|---|---|---|---|---|" + ("---|" if ENUM else ""))
PAIRS = [tuple(v.split(":")) for v in opt("--pairs", "").split(",") if v] or [(source, form) for source in SOURCES for form in FORMS]
for source, form in PAIRS:
    if True:
        if form == "W" and source == "ref":
            continue
        t1 = time.time(); lo, up, _ = make(source, form); a_, b_ = up.lnZ(), lo.lnZ()
        l1, u1 = lo.energy(XGc), up.energy(XGc); vg = int((l1 > EGc + 1e-9).sum() + (u1 < EGc - 1e-9).sum()); fo = BETA * float((u1 - l1).mean())
        R = dict(lnZ_lo=a_, lnZ_hi=b_, width=b_ - a_, first_order=fo, viol_gibbs=vg); cell_e = ""; cell_f = "—"
        if ENUM:
            le, ue = lo.energy(st), up.energy(st); ve = int((le > EE + 1e-9).sum() + (ue < EE - 1e-9).sum())
            R.update(viol_all=ve, inside=bool(a_ <= lnZ <= b_)); cell_e = f"{ve}; {a_ <= lnZ <= b_} | "
        if (source, form) in FLOOR:
            xs = lo.sample(NFLOOR, np.random.default_rng(99)); Ex = pw.f_energy(xs, c0, h, J) + np.concatenate([G.bulk_energy(xs[s:s + 256]) for s in range(0, len(xs), 256)])
            vf = int((lo.energy(xs) > Ex + 1e-9).sum() + (up.energy(xs) < Ex - 1e-9).sum()); offm = float((xs != np.array(x0)[None]).sum(1).mean())
            R.update(floor_viol=vf, floor_off=offm, nfloor=NFLOOR); cell_f = f"{NFLOOR} samples: {offm:.2f}; {vf}"
        res["rows"][f"{source}:{form}"] = R
        log(f"| {source} | {form} | [{a_:.6f}, {b_:.6f}] | **{b_ - a_:.4g}** | {fo:.4g} | {vg} | {cell_e}{cell_f} | {time.time() - t1:.0f} (peak RSS {peak_rss():.0f} MB) |")
        del lo, up
json.dump(res, open(os.path.join(OUT, f"brackets_{stem}.json"), "w"), indent=1)
log.done()
