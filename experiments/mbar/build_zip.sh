#!/usr/bin/env bash
# Consolidated archive of Division 9, built from the committed tree (so it is reproducible from the
# commit).  Usage:
#   experiments/mbar/build_zip.sh --manifest          write experiments/mbar/ZIP_MANIFEST.sha256 (then commit)
#   experiments/mbar/build_zip.sh [out.zip]           build the archive from HEAD
# Verify an unpacked archive:  cd division9_certified_mbar && sha256sum -c experiments/mbar/ZIP_MANIFEST.sha256
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
PATHS="docs/mbar docs/collaboration/messages/mbar docs/collaboration/requests/mbar docs/collaboration/status/mbar.md docs/collaboration/MBAR_TO_ALL.md experiments/mbar"
if [ "${1:-}" = "--manifest" ]; then
  git ls-files $PATHS | grep -v '^experiments/mbar/ZIP_MANIFEST.sha256$' | LC_ALL=C sort | tr '\n' '\0' \
    | xargs -0 sha256sum > experiments/mbar/ZIP_MANIFEST.sha256
  echo "manifest written: $(wc -l < experiments/mbar/ZIP_MANIFEST.sha256) files"
  exit 0
fi
OUT="${1:-division9_certified_mbar.zip}"
git diff --quiet HEAD -- $PATHS || { echo "uncommitted changes under the division's paths" >&2; exit 1; }
git archive --format=zip --prefix=division9_certified_mbar/ -o "$OUT" HEAD $PATHS
echo "archive: $(sha256sum "$OUT")"
echo "commit:  $(git rev-parse HEAD)"
