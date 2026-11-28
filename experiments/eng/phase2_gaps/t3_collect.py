"""T3: feed the timestamped logs of t3_run_kernel.py to engineering's collect.py (unchanged).

    python experiments/eng/phase2_gaps/t3_collect.py --dir <token dir> --out results/kernel_v2.json LOG [LOG ...]

Strips the leading seconds from every line into a temporary clean log (what collect.py expects: the program's own
stdout), runs ``collect.main`` on those, then adds the timing per token file taken from the timestamps (see the comment in
main: the output arrives one block per token file, at the end of that file).
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "sb_review" / "lean_kernel"))
import collect  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("logs", type=Path, nargs="+")
    args = ap.parse_args()
    timing = {}
    with tempfile.TemporaryDirectory() as td:
        clean = []
        for log in args.logs:
            lines = [ln for ln in log.read_text().splitlines() if ln and not ln.startswith("#")]
            stamped = []
            for ln in lines:
                t, _, rest = ln.strip().partition(" ")
                stamped.append((float(t), rest))
            p = Path(td) / log.name
            p.write_text("\n".join(r for _, r in stamped) + "\n")
            clean.append(p)
            # Observed: the program's output reaches the pipe one block per token file, when that file is finished, so
            # the stamp of a block is the END of its file.  wall_s of a file = its stamp minus the previous block's
            # stamp; for the first file of a run it is None and the stamp (load + first file) is reported instead.
            ends = [(t, r.split()[1][: -len(".tokens")]) for t, r in stamped if r.startswith("file ")]
            for idx, (t, name) in enumerate(ends):
                timing[name] = dict(first_block_s=ends[0][0], wall_s=round(t - ends[idx - 1][0], 1) if idx else None, log=log.name)
            for t, r in stamped:
                if r.startswith("timeout"):
                    timing.setdefault(r.split()[1], {})["timeout"] = True
        sys.argv = ["collect.py", "--dir", str(args.dir), "--logs", *map(str, clean), "--out", str(args.out)]
        collect.main()
    rows = json.loads(args.out.read_text())
    for r in rows:
        r["timing"] = timing.get(r["name"])
    args.out.write_text(json.dumps(rows, indent=1))
    print(json.dumps(timing, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
