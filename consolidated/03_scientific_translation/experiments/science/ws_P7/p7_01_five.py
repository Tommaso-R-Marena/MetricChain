"""
P7 item 1: the analyses of workstream P4 in which the reference minimises the lower model and neither
constant nor state-dependent shares certify it -- identified from P4's stored outputs, recomputed from
P2's grids with this workstream's own linear programmes, and the SIZE OF THE GAP made exact.

For each such analysis (instance, split = residual, order, domain X'):
  margin      min_{x != x0} L(x) - L(x0) by enumeration of P4's model grid (the true minimum is L(x0));
  t           optimum of the share LP with slack (P4's quantity; < 0 <=> no shares), compared with P4's stored value;
  relaxation  value of the pairwise (local-polytope) relaxation of min (L - L(x0)), by the primal LP;
  exact       the LP vertex read as a rational point (denominator found, every constraint re-checked in
              integer arithmetic) and its value computed exactly (i) for the float-table model as a
              Fraction, (ii) for the published integer instance (tables rounded down to 2^-40): a feasible
              fractional point with a negative value PROVES that no shares exist (weak duality);
  bracket     an exact dual bound (integer messages, the checker of p7lib.leaf_bound) below it.

usage: python3 -B p7_01_five.py > logs/p7_01_five.log     (writes out/p7_01_five.json; last line "DONE p7_01_five")
"""
import sys, os, json, time
sys.dont_write_bytecode = True
import numpy as np
import p7lib as L7
from p7lib import PM, IPM, L4, Fraction

t00 = time.time()
print(f"p7_01_five  started {L7.now()}")
P4OUT = os.path.join(L7.P4, "out")

# ---------------------------------------------------------------- 1. what P4's stored outputs say
rows4 = json.load(open(os.path.join(P4OUT, "p4_01_shares.json")))
print(f"\nP4 second order (out/p4_01_shares.json): {len(rows4)} analyses")
print(f"{'residual':16s} {'analyses':>8s} {'x0 minimises L':>14s} {'constant shares':>15s} {'state shares':>12s} {'neither (gap)':>13s}")
gaps = []
tot = [0, 0, 0, 0, 0]
for name in L7.RESIDUALS:
    R = [r for r in rows4 if r["name"] == name]
    ex = [r for r in R if r["exact"]]
    sh = [r for r in ex if r["shares"]]
    ss = [r for r in ex if not r["shares"] and r["sshares_slack_exact"] is not None and r["sshares_slack_exact"] >= 0]
    gp = [r for r in ex if not r["shares"] and not (r["sshares_slack_exact"] is not None and r["sshares_slack_exact"] >= 0)]
    gaps += gp
    for k, v in enumerate((len(R), len(ex), len(sh), len(sh) + len(ss), len(gp))):
        tot[k] += v
    print(f"{name:16s} {len(R):8d} {len(ex):14d} {len(sh):15d} {len(sh) + len(ss):12d} {len(gp):13d}")
print(f"{'all':16s} {tot[0]:8d} {tot[1]:14d} {tot[2]:15d} {tot[3]:12d} {tot[4]:13d}")
rows3 = json.load(open(os.path.join(P4OUT, "p4_02_third.json")))
third = {}
for form in ("pair", "site"):
    mins = [r for r in rows3 if r["models"][form]["margin"] >= -1e-9]
    sh = [r for r in mins if r["cert"][form]["shares"]]
    ss = [r for r in mins if not r["cert"][form]["shares"] and r["cert"][form]["sshares_slack"] is not None and r["cert"][form]["sshares_slack"] >= 0]
    third[form] = dict(instances=len(rows3), minimised=len(mins), const=len(sh), state=len(sh) + len(ss), gap=len(mins) - len(sh) - len(ss))
    print(f"P4 third order, {form} form (out/p4_02_third.json): {len(rows3)} instances, reference minimises the model in {len(mins)}, "
          f"constant shares {len(sh)}, state-dependent shares {len(sh) + len(ss)}, neither {len(mins) - len(sh) - len(ss)}")
rowsj = json.load(open(os.path.join(P4OUT, "p4_08_joint.json")))
env_ok = [r for r in rowsj if r["margin_env3"] >= -1e-9]
joint_ok = [r for r in rowsj if r["exact_slack"] is not None and r["exact_slack"] >= 0]
third["joint"] = dict(instances=len(rowsj), envelope_minimised=len(env_ok), joint=len(joint_ok),
                      gap=len([r for r in env_ok if not (r["exact_slack"] is not None and r["exact_slack"] >= 0)]))
print(f"P4 joint programme (out/p4_08_joint.json): {len(rowsj)} instances, reference minimises the three-body envelope in {len(env_ok)}, "
      f"joint certificate in {len(joint_ok)}, envelope minimised but no joint certificate: {third['joint']['gap']}")
print(f"\n==> analyses with 'reference minimises the model, no shares of either kind': {len(gaps)} (second order) + "
      f"{third['pair']['gap']} + {third['site']['gap']} + {third['joint']['gap']} (third order: pair form, site form, joint)")

