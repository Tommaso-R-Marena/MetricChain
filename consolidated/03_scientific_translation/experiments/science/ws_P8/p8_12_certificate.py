"""
P8 step 4, demonstration (beyond the brief) -- the existing certificate pipeline fed with the new constants.

Nothing in the pipeline is mine: the banded models, the transfer matrix and the exact sampler are workstream P3's
(pwmodel), the site / banded-pair / banded-triple penalty forms and the floating-point allowances are workstream P6's
(p6lib.fp_tables, site_form, banded_pair_form; Lemma A, A'), the models with exact in-window evaluated terms and the
two-window triple form are the coordinator's (pi_inference/window_model.py).  They are imported read-only (p6lib copies
enclosure tables into its own cache when it is imported: that copy is switched off here, and its cache directory is
redirected to ws_P8/cache, so nothing is written outside ws_P8).  What is mine: the per-subset constants chat_T
(p8sr.py; Theorem AH / Proposition S), from which the site sums S_i, pair sums G_ij and triple sums H_ijk are formed by
plain summation, and this driver.

Validity of the sandwich m_- <= E <= m_+ : P6's Proposition P6.1 / the coordinator's window models need only
|g(x) - I_{m-1} g(x)| <= sum_{T subset S(x), |T| = m} chat_T, which is Theorem AH for the variants 'SA', 'SAb', 'AH' and
P3's Proposition 1 + Proposition S for 'S', 'Sb' (and P3's own for 'P3').

usage: python3 -B p8_12_certificate.py SEQ BB TAU M W [--variant SAb] [--enum] [--budget SECONDS] [--nsamp 2000]
  --enum : enumerated instance (constants from out/bc_<tag>.json or out/sr_<tag>.json; the sandwich is checked at EVERY
           state and the exact ln Z must lie in the bracket);
  default: an instance too large to enumerate (constants from out/g12_/g12b_<tag>_m<M>.npz; the ball is evaluated with
           checkpoints; the sandwich is checked at the Gibbs states and at exact samples of the floor).
writes logs/cert_<tag>_m<M>_w<W>_<variant>.log, out/cert_<tag>_m<M>_w<W>_<variant>.json
"""
import sys, os, json, time, math, itertools, shutil, hashlib
import numpy as np
from p8lib import *
_copy, _mk = shutil.copy, os.makedirs
shutil.copy = lambda *a_, **k_: None                  # p6lib copies P3's tables into ws_P6/cache at import: switched off
os.makedirs = lambda *a_, **k_: None
sys.path.insert(0, os.path.join(SCI, "ws_P6"))
import p6lib as L                                     # P6 (read-only)
import p6_09_triple as T9                             # P6 (read-only)
shutil.copy, os.makedirs = _copy, _mk
encl.CACHE = MYCACHE; L.encl.CACHE = MYCACHE; L.MYCACHE = MYCACHE
sys.path.insert(0, os.path.join(SCI, "pi_inference"))
import window_model                                   # coordinator (read-only; no side effects at import)
pw = L.pw
WM, build_window_models, diff_window = window_model.make(pw)

a = sys.argv[1:]
seq, bb, tau, m, W = a[0], a[1], float(a[2]), int(a[3]), int(a[4])
VAR = a[a.index("--variant") + 1] if "--variant" in a else "SAb"
ENUM = "--enum" in a
BUDGET = float(a[a.index("--budget") + 1]) if "--budget" in a else 1e18
NS = int(a[a.index("--nsamp") + 1]) if "--nsamp" in a else 2000
tag = tagname(seq, bb, tau)
stem = f"cert_{tag}_m{m}_w{W}_{VAR}"
if os.path.exists(os.path.join(HERE, "out", stem + ".json")) and "--force" not in a:
    print(f"out/{stem}.json exists: this run is complete; nothing done"); sys.exit(0)
M = m - 1
G = GBModel(seq, bb, tau=tau)
n, k = G.ns, list(G.k)
c0, h, J = pw.known_tables(G)
x0, E0, nev = pw.icm_anchor(G, c0, h, J)
x0 = tuple(int(v) for v in x0)
ah = hashlib.sha1(str((x0, [list(map(int, dd)) for dd in G.dom])).encode()).hexdigest()[:10]
ballfile = os.path.join(MYCACHE, f"ball_{tag}_M{M}_{ah}.npz")
ballckpt = os.path.join(MYCACHE, f"ball_{tag}_M{M}_{ah}_ckpt.npz")
resume = os.path.exists(ballckpt) and not os.path.exists(ballfile)
log = Log(os.path.join(HERE, "logs", stem + ".log"), append=resume)
t0 = time.time()
dom = float(np.prod([float(v) for v in k]))
log(f"=== p8_12_certificate: {seq} on {bb}, tau {tau}: {G.nat} atoms, {n} sites, states per site {k}, {dom:.6g} assignments; anchor (ICM) {x0}, E = {E0:.6f} kcal/mol; "
    f"order m = {m}, band {W}, constants '{VAR}'" + ("; enumerated instance" if ENUM else "") + ("; RESUMING the ball" if resume else ""))

