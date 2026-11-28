"""
Phase II (adaptive hierarchy) -- the small-slope 'flag' obstruction (Proposition G of the report, section 7.1).

Units a = 1, h = 1/4.  Types Y in R^3 = (y, q, w) (levels r-2, r-1, r of a flag; the lower levels cancel),
rate |Y|^2, any Lipschitz body K inside the Euclidean ball of radius 2 (so F(Y) - F(e) <= 2 |Y - e|).
Anchors: D = { e : e_y^2 + e_q^2 <= theta, e_q^2 + e_w^2 <= theta }, where -F(e) <= (visible maximum) + e_y^2.
Claim:  for theta >= 1/4 and every Y with |Y_w| >= sqrt(theta):
            min_{e in D} [ e_y^2 + 2 |Y - e| ] - |Y|^2  <=  0.
Proof in the report: the anchor e = (min(y, b), sqrt(theta) (q, w)/rho), b = sqrt(theta) w / rho, reduces the claim to
            G0(Delta, rho) = Delta^2 + Delta/(2 rho) + rho^2 - 2 sqrt(Delta^2 + (rho - 1/2)^2) >= 0   (Delta >= 0, rho >= 1/2),
which follows from  Delta^4 + c2 Delta^2 + c0 >= 0,  c2 = 2 rho^2 - 2 + 1/(4 rho^2),  c0 = (rho-1)^2 (rho^2 + 2 rho - 1),
and  16 rho^4 (4 c0 - c2^2) = -(2 rho - 1)^3 (16 rho^3 - 8 rho^2 - 6 rho - 1).
This script (1) checks the factorisation symbolically, (2) checks G0 >= 0 and its general-theta form on grids,
(3) evaluates the left side of the claim by brute force over anchors for a grid of hidden points.
"""
import numpy as np, sympy as sp
r = sp.symbols('r', positive=True)
c2n = 8*r**4 - 8*r**2 + 1
c0 = (r-1)**2*(r**2+2*r-1)
lhs = sp.expand(64*r**4*c0 - c2n**2)
rhs = sp.expand(-(2*r-1)**3*(16*r**3-8*r**2-6*r-1))
print("(1) factorisation identity holds:", sp.simplify(lhs - rhs) == 0)
q = 16*r**3-8*r**2-6*r-1
r0 = float(sp.cos(sp.pi/8))
qs = [float(q.subs(r, v)) for v in np.linspace(0.5, r0, 2001)]
print("    q(rho) = 16 rho^3 - 8 rho^2 - 6 rho - 1 on [1/2, cos(pi/8)]: max = %.4f (negative, as needed)" % max(qs))
D = np.linspace(0, 6, 3001)[:, None]
worst = 9
for th in [0.25, 0.26, 0.3, 0.5, 1.0]:
    R = np.linspace(np.sqrt(th), 5, 4001)[None, :]
    G = D**2 + 2*(th/R)*D + R**2 - 2*np.sqrt(D**2 + (R-np.sqrt(th))**2)
    worst = min(worst, G.min())
    print("(2) theta = %.2f: min of Delta^2 + 2 (theta/rho) Delta + rho^2 - 2 sqrt(Delta^2 + (rho - sqrt(theta))^2) on the grid: %.3e" % (th, G.min()))
def brute(theta, ny=25, ne=81):
    rt = np.sqrt(theta); g = np.linspace(-rt, rt, ne)
    E1, E2, E3 = np.meshgrid(g, g, g, indexing='ij')
    msk = (E1**2 + E2**2 <= theta + 1e-12) & (E2**2 + E3**2 <= theta + 1e-12)
    E = np.stack([E1[msk], E2[msk], E3[msk]], axis=1); base = E[:, 0]**2
    best = (-9, None)
    for y1 in np.linspace(0, 1.4, ny):
        for y2 in np.linspace(0, 1.2, ny):
            for y3 in np.linspace(rt, 1.3, ny):
                Y = np.array([y1, y2, y3])
                v = np.min(base + 2*np.sqrt(((E - Y)**2).sum(1))) - Y @ Y
                if v > best[0]: best = (v, Y)
    return best, 2*np.sqrt(3)*(g[1]-g[0])/2*2
for th in [0.25, 0.27, 0.30]:
    (v, Y), err = brute(th)
    print("(3) theta = %.2f: brute-force max over hidden points of min over anchors: %+.4f at %s  (anchor-grid error up to +%.3f; plain dip value 1 - 2 sqrt(theta) = %+.4f)" % (th, v, np.round(Y, 2), err, 1 - 2*np.sqrt(th)))