# ---------------------------------------------------------------- 2. recompute each of them
out = []
cache = {}
for r in gaps:
    tag, tau, name = r["tag"], float(r["tau"]), r["name"]
    t0 = time.time()
    inst = L4.load_instance(tag, tau)
    Lmod, x0, E, C = L7.second_order_grid(inst, name)
    assert list(x0) == r["x0"] and list(inst["shape"]) == r["shape"]
    margin = L4.margin_at(Lmod, x0)
    pm = PM.from_grid(Lmod, x0)
    G = pm.grid()
    pwerr = float(np.abs(G - (Lmod - Lmod[x0])).max())           # the model is pairwise up to this (floating-point noise of the grid)
    ipm = IPM(pm)
    IG = ipm.grid()
    assert int(IG.min()) == 0 and int(IG[x0]) == 0               # exact: the published instance is minimised at x0
    nmin = int((IG == 0).sum())
    s = L7.shares_lp(pm)
    p = L7.primal_lp(pm)
    d = L7.dual_lp(pm, pm.full_domain())
    rp = L7.rationalise_point(pm, ipm, p["mu1"], p["mu2"])
    assert rp is not None, "no small common denominator"
    assert rp["value"] < 0 and rp["value_int"] < 0               # exact: a fractional point below the minimum
    mI = L7.messages_to_int(d["m"])
    LB, U, Pd = L7.leaf_bound(ipm, pm.full_domain(), mI)
    frac_sites = [i for i in range(pm.n) if rp["support"][i] > 1]
    vertex = {str(i): [(int(a), f"{int(rp['N1'][i][a])}/{rp['den']}") for a in np.flatnonzero(rp["N1"][i])] for i in range(pm.n)}
    row = dict(tag=tag, tau=r["tau"], split=name, order=2, family=r["res"], nres=r["nres"], bb=r["bb"], shape=list(pm.shape), size=int(np.prod(pm.shape)),
               x0=list(x0), cmax=float(C.max()), margin=margin, margin_P4=r["margin"], t=s["t"], t_P4=r["sshares_t"],
               relaxation=p["val"], dual_value=d["val"], pairwise_err=pwerr, n_minimisers_published=nmin,
               vertex_den=rp["den"], vertex_value_exact=float(rp["value"]), vertex_value_exact_str=str(rp["value"]),
               vertex_value_published=float(rp["value_int"]) * L7.UNIT, dual_bound_published=LB * L7.UNIT,
               fractional_sites=frac_sites, vertex=vertex, lp_size=[p["nvar"], p["nrow"]],
               E_min=float(E[x0]), L_x0=float(Lmod[x0]))
    out.append(row)
    print(f"\n{r['res']}{r['nres']}/{r['bb']}  tau {r['tau']}  split {name}  order 2  domain X' = {list(pm.shape)} ({row['size']} states)  x0 = {list(x0)}")
    print(f"   max c_ij = {row['cmax']:.3e}; model pairwise up to {pwerr:.1e}; x0 is the unique minimiser of the published instance: {nmin == 1}")
    print(f"   margin (enumeration) = {margin:.9f}  (P4 stored {r['margin']:.9f});   share LP t = {s['t']:.9f}  (P4 stored {r['sshares_t']:.9f})")
    print(f"   relaxation value - L(x0): primal LP {p['val']:.9f}, dual LP {d['val']:.9f}   [true minimum - L(x0) = 0]")
    print(f"   EXACT: LP vertex has denominator {rp['den']}; all constraints hold in integers; value = {float(rp['value']):.12f} (float-table model, exact Fraction), "
          f"{float(rp['value_int']) * L7.UNIT:.12f} (published instance) < 0  ==> no shares exist")
    print(f"   EXACT bracket of the relaxation value of the published instance: [{LB * L7.UNIT:.12f}, {float(rp['value_int']) * L7.UNIT:.12f}]")
    print(f"   fractional sites {frac_sites};  vertex (site: [(state, weight)]): {vertex}")
    print(f"   LP size {p['nvar']} variables x {p['nrow']} rows  ({time.time() - t0:.1f}s)")

json.dump(dict(P4_counts=dict(second=tot, third=third), gaps=out), open(os.path.join(L7.HERE, "out", "p7_01_five.json"), "w"), indent=1)
print(f"\nSUMMARY (gap = L(x0) - value of the relaxation, kcal/mol; margin = second-best state above L(x0))")
print(f"{'instance':10s} {'tau':4s} {'split':15s} {'X′':24s} {'states':>7s} {'margin':>9s} {'gap':>11s} {'gap/margin':>10s} {'frac. sites':>14s}")
for r in out:
    print(f"{r['family'] + str(r['nres']) + '/' + r['bb']:10s} {r['tau']:4s} {r['split']:15s} {str(r['shape']) if len(r['shape']) <= 6 else '2 x 16':24s} {r['size']:7d} "
          f"{r['margin']:9.6f} {-r['relaxation']:11.6f} {-r['relaxation'] / r['margin']:10.2f} {str(r['fractional_sites']) if len(r['fractional_sites']) <= 6 else str(len(r['fractional_sites'])) + ' sites':>14s}")
print(f"\n[{time.time() - t00:.0f}s] wrote out/p7_01_five.json   finished {L7.now()}")
print("DONE p7_01_five")
