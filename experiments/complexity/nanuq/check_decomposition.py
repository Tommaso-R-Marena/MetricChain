"""Check, on every system of the network class on n <= 7 leaves (and on random arbitrary circular split
systems, to make sure the identity is an identity and not a property of the class):

  non-trivial split U|V (|U|,|V| >= 2):
     alpha_ij / 2 = Phi4 + sum_{z not in Y} Phi5(z) + sum_{ {z,w} same side, not in Y } Phi6(z,w)
  trivial split {u} | rest, neighbours a (before u) and b (after u):
     alpha / 2 = n - 2 + sum_{ {z,w} subset of X \\ {a,u,b} } Psi(z,w),
     Psi(z,w) = 1 - w(a u | z w) - w(u b | z w) + w(a b | z w)

All quantities are doubled to stay in the integers (2*d, 2*alpha, 2*Phi, 2*Psi)."""
import sys, random
from itertools import combinations
from splitsys import *
from local_terms import weight2, phi4, phi5, phi6
from multiblob import network_systems

def psi2(sigma, n, a, u, b, z, w):
    return 2 - weight2(sigma, n, a, u, z, w) - weight2(sigma, n, u, b, z, w) + weight2(sigma, n, a, b, z, w)

def local_alpha2(sigma, n, i, j):
    """2*alpha_ij from local terms.  gap i is between point i and i+1.  U = {i+1..j}."""
    U = []
    k = (i + 1) % n
    while True:
        U.append(k)
        if k == j:
            break
        k = (k + 1) % n
    V = [(j + 1 + t) % n for t in range(n - len(U))]
    if len(U) == 1 or len(V) == 1:
        if len(V) == 1:
            U, V = V, U
        u = U[0]
        b, a = V[0], V[-1]          # b follows u, a precedes u
        rest = V[1:-1]
        tot2 = 2 * (n - 2)
        for z, w in combinations(rest, 2):
            tot2 += psi2(sigma, n, a, u, b, z, w)
        return 2 * tot2, None
    u1, up, v1, vq = U[0], U[-1], V[0], V[-1]
    tot2 = phi4(sigma, n, u1, up, v1, vq)
    terms = [tot2]
    for z in U[1:-1]:
        t = phi5(sigma, n, u1, z, up, v1, vq); tot2 += t; terms.append(t)
    for z in V[1:-1]:
        # mirror: roles of (u1,up,v1,vq) -> (v1,vq,u1,up)
        t = phi5(sigma, n, v1, z, vq, u1, up); tot2 += t; terms.append(t)
    for z, w in combinations(U[1:-1], 2):
        t = phi6(sigma, n, u1, z, w, up, v1, vq); tot2 += t; terms.append(t)
    for z, w in combinations(V[1:-1], 2):
        t = phi6(sigma, n, v1, z, w, vq, u1, up); tot2 += t; terms.append(t)
    return 2 * tot2, terms

def check_system(n, sigma):
    D = nanuq_2d(n, sigma)
    if D is None:
        return None
    al = alphas_2(n, D)      # 2*alpha computed from 2*d ... D holds 2*d so al holds 2*alpha
    worst = 0
    for (i, j), v in al.items():
        loc, terms = local_alpha2(sigma, n, i, j)
        # v = 2*alpha ; loc = 2 * (2 * alpha/2 ... ) careful: tot2 = 2*(alpha/2) = alpha ; loc = 2*alpha
        assert v == loc, (n, sorted(sigma), i, j, v, loc)
        if terms is not None:
            worst = min(worst, min(terms))
    return worst

if __name__ == "__main__":
    for n in (4, 5, 6, 7):
        systems = network_systems(n, n)
        w = 0
        for s in systems:
            w = min(w, check_system(n, set(s)))
        print(f"n={n}: identity verified on {len(systems)} network systems; most negative local term (x2): {w}", flush=True)
    # identity on arbitrary systems
    rng = random.Random(1)
    for n in (5, 6, 7, 8):
        allsp = all_circular_splits(n)
        triv = [m for m in allsp if is_trivial(n, m)]
        nontriv = [m for m in allsp if not is_trivial(n, m)]
        cnt = 0
        for _ in range(300):
            sub = [m for m in nontriv if rng.random() < 0.6]
            r = check_system(n, set(triv) | set(sub))
            if r is not None:
                cnt += 1
        print(f"n={n}: identity verified on {cnt} random valid circular split systems")
    # Psi on 5 points over the class
    from collections import Counter
    c = Counter()
    for s in network_systems(5, 5):
        c[psi2(set(s), 5, 0, 1, 2, 3, 4)] += 1
    print("2*Psi over the 5-point class (a=0,u=1,b=2,z=3,w=4):", dict(sorted(c.items())))
