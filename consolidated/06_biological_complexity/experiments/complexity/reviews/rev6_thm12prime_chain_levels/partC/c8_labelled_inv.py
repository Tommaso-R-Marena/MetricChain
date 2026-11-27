# c8_labelled_inv.py -- REVIEW 6: number of LABELLED networks with three hybrid nodes when networks are separated by the
# refined invariant INV instead of the unfolding KEY (sum of orbit sizes under the 12 relabellings).  Chunked.
# Usage: python3 c8_labelled_inv.py r M   |   python3 c8_labelled_inv.py merge M
import sys, pickle
from c1_survey import (DIH, parents, topo_children_first, keys_of, inv_of, system_of, wheel_planar, insertions)

if sys.argv[1] == "merge":
    M = int(sys.argv[2])
    allc = {}
    for r in range(M):
        allc.update(pickle.load(open(f"lab_{r}_{M}.pkl", "rb")))
    keys = {k for (k, iv) in allc}
    print(f"k=3: classes up to rotation/reflection by KEY {len(keys)}, by (KEY,INV) {len(allc)}; "
          f"labelled networks by (KEY,INV) = sum of orbit sizes = {sum(allc.values())}  (by KEY alone the survey counts 1151442)")
else:
    r, M = int(sys.argv[1]), int(sys.argv[2])
    prev = pickle.load(open("level_2.pkl", "rb"))
    out, nonplanar = {}, set()
    for idx, (key, (net, root, _, _, _)) in enumerate(sorted(prev.items())):
        if idx % M != r:
            continue
        order0 = topo_children_first(net, root)
        for new in insertions(net, root, order0):
            order = topo_children_first(new, root)
            par = parents(new)
            ks = [keys_of(new, root, order, g)[root] for g in DIH]
            kmin = min(ks)
            iv = min(inv_of(new, root, order, par, g) for g, k in zip(DIH, ks) if k == kmin)
            if iv in nonplanar or iv in out:
                continue
            s = system_of(new, root, order, par)
            if s is None or not wheel_planar(new):
                nonplanar.add(iv)
                continue
            out[iv] = len({inv_of(new, root, order, par, g) for g in DIH})
    pickle.dump(out, open(f"lab_{r}_{M}.pkl", "wb"))
    print("chunk", r, "done", len(out))
