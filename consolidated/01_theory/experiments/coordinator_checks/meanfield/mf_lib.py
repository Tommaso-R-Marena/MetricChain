"""Type-level exponents for a known part that is a function of the type, f(x) = n*phi(|x|/n), on the cube with a
u-Lipschitz residual class.  Everything is a variational problem over profiles z = (a, b) around a centre of type m:
   a = P(X=0 | S=1), b = P(X=1 | S=0);  kappa = m(1-a) + (1-m) b  (type of the point),  rho = m a + (1-m) b  (distance),
   MI = I(S;X) = h(kappa) - m h(a) - (1-m) h(b).
Rate function of the type under the known part: I(kappa) = phi(kappa) - h(kappa) - min(phi - h)."""
import numpy as np


def hb(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return -(x * np.log(x) + (1 - x) * np.log1p(-x))


class Model:
    def __init__(self, phi, u, G=801, K=4001):
        self.u = u
        self.kap = np.linspace(0, 1, K)
        raw = phi(self.kap) - hb(self.kap)
        self.c0 = raw.min()
        self.Ik = raw - self.c0                                    # rate function on the kappa grid
        # v = largest u-Lipschitz minorant of I (inf-convolution with u|.|): two sweeps
        v = self.Ik.copy()
        dk = self.kap[1] - self.kap[0]
        for i in range(1, K):
            v[i] = min(v[i], v[i - 1] + u * dk)
        for i in range(K - 2, -1, -1):
            v[i] = min(v[i], v[i + 1] + u * dk)
        self.vk = v
        self.G = G
        self.a = np.linspace(0, 1, G)
        self.A, self.B = np.meshgrid(self.a, self.a, indexing="ij")
        self.hA, self.hB = hb(self.A), hb(self.B)

    def I(self, kappa):
        return np.interp(kappa, self.kap, self.Ik)

    def v(self, kappa):
        return np.interp(kappa, self.kap, self.vk)

    def fields(self, m):
        """arrays over the (a, b) grid for centre type m"""
        kap = m * (1 - self.A) + (1 - m) * self.B
        rho = m * self.A + (1 - m) * self.B
        MI = hb(kap) - m * self.hA - (1 - m) * self.hB
        MI = np.maximum(MI, 0.0)
        Ik = self.I(kap)
        cone = MI + Ik + self.u * rho                       # minus the exponent of the cone's weight at profile z
        Lam = cone.min()
        return dict(kap=kap, rho=rho, MI=MI, I=Ik, v=self.v(kap), J=cone - Lam, Lam=Lam)

    def theta_na(self, x, ms):
        """max over centre types of min{ MI : J_m <= x }  (cones truncated where the sample does not see them)"""
        best, arg = -1.0, None
        for m in ms:
            f = self.fields(m)
            ok = f["J"] <= x
            val = f["MI"][ok].min() if ok.any() else np.inf
            if val > best:
                best, arg = val, m
        return best, arg

    def R_formula(self, e, ms, which="v"):
        """max over m of min{ MI : u rho + w(kappa) - Lam_m <= e } with w = v (flat-histogram reference) or w = 0
        (the zero residual: the dip of radius rho is e-sensitive iff u rho - Lam_m >= e)"""
        best, arg = -1.0, None
        for m in ms:
            f = self.fields(m)
            eh = self.u * f["rho"] - f["Lam"] + (f["v"] if which == "v" else 0.0 if which == "0" else f["I"])
            ok = eh <= e
            val = f["MI"][ok].min() if ok.any() else np.inf
            if val > best:
                best, arg = val, m
        return best, arg

    def dip_exponent(self, chi_k, m, theta):
        """E(P_theta) for the symmetric instance chi (array on the kappa grid), centre type m:
        max over z in P = {MI >= theta} of [ -MI - I(kappa_z) + c_chi + min_{z' not in P} (u dist(z,z') - chi(kappa_z')) + chi(kappa_z) ]
        with c_chi = min(I + chi)  (normalisation of the Gibbs law of the instance)."""
        f = self.fields(m)
        chi = np.interp(f["kap"], self.kap, chi_k)
        c_chi = (self.Ik + chi_k).min()
        inside = f["MI"] >= theta
        if inside.all() or (~inside).all():
            return np.inf if inside.all() else -np.inf
        g = np.where(inside, np.inf, -chi)
        da = self.a[1] - self.a[0]
        wa, wb = self.u * m * da, self.u * (1 - m) * da
        T = g.copy()
        for i in range(1, self.G):                       # sweeps along a
            T[i, :] = np.minimum(T[i, :], T[i - 1, :] + wa)
        for i in range(self.G - 2, -1, -1):
            T[i, :] = np.minimum(T[i, :], T[i + 1, :] + wa)
        for j in range(1, self.G):                       # sweeps along b
            T[:, j] = np.minimum(T[:, j], T[:, j - 1] + wb)
        for j in range(self.G - 2, -1, -1):
            T[:, j] = np.minimum(T[:, j], T[:, j + 1] + wb)
        val = -f["MI"] - f["I"] - chi + c_chi + chi + T   # -MI - I_chi(kappa) + slack, slack = chi(z) + T(z)
        val = -f["MI"] - (f["I"] + chi - c_chi) + (chi + T)
        return float(val[inside].max())

    def R_dip(self, chi_k, e, ms, iters=22):
        """sup{theta : E(P_theta) >= e}, maximised over centre types (bisection in theta; E is nonincreasing)"""
        best, arg = 0.0, None
        for m in ms:
            lo, hi = 0.0, float(hb(np.array(m))) * 0.999
            if self.dip_exponent(chi_k, m, lo + 1e-4) < e:
                continue
            for _ in range(iters):
                mid = 0.5 * (lo + hi)
                if self.dip_exponent(chi_k, m, mid) >= e:
                    lo = mid
                else:
                    hi = mid
            if lo > best:
                best, arg = lo, m
        return best, arg
