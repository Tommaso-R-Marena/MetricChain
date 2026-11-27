# Coordinator's independent check of ENG-RES-0006 §1: on the uniform cube, for every size M the
# maximum of W(C) = 2^{-n} sum_y exp(u dist(y, C)) over all sets C with |C| = M is attained by the
# initial segment of the simplicial order.  Brute force over all subsets, n <= 4.
import itertools, math
def run(n, u):
    V = list(range(2 ** n))
    dist = [[bin(a ^ b).count("1") for b in V] for a in V]
    def key(x):                         # simplicial order: by weight, then min of symmetric difference in the smaller
        bits = [i for i in range(n) if x >> i & 1]
        return (len(bits), [-(x >> i & 1) for i in range(n)])
    order = sorted(V, key=key)
    best = {}
    for mask in range(1, 2 ** (2 ** n) - 1):
        C = [v for v in V if mask >> v & 1]
        W = sum(math.exp(u * min(dist[y][c] for c in C)) for y in V) / 2 ** n
        M = len(C)
        if W > best.get(M, -1): best[M] = W
    worst = 0.0
    for M in range(1, 2 ** n):
        C = order[:M]
        W = sum(math.exp(u * min(dist[y][c] for c in C)) for y in V) / 2 ** n
        worst = max(worst, best[M] - W)
        assert W <= best[M] + 1e-12
    return worst
for n in (2, 3, 4):
    for u in (0.5, 1.0, 2.0):
        print(n, u, "max over sizes of [max_C W(C) - W(initial segment)] =", f"{run(n, u):.2e}")
