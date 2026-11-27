#!/usr/bin/env python3
"""R19, items 3-5: MEASURING the loss between groups at production size (the division writes "about D^2/4" and "measured";
the logs contain no such measurement beyond five residues).

loss := (corrected width of Proposition A17.19)  -  (width with the SAME routed items put back exactly)
      = [UP - LP]  -  [ ln Z(m_- + s_-) - ln Z(m_+ - s_+) ],      s_+- the sums of the routed items.
ln Z(m_+ - s_+) and ln Z(m_- + s_-) are not transfer-matrix quantities (the items fit no window).  They are estimated here
from exact samples with the first order removed exactly, so that only second-order terms are sampled:
  Z(m_+ - s_+)/Z(m_-) = < e^{-beta W} >_- = 1 - beta <W>_-  +  < e^{-beta W} - 1 + beta W >_- ,     W = m_+ - s_+ - m_- >= 0,
  Z(m_- + s_-)/Z(m_-) = < e^{-beta s_-} >_- = 1 - beta <s_->_-  +  < e^{-beta s_-} - 1 + beta s_- >_- ,
both under the FLOOR, where the integrands are bounded by one (a first version sampled < e^{+beta s_+} > under the ceiling and
failed its validation on Lys5 at band 2: a heavy tail; see NOTES.md).  The first-order terms are exact: <m_+ - m_->_- by
workstream P3's transfer matrix for moments (checked here by enumeration on the small case), <s_+->_- by
held_site_laws._stats_dir on the stored routes (that module agrees with my own elimination to 6e-12 on every group of Lys12
at band 4); the second-order terms come from N exact samples of the floor (the model's own sampler).
Validation: the five-residue case, where the driver's log has the same two numbers by enumeration.

Run: python3 -B r19_loss_between_groups.py case_K12_m4_w4.pkl 400000 > r19_loss_between_groups_K12_m4_w4.log
"""
import os, sys, math, time, pickle, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "NUMEXPR_MAX_THREADS"):
    os.environ[v] = "1"
sys.dont_write_bytecode = True
SCI = "/home/user/MetricChain/experiments/science"
sys.path.insert(0, os.path.join(SCI, "ws_P3")); sys.path.insert(0, os.path.join(SCI, "pi_inference"))
import numpy as np
import pwmodel as pw
import window_model
import slack_recovery as SR
import held_site_laws as HS
WindowModel, _b, _d = window_model.make(pw)
t00 = time.time()
C = pickle.load(open(sys.argv[1], "rb")); N = int(sys.argv[2]) if len(sys.argv) > 2 else 400000
n, k, w, beta = C["n"], C["k"], C["w"], C["beta"]; items, kind, rts = C["items"], C["kind"], C["rts"]; GS = C["GS"][C["last"]]


def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


def build(T):
    mdl = WindowModel(k, w); mdl.const = T["const"]; mdl.one = [np.array(v) for v in T["one"]]
    for (i, j), tab in T["pair"].items(): mdl.add_pair(i, j, tab)
    for U, tab in T["multi"].items(): mdl.add_multi(U, tab)
    return mdl


up, lo = build(C["up"]), build(C["lo"]); lnZup, lnZlo = up.lnZ(beta), lo.lnZ(beta); D = lnZlo - lnZup
print(f"case {C['args']}: ln Z of the models rebuilt from the stored tables against the driver's: {lnZup - C['lnZup']:+.1e}, {lnZlo - C['lnZlo']:+.1e}; D = {D:.8g}; {sum(r is not None for r in rts)} routed items, {len(GS)} groups "
      f"[{time.time() - t00:.0f}s, peak RSS {rss():.0f} MB]", flush=True)
# ---- the corrected bracket from the driver's statistics (no safety factor), and its four ends
B = SR.bounds(lnZlo, lnZup, GS, beta, safe=0.0); lo_c, up_c = max(B["LJ"], B["LP"]), min(B["UE"], B["UP"])
# ---- exact first-order mean of the routed floor items under the FLOOR, by held-site passes on the stored routes
t1 = time.time(); rmodel = SR.reverse_model(WindowModel, lo); msgs = HS.forward_messages(lo, -beta); rmsgs = HS.forward_messages(rmodel, -beta); b_lo = 0.0; a_lo = 0.0; mass = []
for d_, mdl, fm, bm in (("fwd", lo, msgs, rmsgs), ("rev", rmodel, rmsgs, msgs)):
    pl, mi = [], []
    for j, r in enumerate(rts):
        if r is None or r[0] != d_: continue
        U, tab = items[j] if d_ == "fwd" else SR._mirror(items[j], n)
        if kind[j][1] in (+1, 0): pl.append((U, tab, r[2]))
        if kind[j][1] in (-1, 0): mi.append((U, tab, r[2]))
    if pl or mi:
        for key, st in HS._stats_dir(mdl, fm, bm, [(pl, mi)], beta, lnZlo)[0].items():
            b_lo += st["b"]; a_lo += st["a"]; mass.append(st["mass"])
del msgs, rmsgs
print(f"exact means under the FLOOR by held-site passes on the stored routes: beta <s_-> = {beta * b_lo:.8g}, beta <s_+> = {beta * a_lo:.8g}; largest |mass - 1| = {max(abs(v - 1) for v in mass):.1e} [{time.time() - t1:.0f}s, peak RSS {rss():.0f} MB]", flush=True)