# ------------------------------------------------------------------ constants of the subsets of order m
chat = {}
if ENUM:
    src = None
    for fn, key in ((f"bc_{tag}.json", "per_subset"), (f"sr_{tag}.json", "per_subset")):
        p_ = os.path.join(HERE, "out", fn)
        if os.path.exists(p_):
            Jd = json.load(open(p_))
            if VAR in Jd[key]:
                chat = {tuple(int(v) for v in s_.split("-")): float(c_) for s_, c_ in Jd[key][VAR].items() if len(s_.split("-")) == m}
                src = fn
                break
    assert src is not None, f"variant {VAR} not found for the enumerated instance"
    Zm = np.load(os.path.join(HERE, "out", f"m1_{tag}.npz"))
    assert tuple(int(v) for v in Zm["anchor"]) == x0, "the ICM anchor differs from the anchor of the enumeration (argmin E)"
else:
    Z = np.load(os.path.join(HERE, "out", f"g12_{tag}_m{m}.npz"))
    assert tuple(int(v) for v in Z["anchor"]) == x0
    V = [str(v) for v in Z["variants"]]
    if VAR in V:
        vals_ = Z["C"].sum(axis=2)[:, V.index(VAR)]; src = f"g12_{tag}_m{m}.npz"
    else:
        Zb = np.load(os.path.join(HERE, "out", f"g12b_{tag}_m{m}.npz"))
        assert np.array_equal(Zb["T"], Z["T"])
        vals_ = Zb["Cb"][:, [str(v) for v in Zb["variants"]].index(VAR)]; src = f"g12b_{tag}_m{m}.npz"
    chat = {tuple(int(v) for v in T): float(c_) for T, c_ in zip(Z["T"], vals_)}
nsub_expected = len([T for T in itertools.combinations(range(n), m) if all(k[i] >= 2 for i in T)])
assert len(chat) == nsub_expected, (len(chat), nsub_expected)
Gam = sum(chat.values())
S = np.zeros(n); Gp = np.zeros((n, n))
for T, v in chat.items():
    for i in T:
        S[i] += v
    for i, j in itertools.combinations(T, 2):
        Gp[i, j] += v; Gp[j, i] += v
tris = T9.window_triples(n, W)
H = {tr: 0.0 for tr in tris}
for T, v in chat.items():
    for tr in itertools.combinations(T, 3):
        if tr in H:
            H[tr] += v
absA = 1e-12 * Gam                                    # allowance for the rounding of these plain sums of at most C(n, m) positive doubles
log(f"(1) {len(chat)} constants from {src}: Gamma_{m} = {Gam:.6g} kcal/mol = {BETA * Gam:.5g} kT; {len(tris)} in-window triple sums [{time.time() - t0:.0f}s]")
phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
tabs = {"S": (L.site_form(n, m, S, phi1), np.zeros((n, n)), None)}
tabs["B"] = L.banded_pair_form(n, m, W, S, Gp, psi1, psi2, absA) + (None,)
tabs["T"] = window_model.triple_form_two_windows(T9.window_triples, L.RND, n, m, W, W, Gp, H, psi1, psi2, absA, absA)

# ------------------------------------------------------------------ the ball (checkpointed)
blocks, tot = pw.ball_states(k, x0, M)
allst = np.concatenate([b_ for _, b_ in blocks], axis=0)
if os.path.exists(ballfile):
    z = np.load(ballfile); vals = z["vals"]
    assert z["states"].shape == allst.shape and np.array_equal(z["states"], allst)
    log(f"(2) ball of radius {M}: {tot} values read from {os.path.basename(ballfile)}")
else:
    if resume:
        z = np.load(ballckpt); vals = z["vals"]; i_next = int(z["i_next"])
        log(f"    ball checkpoint read: {i_next} of {tot} evaluations done")
    else:
        vals = np.zeros(tot); i_next = 0
    tlast = time.time(); stopped = False
    CH = 256                                           # states per call of P2's block evaluator (small batches are faster and lighter)
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
        log("BUDGET REACHED in the ball: checkpoint on disk, run the same command again to continue (not a complete run)")
        log.f.close(); sys.exit(0)
    np.savez(ballfile, states=allst.astype(np.int16), vals=vals)
    log(f"(2) ball of radius {M}: {tot} evaluations of the solvent term ({100 * tot / dom:.2g} % of the domain) [{time.time() - t0:.0f}s]")
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
log(f"    anchored terms of order <= {M}: {len(d)} tables [{time.time() - t0:.0f}s, RSS {rss_mb():.0f} MB]")

# ------------------------------------------------------------------ the states at which the sandwich is checked
if ENUM:
    XC = G.product_states()
    EC = pw.f_energy(XC, c0, h, J) + Zm["g"]
    devg = float(np.abs(G.energy(XC[:64]) - Zm["g"][:64]).max())
    assert devg < 1e-8
    lnZ_exact = float(-BETA * EC.min() + np.log(np.exp(-BETA * (EC - EC.min())).sum()))
    what = f"all {len(XC)} states"
