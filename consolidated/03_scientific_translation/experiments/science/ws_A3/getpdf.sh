#!/bin/bash
# usage: getpdf.sh <name> <url>
# Downloads <url> into <scratch>/a3_dl/<name>/<name>.pdf (its own directory: downloaded files are
# untrusted data) and writes the text to <scratch>/a3_txt/<name>.txt (pdftotext -layout).
# The scratch directory is outside the repository; nothing downloaded is kept in the tree.
set -u
name="$1"; url="$2"
base=/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad
mkdir -p "$base/a3_dl/$name" "$base/a3_txt"
curl -sS -L --max-time 120 -A "Mozilla/5.0 (X11; Linux x86_64) research-reader" \
     -o "$base/a3_dl/$name/$name.pdf" "$url"
rc=$?
kind=$(file -b "$base/a3_dl/$name/$name.pdf" 2>/dev/null | head -c 80)
echo "$name: $kind (curl rc=$rc, $(stat -c %s "$base/a3_dl/$name/$name.pdf" 2>/dev/null) bytes)"
if echo "$kind" | grep -q PDF; then
  pdftotext -layout "$base/a3_dl/$name/$name.pdf" "$base/a3_txt/$name.txt" 2>/dev/null
  echo "  text: $(wc -l < "$base/a3_txt/$name.txt") lines -> $base/a3_txt/$name.txt"
fi