def group_values(X):
    g = {}
    for j, r in enumerate(rts):
        if r is None: continue
        v = np.asarray(items[j][1])[tuple(X[:, u] for u in items[j][0])]; q = g.setdefault(r, [np.zeros(len(X)), np.zeros(len(X))])
        if kind[j][1] in (+1, 0): q[0] += v
        if kind[j][1] in (-1, 0): q[1] += v
    return g


# ---- the mean of m_+ - m_- under the floor, exactly (workstream P3's transfer matrix for the first two moments of a band model under a band model)
dm = _d(lo, up); mean_dm, _m2 = lo.moments(dm, beta)
if "--enum" in C["args"]:                                                 # check of that number by my enumeration, where the space is small
    X = np.stack(np.meshgrid(*[np.arange(v) for v in k], indexing="ij"), axis=-1).reshape(-1, n)
    def en(T):
        e = np.full(len(X), T["const"])
        for i in range(n): e += T["one"][i][X[:, i]]
        for (i, j), tab in T["pair"].items(): e += tab[X[:, i], X[:, j]]
        for U, tab in T["multi"].items(): e += tab[tuple(X[:, u] for u in U)]
        return e
    el, eu = en(C["lo"]), en(C["up"]); wl = np.exp(-beta * (el - el.min())); wl /= wl.sum()
    print(f"<m+ - m-> under the floor: transfer matrix {mean_dm:.10g}, my enumeration {float(wl @ (eu - el)):.10g}")
t1 = time.time(); XL = lo.sample(N, np.random.default_rng(290001 + w)).astype(np.int64); g = group_values(XL)
sp = sum(v[0] for v in g.values()); sm = sum(v[1] for v in g.values())


def model_energy(T, X):
    e = np.full(len(X), T["const"])
    for i in range(n): e += T["one"][i][X[:, i]]
    for (i, j), tab in T["pair"].items(): e += tab[X[:, i], X[:, j]]
    for U, tab in T["multi"].items(): e += tab[tuple(X[:, u] for u in U)]
    return e


Wv = model_energy(C["up"], XL) - model_energy(C["lo"], XL) - sp                 # m+ - s+ - m- >= 0 (the hypotheses: m+ - s+ >= E >= m-)
Yp = np.expm1(-beta * Wv) + beta * Wv; mYp = float(Yp.mean()); seYp = float(Yp.std(ddof=1)) / math.sqrt(N); meanW = mean_dm - a_lo
lower_exact = lnZlo + math.log1p(-beta * meanW + mYp); se_lower = seYp / (1 - beta * meanW + mYp)
chkW = float(Wv.mean()); seW = float(Wv.std(ddof=1)) / math.sqrt(N)
Yv = np.expm1(-beta * sm) + beta * sm; mY = float(Yv.mean()); seY = float(Yv.std(ddof=1)) / math.sqrt(N)
upper_exact = lnZlo + math.log1p(-beta * b_lo + mY); se_upper = seY / (1 - beta * b_lo + mY)
chk2 = float((beta * sm).mean()); se2 = float((beta * sm).std(ddof=1)) / math.sqrt(N)
print(f"floor, {N} exact samples [{time.time() - t1:.0f}s, peak RSS {rss():.0f} MB]: smallest W = m+ - s+ - m- at a sample {float(Wv.min()):.2e} (must be >= 0); beta <W> exact {beta * meanW:.8g}, sampled {beta * chkW:.8g} +- {beta * seW:.2g} "
      f"({(chkW - meanW) / seW:+.2f} standard errors); second order <e^(-beta W) - 1 + beta W> = {mYp:.4g} +- {seYp:.2g}", flush=True)
print(f"    beta <s_-> exact {beta * b_lo:.8g}, sampled {chk2:.8g} +- {se2:.2g} ({(chk2 - beta * b_lo) / se2:+.2f} standard errors); second order <e^(-beta s-) - 1 + beta s-> = {mY:.4g} +- {seY:.2g}", flush=True)
# the two ends come from the SAME samples and their errors are strongly correlated: the standard error of the width is that of the per-sample difference
Zv = Yv / (1 - beta * b_lo + mY) - Yp / (1 - beta * meanW + mYp); se_w = float(Zv.std(ddof=1)) / math.sqrt(N)
w_corr = up_c - lo_c; w_exact = upper_exact - lower_exact; loss = w_corr - w_exact
print(f"corrected bracket (the driver's statistics, no safety factor): [{lo_c:.9f}, {up_c:.9f}], width {w_corr:.6g}   (LJ {B['LJ']:.9f}, LP {B['LP']:.9f}, UE {B['UE']:.9f}, UP {B['UP']:.9f})")
print(f"the same routed items put back exactly:                        [{lower_exact:.9f} +- {se_lower:.1e}, {upper_exact:.9f} +- {se_upper:.1e}], width {w_exact:.6g} +- {se_w:.1e}")
print(f"LOSS BETWEEN GROUPS, measured: lower end {lower_exact - lo_c:.4g} +- {se_lower:.1e}, upper end {up_c - upper_exact:.4g} +- {se_upper:.1e}, total {loss:.4g} +- {se_w:.1e} nats;  D^2/4 = {D * D / 4:.4g};  "
      f"loss / (D^2/4) = {loss / (D * D / 4):.3f} +- {se_w / (D * D / 4):.3f};  loss / corrected width = {loss / w_corr:.3f};  what the exact treatment of the routed items leaves (envelope, items without a route, allowances): {w_exact:.4g}")
if "--enum" in C["args"]:
    print("    (validation: compare the second line with the driver's own enumeration, 'ln Z of the models with the routed items put back exactly', in the committed *_enum.log)")
print(f"ALL DONE {time.time() - t00:.0f} s; peak RSS {rss():.0f} MB")
