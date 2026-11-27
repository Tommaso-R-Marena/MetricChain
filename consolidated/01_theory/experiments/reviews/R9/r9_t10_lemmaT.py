# R9 test 10: Lemma T (inherently typical subsets, binary alphabet, p-biased pi) and Steps 4-5 of the proof of
# Theorem F6, exactly, by enumeration (n <= 10):
#   (2) pi(C~) >= pi(C)(n+1)^{-2(m+1)^2};  (3) alpha_C - 2/m <= alpha <= alpha_C~;  (4) I(X_I;V|U_I) = alpha_C~ - alpha;
#   Step 4: for every x in C~ the conditional means of d(X'^n,x) and |X'^n| are n P(X' != X) and n Q;
#   Step 5: n^-1 D(P_X'^n || Q^n) <= I(X';U) + alpha_C~ - alpha     for arbitrary kernels W(x'|x,u).
import numpy as np, itertools, sys, time
from math import log, ceil
rng = np.random.default_rng(17); t0 = time.time()
def run(n, p, C_idx, m, nker=3):
    X = np.array(list(itertools.product([0, 1], repeat=n)), dtype=np.int64)
    pi = np.prod(np.where(X == 1, p, 1 - p), axis=1)
    inC = np.zeros(len(X), bool); inC[C_idx] = True
    piC = pi[inC].sum(); PC = np.where(inC, pi / piC, 0.0)
    # conditional laws p_i(1 | prefix) under pi(.|C) and the labels u_i(prefix) = quantised law (as a pair of ceilings)
    labels = np.zeros((len(X), n), dtype=np.int64)        # label id of (x^{i-1}) for every x in C
    lab_id = {}
    for i in range(n):
        # group by prefix of length i
        pref = X[:, :i] @ (1 << np.arange(i)[::-1]) if i > 0 else np.zeros(len(X), dtype=np.int64)
        for pr in np.unique(pref[inC]):
            sel = (pref == pr)
            tot = PC[sel].sum(); p1 = PC[sel & (X[:, i] == 1)].sum() / tot
            c1 = ceil(m * p1 - 1e-12); c0 = ceil(m * (1 - p1) - 1e-12)
            key = (c0, c1)
            if key not in lab_id: lab_id[key] = len(lab_id)
            labels[sel, i] = lab_id[key]
    nlab = len(lab_id); assert nlab <= (m + 1) ** 2
    uvals = {v: (k[1] / (k[0] + k[1])) for k, v in lab_id.items()}      # u(1)
    # joint types
    types = {}
    for xi in np.where(inC)[0]:
        cnt = np.zeros((nlab, 2), dtype=np.int64)
        for i in range(n): cnt[labels[xi, i], X[xi, i]] += 1
        types.setdefault(cnt.tobytes(), []).append(xi)
    best = max(types.values(), key=lambda idx: PC[idx].sum())
    Ct = np.array(best)
    cnt = np.zeros((nlab, 2)); 
    for i in range(n): cnt[labels[Ct[0], i], X[Ct[0], i]] += 1
    PUX = cnt / n
    PU = PUX.sum(axis=1)
    alpha_C = -log(piC) / n; alpha_Ct = -log(pi[Ct].sum()) / n
    alpha = 0.0
    for l in range(nlab):
        for a in (0, 1):
            if PUX[l, a] > 0: alpha += PUX[l, a] * log(PUX[l, a] / PU[l] / (p if a == 1 else 1 - p))
    ok2 = pi[Ct].sum() >= piC * (n + 1.0) ** (-2 * (m + 1) ** 2) * (1 - 1e-12)
    ok3 = (alpha_C - 2 / m <= alpha + 1e-12) and (alpha <= alpha_Ct + 1e-12)
    # (4): I(X_I; V | U_I) under X^n ~ pi(.|C~), V = (I, X^{I-1})
    PCt = np.zeros(len(X)); PCt[Ct] = pi[Ct] / pi[Ct].sum()
    Icond = 0.0
    for i in range(n):
        pref = X[:, :i] @ (1 << np.arange(i)[::-1]) if i > 0 else np.zeros(len(X), dtype=np.int64)
        for pr in np.unique(pref[Ct]):
            sel = (pref == pr); tot = PCt[sel].sum()
            l = labels[np.where(sel & (PCt > 0))[0][0], i]
            for a in (0, 1):
                pa = PCt[sel & (X[:, i] == a)].sum()
                if pa > 0: Icond += (pa / n) * log((pa / tot) / (PUX[l, a] / PU[l]))
    dev4 = abs(Icond - (alpha_Ct - alpha))
    # Steps 4-5 for random kernels W(1 | x, u)
    worst5 = -np.inf; dev_mean = 0.0
    for kk in range(nker):
        W1 = rng.uniform(0, 1, (nlab, 2))                 # P(X'=1 | U=l, X=a)
        if kk == 0: W1 = np.tile(np.array([0.0, 1.0]), (nlab, 1)) * 0.9 + 0.05      # close to the identity
        Q = float(sum(PUX[l, a] * W1[l, a] for l in range(nlab) for a in (0, 1)))
        Pneq = float(sum(PUX[l, a] * (W1[l, a] if a == 0 else 1 - W1[l, a]) for l in range(nlab) for a in (0, 1)))
        # law of X'^n
        Pout = np.zeros(len(X))
        for xi in Ct:
            pr1 = np.array([W1[labels[xi, i], X[xi, i]] for i in range(n)])
            probs = np.prod(np.where(X == 1, pr1[None, :], 1 - pr1[None, :]), axis=1)
            Pout += PCt[xi] * probs
            dev_mean = max(dev_mean, abs((probs * (X != X[xi][None, :]).sum(axis=1)).sum() - n * Pneq), abs((probs * X.sum(axis=1)).sum() - n * Q))
        Qn = np.prod(np.where(X == 1, Q, 1 - Q), axis=1)
        msk = Pout > 0
        Dn = float((Pout[msk] * np.log(Pout[msk] / Qn[msk])).sum()) / n
        # I(X';U)
        IXU = 0.0
        for l in range(nlab):
            if PU[l] <= 0: continue
            q1 = (PUX[l, 0] * W1[l, 0] + PUX[l, 1] * W1[l, 1]) / PU[l]
            for (qa, Qa) in ((q1, Q), (1 - q1, 1 - Q)):
                if qa > 0: IXU += PU[l] * qa * log(qa / Qa)
        worst5 = max(worst5, Dn - (IXU + alpha_Ct - alpha))
    return ok2, ok3, dev4, worst5, dev_mean, nlab, len(Ct)
