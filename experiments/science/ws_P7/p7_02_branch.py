"""
P7 item 2: are the gap analyses certified by shares after branching on one site (then two)?

For each gap analysis of out/p7_01_five.json (model L of P4 on X', reference x0, F = L - L(x0)):

  depth 1   for every site i with more than one state: one leaf per state a of i (the box with x_i = a).
            Leaf that contains x0 (a = x0_i): state-dependent shares with slack (kind R).
            Other leaves: a dual solution of the pairwise relaxation of the leaf whose value is >= 0,
            i.e. >= the FIXED NUMBER L(x0) (kind N).  Every certificate is converted to integers and
            accepted only by the exact integer checker p7lib.leaf_bound (the theory kernel's LeafOK).
  split     the two-block variant: the leaf x_i = x0_i and ONE leaf for all other states of i.
  one state for every site i and every state a != x0_i: the split  x_i = a | x_i != a  (two leaves: the box
            with x_i = a, and the box with the state a of site i removed, which contains x0).
  blocks    for every site that works: a greedy merge of its states into blocks, each block certified by
            ONE set of messages (a certificate for a box is a certificate for every sub-box, so in the
            theory kernel the children of the states of a block may share one leaf): an upper bound on
            the number of DISTINCT leaf certificates that the branching needs.
  depth 2   if no site works: the smallest trees of depth two (a leaf that fails is split on a second site).
  cores     the minimal sets U of sites such that the model restricted to U (all other sites at the
            reference) has no shares: the reference leaf of a branching on i is certified iff i lies in
            every core.

BRUTE FORCE (every leaf, certified or not): the exact minimum over the leaf of the published integer
instance (int64 enumeration) and the minimum over the leaf of P4's float model grid.  Counted:
  bf_checks      leaf certificates compared with the exact leaf minimum  (certified bound <= minimum);
  bf_violations  certificates whose bound exceeds the exact minimum      (must be 0);
  truth          leaves in which the exact minimum is < 0                (must be 0: x0 minimises the model);
  maxdev         largest |published - P4 grid| over the leaf minima      (rounding 2^-40 per table entry).

The smallest tree found for each analysis is written with its integer certificates to
out/p7_02_cert_<label>.json (one leaf per state), and the variant with shared block leaves to
out/p7_02_certB_<label>.json where it has fewer distinct leaves (both read by p7_06_check.py, p7_07_lean.py).

usage: python3 -B p7_02_branch.py > logs/p7_02_branch.log   (writes out/p7_02_branch.json; last line "DONE p7_02_branch")
"""
import sys, os, json, time, itertools
sys.dont_write_bytecode = True
import numpy as np
import p7lib as L7
from p7lib import PM, IPM, L4

t00 = time.time()
print(f"p7_02_branch  started {L7.now()}")
five = json.load(open(os.path.join(L7.HERE, "out", "p7_01_five.json")))["gaps"]
TOT = dict(leaves=0, certified=0, bf_checks=0, bf_violations=0, truth=0, certR=0, certN=0, N_sharp=0)
results = []


def label(g):
    return f"{g['family']}{g['nres']}_{g['bb']}_tau{g['tau']}_{g['split'].split('-')[0]}"


