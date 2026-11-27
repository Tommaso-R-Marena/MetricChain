"""Random small instances, certificates built by a producer written here, and adversarial variants.

Everything is plain Python data in the shape of the *file* (``structbio-zcert/1`` as read in ``indep_zcheck``): a
certificate is a ``dict`` ready for ``json.dumps``.  The producer keeps only what validity needs (working domains and
the set of pairs still present); it computes no bound, so a certificate built here claims nothing unless a claim is
added afterwards.  Variants are produced by ``variants``; each is tagged with whether the reading of the format in
``indep_zcheck`` makes it valid, invalid, or valid only under one reading.
"""
from __future__ import annotations

import copy
import json
import random
from fractions import Fraction

FORMAT_TAG = "structbio-zcert/1"

BETAS = [Fraction(1), Fraction(1, 2), Fraction(3, 7), Fraction(211, 125), Fraction(1, 1000), Fraction(7, 3),
         Fraction(10), Fraction(123456789, 1000000007), Fraction(1, 3), Fraction(5, 2)]


def rational_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


# ----------------------------------------------------------------------------------------------------- instances

def random_tables(rng: random.Random, n: int | None = None, kmax: int = 4, graph: str | None = None,
                  amp: str | None = None, max_configs: int = 4096) -> dict:
    """``{"unary": [[int]], "pair": {(i, j): [[int]]}, "scale_bits": s, "style": {...}}``."""
    n = rng.randint(1, 6) if n is None else n
    while True:
        sizes = [rng.randint(1, kmax) for _ in range(n)]
        if rng.random() < 0.15:
            sizes[rng.randrange(n)] = 1                                   # a one-state site
        configs = 1
        for k in sizes:
            configs *= k
        if configs <= max_configs:
            break
    graph = graph or rng.choice(["none", "chain", "tree", "sparse", "dense", "dense", "star", "isolated"])
    amp = amp or rng.choice(["zero", "ties", "small", "small", "medium", "medium", "large", "penalty", "additive"])
    edges = []
    if graph == "chain":
        edges = [(i, i + 1) for i in range(n - 1)]
    elif graph == "tree":
        edges = [(rng.randrange(i), i) for i in range(1, n)]
    elif graph == "sparse":
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.35]
    elif graph == "dense":
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    elif graph == "star":
        edges = [(0, j) for j in range(1, n)]
    elif graph == "isolated":                                             # dense, but one site has no pair
        lonely = rng.randrange(n)
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if lonely not in (i, j)]

    def value() -> int:
        if amp == "zero":
            return 0
        if amp == "ties":
            return rng.choice([0, 0, 1, -1])
        if amp == "small":
            return rng.randint(-4, 4)
        if amp == "medium":
            return rng.randint(-60, 60)
        if amp == "large":
            return rng.randint(-10 ** 4, 10 ** 4)
        if amp == "penalty":
            return rng.randint(-5, 5) + (rng.choice([0, 0, 0, 400, 5000]))
        return rng.randint(-20, 20)

    unary = [[value() for _ in range(k)] for k in sizes]
    pair = {}
    for (i, j) in edges:
        if amp == "additive" or (amp in ("small", "medium", "penalty") and rng.random() < 0.3):
            f = [rng.randint(-30, 30) for _ in range(sizes[i])]          # exactly additive, or nearly so
            g = [rng.randint(-30, 30) for _ in range(sizes[j])]
            noise = rng.choice([0, 0, 1])
            pair[(i, j)] = [[f[a] + g[b] + rng.randint(-noise, noise) for b in range(sizes[j])]
                            for a in range(sizes[i])]
        else:
            pair[(i, j)] = [[value() for _ in range(sizes[j])] for _ in range(sizes[i])]
    scale_bits = rng.choice([0, 0, 1, 3, 6, 10, 20])
    if amp in ("small", "ties", "zero") and scale_bits > 6:
        scale_bits = rng.choice([0, 1, 3])
    return {"unary": unary, "pair": pair, "scale_bits": scale_bits,
            "style": {"graph": graph, "amp": amp, "sizes": sizes}}


def random_box(rng: random.Random, sizes, full_probability: float = 0.6) -> list:
    if rng.random() < full_probability:
        return [list(range(k)) for k in sizes]
    box = []
    for k in sizes:
        m = rng.randint(1, k)
        box.append(sorted(rng.sample(range(k), m)))
    return box


