"""T1 negative controls on one certificate (v2/1CRN): each checker must refuse
  (a) the claimed lower bound raised by one unit (2^-(scale_bits+message_bits) kcal/mol),
  (b) the correct certificate against tables with one entry changed (checksum no longer matches; for the replay alone
      the change is to an entry the witness uses, lowered by one unit, so the bound is above the witness energy).

    <python> experiments/eng/phase2_gaps/t1_controls.py --tables T.npz --cert C.json --sb <sb-worktree> --scratch DIR
Prints JSON lines (the output of t1_check.py for each altered input).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tables", type=Path, required=True)
    ap.add_argument("--cert", type=Path, required=True)
    ap.add_argument("--sb", type=Path, required=True)
    ap.add_argument("--scratch", type=Path, required=True)
    args = ap.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    text = args.cert.read_text()
    doc = json.loads(text)
    L = doc["claim"]["lower_bound"]
    raised = re.sub(r'"lower_bound":\s*-?\d+', f'"lower_bound": {L + 1}', text, count=1)
    assert json.loads(raised)["claim"]["lower_bound"] == L + 1
    c_raised = args.scratch / "control_raised.mincert.json"
    c_raised.write_text(raised)
    w = doc["claim"]["witness"]
    with np.load(args.tables) as z:
        arrays = {k: z[k].copy() for k in z.files}
    arrays["u0"][w[0]] -= 1                     # one unary entry used by the witness, lowered by one table unit
    t_alt = args.scratch / "control_tables_altered.npz"
    np.savez_compressed(t_alt, **arrays)
    for label, tables, cert in (("claim raised by one unit", args.tables, c_raised),
                                ("one table entry used by the witness lowered by one unit", t_alt, args.cert)):
        for ck in ("files", "indep", "sb"):
            out = subprocess.run([sys.executable, str(HERE / "t1_check.py"), "--checker", ck, "--tables", str(tables),
                                  "--cert", str(cert), "--sb", str(args.sb)], capture_output=True, text=True, timeout=1200)
            r = json.loads(out.stdout)
            keep = {k: r.get(k) for k in ("checker", "accepted", "replay_accepted", "reason", "checksum_matches_certificate",
                                          "file_checksum_matches_tables", "proves", "claimed_lower_bound")}
            print(json.dumps(dict(control=label, **keep)), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
