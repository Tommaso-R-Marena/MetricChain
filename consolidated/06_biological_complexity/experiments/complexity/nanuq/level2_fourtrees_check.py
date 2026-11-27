"""Cross-check of the four trees T_1..T_4 of the nested blob (section 7.2 of the NANUQ note):
for every bloblet N[kB, k1, k2] with at most MAXN leaves, the splits displayed by the EXPLICIT rooted network
(built by level2_explicit.Builder, evaluated by netcalc.py) are exactly the system Sigma[kB, k1, k2] of
level2_nongalled.py, and the network is outer-labeled planar, of level 2 (for kB + k1 + k2 >= 2 positions besides y),
and not galled.

Usage: python3 level2_fourtrees_check.py [MAXN]        (default 9)
"""
import random
import sys
from netcalc import validate, leaves_of, displayed_trees, tree_splits_from_clusters, outer_labeled_planar_order, \
    blobs_and_level, is_galled
from level2_explicit import Builder
from level2_nongalled import system, leaves as family_leaves
from splitsys import canon


class LeafOnly(Builder):
    def pendant(self, budget, depth):
        l = self.leaf()
        return l, [l]


if __name__ == "__main__":
    maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    ok, cnt = True, 0
    for tot in range(3, maxn):
        for kB in range(tot + 1):
            for k1 in range(tot - kB + 1):
                k2 = tot - kB - k1
                B = LeafOnly(random.Random(0))
                top, order = B.nested(kB, k1, k2, ("A",), tot + 1, 0)
                net = B.net
                validate(net)
                L = leaves_of(net)
                n = len(L)
                # the explicit builder lists the leaves in the circular order b_1..b_kB, c_k2..c_1, y, x_k1..x_1,
                # which is the indexing 0..n-1 of level2_nongalled.system
                names, ix = family_leaves(kB, k1, k2)
                assert len(order) == n == len(names)
                pos = {leaf: q for q, leaf in enumerate(order)}
                explicit = set()
                for clusters in displayed_trees(net):
                    for cl in clusters:
                        if 0 < len(cl) < n:
                            m = 0
                            for leaf in cl:
                                m |= 1 << pos[leaf]
                            explicit.add(canon(n, m))
                nn, nm, sigma, trees = system(kB, k1, k2)
                cnt += 1
                good = explicit == set(sigma)
                good &= outer_labeled_planar_order(net) is not None
                comps, levels = blobs_and_level(net)
                good &= max(levels) == 2 and not is_galled(net)
                if not good:
                    print("MISMATCH", (kB, k1, k2), sorted(explicit ^ set(sigma)), levels, is_galled(net))
                ok &= good
    print(f"{cnt} bloblets N[kB,k1,k2] with 4..{maxn} leaves: the splits displayed by the explicit rooted network are"
          f" exactly Sigma[kB,k1,k2]; planar, level 2, not galled: {ok}")
