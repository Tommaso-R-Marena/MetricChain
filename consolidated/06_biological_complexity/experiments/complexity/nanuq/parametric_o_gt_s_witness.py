from fractions import Fraction as F
from twin_trees import system_of
from splitsys import *
from localcrit import blowup
from parametric import param_d, param_alphas
from parametric_domain import ev
# witness with local term s - o:  tree (1,(2,(3,((4,5),6)))) on 7 positions, twin pair at positions (3,4)
t = (1, (2, (3, ((4, 5), 6))))
sig, nn = system_of(7, t, (3,))
z, w = 1, 4
r = (F(0), F(1), F(1, 2), F(11, 10))
for m in (12, 16, 20):
    mult = [1] * 6
    mult[z] = m; mult[w] = m
    n2, s2 = blowup(6, sig, mult)
    D = param_d(n2, s2)
    al = param_alphas(n2, D)
    worst = None
    for (i, j), vv in al.items():
        val = ev(vv[:4], r) + vv[4]
        msk = canon(n2, split_mask(n2, i, j))
        okk = (val > 0) if msk in s2 else (val == 0)
        if not okk and (worst is None or val < worst[0]):
            worst = (val, vv)
    print("m =", m, "n =", n2, "worst violation:", None if worst is None else (str(worst[0]), worst[1]), flush=True)
