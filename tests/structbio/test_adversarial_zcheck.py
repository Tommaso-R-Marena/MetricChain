"""Adversarial review STRUCTBIO-REV-0001 — `zcheck.check_partition_certificate`, the interval tables
(`itables`) and the file format `structbio-zcert/1`.

``FINDING`` tests fail with the reviewed code and are left red; ``SURVIVED`` tests pass.

Ground truth for `ln Z` and for populations is exhaustive enumeration in rigorous interval
arithmetic (`mpmath.iv`, 160 digits, refined to 640 and 2,560 digits when a certified bound and
the truth are closer than the enclosure of the truth); a comparison is never decided by a
rounded number.  Certificates are hand-built or random; none comes from the producer.
"""
import contextlib
import itertools
import json
import math
import random
import signal
import sys
import threading
import tracemalloc
import warnings
from fractions import Fraction

import numpy as np
import pytest
from mpmath import iv

from metricchain_sb import zcert
from metricchain_sb.itables import FloatTables, IntervalTable
from metricchain_sb.model import PairModel
from metricchain_sb.partition import certify_partition
from metricchain_sb.synthetic import random_pair_model
from metricchain_sb.zcert import MalformedZCertificate, ZCertificate
from metricchain_sb.zcheck import check_partition_certificate


# ----------------------------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------------------------

class _Deadline(BaseException):
    """Raised by the alarm; a BaseException so that the checker's `except Exception` cannot swallow it."""


@contextlib.contextmanager
def _deadline(seconds):
    if threading.current_thread() is not threading.main_thread() or not hasattr(signal, "setitimer"):
        pytest.skip("needs SIGALRM in the main thread")

    def handler(signum, frame):
        raise _Deadline()

    old = signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)


def _peak_megabytes(fn):
    tracemalloc.start()
    try:
        out = fn()
        peak = tracemalloc.get_traced_memory()[1]
    finally:
        tracemalloc.stop()
    return out, peak / 1e6


def _ivq(q):
    q = Fraction(q)
    return iv.mpf(q.numerator) / iv.mpf(q.denominator)


class _Truth:
    """Enclosures of ln Z and of every population on a box, by enumeration."""

    def __init__(self, model, beta, domains):
        self.model, self.beta, self.domains = model, Fraction(beta), [list(d) for d in domains]
        self.unit = Fraction(1, 2 ** model.scale_bits)
        self.energies = {x: model.energy_int(x) for x in itertools.product(*self.domains)}
        self.flat = len(set(self.energies.values())) == 1 or self.beta == 0     # all weights equal: rational populations

    def at(self, dps):
        old = iv.dps
        iv.dps = dps
        try:
            z = iv.mpf(0)
            marg = [dict.fromkeys(range(k), iv.mpf(0)) for k in self.model.sizes]
            for x, e in self.energies.items():
                w = iv.exp(-_ivq(self.beta * e * self.unit))
                z += w
                for i, a in enumerate(x):
                    marg[i][a] += w
            pops = []
            for m in marg:
                d = {}
                for a in m:
                    others = iv.mpf(0)
                    for b, v in m.items():
                        if b != a:
                            others += v
                    d[a] = (m[a] / z, others / z)       # P and 1 - P (exact zeros stay exact)
                pops.append(d)
            return iv.log(z), pops
        finally:
            iv.dps = old

    def exact_population(self, site, state):
        count = sum(1 for x in self.energies if x[site] == state)
        return Fraction(count, len(self.energies))


def _violation(truth, result, keep):
    """None if the accepted result certainly contains the truth; otherwise a description."""
    sizes = truth.model.sizes
    for dps in (160, 640, 2560):
        old = iv.dps
        iv.dps = dps
        try:
            lnz, pops = truth.at(dps)
            undecided = False
            lo, hi = _ivq(result.ln_z_lo), _ivq(result.ln_z_hi)
            if lo.a > lnz.b or hi.b < lnz.a:
                return (f"ln Z = {float(lnz.mid):.9g} is outside the accepted interval "
                        f"[{float(result.ln_z_lo):.9g}, {float(result.ln_z_hi):.9g}]")
            undecided |= not (lo.b <= lnz.a and lnz.b <= hi.a)
            if keep is not None:
                for a in range(sizes[keep]):
                    plo, phi = result.population(a)
                    p, comp = pops[keep][a]
                    lo_i, chi = _ivq(plo), _ivq(1 - Fraction(phi))
                    if lo_i.a > p.b or chi.a > comp.b:
                        return (f"ln Z contained, but P(x_{keep} = {a}) = {float(p.mid):.6g} is outside the "
                                f"accepted interval [{float(plo):.6g}, {float(phi):.6g}]")
                    if not (lo_i.b <= p.a and chi.b <= comp.a):
                        if truth.flat and plo <= truth.exact_population(keep, a) <= phi:
                            continue                    # rational truth, compared exactly
                        undecided = True
            if not undecided:
                return None
        finally:
            iv.dps = old
    return "undecided at 2,560 digits"


