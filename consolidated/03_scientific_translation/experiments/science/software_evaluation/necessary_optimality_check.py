#!/usr/bin/env python3
"""Necessary optimality of a configuration of a pair model under entrywise interval data.

Statement tested (elementary; the "worst-case scenario" criterion of interval-data combinatorial optimisation,
quoted here from memory, not from a source opened for this script):

  Let E(x) = sum_i U_i(x_i) + sum_{i<j} P_ij(x_i, x_j) be a pair model on a finite product of state sets and let
  b >= 0 be a table of the same shape (one number per one-body entry and per pair entry).  A scenario is a model
  E' whose every entry lies within b of the corresponding entry of E.  For a configuration x* let E~ be the model
  obtained by RAISING the entries x* uses by b and LOWERING every other entry by b.  Then
      (N)  x* minimises every scenario        <=>  x* minimises E~;
      (U)  x* is the only minimiser of every scenario  <=>  x* is the only minimiser of E~.
  E~ is again a pair model on the same state sets: the question "does the minimiser survive this much model
  error" is one more minimisation of the same kind.

What the script does.
  (A) n = 3 sites with 2 states each (18 entries): ALL 2^18 vertex scenarios are enumerated (the difference of
      two configurations' energies is linear in the scenario, so vertices suffice) and compared with (N), (U).
  (B) larger models (3-5 sites, 2-4 states): if (N) holds, x* must be a minimiser in 2 000 random scenarios
      (vertices and interior points); if (N) fails, the scenario E~ itself must have a strictly better
      configuration.
  (C) controls that must fail: (c1) only the other entries lowered, x*'s own entries not raised; (c2) pair
      bounds ignored; (c3) half the allowance.
  (D) arithmetic: the allowance a one-site change gets under a uniform bound, for the sizes of real instances.

Integers throughout (no rounding).  Run:  python3 -B necessary_optimality_check.py
"""
import itertools, resource, sys, time
import numpy as np

resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
T0 = time.time()


def random_model(rng, n, kmax, emax, bmax, kmin=2):
    ks = [int(rng.integers(kmin, kmax + 1)) for _ in range(n)]
    U = [rng.integers(-emax, emax + 1, size=k) for k in ks]
    P = {(i, j): rng.integers(-emax, emax + 1, size=(ks[i], ks[j])) for i in range(n) for j in range(i + 1, n)}
    bU = [rng.integers(0, bmax + 1, size=k) for k in ks]
    bP = {key: rng.integers(0, bmax + 1, size=P[key].shape) for key in P}
    return ks, U, P, bU, bP


def configs(ks):
    return list(itertools.product(*[range(k) for k in ks]))


def energy(U, P, x):
    return int(sum(U[i][x[i]] for i in range(len(x))) + sum(P[(i, j)][x[i], x[j]] for (i, j) in P))


def tilde(U, P, bU, bP, xs, own=True, pairs=True, factor_num=1, factor_den=1):
    """E~: entries used by xs raised by b (if own), all other entries lowered by b; b scaled by factor."""
    n = len(U)
    U2 = [u * factor_den - bu * factor_num for u, bu in zip(U, bU)]
    for i in range(n):
        U2[i] = U2[i].copy()
        U2[i][xs[i]] = U[i][xs[i]] * factor_den + (bU[i][xs[i]] * factor_num if own else 0)
    P2 = {}
    for (i, j), p in P.items():
        bp = bP[(i, j)] if pairs else np.zeros_like(bP[(i, j)])
        q = p * factor_den - bp * factor_num
        q[xs[i], xs[j]] = p[xs[i], xs[j]] * factor_den + (bp[xs[i], xs[j]] * factor_num if own else 0)
        P2[(i, j)] = q
    return U2, P2


def criterion(ks, U, P, bU, bP, xs, **kw):
    """returns (N, Uq): xs minimises E~; xs is the only minimiser of E~."""
    U2, P2 = tilde(U, P, bU, bP, xs, **kw)
    es = energy(U2, P2, xs)
    others = [energy(U2, P2, x) for x in configs(ks) if x != xs]
    return es <= min(others), es < min(others)


def exhaustive_vertices(ks, U, P, bU, bP, xs):
    """truth by enumeration of every vertex scenario (entry = centre +- b)."""
    cf = configs(ks)
    ents = [("u", i, a) for i in range(len(ks)) for a in range(ks[i])] + \
           [("p", key, a, c) for key in P for a in range(P[key].shape[0]) for c in range(P[key].shape[1])]
    m = len(ents)
    cen = np.array([U[e[1]][e[2]] if e[0] == "u" else P[e[1]][e[2], e[3]] for e in ents], dtype=np.int64)
    rad = np.array([bU[e[1]][e[2]] if e[0] == "u" else bP[e[1]][e[2], e[3]] for e in ents], dtype=np.int64)
    inc = np.zeros((len(cf), m), dtype=np.int64)          # incidence: which entries a configuration uses
    for r, x in enumerate(cf):
        for c, e in enumerate(ents):
            if e[0] == "u":
                inc[r, c] = int(x[e[1]] == e[2])
            else:
                i, j = e[1]
                inc[r, c] = int(x[i] == e[2] and x[j] == e[3])
    signs = ((np.arange(2**m, dtype=np.int64)[:, None] >> np.arange(m)) & 1) * 2 - 1      # all vertices
    en = (cen[None, :] + signs * rad[None, :]) @ inc.T                                     # vertices x configs
    s = cf.index(xs)
    mn = en.min(axis=1)
    is_min = en[:, s] == mn
    unique = is_min & ((en == mn[:, None]).sum(axis=1) == 1)
    return bool(is_min.all()), bool(unique.all()), 2**m


