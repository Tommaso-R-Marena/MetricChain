#!/usr/bin/env python3
"""Assemble RemainderIdentityTheory.lean = parts/Theory_head.txt + Parts 1-6 of
RemainderIdentity.lean (verbatim) + parts/Theory_tail.txt + the `#print axioms` lines.

The files of this directory cannot import each other (they are not in the lake library).
RemainderIdentity.lean imports Mathlib only and carries verbatim copies of the theory division's
definitions (its Part 0); the generated file has the same Parts 1-6 on top of the theory
division's compiled `proofs.Frontiers.HigherOrderEnvelope`, so that the theorems are about
`MetricChain.mixedDiff`, `MetricChain.anchoredInterp`; the tail restates three of them with those
names written out.
Run from anywhere:  python3 experiments/science/ws_L4/assemble.py
"""
import os

here = os.path.dirname(os.path.abspath(__file__))

EXTRA_AXIOMS = ("#print axioms ScienceL4.remainder_identity_theory\n"
                "#print axioms ScienceL4.higherOrder_remainder_of_identity\n"
                "#print axioms ScienceL4.anchored_sandwich_theory\n")


def build():
    src = open(os.path.join(here, "RemainderIdentity.lean")).read()
    start = src.index("/-! ## Part 1:")
    end = src.index("end ScienceL4")
    body = src[start:end]
    axioms = src[src.index("/-! ## Axioms -/"):]
    # item 1 is the theory division's own theorem in this file
    axioms = axioms.replace("#print axioms ScienceL4.anchored_decomposition\n",
                            "#print axioms MetricChain.anchored_decomposition\n")
    head = open(os.path.join(here, "parts", "Theory_head.txt")).read()
    tail = open(os.path.join(here, "parts", "Theory_tail.txt")).read()
    marker = "/-! # Parts 1–6: repeated verbatim from `RemainderIdentity.lean` -/\n\n"
    return head + marker + body + "end ScienceL4\n\n" + tail + axioms + EXTRA_AXIOMS


if __name__ == "__main__":
    out = build()
    open(os.path.join(here, "RemainderIdentityTheory.lean"), "w").write(out)
    print("RemainderIdentityTheory.lean written:", out.count("\n"), "lines")
