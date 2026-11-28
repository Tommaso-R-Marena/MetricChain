"""T2 (d), finding F8: width and soundness of ``expo.exp_bounds_me`` at bits = 64 for large |q|, at a given SB worktree.

    <python with python-flint> experiments/eng/phase2_gaps/t2_f8.py <sb-worktree>

Width = log2(hi/lo - 1) (computed exactly from the integers); soundness checked against Arb (python-flint) at a
working precision well above the width.  Arguments: 1/3, 1e6, 1e9 (+1/7), 2^64 - 1/3, 2^200 + 1/5, and negatives.
"""
from __future__ import annotations

import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "src"))
from metricchain_sb.expo import exp_bounds_me  # noqa: E402
import flint  # noqa: E402

QS = [Fraction(1, 3), Fraction(10 ** 6) + Fraction(1, 7), Fraction(10 ** 9) + Fraction(1, 7), Fraction(2 ** 64) - Fraction(1, 3),
      Fraction(2 ** 200) + Fraction(1, 5)]


def log2_ratio_minus_one(lo: Fraction, hi: Fraction) -> float:
    r = hi / lo - 1
    if r == 0:
        return -math.inf
    return math.log2(r.numerator) - math.log2(r.denominator)


for sign in (1, -1):
    for q0 in QS:
        q = sign * q0
        t0 = time.perf_counter()
        try:
            (ml, el), (mh, eh) = exp_bounds_me(q, 64)
        except Exception as exc:  # noqa: BLE001
            print(json.dumps(dict(q=str(float(q)), raised=f"{type(exc).__name__}: {str(exc)[:80]}")))
            continue
        dt = time.perf_counter() - t0
        # hi/lo = (mh/ml) * 2^(eh-el): never materialise 2^el (el is about 1.44 q for large q)
        d = eh - el
        lo, hi = (Fraction(ml), Fraction(mh) * Fraction(2) ** d) if d >= 0 else (Fraction(ml) * Fraction(2) ** (-d), Fraction(mh))
        w = log2_ratio_minus_one(lo, hi)
        sound = None
        if abs(q) < 2 ** 40:       # Arb check where the exponent is representable without huge precision
            flint.ctx.prec = 256
            e = flint.arb(flint.fmpq(q.numerator, q.denominator)).exp()
            lo_a = flint.arb(flint.fmpz(ml)) * flint.arb(2) ** el
            hi_a = flint.arb(flint.fmpz(mh)) * flint.arb(2) ** eh
            sound = bool((lo_a <= e) and (e <= hi_a))
        else:                      # log-scale check: ln(lo) <= q <= ln(hi), with ln of m*2^e = ln m + e ln 2
            flint.ctx.prec = 512
            qa = flint.arb(flint.fmpq(q.numerator, q.denominator))
            ln_lo = flint.arb(flint.fmpz(ml)).log() + el * flint.arb(2).log() if ml > 0 else None
            ln_hi = flint.arb(flint.fmpz(mh)).log() + eh * flint.arb(2).log()
            sound = bool((ln_lo is None or ln_lo <= qa) and qa <= ln_hi)
        print(json.dumps(dict(q=str(float(q)), log2_relative_width=w, width_below_2_to_minus_64=bool(w < -64), sound_by_arb=sound,
                              mantissa_bits=(ml.bit_length(), mh.bit_length()), seconds=round(dt, 4))), flush=True)
