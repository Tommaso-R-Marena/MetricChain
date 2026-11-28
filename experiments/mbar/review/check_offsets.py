"""Referee A -- numerical trap: state-dependent energy offsets (large |f_k|).  The data below are
ordinary (strong overlap, 100 samples per state); only a constant is added to each state's energy."""
import sys, warnings, traceback
import numpy as np
sys.path.insert(0, "../src")
from d9mbar.estimators import mbar
from d9mbar.certificates import lr_confidence_region
warnings.filterwarnings("ignore")
for off_scale in (0.0, 10.0, 30.0, 50.0, 100.0, 300.0, 1000.0):
    res = {}
    for rep in range(20):
        rng = np.random.default_rng(100 + rep)
        K, n = 4, 100
        ks = np.ones(K); x0 = 0.7 * np.arange(K)
        off = off_scale * rng.normal(size=K)
        x = np.concatenate([rng.normal(x0[k], 1.0, n) for k in range(K)])
        y = np.repeat(np.arange(K), n)
        perm = rng.permutation(K * n); x, y = x[perm], y[perm]
        U = 0.5 * (x[:, None] - x0[None, :]) ** 2 + off[None, :]
        try:
            f, info = mbar(U, y)
            key = "mbar ok (err %.0e)" % 10 ** np.ceil(np.log10(np.abs((f - f[0]) - (off - off[0])).max() + 1e-300))
        except Exception as e:
            key = "mbar " + type(e).__name__
        try:
            reg = lr_confidence_region(U, y)
            key2 = "region " + reg.status
            if reg.status == "OK":
                lo, hi = reg.interval(np.array([-1.0, 0, 0, 1.0]))
                key2 += " finite" if np.isfinite(hi - lo) else " INFINITE interval"
        except Exception as e:
            key2 = "region EXCEPTION " + type(e).__name__
            if "tb" not in res:
                res["tb"] = traceback.format_exc().strip().splitlines()[-6:]
        res[(key, key2)] = res.get((key, key2), 0) + 1
    tb = res.pop("tb", None)
    print(f"offset scale {off_scale:7.1f}:", res)
    if tb:
        print("    traceback tail:", " | ".join(s.strip() for s in tb))
