# myblob.py -- REVIEWER'S OWN CODE: blob structure of an explicit rooted network, read off the graph,
# and the check of Theorem 12 (a), (b) of NANUQ_LOCAL_CRITERION.md on that network.
# Nothing is imported from the repository under review.
import itertools
import networkx as nx
from mynet import Net, alphas, split_mask_of


def blob_report(net):
    """For every non-trivial blob: dict with hybrids, kind, and for blobs with two hybrid nodes the
    theta structure read from the graph.  Returns list of dicts.  Raises AssertionError when a
    structural claim of 'Blobs, positions, sizes' / Lemma C fails (these are collected by callers)."""
    G = net.ugraph()
    cut = net.cut_edges()
    L = net.leaves
    lidx = {x: i for i, x in enumerate(L)}
    out = []
    hybset = set(net.hyb)
    for B in net.blobs():
        rep = {'nodes': B, 'hyb': sorted(B & hybset, key=str)}
        # blob edges (with multiplicity) at each node
        bdeg = {}
        bedges = []
        for u in B:
            for k, v in enumerate(net.ch[u]):
                if frozenset((u, v)) not in cut:
                    assert v in B
                    bedges.append((u, v, k))
                    bdeg[u] = bdeg.get(u, 0) + 1
                    bdeg[v] = bdeg.get(v, 0) + 1
        rep['bdeg'] = bdeg
        # sources: nodes of the blob without a parent in the blob
        src = [v for v in B if not any((p in B and frozenset((p, v)) not in cut) for p in net.par[v])]
        rep['sources'] = src
        # positions = nodes with exactly two blob edges and one cut edge ; pendant leaf sets
        pos = {}
        for v in B:
            cuts = [w for w in list(net.ch[v]) + list(net.par[v]) if frozenset((v, w)) in cut]
            if bdeg[v] == 2 and len(cuts) == 1:
                w = cuts[0]
                H = nx.Graph(G)
                H.remove_edge(v, w)
                comp = nx.node_connected_component(H, w)
                m = 0
                for x in comp:
                    if x in lidx:
                        m |= 1 << lidx[x]
                pos[v] = m
            else:
                # either a branch node (3 blob edges) or the root (2 blob edges, no further edge)
                assert (bdeg[v] == 3 and not cuts) or (v == net.root and bdeg[v] == 2 and not cuts), \
                    ("node of blob neither position nor branch node nor root", v)
        rep['pos'] = pos
        nh = len(rep['hyb'])
        rep['kind'] = 'level%d' % nh
        if nh == 2:
            branch = [v for v in B if bdeg[v] == 3]
            assert len(branch) == 2, ("theta graph expected", branch)
            hb = [h for h in rep['hyb'] if h in branch]
            # galled by Def 2.3(vi) restricted to this blob
            gal = blob_galled(net, B, cut)
            rep['galled'] = gal
            if len(hb) == 0:
                rep['kind'] = 'galled2'
                assert gal, "both hybrids interior but blob not galled"
                # Lemma C(1): on different paths -- checked via gal
            else:
                assert len(hb) == 1, "both hybrid nodes at branch nodes (Lemma C case 4 should be impossible)"
                assert not gal, "hybrid at a branch node but blob galled"
                rep['kind'] = 'nested'
                h1 = hb[0]
                h2 = [h for h in rep['hyb'] if h != h1][0]
                t = [v for v in branch if v != h1][0]
                # the three paths from h1 to t, as lists of interior nodes in order from h1
                def walk(first_edge):
                    # first_edge: (u, v, k) incident to h1
                    path = []
                    prev_edge = first_edge
                    cur = first_edge[0] if first_edge[1] == h1 else first_edge[1]
                    while cur != t:
                        assert bdeg[cur] == 2
                        path.append(cur)
                        inc = [e for e in bedges if (e[0] == cur or e[1] == cur) and e != prev_edge]
                        assert len(inc) == 1
                        prev_edge = inc[0]
                        cur = inc[0][0] if inc[0][1] == cur else inc[0][1]
                    return path
                inc_h1 = [e for e in bedges if e[0] == h1 or e[1] == h1]
                assert len(inc_h1) == 3
                out_e = [e for e in inc_h1 if e[0] == h1]
                in_e = [e for e in inc_h1 if e[1] == h1]
                assert len(out_e) == 1 and len(in_e) == 2
                C = walk(out_e[0])
                P1 = walk(in_e[0])
                P2 = walk(in_e[1])
                assert h2 in C, "h2 not on the path leaving h1 (Lemma C case 3)"
                pos1 = [v for v in P1 if v in pos]
                pos2 = [v for v in P2 if v in pos]
                rep['AB_both_have_positions'] = bool(pos1) and bool(pos2)
                if pos1 and not pos2:
                    Bpath = pos1
                elif pos2 and not pos1:
                    Bpath = pos2
                elif not pos1 and not pos2:
                    Bpath = []
                else:
                    Bpath = None
                i2 = C.index(h2)
                xs = [v for v in C[:i2] if v in pos]
                cs = [v for v in C[i2 + 1:] if v in pos]
                assert h2 in pos
                # the source: on A, on B, or on C between h2 and t
                assert len(src) == 1
                s = src[0]
                assert s in P1 or s in P2 or s in C[i2 + 1:], "source at a forbidden place"
                rep.update(h1=h1, h2=h2, t=t, B=Bpath, xs=xs, cs=cs, y=h2, source=s)
                if Bpath is not None:
                    rep['k'] = (len(Bpath), len(xs), len(cs))
                    rep['beta'] = [bin(pos[v]).count('1') for v in Bpath]
                    rep['xi'] = [bin(pos[v]).count('1') for v in xs]
                    rep['eta'] = bin(pos[h2]).count('1')
                    rep['gamma'] = [bin(pos[v]).count('1') for v in cs]
                    crit = pos[h2]
                    for v in xs:
                        crit |= pos[v]
                    rep['crit_mask'] = crit
                    rep['order_blocks'] = [pos[v] for v in Bpath] + [pos[v] for v in reversed(cs)] + [pos[h2]] + \
                                          [pos[v] for v in reversed(xs)]
        out.append(rep)
    return out


