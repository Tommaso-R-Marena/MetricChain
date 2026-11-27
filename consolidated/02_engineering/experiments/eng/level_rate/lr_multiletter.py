"""Beyond two letters: a product landscape for which hypothesis (H1) of Theorem R fails at one slope.

Site: q equally likely letters with the Hamming envelope of slope u (THEORY_REPORT 11.26, Proposition
11.103(e)).  The vertices of its Lipschitz polytope are the indicator functions -u 1_A of the nonempty proper
subsets A (stated there); the Gibbs law of a vertex is pi_A(a) = e^{u 1_A(a)}/(|A| e^u + q - |A|).  By Theorem
11.99,

    F*(t) = max_M  -t ln sum_a ( sum_A M(A) pi_A(a)^t )^{1/t}.

The programme is the minimisation of a convex function of M that is invariant under permutations of the
letters, so some minimiser is invariant: uniform on the subsets of each size s, with weights m_s.  For such M
the inner sum does not depend on a and is LINEAR in (m_s), so the minimum is at one size:

    F*(t) = max_{1 <= s <= q-1} Phi_s(t),
    Phi_s(t) = (1 - t) ln q + t ln(s e^u + q - s) - ln(s e^{tu} + q - s)

(this derivation is ours; for q = 4 it reproduces the report's h = h_2, a = a_4, E = E_2 at u = 1, and is
checked in run_fourletter.py against a direct numerical solution of the programme over all 14 vertices).
Phi_s is concave with Phi_s(0) = Phi_s(1) = 0; the maximum of several concave functions is not concave, the
dual function J of R_REPORT is the concave envelope of F*, and theta_na = max_s theta_na^{(s)}.
"""
from __future__ import annotations

import math

import mpmath as mp
import numpy as np

import lr_pairs as P


class SubsetDip(P.GamePair):
    """The game function Phi_s of dips on the subsets of size s of q equally likely letters."""

    def __init__(self, q: int, s: int, u: float):
        self.q, self.s, self.u = q, s, float(u)
        self.name = f"dips on {s} of {q} letters, u={u:g}"
        self._const = None

    def F(self, t):
        t = np.asarray(t, dtype=float)
        q, s, u = self.q, self.s, self.u
        return (1 - t) * math.log(q) + t * math.log(s * math.exp(u) + q - s) - np.log(s * np.exp(t * u) + q - s)

    def dF(self, t):
        t = np.asarray(t, dtype=float)
        q, s, u = self.q, self.s, self.u
        e = s * np.exp(t * u)
        return -math.log(q) + math.log(s * math.exp(u) + q - s) - u * e / (e + q - s)

    def F_mp(self, t):
        t = mp.mpf(t)
        q, s, u = self.q, self.s, mp.mpf(self.u)
        return (1 - t) * mp.log(q) + t * mp.log(s * mp.exp(u) + q - s) - mp.log(s * mp.exp(t * u) + q - s)

    def _a_mp(self):
        q, s, u = self.q, self.s, mp.mpf(self.u)
        e = s * mp.exp(u)
        return mp.log(q) - mp.log(e + q - s) + u * e / (e + q - s)

    def _E_mp(self):
        q, s, u = self.q, self.s, mp.mpf(self.u)
        return -mp.log(q) + mp.log(s * mp.exp(u) + q - s) - u * mp.mpf(s) / q


class UniformHammingSite:
    """q equally likely letters, Hamming envelope of slope u: F* = max_s Phi_s; J = its concave envelope."""

    smooth = False

    def __init__(self, q: int, u: float, n_grid: int = 40001):
        self.q, self.u = q, float(u)
        self.name = f"uniform {q}-letter Hamming site, u={u:.12g}"
        self.parts = [SubsetDip(q, s, u) for s in range(1, q)]
        self.a = max(p.a for p in self.parts)
        self.E = max(p.E for p in self.parts)
        hs = [p.h for p in self.parts]
        self.h = max(hs)
        self.branch_h = hs
        self.branch_L = [p.L for p in self.parts]
        # the concave envelope of F* on a grid (upper hull of the points), for the line dynamics
        t = np.linspace(0.0, 1.0, n_grid)
        f = np.max(np.array([p.F(t) for p in self.parts]), axis=0)
        f[0] = f[-1] = 0.0
        idx = [0, 1]
        for i in range(2, n_grid):
            while len(idx) >= 2:
                i0, i1 = idx[-2], idx[-1]
                if (f[i1] - f[i0]) * (t[i] - t[i0]) <= (f[i] - f[i0]) * (t[i1] - t[i0]):
                    idx.pop()
                else:
                    break
            idx.append(i)
        self._tj, self._fj = t[idx], f[idx]
        self.envelope_differs = bool(len(idx) < n_grid)

    def Fstar(self, t):
        t = np.asarray(t, dtype=float)
        return np.max(np.array([p.F(t) for p in self.parts]), axis=0)

    def J(self, t):
        return np.interp(np.asarray(t, dtype=float), self._tj, self._fj)

    def theta_na(self, x):
        x = np.asarray(x, dtype=float)
        return np.max(np.array([p.theta_na(x) for p in self.parts]), axis=0)

    def flat_top(self, tol: float = 1e-9):
        """[L1, L2]: the set where the envelope J is within tol * h of its maximum (a short interval around a
        single point when (H1) holds; the interval between the two maximisers when two branches tie)."""
        t = np.linspace(0.0, 1.0, 400001)
        j = self.J(t)
        m = j >= j.max() - tol * self.h
        return float(t[m].min()), float(t[m].max())


def renyi_direct(q: int, u: float, t: float, restarts: int = 6, seed: int = 0) -> float:
    """F*(t) for the uniform q-letter Hamming site by direct minimisation of the convex function
    G(M) = sum_a (sum_A M(A) pi_A(a)^t)^{1/t} over the simplex of all 2^q - 2 vertices (no symmetry used):
    exponentiated-gradient descent from several random starts.  Slow and only moderately accurate; a check."""
    subsets = [A for A in range(1, 2**q - 1)]
    PA = np.array([[math.exp(u) if (A >> a) & 1 else 1.0 for a in range(q)] for A in subsets])
    PA = PA / PA.sum(axis=1, keepdims=True)
    W = PA**t                                       # (vertices, letters)
    rng = np.random.default_rng(seed)
    best = math.inf
    for r in range(restarts):
        M = rng.dirichlet(np.ones(len(subsets)))
        step = 5.0
        val = math.inf
        for it in range(4000):
            inner = M @ W
            G = float(np.sum(inner ** (1 / t)))
            grad = (W @ (inner ** (1 / t - 1))) / t
            Mn = M * np.exp(-step * (grad - grad.min()))
            Mn /= Mn.sum()
            Gn = float(np.sum((Mn @ W) ** (1 / t)))
            if Gn <= G:
                M, val = Mn, Gn
                step *= 1.1
            else:
                step *= 0.5
                val = G
                if step < 1e-12:
                    break
        best = min(best, val)
    return -t * math.log(best)
