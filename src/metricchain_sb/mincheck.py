"""Independent exact checker for "min" certificates (`metricchain_sb.mincert`).

Trusted-code statement.  This file is the whole checker: it imports the data classes and the
structural validation of `mincert`, numpy for integer arrays, and nothing from the producer
(`gmec`).  It performs integer additions, subtractions, minima and comparisons only — no
floating point, no search.  Every integer handled is bounded in absolute value by `2**62`
(checked before any arithmetic: inputs outside the supported range are *rejected*, never
wrapped), so numpy `int64` arithmetic is exact.

Semantics.  Identical to the theory division's kernel `verify` restricted to leaf / branch / prune
nodes (`proofs/CertificateAlgebra.lean`; soundness theorem `verify_sound`, **[V]**), with pair
tables stored in one orientation (`verify_sound_real_symm` covers that reading).  The checker's
*implementation* is not formally verified; it is tested against the theory division's reference
checker and against exhaustive enumeration (`tests/structbio/test_mincert.py`).

The checker never raises: every malformed or out-of-range input is a rejection.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction

import numpy as np

from .mincert import MalformedCertificate, MinCertificate, validate_structure

__all__ = ["CheckResult", "check_min_certificate"]

_ENTRY_LIMIT = 2 ** 50          # bound on scaled table entries and on messages
_SUM_LIMIT = 2 ** 62            # bound on every intermediate sum


@dataclass
class CheckResult:
    accepted: bool
    reason: str = ""
    lower_bound: Fraction | None = None
    witness_energy: Fraction | None = None
    certified_gap: Fraction | None = None
    stats: dict = field(default_factory=dict)


def check_min_certificate(cert: MinCertificate) -> CheckResult:
    try:
        return _check(cert)
    except MalformedCertificate as exc:
        return CheckResult(False, f"malformed certificate: {exc}")
    except RecursionError:
        return CheckResult(False, "malformed certificate: nested too deeply")
    except Exception as exc:  # noqa: BLE001  (a rejection is always sound)
        return CheckResult(False, f"rejected: {type(exc).__name__} while checking")


def _check(cert: MinCertificate) -> CheckResult:
    validate_structure(cert)
    model = cert.model
    n = model.n
    mb = 2 ** cert.message_bits
    max_deg = max((len(model.neighbors(i)) for i in range(n)), default=0)
    if model.max_abs_entry() * mb >= _ENTRY_LIMIT or abs(cert.lower_bound) >= _SUM_LIMIT \
            or (max_deg + 3) * _ENTRY_LIMIT >= _SUM_LIMIT:
        return CheckResult(False, "table magnitude or degree outside the supported integer range")

    H = [np.array([int(v) for v in u.tolist()], dtype=np.int64) * mb for u in model.unary]
    J = {key: np.array([[int(v) for v in row] for row in t.tolist()], dtype=np.int64) * mb
         for key, t in model.pair.items()}
    nbrs = [model.neighbors(i) for i in range(n)]
    L = int(cert.lower_bound)
    stats = {"leaf": 0, "branch": 0, "prune": 0}

    def pair_rows(i, j, a):
        """Row `J_{ij}(a, .)` over all states of `j`, whatever the stored orientation."""
        return J[(i, j)][a, :] if i < j else J[(j, i)][:, a]

    def leaf_ok(node, D):
        m = {}
        for key, vec in node.get("m", {}).items():
            arr = np.array(vec, dtype=object)
            if any(abs(int(v)) >= _ENTRY_LIMIT for v in vec):
                raise MalformedCertificate("message outside the supported integer range")
            m[key] = arr.astype(np.int64)
        bound = 0
        for i in range(n):
            vals = H[i][D[i]].copy()
            for j in nbrs[i]:
                vec = m.get((i, j))
                if vec is not None:
                    vals += vec[D[i]]
            bound += int(vals.min())
        for (i, j), table in J.items():
            T = table[np.ix_(D[i], D[j])]
            mi, mj = m.get((i, j)), m.get((j, i))
            if mi is not None:
                T = T - mi[D[i]][:, None]
            if mj is not None:
                T = T - mj[D[j]][None, :]
            bound += int(T.min())
        return L <= bound

    def prune_ok(node, D):
        i, r, t = node["site"], node["remove"], node["dominator"]
        if t == r or t not in D[i].tolist():
            return False
        margin = int(H[i][r]) - int(H[i][t])
        for j in nbrs[i]:
            margin += int((pair_rows(i, j, r)[D[j]] - pair_rows(i, j, t)[D[j]]).min())
        return margin >= 0

    stack = [(cert.root, [np.array(d, dtype=np.int64) for d in cert.domains])]
    while stack:
        node, D = stack.pop()
        kind = node["node"]
        stats[kind] += 1
        if kind == "leaf":
            if not leaf_ok(node, D):
                return CheckResult(False, "a leaf bound is below the claimed lower bound", stats=stats)
        elif kind == "branch":
            i = node["site"]
            children = node["children"]
            for a in D[i].tolist():
                if a not in children:
                    return CheckResult(False, f"branch on site {i} has no child for state {a}", stats=stats)
                D2 = list(D)
                D2[i] = np.array([a], dtype=np.int64)
                stack.append((children[a], D2))
        else:  # prune
            if not prune_ok(node, D):
                return CheckResult(False, "a dead-end elimination step fails its dominance inequality", stats=stats)
            i, r = node["site"], node["remove"]
            D2 = list(D)
            D2[i] = D[i][D[i] != r]
            stack.append((node["rest"], D2))

    unit = 2 ** cert.unit_bits
    result = CheckResult(True, "accepted", lower_bound=Fraction(L, unit), stats=stats)
    w = cert.witness
    if w is not None and all(w[i] in cert.domains[i] for i in range(n)):
        result.witness_energy = model.energy(w)
        result.certified_gap = result.witness_energy - result.lower_bound
    return result
