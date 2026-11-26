#!/usr/bin/env python3
"""R13: tau_2 = sup T_2 of the cube in closed form (own derivation), as an anchor for the one-sided iteration.
tau_2 = inf_phi sup_{0<gamma<=phi a} [gamma + (1-phi) theta_na(gamma/(1-phi))]; theta_na is convex (value function of a
convex programme), so the bracket is convex in gamma and its sup is at an end: max((1-phi) a, phi a + (1-phi) theta_na(phi a/(1-phi))).
The first is decreasing in phi, the second is increasing where it matters, so the minimum is at the crossing (found by bisection
on phi; both values printed).  mpmath, 30 digits."""
import mpmath as mp
mp.mp.dps = 30
def kl(r, q): return r*mp.log(r/q) + (1-r)*mp.log((1-r)/(1-q))
for u in ('0.5', '1', '2'):
    u = mp.mpf(u); p = 1/(1+mp.e**u); half = mp.mpf(1)/2
    a = kl(p, half); estar = kl(half, p)
    lam = mp.log(2/(1+mp.e**(-u))); h = kl(lam/u, half)
    def theta_na(x):
        if x >= estar: return mp.mpf(0)
        if x <= 0: return a
        rho = mp.findroot(lambda r: kl(r, p) - x, (p + (half-p)*mp.mpf('0.5')), solver='anderson') if False else None
        lo, hi = p, half
        for _ in range(110):
            mid = (lo+hi)/2
            if kl(mid, p) <= x: lo = mid
            else: hi = mid
        return kl(lo, half)
    f1 = lambda phi: (1-phi)*a
    f2 = lambda phi: phi*a + (1-phi)*theta_na(phi*a/(1-phi))
    # scan then bisection on the crossing
    best = min((max(f1(mp.mpf(i)/2000), f2(mp.mpf(i)/2000)), i) for i in range(1, 2000))
    lo, hi = mp.mpf(best[1]-1)/2000, mp.mpf(best[1]+1)/2000
    for _ in range(90):
        mid = (lo+hi)/2
        if f1(mid) > f2(mid): lo = mid
        else: hi = mid
    phi = (lo+hi)/2
    print(f"u={u}: tau_2/a = {mp.nstr(max(f1(phi), f2(phi))/a, 10)} at phi = {mp.nstr(phi, 8)}  (f1/a={mp.nstr(f1(phi)/a,10)}, f2/a={mp.nstr(f2(phi)/a,10)}; scan minimum {mp.nstr(best[0]/a,8)});  (tau_2-h)*4/a = {mp.nstr((max(f1(phi), f2(phi))-h)*4/a, 6)};  h/a = {mp.nstr(h/a, 8)}")
print("# END")
