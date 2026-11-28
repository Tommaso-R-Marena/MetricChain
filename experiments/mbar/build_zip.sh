#!/usr/bin/env bash
# Consolidated archive of Division 9, built from the committed tree (so it is reproducible from the
# commit).  Usage:
#   experiments/mbar/build_zip.sh --manifest          write experiments/mbar/ZIP_MANIFEST.sha256 (then commit)
#   experiments/mbar/build_zip.sh [out.zip]           build the archive from HEAD
# Verify an unpacked archive:  cd division9_certified_mbar && sha256sum -c experiments/mbar/ZIP_MANIFEST.sha256
# The archive is a `git archive` of the division's paths at HEAD (commit id in the zip comment: unzip -z),
# so its contents are reproducible from the commit; it is byte-identical for the same versions of git and zlib.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
PATHS="docs/mbar docs/collaboration/messages/mbar docs/collaboration/requests/mbar docs/collaboration/status/mbar.md docs/collaboration/MBAR_TO_ALL.md experiments/mbar"
MANIFEST=experiments/mbar/ZIP_MANIFEST.sha256
manifest() {
  git ls-files $PATHS | grep -v "^$MANIFEST\$" | LC_ALL=C sort | tr '\n' '\0' | xargs -0 sha256sum
}
if [ "${1:-}" = "--manifest" ]; then
  manifest > "$MANIFEST"
  echo "manifest written: $(wc -l < "$MANIFEST") files"
  exit 0
fi
OUT="${1:-division9_certified_mbar.zip}"
[ -z "$(git status --porcelain -- $PATHS)" ] || { echo "uncommitted or untracked files under the division's paths" >&2; exit 1; }
manifest | cmp -s - "$MANIFEST" || { echo "manifest is stale: run with --manifest and commit" >&2; exit 1; }
# The tracked file experiments/mbar/zip_root/README.md is also placed at the root of the archive.
git archive --format=zip --prefix=division9_certified_mbar/ --add-file=experiments/mbar/zip_root/README.md \
  -o "$OUT" HEAD $PATHS
echo "archive: $(sha256sum "$OUT")"
echo "commit:  $(git rev-parse HEAD)"
echo "files:   $(unzip -Z1 "$OUT" | grep -vc '/$')"
