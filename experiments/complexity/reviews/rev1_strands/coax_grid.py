# coax_grid.py -- locate the exact threshold for coaxial stacking x (flush nicked stacks) as a function of
# the penalty gamma of bulge/interior loops (sigma = -100).  Referee's claim to test:
#   reduction valid (NO => MFE > E_til, YES => minima are exactly the tilings)  iff  |x| < |sigma| + min(|sigma|, gamma)
from lib import *
import test_main
from fragility import e_tiling, mk, S

insts = [i for i in dict.fromkeys(test_main.INSTANCES) if i[1] * i[2] <= 10 and i[3] != "L"]
data = []
for a, m, B, mode in insts:
    res = run_enum(system(a, m, B), prune=(mode in "PL"), orbit=(mu_fact(a) <= 24 and m * B <= 10))
    faces = {i: Face(s) for i, s in res["desc"].items()}
    data.append((a, m, B, packable(a, m, B), res, faces))

def valid(mod):
    bad = None
    for a, m, B, pk, res, faces in data:
        n = len(a); M = m * B - n
        et = e_tiling(mod, n, m, M)
        h = evaluate(res, mod, faces)
        mfe = min(h)
        if pk:
            if not (mfe == et and h[mfe][0] == h[mfe][2]):
                return False, ("YES", a, m, B, mfe, et, h[mfe])
        else:
            if not mfe > et:
                return False, ("NO", a, m, B, mfe, et)
    return True, None

print("gamma : largest |x| for which the reduction is valid on all %d instances (scan x = -1..-260)" % len(data))
for gamma, label, fn in [
    (0, "all bulge/int = 0", lambda g: (lambda f: 0)),
    (10, "all bulge/int = 10", lambda g: (lambda f: g)),
    (30, "all bulge/int = 30", lambda g: (lambda f: g)),
    (60, "all bulge/int = 60", lambda g: (lambda f: g)),
    (99, "all bulge/int = 99", lambda g: (lambda f: g)),
    (100, "all bulge/int = 100", lambda g: (lambda f: g)),
    (150, "all bulge/int = 150", lambda g: (lambda f: g)),
    (30, "only the pure A-bulge = 30, others 0", lambda g: (lambda f: g if (f.kind == "bulge" and f.tside == "A") else 0)),
    (60, "only the pure A-bulge = 60, others 0", lambda g: (lambda f: g if (f.kind == "bulge" and f.tside == "A") else 0)),
    (150, "only the pure A-bulge = 150, others 0", lambda g: (lambda f: g if (f.kind == "bulge" and f.tside == "A") else 0)),
]:
    pred = -(100 + min(100, gamma))
    xs = sorted(set([0, -50, -99, -100, -101, pred + 1, pred, pred - 1, -150, -199, -200, -201, -250]), reverse=True)
    out = []
    for x in xs:
        mod = mk("x", S, fn(gamma), (lambda xx: (lambda f: xx if f.flush else 0))(x))
        v, ex = valid(mod)
        out.append("%d:%s" % (x, "ok" if v else "FAIL"))
    print("%-40s predicted valid iff x > %d | %s" % (label, pred, "  ".join(out)), flush=True)
