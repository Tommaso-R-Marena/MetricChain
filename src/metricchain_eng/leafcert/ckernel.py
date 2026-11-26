"""ctypes front end of ``leafcert.c``.

The shared library is compiled on first use with the system C compiler into the build directory
(``$METRICCHAIN_ENG_BUILD`` or ``<repository>/build``, git-ignored), as in ``twolevel/ckernel.py``.  The
file name carries a hash of the source and of the compiler flags, so a library compiled from another
version of the source is never loaded.
"""
from __future__ import annotations

import ctypes as ct
import hashlib
import os
import subprocess
import threading
from pathlib import Path

SOURCE = Path(__file__).with_name("leafcert.c")
CFLAGS = ("-std=c11", "-O2", "-Wall", "-Wextra", "-Werror")
MAX_SITES = 4096                      # LC_MAX_SITES of leafcert.c
KINDS = (None, "inequality", "format", "range", "limit", "overflow")
INEQUALITIES = (None, "site", "pair", "total")


class _Result(ct.Structure):
    _fields_ = ([(name, ct.c_int64) for name in ("status", "inequality", "leaf", "visit", "i", "a", "j", "b")]
                + [("lhs_hi", ct.c_int64), ("lhs_lo", ct.c_uint64), ("rhs_hi", ct.c_int64), ("rhs_lo", ct.c_uint64),
                   ("path_len", ct.c_int64), ("bound", ct.c_int64), ("bound_valid", ct.c_int64)]
                + [(name, ct.c_uint64) for name in ("sites", "leaf_certificates", "leaf_boxes", "depth", "cert_integers",
                                                    "instance_integers", "additions", "comparisons")]
                + [("token", ct.c_int64), ("message", ct.c_char * 160)])


_libs = {}
_local = threading.local()


def build_dir() -> Path:
    env = os.environ.get("METRICCHAIN_ENG_BUILD")
    return Path(env) if env else SOURCE.resolve().parents[3] / "build"


def compile_c(out: Path, *, source: Path = SOURCE, flags=(), shared=True) -> Path:
    """Compile ``source`` to ``out`` (a shared library, or an executable with ``-DLEAFCERT_MAIN``)."""
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(f"{out.name}.{os.getpid()}.tmp")
    mode = ["-shared", "-fPIC"] if shared else ["-DLEAFCERT_MAIN"]
    subprocess.run(["cc", *CFLAGS, *flags, *mode, "-o", str(tmp), str(source)], check=True)
    os.replace(tmp, out)
    return out


def _cached(stem: str, suffix: str, flags, shared: bool) -> Path:
    digest = hashlib.sha256(SOURCE.read_bytes() + repr((CFLAGS, tuple(flags), shared)).encode()).hexdigest()[:16]
    out = build_dir() / f"{stem}-{digest}{suffix}"
    if not out.exists():
        compile_c(out, flags=flags, shared=shared)
    return out


def bind(path: Path):
    """Load a compiled library and declare the interface."""
    lib = ct.CDLL(str(path))
    lib.leafcert_check.argtypes = [ct.c_char_p, ct.c_size_t, ct.POINTER(_Result), ct.POINTER(ct.c_int64), ct.c_size_t]
    lib.leafcert_check.restype = ct.c_int
    lib.leafcert_result_size.argtypes = []
    lib.leafcert_result_size.restype = ct.c_size_t
    lib.leafcert_acc_bits.argtypes = []
    lib.leafcert_acc_bits.restype = ct.c_int
    if lib.leafcert_result_size() != ct.sizeof(_Result):
        raise RuntimeError("leafcert.c and ckernel.py disagree on the layout of the result")
    return lib


def load_library(*, acc64: bool = False):
    """The checker as a shared library.  ``acc64``: the build with 64-bit accumulators and overflow
    detection (for tests of that detection); the default accumulates in 128 bits."""
    key = bool(acc64)
    if key not in _libs:
        flags = ("-DLC_ACC64",) if acc64 else ()
        _libs[key] = bind(_cached("libleafcert64" if acc64 else "libleafcert", ".so", flags, True))
    return _libs[key]


def executable(*, flags=()) -> Path:
    """The stand-alone checker (``leafcert FILE...``), compiled on first use."""
    return _cached("leafcert", "", flags, False)


def check_encoded(data: bytes, lib=None) -> dict:
    """Run the C checker on an encoded certificate (``loader.encode``).  Same result dict as
    ``pycheck.verify``, with the additional kinds ``"range"``, ``"limit"`` and ``"overflow"``."""
    lib = lib or load_library()
    if not hasattr(_local, "path"):
        _local.path = (ct.c_int64 * (2 * MAX_SITES))()
    res = _Result()
    lib.leafcert_check(data, len(data), ct.byref(res), _local.path, 2 * MAX_SITES)
    kind = KINDS[res.status]
    message = res.message.decode("ascii", "replace")
    counts = None
    if res.status in (0, 1, 5):
        counts = {name: getattr(res, name) for name in ("leaf_certificates", "leaf_boxes", "depth", "cert_integers",
                                                         "instance_integers", "additions", "comparisons")}
    failure = None
    if res.status in (1, 5):
        failure = {"inequality": INEQUALITIES[res.inequality], "visit": res.visit, "leaf": res.leaf,
                   "path": [[_local.path[2 * q], _local.path[2 * q + 1]] for q in range(res.path_len)],
                   "i": None if res.i < 0 else res.i, "a": None if res.a < 0 else res.a,
                   "j": None if res.j < 0 else res.j, "b": None if res.b < 0 else res.b,
                   "lhs": (res.lhs_hi << 64) | res.lhs_lo if res.status == 1 else None,
                   "rhs": (res.rhs_hi << 64) | res.rhs_lo if res.status == 1 else None}
    if res.status in (2, 3, 4) and res.token >= 0:
        message = f"token {res.token}: {message}"
    return {"accepted": res.status == 0, "kind": kind, "reason": message, "failure": failure,
            "bound": res.bound if res.status in (0, 1, 5) else None, "counts": counts}
