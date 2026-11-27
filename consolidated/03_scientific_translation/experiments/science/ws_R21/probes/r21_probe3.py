import sys, time
sys.path.insert(0, "/home/user/MetricChain/experiments/science/ws_R21")
from r21_common import *
from scipy.optimize import linprog
rng = np.random.default_rng(1)
for M in (1000, 4000):
    for nq in (24,):
        A = np.abs(rng.standard_normal((nq, M))) ** 3
        A[:, :2] = 1.0
        far = rng.random(M) > 0.3
        far[:2] = False
        for eps in (1e-2, 1e-4):
            A_ub = np.vstack([A, -A]); b_ub = np.concatenate([np.full(nq, 1 + eps), -np.full(nq, 1 - eps)])
            for meth in ('highs', 'highs-ds', 'highs-ipm'):
                t0 = time.time()
                res = linprog(-far.astype(float), A_ub=A_ub, b_ub=b_ub, A_eq=np.ones((1, M)), b_eq=[1.0], bounds=(0, None), method=meth)
                print(M, eps, meth, res.status, "%.3f s" % (time.time() - t0), -res.fun if res.status == 0 else None)
