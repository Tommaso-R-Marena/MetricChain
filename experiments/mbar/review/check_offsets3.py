"""Referee A -- consequences of the false convergence for the two finite-sample statements that use
an UNCONSTRAINED fit started at f = 0:  (1) classifier_evalue (Theorem B5): the hindsight MBAR loss is
overestimated -> false rejection of a correct model;  (2) LRRegion.phi_min: with a good user-supplied
plug-in the region is declared empty (REJECT_MODEL) although it contains the truth.
The data are exact equilibrium samples; only a constant off_k is added to the energies of state k."""
import sys, warnings
import numpy as np
from scipy.special import logsumexp
sys.path.insert(0, "../src")
from d9mbar.estimators import mbar
from d9mbar.certificates import classifier_evalue, lr_confidence_region
warnings.filterwarnings("ignore")
K, J, n = 4, 6, 100
print("offset | classifier_evalue: rejections at alpha=0.05 (of which info['converged']=True) | "
      "lr_confidence_region with a correct plug-in: statuses, truth excluded")
for off_scale in (0.0, 5.0, 10.0, 20.0, 30.0, 50.0):
    rej = rej_conv = 0
    st = {}
    truth_out = 0
    trials = 200
    for rep in range(trials):
        rng = np.random.default_rng(5000 + rep)
        P = rng.dirichlet(np.ones(J) * 2, size=K)
        xs = np.concatenate([rng.choice(J, size=n, p=P[k]) for k in range(K)])
        y = np.repeat(np.arange(K), n)
        perm = rng.permutation(K * n); xs, y = xs[perm], y[perm]
        off = off_scale * rng.normal(size=K)
        U0 = -np.log(P[:, xs].T)
        U = U0 + off[None, :]
        ftrue = off.copy()                              # Z_k = e^{-off_k}

        def prob(b, prev, cur):
            cnt = np.ones((J, K)) * 0.5
            np.add.at(cnt, (xs[prev], y[prev]), 1.0)
            return (cnt / cnt.sum(axis=1, keepdims=True))[xs[cur]]
        try:
            logE, info = classifier_evalue(U, y, prob)
            if logE >= np.log(20):
                rej += 1
                rej_conv += int(info["converged"])
        except Exception as e:
            st["clf EXC " + type(e).__name__] = st.get("clf EXC " + type(e).__name__, 0) + 1

        def good_plugin(b, Uprev, yprev):
            f0, _ = mbar(Uprev - off[None, :], yprev)   # a correct estimate from earlier batches only
            return f0 + off
        try:
            reg = lr_confidence_region(U, y, plugin=good_plugin)
            st[reg.status] = st.get(reg.status, 0) + 1
            if reg.status == "REJECT_MODEL":
                truth_out += 1
            elif reg.status == "OK":
                truth_out += int(float(np.sum(logsumexp(reg.A + ftrue, axis=1) - ftrue[reg.labels])) > reg.level)
        except Exception as e:
            st["region EXC " + type(e).__name__] = st.get("region EXC " + type(e).__name__, 0) + 1
    print(f"{off_scale:6.1f} | {rej}/{trials} ({rej_conv}) | {st}, truth excluded or region declared empty: {truth_out}/{trials}")
