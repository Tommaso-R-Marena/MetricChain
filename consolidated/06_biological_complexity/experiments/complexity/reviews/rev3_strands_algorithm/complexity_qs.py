"""The O(L0^4) factor does not come from interior loops only: the recursion 'by the rightmost top-level pair
(d,e)' of Q/QM (and the single-strand Qs/QMs) already costs Theta(l^2) per entry.  Count the pair tests made
inside Tables.Qs alone for a single strand of length l (interior-loop code not involved)."""
import sys, inspect
from fractions import Fraction
sys.dont_write_bytecode = True
sys.path.insert(0, 'author_copy')
import multiset_dp as A
cnt = {'Qs': 0, 'QBs': 0, 'QMs': 0}
orig = A.Tables.can
def can(self, s, i, t, j):
    caller = sys._getframe(1).f_code.co_name
    if caller in cnt:
        cnt[caller] += 1
    return orig(self, s, i, t, j)
A.Tables.can = can
m = A.Model(lambda u: Fraction(1), lambda a, b: Fraction(1), 1, 1, 1)
prev = None
for l in (16, 32, 64):
    for k in cnt: cnt[k] = 0
    T = A.Tables(['A' * l], m, 1)      # poly-A: no pair possible, so only the loop structure of Qs is exercised
    T.Qs(0, 1, l)
    for i in range(1, l + 1):
        for j in range(i, l + 1):
            T.Qs(0, i, j)
    print('single strand of length', l, ': pair tests inside Qs =', cnt['Qs'], '(l^4/24 = %d)' % (l ** 4 // 24), '' if prev is None else 'ratio to previous length: %.1f' % (cnt['Qs'] / prev))
    prev = cnt['Qs']