def _random_model(rng):
    n = rng.randint(1, 5)
    sizes = [rng.randint(1, 4) for _ in range(n)]
    amp = rng.choice([1, 5, 40, 1000, 10 ** 6, 10 ** 9, 2 ** 61, 2 ** 70])

    def val():
        r = rng.random()
        if r < 0.05:
            return 0
        if r < 0.10:
            return rng.choice([-1, 1]) * amp
        if r < 0.2:
            return rng.choice([-1, 1]) * (amp - rng.randint(0, 3))
        return rng.randint(-amp, amp)

    unary = [np.array([val() for _ in range(k)], dtype=object) for k in sizes]
    pair = {}
    density = rng.choice([0.3, 0.7, 1.0])
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < density:
                pair[(i, j)] = np.array([[val() for _ in range(sizes[j])] for _ in range(sizes[i])], dtype=object)
    return PairModel(unary=unary, pair=pair, scale_bits=rng.choice([0, 0, 2, 7, 20, 30]))


class _NodeGenerator:
    """Random certificate trees with a replay of the working model, so that the generator knows
    which certificates are invalid.  Steps: prunes (valid ones with any margin of at least -9/beta,
    occasionally of absent states or by themselves), relaxations with fitted, small or large
    arbitrary `f`, `g` (occasionally of a pair relaxed before), on any site including the kept one;
    branches with occasionally a missing child or an extra child; random elimination orders."""

    def __init__(self, rng, model, beta, keep, cap):
        self.rng, self.model, self.beta, self.keep, self.cap = rng, model, beta, keep, cap
        self.unit = Fraction(1, 2 ** model.scale_bits)
        self.invalid = False
        self.prunes = self.relaxes = self.branches = 0

    @staticmethod
    def margin(D, H, J, i, r, t):
        m = H[i][r] - H[i][t]
        for (a, b), T in J.items():
            if a == i:
                m += min(T[r][s] - T[t][s] for s in D[b])
            elif b == i:
                m += min(T[s][r] - T[s][t] for s in D[a])
        return m

    def node(self, D, H, J, depth, live=True):
        rng, model = self.rng, self.model
        n, sizes = model.n, model.sizes
        D, H, J = [list(d) for d in D], [list(h) for h in H], dict(J)
        steps = []
        for _ in range(rng.choice([0, 0, 1, 2, 3, 5])):
            if rng.random() < 0.5:
                i = rng.randrange(n)
                if len(D[i]) >= 2 and rng.random() < 0.97:
                    r, t = rng.sample(D[i], 2)
                elif rng.random() < 0.06:
                    r, t = rng.randrange(sizes[i]), rng.randrange(sizes[i])
                else:
                    continue
                if r != t and r in D[i] and t in D[i]:
                    if self.beta * self.margin(D, H, J, i, r, t) * self.unit < -9:
                        continue        # exp(exp(9+)): the resource-exhaustion finding, tested separately
                    D[i].remove(r)
                    self.prunes += live
                elif live:
                    self.invalid = True
                steps.append({"op": "prune", "site": i, "remove": r, "dominator": t})
            elif model.pair:
                (i, j) = rng.choice(sorted(J)) if (J and rng.random() < 0.97) else rng.choice(sorted(model.pair))
                mode = rng.random()
                T = model.pair[(i, j)]
                if mode < 0.4:
                    f = [int(round(Fraction(sum(int(T[a, b]) for b in D[j]), len(D[j])))) for a in range(sizes[i])]
                    g = [int(round(Fraction(sum(int(T[a, b]) - f[a] for a in D[i]), len(D[i])))) for b in range(sizes[j])]
                else:
                    c = max(1, min(self.cap, 50)) if mode < 0.7 else max(1, self.cap)
                    f = [rng.randint(-c, c) for _ in range(sizes[i])]
                    g = [rng.randint(-c, c) for _ in range(sizes[j])]
                steps.append({"op": "relax", "pair": [i, j], "f": f, "g": g})
                if (i, j) not in J:
                    if live:
                        self.invalid = True
                else:
                    J.pop((i, j))
                    H[i] = [h + v for h, v in zip(H[i], f)]
                    H[j] = [h + v for h, v in zip(H[j], g)]
                    self.relaxes += live
        node = {"steps": steps}
        candidates = [i for i in range(n) if i != self.keep]
        if depth < 3 and candidates and rng.random() < 0.35:
            i = rng.choice(candidates)
            children = {}
            for a in D[i]:
                if rng.random() < 0.03:
                    if live:
                        self.invalid = True
                    continue
                D2 = list(D)
                D2[i] = [a]
                children[a] = self.node(D2, H, J, depth + 1, live)
            if rng.random() < 0.1:
                extra = rng.randrange(sizes[i])
                if extra not in children and extra not in D[i]:
                    D2 = list(D)
                    D2[i] = [extra]
                    children[extra] = self.node(D2, H, J, depth + 1, False)
            node["branch"], node["children"] = i, children
            self.branches += live
        else:
            order = [i for i in range(n) if i != self.keep]
            rng.shuffle(order)
            node["order"] = order
        return node


