#!/bin/bash
# R19: snapshot (names, sizes, mtimes) of every directory the coordinator's scripts could touch, to prove that a re-run wrote nothing.
# usage: snap_caches.sh OUTFILE
SCI=/home/user/MetricChain/experiments/science
out="$1"
: > "$out"
for d in p9_verification/cache ws_P8/out ws_P8/cache ws_P9/cache ws_P9/out pi_inference/serine_helix_reach_cache ws_P6/cache ws_P6/out ws_P3/cache ws_P5/cache pi_inference/helix_pair_form_cache; do
  find "$SCI/$d" -type f -printf '%p %s %T@\n' 2>/dev/null | sort >> "$out"
done
# the committed logs and scripts of pi_inference (top level only)
find "$SCI/pi_inference" -maxdepth 1 -type f -printf '%p %s %T@\n' | sort >> "$out"
find "$SCI/assumption_audit" "$SCI/p9_verification" -maxdepth 1 -type f -printf '%p %s %T@\n' | sort >> "$out"
wc -l "$out"
