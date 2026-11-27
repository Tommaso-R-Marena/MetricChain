"""Campaign Z1/Z2: their checker against enumeration and against the independent checker, on small instances.

For every random instance (1-6 sites, 1-4 states; graphs none/chain/tree/sparse/dense/star/one isolated site; zero,
tied, small, medium, large, penalised and additive tables; full boxes and sub-boxes; ten values of beta):

* one certificate from THEIR producer (random ``tau``, ``theta``, ``keep``, table budget and leaf budget, so that
  conditioning occurs), serialised with their ``dumps`` (it carries their claim);
* two certificates from the producer of ``gen`` (random trees that their producer would never emit: prunes with
  any margin, relaxations with arbitrary additive functions, conditioning on any site);
* every adversarial variant of one of the latter (``gen.variants``).

Each certificate text goes through (a) their loader and their checker in the exact tier, (b) the same in the float
tier with the claim removed, (c) ``indep_zcheck`` (exact mode; rounded mode when the exact mode abstains), and the
truth is enumerated with 400-bit Arb balls.  Recorded: verdicts and their agreement, containment of the truth by
every accepted interval (``ln Z`` and the population of every state of the kept site), the position of their
interval relative to the *ideal interval* of the certificate, and the float tier relative to the exact tier.

    python campaign_z12.py --seed 1 --instances 400 --out results/z12_seed1.json
"""
from __future__ import annotations

import resource

resource.setrlimit(resource.RLIMIT_AS, (3_000_000_000, 3_000_000_000))

import argparse  # noqa: E402
import collections  # noqa: E402
import json  # noqa: E402
import random  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from fractions import Fraction  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gen  # noqa: E402
import indep_zcheck as Z  # noqa: E402
import sb_bridge as B  # noqa: E402
import truth  # noqa: E402

TIME_LIMIT = 30               # seconds per call of their checker
PRUNE_Q_MAX = 14              # their checker is not run when a prune factor rho = exp(q) has q above this ...
EXPONENT_MAX = 30000          # ... or when a relax factor or a Boltzmann factor has |exponent| above this


def dec(x, digits: int = 25) -> str:
    """A rational as a decimal string (for the JSON files; comparisons are done on the exact values)."""
    if x is None:
        return "None"
    x = Fraction(x)
    sign = "-" if x < 0 else ""
    x = abs(x)
    whole = x.numerator // x.denominator
    frac = x - whole
    digs = (frac.numerator * 10 ** digits) // frac.denominator
    return f"{sign}{whole}.{digs:0{digits}d}"


def _nodigits(text: str) -> str:
    return "".join("#" if ch.isdigit() else ch for ch in text)


def box_as_sets(doc_domains, sizes):
    """The box a ``domains`` field denotes when read as a product of sets; ``None`` if it denotes none."""
    if not isinstance(doc_domains, list) or len(doc_domains) != len(sizes):
        return None
    out = []
    for d, k in zip(doc_domains, sizes):
        if not isinstance(d, list) or not d or any(type(a) is not int or not 0 <= a < k for a in d):
            return None
        out.append(sorted(set(d)))
    return out


