"""Exact checker for "shares at the leaves" certificates (science division, P7 report §5; their request P7-E2).

    from metricchain_eng.leafcert import check
    result = check("p7_02_cert_L16_P2_tau0.60_ff99SB.json")            # engine="c" (default) or "python"
    result.accepted, result.failure, result.counts

A certificate is an integer pairwise instance (tables ``H_i(a)``, ``J_ij(a, b)``), a bound ``L``, a branching
tree and leaf certificates ``(U, P2, m)``.  ``result.accepted`` means: the file is well formed and, at every
leaf node of the tree, on the box ``D`` of that node,

    U_i   <= H_i(a) + sum_{j != i} m_ij(a)            for every site i and every a in D_i,
    P2_ij <= J_ij(a, b) - m_ij(a) - m_ji(b)           for every pair i < j, a in D_i, b in D_j,
    L     <= sum_i U_i + sum_{i<j} P2_ij,

which implies ``sum_i H_i(x_i) + sum_{i<j} J_ij(x_i, x_j) >= L`` for every state ``x`` of the product of the
alphabets (proof in the header of ``leafcert.c``).  It implies nothing about where the tables come from: the
certificate is for the integer instance written in the file, not for any model it was rounded from.

Modules: ``loader`` (strict JSON, structural validation, encoder for the C checker), ``leafcert.c`` with its
ctypes front end ``ckernel`` (64-bit input, 128-bit sums), ``pycheck`` (independent checker with Python
integers).  The two engines return the same verdict, the same first failing inequality and the same
operation counts on every input whose integers fit in 64 bits; beyond that the C engine rejects with
``kind == "range"`` and only the Python engine decides.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import loader, pycheck

__all__ = ["check", "Result"]


@dataclass(frozen=True)
class Result:
    """Outcome of :func:`check`.

    ``accepted``   the certificate is well formed and every inequality holds
    ``kind``       ``None`` if accepted, else why not: ``"inequality"`` (one fails; see ``failure``),
                   ``"format"`` (not a well-formed certificate; see ``reason``), and for the C engine only
                   ``"range"`` (an integer outside 64 bits), ``"limit"`` (size limit of the implementation)
    ``reason``     one line of text
    ``failure``    the first failing inequality in the order of the traversal, or ``None``: a dict with
                   ``inequality`` (``"site"``, ``"pair"`` or ``"total"``), ``visit`` (rank of the leaf node),
                   ``leaf`` (index of its leaf certificate), ``path`` (the ``[site, state]`` pairs fixed above
                   it), ``i``, ``a``, ``j``, ``b`` and the two sides ``lhs > rhs``
    ``bound``      ``L``
    ``counts``     ``leaf_certificates``, ``leaf_boxes``, ``depth``, ``cert_integers``, ``instance_integers``,
                   ``additions``, ``comparisons`` (operations performed, up to and including a failure);
                   ``None`` if the file is not well formed
    ``engine``     ``"c"`` or ``"python"``
    ``notes``      annotation keys of the file that disagree with the certificate (never part of the verdict)
    """
    accepted: bool
    kind: str | None
    reason: str
    failure: dict | None
    bound: int | None
    counts: dict | None
    engine: str
    notes: tuple = ()

    def __bool__(self):
        return self.accepted

    @property
    def verdict(self):
        return "accept" if self.accepted else "reject"

    def to_dict(self):
        return {"verdict": self.verdict, "kind": self.kind, "reason": self.reason, "failure": self.failure,
                "bound": self.bound, "counts": self.counts, "engine": self.engine, "notes": list(self.notes)}


def check(path_or_obj, engine="c"):
    """Check a certificate: a path to a JSON file, JSON text as ``bytes``, or the parsed object.

    ``engine="c"`` runs ``leafcert.c`` (compiled on first use), ``engine="python"`` runs ``pycheck``.  The
    strict loader runs first in both cases; what it rejects is rejected with ``kind == "format"``.
    """
    if engine not in ("c", "python"):
        raise ValueError("engine must be 'c' or 'python'")
    try:
        obj = loader.load(path_or_obj)
        cert = loader.validate(obj)
    except loader.FormatError as exc:
        return Result(False, "format", str(exc), None, None, None, engine)
    if engine == "c":
        from . import ckernel
        out = ckernel.check_encoded(loader.encode(cert))
    else:
        out = pycheck.verify(obj)
    return Result(out["accepted"], out["kind"], out["reason"], out["failure"], out["bound"], out["counts"], engine,
                  tuple(loader.annotation_findings(obj, cert)))
