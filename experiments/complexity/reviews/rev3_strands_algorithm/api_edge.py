import sys
from fractions import Fraction
sys.dont_write_bytecode = True
sys.path.insert(0, 'author_copy')
import multiset_dp as A
m = A.Model(lambda u: Fraction(1), lambda a, b: Fraction(1), 1, 1, 1)
print('GCx2 as one species            :', [A.magnified_pf(['GC'], [2], m, a) for a in (0, 1, 2)], '(correct: 2, 3/2, 5/4)')
print('GCx2 passed as two "species"   :', [A.magnified_pf(['GC', 'GC'], [1, 1], m, a) for a in (0, 1, 2)], '(no check that species are distinct)')
print('zero-count species             :', [A.magnified_pf(['GC', 'AT'], [2, 0], m, a) for a in (0, 1, 2)])
try:
    print('zero count with gcd  (GC x2, GGC x0, CC x4):', A.magnified_pf(['GC', 'GGC', 'CC'], [2, 0, 4], m, 2), A.magnified_pf(['GC', 'CC'], [2, 4], m, 2))
except Exception as ex:
    print('zero-count species raises', type(ex).__name__, ex)
# zero weights and alpha <= 0
m0 = A.Model(lambda u: Fraction(0) if u < 3 else Fraction(1), lambda a, b: Fraction(1), 1, 1, 1)
print('hairpins < 3 forbidden by weight 0, single strand GGGAAACCC: alpha=1 ->', A.magnified_pf(['GGGAAACCC'], [1], m0, 1), '; alpha=0 ->', A.magnified_pf(['GGGAAACCC'], [1], m0, 0), '(alpha = 0 counts the forbidden structures too: 0**0 == 1)')
try:
    print(A.magnified_pf(['GGGAAACCC'], [1], m0, -1))
except Exception as ex:
    print('alpha = -1 with a zero weight raises', type(ex).__name__)