class Run:
    def __init__(self, seed: int):
        self.rng = random.Random(seed)
        self.by = collections.defaultdict(collections.Counter)          # source -> counters
        self.rel = collections.Counter()
        self.flt = collections.Counter()
        self.disagree = collections.Counter()
        self.reasons_theirs = collections.Counter()
        self.examples = []
        self.findings = []
        self.excess_lo, self.excess_hi, self.excess_hi_noprune = [], [], []
        self.float_gap = []
        self.truth_cache = {}

    def truth_for(self, key, tables, beta, box):
        k = (key, beta, json.dumps(box))
        if k not in self.truth_cache:
            if len(self.truth_cache) > 64:
                self.truth_cache.clear()
            self.truth_cache[k] = truth.enumerate_truth(tables["unary"], tables["pair"], tables["scale_bits"], beta, box)
        return self.truth_cache[k]

    def finding(self, kind: str, source: str, text: str, tables: dict, extra: dict):
        rec = {"kind": kind, "source": source, "certificate": text,
               "tables": {"unary": tables["unary"], "pair": {f"{i},{j}": t for (i, j), t in tables["pair"].items()},
                          "scale_bits": tables["scale_bits"]}}
        rec.update(extra)
        if len(self.findings) < 40:
            self.findings.append(rec)

    # ------------------------------------------------------------------------------------------ one certificate
    def one(self, source: str, text: str, tables: dict, key, pm, mine):
        c = self.by[source]
        c["cases"] += 1
        sizes = [len(u) for u in tables["unary"]]
        try:
            doc = json.loads(text)
        except ValueError:
            doc = None
        # (c) the independent checker
        my = Z.check_text(text, mine)
        my_mode = "exact"
        if my.kind == "abstain":
            my = Z.check_text(text, mine, round_bits=256)
            my_mode = "rounded"
        if my.kind == "internal":
            c["mine_internal"] += 1
            self.finding("MINE-INTERNAL", source, text, tables, {"reason": my.reason})
        c["mine_accept" if my.accepted else "mine_reject"] += 1
        c["mine_" + my.kind] += 1
        if my_mode == "rounded" and my.accepted:
            c["mine_accept_rounded_mode"] += 1
        # is their checker about to need gigabytes?  (it keeps exp(rho) of a prune as an exact rational; see the
        # cost campaign) -- then it is not run on this certificate, and the case is counted
        hz = gen.hazard(doc, tables) if isinstance(doc, dict) else None
        if hz is not None and Fraction(doc["beta"]) < 0:
            hz = None                                   # their validation refuses a negative beta before any arithmetic
        if hz is not None and (hz[0] > PRUNE_Q_MAX or hz[1] > EXPONENT_MAX or hz[2] > EXPONENT_MAX):
            c["their_not_run_hazard"] += 1
            c["their_not_run_hazard_prune" if hz[0] > PRUNE_Q_MAX else "their_not_run_hazard_magnitude"] += 1
            if my.accepted:
                c["mine_accept_where_theirs_not_run"] += 1
                beta0 = Fraction(doc["beta"])
                box0 = box_as_sets(doc.get("domains"), sizes)
                tr0 = self.truth_for(key, tables, beta0, box0)
                v = tr0.ln_z_contains(my.ln_z_lo, my.ln_z_hi)
                c["mine_truth_" + v] += 1
                if v != "yes":
                    self.finding("MINE-MISSES-TRUTH", source, text, tables, {"verdict": v})
            return
        # (a) theirs, exact tier
        try:
            with B.time_limit(TIME_LIMIT):
                th = B.their_check_text(text, pm, "exact")
        except B.Timeout:
            c["their_timeout"] += 1
            self.finding(f"THEIR-TIMEOUT-{TIME_LIMIT}s", source, text, tables, {})
            return
        if th.get("exception"):
            c["their_exception"] += 1
            self.finding("THEIR-CHECKER-EXCEPTION", source, text, tables, {"exception": th["exception"]})
        if th.get("load_error") and th["load_error"].startswith("EXC"):
            c["their_loader_exception"] += 1
            self.finding("THEIR-LOADER-EXCEPTION", source, text, tables, {"exception": th["load_error"]})
        c["their_accept" if th["accepted"] else "their_reject"] += 1
        if not th["accepted"]:
            self.reasons_theirs[_nodigits(th["reason"].split(":")[0])[:60] if th.get("load_error") is None
                                else "loader: " + _nodigits(th["reason"])[:60]] += 1
        # agreement
        if th["accepted"] and my.accepted:
            c["agree_accept"] += 1
        elif not th["accepted"] and not my.accepted:
            c["agree_reject"] += 1
        elif th["accepted"]:
            c["only_theirs_accepts"] += 1
            self.disagree[f"{source} | theirs accepts | mine: {my.kind}: "
                          f"{_nodigits(my.reason.split(':')[-1].strip())[:70]}"] += 1
        else:
            c["only_mine_accepts"] += 1
            self.disagree[f"{source} | mine accepts | theirs: {_nodigits(th['reason'])[:80]}"] += 1
        # truth
        tr = None
        beta = None
        if doc is not None and isinstance(doc.get("beta"), str):
            try:
                beta = Fraction(doc["beta"])
            except (ValueError, ZeroDivisionError):
                beta = None
        box = box_as_sets(doc.get("domains") if isinstance(doc, dict) else None, sizes)
        if (th["accepted"] or my.accepted) and (box is None or beta is None):
            c["accepted_without_a_box"] += 1
            self.finding("ACCEPTED-BUT-NO-WELL-DEFINED-BOX", source, text, tables,
                         {"theirs": th["accepted"], "mine": my.accepted})
        elif th["accepted"] or my.accepted:
            tr = self.truth_for(key, tables, beta, box)
        keep = doc.get("keep") if isinstance(doc, dict) else None
        keep_ok = type(keep) is int and 0 <= keep < len(sizes)
        if tr is not None and my.accepted:
            v = tr.ln_z_contains(my.ln_z_lo, my.ln_z_hi)
            c["mine_truth_" + v] += 1
            if v != "yes":
                self.finding("MINE-MISSES-TRUTH", source, text, tables, {"verdict": v})
            if keep_ok:
                for a in range(sizes[keep]):
                    lo, hi = my.population(a)
                    v = tr.pop_contains(keep, a, lo, hi)
                    c["mine_pop_" + v] += 1
                    if v != "yes":
                        self.finding("MINE-POP-MISSES-TRUTH", source, text, tables, {"state": a, "verdict": v})
        if tr is not None and th["accepted"]:
            v = tr.ln_z_contains(th["lo"], th["hi"])
            c["their_truth_" + v] += 1
            if v == "no":
                c["their_unsound_lnz"] += 1
                self.finding("CRITICAL their exact tier accepts and misses ln Z", source, text, tables,
                             {"their_lo": dec(th["lo"]), "their_hi": dec(th["hi"]), "truth": truth.ball_text(tr.ln_z)})
            if keep_ok:
                for a in range(sizes[keep]):
                    p = B.their_population(th, a)
                    if p is None:
                        c["their_pop_missing"] += 1
                        continue
                    v = tr.pop_contains(keep, a, p[0], p[1])
                    c["their_pop_" + v] += 1
                    if v == "no":
                        c["their_unsound_pop"] += 1
                        self.finding("CRITICAL their exact tier accepts and misses a population", source, text, tables,
                                     {"state": a, "their": [dec(p[0]), dec(p[1])],
                                      "truth": truth.ball_text(tr.pop[keep][a]) if a in tr.pop[keep] else "0"})
        # position of their interval relative to the ideal interval of the certificate
        if th["accepted"] and my.accepted:
            r = self.rel
            r["both_accept"] += 1
            r["both_accept_" + my_mode] += 1
            inside = th["lo"] <= my.ln_z_lo and my.ln_z_hi <= th["hi"]
            r["mine_inside_theirs"] += inside
            if th["lo"] > my.ideal_lo[1]:
                r["their_lo_above_ideal_lo"] += 1
                self.finding("their lower bound exceeds what the rules prove", source, text, tables,
                             {"their_lo": dec(th["lo"]), "ideal_lo": dec(my.ideal_lo[1])})
            if th["hi"] < my.ideal_hi[0]:
                r["their_hi_below_ideal_hi"] += 1
                self.finding("their upper bound is below what the rules prove", source, text, tables,
                             {"their_hi": dec(th["hi"]), "ideal_hi": dec(my.ideal_hi[0])})
            scale = max(Fraction(1), abs(my.ln_z_lo), abs(my.ln_z_hi))
            ex_lo = (my.ideal_lo[0] - th["lo"]) / scale
            ex_hi = (th["hi"] - my.ideal_hi[1]) / scale
            self.excess_lo.append(float(ex_lo))
            self.excess_hi.append(float(ex_hi))
            if my.stats.get("prunes", 0) == 0:
                self.excess_hi_noprune.append(float(ex_hi))
            if keep_ok:
                for a in range(sizes[keep]):
                    p = B.their_population(th, a)
                    if p is None or a not in my.pop_ideal:
                        continue
                    r["pop_compared"] += 1
                    (ilo_dn, ilo_up), (ihi_dn, ihi_up) = my.pop_ideal[a]
                    if p[0] > ilo_up:
                        r["their_pop_lo_above_ideal"] += 1
                        self.finding("their population lower bound exceeds what the rules prove", source, text, tables,
                                     {"state": a, "their": dec(p[0]), "ideal": dec(ilo_up)})
                    if p[1] < ihi_dn:
                        r["their_pop_hi_below_ideal"] += 1
                        self.finding("their population upper bound is below what the rules prove", source, text,
                                     tables, {"state": a, "their": dec(p[1]), "ideal": dec(ihi_dn)})
                    r["mine_pop_inside_theirs"] += (p[0] <= my.population(a)[0] and my.population(a)[1] <= p[1])
        # (b) the float tier, claim removed
        if doc is not None and isinstance(doc, dict) and th.get("load_error") is None:
            f = self.flt
            if doc.get("claim"):
                with B.time_limit(TIME_LIMIT):
                    fc = B.their_check_text(text, pm, "float")
                f["with_their_exact_claim"] += 1
                f["with_their_exact_claim_rejected_by_float_tier"] += (th["accepted"] and not fc["accepted"])
                doc2 = dict(doc)
                doc2["claim"] = {}
                text2 = gen.dumps(doc2)
                with B.time_limit(TIME_LIMIT):
                    th2 = B.their_check_text(text2, pm, "exact")
            else:
                text2, th2 = text, th
            with B.time_limit(TIME_LIMIT):
                fl = B.their_check_text(text2, pm, "float")
            f["cases"] += 1
            if fl.get("exception"):
                f["float_exception"] += 1
                self.finding("THEIR-CHECKER-EXCEPTION (float tier)", source, text2, tables, {"exception": fl["exception"]})
            if fl["accepted"] and th2["accepted"]:
                f["both_tiers_accept"] += 1
                contains = fl["lo"] <= th2["lo"] and th2["hi"] <= fl["hi"]
                f["float_contains_exact"] += contains
                if not contains:
                    f["float_lo_above_exact_lo"] += fl["lo"] > th2["lo"]
                    f["float_hi_below_exact_hi"] += fl["hi"] < th2["hi"]
                    scale = max(Fraction(1), abs(th2["lo"]), abs(th2["hi"]))
                    gap = max(fl["lo"] - th2["lo"], th2["hi"] - fl["hi"]) / scale
                    self.float_gap.append(float(gap))
                    if len([x for x in self.examples if x["kind"] == "float tier not containing exact tier"]) < 3:
                        self.examples.append({"kind": "float tier not containing exact tier", "certificate": text2,
                                              "tables": {"unary": tables["unary"],
                                                         "pair": {f"{i},{j}": t for (i, j), t in tables["pair"].items()},
                                                         "scale_bits": tables["scale_bits"]},
                                              "exact": [dec(th2["lo"]), dec(th2["hi"])],
                                              "float": [dec(fl["lo"]), dec(fl["hi"])]})
            elif fl["accepted"] != th2["accepted"]:
                f["tiers_disagree_on_acceptance"] += 1
                f["only_float_accepts" if fl["accepted"] else "only_exact_accepts"] += 1
                self.disagree[f"tiers | exact: {th2['reason'][:50]} | float: {fl['reason'][:70]}"] += 1
            else:
                f["both_tiers_reject"] += 1
            if fl["accepted"] and tr is not None:
                v = tr.ln_z_contains(fl["lo"], fl["hi"])
                f["float_truth_" + v] += 1
                if v == "no":
                    f["float_unsound_lnz"] += 1
                    self.finding("CRITICAL their float tier accepts and misses ln Z", source, text2, tables,
                                 {"their_lo": dec(fl["lo"]), "their_hi": dec(fl["hi"]),
                                  "truth": truth.ball_text(tr.ln_z)})
                if keep_ok:
                    for a in range(sizes[keep]):
                        p = B.their_population(fl, a)
                        if p is None:
                            continue
                        v = tr.pop_contains(keep, a, p[0], p[1])
                        f["float_pop_" + v] += 1
                        if v == "no":
                            f["float_unsound_pop"] += 1
                            self.finding("CRITICAL their float tier accepts and misses a population", source, text2,
                                         tables, {"state": a, "their": [dec(p[0]), dec(p[1])]})

    # --------------------------------------------------------------------------------------------- one instance
    def instance(self, index: int):
        rng = self.rng
        S = B.sb()
        tables = gen.random_tables(rng)
        tame = rng.random() < 0.9
        if tame:
            gen.temper(rng, tables, max(gen.BETAS), 600)
        self.rel["instances_tempered" if tame else "instances_not_tempered"] += 1
        sizes = [len(u) for u in tables["unary"]]
        n = len(sizes)
        pm = B.pair_model(tables)
        mine = Z.make_model(tables["unary"], tables["pair"], tables["scale_bits"])
        sha = Z.model_sha256(mine)
        if sha != S["mincert"].model_sha256(pm):
            self.rel["checksum_mismatch"] += 1
        self.rel["instances"] += 1
        beta = rng.choice(gen.BETAS)
        box = gen.random_box(rng, sizes)
        # their producer
        unit = 2 ** tables["scale_bits"]
        kw = {"domains": box, "keep": rng.randrange(n) if rng.random() < 0.5 else None}
        if rng.random() < 0.7:
            kw["tau"] = Fraction(rng.choice([0, 1, 5, 40, 400, 5000]), unit) * rng.choice([1, 1, unit])
        if rng.random() < 0.7:
            kw["theta"] = Fraction(rng.choice([0, 1, 3, 20, 200]), unit) * rng.choice([1, 1, unit])
        if rng.random() < 0.6:
            kw["max_entries"] = rng.choice([1, 2, 4, 8, 16, 64])
            kw["max_leaves"] = rng.choice([1, 4, 64, 1000])
        try:
            cert = S["partition"].certify_partition(pm, beta, **kw)
            text = S["zcert"].dumps(cert)
        except S["partition"].PartitionBudgetExceeded:
            self.rel["their_producer_abstained"] += 1
            text = None
        except Exception as exc:                                       # noqa: BLE001
            self.rel["their_producer_exception"] += 1
            self.rel["their_producer_exception_" + type(exc).__name__] += 1
            text = None
        if text is not None:
            self.rel["their_producer_certificates"] += 1
            self.rel["their_producer_with_branch"] += '"branch"' in text
            self.one("their producer", text, tables, index, pm, mine)
        # the producer of gen
        base = None
        for _ in range(2):
            if tame:
                doc = gen.random_certificate(rng, tables, sha, beta=rng.choice(gen.BETAS), max_prune_kt=12, wild_kt=200)
            else:
                doc = gen.random_certificate(rng, tables, sha, beta=rng.choice(gen.BETAS))
            self.one("gen producer", gen.dumps(doc), tables, index, pm, mine)
            base = doc
        for name, expect, d in gen.variants(rng, base, tables):
            self.one(f"variant {name}", gen.dumps(d), tables, index, pm, mine)

    def summary(self, seconds: float, seed: int) -> dict:
        def stats(values):
            if not values:
                return {"n": 0}
            v = sorted(values)
            return {"n": len(v), "min": v[0], "median": v[len(v) // 2], "p99": v[min(len(v) - 1, int(0.99 * len(v)))],
                    "max": v[-1]}
        return {"campaign": "z12", "seed": seed, "seconds": round(seconds, 1),
                "by_source": {k: dict(v) for k, v in sorted(self.by.items())},
                "relation": dict(self.rel), "float_tier": dict(self.flt),
                "excess_lo_relative": stats(self.excess_lo), "excess_hi_relative": stats(self.excess_hi),
                "excess_hi_relative_without_prunes": stats(self.excess_hi_noprune),
                "float_inside_exact_gap_relative": stats(self.float_gap),
                "disagreements": dict(self.disagree.most_common()), "their_reject_reasons": dict(self.reasons_theirs),
                "examples": self.examples, "findings": self.findings}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--instances", type=int, default=200)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    run = Run(args.seed)
    t0 = time.time()
    for index in range(args.instances):
        run.instance(index)
    out = run.summary(time.time() - t0, args.seed)
    out["instances"] = args.instances
    path = Path(args.out) if args.out else HERE / "results" / f"z12_seed{args.seed}.json"
    path.write_text(json.dumps(out, indent=1))
    tot = collections.Counter()
    for v in out["by_source"].values():
        tot.update(v)
    print(json.dumps({"seconds": out["seconds"], "totals": dict(tot), "relation": out["relation"],
                      "float_tier": out["float_tier"], "findings": len(out["findings"])}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
