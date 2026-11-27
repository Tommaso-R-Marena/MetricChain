"""R7 OWN statistics of the generic chain: pairs within the cutoff, per bead (written before reading engineering code)."""
import sys, time
import numpy as np
import own_gen as og

def stats(n):
    words = og.enumerate_words(n)
    S = og.truncated_sorted_sq(words)
    cid, ncls, info = og.profile_classes(S)
    N = n + 3
    P = S.shape[1]
    inside = (S < og.SC - 1e-9).sum(axis=1)          # pairs strictly inside the cutoff
    # class representatives
    first = np.zeros(ncls, dtype=np.int64)
    order = np.argsort(cid, kind="stable")
    first[cid[order][::-1]] = order[::-1]
    return dict(n=n, N=N, conf=len(words), classes=ncls, P=P,
                mean_conf=inside.mean() / N, mean_cls=inside[first].mean() / N,
                max=inside.max() / N, argmax_word="".join("tpm"[k] for k in words[inside.argmax()]),
                P_over_N=P / N, min_gap_to_cutoff=float(np.abs(S[S != og.SC] - og.SC).min()) if (S != og.SC).any() else None)

if __name__ == "__main__":
    for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        t0 = time.time()
        r = stats(n)
        print(r, f"t={time.time()-t0:.1f}s", flush=True)
