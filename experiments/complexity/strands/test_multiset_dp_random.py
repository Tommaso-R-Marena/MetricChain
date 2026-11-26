"""Random validation of the multiset DP against exhaustive enumeration."""
import random, sys, time
from fractions import Fraction
from test_multiset_dp import brute, MODEL
from multiset_dp import magnified_pf, Model

def rand_case(rng, maxN):
    while True:
        k = rng.choice([1, 1, 2, 2, 3])
        alphabet = rng.choice(["GC", "GC", "ACGT", "GCA", "GCAT"])
        species = []
        while len(species) < k:
            w = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 6)))
            if w not in species:
                species.append(w)
        counts = [rng.randint(1, 4) for _ in range(k)]
        N = sum(len(w) * n for w, n in zip(species, counts))
        c = sum(counts)
        if N <= maxN and c <= 6:
            return species, counts

def main(seed, ncases, maxN):
    rng = random.Random(seed)
    # a second model with different numbers, to vary the weights
    def hp2(u): return Fraction(2 + u, 5)
    def il2(a, b): return Fraction(7, 2) if (a, b) == (0, 0) else Fraction(1 + (a * b) % 3, 4 + a + b)
    models = [MODEL, Model(hp2, il2, Fraction(5, 3), Fraction(1, 2), Fraction(4, 5))]
    ok = True
    done = 0
    t0 = time.time()
    sym = 0
    while done < ncases:
        species, counts = rand_case(rng, maxN)
        m = rng.choice(models)
        alphas = (0, 1, 2, 3)
        b, nlab, nphys, Rhist = brute(species, counts, m, alphas)
        if nlab == 0:
            continue
        done += 1
        if any(r > 1 for r in Rhist):
            sym += 1
        for a in alphas:
            dp = magnified_pf(species, counts, m, a)
            if dp != b[a]:
                ok = False
                print("MISMATCH", species, counts, "alpha", a, dp, b[a], flush=True)
        if done % 25 == 0:
            print(f"  {done} cases, {sym} with symmetric structures, ok={ok} [{time.time()-t0:.0f}s]", flush=True)
    print(f"seed {seed}: {done} random systems (N <= {maxN}), {sym} of them with rotationally symmetric structures: "
          f"{'ALL OK' if ok else 'FAILURES'}")

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
