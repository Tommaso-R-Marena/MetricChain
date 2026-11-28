#!/usr/bin/env python3
"""Negative controls beyond n = 400: with a hypothesis of Lemma B dropped, the lemma's quantity exceeds the
allowance m(u + 5 ln(n+1)); with all hypotheses it does not.  Uses q1_lemma_b (my code)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import q1_lemma_b as q  # noqa: E402

out = []
for ns, roles, u, th in [((400, 400, 20), "QQT", 4.0, 1.0), ((400, 400, 20), "QQT", 4.0, 1.1),
                         ((400, 400, 20), "QQT", 2.0, 1.1), ((20, 400, 400), "PQT", 4.0, 1.1),
                         ((20, 400, 400), "PTT", 4.0, 1.1), ((20, 20, 960), "QQT", 4.0, 1.0),
                         ((20, 20, 960), "PQT", 4.0, 1.3)]:
    for kw, lab in [({}, "full"), (dict(use_h2=False), "no H2"), (dict(use_h1=False), "no H1"),
                    (dict(use_h1=False, use_h2=False), "no H1,H2")]:
        r = q.evaluate(ns, roles, u, th, **kw)
        flag = "VIOLATES allowance" if r["V"] > r["allowance"] else ""
        s = (f"ns={ns} roles={roles} u={u} th/h={th} [{lab:>9}]: V={r['V']:+9.3f} allow={r['allowance']:7.2f} "
             f"Vhid={r['Vhid']:+9.3f} checks={r['ok']} {flag}")
        print(s, flush=True)
        out.append(s)
(HERE / "out" / "q1_negctl_large.txt").write_text("\n".join(out) + "\n")