def _random_z_certificate(seed):
    rng = random.Random(seed)
    model = _random_model(rng)
    n, sizes = model.n, model.sizes
    unit = Fraction(1, 2 ** model.scale_bits)
    target = rng.choice([0, Fraction(1, 100), 1, 10, 100, 700, 1500, 3000])      # beta * (largest |entry|)
    maxabs = max(1, model.max_abs_entry())
    if target == 0:
        beta = Fraction(0)
    else:
        beta = Fraction(target) / (maxabs * unit) * Fraction(rng.randint(1, 1000), 1000)
        if rng.random() < 0.5:
            beta = beta.limit_denominator(10 ** rng.randint(1, 12)) or beta
    domains = [list(range(k)) if rng.random() < 0.7 else rng.sample(range(k), rng.randint(1, k)) for k in sizes]
    keep = rng.randrange(n) if rng.random() < 0.6 else None
    gen = _NodeGenerator(rng, model, beta, keep, maxabs * 3)
    H0 = [[int(v) for v in u.tolist()] for u in model.unary]
    J0 = {key: [[int(v) for v in row] for row in t.tolist()] for key, t in model.pair.items()}
    root = gen.node(domains, H0, J0, 0)
    cert = ZCertificate(model=model, beta=beta, domains=[list(d) for d in domains], steps=root["steps"],
                        order=root.get("order", []), keep=keep, branch=root.get("branch"),
                        children=root.get("children"))
    return cert, gen


def _two_site_model():
    return PairModel(unary=[np.array([0, 1]), np.array([0, 2])], pair={(0, 1): np.array([[0, 1], [1, 0]])},
                     scale_bits=0)


def _zc(model=None, **fields):
    model = _two_site_model() if model is None else model
    base = dict(model=model, beta=Fraction(1), domains=model.full_domains(), steps=[], order=list(range(model.n)))
    base.update(fields)
    return ZCertificate(**base)


# ----------------------------------------------------------------------------------------------
# attacks that the checker withstood
# ----------------------------------------------------------------------------------------------

@pytest.mark.parametrize("arithmetic", ["exact", "float"])
def test_random_hand_built_z_certificates_enclose_the_enumerated_truth(arithmetic):
    """SURVIVED.  1,000 random certificates per tier (models of up to 5 sites and 4 states, table
    entries up to 2**70, beta from 0 to values that spread the weights over e**+-3000, sub-boxes,
    kept sites, prune / relax / branch trees).  Every accepted result contains ln Z and the
    population of every state of the kept site (states outside the root box and pruned states
    included); `full_box` is right; an invalid certificate is never accepted; a valid one is
    rejected only by an explicit abstention.  (The same campaign on 40,000 seeds during the review:
    31,889 accepted results in the exact tier and 29,683 in the float tier, no miss.)"""
    accepted = rejected = abstained = with_prune = with_relax = with_branch = with_keep = 0
    for seed in range(1000):
        cert, gen = _random_z_certificate(seed)
        model = cert.model
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = check_partition_certificate(cert, arithmetic=arithmetic)
        if not result.accepted:
            rejected += 1
            if "abstained" in result.reason:
                abstained += 1
            else:
                assert gen.invalid, (seed, result.reason)       # a valid certificate is not rejected
            continue
        assert not gen.invalid, seed                            # an invalid certificate is not accepted
        accepted += 1
        problem = _violation(_Truth(model, cert.beta, cert.domains), result, cert.keep)
        assert problem is None, (seed, problem)
        assert result.full_box == all(sorted(d) == list(range(k)) for d, k in zip(cert.domains, model.sizes))
        with_prune += gen.prunes > 0
        with_relax += gen.relaxes > 0
        with_branch += gen.branches > 0
        with_keep += cert.keep is not None
    assert accepted > 600 and rejected > 100
    assert with_prune > 150 and with_relax > 150 and with_branch > 80 and with_keep > 300
    assert (abstained > 10) == (arithmetic == "float")          # only the float tier loses its lower bound


