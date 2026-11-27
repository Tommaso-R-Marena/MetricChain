#!/usr/bin/env python3
"""R25, Item 1 -- transfer-matrix enumeration (LB of nn_model.py) on larger families; own code.

Usage: python3 -B t1c_dp.py "m,B;m,B;..." OUT.json [max_parts]

For every composition (ordered tuple of item sizes) of mB the DP returns the number of connected
unpseudoknotted structures for that circular order by signature (tiling, st, fl, nb, L, z, r).
The structural checks of the proof (counting identities, separator inequality) are tallied as in
t1c_levelA.py part2, with the same controls.  LB was compared with the generic enumerator LA on every
composition with mB <= 8 and on the family (3,3) (logs run02, run03).
max_parts (optional): only compositions with at most that many items (documented restriction of a family).
"""
import sys
import json
import time
from collections import Counter

import nn_model as nn
from t1c_levelA import structural_checks

TALLY_KEYS = ("structures", "structures_B>=2", "tilings", "viol_bond_count", "viol_nick_count",
              "viol_sep_ineq_B1", "viol_sep_ineq_B>=2", "ctrl_B>=2_sep_ineq_without_r",
              "ctrl_B>=2_sep_ineq_without_L", "ctrl_B>=2_sep_ineq_without_z",
              "viol_tiling_signature", "viol_tiling_iff_L0_nobulge", "B1_nontiling_structures")


def main():
    t0 = time.time()
    fams = [tuple(int(v) for v in f.split(",")) for f in sys.argv[1].split(";")]
    outname = sys.argv[2]
    max_parts = int(sys.argv[3]) if len(sys.argv) > 3 else None
    tally = Counter({k: 0 for k in TALLY_KEYS})
    dump = {}
    ncomp = 0
    for (m, B) in fams:
        fam_structs = 0
        fam_comp = 0
        for order in nn.compositions(m * B):
            if max_parts is not None and len(order) > max_parts:
                continue
            ncomp += 1
            fam_comp += 1
            cnt = nn.level_B(m, B, order)
            structural_checks(m, B, order, cnt, tally)
            fam_structs += sum(cnt.values())
            proj = Counter()
            for (til, st, fl, nb, L, z, r), w in cnt.items():
                proj[(til, st, fl, nb)] += w
            dump[f"{m},{B}|" + ",".join(map(str, order))] = [list(k) + [w] for k, w in sorted(proj.items())]
        print(f"  family m={m} B={B}: compositions {fam_comp}, connected structures {fam_structs}, "
              f"elapsed {time.time() - t0:.1f} s", flush=True)
    with open(outname, "w") as fh:
        json.dump(dump, fh)
    print(f"DP families (m,B): {fams}; max_parts {max_parts}; compositions (ordered instances) {ncomp}")
    for k in sorted(tally):
        print(f"DP {k}: {tally[k]}")
    print(f"DP wrote {outname}; time {time.time() - t0:.1f} s")


if __name__ == "__main__":
    nn.limit_memory(2.0)
    main()
    print(f"peak memory {nn.peak_mb():.1f} MB")
