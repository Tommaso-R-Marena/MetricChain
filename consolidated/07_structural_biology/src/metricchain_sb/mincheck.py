"""Independent exact checker for "min" certificates (`metricchain_sb.mincert`).

Trusted-code statement.  This file is the whole checker: it imports the data classes, the
normalisation and the strict loader of `mincert`, the instance snapshot of `model`, numpy for
integer arrays, and nothing from the producer (`gmec`).  It performs integer additions,
subtractions, minima and comparisons only — no floating point, no search.

Exact arithmetic (review STRUCTBIO-REV-0001, findings 1, 4, 7).  The checker computes with the
`mincert.normalised` copy of the certificate — every integer a Python `int`, the node graph a
tree — and with the `model.integer_tables` snapshot of the instance taken at the same moment:
nothing that comes from the certificate or from the instance is a fixed-width NumPy integer
when it is validated, scaled or compared with a limit, and no neighbour list is taken from the
instance object.  The limits below are checked in Python integers *before* any power of two is
computed and before any table is converted; inside them every integer handled is bounded in
absolute value by `2**62`, so the numpy `int64` arithmetic of the leaf and prune inequalities is
exact.  Inputs outside the supported range are *rejected*, never wrapped:

* ``message_bits <= MAX_MESSAGE_BITS = 49`` and ``scale_bits <= model.MAX_SCALE_BITS = 1024``;
* every table entry times ``2**message_bits``, and every message, below ``2**50`` in absolute value;
* ``|lower_bound| < 2**62``; at most 4092 neighbours per site.

Semantics.  Identical to the theory division's kernel `verify` restricted to leaf / branch / prune
nodes (`proofs/CertificateAlgebra.lean`; soundness theorem `verify_sound`, **[V]**), for the
`PairInstance` whose table `J i j` is our pair table when `i < j` and zero when `i > j` (the
kernel's energy and its leaf and prune inequalities use the two orientations only through
their sum, so storing each pair once is that instance and needs no further theorem).  The checker's
*implementation* is not formally verified; it is tested against the theory division's reference
checker and against exhaustive enumeration (`tests/structbio/test_mincert.py`,
`tests/structbio/test_adversarial_mincheck.py`).

The checker never raises: every malformed or out-of-range input is a rejection with a reason.
`check_text` is the same from the text of a file.  Every verdict names the instance it is about
(`CheckResult.model_sha256`, the checksum of the tables the checker actually read).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction

import numpy as np

from .mincert import MalformedCertificate, MinCertificate, loads, snapshot, tables_sha256
from .model import MAX_SCALE_BITS

__all__ = ["CheckResult", "check_min_certificate", "check_text", "MAX_MESSAGE_BITS"]

_ENTRY_LIMIT = 2 ** 50          # bound on scaled table entries and on messages
_SUM_LIMIT = 2 ** 62            # bound on every intermediate sum
MAX_MESSAGE_BITS = 49           # 2**message_bits must stay below the entry limit


@dataclass
class CheckResult:
    accepted: bool
    reason: str = ""
    lower_bound: Fraction | None = None
    witness_energy: Fraction | None = None
    certified_gap: Fraction | None = None
    full_box: bool | None = None      # True iff the root box contains every state of every site: only then
                                      # is an accepted bound a bound on the *global* minimum of the instance
    stats: dict = field(default_factory=dict)
    model_sha256: str | None = None   # checksum (`mincert.model_sha256`) of the instance the verdict is about:
                                      # of the tables the checker read; None if it could not read an instance


def check_min_certificate(cert: MinCertificate) -> CheckResult:
    """Judge an in-memory certificate.  Never raises."""
    checksum = None
    try:
        cert, tables = snapshot(cert)
        try:
            checksum = tables_sha256(*tables)
        except ValueError:      # an entry too long to be written as a numeral: far outside the range accepted below
            pass
        result = _check(cert, tables)
    except MalformedCertificate as exc:
        result = CheckResult(False, f"malformed certificate: {exc}")
    except RecursionError:
        result = CheckResult(False, "malformed certificate: nested too deeply")
    except Exception as exc:  # noqa: BLE001  (a rejection is always sound)
        result = CheckResult(False, f"rejected: {type(exc).__name__} while checking")
    result.model_sha256 = checksum
    return result


def check_text(text, model=None, expected_model_sha256=None) -> CheckResult:
    """From the text of a `structbio-mincert/1` file to a verdict, in one call that never raises.

    `model` is the instance of a detached file (for a file that embeds its instance it must be
    that same instance, see `mincert.loads`).  With `expected_model_sha256` the verdict is a
    rejection unless the certificate is about the instance with that checksum — whoever holds
    the published checksum does not have to trust the instance inside the file.  Text that is
    not a well-formed certificate file is a rejection with the reason, not an exception."""
    try:
        cert = loads(text, model=model)
    except MalformedCertificate as exc:
        return CheckResult(False, f"malformed certificate: {exc}")
    except Exception as exc:  # noqa: BLE001  (`loads` raises nothing else; a rejection is always sound)
        return CheckResult(False, f"rejected: {type(exc).__name__} while reading")
    result = check_min_certificate(cert)
    if expected_model_sha256 is not None and result.model_sha256 != expected_model_sha256:
        return CheckResult(False, "the certificate is about another instance than the expected one "
                                  "(instance checksum differs)", model_sha256=result.model_sha256)
    return result


def _check(cert: MinCertificate, tables) -> CheckResult:
    """`cert` is normalised (Python integers, a tree); `tables` is the instance snapshot."""
    scale_bits, unary, pair = tables
    n = len(unary)
    if cert.message_bits > MAX_MESSAGE_BITS or scale_bits > MAX_SCALE_BITS:
        return CheckResult(False, f"message_bits or scale_bits outside the supported range "
                                  f"(at most {MAX_MESSAGE_BITS} and {MAX_SCALE_BITS})")
    mb = 2 ** cert.message_bits
    nbrs = [[] for _ in range(n)]                       # neighbours, derived here from the pair tables
    for (i, j) in pair:
        nbrs[i].append(j)
        nbrs[j].append(i)
    max_deg = max((len(v) for v in nbrs), default=0)
    max_abs = max((max(max(u), -min(u)) for u in unary), default=0)
    for rows in pair.values():
        max_abs = max(max_abs, max(map(max, rows)), -min(map(min, rows)))
    L = cert.lower_bound
    if max_abs * mb >= _ENTRY_LIMIT or abs(L) >= _SUM_LIMIT or (max_deg + 3) * _ENTRY_LIMIT >= _SUM_LIMIT:
        return CheckResult(False, "table magnitude or degree outside the supported integer range")

    H = [np.array(u, dtype=np.int64) * mb for u in unary]
    J = {key: np.array(rows, dtype=np.int64) * mb for key, rows in pair.items()}
    stats = {"leaf": 0, "branch": 0, "prune": 0}

    def pair_rows(i, j, a):
        """Row `J_{ij}(a, .)` over all states of `j`, whatever the stored orientation."""
        return J[(i, j)][a, :] if i < j else J[(j, i)][:, a]

    def leaf_ok(node, D):
        m = {}
        for key, vec in node["m"].items():
            if min(vec) <= -_ENTRY_LIMIT or max(vec) >= _ENTRY_LIMIT:
                raise MalformedCertificate("message outside the supported integer range")
            m[key] = np.array(vec, dtype=np.int64)
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

    unit = 2 ** (scale_bits + cert.message_bits)
    full_box = all(sorted(d) == list(range(len(u))) for d, u in zip(cert.domains, unary))
    result = CheckResult(True, "accepted", lower_bound=Fraction(L, unit), full_box=full_box, stats=stats)
    w = cert.witness
    if w is not None and all(w[i] in cert.domains[i] for i in range(n)):
        energy = sum(unary[i][a] for i, a in enumerate(w)) + sum(rows[w[i]][w[j]] for (i, j), rows in pair.items())
        result.witness_energy = Fraction(energy, 2 ** scale_bits)
        result.certified_gap = result.witness_energy - result.lower_bound
    return result
