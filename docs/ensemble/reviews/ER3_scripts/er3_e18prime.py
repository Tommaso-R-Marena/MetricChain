#!/usr/bin/env python3
"""ER3 review, Proposition E18' (a prior on the number of atoms).  Reviewer's own code.

A. Cube with n = 4 and n = 5 sites, pair data, states modulo the global flip (8 and 16 states, 6 and 10 pair
   observables).  EXHAUSTIVE over all supports S of every size K (one representative per orbit of the symmetry
   group: permutations of the sites and sign changes), and for each S exhaustive over all competing supports S'
   with |S'| = K (a twin with fewer atoms is a twin on some S' of size K with zero weights).  For each S:
     - are the pair features affinely independent on S; is S flat-isolated; is S a face (LP);
     - random weights (3 draws): is there a twin with at most K atoms (E18' says: no, if flat-isolated);
     - is there SOME strictly positive weight vector with such a twin (the claim after E18': "for every
       flat-isolated support of 6 or 7 conformers that is not a face there are some weights ...", for which the
       division's check L3 samples three supports);
     - uniform weights: is there a twin.
   Twin test for a pair (S, S'): a non-negative v on S' with the data of w on S exists for some w > 0 iff there is
   a linear dependency h of the vectors (1, Phi) on S u S' with h > 0 on S \\ S', h <= 0 on S' \\ S (sign-free on
   the intersection).  Decided from the null space (dimension 0: no; dimension 1: sign test; larger: LP).
B. Random finite instances with integer-valued features that are NOT injective: the three hypotheses separately
   (affine independence; flat isolation; what replaces them when they fail).
"""
import itertools, sys, time
import numpy as np
from scipy.optimize import linprog, nnls

rng = np.random.default_rng(31102)


def cube_mod_flip(n):
    Z = np.array(list(itertools.product((1, -1), repeat=n - 1)))
    return np.hstack([np.ones((len(Z), 1), dtype=int), Z])


def pair_features(Y):
    n = Y.shape[1]; iu = np.triu_indices(n, 1)
    return np.hstack([np.ones((len(Y), 1)), (Y[:, iu[0]] * Y[:, iu[1]]).astype(float)])


def symmetry_perms(Y):
    """Permutations of the state indices induced by site permutations and sign changes (modulo the flip)."""
    n = Y.shape[1]
    index = {tuple(y): i for i, y in enumerate(Y.tolist())}
    perms = set()
    for pi in itertools.permutations(range(n)):
        for s in itertools.product((1, -1), repeat=n - 1):
            sv = np.array((1,) + s)
            img = Y[:, pi] * sv
            img = img * img[:, [0]]                          # normalise the first coordinate to +1
            perms.add(tuple(index[tuple(r)] for r in img.tolist()))
    return np.array(sorted(perms))


def orbit_representatives(N, K, perms):
    seen = {}
    pw = 1 << np.arange(N)
    for S in itertools.combinations(range(N), K):
        key = int((pw[perms[:, list(S)]]).sum(axis=1).min())
        if key not in seen:
            seen[key] = [S, 0]
        seen[key][1] += 1
    return [(tuple(v[0]), v[1]) for v in seen.values()]


def is_face(G, S):
    N = G.shape[0]; mask = np.ones(N, bool); mask[list(S)] = False
    res = linprog(np.zeros(G.shape[1]), A_ub=-G[mask], b_ub=-np.ones(mask.sum()), A_eq=G[list(S)],
                  b_eq=np.zeros(len(S)), bounds=[(None, None)] * G.shape[1], method="highs")
    return res.status == 0


def flat_isolated(G, S):
    B = G[list(S)].T
    Q, _ = np.linalg.qr(B)
    res = np.linalg.norm(G - (G @ Q) @ Q.T, axis=1)
    return int((res < 1e-8).sum()) == len(S)


