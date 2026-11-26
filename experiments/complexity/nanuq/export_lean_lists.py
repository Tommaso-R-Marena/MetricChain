"""Lists used by experiments/complexity/lean/NanuqFinite.lean.

The Lean file contains the literal list `C6` of the 108 systems of the substitution closure on six points, each
system as the sorted list of the canonical bitmasks of its non-trivial splits (the side not containing point 0).
This script recomputes the closure (twin_trees.closure_systems) and

    python3 export_lean_lists.py            checks that the literal list in the Lean file equals the closure
    python3 export_lean_lists.py --print    prints T5 (16), C6 (108), G6 (127 locally good), T6 (150)
"""
import os, re, sys, ast
from splitsys import *
from localcrit import tree_generated_systems, local_ok
from twin_trees import closure_systems


def nontriv(n, s):
    return sorted(m for m in s if not is_trivial(n, m))


def fmt(lists):
    return "[" + ", ".join("[" + ", ".join(str(m) for m in l) + "]" for l in lists) + "]"


if __name__ == "__main__":
    c6 = sorted(nontriv(6, s) for s in closure_systems(6))
    if "--print" in sys.argv:
        t5 = sorted(nontriv(5, s) for s in tree_generated_systems(5))
        g6 = sorted(nontriv(6, s) for s in tree_generated_systems(6) if local_ok(6, s)[0])
        t6 = sorted(nontriv(6, s) for s in tree_generated_systems(6))
        print("T5 :=", fmt(t5))
        print("C6 :=", fmt(c6))
        print("G6 :=", fmt(g6))
        print("T6 :=", fmt(t6))
        print(len(t5), len(c6), len(g6), len(t6), file=sys.stderr)
    else:
        lean = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lean", "NanuqFinite.lean")
        src = open(lean).read()
        m = re.search(r"def C6 : List \(List Nat\) := (\[\[.*?\]\])\n", src, re.S)
        lean_c6 = ast.literal_eval(m.group(1))
        same = sorted(map(tuple, lean_c6)) == sorted(map(tuple, c6))
        print(f"closure on six points: {len(c6)} systems; literal list C6 in NanuqFinite.lean: {len(lean_c6)} systems; "
              f"equal: {same}")
        assert same
