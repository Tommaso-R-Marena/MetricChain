"""Instances, resource limits and serialisation shared by the drivers of GEOMETRY-REQ-0006.

NOT TRUSTED (bookkeeping), except `dec_down` / `dec_up`, which turn exact numbers into decimal
strings rounded in the stated direction (exact integer arithmetic).
"""
from __future__ import annotations

import json
import math
import resource
from fractions import Fraction as Fr
from pathlib import Path

from flint import arb

from gr6_kernel import to_fraction

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
MEMORY_LIMIT = 3_000_000_000


def limit_memory():
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT, MEMORY_LIMIT))


# ------------------------------------------------------------------ instances
PAIRS_A = [(0, 4), (0, 5), (1, 4), (1, 6), (2, 6)]

# Instance A of the request.  `theta_request` are the torsions of the request; `couplings` are the
# stress of (F u E0, X(theta_request)) restricted to F (unit stress vector, sign as in the
# request), rounded to six decimals: the certified statements are about these rationals.
INSTANCE_A = dict(
    name="A", n=7, pairs=PAIRS_A,
    theta_request=[1.517404361415525, -1.046332870741514, 2.7119835539236874, -1.6743919325698102],
    couplings=[Fr(-317197, 10 ** 6), Fr(185025, 10 ** 6), Fr(307367, 10 ** 6), Fr(-150204, 10 ** 6), Fr(115451, 10 ** 6)],
)

# Control: the same graph at a conformation whose stress matrix is semidefinite of rank 3 (found by
# our own random search over torsions, gr6_search.py); couplings = minus the unit stress on F (so that
# the conformation maximises H_c), rounded to six decimals.
CONTROL_PSD = dict(
    name="control-PSD", n=7, pairs=PAIRS_A,
    theta_request=[2.4644, -1.7802, 0.1149, -2.2217],
    couplings=[Fr(192830, 10 ** 6), Fr(-182034, 10 ** 6), Fr(-123365, 10 ** 6), Fr(112213, 10 ** 6), Fr(-95743, 10 ** 6)],
)


# ------------------------------------------------------------------ serialisation
def fr(x):
    x = Fr(x)
    return f"{x.numerator}/{x.denominator}"


def dec_down(x, digits=30):
    """Decimal string <= the exact number x (an exact ball or a Fraction)."""
    x = x if isinstance(x, Fr) else to_fraction(x)
    return _dec(Fr(math.floor(x * 10 ** digits), 10 ** digits), digits)


def dec_up(x, digits=30):
    """Decimal string >= the exact number x (an exact ball or a Fraction)."""
    x = x if isinstance(x, Fr) else to_fraction(x)
    return _dec(Fr(math.ceil(x * 10 ** digits), 10 ** digits), digits)


def _dec(q, digits):
    sign = "-" if q < 0 else ""
    num = abs(q.numerator) * (10 ** digits // q.denominator)
    whole, frac = divmod(num, 10 ** digits)
    return f"{sign}{whole}.{frac:0{digits}d}"


def interval(lo, hi, digits=30):
    """[lower, upper] decimal strings enclosing the interval of exact numbers [lo, hi]."""
    return [dec_down(lo, digits), dec_up(hi, digits)]


def enclosure(x, digits=30):
    """[lower, upper] decimal strings enclosing the ball x."""
    return interval(x.lower(), x.upper(), digits)


def box_json(box):
    return [[fr(lo), fr(hi)] for lo, hi in box]


def radians(tau):
    """A ball containing pi * tau (tau a ball or a Fraction)."""
    return (arb(tau.numerator) / tau.denominator if isinstance(tau, Fr) else tau) * arb.pi()


def write_json(name, data):
    RESULTS.mkdir(exist_ok=True)
    path = RESULTS / name
    path.write_text(json.dumps(data, indent=1) + "\n")
    return path