def test_step_and_node_rules_reject_what_they_must():
    """SURVIVED.  Relaxing a pair twice, pruning an absent state or a state by itself, an order that
    is not a permutation, a branch on the kept site, a missing child, unknown fields, a negative
    beta, a claim tighter than what the checker computes: all rejected, none raises."""
    model = _two_site_model()
    relax = {"op": "relax", "pair": [0, 1], "f": [0, 0], "g": [0, 0]}
    leaf = {"steps": [], "order": [0, 1]}
    good = check_partition_certificate(_zc(steps=[relax]))
    assert good.accepted
    rejected = [
        _zc(steps=[relax, relax]),
        _zc(steps=[{"op": "prune", "site": 0, "remove": 1, "dominator": 1}]),
        _zc(steps=[{"op": "prune", "site": 0, "remove": 1, "dominator": 0}] * 2),
        _zc(domains=[[0], [0, 1]], steps=[{"op": "prune", "site": 0, "remove": 1, "dominator": 0}]),
        _zc(steps=[{"op": "prune", "site": 0, "remove": 2, "dominator": 0}]),
        _zc(steps=[{"op": "relax", "pair": [1, 0], "f": [0, 0], "g": [0, 0]}]),
        _zc(steps=[{"op": "relax", "pair": [0, 1], "f": [0], "g": [0, 0]}]),
        _zc(steps=[{"op": "relax", "pair": [0, 1], "f": [0, 0.0], "g": [0, 0]}]),
        _zc(steps=[{"op": "relax", "pair": [0, 1], "f": [0, True], "g": [0, 0]}]),
        _zc(steps=[{"op": "sum"}]), _zc(steps=[dict(relax, extra=1)]), _zc(steps=({"op": "relax"},)),
        _zc(order=[0]), _zc(order=[0, 0]), _zc(order=[0, 1, 1]), _zc(order=[1, 2]), _zc(order=(0, 1)),
        _zc(keep=0, order=[0, 1]), _zc(keep=2, order=[0, 1]), _zc(keep=True, order=[0]),
        _zc(beta=Fraction(-1)), _zc(beta=1), _zc(beta=1.0),
        _zc(domains=[[0, 1], []]), _zc(domains=[[0, 0], [0, 1]]), _zc(domains=[[0, 1], [0, 2]]),
        _zc(domains=[(0, 1), [0, 1]]),
        _zc(order=[], branch=0, children={0: leaf}),                      # no child for state 1
        _zc(order=[], branch=0, children={0: leaf, 1: None}),
        _zc(order=[], branch=0, children={0: leaf, 1: dict(leaf, weight=1)}),
        _zc(order=[], branch=0, children=[leaf, leaf]),
        _zc(order=[], branch=2, children={0: leaf, 1: leaf}),
        _zc(order=[1], keep=0, branch=0, children={0: {"steps": [], "order": [1]}, 1: {"steps": [], "order": [1]}}),
        _zc(order=[], branch=0, children={0: leaf, 1: {"steps": [], "order": [0, 1], "branch": 1, "children": {}}}),
        _zc(steps=[relax], claim={"ln_z_lo": good.ln_z_lo + Fraction(1, 10 ** 6)}),
        _zc(steps=[relax], claim={"ln_z_hi": good.ln_z_hi - Fraction(1, 10 ** 6)}),
        _zc(steps=[relax], claim={"ln_z_lo": 0.0}), _zc(steps=[relax], claim={"lo": Fraction(0)}),
    ]
    for cert in rejected:
        for arithmetic in ("exact", "float"):
            result = check_partition_certificate(cert, arithmetic=arithmetic)
            assert result.accepted is False and result.reason, cert
    assert check_partition_certificate(None).accepted is False
    assert check_partition_certificate(_zc(), arithmetic="double").accepted is False
    assert check_partition_certificate(_zc(steps=[relax], claim={"ln_z_lo": good.ln_z_lo, "ln_z_hi": good.ln_z_hi})).accepted
    assert check_partition_certificate(PairModel(unary=[], pair={}, scale_bits=0)).accepted is False


