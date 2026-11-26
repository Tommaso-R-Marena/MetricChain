#!/usr/bin/env python3
"""Build the artifact files of freeze FRONTIER-FRZ-0001 from raw pages fetched from
predictioncenter.org and data.rcsb.org (run once, 2026-11-26; kept for the record).

usage: build_casp17_snapshot.py RAW_DIR SEQ_DIR RCSB_JSON OUT_DIR

The raw HTML is not copied (the target-list page alone is 0.4 MB); its SHA-256 is recorded.
Copied verbatim: the target list CSV (21 kB).  Everything else is derived and says so.
Data of the Protein Structure Prediction Center are used under its terms (CC BY 4.0).
"""
import csv
import hashlib
import html
import json
import re
import sys
from pathlib import Path

raw, seqdir, rcsb_json, out = (Path(p) for p in sys.argv[1:5])
out.mkdir(parents=True, exist_ok=True)
BASE = "https://predictioncenter.org"
PAGES = {  # local name -> URL
    "casp17_index.html": f"{BASE}/casp17/",
    "news.html": f"{BASE}/news.cgi",
    "targetlist.cgi.html": f"{BASE}/casp17/targetlist.cgi",
    "targetlist.csv": f"{BASE}/casp17/targetlist.cgi?type=csv",
    "index.cgi_page_format.html": f"{BASE}/casp17/index.cgi?page=format",
    "index.cgi_page_QandA.html": f"{BASE}/casp17/index.cgi?page=QandA",
    "domains_summary.cgi.html": f"{BASE}/casp17/domains_summary.cgi",
    "results_page.html": f"{BASE}/casp17/results.cgi",
}
LISTINGS = {  # local name -> directory of the download area
    "dl_.html": "", "dl_targets.html": "targets/", "dl_results.html": "results/",
    "dl_sequences_.html": "sequences/", "dl_predictions.html": "predictions/",
    "dl_predictions_regular_.html": "predictions/regular/", "dl_predictions_oligo_.html": "predictions/oligo/",
    "dl_predictions_E-targets_.html": "predictions/E-targets/", "dl_predictions_QA_.html": "predictions/QA/",
    "dl_predictions_RNA_.html": "predictions/RNA/", "dl_predictions_RNA_oligo_.html": "predictions/RNA_oligo/",
    "dl_predictions_hybrid_.html": "predictions/hybrid/", "dl_predictions_ligands_.html": "predictions/ligands/",
    "dl_predictions_W-targets_.html": "predictions/W-targets/", "dl_extra_experiments_.html": "extra_experiments/",
    "dl_extra_experiments_ligands_.html": "extra_experiments/ligands/",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# 1. verbatim copy of the target list
(out / "targetlist.csv").write_bytes((raw / "targetlist.csv").read_bytes())

# 2. checksums of every raw page that was read
pages = []
for name, url in {**PAGES, **{k: f"{BASE}/download_area/CASP17/{v}" for k, v in LISTINGS.items()}}.items():
    p = raw / name
    pages.append({"url": url, "bytes": p.stat().st_size, "sha256": sha(p)})
for p in sorted(seqdir.glob("casp17.*.seq.txt")):
    pages.append({"url": f"{BASE}/download_area/CASP17/sequences/{p.name}", "bytes": p.stat().st_size, "sha256": sha(p),
                  "fasta_records": p.read_text(errors="replace").count(">")})
pages.sort(key=lambda d: d["url"])
(out / "pages_sha256.json").write_text(json.dumps(pages, indent=1, sort_keys=True) + "\n")

# 3. parsed directory listings of the download area (name, last modified, size as shown)
row_re = re.compile(r'<a href="([^"?][^"]*)">[^<]*</a>\s*</td>\s*<td[^>]*>\s*([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9:]{5})\s*</td>\s*<td[^>]*>\s*([^<]*?)\s*</td>', re.S)
listing = {}
for name, d in LISTINGS.items():
    text = (raw / name).read_text(errors="replace")
    rows = [{"name": html.unescape(a), "last_modified": b, "size": c.strip()} for a, b, c in row_re.findall(text)]
    listing["/download_area/CASP17/" + d] = rows
(out / "download_area_listing.json").write_text(json.dumps(listing, indent=1, sort_keys=True) + "\n")

# 4. the announcements, as short verbatim extracts
news = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", (raw / "news.html").read_text(errors="replace"))
news = html.unescape(re.sub(r"(?s)<[^>]+>", "\n", news))
lines = [re.sub(r"\s+", " ", l).strip() for l in news.split("\n")]
lines = [l for l in lines if l]
keep = []
for i, l in enumerate(lines):
    if l in ("CASP17 program is online", "In preparation for the CASP17 conference"):
        keep += ["## " + l] + lines[i + 1:i + (6 if "program" in l else 16)] + [""]
res = html.unescape(re.sub(r"(?s)<[^>]+>", "\n", (raw / "results_page.html").read_text(errors="replace")))
res_line = next((re.sub(r"\s+", " ", l).strip() for l in res.split("\n") if "No results available" in l), "(sentence not found)")
(out / "announcements_extract.txt").write_text(
    "Verbatim extracts from https://predictioncenter.org/news.cgi and /casp17/results.cgi\n"
    "(fetched 2026-11-26 22:37-23:02 UTC; (c) Protein Structure Prediction Center, CC BY 4.0)\n\n"
    + "\n".join(keep) + "\n## /casp17/results.cgi\n" + res_line + "\n")

# 5. derived classification of every target
rcsb = json.loads(rcsb_json.read_text())
entries = rcsb["entries"]
rows = []
with open(raw / "targetlist.csv", encoding="utf-8", errors="replace", newline="") as fh:
    reader = csv.reader(fh, delimiter=";")
    header = [h.strip() for h in next(reader)]
    for r in reader:
        if not r or not r[0].strip():
            continue
        d = dict(zip(header, (c.strip() for c in r)))
        desc = re.sub(r"<[^>]+>", "", d["Description"]).strip()
        codes = [c for c in re.findall(r"(?<![A-Za-z0-9])([0-9][0-9a-z]{3})(?![A-Za-z0-9])", desc)
                 if re.search(r"[a-z]", c) and entries.get(c, {}).get("http") == "200"]
        cancelled = d.get("Cancellation Date", "-") not in ("-", "")
        releases = sorted(entries[c]["release"] for c in codes)
        if cancelled:
            status = "cancelled"
        elif codes:
            status = "reference public in the PDB"
        else:
            status = "no PDB code on the target list"
        rows.append([d["Target"], d["Type"], d["Res"], d["Oligo.State"], d["Entry Date"], d["Human Exp."],
                     " ".join(codes), releases[0] if releases else "", status])
with open(out / "targets_classified.csv", "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["target", "type", "residues", "stoichiometry", "entry_date", "human_expiration",
                "pdb_codes_on_target_list_found_released_at_rcsb", "earliest_pdb_release", "reference_status_2026-11-26"])
    w.writerows(rows)
(out / "rcsb_release_status.json").write_text(json.dumps(rcsb, indent=1, sort_keys=True) + "\n")
counts = {}
for r in rows:
    counts[r[-1]] = counts.get(r[-1], 0) + 1
print(len(rows), "targets;", counts)
