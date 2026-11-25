"""R7 OWN: exact ties in the comparisons D <= rho*N of the distance entropy (ENG-RES-0009 section 2), and the nearest non-tie.
(l1_integer_stats with gmin = 0 and eps = the six radii; ordered pairs are counted, so an unordered tie counts twice.)"""
import ctypes, json, sys
import numpy as np
import own_cover as oc
lib = ctypes.CDLL("./l1kern.so")
dp = ctypes.POINTER(ctypes.c_double); ip = ctypes.POINTER(ctypes.c_int64)
lib.l1_integer_stats.argtypes = [dp, ctypes.c_int64, ctypes.c_int64, dp, dp, ctypes.c_int64, ctypes.c_double, ip, dp, ip, dp]
RHOS = [0.25, 0.5, 1.0, 1.25, 2.5, 5.0]
out = []
for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    cd = oc.class_data(n)
    S = np.ascontiguousarray(cd["Srep"]); C, P = S.shape
    N = n + 3
    radii = np.array([r * N for r in RHOS]); zero = np.zeros(C)
    n_int = ctypes.c_int64(0); near = ctypes.c_double(0.0)
    ties = np.zeros(len(RHOS), dtype=np.int64); nearest = np.zeros(len(RHOS))
    lib.l1_integer_stats(S.ctypes.data_as(dp), C, P, zero.ctypes.data_as(dp), radii.ctypes.data_as(dp), len(RHOS), 1e-9,
                         ctypes.byref(n_int), ctypes.byref(near), ties.ctypes.data_as(ip), nearest.ctypes.data_as(dp))
    rec = dict(n=n, classes=int(C), unordered_ties={str(r): int(t) // 2 for r, t in zip(RHOS, ties)},
               nearest_non_tie={str(r): float(v) for r, v in zip(RHOS, nearest)})
    out.append(rec); print(rec, flush=True)
json.dump(out, open(f"out_own_entropy_ties_{sys.argv[1]}_{sys.argv[2]}.json", "w"), indent=1)
