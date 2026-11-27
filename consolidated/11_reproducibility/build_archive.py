#!/usr/bin/env python3
"""build_archive.py - assemble `consolidated/` from pinned commits of the eight MetricChain division branches.

An administrative tool.  It copies files byte for byte out of git objects, records provenance and
checksums, and writes mechanical indexes.  It evaluates no mathematics, runs no code of any division,
opens no sealed file, and uses the standard library only.

    python3 consolidated/11_reproducibility/build_archive.py

run from a checkout of the branch `research/consolidated-archive` inside a clone that also has the
eight pinned commits listed in `pins.json` (fetch all branches of the repository first).

What it does
  1. For every division: lists the tree of the pinned commit; keeps the files the division *owns*
     (theory: the whole tree; every other division: the files added or modified relative to the
     merge-base of its pinned commit with the pinned theory commit); writes each kept file to
     `consolidated/<NN_division>/<original repository path>`.
  2. Leaves out, and records with path, commit, git object id and (where the file may be read) SHA-256:
     sealed evaluation material named in `pins.json` (never read, not even to hash it), files larger
     than 5 MiB, caches and build products.
  3. Writes `MANIFEST.json`, one `00_DIVISION_INDEX.md` per division, the mailbox index and the
     cross-reference table of `09_cross_divisional_dependencies/`, and the tables of
     `11_reproducibility/`; fills the `<!-- GEN:name -->` blocks of the hand-written index files.
The output is a function of `pins.json` and of the hand-written files alone (no clock, no randomness).
"""
import collections
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CONS = os.path.join(ROOT, "consolidated")
REPO_URL = "https://github.com/Tommaso-R-Marena/MetricChain"
ARCHIVE_BRANCH = "research/consolidated-archive"
LARGE = 5 * 1024 * 1024

DIVS = [
    ("theory", "01_theory", "Theoretical Research Division"),
    ("engineering", "02_engineering", "Computational Research Division (engineering)"),
    ("science", "03_scientific_translation", "Scientific Discovery, Translation & Independent Validation Division"),
    ("ensemble", "04_ensemble_identifiability", "Ensemble Identifiability and Certified Inference Division"),
    ("geometry", "05_geometric_inference", "Geometric Inference, Rigidity and Inverse Problems Division"),
    ("complexity", "06_biological_complexity", "Mathematical Biology and Computational Complexity Division"),
    ("structbio", "07_structural_biology", "Structural & Computational Biology, Software Development and Applications Division"),
    ("frontier", "08_frontier_benchmarking", "Frontier Benchmarking, Experimental Evidence and Scientific Evaluation Division"),
]
DIRS = {k: d for k, d, _ in DIVS}
TITLES = {k: t for k, _, t in DIVS}
ID_PREFIX = {"THY": "theory", "ENG": "engineering", "SCI": "science", "ENSEMBLE": "ensemble",
             "GEOMETRY": "geometry", "COMPLEXITY": "complexity", "STRUCTBIO": "structbio", "FRONTIER": "frontier"}
ID_RE = re.compile(r"\b(THY|ENG|SCI|ENSEMBLE|GEOMETRY|COMPLEXITY|STRUCTBIO|FRONTIER)-(MSG|REQ|RES|REV|FRZ)-(\d{4})\b")

TEXT_EXT = {".md", ".txt", ".py", ".lean", ".json", ".jsonl", ".log", ".out", ".stdout", ".sh", ".c", ".cpp",
            ".h", ".csv", ".tsv", ".toml", ".cfg", ".ini", ".yml", ".yaml", ".diff", ".tokens", ".sing", ".m2", ""}
CODE_EXT = {".py", ".sh", ".c", ".cpp", ".h", ".sing", ".m2", ".jl", ".sage"}
CACHE_RE = re.compile(r"(^|/)(__pycache__|\.lake|\.pytest_cache|\.mypy_cache|\.ipynb_checkpoints|node_modules)(/|$)"
                      r"|\.(pyc|pyo|olean|ilean|o|so|a|class)$")

