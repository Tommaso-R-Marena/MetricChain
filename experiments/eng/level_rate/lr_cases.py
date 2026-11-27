"""The instances of the independent check of Theorem R, and what the theory division reports for them.

``PINNED`` is the commit of the theory branch (claude/determined-ride-og1u7j) at which the reports were read;
every number under ``THEIRS`` was transcribed by hand from files of that commit (R_REPORT.md sections 0, 1, 11;
THEORY_REPORT.md section 11.19 remark (1); experiments/workstreams/R/out_r3_gauss_exact_lb.txt and
experiments/coordinator_checks/level_rate/out_lines_lb.txt, out_lines_lb_general.txt) -- none of those scripts
was executed.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import lr_pairs as P  # noqa: E402

PINNED = "fc3f5d989846ff5900034a5b072c24d9c4fd35b8"
RES = Path(__file__).resolve().parent / "results"


def make(case: str):
    """The pair of a case name."""
    if case == "gauss":
        return P.GaussPair()
    if case.startswith("cube_u"):
        return P.cube(float(case[6:]))
    if case.startswith("prod_"):                  # prod_<u1>_<u2>_l<lambda1>   or   prod3_<u1>_<u2>_<u3>
        parts = case.split("_")
        return P.product2(float(parts[1]), float(parts[2]), float(parts[3][1:]))
    if case.startswith("prod3_"):
        us = [float(v) for v in case.split("_")[1:]]
        return P.SitePair([(1.0 / 3, us[0], 0.5), (1.0 / 3, us[1], 0.5), (1.0 - 2.0 / 3, us[2], 0.5)],
                          name=f"three types u=({us[0]:g},{us[1]:g},{us[2]:g}), equal fractions")
    if case.startswith("biased_"):                # biased_p<p>_u<u>
        parts = case.split("_")
        return P.biased_cube(float(parts[1][1:]), float(parts[2][1:]))
    if case == "kinked":
        return P.KinkedPair()
    if case.startswith("powertop"):
        return P.PowerTopPair(float(case[8:]))
    raise KeyError(case)


VALIDATION = ["gauss", "cube_u1"]
NEW = ["prod_2_0.5_l0.25", "prod_2_0.5_l0.5", "prod_1_0.5_l0.25", "prod_1_0.5_l0.5", "prod_4_1_l0.25",
       "prod_4_1_l0.5", "biased_p0.3_u1"]
# attempts to break the law: extreme mixtures (boundary layers of F at t -> 0), three types, steep cubes
STRESS = ["prod_12_0.3_l0.03", "prod_20_1_l0.01", "prod_30_0.05_l0.002", "prod3_0.3_3_12", "cube_u20",
          "cube_u0.05", "biased_p0.02_u2"]
# pairs that violate hypothesis (H1): negative controls
NEGATIVE = ["kinked", "powertop4"]

# ---------------------------------------------------------------------------------------------------------------
# transcribed from the pinned commit (see the module docstring); nothing here is computed
# ---------------------------------------------------------------------------------------------------------------
THEIRS = {
    "cube_u1": {
        "a": 0.11094407, "h": 0.02913914, "L": 0.490034, "vartheta": 4.244977, "constant": 0.0711473,
        "constant_over_a": 0.64129,
        "tau_over_a": {2: 0.5004, 3: 0.361, 4: 0.311, 5: 0.290, 6: 0.280, 40: 0.2631},   # 11.19 remark (1)
        "lines_lb": {2: 0.0441846653, 3: 0.0357866497, 5: 0.0316179986, 10: 0.0297934159, 20: 0.0293090059,
                     40: 0.0291825463, 80: 0.0291501190, 100: 0.0291461830, 120: 0.0291440385, 160: 0.0291419004},
        "grid_recursion": {2: 0.0555255307, 3: 0.0401939046, 4: 0.0345213704, 5: 0.0321673595, 10: 0.0298218384,
                           20: 0.0293125086, 40: 0.0291830021, 80: 0.0291501797, 100: 0.0291462153,
                           120: 0.0291440588},
        "dual_ub_ratio": {120: 0.99873, 160: 0.99903},
    },
    "gauss": {
        "a": 1.0, "h": 0.25, "L": 0.5, "vartheta": 0.5, "constant": 0.61685028,
        "exact_lb_1e9": {2: 381966011, 3: 307978528, 10: 255679562, 40: 250376448, 160: 250023947},
        "shifted_ratio": {10: 1.0151, 40: 1.0010, 160: 1.00005},      # (k + 1/2)^2 (tau_k - 1/4) / (pi^2/16) >=
        "grid_recursion": {2: 0.5003328886, 3: 0.3559324861, 4: 0.3017864165, 5: 0.2787193349, 10: 0.2560223539,
                           20: 0.2515145668, 40: 0.2503816167, 80: 0.2500958910, 100: 0.2500614396,
                           160: 0.2500240518},
        "dual_ub_ratio": {100: 1.00016, 160: 1.00006, 320: 1.00001},
        "dual_ub_tau3": 5.0 / 14.0,
        "passage": {1e-2: 0.764, 1e-3: 0.906, 1e-4: 0.968, 1e-5: 0.990, 1e-6: 0.997},
    },
    "biased_p0.3_u1": {
        "a": 0.095300, "h": 0.02503352, "L": 0.490078, "vartheta": 4.954673, "constant": 0.06128986,
        "lines_lb": {2: 0.0379560724, 3: 0.0307429298, 5: 0.0271625228, 10: 0.0255954483, 20: 0.0251794170,
                     40: 0.0250708098, 80: 0.0250429585, 160: 0.0250358973},
        "lines_ratio": {160: 0.99197},
    },
    "biased_p0.1_u1": {"a": 0.043863, "h": 0.01152689, "L": 0.490231, "vartheta": 10.649336, "constant": 0.02793035,
                       "lines_lb": {160: 0.0115279755}, "lines_ratio": {160: 0.99796}},
    "biased_p0.1_u2": {"a": 0.163738, "h": 0.04813000, "L": 0.466621, "vartheta": 2.492315, "constant": 0.11396312,
                       "lines_lb": {160: 0.0481344164}, "lines_ratio": {160: 0.99283}},
    "biased_p0.02_u2": {"a": 0.043596, "h": 0.01273973, "L": 0.468006, "vartheta": 9.426415, "constant": 0.03019929,
                        "lines_lb": {160: 0.0127409012}, "lines_ratio": {160: 0.99291}},
}


def dump(name: str, obj) -> Path:
    RES.mkdir(exist_ok=True)
    path = RES / name
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return path


def load(name: str):
    with open(RES / name) as fh:
        return json.load(fh)
