import sys, time
from collections import Counter
from splitsys import *
from twin_trees import *
from multiblob import network_systems
from localcrit import local_ok

t0 = time.time()
for n in (4, 5, 6):
    A = A_systems(n)
    C = closure_systems(n)
    net = network_systems(n, n)
    print(f"n={n}: |A|={len(A)} |closure|={len(C)} |network systems (constrained generator)|={len(net)}  "
          f"A subset closure: {A <= C}  closure == network systems: {C == net}  [{time.time()-t0:.0f}s]", flush=True)
C6 = closure_systems(6)
bad = [s for s in C6 if not local_ok(6, s)[0]]
print("closure systems on 6 leaves that are not locally good:", len(bad))
A6 = A_systems(6)
print("A-systems on 6 leaves locally good:", all(local_ok(6, s)[0] for s in A6))
