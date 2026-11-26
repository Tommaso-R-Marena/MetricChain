import pickle, sys
from collections import Counter
import rnet
c = Counter()
for fn in sys.argv[1:]:
    for net, order, f, st in pickle.load(open(fn, "rb")):
        G, H, leaves = rnet.semi_directed(net)
        par = any(G.number_of_edges(u, v) > 1 for u, v in set((min(a, b), max(a, b)) for a, b in G.edges()))
        c["parallel edges in semi-directed network" if par else "simple"] += 1
        bl = rnet.blobs(net)
        br = rnet.bridges_multigraph(G)
        # blobs by number of articulation nodes
        for comp, k in bl:
            art = sum(1 for v in comp if any(v in e for e in br))
            c[f"blob with {min(art, 4)}{'+' if art >= 4 else ''} articulation nodes"] += 1
print(dict(sorted(c.items())))
