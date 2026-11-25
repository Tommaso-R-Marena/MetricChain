"""
Main analysis of one enumerated fixed-backbone rotamer model (data/<tag>.npz from enum_fb.py).

usage: python3 -B an_main.py TAG TAU [--names GB,ff03-ff14SB,...] [--nothird] [--nofits] [--nocover] [--quiet]

Domains (NOTES.md, Step 2):  X = product of the states with one-site clash score > TAU;
X_tau = {x in X : every two-site clash score > TAU}.  Every number printed is an exact maximum,
mean or sum over one of these two finite sets.

For each residual g (GB = GBn2 polarisation energy; ff03-ff14SB etc.; coul+GB; and the known
part f itself as a check of pairwiseness):
  first order   c_i, RMS single-flip difference;
  second order  c_ij, half row sums, Dobrushin-type sums sum_j tanh(beta c_ij/4);
  third order   c_ijk (max over triples, sum over triples);
  fits          best one-site and two-site approximations (least squares; Chebyshev LP if small);
  second-order interface (theory report 11.7) on the product domain X: star at x0, measured
                remainder against the bound sum c_ij, row-sum condition, the exact criterion of
                Thm 11.17 evaluated by enumeration, accuracy eps* certified by one star,
                free-energy bracket ln Z(lower model) - ln Z(upper model);
  third-order interface (Thm 11.18, m = 3): the same with the Hamming-2 ball and c_ijk;
  first-order format (as P's an7): sharp sites, lambda*, accuracy certified by one evaluation,
                Jensen gap against sum ln cosh(beta c_i/2); covers are in an_cover.py.
Output: out/an_<tag>_tau<TAU>.json
"""
import sys, os, json, math, time, itertools
import numpy as np
from anlib import *

np.set_printoptions(precision=2, suppress=True, linewidth=250)


def fl(v):
    return [float(x) for x in np.asarray(v).ravel()]


