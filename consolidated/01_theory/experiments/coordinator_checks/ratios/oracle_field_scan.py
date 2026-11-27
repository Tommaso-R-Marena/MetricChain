import numpy as np, itertools, math
def scan(n, p, u, m, rho):
    pts = np.array(list(itertools.product((0, 1), repeat=n)), dtype=np.int8)
    wt = pts.sum(axis=1)
    H = (pts[:, None, :] != pts[None, :, :]).sum(axis=2).astype(float)
    logpi = wt * math.log(p) + (n - wt) * math.log(1 - p)
    centre = np.array([1] * m + [0] * (n - m), dtype=np.int8)
    D = np.zeros(len(pts), dtype=bool)
    for c in range(n):
        D |= (pts != np.roll(centre, c)).sum(axis=1) <= rho
    out = ~D
    HD = H[np.ix_(D, out)]
    rows = []
    for gamma in np.linspace(-u, u, 21):
        psi = gamma * wt.astype(float)
        alt = psi.copy(); alt[D] = (psi[out][None, :] - u * HD).max(axis=1)
        vals = []
        for f in (psi, alt):
            lw = logpi - f; mx = lw.max(); w = np.exp(lw - mx)
            vals.append((mx + math.log(w.sum()), float((w * wt).sum() / w.sum() / n)))
        exc = np.exp(logpi - alt) - np.exp(logpi - psi)
        texc = float((exc * wt).sum() / exc.sum() / n) if exc.sum() > 0 else float("nan")
        rows.append((gamma, vals[1][0] - vals[0][0], vals[0][1], vals[1][1] - vals[0][1], texc))
    print(f"n={n} p={p} u={u} centre type {m} radius {rho}  |D'|={int(D.sum())}")
    print("   gamma    ln(1+Phi)   null type   F = alt - null    excess type")
    for r in rows:
        print("   %+.2f   %9.5f   %.5f    %+.3e      %.5f" % r)
scan(10, 0.25, 1.0, 5, 1)
scan(10, 0.25, 1.0, 3, 2)
