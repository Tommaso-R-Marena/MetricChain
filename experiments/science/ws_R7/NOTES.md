# Workstream R7 — notes (kept from the first minute)

Referee: independent review + replication of the ENGINEERING division
(branch `research/ubuntu-engineering` at `a2f6dc7`).

Conventions in these notes:
* "OWN" = my own code written before reading engineering's implementation.
* "RERUN" = their code exported into `eng_copy/` and run here.
* "READ" = read only.
* Times are UTC from `date`.

## Log

### 2026-11-25 20:21 — start
* Read COMMON.md and R7_brief.md in full.
* Created `experiments/science/ws_R7/` and `eng_copy/`.
* `git rev-parse origin/research/ubuntu-engineering` = a2f6dc781de05b642189a51d2ed88f94e8ed7026 (matches brief).
* Plan (order of the brief):
  1. X-004 generic chain: read the MODEL DEFINITION ONLY (theory P_REPORT §§0, 2.1, 3.3), write own enumerator,
     then read ENG-RES-0007/-0009 numbers, compare, THEN read their code.
  2. X-002 lattice covers as certificates.
  3. X-003 Harper closed form.
  4. X-005 statistics/claims.
  5. Record traceability.
  6. What is missing.

### 20:24 — step 1a: OWN enumerator of the generic chain (before reading any engineering file on X-004)
* Read ONLY theory `docs/workstreams/P_REPORT.md` §0, §2.1, §3.2 (table of gen), §3.3 and theory report §11.2 (Thm 11.4,
  definition of N_cov).  Model "gen": b=1, theta=111 deg, torsions 180/+60/-60, hard core s>=3.0 for q-p>=3, S_c=16,
  pairs q-p>=3, profile = sorted multiset of min(s,16), d_P = L*||N^x-N^y||_1.
* Wrote `own_gen.py` (level-by-level growth with prefix pruning; float64; global clustering of distance values, tol 1e-9,
  gap spectrum recorded).
* Sanity: 1-4 squared distances 6.4334718 (t), 3.81875456 (g) [P_REPORT: 6.433 / 3.819]; 1-5 for g+g-: 2.92460422 [2.92]. OK.
* OWN results n=1..11 (run 0.7 s):
  conf   = 3, 7, 17, 41, 99, 239, 577, 1393, 3363, 8115, 19559
  classes= 2, 3, 7, 13, 30, 60, 136, 291, 639, 1360, 2908
  -> agrees with theory P_REPORT §3.3 table for n=5..10 (99/30, 239/60, 577/136, 1393/291, 3363/639, 8115/1360).
* Tie structure (important for "generic" claims): max gap inside a cluster 2e-14 (float noise), min gap between distinct
  clusters 1.385e-4 (n>=8), 7.5e-3 (n=4..7) -> ties are unambiguous in float64 at these sizes.
  smallest |s - 3.0| over all tested pairs: 7.5e-2 (n<=5), 5.2e-2 (n<=9), 2.0e-2 (n=10,11) -> hard-core test not tolerance-sensitive.
* number of distinct truncated distance values incl. the cutoff: 22 (n=5) ... 151 (n=10) = "21-150 features" of P_REPORT. OK.

### 20:30 — step 1b: OWN covering numbers (still before reading engineering X-004 files)
* Wrote `own_cover.py`: classes -> D[a,y]=||N^a-N^y||_1 -> boolean cover matrix (L*D <= mingap+eps, tol 1e-9, min margin
  recorded) -> greedy, LP (HiGHS), tolerance-free LP lower bound (dual rounded to integers and rescaled by exact max load),
  MILP (HiGHS, mip_rel_gap=0) with exact feasibility re-check of the returned 0/1 vector.
* OWN results (out_own_cover_n5_9.txt), format (L=1,eps=0) / (L=1,eps=N/2) / (L=0.2,eps=0):
  n=5: 27 / 9 / 5;  n=6: 48 / 15 / 5;  n=7: 92 / 21 / 6;  n=8: 137 / 34 / 9;  n=9: 215 / 43 / 11
  = theory P_REPORT §3.3 column P exactly (27,48,92,137,215; 9,15,21,34,43; 5,5,6,9,11).
* Smallest |L*D - radius| over all (centre, point) pairs: >= 2.9e-5 -> cover matrices not tolerance-sensitive (tol 1e-9).
* Now reading ENG-RES-0007 / -0009 (reports, not code) to learn which numbers engineering claims.

### 20:40 — step 1c: read ENG-RES-0007 and ENG-RES-0009 (reports only; their code still unread); OWN stats + entropy
* Claims to test (X-004): conformations/classes n=5..14; 12-column cover table n=5..12; "nearest tie" column and the
  "five exact ties at n=11, L=1, eps=N/2"; "distinct classes never closer than 0.035"; hard-core margins
  (0.078 above / 0.020 below at n=10); entropy table sigma(rho) n=5..14; pairs-within-cutoff per bead.
* `own_stats.py` (pairs strictly inside the cutoff, per bead: mean over classes / over conformations / max):
  n=5: 1.62/1.63/1.88; n=6: 1.88/1.86/2.33; n=10: 2.58/2.46/4.23; n=12: 2.85/2.65/5.20 -> identical to ENG-RES-0009 table.
  NB the max equals (number of pairs)/N at every n<=12: the conformation (t g+ g+)^k has ALL pairs within the cutoff
  (I suspected a bug in the "max" column since it coincides with P/N; it is real).
* `l1kern.c` + `own_entropy.py`: sigma(rho) = mean_c ln m_c(rho) / n with m_c = #classes within rho*N (<=, tol 1e-9).
  n=5..14 all six columns identical to ENG-RES-0009 to the 3 printed decimals; n=13: 113 587 conf / 13 012 classes;
  n=14: 273 623 / 27 421 (their "new" numbers) REPLICATED with own code. (n=14: 77 s, 1 core.)
  nearest distinct classes: 0.302, 0.204, 0.094 (n=7..10), 0.0353 (n=11,12), 0.0075 (n=13), 0.0072 (n=14):
  the sentence "never closer than 0.035" is true for n<=12 (the range it was made for).
