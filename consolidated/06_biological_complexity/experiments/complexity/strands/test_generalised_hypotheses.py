"""Exhaustive tests of the generalised statements of docs/complexity/STRANDS_NN_HARDNESS.md (added after the
internal review COMPLEXITY-REV-0001):

 (A) Theorem 1 under (H2'): bulge / interior loops may be favourable, as long as
         g(f) >= sigma * iota(f) + delta        (iota(f) = number of item bonds on f = unpaired C's + 1);
 (B) Theorem 1c: flush coaxial stacks (two pairs, one template bond, one nick, no unpaired base) have energy
     x <= 0, all other exterior loops 0, bulge / interior loops >= gamma >= 0, and
         |x| < |sigma| + min(|sigma|, gamma)    (B >= 2 if |x| >= |sigma|);
 (C) Fact 1 (connected iff no face has two nicks), R(S) = 1, and #physical minima = Til / prod mu_s!;
 (E) Theorem 1e: flush stacks of energy x in [sigma, 0] together with dangles as in (D), bulge / interior loops
     >= gamma, B >= 2, D_C + max(D_G, |x|/B) < |sigma| and |sigma| - |x| + gamma + |e_A| > 0;
     E* = sigma*M + x*(n-m) + (m-1)*e_A, eps = min(|sigma| - D_C - max(D_G, |x|/B), |sigma| - |x| + gamma + |e_A|).
 (D) Theorem 1d (dangles; statement (P3) of the science division's review SCI-REV-0019): an exterior loop has
     energy  sum of d(u)  over its unpaired bases u that are covalent neighbours of a paired base of the loop,
     d(G) = -D_G, d(C) = -D_C, d(A) = e_A <= 0, bulge / interior loops >= 0, and |sigma| > D_G + D_C;
     then E* = sigma*M + (m-1)*e_A and eps = |sigma| - D_G - D_C.

For every instance all connected unpseudoknotted structures over all circular orderings are enumerated once
and the energies of all models are accumulated together (integers).  For each model:
     E*  = sigma*M + x*(n - m)             (x = 0 in (A))
     YES instance:  min = E*, the number of minimisers equals the number of labelled tilings, and every other
                    structure has energy >= E* + eps;
     NO instance:   min >= E* + eps,
with the eps of the theorem.  "Control" models violate a hypothesis; for them the script only reports
whether the statement happens to fail on some instance.
"""
import sys, itertools, random, time
import numpy as np
from ref_enum import *
from test_partition_reduction import count_labelled_tilings

SIGMA = -6

def models():
    """list of (name, kind, params, eps or None for controls)"""
    out = []
    # (A): g(f) = sigma*iota + delta + r,  r in {0,..,rmax} depending on the loop shape
    for delta, rmax in ((1, 0), (1, 2), (3, 5)):
        out.append((f"H2' delta={delta} r<={rmax}", "A", (delta, rmax), min(delta, -SIGMA)))
    out.append(("control: H2' with delta=0", "A", (0, 0), None))
    out.append(("control: H2' with delta=-1", "A", (-1, 0), None))
    # (B): flush energy x, bulge/interior = gamma + r
    for x, gamma in ((-1, 0), (-3, 0), (-5, 0), (-5, 2)):
        out.append((f"coax x={x} gamma={gamma}", "B", (x, gamma, 1), -SIGMA + x))            # |sigma| - |x|
    for x, gamma in ((-6, 1), (-6, 3), (-6, 9), (-7, 2), (-8, 3), (-11, 6), (-11, 9)):
        d = -x + SIGMA
        out.append((f"coax x={x} gamma={gamma}", "B2", (x, gamma, 1), min(-SIGMA, gamma) - d))
    for DG, DC, eA in ((1, 1, -2), (2, 3, -1), (0, 5, 0), (5, 0, -3)):
        out.append((f"dangles D_G={DG} D_C={DC} e_A={eA}", "D", (DG, DC, eA, 1), -SIGMA - DG - DC))
    # (E): flush energy x in [sigma, 0], dangles, bulge/interior = gamma + r   (Theorem 1e)
    # the hypothesis D_C + max(D_G, |x|/B) < |sigma| depends on B: eps is computed per instance (marker "perB");
    # an instance on which the hypothesis fails is treated as a control for that model
    for x, DG, DC, eA, gamma in ((-6, 1, 1, -1, 0), (-6, 2, 0, 0, 1), (-6, 0, 2, -3, 0), (-3, 2, 2, -2, 0), (-4, 1, 2, 0, 2),
                                 (-6, 2, 2, -1, 1), (-6, 3, 1, 0, 1), (-6, 3, 2, -1, 1),
                                 (-6, 0, 4, 0, 1), (-6, 0, 5, -1, 1)):
        out.append((f"coax x={x} with dangles D_G={DG} D_C={DC} e_A={eA}, gamma={gamma}", "E", (x, DG, DC, eA, gamma, 1), "perB"))
    out.append(("control: coax x=sigma, dangles 1,1, e_A=0, gamma=0", "E", (-6, 1, 1, 0, 0, 0), None))
    out.append(("control: coax x=sigma, dangles 3,3 (sum = |sigma|)", "E", (-6, 3, 3, -1, 1, 0), None))
    out.append(("control: dangles D_G=3 D_C=3 e_A=0 (sum = |sigma|)", "D", (3, 3, 0, 0), None))
    out.append(("control: dangles D_G=4 D_C=3 e_A=-1", "D", (4, 3, -1, 0), None))
    out.append(("control: coax x=sigma, gamma=0", "B", (-6, 0, 0), None))
    out.append(("control: coax x=-9, gamma=3 (d = min)", "B", (-9, 3, 0), None))
    out.append(("control: coax x=-12, gamma=9 (d = |sigma|)", "B", (-12, 9, 0), None))
    return out

