#!/usr/bin/env python3
"""Independent checker for certificates of two-sided bounds on ``ln Z`` (file format ``structbio-zcert/1``).

Written by the Computational Research Division from the *specification* published by the structural-biology
division -- its request STRUCTBIO-REQ-0004 and the docstrings of its modules ``zcert``, ``zcheck``, ``expo``,
``itables`` and ``model`` at its commit 0544ff4 -- and not from its code: no body of its checker, loader or
validator had been read when this file was frozen (the reading log and the freeze time are in
``results/freeze.json``).  Nothing of that package is imported or copied here.

What is checked
---------------
The instance is a pairwise model with integer tables in units ``u = 2**-scale_bits``,

    E(x) = sum_i H_i(x_i) + sum_{(i, j) listed, i < j} J_ij(x_i, x_j),      Z(B) = sum_{x in B} exp(-beta E(x)),

and the certificate is a tree of nodes replayed on a working model ``(H, J)`` and a working box ``D``:

* ``prune(site i, remove r, dominator t)``: with the margin
  ``m = H_i(r) - H_i(t) + sum_{j ~ i} min_{s in D_j} (J_ij(r, s) - J_ij(t, s))`` of the working model and box,
  ``Z(D without r) <= Z(D) <= (1 + exp(-beta m)) Z(D without r)``; then ``r`` leaves ``D_i``.
* ``relax(pair [i, j], f, g)``: with ``R(a, b) = J_ij(a, b) - f(a) - g(b)`` and ``r_lo <= R <= r_hi`` on
  ``D_i x D_j``, the pair is removed, ``f`` and ``g`` are added to ``H_i`` and ``H_j``, and
  ``exp(-beta r_hi) Z' <= Z <= exp(-beta r_lo) Z'``.
* a leaf sums every site but the kept one out of the working model on the working box;
* a branch node on site ``i`` has one child per state of the working ``D_i`` and ``Z(D) = sum_a Z(D, x_i = a)``.

The interval that the rules prove (the *ideal interval* of the certificate) is defined by recursion on the tree,

    lo(node) = exp(-beta sum_relax r_hi) * inner_lo,
    hi(node) = exp(-beta sum_relax r_lo) * prod_prune (1 + exp(-beta m)) * inner_hi,
    inner_lo = inner_hi = Z(working model, working box) at a leaf;  the sums of the children's lo, hi at a branch,

and is ``[ln lo(root), ln hi(root)]``.  With a kept site ``t`` every node also carries, for each state ``a`` of ``t``,
``low_a(node) = exp(-beta sum_relax r_hi) * (Z(working, x_t = a) at a leaf | sum of the children's low_a)``, and

    P(x_t = a) >= low_a(root) / hi(root),      P(x_t = a) <= 1 - sum_{b != a} low_b(root) / hi(root).

These are real numbers; this checker returns rigorous rational enclosures of them.

Arithmetic
----------
Steps (margins, residual ranges, working tables): Python integers, exact.  Every exponential ``exp(q)`` at a rational
``q`` is enclosed by two dyadic rationals ``m 2**e`` (``m``, ``e`` Python integers): by default from an Arb ball
(python-flint) at ``exp_bits + 32`` bits, or from a Taylor sum with a proved remainder written here
(``exp_impl="taylor"``; no library).  Sums and products of the tables are done on the pairs ``(m, e)``: exactly
(``round_bits=None``, the default: the result is the exact rational value of the sum of products of the enclosed
weights) or with every result rounded outward to ``round_bits`` significant bits (lower table down, upper table up;
bounded memory for long products and astronomically large exponents).  The final logarithms are Arb enclosures
(with ``exp_impl="taylor"`` they are in addition certified through the Taylor exponential, so that Arb is then only a
source of guesses).  No binary floating point is used anywhere.

Besides the certified interval ``[ln_z_lo, ln_z_hi]`` the result gives two-sided enclosures of *each end* of the ideal
interval (``ideal_lo``, ``ideal_hi``), so that another checker's interval can be compared with what the rules prove:
a checker that implements these rules with outward rounding must return ``lo <= ideal_lo`` and ``hi >= ideal_hi``.

Readings adopted where the specification is silent (each is listed in the report as an ambiguity)
---------------------------------------------------------------------------------------------------
R1  File: a JSON object with exactly the keys ``format``, ``model_sha256``, ``beta``, ``domains``, ``keep``,
    ``claim``, ``root``, ``meta`` (layout learnt from the output of their serialiser on three hand-built objects;
    no docstring states it).  Key order and insignificant whitespace are free.  Duplicate keys, floats, exponents,
    ``NaN``/``Infinity``, ``-0``, booleans or strings where integers are required, and unknown or missing keys at
    any level are errors.
R2  Rationals (``beta``, the claim) are text ``p/q`` in lowest terms with ``q >= 1``, no sign on zero, no leading
    zeros, no ``+`` (``"10/1"``, ``"-5/3"``, ``"0/1"``).
R3  ``model_sha256`` is the SHA-256 of ``json.dumps({"pair": {"i,j": rows}, "scale_bits": s, "unary": rows},
    sort_keys=True, separators=(",", ":"))`` (read from the body of their ``mincert.model_sha256``: the docstrings
    only say "canonical JSON of scale and tables").
R4  ``beta >= 0`` is required (both rules are stated for an inverse temperature and are false for ``beta < 0``).
R5  ``domains``: one strictly increasing, non-empty list of states per site (a box is a product of sets; an empty
    box has ``Z = 0`` and no logarithm).
R6  ``prune``: ``r`` and ``t`` are distinct states of the working ``D_i`` (the inequality is false otherwise); the
    margin may have any sign (the inequality is true for every margin when ``beta >= 0``); ``j ~ i`` ranges over
    the pairs still present in the working model.
R7  ``relax``: the pair must still be present in the working model; it may be written in either orientation, ``f``
    belonging to the first site named; ``f`` and ``g`` have one integer per state of the site (all ``k`` states,
    not only those of the working domain).
R8  A leaf's ``order`` is a permutation of all sites except the kept one -- including sites fixed by conditioning,
    which have one state left.
R9  A branch names any site but the kept one (a site with one state left is allowed) and its ``children`` are keyed
    by the decimal states of the working domain of that site, exactly (no child missing, none in surplus).
R10 ``claim`` is ``{}`` or has exactly ``ln_z_lo`` and ``ln_z_hi``; it is accepted iff it contains the interval
    computed *here* (which is tighter than any outward-rounded checker's: a claim accepted by them is accepted
    here, not conversely).  ``meta`` is a string and is not interpreted.
R11 Populations are reported for every state of the root domain of the kept site; a state that survives in no leaf
    has the interval ``[0, removed_upper]``.

Limits of this implementation (reported as abstentions, never as acceptances): tables above ``max_entries``
entries; in the exact mode, Boltzmann factors ``exp(q)`` with ``|q| > max_exact_exponent`` (use ``round_bits``; the
rounded mode stops at ``|q| >= 2**256``); ``|scale_bits| > 65536``; JSON nested deeper than the parser's recursion
limit; integers of more than 4300 digits.

The checker never raises: every failure is a ``Result`` with ``accepted = False``, a reason and a ``kind``
(``malformed``, ``invalid``, ``abstain``, ``claim``; ``internal`` would be a defect of this file).

    python indep_zcheck.py CERTIFICATE.json MODEL.json        # MODEL.json: {"scale_bits":..,"unary":..,"pair":{"i,j":..}}
"""
from __future__ import annotations

