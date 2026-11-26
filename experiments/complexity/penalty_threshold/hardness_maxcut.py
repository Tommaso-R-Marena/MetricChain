"""Brute-force check of the two reductions from MAX-CUT in docs/complexity/PENALTY_THRESHOLD.md section 6
(answer to the question of SCI-MSG-0031 section 2).

For a graph H = (V, E), n = |V|, and theta > 0:

 (i)  three states per site (anchor 0, off states 1, 2), product reference uniform on the three states,
      pair tables  Theta_ij(s, s') = theta if ij in E and {s, s'} = {1, 2}, else 0:
          G = max_x [ b(x) + ln pi_0(x) ] = theta * maxcut(H) - n ln 3.
 (ii) two states per site, sites (v,1), (v,2) for v in V, reference = independent two-site blocks with weights
      1, 1, 1, exp(-B) for (0,0), (1,0), (0,1), (1,1)  (a nearest-neighbour chain with couplings inside blocks),
      pair tables theta on ((u,1),(v,2)) and ((u,2),(v,1)) for uv in E (non-zero only if both sites are off):
          G = theta * maxcut(H) - n ln(3 + exp(-B))      provided  B >= theta * |E|.
"""
import itertools, math, random


def maxcut(n, E):
    best = 0
    for bits in itertools.product((0, 1), repeat=n):
        best = max(best, sum(1 for u, v in E if bits[u] != bits[v]))
    return best


def G_three_state(n, E, theta):
    best = -1e300
    for x in itertools.product((0, 1, 2), repeat=n):
        b = theta * sum(1 for u, v in E if {x[u], x[v]} == {1, 2})
        best = max(best, b - n * math.log(3))
    return best


def G_two_state(n, E, theta, B):
    best = -1e300
    lnZ = n * math.log(3 + math.exp(-B))
    for x in itertools.product((0, 1), repeat=2 * n):          # site (v,s) is index 2v + s - 1
        cost = B * sum(1 for v in range(n) if x[2 * v] and x[2 * v + 1]) + lnZ
        b = theta * sum((x[2 * u] and x[2 * v + 1]) + (x[2 * u + 1] and x[2 * v]) for u, v in E)
        best = max(best, b - cost)
    return best


if __name__ == "__main__":
    rng = random.Random(1)
    for trial in range(40):
        n = rng.randint(3, 6)
        E = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.6]
        if not E:
            continue
        theta = rng.choice((0.3, 1.0, 2.5))
        mc = maxcut(n, E)
        g3 = G_three_state(n, E, theta)
        assert abs(g3 - (theta * mc - n * math.log(3))) < 1e-9, (n, E, theta, g3, mc)
        B = theta * len(E) + 0.01
        g2 = G_two_state(n, E, theta, B)
        assert abs(g2 - (theta * mc - n * math.log(3 + math.exp(-B)))) < 1e-9, (n, E, theta, g2, mc)
    print("both reductions agree with brute force on 40 random graphs with 3 to 6 vertices")
