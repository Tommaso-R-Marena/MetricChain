"""SB-X-009 — the coordinator's probe of the repaired checkers against exhaustive enumeration.

Purpose.  The checkers were changed after the adversarial review STRUCTBIO-REV-0001 (commit
`0e934eb`).  The changes were written by one agent and reviewed by the coordinator; this script
is the coordinator's own evidence, independent of the tests that came with the repair: on small
random instances it lets the producers make certificates, damages them in ways that keep them
well typed, and compares **every accepted statement** with exhaustive enumeration.

What counts as a failure (each is counted and printed):

* a `min` certificate accepted with a lower bound above the enumerated minimum of its box, or
  with a witness energy below it;
* a `min` certificate judged differently in memory and from the text of its own file;
* a Z certificate accepted with an interval that does not contain the enumerated `ln Z` of its
  box (60 significant digits), in either arithmetic tier, at `exp_bits` 64 and at one of
  16, 48, 96, 400;
* a population interval that does not contain the enumerated population.

Expected outcome: zero failures of every kind (a single one would be a soundness defect of
trusted code).  The expectation was not committed before the first run: the script was first
run from the session's scratch directory, before the repair was committed, with this seed and
with the counts recorded in `RESULT.txt`.  The script proves nothing: it is a test on small
instances (at most 5 sites, at most 4 states), deterministic for a fixed seed.

Usage:  python experiments/structbio/checker_probe/run.py     (about one minute on one core)
"""
from __future__ import annotations

import copy
import pathlib
import random
import subprocess
import sys
import time
from fractions import Fraction

import mpmath
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_sb import mincert  # noqa: E402
from metricchain_sb.gmec import certify_gmec  # noqa: E402
from metricchain_sb.mincheck import check_min_certificate, check_text  # noqa: E402
from metricchain_sb.model import PairModel, brute_force_energies, brute_force_min  # noqa: E402
from metricchain_sb.partition import certify_partition  # noqa: E402
from metricchain_sb.zcheck import check_partition_certificate  # noqa: E402

SEED = 20261127
START_COMMIT = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()

mpmath.mp.dps = 60
rng = random.Random(SEED)


def random_model(n, kmax, span, p_pair=0.8):
    sizes = [rng.randint(1, kmax) for _ in range(n)]
    unary = [np.array([rng.randint(-span, span) for _ in range(k)], dtype=object) for k in sizes]
    pair = {}
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p_pair:
                pair[(i, j)] = np.array([[rng.randint(-span, span) for _ in range(sizes[j])]
                                         for _ in range(sizes[i])], dtype=object)
    return PairModel(unary, pair, scale_bits=rng.choice([0, 3, 20]))


def random_box(model):
    doms = []
    for k in model.sizes:
        d = [a for a in range(k) if rng.random() < 0.8]
        doms.append(d or [rng.randrange(k)])
    return doms


def mutate_min(cert):
    """One random change of a min certificate (well typed most of the time)."""
    c = copy.deepcopy(cert)
    kind = rng.randrange(8)
    nodes, stack = [], [c.root]
    while stack:
        nd = stack.pop()
        nodes.append(nd)
        if nd["node"] == "branch":
            stack.extend(nd["children"].values())
        elif nd["node"] == "prune":
            stack.append(nd["rest"])
    nd = rng.choice(nodes)
    if kind == 0:
        c.lower_bound += rng.choice([1, 2, 17, 2 ** 12, 2 ** 40])
    elif kind == 1 and nd["node"] == "leaf" and nd["m"]:
        vec = nd["m"][rng.choice(list(nd["m"]))]
        vec[rng.randrange(len(vec))] += rng.choice([-5, -1, 1, 5, 2 ** 30])
    elif kind == 2 and nd["node"] == "prune":
        nd["dominator"] = rng.randrange(c.model.sizes[nd["site"]])
    elif kind == 3 and nd["node"] == "prune":
        nd["remove"] = rng.randrange(c.model.sizes[nd["site"]])
    elif kind == 4 and nd["node"] == "branch" and nd["children"]:
        del nd["children"][rng.choice(list(nd["children"]))]
    elif kind == 5:                                              # a NumPy integer in the claim, possibly raised
        c.lower_bound = np.int64(int(c.lower_bound)) + np.int64(rng.choice([0, 1, 3]))
    elif kind == 6:                                              # a larger box than was certified
        i = rng.randrange(len(c.domains))
        extra = [a for a in range(c.model.sizes[i]) if a not in c.domains[i]]
        if extra:
            c.domains[i] = c.domains[i] + [rng.choice(extra)]
    else:
        c.message_bits = c.message_bits + rng.choice([-1, 1])
    return c


