"""Task 1 (definitions audit): displayed quartets computed LITERALLY as in arXiv:2507.17308 --
   N|_Y  = union of all up-down paths between leaves of Y in the semi-directed network, degree-2 nodes
           suppressed (Def. 2.5);
   T(N|_Y) = trees obtained by deleting one hybrid edge per hybrid node of N|_Y, recursively deleting leaves
           not in Y, suppressing degree-2 nodes (Section 2.1);
   'displayed quartet of N' = quartet tree displayed by a quarnet N|_{xyzw}.
and compared with the quartets induced by the displayed trees of N (what the working paper uses)."""
from itertools import combinations, product
import rnet


def mixed_edges(net):
    """edges of the semi-directed network: list of (u, v, head) ; head in {None, u, v}"""
    G, H, leaves = rnet.semi_directed(net)
    return [(u, v, d["head"]) for u, v, d in G.edges(data=True)], leaves


def updown_paths(edges, x1, x2):
    """all simple paths x1..x2 (as lists of edge indices) of the form: first edges directed towards x1,
    then edges directed towards x2 (undirected edges count as bidirected)."""
    adj = {}
    for idx, (u, v, head) in enumerate(edges):
        adj.setdefault(u, []).append((idx, v, head))
        adj.setdefault(v, []).append((idx, u, head))
    out = []

    def dfs(node, visited, used, seen_forward):
        if node == x2:
            out.append(list(used))
            return
        for idx, nxt, head in adj[node]:
            if nxt in visited:
                continue
            if head is None:
                sf = seen_forward
            elif head == nxt:          # traversed along its direction: 'directed towards x2'
                sf = True
            else:                      # head == node: traversed against its direction: 'directed towards x1'
                if seen_forward:
                    continue
                sf = False
            visited.add(nxt)
            used.append(idx)
            dfs(nxt, visited, used, sf)
            used.pop()
            visited.discard(nxt)

    dfs(x1, {x1}, [], False)
    return out


def suppress_degree2(edges, keep):
    """exhaustively suppress degree-2 nodes not in keep.  edges: list of (u,v,head)."""
    edges = list(edges)
    while True:
        deg = {}
        for u, v, h in edges:
            deg[u] = deg.get(u, 0) + 1
            deg[v] = deg.get(v, 0) + 1
        x = next((n for n, dg in deg.items() if dg == 2 and n not in keep), None)
        if x is None:
            return edges
        inc = [e for e in edges if x in (e[0], e[1])]
        assert len(inc) == 2
        rest = [e for e in edges if x not in (e[0], e[1])]
        (u1, v1, h1), (u2, v2, h2) = inc
        a = v1 if u1 == x else u1
        b = v2 if u2 == x else u2
        assert a != b, "loop created"
        heads = [h for h in (h1, h2) if h is not None and h != x]
        assert len(heads) <= 1, "edge directed both ways"
        rest.append((a, b, heads[0] if heads else None))
        edges = rest


def subnetwork(net, Y):
    edges, leaves = mixed_edges(net)
    used = set()
    for x1, x2 in combinations(Y, 2):
        for p in updown_paths(edges, x1, x2):
            used.update(p)
    sub = [edges[i] for i in sorted(used)]
    return suppress_degree2(sub, set(Y))


def displayed_trees_mixed(edges, Y):
    """list of trees (edge lists) displayed by the mixed graph, with multiplicity"""
    Y = set(Y)
    heads = {}
    for idx, (u, v, h) in enumerate(edges):
        if h is not None:
            heads.setdefault(h, []).append(idx)
    hyb = sorted(heads, key=str)
    for h in hyb:
        assert len(heads[h]) in (1, 2), (h, heads[h])
    true_hyb = [h for h in hyb if len(heads[h]) == 2]
    out = []
    for choice in product((0, 1), repeat=len(true_hyb)):
        dele = {heads[h][c] for h, c in zip(true_hyb, choice)}
        E = [(u, v, None) for idx, (u, v, hh) in enumerate(edges) if idx not in dele]
        # recursively delete leaves not in Y
        while True:
            deg = {}
            for u, v, _ in E:
                deg[u] = deg.get(u, 0) + 1
                deg[v] = deg.get(v, 0) + 1
            bad = {n for n, dg in deg.items() if dg == 1 and n not in Y}
            if not bad:
                break
            E = [e for e in E if e[0] not in bad and e[1] not in bad]
        E = suppress_degree2(E, Y)
        out.append(E)
    return out


def quartet_of_tree(E, Y):
    """the non-trivial split of a 4-leaf tree given by its edge list"""
    Y = list(Y)
    nodes = set()
    for u, v, _ in E:
        nodes.add(u); nodes.add(v)
    assert set(Y) <= nodes
    assert len(E) == len(nodes) - 1, "not a tree"
    res = None
    for k in range(len(E)):
        F = E[:k] + E[k + 1:]
        adj = {}
        for u, v, _ in F:
            adj.setdefault(u, []).append(v)
            adj.setdefault(v, []).append(u)
        comp, stack = {E[k][0]}, [E[k][0]]
        while stack:
            x = stack.pop()
            for y in adj.get(x, []):
                if y not in comp:
                    comp.add(y)
                    stack.append(y)
        side = frozenset(l for l in Y if l in comp)
        if len(side) == 2:
            res = frozenset((side, frozenset(Y) - side))
    assert res is not None, "unresolved quartet tree"
    return res


def quartets_via_quarnet(net, Y):
    sub = subnetwork(net, Y)
    return {quartet_of_tree(E, Y) for E in displayed_trees_mixed(sub, Y)}, sub
