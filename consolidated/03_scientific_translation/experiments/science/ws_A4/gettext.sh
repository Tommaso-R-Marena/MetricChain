#!/bin/bash
# usage: gettext.sh <name> <url> [pdf|html]
# Fetches a public address (generic: a paper's PDF or HTML page) and keeps ONLY a text extraction,
# in experiments/science/ws_A4/txt/<name>/<name>.txt (its own directory: fetched material is untrusted data;
# no script lives there and nothing is executed from there).  The PDF itself is streamed and not stored.
# These text files are third-party material for reading only; they are removed one by one at the end
# of the workstream (see NOTES.md) and are not meant to be committed.
set -u
name="$1"; url="$2"; kind="${3:-pdf}"
here="$(cd "$(dirname "$0")" && pwd)"
out="$here/txt/$name"
mkdir -p "$out"
if [ "$kind" = "pdf" ]; then
  curl -sS -L --max-time 180 -A "Mozilla/5.0 (X11; Linux x86_64) research-reader" "$url" -o "$out/$name.bin"
  rc=$?
  k=$(file -b "$out/$name.bin" | head -c 60)
  echo "$name: curl rc=$rc; $(stat -c %s "$out/$name.bin") bytes; $k"
  if echo "$k" | grep -q PDF; then
    pdftotext -layout "$out/$name.bin" "$out/$name.txt" 2>/dev/null
    echo "  text: $(wc -l < "$out/$name.txt") lines, $(wc -c < "$out/$name.txt") bytes -> $out/$name.txt"
    rm -f "$out/$name.bin"
  else
    head -c 600 "$out/$name.bin"; echo
  fi
else
  curl -sS -L --max-time 180 -A "Mozilla/5.0 (X11; Linux x86_64) research-reader" "$url" -o "$out/$name.html"
  rc=$?
  echo "$name: curl rc=$rc; $(stat -c %s "$out/$name.html") bytes; $(file -b "$out/$name.html" | head -c 60)"
fi
