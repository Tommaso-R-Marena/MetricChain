#!/bin/bash
# usage: ./run_after.sh REGEX LISTFILE -- wait until no process matches REGEX, then run the queue LISTFILE.
# Write the regex so that it does not match this script's own command line, e.g. '[p]8_05_gibbs'.
cd "$(dirname "$0")"
while pgrep -f "$1" > /dev/null; do sleep 3; done
./run_queue.sh "$2"
