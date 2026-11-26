import time, sys
import bf, drv
m = bf.model_sizes()
for species, counts in [(['GG','CC'],[4,4]), (['GA','TC'],[4,4]), (['GA','TC'],[6,6]), (['GG','CC'],[5,5]), (['GC'],[8]), (['GGCC'],[4]), (['GGCC'],[5]), (['GAC','GTC'],[3,3]), (['GA','TC','GC'],[3,3,3]), (['GC','GGCC'],[4,2]), (['GG','CC'],[6,6])]:
    t0 = time.time()
    res, nw, ns = drv.brute_mod(species, counts, m, [0, 1, 2], mode=1)
    print(species, counts, 'words', nw, 'structs', ns, {R: v[0] for R, v in res.items()}, '%.1fs' % (time.time() - t0), flush=True)