CLASS_LEGEND = collections.OrderedDict([
    ("consolidation-report", "the division's own critical assessment written under the consolidation directive"),
    ("mathematical-report", "theorem statements, definitions, proofs, workstream reports and research notes"),
    ("lean-proof", "Lean 4 source (formal statements and proofs)"),
    ("theorem-register", "registers of statements, proof obligations, experiments or improvements, with their status"),
    ("referee-report", "internal AI referee reports and reviews kept as documents"),
    ("mailbox-review", "reviews with replication sent through the collaboration mailbox"),
    ("mailbox-message", "messages between divisions"),
    ("mailbox-request", "requests between divisions"),
    ("mailbox-response", "responses between divisions"),
    ("mailbox-other", "other files of a mailbox directory (templates, placeholders, notes)"),
    ("status-or-digest", "status tables, digests to other divisions, synchronisation logs, mailbox rules"),
    ("cross-division-intake", "a division's written reading of the other divisions' work"),
    ("prior-art", "prior-art and literature assessments"),
    ("assumption-audit", "assumption audits and registers"),
    ("negative-results", "dead ends, withdrawn claims, negative results"),
    ("open-problems", "open problems, publication opportunities, frontier maps"),
    ("handoff-or-log", "research logs, handoff documents, plans, READMEs"),
    ("owner-directives", "the research owner's directives as recorded by a division"),
    ("benchmark-or-evaluation-record", "benchmark plans, protocols, registries, results, ledgers, verification reports"),
    ("software-documentation", "interfaces, formats and implementation guides"),
    ("workstream-brief", "briefs given to subagents (what a workstream or referee was asked to do)"),
    ("source-code", "packages, job drivers and repository scripts"),
    ("test", "test suites"),
    ("experiment-script", "scripts of experiments, checks and reviews"),
    ("experiment-report", "reports and READMEs stored with experiments"),
    ("certificate", "certificate files and conformance vectors"),
    ("stored-result", "stored outputs and raw results of computations"),
    ("evaluation-freeze", "frozen evaluation records: manifests, commitments, time-stamp tokens, frozen scores"),
    ("input-data", "public input structures and test data"),
    ("build-config", "toolchain and dependency pins, ignore files"),
    ("other", "anything else"),
])
EV = collections.OrderedDict([
    ("formal-lean-source", "Lean 4 source: machine-checkable; whether it builds, and on which axioms, is what the division's own audit documents (quoted in the division index)"),
    ("paper-proof-or-statement", "statements and paper proofs written by AI sessions; inside the document the division's labels separate machine-checked, "
                                 "proved, numerical and conjectural items; not externally reviewed"),
    ("internal-ai-review", "internal AI review (by a subagent of the division or by another division); not external peer review"),
    ("prior-art-assessment", "an AI session's assessment of externally established results; reading depth as stated in the document"),
    ("computational-evidence", "exact or numerical computation, code and stored output, as the producing division states; regenerable where it says how"),
    ("external-public-data", "externally established public data, copied unchanged by the division"),
    ("administrative-record", "administrative or communication record; claims in it have the status of the documents they cite"),
])
EVIDENCE = collections.defaultdict(lambda: "administrative-record", {
    "lean-proof": "formal-lean-source", "mathematical-report": "paper-proof-or-statement", "consolidation-report": "paper-proof-or-statement",
    "theorem-register": "paper-proof-or-statement", "open-problems": "paper-proof-or-statement", "software-documentation": "paper-proof-or-statement",
    "referee-report": "internal-ai-review", "mailbox-review": "internal-ai-review", "assumption-audit": "internal-ai-review",
    "cross-division-intake": "internal-ai-review", "prior-art": "prior-art-assessment",
    "stored-result": "computational-evidence", "experiment-script": "computational-evidence", "experiment-report": "computational-evidence",
    "certificate": "computational-evidence", "test": "computational-evidence", "source-code": "computational-evidence",
    "evaluation-freeze": "computational-evidence", "benchmark-or-evaluation-record": "computational-evidence",
    "input-data": "external-public-data",
})


def git(*args, data=None):
    return subprocess.run(["git", "-C", ROOT, "-c", "core.quotePath=false", *args], input=data, check=True,
                          capture_output=True).stdout


