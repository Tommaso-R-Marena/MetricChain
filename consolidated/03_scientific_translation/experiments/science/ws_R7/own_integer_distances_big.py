"""R7 OWN: integer-valued profile distances and ties of the cover relation at L = 1 for larger n (no matrix stored).
For each n and each eps in {0, 1, N/20, N/10, N/4, N/2}: number of ordered (centre, point) pairs with
|D - (gmin(point) + eps)| < 1e-9 (exact ties) and the nearest non-tie."""
import ctypes, json, sys, time
import numpy as np
import own_cover as oc

lib = ctypes.CDLL("./l1kern.so")
dp = ctypes.POINTER(ctypes.c_double); ip = ctypes.POINTER(ctypes.c_int64)
lib.l1_integer_stats.argtypes = [dp, ctypes.c_int64, ctypes.c_int64, dp, dp, ctypes.c_int64, ctypes.c_double, ip, dp, ip, dp]
out = []
for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    t0 = time.time()
    cd = oc.class_data(n)
    S = np.ascontiguousarray(cd["Srep"]); C, P = S.shape
    N = n + 3
    names = ["0", "1", "N/20", "N/10", "N/4", "N/2"]
    eps = np.array([0.0, 1.0, N / 20, N / 10, N / 4, N / 2])
    gmin = cd["mingap"].astype(np.float64)
    n_int = ctypes.c_int64(0); near = ctypes.c_double(0.0)
    ties = np.zeros(len(eps), dtype=np.int64); nearest = np.zeros(len(eps))
    lib.l1_integer_stats(S.ctypes.data_as(dp), C, P, gmin.ctypes.data_as(dp), eps.ctypes.data_as(dp), len(eps), 1e-9,
                         ctypes.byref(n_int), ctypes.byref(near), ties.ctypes.data_as(ip), nearest.ctypes.data_as(dp))
    rec = dict(n=n, classes=int(C), integer_valued_pairs=int(n_int.value), nearest_non_integer=float(near.value),
               ties_L1={k: int(v) for k, v in zip(names, ties)}, nearest_non_tie_L1={k: float(v) for k, v in zip(names, nearest)},
               seconds=round(time.time() - t0, 1))
    out.append(rec); print(rec, flush=True)
    json.dump(out, open(f"out_own_integer_distances_big_{sys.argv[1]}_{sys.argv[2]}.json", "w"), indent=1)