for g in five:
    t0 = time.time()
    tag, tau, name = g["tag"], float(g["tau"]), g["split"]
    inst = L4.load_instance(tag, tau)
    Lmod, x0, E, C = L7.second_order_grid(inst, name)
    GP4 = Lmod - Lmod[x0]                                  # P4's model on the grid (float)
    pm = PM.from_grid(Lmod, x0); ipm = IPM(pm); IG = ipm.grid()
    n = pm.n
    Dfull = pm.full_domain()
    st = dict(leaves=0, certified=0, bf_checks=0, bf_violations=0, truth=0, maxdev=0.0, certR=0, certN=0, N_sharp=0)
    cache = {}

    def leaf(D):
        key = tuple(tuple(int(v) for v in d) for d in D)
        if key in cache:
            return cache[key]
        c = L7.certify_leaf(pm, ipm, D)
        bI = int(L7.box_min(IG, D)); bG = float(L7.box_min(GP4, D))
        st["leaves"] += 1
        st["maxdev"] = max(st["maxdev"], abs(bI * L7.UNIT - bG))
        if bI < 0:
            st["truth"] += 1
        if c["ok"]:
            st["certified"] += 1; st["bf_checks"] += 1
            if c["LB"] > bI:
                st["bf_violations"] += 1
            if c["kind"] == "R":                           # the leaf with the reference: the minimum is attained at x0 and equals the bound
                assert c["LB"] == 0 and bI == 0
                st["certR"] += 1                           # (here the comparison tests the statement, the minimum 0 being known)
            else:
                st["certN"] += 1
                if bI - c["LB"] <= 1024:                   # the certified bound is the exact leaf minimum up to 2^-30: a sharp test
                    st["N_sharp"] += 1
        c = dict(c, bfI=bI, bfG=bG, nstates=L7.n_states(D))
        cache[key] = c
        return c

    print(f"\n=== {g['family']}{g['nres']}/{g['bb']} tau {g['tau']} split {name}: X' = {list(pm.shape)}, x0 = {list(x0)}, margin {g['margin']:.6f}, gap {-g['relaxation']:.6f}")
    root = leaf(Dfull)
    assert not root["ok"], "the root should not be certified"
    # ---------------------------------------------------------------- depth 1
    sites = {}
    print(f"  {'site':>4s} {'states':>6s} | {'ref. leaf: t':>12s} {'ok':>3s} | {'other leaves':>12s} {'failing':>7s} {'least LP value':>14s} {'least true min':>14s} {'least exact bound':>17s} | {'ALL':>4s} | two-block split: other block LP value, ok")
    for i in pm.active():
        L = []
        for a in pm.dom[i]:
            c = leaf(L7.fix(Dfull, i, a))
            L.append(dict(state=int(a), kind=c["kind"], lp=c["lp"], ok=c["ok"], LB=c["LB"], bfI=c["bfI"], bfG=c["bfG"]))
        ref = [x for x in L if x["kind"] == "R"][0]
        non = [x for x in L if x["kind"] == "N"]
        allok = all(x["ok"] for x in L)
        # two-block split: {x0_i} and all other states of i in ONE leaf
        Dn = [d.copy() for d in Dfull]; Dn[i] = np.array([a for a in pm.dom[i] if a != x0[i]])
        cb = leaf(Dn)
        sites[i] = dict(states=len(L), leaves=L, works=allok, ref_t=ref["lp"], ref_ok=ref["ok"], nonref_fail=sum(1 for x in non if not x["ok"]),
                        nonref_min_lp=min(x["lp"] for x in non), nonref_min_true=min(x["bfI"] for x in non) * L7.UNIT,
                        nonref_min_bound=(min(x["LB"] for x in non if x["ok"]) * L7.UNIT if any(x["ok"] for x in non) else None),
                        block_lp=cb["lp"], block_ok=bool(cb["ok"] and ref["ok"]), block_true=cb["bfI"] * L7.UNIT)
        s_ = sites[i]
        print(f"  {i:4d} {len(L):6d} | {ref['lp']:12.6f} {'yes' if ref['ok'] else 'NO':>3s} | {len(non):12d} {s_['nonref_fail']:7d} {s_['nonref_min_lp']:14.6f} {s_['nonref_min_true']:14.6f} "
              f"{(s_['nonref_min_bound'] if s_['nonref_min_bound'] is not None else float('nan')):17.9f} | {'YES' if allok else 'no':>4s} | {cb['lp']:.6f}, {'yes' if s_['block_ok'] else 'no'}")
    working = [i for i in sites if sites[i]["works"]]
    blockers = [i for i in sites if sites[i]["block_ok"]]
    print(f"  sites whose branching certifies every leaf: {working}  -> least number of leaves {min((sites[i]['states'] for i in working), default=None)}")
    print(f"  sites for which the two-block split (x_i = x0_i | x_i != x0_i) certifies: {blockers}")

    def greedy_blocks(i):
        """merge the states of site i into blocks, each certified by one leaf (first fit; states in the
        order of decreasing exact bound of their own leaf; the first block starts with the reference state)."""
        order = sorted([x for x in sites[i]["leaves"] if x["kind"] == "N"], key=lambda x: -x["LB"])
        blocks = [[int(x0[i])]]
        for x in order:
            a = x["state"]
            for B in blocks:
                D = [d.copy() for d in Dfull]; D[i] = np.array(sorted(B + [a]))
                if leaf(D)["ok"]:
                    B.append(a)
                    break
            else:
                blocks.append([a])
        return [sorted(B) for B in blocks]
    blocks = {i: greedy_blocks(i) for i in working}
    # single-state splits  x_i = a | x_i != a
    single = []
    for i in pm.active():
        for x in sites[i]["leaves"]:
            if x["kind"] != "N" or not x["ok"]:
                continue
            a = x["state"]
            D = [d.copy() for d in Dfull]; D[i] = np.array([b for b in pm.dom[i] if b != a])
            c = leaf(D)
            if c["ok"]:
                single.append(dict(site=int(i), state=int(a), t_rest=c["lp"], bound_state=x["LB"] * L7.UNIT))
    by_site = {}
    for x in single:
        by_site.setdefault(x["site"], []).append(x["state"])
    print(f"  single-state splits (x_i = a | x_i != a) that certify with TWO leaves: {len(single)}: " + ("; ".join(f"site {i}: states {v}" for i, v in sorted(by_site.items())) if single else "none"))
    for i in working:
        print(f"  site {i}: greedy blocks of states sharing one leaf certificate: {len(blocks[i])} blocks (of {sites[i]['states']} states): {blocks[i]}")

    # ---------------------------------------------------------------- smallest tree of depth <= 2
    def best_tree(D, depth):
        """smallest (by leaves) tree of depth <= depth all of whose leaves are certified; None if none."""
        c = leaf(D)
        if c["ok"]:
            return dict(nleaves=1, depth=0, D=D)
        if depth == 0:
            return None
        best = None
        for i in range(n):
            if len(D[i]) < 2:
                continue
            subs = []
            for a in D[i]:
                sub = best_tree(L7.fix(D, i, a), depth - 1)
                if sub is None:
                    subs = None
                    break
                subs.append((int(a), sub))
            if subs is None:
                continue
            tot = sum(s["nleaves"] for _, s in subs)
            if best is None or tot < best["nleaves"]:
                best = dict(nleaves=tot, depth=1 + max(s["depth"] for _, s in subs), site=i, children=subs)
        return best

    depth2 = None
    if working:
        # depth one suffices: choose the working site with the fewest states (ties: the largest least slack)
        def least_slack(i):
            return min([sites[i]["ref_t"]] + [x["LB"] * L7.UNIT for x in sites[i]["leaves"] if x["kind"] == "N"])
        isel = sorted(working, key=lambda i: (sites[i]["states"], -least_slack(i)))[0]
        tree = dict(nleaves=sites[isel]["states"], depth=1, site=isel,
                    children=[(int(a), dict(nleaves=1, depth=0, D=L7.fix(Dfull, isel, a))) for a in pm.dom[isel]])
    else:
        tree = best_tree(Dfull, 2)
        assert tree is not None, "no tree of depth two"
        # all pairs of sites (complete trees of depth two, k_i * k_j leaves) and all 3-leaf trees, for the record
        pairs_ok = []
        for i, j in itertools.combinations(pm.active(), 2):
            if all(leaf(L7.fix(L7.fix(Dfull, i, a), j, b))["ok"] for a in pm.dom[i] for b in pm.dom[j]):
                pairs_ok.append((i, j))
        small = []
        for i in pm.active():
            L1 = {int(a): leaf(L7.fix(Dfull, i, a)) for a in pm.dom[i]}
            bad = [a for a in L1 if not L1[a]["ok"]]
            if len(bad) != 1:
                continue
            a = bad[0]
            for j in pm.active():
                if j != i and all(leaf(L7.fix(L7.fix(Dfull, i, a), j, b))["ok"] for b in pm.dom[j]):
                    small.append((i, a, j))
        depth2 = dict(pairs_ok=pairs_ok, npairs=len(list(itertools.combinations(pm.active(), 2))), adaptive=small)
        print(f"  NO single site certifies.  Depth two: {len(pairs_ok)} of {depth2['npairs']} pairs of sites certify all their leaves: {pairs_ok}")
        print(f"  adaptive trees (branch on i; the one failing leaf x_i = a is split on j), as (i, a, j): {len(small)}: {small}")

    def show(tr, indent="    "):
        if "site" not in tr:
            c = leaf(tr["D"])
            fx = {i: int(tr["D"][i][0]) for i in range(n) if len(tr["D"][i]) == 1 and len(Dfull[i]) > 1}
            return [f"{indent}leaf {fx}: kind {c['kind']}, LP {c['lp']:.6f}, exact bound {c['LB'] * L7.UNIT:.9f}, exact leaf minimum {c['bfI'] * L7.UNIT:.9f} ({c['nstates']} states)"]
        out = [f"{indent}branch on site {tr['site']}:"]
        for a, sub in tr["children"]:
            out += show(sub, indent + "  ")
        return out
    print(f"  SMALLEST TREE FOUND: depth {tree['depth']}, {tree['nleaves']} leaves")
    lines = show(tree)
    for ln in (lines if len(lines) <= 14 else lines[:6] + [f"      ... ({len(lines) - 12} more lines) ..."] + lines[-6:]):
        print(ln)

    # ---------------------------------------------------------------- cores
    act = pm.active()
    cores = None
    if len(act) <= 8:
        tight = {}
        for m_ in range(1, len(act) + 1):
            for U in itertools.combinations(act, m_):
                if m_ <= 2:
                    tight[U] = True                       # one or two sites: the relaxation is exact (a tree)
                    continue
                D = [Dfull[i] if i in U else np.array([x0[i]]) for i in range(n)]
                tight[U] = bool(leaf(D)["ok"])
        cores = [list(U) for U in tight if not tight[U] and all(tight[V] for V in itertools.combinations(U, len(U) - 1))]
        method = "share LP on every subset of sites (exact integer acceptance)"
    elif all(pm.shape[i] == 2 for i in act):
        # binary sites: shares exist on U iff no subset S of U is over-dense, sum_{i<j in S} [-M_ij]_+ > sum_{i in S} A_i
        m_ = len(act)
        Ach = np.array([ipm.H[i][1 - x0[i]] for i in act], dtype=np.int64)
        bits = ((np.arange(1 << m_)[:, None] >> np.arange(m_)[None, :]) & 1).astype(np.int64)
        exc = -(bits @ Ach)
        for a_ in range(m_):
            for b_ in range(a_ + 1, m_):
                w = max(-int(ipm.pair(act[a_], act[b_])[1 - x0[act[a_]], 1 - x0[act[b_]]]), 0)
                if w:
                    exc = exc + w * bits[:, a_] * bits[:, b_]
        od = exc > 0                                        # exact integers (published instance)
        od[0] = False
        has = od.copy()
        for S in range(1, 1 << m_):                         # has[S]: S contains an over-dense subset
            if not has[S]:
                for b_ in range(m_):
                    if (S >> b_) & 1 and has[S & ~(1 << b_)]:
                        has[S] = True
                        break
        cores = []
        for S in np.flatnonzero(od):
            if not any(has[S & ~(1 << b_)] for b_ in range(m_) if (S >> b_) & 1):
                cores.append([act[b_] for b_ in range(m_) if (S >> b_) & 1])
        # cross-check with the LP on the sets V \ {i}
        for i in act:
            S = sum(1 << b_ for b_ in range(m_) if act[b_] != i)
            assert bool(has[S]) == (not sites[i]["ref_ok"]), "over-dense enumeration disagrees with the share LP"
        method = "exact enumeration of over-dense sets of the published instance (binary sites), cross-checked with the share LP on V minus one site"
    if cores is not None:
        inall = [i for i in act if all(i in U for U in cores)]
        hit = None
        for m_ in range(1, len(act) + 1):
            hs = [list(H) for H in itertools.combinations(act, m_) if all(any(i in U for i in H) for U in cores)]
            if hs:
                hit = dict(size=m_, sets=hs[:40], count=len(hs))
                break
        print(f"  CORES (minimal sets of sites without shares; {method}): {len(cores)}: {cores if len(cores) <= 12 else str(cores[:12]) + ' ...'}")
        print(f"  sites in every core (= sites whose reference leaf is certified): {inall};  smallest hitting sets have {hit['size']} site(s): {hit['count']} of them")
        assert sorted(inall) == sorted(i for i in sites if sites[i]["ref_ok"])

    # ---------------------------------------------------------------- write the certificate of the smallest tree
    def export_tree(tr, leaves):
        if "site" not in tr:
            D = tr["D"]
            c = leaf(D)
            LB, U, P = L7.leaf_bound(ipm, D, c["m"])
            assert LB == c["LB"] and LB >= 0
            leaves.append(dict(kind=c["kind"], box=[[int(v) for v in d] for d in D], U=[int(u) for u in U],
                               P2={f"{i},{j}": int(v) for (i, j), v in P.items()},
                               m={f"{i},{j}": [int(v) for v in arr] for (i, j), arr in c["m"].items()}, LB=int(LB),
                               bf_min=int(c["bfI"]), nstates=int(c["nstates"])))
            return dict(leaf=len(leaves) - 1)
        return dict(site=int(tr["site"]), children={str(a): export_tree(sub, leaves) for a, sub in tr["children"]})

    def write_cert(fname, tree_json, leaves, nchildren, depth, variant):
        cert = dict(label=label(g), variant=variant, instance=f"{g['family']}{g['nres']}/{g['bb']}", tag=tag, tau=g["tau"], split=name, order=2,
                    unit_log2=-L7.SCALE, shape=list(pm.shape), ref=list(x0), L=0,
                    H=[[int(v) for v in h] for h in ipm.H], J={f"{i},{j}": [[int(v) for v in row] for row in T] for (i, j), T in ipm.J.items()},
                    tree=tree_json, leaves=leaves, n_leaf_certificates=len(leaves), n_leaf_boxes=nchildren, depth=depth,
                    note="published instance: P4's second-order lower model in difference form at the reference, every table entry rounded DOWN to a multiple of 2^-40 kcal/mol "
                         "(energy = sum_i H_i(x_i) + sum_{i<j} J_ij(x_i, x_j); value 0 at the reference).  leaf: U_i <= H_i(a) + sum_j m_ij(a), "
                         "P2_ij <= J_ij(a,b) - m_ij(a) - m_ji(b) for all states of the leaf box, 0 <= sum U + sum P2 "
                         "(theory kernel: u = U, p_ij = p_ji = P2_ij/2, L = 0).  A leaf shared by several children was certified on the union of their boxes.")
        json.dump(cert, open(os.path.join(L7.HERE, "out", fname), "w"))
        print(f"  certificate written: out/{fname}  ({len(leaves)} leaf certificates for {nchildren} leaf boxes)")

    leaves = []
    tj = export_tree(tree, leaves)
    write_cert(f"p7_02_cert_{label(g)}.json", tj, leaves, tree["nleaves"], tree["depth"], "one leaf per state")
    nblocks = None
    if working:
        ib = sorted(working, key=lambda i: (len(blocks[i]), sites[i]["states"]))[0]
        if single and len(blocks[ib]) > 2:                 # a two-leaf split exists that the greedy merge did not find
            best = max(single, key=lambda x: min(x["t_rest"], x["bound_state"]))
            ib = best["site"]
            blocks[ib] = [sorted(b for b in pm.dom[ib] if b != best["state"]), [best["state"]]]
            blocks[ib] = [[int(v) for v in B] for B in blocks[ib]]
        nblocks = len(blocks[ib])
        if nblocks < sites[ib]["states"]:
            leavesB = []
            children = {}
            for B in blocks[ib]:
                D = [d.copy() for d in Dfull]; D[ib] = np.array(B)
                c = leaf(D)
                LB, U, P = L7.leaf_bound(ipm, D, c["m"])
                assert LB == c["LB"] and LB >= 0
                leavesB.append(dict(kind=c["kind"], box=[[int(v) for v in d] for d in D], U=[int(u) for u in U],
                                    P2={f"{i},{j}": int(v) for (i, j), v in P.items()},
                                    m={f"{i},{j}": [int(v) for v in arr] for (i, j), arr in c["m"].items()}, LB=int(LB),
                                    bf_min=int(c["bfI"]), nstates=int(c["nstates"])))
                for a in B:
                    children[str(a)] = dict(leaf=len(leavesB) - 1)
            write_cert(f"p7_02_certB_{label(g)}.json", dict(site=int(ib), children=children), leavesB, sites[ib]["states"], 1, "greedy blocks, shared leaves")
    print(f"  of the certified leaves {st['certR']} contain x0 (bound 0 = minimum) and {st['certN']} do not; of the latter {st['N_sharp']} have a certified bound within 2^-30 of the exact leaf minimum")
    print(f"  brute force: {st['leaves']} leaves enumerated ({sum(c['nstates'] for c in cache.values())} states in all), {st['certified']} certified, "
          f"{st['bf_checks']} certificates compared with the exact leaf minimum, violations {st['bf_violations']}; leaves with a negative exact minimum {st['truth']}; "
          f"largest |published - P4 grid| over leaf minima {st['maxdev']:.1e}   ({time.time() - t0:.1f}s)")
    for k in TOT:
        TOT[k] += st[k]
    results.append(dict(label=label(g), instance=f"{g['family']}{g['nres']}/{g['bb']}", tau=g["tau"], split=name, shape=list(pm.shape), x0=list(x0),
                        margin=g["margin"], gap=-g["relaxation"],
                        sites={str(i): {k: v for k, v in s.items() if k != "leaves"} for i, s in sites.items()},
                        site_leaves={str(i): s["leaves"] for i, s in sites.items()},
                        working=working, block_working=blockers, single_state_splits=single, blocks={str(i): b for i, b in blocks.items()}, tree_depth=tree["depth"], tree_leaves=tree["nleaves"],
                        tree_site=tree.get("site"), depth2=depth2, cores=cores, stats=st))