def utc(epoch):
    return datetime.datetime.fromtimestamp(int(epoch), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ls_tree(commit):
    out = {}
    for rec in git("ls-tree", "-r", "-l", "-z", commit).decode("utf-8", "surrogateescape").split("\0"):
        if rec:
            meta, path = rec.split("\t", 1)
            mode, typ, sha, size = meta.split()
            out[path] = (mode, typ, sha, int(size) if size != "-" else 0)
    return out


def last_change(commit, base):
    """path -> (commit, date) of the newest commit in base..commit (all history if base is None) that touched it."""
    rng = commit if base is None else base + ".." + commit
    seen, cur = {}, None
    for line in git("log", "--format=@@%H %ct", "--name-only", rng).decode("utf-8", "surrogateescape").splitlines():
        if line.startswith("@@"):
            h, ct = line[2:].split()
            cur = (h, utc(ct))
        elif line and cur and line not in seen:
            seen[line] = cur
    return seen


class Cat:
    def __init__(self):
        self.p = subprocess.Popen(["git", "-C", ROOT, "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def get(self, sha):
        self.p.stdin.write(sha.encode() + b"\n")
        self.p.stdin.flush()
        head = self.p.stdout.readline().split()
        assert head[1] == b"blob", head
        n = int(head[2])
        data = self.p.stdout.read(n)
        self.p.stdout.read(1)
        return data

    def close(self):
        self.p.stdin.close()
        self.p.wait()


def classify(p):
    b = os.path.basename(p)
    ext = os.path.splitext(b)[1].lower()
    up = b.upper()
    if p.startswith("docs/collaboration/consolidation/"):
        return "consolidation-report"
    if re.match(r"docs/collaboration/(messages|requests|responses)/", p):
        for tag, cls in (("-REV-", "mailbox-review"), ("-MSG-", "mailbox-message"), ("-REQ-", "mailbox-request"),
                         ("-RES-", "mailbox-response")):
            if re.search(tag + r"\d{4}", b):
                return cls
        return "mailbox-other"
    if p.startswith("docs/collaboration/"):
        return "status-or-digest"
    if ext == ".lean":
        return "lean-proof"
    if p.startswith("experiments/frontier/freezes/"):
        return "evaluation-freeze"
    if p.startswith("benchmarks/") or p.startswith("tests/frontier/data/"):
        return "input-data"
    if b in ("lakefile.lean", "lakefile.toml", "lean-toolchain", "lake-manifest.json", ".gitignore", "pyproject.toml",
             "setup.cfg", "setup.py") or re.match(r"requirements.*\.txt$", b):
        return "build-config"
    if p.startswith("docs/"):
        if ext in CODE_EXT:
            return "experiment-script"
        if ext != ".md":
            return "stored-result"
        if b.lower().endswith("brief.md"):
            return "workstream-brief"
        if "/intake/" in p or up == "RESEARCH_INTAKE.MD":
            return "cross-division-intake"
        if p.startswith("docs/audit/") or "ASSUMPTION" in up:
            return "assumption-audit"
        if "/reviews/" in p or "REVIEW" in up or "REFEREE" in up or re.match(r"docs/science/workstreams/R\d+_", p):
            return "referee-report"
        if p.startswith("docs/prior_art/") or "PRIOR_ART" in up or "STATE_OF_THE_ART" in up or "/literature/" in p \
                or re.match(r"docs/science/workstreams/A\d+_REPORT", p):
            return "prior-art"
        if "DEAD_ENDS" in up or "NEGATIVE_RESULTS" in up:
            return "negative-results"
        if up in ("THEOREM_REGISTER.MD", "THEOREMS.MD", "BLUEPRINT.MD", "THEOREM_TO_SOFTWARE_REGISTER.MD",
                  "PROOF_OBLIGATIONS.MD", "OPEN_OBLIGATIONS.MD", "EXPERIMENT_REGISTER.MD", "IMPROVEMENT_REGISTER.MD"):
            return "theorem-register"
        if "OPEN_PROBLEMS" in up or "PUBLICATION_OPPORTUNITIES" in up or "FRONTIER_MAP" in up:
            return "open-problems"
        if "DIRECTIVES" in up:
            return "owner-directives"
        if "BENCHMARK" in up or "/protocols/" in p or up in (
                "ASSESSMENT_PROTOCOLS.MD", "PREDICTION_FREEZE.MD", "PREDICTION_FREEZE_REGISTER.MD", "CASP17_ASSESSMENT.MD",
                "RESULTS.MD", "COMPUTE_LEDGER.MD", "BASELINE_SPECIFICATIONS.MD", "BASELINE_REGISTER.MD",
                "CONTAMINATION_AUDIT.MD", "DATA_PROVENANCE.MD", "REPRODUCIBILITY.MD", "SOFTWARE_EVALUATION_PROTOCOL.MD",
                "VERIFICATION_REPORT.MD", "INDEPENDENT_VALIDATION.MD"):
            return "benchmark-or-evaluation-record"
        if up in ("SOFTWARE_INTERFACE.MD", "IMPLEMENTATION_GUIDE.MD", "SANDWICH_CERTIFICATE_FORMAT.MD", "ARCHITECTURE.MD"):
            return "software-documentation"
        if "RESEARCH_LOG" in up or up in ("HANDOFF.MD", "RESEARCH_SYNTHESIS.MD", "README.MD", "COMMON.MD", "RESEARCH_PLAN.MD",
                                          "DEPENDENCY_MAP.MD", "SCIENTIFIC_SYNTHESIS.MD"):
            return "handoff-or-log"
        return "mathematical-report"
    if p.startswith("src/") or p.startswith("modal_jobs/") or p.startswith("scripts/"):
        return "source-code"
    if p.startswith("tests/"):
        return "test"
    if p.startswith("experiments/"):
        if ext in CODE_EXT:
            return "experiment-script"
        if ext == ".md":
            return "experiment-report"
        if p.startswith("experiments/certs/") or (ext == ".json" and "cert" in b.lower()):
            return "certificate"
        return "stored-result"
    if "/" not in p and ext == ".md":
        return "handoff-or-log"
    return "other"


def md_title(text):
    m = re.search(r"^#{1,3}\s+(.+?)\s*$", text, re.M)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def lean_stats(text):
    body = re.sub(r"/-.*?-/", " ", text, flags=re.S)
    body = re.sub(r"--[^\n]*", " ", body)
    imports = re.findall(r"^import\s+(\S+)", text, re.M)
    local = [i for i in imports if not re.match(r"(Mathlib|Lean|Std|Batteries|Aesop|Init|Qq|ProofWidgets|Plausible|LeanSearchClient|ImportGraph)(\.|$)", i)]
    return {"lines": text.count("\n") + (0 if text.endswith("\n") or not text else 1),
            "sorry_outside_comments": len(re.findall(r"\bsorry\b", body)),
            "axiom_declarations": len(re.findall(r"^\s*(?:private\s+|protected\s+)?axiom\s", body, re.M)),
            "theorem_or_lemma_declarations": len(re.findall(r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*(?:theorem|lemma)\s", body, re.M)),
            "project_imports": local}


def mailbox_meta(text):
    head = text[:8000]

    def field(name):
        m = re.search(r"^%s\s*:[ \t]*(.*(?:\n[ \t]{6,}\S.*)*)" % name, head, re.M)
        return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    d = re.search(r"20\d\d-\d\d-\d\d[ T]\d\d:\d\d", field(r"Date and time \(UTC\)") or head)
    return {"from": field("From"), "to": field("To"), "date_utc": d.group(0).replace("T", " ") if d else "",
            "type": field("(?:Message|Request|Response) type"), "status": field("Status"),
            "related_ids_field": field(r"Related message/request IDs")}


def mib(n):
    return "%.2f" % (n / 1048576.0)


def cell(s, n=None):
    s = re.sub(r"\s+", " ", str(s)).replace("|", "\\|")
    return s if n is None or len(s) <= n else s[: n - 1] + "…"


def main():
    pins = json.load(open(os.path.join(HERE, "pins.json"), encoding="utf-8"))
    pd = pins["divisions"]
    theory_commit = pd["theory"]["commit"]
    sealed = {(k, p) for k, ps in pins.get("sealed_paths", {}).items() for p in ps}
    cat = Cat()
    artifacts, excluded, divinfo = [], [], collections.OrderedDict()
    texts = {}          # archive_path -> decoded text, for .md and .lean only (indexes)

    for key, dname, title in DIVS:
        commit = pd[key]["commit"]
        branch = pd[key]["branch"]
        tree = ls_tree(commit)
        if key == "theory":
            base, own = None, sorted(tree)
        else:
            base = git("merge-base", theory_commit, commit).decode().strip()
            own = sorted(p for p in git("diff", "--name-only", "-z", base, commit).decode("utf-8", "surrogateescape").split("\0")
                         if p and p in tree)
        lc = last_change(commit, base)
        ddir = os.path.join(CONS, dname)
        if os.path.isdir(ddir):
            shutil.rmtree(ddir)
        os.makedirs(ddir)
        n_in = b_in = n_ex = b_ex = 0
        for p in own:
            mode, typ, sha, size = tree[p]
            common = {"division": key, "branch": branch, "pinned_commit": commit, "original_path": p,
                      "git_blob": sha, "bytes": size}
            why = None
            if (key, p) in sealed:
                why = "sealed-evaluation-material"
            elif typ != "blob" or mode not in ("100644", "100755"):
                why = "not-a-regular-file (mode %s)" % mode
            elif CACHE_RE.search(p):
                why = "cache-or-build-product"
            elif size > LARGE:
                why = "larger-than-5-MiB"
            if why:
                rec = dict(common, reason=why,
                           retrieval="git show %s:%s > %s" % (commit, p, os.path.basename(p)))
                if why == "sealed-evaluation-material":
                    rec["sha256"] = None
                    rec["note"] = ("not read by the archive builder, not even to hash it; the passphrase and the "
                                   "commitment salt are held by the research owner outside the repository")
                elif typ == "blob":
                    rec["sha256"] = hashlib.sha256(cat.get(sha)).hexdigest()
                excluded.append(rec)
                n_ex += 1
                b_ex += size
                continue
            data = cat.get(sha)
            assert len(data) == size, p
            dst = os.path.join(ddir, p)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(os.fsencode(dst), "wb") as f:
                f.write(data)
            os.chmod(os.fsencode(dst), 0o755 if mode == "100755" else 0o644)
            cls = classify(p)
            ap = "%s/%s" % (dname, p)
            h, d = lc.get(p, (None, None))
            a = dict(common, archive_path=ap, sha256=hashlib.sha256(data).hexdigest(), mode=mode,
                     last_change_commit=h, last_change_date=d, **{"class": cls}, evidence=EVIDENCE[cls])
            ext = os.path.splitext(p)[1].lower()
            if ext in (".md", ".lean"):
                t = data.decode("utf-8", "replace")
                texts[ap] = t
                if ext == ".md":
                    a["title"] = md_title(t)
                else:
                    a["lean"] = lean_stats(t)
            artifacts.append(a)
            n_in += 1
            b_in += size
        ct = git("show", "-s", "--format=%ct", commit).decode().strip()
        info = {"key": key, "directory": dname, "title": title, "branch": branch, "pinned_commit": commit,
                "pinned_commit_date": utc(ct), "merge_base_with_theory": base,
                "merge_base_date": utc(git("show", "-s", "--format=%ct", base).decode().strip()) if base else None,
                "ownership_rule": ("the whole tree of the pinned commit" if key == "theory" else
                                   "files added or modified relative to the merge-base with the pinned theory commit"),
                "files_in_branch_tree": len(tree), "files_owned": len(own), "files_included": n_in,
                "bytes_included": b_in, "files_excluded": n_ex, "bytes_excluded": b_ex,
                "consolidation_report": "%s/%s" % (dname, pd[key]["consolidation_report"]),
                "status_registers": ["%s/%s" % (dname, r) for r in pd[key].get("registers", [])],
                "documented_verification": pd[key].get("documented_verification", ""),
                "documented_verification_source": pd[key].get("documented_verification_source", "")}
        divinfo[key] = info
    cat.close()

    apaths = {a["archive_path"] for a in artifacts}
    for info in divinfo.values():
        for r in [info["consolidation_report"]] + info["status_registers"]:
            assert r in apaths, "pins.json names a file that was not imported: " + r

    by_sha = collections.defaultdict(list)
    for a in artifacts:
        if a["bytes"] > 0:
            by_sha[a["sha256"]].append(a["archive_path"])
    for a in artifacts:
        same = [x for x in by_sha.get(a["sha256"], []) if x != a["archive_path"]]
        if same and a["bytes"] > 200:
            a["same_content_as"] = same[:12]
        if a["class"] == "lean-proof":
            a["verification"] = "Lean 4 source; text-scan counts in field 'lean'; audit status: divisions[].documented_verification"

    # ---------------------------------------------------------------- generated indexes
    gen = {}
    byd = collections.defaultdict(list)
    for a in artifacts:
        byd[a["division"]].append(a)

    def rel(a):
        return a["original_path"]

    for key, dname, title in DIVS:
        info, L = divinfo[key], []
        L += ["# %s — %s: index of imported artifacts" % (dname.split("_")[0], title), "",
              "*Generated by `11_reproducibility/build_archive.py`; do not edit.  Every file below this directory other than this "
              "index is a byte-for-byte copy of `%s` at the pinned commit; paths below this directory are the original repository paths.*" % info["branch"], "",
              "| | |", "|---|---|",
              "| branch | `%s` |" % info["branch"],
              "| pinned commit | `%s` (%s) |" % (info["pinned_commit"], info["pinned_commit_date"]),
              "| what was imported | %s%s |" % (info["ownership_rule"], "" if key == "theory" else " `%s` (%s)" % (info["merge_base_with_theory"][:12], info["merge_base_date"])),
              "| files | %d imported (%s MiB); %d left out by reference (%s MiB); the branch tree has %d files |" % (
                  info["files_included"], mib(info["bytes_included"]), info["files_excluded"], mib(info["bytes_excluded"]), info["files_in_branch_tree"]),
              "| formal verification, as the division documents it | %s  *(source: `%s`)* |" % (cell(info["documented_verification"]), info["documented_verification_source"]),
              "", "## Start here", "",
              "* The division's own critical assessment: [`%s`](%s)" % (pd[key]["consolidation_report"], pd[key]["consolidation_report"])]
        for r in pd[key].get("registers", []):
            L.append("* State of statements / results: [`%s`](%s)" % (r, r))
        for a in byd[key]:
            if a["class"] == "handoff-or-log" and a["original_path"].startswith("docs/") and "/workstreams/" not in a["original_path"] \
                    and os.path.basename(a["original_path"]).upper() not in ("README.MD", "COMMON.MD"):
                L.append("* Handoff / log: [`%s`](%s)" % (rel(a), rel(a)))
        L += ["", "## Files by class", "", "| class | files | MiB | meaning |", "|---|---:|---:|---|"]
        cc = collections.Counter()
        cb = collections.Counter()
        for a in byd[key]:
            cc[a["class"]] += 1
            cb[a["class"]] += a["bytes"]
        for c in CLASS_LEGEND:
            if cc[c]:
                L.append("| %s | %d | %s | %s |" % (c, cc[c], mib(cb[c]), CLASS_LEGEND[c]))
        docs = [a for a in byd[key] if a["original_path"].endswith(".md") and not a["class"].startswith("mailbox")
                and not a["original_path"].startswith("experiments/") and a["class"] != "workstream-brief"]
        L += ["", "## Documents (mailbox items, briefs and files under `experiments/` not listed)", "",
              "| class | file | title | kB |", "|---|---|---|---:|"]
        order = list(CLASS_LEGEND)
        for a in sorted(docs, key=lambda a: (order.index(a["class"]), a["original_path"])):
            L.append("| %s | [`%s`](%s) | %s | %d |" % (a["class"], rel(a), rel(a).replace(" ", "%20"), cell(a.get("title", ""), 120), round(a["bytes"] / 1024)))
        nb = sum(1 for a in byd[key] if a["class"] == "workstream-brief")
        nm = sum(1 for a in byd[key] if a["class"].startswith("mailbox"))
        L += ["", "Mailbox items of this division: %d, listed with dates and titles in "
              "[`../09_cross_divisional_dependencies/MAILBOX_INDEX.md`](../09_cross_divisional_dependencies/MAILBOX_INDEX.md).  "
              "Briefs to subagents: %d (class `workstream-brief` in `MANIFEST.json`)." % (nm, nb)]
        lean = [a for a in byd[key] if a["class"] == "lean-proof"]
        if lean:
            L += ["", "## Lean files", "",
                  "*Counts are a text scan of the source by the archive builder (comments removed), not a build.*", "",
                  "| file | lines | `theorem`/`lemma` | `sorry` | `axiom` | imports within the project |", "|---|---:|---:|---:|---:|---|"]
            for a in sorted(lean, key=rel):
                s = a["lean"]
                L.append("| [`%s`](%s) | %d | %d | %d | %d | %s |" % (rel(a), rel(a), s["lines"], s["theorem_or_lemma_declarations"],
                                                                 s["sorry_outside_comments"], s["axiom_declarations"],
                                                                 cell(", ".join(s["project_imports"]), 160)))
        tree_dirs = collections.OrderedDict()
        for a in byd[key]:
            parts = a["original_path"].split("/")
            if parts[0] in ("experiments", "src", "tests", "modal_jobs", "scripts", "benchmarks", "proofs"):
                k = "/".join(parts[:3]) if len(parts) > 3 else "/".join(parts[:-1]) or parts[0]
                e = tree_dirs.setdefault(k, [0, 0, collections.Counter()])
                e[0] += 1
                e[1] += a["bytes"]
                e[2][a["class"]] += 1
        if tree_dirs:
            L += ["", "## Code, proofs, experiments and stored results by directory", "",
                  "| directory | files | MiB | classes |", "|---|---:|---:|---|"]
            for k in sorted(tree_dirs):
                e = tree_dirs[k]
                L.append("| [`%s/`](%s) | %d | %s | %s |" % (k, k, e[0], mib(e[1]), ", ".join("%s %d" % kv for kv in e[2].most_common())))
        ex = [e for e in excluded if e["division"] == key]
        L += ["", "## Left out of the archive (retrievable at the pinned commit)", ""]
        if ex:
            L += ["| file | bytes | reason | git object | SHA-256 |", "|---|---:|---|---|---|"]
            for e in ex:
                L.append("| `%s` | %d | %s | `%s` | %s |" % (e["original_path"], e["bytes"], e["reason"], e["git_blob"],
                                                          "`%s`" % e["sha256"] if e.get("sha256") else "not computed (file not read)"))
            L += ["", "Retrieve with `git show <pinned commit>:<path> > <file>` in a clone of `%s`." % REPO_URL]
        else:
            L.append("Nothing: every file this division owns at the pinned commit is in the archive.")
        gen["%s/00_DIVISION_INDEX.md" % dname] = "\n".join(L) + "\n"

    # mailbox index and cross references
    mail = []
    for a in artifacts:
        if a["class"].startswith("mailbox") and a["class"] != "mailbox-other":
            m = ID_RE.search(os.path.basename(a["original_path"]))
            if not m:
                continue
            t = texts[a["archive_path"]]
            meta = mailbox_meta(t)
            mail.append(dict(meta, id=m.group(0), division=a["division"], archive_path=a["archive_path"],
                             title=a.get("title", ""), last_change_date=a["last_change_date"]))
    defined = {m["id"]: m["archive_path"] for m in mail}
    for a in artifacts:
        m = ID_RE.match(os.path.basename(a["original_path"]))
        if m and a["original_path"].endswith(".md"):
            defined.setdefault(m.group(0), a["archive_path"])
    cited_by = collections.defaultdict(set)
    matrix = collections.defaultdict(set)
    for ap, t in texts.items():
        if not ap.endswith(".md"):
            continue
        src_div = next(k for k, d in DIRS.items() if ap.startswith(d + "/"))
        own_id = ID_RE.search(os.path.basename(ap))
        for m in ID_RE.finditer(t):
            i = m.group(0)
            if own_id and i == own_id.group(0):
                continue
            cited_by[i].add(ap)
            matrix[(src_div, ID_PREFIX[m.group(1)])].add(i)
    xref = collections.OrderedDict()
    for i in sorted(set(defined) | set(cited_by)):
        xref[i] = {"defined_in": defined.get(i), "cited_by": sorted(cited_by.get(i, ()))}
    gen["09_cross_divisional_dependencies/CROSS_REFERENCES.json"] = json.dumps(
        {"note": "Mechanical: every identifier of the form <DIVISION>-(MSG|REQ|RES|REV|FRZ)-NNNN found in the imported Markdown files; "
                 "'defined_in' is the mailbox file with that name, null if no such file was imported (FRZ identifiers are freezes, "
                 "not mailbox files; an identifier may also be cited before or without being published).",
         "identifiers": xref}, indent=1, ensure_ascii=False) + "\n"
    L = ["# Mailbox index — every message, request, response and review of the eight divisions", "",
         "*Generated by `11_reproducibility/build_archive.py` from the header block and first heading of each mailbox file; do not edit.  "
         "Dates are the ones the authors wrote in the header (UTC); where a header has none, the commit date of the file's last change is given in brackets.*", "",
         "## Who cites whom", "",
         "Number of distinct mailbox identifiers of the column division that occur anywhere in the imported Markdown files of the row division "
         "(a count of citations, not a judgement of dependence; details per identifier in `CROSS_REFERENCES.json`).", "",
         "| documents of ↓ cite identifiers of → | " + " | ".join(k for k, _, _ in DIVS) + " |", "|---|" + "---:|" * len(DIVS)]
    for k, _, _ in DIVS:
        L.append("| %s | " % k + " | ".join(str(len(matrix.get((k, c), ()))) if k != c else "(%d)" % len(matrix.get((k, c), ())) for c, _, _ in DIVS) + " |")
    L += ["", "## Identifiers cited but not present as a mailbox file in the archive", ""]
    missing = [i for i in xref if not xref[i]["defined_in"] and "-FRZ-" not in i]
    L.append(", ".join("`%s` (%d files)" % (i, len(xref[i]["cited_by"])) for i in missing) if missing else "None.")
    L += ["", "## Items in order of date", "", "| date (UTC) | id | from | to | title | cited by (files) |", "|---|---|---|---|---|---:|"]

    def mkey(m):
        return (m["date_utc"] or (m["last_change_date"] or "").replace("T", " ")[:16], m["id"])
    for m in sorted(mail, key=mkey):
        date = m["date_utc"] or "[%s]" % (m["last_change_date"] or "?")[:16].replace("T", " ")
        L.append("| %s | [`%s`](../%s) | %s | %s | %s | %d |" % (date, m["id"], m["archive_path"], m["division"],
                                                               cell(m["to"], 70), cell(m["title"], 140), len(cited_by.get(m["id"], ()))))
    L += ["", "%d items: " % len(mail) + ", ".join("%s %d" % (k, sum(1 for m in mail if m["division"] == k)) for k, _, _ in DIVS) + "."]
    gen["09_cross_divisional_dependencies/MAILBOX_INDEX.md"] = "\n".join(L) + "\n"

    # reproducibility tables
    pins_rows = ["| # | division | branch | pinned commit | commit date (UTC) | merge-base with theory | files | MiB |",
                 "|---|---|---|---|---|---|---:|---:|"]
    for key, dname, title in DIVS:
        i = divinfo[key]
        pins_rows.append("| %s | %s | `%s` | `%s` | %s | %s | %d | %s |" % (
            dname[:2], title, i["branch"], i["pinned_commit"], i["pinned_commit_date"].replace("T", " ").replace("Z", ""),
            "—" if not i["merge_base_with_theory"] else "`%s`" % i["merge_base_with_theory"][:12], i["files_included"], mib(i["bytes_included"])))
    tot_n = sum(i["files_included"] for i in divinfo.values())
    tot_b = sum(i["bytes_included"] for i in divinfo.values())
    pins_rows.append("| | **all eight** | | | | | **%d** | **%s** |" % (tot_n, mib(tot_b)))
    blocks = {"pins": "\n".join(pins_rows)}
    blocks["status"] = pins.get("status", "")
    blocks["totals"] = ("%d files (%s MiB) imported from the eight branches; %d files (%s MiB) left out by reference; "
                        "heads pinned at %s." % (tot_n, mib(tot_b), len(excluded), mib(sum(e["bytes"] for e in excluded)), pins["pinned_at_utc"]))
    ex_rows = ["| division | file | bytes | reason | git object | SHA-256 |", "|---|---|---:|---|---|---|"]
    for e in excluded:
        ex_rows.append("| %s | `%s` | %d | %s | `%s` | %s |" % (e["division"], e["original_path"], e["bytes"], e["reason"], e["git_blob"],
                                                              "`%s`" % e["sha256"] if e.get("sha256") else "not computed (file not read)"))
    blocks["excluded"] = "\n".join(ex_rows)
    cc, cb = collections.Counter(), collections.Counter()
    for a in artifacts:
        cc[a["class"]] += 1
        cb[a["class"]] += a["bytes"]
    blocks["classes"] = "\n".join(["| class | files | MiB | meaning |", "|---|---:|---:|---|"] +
                                  ["| %s | %d | %s | %s |" % (c, cc[c], mib(cb[c]), CLASS_LEGEND[c]) for c in CLASS_LEGEND if cc[c]])
    lrows = ["| division | Lean files | lines | `theorem`/`lemma` | files containing `sorry` | `axiom` declarations |", "|---|---:|---:|---:|---:|---:|"]
    for key, dname, title in DIVS:
        ls = [a["lean"] for a in byd[key] if a["class"] == "lean-proof"]
        lrows.append("| %s | %d | %d | %d | %d | %d |" % (key, len(ls), sum(s["lines"] for s in ls), sum(s["theorem_or_lemma_declarations"] for s in ls),
                                                        sum(1 for s in ls if s["sorry_outside_comments"]), sum(s["axiom_declarations"] for s in ls)))
    blocks["lean"] = "\n".join(lrows)
    late = ["| date (UTC) | id | from | to | title |", "|---|---|---|---|---|"]
    for m in sorted(mail, key=mkey):
        when = m["date_utc"] or (m["last_change_date"] or "").replace("T", " ")[:16]
        outside = [c for c in cited_by.get(m["id"], ()) if not c.startswith(DIRS[m["division"]] + "/")]
        if when >= pins.get("late_messages_from", "2026-11-26 23:00") and not outside:
            late.append("| %s | [`%s`](../%s) | %s | %s | %s |" % (when, m["id"], m["archive_path"], m["division"], cell(m["to"], 90), cell(m["title"], 150)))
    blocks["unread"] = "\n".join(late)
    blocks["mail"] = "%d mailbox items (%s)" % (len(mail), ", ".join("%s %d" % (k, sum(1 for m in mail if m["division"] == k)) for k, _, _ in DIVS))

    L = ["# Pinned commits", "", "*Generated; do not edit.*  Repository: <%s>.  %s" % (REPO_URL, blocks["totals"]), "", blocks["pins"], "",
         "To obtain one division's complete tree (the archive holds only the files the division owns):", "", "```",
         "git clone %s.git && cd MetricChain" % REPO_URL, "git checkout <pinned commit>", "```", ""]
    gen["11_reproducibility/PINNED_COMMITS.md"] = "\n".join(L)
    L = ["# Artifacts left out of the archive", "", "*Generated; do not edit.*", "", blocks["excluded"], "",
         "Rules: sealed evaluation material is never copied and never read; files larger than 5 MiB, caches and build products are referenced, not copied.  "
         "Every file listed is unchanged in the repository and is retrieved with", "", "```",
         "git clone %s.git && cd MetricChain" % REPO_URL, "git show <pinned commit of the division>:<file> > <local name>", "sha256sum <local name>", "```", "",
         "Not part of any branch, and therefore not referenced here: untracked caches that divisions describe as regenerable "
         "(their reports say how), tool installations, and the credentials of the sealed list (held by the research owner)."]
    gen["11_reproducibility/EXCLUDED_ARTIFACTS.md"] = "\n".join(L) + "\n"
    L = ["# Lean files in the archive", "", "*Generated; do not edit.  A text scan of the sources (comments removed) — not a build and not an axiom audit.  "
         "What each division's own audit established is quoted in the division indexes and in `00_MASTER_INDEX.md`.*", "", blocks["lean"], "",
         "| division | file | lines | `theorem`/`lemma` | `sorry` | `axiom` | imports within the project |", "|---|---|---:|---:|---:|---:|---|"]
    for a in artifacts:
        if a["class"] == "lean-proof":
            s = a["lean"]
            L.append("| %s | [`%s`](../%s) | %d | %d | %d | %d | %s |" % (a["division"], a["original_path"], a["archive_path"], s["lines"], s["theorem_or_lemma_declarations"],
                                                                    s["sorry_outside_comments"], s["axiom_declarations"], cell(", ".join(s["project_imports"]), 150)))
    gen["11_reproducibility/LEAN_FILES.md"] = "\n".join(L) + "\n"

    for relp, content in gen.items():
        dst = os.path.join(CONS, relp)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)

    # GEN blocks of the hand-written files
    hand = []
    for dp, dn, fn in os.walk(CONS):
        for f in fn:
            ap = os.path.relpath(os.path.join(dp, f), CONS).replace(os.sep, "/")
            if ap in apaths or ap == "MANIFEST.json":
                continue
            hand.append(ap)
            if ap in gen or not ap.endswith(".md"):
                continue
            path = os.path.join(CONS, ap)
            s = open(path, encoding="utf-8").read()

            def sub(m):
                name = m.group(1)
                if name not in blocks:
                    sys.exit("unknown GEN block %s in %s" % (name, ap))
                return "<!-- GEN:%s -->\n%s\n<!-- /GEN:%s -->" % (name, blocks[name], name)
            s2 = re.sub(r"<!-- GEN:(\w+) -->.*?<!-- /GEN:\1 -->", sub, s, flags=re.S)
            if s2 != s:
                with open(path, "w", encoding="utf-8", newline="\n") as f2:
                    f2.write(s2)

    archive_files = []
    for ap in sorted(hand):
        data = open(os.path.join(CONS, ap), "rb").read()
        archive_files.append({"archive_path": ap, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                              "class": "archive-index (generated by build_archive.py)" if ap in gen else "archive-index or tool (written for this archive)"})

    def line(o):
        return json.dumps(o, ensure_ascii=False, sort_keys=True)
    head = collections.OrderedDict([
        ("schema", "metricchain-consolidated-archive/1"),
        ("source_repository", REPO_URL),
        ("archive_branch", ARCHIVE_BRANCH),
        ("division_heads_pinned_at_utc", pins["pinned_at_utc"]),
        ("status", pins.get("status", "")),
        ("checksums", "sha256 = SHA-256 of the file's bytes; git_blob = git object id of the same bytes (identical to the id in the source branch)"),
        ("path_rule", "archive_path = <division directory>/<original_path>, relative to consolidated/"),
        ("ownership_rule", "theory: the whole tree of its pinned commit; every other division: files added or modified relative to the "
                           "merge-base of its pinned commit with the pinned theory commit (files a division merely inherited are not copied twice)"),
        ("exclusion_rules", ["sealed evaluation material (listed in pins.json): never copied, never read",
                             "files larger than 5 MiB: referenced with path, commit, git object id and SHA-256",
                             "caches and build products: referenced, not copied",
                             "nothing was edited, redacted or renamed"]),
        ("evidence_legend", dict(EV, note="the 'evidence' field of an artifact is assigned by file class, mechanically; conjectures are not a file "
                                             "class - they are labelled inside the documents; the status of an individual statement is what the "
                                             "division's register (field 'verification') and the master index say")),
        ("verification_rule", "per division: divisions[].documented_verification quotes the division's own statement of what is machine-checked, and "
                              "divisions[].status_registers are the files that give the status of every statement or result; per artifact: Lean files "
                              "carry text-scan counts (not a build); no status was assigned by the archive builder"),
        ("class_legend", CLASS_LEGEND),
        ("totals", {"files_imported": tot_n, "bytes_imported": tot_b, "files_excluded": len(excluded),
                    "bytes_excluded": sum(e["bytes"] for e in excluded), "archive_index_files": len(archive_files)}),
    ])
    out = json.dumps(head, indent=1, ensure_ascii=False)[:-2] + ",\n"
    out += ' "divisions": [\n' + ",\n".join("  " + line(i) for i in divinfo.values()) + "\n ],\n"
    out += ' "artifacts": [\n' + ",\n".join("  " + line(a) for a in artifacts) + "\n ],\n"
    out += ' "excluded": [\n' + ",\n".join("  " + line(e) for e in excluded) + "\n ],\n"
    out += ' "archive_files": [\n' + ",\n".join("  " + line(a) for a in archive_files) + "\n ]\n}\n"
    json.loads(out)
    with open(os.path.join(CONS, "MANIFEST.json"), "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print("imported %d files, %s MiB; excluded %d (%s MiB); %d index files; %d mailbox items; manifest %s MiB" % (
        tot_n, mib(tot_b), len(excluded), mib(sum(e["bytes"] for e in excluded)), len(archive_files), len(mail), mib(len(out.encode()))))
    for key, dname, _ in DIVS:
        i = divinfo[key]
        print("  %-12s %s  %5d files %8s MiB  excluded %d" % (key, i["pinned_commit"][:12], i["files_included"], mib(i["bytes_included"]), i["files_excluded"]))


if __name__ == "__main__":
    main()
