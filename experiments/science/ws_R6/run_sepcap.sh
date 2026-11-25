#!/bin/bash
# workstream R6: the finite-n separation with the lowered cap of 40c5bd7, wider range of outer fractions (one process).
export OMP_NUM_THREADS=1
cd "$(dirname "$0")"
until [ "$(grep -c '^adv2 ' logs/progress.txt)" -ge 2 ]; do sleep 5; done
python3 separation_cap.py 1.0 1150,1200,1250,1275,1300 > logs/separation_cap_u1.log 2>&1; echo "sepcap u1 exit $?" >> logs/progress.txt
python3 separation_cap.py 2.0 400,425,450,475,500 > logs/separation_cap_u2.log 2>&1; echo "sepcap u2 exit $?" >> logs/progress.txt
python3 separation_cap.py 0.5 3700,3850,4000,4150,4300 > logs/separation_cap_u05.log 2>&1; echo "sepcap u05 exit $?" >> logs/progress.txt
echo ALLDONE_SEPCAP >> logs/progress.txt
