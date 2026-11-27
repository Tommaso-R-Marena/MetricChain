# fragility.py -- how fragile is the reduction when the hypotheses are violated?
# Uses the brute-force signature tables (every connected structure of every instance with m*B <= 10).
#
# For ANY loop-local model all tiling structures of I(a,m,B) have the same multiset of faces:
#   M stacks 'C-C=G-G=', (n-m) flush nicked stacks 'C=G-G=C|', (m-1) A-loops 'A-G=C|C=G-',
#   and the two terminal exterior loops 'C=G|', 'C|G='.
# So the natural threshold of a reduction is E_til(model; n,m,M).  The reduction (with that
# threshold) is correct for a model iff every NO-instance has MFE > E_til.  We also record whether,
# on YES-instances, MFE == E_til and whether the minimum-energy structures are exactly the tilings.
import sys
from lib import *
import test_main

S = -100  # sigma for the synthetic models


def dangles(f):
    """(n3, n5): unpaired bases covalently adjacent to a paired base inside the loop,
    n3: unpaired base is 3' of the paired base, n5: unpaired base is 5' of the paired base"""
    letters, seps = f.s[0::2], f.s[1::2]
    L = len(letters)
    paired = [seps[j] == "=" or seps[(j - 1) % L] == "=" for j in range(L)]
    n3 = n5 = 0
    for j in range(L):
        if seps[j] == "-":
            a, b = j, (j + 1) % L
            if paired[a] and not paired[b]:
                n3 += 1
            if (not paired[a]) and paired[b]:
                n5 += 1
    return n3, n5


def mk(name, sigma=S, fn=None, ext=None):
    return Model(name, sigma, fn, ext, hyp=False)


def turner_like(f):
    """integer caricature (0.01 kcal/mol) of the Turner-2004 single-nucleotide bulge rule, sigma = -326"""
    if f.kind == "bulge":
        if f.unp == 1:
            if f.iside == 1:          # bulged C in a C run: 3.81 - 0.9 - 3.26 - RT ln 3
                return -103
            if f.tside == "A":        # bulged A, one state: 3.81 - 3.26
                return 55
            return -13                # bulged G in a G run (3 states): 3.81 - 3.26 - 0.68
        return 280 if f.unp == 2 else 320
    if f.kind == "interior":
        return 100 + 20 * f.unp
    return 500


MODELS = [
    mk("(control) stack-only", S),
    mk("ext const +37", S, None, lambda f: 37),
    mk("ext const -37", S, None, lambda f: -37),
    mk("coax -50, bulge/int 0", S, None, lambda f: -50 if f.flush else 0),
    mk("coax -99, bulge/int 0", S, None, lambda f: -99 if f.flush else 0),
    mk("coax -100 (=sigma), bulge/int 0", S, None, lambda f: -100 if f.flush else 0),
    mk("coax -101, bulge/int 0", S, None, lambda f: -101 if f.flush else 0),
    mk("coax -150, bulge/int 0", S, None, lambda f: -150 if f.flush else 0),
    mk("coax -50, bulge/int +30", S, lambda f: 30, lambda f: -50 if f.flush else 0),
    mk("coax -100 (=sigma), bulge/int +30", S, lambda f: 30, lambda f: -100 if f.flush else 0),
    mk("coax -100 (=sigma), only A-bulge +30", S, lambda f: 30 if (f.kind == "bulge" and f.tside == "A") else 0, lambda f: -100 if f.flush else 0),
    mk("coax -101, bulge/int +30", S, lambda f: 30, lambda f: -101 if f.flush else 0),
    mk("coax -120, bulge/int +30", S, lambda f: 30, lambda f: -120 if f.flush else 0),
    mk("coax -150, bulge/int +30", S, lambda f: 30, lambda f: -150 if f.flush else 0),
    mk("dangles -10/adjacency, bulge/int 0", S, None, lambda f: -10 * sum(dangles(f))),
    mk("dangles -30/adjacency, bulge/int 0", S, None, lambda f: -30 * sum(dangles(f))),
    mk("dangles -34/adjacency, bulge/int 0", S, None, lambda f: -34 * sum(dangles(f))),
    mk("dangles -50/adjacency, bulge/int 0", S, None, lambda f: -50 * sum(dangles(f))),
    mk("dangles -60/adjacency, bulge/int 0", S, None, lambda f: -60 * sum(dangles(f))),
    mk("dangles -100/adjacency, bulge/int 0", S, None, lambda f: -100 * sum(dangles(f))),
    mk("dangles -30/adjacency, bulge/int +50", S, lambda f: 50, lambda f: -30 * sum(dangles(f))),
    mk("dangles -50/adjacency, bulge/int +50", S, lambda f: 50, lambda f: -50 * sum(dangles(f))),
    mk("bulges -50, interior 0", S, lambda f: -50 if f.kind == "bulge" else 0),
    mk("bulges -99, interior 0", S, lambda f: -99 if f.kind == "bulge" else 0),
    mk("bulges -100 (=sigma), interior 0", S, lambda f: -100 if f.kind == "bulge" else 0),
    mk("bulges -101, interior 0", S, lambda f: -101 if f.kind == "bulge" else 0),
    mk("template-side bulges 0, item-side bulges -199", S, lambda f: (-199 if f.tside == "" else 0) if f.kind == "bulge" else 0),
    mk("template-side bulges 0, item-side bulges -201", S, lambda f: (-201 if f.tside == "" else 0) if f.kind == "bulge" else 0),
    mk("interior -199, bulges 0", S, lambda f: -199 if f.kind == "interior" else 0),
    mk("interior -201, bulges 0", S, lambda f: -201 if f.kind == "interior" else 0),
    mk("generalised (H2'): g = sigma*iota + 1 for bulge/int", S, lambda f: S * f.iota + 1),
    mk("borderline: g = sigma*iota for bulge/int", S, lambda f: S * f.iota),
    mk("Turner-2004-like bulges (no dangles), sigma=-326", -326, turner_like),
    mk("Turner-2004-like + dangles 3'=-110 5'=-30", -326, turner_like, lambda f: -110 * dangles(f)[0] - 30 * dangles(f)[1]),
    mk("Turner-2004-like + coax -326", -326, turner_like, lambda f: -326 if f.flush else 0),
    mk("Turner-2004-like + coax -326 + dangles", -326, turner_like, lambda f: (-326 if f.flush else 0) - 110 * dangles(f)[0] - 30 * dangles(f)[1]),
]


