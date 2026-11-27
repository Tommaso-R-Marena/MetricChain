import math, sys
sys.path.insert(0, sys.argv[1] + "/src")
import numpy as np
from metricchain_sb import mincert, zcert
from metricchain_sb.model import PairModel
from metricchain_sb.zcheck import check_partition_certificate
m = PairModel(unary=[np.array([0, 678]), np.array([0])], pair={(0, 1): np.array([[677], [0]])}, scale_bits=0)
sha = mincert.model_sha256(m)
text = ('{"format":"structbio-zcert/1","model_sha256":"%s","beta":"1/1","domains":[[0,1],[0]],"keep":null,"claim":{},'
        '"root":{"steps":[],"order":[1,0]},"meta":"{}"}' % sha)
cert = zcert.loads(text, model=m)
truth = -677 + math.log1p(math.exp(-1.0))          # ln(e^-677 + e^-678): the two configurations have energies 677 and 678
print("model_sha256", sha[:16], " energies", m.energy((0, 0)), m.energy((1, 0)), " ln Z =", repr(truth))
for tier, bits in (("exact", 64), ("float", 64), ("exact", 990), ("float", 980), ("float", 990), ("float", 991), ("float", 992)):
    try:
        r = check_partition_certificate(cert, arithmetic=tier, exp_bits=bits)
        d = {k: getattr(r, k) for k in dir(r) if not k.startswith("_") and not callable(getattr(r, k))}
        lo = hi = None
        for k, v in d.items():
            if "ln" in k.lower() and isinstance(v, (tuple, list)) and len(v) == 2:
                lo, hi = float(v[0]), float(v[1])
        if lo is None:
            cand = {k: v for k, v in d.items() if any(s in k.lower() for s in ("lo", "hi", "lower", "upper"))}
            print(tier, bits, "accepted", d.get("accepted"), {k: (float(v) if v is not None and not isinstance(v, (str, dict, list, tuple)) else v) for k, v in cand.items()}, "reason", d.get("reason"))
        else:
            print(tier, bits, "accepted", d.get("accepted"), "ln Z in [%.9f, %.9f]" % (lo, hi), "contains the truth:", lo <= truth <= hi, "| reason", d.get("reason"))
    except Exception as exc:
        print(tier, bits, "raised", type(exc).__name__, str(exc)[:100])
