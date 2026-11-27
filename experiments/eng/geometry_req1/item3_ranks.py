"""GEOMETRY-REQ-0001, item 3: independent replication of the exact witnesses of Theorems C(b)
and H of docs/geometry/ENSEMBLE_RIGIDITY.md (Geometric Inference division, commit d84a43b), for
K = 2, 3, 4 states, unit bonds, bond-angle cosine -5/13.

Run from the repository root:

    python experiments/eng/geometry_req1/item3_ranks.py          # about 1 min with python-flint

Output: experiments/eng/geometry_req1/results/item3_ranks.json

Arithmetic: every matrix entry is an exact rational (fractions.Fraction); every rank is the rank
OVER Q, computed exactly on the row-scaled integer matrix (FLINT fmpz_mat.rank when python-flint is
installed, fraction-free Bareiss elimination in pure Python otherwise).  As a cross-check each rank
is recomputed modulo the prime 2^61 - 1 (rank_p <= rank_Q).

Definitions as implemented here (ours; written from the report, not from their scripts):

(a) CONIC SYSTEM.  For K chains with n atoms let z_i = (x_i^(1), ..., x_i^(K)) in Q^{3K} be the
    unweighted stacked configuration.  The conic matrix has one row for each of the 2n-3
    constrained edge vectors e (n-1 bonds z_{i+1}-z_i, n-2 one-three vectors z_{i+2}-z_i) and one
    column for each pair i <= j <= 3K; the entry is the coefficient of S_ij in e^T S e
    (e_i^2 if i = j, 2 e_i e_j otherwise).  Its kernel is N(z); the K-1 trivial quadrics
    sum_k s_k E_k, sum_k s_k = 0 (in unweighted coordinates) are always in the kernel, so
    rank <= D_K = 3K(3K+1)/2 - (K-1) = (9K^2+K+2)/2.  Claim: rank = D_K at n_0 = ceil((9K^2+K+8)/4)
    and rank < D_K at n_0 - 1 (there 2n-3 < D_K).

(b) JACOBIAN.  Parameters: the K(n-3) torsions (we differentiate with respect to the half-angle
    tangents t; d(angle)/dt = 2/(1+t^2) != 0, so the rank is that of the Jacobian with respect to
    the angles) and the K-1 weights w_1..w_{K-1} (w_K = 1 - sum of the others).  Data: the averaged
    squared distances M_ij = sum_k w_k |x_i^(k) - x_j^(k)|^2 for the pairs ij of a set F.
    Columns: dM_ij/dt_m^(k) = w_k d|x_i^(k)-x_j^(k)|^2/dt_m (exact derivative of the rational
    chain map, by differentiating the bond recursion), dM_ij/dw_k = D(X_k)_ij - D(X_K)_ij.
    "Complete data": F = all pairs i < j (pairs at separation 1 and 2 give zero rows).
    "Separation w": F_w = {ij : 3 <= |i-j| <= w}.
    Claims: full column rank K(n-3)+K-1 for complete data at n = 2K+3 and for F_{K+3} at
    n = (K^2+3K+4)/2; column-rank deficiency for F_{K+2} (any n).

Witnesses: "eng" = ours (enslib.eng_witness_tangents, indices 0, 1, 2; weights proportional to
index+1, ..., index+K), "geometry" = the witnesses of their scripts for seeds 0..4, re-derived
here from the text of exact_conic_rank.py / exact_jacobian_rank.py (same Mersenne-twister calls;
their scripts accept the first seed in 0..4 that reaches the target rank modulo 2147483629, so we
also record the rank modulo that prime).
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import enslib as el  # noqa: E402

P61 = 2305843009213693951
PIN = "d84a43b"


# ------------------------------------------------------------------------------ derivatives
def chain_tangent_derivatives(tans, cos=el.COS, sin=el.SIN):
    """For the chain with half-angle tangents `tans`: the list over torsions m of the list over
    atoms j of d x_j / d t_m (exact).  Obtained by differentiating the bond recursion of
    enslib.chain_from_tangents:  u_i = -cos q + c_i (-cos q - p) + s_i (p x q),  p = u_{i-2},
    q = u_{i-1}, (c_i, s_i) the circle point of torsion i-2."""
    cos, sin = Fr(cos), Fr(sin)
    n = len(tans) + 3
    # bonds
    u = [(Fr(1), Fr(0), Fr(0)), (-cos, sin, Fr(0))]
    cs = []
    for t in tans:
        c, s = el.circle_point(t)
        cs.append((c, s))
        p, q = u[-2], u[-1]
        pq = el.cross(p, q)
        u.append(tuple(-cos * q[j] + c * (-cos * q[j] - p[j]) + s * pq[j] for j in range(3)))
    out = []
    zero = (Fr(0), Fr(0), Fr(0))
    for m, t in enumerate(tans):
        t = Fr(t)
        d = (1 + t * t) ** 2
        dc, ds = -4 * t / d, 2 * (1 - t * t) / d
        du = [zero] * (n - 1)
        i = m + 2
        p, q = u[i - 2], u[i - 1]
        pq = el.cross(p, q)
        du[i] = tuple(dc * (-cos * q[j] - p[j]) + ds * pq[j] for j in range(3))
        for i in range(m + 3, n - 1):
            c, s = cs[i - 2]
            p, q = u[i - 2], u[i - 1]
            dp, dq = du[i - 2], du[i - 1]
            a = el.cross(dp, q)
            b = el.cross(p, dq)
            du[i] = tuple(-cos * dq[j] + c * (-cos * dq[j] - dp[j]) + s * (a[j] + b[j]) for j in range(3))
        dx = [zero]
        for i in range(n - 1):
            dx.append(tuple(dx[-1][j] + du[i][j] for j in range(3)))
        out.append(dx)
    return out


def jacobian(tangents, weights, pairs):
    """Jacobian of (tangents, w_1..w_{K-1}) -> (M_ij)_{ij in pairs}; rows = pairs."""
    K = len(tangents)
    chains = [el.chain_from_tangents(t) for t in tangents]
    ders = [chain_tangent_derivatives(t) for t in tangents]
    rows = []
    for (i, j) in pairs:
        row = []
        for k in range(K):
            x = chains[k]
            diff = tuple(x[j][c] - x[i][c] for c in range(3))
            for dx in ders[k]:
                dd = tuple(dx[j][c] - dx[i][c] for c in range(3))
                row.append(2 * weights[k] * el.dot(diff, dd))
        dK = sum((chains[K - 1][j][c] - chains[K - 1][i][c]) ** 2 for c in range(3))
        for k in range(K - 1):
            dk = sum((chains[k][j][c] - chains[k][i][c]) ** 2 for c in range(3))
            row.append(dk - dK)
        rows.append(row)
    return rows


def all_pairs(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def band_pairs(n, w):
    return [(i, j) for i in range(n) for j in range(i + 3, min(n, i + w + 1))]


# ------------------------------------------------------------------------------ witnesses
def eng_weights(K, index):
    raw = [k + 1 + index for k in range(K)]
    return [Fr(x, sum(raw)) for x in raw]


def geometry_jacobian_witness(K, n, seed):
    """Tangents and weights of `jacobian(K, n, pairs, "rational", seed)` in their
    exact_jacobian_rank.py, re-derived: the tangents as in exact_conic_rank.py, then K integers
    randint(1, 9), normalised to sum 1."""
    rnd = random.Random(seed)
    tans = [[Fr(rnd.randint(-9, 9), rnd.randint(1, 9)) for _ in range(n - 3)] for _ in range(K)]
    raw = [rnd.randint(1, 9) for _ in range(K)]
    return tans, [Fr(x, sum(raw)) for x in raw]


P_GEOMETRY = 2147483629      # the prime of their scripts for the "rational" bond geometry


def ranks(rows):
    """(rank over Q, rank mod 2^61-1, rank mod the prime 2147483629 used by their scripts)."""
    return el.rank_exact(rows), el.rank_mod_p(rows, P61), el.rank_mod_p(rows, P_GEOMETRY)


def main():
    t_start = time.time()
    out = {"request": "GEOMETRY-REQ-0001 item 3", "geometry_commit": PIN,
           "arithmetic": "entries exact rationals; ranks over Q (%s); cross-checks modulo 2^61-1 "
                         "and modulo 2147483629" % ("FLINT fmpz_mat.rank" if el.HAVE_FLINT
                                                     else "pure-Python Bareiss"),
           "conic": [], "jacobian_complete": [], "jacobian_band": [], "summary": []}
    eng_idx, geo_idx = (0, 1, 2), (0, 1, 2, 3, 4)

    def summarise(kind, K, n, extra, target, recs, expect_full):
        """One summary line per claim: our witnesses, their seeds 0..4 (their script accepts the
        first seed that reaches the target)."""
        eng = [r for r in recs if r["witness"].startswith("eng")]
        geo = [r for r in recs if r["witness"].startswith("geometry")]
        first_seed = next((int(r["witness"].split("_")[1]) for r in geo if r["rank_mod_2147483629"] == target), None)
        s = {"claim": kind, "K": K, "n": n, **extra, "target": target,
             "eng_ranks_Q": [r["rank_Q"] for r in eng], "geometry_seed_ranks_Q": [r["rank_Q"] for r in geo],
             "first_geometry_seed_reaching_target_mod_2147483629": first_seed}
        if expect_full:
            s["confirmed"] = all(r["rank_Q"] == target for r in eng) and first_seed is not None
            s["witnesses_below_target"] = [r["witness"] for r in recs if r["rank_Q"] != target]
        else:
            s["confirmed"] = all(r["rank_Q"] < target for r in recs)
            s["max_rank_seen"] = max(r["rank_Q"] for r in recs)
        out["summary"].append(s)
        return s

    print("== (a) conic system: rank over Q; target D_K = (9K^2+K+2)/2 at n_0 = ceil((9K^2+K+8)/4)")
    for K in (2, 3, 4):
        DK = (9 * K * K + K + 2) // 2
        n0 = -(-(9 * K * K + K + 8) // 4)
        for n in (n0, n0 - 1):
            recs = []
            for label, fn, indices in (("eng", el.eng_witness_tangents, eng_idx),
                                       ("geometry", el.geometry_witness_tangents, geo_idx)):
                for idx in indices:
                    tans = fn(K, n, idx)
                    chains, z = el.ensemble(tans)
                    assert all(el.check_chain(c) for c in chains)
                    C = el.conic_matrix(z)
                    rq, rp, rg = ranks(C)
                    recs.append({"K": K, "n": n, "witness": "%s_%d" % (label, idx), "rows": len(C),
                                 "columns": len(C[0]), "target_D_K": DK, "rank_Q": rq,
                                 "rank_mod_2^61-1": rp, "rank_mod_2147483629": rg,
                                 "deficiency": DK - rq})
            out["conic"] += recs
            s = summarise("conic rank = D_K" if n == n0 else "conic rank < D_K", K, n,
                          {"rows": 2 * n - 3, "columns": 3 * K * (3 * K + 1) // 2}, DK, recs, n == n0)
            print(f"  K={K} n={n:2d} ({2 * n - 3} x {3 * K * (3 * K + 1) // 2}) D_K={DK}: eng ranks "
                  f"{s['eng_ranks_Q']}, geometry seeds 0..4 ranks {s['geometry_seed_ranks_Q']} "
                  f"-> {'confirmed' if s['confirmed'] else 'DIFFERS'}", flush=True)

    print("== (b1) Jacobian, complete averaged data: full column rank at n = 2K+3, not at 2K+2")
    for K in (2, 3, 4):
        for n in (2 * K + 3, 2 * K + 2):
            recs = []
            params = K * (n - 3) + K - 1
            for label, indices in (("eng", eng_idx), ("geometry", geo_idx)):
                for idx in indices:
                    if label == "eng":
                        tans, w = el.eng_witness_tangents(K, n, idx), eng_weights(K, idx)
                    else:
                        tans, w = geometry_jacobian_witness(K, n, idx)
                    Jm = jacobian(tans, w, all_pairs(n))
                    rq, rp, rg = ranks(Jm)
                    recs.append({"K": K, "n": n, "witness": "%s_%d" % (label, idx), "parameters": params,
                                 "data_pairs_all": len(Jm),
                                 "data_pairs_separation_ge_3": len(band_pairs(n, n)),
                                 "rank_Q": rq, "rank_mod_2^61-1": rp, "rank_mod_2147483629": rg,
                                 "weights": [str(x) for x in w]})
            out["jacobian_complete"] += recs
            s = summarise("complete data: full column rank" if n == 2 * K + 3
                          else "complete data: column-rank deficient", K, n,
                          {"parameters": params, "data": len(band_pairs(n, n))}, params, recs, n == 2 * K + 3)
            print(f"  K={K} n={n:2d} parameters={params} data={len(band_pairs(n, n))}: eng ranks "
                  f"{s['eng_ranks_Q']}, geometry seeds 0..4 ranks {s['geometry_seed_ranks_Q']} "
                  f"-> {'confirmed' if s['confirmed'] else 'DIFFERS'}", flush=True)

    print("== (b2) Jacobian, separation <= w: full column rank for w = K+3 at n = (K^2+3K+4)/2; "
          "deficient at n-1 and for w = K+2")
    for K in (2, 3, 4):
        nb = (K * K + 3 * K + 4) // 2
        for (n, w_sep) in ((nb, K + 3), (nb - 1, K + 3), (nb, K + 2), (nb + 1, K + 2), (nb + 4, K + 2),
                           (nb + 12, K + 2)):
            recs = []
            params = K * (n - 3) + K - 1
            pairs = band_pairs(n, w_sep)
            for label, indices in (("eng", eng_idx), ("geometry", geo_idx)):
                for idx in indices:
                    if label == "eng":
                        tans, w = el.eng_witness_tangents(K, n, idx), eng_weights(K, idx)
                    else:
                        tans, w = geometry_jacobian_witness(K, n, idx)
                    Jm = jacobian(tans, w, pairs)
                    rq, rp, rg = ranks(Jm)
                    recs.append({"K": K, "n": n, "separation_w": w_sep, "witness": "%s_%d" % (label, idx),
                                 "parameters": params, "data_pairs": len(pairs), "rank_Q": rq,
                                 "rank_mod_2^61-1": rp, "rank_mod_2147483629": rg,
                                 "weights": [str(x) for x in w]})
            out["jacobian_band"] += recs
            full = (n, w_sep) == (nb, K + 3)
            s = summarise("separation K+3: full column rank" if full else
                          ("separation K+3 at n-1: deficient" if w_sep == K + 3 else
                           "separation K+2: column-rank deficient"), K, n,
                          {"separation_w": w_sep, "parameters": params, "data": len(pairs)}, params, recs, full)
            print(f"  K={K} n={n:2d} w={w_sep} parameters={params} data={len(pairs)}: eng ranks "
                  f"{s['eng_ranks_Q']}, geometry seeds 0..4 ranks {s['geometry_seed_ranks_Q']} "
                  f"-> {'confirmed' if s['confirmed'] else 'DIFFERS'}", flush=True)

    allrecs = out["conic"] + out["jacobian_complete"] + out["jacobian_band"]
    out["all_Q_ranks_equal_both_modular_ranks"] = all(
        r["rank_Q"] == r["rank_mod_2^61-1"] == r["rank_mod_2147483629"] for r in allrecs)
    out["claims_not_confirmed"] = [s for s in out["summary"] if not s["confirmed"]]
    out["instances_below_target_where_full_rank_is_claimed"] = [
        {"claim": s["claim"], "K": s["K"], "n": s["n"], "witnesses": s["witnesses_below_target"]}
        for s in out["summary"] if s.get("witnesses_below_target")]
    out["seconds"] = round(time.time() - t_start, 1)
    path = HERE / "results" / "item3_ranks.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(out, indent=1) + "\n")
    print("claims not confirmed:", len(out["claims_not_confirmed"]),
          "| instances below target:", out["instances_below_target_where_full_rank_is_claimed"],
          "| Q-ranks equal both modular ranks:", out["all_Q_ranks_equal_both_modular_ranks"],
          "| wrote", path.relative_to(HERE.parents[2]), "| %.0f s" % (time.time() - t_start))


if __name__ == "__main__":
    main()