def test_float_tier_primitives_are_outward_on_adversarial_data():
    """SURVIVED.  The assumptions F1-F3 of `itables`, checked in exact rational arithmetic:
    `sum_out` on axes of 1 to 4,096 doubles (many tiny + one large, addends of half an ulp,
    geometric and random magnitudes over 300 decades, both axis orders), the statement F2 itself
    for `numpy.sum`, 5,000 products including results in the subnormal range, and `from_me_bounds`
    for mantissas of up to 200 bits and exponents down to -3000."""
    ft = FloatTables()
    rng = random.Random(11)
    nprng = np.random.default_rng(11)
    u = Fraction(1, 2 ** 53)

    def adversarial(m):
        kind = rng.randrange(8)
        if kind == 0:
            v = np.full(m, 1e-300)
            v[rng.randrange(m)] = 1.0
        elif kind == 1:
            v = np.full(m, 2.0 ** -53 * (1 + 2.0 ** -30))
            v[0] = 1.0
        elif kind == 2:
            v = np.full(m, 2.0 ** -53)
            v[0] = 1.0
        elif kind == 3:
            v = 0.5 ** (np.arange(m) % 1000)
        elif kind == 4:
            v = 10.0 ** nprng.uniform(-300, 0, size=m)
        elif kind == 5:
            v = np.full(m, math.nextafter(1.0, 0.0))
        elif kind == 6:
            v = np.where(np.arange(m) % 2 == 0, 1.0, 2.0 ** -52 * 0.75)
        else:
            v = nprng.uniform(0.5, 1.0, size=m)
        if rng.random() < 0.3:
            nprng.shuffle(v)
        return v.astype(np.float64)

    sums = 0
    for _ in range(120):
        m = rng.choice([1, 2, 3, 7, 8, 9, 15, 16, 17, 100, 127, 128, 129, 1000, 4096])
        v = adversarial(m)
        for axis in (0, 1):
            arr = np.stack([v, v[::-1], np.roll(v, 1)], axis=1 - axis)
            lo_list, hi_list = ft.bounds(ft.sum_out(IntervalTable((0, 1), arr.copy(), arr.copy(), 0), axis))
            for col, (lo, hi) in enumerate(zip(lo_list, hi_list)):
                column = arr[:, col] if axis == 0 else arr[col, :]
                exact = sum((Fraction(float(x)) for x in column), Fraction(0))
                assert lo <= exact <= hi, (m, axis)
                assert hi - lo <= exact * Fraction(1, 10 ** 10) + Fraction(1, 10 ** 290)
                s = Fraction(float(np.sum(column)))
                g = (m - 1) * u / (1 - (m - 1) * u)
                assert exact * (1 - g) <= s <= exact * (1 + g)             # F2 as stated
                sums += 1
    assert sums == 720
    for _ in range(5000):
        a, b = 10.0 ** rng.uniform(-300, 0), 10.0 ** rng.uniform(-300, 0)
        out = ft.multiply(IntervalTable((0,), np.array([a]), np.array([a]), 0),
                          IntervalTable((0,), np.array([b]), np.array([b]), 0), {0: 1}, None)
        lo, hi = ft.bounds(out)
        assert lo[0] <= Fraction(a) * Fraction(b) <= hi[0]
    for _ in range(1500):
        k = rng.randint(1, 5)
        hi_me = [(rng.getrandbits(rng.randint(1, 200)) | 1, rng.randint(-3000, 3000)) for _ in range(k)]
        lo_me = [(max(0, m - rng.randint(0, 3)), e) for m, e in hi_me]
        lo, hi = ft.bounds(ft.from_me_bounds((0,), lo_me, hi_me, (k,)))
        for (ml, el), (mh, eh), l, h in zip(lo_me, hi_me, lo, hi):
            assert l <= Fraction(ml) * Fraction(2) ** el and Fraction(mh) * Fraction(2) ** eh <= h


def test_z_file_round_trip_is_canonical_and_bound_to_the_instance():
    """SURVIVED.  A branched certificate with a claim survives `dumps`/`loads` unchanged, is judged
    identically, and is refused for an instance with another checksum or with a non-canonical
    rational, a float, a boolean, a duplicate key or an unknown top-level field."""
    model = _two_site_model()
    relax = {"op": "relax", "pair": [0, 1], "f": [1, 0], "g": [0, -1]}
    cert = _zc(model, beta=Fraction(3, 2), steps=[relax], order=[], branch=0,
               children={0: {"steps": [{"op": "prune", "site": 1, "remove": 1, "dominator": 0}], "order": [0, 1]},
                         1: {"steps": [], "order": [1, 0]}})
    first = check_partition_certificate(cert)
    assert first.accepted
    cert.claim = {"ln_z_lo": first.ln_z_lo, "ln_z_hi": first.ln_z_hi}
    text = zcert.dumps(cert)
    back = zcert.loads(text, model)
    assert zcert.dumps(back) == text
    again = check_partition_certificate(back)
    assert again.accepted and (again.ln_z_lo, again.ln_z_hi) == (first.ln_z_lo, first.ln_z_hi)
    other = PairModel(unary=[np.array([0, 1]), np.array([0, 3])], pair={(0, 1): np.array([[0, 1], [1, 0]])}, scale_bits=0)

    def edit(fn):
        doc = json.loads(text)
        fn(doc)
        return json.dumps(doc, separators=(",", ":"))

    bad = [edit(lambda d: d.__setitem__("beta", v)) for v in ("6/4", "3/-2", " 3/2", "3/2 ", "+3/2", "3/2/1", "1.5", "3", "-3/2",
                                                               "03/2", "3/02", "3 /2", "٣/٢")]
    bad += [edit(lambda d: d.__setitem__("beta", v)) for v in (3, 1.5, None, True, ["3/2"])]
    bad += [edit(lambda d: d.__setitem__("zzz", 1)), edit(lambda d: d["claim"].__setitem__("zzz", "1/1")),
            edit(lambda d: d["claim"].__setitem__("ln_z_lo", "1/2/3")), edit(lambda d: d.__setitem__("keep", False)),
            edit(lambda d: d.__setitem__("keep", "0")), edit(lambda d: d.__setitem__("domains", [[0, 0], [0, 1]])),
            edit(lambda d: d.__setitem__("domains", [[0, True], [0, 1]])), edit(lambda d: d["root"].__setitem__("branch", None)),
            edit(lambda d: d["root"].__setitem__("steps", {})), edit(lambda d: d["root"]["steps"][0].__setitem__("f", [1.0, 0])),
            edit(lambda d: d["root"]["steps"][0].__setitem__("op", "prunes")),
            edit(lambda d: d["root"]["children"].__setitem__("01", d["root"]["children"]["0"])),
            edit(lambda d: d.__setitem__("format", "structbio-zcert/2")), edit(lambda d: d.pop("root")),
            edit(lambda d: d.__setitem__("model_sha256", "0" * 64)),
            text.replace('"beta":"3/2"', '"beta":"3/2","beta":"1/1"'), text + "x", "[" + text + "]", ""]
    for mutated in bad:
        with pytest.raises(MalformedZCertificate):
            zcert.loads(mutated, model)
    with pytest.raises(MalformedZCertificate):
        zcert.loads(text, other)