json.dump(results, open(os.path.join(L7.HERE, "out", "p7_02_branch.json"), "w"), indent=1, default=lambda o: int(o) if isinstance(o, np.integer) else float(o))
print("\nSUMMARY")
print(f"{'instance':10s} {'tau':4s} {'split':15s} {'sites':>5s} | {'sites that certify (one branching)':36s} {'least leaves':>12s} | {'two-block split works at':26s} | {'least leaf certificates':>23s} | {'smallest tree':>20s}")
for r in results:
    w = r["working"]
    print(f"{r['instance']:10s} {r['tau']:4s} {r['split']:15s} {len(r['sites']):5d} | {str(w) if w else 'NONE':36s} {str(min((r['sites'][str(i)]['states'] for i in w), default='-')):>12s} | "
          f"{str(r['block_working']) if r['block_working'] else 'none':26s} | {('2 (split off one state)' if r['single_state_splits'] else str(min((len(b) for b in r['blocks'].values()), default='-'))):>23s} | depth {r['tree_depth']}, {r['tree_leaves']} leaves")
print(f"\nBRUTE FORCE TOTAL: {TOT['leaves']} leaves enumerated; {TOT['certified']} leaf certificates accepted by the integer checker; "
      f"{TOT['bf_checks']} compared with the exact leaf minimum; violations {TOT['bf_violations']}; leaves with a negative exact minimum {TOT['truth']}")
print(f"of the {TOT['certified']} certified leaf boxes {TOT['certR']} contain the reference (certified bound 0 = the minimum, attained at x0) and {TOT['certN']} do not; "
      f"in {TOT['N_sharp']} of these {TOT['certN']} the certified bound equals the exact leaf minimum up to 2^-30 kcal/mol (a sharp test of the checker), in the others it is strictly below")
print(f"[{time.time() - t00:.0f}s] wrote out/p7_02_branch.json   finished {L7.now()}")
print("DONE p7_02_branch")
