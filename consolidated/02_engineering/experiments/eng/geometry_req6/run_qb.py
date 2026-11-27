"""Driver for (Q-b) of GEOMETRY-REQ-0006: a realisation in R^4, of affine dimension 4, with the
squared lengths of the certified maximiser X^ = X(theta^) on the 16 pairs of F u E0.

    python run_qb.py            # instance A, stored candidate -> results/qb_instance_A.json
    python run_qb.py --search   # use the candidate proposed by the search heuristics instead
                                # -> results/qb_instance_A_search.json

NOT TRUSTED (orchestration and bookkeeping, see gr6_records.py): the statement comes from
gr6_qb_proof.certify_realisation; the targets are the balls |x_i - x_j|^2 evaluated on the
enclosure of theta^ certified by gr6_qa_proof (so the statement holds for the lengths of X^).
"""
from __future__ import annotations

import sys
import time

import gr6_common as common

common.limit_memory()

import numpy as np  # noqa: E402

import gr6_kernel as kernel  # noqa: E402
import gr6_model as model  # noqa: E402
import gr6_qb_proof as QB  # noqa: E402
import gr6_records as records  # noqa: E402
import gr6_search as search  # noqa: E402
from gr6_common import enclosure  # noqa: E402


def main(argv):
    kernel.set_precision()
    inst = common.INSTANCE_A
    n, edges = inst["n"], model.statewise_pairs(inst["n"]) + inst["pairs"]
    qa, obj = records.certificate_record(inst, log=lambda *a: None)
    if not qa["certified"]:
        print("(Q-a) is not certified: no enclosure of the maximiser")
        return 1
    K = records.plus_local(obj["result"])["K"]
    targets = records.length_targets(obj["chain"], edges, K)
    rec = {"request": "GEOMETRY-REQ-0006 (Q-b)", "instance": inst["name"], "precision_bits": kernel.PREC,
           "couplings": qa["couplings"], "maximiser_radians": qa["maximiser_radians"],
           "pairs": [list(e) for e in edges],
           "targets": {f"{i}-{j}": enclosure(t, 30) for (i, j), t in zip(edges, targets)}}
    cand = records.CANDIDATE_A
    if "--search" in argv:
        X = model.nerf_chain([float(k.mid()) * np.pi for k in K])
        _, Om, _ = search.stress(X, edges)
        cand, rec["search"] = records.find_candidate(X, edges, Om)
        if cand is None:
            print("the search found no non-flat candidate")
            return 1
        print("candidate proposed by the search: pins", {u: str(v) for u, v in cand["pins"].items()})
    t0 = time.perf_counter()
    cert, resid = records.certify_candidate(n, edges, targets, cand)
    rec.update(records.realisation_record(n, edges, targets, cert, cand))
    rec["newton_residual"] = resid
    rec["seconds"] = time.perf_counter() - t0
    if cert["ok"]:
        # the pairs that are not constrained: a certified difference between the realisation and X^
        Y = cert["Y"]
        P = [kernel.point(t) for t in K]
        rec["unconstrained_pairs"] = {}
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) not in edges:
                    dy, dx = QB.sq_length(Y, i, j), kernel.ma_eval(obj["chain"].sqdist(i, j), P)
                    rec["unconstrained_pairs"][f"{i}-{j}"] = {
                        "realisation": enclosure(dy, 20), "chain": enclosure(dx, 20), "difference": enclosure(dy - dx, 20)}
    rec["statement"] = ("certified == true: there is a configuration of 7 points in R^4 (coordinates in "
                        "'configuration', gauge of gr6_qb_proof.py, pinned coordinates exact) whose squared lengths on "
                        "the 16 pairs equal those of X(theta^) for the maximiser theta^ of (Q-a), and whose centred "
                        "configuration matrix has all four singular values >= sigma_4_lower_bound > 0.")
    path = common.write_json("qb_instance_A_search.json" if "--search" in argv else "qb_instance_A.json", rec)
    print(f"certified: {rec['certified']};  sigma_4 >= {rec.get('sigma_4_lower_bound')};  wrote results/{path.name}")
    return 0 if rec["certified"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