else:
    Zg = np.load(os.path.join(HERE, "out", f"gibbs_{tag}.npz"))
    assert tuple(int(v) for v in Zg["anchor"]) == x0
    XC = Zg["X"]
    EC = pw.f_energy(XC, c0, h, J) + G.bulk_energy(XC)
    lnZ_exact = None
    what = f"the {len(XC)} Gibbs states of the true ensemble"
res = dict(seq=seq, bb=bb, tau=tau, m=m, w=W, variant=VAR, n=n, domain=dom, nball=int(tot), Gamma_kT=BETA * Gam, forms={}, lnZ_exact=lnZ_exact)
models = {}
for form, name in (("S", "site penalties"), ("B", "banded pair penalties"), ("T", "banded triple penalties")):
    t1 = time.time()
    lo, up, info = build_window_models(k, x0, c0, h, J, d, W, L.EPS_G, M, *tabs[form])
    a_, b_ = up.lnZ(), lo.lnZ()
    models[form] = (lo, up)
    l1, u1 = lo.energy(XC), up.energy(XC)
    v_lo = int((l1 > EC + 1e-9).sum()); v_up = int((u1 < EC - 1e-9).sum())
    inside = (a_ <= lnZ_exact <= b_) if lnZ_exact is not None else None
    res["forms"][form] = dict(lnZ_lo=a_, lnZ_hi=b_, width=b_ - a_, viol_lo=v_lo, viol_up=v_up, info=info, exact_inside=inside,
                              max_E_minus_lo=float((EC - l1).max()), max_up_minus_E=float((u1 - EC).max()))
    log(f"(3) form {form} ({name}), exact window terms ({info['exact']} terms of order >= 3 exact, {info['reduced']} reduced, {info['far_pairs']} pairs beyond the band): "
        f"ln Z(E) in [{a_:.6f}, {b_:.6f}], width {b_ - a_:.6g} nats; m_- > E at {v_lo}, m_+ < E at {v_up} of {what}"
        + (f"; exact ln Z = {lnZ_exact:.6f} inside: {inside}" if lnZ_exact is not None else "") + f" [{time.time() - t1:.0f}s, RSS {rss_mb():.0f} MB]")
# ------------------------------------------------------------------ what part of the width is NOT the constants
# The same window models with every penalty set to zero.  This is NOT a sandwich (nothing pays for the remainder
# g - I_{m-1} g); its width is what the pipeline's reduction of the evaluated terms that do not fit the band (each is
# replaced by its minimum / maximum over some of its sites) and of the pairs beyond the band costs by itself, plus
# P6's constant allowance -- the part of every bracket above that no constant chat_T can remove.
t1 = time.time()
lo0, up0, info0 = build_window_models(k, x0, c0, h, J, d, W, L.EPS_G, M, np.zeros_like(tabs["S"][0]), np.zeros((n, n)), None)
w0 = lo0.lnZ() - up0.lnZ()
res["width_zero_penalties"] = w0
log(f"(3b) the same models with ALL PENALTIES SET TO ZERO (not a sandwich): width {w0:.6g} nats -- the part of the brackets above that comes from the reduction of the {info0['reduced']} evaluated "
    f"terms that do not fit the band (sum of their sup-norm slacks {info0['reduced_sup']:.4g} kcal/mol) and of the {info0['far_pairs']} pairs beyond it, not from the constants; "
    f"widths minus this: " + ", ".join(f"{fm} {res['forms'][fm]['width'] - w0:.4g}" for fm in ("S", "B", "T")) + f" [{time.time() - t1:.0f}s]")
del lo0, up0
# ------------------------------------------------------------------ samples of the floor of the triple form
lo, up = models["T"]
a_, b_ = up.lnZ(), lo.lnZ()
xs = lo.sample(NS, rng)
Ex = pw.f_energy(xs, c0, h, J) + G.bulk_energy(xs)
ml, mu = lo.energy(xs), up.energy(xs)
wts = np.exp(-BETA * (Ex - ml)); est = b_ + math.log(wts.mean()); se_est = float(wts.std(ddof=1) / math.sqrt(len(wts)) / wts.mean())
offx = (xs != np.array(x0)[None]).sum(1)
log(f"(4) {NS} exact samples of the floor of the triple form ({len(np.unique(xs, axis=0))} distinct; {offx.mean():.2f} sites off the anchor on average): "
    f"m_- > E at {int((ml > Ex + 1e-9).sum())}, m_+ < E at {int((mu < Ex - 1e-9).sum())}; largest E - m_- = {float((Ex - ml).max()):.4f}, largest m_+ - E = {float((mu - Ex).max()):.4f} kcal/mol")
log(f"    uncertified estimate by reweighting the floor's samples: ln Z(E) = {est:.6f} +- {se_est:.6f} (inside the bracket: {a_ <= est <= b_})")
res["floor_samples"] = dict(N=NS, viol_lo=int((ml > Ex + 1e-9).sum()), viol_up=int((mu < Ex - 1e-9).sum()), est=est, se=se_est, mean_off=float(offx.mean()))
with open(os.path.join(HERE, "out", stem + ".json"), "w") as fh:
    json.dump(res, fh, indent=1)
log.done()
