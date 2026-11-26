"""R11 / 08c -- convergence of my safe tilt-state bound with the grid (report, section 6.3: at p = 0.3,
t = 0.43, q~ = 0.255 its two ends are 0.04468 (safe, G = 1601) and 0.04435 (restricted)), and the
best reference for p = 0.1 (q~ > p).

Run:  python3 r11_08c_convergence.py      (about 2 minutes)
"""
import time
from r11_08_propG import Grid
T0 = time.time()
for p, t, q in ((0.3, 0.43, 0.255), (0.4, 0.452, 0.342), (0.2, 0.419, 0.2), (0.1, 0.398, 0.152)):
    row = []
    for G in (201, 401, 801, 1601):
        v = Grid(p, G).rate(t, q, iters=8000, tol=1e-11)[0]
        row.append(f"G={G}: {v:.6f}")
    print(f"p={p} t={t} q~={q}: safe bound for F_inf(t): " + "  ".join(row) + f"   [{time.time()-T0:.0f} s]", flush=True)
