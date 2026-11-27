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

Changed by the coordinator on 2026-11-26 after the engineering division's report X-012 (experiments/eng/leafcert/REPORT.md
at their commit 0e5103b, section 9): the version of the workstream did not validate its input, and its total
`sum(U) + sum(P2.values())` ran over everything in U and P2 while the inequalities looked only at U[0..n-1] and the pairs
i < j < n -- so an extra entry was added to the total without being bounded, and a malformed file could be accepted with a
false bound (their example: one site, H = [[5, 7]], U = [5, 100], L = 100).  None of the nine files is malformed and none
of their verdicts or counts changes.  Now: (i) the file is loaded strictly (no duplicate keys, integers only); (ii)
`well_formed` rejects, before any arithmetic, everything that is not exactly the format above (lengths, key sets in
canonical spelling, a tree that branches on unfixed sites with exactly one child per state, leaf indices in range);
(iii) the total is taken over the sites and the pairs i < j only.  Two more controls, which must be REJECTED:
  (c4) the engineering division's example;
  (c5) each file with one extra key "1,0" in the P2 of every leaf, large enough to lift every total above L + 1,
       checked against the bound L + 1 (the unvalidated version accepts it: a false bound, since the minimum is L).
The log of the version before this change is logs/p7_06_check.log (and logs/run1/); of this version logs/p7_06_check_v2.log.
"""
import sys, os, json, glob, time, copy
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
t00 = time.time()
print(f"p7_06_check  started {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")


def _no_duplicates(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError(f"duplicate key {k!r}")
        d[k] = v
    return d


def _reject(x):
    raise ValueError(f"not an integer: {x!r}")


def load_strict(text):
    """JSON with no duplicate keys and no number that is not an integer (no fraction, exponent, NaN, Infinity)."""
    return json.loads(text, object_pairs_hook=_no_duplicates, parse_float=_reject, parse_constant=_reject)


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def well_formed(cert):
    """None if the object is exactly a certificate in the format of the docstring, otherwise the reason (a string)."""
    try:
        for key in ("shape", "H", "J", "L", "tree", "leaves"):
            if key not in cert:
                return f"key {key!r} missing"
        shape = cert["shape"]
        if not (isinstance(shape, list) and len(shape) >= 1 and all(_is_int(k) and k >= 1 for k in shape)):
            return "shape is not a list of positive integers"
        n = len(shape)
        H = cert["H"]
        if not (isinstance(H, list) and len(H) == n and all(isinstance(h, list) and len(h) == shape[i] and all(_is_int(v) for v in h) for i, h in enumerate(H))):
            return "H does not have one integer per state of every site"
        pair_keys = {f"{i},{j}" for i in range(n) for j in range(i + 1, n)}
        ordered_keys = {f"{i},{j}" for i in range(n) for j in range(n) if i != j}
        J = cert["J"]
        if not (isinstance(J, dict) and set(J) == pair_keys):
            return "J does not have exactly the keys 'i,j' with i < j"
        for key, T in J.items():
            i, j = (int(v) for v in key.split(","))
            if not (isinstance(T, list) and len(T) == shape[i] and all(isinstance(r, list) and len(r) == shape[j] and all(_is_int(v) for v in r) for r in T)):
                return f"J[{key}] is not a {shape[i]} x {shape[j]} table of integers"
        if not _is_int(cert["L"]):
            return "L is not an integer"
        leaves = cert["leaves"]
        if not (isinstance(leaves, list) and len(leaves) >= 1):
            return "leaves is not a non-empty list"
        for t, leaf in enumerate(leaves):
            if not isinstance(leaf, dict) or any(key not in leaf for key in ("U", "P2", "m")):
                return f"leaf {t}: U, P2 or m missing"
            U, P2, m = leaf["U"], leaf["P2"], leaf["m"]
            if not (isinstance(U, list) and len(U) == n and all(_is_int(v) for v in U)):
                return f"leaf {t}: U is not a list of exactly {n} integers"
            if not (isinstance(P2, dict) and set(P2) == pair_keys and all(_is_int(v) for v in P2.values())):
                return f"leaf {t}: P2 does not have exactly the keys 'i,j' with i < j, with integer values"
            if not (isinstance(m, dict) and set(m) == ordered_keys):
                return f"leaf {t}: m does not have exactly the keys 'i,j' with i != j"
            for key, vec in m.items():
                i = int(key.split(",")[0])
                if not (isinstance(vec, list) and len(vec) == shape[i] and all(_is_int(v) for v in vec)):
                    return f"leaf {t}: m[{key}] is not a list of {shape[i]} integers"
        used = set()

        def walk(node, fixed):
            if not isinstance(node, dict):
                return "a node is not an object"
            if set(node) == {"leaf"}:
                if not (_is_int(node["leaf"]) and 0 <= node["leaf"] < len(leaves)):
                    return "a leaf index is out of range"
                used.add(node["leaf"]); return None
            if set(node) == {"site", "children"}:
                i = node["site"]
                if not (_is_int(i) and 0 <= i < n):
                    return "a branch on a site that does not exist"
                if i in fixed:
                    return "a branch on a site that an ancestor has fixed"
                ch = node["children"]
                if not (isinstance(ch, dict) and set(ch) == {str(a) for a in range(shape[i])}):
                    return "a branch without exactly one child per state"
                for a in range(shape[i]):
                    r = walk(ch[str(a)], fixed | {i})
                    if r is not None:
                        return r
                return None
            return "a node that is neither a leaf nor a branch"
        r = walk(cert["tree"], frozenset())
        if r is not None:
            return r
        if used != set(range(len(leaves))):
            return "a leaf certificate that no node names"
        return None
    except (TypeError, ValueError, KeyError, AttributeError) as e:
        return f"malformed ({type(e).__name__}: {e})"


def accepts(cert, L=None, tree=None):
    """The verdict on a certificate object: well formed and all inequalities hold (for the bound L and the tree given, if any)."""
    if tree is not None:
        cert = dict(cert); cert["tree"] = tree
        used = set()

        def names(node):
            if "leaf" in node: used.add(node["leaf"])
            else:
                for c in node["children"].values(): names(c)
        try:
            names(tree)
            order = sorted(used); remap = {t: q for q, t in enumerate(order)}
            cert["leaves"] = [cert["leaves"][t] for t in order]

            def rename(node):
                return {"leaf": remap[node["leaf"]]} if "leaf" in node else {"site": node["site"], "children": {k: rename(c) for k, c in node["children"].items()}}
            cert["tree"] = rename(tree)
        except (TypeError, KeyError, AttributeError, IndexError):
            return False
    if well_formed(cert) is not None:
        return False
    return Checker(cert).verify(cert["tree"], [list(range(k)) for k in cert["shape"]], cert["L"] if L is None else L)


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
        tot = sum(U[i] for i in range(n)) + sum(P2[(i, j)] for i in range(n) for j in range(i + 1, n))
        self.adds += n + n * (n - 1) // 2 - 1; self.cmps += 1
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


rows = []; rows_c5 = []
# (c4) the engineering division's example of a malformed object with a false bound
ex = dict(shape=[2], H=[[5, 7]], J={}, L=100, tree=dict(leaf=0), leaves=[dict(U=[5, 100], P2={}, m={})])
c4 = accepts(ex); c4_reason = well_formed(ex)
print(f"control (c4), one site, H = [[5, 7]], U = [5, 100], L = 100 (the minimum is 5): accepted {c4} (must be False; reason: {c4_reason})")
ex_ok = dict(shape=[2], H=[[5, 7]], J={}, L=5, tree=dict(leaf=0), leaves=[dict(U=[5], P2={}, m={})])
print(f"   the well-formed certificate of the same instance for its true minimum 5: accepted {accepts(ex_ok)} (must be True); for 6: {accepts(ex_ok, L=6)} (must be False)")
assert c4 is False and c4_reason is not None and accepts(ex_ok) is True and accepts(ex_ok, L=6) is False
for bad_text, why in (('{"a": 1, "a": 2}', "a duplicate key"), ('{"L": 1.0}', "a fraction"), ('{"L": NaN}', "NaN"), ('{"L": 1e3}', "an exponent")):
    try:
        load_strict(bad_text); raise AssertionError(why)
    except ValueError:
        pass
print("   strict loading rejects a duplicate key, a fraction, NaN and an exponent")
for path in sorted(glob.glob(os.path.join(HERE, "out", "p7_02_cert*.json"))):
    cert = load_strict(open(path).read())
    wf = well_formed(cert)
    assert wf is None, (path, wf)
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
    # (c5) one extra key in the P2 of every leaf, large enough to lift every total above L + 1: must be rejected for L + 1
    bad = copy.deepcopy(cert)
    for leaf_ in bad["leaves"]: leaf_["P2"]["1,0"] = 10 ** 15
    c5 = accepts(bad, L=cert["L"] + 1)
    c5_reason = well_formed(bad)
    # what the version before the change did with it (its rule, reproduced: no validation, the total over everything)
    def old_rule(c, L):
        ck_ = Checker(c); orig = Checker.leaf_ok

        def leaf_old(self, leaf, dom_, L_):
            m_ = {tuple(int(v) for v in k.split(",")): arr for k, arr in leaf["m"].items()}
            P2_ = {tuple(int(v) for v in k.split(",")): v2 for k, v2 in leaf["P2"].items()}
            U_ = leaf["U"]
            for i_ in range(self.n):
                for a_ in dom_[i_]:
                    if not U_[i_] <= self.H[i_][a_] + sum(m_[(i_, j_)][a_] for j_ in range(self.n) if j_ != i_): return False
            for i_ in range(self.n):
                for j_ in range(i_ + 1, self.n):
                    for a_ in dom_[i_]:
                        for b_ in dom_[j_]:
                            if not P2_[(i_, j_)] <= self.J[(i_, j_)][a_][b_] - m_[(i_, j_)][a_] - m_[(j_, i_)][b_]: return False
            return L_ <= sum(U_) + sum(P2_.values())
        Checker.leaf_ok = leaf_old
        try: return ck_.verify(c["tree"], [list(range(k_)) for k_ in c["shape"]], L)
        finally: Checker.leaf_ok = orig
    c5_old = old_rule(bad, cert["L"] + 1)
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
    print(f"   malformed control (c5), an extra key '1,0' in the P2 of every leaf, against the bound L+1: accepted {c5} (must be False; reason: {c5_reason}); "
          f"the rule of the version before the change on the same object: accepted {c5_old} (the defect, if True)")
    assert c5 is False and c5_reason is not None
    rows_c5.append((c5, c5_old))
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
print(f"malformed controls (c5): {sum(1 for a, b in rows_c5 if a is False)} of {len(rows_c5)} rejected; the rule before the change accepted {sum(1 for a, b in rows_c5 if b)} of them")
print(f"[{time.time() - t00:.0f}s] wrote out/p7_06_check.json")
print("DONE p7_06_check")