import hashlib
import itertools
import json
import re
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from math import gcd

FORMAT_TAG = "structbio-zcert/1"
TOP_KEYS = frozenset({"format", "model_sha256", "beta", "domains", "keep", "claim", "root", "meta"})
PRUNE_KEYS = frozenset({"op", "site", "remove", "dominator"})
RELAX_KEYS = frozenset({"op", "pair", "f", "g"})
LEAF_KEYS = frozenset({"steps", "order"})
BRANCH_KEYS = frozenset({"steps", "branch", "children"})
CLAIM_KEYS = frozenset({"ln_z_lo", "ln_z_hi"})

_RATIONAL_RE = re.compile(r"(0|-?[1-9][0-9]*)/([1-9][0-9]*)\Z")
_STATE_KEY_RE = re.compile(r"(0|[1-9][0-9]*)\Z")
_SHA_RE = re.compile(r"[0-9a-f]{64}\Z")

ONE = (1, 0)                      # the dyadic number 1 = 1 * 2**0
_RATIO_LIMIT = 1 << 16            # a ratio below 2**-65536 is reported as the interval [0, 2**-65536]


class Reject(Exception):
    """Not accepted.  ``kind``: malformed | invalid | abstain | claim | internal."""

    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind
        self.reason = reason


# ------------------------------------------------------------------------------------------------ the instance

@dataclass(frozen=True)
class Model:
    """Pairwise model with integer tables in units ``2**-scale_bits``; ``pair[(i, j)][a][b]`` with ``i < j``."""
    unary: tuple
    pair: dict
    scale_bits: int

    @property
    def n(self) -> int:
        return len(self.unary)

    @property
    def sizes(self) -> tuple:
        return tuple(len(u) for u in self.unary)


def make_model(unary, pair, scale_bits=0) -> Model:
    """Validate plain Python tables (lists of ``int``) and freeze them.  Raises ``Reject('malformed', ...)``."""
    if type(scale_bits) is not int:
        raise Reject("malformed", "model: scale_bits is not an integer")
    if type(unary) not in (list, tuple):
        raise Reject("malformed", "model: unary is not a list")
    rows = []
    for i, row in enumerate(unary):
        if type(row) not in (list, tuple) or len(row) == 0:
            raise Reject("malformed", f"model: unary table of site {i} is not a non-empty list")
        if any(type(v) is not int for v in row):
            raise Reject("malformed", f"model: unary table of site {i} has a non-integer entry")
        rows.append(tuple(row))
    n = len(rows)
    if type(pair) is not dict:
        raise Reject("malformed", "model: pair is not a dict")
    tables = {}
    for key, table in pair.items():
        if type(key) is not tuple or len(key) != 2 or type(key[0]) is not int or type(key[1]) is not int:
            raise Reject("malformed", f"model: pair key {key!r} is not a pair of integers")
        i, j = key
        if not 0 <= i < j < n:
            raise Reject("malformed", f"model: pair key {key!r} is not i < j within range")
        if type(table) not in (list, tuple) or len(table) != len(rows[i]):
            raise Reject("malformed", f"model: pair table {key!r} has the wrong number of rows")
        out = []
        for r in table:
            if type(r) not in (list, tuple) or len(r) != len(rows[j]) or any(type(v) is not int for v in r):
                raise Reject("malformed", f"model: pair table {key!r} has a malformed row")
            out.append(tuple(r))
        tables[(i, j)] = tuple(out)
    return Model(tuple(rows), tables, scale_bits)


def model_sha256(model: Model) -> str:
    """Reading R3 of the module docstring."""
    doc = {"scale_bits": model.scale_bits,
           "unary": [list(u) for u in model.unary],
           "pair": {f"{i},{j}": [list(r) for r in t] for (i, j), t in model.pair.items()}}
    try:
        text = json.dumps(doc, sort_keys=True, separators=(",", ":"))
    except ValueError as exc:                    # an integer of more than 4300 digits
        raise Reject("abstain", f"model: cannot serialise the tables ({exc})") from None
    return hashlib.sha256(text.encode()).hexdigest()


