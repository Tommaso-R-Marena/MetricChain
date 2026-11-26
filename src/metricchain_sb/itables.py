"""Interval factor tables: nonnegative tables known only through entrywise lower and upper bounds,
with the two operations that variable elimination needs — product and sum over one axis.

Two arithmetic tiers implement the same interface.

``ExactTables`` — entries are `fractions.Fraction`; every operation is exact, so the lower
(upper) table of a product or sum is the product or sum of the lower (upper) tables, and is a
valid lower (upper) bound because all entries are nonnegative.

``FloatTables`` — entries are IEEE-754 binary64 numbers, each table carrying a common binary
exponent `shift` (true value = stored value * 2**shift).  Rigor rests on three facts, stated
here because they are the *floating-point assumptions* of every result of this tier:

* F1 (products).  A correctly rounded product of two nonnegative doubles differs from the exact
  product by less than one unit in the last place of the result, also in the subnormal range.
  We move every computed product one representable number outward (`numpy.nextafter`), so the
  lower table stays a lower bound and the upper table an upper bound.
* F2 (sums).  The computed sum `s'` of `m` nonnegative doubles, in *any* order of summation and
  with any intermediate precision of at least binary64, satisfies
  `s (1 - g) <= s' <= s (1 + g)` with `g = (m-1)u / (1 - (m-1)u)`, `u = 2**-53` (Higham,
  *Accuracy and Stability of Numerical Algorithms*, 2nd ed., §4.2; additions cannot underflow
  inexactly).  We multiply the computed sum by `1 -/+ m 2**-52` (which exceeds what is needed)
  and move one representable number outward.
* F3 (range).  Lower bounds below `1e-300` are replaced by `0` and positive upper bounds are
  kept at or above `1e-300`, so no input of an operation is subnormal and the bounds do not
  depend on flush-to-zero settings; an overflow (a non-finite upper bound) is an error and
  aborts the computation.

Assumed and not proved here: that `numpy` multiplies and adds doubles as IEEE-754 round-to-nearest
operations on this platform (F1, F2 are stated for such operations), and that `numpy.nextafter`
returns the adjacent double.  Label of results of this tier: rigorous *under these assumptions*.
"""
from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

__all__ = ["ExactTables", "FloatTables", "IntervalTable", "TableTooLarge"]

_TINY = 1e-300


class TableTooLarge(RuntimeError):
    """A table would exceed the memory budget: the computation is abandoned (an abstention)."""


class IntervalTable:
    """`scope` = sorted tuple of sites; `lo`, `hi` arrays with one axis per site of the scope;
    true values lie in `[lo, hi] * 2**shift`."""

    __slots__ = ("scope", "lo", "hi", "shift")

    def __init__(self, scope, lo, hi, shift=0):
        self.scope, self.lo, self.hi, self.shift = tuple(scope), lo, hi, shift


class ExactTables:
    name = "exact"

    def from_me_bounds(self, scope, lo_me, hi_me, shape):
        """Table from mantissa/exponent pairs `(m, e)` (value `m * 2**e`, `m >= 0`), kept exactly."""
        def frac(m, e):
            return Fraction(m * 2 ** e) if e >= 0 else Fraction(m, 2 ** (-e))
        lo = np.empty(len(lo_me), dtype=object)
        hi = np.empty(len(hi_me), dtype=object)
        lo[:] = [frac(m, e) for m, e in lo_me]
        hi[:] = [frac(m, e) for m, e in hi_me]
        return IntervalTable(scope, lo.reshape(shape), hi.reshape(shape), 0)

    def multiply(self, a: IntervalTable, b: IntervalTable, sizes, max_entries):
        scope = tuple(sorted(set(a.scope) | set(b.scope)))      # the product lives on the union of the scopes
        _guard(scope, sizes, max_entries)
        la, ha = _expand(a, scope, sizes), _expand_hi(a, scope, sizes)
        lb, hb = _expand(b, scope, sizes), _expand_hi(b, scope, sizes)
        return IntervalTable(scope, la * lb, ha * hb, 0)

    def sum_out(self, t: IntervalTable, site):
        axis = t.scope.index(site)
        scope = t.scope[:axis] + t.scope[axis + 1:]
        lo = np.sum(t.lo, axis=axis)
        hi = np.sum(t.hi, axis=axis)
        if not scope:                                   # numpy returns a bare Fraction for a full reduction
            lo, hi = _scalar(lo), _scalar(hi)
        return IntervalTable(scope, lo, hi, 0)

    def bounds(self, t: IntervalTable):
        """Exact rational lower and upper bounds, as flat lists in C order."""
        return [Fraction(v) for v in np.asarray(t.lo, dtype=object).reshape(-1)], \
               [Fraction(v) for v in np.asarray(t.hi, dtype=object).reshape(-1)]


def _scalar(v):
    out = np.empty((), dtype=object)
    out[()] = v
    return out


def _expand(t, scope, sizes):
    shape = [sizes[s] if s in t.scope else 1 for s in scope]
    return np.asarray(t.lo, dtype=t.lo.dtype if hasattr(t.lo, "dtype") else object).reshape(shape)


