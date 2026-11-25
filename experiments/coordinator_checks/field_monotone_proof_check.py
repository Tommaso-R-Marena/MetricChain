# Check of the coordinator's proof that F*(t; theta) is nonincreasing in theta >= 0.
#  Phi(theta, s) = ln I_theta(theta+s) - t ln C(theta+s),  C(x) = 2 cosh(x/2),
#  I_theta(theta+s) = [sinh(t(u-s)/2) C(theta-u)^t + sinh(t(u+s)/2) C(theta+u)^t]/sinh(t u).
# Steps checked: (2) Phi(theta,.) has a single critical point (a maximum); (3) s* < 0 for theta > 0;
# (4) M'(theta) = dPhi/dtheta at s*, and its sign equals the sign of
#     -( [l(Q) - l(P)] - (1-t)[l((theta+u)/2) - l((theta-u)/2)] ),  l = ln cosh,
#     P = (theta-u)/2 + t(u-s*)/2, Q = (theta+u)/2 - t(u+s*)/2;
# (5) the interval-average lemma for tanh.
import numpy as np, math
lc = lambda x: np.log(np.cosh(x))
def Phi(theta, s, t, u):
    A = t*np.log(2*np.cosh((theta-u)/2)); B = t*np.log(2*np.cosh((theta+u)/2))
    return np.logaddexp(np.log(np.sinh(t*(u-s)/2)) + A, np.log(np.sinh(t*(u+s)/2)) + B) - math.log(math.sinh(t*u)) - t*np.log(2*np.cosh((theta+s)/2))
worst_uni = 0; worst_sign = 0; worst_env = 0; worst_ineq = 1e9; worst_mono = -1e9; cases = 0
for u in (0.3, 1.0, 2.0, 4.0):
    for t in (0.05, 0.3, 0.6, 0.9, 0.99):
        s = np.linspace(-u, u, 400001)[1:-1]
        prevM = None
        for theta in np.linspace(0.0, 6.0, 61):
            ph = Phi(theta, s, t, u)
            d = np.diff(ph)
            # unimodal: sign of the increments changes at most once, from + to -
            sg = np.sign(d[np.abs(d) > 1e-15])
            changes = int((np.diff(sg) != 0).sum())
            worst_uni = max(worst_uni, changes)
            i = int(ph.argmax()); sstar = s[i]; M = ph[i]
            if theta > 1e-9: worst_sign = max(worst_sign, sstar)       # must be < 0
            if prevM is not None: worst_mono = max(worst_mono, M - prevM)   # must be <= 0
            prevM = M
            # envelope formula against a finite difference of M
            h = 1e-5
            Mp = Phi(theta + h, s, t, u).max(); Mm = Phi(theta - h, s, t, u).max()
            fd = (Mp - Mm)/(2*h)
            a = math.sinh(t*(u-sstar)/2)*(2*math.cosh((theta-u)/2))**t; b = math.sinh(t*(u+sstar)/2)*(2*math.cosh((theta+u)/2))**t
            wA, wB = a/(a+b), b/(a+b)
            env = (t/2)*(wA*math.tanh((theta-u)/2) + wB*math.tanh((theta+u)/2) - math.tanh((theta+sstar)/2))
            worst_env = max(worst_env, abs(fd - env))
            P = (theta-u)/2 + t*(u-sstar)/2; Q = (theta+u)/2 - t*(u+sstar)/2
            ineq = (lc(Q) - lc(P)) - (1-t)*(lc((theta+u)/2) - lc((theta-u)/2))
            worst_ineq = min(worst_ineq, ineq)
            # sign agreement between env and -ineq (both ~0 at theta = 0)
            if abs(env) > 1e-7 and abs(ineq) > 1e-7 and (env > 0) != (ineq < 0): print("sign mismatch", u, t, theta, env, ineq)
            cases += 1
print(f"cases={cases}: max number of sign changes of the increments (1 = unimodal) = {worst_uni}; max s* for theta>0 = {worst_sign:.4f} (must be < 0)")
print(f"max increase of M between consecutive theta = {worst_mono:.2e} (must be <= 0); max |finite difference - envelope formula| = {worst_env:.2e}; min of the inequality (*) = {worst_ineq:.2e} (must be >= 0)")
# interval-average lemma: A(r) = avg of tanh over [c-r, c+r] nonincreasing in r for c >= 0
bad = 0
for c in np.linspace(0, 5, 51):
    r = np.linspace(1e-6, 8, 4001)
    A = (lc(c + r) - lc(c - r))/(2*r)
    if (np.diff(A) > 1e-12).any(): bad += 1
print("interval-average lemma violations:", bad)
