"""ctypes front end of ``kernel.c`` (integer message passing and exact evaluation of messages on a box).

The shared library is compiled on first use with the system C compiler into the build directory
(``$METRICCHAIN_ENG_BUILD`` or ``<repository>/build``, git-ignored), as the checker's ``ckernel.py`` does; the
file name carries a hash of the source and of the flags.  ``pykernel.Kernel`` is the same interface in plain
Python (the reference the tests compare this one with).
"""
from __future__ import annotations

import ctypes as ct
import hashlib
import os
import subprocess
from pathlib import Path

import numpy as np

from .model import CModel

SOURCE = Path(__file__).with_name("kernel.c")
CFLAGS = ("-std=c11", "-O2", "-fwrapv", "-Wall", "-Wextra", "-Werror")
INT64_MIN = -(1 << 63)

_I64P = ct.POINTER(ct.c_int64)
_lib = None


def build_dir() -> Path:
    env = os.environ.get("METRICCHAIN_ENG_BUILD")
    return Path(env) if env else SOURCE.resolve().parents[3] / "build"


def load_library():
    """Compile (if needed) and load the kernel."""
    global _lib
    if _lib is not None:
        return _lib
    digest = hashlib.sha256(SOURCE.read_bytes() + repr(CFLAGS).encode()).hexdigest()[:16]
    out = build_dir() / f"libleafprod-{digest}.so"
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_name(f"{out.name}.{os.getpid()}.tmp")
        subprocess.run(["cc", *CFLAGS, "-shared", "-fPIC", "-o", str(tmp), str(SOURCE)], check=True)
        os.replace(tmp, out)
    lib = ct.CDLL(str(out))
    mp = ct.POINTER(CModel)
    lib.lp_model_size.restype = ct.c_size_t
    if lib.lp_model_size() != ct.sizeof(CModel):
        raise RuntimeError("kernel.c and model.py disagree on the layout of lp_model")
    lib.lp_eval.argtypes = [mp, _I64P, _I64P, _I64P, _I64P, _I64P, _I64P]
    lib.lp_eval.restype = ct.c_int64
    lib.lp_pull_site.argtypes = [mp, _I64P, _I64P, _I64P, ct.c_int64, _I64P]
    lib.lp_pull_site.restype = None
    lib.lp_probe_all.argtypes = [mp, _I64P, _I64P, _I64P, _I64P]
    lib.lp_probe_all.restype = None
    lib.lp_ascent.argtypes = [mp, _I64P, _I64P, _I64P, ct.c_int64, ct.c_int64, ct.c_int64, ct.c_int64, _I64P]
    lib.lp_ascent.restype = ct.c_int64
    lib.lp_decode.argtypes = [mp, _I64P, _I64P, _I64P, _I64P, _I64P]
    lib.lp_decode.restype = ct.c_int
    lib.lp_core.argtypes = [mp, _I64P, _I64P, _I64P]
    lib.lp_core.restype = None
    lib.lp_energy.argtypes = [mp, _I64P]
    lib.lp_energy.restype = ct.c_int64
    lib.lp_icm.argtypes = [mp, _I64P, _I64P, _I64P, ct.c_int64, _I64P]
    lib.lp_icm.restype = ct.c_int64
    _lib = lib
    return lib


def _p(arr):
    return arr.ctypes.data_as(_I64P)


class Kernel:
    """The kernels for one :class:`~metricchain_eng.leafprod.model.Model`.  Boxes are ``(dlen, dom)`` as returned
    by ``Model.box``; messages are ``int64`` vectors of length ``Model.M`` and are updated in place."""

    name = "c"

    def __init__(self, model):
        self.model = model
        self.lib = load_library()
        self.cm = ct.byref(model.cstruct)
        self._info = np.zeros(8, dtype=np.int64)
        self._work = np.zeros(int(model.k.max()) + 2 * model.n + 1, dtype=np.int64)

    def eval(self, dlen, dom, m):
        """Exact dual value of ``m`` on the box: ``(total, U, P, arg)`` with ``U[i]``, ``P[e]`` its terms and
        ``arg[i]`` a state that minimises the term of site ``i``."""
        mod = self.model
        U = np.empty(mod.n, dtype=np.int64)
        P = np.empty(max(mod.ne, 1), dtype=np.int64)
        arg = np.empty(mod.n, dtype=np.int64)
        self.lib.lp_eval(self.cm, _p(dlen), _p(dom), _p(m), _p(U), _p(P), _p(arg))
        P = P[:mod.ne]
        # every term is exact in int64 (model.py bounds tables and messages); their sum is taken with Python
        # integers, so that the total is exact whatever the number of terms
        return sum(U.tolist()) + sum(P.tolist()), U, P, arg

    def ascent(self, dlen, dom, m, target, max_sweeps, patience, wmode=0):
        """Integer block-coordinate ascent from ``m`` (in place).  Returns ``(value, sweeps, reached,
        nfree, first)``; ``value`` is ``None`` if no pass was made."""
        info = self._info
        value = self.lib.lp_ascent(self.cm, _p(dlen), _p(dom), _p(m), target, max_sweeps, patience, wmode, _p(info))
        if info[0] < 0:
            raise MemoryError("kernel.c: out of memory")
        first = None if info[3] == INT64_MIN else int(info[3])
        return (None if value == INT64_MIN else value), int(info[0]), bool(info[1]), int(info[2]), first

    def pull_site(self, dlen, dom, m, i):
        """Pull at site ``i`` for every state of its alphabet (``m`` in place); returns the terms
        ``theta[a] = H_i(a) + sum_e m_i,e(a)``."""
        theta = np.empty(int(self.model.k[i]), dtype=np.int64)
        self.lib.lp_pull_site(self.cm, _p(dlen), _p(dom), _p(m), i, _p(theta))
        return theta

    def probe_all(self, dlen, dom, m):
        """For every (site, state): the term of the site after a pull, messages unchanged (length ``S``)."""
        c = np.empty(self.model.S, dtype=np.int64)
        self.lib.lp_probe_all(self.cm, _p(dlen), _p(dom), _p(m), _p(c))
        return c

    def decode(self, dlen, dom, m):
        """A state of the box read off the messages (sequential decoding; exact on forests after a sweep)."""
        x = np.empty(self.model.n, dtype=np.int64)
        self.lib.lp_decode(self.cm, _p(dlen), _p(dom), _p(m), _p(x), _p(self._work))
        return x

    def core(self, dlen):
        """Degrees inside the 2-core of the graph of free sites (0 for the sites outside it)."""
        deg = np.empty(self.model.n, dtype=np.int64)
        self.lib.lp_core(self.cm, _p(dlen), _p(deg), _p(self._work))
        return deg

    def energy(self, x):
        return self.lib.lp_energy(self.cm, _p(x))

    def icm(self, x, box=None, max_sweeps=1000):
        """Iterated conditional modes from ``x`` (in place), inside ``box`` if given; returns the energy."""
        if box is None:
            return self.lib.lp_icm(self.cm, None, None, _p(x), max_sweeps, _p(self._work))
        return self.lib.lp_icm(self.cm, _p(box[0]), _p(box[1]), _p(x), max_sweeps, _p(self._work))