def main():
    rng = np.random.default_rng(20261126)
    print("necessary_optimality_check.py   started", time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))

    # ---------------- (A) exhaustive over all vertex scenarios
    nA = 400
    agreeN = agreeU = 0
    posN = posU = 0
    c1_dis = c2_dis = c3_dis = 0
    nvert = 0
    for t in range(nA):
        ks, U, P, bU, bP = random_model(rng, 3, 2, emax=12, bmax=3)
        cf = configs(ks)
        es = [energy(U, P, x) for x in cf]
        xs = cf[int(np.argmin(es))]
        tN, tU, nv = exhaustive_vertices(ks, U, P, bU, bP, xs)
        nvert = nv
        cN, cU = criterion(ks, U, P, bU, bP, xs)
        agreeN += int(tN == cN)
        agreeU += int(tU == cU)
        posN += int(tN)
        posU += int(tU)
        c1_dis += int(criterion(ks, U, P, bU, bP, xs, own=False)[0] != tN)
        c2_dis += int(criterion(ks, U, P, bU, bP, xs, pairs=False)[0] != tN)
        c3_dis += int(criterion(ks, U, P, bU, bP, xs, factor_num=1, factor_den=2)[0] != tN)
    print(f"(A) {nA} models, 3 sites x 2 states, every one of the {nvert} vertex scenarios enumerated")
    print(f"    (N) criterion equals enumeration: {agreeN}/{nA}   (necessarily optimal in {posN}, not in {nA - posN})")
    print(f"    (U) criterion equals enumeration: {agreeU}/{nA}   (necessarily the only minimiser in {posU})")
    print(f"    controls, disagreements with enumeration (each must be > 0): "
          f"(c1) own entries not raised {c1_dis}; (c2) pair bounds ignored {c2_dis}; (c3) half the allowance {c3_dis}")
    assert agreeN == nA and agreeU == nA
    assert 0 < posN < nA, "the family must contain both outcomes"
    assert c1_dis > 0 and c2_dis > 0 and c3_dis > 0, "a control did not fail"

    # ---------------- (B) larger models, sampled scenarios and the constructed scenario
    nB = 600
    hold = fail = 0
    viol_hold = 0
    constructed_beats = 0
    scen_tested = 0
    for t in range(nB):
        n = int(rng.integers(3, 6))
        ks, U, P, bU, bP = random_model(rng, n, 4, emax=30, bmax=int(rng.integers(0, 4)))
        cf = configs(ks)
        es = [energy(U, P, x) for x in cf]
        xs = cf[int(np.argmin(es))]
        cN, cU = criterion(ks, U, P, bU, bP, xs)
        if cN:
            hold += 1
            for r in range(2000 // len(cf) + 20):
                # a random scenario: vertices half of the time, interior points otherwise (doubled to stay integer)
                if r % 2 == 0:
                    U2 = [2 * (u + bu * rng.choice([-1, 1], size=u.shape)) for u, bu in zip(U, bU)]
                    P2 = {key: 2 * (P[key] + bP[key] * rng.choice([-1, 1], size=P[key].shape)) for key in P}
                else:
                    U2 = [2 * u + rng.integers(-2 * bu, 2 * bu + 1) for u, bu in zip(U, bU)]
                    P2 = {key: 2 * P[key] + rng.integers(-2 * bP[key], 2 * bP[key] + 1) for key in P}
                e2 = [energy(U2, P2, x) for x in cf]
                scen_tested += 1
                if e2[cf.index(xs)] != min(e2):
                    viol_hold += 1
        else:
            fail += 1
            U2, P2 = tilde(U, P, bU, bP, xs)
            e2 = [energy(U2, P2, x) for x in cf]
            constructed_beats += int(min(e2) < e2[cf.index(xs)])
    print(f"(B) {nB} models, 3-5 sites with 2-4 states: criterion (N) holds in {hold}, fails in {fail}")
    print(f"    where it holds: {scen_tested} random scenarios, x* not a minimiser in {viol_hold} (must be 0)")
    print(f"    where it fails: the scenario E~ has a strictly better configuration in {constructed_beats}/{fail} (must be all)")
    assert viol_hold == 0 and constructed_beats == fail and hold > 0 and fail > 0

    # ---------------- (D) arithmetic of the allowance under a uniform bound
    print("(D) uniform bound: every one-body entry within d1, every pair entry within d2 of the table.")
    print("    A configuration that differs from x* at m sites of n uses m other one-body entries and")
    print("    m(n-m) + m(m-1)/2 other pair entries; it beats x* in some scenario iff its energy gap is below")
    print("    2 d1 m + 2 d2 [m(n-m) + m(m-1)/2].  For m = 1:  2 d1 + 2 d2 (n-1).")
    for n in (26, 36, 46, 49, 65):
        for d2 in (2**-21, 4e-11, 0.01, 0.1):
            print(f"    n = {n:3d}, d1 = d2 = {d2:9.3g} kcal/mol: one-site allowance {2*d2 + 2*d2*(n-1):10.3g} kcal/mol")
    print("    (2^-21 kcal/mol is half a rounding unit of tables in units of 2^-20; 4e-11 is an OBSERVED agreement,")
    print("     not a bound.)")
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    print(f"ALL DONE   computed in {time.time() - T0:.1f} s   peak memory {peak:.0f} MB")


if __name__ == "__main__":
    main()
