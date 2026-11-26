"""
P7, a remark for item 1: what the lower model IS in each of the five gap analyses.

For each: the range of the residual g over X', its largest second-order constant, the largest distance
max |L - E| between P4's lower model and the energy E = f + g on X' (0 means the model is the energy itself),
and the largest distance between E and the known part f up to a constant (0 means the residual is constant).

usage: python3 -B p7_00_models.py > logs/p7_00_models.log    (last line "DONE p7_00_models")
"""
import sys, os, json, time
sys.dont_write_bytecode = True
import numpy as np
import p7lib as L7
from p7lib import L4

print(f"p7_00_models  started {L7.now()}")
five = json.load(open(os.path.join(L7.HERE, "out", "p7_01_five.json")))["gaps"]
print(f"{'instance':9s} {'tau':4s} {'split':15s} {'range of g':>11s} {'max c_ij':>9s} {'max |L - E|':>12s} {'range of f':>11s}   reading")
for g in five:
    inst = L4.load_instance(g["tag"], float(g["tau"]))
    Lmod, x0, E, C = L7.second_order_grid(inst, g["split"])
    res = inst["R"][g["split"]]
    rg = float(res.max() - res.min())
    d = float(np.abs(Lmod - E).max())
    f = inst["f"]
    reading = ("the lower model is the energy E itself" if d < 1e-8 else "a genuine lower model (constants > 0)") + (
        "; the residual is constant: E = f + const" if rg < 1e-5 else "")
    print(f"{g['family'] + str(g['nres']) + '/' + g['bb']:9s} {g['tau']:4s} {g['split']:15s} {rg:11.3e} {float(C.max()):9.2e} {d:12.3e} {float(f.max() - f.min()):11.3f}   {reading}")
# the binary instance (Leu16 on PPII): excitation energies of the changed states and the pair terms by separation
for g in five:
    if g["nres"] == 16:
        inst = L4.load_instance(g["tag"], float(g["tau"]))
        Lmod, x0, E, C = L7.second_order_grid(inst, g["split"])
        pm = L7.PM.from_grid(Lmod, x0)
        n = pm.n
        A = sorted((float(pm.A[i][1 - x0[i]]), i) for i in range(n))
        print(f"\n{g['family']}{g['nres']}/{g['bb']}: the three smallest excitation energies (kcal/mol, site): "
              + ", ".join(f"{a:.6f} (site {i})" for a, i in A[:3]) + f"; the largest {A[-1][0]:.4f}")
        by = {}
        for (i, j), T in pm.M.items():
            by.setdefault(j - i, []).append(abs(float(T[1 - x0[i], 1 - x0[j]])))
        print("   |pair term of the two changed states| by separation along the chain (min .. max over the pairs): "
              + "; ".join(f"{d}: {min(v):.4f}..{max(v):.4f}" for d, v in sorted(by.items())[:5]) + f"; separations >= 4: at most {max(max(v) for d, v in by.items() if d >= 4):.5f}")
        sg = {}
        for (i, j), T in pm.M.items():
            if j - i <= 3:
                sg.setdefault(j - i, [0, 0])[0 if T[1 - x0[i], 1 - x0[j]] < 0 else 1] += 1
        print("   signs (negative, positive) by separation: " + "; ".join(f"{d}: {tuple(v)}" for d, v in sorted(sg.items())))
print("DONE p7_00_models")