def analyse(tag, tau, names=None, do_third=True, do_fits=True, quiet=False, third_names=None):
    t00 = time.time()
    d0 = load_fb(tag)
    d = restrict(d0, tau) if tau > d0["tau_enum"] + 1e-12 else dict(d0, tau=tau)
    shape = d["shape"]; n = len(shape)
    res = dict(tag=tag, tau=tau, seq=d["seq"], bb=d["bb"], grid=d["grid"], shape=list(shape), natoms=d["natoms"])
    say = (lambda *a: None) if quiet else (lambda *a: print(*a, flush=True))
    say(f"\n################ {tag}  tau = {tau}: {d['seq']} on {d['bb']}, grid {d['grid']}; states per site {list(shape)}")
    if min(shape) == 0:
        say("   EMPTY domain (a site has no state above the threshold)")
        res["empty"] = True
        return res
    size = int(np.prod(shape))
    R = residuals(d)
    X = np.ones(shape, dtype=bool)
    Xt = d["s2min"] > tau
    res.update(size=size, clashfree=int(Xt.sum()))
    say(f"   product domain X: {size} assignments; pair-clash-free X_tau: {int(Xt.sum())} ({100 * Xt.mean():.1f} %); kT = {KT300:.4f} kcal/mol")
    cb = d["CB"]
    dist = np.sqrt(((cb[:, None, :] - cb[None, :, :]) ** 2).sum(-1))
    res["cb_dist"] = dist.tolist()
    if names is None:
        names = ["GB", "coul+GB", "ff03-ff14SB", "ff15ipq-ff14SB", "ff99SB-ff14SB", "f"]
    names = [nm for nm in names if nm in R]
    if third_names is None:
        third_names = names
    f = R["f"]
    doms = [("X", X)] + ([("Xtau", Xt)] if not Xt.all() else [])
    for dname, mask in doms:
        if mask.sum() < 2:
            continue
        for name in names:
            g = R[name]
            key = f"{dname}|{name}"
            t0 = time.time()
            c, rms, cnt = first_order(g, mask)
            out = dict(c=fl(c), rms=fl(rms), range=float(g[mask].max() - g[mask].min()), std=float(g[mask].std()))
            say(f"--- [{dname}] {name}: range {out['range']:.2f}, std {out['std']:.2f} kcal/mol")
            say(f"    c_i   = {c}   max {c.max():.2f} kcal/mol = {c.max() * BETA:.1f} kT;  rms single flip = {rms}")
            if n >= 2:
                C, Rm = second_order(g, mask)
                half = 0.5 * C.sum(axis=1)
                dob = np.tanh(BETA * C / 4.0).sum(axis=1)
                bysep = {}
                for s in range(1, n):
                    v = [C[i, i + s] for i in range(n - s)]
                    bysep[s] = (float(np.max(v)), float(np.mean(v)))
                out.update(C=C.tolist(), Crms=Rm.tolist(), half_rowsum=fl(half), dobrushin=fl(dob),
                           bysep={str(s): v for s, v in bysep.items()})
                say(f"    c_ij  : max {C.max():.3f} kcal/mol = {C.max() * BETA:.2f} kT; max by separation 1..: "
                    + " ".join(f"{bysep[s][0]:.3f}" for s in range(1, n)))
                say(f"    half row sums (1/2) sum_j c_ij = {half};  Dobrushin-type sums = {dob} (max {dob.max():.2f})")
                if n <= 8 and name in ("GB", "ff03-ff14SB") and dname == "X":
                    say("    matrix c_ij:\n" + "\n".join("      " + str(row) for row in C))
            if n >= 3 and do_third and name in third_names:
                T = third_order(g, mask)
                mx = max(v[0] for v in T.values())
                sm = sum(v[0] for v in T.values())
                span = {}
                for (i, j, k), v in T.items():
                    span[k - i] = max(span.get(k - i, 0.0), v[0])
                out.update(c3max=mx, c3sum=sm, c3span={str(s): v for s, v in span.items()},
                           c3={f"{i},{j},{k}": v[0] for (i, j, k), v in T.items()} if n <= 8 else None)
                say(f"    c_ijk : max {mx:.3e} kcal/mol; sum over the {len(T)} triples {sm:.3e}; max by span k-i = 2..: "
                    + " ".join(f"{span[s]:.2e}" for s in sorted(span)))
            if do_fits and name != "f" and n >= 2:
                fit = low_order_fits(g, mask, lp_limit=7000)
                out["fit"] = fit
                say(f"    fits  : one-site LS rms {fit['ls1_rms']:.3f} max {fit['ls1_max']:.3f}"
                    + (f" sup-opt {fit['sup1']:.3f}" if "sup1" in fit else "")
                    + f" | two-site LS rms {fit['ls2_rms']:.4f} max {fit['ls2_max']:.4f}"
                    + (f" sup-opt {fit['sup2']:.4f}" if "sup2" in fit else "") + f"  [{fit['M']} points, {fit.get('npar2', 0)} parameters]")
            res[key] = out
            say(f"    ({time.time() - t0:.1f}s)")
    # ------------------------------------------------------------------ interfaces of the theory
    for name in names:
        if name == "f":
            continue
        g = R[name]
        E = f + g
        key = f"X|{name}"
        if key not in res or n < 2:
            continue
        c = np.array(res[key]["c"]); C = np.array(res[key]["C"])
        o = {}
        xf = tuple(int(v) for v in np.unravel_index(np.argmin(f), shape))
        xE = tuple(int(v) for v in np.unravel_index(np.argmin(E), shape))
        o.update(argmin_f=list(xf), argmin_E=list(xE), same_min=bool(xf == xE), regret=float(E[xf] - E[xE]))
        say(f"=== interfaces on the product domain X, residual {name}: argmin f = {xf}, argmin E = {xE} (same: {xf == xE}; "
            f"E(argmin f) - min E = {E[xf] - E[xE]:.3f} kcal/mol)")
        # ---- first-order format
        for cname, x0, h in (("argmin_f", xf, f), ("argmin_E", xE, E)):
            gaps = []
            for i in range(n):
                idx = list(x0); idx[i] = slice(None)
                line = h[tuple(idx)] - h[x0]
                line = np.delete(line, x0[i])
                gaps.append(float(line.min()) if line.size else float("inf"))
            gaps = np.array(gaps)
            o[f"gaps_{cname}"] = fl(gaps)
            o[f"sharp_{cname}"] = int((gaps >= c).sum())
            say(f"    first order, centre {cname}: single-site excitation energies (of {'f' if cname == 'argmin_f' else 'E'}) = {gaps}; "
                f"sharp sites (gap >= c_i): {int((gaps >= c).sum())} of {n}; ratios gap/c = {gaps / np.where(c > 0, c, np.nan)}")
        D = weighted_hamming(shape, xf, c)
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = np.where(D > 0, (f - f[xf]) / D, np.inf)
        lam = float(ratio.min())
        eps1 = float(np.max(D - (f - f[xf])))            # accuracy certified by the single evaluation at argmin f (Thm 11.7 with eps)
        o.update(lambda_star=lam, eps_one_eval=max(eps1, 0.0))
        lnc = lncosh_sum(c)
        pif = gibbs(f, X)
        jensen = lnZ(E, X) - lnZ(f, X) + BETA * float((pif * g).sum())
        o.update(lncosh=lnc, jensen=jensen, dlnZ=lnZ(E, X) - lnZ(f, X))
        say(f"    first order: lambda* = {lam:.4f} (one evaluation certifies the minimum iff >= 1); one evaluation at argmin f certifies to within "
            f"eps = {max(eps1, 0):.2f} kcal/mol;  sum ln cosh(beta c_i/2) = {lnc:.2f} nats, exact Jensen gap = {jensen:.3f} nats")
        # ---- second-order format: star
        for cname, x0 in (("argmin_E", xE), ("argmin_f", xf)):
            gs = star_part(g, x0)
            W = pair_weight(shape, x0, C)
            rem = g - gs
            L = f + gs - W
            U = f + gs + W
            nstar = 1 + sum(k - 1 for k in shape)
            # best evaluated energy on the star
            Estar = [E[x0]]
            for i in range(n):
                idx = list(x0); idx[i] = slice(None)
                Estar.append(float(E[tuple(idx)].min()))
            best_eval = min(Estar)
            eps2 = best_eval - float(L.min())
            # row-sum condition (generalised to a pairwise known part): for every changed set S,
            # sum_{i in S} Delta_i + sum_{i<j in S} (M^f_ij - c_ij) >= 0; sufficient: Delta_i(a) >= (1/2) sum_j max_b (c_ij - M^f_ij(a,b))_+
            Delta = []
            for i in range(n):
                idx = list(x0); idx[i] = slice(None)
                Delta.append(E[tuple(idx)] - E[x0])
            half = 0.5 * C.sum(axis=1)
            minDelta = np.array([np.delete(Delta[i], x0[i]).min() if shape[i] > 1 else np.inf for i in range(n)])
            row_ok_plain = bool((minDelta >= half).all())
            need = np.zeros(n)
            worst_margin = np.inf
            for i in range(n):
                acc = np.zeros(shape[i])
                for j in range(n):
                    if j == i:
                        continue
                    idx = list(x0); idx[i] = slice(None); idx[j] = slice(None)
                    plane = f[tuple(idx)]
                    if j < i:
                        plane = plane.T
                    ii = list(x0); ii[i] = slice(None)
                    jj = list(x0); jj[j] = slice(None)
                    Mf = plane - f[tuple(ii)][:, None] - f[tuple(jj)][None, :] + f[x0]          # (k_i, k_j) mixed difference of f at x0
                    t = np.clip(C[i, j] - Mf, 0.0, None)
                    t[:, x0[j]] = 0.0
                    acc += 0.5 * t.max(axis=1)
                marg = np.delete(Delta[i] - acc, x0[i])
                if marg.size:
                    worst_margin = min(worst_margin, float(marg.min()))
            o[f"star_{cname}"] = dict(nstar=nstar, rem_max=float(np.abs(rem).max()), rem_rms=float(np.sqrt((rem ** 2).mean())),
                                      bound_max=float(W.max()), eps_star=max(eps2, 0.0), certifies_exactly=bool(eps2 <= 1e-9 and x0 == xE),
                                      rowsum_plain_ok=row_ok_plain, half_rowsum=fl(half), min_excitation=fl(minDelta),
                                      rowsum_pairwise_margin=worst_margin,
                                      lnZ_lower=lnZ(L, X), lnZ_upper=lnZ(U, X), lnZ_true=lnZ(E, X),
                                      bracket=lnZ(L, X) - lnZ(U, X))
            s_ = o[f"star_{cname}"]
            say(f"    second order, star at {cname} ({nstar} evaluations): measured |g - g_star| max {s_['rem_max']:.3f} rms {s_['rem_rms']:.3f} "
                f"(bound sum c_ij: max {s_['bound_max']:.3f});")
            say(f"        single-site excitation energies of E at the centre (min over states) = {minDelta};  half row sums = {half};  "
                f"row-sum condition (theory report 11.7) holds: {row_ok_plain}; pairwise-known-part version: margin {worst_margin:.3f} kcal/mol")
            say(f"        exact criterion of Thm 11.17 (enumeration of the lower pairwise model): the star certifies min E to within eps* = {max(eps2, 0):.4f} kcal/mol "
                f"= {max(eps2, 0) * BETA:.3f} kT  -> {'EXACT CERTIFICATE' if s_['certifies_exactly'] else 'no exact certificate'};")
            say(f"        free energy: ln Z in [{s_['lnZ_upper']:.3f}, {s_['lnZ_lower']:.3f}], true {s_['lnZ_true']:.3f}; bracket width {s_['bracket']:.3f} nats "
                f"= {s_['bracket'] * KT300:.3f} kcal/mol")
        # ---- third-order format: Hamming-2 ball (Thm 11.18 with m = 3)
        if n >= 3 and res[key].get("c3") is not None:
            T3 = res[key]["c3"]
            x0 = xE
            a2 = anchored2(g, x0)
            ch = changed(shape, x0)
            W3 = np.zeros(shape)
            for kk, v in T3.items():
                i, j, k = (int(t) for t in kk.split(","))
                W3 = W3 + v * ch[i] * ch[j] * ch[k]
            L3 = f + a2 - W3
            nball = 1 + sum(k - 1 for k in shape) + sum((shape[i] - 1) * (shape[j] - 1) for i in range(n) for j in range(i + 1, n))
            Hm = hamming(shape, x0)
            best_eval = float(E[Hm <= 2].min())
            eps3 = best_eval - float(L3.min())
            o["ball2"] = dict(nball=nball, rem_max=float(np.abs(g - a2).max()), rem_rms=float(np.sqrt(((g - a2) ** 2).mean())),
                              bound_max=float(W3.max()), eps=max(eps3, 0.0),
                              bracket=lnZ(L3, X) - lnZ(f + a2 + W3, X))
            say(f"    third order, Hamming-2 ball at argmin_E ({nball} evaluations): measured |g - I_2 g| max {o['ball2']['rem_max']:.4f} rms {o['ball2']['rem_rms']:.4f} "
                f"(bound sum c_ijk: max {o['ball2']['bound_max']:.4f}); certifies min E to within {max(eps3, 0):.4f} kcal/mol; "
                f"free-energy bracket {o['ball2']['bracket']:.4f} nats")
        res[f"iface|{name}"] = o
    res["seconds"] = time.time() - t00
    return res


if __name__ == "__main__":
    a = sys.argv[1:]
    tag, tau = a[0], float(a[1])
    names = a[a.index("--names") + 1].split(",") if "--names" in a else None
    tnames = a[a.index("--thirdnames") + 1].split(",") if "--thirdnames" in a else None
    r = analyse(tag, tau, names=names, do_third="--nothird" not in a, do_fits="--nofits" not in a, quiet="--quiet" in a, third_names=tnames)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    json.dump(r, open(os.path.join(HERE, "out", f"an_{tag}_tau{tau:.2f}.json"), "w"), indent=0)
    print(f"   [{r.get('seconds', 0):.0f}s] -> out/an_{tag}_tau{tau:.2f}.json")
