"""
Mechanism analysis: where do the constants of g_GB in rotamer variables come from?

usage: python3 -B an_mech.py TAG TAU

On the pruned product domain X'(TAU) of an enumerated model the GBn2 energy is split in two ways:
  (a) GB = GBself + GBcross      self = -(pref/2) sum_p q_p^2 / B_p(x)   (desolvation: depends on x
                                 only through the Born radii)
                                 cross = -pref sum_{p<q} q_p q_q / f_GB(r_pq, B_p B_q)
  (b) GB = GBfrozen + GBfluct    GBfrozen = the GB expression with the Born radii frozen at their
                                 values in the reference assignment x0 = argmin f: pair-additive
                                 in atoms, hence EXACTLY pairwise in the sites and computable
                                 without knowing the radii of any other assignment;
                                 GBfluct = GB - GBfrozen: the part that exists only because the
                                 radii respond to the rotamers.
For every part: c_i, c_ij (max, half row sums), c_ijk (max, sum).  Also the alternative residuals
coul+GB ("solvated electrostatics") and coul+GBfrozen.  Output: out/mech_<tag>_tau<TAU>.json
"""
import sys, os, json, time
import numpy as np
from anlib import *
from fbmodel import FBModel

np.set_printoptions(precision=3, suppress=True, linewidth=220)
tag, tau = sys.argv[1], float(sys.argv[2])
from an_main import pruned_product, subselect
d0 = load_fb(tag)
d = restrict(d0, tau) if tau > d0["tau_enum"] + 1e-12 else d0
if not (d["s2min"] > tau).all():
    d = subselect(d, pruned_product(d, tau))          # pair-clash-free product X'
shape = d["shape"]; n = len(shape)
Mdl = FBModel(d["seq"], d["bb"], grid=d["grid"], extra_ffs=())
st = Mdl.product_states(d["dom"])
f = d["tors"] + d["lj"] + d["coul"]
x0 = int(np.argmin(f))
B0 = Mdl.born_radii(st[x0][None])[0]
t0 = time.time()
tot = np.empty(len(st)); eself = np.empty(len(st)); ecross = np.empty(len(st)); frozen = np.empty(len(st))
Bmin = np.full(Mdl.P.natoms, np.inf); Bmax = np.zeros(Mdl.P.natoms)
for s in range(0, len(st), 16384):
    sl = slice(s, s + 16384)
    tot[sl], eself[sl], ecross[sl] = Mdl.gb_energy(st[sl], parts=True)
    frozen[sl] = Mdl.gb_energy(st[sl], Bfix=B0)
    B = Mdl.born_radii(st[sl])
    Bmin = np.minimum(Bmin, B.min(0)); Bmax = np.maximum(Bmax, B.max(0))
assert np.abs(tot - d["gb"].reshape(-1)).max() < 1e-8
parts = {"GB": tot, "GBself": eself, "GBcross": ecross, "GBfrozen": frozen, "GBfluct": tot - frozen,
         "coul": d["coul"].reshape(-1), "coul+GB": d["coul"].reshape(-1) + tot, "coul+GBfrozen": d["coul"].reshape(-1) + frozen,
         "coul+GBcross": d["coul"].reshape(-1) + ecross}
X = np.ones(shape, dtype=bool)
rel = (Bmax - Bmin) / B0
q = Mdl.F.gb["gbn2"]["charge"]
out = dict(tag=tag, tau=tau, shape=list(shape), x0=[int(v) for v in np.unravel_index(x0, shape)],
           born_rel_range_max=float(rel.max()), born_rel_range_mean=float(rel.mean()),
           born_ref_min_A=float(B0.min() * 10), born_ref_max_A=float(B0.max() * 10))
print(f"=== {tag} tau={tau}: {d['seq']} on {d['bb']}, states/site {list(shape)}; reference x0 = argmin f = {out['x0']}")
print(f"    Born radii over the domain: reference values {B0.min()*10:.2f}-{B0.max()*10:.2f} A; relative range (max-min)/ref per atom: "
      f"max {rel.max():.3f}, mean {rel.mean():.3f}   [{time.time()-t0:.0f}s]")
for name, v in parts.items():
    g = v.reshape(shape)
    c, rms, _ = first_order(g, X)
    o = dict(c=[float(x) for x in c], range=float(g.max() - g.min()))
    line = f"    {name:14s} range {o['range']:8.3f}  c_i max {c.max():7.3f}"
    if n >= 2:
        C, _ = second_order(g, X)
        o["C"] = C.tolist(); o["half_rowsum"] = [float(x) for x in 0.5 * C.sum(1)]
        line += f"   c_ij max {C.max():7.3f}  half row sum max {0.5*C.sum(1).max():7.3f}"
    if n >= 3 and max(shape) <= 9:
        T = third_order(g, X)
        o["c3max"] = max(x[0] for x in T.values()); o["c3sum"] = sum(x[0] for x in T.values())
        line += f"   c_ijk max {o['c3max']:.2e} sum {o['c3sum']:.2e}"
    out[name] = o
    print(line, flush=True)
json.dump(out, open(os.path.join(HERE, "out", f"mech_{tag}_tau{tau:.2f}.json"), "w"), indent=0)
