# instrumented re-run of the authors' generator loop of level2_all_orders_explicit.py (their code, copied):
# which kinds of entry and of pendant subnetworks occur among the blobs with NEGATIVE critical weight?
import random, sys
from netcalc import leaves_of
from level2_explicit import random_network, formula

def run(count, seed, maxleaves):
    rng = random.Random(seed)
    done = 0
    hist = {}
    ysz = {}; xsz = {}
    nneg = 0
    b1sz = {}; ccsz = {}
    while done < count:
        net, order, records = random_network(rng, maxleaves)
        L = leaves_of(net)
        if len(L) < 5 or not records:
            continue
        done += 1
        for rc in records:
            kB, k1, k2 = rc["k"]
            if not (k1 >= 1 and kB >= 2):
                continue
            inside = set(rc["y"])
            for lst in rc["x"]:
                inside |= set(lst)
            named = set(inside)
            for lst in rc["b"] + rc["c"]:
                if lst is not None:
                    named |= set(lst)
            outside = [l for l in order if l not in named]
            beta = [len(lst) if lst is not None else len(outside) for lst in rc["b"]]
            gamma = [len(lst) if lst is not None else len(outside) for lst in rc["c"]]
            xi = [len(lst) for lst in rc["x"]]
            pred = formula(beta, xi, len(rc["y"]), gamma)
            if pred >= 0:
                continue
            nneg += 1
            e = rc["entry"]
            if e == ("A",):
                kind = "root on A"
            elif e[0] == "b":
                kind = "b_1" if e[1] == 1 else ("b_kB" if e[1] == kB else "middle b")
            else:
                kind = "c_1" if e[1] == 1 else "c_e, e>1"
            hist[kind] = hist.get(kind, 0) + 1
            ysz[len(rc["y"])] = ysz.get(len(rc["y"]), 0) + 1
            xsz[xi[0]] = xsz.get(xi[0], 0) + 1
            b1sz[beta[0]] = b1sz.get(beta[0], 0) + 1
            cc = gamma[0] if k2 >= 1 else beta[-1]
            ccsz[cc] = ccsz.get(cc, 0) + 1
    return nneg, hist, ysz, xsz, b1sz, ccsz

tot = {}
for args in ((500, 6, 12), (500, 7, 13), (400, 8, 14)):
    nneg, hist, ysz, xsz, b1sz, ccsz = run(*args)
    print(args, "negative critical weights:", nneg)
    print("   entry kinds:", hist)
    print("   size of position y:", dict(sorted(ysz.items())), " size of x_1:", dict(sorted(xsz.items())))
    print("   size of b_1:", dict(sorted(b1sz.items())), " size of c_1 (b_kB if k2=0):", dict(sorted(ccsz.items())))
    for k, v in hist.items():
        tot[k] = tot.get(k, 0) + v
print("total by entry kind:", tot)
