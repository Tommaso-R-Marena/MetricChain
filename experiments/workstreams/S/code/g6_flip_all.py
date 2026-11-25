#!/usr/bin/env python3
"""Complete check of the hairpin lower bound for all arm lengths 3 <= a, b <= AMAX:
D(a,b) = profile distance between t^a +-+ t^b and t^a +t+ t^b; d = min(a,b) + 2.  Prints min and max of D - 14 d,
and checks the periodicity D(a+2,b+2) = D(a,b) + 28 and D(a,b+2) = D(a,b) for b >= a + 6 (a >= 5)."""
import sys
from lat import *
from g6_flip import word_to_walk, cumdist
amax = int(sys.argv[1])
D = {}
for a in range(3, amax + 1):
    for b in range(3, amax + 1):
        x = word_to_walk('t' * a + '+-+' + 't' * b); y = word_to_walk('t' * a + '+t+' + 't' * b)
        assert is_walk(x) and is_walk(y)
        D[(a, b)] = cumdist(profile(x), profile(y))
vals = [D[(a, b)] - 14 * (min(a, b) + 2) for (a, b) in D]
print(f"arms 3..{amax}: {len(D)} hairpins, all self-avoiding; D - 14 d in [{min(vals)}, {max(vals)}]")
bad1 = [(a, b) for (a, b) in D if a >= 5 and b >= 5 and (a + 2, b + 2) in D and D[(a + 2, b + 2)] != D[(a, b)] + 28]
bad2 = [(a, b) for (a, b) in D if a >= 5 and b >= a + 6 and (a, b + 2) in D and D[(a, b + 2)] != D[(a, b)]]
print("violations of D(a+2,b+2) = D(a,b) + 28 for a,b >= 5:", len(bad1), "; of D(a,b+2) = D(a,b) for b >= a+6, a >= 5:", len(bad2))