# ----------------------------------------------------------------------------------------------
# findings (these tests fail with the reviewed code)
# ----------------------------------------------------------------------------------------------

@pytest.mark.parametrize("dtype, entry, beta", [(np.int8, 100, Fraction(1, 100)),
                                                (np.int32, 1_500_000_000, Fraction(1, 10 ** 9)),
                                                (np.int64, 2 ** 62, Fraction(1, 2 ** 60))])
def test_numpy_integers_in_relax_vectors_must_not_wrap(dtype, entry, beta):
    """FINDING (unsound acceptance; in-memory certificates only).  `validate_structure` admits NumPy
    integers in `f` and `g`; the checker then computes `table - f - g` and `H += f` in fixed-width
    arithmetic.  With one configuration of energy `entry` and the relaxation `f = [-entry]` the
    residual `2 * entry` wraps around and the accepted interval for ln Z misses the truth by
    `beta * 2**width` nats (the docstring says "Steps: Python integers (exact)")."""
    model = PairModel(unary=[np.array([0]), np.array([0])], pair={(0, 1): np.array([[entry]], dtype=object)},
                      scale_bits=0)
    cert = _zc(model, beta=beta, steps=[{"op": "relax", "pair": [0, 1], "f": [dtype(-entry)], "g": [dtype(0)]}])
    truth = -beta * entry                                       # one configuration: ln Z = -beta * E exactly
    for arithmetic in ("exact", "float"):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = check_partition_certificate(cert, arithmetic=arithmetic)
        assert (not result.accepted) or result.ln_z_lo <= truth <= result.ln_z_hi, (
            f"{arithmetic}: accepted [{float(result.ln_z_lo):.6f}, {float(result.ln_z_hi):.6f}], "
            f"but ln Z = {float(truth):.6f}")


def _weight_energy(log2_inverse_weight, scale_bits=20):
    """Table entry whose Boltzmann weight at beta = 1 is 2**-log2_inverse_weight."""
    return int(round(log2_inverse_weight * math.log(2) * 2 ** scale_bits))


@pytest.mark.parametrize("exp_bits", [980, 990])
def test_float_tier_stays_sound_when_exp_bits_is_large(exp_bits):
    """FINDING (unsound acceptance; float tier with a non-default `exp_bits` between about 872 and
    1001).  `FloatTables._ldexp_up` returns 1e-300 whenever the binary exponent is below -2000,
    which is an upper bound only if the mantissa is below 2**1003.  `exp_bits` near 1000 gives
    mantissas of 1012 to 1022 bits, and a weight of 2**-990 relative to the largest entry of its
    table is then replaced by 1e-300 = 2**-996.6.  Here the configuration carrying 80% of the
    partition sum is underestimated: the accepted interval misses ln Z by more than a nat and the
    population interval of the dominant state excludes it.  (`expo` says more bits "only cost time".)"""
    model = PairModel(unary=[np.array([_weight_energy(495), 0]), np.array([0, _weight_energy(1200)])],
                      pair={(0, 1): np.array([[_weight_energy(497), 0], [_weight_energy(990), 0]])}, scale_bits=20)
    truth = _Truth(model, Fraction(1), model.full_domains())
    assert check_partition_certificate(_zc(model, keep=0, order=[1]), arithmetic="exact", exp_bits=exp_bits).accepted
    result = check_partition_certificate(_zc(model, keep=0, order=[1]), arithmetic="float", exp_bits=exp_bits)
    problem = _violation(truth, result, 0) if result.accepted else None
    assert problem is None, f"float tier, exp_bits={exp_bits}: {problem}"


