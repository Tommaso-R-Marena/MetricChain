"""R7 OWN checker of the engineering division's lattice covers, taken AS CERTIFICATES.

Inputs (engineering branch research/ubuntu-engineering, commit a2f6dc7; re-create with make_eng_copy.sh):
  experiments/eng/chain_cover/data/dia_Sc12_n{1..24}.txt   class tables (h3 h8 h11 | count | gmin | count_gmin | gmax)
  experiments/eng/chain_cover/results/lattice_Sc12.json     per cell: N_cov, centres_hist (the primal cover), bounds

What is checked here with my own code (no engineering code is imported):
  PRIMAL  every stored cover (list of centre classes) covers every class of the table:
            L * ||N^a - N^c||_1 <= gmin(c) + eps      in exact integer arithmetic;
          and its size equals the published N_cov.
  DUAL    a lower bound that does not depend on solver tolerances: the dual of the covering LP is solved
          in floating point (HiGHS), the weights are truncated to integers, the maximal centre load is
          computed in exact integer arithmetic on the full (unreduced) boolean matrix, and
          ceil(total / max load) is a valid lower bound whatever the LP solver did.
  The profile distance is derived from the definition (P_REPORT section 0), not copied:
    N(s) = #{pairs with s_pq <= s}, s in [0,12): N = C1 on [3,8), C2 on [8,11), C3 on [11,12), with
    C1 = h3, C2 = h3+h8, C3 = h3+h8+h11  =>  ||N^a - N^c||_1 = 5|dC1| + 3|dC2| + 1|dC3|.

Usage: python3 own_lattice_cert.py primal            # all 288 cells
       python3 own_lattice_cert.py dual NMIN NMAX     # certified LP bounds
"""
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

ENG = Path(__file__).resolve().parent / "eng_copy" / "experiments" / "eng" / "chain_cover"


def read_table(n):
    hist, count, gmin = [], [], []
    dist = None
    for line in (ENG / "data" / f"dia_Sc12_n{n}.txt").read_text().splitlines():
        if line.startswith("# distances"):
            dist = [int(t) for t in line.split()[2:]]
        if line.startswith("#") or not line.strip():
            continue
        v = [int(t) for t in line.split()]
        hist.append(v[:3]); count.append(v[3]); gmin.append(v[4])
    assert dist == [3, 8, 11]
    return np.array(hist, dtype=np.int64), count, np.array(gmin, dtype=np.int64)


def l1_matrix(hist):
    C = np.cumsum(hist, axis=1)
    w = (5, 3, 1)                      # widths of [3,8), [8,11), [11,12)
    D = np.zeros((len(C), len(C)), dtype=np.int64)
    for k in range(3):
        D += w[k] * np.abs(C[:, k][:, None] - C[:, k][None, :])
    return D


def parse_key(key, N):
    """'L=1/5,eps=1/4*N' -> (Fraction L, Fraction eps)."""
    ls, es = key.split(",")
    L = Fraction(ls.split("=")[1])
    e = es.split("=")[1]
    eps = Fraction(e[:-2]) * N if e.endswith("*N") else Fraction(e)
    return L, eps


def cover_matrix(D, gmin, L, eps):
    """M[a,c] = (L*D[a,c] <= gmin[c] + eps), exact: multiply by the common denominator."""
    den = L.denominator * eps.denominator
    lhs = (L.numerator * (den // L.denominator)) * D
    rhs = den * gmin + eps.numerator * (den // eps.denominator)
    assert int(np.abs(lhs).max()) < 2 ** 62
    return lhs <= rhs[None, :]


def certified_lb(M, den=1 << 30):
    """Tolerance-free lower bound on the minimum cover of boolean M (rows = centres, cols = classes)."""
    from scipy.optimize import linprog
    from scipy.sparse import csr_matrix
    C = M.shape[1]
    # dual LP: max sum w  s.t. for every centre a: sum_{c covered by a} w_c <= 1, w >= 0
    res = linprog(c=-np.ones(C), A_ub=csr_matrix(M.astype(np.float64)), b_ub=np.ones(M.shape[0]),
                  bounds=(0, None), method="highs")
    w = np.maximum(res.x, 0.0)
    wi = np.floor(w * den).astype(np.int64)             # integers
    load = M.astype(np.int64) @ wi                      # exact (values < 2^30 * 5000 < 2^63)
    mx, tot = int(load.max()), int(wi.sum())
    lb = Fraction(tot, mx) if mx > 0 else Fraction(0)
    return math.ceil(lb), float(-res.fun), lb


def main():
    mode = sys.argv[1]
    res = json.loads((ENG / "results" / "lattice_Sc12.json").read_text())
    rows = {r["n_torsions"]: r for r in res["rows"]}
    out = []
    if mode == "primal":
        bad = 0
        ncell = 0
        for n in sorted(rows):
            hist, count, gmin = read_table(n)
            N = n + 3
            # header consistency
            assert sum(count) == rows[n]["conformations"] and len(hist) == rows[n]["classes"], (n, sum(count), len(hist))
            index = {tuple(h): i for i, h in enumerate(hist.tolist())}
            D = l1_matrix(hist)
            for key, cell in rows[n]["cover"].items():
                L, eps = parse_key(key, N)
                M = cover_matrix(D, gmin, L, eps)
                centres = [index[tuple(h)] for h in cell["centres_hist"]]
                ok_cover = bool(M[centres].any(axis=0).all())
                ok_size = (len(centres) == cell["N_cov"]) and (len(set(centres)) == len(centres))
                ncell += 1
                if not (ok_cover and ok_size):
                    bad += 1
                    print("PRIMAL FAILURE", n, key, ok_cover, ok_size)
                out.append(dict(n=n, key=key, N_cov=cell["N_cov"], primal_ok=ok_cover and ok_size))
        print(f"primal certificates checked: {ncell} cells, failures: {bad}")
        json.dump(out, open("out_own_lattice_primal.json", "w"), indent=0)
    elif mode == "dual":
        nmin, nmax = int(sys.argv[2]), int(sys.argv[3])
        for n in range(nmin, nmax + 1):
            hist, count, gmin = read_table(n)
            N = n + 3
            D = l1_matrix(hist)
            for key, cell in rows[n]["cover"].items():
                t0 = time.time()
                L, eps = parse_key(key, N)
                M = cover_matrix(D, gmin, L, eps)
                lb, lp, frac = certified_lb(M)
                rec = dict(n=n, key=key, N_cov=cell["N_cov"], own_certified_lb=lb, own_lp=lp,
                           eng_lower_certified=cell.get("lower_certified"), eng_lower_solver=cell.get("lower_solver"),
                           eng_proved=cell["proved_optimal"], eng_lp=cell["lp_bound"],
                           certified_optimal=(lb == cell["N_cov"]), seconds=round(time.time() - t0, 2))
                out.append(rec)
                flag = "" if rec["certified_optimal"] else ("  <-- gap %d" % (cell["N_cov"] - lb))
                if rec["eng_lower_certified"] is not None and rec["eng_lower_certified"] != lb:
                    flag += "  (eng certified %d)" % rec["eng_lower_certified"]
                print(f"n={n} {key}: N_cov={cell['N_cov']} ownLB={lb} LP={lp:.4f} engLP={cell['lp_bound']:.4f} "
                      f"engC={rec['eng_lower_certified']} engS={rec['eng_lower_solver']} proved={cell['proved_optimal']}{flag}",
                      flush=True)
            json.dump(out, open(f"out_own_lattice_dual_{nmin}_{nmax}.json", "w"), indent=0)


if __name__ == "__main__":
    main()
