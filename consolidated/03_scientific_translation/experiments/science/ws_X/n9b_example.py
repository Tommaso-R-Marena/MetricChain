"""N9b — a small explicit instance with 0 < tau_LP < tau (LP tight for f itself, but the LP
funnel slope strictly below the integer funnel slope).  Exhaustive over triangles with
half-integer fields in [-4,4] and J = +-1; if none, over 4-site graphs (4-cycle with one chord)
with integer fields in [-3,3]."""
import itertools
import json

import numpy as np

from n9_lp_funnel import energies, tau_integer, tau_lp


def search(n, edges, field_vals, Jvals):
    best = None
    c = np.ones(n)
    for Js in itertools.product(Jvals, repeat=len(edges)):
        for hs in itertools.product(field_vals, repeat=n):
            h, J = np.array(hs, dtype=float), np.array(Js, dtype=float)
            E, _ = energies(n, h, edges, J)
            srt = np.sort(E)
            if srt[1] - srt[0] < 1e-9:
                continue
            xs, tau, droplet = tau_integer(n, E, c)
            tlp, st = tau_lp(n, h, edges, J, c, xs)
            if st == 0 and tlp > 1e-6 and tau - tlp > 1e-6:
                gap = (tau - tlp) / tau
                if best is None or gap > best["rel_gap"] + 1e-9:
                    best = {"rel_gap": gap, "h": hs, "J": Js, "edges": edges, "tau": tau,
                            "tau_LP": tlp, "xstar": xs, "worst_droplet_size": droplet}
    return best


if __name__ == "__main__":
    out = {}
    out["triangle"] = search(3, [(0, 1), (1, 2), (0, 2)], [x / 2 for x in range(-8, 9)], (-1.0, 1.0))
    print("triangle:", out["triangle"])
    out["4cycle+chord"] = search(4, [(0, 1), (1, 2), (2, 3), (0, 3), (0, 2)], list(range(-3, 4)), (-1.0, 1.0))
    print("4-cycle with chord:", out["4cycle+chord"])
    json.dump(out, open("n9b_example.json", "w"), indent=1)