cases = 0; bad2 = bad3 = 0; d4 = 0.0; w5 = -np.inf; dm = 0.0; needed = 0
for trial in range(70):
    n = int(rng.integers(5, 10)); p = rng.uniform(0.1, 0.9); N = 1 << n
    kind = trial % 5
    X = np.array(list(itertools.product([0, 1], repeat=n)))
    if kind == 0: C = np.where(rng.uniform(size=N) < rng.uniform(0.05, 0.6))[0]
    elif kind == 1: c = X[rng.integers(0, N)]; C = np.where((X != c).sum(axis=1) <= rng.integers(1, n // 2 + 1))[0]
    elif kind == 2: C = np.where(X.sum(axis=1) % 2 == 0)[0]
    elif kind == 3: C = np.where((X @ rng.normal(size=n)) > rng.normal())[0]
    else: C = np.where(np.all(X[:, 1:] + X[:, :-1] <= 1, axis=1))[0]      # no two adjacent ones (golden-mean set)
    if len(C) == 0: continue
    for m in (1, 2, 4):
        ok2, ok3, dev4, worst5, dev_mean, nlab, nCt = run(n, p, C, m)
        cases += 1; bad2 += (not ok2); bad3 += (not ok3); d4 = max(d4, dev4); w5 = max(w5, worst5); dm = max(dm, dev_mean)
print(f"{cases} (set, m) instances, n in 5..9, random p: violations of (2): {bad2}, of (3): {bad3}; max |I(X_I;V|U_I) - (alpha_C~ - alpha)| = {d4:.1e}; "
      f"Step 4 mean deviations <= {dm:.1e}; Step 5: max [n^-1 D(P_X'^n||Q^n) - I(X';U) - (alpha_C~ - alpha)] = {w5:+.2e} (must be <= 0)   [{time.time()-t0:.0f}s]")