def run(items, m, B, MODELS, rng):
    template = "A".join(["G" * B] * m)
    strands = [template] + ["C" * a for a in items]
    n = len(items)
    M = sum(a - 1 for a in items)
    cache = {}
    nm = len(MODELS)

    def loop_energy(kind, face, seq, owner):
        e = np.zeros(nm, dtype=np.int64)
        if kind == "exterior":
            ends = set()
            for i, j in face["pairs"]:
                ends.add(i); ends.add(j)
            nG = nC = nA = 0
            for p_ in face["unpaired"]:
                if any(0 <= q_ < len(seq) and owner[q_] == owner[p_] and q_ in ends for q_ in (p_ - 1, p_ + 1)):
                    if seq[p_] == "G":
                        nG += 1
                    elif seq[p_] == "C":
                        nC += 1
                    else:
                        nA += 1
        if kind == "hairpin" or kind == "multi":
            raise AssertionError("hairpins and multiloops cannot occur in these instances")
        flush = kind == "exterior" and len(face["pairs"]) == 2 and len(face["unpaired"]) == 0
        if kind in ("bulge", "interior"):
            iota = 1 + sum(1 for p in face["unpaired"] if seq[p] == "C")
            key = (kind, tuple(face["segs"]))
            if key not in cache:
                cache[key] = rng.random()
            u = cache[key]
        for q, (name, typ, par, eps) in enumerate(MODELS):
            if kind == "stack":
                e[q] = SIGMA
            elif typ == "A":
                if kind in ("bulge", "interior"):
                    delta, rmax = par
                    e[q] = SIGMA * iota + delta + int(u * (rmax + 1))
            elif typ == "D":
                DG, DC, eA, rmax = par
                if kind == "exterior":
                    e[q] = -DG * nG - DC * nC + eA * nA
                elif kind in ("bulge", "interior"):
                    e[q] = int(u * (rmax + 1))
            elif typ == "E":
                x, DG, DC, eA, gamma, rmax = par
                if flush:
                    e[q] = x
                elif kind == "exterior":
                    e[q] = -DG * nG - DC * nC + eA * nA
                elif kind in ("bulge", "interior"):
                    e[q] = gamma + int(u * (rmax + 1))
            else:
                x, gamma, rmax = par
                if flush:
                    e[q] = x
                elif kind in ("bulge", "interior"):
                    e[q] = gamma + int(u * (rmax + 1))
        return e

    t0 = time.time()
    energies = []
    labs = []
    seen = set()
    c = len(strands)
    for rest in itertools.permutations(range(1, c)):
        order = (0,) + rest
        seq, owner, idx, nick_after = concat(strands, order)
        N = len(seq)
        can_pair = lambda i, j: (seq[i], seq[j]) in COMPLEMENT
        for pairs in noncrossing_matchings(seq, 0, N, can_pair):
            fs = faces(N, pairs, nick_after)
            kinds = [classify(f) for f in fs]
            conn = "disconnected" not in kinds
            assert conn == connected_uf(N, pairs, owner), (order, pairs)          # Fact 1
            if not conn:
                continue
            e = 0
            for f, kd in zip(fs, kinds):
                e = e + loop_energy(kd, f, seq, owner)
            lab = frozenset(((owner[i], idx[i]), (owner[j], idx[j])) for i, j in pairs)
            assert lab not in seen
            seen.add(lab)
            energies.append(e)
            labs.append(lab)
    E = np.array(energies)
    til = count_labelled_tilings(items, m, B)
    feasible = til > 0
    allok = True
    report = []
    for q, (name, typ, par, eps) in enumerate(MODELS):
        if typ == "B2" and B < 2:
            continue
        if typ == "E" and B < 2:
            continue
        if typ == "E":
            Estar = SIGMA * M + par[0] * (n - m) + (m - 1) * par[3]
        elif typ == "D":
            Estar = SIGMA * M + (m - 1) * par[2]
        else:
            x = 0 if typ == "A" else par[0]
            Estar = SIGMA * M + x * (n - m)
        col = E[:, q]
        mn = int(col.min())
        nmin = int((col == mn).sum())
        if eps == "perB":
            x_, DG, DC, eA, gamma, _ = par
            margin = -SIGMA - DC - max(DG, -x_ / B)
            eps = min(margin, -SIGMA + x_ + gamma - eA) if margin > 0 else None
            if eps is None:
                name = name + " [hypothesis fails for this B]"
        if eps is None:
            holds = (mn == Estar and nmin == til) if feasible else (mn > Estar)
            report.append(("control: " + name if not name.startswith("control") else name,
                           "statement holds here" if holds else "STATEMENT FAILS HERE (expected for a control)"))
            continue
        if feasible:
            others = col[col != Estar]
            ok = mn == Estar and nmin == til and (len(others) == 0 or int(others.min()) >= Estar + eps)
        else:
            ok = mn >= Estar + eps
        if not ok:
            allok = False
            report.append((name, f"MISMATCH min={mn} E*={Estar} nmin={nmin} til={til}"))
    # (C) symmetry: every structure has trivial stabiliser; physical minima = Til / prod mu!
    mu = 1
    for a in set(items):
        k = items.count(a)
        for t in range(2, k + 1):
            mu *= t
    q0 = 0   # model 0 is of type (A) with eps > 0: its minimisers are the tilings in YES instances
    orbs = symmetry_orbits(strands, [(lab, int(e[q0])) for lab, e in zip(labs, energies)])
    assert all(st == 1 and sz == mu for _, _, sz, st in orbs), "non-trivial symmetry found"
    if feasible:
        Estar = SIGMA * M
        phys = sum(1 for _, e, _, _ in orbs if e == Estar)
        if phys * mu != til:
            allok = False
            report.append(("physical count", f"MISMATCH {phys} * {mu} != {til}"))
    print(f"items={items} m={m} B={B}: {'YES' if feasible else 'NO '} structures={len(labs)} orbits={len(orbs)} "
          f"tilings={til} {'OK' if allok else 'MISMATCH'} [{time.time()-t0:.1f}s]", flush=True)
    for name, msg in report:
        print(f"      {name}: {msg}")
    return allok, report

