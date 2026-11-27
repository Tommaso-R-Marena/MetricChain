"""Campaign Z4: their certified exponential and logarithm against two independent enclosures.

``expo.exp_bounds_me(q, bits)`` (mantissa/exponent pairs; what their checker uses for Boltzmann factors) and
``expo.exp_bounds(q, bits)`` (rationals; what it uses for the factors of the steps) are compared, for many rationals
``q`` and several ``bits``, with an Arb ball at ``bits + 200`` bits and with the Taylor enclosure of ``indep_zcheck``
(integer arithmetic, written here).  A bound is *violated* only when it is on the wrong side of the whole reference
enclosure (certified); it is *confirmed* when it is on the right side of the whole enclosure.  The relative width is
recorded per magnitude class.  ``expo.log_bounds`` is tested the same way, and for monotonicity (it is the source of
the float-tier intervals that do not contain the exact-tier ones, see the Z3 campaign).

    python campaign_z4.py --seed 1 --cases 20000
"""
from __future__ import annotations

import resource

resource.setrlimit(resource.RLIMIT_AS, (3_000_000_000, 3_000_000_000))

import argparse  # noqa: E402
import collections  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import random  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from fractions import Fraction  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import indep_zcheck as Z  # noqa: E402
import sb_bridge as B  # noqa: E402

CLASSES = ["zero", "tiny", "small", "unit", "tens", "hundreds", "1e4", "1e6", "1e9", "2^64", "2^200", "2^1000",
           "many_digits", "dyadic_edge", "near_integer_ln2"]


def random_q(rng: random.Random, cls: str) -> Fraction:
    sign = rng.choice([-1, 1])
    if cls == "zero":
        return Fraction(0)
    if cls == "tiny":
        return sign * Fraction(rng.randint(1, 10 ** 6), 10 ** rng.randint(8, 400))
    if cls == "small":
        return sign * Fraction(rng.randint(1, 10 ** 6), 10 ** rng.randint(6, 9))
    if cls == "unit":
        return sign * Fraction(rng.randint(1, 4 * 10 ** 6), 10 ** 6)
    if cls == "tens":
        return sign * Fraction(rng.randint(1, 10 ** 8), 10 ** 6)
    if cls == "hundreds":
        return sign * Fraction(rng.randint(10 ** 8, 10 ** 9), 10 ** 6)
    if cls == "1e4":
        return sign * Fraction(rng.randint(10 ** 9, 10 ** 11), 10 ** 6)
    if cls == "1e6":
        return sign * Fraction(rng.randint(10 ** 11, 10 ** 13), rng.randint(1, 10 ** 6))
    if cls == "1e9":
        return sign * Fraction(rng.randint(10 ** 14, 10 ** 16), rng.randint(1, 10 ** 6))
    if cls == "2^64":
        return sign * Fraction(rng.randint(2 ** 60, 2 ** 70), rng.randint(1, 1000))
    if cls == "2^200":
        return sign * Fraction(rng.randint(2 ** 150, 2 ** 210), rng.randint(1, 1000))
    if cls == "2^1000":
        return sign * Fraction(rng.randint(2 ** 900, 2 ** 1010), rng.randint(1, 1000))
    if cls == "many_digits":
        return sign * Fraction(rng.randint(1, 10 ** 300), rng.randint(1, 10 ** 300))
    if cls == "dyadic_edge":                                # |q| at and next to powers of two (the halving guard)
        p = rng.randint(-70, 70)
        return sign * (Fraction(2) ** p + rng.choice([0, 0, 1, -1]) * Fraction(1, 2 ** rng.randint(60, 300)))
    k = rng.randint(1, 10 ** 6)                              # near an integer multiple of ln 2: exp(q) near 2**k
    return sign * (Fraction(k) * Fraction(6243314768165359, 9007199254740992) + Fraction(rng.randint(-3, 3), 10 ** 20))


