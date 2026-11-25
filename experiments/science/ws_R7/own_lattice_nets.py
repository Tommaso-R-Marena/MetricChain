"""R7 OWN check of the entropy table of ENG-RES-0002 section 4 (internal covering numbers of the lattice profile set at
closed radius delta*N, normalised metric ||N^x - N^y||_1 / N).

For each n and delta: boolean matrix M[a,c] = (D[a,c] <= delta*N) in exact integers; my greedy cover (verified) and my
tolerance-free LP-duality bound.  CONSISTENCY with the published bracket [lo, hi]:
   my certified lower bound must be <= hi   and   my verified cover must be >= lo,
otherwise one of the two is wrong.  Where the published value is a single number and my certified bound equals it,
optimality is certified without trusting branch and bound.  Optionally (TIME_LIMIT > 0) HiGHS is run on the cells
that remain open.
   python3 own_lattice_nets.py TIME_LIMIT n [n ...]
"""
import json, sys, time
from fractions import Fraction
import numpy as np
import own_lattice_cert as lc
import own_cover as oc
import own_lattice_opt as lo

DELTAS = {"delta=4": Fraction(4), "delta=2": Fraction(2), "delta=1": Fraction(1), "delta=1/2": Fraction(1, 2), "delta=1/4": Fraction(1, 4)}

if __name__ == "__main__":
    tl = float(sys.argv[1])
    res = json.loads((lc.ENG / "results" / "lattice_Sc12.json").read_text())
    rows = {r["n_torsions"]: r for r in res["rows"]}
    out = []
    for n in [int(a) for a in sys.argv[2:]]:
        hist, count, gmin = lc.read_table(n)
        D = lc.l1_matrix(hist)
        N = n + 3
        for key, d in DELTAS.items():
            e = rows[n]["entropy"][key]
            pub = e.get("net_closed_radius")
            r = d * N
            M = (D * r.denominator) <= r.numerator
            g = len(oc.greedy_cover(M))
            lb, lp, _ = lc.certified_lb(M)
            rec = dict(n=n, key=key, own_greedy=g, own_certified_lb=lb, own_lp=lp, published=pub, m_fpt=e.get("m_fpt"))
            if pub is not None:
                rec["consistent"] = bool(lb <= pub["upper"] and g >= pub["lower"])
                rec["published_lower_is_certified_here"] = bool(lb >= pub["lower"])
                if tl > 0 and lb < pub["lower"]:
                    t1 = time.time(); rec["highs"] = lo.highs_cover(M, tl); rec["highs"]["seconds"] = round(time.time() - t1, 1)
            out.append(rec)
            print(rec, flush=True)
        json.dump(out, open("out_own_lattice_nets.json", "w"), indent=1)
