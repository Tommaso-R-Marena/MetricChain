#!/bin/bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd "$(dirname "$0")"
timeout 1150 python3 -B t04_tight.py out/tight_apolar.json V3:E:0.70 V4:E:0.70 V6:E:0.70 V8:E:0.70 V4:P2:0.70 V6:P2:0.70 V8:P2:0.70 L4:E:0.60 L6:E:0.60 L8:E:0.60 L4:P2:0.60 L6:P2:0.60 L8:P2:0.60 L4:H:0.60 L6:H:0.60 L8:H:0.60 > logs/t04_tight_apolar.log 2>&1
timeout 1150 python3 -B t04_tight.py out/tight_polar.json S3:E:0.70 S4:E:0.70 S5:E:0.70 S6:E:0.70 S4:P2:0.70 S6:P2:0.70 S4:H:0.70 S5:H:0.70 S6:H:0.70 S6:H:0.60 F4:E:0.60 F6:E:0.60 F4:H:0.60 F6:H:0.60 F4:P2:0.60 F6:P2:0.60 > logs/t04_tight_polar.log 2>&1
timeout 1150 python3 -B t04_tight.py out/tight_charged.json K3:H:0.70 K4:H:0.70 K3:E:0.70 K4:E:0.70 K4:P2:0.70 K4:H:0.60 K4:P2:0.60 LKSEc4:H:0.60 LKSEc5:H:0.60 LKSEc6:H:0.60 LKSEc6:P2:0.60 LKSEc6:E:0.60 > logs/t04_tight_charged.log 2>&1
echo DONE >> logs/t04_tight_charged.log
