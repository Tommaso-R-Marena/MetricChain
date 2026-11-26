#!/bin/bash
# wait for the first leg of the LKSE:6 measurement (started by hand at 06:10) to stop at its budget, then run the queue
cd "$(dirname "$0")"
while pgrep -f "p8_01_measure.py LKSE:6" > /dev/null; do sleep 5; done
./run_queue.sh queue_enum.txt
