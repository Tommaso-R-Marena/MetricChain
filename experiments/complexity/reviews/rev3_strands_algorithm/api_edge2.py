import sys
from fractions import Fraction
sys.dont_write_bytecode = True
sys.path.insert(0, 'author_copy')
import multiset_dp as A
import bf
hp0 = lambda u: Fraction(0) if u < 3 else Fraction(1, u)
il = lambda a, b: Fraction(2) if (a, b) == (0, 0) else Fraction(1, 1 + a + b)
m0 = A.Model(hp0, il, Fraction(1, 2), Fraction(2, 3), Fraction(5, 4))
bm = bf.Model(lambda u, a, b: hp0(u), lambda l1, a1, b1, l2, a2, b2: il(l1, l2), Fraction(1, 2), Fraction(2, 3), Fraction(5, 4), 'hp0')
for strands in (['GCGC'], ['GGCC'] * 2):
    sp = sorted(set(strands)); ct = [strands.count(s) for s in sp]
    structs = []
    for Y in bf.distinct_words(strands):
        st, _ = bf.all_connected(list(Y), bm)
        structs += st
    allowed = sum(1 for p, w, R in structs if w != 0)
    print(strands, ': (Y,S) pairs', len(structs), 'of which with non-zero weight', allowed,
          '| author alpha=0:', A.magnified_pf(sp, ct, m0, 0), '(= count including zero-weight structures, 0**0 = 1)',
          '| alpha=1:', A.magnified_pf(sp, ct, m0, 1))
    try:
        print('   alpha=-1:', A.magnified_pf(sp, ct, m0, -1))
    except Exception as ex:
        print('   alpha=-1 raises', type(ex).__name__)
# large alpha
st = ['GGCC'] * 3
ref = bf.physical_sum_by_words(st, bf.model_sizes(), [200])
from cmp1 import mk_models
name, hp, il2, ma, mb, mc = mk_models()[1]
print('alpha = 200, GGCC x3, model sizes: exact equality with brute force:', A.magnified_pf(['GGCC'], [3], A.Model(hp, il2, ma, mb, mc), 200) == ref[200])
