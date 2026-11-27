#!/usr/bin/env python3
"""r29_i1_mutworker.py <instrumented mutant .py> u J K  --  independent verdict on one (mutated) copy of z6_certified_tops.py.

The file given is a copy of the theory division's script with (a) possibly one mutation and (b) two inserted
logging statements (see r29_i1_mutations.py): every generated line is appended to the module-level list _R29LOG
as (alpha, beta, rho, e', th, a0, b0).  This worker imports it (its main() is not run), drives its step() for J
levels and checks every step with my exact checker (r29lib.check_step) -- certificates from the log; a stored line
that is not a logged image line is treated as the cap line and needs two certified witnesses.  It also counts
  * pairs that are TRULY invalid: th < theta_na(e') in 40-digit arithmetic (for the pairs my checker flags);
  * tops below the semi-analytic envelope top b_j (then the sequence is certainly not admissible);
  * (S1) failures and V'(c') > 1.
Prints one line starting with R29-MUT-RESULT followed by a Python dict literal.
"""
import importlib.util
import math
import sys
import traceback
from fractions import Fraction as Fr

import r29lib as R
import r29env as E

R.cap_memory()
R.DI.P = 160

path, u_str, JMAX, K = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
res = dict(path=path, crashed=None, steps=0, tops=[], viol=0, kinds={}, pair_flagged=0, pair_truly_invalid=0,
           below_env=0, min_top_minus_env=None, abar_ok=None, lines=0)


def load(path, argv):
    old = sys.argv
    sys.argv = argv
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("z6_mut", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.argv = old
    return mod


def kind(msg):
    for key, name in (("pair: e'", "pair e'"), ("pair: th", "pair th"), ("slope above", "slope"), ("beta below", "beta"),
                      ("cap", "cap"), ("uncertified", "uncertified line"), ("(S1)", "(S1) top"), ("V'(c') > 1", "V'(c')>1"),
                      ("V(c) > 1", "V(c)>1"), ("abar", "abar < a"), ("parent", "parent not a line of V"), ("beta < 0", "beta<0"),
                      ("top not in", "top range")):
        if key in msg:
            return name
    return "other"


try:
    z6 = load(path, [path, u_str, str(JMAX), str(K), "nocompare"])
    ufr = Fr(u_str)
    cube = R.CubeDI(ufr)
    mpP = R.CubeMP(ufr, dps=40)
    ABAR = Fr(z6.ABAR)
    res["abar_ok"] = bool(ABAR >= cube.A.hi_fr())
    envf = E.EnvSA(E.CubeF(float(ufr)), JMAX)

    def to_PL(V):
        return R.PL([(Fr(float(a_)), Fr(float(b_))) for a_, b_ in zip(V.al, V.be)], Fr(V.c))

    V = z6.Curve([], [], z6.ABAR)
    Vpl = to_PL(V)
    import mpmath
    for j in range(1, JMAX + 1):
        del z6._R29LOG[:]
        Vn = z6.step(V)
        recs = list(z6._R29LOG)
        Vn_pl = to_PL(Vn)
        img = {}
        for al, be, r_, e_, th_, a0, b0 in recs:
            key = (Fr(al), Fr(be))
            if key not in img:
                img[key] = ("img", (Fr(a0), Fr(b0)), Fr(r_), Fr(e_), Fr(th_))
        certs = {}
        Hfull = None
        for ln in Vn_pl.lines():
            if ln in img:
                certs[ln] = img[ln]
            else:                                   # not a logged image line: the cap line (or something uncertifiable)
                if Hfull is None:
                    Hfull = R.PL(list(img.keys()), Vn_pl.c)
                hl = Hfull.hull
                if len(hl) >= 2:
                    k = 1
                    while k + 1 < len(hl) and hl[k][0] < ln[0]:
                        k += 1
                    l1, l2 = (hl[k - 1][0], hl[k - 1][1]), (hl[k][0], hl[k][1])
                    certs[ln] = ("cap", (l1, img.get(l1)), (l2, img.get(l2)))
        bad = R.check_step(Vpl, Vn_pl, certs, cube, ABAR)
        # stored lines of their curve that my hull dropped are not checked by check_step: check them as well
        stored = [(Fr(float(a_)), Fr(float(b_))) for a_, b_ in zip(Vn.al, Vn.be)]
        extra = [ln for ln in stored if ln not in set(Vn_pl.lines())]
        if extra:
            bad.append("other: %d stored lines are not on the hull of the stored lines" % len(extra))
        for b in bad:
            kd = kind(b)
            res["kinds"][kd] = res["kinds"].get(kd, 0) + 1
        res["viol"] += len(bad)
        # truly invalid pairs among the distinct pairs of this level that my enclosures do not certify
        seen = set()
        for al, be, r_, e_, th_, a0, b0 in recs:
            if (r_, e_, th_) in seen:
                continue
            seen.add((r_, e_, th_))
            Eh, Th = cube.pair_enclosures(Fr(r_))
            if Fr(e_) < Eh.hi_fr() or Fr(th_) < Th.hi_fr():
                res["pair_flagged"] += 1
                if res["pair_flagged"] <= 400:
                    th_true = mpP.theta(mpmath.mpf(e_))             # theta_na(e') in 40 digits
                    if mpmath.mpf(th_) < th_true:
                        res["pair_truly_invalid"] += 1
        res["tops"].append(Vn.c)
        res["lines"] += len(stored)
        d = Vn.c - envf.b[j]
        if res["min_top_minus_env"] is None or d < res["min_top_minus_env"]:
            res["min_top_minus_env"] = d
        if d < -1e-12:
            res["below_env"] += 1
        res["steps"] = j
        V, Vpl = Vn, Vn_pl
except BaseException as ex:                             # an assertion of the mutant, or a crash: a result as well
    res["crashed"] = "%s: %s" % (type(ex).__name__, str(ex)[:120])
print("R29-MUT-RESULT " + repr(res))
R.finish("r29_i1_mutworker")
