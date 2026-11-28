"""Referee A -- mechanism of the silent wrong answer of mbar()/minimize_lse under energy offsets."""
import sys, warnings
import numpy as np
from scipy.special import logsumexp
sys.path.insert(0, "../src")
from d9mbar.estimators import mbar, minimize_lse
warnings.filterwarnings("ignore")
found = 0
tot = 0
for rep in range(400):
    rng = np.random.default_rng(100 + rep)
    K, n = 4, 100
    x0 = 0.7 * np.arange(K)
    off = 30.0 * rng.normal(size=K)
    x = np.concatenate([rng.normal(x0[k], 1.0, n) for k in range(K)])
    y = np.repeat(np.arange(K), n)
    U0 = 0.5 * (x[:, None] - x0[None, :]) ** 2
    U = U0 + off[None, :]
    f0, _ = mbar(U0, y)
    tot += 1
    try:
        f, info = mbar(U, y)
    except Exception:
        continue
    err = np.abs((f - f[0]) - (f0 - f0[0] + off - off[0])).max()
    if err > 1e-5:
        found += 1
        if found <= 3:
            A = np.log(np.bincount(y) / len(y))[None, :] - U
            psi = lambda g: float(logsumexp(A + g, axis=1).mean() - (np.bincount(y) / len(y)) @ g)
            fgood = f0 + off
            print(f"rep {rep}: offsets {np.round(off, 1)}")
            print(f"   returned f - f[0] = {np.round(f - f[0], 2)}   correct = {np.round(fgood - fgood[0], 2)}   max error {err:.1f}")
            print(f"   info: converged={info['converged']} iterations={info['iterations']} grad={info['grad']:.3e} "
                  f"decrement={info.get('decrement'):.3e} step={info.get('step'):.3e}")
            print(f"   objective at returned f = {psi(f):.6f}; at the correct f = {psi(fgood):.6f}  (difference {psi(f) - psi(fgood):.4f} per sample, "
                  f"{len(y) * (psi(f) - psi(fgood)):.1f} in total)")
print(f"offset scale 30, K=4, n=100 per state, strong overlap: mbar returned a wrong estimate with converged=True in {found} of {tot} data sets")
