"""
P6: ADVERSARIAL check of the covering (Proposition P6.1 of the report) through the actual model tables.

The enumeration check `m_- <= E <= m_+` with the real GB energy has little power against an error in the
allocation of the penalties, because the real remainder is 20 to 10^9 times smaller than its certified bound.
The certified class is
     C = { E' : |E'(x) - f(x) - I~(x)| <= env(x) + fp(x) for all x },
     env(x) = sum of chat_T over T inside the changed set S(x)   (EXPLICITLY ENUMERATED subsets, P3's total(m, T)),
     fp(x)  = EPS_G * sum_{U subset S(x), |U| <= m-1} 2^|U|      (P3's floating-point allowance, U = {} included),
     I~     = the stored anchored expansion of order m-1.
A sandwich is valid for every member of C iff it is valid for the two extreme members
     E_low = f + I~ - env - fp,     E_high = f + I~ + env + fp.
This script checks  m_-(x) <= E_low(x)  and  E_high(x) <= m_+(x)  at EVERY state, for the site form and the banded
pair form, for every band, on every instance of a list where C(n, m) <= MAXSUB.  A violation would mean that the
construction is wrong even if the real energy happens to stay inside.

usage: python3 -B p6_06_adversarial.py LISTFILE      (lines: SEQ BB TAU --m ORDERS [--kind K])
"""
import sys, os, time, math, json, itertools
import numpy as np
import p6lib as L
pw = L.pw
BETA = L.BETA
MAXSUB = 500


def run(seq, bb, tau, orders, kind):
    t0 = time.time()
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau, kind)
    n, k = G.ns, G.k
    size = float(np.prod([float(v) for v in k]))
    if size > 3.0e6:
        return None
    kmax = max(k)
    w_p3 = max(1, min(n - 1, int(math.floor(math.log(3e6) / math.log(max(kmax, 2)))) - 1))
    bands = sorted({w_p3, n - 1, 1, 2} & set(range(1, n)), reverse=True)
    st = G.product_states()
    sx = (st != np.array(x0)[None])
    act = np.array([kk > 1 for kk in k])
    nch = (sx & act[None]).sum(1)
    fbase = pw.f_energy(st, c0, h, J)
    sup = L.EnvelopeSup(G)
    out = dict(seq=seq, bb=bb, tau=tau, kind=kind, n=n, size=size, cases=[])
    for m in orders:
        if m > n or math.comb(n, m) > MAXSUB:
            continue
        M = m - 1
        GF = L.GFBound2(G, x0, sup, K=m)
        Gam, S, Gp, srcp = L.load_or_compute_pair_sums(G, GF, x0, seq, bb, tau, kind, m)
        chat = L.enum_chat(GF, m)
        env = L.envelope_value(st, x0, chat)
        d, nball, srcb = L.ball_terms(G, x0, M, seq, bb, tau, kind, verbose=False)
        Itil = pw.expansion_value(d, st)
        fpx = L.EPS_G * np.array([sum(math.comb(t, j) * 2 ** j for j in range(0, min(t, M) + 1)) for t in range(n + 1)])[nch]
        Elow = fbase + Itil - env - fpx
        Ehigh = fbase + Itil + env + fpx
        phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
        for w in bands:
            for form in ("S", "B"):
                if form == "S":
                    gs, g2 = L.site_form(n, m, S, phi1), np.zeros((n, n))
                else:
                    gs, g2 = L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, 5e-9 * Gam)
                lo, up = L.build_models(k, x0, c0, h, J, d, w, M, gs, g2)
                ml, mu = lo.energy(st), up.energy(st)
                tol = 1e-10                      # rounding of the sums of ~200 table entries of size up to 300 kcal/mol
                vl = int((ml > Elow + tol).sum()); vu = int((mu < Ehigh - tol).sum())
                sl = float((Elow - ml).min()); su = float((mu - Ehigh).min())
                # how much of the sandwich width is forced by the class: (m_+ - m_-) / (E_high - E_low), over states off the anchor
                off = nch > 0
                ratio = (mu - ml)[off] / (Ehigh - Elow)[off] if off.any() else np.array([1.0])
                out["cases"].append(dict(m=m, w=w, form=form, states=int(len(st)), viol_lower=vl, viol_upper=vu, min_slack_lower=sl,
                                         min_slack_upper=su, ratio_min=float(ratio.min()), ratio_max=float(ratio.max()), n_subsets=len(chat)))
        cs = [c for c in out["cases"] if c["m"] == m]
        print(f"  {seq}/{bb} tau {tau} {kind} m = {m}: {len(chat)} subsets enumerated, {len(st)} states, bands {bands}: "
              f"violations of m_- <= E_low: {sum(c['viol_lower'] for c in cs)}, of E_high <= m_+: {sum(c['viol_upper'] for c in cs)} "
              f"({2 * len(st) * len(cs)} checks); smallest slack {min(min(c['min_slack_lower'], c['min_slack_upper']) for c in cs):.2e} kcal/mol; "
              f"(m_+ - m_-)/(E_high - E_low) over states off the anchor: site form {min(c['ratio_min'] for c in cs if c['form'] == 'S'):.3f}..{max(c['ratio_max'] for c in cs if c['form'] == 'S'):.3g}, "
              f"banded pair form {min(c['ratio_min'] for c in cs if c['form'] == 'B'):.3f}..{max(c['ratio_max'] for c in cs if c['form'] == 'B'):.3g} [{time.time() - t0:.0f}s]", flush=True)
    return out