def twin_for_some_weights(G, S, Sp):
    """Is there w > 0 on S and v >= 0 on Sp (Sp != S, |Sp| <= |S|) with G_S^T w = G_Sp^T v ?"""
    Sset = set(S); T = [y for y in Sp if y not in Sset]; R = [y for y in Sp if y in Sset]
    Sm = [x for x in S if x not in set(R)]
    if not T or not Sm:
        return False
    order = Sm + R + T
    A = G[order].T                                           # columns: Sm (h > 0), R (free), T (h <= 0)
    _, s, Vt = np.linalg.svd(A, full_matrices=True)
    rank = int((s > 1e-9).sum())
    d = len(order) - rank
    if d == 0:
        return False
    a, b = len(Sm), len(Sm) + len(R)
    if d == 1:
        h = Vt[-1]
        for sg in (1, -1):
            g = sg * h
            if g[:a].min() > 1e-9 and g[b:].max() < 1e-9:
                return True
        return False
    Nsp = Vt[rank:].T                                        # len(order) x d
    # maximise t s.t. (Nsp c)[:a] >= t, (Nsp c)[b:] <= 0, |c| <= 1
    c = np.zeros(d + 1); c[-1] = -1
    A_ub = np.vstack([np.hstack([-Nsp[:a], np.ones((a, 1))]), np.hstack([Nsp[b:], np.zeros((len(order) - b, 1))])])
    res = linprog(c, A_ub=A_ub, b_ub=np.zeros(A_ub.shape[0]), bounds=[(-1, 1)] * d + [(0, 1)], method="highs")
    return res.status == 0 and -res.fun > 1e-7


def twin_for_weights(G, S, w, subsets):
    b = G[list(S)].T @ w; Sset = set(S)
    for Sp in subsets:
        if set(Sp) == Sset:
            continue
        v, r = nnls(G[list(Sp)].T, b)
        if r < 1e-9:
            return Sp, v
    return None, None


def part_A(n, Kmax, time_budget):
    Y = cube_mod_flip(n); G = pair_features(Y); N = len(Y); m = G.shape[1] - 1
    perms = symmetry_perms(Y)
    print(f"A. cube, n = {n}: {N} states modulo flip, {m} pair observables, symmetry group acting through "
          f"{len(perms)} permutations of the states")
    print("   K | supports (orbits) | affinely dependent | aff. indep., not flat-isolated | flat-isolated: faces | "
          "flat-isolated non-faces | of these: twin for random w / for uniform w / for SOME w > 0 | "
          "faces with a twin for some w (must be 0)")
    ok = True; t0 = time.time()
    for K in range(2, Kmax + 1):
        reps = orbit_representatives(N, K, perms)
        subsets = list(itertools.combinations(range(N), K))
        n_tot = sum(c for _, c in reps)
        dep = [0, 0]; notiso = [0, 0]; faces = [0, 0]; nonf = [0, 0]
        rand_twin = [0, 0]; unif_twin = [0, 0]; some_twin = [0, 0]; face_twin = 0; notiso_twin_freq = []
        skipped = 0
        for S, cnt in reps:
            GS = G[list(S)]
            if np.linalg.matrix_rank(GS, tol=1e-9) < K:
                dep[0] += 1; dep[1] += cnt; continue
            iso = flat_isolated(G, S)
            if not iso:
                notiso[0] += 1; notiso[1] += cnt
                # not flat-isolated: twins should exist on an open set of weights
                hits = sum(twin_for_weights(G, S, rng.dirichlet(np.ones(K)), subsets)[0] is not None for _ in range(10))
                notiso_twin_freq.append(hits / 10)
                continue
            f = is_face(G, S)
            if time.time() - t0 > time_budget:
                skipped += 1; continue
            some = any(twin_for_some_weights(G, S, Sp) for Sp in subsets if set(Sp) != set(S))
            if f:
                faces[0] += 1; faces[1] += cnt
                face_twin += some
                continue
            nonf[0] += 1; nonf[1] += cnt
            rt = any(twin_for_weights(G, S, rng.dirichlet(3 * np.ones(K)), subsets)[0] is not None for _ in range(3))
            ut = twin_for_weights(G, S, np.ones(K) / K, subsets)[0] is not None
            rand_twin[0] += rt; rand_twin[1] += rt * cnt
            unif_twin[0] += ut; unif_twin[1] += ut * cnt
            some_twin[0] += some; some_twin[1] += some * cnt
        ok &= rand_twin[0] == 0 and face_twin == 0
        fr = (f"{min(notiso_twin_freq):.1f}..{max(notiso_twin_freq):.1f}" if notiso_twin_freq else "-")
        print(f"   {K:2d} | {n_tot:6d} ({len(reps):4d}) | {dep[1]:6d} ({dep[0]:3d}) | {notiso[1]:6d} ({notiso[0]:3d}) "
              f"[twin frequency over random w: {fr}] | {faces[1]:6d} ({faces[0]:3d}) | {nonf[1]:6d} ({nonf[0]:3d}) | "
              f"{rand_twin[1]} ({rand_twin[0]}) / {unif_twin[1]} ({unif_twin[0]}) / {some_twin[1]} ({some_twin[0]}) | {face_twin}"
              + (f"   [{skipped} orbits skipped: time budget]" if skipped else ""), flush=True)
    return ok


