#!/usr/bin/env python3
"""Query the public arXiv API (export.arxiv.org) and print id, date, title, authors.

usage: arxiv_q.py '<search_query in arXiv API syntax>' [max_results] [relevance|date]
e.g.   arxiv_q.py 'ti:"sample size required in importance sampling"' 5

Only generic bibliographic queries are sent (titles / authors / keywords of published papers).
"""
import os
import re
import ssl
import sys
import urllib.parse
import urllib.request

q = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
sort = sys.argv[3] if len(sys.argv) > 3 else "relevance"
params = {"search_query": q, "start": 0, "max_results": n,
          "sortBy": "submittedDate" if sort == "date" else "relevance", "sortOrder": "descending"}
url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or "/root/.ccr/ca-bundle.crt")
req = urllib.request.Request(url, headers={"User-Agent": "research-reader/1.0"})
try:
    data = urllib.request.urlopen(req, timeout=60, context=ctx).read().decode()
except Exception as e:  # network errors are reported, not raised
    print("ERR", e)
    sys.exit(0)
ents = re.findall(r"<entry>(.*?)</entry>", data, flags=re.S)
tot = re.search(r"totalResults[^>]*>(\d+)<", data)
print("query:", q, "| total:", tot.group(1) if tot else "?")
for e in ents:
    t = re.sub(r"\s+", " ", re.search(r"<title>(.*?)</title>", e, flags=re.S).group(1))
    i = re.search(r"<id>(.*?)</id>", e).group(1).split("/abs/")[-1]
    p = re.search(r"<published>(.*?)</published>", e).group(1)[:10]
    au = re.findall(r"<name>(.*?)</name>", e)
    jr = re.search(r"<arxiv:journal_ref[^>]*>(.*?)</arxiv:journal_ref>", e, flags=re.S)
    print(f"  {i} [{p}] {t} — {', '.join(au[:5])}{' et al.' if len(au) > 5 else ''}"
          + (f" | {re.sub(r'\\s+', ' ', jr.group(1))}" if jr else ""))