def mutate_z(cert):
    c = copy.deepcopy(cert)
    kind = rng.randrange(7)
    nodes, stack = [], [c.root_node()]
    while stack:
        nd = stack.pop()
        nodes.append(nd)
        if nd.get("branch") is not None:
            stack.extend(nd["children"].values())
    steps = rng.choice(nodes)["steps"]
    if kind == 0 and "ln_z_lo" in c.claim:
        c.claim["ln_z_lo"] += Fraction(rng.choice([1, 1000, 10 ** 6]), 10 ** 6)
    elif kind == 1 and "ln_z_hi" in c.claim:
        c.claim["ln_z_hi"] -= Fraction(rng.choice([1, 1000, 10 ** 6]), 10 ** 6)
    elif kind == 2 and steps:
        s = rng.choice(steps)
        if s["op"] == "prune":
            s["dominator"] = rng.randrange(c.model.sizes[s["site"]])
        else:
            s["f"][rng.randrange(len(s["f"]))] += rng.choice([-3, 3, 10 ** 4])
    elif kind == 3 and steps:
        s = rng.choice(steps)
        if s["op"] == "prune":
            s["remove"] = rng.randrange(c.model.sizes[s["site"]])
        else:
            s["g"][rng.randrange(len(s["g"]))] -= rng.choice([1, 7])
    elif kind == 4:
        c.claim = {}                                             # no claim: the checker's own interval
    elif kind == 5 and steps:
        steps.append(copy.deepcopy(rng.choice(steps)))           # a repeated step
    else:
        i = rng.randrange(len(c.domains))
        extra = [a for a in range(c.model.sizes[i]) if a not in c.domains[i]]
        if extra:
            c.domains[i] = c.domains[i] + [rng.choice(extra)]
    return c


def enumerated_z(model, beta, doms, keep=None):
    unit = mpmath.mpf(1) / (2 ** model.scale_bits)
    b = mpmath.mpf(beta.numerator) / beta.denominator
    total, parts = mpmath.mpf(0), {}
    for x, e in brute_force_energies(model, doms):
        w = mpmath.exp(-b * e * unit)
        total += w
        if keep is not None:
            parts[x[keep]] = parts.get(x[keep], mpmath.mpf(0)) + w
    return total, parts


def frac(q):
    return mpmath.mpf(q.numerator) / q.denominator


def main():
    t0 = time.time()
    stats = {"min_checks": 0, "min_accepted": 0, "min_unsound": 0, "min_memory_vs_text_disagree": 0,
             "z_checks": 0, "z_accepted": 0, "z_unsound": 0, "populations_checked": 0, "populations_unsound": 0}

    for trial in range(700):
        m = random_model(rng.randint(1, 5), 4, rng.choice([3, 50, 10 ** 6]))
        box = random_box(m)
        try:
            cert = certify_gmec(m, domains=box, eliminate=rng.random() < 0.7, max_nodes=2000)
        except Exception:  # noqa: BLE001  (an abstention of the producer is not the subject)
            continue
        for c in [cert] + [mutate_min(cert) for _ in range(6)]:
            stats["min_checks"] += 1
            r = check_min_certificate(c)
            try:
                if check_text(mincert.dumps(c)).accepted != r.accepted:
                    stats["min_memory_vs_text_disagree"] += 1
                    print("DISAGREE memory/text", trial)
            except mincert.MalformedCertificate:
                if r.accepted:
                    stats["min_memory_vs_text_disagree"] += 1
                    print("DISAGREE: accepted in memory, not writable", trial)
            if not r.accepted:
                continue
            stats["min_accepted"] += 1
            emin, _ = brute_force_min(c.model, [[int(a) for a in d] for d in c.domains])
            true_min = Fraction(emin, 2 ** c.model.scale_bits)
            if r.lower_bound > true_min or (r.witness_energy is not None and r.witness_energy < true_min):
                stats["min_unsound"] += 1
                print("UNSOUND min", trial, r.lower_bound, true_min)

    eps = mpmath.mpf(10) ** -40
    for trial in range(260):
        m = random_model(rng.randint(1, 5), 3, rng.choice([2, 20, 200]))
        beta = Fraction(rng.choice([1, 3, 1000]), rng.choice([1, 7, 593]))
        box = random_box(m)
        keep = rng.choice([None, rng.randrange(m.n)])
        tier = rng.choice(["exact", "float"])
        try:
            cert = certify_partition(m, beta, domains=box, keep=keep, tau=rng.choice([None, 0.5, 5.0]),
                                     theta=rng.choice([None, 0.01, 1.0]), arithmetic=tier,
                                     max_leaves=rng.choice([1, 4]))
        except Exception:  # noqa: BLE001
            continue
        other = "float" if tier == "exact" else "exact"
        for c in [cert] + [mutate_z(cert) for _ in range(5)]:
            for arithmetic, bits in ((tier, 64), (other, rng.choice([16, 48, 96, 400]))):
                stats["z_checks"] += 1
                r = check_partition_certificate(c, arithmetic=arithmetic, exp_bits=bits)
                if not r.accepted:
                    continue
                stats["z_accepted"] += 1
                total, parts = enumerated_z(c.model, c.beta, [[int(a) for a in d] for d in c.domains], c.keep)
                lnz = mpmath.log(total)
                if not (frac(r.ln_z_lo) <= lnz + eps and lnz - eps <= frac(r.ln_z_hi)):
                    stats["z_unsound"] += 1
                    print("UNSOUND Z", trial, arithmetic, bits)
                if c.keep is not None:
                    for a in range(c.model.sizes[c.keep]):
                        p = parts.get(a, mpmath.mpf(0)) / total
                        lo, hi = r.population(a)
                        stats["populations_checked"] += 1
                        if not (frac(lo) <= p + eps and p - eps <= frac(hi)):
                            stats["populations_unsound"] += 1
                            print("UNSOUND population", trial, a)

    print(f"commit of the code in memory: {START_COMMIT}; seed {SEED}; {time.time() - t0:.0f} s")
    print(stats)
    failures = sum(v for k, v in stats.items() if k.endswith("unsound") or k.endswith("disagree"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
