#!/usr/bin/env python3
"""r20_rerun_check_true.py -- RE-RUN of the reviewed division's enumerator (rerun_copy/ref_enum.py, unmodified)
with its option check=True, which their two test scripts never pass although the note (section 1, Fact 1) says that
Fact 1 is "re-checked exhaustively by the enumerator's check=True mode against a union-find computation".
For every case below ALL non-crossing structures over all orders are enumerated (connected_only=False) and their code
asserts, for each, that "no face has two nicks" agrees with their union-find over strands.
Also counts connected structures, for comparison with my own enumeration.
Usage: python3 -I -B r20_rerun_check_true.py"""
import os
import sys
import time

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "rerun_copy"))
import ref_enum as R  # noqa: E402  (their module, unmodified)

CASES = [([1, 2, 1, 2], 2, 3), ([2, 2, 2], 2, 3), ([3, 1, 1, 1], 2, 3), ([3, 3], 2, 3), ([1, 1, 1, 3], 2, 3),
         ([2, 2, 1, 1], 2, 3), ([2, 2, 3, 1], 2, 4), ([3, 3, 2], 2, 4), ([3, 3, 1, 1], 2, 4), ([2, 2, 2, 2], 2, 4)]


def loop_energy(kind, face, seq):
    return -1 if kind == "stack" else 0


def main():
    t0 = time.time()
    print("r20_rerun_check_true.py: their enumerate_structures(..., connected_only=False, check=True)")
    tot = 0
    for items, m, B in CASES:
        strands = ["A".join(["G" * B] * m)] + ["C" * a for a in items]
        n_all = 0
        n_conn = 0
        try:
            for order, lab, e, kinds in R.enumerate_structures(strands, loop_energy, connected_only=False, check=True):
                n_all += 1
                if "disconnected" not in kinds:
                    n_conn += 1
            status = "no assertion failed"
        except AssertionError as ex:
            status = "ASSERTION FAILED: %r" % (ex,)
        tot += n_all
        print("items=%s m=%d B=%d: non-crossing (order, structure) pairs=%d, connected=%d: %s" % (items, m, B, n_all, n_conn, status))
        sys.stdout.flush()
    print("total structures checked: %d; elapsed %.1f s" % (tot, time.time() - t0))
    print("END r20_rerun_check_true.py")


if __name__ == "__main__":
    main()
