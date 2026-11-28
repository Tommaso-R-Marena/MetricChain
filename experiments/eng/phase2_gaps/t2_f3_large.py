"""T2 (d), finding F3 beyond findings_repro.py: a prune step with margin -9, -9.5 (scale_bits 1), -30, -20000 kT on the
one-site instance of F3, exact and float tier, at a given SB worktree; time and outcome of each call (30 s alarm).

    <their python> experiments/eng/phase2_gaps/t2_f3_large.py <sb-worktree>
"""
from __future__ import annotations

import json
import signal
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "src"))
import numpy as np  # noqa: E402
from metricchain_sb import mincert, zcert  # noqa: E402
from metricchain_sb.model import PairModel  # noqa: E402
from metricchain_sb.zcheck import check_partition_certificate  # noqa: E402


class Alarm(BaseException):
    pass


def fire(*_):
    raise Alarm()


signal.signal(signal.SIGALRM, fire)
for x, sb in ((9, 0), (19, 1), (30, 0), (20000, 0)):     # margin = -x / 2**sb kT (beta = 1)
    m = PairModel(unary=[np.array([0, x])], pair={}, scale_bits=sb)
    text = ('{"format":"structbio-zcert/1","model_sha256":"%s","beta":"1/1","domains":[[0,1]],"keep":null,"claim":{},'
            '"root":{"steps":[{"op":"prune","site":0,"remove":0,"dominator":1}],"order":[0]},"meta":"{}"}' % mincert.model_sha256(m))
    cert = zcert.loads(text, model=m)
    for tier in ("exact", "float"):
        t0 = time.perf_counter()
        signal.alarm(30)
        try:
            r = check_partition_certificate(cert, arithmetic=tier)
            out = dict(accepted=r.accepted, reason=r.reason[:110], hi=float(r.ln_z_hi) if r.accepted else None)
        except Alarm:
            out = dict(outcome="no return within 30 s")
        finally:
            signal.alarm(0)
        print(json.dumps(dict(margin_kT=-x / 2 ** sb, tier=tier, seconds=round(time.perf_counter() - t0, 3), **out)), flush=True)
