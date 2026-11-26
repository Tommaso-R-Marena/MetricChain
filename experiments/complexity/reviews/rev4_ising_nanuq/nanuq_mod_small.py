"""Modified NANUQ (1/2,1,1/2,1): smallest failing galled outer-labeled planar networks (referee's side check)."""
import random, itertools
from collections import Counter
from fractions import Fraction as Fr
from nanuq_core import *
from nanuq_param import cycle_network, kalmanson_some_order, R_MOD, R_NANUQ, fmt, blow_up, all_circular_orders

# (i) the 7-leaf level-1 network: 6-cycle, cherry below the hybrid
net = cycle_network([["h1", "h2"], ["p1"], ["p2"], ["p3"], ["p4"], ["p5"]])
order = net.planar_order()
S = net.split_system()
print("7-leaf network: valid", net.is_valid(), "galled", net.is_galled(), "level/blobs", net.level(), "order", order)
forms = alpha_forms(S, order)
for sp, f in forms.items():
    v = ev(f, R_MOD)
    if v <= 0 or (sp not in S):
        print("   split", sorted(min(sp, key=len)), "displayed", sp in S, "alpha form", fmt(f), "Modified:", v, "NANUQ:", ev(f, R_NANUQ))
dm = {k: ev(v, R_MOD) for k, v in param_metric(S, order).items()}
print("   Modified NANUQ: circular orders (of 360) with all alpha >= 0:", kalmanson_some_order(dm, net.leaves()))

# (ii) random search for failures with n <= 6
rng = random.Random(99)
seen = set()
st = Counter()
for it in range(30000):
    n = rng.randint(4, 6)
    k = rng.randint(1, 4)
    net = random_network(n, k, rng, galled=True, planar=True, tries=40)
    if not net.hybrids():
        continue
    key = canonical_key(net)
    if key in seen:
        continue
    seen.add(key)
    order = net.planar_order()
    S = net.split_system()
    nonneg, supp, mn, bad = check_conclusion(S, order, R_MOD)
    st[(n, "ok" if (nonneg and supp) else ("negative" if not nonneg else "wrong support"))] += 1
    if not (nonneg and supp) and st[(n, "printed")] < 2:
        st[(n, "printed")] += 1
        print("   n=%d failure:" % n, net.ch, order, [(sorted(min(sp, key=len)), str(a)) for sp, a in bad])
print("distinct galled outer-labeled planar networks with n<=6 (random insertion, 30000 draws):", dict(sorted(st.items())))

# (iii) the 2a-c-s blow-up at m = 10 for a point of (b) minus (a)
from nanuq_param import find_witnesses
import nanuq_param
nanuq_param.rng = random.Random(5)
F = (-1, -1, 2, 0)
found = find_witnesses({F}, trials=3000)
w = found.get((F, False))
net, order, sp, z, w_, kind = w
for m in (2, 10, 12):
    n2, o2 = blow_up(net, order, z, m, "Z")
    n2, o2 = blow_up(n2, o2, w_, m, "W")
    S2 = n2.split_system()
    A, B = tuple(sp)
    def img(side):
        out = set()
        for x in side:
            if x == z: out |= {t for t in o2 if t.startswith(z + "Z")} if m > 1 else {z}
            elif x == w_: out |= {t for t in o2 if t.startswith(w_ + "W")} if m > 1 else {w_}
            else: out.add(x)
        return frozenset(out)
    sp2 = frozenset([img(A), img(B)])
    f = alpha_forms(S2, o2)[sp2]
    r = (Fr(1, 2), 1, Fr(7, 10), 1)
    print("2a-c-s witness blown up, m=%d (%d leaves, level %s, galled %s): alpha = %s ; at (0.5,1,0.7,1): %s ; at Modified: %s ; at NANUQ: %s"
          % (m, len(o2), n2.level(), n2.is_galled(), fmt(f), ev(f, r), ev(f, R_MOD), ev(f, R_NANUQ)))
print("witness network:", net.ch, "order", order, "split", [sorted(s) for s in sp], "z,w", z, w_)
