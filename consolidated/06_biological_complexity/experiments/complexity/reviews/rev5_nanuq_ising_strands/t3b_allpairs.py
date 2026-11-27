# t3b: Theorem 10'(d) for ALL 30 (system, missing 2-split) pairs at their own least m, all 4 clade orientations
import sys
sys.argv = [sys.argv[0]]
exec(open('t3_thm10prime.py').read().split("# (d): for the least m")[0])
none_cnt = 0; found = []
for S6, zi, F4, F5z, F5w, least, okf in results:
    for variant in ((True, True), (True, False), (False, True), (False, False)):
        Sm, nm, idm = blowup(S6, zi, least, variant)
        M = nanuq2(Sm, nm)
        o = kalmanson_some_order([[int(x) for x in row] for row in M], nontrivial_only=True)
        if o is None: none_cnt += 1
        else: found.append((show(S6, 6), zi, least, variant, o))
        if least == 1: break
print("all 30 pairs at their least m: no Kalmanson order in", none_cnt, "cases; order exists in", len(found))
for f in found[:10]: print("  ORDER FOUND", f)
