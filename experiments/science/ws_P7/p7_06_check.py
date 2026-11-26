"""
P7 item 5: a reference checker for the certificate "shares at the leaves of a branching tree".

Independent of p7lib: reads a certificate file out/p7_02_cert*.json and uses Python integers only.
The file holds (all numbers are integers in units of 2^unit_log2 kcal/mol):
  shape, ref          states per site, reference configuration
  H[i][a], J["i,j"][a][b] (i < j)   the published instance (energy = sum_i H_i(x_i) + sum_{i<j} J_ij(x_i, x_j))
  L                   the bound to certify (0 = the value of the instance at the reference)
  tree                {"site": i, "children": {state: subtree}}  or  {"leaf": index}
  leaves[l]           U[i], P2["i,j"] (i < j), m["i,j"][a] (ordered pairs i != j)

The checker is the theory division's `verify` restricted to `branch` and `leaf`
(proofs/CertificateAlgebra.lean: `(D i).all fun a => verify (ch a) I (D.fix i a) L` and `LeafOK`):
  branch i:  every state a of the current domain of i must have a child; recurse with D_i := {a};
  leaf:      for every site i and a in D_i:               U_i  <= H_i(a) + sum_{j != i} m_ij(a)
             for every pair i < j, a in D_i, b in D_j:    P2_ij <= J_ij(a, b) - m_ij(a) - m_ji(b)
             and                                          L <= sum_i U_i + sum_{i<j} P2_ij .
Only additions and comparisons of integers; they are counted.  Controls, which must be REJECTED:
  (c1) the same certificate for the bound L + 1 (one unit above the minimum);
  (c2) the first leaf of the certificate used alone on the whole domain (no branching);
  (c3) the certificate with the children of two states of the branching site exchanged.
Brute force (numpy, int64, from the tables of the file): the exact minimum of the published instance over
every leaf box against the bound the leaf certifies, and over the whole domain (must be exactly L at ref).

usage: python3 -B p7_06_check.py > logs/p7_06_check.log   (all out/p7_02_cert*.json; writes out/p7_06_check.json; last line "DONE p7_06_check")
"""
import sys, os, json, glob, time, copy
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
t00 = time.time()
print(f"p7_06_check  started {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")


class Checker:
    def __init__(self, cert):
        self.c = cert
        self.n = len(cert["shape"])
        self.H = cert["H"]
        self.J = {tuple(int(v) for v in k.split(",")): T for k, T in cert["J"].items()}
        self.adds = 0; self.cmps = 0; self.leaf_visits = 0

    def leaf_ok(self, leaf, dom, L):
        n = self.n
        m = {tuple(int(v) for v in k.split(",")): arr for k, arr in leaf["m"].items()}
        P2 = {tuple(int(v) for v in k.split(",")): v2 for k, v2 in leaf["P2"].items()}
        U = leaf["U"]
        self.leaf_visits += 1
        for i in range(n):
            for a in dom[i]:
                v = self.H[i][a]
                for j in range(n):
                    if j != i:
                        v += m[(i, j)][a]; self.adds += 1
                self.cmps += 1
                if not U[i] <= v:
                    return False
        for i in range(n):
            for j in range(i + 1, n):
                T = self.J[(i, j)]; mi = m[(i, j)]; mj = m[(j, i)]; p = P2[(i, j)]
                for a in dom[i]:
                    Ta = T[a]; ma = mi[a]
                    for b in dom[j]:
                        self.adds += 2; self.cmps += 1
                        if not p <= Ta[b] - ma - mj[b]:
                            return False
        tot = sum(U) + sum(P2.values())
        self.adds += n + len(P2) - 1; self.cmps += 1
        return L <= tot

    def verify(self, node, dom, L):
        if "leaf" in node:
            return self.leaf_ok(self.c["leaves"][node["leaf"]], dom, L)
        i = node["site"]
        for a in dom[i]:
            child = node["children"].get(str(a))
            if child is None:
                return False
            d2 = list(dom); d2[i] = [a]
            if not self.verify(child, d2, L):
                return False
        return True


def leaf_boxes(node, dom, out):
    if "leaf" in node:
        out.append((node["leaf"], [list(d) for d in dom]))
        return
    i = node["site"]
    for a in dom[i]:
        d2 = list(dom); d2[i] = [a]
        leaf_boxes(node["children"][str(a)], d2, out)