# -------------------------------------------------------------------------------------------------- the producer

class _Work:
    """Working state of the producer: domains, unary tables and the pairs still present (tables are shared)."""

    def __init__(self, domains, unary, pairs):
        self.D = [list(d) for d in domains]
        self.H = [list(h) for h in unary]
        self.J = dict(pairs)

    @property
    def live(self):
        return self.J.keys()

    def copy(self) -> "_Work":
        return _Work(self.D, self.H, self.J)

    def margin(self, i: int, r: int, t: int) -> int:
        """Goldstein margin of removing ``r`` with dominator ``t`` (used to *choose* steps, never to judge them)."""
        m = self.H[i][r] - self.H[i][t]
        for (p, q), table in self.J.items():
            if p == i:
                m += min(table[r][s] - table[t][s] for s in self.D[q])
            elif q == i:
                m += min(table[s][r] - table[s][t] for s in self.D[p])
        return m


def _fit(rng: random.Random, table, dom_i, dom_j, sizes_i: int, sizes_j: int, how: str, wild: int):
    """Additive functions ``f``, ``g`` for a relax step (any integers are admissible)."""
    f, g = [0] * sizes_i, [0] * sizes_j
    if how == "zero":
        return f, g
    if how == "random":
        return [rng.randint(-9, 9) for _ in f], [rng.randint(-9, 9) for _ in g]
    if how == "wild":
        return [rng.randint(-wild, wild) for _ in f], [rng.randint(-wild, wild) for _ in g]
    for a in range(sizes_i):                                              # "fit": row minimum, then column minimum
        f[a] = min(table[a][b] for b in dom_j)
    for b in range(sizes_j):
        g[b] = min(table[a][b] - f[a] for a in dom_i)
    return f, g


