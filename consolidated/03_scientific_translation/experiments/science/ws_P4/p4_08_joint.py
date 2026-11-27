"""
P4 (extension of item 2, "does an LP over shares do better still?"): one linear programme that
chooses the pair shares of the triples AND state-dependent shares of the resulting deficits
together -- a search for a certificate "checked by additions" that needs no enumeration of the domain:

  variables   mu_{T,p} >= 0 (p a pair of T), sum_p mu_{T,p} = 1          (pair shares of each c_T > 0)
              s_ij(a) >= 0 (a a changed state of i), t
  cover       s_ij(a) + s_ji(b) >= sum_{T contains i,j} c_T mu_{T,ij} - M^E_ij(a, b)     (a, b changed)
  loads       sum_{j != i} s_ij(a) + t <= A_i(a)                                          (a changed)
  maximise t.   t >= 0  =>  x0 minimises  f + I_2 g - sum_{changed pairs} gamma_ij(mu)  <= E.

(M^E_ij = second difference of the full energy at x0, A_i = single-site excitation energies; inputs:
the ball data and the measured c_T only.)  Every accepted solution is turned into an exact
certificate: shares clipped and completed so that they add up to at least one in exact arithmetic,
gamma_ij rounded up, state shares repaired and the loads checked exactly (p4lib.verify_state_shares);
and the model is rebuilt on the full grid, where m <= E and "x0 minimises m" are checked by enumeration.

usage: python3 -B p4_08_joint.py   -> out/p4_08_joint.json ; last line "DONE p4_08_joint"
"""
import sys, os, re, glob, json, time, math, itertools
from fractions import Fraction
import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog
import p4lib as L4

t00 = time.time()
prev = {(r["tag"], r["tau"]): r for r in json.load(open(os.path.join(L4.HERE, "out", "p4_02_third.json")))}
rows = []
for p in sorted(glob.glob(os.path.join(L4.P2, "out", "an_fb_*_R3_t0.60_tau*.json"))):
    mm = re.match(r"an_(fb_([A-Z]+?)c?(\d+)_([A-Za-z0-9]+)_R3_t0\.60)_tau([0-9.]+)\.json", os.path.basename(p))
    if not mm:
        continue
    tag, res, nres, bb, taus = mm.group(1), mm.group(2), int(mm.group(3)), mm.group(4), mm.group(5)
    if (tag, taus) not in prev:
        continue
    pr = prev[(tag, taus)]
    t0 = time.time()
    inst = L4.load_instance(tag, float(taus))
    shape = inst["shape"]; n = len(shape)
    f = inst["f"]; g = inst["R"]["GB"]; E = f + g
    x0 = L4.argmin_index(E)
    c3 = L4.c3_dict(g)
    A = L4.excitations(E, x0)
    act = [i for i in range(n) if shape[i] >= 2]
    ME = {(i, j): L4.second_diff(E, x0, i, j) for i in act for j in act if i < j}
    trip = [(T, v) for T, v in c3.items() if v > 0 and all(shape[s] >= 2 for s in T)]
    gmax = np.zeros((n, n))
    for (T, v) in trip:
        for (u, w) in itertools.combinations(T, 2):
            gmax[u, w] += v; gmax[w, u] += v
    # variables: s blocks, then mu, then t
    off = {}
    nv = 0
    for i in act:
        for j in act:
            if i != j:
                off[(i, j)] = nv; nv += shape[i]
    muoff = {}
    for q, (T, v) in enumerate(trip):
        for r_, pr_ in enumerate(itertools.combinations(T, 2)):
            muoff[(T, pr_)] = nv + 3 * q + r_
    nmu = 3 * len(trip)
    tvar = nv + nmu
    pair_trips = {}
    for (T, v) in trip:
        for pr_ in itertools.combinations(T, 2):
            pair_trips.setdefault(pr_, []).append((T, v))
    rws, cls, vls, rhs = [], [], [], []
    r = 0
    for (i, j), M in ME.items():
        tl = pair_trips.get((i, j), [])
        for a in range(shape[i]):
            if a == x0[i]:
                continue
            for b in range(shape[j]):
                if b == x0[j]:
                    continue
                if gmax[i, j] - M[a, b] <= 0:
                    continue
                rws += [r, r]; cls += [off[(i, j)] + a, off[(j, i)] + b]; vls += [-1.0, -1.0]
                for (T, v) in tl:
                    rws.append(r); cls.append(muoff[(T, (i, j))]); vls.append(v)
                rhs.append(float(M[a, b])); r += 1
    for i in act:
        for a in range(shape[i]):
            if a == x0[i]:
                continue
            for j in act:
                if j != i:
                    rws.append(r); cls.append(off[(i, j)] + a); vls.append(1.0)
            rws.append(r); cls.append(tvar); vls.append(1.0)
            rhs.append(float(A[i][a])); r += 1
    Aub = sp.csr_matrix((vls, (rws, cls)), shape=(r, tvar + 1))
    Aeq = sp.csr_matrix((np.ones(nmu), (np.repeat(np.arange(len(trip)), 3), nv + np.arange(nmu))), shape=(len(trip), tvar + 1)) if trip else None
    cost = np.zeros(tvar + 1); cost[tvar] = -1.0
    sol = linprog(cost, A_ub=Aub, b_ub=np.array(rhs), A_eq=Aeq, b_eq=(np.ones(len(trip)) if trip else None),
                  bounds=[(0, None)] * (nv + nmu) + [(None, None)], method="highs")
    out = dict(tag=tag, res=res, nres=nres, bb=bb, tau=taus, shape=list(shape), nvar=int(tvar + 1), nrows=int(r),
               margin_env3=pr["models"]["env3"]["margin"], margin_pair_thirds=pr["models"]["pair"]["margin"],
               thirds_shares=pr["cert"]["pair"]["shares"], thirds_state_shares=pr["cert"]["pair"]["sshares_slack"])
    if sol.x is None:
        out.update(lp_t=None, exact_slack=None, grid_margin=None, grid_sound=None)
    else:
        tval = float(sol.x[tvar])
        # exact certificate: shares
        g2 = np.zeros((n, n)); g2x = {}
        for (T, v) in trip:
            prs = list(itertools.combinations(T, 2))
            mu = [max(Fraction(float(sol.x[muoff[(T, pr_)]])), Fraction(0)) for pr_ in prs]
            tot = sum(mu, Fraction(0))
            if tot < 1:
                mu[0] += 1 - tot                                    # shares add up to at least one, exactly
            for pr_, m_ in zip(prs, mu):
                g2x[pr_] = g2x.get(pr_, Fraction(0)) + Fraction(float(v)) * m_
        for (u, w), val in g2x.items():
            fl = float(val)
            while Fraction(fl) < val:                               # round the pair penalty up
                fl = math.nextafter(fl, math.inf)
            g2[u, w] = g2[w, u] = fl
        ss = {key: sol.x[o:o + shape[key[0]]].copy() for key, o in off.items()}
        MEf = lambda i, j: ME[(i, j)]
        sl = L4.verify_state_shares(g2, MEf, A, x0, shape, ss)
        mod = f + L4.interp2(g, x0) - L4.pair_penalty(shape, x0, g2)
        out.update(lp_t=tval, exact_slack=(float(sl) if sl is not None else None), grid_margin=L4.margin_at(mod, x0), grid_sound=float((E - mod).min()),
                   dlnZ=L4.lnZ(mod) - L4.lnZ(E))
        if sl is not None and sl >= 0:
            assert out["grid_margin"] >= -1e-9 and out["grid_sound"] >= -1e-9, (tag, taus, "exact certificate accepted but the model fails on the grid")
    rows.append(out)
    print(f"[{time.time() - t00:5.0f}s] {res}{nres}/{bb} tau {taus}: LP {out['nvar']} variables, {out['nrows']} rows; t = {out['lp_t']}; exact slack {out['exact_slack']}; "
          f"grid margin {out['grid_margin']}; env3 {out['margin_env3']:.4f}, pair thirds {out['margin_pair_thirds']:.4f} ({time.time() - t0:.1f}s)", flush=True)
