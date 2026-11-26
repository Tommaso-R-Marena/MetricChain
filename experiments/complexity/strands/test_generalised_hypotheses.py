"""Exhaustive tests of the generalised statements of docs/complexity/STRANDS_NN_HARDNESS.md (added after the
internal review COMPLEXITY-REV-0001):

 (A) Theorem 1 under (H2'): bulge / interior loops may be favourable, as long as
         g(f) >= sigma * iota(f) + delta        (iota(f) = number of item bonds on f = unpaired C's + 1);
 (B) Theorem 1c: flush coaxial stacks (two pairs, one template bond, one nick, no unpaired base) have energy
     x <= 0, all other exterior loops 0, bulge / interior loops >= gamma >= 0, and
         |x| < |sigma| + min(|sigma|, gamma)    (B >= 2 if |x| >= |sigma|);
 (C) Fact 1 (connected iff no face has two nicks), R(S) = 1, and #physical minima = Til / prod mu_s!.

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

    def loop_energy(kind, face, seq):
        e = np.zeros(nm, dtype=np.int64)
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
    for order, lab, e, kinds in enumerate_structures(strands, loop_energy, connected_only=True, check=True):
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
        x = 0 if typ == "A" else par[0]
        if typ == "B2" and B < 2:
            continue
        Estar = SIGMA * M + x * (n - m)
        col = E[:, q]
        mn = int(col.min())
        nmin = int((col == mn).sum())
        if eps is None:
            holds = (mn == Estar and nmin == til) if feasible else (mn > Estar)
            report.append((name, "statement holds here" if holds else "STATEMENT FAILS HERE (expected for a control)"))
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