rows = []
for path in sorted(glob.glob(os.path.join(HERE, "out", "p7_02_cert*.json"))):
    cert = json.load(open(path))
    n = len(cert["shape"]); shape = cert["shape"]
    dom = [list(range(k)) for k in shape]
    t0 = time.time()
    ck = Checker(cert)
    ok = ck.verify(cert["tree"], dom, cert["L"])
    adds, cmps, visits = ck.adds, ck.cmps, ck.leaf_visits
    # cost if every DISTINCT leaf certificate were checked once on the box it was produced for (a "split the domain of a
    # site into blocks" rule instead of one child per state); for trees with one leaf per state this is the same cost
    ck2 = Checker(cert)
    ok_split = all(ck2.leaf_ok(l, l["box"], cert["L"]) for l in cert["leaves"])
    covered_split = sum(int(np.prod([len(d) for d in l["box"]])) for l in cert["leaves"])
    # size of the certificate: integers stored
    nint = sum(len(l["U"]) + len(l["P2"]) + sum(len(v) for v in l["m"].values()) for l in cert["leaves"])
    ninst = sum(len(h) for h in cert["H"]) + sum(len(T) * len(T[0]) for T in cert["J"].values())
    # controls
    c1 = Checker(cert).verify(cert["tree"], dom, cert["L"] + 1)
    c2 = Checker(cert).verify(dict(leaf=0), dom, cert["L"])
    c3 = None
    if "site" in cert["tree"]:
        t2 = copy.deepcopy(cert["tree"])
        ch = t2["children"]
        keys = sorted(ch, key=int)
        # exchange the child of the reference state with a child that is a different leaf / subtree
        kref = str(cert["ref"][t2["site"]])
        other = next((k_ for k_ in keys if ch[k_] != ch[kref]), None)
        if other is not None:
            ch[kref], ch[other] = ch[other], ch[kref]
            c3 = Checker(cert).verify(t2, dom, cert["L"])
    # brute force from the tables of the file
    G = np.zeros(shape, dtype=np.int64)
    for i in range(n):
        sh = [1] * n; sh[i] = shape[i]
        G = G + np.array(cert["H"][i], dtype=np.int64).reshape(sh)
    for k, T in cert["J"].items():
        i, j = (int(v) for v in k.split(","))
        sh = [1] * n; sh[i] = shape[i]; sh[j] = shape[j]
        G = G + np.array(T, dtype=np.int64).reshape(sh)
    gmin = int(G.min()); at_ref = int(G[tuple(cert["ref"])])
    boxes = []
    leaf_boxes(cert["tree"], dom, boxes)
    viol = 0; covered = 0
    for (l, box) in boxes:
        bm = int(G[np.ix_(*box)].min())
        covered += int(np.prod([len(d) for d in box]))
        if cert["leaves"][l]["LB"] > bm or cert["leaves"][l]["LB"] < cert["L"]:
            viol += 1
    rows.append(dict(file=os.path.basename(path), instance=cert["instance"], tau=cert["tau"], split=cert["split"], variant=cert["variant"], shape=shape,
                     depth=cert["depth"], leaf_certificates=len(cert["leaves"]), leaf_boxes=len(boxes), accepted=ok, integers_in_certificate=nint,
                     integers_in_instance=ninst, additions=adds, comparisons=cmps, control_L_plus_1=c1, control_first_leaf_alone=c2, control_swapped_children=c3,
                     bf_min=gmin, bf_at_ref=at_ref, bf_states=int(G.size), bf_states_covered_by_leaves=covered, bf_leaf_violations=viol,
                     split_rule_accepted=ok_split, split_rule_additions=ck2.adds, split_rule_comparisons=ck2.cmps, split_rule_states_covered=covered_split))
    r = rows[-1]
    print(f"{r['file']}: {r['instance']} tau {r['tau']} {r['split']} [{r['variant']}]  depth {r['depth']}, {r['leaf_certificates']} leaf certificates for {r['leaf_boxes']} leaf boxes")
    print(f"   ACCEPTED: {ok}   ({adds} additions, {cmps} comparisons of integers; certificate {nint} integers, instance {ninst} integers; {time.time() - t0:.2f}s)")
    print(f"   controls (each must be False): bound L+1: {c1};  first leaf alone on the whole domain: {c2};  children of two states exchanged: {c3}")
    print(f"   brute force: minimum of the published instance over the {G.size} states = {gmin} (at the reference: {at_ref}); leaf boxes cover {covered} states; "
          f"leaves whose certified bound exceeds the exact leaf minimum: {viol}")
    print(f"   with a domain-split rule (each distinct leaf checked once on its own box; the boxes cover {covered_split} states): accepted {ok_split}; "
          f"{ck2.adds} additions, {ck2.cmps} comparisons")
    assert ok and not c1 and not c2 and c3 in (False, None) and gmin == cert["L"] == at_ref and covered == G.size and viol == 0
    assert ok_split and covered_split == G.size

json.dump(rows, open(os.path.join(HERE, "out", "p7_06_check.json"), "w"), indent=1)
print(f"\n{'instance':9s} {'tau':4s} {'variant':30s} {'depth':>5s} {'leaf cert.':>10s} {'leaf boxes':>10s} {'integers':>9s} {'additions':>10s} {'comparisons':>11s} | {'split rule: additions':>21s} {'comparisons':>11s} | {'states (brute force)':>20s}")
for r in rows:
    print(f"{r['instance']:9s} {r['tau']:4s} {r['variant']:30s} {r['depth']:5d} {r['leaf_certificates']:10d} {r['leaf_boxes']:10d} {r['integers_in_certificate']:9d} {r['additions']:10d} {r['comparisons']:11d} | "
          f"{r['split_rule_additions']:21d} {r['split_rule_comparisons']:11d} | {r['bf_states']:20d}")
print(f"\nall {len(rows)} certificates accepted; all {3 * len(rows) - sum(r['control_swapped_children'] is None for r in rows)} controls rejected; "
      f"brute force: {sum(r['leaf_boxes'] for r in rows)} leaf boxes, 0 violations")
print(f"[{time.time() - t00:.0f}s] wrote out/p7_06_check.json")
print("DONE p7_06_check")
