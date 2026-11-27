"""
P4, Propositions 11.18c(a),(b) with Theorem 11.18a on P2's real non-product domains (g_GB):
reference x* = the minimiser of E over the pair-clash-free domain X_tau, domain D'(x*) = the
largest reset-closed part of X_tau at x* (not a product in general).  Third-order constants over
the boxes inside D'(x*) (p4lib.c3_dict_masked), I_2 g from the ball points inside D'(x*), and the
models  env3 / pair form / site form  on D'(x*):
  * the remainder bound |g - I_2 g| <= sum_{T subset S} c_T and m <= E at every state of D'(x*)
    (the content of Proposition 11.18c(a) for Theorems 11.18 and 11.18a);
  * does x* minimise each model over D'(x*)?  (a certificate, given the constants, that the
    minimiser of X_tau is the minimiser over D'(x*));  ln Z over D'(x*) of each model against E.
usage: python3 -B p4_07_dprime3.py  -> out/p4_07_dprime3.json ; last line "DONE p4_07_dprime3"
"""
import sys, os, re, glob, json, time, math
import numpy as np
import p4lib as L4

t00 = time.time()
BETA = L4.BETA


def lnZm(Em, D):
    e = Em[D]
    m = e.min()
    return float(np.log(np.exp(-BETA * (e - m)).sum()) - BETA * m)


rows = []
for p in sorted(glob.glob(os.path.join(L4.P2, "out", "an_fb_*_R3_t0.60_tau*.json"))):
    mm = re.match(r"an_(fb_([A-Z]+?)c?(\d+)_([A-Za-z0-9]+)_R3_t0\.60)_tau([0-9.]+)\.json", os.path.basename(p))
    if not mm:
        continue
    tag, res, nres, bb, taus = mm.group(1), mm.group(2), int(mm.group(3)), mm.group(4), mm.group(5)
    J = json.load(open(p))
    if J.get("empty") or "iface|GB" not in J or J["clashfree"] == J["size"]:
        continue
    t0 = time.time()
    inst = L4.load_instance(tag, float(taus))
    Xt = inst["Xt"]; shape = Xt.shape; n = len(shape)
    f = inst["Rraw"]["f"]; g = inst["Rraw"]["GB"]
    E = np.where(Xt, f + g, np.inf)
    xs = L4.argmin_index(E)
    D = L4.dprime_mask(Xt, xs)
    # sites that can change inside D'
    act = [i for i in range(n) if L4.line(D, xs, i).sum() >= 2]
    if len(act) < 3:
        continue
    gm = np.where(D, g, 0.0)
    c3 = L4.c3_dict_masked(g, D)
    I2 = L4.interp2(gm, xs)                                      # on D' only ball points inside D' enter
    rem = np.where(D, g - I2, 0.0)
    pen = L4.triple_penalty(shape, xs, c3)
    slack = float(np.where(D, pen - np.abs(rem), np.inf).min())
    gam = np.zeros(n); gam2 = np.zeros((n, n))
    for (i, j, k), v in c3.items():
        for s_ in (i, j, k):
            gam[s_] += v / 3.0
        for (u, w) in ((i, j), (i, k), (j, k)):
            gam2[u, w] += v / 3.0; gam2[w, u] += v / 3.0
    base = f + I2
    lnZE = lnZm(E, D)
    out = dict(tag=tag, res=res, nres=nres, bb=bb, tau=taus, shape_raw=list(shape), nXt=int(Xt.sum()), nD=int(D.sum()), xstar=list(xs), nact=len(act),
               c3max=max(c3.values()), c3sum=sum(c3.values()), rem_max=float(np.abs(rem).max()), bound_slack_min=slack, models={})
    for nm, mod in (("env3", base - pen), ("pair", base - L4.pair_penalty(shape, xs, gam2)), ("site", base - L4.site_penalty(shape, xs, gam))):
        md = np.where(D, mod, np.inf)
        gap = np.where(D, (f + g) - mod, np.inf)
        v = md[xs]; md2 = md.copy(); md2[xs] = np.inf
        out["models"][nm] = dict(sound=float(gap.min()), margin=float(md2.min() - v), dlnZ=lnZm(md, D) - lnZE)
    rows.append(out)
    ms = out["models"]
    print(f"[{time.time() - t00:5.0f}s] {res}{nres}/{bb} tau {taus}: |X_tau| {out['nXt']} |D'(x*)| {out['nD']}; c3 max {out['c3max']:.4f} sum {out['c3sum']:.4f}; bound slack {slack:.1e}; "
          f"sound {min(ms[k]['sound'] for k in ms):.1e}; margin env3/pair/site {ms['env3']['margin']:.4f}/{ms['pair']['margin']:.4f}/{ms['site']['margin']:.4f}; "
          f"dlnZ {ms['env3']['dlnZ']:.2e}/{ms['pair']['dlnZ']:.2e}/{ms['site']['dlnZ']:.2e} ({time.time() - t0:.0f}s)", flush=True)
json.dump(rows, open(os.path.join(L4.HERE, "out", "p4_07_dprime3.json"), "w"), indent=0)
n = len(rows)
print(f"\n{n} analyses of g_GB with a non-product X_tau and at least three sites that can change inside D'(x*)")
print(f"remainder bound of Theorem 11.18 (m = 3) on D'(x*), constants over the boxes inside D'(x*): smallest slack {min(r['bound_slack_min'] for r in rows):.2e}; "
      f"smallest E - m over all states, domains and models {min(v['sound'] for r in rows for v in r['models'].values()):.2e}")
for k in ("env3", "pair", "site"):
    print(f"x* minimises the {k} model over D'(x*): {sum(r['models'][k]['margin'] >= -1e-9 for r in rows)} of {n};  by family:",
          {fam: f"{sum(r['models'][k]['margin'] >= -1e-9 for r in rows if r['res'] == fam)}/{sum(1 for r in rows if r['res'] == fam)}" for fam in ("F", "K", "LKSE")})
print("not certified by the pair model:", [f"{r['res']}{r['nres']}/{r['bb']}({r['tau'][1:]}): env3 {r['models']['env3']['margin']:.3f}, pair {r['models']['pair']['margin']:.3f}, c3max {r['c3max']:.2f}" for r in rows if r["models"]["pair"]["margin"] < -1e-9])
print(f"[{time.time() - t00:.0f}s] DONE p4_07_dprime3")