def e_tiling(mod, n, m, M):
    f = lambda s: mod.g(Face(s))
    e = M * f("C-C=G-G=") + f("C=G|") + f("C|G=")
    if n - m > 0:
        e += (n - m) * f("C=G-G=C|")
    if m - 1 > 0:
        e += (m - 1) * f("A-G=C|C=G-")
    return e


if __name__ == "__main__":
    insts = [i for i in dict.fromkeys(test_main.INSTANCES) if i[1] * i[2] <= 10 and i[3] != "L"]
    data = []
    for a, m, B, mode in insts:
        res = run_enum(system(a, m, B), prune=(mode in "PL"), orbit=(mu_fact(a) <= 24 and m * B <= 10))
        faces = {i: Face(s) for i, s in res["desc"].items()}
        data.append((a, m, B, packable(a, m, B), res, faces))
    ny = sum(d[3] for d in data)
    print("instances: %d (YES %d, NO %d)" % (len(data), ny, len(data) - ny))
    print("%-52s | %-28s | %-34s | %s" % ("model", "NO: MFE > E_til ? (ok/bad)", "YES: MFE == E_til ? (ok/bad)", "YES: minima == tilings ? (ok/bad)   first counterexample"))
    for mod in MODELS:
        no_ok = no_bad = yes_ok = yes_bad = til_ok = til_bad = 0
        ex = None
        mingap = None
        for a, m, B, pk, res, faces in data:
            n = len(a)
            M = m * B - n
            et = e_tiling(mod, n, m, M)
            h = evaluate(res, mod, faces)
            mfe = min(h)
            if pk:
                # consistency: tiling structures really have energy E_til
                for e, (l_, p_, t_) in h.items():
                    assert (t_ == 0) or (e == et), (mod.name, a, m, B, e, et)
                if mfe == et:
                    yes_ok += 1
                else:
                    yes_bad += 1
                    ex = ex or ("YES %s m=%d B=%d: MFE %d < E_til %d" % (a, m, B, mfe, et))
                if mfe == et and h[mfe][0] == h[mfe][2]:
                    til_ok += 1
                else:
                    til_bad += 1
                    ex = ex or ("YES %s m=%d B=%d: %d minima, %d tilings" % (a, m, B, h[mfe][0], h[mfe][2]))
            else:
                if mfe > et:
                    no_ok += 1
                    mingap = (mfe - et) if mingap is None else min(mingap, mfe - et)
                else:
                    no_bad += 1
                    ex = ex or ("NO %s m=%d B=%d: MFE %d <= E_til %d" % (a, m, B, mfe, et))
        print("%-52s | %3d / %3d  min gap %-9s | %3d / %3d %22s | %3d / %3d   %s" % (
            mod.name, no_ok, no_bad, mingap, yes_ok, yes_bad, "", til_ok, til_bad, ex or ""))