def model_from_json(text: str) -> Model:
    """Model from the canonical JSON of R3 (``{"scale_bits": s, "unary": [...], "pair": {"i,j": [...]}}``)."""
    doc = parse_json_strict(text)
    if type(doc) is not dict or set(doc) != {"scale_bits", "unary", "pair"} or type(doc["pair"]) is not dict:
        raise Reject("malformed", "model file: expected an object with scale_bits, unary and pair")
    pair = {}
    for key, table in doc["pair"].items():
        parts = key.split(",")
        if len(parts) != 2 or not all(_STATE_KEY_RE.match(p) and len(p) < 19 for p in parts):
            raise Reject("malformed", f"model file: pair key {key!r}")
        pair[(int(parts[0]), int(parts[1]))] = table
    return make_model(doc["unary"], pair, doc["scale_bits"])


# ------------------------------------------------------------------------------------------- dyadic arithmetic
# A nonnegative dyadic number is a pair (m, e) of Python integers, value m * 2**e, m >= 0.

class _Arith:
    """Products and sums of nonnegative dyadic numbers, exact (``bits is None``) or rounded in one direction."""
    __slots__ = ("up", "bits", "gap")

    def __init__(self, up: bool, bits):
        self.up = up
        self.bits = bits
        self.gap = None if bits is None else 2 * bits + 4

    def rnd(self, m: int, e: int):
        bits = self.bits
        if bits is not None:
            s = m.bit_length() - bits
            if s > 0:
                return ((-((-m) >> s)) if self.up else (m >> s)), e + s
        return m, e

    def mul(self, a, b):
        return self.rnd(a[0] * b[0], a[1] + b[1])

    def add(self, a, b):
        ma, ea = a
        mb, eb = b
        if ma == 0:
            return b
        if mb == 0:
            return a
        if ea < eb:
            ma, ea, mb, eb = mb, eb, ma, ea
        d = ea - eb
        if self.gap is not None and d >= self.gap:
            # rounded mode: every mantissa has at most bits + 1 bits, so b < 2**(bits + 1 + eb) <= 2**(ea - bits - 3)
            if not self.up:
                return ma, ea
            s = self.bits + 3
            return self.rnd((ma << s) + 1, ea - s)
        return self.rnd((ma << d) + mb, eb)


def _dy_le(a, b) -> bool:
    """a <= b for nonnegative dyadic numbers, without shifting by more than a mantissa length."""
    ma, ea = a
    mb, eb = b
    if ma == 0:
        return True
    if mb == 0:
        return False
    ta, tb = ma.bit_length() + ea, mb.bit_length() + eb
    if ta != tb:
        return ta < tb
    if ea >= eb:
        return (ma << (ea - eb)) <= mb
    return ma <= (mb << (eb - ea))


def _dy_fraction(a) -> Fraction:
    m, e = a
    return Fraction(m << e) if e >= 0 else Fraction(m, 1 << -e)


def _ratio_dn(a, b) -> Fraction:
    """A rational lower bound of a / b (exact unless the ratio is below 2**-_RATIO_LIMIT, then 0)."""
    if a[0] == 0:
        return Fraction(0)
    mag = a[0].bit_length() + a[1] - b[0].bit_length() - b[1]
    if mag < -_RATIO_LIMIT:
        return Fraction(0)
    if mag > _RATIO_LIMIT:
        raise Reject("abstain", "a ratio of bounds is out of range")
    d = a[1] - b[1]
    return Fraction(a[0] << d, b[0]) if d >= 0 else Fraction(a[0], b[0] << -d)


def _ratio_up(a, b) -> Fraction:
    """A rational upper bound of a / b (exact unless the ratio is below 2**-_RATIO_LIMIT, then 2**-_RATIO_LIMIT)."""
    if a[0] == 0:
        return Fraction(0)
    mag = a[0].bit_length() + a[1] - b[0].bit_length() - b[1]
    if mag < -_RATIO_LIMIT:                      # a / b < 2**(mag + 1) <= 2**-_RATIO_LIMIT
        return Fraction(1, 1 << _RATIO_LIMIT)
    if mag > _RATIO_LIMIT:
        raise Reject("abstain", "a ratio of bounds is out of range")
    d = a[1] - b[1]
    return Fraction(a[0] << d, b[0]) if d >= 0 else Fraction(a[0], b[0] << -d)


# ------------------------------------------------------------------------------------- exponential and logarithm

def _arb_fraction(x) -> Fraction:
    m, e = x.man_exp()
    m, e = int(m), int(e)
    return Fraction(m << e) if e >= 0 else Fraction(m, 1 << -e)


