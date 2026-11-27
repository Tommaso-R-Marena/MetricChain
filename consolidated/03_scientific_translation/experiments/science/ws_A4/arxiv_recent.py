#!/usr/bin/env python3
"""arXiv API search sorted by submission date (newest first): id, date, title, authors.
usage: python3 arxiv_recent.py '<query in arXiv API syntax>' [max]   (generic bibliographic queries only)"""
import os, re, ssl, sys, urllib.parse, urllib.request, html
ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or "/root/.ccr/ca-bundle.crt")
n = int(sys.argv[2]) if len(sys.argv) > 2 else 15
url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
    {"search_query": sys.argv[1], "start": 0, "max_results": n, "sortBy": "submittedDate", "sortOrder": "descending"})
print("URL:", url)
try:
    data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "research-reader/1.0"}),
                                  timeout=90, context=ctx).read().decode()
except Exception as e:
    print("ERR", e); sys.exit(0)
tot = re.search(r"totalResults[^>]*>(\d+)<", data); print("total:", tot.group(1) if tot else "?")
for e in re.findall(r"<entry>(.*?)</entry>", data, flags=re.S):
    g = lambda pat: (re.search(pat, e, flags=re.S) or [None, ""])[1]
    t = re.sub(r"\s+", " ", html.unescape(g(r"<title>(.*?)</title>")))
    i = g(r"<id>(.*?)</id>").split("/abs/")[-1]; p = g(r"<published>(.*?)</published>")[:10]
    au = re.findall(r"<name>(.*?)</name>", e)
    print(f"  {i} [{p}] {t} — {', '.join(au[:4])}{' et al.' if len(au) > 4 else ''}")
