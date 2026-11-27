"""Certified enclosures of `exp` and `log` at rational points, in exact integer arithmetic.

Mathematical basis.  The theory division's `exp_enclosure` (`proofs/Core/Rounding.lean`, **[V]**):
for `n > 0` Taylor terms and `k` halvings with `|q| <= 2**k`,

    expLo n k q  <=  exp q  <=  expHi n k q,
    expLo n k q = max(0, T - err) ** (2**k),   expHi n k q = (T + err) ** (2**k),
    x = q / 2**k,   T = sum_{m<n} x**m / m!,   err = |x|**n * (n + 1) / (n! * n).

Taken literally, the `2**k`-th powers are rationals of 10**4 to 10**6 bits for the exponents
that occur in Boltzmann factors.  We therefore round *outward* after every squaring: the lower
value is rounded down to `P` significant bits, the upper value up.  Soundness of that step is the
monotonicity of squaring on nonnegative numbers (`0 <= a' <= a  =>  a'**2 <= a**2`, and its
mirror image), applied `k` times, so that

    our lower value  <=  expLo n k q  <=  exp q  <=  expHi n k q  <=  our upper value.

Status of that last step: a paper argument of two lines (label [P], unrefereed; sent to the
theory division as item R-4 of STRUCTBIO-REQ-0003); everything is tested against high-precision
references (`tests/structbio/test_expo.py`, `tests/structbio/test_adversarial_expo_model_stability.py`).

Width (review STRUCTBIO-REV-0001, finding 19).  The enclosure theorem holds for every `n > 0`;
`n` is chosen here from the precision asked for and from the size of the argument, so that the
relative width `hi / lo - 1` is below `2**-bits` for *every* rational `q` and every `bits >= 0`
(derivation at `_terms`).  With the `n = 12` terms that were used for every argument until that
review, the width was `2**(k - 100)` at best, `k = 6 + bit length of |q|`: `2**-74` at
`|q| = 1e6` however many bits were asked for, and no information at all beyond `|q| = 2**105`.
Twelve terms are still what is used whenever they suffice (`bits + k <= 97`), and there the
results are bit for bit what they were — in particular for the Z checker's default precision
of 64 bits at every `|q| < 2**27`.

Everything here is integer arithmetic on Python integers; no floating point is used for any
bound.  (`log_bounds` uses a floating-point *guess* that is then certified through `exp_bounds`:
`exp_hi(a) <= z` proves `a <= log z` — the theory division's `le_log_of_expHi_le`.)
"""
from __future__ import annotations

import math
import operator
from fractions import Fraction

__all__ = ["exp_bounds", "exp_bounds_me", "log_bounds"]

_MIN_TERMS = 12      # Taylor terms n: at least this many
_EXTRA_HALVINGS = 6  # |x| <= 2**-6, so that err(n) <= 2**(-6n) * (n + 1) / (n! * n)   (12 terms: < 2**-100)


def _terms(bits: int, k: int) -> int:
    """Number `n` of Taylor terms for `bits` of precision after `k` squarings: the least `n >= 12`
    with `2**(k + 3) * err(n) <= 2**-bits`, decided exactly in integers (`err(n)` as bounded above).

    Why this gives `hi / lo - 1 < 2**-bits`.  Write `P = bits + k + 16` for the working precision.
    Before the squarings the two values differ by at most `2 * err + 2**(1 - P)` and are above
    0.98, so the logarithm of their ratio is below `2.05 * (err + 2**-P)`.  A squaring doubles the
    logarithm of the ratio, and its two roundings add at most `2.01 * 2**(1 - P)`.  After `k`
    squarings the logarithm of the ratio is below `2.05 * 2**k * err + 6.1 * 2**(k - P)`
    `<= (0.26 + 0.0001) * 2**-bits`, and `exp(y) - 1 <= y + y*y` for `0 <= y <= 1`."""
    n = _MIN_TERMS
    while ((n + 1) << (bits + k + 3)) > ((math.factorial(n) * n) << (6 * n)):
        n += 1
    return n


def _round_down(m: int, e: int, bits: int):
    shift = m.bit_length() - bits
    return (m >> shift, e + shift) if shift > 0 else (m, e)


