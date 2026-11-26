import sys
sys.dont_write_bytecode = True
import cmp2, cmp4_letters, bf
from cmp1 import mk_models
cmp2.TLIM = 200
ok = True
cases = [(['GC', 'CG'], [2, 2]), (['GC', 'CG'], [3, 3]), (['GC', 'CG'], [4, 4]), (['GC', 'CG'], [4, 2]), (['GCG', 'CGC'], [2, 2]), (['GCG', 'CGC'], [3, 3]), (['GCG', 'CGC'], [4, 4]),
         (['AT', 'TA', 'GC'], [2, 2, 2]), (['GGC', 'GCC', 'CGC'], [2, 2, 2]), (['GC', 'CG', 'GGCC'], [2, 2, 2]), (['G', 'C', 'GC', 'CG'], [2, 2, 2, 2]), (['GCGC', 'CGCG'], [2, 2]), (['GCGC', 'CGCG'], [3, 3]),
         (['ACGTACGT'], [2]), (['ACGTACGT'], [3]), (['GCGCAAGCGC'], [2]), (['GGGCCC', 'GC'], [2, 4]), (['GGGCCC', 'GC'], [2, 2]), (['GCATGC', 'ATGCAT'], [2, 2])]
with open('cmp7_misc.log', 'w') as log:
    for sp, ct in cases:
        ok &= cmp2.run(sp, ct, alphas=(0, 1, 2, 3, -1), log=log, models=mk_models()[1:3])
        ok &= cmp4_letters.run(sp, ct, [bf.model_letters(5)], alphas=(0, 1, 2, 3, -1), log=log)
print('ALL OK' if ok else 'SOME MISMATCH')
