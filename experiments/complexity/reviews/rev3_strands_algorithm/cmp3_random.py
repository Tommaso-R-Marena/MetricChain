#!/usr/bin/env python3
"""Random sweep: author's DP vs referee's C++ brute force (mod 2^61-1).  Random species over several alphabets,
1-4 species, copy numbers biased towards common divisors, single strands with hairpins/multiloops included."""
import sys, random, time
sys.dont_write_bytecode = True
import cmp2

def rand_case(rng):
    while True:
        mode = rng.random()
        k = rng.choice([1, 1, 2, 2, 2, 3, 3, 4])
        alphabet = rng.choice(['GC', 'GC', 'ACGT', 'GCA', 'GCAT', 'GCT'])
        species = []
        tries = 0
        while len(species) < k and tries < 100:
            tries += 1
            L = rng.choice([1, 2, 2, 3, 3, 4, 4, 5, 6, 7, 8]) if k > 1 else rng.randint(4, 22)
            w = ''.join(rng.choice(alphabet) for _ in range(L))
            if w not in species:
                species.append(w)
        if len(species) < k:
            continue
        if k == 1 and rng.random() < 0.5:
            counts = [1]
        else:
            g = rng.choice([1, 1, 2, 2, 2, 3, 3, 4, 5, 6])
            counts = [g * rng.choice([1, 1, 1, 2, 3]) for _ in range(k)]
        N = sum(len(w) * n for w, n in zip(species, counts))
        c = sum(counts)
        if N <= 22 and c <= 12:
            return species, counts

if __name__ == '__main__':
    seed, ncases = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    cmp2.TLIM = 120
    done = 0; ok = True
    with open('cmp3_seed%d.log' % seed, 'w') as log:
        while done < ncases:
            sp, ct = rand_case(rng)
            ok &= cmp2.run(sp, ct, alphas=(0, 1, 2, 3, -1, 40), log=log)
            done += 1
        log.write('ALL OK\n' if ok else 'SOME MISMATCH\n')
    print('ALL OK' if ok else 'SOME MISMATCH')
