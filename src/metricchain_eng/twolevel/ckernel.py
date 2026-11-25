"""ctypes front end of ``meanrun_kernel.c`` (the fast version of ``meanrun.mean_run``).

``Evaluator`` fixes the parameters of Algorithm 2L+ (tables, constants, inner costs, work
arrays) and evaluates many instances; ``run`` returns the same ``Run`` record as the
reference implementation.  The shared library is compiled on first use into ``build/``
(git-ignored) with the system C compiler.
"""
from __future__ import annotations

import ctypes as ct
import math
import os
import subprocess
from pathlib import Path

import numpy as np

from .alg2l import Constants, Params, constants, inner_costs, lC_max
from .meanrun import Instance, Law, Run
from .tables import CubeTables

_SRC = Path(__file__).with_name("meanrun_kernel.c")
_STATUS = ("closed-populated", "closed-unpopulated", "abort-levels", "abort-sample")
_RES = ("status", "j_stop", "r_close", "lM_last", "lM_max", "lL", "lU", "lA", "npop", "nneg", "min_pop_radius",
        "slack_valid_lower", "slack_valid_upper", "slack_width", "margin_iii", "slack_iv_M", "slack_iv_Mneg",
        "slack_iv_Mbar", "slack_v", "slack_vi", "lcost")


class _MrParams(ct.Structure):
    _fields_ = [(k, ct.c_int) for k in ("n", "n_o", "J", "m_max", "L", "harper", "enforce_abort", "oracle")] + \
               [(k, ct.c_double) for k in ("u", "lam", "b", "eta", "theta", "lK", "lnu", "psi0", "t0", "lpi_dag", "lM_bar",
                                           "lMneg_cap", "lcount_factor", "x_out", "lcnt_const")]


_lib = None


def _build_dir() -> Path:
    env = os.environ.get("METRICCHAIN_ENG_BUILD")
    return Path(env) if env else _SRC.resolve().parents[3] / "build"


def load_library(rebuild: bool = False):
    """Compile (if needed) and load the kernel."""
    global _lib
    if _lib is not None and not rebuild:
        return _lib
    out = _build_dir() / "libmeanrun.so"
    if rebuild or not out.exists() or out.stat().st_mtime < _SRC.stat().st_mtime:
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_suffix(f".{os.getpid()}.tmp")
        subprocess.run(["cc", "-O2", "-Wall", "-Wextra", "-Werror", "-shared", "-fPIC", "-o", str(tmp), str(_SRC), "-lm"], check=True)
        os.replace(tmp, out)
    lib = ct.CDLL(str(out))
    dp = np.ctypeslib.ndpointer(dtype=np.float64, flags="C_CONTIGUOUS")
    lib.mr_run.argtypes = [ct.POINTER(_MrParams), ct.c_int, dp, dp, dp, dp, dp, dp, dp, dp, ct.c_int, dp,
                           dp, np.ctypeslib.ndpointer(dtype=np.int8, flags="C_CONTIGUOUS"), dp, dp, dp, dp]
    lib.mr_run.restype = ct.c_int
    _lib = lib
    return lib


class Evaluator:
    """Fast mean runs of Algorithm 2L+ for fixed parameters ``P`` (see ``meanrun.mean_run``)."""

    def __init__(self, P: Params, outer: CubeTables | None = None, *, lC: np.ndarray | None = None, harper: bool = True,
                 enforce_abort: bool = True, count_grid: tuple = ()):
        self.P = P
        self.outer = outer if outer is not None else CubeTables(P.n_o, P.u)
        self.C: Constants = constants(P, self.outer)
        self.lib = load_library()
        self.count_grid = np.ascontiguousarray(count_grid if len(count_grid) else [0.0], dtype=np.float64)
        self.n_grid = len(count_grid)
        if P.n_i > 0:
            self.lC = np.ascontiguousarray(inner_costs(P, self.C) if lC is None else lC, dtype=np.float64)
            self.lCmax = lC_max(P, self.C, self.lC)
            self.xs = np.ascontiguousarray(P.xs, dtype=np.float64)
        else:
            self.lC = np.zeros(P.L + 1)
            self.lCmax = math.inf
            self.xs = np.zeros(P.L + 1)
        J = self.C.J
        self._lM = np.empty(J + 1)
        self._kind = np.empty(J + 1, dtype=np.int8)
        self._lq = np.empty(J + 1)
        self._lMneg = np.empty(J + 1)
        self._lcalls = np.empty(P.L + 1)
        self._res = np.empty(len(_RES))
        self._lE = np.ascontiguousarray(self.outer.lE)
        self._lball = np.ascontiguousarray(self.outer.lball)
        self._lT = np.ascontiguousarray(self.outer.lT)
        C = self.C
        self._par = _MrParams(
            n=P.n, n_o=P.n_o, J=J, m_max=C.m_max, L=P.L, harper=int(harper), enforce_abort=int(enforce_abort), oracle=0,
            u=P.u, lam=P.lam, b=P.b, eta=P.eta, theta=P.theta, lK=C.lK, lnu=C.lnu, psi0=0.0, t0=0.0,
            lpi_dag=C.lpi_dag, lM_bar=C.lM_bar, lMneg_cap=C.lMneg_cap, lcount_factor=C.lcount_factor, x_out=C.x_out,
            lcnt_const=math.log(2 * (1 + P.eta) ** 2 / (1 - P.eta)) + P.lam + C.lnu)

    def run(self, inst: Instance, oracle: str = "bottom", record: bool = False) -> Run:
        P, law = self.P, inst.law
        ls0 = -inst.psi0 - P.u * P.n
        if law.lw[0] < ls0 - 1e-9 or law.lw[-1] > ls0 + 2 * P.u * P.n + 1e-9:
            raise ValueError("the law is not supported in [s_0, s_0 e^{2un}]: psi0 does not belong to this instance")
        if P.n_i > 0 and not (-1e-9 <= inst.t0 <= P.xs[0] + 1e-9):
            raise ValueError("t0 must lie in [0, x_0]")
        par = self._par
        par.oracle = {"bottom": 0, "top": 1}[oracle]
        par.psi0, par.t0 = inst.psi0, inst.t0
        rc = self.lib.mr_run(ct.byref(par), len(law.lw), np.ascontiguousarray(law.lw), np.ascontiguousarray(law.lpr),
                             np.ascontiguousarray(law.ltail_ge), self._lE, self._lball, self._lT, self.xs, self.lC,
                             self.n_grid, self.count_grid, self._lM, self._kind, self._lq, self._lMneg, self._lcalls, self._res)
        if rc != 0:
            raise MemoryError("mr_run failed")
        v = dict(zip(_RES, self._res.tolist()))
        R = Run(status=_STATUS[int(v.pop("status"))])
        for k in ("j_stop", "r_close", "npop", "nneg"):
            setattr(R, k, int(v.pop(k)))
        for k, val in v.items():
            setattr(R, k, val)
        if R.closed:
            R.width = R.lU - R.lL
        if P.n_i > 0:
            R.lcalls = self._lcalls.copy()
            R.lCmax = self.lCmax
        if record:
            used = slice(0, R.j_stop + 1)
            R.lM, R.kind, R.lq, R.lMneg = self._lM[used].copy(), self._kind[used].copy(), self._lq[used].copy(), self._lMneg[used].copy()
        return R
