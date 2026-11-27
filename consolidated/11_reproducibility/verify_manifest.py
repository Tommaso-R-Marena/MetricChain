#!/usr/bin/env python3
"""verify_manifest.py - check a copy of `consolidated/` against its MANIFEST.json.

    python3 consolidated/11_reproducibility/verify_manifest.py [--git]

Recomputes the SHA-256 of every file the manifest lists (imported artifacts and the archive's own index
files), and reports files that are missing, altered, or present without being listed.  With --git, and
inside a clone that has the eight division branches, it also checks that every imported artifact is the
same git object as the file at its original path in the pinned commit.  Standard library only.
Exit status 0 if everything matches.
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONS = os.path.dirname(HERE)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    m = json.load(open(os.path.join(CONS, "MANIFEST.json"), encoding="utf-8"))
    listed = {}
    for a in m["artifacts"] + m["archive_files"]:
        listed[a["archive_path"]] = a
    bad = []
    for ap, a in sorted(listed.items()):
        path = os.path.join(CONS, *ap.split("/"))
        if not os.path.isfile(path):
            bad.append(("missing", ap))
        elif os.path.getsize(path) != a["bytes"] or sha256(path) != a["sha256"]:
            bad.append(("altered", ap))
    present = set()
    for dp, dn, fn in os.walk(CONS):
        for f in fn:
            present.add(os.path.relpath(os.path.join(dp, f), CONS).replace(os.sep, "/"))
    for ap in sorted(present - set(listed) - {"MANIFEST.json"}):
        bad.append(("not listed", ap))
    if "--git" in sys.argv:
        root = os.path.dirname(CONS)
        for a in m["artifacts"]:
            r = subprocess.run(["git", "-C", root, "rev-parse", "%s:%s" % (a["pinned_commit"], a["original_path"])],
                               capture_output=True, text=True)
            if r.returncode != 0 or r.stdout.strip() != a["git_blob"]:
                bad.append(("differs from the pinned commit", a["archive_path"]))
    for kind, ap in bad[:200]:
        print("%-32s %s" % (kind, ap))
    t = m["totals"]
    print("%d imported artifacts and %d index files listed; %d problems%s" % (
        len(m["artifacts"]), len(m["archive_files"]), len(bad), "" if not bad else " (first 200 shown)"))
    print("division heads: " + ", ".join("%s %s" % (d["key"], d["pinned_commit"][:12]) for d in m["divisions"]))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
