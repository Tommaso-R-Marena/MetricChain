"""R7 OWN: hard-core margins of the generic chain (closest accepted pair above the core, closest rejected below)."""
import math, sys
import numpy as np
import own_gen as og

def margins(n, chunk=60000):
    words = np.zeros((1, 0), dtype=np.uint8)
    best_acc, best_rej = math.inf, math.inf   # min (s-3) over accepted conformations' pairs; min (3-s) over rejected pairs
    for level in range(1, n + 1):
        out = []
        for lo in range(0, len(words), chunk):
            w = words[lo:lo + chunk]
            ext = np.concatenate([np.repeat(w, 3, axis=0), np.tile(np.arange(3, dtype=np.uint8), len(w))[:, None]], axis=1)
            X = og.coords_from_words(ext)
            s = ((X[:, :level, :] - X[:, -1][:, None, :]) ** 2).sum(axis=2)
            ok = (s >= og.HC - 1e-9).all(axis=1)
            if (~ok).any():
                viol = s[~ok]
                best_rej = min(best_rej, float((og.HC - viol[viol < og.HC]).min()))
            if level == n and ok.any():
                pass
            out.append(ext[ok])
        words = np.concatenate(out, axis=0)
    # accepted: all pairs q-p>=3 of the final conformations
    N = n + 3
    p, q = np.triu_indices(N, k=3)
    for lo in range(0, len(words), 20000):
        X = og.coords_from_words(words[lo:lo + 20000])
        s = ((X[:, p, :] - X[:, q, :]) ** 2).sum(axis=2)
        best_acc = min(best_acc, float((s - og.HC).min()))
    return best_acc, best_rej, len(words)

if __name__ == "__main__":
    for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        a, r, m = margins(n)
        print(f"n={n} conf={m} closest accepted pair above core: {a:.6f}; closest rejected below core: {r:.6f}", flush=True)
