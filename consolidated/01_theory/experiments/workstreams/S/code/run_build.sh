#!/bin/bash
# finite bridges from periodic chain systems; one process at a time
ulimit -v 2000000
cd "$(dirname "$0")"
run() {  # name ideal witness sizes...
  name="$1"; ideal="$2"; wit="$3"; shift 3
  echo "== $name   ideal (p3,p8,p11,g) = $ideal"
  for W in "$@"; do python3 build.py "$wit" $W $W $W | sed -n '2p' | sed "s/^/   box $W:/"; done
}
run "W3 woodpile" "(0, 3, 4, 0)" "hnf rows (1 0 0) (0 1 2) (0 0 3); path bonds A(n)-type: A(0,0,1):a2,a3 A(0,0,2):a0,a1" 16 32 48 64
run "checkerboard of rods" "(0, 1, 3, 0)" "hnf rows (1 0 0) (0 1 1) (0 0 2); path bonds A(n)-type: A(0,0,1):a0,a1" 16 32 48 64
run "coplanar sheet stack" "(0, 0, 1, 0)" "hnf rows (1 0 0) (0 1 1) (0 0 3); path bonds A(n)-type: A(0,0,2):a0,a1" 16 32 48 64
run "(1/2,2,5/2) rods" "(0.5, 2, 2.5, 0)" "hnf rows (1 0 0) (0 1 1) (0 0 4); path bonds A(n)-type: A(0,0,2):a0,a1 A(0,0,3):a0,a1" 16 32 48 64
run "(1/2,4,9/2) crossed rods" "(0.5, 4, 4.5, 0)" "hnf rows (1 0 0) (0 1 4) (0 0 5); path bonds A(n)-type: A(0,0,1):a2,a3 A(0,0,2):a2,a3 A(0,0,3):a0,a1 A(0,0,4):a0,a1" 16 32 48 64
run "full crystal (generic builder)" "(1, 5, 6, 0)" "hnf rows (1 0 0) (0 1 0) (0 0 1); path bonds A(n)-type: A(0,0,0):a0,a1" 16 32 48
run "gauche-rich (0,12/5,22/5)" "(0, 2.4, 4.4, 0.8)" "hnf rows (1 0 1) (0 1 4) (0 0 8); path bonds A(n)-type: A(0,0,2):a0,a3 A(0,0,4):a0,a2 A(0,0,5):a2,a3 A(0,0,6):a1,a2 A(0,0,7):a0,a1" 16 32 48 64
run "gauche-rich (1/3,5/3,3)" "(0.3333, 1.6667, 3, 0.6667)" "hnf rows (1 0 2) (0 1 3) (0 0 6); path bonds A(n)-type: A(0,0,2):a0,a1 A(0,0,4):a0,a2 A(0,0,5):a1,a2" 16 32 48 64
run "all-gauche (0,1/2,9/4)" "(0, 0.5, 2.25, 1)" "hnf rows (1 0 4) (0 1 5) (0 0 10); path bonds A(n)-type: A(0,0,4):a0,a1 A(0,0,6):a0,a2 A(0,0,7):a1,a3 A(0,0,9):a2,a3" 16 32 48 64