def part_B():
    print("B. random finite instances, integer features (not injective)")
    stats = {"iso": [0, 0], "noniso": [0, 0, 0], "dep": [0, 0]}
    ok = True
    for trial in range(1500):
        N = int(rng.integers(7, 11)); m = int(rng.integers(2, 5))
        Phi = rng.integers(0, 3, size=(N, m)).astype(float)
        G = np.hstack([np.ones((N, 1)), Phi])
        K = int(rng.integers(2, m + 2))
        S = tuple(sorted(rng.choice(N, size=K, replace=False).tolist()))
        subsets = list(itertools.combinations(range(N), K))
        w = rng.dirichlet(2 * np.ones(K))
        if np.linalg.matrix_rank(G[list(S)], tol=1e-9) < K:
            # affinely dependent: a twin on S itself (move along the dependency) -- test it directly
            _, s, Vt = np.linalg.svd(G[list(S)].T); h = Vt[-1]
            eps = 0.5 * w.min() / np.abs(h).max()
            w2 = w + eps * h
            stats["dep"][0] += 1
            good = np.allclose(G[list(S)].T @ w2, G[list(S)].T @ w, atol=1e-10) and w2.min() >= 0 and not np.allclose(w2, w)
            stats["dep"][1] += good; ok &= good
            continue
        if flat_isolated(G, S):
            stats["iso"][0] += 1
            Sp, v = twin_for_weights(G, S, w, subsets)
            stats["iso"][1] += Sp is not None
            ok &= Sp is None
        else:
            stats["noniso"][0] += 1
            hits = sum(twin_for_weights(G, S, rng.dirichlet(np.ones(K)), subsets)[0] is not None for _ in range(20))
            stats["noniso"][1] += hits > 0
            stats["noniso"][2] += hits == 20
    print(f"   flat-isolated and affinely independent: {stats['iso'][0]} instances, twin with <= K atoms for a random "
          f"weight: {stats['iso'][1]} (E18': must be 0)")
    print(f"   affinely independent, NOT flat-isolated: {stats['noniso'][0]} instances; a twin for at least one of 20 "
          f"random weights in {stats['noniso'][1]}, for all 20 in {stats['noniso'][2]}")
    print(f"   affinely dependent on S: {stats['dep'][0]} instances; second ensemble on the same support in {stats['dep'][1]}")
    # explicit: the hypothesis 'Phi injective' is not needed off S, and non-injectivity onto S destroys flat isolation
    Phi = np.array([[0., 0.], [1., 0.], [0., 1.], [2., 2.], [2., 2.], [1., 0.]])
    G = np.hstack([np.ones((6, 1)), Phi])
    for S in ((0, 2), (0, 1)):
        subsets = list(itertools.combinations(range(6), 2))
        tw = [twin_for_weights(G, S, rng.dirichlet(np.ones(2)), subsets)[0] for _ in range(5)]
        print(f"   explicit X = 6 points, Phi = (0,0),(1,0),(0,1),(2,2),(2,2),(1,0); S = {S}: flat-isolated "
              f"{flat_isolated(G, S)}; twins found for 5 random weights: {[t for t in tw]}")
    return ok


if __name__ == "__main__":
    a4 = part_A(4, 6, 60)
    a5 = part_A(5, 10, float(sys.argv[1]) if len(sys.argv) > 1 else 480)
    b = part_B()
    print("PASS" if (a4 and a5 and b) else "FAIL")
