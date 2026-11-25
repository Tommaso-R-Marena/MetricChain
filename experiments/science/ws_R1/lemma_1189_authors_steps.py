#!/usr/bin/env python3
"""R1: the AUTHORS' proof of Lemma 11.89 (six steps), checked step by step with own code (mpmath, 40 digits).
 (1) information density iota = J b x - delta(h2) b - delta(h1) x + const
 (2) dI/dh1 = (1/2)(1 - mu^2) [T(h2) - delta(h1) Delta(h2)]          (finite differences of I itself)
 (3) T(h) < 0 for h > 0
 (4) -T - delta*Delta = [(ab+2b+1) ln((a+1)/(b+1)) - b(a+1) ln(a/b)] / ((a+1)(b+1)),  a = e^{2(h+J)}, b = e^{2(h-J)};
     and -T < delta*Delta for h > 0;  the reduction X ln(Y/X) < (1-Y) ln((1-X)/(1-Y))
 (5) for h2 > 0: the maximiser h1 = -k with delta(k) = g(h2) := -T/Delta, 0 < k < h2, g(k) < delta(h2);
     dC/dh2 = (1/2)(1-nu^2) Delta(k) [g(k) - delta(h2)] < 0  -- compared with a finite difference of the capacity
     C(h2) = max_{h1} I computed by direct maximisation (no formula)
 (6) C even, C(h2) < C(0) = K(J)."""
import random
import mpmath as mp
mp.mp.dps = 40
phi = lambda x: mp.log(mp.cosh(x))
def table(J, h1, h2):
    w = {(b, x): mp.e ** (J*b*x + h1*b + h2*x) for b in (1, -1) for x in (1, -1)}
    Z = sum(w.values()); return {k: v/Z for k, v in w.items()}
def MI(J, h1, h2):
    T = table(J, h1, h2)
    pb = {b: T[(b,1)] + T[(b,-1)] for b in (1,-1)}; px = {x: T[(1,x)] + T[(-1,x)] for x in (1,-1)}
    return sum(v*mp.log(v/(pb[k[0]]*px[k[1]])) for k, v in T.items())
delta = lambda J, h: (phi(h+J) - phi(h-J))/2
Tf = lambda J, h: J*(mp.tanh(h+J) + mp.tanh(h-J)) - 2*delta(J, h)
Delta = lambda J, h: mp.tanh(h+J) - mp.tanh(h-J)
g = lambda J, h: -Tf(J, h)/Delta(J, h)
rng = random.Random(1189)
e1 = e2 = e4 = mp.mpf(0); maxT = -mp.inf; max_kernel = -mp.inf; ok5 = True; e5 = mp.mpf(0); maxdC = -mp.inf; ok6 = True
for trial in range(400):
    J = mp.mpf(rng.uniform(0.02, 4)); h1 = mp.mpf(rng.uniform(-4, 4)); h2 = mp.mpf(rng.uniform(-4, 4))
    T = table(J, h1, h2)
    pb = {b: T[(b,1)] + T[(b,-1)] for b in (1,-1)}; px = {x: T[(1,x)] + T[(-1,x)] for x in (1,-1)}
    # (1): iota - (J b x - delta(h2) b - delta(h1) x) must be the same constant in all four cells
    cs = [mp.log(T[(b,x)]/(pb[b]*px[x])) - (J*b*x - delta(J,h2)*b - delta(J,h1)*x) for b in (1,-1) for x in (1,-1)]
    e1 = max(e1, max(cs) - min(cs))
    # (2)
    mu = pb[1] - pb[-1]
    grad = mp.diff(lambda t: MI(J, t, h2), h1)
    e2 = max(e2, abs(grad - (1 - mu**2)/2*(Tf(J,h2) - delta(J,h1)*Delta(J,h2))))
    # (3), (4) at h = |h2| > 0
    h = abs(h2) + mp.mpf('1e-3')
    maxT = max(maxT, Tf(J, h))
    a, b = mp.e**(2*(h+J)), mp.e**(2*(h-J))
    closed = ((a*b + 2*b + 1)*mp.log((a+1)/(b+1)) - b*(a+1)*mp.log(a/b))/((a+1)*(b+1))
    lhs = -Tf(J,h) - delta(J,h)*Delta(J,h)
    e4 = max(e4, abs(lhs - closed))
    max_kernel = max(max_kernel, lhs)
    X, Y = 1/(1+a), 1/(1+b)
    assert 0 < X < Y and X + Y < 1 and X*mp.log(Y/X) < (1-Y)*mp.log((1-X)/(1-Y))
for trial in range(60):
    J = mp.mpf(rng.uniform(0.05, 3)); h2 = mp.mpf(rng.uniform(0.02, 3))
    # (5): k from the formula, and the maximiser by direct maximisation of I over h1
    k = mp.findroot(lambda x: delta(J, x) - g(J, h2), h2/2)
    h1star = mp.findroot(lambda t: mp.diff(lambda s: MI(J, s, h2), t), -k*mp.mpf('0.9'))
    e5 = max(e5, abs(h1star + k))
    ok5 &= (0 < k < h2) and (g(J, k) < delta(J, h2))
    C = lambda hh: MI(J, mp.findroot(lambda t: mp.diff(lambda s: MI(J, s, hh), t), -k), hh)
    dC_fd = (C(h2 + mp.mpf('1e-6')) - C(h2 - mp.mpf('1e-6')))/mp.mpf('2e-6')
    T = table(J, -k, h2); nu = (T[(1,1)] + T[(-1,1)]) - (T[(1,-1)] + T[(-1,-1)])
    dC_formula = (1 - nu**2)/2*Delta(J, k)*(g(J, k) - delta(J, h2))
    assert abs(dC_fd - dC_formula) < mp.mpf('1e-9'), (dC_fd, dC_formula)
    maxdC = max(maxdC, dC_formula)
    K = J*mp.tanh(J) - mp.log(mp.cosh(J))
    ok6 &= (C(h2) < K) and abs(C(h2) - MI(J, k, -h2)) < mp.mpf('1e-25')
print(f"(1) spread of iota - (J b x - delta(h2) b - delta(h1) x) over the four cells <= {mp.nstr(e1, 3)}")
print(f"(2) |dI/dh1 - (1/2)(1-mu^2)[T(h2) - delta(h1)Delta(h2)]| <= {mp.nstr(e2, 3)}")
print(f"(3) max T(h) over h>0: {mp.nstr(maxT, 5)}  (< 0)")
print(f"(4) closed form of -T - delta*Delta: error <= {mp.nstr(e4, 3)}; max(-T - delta*Delta) = {mp.nstr(max_kernel, 5)} (< 0); reduction to X ln(Y/X) < (1-Y)ln((1-X)/(1-Y)) holds")
print(f"(5) maximiser h1* = -k with delta(k)=g(h2): |h1* + k| <= {mp.nstr(e5, 3)}; 0<k<h2 and g(k)<delta(h2): {ok5}; dC/dh2 formula = finite difference (1e-9); max dC/dh2 = {mp.nstr(maxdC, 5)} (< 0)")
print(f"(6) C(h2) < K(J) and C even: {ok6}")
print("SUMMARY:", "ALL PASS" if (e1 < 1e-30 and e2 < 1e-25 and maxT < 0 and e4 < 1e-30 and max_kernel < 0 and ok5 and maxdC < 0 and ok6 and e5 < 1e-20) else "FAILURES")
