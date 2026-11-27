"""Self-test of own_certified_bb.py against brute force on random small instances:
   target = optimum      -> the tree must be exhausted ("PROVED");
   target = optimum + 1  -> a cover of size <= optimum must be found ("REFUTED")."""
import itertools, sys
import numpy as np
from own_certified_bb import CertifiedBB, reduce_instance

def brute(M):
    n = M.shape[0]
    for k in range(1, n + 1):
        for comb in itertools.combinations(range(n), k):
            if M[list(comb)].any(axis=0).all():
                return k

rng = np.random.default_rng(3)
ok = 0
for trial in range(300):
    n = int(rng.integers(4, 13)); m = int(rng.integers(4, 13))
    M = rng.random((n, m)) < rng.uniform(0.15, 0.5)
    for c in range(m):
        if not M[:, c].any(): M[rng.integers(0, n), c] = True
    opt = brute(M)
    R, rows, cols = reduce_instance(M)
    assert brute(R) == opt, "reduction changed the optimum"
    for inst in (M, R):
        bb = CertifiedBB(inst, opt); bb.solve([], np.zeros(inst.shape[0], bool), np.zeros(inst.shape[1], bool))
        assert not bb.incomplete and bb.found_cover is None, "false refutation / incomplete at target = optimum"
        bb = CertifiedBB(inst, opt + 1); bb.solve([], np.zeros(inst.shape[0], bool), np.zeros(inst.shape[1], bool))
        assert bb.found_cover is not None and len(bb.found_cover) <= opt and inst[bb.found_cover].any(axis=0).all(), "missed a smaller cover"
    ok += 1
print("certified branch and bound: self-test passed on", ok, "random instances (both the reduced and the unreduced form)")
