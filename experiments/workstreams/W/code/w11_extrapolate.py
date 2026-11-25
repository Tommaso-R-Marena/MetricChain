"""w11: three-point extrapolations theta_n = a + b ln n/n + c/n of the exact finite-n series of w05 (hinted, instances
gamma* and H) and w07 (non-adaptive), read from the output files in ../out."""
import glob
import math
import re

import numpy as np


def fit3(pts):
    (n1, t1), (n2, t2), (n3, t3) = pts[-3:]
    A = np.array([[1, math.log(n) / n, 1 / n] for n in (n1, n2, n3)])
    a, b, c = np.linalg.solve(A, np.array([t1, t2, t3]))
    return a, b, c


for f in sorted(glob.glob("../out/w05_*.txt")):
    txt = open(f).read()
    R = float(re.search(r"R\^max\(eps_1\) = ([0-9.]+)", txt).group(1))
    for inst in ("gamma", "H"):
        pts = [(int(m.group(1)), float(m.group(2))) for m in re.finditer(r"n =\s+(\d+) \[%s\s*\].*?theta_n = ([0-9.]+)" % inst, txt)]
        if len(pts) >= 3:
            a, b, c = fit3(pts)
            print(f"{f[7:-4]:18s} [{inst:5s}] n = {[p[0] for p in pts]}: theta_n = {[p[1] for p in pts]}; 3-point fit a = {a:.6f} (b = {b:+.2f}, c = {c:+.2f}); R = {R:.6f}; a/R - 1 = {100*(a/R-1):+.1f} %")
for f in sorted(glob.glob("../out/w07_*.txt")):
    txt = open(f).read()
    R = float(re.search(r"theta_na\(x\) = R\(e\) = ([0-9.]+)", txt).group(1))
    pts = [(int(m.group(1)), float(m.group(2))) for m in re.finditer(r"n =\s+(\d+):.*?theta_n = ([0-9.]+)", txt)]
    if len(pts) >= 3:
        a, b, c = fit3(pts)
        print(f"{f[7:-4]:18s} [non-adaptive] n = {[p[0] for p in pts]}: theta_n = {[p[1] for p in pts]}; 3-point fit a = {a:.6f} (b = {b:+.2f}, c = {c:+.2f}); theta_na = {R:.6f}; a/theta_na - 1 = {100*(a/R-1):+.1f} %")