def _expand_hi(t, scope, sizes):
    shape = [sizes[s] if s in t.scope else 1 for s in scope]
    return np.asarray(t.hi, dtype=t.hi.dtype if hasattr(t.hi, "dtype") else object).reshape(shape)


def _guard(scope, sizes, max_entries):
    entries = 1
    for s in scope:
        entries *= sizes[s]
    if max_entries is not None and entries > max_entries:
        raise TableTooLarge(f"a table over sites {list(scope)} would have {entries} entries (budget {max_entries})")


class FloatTables:
    name = "float"

    # ---- directed conversions of exact data ------------------------------------------------
    @staticmethod
    def _down(m: int) -> float:
        """Largest double not above the nonnegative integer `m`."""
        f = float(m)
        return math.nextafter(f, 0.0) if int(f) > m else f

    @staticmethod
    def _up(m: int) -> float:
        f = float(m)
        return math.nextafter(f, math.inf) if int(f) < m else f

    def from_me_bounds(self, scope, lo_me, hi_me, shape):
        """Table from mantissa/exponent pairs `(m, e)` (value `m * 2**e`, `m >= 0`)."""
        shift = max((m.bit_length() + e for m, e in hi_me if m > 0), default=0)
        lo = np.empty(len(lo_me), dtype=np.float64)
        hi = np.empty(len(hi_me), dtype=np.float64)
        for idx, ((ml, el), (mh, eh)) in enumerate(zip(lo_me, hi_me)):
            lo[idx] = self._ldexp_down(self._down(ml), el - shift)
            hi[idx] = self._ldexp_up(self._up(mh), eh - shift) if mh > 0 else 0.0
        return IntervalTable(scope, lo.reshape(shape), hi.reshape(shape), shift)

    @staticmethod
    def _ldexp_down(f: float, e: int) -> float:
        if f == 0.0 or e < -2000:
            return 0.0
        v = math.ldexp(f, e)                           # exact unless it underflows
        return v if v >= _TINY else 0.0

    @staticmethod
    def _ldexp_up(f: float, e: int) -> float:
        if e < -2000:
            return _TINY
        v = math.ldexp(f, e)
        if math.isinf(v):
            raise OverflowError("weight above the double range after scaling")
        return v if v >= _TINY else _TINY

    # ---- the two operations ------------------------------------------------------------------
    @staticmethod
    def _finish(lo, hi, positive):
        lo = np.where(lo < _TINY, 0.0, lo)
        hi = np.where(positive, np.maximum(hi, _TINY), 0.0)
        if not np.all(np.isfinite(hi)):
            raise OverflowError("an upper bound left the double range")
        return lo, hi

    def multiply(self, a: IntervalTable, b: IntervalTable, sizes, max_entries):
        scope = tuple(sorted(set(a.scope) | set(b.scope)))      # the product lives on the union of the scopes
        _guard(scope, sizes, max_entries)
        la, ha, lb, hb = _expand(a, scope, sizes), _expand_hi(a, scope, sizes), _expand(b, scope, sizes), _expand_hi(b, scope, sizes)
        lo = np.nextafter(la * lb, 0.0)                                   # F1
        hi = np.nextafter(ha * hb, np.inf)
        lo, hi = self._finish(lo, hi, (ha > 0) & (hb > 0))
        return self._renormalise(IntervalTable(scope, lo, hi, a.shift + b.shift))

    def sum_out(self, t: IntervalTable, site):
        axis = t.scope.index(site)
        m = t.lo.shape[axis]
        c = m * 2.0 ** -52                                                # F2
        if c >= 0.25:
            raise TableTooLarge("an axis is too long for the summation bound")
        lo = np.nextafter(np.sum(t.lo, axis=axis) * (1.0 - c), 0.0)
        raw_hi = np.sum(t.hi, axis=axis)
        hi = np.nextafter(raw_hi * (1.0 + c), np.inf)
        lo, hi = self._finish(np.asarray(lo), np.asarray(hi), np.asarray(raw_hi) > 0)
        return self._renormalise(IntervalTable(t.scope[:axis] + t.scope[axis + 1:], lo, hi, t.shift))

    def _renormalise(self, t: IntervalTable) -> IntervalTable:
        """Divide by a power of two so that the largest upper bound is in [1/2, 1) (keeps products
        away from overflow and underflow).  The scaling is itself rounded outward."""
        top = float(np.max(t.hi)) if t.hi.size else 0.0
        if top <= 0.0:
            return t
        e = math.frexp(top)[1]
        if e == 0:
            return t
        scale = math.ldexp(1.0, -e)
        lo = np.nextafter(t.lo * scale, 0.0)
        hi = np.nextafter(t.hi * scale, np.inf)
        lo, hi = self._finish(lo, hi, t.hi > 0)
        return IntervalTable(t.scope, lo, hi, t.shift + e)

    def bounds(self, t: IntervalTable):
        two = Fraction(2) ** t.shift if t.shift >= 0 else Fraction(1, 2 ** (-t.shift))
        return [Fraction(float(v)) * two for v in np.asarray(t.lo).reshape(-1)], \
               [Fraction(float(v)) * two for v in np.asarray(t.hi).reshape(-1)]
