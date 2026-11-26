# t11_mutation.py -- REVIEWER'S OWN CODE: is my checker sensitive?  Replace the formula of Theorem 12(b) by
# wrong variants and count how many of 600 random structured networks then report a violation.
import random, itertools
import myblob
from mybuild import rand_spec, build
from myblob import blob_report, check_theorem12

def variants():
    def right(beta, xi, eta, gamma):
        R = eta + sum(xi[1:])
        if gamma: G, M = sum(gamma), beta[1:]
        else: G, M = beta[-1], beta[1:-1]
        return beta[0] * G + xi[0] * R - sum(a * b for a, b in itertools.combinations(M, 2))
    def v1(beta, xi, eta, gamma):      # M = {2..kB} also when k2 = 0
        R = eta + sum(xi[1:])
        G = sum(gamma) if gamma else beta[-1]
        M = beta[1:]
        return beta[0] * G + xi[0] * R - sum(a * b for a, b in itertools.combinations(M, 2))
    def v2(beta, xi, eta, gamma):      # G = gamma_1 only
        R = eta + sum(xi[1:])
        if gamma: G, M = gamma[0], beta[1:]
        else: G, M = beta[-1], beta[1:-1]
        return beta[0] * G + xi[0] * R - sum(a * b for a, b in itertools.combinations(M, 2))
    def v3(beta, xi, eta, gamma):      # R = eta only
        R = eta
        if gamma: G, M = sum(gamma), beta[1:]
        else: G, M = beta[-1], beta[1:-1]
        return beta[0] * G + xi[0] * R - sum(a * b for a, b in itertools.combinations(M, 2))
    def v4(beta, xi, eta, gamma):      # b_1 included in M
        R = eta + sum(xi[1:])
        if gamma: G, M = sum(gamma), beta
        else: G, M = beta[-1], beta[:-1]
        return beta[0] * G + xi[0] * R - sum(a * b for a, b in itertools.combinations(M, 2))
    return [('formula of the note', right), ('M = {2..kB} also for k2 = 0', v1), ('G = gamma_1', v2), ('R = eta', v3), ('b_1 in M', v4)]

rng = random.Random(5)
nets = []
while len(nets) < 600:
    spec = rand_spec(rng, rng.randint(6, 11), True)
    net = build(spec)
    if len(net.hyb) > 8 or not net.is_valid(): continue
    order = net.circular_order()
    if order is None: continue
    nets.append((net, order, blob_report(net), net.nanuq6()))
for name, f in variants():
    myblob.formula12b = f
    bad = sum(1 for net, order, reps, M6 in nets if check_theorem12(net, order=order, reps=reps, M6=M6)['viol'])
    print("%-32s networks with a reported violation: %d of %d" % (name, bad, len(nets)))
