"""Two probes of the structural-biology division's software at its commit 0544ff4, beyond its own tests.

K8  ``CheckResult.full_box`` is true exactly when every root domain lists every state of its site: certificates on
    full boxes written in another order, on sub-boxes, and on boxes that differ from the full one in one site.
K5  (an extension of their own validation, with their code -- not an independent implementation): the table energy
    against the full-system OpenMM energy on many more configurations than their test uses, random ones included,
    on several structures and seeds.  Their claim: agreement to 4e-11 kcal/mol on low-energy configurations.

    <their python> experiments/eng/sb_review/probe_head.py --sb <copy of their tree> --out FILE [--structures 1CRN ...]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np


def probe_k8(sb) -> list:
    from metricchain_sb.mincert import MinCertificate
    from metricchain_sb.mincheck import check_min_certificate
    from metricchain_sb.model import PairModel
    m = PairModel(unary=[np.array([5, 7, 9]), np.array([0, 3])], pair={(0, 1): np.array([[0, 2], [1, 0], [4, 4]])})
    leaf = {"node": "leaf", "m": {}}
    out = []

    def case(name, domains, L, expect_full):
        root = {"node": "branch", "site": 0, "children": {a: {"node": "branch", "site": 1, "children": {b: leaf for b in domains[1]}} for a in domains[0]}}
        r = check_min_certificate(MinCertificate(model=m, message_bits=0, domains=domains, lower_bound=L, witness=None, root=root))
        out.append(dict(name=name, domains=domains, accepted=r.accepted, full_box=getattr(r, "full_box", None), expected_full_box=expect_full,
                        as_expected=bool(r.accepted) and getattr(r, "full_box", None) == expect_full, reason=r.reason))

    case("full box, states in order", [[0, 1, 2], [0, 1]], 5, True)
    case("full box, states in another order", [[2, 0, 1], [1, 0]], 5, True)
    case("one state of site 0 missing", [[0, 1], [0, 1]], 5, False)
    case("the minimiser's state missing: a true bound on the sub-box that is false globally", [[1, 2], [0, 1]], 7, False)
    case("one state of site 1 missing", [[0, 1, 2], [0]], 5, False)
    case("a single configuration", [[2], [1]], 13, False)
    return out


def probe_k5(sb: Path, structures, seeds, n_random, n_low) -> list:
    from metricchain_sb.molecular import build_energy_tables
    from metricchain_sb.molecular.reference import validate_against_openmm
    rows = []
    for pdb_id in structures:
        t0 = time.perf_counter()
        t = build_energy_tables(str(sb / "benchmarks" / "structbio" / "pdb" / f"{pdb_id}.pdb"), eps0=4.0, e_clip=1000.0,
                                max_states_per_site=None, include_native=True, seed=0)
        for seed in seeds:
            v = validate_against_openmm(t, n_random=n_random, seed=seed, n_clash_free=n_low)
            rows.append(dict(pdb_id=pdb_id, seed=seed,
                             random=dict(n=v["random"]["n"], max_abs_diff=v["random"]["max_abs_diff"], max_rel_diff=v["random"]["max_rel_diff"],
                                         max_abs_energy=v["random"]["max_abs_energy"], min_contact_ratio=v["random"]["min_contact_ratio"]),
                             low_energy=dict(n=v["clash_free"]["n"], max_abs_diff=v["clash_free"]["max_abs_diff"], max_rel_diff=v["clash_free"]["max_rel_diff"],
                                             max_abs_energy=v["clash_free"]["max_abs_energy"], min_contact_ratio=v["clash_free"]["min_contact_ratio"]),
                             bonded_constant_max_spread=v["bonded_constant_max_spread"]))
            print(json.dumps(rows[-1]), flush=True)
        print(f"{pdb_id}: {time.perf_counter() - t0:.0f} s", flush=True)
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sb", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--structures", nargs="*", default=["1CRN", "1UBQ"])
    ap.add_argument("--seeds", type=int, nargs="*", default=[1, 2, 3])
    ap.add_argument("--n-random", type=int, default=100)
    ap.add_argument("--n-low", type=int, default=100)
    args = ap.parse_args()
    sys.path.insert(0, str(args.sb / "src"))
    out = dict(k8=probe_k8(args.sb))
    for r in out["k8"]:
        print(json.dumps(r), flush=True)
    out["k5"] = probe_k5(args.sb, args.structures, args.seeds, args.n_random, args.n_low)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
