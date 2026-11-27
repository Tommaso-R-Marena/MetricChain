#!/usr/bin/env python3
"""scan_sensitive.py - scan `consolidated/` for credentials, personal data and local paths before publication.

    python3 consolidated/11_reproducibility/scan_sensitive.py [--show]

Prints one line per finding (file, line number, pattern name); with --show also the matching text with the
middle masked.  Extra literal strings to search for (for instance a workspace name or an address that must not
appear) are read, one per line, from the file named by the environment variable SCAN_EXTRA_FILE and are never
printed.  Exit status 1 if a pattern of the class 'credential' or 'extra' matched.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONS = os.path.dirname(HERE)
PATTERNS = [
    ("credential", "anthropic-key", r"sk-ant-[A-Za-z0-9_\-]{16,}"),
    ("credential", "openai-style-key", r"\bsk-[A-Za-z0-9]{32,}\b"),
    ("credential", "modal-token", r"\b(?:ak|as)-[A-Za-z0-9]{18,}\b"),
    ("credential", "github-token", r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b|\bgithub_pat_[A-Za-z0-9_]{30,}\b"),
    ("credential", "huggingface-token", r"\bhf_[A-Za-z0-9]{30,}\b"),
    ("credential", "aws-key", r"\bAKIA[0-9A-Z]{16}\b"),
    ("credential", "google-key", r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    ("credential", "slack-token", r"\bxox[baprs]-[A-Za-z0-9\-]{10,}"),
    ("credential", "private-key-block", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("credential", "secret-assignment", r"(?i)\b(?:passphrase|password|passwd|secret|api[_-]?key|token|salt)\b\s*[:=]\s*[\"']?[A-Za-z0-9+/_\-]{20,}"),
    ("personal", "email", r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"),
    ("path", "home-directory", r"/home/[A-Za-z0-9._\-]+|/Users/[A-Za-z0-9._\-]+|[A-Z]:\\Users\\|/mnt/[a-z]/Users"),
    ("service", "modal-url", r"modal\.com/apps/[A-Za-z0-9_\-]+|[A-Za-z0-9\-]+--[A-Za-z0-9\-]+\.modal\.run"),
]
EMAIL_OK = re.compile(r"(?i)noreply@anthropic\.com|@example\.(com|org)|git@github\.com|@v\d|@[0-9a-f]{7,}$|\.(py|md|json|txt|lean|tsr|npz)$")
BINARY_EXT = {".npy", ".npz", ".pkl", ".tsr", ".enc", ".png", ".jpg", ".pdf", ".gz", ".zip"}


def main():
    show = "--show" in sys.argv
    extra = []
    if os.environ.get("SCAN_EXTRA_FILE"):
        extra = [l.strip() for l in open(os.environ["SCAN_EXTRA_FILE"], encoding="utf-8") if l.strip()]
    comp = [(c, n, re.compile(r)) for c, n, r in PATTERNS]
    bad = 0
    counts = {}
    nfiles = 0
    for dp, dn, fn in os.walk(CONS):
        dn.sort()
        for f in sorted(fn):
            path = os.path.join(dp, f)
            rel = os.path.relpath(path, CONS)
            if os.path.splitext(f)[1].lower() in BINARY_EXT:
                continue
            try:
                text = open(path, "rb").read().decode("utf-8", "replace")
            except OSError:
                continue
            nfiles += 1
            low = text.lower()
            for k, e in enumerate(extra):
                if e.lower() in low:
                    bad += 1
                    counts["extra"] = counts.get("extra", 0) + 1
                    ln = low[: low.index(e.lower())].count("\n") + 1
                    print("EXTRA[%d]  %s:%d" % (k, rel, ln))
            for cls, name, rx in comp:
                for m in rx.finditer(text):
                    s = m.group(0)
                    if name == "email" and EMAIL_OK.search(s):
                        continue
                    counts[name] = counts.get(name, 0) + 1
                    if cls == "credential":
                        bad += 1
                    ln = text[: m.start()].count("\n") + 1
                    masked = s if cls != "credential" else s[:6] + "…" + s[-2:]
                    print("%-10s %-18s %s:%d%s" % (cls, name, rel, ln, "   " + masked[:90] if show else ""))
    print("scanned %d text files; findings: %s" % (nfiles, ", ".join("%s %d" % kv for kv in sorted(counts.items())) or "none"))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
