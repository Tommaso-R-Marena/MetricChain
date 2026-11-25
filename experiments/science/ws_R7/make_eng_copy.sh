#!/usr/bin/env bash
# Re-creates experiments/science/ws_R7/eng_copy/ (git-ignored; NOT part of the science branch) from the
# engineering branch at the commit reviewed by workstream R7.  Read-only with respect to git state
# (git archive writes nothing into the repository's index, HEAD or work tree outside eng_copy/).
#
#   bash experiments/science/ws_R7/make_eng_copy.sh            # from the repository root
#
# A single file can equally be obtained with:  git show a2f6dc781de05b642189a51d2ed88f94e8ed7026:<path>
set -euo pipefail
ENG_COMMIT=a2f6dc781de05b642189a51d2ed88f94e8ed7026     # origin/research/ubuntu-engineering as reviewed
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
mkdir -p "$HERE/eng_copy"
git -C "$ROOT" archive "$ENG_COMMIT" \
    ENGINEERING.md docs/engineering docs/collaboration src/metricchain_eng experiments/eng modal_jobs tests/eng scripts \
  | tar -x -C "$HERE/eng_copy"
echo "eng_copy/ re-created from $ENG_COMMIT: $(find "$HERE/eng_copy" -type f | wc -l) files"