def random_node(rng: random.Random, tables: dict, work: _Work, keep, depth: int, leaves: list,
                max_steps: int = 4, branch_probability: float = 0.45, margin_floor=None, wild: int = 10 ** 5) -> dict:
    """A valid node (my reading) on the working state ``work`` (which is modified).

    ``margin_floor``: when not ``None``, only prunes whose margin (table units) is at least this are emitted --
    the reviewed checker needs gigabytes for a prune whose margin is below about -20 kT (see the cost campaign).
    """
    sizes = [len(u) for u in tables["unary"]]
    n = len(sizes)
    steps = []
    for _ in range(rng.randint(0, max_steps)):
        kind = rng.choice(["prune", "relax"])
        if kind == "prune":
            cands = [(i, r, t) for i in range(n) if len(work.D[i]) >= 2 for r in work.D[i] for t in work.D[i]
                     if r != t]
            if margin_floor is not None:
                cands = [(i, r, t) for (i, r, t) in cands if work.margin(i, r, t) >= margin_floor]
            if not cands:
                continue
            if rng.random() < 0.5:                                        # prefer the largest margins
                cands.sort(key=lambda c: -work.margin(*c))
                cands = cands[:max(1, len(cands) // 4)]
            i, r, t = rng.choice(cands)
            steps.append({"op": "prune", "site": i, "remove": r, "dominator": t})
            work.D[i].remove(r)
        else:
            if not work.J:
                continue
            i, j = rng.choice(sorted(work.J))
            how = rng.choice(["fit", "fit", "fit", "zero", "random", "wild"])
            f, g = _fit(rng, work.J[(i, j)], work.D[i], work.D[j], sizes[i], sizes[j], how, wild)
            steps.append({"op": "relax", "pair": [i, j], "f": f, "g": g})
            del work.J[(i, j)]
            work.H[i] = [h + v for h, v in zip(work.H[i], f)]
            work.H[j] = [h + v for h, v in zip(work.H[j], g)]
    candidates = [i for i in range(n) if i != keep]
    if depth > 0 and candidates and len(leaves) < 24 and rng.random() < branch_probability:
        wide = [i for i in candidates if len(work.D[i]) >= 2]
        site = rng.choice(wide) if wide and rng.random() < 0.85 else rng.choice(candidates)
        children = {}
        for a in work.D[site]:
            sub = work.copy()
            sub.D[site] = [a]
            children[str(a)] = random_node(rng, tables, sub, keep, depth - 1, leaves, max_steps, branch_probability,
                                           margin_floor, wild)
        return {"steps": steps, "branch": site, "children": children}
    order = [i for i in range(n) if i != keep]
    rng.shuffle(order)
    leaves.append(1)
    return {"steps": steps, "order": order}


def random_certificate(rng: random.Random, tables: dict, sha: str, beta: Fraction | None = None, domains=None,
                       keep="random", depth: int | None = None, max_steps: int = 4, max_prune_kt=None,
                       wild_kt=None) -> dict:
    """``max_prune_kt``: no prune with a margin below ``-max_prune_kt`` (in units of ``1 / beta``);
    ``wild_kt``: bound of the "wild" additive functions in the same units (default: 10**5 table units)."""
    sizes = [len(u) for u in tables["unary"]]
    n = len(sizes)
    beta = rng.choice(BETAS) if beta is None else beta
    domains = random_box(rng, sizes) if domains is None else domains
    if keep == "random":
        keep = rng.randrange(n) if rng.random() < 0.5 else None
    depth = rng.choice([0, 0, 1, 2, 3]) if depth is None else depth
    unit = Fraction(1, 2 ** tables["scale_bits"])
    floor = None
    wild = 10 ** 5
    if beta > 0:
        if max_prune_kt is not None:
            floor = -int(max_prune_kt / (beta * unit))
        if wild_kt is not None:
            wild = max(1, int(wild_kt / (beta * unit)))
    work = _Work(domains, tables["unary"], tables["pair"])
    root = random_node(rng, tables, work, keep, depth, [], max_steps, 0.45, floor, wild)
    return {"format": FORMAT_TAG, "model_sha256": sha, "beta": rational_text(beta),
            "domains": [list(d) for d in domains], "keep": keep, "claim": {}, "root": root, "meta": "{}"}


def temper(rng: random.Random, tables: dict, beta: Fraction, limit: int = 600) -> None:
    """Raise ``scale_bits`` (in place) until ``beta * max|entry| * 2**-scale_bits <= limit``: the reviewed checker's
    exact tier keeps every Boltzmann factor as an exact rational, so colder instances cost it megabytes per entry."""
    top = max([abs(v) for u in tables["unary"] for v in u] + [abs(v) for t in tables["pair"].values() for r in t
                                                               for v in r] + [1])
    while beta * top > limit * 2 ** tables["scale_bits"]:
        tables["scale_bits"] += 1


def hazard(doc: dict, tables: dict):
    """What a checker that keeps exponentials as exact rationals is about to face: ``(max exponent of a prune factor
    rho = exp(q), max |exponent| of a relax factor, max |exponent| of a Boltzmann factor at a leaf)``, by a replay
    that stops silently at the first invalid step (the reviewed checker stops there too).  Used only to decide
    whether to *run* that checker on a certificate, never to judge it."""
    try:
        beta = Fraction(doc["beta"])
        unit = Fraction(1, 2 ** tables["scale_bits"])
        worst = [Fraction(0), Fraction(0), Fraction(0)]
        stack = [(doc["root"], _Work(doc["domains"], tables["unary"], tables["pair"]))]
        guard = 0
        while stack and guard < 5000:
            guard += 1
            node, work = stack.pop()
            alive = True
            total = Fraction(0)
            lo_sum = hi_sum = 0
            for step in node["steps"]:
                if step["op"] == "prune":
                    i, r, t = step["site"], step["remove"], step["dominator"]
                    if r == t or r not in work.D[i] or t not in work.D[i]:
                        alive = False
                        break
                    q = -beta * work.margin(i, r, t) * unit
                    worst[0] = max(worst[0], q)
                    work.D[i].remove(r)
                else:
                    i, j = step["pair"]
                    f, g = step["f"], step["g"]
                    table = work.J.pop((i, j))
                    res = [table[a][b] - f[a] - g[b] for a in work.D[i] for b in work.D[j]]
                    lo_sum += min(res)
                    hi_sum += max(res)
                    worst[1] = max(worst[1], abs(beta * lo_sum * unit), abs(beta * hi_sum * unit))
                    work.H[i] = [h + v for h, v in zip(work.H[i], f)]
                    work.H[j] = [h + v for h, v in zip(work.H[j], g)]
            if not alive:
                continue
            if "children" in node:
                site = node["branch"]
                for a in work.D[site]:
                    sub = node["children"].get(str(a))
                    if sub is None:
                        break
                    child = work.copy()
                    child.D[site] = [a]
                    stack.append((sub, child))
            else:
                top = max([abs(work.H[i][a]) for i in range(len(work.H)) for a in work.D[i]]
                          + [abs(t[a][b]) for (i, j), t in work.J.items() for a in work.D[i] for b in work.D[j]] + [0])
                worst[2] = max(worst[2], beta * top * unit)
        return tuple(worst)
    except Exception:                                                      # noqa: BLE001  (malformed: no estimate)
        return None


def dumps(doc: dict) -> str:
    return json.dumps(doc, separators=(",", ":"))


# ------------------------------------------------------------------------------------------------------ variants

def _nodes(root: dict) -> list:
    out, stack = [], [root]
    while stack:
        node = stack.pop()
        out.append(node)
        if "children" in node and isinstance(node["children"], dict):
            stack.extend(node["children"].values())
    return out


def _index(nodes: list, node: dict) -> int:
    """Position of ``node`` itself (identity, not equality: equal leaves are common)."""
    return next(k for k, other in enumerate(nodes) if other is node)


def _replay_domains(doc: dict, sizes):
    """Working domains and live pairs *before the steps* of every node, and after them (by ``id(node)``)."""
    before, after = {}, {}
    stack = [(doc["root"], [list(d) for d in doc["domains"]], None)]
    while stack:
        node, D, _ = stack.pop()
        before[id(node)] = [list(d) for d in D]
        D = [list(d) for d in D]
        for step in node["steps"]:
            if step.get("op") == "prune" and step["remove"] in D[step["site"]]:
                D[step["site"]].remove(step["remove"])
        after[id(node)] = D
        if "children" in node:
            for key, sub in node["children"].items():
                Dc = [list(d) for d in D]
                Dc[node["branch"]] = [int(key)]
                stack.append((sub, Dc, None))
    return before, after


def variants(rng: random.Random, doc: dict, tables: dict) -> list:
    """Adversarial variants of a valid certificate: ``[(name, expectation, doc)]``.

    ``expectation`` is what the reading of ``indep_zcheck`` says: ``"invalid"`` (must not be accepted, or if accepted
    must still be sound -- enumeration decides), ``"valid"`` (still a correct certificate) or ``"reading"`` (valid
    under one natural reading of the specification, invalid under another).
    """
    sizes = [len(u) for u in tables["unary"]]
    n = len(sizes)
    out = []

    def fresh():
        d = copy.deepcopy(doc)
        nodes = _nodes(d["root"])
        before, after = _replay_domains(d, sizes)
        return d, nodes, before, after

    def add(name, expectation, d):
        out.append((name, expectation, d))

    # --- prune steps -------------------------------------------------------------------------------------------
    d, nodes, before, after = fresh()
    cands = [(nd, k) for nd in nodes for k, s in enumerate(nd["steps"]) if s["op"] == "prune"]
    if cands:
        nd, k = rng.choice(cands)
        d2 = copy.deepcopy(d)
        st = _nodes(d2["root"])[_index(nodes, nd)]["steps"][k]
        st["dominator"] = st["remove"]
        add("prune_dominator_is_removed", "invalid", d2)
        d2 = copy.deepcopy(d)
        st = _nodes(d2["root"])[_index(nodes, nd)]["steps"][k]
        st["dominator"] = sizes[st["site"]]
        add("prune_dominator_out_of_range", "invalid", d2)
        d2 = copy.deepcopy(d)
        st = _nodes(d2["root"])[_index(nodes, nd)]["steps"][k]
        st["dominator"] = -1
        add("prune_dominator_minus_one", "invalid", d2)
        d2 = copy.deepcopy(d)
        st = _nodes(d2["root"])[_index(nodes, nd)]["steps"][k]
        st["site"] = n
        add("prune_site_out_of_range", "invalid", d2)
        d2 = copy.deepcopy(d)
        st = _nodes(d2["root"])[_index(nodes, nd)]["steps"][k]
        st["site"] = st["site"] - n                                      # a negative index that Python would accept
        add("prune_site_negative_alias", "invalid", d2)
        d2 = copy.deepcopy(d)
        nd2 = _nodes(d2["root"])[_index(nodes, nd)]
        nd2["steps"].insert(k + 1, copy.deepcopy(nd2["steps"][k]))        # the same prune twice
        add("prune_repeated", "invalid", d2)
        d2 = copy.deepcopy(d)
        nd2 = _nodes(d2["root"])[_index(nodes, nd)]
        st = nd2["steps"][k]
        nd2["steps"].insert(k + 1, {"op": "prune", "site": st["site"], "remove": st["dominator"],
                                    "dominator": st["remove"]})           # then the dominator "dominated" by the removed
        add("prune_by_removed_state", "invalid", d2)
        d2 = copy.deepcopy(d)
        st = _nodes(d2["root"])[_index(nodes, nd)]["steps"][k]
        st["remove"], st["dominator"] = st["dominator"], st["remove"]    # swapped roles: valid, the margin changes sign
        add("prune_roles_swapped", "valid_if_consistent", d2)
    # a prune whose dominator lies outside the working domain but inside the alphabet
    d, nodes, before, after = fresh()
    cands = []
    for nd in nodes:
        D = after[id(nd)]
        for i in range(n):
            outside = [a for a in range(sizes[i]) if a not in D[i]]
            if outside and len(D[i]) >= 1:
                cands.append((nd, i, D[i], outside))
    if cands:
        nd, i, inside, outside = rng.choice(cands)
        d2 = copy.deepcopy(d)
        nd2 = _nodes(d2["root"])[_index(nodes, nd)]
        nd2["steps"].append({"op": "prune", "site": i, "remove": rng.choice(inside), "dominator": rng.choice(outside)})
        add("prune_dominator_outside_domain", "invalid", d2)
        d2 = copy.deepcopy(d)
        nd2 = _nodes(d2["root"])[_index(nodes, nd)]
        if len(inside) >= 1:
            nd2["steps"].append({"op": "prune", "site": i, "remove": rng.choice(outside),
                                 "dominator": rng.choice(inside)})
            add("prune_removed_outside_domain", "invalid", d2)
    # a prune that empties a domain (only one state left: the dominator must be the state itself or outside)
    d, nodes, before, after = fresh()
    cands = [(nd, i) for nd in nodes for i in range(n) if len(after[id(nd)][i]) == 1]
    if cands:
        nd, i = rng.choice(cands)
        d2 = copy.deepcopy(d)
        nd2 = _nodes(d2["root"])[_index(nodes, nd)]
        a = after[id(nd)][i][0]
        nd2["steps"].append({"op": "prune", "site": i, "remove": a, "dominator": a})
        add("prune_last_state_by_itself", "invalid", d2)

    # --- relax steps -------------------------------------------------------------------------------------------
    d, nodes, before, after = fresh()
    cands = [(nd, k) for nd in nodes for k, s in enumerate(nd["steps"]) if s["op"] == "relax"]
    if cands:
        nd, k = rng.choice(cands)
        idx = _index(nodes, nd)
        d2 = copy.deepcopy(d)
        nd2 = _nodes(d2["root"])[idx]
        nd2["steps"].insert(k + 1, copy.deepcopy(nd2["steps"][k]))
        add("relax_repeated", "invalid", d2)
        d2 = copy.deepcopy(d)
        st = _nodes(d2["root"])[idx]["steps"][k]
        st["f"] = st["f"] + [0]
        add("relax_f_too_long", "invalid", d2)
        d2 = copy.deepcopy(d)
        st = _nodes(d2["root"])[idx]["steps"][k]
        if len(st["g"]) > 1:
            st["g"] = st["g"][:-1]
            add("relax_g_too_short", "invalid", d2)
        d2 = copy.deepcopy(d)
        st = _nodes(d2["root"])[idx]["steps"][k]
        st["pair"] = [st["pair"][0], st["pair"][0]]
        add("relax_pair_same_site", "invalid", d2)
        d2 = copy.deepcopy(d)
        st = _nodes(d2["root"])[idx]["steps"][k]
        st["pair"] = [st["pair"][1], st["pair"][0]]
        st["f"], st["g"] = st["g"], st["f"]
        add("relax_pair_reversed_consistent", "reading", d2)
        d2 = copy.deepcopy(d)
        st = _nodes(d2["root"])[idx]["steps"][k]
        if len(st["f"]) == len(st["g"]):
            st["pair"] = [st["pair"][1], st["pair"][0]]                  # reversed, f and g NOT swapped
            add("relax_pair_reversed_same_shapes", "reading", d2)
        d2 = copy.deepcopy(d)
        st = _nodes(d2["root"])[idx]["steps"][k]
        st["pair"] = [st["pair"][0] - n, st["pair"][1]]
        add("relax_site_negative_alias", "invalid", d2)
        d2 = copy.deepcopy(d)
        st = _nodes(d2["root"])[idx]["steps"][k]
        st["f"] = [v + rng.randint(-3, 3) for v in st["f"]]             # another additive function: still valid
        add("relax_other_f", "valid", d2)
    # relax of a pair that the model does not list
    d, nodes, before, after = fresh()
    absent = [(i, j) for i in range(n) for j in range(i + 1, n) if (i, j) not in tables["pair"]]
    if absent:
        i, j = rng.choice(absent)
        nd = rng.choice(nodes)
        nd["steps"].append({"op": "relax", "pair": [i, j], "f": [rng.randint(-2, 2) for _ in range(sizes[i])],
                            "g": [rng.randint(-2, 2) for _ in range(sizes[j])]})
        add("relax_unlisted_pair", "reading", d)

    # --- orders ------------------------------------------------------------------------------------------------
    d, nodes, before, after = fresh()
    leaves = [nd for nd in nodes if "order" in nd]
    nd = rng.choice(leaves)
    idx = _index(nodes, nd)
    if nd["order"]:
        d2 = copy.deepcopy(d)
        nd2 = _nodes(d2["root"])[idx]
        nd2["order"] = nd2["order"][:-1]
        add("order_missing_site", "invalid", d2)
        d2 = copy.deepcopy(d)
        nd2 = _nodes(d2["root"])[idx]
        nd2["order"] = nd2["order"] + [nd2["order"][0]]
        add("order_repeated_site", "invalid", d2)
        if len(nd["order"]) >= 2:
            d2 = copy.deepcopy(d)
            nd2 = _nodes(d2["root"])[idx]
            nd2["order"] = nd2["order"][:-1] + [nd2["order"][0]]
            add("order_repeat_replaces_site", "invalid", d2)
        d2 = copy.deepcopy(d)
        nd2 = _nodes(d2["root"])[idx]
        nd2["order"] = [v - n for v in nd2["order"]]
        add("order_negative_aliases", "invalid", d2)
    d2 = copy.deepcopy(d)
    nd2 = _nodes(d2["root"])[idx]
    nd2["order"] = nd2["order"] + [n]
    add("order_site_out_of_range", "invalid", d2)
    if d["keep"] is not None:
        d2 = copy.deepcopy(d)
        nd2 = _nodes(d2["root"])[idx]
        nd2["order"] = nd2["order"] + [d["keep"]]
        add("order_contains_kept_site", "invalid", d2)
    # sites fixed by conditioning left out of a leaf's order (valid under the reading "the remaining sites")
    d, nodes, before, after = fresh()
    fixed_cands = []
    stack = [(d["root"], [])]
    while stack:
        node, fixed = stack.pop()
        if "children" in node:
            for sub in node["children"].values():
                stack.append((sub, fixed + [node["branch"]]))
        elif fixed:
            fixed_cands.append((node, fixed))
    if fixed_cands:
        node, fixed = rng.choice(fixed_cands)
        node["order"] = [v for v in node["order"] if v not in fixed]
        add("order_without_conditioned_sites", "reading", d)

    # --- branch nodes ------------------------------------------------------------------------------------------
    d, nodes, before, after = fresh()
    branches = [nd for nd in nodes if "children" in nd]
    if branches:
        nd = rng.choice(branches)
        idx = _index(nodes, nd)
        if len(nd["children"]) >= 1:
            d2 = copy.deepcopy(d)
            nd2 = _nodes(d2["root"])[idx]
            key = rng.choice(sorted(nd2["children"]))
            del nd2["children"][key]
            add("branch_missing_child", "invalid", d2)
        d2 = copy.deepcopy(d)
        nd2 = _nodes(d2["root"])[idx]
        site = nd2["branch"]
        gone = [a for a in range(sizes[site]) if str(a) not in nd2["children"]]
        some = copy.deepcopy(next(iter(nd2["children"].values())))
        if gone:
            nd2["children"][str(rng.choice(gone))] = some
            add("branch_surplus_child_outside_domain", "invalid", d2)
        d2 = copy.deepcopy(d)
        nd2 = _nodes(d2["root"])[idx]
        nd2["children"][str(sizes[site])] = copy.deepcopy(some)
        add("branch_surplus_child_out_of_range", "invalid", d2)
        d2 = copy.deepcopy(d)
        nd2 = _nodes(d2["root"])[idx]
        key = sorted(nd2["children"])[0]
        nd2["children"] = {("0" + k if k == key else k): v for k, v in nd2["children"].items()}
        add("branch_child_key_leading_zero", "invalid", d2)
        d2 = copy.deepcopy(d)
        nd2 = _nodes(d2["root"])[idx]
        nd2["branch"] = n
        add("branch_site_out_of_range", "invalid", d2)
        d2 = copy.deepcopy(d)
        nd2 = _nodes(d2["root"])[idx]
        nd2["branch"] = nd2["branch"] - n
        add("branch_site_negative_alias", "invalid", d2)
        if d["keep"] is not None and len(after[id(nd)][d["keep"]]) == len(nd["children"]):
            d2 = copy.deepcopy(d)
            nd2 = _nodes(d2["root"])[idx]
            nd2["branch"] = d["keep"]
            add("branch_on_kept_site_same_arity", "invalid", d2)
        # a child that prunes the conditioned site with the state conditioned on elsewhere
        d2 = copy.deepcopy(d)
        nd2 = _nodes(d2["root"])[idx]
        keys = sorted(nd2["children"])
        if len(keys) >= 2:
            nd2["children"][keys[0]]["steps"].insert(0, {"op": "prune", "site": site, "remove": int(keys[0]),
                                                           "dominator": int(keys[1])})
            add("child_prunes_conditioned_state", "invalid", d2)
    if d["keep"] is not None:
        d2 = copy.deepcopy(d)
        leaf = rng.choice([nd for nd in _nodes(d2["root"]) if "order" in nd])
        dom = None
        # replace a leaf by a branch on the kept site
        before2, after2 = _replay_domains(d2, sizes)
        dom = after2[id(leaf)][d2["keep"]]
        order = leaf.pop("order")
        leaf["branch"] = d2["keep"]
        leaf["children"] = {str(a): {"steps": [], "order": list(order)} for a in dom}
        add("branch_on_kept_site", "invalid", d2)
    # branch on a site with one state left (valid: Z(D) = Z(D, x_i = a))
    d, nodes, before, after = fresh()
    leaves = [nd for nd in nodes if "order" in nd]
    nd = rng.choice(leaves)
    singles = [i for i in range(n) if i != d["keep"] and len(after[id(nd)][i]) == 1]
    if singles:
        site = rng.choice(singles)
        order = nd.pop("order")
        nd["branch"] = site
        nd["children"] = {str(after[id(nd)][site][0]): {"steps": [], "order": order}}
        add("branch_on_single_state_site", "valid", d)

    # --- the header --------------------------------------------------------------------------------------------
    d2 = copy.deepcopy(doc)
    i = rng.randrange(n)
    d2["domains"][i] = d2["domains"][i] + [d2["domains"][i][-1]]
    add("domain_duplicate_state", "invalid", d2)
    cand = [i for i in range(n) if len(doc["domains"][i]) >= 2]
    if cand:
        d2 = copy.deepcopy(doc)
        i = rng.choice(cand)
        d2["domains"][i] = list(reversed(d2["domains"][i]))
        add("domain_not_sorted", "reading", d2)
    d2 = copy.deepcopy(doc)
    i = rng.randrange(n)
    d2["domains"][i] = d2["domains"][i] + [sizes[i]]
    add("domain_state_out_of_range", "invalid", d2)
    d2 = copy.deepcopy(doc)
    i = rng.randrange(n)
    d2["domains"][i] = [a - sizes[i] for a in d2["domains"][i]]
    add("domain_negative_aliases", "invalid", d2)
    d2 = copy.deepcopy(doc)
    d2["domains"][rng.randrange(n)] = []
    add("domain_empty", "invalid", d2)
    d2 = copy.deepcopy(doc)
    d2["domains"] = d2["domains"] + [[0]]
    add("domains_one_too_many", "invalid", d2)
    d2 = copy.deepcopy(doc)
    b = Fraction(doc["beta"])
    d2["beta"] = rational_text(-b if b != 0 else Fraction(-1))
    add("beta_negative", "invalid", d2)
    d2 = copy.deepcopy(doc)
    d2["beta"] = "0/1"
    add("beta_zero", "valid", d2)
    d2 = copy.deepcopy(doc)
    d2["keep"] = n
    add("keep_out_of_range", "invalid", d2)
    d2 = copy.deepcopy(doc)
    d2["keep"] = -1
    add("keep_minus_one", "invalid", d2)
    return out
