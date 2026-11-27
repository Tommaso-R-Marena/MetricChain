#!/usr/bin/env python3
"""r20_count.py -- count the connected unpseudoknotted labelled structures of packing instances (no face
decomposition), with a wall-clock cap per instance; used only to decide which instances fit the time limit.
Usage: python3 -I -B r20_count.py <instance-set> <cap seconds>"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r20_enum as E
import r20_theorem as T


class Cap(Exception):
    pass


def main():
    setname = sys.argv[1]
    cap = float(sys.argv[2])
    print("r20_count.py set", setname, "cap", cap, "s per instance")
    for (a, m, B) in T.INSTANCE_SETS[setname]:
        n = len(a)
        strands = ["A".join(["G" * B] * m)] + ["C" * x for x in a]
        t0 = time.time()
        cnt = [0]
        done_orders = 0
        capped = False

        def visit(partner):
            cnt[0] += 1
            if cnt[0] % 20000 == 0 and time.time() - t0 > cap:
                raise Cap()

        try:
            for order in E.cyclic_orders(n + 1):
                E.enum_noncrossing(E.Circle(strands, order), E.WATSON_CRICK, visit, prune_two_nicks=True)
                done_orders += 1
        except Cap:
            capped = True
        nord = 1
        for i in range(2, n + 1):
            nord *= i
        dt = time.time() - t0
        print("a=%s m=%d B=%d  N=%d orders=%d : %s%d structures in %.1f s (%d orders done)%s" % (
            list(a), m, B, m * B + m - 1 + sum(a), nord, ">= " if capped else "", cnt[0], dt, done_orders,
            ("  extrapolated total ~ %.2e" % (cnt[0] * nord / max(done_orders, 0.5))) if capped else ""))
        sys.stdout.flush()
    print("END r20_count.py")


if __name__ == "__main__":
    main()
