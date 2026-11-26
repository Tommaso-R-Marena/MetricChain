"""Site-dependent slopes: certified cost bounds at finite n for cubes whose sites are of several types (X-014).

The class.  Sites i = 1..n with slopes u_i > 0; ``L_u(Q_n) = { psi : |psi(x) - psi(x + e_i)| <= u_i }``, the Lipschitz
class of the weighted Hamming distance d_u(x, y) = sum_i u_i [x_i != y_i]; uniform reference measure; the quantity is
A(psi) = 2^-n sum_x e^-psi(x).  A *block* is a multiset of sites, written ((u_1, n_1), ..., (u_m, n_m)).

What is used, and its status:

(1) **Inclusion [trivial].**  L_u(Q_n) is contained in L_{u_max}(Q_n): every procedure for the uniform cube with slope
    u_max is a procedure for the block.  This is the comparator "homogeneous algorithm".

(2) **Algorithm 2L+ with an outer block of one type [P; engineering; a transfer of the proof of Theorem K1 of
    docs/workstreams/K_REPORT.md §2.4 on the theory branch, not refereed].**  Let the outer block consist of n_o
    sites of one slope u_o and the inner block Y of any sites; write Omega = sum of all slopes (whole block),
    Omega_i = sum of the slopes of Y.  For psi in the class, every fibre psi(a, .) is in the class of Y and
    -ln W is in L_{u_o}(Q_{n_o}) for the fibre averages W (term by term, as in Lemma K.2).  The proof of Theorem K1
    uses the slope in exactly these places, and each survives with the substitution shown:
      * tables E_r, T_m, the ratios and r_dagger on the outer cube: Lemma K.1 for W, i.e. slope u_o       (unchanged)
      * s_0 = e^{-psi_0 - Omega},  s_0 <= W <= s_0 e^{2 Omega}                                       (u n  -> Omega)
      * the trivial bracket of a fibre has ratio e^{x_0}, x_0 = 2 Omega_i                             (u n_i -> Omega_i)
      * the first lower bound l = e^{-psi_0} prod_i (1 + e^{-u_i})/2  (w(x) >= e^{-psi_0 - d_u(x, 0)})
      * J = ceil((2 Omega + b + n_o ln 2)/lambda)   (Step 9: s_J e^-b >= s_0 e^{2 Omega} 2^{n_o} >= max W)
      * the width (Step 4): s_0 <= prod_i (2 p_{u_i}) * L, so
            x_out = ln[ prod_i 2 p_{u_i} + e^b ( e^lambda (1 + eta)/(1 - eta) + eta' + theta ) ],  p_u = 1/(1 + e^u).
    Steps 1-3 and 5-8 do not mention the slope.  The inner procedures are bracket procedures for the class of Y.
    Hence C_max = 1 + 2 M_bar + sum_l min{2 M_bar, (J + 1) cnt(x_{l-1})} C_l with these constants is a cost bound
    in every run, and nesting by certified cost (``certified.py``) applies with blocks in place of dimensions.

(3) **Lower bound for every algorithm [P; the argument of Theorem 11.25(a) with weighted balls].**  For rho > 0 the
    dip f_c(x) = -(rho - d_u(x, c))_+ is in the class, differs from 0 exactly on D_rho(c) = {d_u(x, c) < rho}, and
    raises A by the factor 1 + Exc(rho), Exc(rho) = 2^-n sum_{x in D_rho} (e^{rho - d_u(x, c)} - 1).  Translations of
    the cube preserve d_u and act transitively, so an (eps/2, delta)-correct algorithm makes at least
    (1 - 2 delta) 2^n / |D_rho| evaluations at the zero function whenever Exc(rho) > e^eps - 1.

(4) **Asymptotic exponent [theory report §11.26, Theorems 11.98-11.101: the site types share one slope t].**  For
    binary symmetric sites  h = max_{0<=t<=1} sum_j lambda_j F_j(t),
    F_j(t) = (1 - t) ln 2 - ln(1 + e^{-t u_j}) + t ln(1 + e^{-u_j})   (the Renyi-capacity form for the binary
    symmetric channel with crossover p_{u_j}); the non-adaptive exponent adds over sites, a = sum_j lambda_j a(u_j).

Everything is a natural logarithm.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field

import numpy as np

from scipy.special import gammaln

from .certified import WIDE_PHIS, acc_const, k0_lcost, k0_lcost_vec, tables
from .tables import LN2, CubeTables, cube_constants

Block = tuple          # ((u_1, n_1), ..., (u_m, n_m)), slopes distinct and decreasing, counts positive


def make_block(pairs) -> Block:
    acc: dict = {}
    for u, n in pairs:
        if n < 0 or u <= 0:
            raise ValueError("need u > 0 and n >= 0")
        if n:
            acc[float(u)] = acc.get(float(u), 0) + int(n)
    return tuple(sorted(acc.items(), reverse=True))


def dim(B: Block) -> int:
    return sum(n for _, n in B)


def omega(B: Block) -> float:
    return sum(u * n for u, n in B)


def l2p(B: Block) -> float:
    """ln prod_i 2 p_{u_i}  (<= 0)."""
    return sum(n * (LN2 - math.log1p(math.exp(u))) for u, n in B)


def eps_sum(B: Block) -> float:
    return sum(n * math.log(math.cosh(u / 2)) for u, n in B)


def umax(B: Block) -> float:
    return B[0][0]


def remove(B: Block, j: int, k: int) -> Block:
    u, n = B[j]
    if not 0 < k <= n:
        raise ValueError("cannot remove that many sites")
    return tuple((v, m - k if i == j else m) for i, (v, m) in enumerate(B) if not (i == j and m == k))


def remove_comp(B: Block, comp: Block) -> Block:
    """The block ``B`` without the sites of the composition ``comp`` (a sub-multiset of B)."""
    have = dict(B)
    for u, k in comp:
        if have.get(u, 0) < k:
            raise ValueError("composition is not part of the block")
        have[u] -= k
    return make_block(have.items())


# ---------------------------------------------------------------------------------------------
# Tables of a *mixed* outer block: the sorted-slope bounds
# ---------------------------------------------------------------------------------------------
def _window_logsum(prefix: np.ndarray, suffix: np.ndarray, lo: np.ndarray, hi: np.ndarray) -> np.ndarray:
    """ln sum_{i=lo}^{hi} e^{a_i} from ln-prefix sums (prefix[i] = ln sum_{i'<=i}) and ln-suffix sums; -inf where hi < lo.
    The difference of prefix sums is used where the terms grow with i and that of suffix sums where they decay, so
    that no subtraction of nearly equal numbers occurs in either tail."""
    n = prefix.size
    out = np.full(lo.shape, -np.inf)
    ok = hi >= lo
    lo_c = np.clip(lo, 0, n - 1)
    hi_c = np.clip(hi, 0, n - 1)
    p_hi = prefix[hi_c]
    p_lo = np.where(lo_c > 0, prefix[np.maximum(lo_c - 1, 0)], -np.inf)
    s_lo = suffix[lo_c]
    s_hi = np.where(hi_c < n - 1, suffix[np.minimum(hi_c + 1, n - 1)], -np.inf)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        via_p = p_hi + np.log1p(-np.exp(np.minimum(p_lo - p_hi, 0.0)))
        via_s = s_lo + np.log1p(-np.exp(np.minimum(s_hi - s_lo, 0.0)))
    use_p = (p_hi - p_lo) >= (s_lo - s_hi)                    # the better conditioned of the two differences
    out[ok] = np.where(use_p, via_p, via_s)[ok]
    return out


@dataclass
class MixedTables(CubeTables):
    """Tables of the m-cube whose sites have several slopes, for the sorted-slope tail bounds.

    Let U_j be the sum of the j largest slopes.  For V > 0 with -ln V in the class of d_u on Q_m:

      upper tail (Lemma N14 of the theory division's workstream N [P; theirs]):
          |{V > s}| <= |B(m, r)|, r <= m - 1   ==>   E (V - s)_+ <= s 2^-m E_r,
          E_r = sum_{j=1}^{r+1} (e^{U_j} - e^{U_{j-1}}) |B(m, r + 1 - j)|;
      lower tail (the same argument applied to Lemma K.1(b) [P; ours]):
          |{V >= t}| >= |B(m, k)|              ==>   E min(V, t) >= t 2^-m T(k),
          T(k) = sum_j C(m, j) e^{-U_{(j - k)_+}}
      (a point at Hamming distance i from a set is at weighted distance at most U_i from it; then Harper's theorem for
      the neighbourhoods, as in the uniform cube).

    With one slope these are the tables of ``CubeTables``.  ``u`` is the largest slope (the value of the ratio at
    radius 0 is e^{U_1} - 1)."""

    comp: Block = ()

    def __post_init__(self) -> None:
        comp = self.comp
        m = dim(comp)
        if m != self.m or abs(umax(comp) - self.u) > 0:
            raise ValueError("composition does not match (m, u)")
        j = np.arange(m + 1, dtype=float)
        self.lbinom = gammaln(m + 1.0) - gammaln(j + 1.0) - gammaln(m - j + 1.0)
        self.lball = np.logaddexp.accumulate(self.lbinom)
        r = np.arange(m + 1)
        k = np.arange(m + 1)
        lE = np.full(m + 1, -np.inf)
        lTail = np.full(m + 1, -np.inf)                      # ln sum_{i>=1} C(m, k+i) e^{-U_i}
        a_t, base = 0, 0.0                                   # segment (a_t, b_t] of the sorted slopes; U_{a_t} = base
        for u, cnt in comp:                                  # slopes in decreasing order
            b_t = a_t + cnt
            # E_r: sum_{j=a_t+1}^{min(b_t, r+1)} (e^u - 1) e^{base + u (j - a_t - 1)} |B(m, r+1-j)|
            #    = (e^u - 1) e^{base + u (r - a_t)} sum_{i=max(0, r+1-b_t)}^{r-a_t} |B(m, i)| e^{-u i}
            seq = self.lball - u * j
            pre = np.logaddexp.accumulate(seq)
            suf = np.logaddexp.accumulate(seq[::-1])[::-1]
            w = _window_logsum(pre, suf, np.maximum(0, r + 1 - b_t), r - a_t)
            lE = np.logaddexp(lE, math.log(math.expm1(u)) + base + u * (r - a_t) + w)
            # tail of T(k): sum_{i=a_t+1}^{min(b_t, m-k)} C(m, k+i) e^{-base - u (i - a_t)}
            #    = e^{-base + u (k + a_t)} sum_{jj=k+a_t+1}^{min(k+b_t, m)} C(m, jj) e^{-u jj}
            seq2 = self.lbinom - u * j
            pre2 = np.logaddexp.accumulate(seq2)
            suf2 = np.logaddexp.accumulate(seq2[::-1])[::-1]
            w2 = _window_logsum(pre2, suf2, k + a_t + 1, np.minimum(k + b_t, m))
            lTail = np.logaddexp(lTail, -base + u * (k + a_t) + w2)
            a_t, base = b_t, base + u * cnt
        self.lE = lE
        self.lT = np.logaddexp(self.lball, lTail)
        self.lGt = np.concatenate([[math.log(math.expm1(self.u))], self.lE[1:] - self.lball[:-1]])


_mixed: dict = {}
_mixed_total = 0
MIXED_BUDGET = 2_000_000


def mixed_tables(comp: Block) -> CubeTables:
    """Tables of an outer block with the composition ``comp``: the exact ones of the uniform cube if it has one
    slope, the sorted-slope ones otherwise (cached with a bound on memory)."""
    global _mixed_total
    if len(comp) == 1:
        return tables(comp[0][1], comp[0][0])
    t = _mixed.pop(comp, None)
    if t is None:
        t = MixedTables(m=dim(comp), u=umax(comp), comp=comp)
        _mixed_total += t.m
        while _mixed_total > MIXED_BUDGET and _mixed:
            old = next(iter(_mixed))
            _mixed_total -= _mixed.pop(old).m
    _mixed[comp] = t
    return t


# ---------------------------------------------------------------------------------------------
# Base procedure, constants of one level
# ---------------------------------------------------------------------------------------------
def base_lcost(B: Block, x: float, lid: float) -> tuple[float, str]:
    """The base bracket on a block: Proposition K0 for the slope of a one-type block, or for the largest slope of a
    mixed block (inclusion (1)); enumeration where it is cheaper."""
    c, kind = k0_lcost(dim(B), umax(B), x, lid)
    return c, kind if len(B) == 1 else f"{kind}(u_max)"


def base_lcost_vec(B: Block, xs, lid: float) -> np.ndarray:
    return k0_lcost_vec(dim(B), umax(B), xs, lid)


@dataclass(frozen=True)
class HDesign:
    """One level: the outer block is ``k`` sites of type ``j`` of the block it is applied to."""

    j: int
    k: int
    lam: float
    eta: float
    etap: float
    b: float
    Lr: int
    theta: float | None = None
    ltheta: float | None = None
    bounded: bool = True
    name: str = ""
    comp: Block | None = None       # a *mixed* outer block (sites of several types): then j, k are ignored

    def lth(self) -> float:
        return math.log(self.theta) if self.ltheta is None else self.ltheta

    def outer(self, B: Block) -> Block:
        """The composition of the outer block."""
        return self.comp if self.comp is not None else ((B[self.j][0], self.k),)


@dataclass
class HConstants:
    n_o: int
    u_o: float
    inner: Block
    J: int
    K: int
    lK: float
    lnu: float
    lM_bar: float
    l_inv_delta_p: float
    x_out: float
    xs: tuple
    lam: float
    eta: float
    nu0: float = 1.0
    m_max: int = 0
    r_dag: int = -1
    lth: float = 0.0
    etap: float = 1.0
    b: float = 0.0
    omega: float = 0.0          # Omega: the sum of all slopes of the block
    l2p: float = 0.0            # ln prod_i 2 p_{u_i}

    def lcnt(self, x: float) -> float:
        return max(self.lK, math.log(2 * (1 + self.eta) ** 2 / (1 - self.eta)) + self.lam + self.lnu + x)

    def lmult(self) -> np.ndarray:
        L = len(self.xs) - 1
        return np.array([min(LN2 + self.lM_bar, math.log(self.J + 1) + self.lcnt(self.xs[l - 1])) for l in range(1, L + 1)])


def constants(B: Block, D: HDesign, l_inv_delta: float) -> HConstants | None:
    """The constants of Theorem K1 in the form (2) of the module's header; None if the level does not exist."""
    if D.comp is None:
        u_o, n_j = B[D.j]
        if not 0 < D.k <= n_j or D.k == dim(B):
            return None
        comp = ((u_o, D.k),)
    else:
        comp = D.comp
        if not 0 < dim(comp) < dim(B):
            return None
        u_o = umax(comp)                                    # enters the design choice nu_1 only
    inner = remove_comp(B, comp)
    x0 = 2 * omega(inner)
    if not (D.b > 0 and x0 > D.b):
        return None
    if not (0 < D.lam <= 1 and 0 < D.eta <= 0.5 and 0 < D.etap <= 1):
        raise ValueError("parameter outside the range of Theorem K1")
    xs = [x0 * (D.b / x0) ** (l / D.Lr) for l in range(D.Lr + 1)]
    xs[-1] = D.b
    lth = D.lth()
    n_o = dim(comp)
    nu1 = max(1.0, math.exp(math.log(2 * n_o) + u_o - lth)) if D.bounded else 1.0
    J = math.ceil((2 * omega(B) + D.b + n_o * LN2) / D.lam)
    nu0 = max((J + 1) * math.expm1(D.lam) / D.etap, nu1) / (1 - D.eta)
    outer = mixed_tables(comp)
    r_dag = outer.r_dagger(D.eta, None, nu0, lth=lth)
    lpi = outer.lpi_dagger(r_dag)
    m_max = math.ceil((math.log(2 * (1 + D.eta) * nu0 / (1 - D.eta)) + D.lam - lpi) / LN2)
    K = math.ceil(3 * (1 + D.eta) / D.eta ** 2 * (math.log(2 * (J + 1) * (m_max + 1) * (D.Lr + 2)) + l_inv_delta))
    lK = math.log(K)
    lnu = lK + math.log(nu0)
    lM_dag = lK - math.log(1 - D.eta) - lpi
    lM_bar = math.log(2 * (1 + D.eta) * nu0) + D.lam + lM_dag
    inside = float(np.logaddexp.reduce([D.lam + math.log((1 + D.eta) / (1 - D.eta)), math.log(D.etap), lth]))
    x_out = float(np.logaddexp(l2p(B), D.b + inside))
    return HConstants(n_o=n_o, u_o=u_o, inner=inner, J=J, K=K, lK=lK, lnu=lnu, lM_bar=lM_bar,
                      l_inv_delta_p=math.log(4 * D.Lr) + l_inv_delta + lM_bar, x_out=x_out, xs=tuple(xs), lam=D.lam, eta=D.eta,
                      nu0=nu0, m_max=m_max, r_dag=r_dag, lth=lth, etap=D.etap, b=D.b, omega=omega(B), l2p=l2p(B))


# ---------------------------------------------------------------------------------------------
# Candidate designs
# ---------------------------------------------------------------------------------------------
def outer_choices(B: Block, phis=WIDE_PHIS):
    """(type index, number of sites): for every type, the fractions of the *block's* dimension that fit into the type,
    and the whole type; never the whole block."""
    d = dim(B)
    out = []
    for j, (_, n_j) in enumerate(B):
        ks = set()
        for p in phis:
            k = min(max(int(math.floor(p * d)), 1), d - 1)
            if k <= n_j:
                ks.add(k)
        if n_j < d:
            ks.add(n_j)
        out += [(j, k) for k in sorted(ks, reverse=True)]
    return out


def proportional_comps(B: Block, phis=WIDE_PHIS):
    """Mixed outer blocks: the same fraction of the sites of every type (the splits of Theorem 11.101)."""
    if len(B) < 2:
        return []
    out, seen = [], set()
    for p in phis:
        comp = make_block((u, int(math.floor(p * n))) for u, n in B)
        if len(comp) < 2 or comp in seen or dim(comp) >= dim(B):
            continue
        seen.add(comp)
        out.append(comp)
    return out


def candidates(B: Block, x: float, phis=WIDE_PHIS, blocks: str = "aligned"):
    """The family "wide" of ``certified.py`` with the outer block chosen among the types: the bounded design
    (lam = eta = eta' = theta = c = min(x/12, 1/3)) with three tolerances, and for x >= 8 the extensive design
    (lam = 1, eta = 1/2, eta' = 1, the largest theta) with three tolerances.

    ``blocks``: "aligned" — outer blocks of one type (exact tables); "mixed" — outer blocks with the same fraction of
    every type (sorted-slope tables; for a block of one type this is the same as "aligned"); "both"."""
    out = []
    c = min(x / 12, 1 / 3)
    bmax = x - acc_const(c) - 1e-6
    lp = l2p(B)
    choices = []                                             # (j, k, comp, label, x0)
    if blocks in ("aligned", "both") or len(B) == 1:
        choices += [(j, k, None, f"{k}x[u={B[j][0]:g}]", 2 * (omega(B) - B[j][0] * k)) for j, k in outer_choices(B, phis)]
    if blocks in ("mixed", "both"):
        choices += [(0, 0, comp, "mixed" + str(tuple(n for _, n in comp)), 2 * (omega(B) - omega(comp))) for comp in proportional_comps(B, phis)]
    for j, k, comp, label, x0 in choices:
        for bm, tag in ((x / 2, "x/2"), (bmax, "max"), (0.75 * bmax, "0.75max")):
            if bm <= 0 or bm > bmax or x0 <= bm * 1.5:
                continue
            out.append(HDesign(j=j, k=k, lam=c, eta=c, etap=c, b=bm, Lr=30, theta=c, bounded=True, comp=comp,
                               name=f"bounded(c={c:.3f},b={tag},outer={label})"))
        if x >= 8:
            for bfrac in (0.25, 0.5, 0.125):
                bm = bfrac * x
                if x0 <= bm * 1.5:
                    continue
                lth = (x - bm) + math.log1p(-(3 * math.e + 1 + math.exp(lp - bm)) * math.exp(-(x - bm)))
                out.append(HDesign(j=j, k=k, lam=1.0, eta=0.5, etap=1.0, b=bm, Lr=30, ltheta=lth, bounded=False, comp=comp,
                                   name=f"extensive(b={bfrac:g}x,outer={label})"))
    return out


def top_design(j: int, k: int, b: float = 0.5, lam: float = 0.2, eta: float = 0.05, etap: float = 0.05, theta: float = 0.05,
               Lr: int = 40, comp: Block | None = None) -> HDesign:
    """The top level of X-011 (certified accuracy 0.8715) with the outer block ``k`` sites of type ``j``, or the mixed
    composition ``comp``."""
    return HDesign(j=j, k=k, lam=lam, eta=eta, etap=etap, b=b, Lr=Lr, theta=theta, bounded=True, comp=comp,
                   name=f"top(outer={k} of type {j})" if comp is None else f"top(outer=mixed{tuple(n for _, n in comp)})")


def top_choices(B: Block, phis=WIDE_PHIS, blocks: str = "aligned"):
    """Top designs to try: (j, k, comp) for outer blocks of one type and/or proportional mixed ones."""
    out = []
    if blocks in ("aligned", "both") or len(B) == 1:
        out += [(j, k, None) for j, k in outer_choices(B, phis)]
    if blocks in ("mixed", "both"):
        out += [(0, 0, comp) for comp in proportional_comps(B, phis)]
    return out


# ---------------------------------------------------------------------------------------------
# The search (the algorithm of certified.Search with blocks for dimensions)
# ---------------------------------------------------------------------------------------------
@dataclass
class HBound:
    lCmax: float
    xout: float
    block: Block
    design: HDesign
    C: HConstants
    lC: np.ndarray
    servers: list = field(default_factory=list)

    def depth(self) -> int:
        return 1 + max([s.depth() for s in self.servers if isinstance(s, HBound)], default=0)


class HSearch:
    """min over the candidates of the certified cost of at most ``depth`` nested levels above base brackets, on blocks."""

    def __init__(self, phis=WIDE_PHIS, coarse_rule: bool = True, blocks: str = "aligned"):
        if blocks not in ("aligned", "mixed", "both"):
            raise ValueError(blocks)
        self.phis = phis
        self.blocks = blocks
        self.coarse_rule = coarse_rule
        self.nodes = 0
        self.levels = 0
        self.deadline: float | None = None

    def best(self, B: Block, x: float, lid: float, depth: int, cutoff: float = math.inf):
        self.nodes += 1
        if self.deadline is not None and (self.nodes & 255) == 0 and time.time() > self.deadline:
            raise TimeoutError("search deadline reached")
        c0, kind0 = base_lcost(B, x, lid)
        if depth == 0 or dim(B) < 2 or (self.coarse_rule and (x >= 0.9 * eps_sum(B) or dim(B) < 50)):
            return c0, kind0
        inc, desc = c0, kind0
        ranked = []
        bound = min(inc, cutoff)
        for D in candidates(B, x, self.phis, self.blocks):
            C = constants(B, D, lid)
            if C is None or C.x_out > x + 1e-9 or LN2 + C.lM_bar >= bound:
                continue
            lC0 = base_lcost_vec(C.inner, C.xs[1:], C.l_inv_delta_p)
            mult = C.lmult()
            base = float(np.logaddexp(0.0, LN2 + C.lM_bar))
            shallow = float(np.logaddexp(base, np.logaddexp.reduce(mult + lC0)))
            ranked.append((shallow, len(ranked), D, C, lC0, mult, base))
        ranked.sort(key=lambda t: t[:2])
        for shallow, _, D, C, lC0, mult, base in ranked:
            bound = min(inc, cutoff)
            if base >= bound:
                continue
            self.levels += 1
            if depth == 1:
                val, lC, servers = shallow, lC0, None
            else:
                res = self._deep(C, lC0, mult, base, depth, bound)
                if res is None:
                    continue
                val, lC, servers = res
            if val < inc:
                inc = val
                desc = HBound(lCmax=val, xout=C.x_out, block=B, design=D, C=C, lC=np.concatenate([[-np.inf], lC]),
                              servers=servers if servers is not None else ["base"] * len(lC0))
        return inc, desc

    def _deep(self, C: HConstants, lC0, mult, base: float, depth: int, bound: float):
        order = np.argsort(-(mult + lC0), kind="stable")
        lC = lC0.copy()
        servers = [None] * len(lC0)
        acc = base
        for l in order:
            if acc >= bound:
                return None
            rem = bound + math.log(-math.expm1(acc - bound)) if math.isfinite(bound) else math.inf
            c, s = self.best(C.inner, C.xs[l + 1], C.l_inv_delta_p, depth - 1, cutoff=rem - mult[l])
            acc = float(np.logaddexp(acc, mult[l] + c))
            lC[l] = c
            servers[l] = s
        if acc >= bound:
            return None
        return acc, lC, servers

    def top(self, B: Block, D: HDesign, lid: float, depth: int, cutoff: float = math.inf) -> HBound | None:
        C = constants(B, D, lid)
        if C is None:
            return None
        lC0 = base_lcost_vec(C.inner, C.xs[1:], C.l_inv_delta_p)
        mult = C.lmult()
        base = float(np.logaddexp(0.0, LN2 + C.lM_bar))
        if base >= cutoff:
            return None
        if depth == 1:
            val, lC, servers = float(np.logaddexp(base, np.logaddexp.reduce(mult + lC0))), lC0, None
            if val >= cutoff:
                return None
        else:
            res = self._deep(C, lC0, mult, base, depth, cutoff)
            if res is None:
                return None
            val, lC, servers = res
        return HBound(lCmax=val, xout=C.x_out, block=B, design=D, C=C, lC=np.concatenate([[-np.inf], lC]),
                      servers=servers if servers is not None else ["base"] * len(lC0))


# ---------------------------------------------------------------------------------------------
# Lower bound (3) and asymptotic exponents (4)
# ---------------------------------------------------------------------------------------------
def weighted_shells(B: Block):
    """(distances, ln counts) of the weighted Hamming distance from a point, sorted by distance: for every vector of
    flips per type (j_1, ..., j_m) the distance sum u_t j_t and the number prod C(n_t, j_t) of points."""
    from scipy.special import gammaln

    dist = np.zeros(1)
    lcnt = np.zeros(1)
    for u, n in B:
        j = np.arange(n + 1, dtype=float)
        lb = gammaln(n + 1.0) - gammaln(j + 1.0) - gammaln(n - j + 1.0)
        dist = (dist[:, None] + u * j[None, :]).ravel()
        lcnt = (lcnt[:, None] + lb[None, :]).ravel()
    order = np.argsort(dist, kind="stable")
    return dist[order], lcnt[order]


def hinted_lower_bound(B: Block, eps: float, delta: float) -> dict:
    """ln of the lower bound (3): the smallest dip {d_u < rho} (in number of points) whose excess exceeds e^eps - 1.

    The excess Exc(rho) is continuous and increasing in rho; the dip is constant between consecutive distance
    values.  So the smallest admissible dip is {d_u <= d_k} for the first distance value d_k such that the excess at
    rho -> d_{k+1} (the supremum over the interval on which the dip is that set) exceeds e^eps - 1; if the threshold is
    crossed inside the interval, any rho beyond the crossing gives the same set."""
    d, lc = weighted_shells(B)
    n = dim(B)
    # merge equal distances
    uniq, start = np.unique(np.round(d, 12), return_index=True)
    lcm = np.array([np.logaddexp.reduce(lc[s:e]) for s, e in zip(start, list(start[1:]) + [len(d)])])
    lball = np.logaddexp.accumulate(lcm)                       # ln |{d_u <= uniq[k]}|
    lS = np.logaddexp.accumulate(lcm - uniq)                   # ln sum_{d <= uniq[k]} cnt e^{-d}
    target = math.log(math.expm1(eps)) + n * LN2               # need  e^rho S_k - |ball_k| > (e^eps - 1) 2^n  for some rho <= next distance
    nxt = np.append(uniq[1:], np.inf)
    lead = nxt + lS
    with np.errstate(over="ignore", invalid="ignore"):
        lexc_sup = np.where(np.isinf(nxt), np.inf, lead + np.log1p(-np.exp(np.minimum(lball - lead, 0.0))))
    k = int(np.argmax(lexc_sup > target))
    if not lexc_sup[k] > target:
        raise ValueError("no dip is deep enough")
    # the least rho in (uniq[k], nxt[k]] at which the excess reaches the threshold: e^rho S_k = target' + |ball_k|
    rho = float(np.logaddexp(target, lball[k]) - lS[k])
    rho = max(rho, float(uniq[k]))
    return dict(lbound=math.log(1 - 2 * delta) + n * LN2 - float(lball[k]), rho=rho, radius_value=float(uniq[k]), ldip=float(lball[k]))


def site_F(u: float, t: float) -> float:
    """F(t) of a binary symmetric site of slope u: (1 - t) ln 2 - ln(p^t + q^t), p = p_u."""
    return (1 - t) * LN2 - math.log1p(math.exp(-t * u)) + t * math.log1p(math.exp(-u))


def asymptotic(B: Block) -> dict:
    """Exponents per site at a bounded accuracy: h = max_t sum lambda_j F_j(t) (one common t), the average of the
    one-type values h(u_j) (which is not the exponent), a = sum lambda_j a(u_j), and the same for u_max alone."""
    n = dim(B)
    lam = [(u, m / n) for u, m in B]

    def F(t):
        return sum(w * site_F(u, t) for u, w in lam)

    lo, hi = 0.0, 1.0
    for _ in range(200):                      # F is concave in t for binary symmetric sites: ternary search
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if F(m1) < F(m2):
            lo = m1
        else:
            hi = m2
    t = 0.5 * (lo + hi)
    return dict(h=F(t), t=t, h_average=sum(w * cube_constants(u).h for u, w in lam), a=sum(w * cube_constants(u).a for u, w in lam),
                h_umax=cube_constants(umax(B)).h, a_umax=cube_constants(umax(B)).a)