if __name__ == "__main__":
    big = len(sys.argv) > 1 and sys.argv[1] == "big"
    cases = [([1, 1], 2, 1), ([2], 2, 1), ([1, 1, 1], 3, 1), ([2, 1], 3, 1),
             ([2], 1, 2), ([1, 1], 1, 2), ([3], 1, 3), ([1, 2], 1, 3), ([1, 1, 1], 1, 3), ([2, 2], 1, 4), ([1, 3], 1, 4),
             ([2, 2], 2, 2), ([1, 1, 2], 2, 2), ([1, 1, 1, 1], 2, 2), ([3, 1], 2, 2), ([4], 2, 2),
             ([3, 3], 2, 3), ([1, 2, 1, 2], 2, 3), ([2, 2, 2], 2, 3), ([4, 2], 2, 3), ([3, 2, 1], 2, 3), ([5, 1], 2, 3),
             ([6], 2, 3), ([2, 2, 2], 3, 2), ([3, 3], 3, 2), ([1, 2, 3], 3, 2), ([2, 2, 1, 1], 3, 2), ([4, 2], 3, 2),
             ([4, 4], 2, 4), ([3, 3, 2], 2, 4), ([5, 3], 2, 4)]
    if big:
        cases += [([2, 2, 3, 1], 2, 4), ([2, 2, 2, 2], 2, 4), ([3, 3, 1, 1], 2, 4), ([2, 2, 2, 3], 3, 3), ([4, 4, 2], 2, 5)]
    MODELS = models()
    rng = random.Random(7)
    allok = True
    fails = {}
    for items, m, B in cases:
        ok, rep = run(items, m, B, MODELS, rng)
        allok &= ok
        for name, msg in rep:
            if name.startswith("control") and "FAILS" in msg:
                fails[name] = fails.get(name, 0) + 1
    print("controls: number of instances on which the statement fails:", fails)
    print("ALL OK" if allok else "SOME MISMATCH")
