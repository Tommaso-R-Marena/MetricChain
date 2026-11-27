# c2_survey_sym.py -- REVIEW 6: the re-enumeration of c1_survey.py up to the 12 rotations/reflections of the leaf
# labels, in chunks (parents with index = r mod M), so that k = 3 fits into short runs.  For every class: canonical
# KEY (min over the dihedral group of the marked unfolding), the INV refinements seen under that KEY, the orbit size
# (number of distinct KEYs of the 12 relabellings) and the split system.
# Usage: python3 c2_survey_sym.py K r M      -- extends level K-1 (file level_{K-1}.pkl) by one insertion; writes chunk file
#        python3 c2_survey_sym.py merge K M  -- merges the chunks into level_K.pkl and prints the counts
#        python3 c2_survey_sym.py init       -- writes level_0.pkl
import sys, time, pickle, itertools
from c1_survey import (N, DIH, planar_rooted_trees, parents, topo_children_first, keys_of, inv_of, system_of,
                       wheel_planar, insertions, image_system)


def canon(net, root, order, par):
    ks = [keys_of(net, root, order, g)[root] for g in DIH]
    kmin = min(ks)
    orbit = len(set(ks))
    iv = min(inv_of(net, root, order, par, g) for g, k in zip(DIH, ks) if k == kmin)
    return kmin, iv, orbit


if sys.argv[1] == "init":
    level = {}
    for net, root in planar_rooted_trees():
        order = topo_children_first(net, root)
        par = parents(net)
        k, iv, orb = canon(net, root, order, par)
        level[k] = (net, root, {iv}, orb, system_of(net, root, order, par))
    pickle.dump(level, open("level_0.pkl", "wb"))
    print("k=0: classes", len(level), "labelled", sum(v[3] for v in level.values()))
elif sys.argv[1] == "merge":
    K, M = int(sys.argv[2]), int(sys.argv[3])
    level = {}
    for r in range(M):
        part = pickle.load(open(f"chunk_{K}_{r}_{M}.pkl", "rb"))
        for k, (net, root, ivs, orb, s) in part.items():
            if k in level:
                level[k][2].update(ivs)
            else:
                level[k] = (net, root, set(ivs), orb, s)
    pickle.dump(level, open(f"level_{K}.pkl", "wb"))
    ninv = sum(len(v[2]) for v in level.values())
    multi = sum(1 for v in level.values() if len(v[2]) > 1)
    systems = set()
    for k, (net, root, ivs, orb, s) in level.items():
        for g in DIH:
            systems.add(image_system(s, g))
    print(f"k={K}: classes by KEY {len(level)}, by INV {ninv} (KEYs carrying several INVs: {multi}); "
          f"labelled by KEY (sum of orbit sizes) {sum(v[3] for v in level.values())}; systems at this level {len(systems)}")
    pickle.dump(systems, open(f"systems_level_{K}.pkl", "wb"))
else:
    K, r, M = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    t0 = time.time()
    prev = pickle.load(open(f"level_{K-1}.pkl", "rb"))
    out = {}
    nonplanar = set()
    for idx, (key, (net, root, _, _, _)) in enumerate(sorted(prev.items())):
        if idx % M != r:
            continue
        order0 = topo_children_first(net, root)
        for new in insertions(net, root, order0):
            order = topo_children_first(new, root)
            par = parents(new)
            kk, iv, orb = canon(new, root, order, par)
            if iv in nonplanar:
                continue
            if kk in out and iv in out[kk][2]:
                continue
            s = system_of(new, root, order, par)
            if s is None or not wheel_planar(new):
                nonplanar.add(iv)
                continue
            if kk in out:
                out[kk][2].add(iv)
            else:
                out[kk] = (new, root, {iv}, orb, s)
    pickle.dump(out, open(f"chunk_{K}_{r}_{M}.pkl", "wb"))
    print(f"chunk {r}/{M} of level {K}: {len(out)} classes, {time.time()-t0:.0f}s")
