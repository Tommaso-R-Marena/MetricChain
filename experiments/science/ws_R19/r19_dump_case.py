#!/usr/bin/env python3
"""R19: re-run the coordinator's first_order_recovery.py (committed file, unmodified, in-process) and store, in MY directory,
the objects a later check needs: the tables of the two models, the items with their classes and routes, the group statistics
and the two ln Z as the driver computed them.  Nothing outside ws_R19 is written.

Run: python3 -B r19_dump_case.py K12 4 4 > r19_dump_case_K12_m4_w4.log     (writes case_K12_m4_w4.pkl)
"""
import os, sys, time, pickle, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "NUMEXPR_MAX_THREADS"):
    os.environ[v] = "1"
sys.dont_write_bytecode = True
PI = "/home/user/MetricChain/experiments/science/pi_inference"; HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PI)
import numpy as np
t00 = time.time(); args = sys.argv[1:]
import first_order_recovery as FOR
cap = {}


def _prof(frame, event, arg):
    if event == "return" and frame.f_code is FOR.main.__code__:
        cap.update(frame.f_locals)


sys.argv = [os.path.join(PI, "first_order_recovery.py")] + args
print("##### R19: output of the coordinator's driver (re-run, unmodified) #####", flush=True)
sys.setprofile(_prof)
try:
    FOR.main()
finally:
    sys.setprofile(None)


def tables(mdl):
    return dict(const=float(mdl.const), one=[np.array(v, dtype=float) for v in mdl.one], pair={k_: np.array(v, dtype=float) for k_, v in mdl.pair.items()},
                multi={k_: np.array(v, dtype=float) for k_, v in mdl.multi.items()})


name = list(cap["GS"].keys())[-1]
out = dict(args=args, n=cap["n"], k=list(cap["k"]), x0=list(cap["x0"]), m=cap["m"], w=cap["w"], beta=FOR.BETA, up=tables(cap["up"]), lo=tables(cap["lo"]),
           items=[(tuple(it[0]), np.array(it[1], dtype=float)) for it in cap["items"]], kind=list(cap["kind"]), rts=list(cap["rts"]),
           GS={st: {gk: dict(v) for gk, v in g.items()} for st, g in cap["GS"].items()}, last=name, lnZup=cap["lnZup"], lnZlo=cap["lnZlo"], res=dict(cap["res"]))
tag = f"{args[0].replace(':', 'c')}_m{args[1]}_w{args[2]}" + ("_enum" if "--enum" in args else "")
fn = os.path.join(HERE, f"case_{tag}.pkl")
assert not os.path.exists(fn), "refusing to overwrite " + fn
with open(fn, "wb") as f: pickle.dump(out, f)
print(f"##### R19: wrote {fn} ({os.path.getsize(fn) / 1e6:.1f} MB): {len(out['items'])} items, {len(out['GS'][name])} groups #####")
print(f"ALL DONE {time.time() - t00:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")
