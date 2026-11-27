#!/usr/bin/env python3
"""Print title / authors / date / journal-ref / abstract of arXiv papers by id (public arXiv API).
usage: python3 arxiv_meta.py 2006.08840 1908.04021 ...     (ids only: generic bibliographic lookups)
   or: python3 arxiv_meta.py -q 'all:"geometric rigidity" AND all:rod' [max]   (API search syntax)"""
import os, re, ssl, sys, urllib.parse, urllib.request, html
ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or "/root/.ccr/ca-bundle.crt")
def get(params):
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "research-reader/1.0"})
    try:
        return url, urllib.request.urlopen(req, timeout=90, context=ctx).read().decode()
    except Exception as e:
        return url, "ERR %s" % e
if sys.argv[1] == "-q":
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    url, data = get({"search_query": sys.argv[2], "start": 0, "max_results": n, "sortBy": "relevance"})
    full = False
else:
    url, data = get({"id_list": ",".join(sys.argv[1:]), "max_results": len(sys.argv) - 1})
    full = True
print("URL:", url)
if data.startswith("ERR"):
    print(data); sys.exit(0)
tot = re.search(r"totalResults[^>]*>(\d+)<", data)
print("total:", tot.group(1) if tot else "?")
for e in re.findall(r"<entry>(.*?)</entry>", data, flags=re.S):
    g = lambda pat: (re.search(pat, e, flags=re.S) or [None, ""])[1]
    t = re.sub(r"\s+", " ", html.unescape(g(r"<title>(.*?)</title>")))
    i = g(r"<id>(.*?)</id>").split("/abs/")[-1]
    p = g(r"<published>(.*?)</published>")[:10]
    au = re.findall(r"<name>(.*?)</name>", e)
    jr = re.sub(r"\s+", " ", html.unescape(g(r"<arxiv:journal_ref[^>]*>(.*?)</arxiv:journal_ref>")))
    print(f"\n* {i} [{p}] {t}\n  {', '.join(au[:6])}{' et al.' if len(au) > 6 else ''}" + (f"\n  journal-ref: {jr}" if jr else ""))
    if full:
        ab = re.sub(r"\s+", " ", html.unescape(g(r"<summary>(.*?)</summary>"))).strip()
        print("  abstract:", ab)