json.dump(rows, open(os.path.join(L4.HERE, "out", "p4_08_joint.json"), "w"), indent=0)
ok = lambda r: r["exact_slack"] is not None and r["exact_slack"] >= 0
th = lambda r: r["thirds_shares"] or (r["thirds_state_shares"] is not None and r["thirds_state_shares"] >= 0)
n = len(rows)
print(f"\n{n} instances.  certificate by additions exists (exactly verified):  joint LP {sum(ok(r) for r in rows)};  equal thirds + state-dependent shares {sum(th(r) for r in rows)};  "
      f"reference minimises: envelope {sum(r['margin_env3'] >= -1e-9 for r in rows)}, pair thirds {sum(r['margin_pair_thirds'] >= -1e-9 for r in rows)}")
print("joint certifies, thirds do not:", [f"{r['res']}{r['nres']}/{r['bb']}({r['tau'][1:]}): exact slack {r['exact_slack']:.4f}, grid margin {r['grid_margin']:.4f}" for r in rows if ok(r) and not th(r)])
print("thirds certify, joint does not (would be a bug):", [f"{r['res']}{r['nres']}/{r['bb']}({r['tau'][1:]})" for r in rows if th(r) and not ok(r)])
print("envelope certifies, joint does not:", [f"{r['res']}{r['nres']}/{r['bb']}({r['tau'][1:]}): LP t {r['lp_t']}" for r in rows if r["margin_env3"] >= -1e-9 and not ok(r)])
print(f"largest LP: {max(r['nvar'] for r in rows)} variables, {max(r['nrows'] for r in rows)} rows;  smallest E - m on the grids: {min(r['grid_sound'] for r in rows if r['grid_sound'] is not None):.2e}")
print(f"[{time.time() - t00:.0f}s] DONE p4_08_joint")
