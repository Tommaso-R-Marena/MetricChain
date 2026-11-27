"""Access to the reviewed package (``metricchain_sb`` of the structural-biology division) for the campaigns.

Nothing of that package is copied into this repository: it is imported from a read-only checkout whose path is
``$SB_CHECKOUT`` or, by default, ``MetricChain-sb-0544ff4`` next to this repository.  All calls into it go through
the wrappers below, which record *every* exception instead of letting it escape (an exception of its checker is a
finding against its claim Z5; an exception of its loader other than ``MalformedZCertificate`` is recorded too).
"""
from __future__ import annotations

import os
import signal
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_CHECKOUT = HERE.parents[2].parent / "MetricChain-sb-0544ff4"


def checkout() -> Path:
    return Path(os.environ.get("SB_CHECKOUT", str(DEFAULT_CHECKOUT)))


def available() -> bool:
    return (checkout() / "src" / "metricchain_sb" / "zcheck.py").is_file()


class Timeout(BaseException):
    """Raised by the alarm of ``time_limit`` (a ``BaseException`` so that ``except Exception`` cannot swallow it)."""


class time_limit:
    """``with time_limit(seconds): ...`` -- raises ``Timeout`` inside the block when the time is over."""

    def __init__(self, seconds: float):
        self.seconds = seconds

    def _fire(self, signum, frame):
        raise Timeout()

    def __enter__(self):
        self.old = signal.signal(signal.SIGALRM, self._fire)
        signal.setitimer(signal.ITIMER_REAL, self.seconds)
        return self

    def __exit__(self, *exc):
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, self.old)
        return False


_SB = None


def sb():
    """The modules of the reviewed package, imported once."""
    global _SB
    if _SB is None:
        root = checkout()
        if not available():
            raise RuntimeError(f"no checkout of the reviewed package (set SB_CHECKOUT; looked in {root.name})")
        sys.path.insert(0, str(root / "src"))
        import metricchain_sb.expo as expo
        import metricchain_sb.itables as itables
        import metricchain_sb.mincert as mincert
        import metricchain_sb.model as model
        import metricchain_sb.partition as partition
        import metricchain_sb.zcert as zcert
        import metricchain_sb.zcheck as zcheck
        _SB = dict(expo=expo, itables=itables, mincert=mincert, model=model, partition=partition, zcert=zcert,
                   zcheck=zcheck)
    return _SB


def pair_model(tables: dict):
    """Their ``PairModel`` from plain tables (``{"unary", "pair", "scale_bits"}``)."""
    return sb()["model"].PairModel(unary=[list(u) for u in tables["unary"]],
                                   pair={k: [list(r) for r in t] for k, t in tables["pair"].items()},
                                   scale_bits=tables["scale_bits"])


def plain_tables(pm) -> dict:
    """Plain Python tables of one of their models (exact integers)."""
    return {"unary": [[int(v) for v in u.tolist()] for u in pm.unary],
            "pair": {(int(i), int(j)): [[int(v) for v in row] for row in t.tolist()] for (i, j), t in pm.pair.items()},
            "scale_bits": pm.scale_bits}


def result_record(res) -> dict:
    """What a ``ZResult`` says, as exact data (``Fraction`` kept)."""
    out = {"accepted": bool(res.accepted), "reason": str(res.reason), "lo": res.ln_z_lo, "hi": res.ln_z_hi,
           "keep": res.keep, "pops": dict(res.populations), "removed_upper": res.removed_upper,
           "stats": dict(res.stats), "obj": res}
    return out


def their_load(text: str, pm):
    """``(certificate | None, error)``: ``error`` is ``None``, ``"malformed: ..."`` (their own rejection) or
    ``"EXC <type>: ..."`` for any other exception of their loader."""
    zcert = sb()["zcert"]
    try:
        return zcert.loads(text, pm), None
    except zcert.MalformedZCertificate as exc:
        return None, f"malformed: {exc}"
    except Timeout:
        raise
    except BaseException as exc:                                  # noqa: BLE001  (recorded, never hidden)
        return None, f"EXC {type(exc).__name__}: {str(exc)[:200]}"


def their_check(cert, arithmetic: str = "exact", exp_bits: int = 64, max_entries=5_000_000) -> dict:
    """Their checker on an in-memory certificate; an exception is recorded under ``"exception"``."""
    zcheck = sb()["zcheck"]
    try:
        res = zcheck.check_partition_certificate(cert, arithmetic=arithmetic, max_entries=max_entries,
                                                 exp_bits=exp_bits)
    except Timeout:
        raise
    except BaseException as exc:                                  # noqa: BLE001
        return {"accepted": False, "reason": "", "exception": f"{type(exc).__name__}: {str(exc)[:200]}",
                "lo": None, "hi": None, "pops": {}, "removed_upper": None, "keep": None, "stats": {}, "obj": None}
    out = result_record(res)
    out["exception"] = None
    return out


def their_check_text(text: str, pm, arithmetic: str = "exact", exp_bits: int = 64, max_entries=5_000_000) -> dict:
    """File pipeline: their loader, then their checker.  ``"load_error"`` is set when the loader refused."""
    cert, err = their_load(text, pm)
    if cert is None:
        return {"accepted": False, "reason": err, "load_error": err, "exception": None, "lo": None, "hi": None,
                "pops": {}, "removed_upper": None, "keep": None, "stats": {}, "obj": None}
    out = their_check(cert, arithmetic, exp_bits, max_entries)
    out["load_error"] = None
    return out


def their_population(rec: dict, state: int):
    """Their ``ZResult.population(state)`` (``None`` when not available)."""
    obj = rec.get("obj")
    if obj is None or obj.keep is None or not obj.accepted:
        return None
    lo, hi = obj.population(state)
    if lo is None or hi is None:
        return None
    return Fraction(lo), Fraction(hi)


def set_rounding(mode: str) -> int:
    """Switch the floating-point rounding mode of the process (x86-64 values of ``fesetround``).  Returns the
    previous mode as the integer of ``fegetround``."""
    import ctypes
    import ctypes.util
    libm = ctypes.CDLL(ctypes.util.find_library("m") or "libm.so.6")
    codes = {"nearest": 0x000, "downward": 0x400, "upward": 0x800, "towardzero": 0xC00}
    old = libm.fegetround()
    if libm.fesetround(codes[mode]) != 0:
        raise RuntimeError("fesetround failed")
    return old


def rounding_is_nearest() -> bool:
    one, tiny = 1.0, 2.0 ** -53
    return one + tiny == one and one - tiny / 2 == one
