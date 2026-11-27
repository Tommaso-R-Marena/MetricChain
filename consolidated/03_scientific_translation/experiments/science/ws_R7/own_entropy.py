"""R7 OWN distance entropy sigma(rho) of the generic chain (definition from ENG-RES-0009 section 2 text,
code written before reading engineering code).

m_c(rho) = #{classes within profile distance rho*N of class c, itself included}
sigma(rho) = (1/n) * mean over classes of ln m_c(rho)
also: median over classes, and mean weighted by the number of conformations in the class.
"""
import ctypes, json, math, sys, time
import numpy as np
import own_gen as og

lib = ctypes.CDLL("./l1kern.so")
dp = ctypes.POINTER(ctypes.c_double)
ip = ctypes.POINTER(ctypes.c_int64)
lib.l1_ball_counts.argtypes = [dp, ctypes.c_int64, ctypes.c_int64, dp, ctypes.c_int64, ctypes.c_double, ip, dp]
lib.l1_nearest.argtypes = [dp, ctypes.c_int64, ctypes.c_int64, dp]
lib.l1_full.argtypes = [dp, ctypes.c_int64, ctypes.c_int64, dp]

RHOS = [0.25, 0.5, 1.0, 1.25, 2.5, 5.0]

def classes(n):
    words = og.enumerate_words(n)
    S = og.truncated_sorted_sq(words)
    cid, ncls, info = og.profile_classes(S)
    order = np.argsort(cid, kind="stable")
    first = np.zeros(ncls, dtype=np.int64)
    first[cid[order][::-1]] = order[::-1]
    size = np.bincount(cid, minlength=ncls)
    Srep = np.ascontiguousarray(S[first])
    return words, cid, ncls, Srep, size, info

def entropy(n, tol=1e-9):
    words, cid, ncls, Srep, size, info = classes(n)
    N = n + 3
    C, P = Srep.shape
    thr = np.array([r * N for r in RHOS])
    counts = np.zeros((len(RHOS), C), dtype=np.int64)
    mind = np.zeros(len(RHOS))
    lib.l1_ball_counts(Srep.ctypes.data_as(dp), C, P, thr.ctypes.data_as(dp), len(RHOS), tol,
                       counts.ctypes.data_as(ip), mind.ctypes.data_as(dp))
    nn = np.zeros(C)
    lib.l1_nearest(Srep.ctypes.data_as(dp), C, P, nn.ctypes.data_as(dp))
    out = dict(n=n, N=N, conformations=int(len(words)), classes=int(ncls), ln_classes_over_n=math.log(ncls) / n,
               nearest_distinct_classes=float(nn.min()), sigma_mean={}, sigma_median={}, sigma_weighted={},
               min_margin={})
    for t, r in enumerate(RHOS):
        lm = np.log(counts[t])
        out["sigma_mean"][str(r)] = float(lm.mean() / n)
        out["sigma_median"][str(r)] = float(np.median(lm) / n)
        out["sigma_weighted"][str(r)] = float((lm * size).sum() / size.sum() / n)
        out["min_margin"][str(r)] = float(mind[t])
    return out

if __name__ == "__main__":
    res = []
    for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        t0 = time.time()
        r = entropy(n)
        r["seconds"] = time.time() - t0
        res.append(r)
        print(f"n={n} conf={r['conformations']} classes={r['classes']} lnC/n={r['ln_classes_over_n']:.3f} "
              + " ".join(f"s({k})={v:.3f}" for k, v in r["sigma_mean"].items())
              + f" nearest_classes={r['nearest_distinct_classes']:.4f} t={r['seconds']:.1f}s", flush=True)
        json.dump(res, open(f"out_own_entropy_{sys.argv[1]}_{sys.argv[2]}.json", "w"), indent=1)