def test_z_checker_must_not_trust_a_stale_neighbour_cache_of_the_instance():
    """FINDING (unsound acceptance; in-memory instance changed after construction).  As in the min
    checker: after `model.pair[(0, 1)] = table` the prune margin ignores the new pair (the cached
    neighbour lists are stale) while the Boltzmann factors include it."""
    model = PairModel(unary=[np.array([0, 0]), np.array([0])], pair={}, scale_bits=0)
    model.pair[(0, 1)] = np.array([[50], [0]])                  # state 0 of site 0 costs 50, state 1 nothing
    cert = _zc(model, steps=[{"op": "prune", "site": 0, "remove": 1, "dominator": 0}])
    truth = _Truth(model, Fraction(1), model.full_domains())
    for arithmetic in ("exact", "float"):
        result = check_partition_certificate(cert, arithmetic=arithmetic)
        problem = _violation(truth, result, None) if result.accepted else None
        assert problem is None, f"{arithmetic}: {problem}"


@pytest.mark.parametrize("case", ["prune with margin -16", "relax with f = 10**7"])
def test_work_of_the_z_checker_is_not_exponential_in_the_numbers_of_a_step(case):
    """FINDING (resource exhaustion; reachable from a `structbio-zcert/1` file).  The accumulated
    factors of the steps are exponentiated as exact rationals: a prune with margin `m < 0` costs
    `exp(-beta*m)` nats, so the checker builds a rational of about `1.44 * exp(-beta*m)` bits, and
    a relaxation with large `f` one of `1.44 * beta * |f|` bits.  Measured during the review
    (both tiers): margin -19 -> 7.7 s and 189 MB, -21 -> more than 1.1 GB, -40 would need 4e16
    bytes; `f = 10**9` -> more than 20 s and 1.5 GB.  The certificates below are a few hundred
    bytes; they are *accepted*, after megabytes of big-integer work."""
    if case.startswith("prune"):
        model = PairModel(unary=[np.array([0, 16])], pair={}, scale_bits=0)
        cert = _zc(model, steps=[{"op": "prune", "site": 0, "remove": 0, "dominator": 1}])
    else:
        cert = _zc(steps=[{"op": "relax", "pair": [0, 1], "f": [10 ** 7, 0], "g": [0, 0]}])
    text = zcert.dumps(cert)
    assert len(text) < 400
    result, peak = _peak_megabytes(
        lambda: check_partition_certificate(zcert.loads(text, cert.model), arithmetic="float"))
    assert peak < 2.0, f"{peak:.1f} MB allocated to judge a {len(text)}-byte file (accepted={result.accepted})"


@pytest.mark.parametrize("case, arithmetic", [
    ("prune with beta * margin = +3e5", "float"), ("table entry 2**60000", "float"), ("scale_bits = 10**8", "float"),
    ("beta * energy = 2e7", "exact"), ("node that contains itself", "exact")])
def test_z_checker_returns_within_seconds_on_tiny_certificates(case, arithmetic):
    """FINDING (hang).  Each certificate has at most two sites and one step.  A thermal dead-end
    elimination with a *large positive* margin (a clash: the safest prune there is) adds a rational
    with a denominator of `1.44 * beta * m` bits whose exact Taylor series is then evaluated: 11 s
    at beta*m = 1e5, more than 30 s at 3e5 (measured).  An astronomical table entry or `scale_bits`
    is not refused but exponentiated; the exact tier at beta = 1e7 did not return within 20 s and
    does not abstain; a node that is its own child makes `validate_structure` loop for ever."""
    model = _two_site_model()
    if case.startswith("prune"):
        model = PairModel(unary=[np.array([0, 300_000]), np.array([0, 2])], pair={(0, 1): np.array([[0, 1], [1, 0]])},
                          scale_bits=0)
        cert = _zc(model, steps=[{"op": "prune", "site": 0, "remove": 1, "dominator": 0}])
    elif case.startswith("table entry"):
        model = PairModel(unary=[np.array([0, 2 ** 60000], dtype=object), np.array([0, 2])],
                          pair={(0, 1): np.array([[0, 1], [1, 0]])}, scale_bits=0)
        cert = _zc(model)
    elif case.startswith("scale_bits"):
        model = PairModel(unary=[np.array([0, 1]), np.array([0, 2])], pair={(0, 1): np.array([[0, 1], [1, 0]])},
                          scale_bits=10 ** 8)
        cert = _zc(model)
    elif case.startswith("beta"):
        cert = _zc(beta=Fraction(10 ** 7))
    else:
        node = {"steps": [], "branch": 0, "children": {1: {"steps": [], "order": [0, 1]}}}
        node["children"][0] = node
        cert = _zc(order=[], branch=0, children=node["children"])
    result = None
    try:
        with _deadline(3.0):
            result = check_partition_certificate(cert, arithmetic=arithmetic)
    except _Deadline:
        pass
    assert result is not None, f"check_partition_certificate ({arithmetic} tier) did not return within 3 s: {case}"


