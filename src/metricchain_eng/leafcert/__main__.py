"""Command line of the exact checker for "shares at the leaves" certificates.

    PYTHONPATH=src python -m metricchain_eng.leafcert [--engine c|python|both] FILE.json ...
    PYTHONPATH=src python -m metricchain_eng.leafcert --encode FILE.json > FILE.txt

The first form prints one line per file and engine; the exit status is 0 if every file is accepted (by
both engines with identical results when ``--engine both``, the default), 1 otherwise.  The second form
writes the text that the stand-alone C checker reads (``leafcert FILE.txt``, see the header of
``leafcert.c``) after the strict loader has accepted the file.
"""
from __future__ import annotations

import argparse
import sys

from . import check, loader


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m metricchain_eng.leafcert", description=__doc__.split("\n")[0])
    parser.add_argument("--engine", choices=("c", "python", "both"), default="both")
    parser.add_argument("--encode", action="store_true", help="write the text encoding of one file to standard output")
    parser.add_argument("files", nargs="+")
    args = parser.parse_args(argv)
    if args.encode:
        if len(args.files) != 1:
            parser.error("--encode takes exactly one file")
        try:
            sys.stdout.buffer.write(loader.encode(loader.validate(loader.load(args.files[0]))))
        except loader.FormatError as exc:
            print(f"{args.files[0]}: not a well-formed certificate: {exc}", file=sys.stderr)
            return 1
        return 0
    engines = ("c", "python") if args.engine == "both" else (args.engine,)
    status = 0
    for name in args.files:
        results = [check(name, engine) for engine in engines]
        for result in results:
            line = f"{name}: [{result.engine}] {result.verdict.upper()}"
            if result.accepted:
                c = result.counts
                line += (f" bound={result.bound} leaf_certificates={c['leaf_certificates']} leaf_boxes={c['leaf_boxes']}"
                         f" depth={c['depth']} integers={c['cert_integers']} additions={c['additions']}"
                         f" comparisons={c['comparisons']}")
            else:
                line += f" ({result.kind}) {result.reason}"
                status = 1
            print(line)
        for note in results[0].notes:
            print(f"{name}: note (annotation, not part of the verdict): {note}")
        same = {key: value for key, value in results[0].to_dict().items() if key not in ("engine", "reason")}
        if any(same != {key: value for key, value in r.to_dict().items() if key not in ("engine", "reason")}
               for r in results[1:]):
            print(f"{name}: THE TWO ENGINES DISAGREE")
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())
