#!/usr/bin/env python3
"""G6 (question 4): a proved linear LOWER bound for the single-flip constants on the self-avoiding chain.

Hairpin family: torsion word  t^(a) g g g t^(b)  (the tight fold between two adjacent all-trans stems joined by one
rung bond), and the word obtained by changing ONE of the three fold torsions.  Both conformations are generated
from their torsion words, checked to be self-avoiding, and the profile distance ||N^x - N^x'||_1 (cumulative
profiles, weights 5,3,1) is computed.  The distance is  14 * (length of the shorter arm) + const: the stems lose
all their mutual pairs, (1,4,3) pairs of squared distances (3,8,11) per two beads of stem.

usage: g6_flip.py NMAX
"""
import sys
from lat import *

def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def word_to_walk(word):
    """word over 't', '+', '-' (trans, gauche+, gauche-) -> list of sites (first bonds +a0, -a1)"""
    idx = [0, 1]
    for j, s in enumerate(word):
        a, b = idx[j], idx[j + 1]
        if s == 't':
            idx.append(a); continue
        sg = lambda m, i: tuple((1 if m % 2 == 0 else -1) * c for c in A[i])
        cands = [c for c in range(4) if c != a and c != b]
        chosen = None
        for c in cands:
            b0, b1, b2 = sg(j, a), sg(j + 1, b), sg(j + 2, c)
            cr = cross(b1, b2)
            trip = b0[0]*cr[0] + b0[1]*cr[1] + b0[2]*cr[2]
            if (trip > 0) == (s == '+'):
                chosen = c
        idx.append(chosen)
    pos = [(0, 0, 0)]
    for m, i in enumerate(idx):
        s = 1 if m % 2 == 0 else -1
        pos.append((pos[-1][0] + s*A[i][0], pos[-1][1] + s*A[i][1], pos[-1][2] + s*A[i][2]))
    return pos

def walk_to_word(pos):
    out = []
    for j in range(len(pos) - 3):
        b0, b1, b2 = sub(pos[j+1], pos[j]), sub(pos[j+2], pos[j+1]), sub(pos[j+3], pos[j+2])
        if b2 == b0: out.append('t'); continue
        cr = cross(b1, b2)
        out.append('+' if b0[0]*cr[0] + b0[1]*cr[1] + b0[2]*cr[2] > 0 else '-')
    return ''.join(out)

def cumdist(p, q):
    c1 = (p[0], p[0] + p[1], p[0] + p[1] + p[2]); c2 = (q[0], q[0] + q[1], q[0] + q[1] + q[2])
    return 5 * abs(c1[0] - c2[0]) + 3 * abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])

def main():
    nmax = int(sys.argv[1])
    # the fold word: read it off an explicit hairpin (stem up rod 0, rung, stem down rod 1) built with lamella.py
    import lamella as lam
    w = lam.lamella(3, 1, 6)
    word = walk_to_word(w)
    print("# torsion word of a 3-stem rung-folded sheet:", word)
    i = word.index('+') if '+' in word else word.index('-')
    k = i
    while k < len(word) and word[k] != 't': k += 1
    fold = word[i:k]
    print("# fold between two stems:", fold, " (", len(fold), "gauche torsions )")
    print("# n = a + b + len(fold) torsions; flip of fold torsion number f (0-based) to state s; d = distance of the flipped torsion from the nearer end")
    print("#   a    b    n   d | best single flip at the fold: (f, s), profile distance D | D/d | D - 14 d")
    for a, b in [(m, m) for m in range(3, nmax + 1, 4)] + [(5, 30), (10, 30), (20, 30), (10, 60), (20, 60), (30, 60)]:
        base = 't' * a + fold + 't' * b
        x = word_to_walk(base)
        assert is_walk(x) and walk_to_word(x) == base
        px = profile(x)
        best = None
        for f in range(len(fold)):
            for s in 't+-':
                if s == fold[f]: continue
                w2 = base[:a + f] + s + base[a + f + 1:]
                y = word_to_walk(w2)
                if not is_walk(y): continue
                D = cumdist(px, profile(y))
                j = a + f + 1                         # 1-based index of the flipped torsion
                d = min(j, len(base) + 1 - j)
                if best is None or D > best[0]: best = (D, f, s, d)
        D, f, s, d = best
        print(f"  {a:3d} {b:4d} {len(base):4d} {d:3d} |   ({f}, {s})   {D:5d}   | {D/d:6.2f} | {D - 14*d:4d}")

if __name__ == "__main__":
    main()
