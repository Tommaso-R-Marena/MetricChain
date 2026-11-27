#!/usr/bin/env bash
# Source this file to put the pinned Lean toolchain (see lean-toolchain) on PATH.
# Preference order: an existing `lake` on PATH, elan, then a direct release unpack in ~/.lean.
if ! command -v lake >/dev/null 2>&1; then
  for d in "$HOME/.elan/bin" "$HOME/.lean/lean-4.31.0-linux/bin"; do
    if [ -x "$d/lake" ]; then export PATH="$d:$PATH"; break; fi
  done
fi
if ! command -v lake >/dev/null 2>&1; then
  echo "error: Lean toolchain not found. Install elan (https://lean-lang.org/install) or unpack" >&2
  echo "       the lean-4.31.0 release archive into \$HOME/.lean/ ; then run 'lake exe cache get'." >&2
  return 1 2>/dev/null || exit 1
fi