def log2_ratio(hi, lo) -> float:
    """log2((hi - lo) / lo) for dyadic pairs (``-inf`` when equal)."""
    (mh, eh), (ml, el) = hi, lo
    apart = (mh.bit_length() + eh) - (ml.bit_length() + el)
    if apart > 4000:                                         # the enclosure spans more than 4000 binary orders
        return float(apart) if apart < 10 ** 300 else math.inf
    e = min(eh, el)
    a, b = mh << (eh - e), ml << (el - e)
    if a == b:
        return -math.inf
    num, den = a - b, b
    return (num.bit_length() - den.bit_length()) + math.log2((num / (1 << num.bit_length())) /
                                                             (den / (1 << den.bit_length())))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--cases", type=int, default=20000)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    expo = B.sb()["expo"]
    t0 = time.time()
    tally = collections.Counter()
    width = collections.defaultdict(list)
    violations = []
    exceptions = collections.Counter()
    seconds = collections.defaultdict(float)
    calls = collections.Counter()
    for case in range(args.cases):
        cls = rng.choice(CLASSES)
        q = random_q(rng, cls)
        bits = rng.choice([80, 64, 64, 64, 40, 24, 8, 1, 0, -8, 120, 300])
        tally["cases"] += 1
        t1 = time.perf_counter()
        try:
            lo, hi = expo.exp_bounds_me(q, bits)
        except Exception as exc:                                   # noqa: BLE001
            exceptions[f"exp_bounds_me bits={bits}: {type(exc).__name__}"] += 1
            continue
        if bits == 64:
            seconds[cls] += time.perf_counter() - t1
            calls[cls] += 1
        if type(lo[0]) is not int or type(hi[0]) is not int or lo[0] < 0 or hi[0] < 0:
            tally["malformed_result"] += 1
            violations.append({"what": "malformed result", "q": str(q), "bits": bits})
            continue
        ref_bits = max(bits, 64) + 200
        if 0 < abs(q) < 1:                                         # resolve exp(q) - 1 as well
            ref_bits += (q.denominator // abs(q.numerator)).bit_length()
        refs = (("arb", Z.exp_enclosure_arb(q, ref_bits)), ("taylor", Z.exp_enclosure_taylor(q, ref_bits)))
        low = {name: ("confirmed" if Z._dy_le(lo, r_lo) else "VIOLATED" if not Z._dy_le(lo, r_hi) else "undecided")
               for name, (r_lo, r_hi) in refs}
        upp = {name: ("confirmed" if Z._dy_le(r_hi, hi) else "VIOLATED" if not Z._dy_le(r_lo, hi) else "undecided")
               for name, (r_lo, r_hi) in refs}
        for side, verdicts in (("lower", low), ("upper", upp)):
            for name, v in verdicts.items():
                tally[f"{side}_{v}_{name}"] += 1
            if "VIOLATED" in verdicts.values():
                tally[f"{side}_VIOLATED"] += 1
                violations.append({"what": f"{side} bound on the wrong side of exp(q)", "q": str(q), "bits": bits,
                                   "verdicts": verdicts})
            elif "confirmed" in verdicts.values():
                tally[f"{side}_confirmed"] += 1
            else:
                tally[f"{side}_undecided"] += 1
        if not (Z._dy_le(refs[0][1][0], refs[1][1][1]) and Z._dy_le(refs[1][1][0], refs[0][1][1])):
            tally["REFERENCES_DISJOINT"] += 1
            violations.append({"what": "the two references are disjoint", "q": str(q), "bits": bits})
        if lo[0] > 0:
            w = log2_ratio(hi, lo)
            if bits in (64, 80):
                width[f"{cls} bits={bits}"].append(w)
            if q != 0 and w > -bits + 4 and bits in (24, 40, 64, 80):
                tally[f"wider_than_2^-(bits-4)_bits={bits}"] += 1
                tally[f"wider_than_2^-(bits-4)_bits={bits}_{cls}"] += 1
        else:
            tally["lower_bound_zero"] += 1
            tally[f"lower_bound_zero_{cls}"] += 1
        # the rational form, where it can be materialised
        if abs(q) <= 10 ** 5 and bits >= -8:
            try:
                f_lo, f_hi = expo.exp_bounds(q, bits)
                same = (f_lo == Z._dy_fraction(lo) and f_hi == Z._dy_fraction(hi))
                tally["exp_bounds_equals_me_form"] += same
                tally["exp_bounds_differs_from_me_form"] += (not same)
            except Exception as exc:                               # noqa: BLE001
                exceptions[f"exp_bounds bits={bits}: {type(exc).__name__}"] += 1

    # --- log_bounds --------------------------------------------------------------------------------------------
    logt = collections.Counter()
    log_width = []
    for case in range(args.cases // 10):
        kind = rng.choice(["near1", "moderate", "big", "small", "huge_fraction", "integer"])
        if kind == "near1":
            z = 1 + Fraction(rng.randint(-10 ** 6, 10 ** 6), 10 ** rng.randint(7, 40))
        elif kind == "moderate":
            z = Fraction(rng.randint(1, 10 ** 9), rng.randint(1, 10 ** 9))
        elif kind == "big":
            z = Fraction(rng.randint(1, 10 ** 300), rng.randint(1, 10 ** 3))
        elif kind == "small":
            z = Fraction(rng.randint(1, 10 ** 3), rng.randint(1, 10 ** 300))
        elif kind == "integer":
            z = Fraction(rng.randint(1, 4096))
        else:                                                      # a moderate value with a huge numerator and denominator
            d = rng.randint(10 ** 2000, 10 ** 2001)
            z = Fraction(d * rng.randint(1, 1000) + rng.randint(0, 10 ** 1990), d)
        logt["cases"] += 1
        try:
            lo, hi = expo.log_bounds(z)
        except Exception as exc:                                   # noqa: BLE001
            exceptions[f"log_bounds {kind}: {type(exc).__name__}"] += 1
            continue
        # reference: ln z as an Arb ball through exact integers
        num_lo, num_hi = Z.ln_enclosure((z.numerator, 0), 300)
        den_lo, den_hi = Z.ln_enclosure((z.denominator, 0), 300)
        r_lo, r_hi = num_lo - den_hi, num_hi - den_lo
        if lo <= r_lo:
            logt["lower_confirmed"] += 1
        elif lo > r_hi:
            logt["lower_VIOLATED"] += 1
            violations.append({"what": "log_bounds lower above ln z", "z": str(z)[:200]})
        else:
            logt["lower_undecided"] += 1
        if hi >= r_hi:
            logt["upper_confirmed"] += 1
        elif hi < r_lo:
            logt["upper_VIOLATED"] += 1
            violations.append({"what": "log_bounds upper below ln z", "z": str(z)[:200]})
        else:
            logt["upper_undecided"] += 1
        rel = (hi - lo) / max(Fraction(1), abs(r_lo))
        log_width.append(float(rel) * 2 ** 40)
        if kind == "huge_fraction":
            logt["huge_fraction_cases"] += 1
            logt["huge_fraction_wider_than_4x_2^-40"] += rel > 4 * Fraction(1, 2 ** 40)
    # monotonicity of the lower bound: z1 < z2 but lo(z1) > lo(z2)
    mono = collections.Counter()
    worst = Fraction(0)
    for case in range(args.cases // 10):
        z1 = Fraction(rng.randint(10 ** 6, 10 ** 9), rng.randint(1, 10 ** 6))
        z2 = z1 * (1 + Fraction(1, 10 ** rng.randint(13, 18)))
        mono["pairs"] += 1
        lo1, hi1 = expo.log_bounds(z1)
        lo2, hi2 = expo.log_bounds(z2)
        if lo1 > lo2:
            mono["lower_not_monotone"] += 1
            worst = max(worst, (lo1 - lo2) / max(Fraction(1), abs(lo1)))
        if hi1 > hi2:
            mono["upper_not_monotone"] += 1

    def stats(v):
        v = sorted(v)
        return {"n": len(v), "min": v[0], "median": v[len(v) // 2], "max": v[-1]} if v else {"n": 0}

    out = {"campaign": "z4", "seed": args.seed, "cases": args.cases, "seconds": round(time.time() - t0, 1),
           "exp": dict(tally), "exp_exceptions": dict(exceptions),
           "exp_log2_relative_width": {k: stats(v) for k, v in sorted(width.items())},
           "exp_microseconds_per_call_bits64": {k: round(1e6 * seconds[k] / calls[k], 1) for k in sorted(calls)},
           "log": dict(logt), "log_width_in_units_of_2^-40": stats(log_width),
           "log_monotonicity": dict(mono), "log_worst_inversion_relative": float(worst),
           "violations": violations[:20]}
    path = Path(args.out) if args.out else HERE / "results" / "z4.json"
    path.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("seconds", "exp", "exp_exceptions", "log", "log_monotonicity",
                                          "log_worst_inversion_relative")}, indent=1))
    for k, v in out["exp_log2_relative_width"].items():
        print(f"  width {k:28s} {v}")
    print("  us/call", out["exp_microseconds_per_call_bits64"])
    print("  log width (units of 2^-40)", out["log_width_in_units_of_2^-40"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
