#!/usr/bin/env python3
"""R18: split the re-run of the engineering division's two checks into pieces WITHOUT changing their scripts.
A piece is one (job, n), and for n >= 2000 one (job, n, u), as a directory tree

    rerun_copy/chunks/<key>/experiments/eng/twolevel/{recheck_classification.py, nonproduct_bound.py, run_search.py}
    rerun_copy/chunks/<key>/experiments/eng/twolevel/results/x005_<job>.jsonl      (only the lines of the piece)
    rerun_copy/chunks/<key>/src -> ../../src                                        (their package + the R18 adapter)

with <key> = <job>_n<n> or <job>_n<n>_u<u>, so that their scripts, which read `results/x005_<job>.jsonl` beside
themselves and import `ROOT/src`, run verbatim.            usage: python3 -I -B r18_make_chunks.py"""
import json, os, shutil, resource
from pathlib import Path
HERE = Path(__file__).resolve().parent
COPY = HERE / "rerun_copy"
SRC = COPY / "experiments" / "eng" / "twolevel"
made = []
for job in ("cost", "claims", "converge", "converge2"):
    groups = {}
    for line in (SRC / "results" / f"x005_{job}.jsonl").read_text().splitlines():
        if line.strip():
            c = json.loads(line)
            key = f"{job}_n{c['n']}" if c["n"] < 2000 else f"{job}_n{c['n']}_u{c['u']:g}"
            groups.setdefault((c["n"], c["u"] if c["n"] >= 2000 else 0.0, key), []).append(line)
    for (n, u, key), ls in sorted(groups.items()):
        d = COPY / "chunks" / key / "experiments" / "eng" / "twolevel"
        (d / "results").mkdir(parents=True, exist_ok=True)
        for f in ("recheck_classification.py", "nonproduct_bound.py", "run_search.py"):
            shutil.copy2(SRC / f, d / f)
        (d / "results" / f"x005_{job}.jsonl").write_text("\n".join(ls) + "\n")
        link = COPY / "chunks" / key / "src"
        if not link.is_symlink():
            os.symlink(os.path.join("..", "..", "src"), link)
        made.append((key, len(ls), sum(len(json.loads(x)["searches"]) for x in ls)))
for m in made:
    print("chunk %-22s cells=%3d searches=%4d" % m)
print("chunks:", len(made), " searches in all:", sum(m[2] for m in made))
print("peak RSS MB: %.1f" % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024))