def exp_enclosure_arb(q: Fraction, bits: int):
    """``((m_lo, e_lo), (m_hi, e_hi))`` with ``m_lo 2**e_lo <= exp(q) <= m_hi 2**e_hi`` from an Arb ball.

    The ball of ``exp`` is computed at ``bits + 32 + log2|q|`` bits (the rational ``q`` enters as a ball of that
    precision, so the relative width of the result is below ``2**-bits``); its end points are exact dyadic numbers.
    """
    if q == 0:
        return ONE, ONE
    from flint import arb, ctx, fmpq
    old = ctx.prec
    try:
        ctx.prec = bits + 32 + max(0, (abs(q.numerator) // q.denominator).bit_length())
        ball = arb(fmpq(q.numerator, q.denominator)).exp()
        if not ball.is_finite():
            raise Reject("abstain", "an exponential is out of the range of the multiprecision library")
        lo, hi = ball.lower().man_exp(), ball.upper().man_exp()
    finally:
        ctx.prec = old
    lo, hi = (int(lo[0]), int(lo[1])), (int(hi[0]), int(hi[1]))
    if lo[0] <= 0 or hi[0] <= 0:
        raise Reject("abstain", "an exponential is out of the range of the multiprecision library")
    return lo, hi


def exp_enclosure_taylor(q: Fraction, bits: int):
    """The same enclosure in integer arithmetic only (no library), with the proof in the comments.

    For ``0 <= x = |q| / 2**k <= 1/2``:  ``T_N(x) = sum_{m < N} x**m / m!  <=  exp(x)  <=  T_N(x) + 2 x**N / N!``
    (the tail is at most ``x**N / N! * 1 / (1 - x / (N + 1)) <= 2 x**N / N!``).  Lower sums are computed with every
    term rounded down and ``x`` rounded down, upper sums with every term and ``x`` rounded up, so they bracket.
    Then ``exp(|q|) = exp(x)**(2**k)``: ``k`` squarings, the lower value rounded down and the upper value rounded
    up after each (squaring is increasing on nonnegative numbers).  For ``q < 0`` the two reciprocals, rounded
    outward.
    """
    if q == 0:
        return ONE, ONE
    x = -q if q < 0 else q
    k = (-((-x.numerator) // x.denominator)).bit_length() + 1        # ceil(x) < 2**(k - 1), so x / 2**k < 1/2
    work = bits + 2 * k + 64                                         # fractional bits of the Taylor sums
    keep = bits + k + 32                                             # significant bits kept after each squaring
    one = 1 << work
    den = x.denominator << k
    x_dn = (x.numerator << work) // den
    x_up = -((-(x.numerator << work)) // den)
    lo, term, m = one, one, 0
    while term:
        m += 1
        term = (term * x_dn) // (m << work)                          # floor: a lower bound of x**m / m!
        lo += term
    hi, term, m = one, one, 0
    while True:
        m += 1
        term = -((-(term * x_up)) // (m << work))                    # ceil: an upper bound of x**m / m!
        if term <= 1:                                                # x**m / m! <= 2**-work: tail <= 2 * term
            hi += 2 * term
            break
        hi += term
    dn, up = _Arith(False, keep), _Arith(True, keep)
    a, b = (lo, -work), (hi, -work)
    for _ in range(k):
        a = dn.rnd(a[0] * a[0], 2 * a[1])
        b = up.rnd(b[0] * b[0], 2 * b[1])
    if q > 0:
        return a, b
    sa, sb = a[0].bit_length() + keep, b[0].bit_length() + keep     # 1 / (m 2**e) = (2**s / m) 2**(-s - e)
    return ((1 << sb) // b[0], -sb - b[1]), (-((-(1 << sa)) // a[0]), -sa - a[1])


_EXP_IMPL = {"arb": exp_enclosure_arb, "taylor": exp_enclosure_taylor}


def ln_enclosure(v, bits: int, impl: str = "arb"):
    """Fractions ``lo <= ln(m 2**e) <= hi`` for a positive dyadic number ``v = (m, e)``.

    Arb ball of ``ln(m / 2**top) + (e + top) ln 2`` (no cancellation: the first term is in ``[0, ln 2)``).  With
    ``impl="taylor"`` each end is moved outward by ``2**-(bits - 8)`` (relative
    to ``max(1, |ln v|)``) and then *proved* with the Taylor exponential: ``exp_hi(lo) <= v`` and ``v <= exp_lo(hi)``.
    """
    m, e = v
    if m <= 0:
        raise Reject("internal", "logarithm of a non-positive bound")
    shift = (m & -m).bit_length() - 1                 # canonical form: equal values get equal enclosures
    m, e = m >> shift, e + shift
    v = (m, e)
    if m == 1 and e == 0:
        return Fraction(0), Fraction(0)
    from flint import arb, ctx, fmpz
    top = m.bit_length() - 1                          # v = (m / 2**top) * 2**(e + top), the first factor in [1, 2)
    old = ctx.prec
    try:
        ctx.prec = bits + 64 + abs(e + top).bit_length()
        ball = (arb(fmpz(m)) / arb(fmpz(1 << top))).log() + arb(fmpz(e + top)) * arb.const_log2()
        if not ball.is_finite():
            raise Reject("abstain", "a logarithm is out of the range of the multiprecision library")
        lo, hi = _arb_fraction(ball.lower()), _arb_fraction(ball.upper())
    finally:
        ctx.prec = old
    if impl == "taylor":
        step = max(Fraction(1), abs(lo), abs(hi)) / (1 << max(8, bits - 8))
        lo, hi = lo - step, hi + step
        if not _dy_le(exp_enclosure_taylor(lo, bits + 16)[1], v) or not _dy_le(v, exp_enclosure_taylor(hi, bits + 16)[0]):
            raise Reject("abstain", "a logarithm could not be certified through the Taylor exponential")
    return lo, hi


class _Weights:
    """Enclosures of ``exp(-beta * E * 2**-scale_bits)`` for integers ``E`` (table units), cached."""

    def __init__(self, beta: Fraction, scale_bits: int, exp_bits: int, round_bits, impl: str, max_exact_exponent: int):
        num, den = -beta.numerator, beta.denominator
        if scale_bits >= 0:
            den <<= scale_bits
        else:
            num <<= -scale_bits
        self.num, self.den = num, den
        self.exp_bits = exp_bits
        self.fn = _EXP_IMPL[impl]
        self.exact = round_bits is None
        self.limit = max_exact_exponent
        self.dn, self.up = _Arith(False, round_bits), _Arith(True, round_bits)
        self.cache = {}

    def get(self, energy: int):
        got = self.cache.get(energy)
        if got is None:
            q = Fraction(self.num * energy, self.den)
            size = abs(q.numerator) // q.denominator                 # floor |q|
            if size > (self.limit if self.exact else 1 << 256):
                raise Reject("abstain", "the exponent of a Boltzmann factor exceeds max_exact_exponent in absolute "
                                        "value: use round_bits" if self.exact else "a Boltzmann factor is out of range")
            lo, hi = self.fn(q, self.exp_bits)
            if not self.exact:
                lo, hi = self.dn.rnd(*lo), self.up.rnd(*hi)
            got = self.cache[energy] = (lo, hi)
        return got


# ------------------------------------------------------------------------------------------ strict file loading

def parse_json_strict(text):
    """RFC 8259 JSON with: no duplicate keys, integers only, no ``NaN``/``Infinity``, no ``-0``."""
    if type(text) is not str:
        raise Reject("malformed", "the certificate text is not a string")

    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise Reject("malformed", f"duplicate key {key[:40]!r}")
            out[key] = value
        return out

    def no_float(literal):
        raise Reject("malformed", f"non-integer number {literal[:40]!r}")

    def no_constant(literal):
        raise Reject("malformed", f"non-finite number {literal!r}")

    def strict_int(literal):
        if literal == "-0":
            raise Reject("malformed", "non-canonical integer '-0'")
        try:
            return int(literal)
        except ValueError:
            raise Reject("abstain", "an integer of more than 4300 digits") from None

    try:
        return json.loads(text, object_pairs_hook=pairs, parse_float=no_float, parse_constant=no_constant,
                          parse_int=strict_int)
    except Reject:
        raise
    except RecursionError:
        raise Reject("abstain", "JSON nested too deep for the parser") from None
    except ValueError as exc:
        raise Reject("malformed", f"not valid JSON: {exc}") from None


def _rational(value, what: str) -> Fraction:
    if type(value) is not str:
        raise Reject("malformed", f"{what}: not a rational written as text 'p/q'")
    match = _RATIONAL_RE.match(value)
    if not match:
        raise Reject("malformed", f"{what}: not a canonical rational 'p/q'")
    try:
        p, q = int(match.group(1)), int(match.group(2))
    except ValueError:
        raise Reject("abstain", f"{what}: an integer of more than 4300 digits") from None
    if gcd(p, q) != 1:
        raise Reject("malformed", f"{what}: rational not in lowest terms")
    return Fraction(p, q)


def _int(value, what: str) -> int:
    if type(value) is not int:
        raise Reject("malformed", f"{what}: not an integer")
    return value


def _int_list(value, what: str) -> tuple:
    if type(value) is not list:
        raise Reject("malformed", f"{what}: not a list")
    for v in value:
        if type(v) is not int:
            raise Reject("malformed", f"{what}: not a list of integers")
    return tuple(value)


def _steps(value, where) -> list:
    if type(value) is not list:
        raise Reject("malformed", f"{_path(where)}: steps is not a list")
    out = []
    for pos, step in enumerate(value):
        what = f"{_path(where)} step {pos}"
        if type(step) is not dict:
            raise Reject("malformed", f"{what}: not an object")
        op = step.get("op")
        if type(op) is not str:
            raise Reject("malformed", f"{what}: no 'op'")
        if op == "prune":
            if frozenset(step) != PRUNE_KEYS:
                raise Reject("malformed", f"{what}: a prune step has exactly the keys op, site, remove, dominator")
            out.append(("prune", _int(step["site"], what), _int(step["remove"], what), _int(step["dominator"], what)))
        elif op == "relax":
            if frozenset(step) != RELAX_KEYS:
                raise Reject("malformed", f"{what}: a relax step has exactly the keys op, pair, f, g")
            pair = _int_list(step["pair"], what)
            if len(pair) != 2:
                raise Reject("malformed", f"{what}: pair is not a list of two sites")
            out.append(("relax", pair[0], pair[1], _int_list(step["f"], what), _int_list(step["g"], what)))
        else:
            raise Reject("malformed", f"{what}: unknown op {op[:40]!r}")
    return out


def _path(where) -> str:
    parts = []
    while where is not None:
        where, key = where
        parts.append(str(key))
        if len(parts) > 12:
            parts.append("...")
            break
    return "root" + "".join("/" + p for p in reversed(parts))


def _node(doc) -> dict:
    """Structure of a tree of nodes (no recursion: the depth is limited by the JSON parser only)."""
    root = {}
    stack = [(doc, root, None)]
    while stack:
        raw, out, where = stack.pop()
        if type(raw) is not dict:
            raise Reject("malformed", f"{_path(where)}: a node is not an object")
        keys = frozenset(raw)
        if keys == LEAF_KEYS:
            out["steps"] = _steps(raw["steps"], where)
            out["order"] = _int_list(raw["order"], f"{_path(where)}: order")
        elif keys == BRANCH_KEYS:
            out["steps"] = _steps(raw["steps"], where)
            out["branch"] = _int(raw["branch"], f"{_path(where)}: branch")
            children = raw["children"]
            if type(children) is not dict:
                raise Reject("malformed", f"{_path(where)}: children is not an object")
            out["children"] = {}
            for key, sub in children.items():
                if type(key) is not str or not _STATE_KEY_RE.match(key) or len(key) > 18:
                    raise Reject("malformed", f"{_path(where)}: child key {str(key)[:40]!r} is not a canonical state")
                child = out["children"][int(key)] = {}
                stack.append((sub, child, (where, key)))
        else:
            raise Reject("malformed", f"{_path(where)}: a node has exactly the keys steps + order, or steps + branch "
                                      f"+ children")
    return root


@dataclass
class Certificate:
    beta: Fraction
    domains: list
    keep: object
    claim: object                 # None or (lo, hi)
    root: dict
    meta: str


def parse_document(doc, model: Model) -> Certificate:
    """Validate a parsed JSON document against the format and the instance (structure only; no replay)."""
    if type(model) is not Model:
        raise Reject("malformed", "the instance is not a Model of this module")
    if type(doc) is not dict:
        raise Reject("malformed", "the certificate is not a JSON object")
    keys = frozenset(doc)
    if keys != TOP_KEYS:
        missing = sorted(str(k) for k in TOP_KEYS - keys)
        surplus = sorted(str(k)[:40] for k in keys - TOP_KEYS)
        raise Reject("malformed", f"top-level keys: missing {missing}, unknown {surplus}")
    if type(doc["format"]) is not str or doc["format"] != FORMAT_TAG:
        raise Reject("malformed", "format is not 'structbio-zcert/1'")
    sha = doc["model_sha256"]
    if type(sha) is not str or not _SHA_RE.match(sha):
        raise Reject("malformed", "model_sha256 is not 64 lower-case hexadecimal digits")
    if sha != model_sha256(model):
        raise Reject("malformed", "model_sha256 is not the checksum of the instance")
    beta = _rational(doc["beta"], "beta")
    if beta < 0:
        raise Reject("invalid", "beta is negative: the prune and relax inequalities do not hold")
    sizes = model.sizes
    raw = doc["domains"]
    if type(raw) is not list or len(raw) != model.n:
        raise Reject("malformed", "domains is not a list with one entry per site")
    domains = []
    for i, dom in enumerate(raw):
        states = _int_list(dom, f"domain of site {i}")
        prev = -1
        for a in states:
            if not prev < a < sizes[i]:
                raise Reject("malformed", f"domain of site {i} is not strictly increasing within 0..{sizes[i] - 1}")
            prev = a
        if not states:
            raise Reject("invalid", f"domain of site {i} is empty: Z = 0 has no logarithm")
        domains.append(states)
    keep = doc["keep"]
    if keep is not None:
        if type(keep) is not int or not 0 <= keep < model.n:
            raise Reject("malformed", "keep is neither null nor a site")
    raw = doc["claim"]
    if type(raw) is not dict:
        raise Reject("malformed", "claim is not an object")
    if not raw:
        claim = None
    elif frozenset(raw) == CLAIM_KEYS:
        claim = (_rational(raw["ln_z_lo"], "claim ln_z_lo"), _rational(raw["ln_z_hi"], "claim ln_z_hi"))
    else:
        raise Reject("malformed", "claim is neither {} nor exactly {ln_z_lo, ln_z_hi}")
    root = _node(doc["root"])
    if type(doc["meta"]) is not str:
        raise Reject("malformed", "meta is not a string")
    return Certificate(beta, domains, keep, claim, root, doc["meta"])


# ------------------------------------------------------------------------------------------------------- replay

class _State:
    __slots__ = ("H", "pairs", "D")

    def __init__(self, H, pairs, D):
        self.H, self.pairs, self.D = H, pairs, D

    def child(self, site: int, state: int) -> "_State":
        D = list(self.D)
        D[site] = (state,)
        return _State([list(h) for h in self.H], dict(self.pairs), D)


class _Factors:
    """What the steps of one node have proved: prune margins and the sums of the relax ranges (table units)."""
    __slots__ = ("margins", "r_lo", "r_hi")

    def __init__(self):
        self.margins, self.r_lo, self.r_hi = [], 0, 0


def _apply_steps(steps, st: _State, sizes, acc: _Factors, stats: dict, where) -> None:
    n = len(sizes)
    for pos, step in enumerate(steps):
        if step[0] == "prune":
            _, i, r, t = step
            if not 0 <= i < n:
                raise Reject("invalid", f"{_path(where)} step {pos}: prune of a site that does not exist")
            dom = st.D[i]
            if r not in dom:
                raise Reject("invalid", f"{_path(where)} step {pos}: the removed state is not in the working domain")
            if t not in dom:
                raise Reject("invalid", f"{_path(where)} step {pos}: the dominator is not in the working domain")
            if r == t:
                raise Reject("invalid", f"{_path(where)} step {pos}: a state cannot dominate itself")
            margin = st.H[i][r] - st.H[i][t]
            for (p, q), table in st.pairs.items():
                if p == i:
                    row_r, row_t = table[r], table[t]
                    margin += min(row_r[s] - row_t[s] for s in st.D[q])
                elif q == i:
                    margin += min(table[s][r] - table[s][t] for s in st.D[p])
            st.D[i] = tuple(a for a in dom if a != r)
            acc.margins.append(margin)
            stats["prunes"] += 1
        else:
            _, i, j, f, g = step
            if not (0 <= i < n and 0 <= j < n) or i == j:
                raise Reject("invalid", f"{_path(where)} step {pos}: relax of a pair of sites that does not exist")
            key = (i, j) if i < j else (j, i)
            table = st.pairs.get(key)
            if table is None:
                raise Reject("invalid", f"{_path(where)} step {pos}: the pair is not in the working model")
            if len(f) != sizes[i] or len(g) != sizes[j]:
                raise Reject("invalid", f"{_path(where)} step {pos}: f, g must have one integer per state of the site")
            if i < j:
                residuals = [table[a][b] - f[a] - g[b] for a in st.D[i] for b in st.D[j]]
            else:
                residuals = [table[b][a] - f[a] - g[b] for a in st.D[i] for b in st.D[j]]
            acc.r_lo += min(residuals)
            acc.r_hi += max(residuals)
            st.H[i] = [h + v for h, v in zip(st.H[i], f)]
            st.H[j] = [h + v for h, v in zip(st.H[j], g)]
            del st.pairs[key]
            stats["relaxes"] += 1


def _eliminate(factors, order, D, keep, ar: _Arith, budget, stats):
    """Sum the sites of ``order`` out of a list of ``(scope, table)``; tables are dicts keyed by state tuples."""
    mul, add = ar.mul, ar.add
    for site in order:
        bucket = [f for f in factors if site in f[0]]
        factors = [f for f in factors if site not in f[0]]
        scope = sorted(set().union(*(f[0] for f in bucket)))
        rest = tuple(x for x in scope if x != site)
        size = 1
        for x in scope:
            size *= len(D[x])
        if budget is not None and size > budget:
            raise Reject("abstain", f"a table of {size} entries exceeds the budget of {budget}")
        if stats is not None:
            stats["max_table"] = max(stats["max_table"], size)
            stats["entries"] += size
        place = {x: p for p, x in enumerate(rest)}
        plans = [(tuple(-1 if x == site else place[x] for x in sc), table) for sc, table in bucket]
        states = D[site]
        out = {}
        for assign in itertools.product(*(D[x] for x in rest)):
            total = None
            for a in states:
                prod = None
                for index, table in plans:
                    v = table[tuple(a if p < 0 else assign[p] for p in index)]
                    prod = v if prod is None else mul(prod, v)
                total = prod if total is None else add(total, prod)
            out[assign] = total
        factors.append((rest, out))
    if keep is None:
        z = ONE
        for _, table in factors:
            z = mul(z, table[()])
        return z
    result = {}
    for a in D[keep]:
        v = ONE
        for sc, table in factors:
            v = mul(v, table[(a,)] if sc else table[()])
        result[a] = v
    return result


def _leaf(st: _State, order, keep, n: int, weights: _Weights, budget, stats, where):
    """Enclosures ``{a: (dn, up)}`` of ``Z(working, x_keep = a)`` (key ``None`` when no site is kept)."""
    if sorted(order) != [i for i in range(n) if i != keep]:
        raise Reject("invalid", f"{_path(where)}: order is not a permutation of all sites but the kept one")
    f_dn, f_up = [], []
    for i in range(n):
        h, t_dn, t_up = st.H[i], {}, {}
        for a in st.D[i]:
            t_dn[(a,)], t_up[(a,)] = weights.get(h[a])
        f_dn.append(((i,), t_dn))
        f_up.append(((i,), t_up))
    for (i, j), table in st.pairs.items():
        t_dn, t_up = {}, {}
        for a in st.D[i]:
            row = table[a]
            for b in st.D[j]:
                t_dn[(a, b)], t_up[(a, b)] = weights.get(row[b])
        f_dn.append(((i, j), t_dn))
        f_up.append(((i, j), t_up))
    z_dn = _eliminate(f_dn, order, st.D, keep, weights.dn, budget, stats)
    z_up = _eliminate(f_up, order, st.D, keep, weights.up, budget, None)
    stats["leaves"] += 1
    if keep is None:
        return {None: (z_dn, z_up)}
    return {a: (z_dn[a], z_up[a]) for a in st.D[keep]}


def _close(acc: _Factors, inner_lo, inner_hi, low, weights: _Weights):
    """Apply the factors of a node's steps to the bounds of what is below it."""
    dn, up = weights.dn, weights.up
    lo_dn, lo_up = weights.get(acc.r_hi)
    hi_dn, hi_up = weights.get(acc.r_lo)
    for margin in acc.margins:
        e_dn, e_up = weights.get(margin)
        hi_dn = dn.mul(hi_dn, dn.add(ONE, e_dn))
        hi_up = up.mul(hi_up, up.add(ONE, e_up))
    z_lo = (dn.mul(lo_dn, inner_lo[0]), up.mul(lo_up, inner_lo[1]))
    z_hi = (dn.mul(hi_dn, inner_hi[0]), up.mul(hi_up, inner_hi[1]))
    low = {a: (dn.mul(lo_dn, v[0]), up.mul(lo_up, v[1])) for a, v in low.items()}
    return z_lo, z_hi, low


def _sum2(a, b, weights: _Weights):
    return weights.dn.add(a[0], b[0]), weights.up.add(a[1], b[1])


def _evaluate(root: dict, st: _State, keep, sizes, weights: _Weights, budget, stats):
    """Post-order evaluation of the tree with an explicit stack.  Returns ``(z_lo, z_hi, low)`` of the root."""
    n = len(sizes)
    zero = ((0, 0), (0, 0))
    frames = [{"node": root, "st": st, "where": None, "acc": None}]
    done = None
    while frames:
        fr = frames[-1]
        if fr["acc"] is None:                                         # first visit: this node's steps
            stats["nodes"] += 1
            acc = fr["acc"] = _Factors()
            node, state = fr["node"], fr["st"]
            _apply_steps(node["steps"], state, sizes, acc, stats, fr["where"])
            if "order" in node:
                parts = _leaf(state, node["order"], keep, n, weights, budget, stats, fr["where"])
                total = zero
                for v in parts.values():
                    total = _sum2(total, v, weights)
                done = _close(acc, total, total, {} if keep is None else parts, weights)
                frames.pop()
                continue
            site = node["branch"]
            if not 0 <= site < n:
                raise Reject("invalid", f"{_path(fr['where'])}: branch on a site that does not exist")
            if site == keep:
                raise Reject("invalid", f"{_path(fr['where'])}: branch on the kept site")
            if sorted(node["children"]) != list(state.D[site]):
                raise Reject("invalid", f"{_path(fr['where'])}: the children are not exactly the states of the "
                                        f"working domain of site {site}")
            fr["todo"] = list(reversed(state.D[site]))
            fr["lo"], fr["hi"], fr["low"] = zero, zero, {}
            done = None
        if done is not None:                                          # a child has just returned
            z_lo, z_hi, low = done
            fr["lo"], fr["hi"] = _sum2(fr["lo"], z_lo, weights), _sum2(fr["hi"], z_hi, weights)
            for a, v in low.items():
                fr["low"][a] = _sum2(fr["low"][a], v, weights) if a in fr["low"] else v
            done = None
        if fr["todo"]:
            a = fr["todo"].pop()
            site = fr["node"]["branch"]
            frames.append({"node": fr["node"]["children"][a], "st": fr["st"].child(site, a),
                           "where": (fr["where"], a), "acc": None})
            continue
        done = _close(fr["acc"], fr["lo"], fr["hi"], fr["low"], weights)
        frames.pop()
    return done


# ------------------------------------------------------------------------------------------------------- result

@dataclass
class Result:
    accepted: bool
    reason: str = ""
    kind: str = "ok"
    ln_z_lo: Fraction | None = None          # certified:  ln_z_lo <= ln Z(root box) <= ln_z_hi
    ln_z_hi: Fraction | None = None
    ideal_lo: tuple | None = None            # (below, above) enclosure of the lower end of the ideal interval
    ideal_hi: tuple | None = None            # (below, above) enclosure of the upper end of the ideal interval
    keep: int | None = None
    populations: dict = field(default_factory=dict)       # state -> (lo, hi), certified
    pop_ideal: dict = field(default_factory=dict)         # state -> ((lo below, lo above), (hi below, hi above))
    removed_upper: Fraction | None = None
    survivors: tuple = ()
    full_box: bool | None = None
    claim: tuple | None = None
    stats: dict = field(default_factory=dict)

    def population(self, state: int):
        """Certified interval of ``P(x_keep = state)`` on the root box (``(0, 0)`` for a state outside it)."""
        if self.keep is None or self.ln_z_lo is None:
            return None
        return self.populations.get(state, (Fraction(0), Fraction(0)))


def _check(doc, model, exp_bits, round_bits, max_entries, exp_impl, max_exact_exponent) -> Result:
    if type(exp_bits) is not int or not 16 <= exp_bits <= 100000:
        raise Reject("malformed", "exp_bits must be an integer in 16..100000")
    if round_bits is not None and (type(round_bits) is not int or not 16 <= round_bits <= 100000):
        raise Reject("malformed", "round_bits must be None or an integer in 16..100000")
    if max_entries is not None and (type(max_entries) is not int or max_entries < 1):
        raise Reject("malformed", "max_entries must be None or a positive integer")
    if exp_impl not in _EXP_IMPL:
        raise Reject("malformed", "exp_impl must be 'arb' or 'taylor'")
    if type(max_exact_exponent) is not int or max_exact_exponent < 0:
        raise Reject("malformed", "max_exact_exponent must be a nonnegative integer")
    cert = parse_document(doc, model)
    if abs(model.scale_bits) > 65536:
        raise Reject("abstain", "scale_bits beyond 65536 in absolute value")
    sizes = model.sizes
    weights = _Weights(cert.beta, model.scale_bits, exp_bits, round_bits, exp_impl, max_exact_exponent)
    stats = {"nodes": 0, "leaves": 0, "prunes": 0, "relaxes": 0, "max_table": 0, "entries": 0}
    state = _State([list(u) for u in model.unary], dict(model.pair), list(cert.domains))
    z_lo, z_hi, low = _evaluate(cert.root, state, cert.keep, sizes, weights, max_entries, stats)
    stats["distinct_exponentials"] = len(weights.cache)
    ln_bits = max(exp_bits, 64)
    lo_dn, _ = ln_enclosure(z_lo[0], ln_bits, exp_impl)
    _, lo_up = ln_enclosure(z_lo[1], ln_bits, exp_impl)
    hi_dn, _ = ln_enclosure(z_hi[0], ln_bits, exp_impl)
    _, hi_up = ln_enclosure(z_hi[1], ln_bits, exp_impl)
    res = Result(accepted=True, ln_z_lo=lo_dn, ln_z_hi=hi_up, ideal_lo=(lo_dn, lo_up), ideal_hi=(hi_dn, hi_up),
                 keep=cert.keep, stats=stats, claim=cert.claim,
                 full_box=all(len(d) == k for d, k in zip(cert.domains, sizes)))
    if cert.keep is not None:
        states = cert.domains[cert.keep]
        p_dn = {a: (_ratio_dn(low[a][0], z_hi[1]) if a in low else Fraction(0)) for a in states}
        p_up = {a: (_ratio_up(low[a][1], z_hi[0]) if a in low else Fraction(0)) for a in states}
        tot_dn, tot_up = sum(p_dn.values(), Fraction(0)), sum(p_up.values(), Fraction(0))
        for a in states:
            hi_above = 1 - (tot_dn - p_dn[a])
            hi_below = 1 - (tot_up - p_up[a])
            res.populations[a] = (p_dn[a], hi_above)
            res.pop_ideal[a] = ((p_dn[a], p_up[a]), (hi_below, hi_above))
        res.removed_upper = 1 - tot_dn
        res.survivors = tuple(a for a in states if a in low)
    if cert.claim is not None and not (cert.claim[0] <= res.ln_z_lo and res.ln_z_hi <= cert.claim[1]):
        res.accepted = False
        res.kind = "claim"
        res.reason = "the claim does not contain the interval computed by this checker"
    return res


def check_document(doc, model, *, exp_bits: int = 256, round_bits=None, max_entries=2_000_000,
                   exp_impl: str = "arb", max_exact_exponent: int = 20000) -> Result:
    """Check a certificate given as a parsed JSON document (``dict``).  Never raises."""
    try:
        return _check(doc, model, exp_bits, round_bits, max_entries, exp_impl, max_exact_exponent)
    except Reject as rej:
        return Result(accepted=False, reason=rej.reason, kind=rej.kind)
    except RecursionError:
        return Result(accepted=False, reason="recursion limit reached", kind="abstain")
    except MemoryError:
        return Result(accepted=False, reason="out of memory", kind="abstain")
    except Exception as exc:                                          # a defect of this file, made visible
        return Result(accepted=False, reason=f"internal error: {type(exc).__name__}: {exc}", kind="internal")


def check_text(text, model, **options) -> Result:
    """Check a certificate file's text against the instance ``model``.  Never raises."""
    try:
        doc = parse_json_strict(text)
    except Reject as rej:
        return Result(accepted=False, reason=rej.reason, kind=rej.kind)
    except MemoryError:
        return Result(accepted=False, reason="out of memory", kind="abstain")
    except Exception as exc:
        return Result(accepted=False, reason=f"internal error: {type(exc).__name__}: {exc}", kind="internal")
    return check_document(doc, model, **options)


def _main(argv) -> int:
    if len(argv) != 3:
        print(__doc__.strip().splitlines()[-1].strip(), file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as handle:
        cert_text = handle.read()
    with open(argv[2], encoding="utf-8") as handle:
        model_text = handle.read()
    try:
        model = model_from_json(model_text)
    except Reject as rej:
        print(json.dumps({"accepted": False, "kind": rej.kind, "reason": rej.reason}))
        return 1
    res = check_text(cert_text, model)
    out = {"accepted": res.accepted, "kind": res.kind, "reason": res.reason, "stats": res.stats}
    if res.ln_z_lo is not None:
        out["ln_z_lo"] = f"{res.ln_z_lo.numerator}/{res.ln_z_lo.denominator}"
        out["ln_z_hi"] = f"{res.ln_z_hi.numerator}/{res.ln_z_hi.denominator}"
        out["ln_z_lo_float"], out["ln_z_hi_float"] = float(res.ln_z_lo), float(res.ln_z_hi)
        out["populations"] = {str(a): [float(lo), float(hi)] for a, (lo, hi) in res.populations.items()}
    print(json.dumps(out, indent=1))
    return 0 if res.accepted else 1


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
