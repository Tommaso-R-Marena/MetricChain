"""Workstream K, numerical check (vi): the outer loop of Algorithm 2L+ on RADIAL outer landscapes at large n_o,
"in expectation" (counts replaced by their means; everything in logarithms; no sampling).

The run of the outer loop depends on the instance only through the law of W(a) and on the inner oracle only through
which points of the tolerance zone it lets be HIGH (theta_z = 0: none, i.e. N = M p(s_j); theta_z = 1: all, i.e.
N = M p(s_j e^-b)).  For W(a) = exp(-F(d(a, centre))) the law is binomial.  For every level the pass at which it is
populated, negligible or closed is found in closed form (tail and counts are monotone in M).

Two variants: the algorithm of Theorem K1 ("harper"), and the same without the Harper term in the lower bound
("plain": the lower end of the coordinator's sketch, layer-cake only).

Reported per run: the closing level (populated or not), the closing radius, ln M_last/n_o against a, the width;
  min over the populated levels that were LEFT of (r(q_j) - p_u n_o)/sqrt(n_o ln n_o)      [section 5(2) of the report:
       populated levels sit within O(sqrt(n log n)) of p_u n_o or above -- in BOTH variants];
  claim (iii) of Theorem K1: every level left has r(q_j) > r_dagger                         [variant "harper"];
  claim (iv):  M_j^neg <= (1+eta) e^lam nu0 M_dagger, M_j <= Mbar                           [variant "harper"];
  claim (v):   M_j^neg p(s_j e^-x) <= nu e^lam (1+eta)/(1-eta) e^x for x on a grid          [both variants].
"""
import math, sys, time
import numpy as np
from klib import Cube, consts


def profiles(n_o, u, rng):
    d = np.arange(n_o + 1, dtype=float)
    pu = 1 / (1 + math.exp(u))
    out = {}
    out["flat"] = np.zeros(n_o + 1)
    out["cone"] = u * d
    out["cone slope u/2"] = 0.5 * u * d
    out["anti-cone"] = -u * d
    for frac in (0.5, 1.0, 1.5):
        R = int(frac * pu * n_o)
        out[f"flattened bottom R={frac:.1f} p_u n_o"] = u * np.maximum(d, R)
        out[f"mesa R={frac:.1f} p_u n_o"] = u * np.minimum(d, R)
    lam1 = math.log(2 / (1 + math.exp(-u)))
    for frac in (0.8, 1.0, 1.2):
        R = int(frac * lam1 / u * n_o)
        out[f"dip R={frac:.1f} Lambda1 n_o/u"] = -u * np.maximum(R - d, 0)
    c = Cube(n_o, u)
    F = np.zeros(n_o + 1)
    for k in range(1, n_o + 1):                                  # "staircase": s p(s) flat over many levels
        F[k] = F[k - 1] + min(u, c.lball_r(k) - c.lball_r(k - 1))
    out["staircase W ~ 1/|B(d)|"] = F
    for i in range(3):
        out[f"random walk {i}"] = np.concatenate([[0.0], np.cumsum(rng.uniform(-u, u, size=n_o))])
    out["2-periodic"] = (u / 2) * (-1.0) ** d
    return out, c