def test_a_certificate_made_in_one_tier_is_accepted_by_the_other_tier_and_by_other_precisions():
    """FINDING (one file, several verdicts).  The producer stores the interval it computed as the
    claim, and a claim is accepted only if it contains the interval the checker computes — to the
    last bit of a floating-point guess inside `log_bounds`.  The verdict on an honest certificate
    therefore depends on checker options that the file does not record (`exp_bits`) or records
    only as untrusted metadata (`arithmetic`): most certificates made in one tier are *rejected*
    in the other, and about half are rejected at `exp_bits` 48 or 96 instead of 64."""
    beta = Fraction(1000, 593)
    verdicts = {}
    for seed in range(12):
        rng = random.Random(seed)
        model = random_pair_model(seed, n=rng.randint(2, 5), kmax=rng.randint(2, 4), density=1.0,
                                  scale_bits=rng.choice([2, 5]), amplitude=rng.choice([6, 40]), kmin=1)
        for made in ("exact", "float"):
            cert = certify_partition(model, beta, tau=None, theta=None, arithmetic=made)
            cert = zcert.loads(zcert.dumps(cert), model)                # through the file
            for checked, bits in (("exact", 64), ("float", 64), ("exact", 48), ("exact", 96)):
                ok = check_partition_certificate(cert, arithmetic=checked, exp_bits=bits).accepted
                key = f"made {made}, checked {checked}/{bits}"
                verdicts[key] = verdicts.get(key, 0) + ok
    assert verdicts["made exact, checked exact/64"] == 12 and verdicts["made float, checked float/64"] == 12
    rejected = {k: 12 - v for k, v in verdicts.items() if v < 12}
    assert not rejected, f"honest certificates rejected (out of 12): {rejected}"


def _z_text():
    cert = _zc(beta=Fraction(3, 2), order=[], branch=0,
               children={0: {"steps": [], "order": [0, 1]}, 1: {"steps": [], "order": [1, 0]}})
    return zcert.dumps(cert)


@pytest.mark.parametrize("case", ["beta '--3/2'", "beta with a superscript digit", "beta with 5,000 digits",
                                  "child key with a superscript digit", "1,500 nested branch nodes"])
def test_z_loader_reports_every_malformed_file_as_malformed_zcertificate(case):
    """FINDING (the loader raises an exception that is not `MalformedZCertificate`).  `'--3'.lstrip('-')`
    and SUPERSCRIPT THREE pass `str.isdigit` but not `int`; a numeral longer than the interpreter's
    limit for integer conversion raises ValueError; 1,500 nested branch nodes pass the JSON parser
    and overflow the recursive `_node_from_json` (RecursionError)."""
    text = _z_text()
    doc = json.loads(text)
    if case == "beta '--3/2'":
        doc["beta"] = "--3/2"
    elif case == "beta with a superscript digit":
        doc["beta"] = "³/2"
    elif case == "beta with 5,000 digits":
        doc["beta"] = "1" * 5000 + "/1"
    elif case == "child key with a superscript digit":
        doc["root"]["children"]["²"] = doc["root"]["children"].pop("1")
    mutated = json.dumps(doc, separators=(",", ":"))
    if case == "1,500 nested branch nodes":
        leaf = '{"steps":[],"order":[0,1]}'
        doc["root"] = "@@"
        deep = '{"steps":[],"branch":0,"children":{"0":' * 1500 + leaf + (',"1":' + leaf + '}}') * 1500
        mutated = json.dumps(doc, separators=(",", ":")).replace('"@@"', deep)
    old_limit, old_digits = sys.getrecursionlimit(), sys.get_int_max_str_digits()
    sys.setrecursionlimit(1000)                 # the interpreter's defaults (the reference checker changes both)
    sys.set_int_max_str_digits(4300)
    outcome = "accepted"
    try:
        try:
            zcert.loads(mutated, _two_site_model())
        except MalformedZCertificate:
            outcome = "MalformedZCertificate"
        except (ValueError, RecursionError) as exc:
            outcome = f"{type(exc).__name__}: {str(exc)[:60]}"
    finally:
        sys.setrecursionlimit(old_limit)
        sys.set_int_max_str_digits(old_digits)
    assert outcome == "MalformedZCertificate", f"zcert.loads -> {outcome}"


@pytest.mark.parametrize("case", ["node with both branch and order", "unknown key in a node", "unknown key in a step"])
def test_z_loader_rejects_fields_outside_the_format(case):
    """FINDING (strictness).  Unknown fields are refused at the top level only.  Inside the tree they
    are dropped before `validate_structure` (which would refuse them in memory) sees the node: a
    node with both `branch` and `order` is read as a branch node, and a step may carry any extra
    field, e.g. a "margin" that nobody checks."""
    doc = json.loads(_z_text())
    if case == "node with both branch and order":
        doc["root"]["order"] = [0, 1]
    elif case == "unknown key in a node":
        doc["root"]["children"]["0"]["weight"] = "1/1"
    else:
        doc["root"]["steps"] = [{"op": "prune", "site": 1, "remove": 1, "dominator": 0, "margin": "999/1"}]
    with pytest.raises(MalformedZCertificate):
        zcert.loads(json.dumps(doc, separators=(",", ":")), _two_site_model())