def _round_up(m: int, e: int, bits: int):
    shift = m.bit_length() - bits
    return (-((-m) >> shift), e + shift) if shift > 0 else (m, e)


def exp_bounds_me(q: Fraction, bits: int = 80):
    """`((m_lo, e_lo), (m_hi, e_hi))` with `m_lo * 2**e_lo <= exp(q) <= m_hi * 2**e_hi`, the
    mantissas being nonnegative integers of at most `bits + k + 17` bits, where
    `k = 6 + bit length of the integer part of |q|` is the number of squarings.

    Width: `hi / lo - 1 < 2**-bits`, for every `q` and every natural number `bits` (see the
    module docstring; `ValueError` for a negative `bits`, `TypeError` for one that is not an
    integer).  A larger `bits` never makes the enclosure wrong: it costs time here (the working
    precision is `bits + k + 16` bits, with `k` squarings and exact Taylor arithmetic on the
    denominator of `q`), and a consumer that converts the mantissas to another number format has
    limits of its own — the float tier of the Z checker accepts at most 512 bits."""
    bits = int(operator.index(bits))
    if bits < 0:
        raise ValueError("bits must be a natural number")
    q = Fraction(q)
    if q == 0:
        return (1, 0), (1, 0)
    k = max(0, (abs(q.numerator) // q.denominator).bit_length()) + _EXTRA_HALVINGS   # |q| <= 2**(k - extra)
    while abs(q) > Fraction(2) ** (k - _EXTRA_HALVINGS):                             # exact guard of the hypothesis
        k += 1
    x = q / (2 ** k)
    terms = _terms(bits, k)
    term = Fraction(1)
    taylor = Fraction(0)
    for m in range(terms):
        taylor += term
        term = term * x / (m + 1)
    err = abs(x) ** terms * Fraction(terms + 1, math.factorial(terms) * terms)
    lo0 = max(Fraction(0), taylor - err)
    hi0 = taylor + err
    prec = bits + k + 16                       # the first rounding error is doubled by each squaring
    m_lo, e_lo = (lo0.numerator << prec) // lo0.denominator, -prec                    # floor
    m_hi, e_hi = -((-hi0.numerator << prec) // hi0.denominator), -prec                # ceiling
    for _ in range(k):
        m_lo, e_lo = _round_down(m_lo * m_lo, 2 * e_lo, prec)
        m_hi, e_hi = _round_up(m_hi * m_hi, 2 * e_hi, prec)
    return (m_lo, e_lo), (m_hi, e_hi)


def _to_fraction(m: int, e: int) -> Fraction:
    return Fraction(m * 2 ** e) if e >= 0 else Fraction(m, 2 ** (-e))


def exp_bounds(q: Fraction, bits: int = 80):
    """Rationals `lo <= exp(q) <= hi` with `hi / lo - 1 < 2**-bits` (see `exp_bounds_me`).

    The rationals have about `1.44 * |q| + bits` bits: whoever calls this with an argument taken
    from untrusted input bounds `|q|` first (the Z checker evaluates `|q| <= 2**16`);
    `exp_bounds_me` returns the same enclosure as mantissa/exponent pairs of bounded size."""
    (m_lo, e_lo), (m_hi, e_hi) = exp_bounds_me(q, bits)
    return _to_fraction(m_lo, e_lo), _to_fraction(m_hi, e_hi)


def log_bounds(z: Fraction, bits: int = 40):
    """Rationals `lo <= log(z) <= hi` for a positive rational `z`, of width about `2**-bits`
    relative to `max(1, |log z|)`.  Each bound is *certified through the exponential*: `lo` is
    returned only after `exp_hi(lo) <= z` has been checked exactly, `hi` only after
    `z <= exp_lo(hi)`."""
    z = Fraction(z)
    if z <= 0:
        raise ValueError("log_bounds needs a positive argument")
    guess = math.log(z.numerator) - math.log(z.denominator)      # a guess; certified below
    delta = Fraction(max(1.0, abs(guess))) / (2 ** bits)
    for _ in range(60):
        lo = Fraction(guess) - delta
        hi = Fraction(guess) + delta
        if exp_bounds(lo, bits + 24)[1] <= z <= exp_bounds(hi, bits + 24)[0]:
            return lo, hi
        delta *= 4
    raise ArithmeticError("could not certify a logarithm enclosure")
