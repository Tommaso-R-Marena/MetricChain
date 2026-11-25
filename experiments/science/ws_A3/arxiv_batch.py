#!/usr/bin/env python3
"""Run several arXiv API title queries in sequence (3 s apart, as the API asks).
usage: arxiv_batch.py 'query1' 'query2' ...   (each in arXiv API syntax)"""
import subprocess, sys, time, os
here = os.path.dirname(os.path.abspath(__file__))
for i, q in enumerate(sys.argv[1:]):
    if i:
        time.sleep(3.2)
    out = subprocess.run([sys.executable, os.path.join(here, "arxiv_q.py"), q, "4"], capture_output=True, text=True)
    print(out.stdout.rstrip())
