"""R7: the growth test of ENG-RES-0009 section 2 with the finite-size-consistent form.
If N_cov(n) ~ classes(n) / (typical ball size) = classes(n) * exp(-n sigma_n), then
   N_cov(n+1)/N_cov(n) ~ g_n * exp(n sigma_n - (n+1) sigma_{n+1}),     g_n = classes(n+1)/classes(n),
which reduces to g_n / e^sigma only if sigma does not depend on n.  From the stored files (own code)."""
import json, math
from pathlib import Path
E = Path(__file__).resolve().parent / "eng_copy" / "experiments" / "eng" / "chain_cover" / "results"
e = json.load(open(E / "generic_Sc16_entropy.json"))["rows"]
g = json.load(open(E / "generic_Sc16.json"))["rows"]
for key, rho in (("L=1,eps=1/2*N", "0.5"), ("L=1,eps=1/4*N", "0.25")):
    print(key, "(radius rho =", rho + ")")
    for n in range(5, 14):
        a, b = e[str(n)], e[str(n + 1)]
        gr = b["classes"] / a["classes"]
        const = gr / math.exp(b["sigma"][rho]["mean"])
        fs = gr * math.exp(n * a["sigma"][rho]["mean"] - (n + 1) * b["sigma"][rho]["mean"])
        meas = ""
        if str(n) in g and str(n + 1) in g:
            ca, cb = g[str(n)]["cover"][key], g[str(n + 1)]["cover"][key]
            meas = f"{cb['upper'] / ca['upper']:.2f}" if ca["exact"] and cb["exact"] else f"[{cb['lower'] / ca['upper']:.2f}, {cb['upper'] / ca['lower']:.2f}]"
        print(f"  {n}->{n+1}: classes growth {gr:.3f}; constant-sigma prediction {const:.2f}; finite-size form {fs:.2f}; measured {meas}")