def run(F, cube, u, variant, theta_z, b=0.5, lam=0.5, eta=0.25, etap=0.1, theta=0.1, delta=0.05, Lx=6, law=None):
    """F: radial profile (-ln W as a function of the outer distance), or None with law = (ln W values, ln probabilities,
    psi0) for a non-radial outer landscape whose law of W is known exactly (additive landscapes)."""
    n_o = cube.n
    n = n_o                                                         # the outer problem alone (n_i = 0 in the constants)
    pu, lam1, estar, a, h = consts(u)
    ln2 = math.log(2)
    if law is None:
        # the law of W: ln W = -F(d), d ~ Bin(n_o, 1/2); sorted by ln W
        lw = -F
        lpr = cube.lb - n_o * ln2
        psi0_given = float(F[n_o // 2])                             # reference point at the median distance
    else:
        lw, lpr, psi0_given = law
    order = np.argsort(lw, kind="stable")
    lws = lw[order]
    lprob = lpr[order]
    ltail = np.concatenate([np.logaddexp.accumulate(lprob[::-1])[::-1], [-np.inf]])   # ltail[i] = ln P(W >= lws[i])
    def lp(ls):                                                     # ln P(W > e^ls)
        return float(ltail[np.searchsorted(lws, ls, side="right")])
    lA = float(np.logaddexp.reduce(lws + lprob))
    # constants of Theorem K1
    J = math.ceil((2 * u * n + b + n_o * ln2) / lam)
    nu1 = 2 * math.exp(u) * n_o / theta
    nu0 = max((J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
    lth = math.log(theta)
    ceta = math.log((1 - eta) / (1 + eta))
    rdag = -1
    for r in range(n_o):
        okN = cube.lGt[r] <= lth + math.log((1 - eta) * nu0)
        okP = min(cube.lGt[r] - ceta, cube.lG2(r, eta)) <= lth
        if okN and okP:
            rdag = r
        else:
            break
    lpidag = (cube.lball_r(rdag) if rdag >= 0 else math.log(0.5)) - n_o * ln2
    mmax = math.ceil((math.log(2 * (1 + eta) * math.exp(lam) * nu0 / (1 - eta)) - lpidag) / ln2)
    K = math.ceil(3 * (1 + eta) / eta ** 2 * math.log(2 * (J + 1) * (mmax + 1) * (Lx + 2) / delta))
    lK = math.log(K)
    lnu = lK + math.log(nu0)
    lMdag = lK - math.log(1 - eta) - lpidag
    lMbar = math.log(2 * (1 + eta) * math.exp(lam) * nu0) + lMdag
    psi0 = psi0_given
    ls0 = -psi0 - u * n
    lell = -psi0 + n * math.log((1 + math.exp(-u)) / 2)
    lsum = -np.inf                                                  # ln Sigma
    upper_terms = [ls0]
    res = dict(viol=[], minpop=math.inf, npop=0, nneg=0)
    xs_grid = [0.5, 2.0, 8.0, 32.0, 0.01 * n_o, 0.05 * n_o, 0.2 * n_o]
    for j in range(J + 1):
        ls = ls0 + j * lam
        lell_in = lell
        lMneg = lnu + ls - lell_in - b
        # claim (v) at this level
        for x in xs_grid:
            if lMneg + lp(ls - x) > lnu + lam - ceta + x + 1e-9:
                res["viol"].append(("count", j, x))
        if variant == "harper" and lMneg > math.log((1 + eta) * math.exp(lam) * nu0) + lMdag + 1e-9:
            res["viol"].append(("Mneg", j))
        lpz = lp(ls - b * theta_z)                                  # N = M p(s e^{-b theta_z}) in expectation
        m_pop = math.inf if lpz == -np.inf else max(0, math.ceil(-lpz / ln2 - 1e-12))
        m_neg = max(0, math.ceil((lMneg - lK) / ln2 - 1e-12))
        # closure at an unpopulated pass m (q = min(1, 1/((1-eta) 2^m))): the smallest such m
        m_empty = max(0, math.floor((n_o * ln2 - math.log(1 - eta)) / ln2 + 1e-12) + 1)      # 2^{n_o} q < 1
        m_close = m_empty
        r_ok = int(np.searchsorted(cube.lE[:n_o], lth + b + lell_in - ls + n_o * ln2 + 1e-12, side="right")) - 1
        if r_ok >= 0:
            m2 = max(0, math.ceil((n_o * ln2 - math.log(1 - eta) - cube.lball_r(r_ok)) / ln2 - 1e-12))
            m_close = min(m_close, m2)
        m_end = min(m_pop, m_neg)
        if m_close < m_end or (m_close == m_end and m_pop > m_neg):
            lM = lK + m_close * ln2
            lq = min(0.0, -math.log(1 - eta) - m_close * ln2)
            r = -1 if n_o * ln2 + lq < 0 else cube.radius(lq)
            ltailv = -np.inf if r < 0 else ls - n_o * ln2 + cube.lE[r]
            res.update(closed="unpopulated", level=j, r=r, lM=lM)
            break
        lM = lK + m_end * ln2
        if m_pop <= m_neg:                                          # populated at this pass
            lq = min(0.0, lpz - math.log(1 - eta))
            lpbar = lpz - math.log(1 + eta)
            k = cube.kball(n_o * ln2 + lpbar)
            lell = max(lell, ls - b + lpbar)
            if variant == "harper":
                lell = max(lell, ls - b - n_o * ln2 + cube.lT[k])
            r = -1 if n_o * ln2 + lq < 0 else cube.radius(lq)
            ltailv = -np.inf if r < 0 else (ls - n_o * ln2 + cube.lE[r] if r <= n_o - 1 else np.inf)
            lsum_new = np.logaddexp(lsum, math.log(-math.expm1(-lam)) - b + ls + lpbar)
            if ltailv <= lth + b + lell:
                lsum = lsum_new
                res.update(closed="populated", level=j, r=r, lM=lM)
                break
            lsum = lsum_new
            res["npop"] += 1
            if r <= n_o - 1:
                res["minpop"] = min(res["minpop"], (r - pu * n_o) / math.sqrt(n_o * math.log(n_o)))
        else:                                                       # negligible
            lq = min(0.0, -math.log(1 - eta) - m_end * ln2)
            r = cube.radius(lq)
            res["nneg"] += 1
        if variant == "harper":
            if r <= rdag:
                res["viol"].append(("closing radius", j, r, rdag))
            if lM > lMbar + 1e-9:
                res["viol"].append(("Mbar", j))
        upper_terms.append(math.log(math.expm1(lam)) + ls + lq)
    else:
        res.update(closed=None)
        return res
    upper_terms.append(ltailv)
    lU = float(np.logaddexp.reduce(np.array(upper_terms)))
    lL = max(lell, lsum)
    res.update(width=lU - lL, valid=(lL <= lA + 1e-9 and lA <= lU + 1e-9), lMdag=lMdag, rdag=rdag, K=K, J=J,
               bound=math.log((2 * pu) ** n + math.exp(b) * (math.exp(lam) * (1 + eta) / (1 - eta) + etap + theta)))
    return res


def additive_law(groups, u):
    """Law of -ln W(a) = sum_i c_i a_i for an additive outer landscape whose slopes c_i take the values mult*u/2 on
    groups of coordinates: groups = [(size, mult), ...], mult an integer in {-2,...,2} (|c_i| <= u).  Returns
    (ln W values, ln probabilities) on the lattice (u/2) Z, by convolving binomial laws in the log domain."""
    vals = np.array([0])                                            # in units of u/2
    lp = np.array([0.0])
    for size, mult in groups:
        if mult == 0:
            continue
        j = np.arange(size + 1)
        lb = np.array([math.lgamma(size + 1) - math.lgamma(k + 1) - math.lgamma(size - k + 1) for k in j]) - size * math.log(2)
        step = abs(mult)
        newlen = len(lp) + size * step
        acc = np.full(newlen, -np.inf)
        for k in range(size + 1):                                   # add k coordinates of this group
            seg = lp + lb[k]
            acc[k * step:k * step + len(lp)] = np.logaddexp(acc[k * step:k * step + len(lp)], seg)
        if mult > 0:
            vals = vals[0] + np.arange(newlen)
        else:                                                       # negative slopes: reflect this group's contribution
            # value = old + mult*k = old - step*k: rebuild with reversed shifts
            acc2 = np.full(newlen, -np.inf)
            for k in range(size + 1):
                seg = lp + lb[k]
                off = (size - k) * step
                acc2[off:off + len(lp)] = np.logaddexp(acc2[off:off + len(lp)], seg)
            acc = acc2
            vals = vals[0] - size * step + np.arange(newlen)
        lp = acc
    keep = np.isfinite(lp)
    return -(u / 2) * vals[keep].astype(float), lp[keep]          # ln W = -(u/2) * value


def additive_cases(n_o):
    third = n_o // 3
    return {
        "additive: slopes u (half), u/2 (half)": [(n_o // 2, 2), (n_o - n_o // 2, 1)],
        "additive: slopes u (third), 0 (rest)": [(third, 2), (n_o - third, 0)],
        "additive: slopes +u (half), -u (half)": [(n_o // 2, 2), (n_o - n_o // 2, -2)],
        "additive: slopes u, u/2, -u/2 (thirds)": [(third, 2), (third, 1), (n_o - 2 * third, -1)],
        "additive: slopes u/2 (all)": [(n_o, 1)],
    }


def main():
    lines = []
    def out(s=""):
        print(s); lines.append(s); sys.stdout.flush()
    quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
    ok = True
    t0 = time.time()
    rng = np.random.default_rng(11)
    for u in ((1.0,) if quick else (0.5, 1.0, 2.0)):
        pu, lam1, estar, a, h = consts(u)
        for n_o in ((2000,) if quick else (1000, 4000, 16000)):
            profs, cube = profiles(n_o, u, rng)
            out(f"\n=== u = {u}, n_o = {n_o}: p_u n_o = {pu * n_o:.0f}, a = {a:.5f};  b = 0.5, lam = 0.5, eta = 0.25, eta' = theta = 0.1")
            out(f"{'profile':34s} | variant th | closes at      r   | ln M/(n_o a) | width (bound) | levels pop/neg | min_pop (r - p_u n_o)/sqrt(n_o ln n_o)")
            worst = dict(harper=-math.inf, plain=-math.inf)
            for name, F in profs.items():
                for variant in ("harper", "plain"):
                    for tz in ((1,) if n_o > 4000 else (0, 1)):
                        res = run(F, cube, u, variant, tz)
                        if res.get("closed") is None:
                            ok = False; out(f"{name:34s} | {variant:6s} {tz}  | NO CLOSURE"); continue
                        if res["viol"] or not res["valid"] or (variant == "harper" and res["width"] > res["bound"] + 1e-9):
                            ok = False
                            out(f"   VIOLATION {name} {variant} {tz}: {res['viol'][:3]} valid={res['valid']} width={res['width']:.3f}")
                        worst[variant] = max(worst[variant], res["lM"] / (n_o * a))
                        mp = "    -   " if res["minpop"] == math.inf else f"{res['minpop']:8.3f}"
                        if tz == 1:
                            out(f"{name:34s} | {variant:6s} {tz}  | {res['closed']:11s} {res['r']:6d} | {res['lM'] / (n_o * a):12.4f} | {res['width']:5.3f} ({res['bound']:.3f}) | {res['npop']:6d}/{res['nneg']:<6d} | {mp}")
            out(f"largest ln M_last/(n_o a) over the profiles: with the Harper term {worst['harper']:.4f}, without {worst['plain']:.4f}")
            if n_o <= 4000:                                         # non-radial laws of W: additive outer landscapes
                for name, groups in additive_cases(n_o).items():
                    lwv, lpv = additive_law(groups, u)
                    if abs(float(np.logaddexp.reduce(lpv))) > 1e-8:
                        ok = False; out(f"   law of {name} is not normalised")
                    for variant in ("harper", "plain"):
                        for tz in (0, 1):
                            res = run(None, cube, u, variant, tz, law=(lwv, lpv, 0.0))     # reference point a = 0: psi = 0
                            if res.get("closed") is None:
                                ok = False; out(f"{name:40s} | {variant:6s} {tz}  | NO CLOSURE"); continue
                            if res["viol"] or not res["valid"] or (variant == "harper" and res["width"] > res["bound"] + 1e-9):
                                ok = False
                                out(f"   VIOLATION {name} {variant} {tz}: {res['viol'][:3]} valid={res['valid']} width={res['width']:.3f}")
                            mp = "    -   " if res["minpop"] == math.inf else f"{res['minpop']:8.3f}"
                            if tz == 1:
                                out(f"{name:40s} | {variant:6s} {tz}  | {res['closed']:11s} {res['r']:6d} | {res['lM'] / (n_o * a):12.4f} | {res['width']:5.3f} ({res['bound']:.3f}) | {res['npop']:6d}/{res['nneg']:<6d} | {mp}")
    out(f"\nno violation of claims (iii), (iv), (v), validity or width (in expectation): {ok}   ({time.time() - t0:.0f} s)")
    open("out_radial_trajectory.txt" if not quick else "out_radial_trajectory_quick.txt", "w").write("\n".join(lines) + "\n")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
