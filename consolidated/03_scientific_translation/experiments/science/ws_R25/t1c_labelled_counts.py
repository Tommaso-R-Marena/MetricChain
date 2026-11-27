#!/usr/bin/env python3
"""R25 -- number of connected unpseudoknotted structures per instance with ALL strands labelled, from the
signature files (own code).  Usage: python3 -B t1c_labelled_counts.py N1 N2 ... -- SIG.json [SIG.json ...]
Prints every instance (multiset a, m, B) whose labelled count equals one of the given numbers N_i, and the
largest labelled counts.  Purpose: comparison with the two per-instance counts quoted in section 6 of the note
(1 887 888 and 762 294), which is the only numerical output of their enumerators visible to this workstream."""
import sys
import json
from math import factorial
from collections import defaultdict

import nn_model as nn


def main():
    k = sys.argv.index("--")
    targets = [int(v) for v in sys.argv[1:k]]
    lab = defaultdict(int)
    for fn in sys.argv[k + 1:]:
        with open(fn) as fh:
            d = json.load(fh)
        for key, rows in d.items():
            mb, od = key.split("|")
            m, B = (int(v) for v in mb.split(","))
            order = tuple(int(v) for v in od.split(","))
            mult = 1
            for s in set(order):
                mult *= factorial(order.count(s))
            lab[(m, B, tuple(sorted(order)))] += mult * sum(r[-1] for r in rows)
    print(f"instances: {len(lab)}")
    for t in targets:
        hits = sorted(kk for kk, v in lab.items() if v == t)
        print(f"labelled count {t}: {len(hits)} instance(s): {hits}")
    small = sorted(((v, kk) for kk, v in lab.items() if 2 <= kk[0] <= 3 and 3 <= kk[1] <= 5), reverse=True)[:6]
    print("largest labelled counts among instances with 2 <= m <= 3, 3 <= B <= 5: "
          + "; ".join(f"{v} for a={kk[2]}, m={kk[0]}, B={kk[1]}" for v, kk in small))


if __name__ == "__main__":
    nn.limit_memory(2.0)
    main()
    print(f"peak memory {nn.peak_mb():.1f} MB")
