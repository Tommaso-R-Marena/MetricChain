#!/bin/bash
# Regenerates the text extractions listed in sources_manifest.tsv (public addresses; 3 s apart) into txt/<name>/,
# so that check_quotes.py can be re-run:  ./regen_sources.sh && python3 -I check_quotes.py <report> txt <dir of read-only copies>
# The extractions are third-party texts: do not commit them; remove them after use.
here="$(cd "$(dirname "$0")" && pwd)"
grep -v '^#' "$here/sources_manifest.tsv" | while IFS=$'\t' read -r name url rest; do
  case "$url" in *"/html/"*) kind=html ;; *) kind=pdf ;; esac
  "$here/gettext.sh" "$name" "$url" "$kind"
  sleep 3
done
