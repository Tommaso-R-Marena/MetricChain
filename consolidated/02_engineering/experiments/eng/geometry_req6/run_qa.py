"""Driver for (Q-a) of GEOMETRY-REQ-0006: the global maximisers of H_c on the 4-torus.

    python run_qa.py            # instance A -> results/qa_instance_A.json

NOT TRUSTED (orchestration and bookkeeping, see gr6_records.py).  Runs, for instance A with the
rounded couplings: certificate R (reduced to the two middle torsions), certificate D (direct, on
the 4-torus), and the certificate of the supremum away from the two maximisers ("second local
maximum").  Cost: certificate R under a second, certificate D about ten seconds.
"""
from __future__ import annotations

import sys
import time

import gr6_common as common

common.limit_memory()

import gr6_kernel as kernel  # noqa: E402
import gr6_records as records  # noqa: E402
import gr6_search as search  # noqa: E402
from gr6_common import enclosure  # noqa: E402


def main():
    kernel.set_precision()
    rec, obj = records.certificate_record(common.INSTANCE_A, direct=True)
    form, centre = obj["form"], obj["centre"]
    rec["request"] = "GEOMETRY-REQ-0006 (Q-a)"
    rec["precision_bits"] = kernel.PREC
    rec["statement"] = ("certified == true (certificate R) and direct.certified == true (certificate D), each on its "
                        "own: on the torus T^4 the function H_c (couplings as listed, exact rationals) attains its "
                        "maximum exactly at +-theta^, theta^ in maximiser_radians; every other theta is strictly "
                        "below.  Proof structure: gr6_qa_proof.py.")
    # the supremum away from the two maximisers ("second local maximum")
    t0 = time.perf_counter()
    maxima = search.local_maxima(form, starts=200, seed=0)
    rec["local_maxima_float"] = [{"H": v, "theta": [float(x) for x in t]} for v, t in maxima]
    rec["seconds"]["multistart_float"] = time.perf_counter() - t0
    if len(maxima) > 1 and rec["certified"]:
        other, _ = search.refine_critical(form, maxima[1][1])
        out, r2 = records.outside_record(form, centre, other)
        out["statement"] = ("certified == true: H(theta) <= second_maximum for every theta in T^4 whose "
                            "(theta_1, theta_2) is not in the interior of the hill region N (the listed boxes "
                            "(level, j1, j2) of the (theta_1, theta_2)-plane: two neighbourhoods of "
                            "+-(theta^_1, theta^_2)), with equality exactly at +-theta2^ (second_maximiser_radians), "
                            "a strict local maximiser.")
        if r2["certified"]:
            out["margin"] = enclosure(records.plus_local(obj["result"])["H"] - records.plus_local(r2)["H"], 36)
        rec["outside"] = out
    path = common.write_json("qa_instance_A.json", rec)
    print(f"certificate R: {rec['certified']};  certificate D: {rec['direct']['certified']};  "
          f"maximum in {rec.get('maximum')};  wrote results/{path.name}")
    return 0 if rec["certified"] and rec["direct"]["certified"] else 1


if __name__ == "__main__":
    sys.exit(main())
