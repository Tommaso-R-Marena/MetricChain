# strands_mine.py -- REVIEWER'S OWN CODE: brute-force enumeration of the set W of
# STRANDS_ALGORITHM.md (pairs (Y,S): a sequence Y of species = circular arrangement with a marked first
# slot, S a connected non-crossing structure), the action of the cyclic group on slots, and the table
# (R, m) -> number of physical structures with symmetry exactly R and loop energy m.
# Loop model of the note (Section 1): hairpin hp(u); two-pair loop il(l1,l2); multiloop a + b*#pairs + c*#unpaired;
# loops containing a nick: 0.  Nothing is imported from the repository under review.
import itertools, sys, json, math
from collections import Counter

COMP = {('A', 'T'), ('T', 'A'), ('C', 'G'), ('G', 'C')}

# the integer energies used in the authors' level_counts.py (so that the tables can be compared)
def e_hp(u):
    return 2 + (u % 3)
def e_il(l1, l2):
    if l1 == 0 and l2 == 0:
        return -3
    return 1 + (abs(l1 - l2) % 2) + (l1 + l2) // 3
E_MA, E_MB, E_MC = 2, -1, 1


def multiset_sequences(counts):
    """all sequences with counts[i] copies of i"""
    items = []
    for i, n in enumerate(counts):
        items += [i] * n
    return sorted(set(itertools.permutations(items)))


def matchings(seq):
    N = len(seq)
    memo = {}
    def rec(i, j):
        if i >= j:
            return [()]
        key = (i, j)
        if key in memo:
            return memo[key]
        out = list(rec(i + 1, j))
        for k in range(i + 1, j):
            if (seq[i], seq[k]) in COMP:
                for a in rec(i + 1, k):
                    for b in rec(k + 1, j):
                        out.append(((i, k),) + a + b)
        memo[key] = out
        return out
    return rec(0, N)


def energy_or_none(N, pairs, nick_after):
    """nick_after: set of positions p such that the gap between p and p+1 (mod N) is a nick.
    returns the loop energy, or None if some face contains two or more nicks (disconnected)."""
    partner = {}
    for i, j in pairs:
        partner[i] = j; partner[j] = i
    seen = [False] * N          # gap g_p between p and p+1
    total = 0
    for g0 in range(N):
        if seen[g0]:
            continue
        # walk the face containing gap g0
        events = []             # 'u' unpaired base, 'c' chord, 'n' nick
        g = g0
        while True:
            seen[g] = True
            if g in nick_after:
                events.append('n')
            p = (g + 1) % N
            if p in partner:
                events.append('c')
                g = partner[p]
            else:
                events.append('u')
                g = p
            if g == g0:
                break
        nn = events.count('n'); nc = events.count('c'); nu = events.count('u')
        if nn >= 2:
            return None
        if nn == 1:
            continue                                   # exterior loop
        if nc == 0:
            raise AssertionError("face without chord and without nick")
        if nc == 1:
            total += e_hp(nu)
        elif nc == 2:
            # side lengths: unpaired runs between the two chords
            s = ''.join(e for e in events if e in 'uc')
            k = s.index('c'); s = s[k:] + s[:k]         # starts with 'c'
            parts = s[1:].split('c')
            assert len(parts) == 2
            total += e_il(len(parts[0]), len(parts[1]))
        else:
            total += E_MA + E_MB * nc + E_MC * nu
    return total


def levels(species, counts):
    """returns (table {(R,m): number of physical structures}, N_R(m) table, |W|)"""
    c = sum(counts)
    W = {}
    for Y in multiset_sequences(counts):
        seq = ''.join(species[i] for i in Y)
        N = len(seq)
        owner = []; idx = []
        nick_after = set()
        pos = 0
        for slot, i in enumerate(Y):
            for t in range(len(species[i])):
                owner.append(slot); idx.append(t)
            pos += len(species[i])
            nick_after.add(pos - 1)
        for pairs in matchings(seq):
            en = energy_or_none(N, pairs, nick_after)
            if en is None:
                continue
            S = frozenset(frozenset(((owner[a], idx[a]), (owner[b], idx[b]))) for a, b in pairs)
            W[(Y, S)] = en
    NR = Counter()
    for (Y, S), en in W.items():
        R = 0
        for j in range(c):
            Y2 = Y[j:] + Y[:j]
            if Y2 != Y:
                continue
            S2 = frozenset(frozenset((((s - j) % c), t) for (s, t) in pr) for pr in S)
            if S2 == S:
                R += 1
        NR[(R, en)] += 1
    phys = {}
    for (R, en), cnt in NR.items():
        assert (cnt * R) % c == 0, "N_R(m)*R/c is not an integer"
        phys[(R, en)] = cnt * R // c
    return phys, dict(NR), len(W)


if __name__ == '__main__':
    species = sys.argv[1].split(','); counts = [int(x) for x in sys.argv[2].split(',')]
    phys, NR, w = levels(species, counts)
    print(json.dumps({'W': w, 'phys': sorted([[R, m, v] for (R, m), v in phys.items()])}))