def main():
    lst = sys.argv[1]
    t0 = time.time()
    allres = []
    for line in open(lst):
        t = line.split()
        if len(t) < 5:
            continue
        seq, bb, tau = t[0], t[1], float(t[2])
        orders = [int(v) for v in t[t.index("--m") + 1].split(",")]
        kind = t[t.index("--kind") + 1] if "--kind" in t else "gbn2"
        r = run(seq, bb, tau, orders, kind)
        if r is not None and r["cases"]:
            allres.append(r)
    nchk = sum(2 * c["states"] for r in allres for c in r["cases"])
    nv = sum(c["viol_lower"] + c["viol_upper"] for r in allres for c in r["cases"])
    ncase = len({(r["seq"], r["bb"], r["tau"], r["kind"], c["m"]) for r in allres for c in r["cases"]})
    smin = min(min(c["min_slack_lower"], c["min_slack_upper"]) for r in allres for c in r["cases"])
    rS = [c for r in allres for c in r["cases"] if c["form"] == "S"]; rB = [c for r in allres for c in r["cases"] if c["form"] == "B"]
    print(f"TOTAL {os.path.basename(lst)}: {len(allres)} instances, {ncase} (instance, order) cases, {len(rS) + len(rB)} sandwiches, {nchk} checks of the two extreme members of the "
          f"certified class against the models, violations: {nv}; smallest slack {smin:.2e} kcal/mol; ratio (m_+ - m_-)/(E_high - E_low): "
          f"site form {min(c['ratio_min'] for c in rS):.3f}..{max(c['ratio_max'] for c in rS):.3g}, banded pair form {min(c['ratio_min'] for c in rB):.3f}..{max(c['ratio_max'] for c in rB):.3g}")
    os.makedirs(os.path.join(L.HERE, "out"), exist_ok=True)
    json.dump(dict(list=os.path.basename(lst), checks=nchk, violations=nv, cases=ncase, results=allres),
              open(os.path.join(L.HERE, "out", f"adversarial_{os.path.basename(lst).replace('.txt', '')}.json"), "w"), indent=0)
    print(f"DONE p6_06_adversarial {os.path.basename(lst)} [{time.time() - t0:.0f}s]", flush=True)


if __name__ == "__main__":
    main()
