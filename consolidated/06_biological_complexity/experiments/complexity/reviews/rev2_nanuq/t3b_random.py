"""Task 3(b): attempt to falsify Theorem 7 on galled outer-labeled planar networks produced by random hybrid
insertion and FILTERED by the actual tests (Def. 2.3(vi) galledness, planarity with an apex, LSA).

usage: python3 t3b_random.py SEED NUM_ACCEPTED MODE OUTFILE
   MODE = 'step'  : rejection after each insertion (galled & outer-labeled planar must hold at each step)
   MODE = 'final' : no intermediate filter, only the final network is tested
"""
import sys, random, pickle, time
from collections import Counter
import rnet, gen


def accept(net):
    return rnet.is_galled_def(net) and rnet.planar_circular_order(net) is not None


def main():
    seed, target, mode, outfile = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
    rng = random.Random(seed)
    t0 = time.time()
    stats = Counter()
    by_class = Counter()
    failures = []
    nets = []
    crit_mismatch = 0
    tried = 0
    seen = set()
    while len(nets) < target:
        tried += 1
        n = rng.choice([6, 6, 7, 7, 8, 8, 9, 10])
        k = rng.choice([1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7])
        net = gen.grow(n, k, rng, per_step=(accept if mode == "step" else None))
        if net is None:
            stats["grow_failed"] += 1
            continue
        # definitions cross-check on EVERY generated network (galled or not)
        g1, g2, g3 = rnet.is_galled_def(net), rnet.is_galled_articulation(net), rnet.is_galled_ancestor(net)
        if not (g1 == g2 == g3):
            crit_mismatch += 1
            failures.append(("galled-criteria-mismatch", net, (g1, g2, g3)))
        if not g1:
            stats["rejected_not_galled"] += 1
            continue
        order = rnet.planar_circular_order(net)
        if order is None:
            stats["rejected_not_planar"] += 1
            continue
        if not rnet.is_lsa_network(net):
            stats["rejected_not_lsa"] += 1
            continue
        key = tuple(sorted((v, tuple(sorted(ch))) for v, ch in net.items()))
        if key in seen:
            stats["duplicate"] += 1
            continue
        seen.add(key)
        f = gen.features(net)
        st, det, sigma, nn = gen.check_fast(net, order)
        stats[st] += 1
        by_class[(f["n"], f["level"], f["nblobs"], f["nonleaf_hyb_children"] > 0)] += 1
        nets.append((net, order, f, st))
        if st != "ok":
            failures.append((st, net, det))
            print("FAILURE", st, det, net, flush=True)
    dt = time.time() - t0
    with open(outfile, "wb") as fh:
        pickle.dump(nets, fh)
    print(f"seed={seed} mode={mode}: generated {tried}, accepted (galled, OLP, LSA, distinct) {len(nets)} in {dt:.0f}s")
    print("   stats:", dict(stats))
    print("   galled-criteria mismatches (Def 2.3(vi) vs articulation vs ancestor), over all generated:", crit_mismatch)
    print("   failures of the theorem:", sum(1 for f in failures if f[0] != "galled-criteria-mismatch"))
    lv = Counter(); nb = Counter(); nl = Counter(); nn_ = Counter(); hy = Counter()
    for net, order, f, st in nets:
        lv[f["level"]] += 1; nb[f["nblobs"]] += 1; nn_[f["n"]] += 1; hy[f["hyb"]] += 1
        nl[f["nonleaf_hyb_children"]] += 1
    print("   by leaves:", dict(sorted(nn_.items())))
    print("   by #hybrids:", dict(sorted(hy.items())))
    print("   by level:", dict(sorted(lv.items())))
    print("   by #non-trivial blobs:", dict(sorted(nb.items())))
    print("   by #hybrids with non-leaf child:", dict(sorted(nl.items())))


if __name__ == "__main__":
    main()