def blob_galled(net, B, cut):
    hyb_edges = set()
    for h in net.hyb:
        for p in net.par[h]:
            hyb_edges.add((p, h))
    for h in net.hyb:
        if h not in B:
            continue
        p1, p2 = net.par[h]
        if p1 == p2:
            continue
        G = nx.Graph()
        G.add_nodes_from(net.nodes)
        for u in net.nodes:
            for v in net.ch[u]:
                if (u, v) not in hyb_edges:
                    G.add_edge(u, v)
        G.remove_node(h)
        if not nx.has_path(G, p1, p2):
            return False
    return True


def formula12b(beta, xi, eta, gamma):
    """Theorem 12(b): alpha(S*) = beta_1*G + xi_1*R - e_2(beta_j : j in M)"""
    kB, k1, k2 = len(beta), len(xi), len(gamma)
    assert k1 >= 1 and kB >= 2
    R = eta + sum(xi[1:])
    if k2 >= 1:
        Gv = sum(gamma)
        M = beta[1:]
    else:
        Gv = beta[-1]
        M = beta[1:-1]
    e2 = sum(a * b for a, b in itertools.combinations(M, 2))
    return beta[0] * Gv + xi[0] * R - e2


def check_theorem12(net, order=None, reps=None, M6=None):
    """returns dict with the list of violations of Theorem 12 (a),(b) for this network and info.
    order: list of leaves (an induced circular order); default: one from a planar embedding."""
    L = net.leaves
    n = len(L)
    if order is None:
        order = net.circular_order()
        assert order is not None
    P = [L.index(x) for x in order]
    if M6 is None:
        M6 = net.nanuq6()
    al = alphas(M6, P)
    ds = net.displayed_splits()
    full = (1 << n) - 1
    if reps is None:
        reps = blob_report(net)
    crit = {}
    info = {'nested': [], 'viol': [], 'ncrit': 0, 'crit_values': []}
    for r in reps:
        if r['kind'] == 'nested':
            if r['B'] is None:
                info['viol'].append(('A and B both have positions in a planar network', r['h1']))
                continue
            kB, k1, k2 = r['k']
            info['nested'].append(r['k'])
            if k1 >= 1 and kB >= 2:
                m = r['crit_mask']
                if m & 1:
                    m = full ^ m
                val = formula12b(r['beta'], r['xi'], r['eta'], r['gamma'])
                if m in crit:
                    info['viol'].append(('two nested blobs with the same critical split', m))
                crit[m] = val
            # order of the pendant blocks around the circle (claim of the note)
            blocks = r['order_blocks']
            if not blocks_in_circular_order(blocks, P, n):
                info['viol'].append(('circular order of positions differs from the note', r['k']))
    seen_masks = set()
    for (i, j), a in al.items():
        m = split_mask_of(P, i, j, n)
        seen_masks.add(m)
        if m in crit:
            info['ncrit'] += 1
            info['crit_values'].append(crit[m])
            if a != 6 * crit[m]:
                info['viol'].append(('12(b) formula', (i, j), a / 6, crit[m]))
        else:
            if a < 0:
                info['viol'].append(('12(a) negative non-critical split', (i, j), a / 6, m in ds))
            elif (a > 0) != (m in ds):
                info['viol'].append(('12(a) support', (i, j), a / 6, m in ds))
    for m in ds:
        if m not in seen_masks:
            info['viol'].append(('displayed split not circular for the order', m))
    for m in crit:
        if m not in seen_masks:
            info['viol'].append(('critical split not circular', m))
        if m not in ds:
            info['viol'].append(('critical split not displayed', m))
    info['alpha'] = al
    info['order'] = order
    return info


def blocks_in_circular_order(blocks, P, n):
    """blocks: list of leaf bitmasks (matrix indices); P: circular order as matrix indices.
    True iff each block is an interval of the circular order and the blocks occur in the given
    cyclic order or its reverse."""
    where = {}
    for k, m in enumerate(blocks):
        for i in range(n):
            if (m >> i) & 1:
                where[i] = k
    seq = [where[p] for p in P]
    # compress consecutive repeats cyclically
    comp = [seq[i] for i in range(n) if seq[i] != seq[i - 1]]
    if len(comp) == 0:
        comp = [seq[0]]
    K = len(blocks)
    if len(comp) != K:
        return False
    s = comp.index(0)
    rot = comp[s:] + comp[:s]
    return rot == list(range(K)) or rot == [0] + list(range(K - 1, 0, -1))
