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

### ~20:23 — step 1a: OWN enumerator of the generic chain (before reading any engineering file on X-004)
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

### ~20:25 — step 1b: OWN covering numbers (still before reading engineering X-004 files)
* Wrote `own_cover.py`: classes -> D[a,y]=||N^a-N^y||_1 -> boolean cover matrix (L*D <= mingap+eps, tol 1e-9, min margin
  recorded) -> greedy, LP (HiGHS), tolerance-free LP lower bound (dual rounded to integers and rescaled by exact max load),
  MILP (HiGHS, mip_rel_gap=0) with exact feasibility re-check of the returned 0/1 vector.
* OWN results (out_own_cover_n5_9.txt), format (L=1,eps=0) / (L=1,eps=N/2) / (L=0.2,eps=0):
  n=5: 27 / 9 / 5;  n=6: 48 / 15 / 5;  n=7: 92 / 21 / 6;  n=8: 137 / 34 / 9;  n=9: 215 / 43 / 11
  = theory P_REPORT §3.3 column P exactly (27,48,92,137,215; 9,15,21,34,43; 5,5,6,9,11).
* Smallest |L*D - radius| over all (centre, point) pairs: >= 2.9e-5 -> cover matrices not tolerance-sensitive (tol 1e-9).
* Now reading ENG-RES-0007 / -0009 (reports, not code) to learn which numbers engineering claims.

### ~20:27 — step 1c: read ENG-RES-0007 and ENG-RES-0009 (reports only; their code still unread); OWN stats + entropy
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

### ~20:31 — coordinator note (received while working), acted on
* `eng_copy/` is git-ignored (coordinator added `ws_R7/.gitignore`).  Consequences adopted:
  (1) every engineering file I re-run or quote is cited as `<path>` on `research/ubuntu-engineering` at commit `a2f6dc7`
      (obtain with `git show a2f6dc7:<path>`), never as `eng_copy/...`;
  (2) everything needed to reproduce my numbers lives outside `eng_copy/` (own scripts + outputs in `ws_R7/`), and
      `make_eng_copy.sh` re-creates `eng_copy/` from the engineering commit by `git archive | tar -x` (read-only for git).
* eng_copy was created at ~20:28 by exactly that command (129 files, 8.2 MB).

### ~20:28-20:31 — read (engineering): generic_chain.py, generic_analysis.py, profile_cover.py, generic_entropy.py, make_tables.py,
    results/generic_Sc16.json, generic_Sc16_ties.json, lattice_Sc12.json; ENGINEERING.md, EXPERIMENT_REGISTER.md,
    COMPUTE_LEDGER.md, ENGINEERING_TO_THEORY.md, ENG-RES-0002, -0007, -0009.
* Differences between their generic-chain code and mine (same definitions, independent implementations):
  - enumeration: theirs depth-first with mirror reduction (first gauche must be g+, weight 2); mine breadth-first, no reduction;
  - classes: theirs key = round(sorted distances below cutoff, 8 decimals).tobytes(); mine = global clustering of values
    (chains of gaps < 1e-9) -> immune to a value sitting on a rounding boundary (probability ~1e-5 per distinct value for theirs);
    class counts agree at every n = 5..14, so no such event occurred;
  - cover relation: identical rule (L*D <= gmin + eps + 1e-9);
  - "min_rejected_margin": theirs = min over rejected PLACEMENTS of (3 - min distance of the placement); my first version took the
    min over all violating PAIRS -> 0.0517 for n=6..9 against their 0.0754.  Definitional, not a discrepancy (theirs is the right
    notion: the decision flips only if the minimum crosses).  To recompute with their definition.
  - LOWER BOUNDS (to examine): in `generic_analysis.cover_bracket` and `profile_cover.net_bracket` the reported "lower" is
    max(certified LP-dual bound, ceil(HiGHS dual bound - 1e-6)); the two are NOT stored separately for the generic chain,
    yet ENG-RES-0007 calls the brackets "[certified lower bound, verified cover]".
  - lattice (`covering_number_P`): `lower` (certified) and `lower_solver` stored separately only for n >= 19; table cell uses
    max(lower_certified, lower_solver) (make_tables.cover_cell) while ENG-RES-0002 text says "a a certified lower bound".
    From lattice_Sc12.json: 25 bracket cells, in 10 of them the published lower end is the solver bound, one above the certified
    bound: n=19 eps=0 [52,56] (cert 51), eps=1 and N/20 [42,44] (41); n=20 eps=0 [57,61] (56), eps=N/10 [37,40] (36);
    n=21 eps=1 and N/20 [50,54] (49); n=23 eps=0 [74,83] (73), eps=1 and N/20 [60,67] (59).
  - generic chain: NO primal covers stored (only sizes) -> covers cannot be checked as certificates, only regenerated.
  - lattice: primal covers stored for all 288 cells (`centres_hist`) -> checkable.

(Clock note, 20:32 real time by `date`: the section times above were first written as guesses that ran ahead of the clock;
they have been corrected to approximate real times.  From here on times are read from `date`.)

### 20:33-20:37 — step 1d (generic covers, 12 cells) and start of step 2 (lattice)
* `own_cover_table.py 5 9` (out_own_cover_table_5_9.txt/.json): ALL 60 cells for n=5..9 equal ENG-RES-0007's table:
  n=5: 27 23 26 23 19 9 | 5 3 4 3 2 2;  n=6: 48 43 46 43 29 15 | 5 4 5 4 3 2;  n=7: 92 66 82 66 44 21 | 6 5 6 5 3 2;
  n=8: 137 97 115 94 59 34 | 9 6 7 5 4 3;  n=9: 215 147 176 141 86 43 | 11 7 8 7 4 3.
  My "nearest tie" (min over 12 cells and all off-diagonal pairs of |L*D - (gmin+eps)|): 5.211e-4, 2.711e-4, 1.155e-4,
  1.824e-5, 4.473e-6  = their column (5.2e-04, 2.7e-04, 1.2e-04, 1.8e-05, 4.5e-06).
  In 40 of the 60 cells my tolerance-free LP bound already equals the MILP optimum; in the others MILP (HiGHS) closes.
* `own_hardcore.py`: closest accepted pair above the core / closest rejected below: n=10: 0.078462 / 0.020008
  (= ENG-RES-0007 "0.078 above ... 0.020 below at n = 10"); n=12: 0.0517 / 0.0200 (their json: 0.05171 / 0.02001).
* n=10 generic cover table running in background (240 s/cell): so far eps=0: 319 (proved; their 319), eps=1: 223 (223),
  eps=N/20: 255 (255).
* Coordinator note acted on (see above).
* LATTICE, primal: `own_lattice_cert.py primal` -> all 288 stored covers (n=1..24, 12 cells each; `centres_hist` of
  lattice_Sc12.json) are valid covers of the stored class tables under my own distance formula
  (5|dC1|+3|dC2|+|dC3|) and exact integer cover relation, and have the published sizes.  0 failures.
  Also: sum of class counts = "conformations" and number of rows = "classes" in every row n=1..24.
* LATTICE, own enumerator `own_dia.c` (written from the definition before reading their dia_enum.c): class tables
  (per class: count, gmin, gmax) IDENTICAL to data/dia_Sc12_n{1..17}.txt; without mirror reduction identical for n=1..9.
  Speed here ~1.6e7 conformations/s (machine loaded): n=17 in 5.3 s.  Plan: n=18..22 later (n=21, 22 are Modal-produced
  tables nobody outside engineering has replicated; R2 reached n=20).

### 20:38-20:40 — step 4 (X-005) first pass: read ENG-RES-0008 in full; refit of the trend from stored data
* `x005_refit.py` (reads x005_cost.jsonl, rebuilds TABLE:trend with my own code): my table equals theirs in every digit
  shown (worst/(na), claimed/a, difference, difference*sqrt(n)) for the 39 rows.  So the published trend table IS
  traceable to the stored file.
* The count 7,095,840 = sum of `n_eval` of the differential-evolution searches: 5,144,256 (x005_cost) + 1,568,160 (claims)
  + 383,424 (converge).  It is a COUNT OF OBJECTIVE-FUNCTION EVALUATIONS along optimisation trajectories (deterministic
  "mean runs" on instances proposed by the optimiser), not a number of random runs; no probability statement attaches.
* Refit (relative least squares on excess = worst/(na) - claimed/a):
    pure power law C n^-p, all 13 sizes: p = 0.758 (u=1/2), 0.676 (u=1), 0.626 (u=2); n>=4000 (phi fixed 0.50): 0.707, 0.612, 0.560
    A/sqrt(n) alone: rms relative misfit 45 %, 33 %, 24 % (all sizes); 23 %, 13 %, 7 % (n >= 4000)
    A/sqrt(n) + B/n: 3.0 %, 4.0 %, 3.7 % (all); 0.6 %, 3.0 %, 1.3 % (n >= 4000);  A = 11.8/7.3/4.6, B = 917/265/95
    A/sqrt(n) + B ln n / n: 4.6 %, 4.0 %, 3.8 % ; A n^-2/3: 18 %, 7.7 %, 9.9 % ; A n^-3/4: 7.4 %, 14 %, 22 %
    local exponent between consecutive sizes falls from ~0.85-0.9 to 0.63 (u=1/2), 0.56 (u=1), 0.54 (u=2) at 128 000.
  => "decays about like 1/sqrt(n)" (digest item 1) is not what the data show over the range: difference*sqrt(n) falls by a factor
     4.9 / 2.9 / 2.2 across the range.  Accurate statement: decays FASTER than 1/sqrt(n) at every size (effective exponent
     0.63-0.76), compatible with an asymptote A/sqrt(n) plus a 1/n (or ln n/n) correction, and equally with a pure power
     n^-0.6..-0.7; the asymptotic exponent 1/2 is neither established nor excluded.  (ENG-RES-0008 section 3 itself says only
     "consistent with the O(sqrt n) correction", which is true as an upper bound.)
* Search budget is NOT uniform in n: (4000 monotone / 2000 general) for n <= 32 000, 2500/1250 at 64 000, 1500/750 at 128 000;
  and the gain of the search over the 63 structured starting points shrinks from 0.11 na (n=250) to 0.003 na (n=128 000), median
  gain exactly 0 for n >= 1400.  The convergence control (M-010) covers n = 1000 and 16 000, u = 1 only.  So at the two largest
  sizes the "worst found" is essentially "best of 63 hand-made instances", with the smallest budget and no convergence control.

### 20:47 — n=10 generic cover table finished (out_own_cover_table_10.txt/.json; 240 s per cell, 1 loaded core)
  mine:   319  223  255  [209,211]  [119,123]  60  |  13  8  10  8  (5, 3 pending at the time of writing -> see file)
  theirs: 319  223  255  [209,211]  [119,123]  60  |  13  8  10  8  5  3      nearest tie mine 3.248e-07, theirs 3.2e-07
  -> the two brackets they could not close in 90 s on 8 cores are the same two I could not close in 240 s on 1 core, with the
     same ends; both of the published brackets of the theory division ([318,319] and [58,62]) close to 319 and 60 in my runs too.
  NB my tolerance-free LP bound alone gives 316 / 219 / 251 / 206 / 117 / 58: every L=1 optimum at n=10 rests on branch and bound
  (HiGHS in both divisions' runs) - there is no solver-independent proof of 319, 223, 255, 60.

### 20:41-20:47 — reading while waiting (no CPU): engineering RESEARCH_LOG, DEAD_ENDS, DEPENDENCY_MAP, tests; git history
* RECORD FINDING (traceability): `git show <c>:src/metricchain_eng/chains/lattice_analysis.py` writes the keys
  lower_certified / lower_solver / exact_certified for every row at EVERY engineering commit (206fd9e, db56d05, a2f6dc7), but the
  stored rows n = 1..18 of results/lattice_Sc12.json (216 of 288 cells) do not have them: those rows were produced by a code
  version that is in no commit (job M-004, before "time limits and certified brackets").  Moreover the committed
  `covering_number_P` breaks out of the solver loop as soon as the first solver (HiGHS) proves optimality, so the committed
  driver never runs CP-SAT on a cell HiGHS closes: the sentence "two solvers agree on every cover" (register X-002 (vi);
  ENG-RES-0002 "by HiGHS and CP-SAT independently for n <= 18") is supported only by those stored rows, and the stated
  reproduction command `run_lattice.py --nmin 1 --nmax 18` would not re-test it.  To verify by re-running their code.
* Compute ledger: jobs M-008..M-011 carry "ran at commit ..."; M-001..M-007 carry no commit.
* OR-Tools 9.15.6755 installed into a PRIVATE directory (scratchpad/pydeps, --no-deps, with its own protobuf 6.33.6) so that the
  shared Python environment is untouched (global protobuf stays 7.36.1).  Use: PYTHONPATH=<scratchpad>/pydeps.
* Wrote (not yet run): own_harper.py, own_tail.py, own_ties.py, own_lattice_opt.py, own_lattice_nets.py.

### 20:47-20:50 — step 3 (X-003, Harper closed form) and step 4b (tail-function reduction of ENG-RES-0008 section 5)
* OWN derivation first (in own_harper.py docstring; H1 symmetrisation, H2 Harper applied to all erosion layers at once,
  H3 nestedness -> monotone one-dimensional search), THEN read ENG-RES-0006: their derivation is the same.
* `own_harper.py brute` (out_own_harper_brute.txt/.json): all 2^(2^n)-2 proper nonempty subsets, n = 2,3,4,
  30 parameter pairs (u in {.25,.5,1,2,3} x eps in {.05,.1,.3,.5,1,2}) = 90 cases:
    - least sensitive size by brute force == simplicial-order prediction: 90/90;
    - LP max_q min_D q(D) over all minimal sensitive sets, WITHOUT the symmetry assumption == m*/2^n: max deviation 5.6e-16;
    - for EVERY size m the true maximum of sum_y exp(u d(y,D^c)) == value at the complement of the initial segment: max rel dev 6.7e-16;
    - smallest margin of a sensitivity comparison: 6.0e-4 (no tolerance issue).
* `own_harper.py table 14` (out_own_harper_table.*): explicit simplicial-order sets + BFS, binary search over m.
  All 52 rows of experiments/eng/fc_uniform_cube/harper_fc_table.json (4 parameter sets x n=2..14) IDENTICAL to mine
  (smallest sensitive |D|, smallest sensitive ball, its radius).  e.g. u=1, eps=0.3: 1,2,4,6,11,19,36,64,120,222,408,763,1432.
* RE-RUN of their script (work tree outside the repo, `rerun_engineering.sh <dir> harper`): `harper_fc.py --check` -> "72 cases,
  all agree"; `--nmax 14` regenerates harper_fc_table.json BYTE-IDENTICAL to the stored file.
* RE-RUN `make_tables.py --verify` (chain_cover: ENG-RES-0002, -0007, -0009; twolevel: ENG-RES-0008): all four "match the
  artifacts" (rerun_logs/make_tables_*.log).  NB this covers only numbers inside <!-- TABLE --> blocks.
* `own_tail.py` (out_own_tail.txt), exact integer arithmetic:
    T0 Harper's theorem by brute force over all subsets of Q_m, m=2,3,4: min |N(S)| = |N(I_k)| for every k: True;
       N(I_k) is an initial segment for every k, m <= 12: True.
    T1 claim (a) on 3 kinds of random u-Lipschitz landscapes (m = 3..10; 150-3000 trials each; grids u = 1, 7, 1000 units):
       min over all thresholds of m(t e^-u) - d(m(t)) = 0 in every block (never negative; 0 = tight).
    T2 claim (b): random admissible tail functions -> landscape with initial-segment level sets is u-Lipschitz: 0 failures
       in 27 900 constructions (m = 3..10, q = 1, 2, 5 levels per slope).
    T3 exhaustive converse: integer 1-Lipschitz h on Q_m with min 0: #functions 19 / 495 / 197 547 (m = 2, 3, 4);
       achieved level-size sequences = admissible sequences: 5 = 5, 17 = 17, 86 = 86, sets equal.
* RECORD FINDINGS: (i) results/generic_Sc16_ties.json (the evidence for "five exact ties ... none elsewhere") has NO generating
  script on the branch (grep for its keys finds only the two documents that cite it).  (ii) The generic cover table has only a
  Modal entry point (chain_cover_app.py::generic); no local driver exists (run_lattice.py is lattice-only).
  (iii) ENG-RES-0007 cites "job M-006, DEAD_ENDS ED-3" but ED-3 describes the lattice job M-004.

### 20:50-20:57 — step 1e: the "exact ties" of the generic chain, pursued (ENG-RES-0007 left this open)
* `own_ties.py 5 12` (out_own_ties_5_12.txt/.json): off-diagonal (centre, point) pairs with |L*D - (gmin+eps)| < 1e-9 over the
  12 cells: n=5..10: none; n=11: exactly 5, all at L=1, eps=N/2=7, D = 13 (gmin 6); n=12: none.
  nearest non-tie: 5.2105e-4, 2.7114e-4, 1.1553e-4, 1.8238e-5, 4.4733e-6, 3.2482e-7, 1.2734e-7, 2.9286e-8 (n=5..12)
  = their generic_Sc16_ties.json (n=8..12: 1.82e-5, 4.47e-6, 3.25e-7, 1.27e-7, 2.93e-8).  REPLICATED.
  The 5 ties re-evaluated with mpmath at 60 digits from the torsion words: D - 13 = O(1e-60) in all five.
  In MY float64 run all five D are slightly ABOVE 13 (13.000000000000014 .. 37): without the tolerance they would count as
  NOT covered; in theirs one example is 12.999999999999998.  The sign is rounding noise; the exact value is 13.
* WHY (own_ties_structure.py, own_ties_detail.py):
  - every squared distance is a polynomial in c = -cos(theta) with RATIONAL coefficients (PSLQ on 50 digits:
    1-4 trans 5+4c; 1-4 gauche 2+4c+3c^2; 1-5 tt 8+8c; 1-5 g+g+ 7/2+7/2c+9/2c^2+9/2c^3; 1-5 tg 5+8c+3c^2; ...).
    Proof sketch: s_pq = (q-p) + 2 sum b_k.b_l, b_k.b_l = (1,1) entry of a product of rotations; even in sin(theta) (conjugate
    by the rotation by pi about the bond axis) and even in sqrt 3 (mirror image).
  - for the pair tt++t-tt+t- / +t+ttt++t--: 11 of the 66 sorted positions differ; the positive differences sum to
    13/2 + P(c), the negative ones to 13/2 - P(c), P(c) = 21/2 c - 3/2 c^2 - 9/2 c^3 (checked by hand from the PSLQ forms):
    D = 13 IDENTICALLY in c.
  - the same five pairs have D = 13.000...0 (30 digits) at bond angles 110, 110.5, 111, 111.5, 112, 113, 115 degrees, and
    D != 13 at 109 and 109.47 degrees (where the order of the distances changes).
  => the ties are polynomial identities, independent of the "generic" angle; and since cos 69deg has degree 16 over Q while the
     polynomials have degree <= n+1 <= 15 for n <= 14, a profile distance of this chain is RATIONAL at 111 deg only if it is
     constant in the angle (for n <= 14).
* How common (own_integer_distances.py, *_big.py; |D - rint(D)| < 1e-9 over unordered pairs of distinct classes):
  n=5,6,7: 0;  n=8: 1;  n=9: 11;  n=10: 17;  n=11: 65;  n=12: 208   (1-5 e-5 of all pairs); values mostly 13, 15, 17, 19.
  A tie needs D = gmin + eps with eps integer: eps = 0, 1 always, N/2 for even N, N/4 for N = 0 mod 4, N/10 for N = 10.
  (n = 13, 14 running.)
* `own_angle_robust.py 5 12`: the accepted torsion words AND the partition of the words into profile classes are identical
  at 111 deg and at 111 -0.02, -0.007, +0.003, +0.011, +0.03 deg, n = 5..12  => the equalities defining the classes are
  polynomial identities too, not accidents of the angle.  Min gap between distinct distance values: 7.5e-3 (n<=7),
  1.4e-4 (n = 8..11), 5.4e-6 (n = 12).
  (process note: this ran for ~1 minute concurrently with the n=13/14 job - my mistake; no further overlap intended.)

### 20:57-20:59 — n = 13, 14 integer distances; degree of cos 69deg; lattice dual bounds started
* out_own_integer_distances_big_13_14.json (C kernel, nothing stored):
  n=13 (13 012 classes): 581 integer-valued distances; exact ties of the L=1 cover relation: eps=N/4=4: 4;  eps=N/2=8: 253;
       nearest non-tie per cell >= 5.0e-7; nearest non-integer distance 2.8e-8.
  n=14 (27 421 classes): 1566 integer-valued distances; no integer eps besides 0, 1 -> 0 ties; nearest non-tie: 2.06e-8 (eps=N/10),
       5.2e-8 (N/2), 8.1e-8 (N/4); nearest non-integer 8.5e-9.
  => at n = 13 - the next size on engineering's list - 253 (centre, point) comparisons of the N/2 cell sit EXACTLY on the
     threshold, and at n = 14 the nearest non-tie is within a factor 20 of the tolerance 1e-9.  A float treatment with a fixed
     tolerance is at its limit there; exact polynomial arithmetic in c (degree <= n+1) is the clean remedy.
* sympy: minimal polynomial of cos(23 pi/60) has degree 16 (65536x^16 - ... + 1).  With G1 (distances in Q[c], degree <= q-p-1
  <= n+1): for n <= 14 two squared distances (or a distance and 3 or 16, or a profile distance and a rational threshold) are
  equal at 111 deg IFF they are equal as polynomials.  So for n <= 14 every equality met by the floating-point code is an
  identity and every inequality has the recorded margin: the float results of X-004 are exact (label [X*] can become [X]
  for n <= 12 once margins > float error are recorded, which they are: >= 2.9e-8 vs ~1e-13).
* own_lattice_cert.py dual 1 18 (out_own_lattice_dual_1_18.txt): my LP values equal the stored `lp_bound` in every cell;
  my tolerance-free bound equals N_cov (optimality certified without branch and bound) in 198 of 216 cells; the 18 others
  (n=14: 2, n=15..18: 4 each; all L=1, eps in {0, 1, N/20, N/10}) have gap 1 or 2 -> optimality there rests on branch and bound.

### 21:00-21:03 — prose numbers of ENG-RES-0002/-0009; X-006 recount (all from stored files, own code, negligible CPU)
* `check_eng_res_0002_prose.py` (out_check_eng_res_0002_prose.txt): finite-size table (2.45 ... 4.56; 6.64 ... 13.56; 7/8 ... 14/24),
  "four gauche torsions reach ||N||_1 = 166" (166/27 = 6.15; text says 6.1), sequence n=13..24, N_cov/N^2 = 0.100, 0.093, 0.109,
  [0.110, 0.126], effective exponent 4.33 ("4.3"), eps=N/2 sequence, "at most 8" at L=1/5, flip-bound table of ENG-RES-0009
  (36 cases, 0 violated; 21 ... 73; 0.136 ... 0.286), min_j c_j/d_j in [14.5, 21.2]: ALL consistent with the stored files.
* `x006_recount.py` (out_x006_recount.txt): the table of ENG-RES-0008 section 6 reproduced from x006_sampled.jsonl:
  117 cases x 5000 runs = 585 000 at the theorem's K, 0 failures of any kind; scaled K: 82/14 668/29 408/31 698 (u=1/2) etc.
  "below 5.1e-06 at 95 % (pooled)": 1-0.05^(1/585000) = 5.12e-6 OK; per case 6.0e-4; Bonferroni over the 117 cases 1.6e-3.
  literal runs vs mean run at the theorem's K (oracles bottom/top): mean ln(evaluations) - mean-run value in [-0.0006, +0.0019];
  within a case the extreme runs are within [-0.0035, +0.018] of the mean run: at these sizes the cost is essentially deterministic.

### 21:11 — step 2, lattice dual bounds complete (own_lattice_cert.py dual; out_own_lattice_dual_{1_18,19_24}.txt/.json; 764 s)
* 288 cells.  My tolerance-free LP-duality bound (dual solved by HiGHS in floating point, truncated to integers, maximal
  centre load evaluated in exact integer arithmetic on the unreduced matrix):
    - equals the published N_cov in 241 cells: there the published number is an optimum certified WITHOUT any branch and
      bound (stored primal cover checked exactly + exact dual bound);
    - 22 cells published as "proved optimum" rest on branch and bound (LP certificate 1 or 2 below): 18 cells at n = 14..18
      (L=1, eps in {0, 1, N/20, N/10}) and 4 cells at n >= 19 where HiGHS alone ran: (19, N/10) 35 vs 34, (19, N/4) 22 vs 21,
      (20, N/4) 24 vs 23, (22, N/4) 26 vs 25;
    - 25 cells are brackets.  My certified bound equals engineering's stored `lower_certified` in all 72 cells with n >= 19
      (no difference at all), and my LP value equals their `lp_bound` in all 288 cells (max diff 5e-7 = their rounding).
* IS EACH BRACKET WHAT IT SAYS?  Upper end: yes (verified cover, 25/25).  Lower end: ENG-RES-0002 says "a a certified lower
  bound"; in 15 brackets it is (reproduced), in 10 it is the HiGHS branch-and-bound bound after 300 s, one above the certified
  one: (19,eps=0) 52 vs 51; (19,eps=1) and (19,N/20) 42 vs 41; (20,eps=0) 57 vs 56; (20,N/10) 37 vs 36; (21,eps=1) and (21,N/20)
  50 vs 49; (23,eps=0) 74 vs 73; (23,eps=1) and (23,N/20) 60 vs 59.  These 10 lower ends are solver-trusted, not certified.
* own single-flip code `own_flip.c` (brute force, chirality-defined gauche states): c_sf identical to the stored
  lattice_Sc12_flip.json for n = 3, 5, 8, 9 (e.g. n=8: 35 50 56 58 58 56 50 35).  Larger n queued.
* Two-solver test (own formulation, unreduced instance; HiGHS via scipy + CP-SAT via private OR-Tools) started on a sample
  of the 22 branch-and-bound cells.

### 21:11-21:32 — the two-solver sentence, tested (three cells where optimality rests on branch and bound)
* OWN formulation, UNREDUCED instance (own_lattice_opt.py; out_own_lattice_opt_batch1.txt), 120 s per solver, 1 core:
    n=14 L=1 eps=1 (published 25, LP-certified 24):  HiGHS optimal 25 (12.8 s)   | CP-SAT 1 worker: cover 27, bound 6
    n=15 L=1 eps=0 (33, 32):                         HiGHS optimal 33 (6.4 s)    | CP-SAT: cover 38, bound 6
    n=16 L=1 eps=0 (38, 36):                         HiGHS optimal 38 (44.8 s)   | CP-SAT: cover 50, bound 7
* RE-RUN of THEIR functions on THEIR reduced instances (rerun_eng_two_solvers.py; out_rerun_eng_two_solvers.txt), 240 s, CP-SAT with 1 worker:
    n=14: reduced 265x175; min_cover_highs proves 25 in 4.8 s; min_cover_cpsat(workers=1): size 27, not proved, bound 7
    n=15: 450x298; HiGHS proves 33 in 3.8 s; CP-SAT: 39, bound 8
    n=16: 573x364; HiGHS proves 38 in 20.9 s; CP-SAT: 43, bound 7
  (wall 12.5 min for 5 min of CPU: the machine is oversubscribed; my process gets ~40 % of a core.)
* So: the published optima are confirmed by HiGHS in three independent settings (their stored run, my formulation on the
  unreduced matrix, their function re-run here).  "CP-SAT proves them independently" could NOT be confirmed with one worker:
  in 240 s it neither finds the optimum nor gets a bound above 8.  Their runs used 8 workers on 4 cores and (job M-004) no time
  limit, with a code version that is not in the repository; the stored rows record for each solver only the size it found.
* Idea for an independent, tolerance-free proof of such a cell: a small own branch and bound whose every leaf carries the
  exact-integer LP-dual certificate (queued, low priority).

### 21:32-21:40 — RE-RUN of the committed lattice driver; own flips; own class tables to n = 20
* `rerun_engineering.sh <work> lattice_solvers 14` (out_rerun_lattice_solvers.txt): `analyse_table` at a2f6dc7 with solvers
  ("highs","cpsat") regenerates all 12 covering numbers of n = 14 (29, 25, 29, 25, 14, 9 ; 4, 4, 4, 4, 3, 2) and writes
  solvers = {'greedy': ., 'highs': .} (L=1) or {'greedy': .} (L=1/5): CP-SAT IS NOT CALLED IN ANY CELL, whereas the stored row
  has {'highs': k, 'cpsat': k} in all 12 and lacks the certified-bound keys.  => record finding confirmed by execution.
* `own_flip` (brute force): c_sf for n = 10, 11, 12, 13 identical to lattice_Sc12_flip.json
  (n=12: 52 85 92 108 114 114 | sym, the published vector; n=13: 53 89 98 113 132 132 130 | sym; 44 s).
  Together with n = 3, 5, 8, 9: REPLICATED for n <= 13.  (n = 14..16 of their table not replicated.)
* `own_dia_compare.py 18 20`: class tables identical for n = 18 (254 325 043 / 1594), 19 (738 087 517 / 1911),
  20 (2 139 332 335 / 2328); 253 s wall for n = 20.  So own enumerator = their tables for n = 1..20.
* queued: generic covers n = 11 (running), 12; nets; their tests / recheck / run_search; lattice n = 21 (and 22 in chunks).

### 21:40-21:52 — generic covers n = 11 (own); RE-RUNS of engineering code at reduced size
* `own_cover_table.py 11 11 200 <all cells> 0` (out_own_cover_table_11.txt): L=1/5 cells, MILP: 16, 10, 11, 10, 6, 4 = theirs
  (five also certified by my LP bound alone).  L=1 cells, bounds only [my tolerance-free LP bound, my greedy cover]:
  [471,523] [338,388] [378,432] [307,361] [167,208] [85,105]  vs published [474,484] [339,350] [379,392] [308,319] [168,179] [85,90]:
  consistent everywhere; BUT in 5 of the 6 the published lower end is 1-3 above the LP certificate, i.e. it is the HiGHS
  branch-and-bound bound at the 90 s limit, not "the certified lower bound" (the stored file keeps only one "lower").
* RE-RUN `analyse_generic(n)`, n = 5..9 (the function the Modal entry point maps; rerun_logs/generic_cover.log): counts,
  margins, all 12 cover cells (lower, upper, exact), reduced sizes: identical to the stored rows; nearest_tie to 4.5e-14.
* RE-RUN `generic_entropy.py --nmin 5 --nmax 11`: rows 5..11 regenerated identical to stored (all fields but timings).
* RE-RUN `recheck.py --nmax 2000` (rerun_logs/recheck_nmax2000.log): cost: 1008 searches + 504 flat values reproduce the
  stored values exactly without the tie rule (max change 0.0), with it by <= 1.5e-5; claims (240 + 120) and converge (16 + 8):
  0.0 with the tie rule; 0 violations under either convention.
* RE-RUN `run_search.py --u 1 --n 1000 --phi 0.5 0.8` (the stated local command; rerun_logs/run_search.log): flat 1.0405 /
  worst 1.0466 and flat 0.7013 / worst 1.3382; all eight search optima equal the stored ones to the last bit (same numbers
  of evaluations 4002/4002/1950/1950).  54 s here.

### 21:52-21:58 — record numbers traced; partial-shell control; engineering test suite
* `check_record_numbers.py` (out_check_record_numbers.txt), all from stored files with own code:
  M-008: 468 tasks, 5 144 256 instances, 34.8 core-hours, longest task 2241 s; M-009: 180, 1 568 160, 20.7 h, 2147 s;
  M-010: 8, 383 424, 1.1 h, 971 s  (= ledger).  Extremes of the claims table of ENG-RES-0008 section 4 (cost over cap -10.374 /
  -9.433 / -9.402; count (v) -0.052 / -0.051 / -0.051; ...) = stored `extremes`.  Generic timings 389/565/701 s; entropy 25 s
  (n=5..12), 73 s, 334 s; "differ by at most 0.05 ... 0.03 at 13 and 14" (0.049; 0.031); increments 0.0132 (rho=1/2), 0.0134
  (rho=1/4; text says 0.014, from the rounded table), +0.004; 3.1 pairs per bead, +0.12 per bead: all traced.
* PARTIAL-SHELL CONTROL (rerun_eng_partial_shell.py; out_rerun_eng_partial_shell.{txt,json}; engineering's evaluator and search
  re-run with a new instance family): cylinders g(a) = F(|a_{k+1..n_o}|), k = 1, 2, 4, 8, 16, 32 (level sets are not balls of the
  outer cube; law of W = radial law of the (n_o-k)-cube), monotone profiles, both oracles, budget 2000, 6 cells:
     u=1 n=250 phi=.60:  radial (k=0, re-run) 2.0811 = stored;  cylinders 2.0553 (all k)
     u=1 n=1000 phi=.55: radial 1.0401 (stored 1.0402);        cylinders 0.9959 .. 0.9904
     u=1 n=1000 phi=.80: radial 1.3382 = stored;               cylinders 1.2882 .. 1.2632
     u=1/2 n=1000 phi=.55: 1.8285 = stored;                    cylinders 1.8285 (all k)
     u=2 n=1000 phi=.50: radial 0.7723 (stored 0.7726);        cylinders 0.7723 .. 0.7728   (+0.0002 na above the stored worst)
     u=1 n=4000 phi=.50: 0.6941 = stored;                      cylinders 0.6926 .. 0.6939
  158 508 mean runs on cylinders+radial: NO claim violated; largest ln(cost) - ln(C_max) = -10.75.
  => in these cells non-ball level sets of cylinder type never beat the radial worst case by more than 0.0002 na and often
     cost much less (down to -0.075 na): the conclusion of ENG-RES-0008 section 5 survives this control; the cost is NOT
     insensitive to partial shells at the 0.002 na level, though (differences up to 0.075 na, in the favourable direction).
* RE-RUN `python -m pytest tests/eng -q` (with dia_enum/dia_flip compiled from their sources; CP-SAT from the private
  OR-Tools): 128 passed in 11 s (rerun_logs/pytest.log).

### 21:58-22:06 — lattice n = 21 replicated; entropy nets; flips n = 14; report sections 2-7 drafted
* `own_dia_compare.py 21 21`: own enumerator 6 204 141 457 conformations, 2 753 classes, class table IDENTICAL (per class:
  count, gmin, gmax) to data/dia_Sc12_n21.txt, the first of the four tables produced on Modal (job M-002) and not replicated
  by anybody so far (R2 stopped at n = 20).  278 s wall, one core.
* `own_flip -n 14`: 57 92 109 118 137 154 147 | sym = stored (52 s).  => c_sf replicated for n = 3, 5, 8..14.
* `own_lattice_nets.py 0 8 10 12 13 14 16 18 20 22 24` (out_own_lattice_nets.{txt,json}): 50 cells of the entropy table of
  ENG-RES-0002 section 4.  No inconsistency (my certified LB <= published upper, my greedy cover >= published lower, in all 50).
  Of the 40 published single values my tolerance-free LP bound equals 33 (lower side certified; the upper side - a cover of
  that size - is NOT checkable: net covers are not stored); 7 rest on branch and bound (n=10 d=1/4: 43 vs 40; n=12 d=1/4: 65 vs
  60; n=13: 20 vs 19, 55 vs 52; n=14: 25 vs 24, 72 vs 66).  In all 10 brackets the published lower end EQUALS my certified
  bound (25, 98, 29, 104, 33, 146, 38, 141, 41, 186): for the nets "certified lower bound" is accurate.
* web search (2 queries, standard mode) for the two cited theorems: Harper 1966 (bibliographic data confirmed, statement not
  seen), Lehmer 1933 (statement and reference confirmed in snippets).  Logged in the report, section 4.
* wrote `own_certified_bb.py` (+ self-test): branch and bound with an exact-integer LP-dual certificate at every pruned node.

### 22:06-22:14 — certified branch and bound; external control of the conformation totals
* `own_certified_bb.py` self-test (test_own_certified_bb.py): 300 random instances, reduced and unreduced, target = optimum
  -> tree exhausted; target = optimum + 1 -> smaller cover found.  Passed.
* `own_certified_bb_all.py optima 240 14 16` (out_own_certified_bb_optima_14_16.{txt,json}): every pruned node certified by an
  exact-integer LP-dual bound:
     n=14 L=1 eps=1 (= eps=N/10):  >= 25 PROVED, 598 nodes, 3.7 s
     n=15 L=1 eps=0 (= N/20):      >= 33 PROVED, 99 nodes, 1.6 s
     n=15 L=1 eps=1 (= N/10):      >= 27 PROVED, 12 nodes, 0.2 s
     n=16 L=1 eps=1 (= N/10):      >= 30 PROVED, 8 nodes, 0.3 s
     n=16 L=1 eps=0 (= N/20):      target 38 (LP 35.56, gap 2): NOT finished in 240 s (11 226 nodes)
  With the stored covers (primal-checked) these 8 cells are now optima certified without any MILP solver.
  n = 17..22 running (240 s cap per distinct instance).
* EXTERNAL CONTROL (check_saw_counts_oeis.py): the total number of conformations of every class table n = 1..24 equals
  A001394(n+2)/12, A001394 = number of n-step self-avoiding walks on the diamond lattice (OEIS b-file fetched today;
  [full text of the b-file through a page-reading tool]).  In particular the four Modal-produced tables:
  n=21: 74 449 697 484/12 = 6 204 141 457; n=22: 215 677 847 460/12 = 17 973 153 955; n=23: 625 096 195 404/12 = 52 091 349 617;
  n=24: 1 810 062 340 812/12 = 150 838 528 401.  The engineering register does not use this control (it validates counts
  against P_REPORT up to n = 13 only).  It checks totals, not the split into classes.

### 22:14-22:47 — certified branch and bound on all 22 cells that rest on a solver's search (240 s cap per distinct instance)
* out_own_certified_bb_optima_{14_16,17_24}.{txt,json}, tally in out_own_certified_bb_tally.txt.
  PROVED with exact certificates (13 cells, 8 distinct instances): n=14 eps=1 & N/10 (25; 598 nodes); n=15 eps=0 & N/20 (33; 99),
  eps=1 & N/10 (27; 12); n=16 eps=1 & N/10 (30; 8); n=17 eps=1 & N/20 (34; 493), N/10 (28; 225); n=19 N/4 (22; 8); n=20 N/4 (24; 207).
  NOT finished in 240 s (9 cells, 7 distinct instances): n=16 eps=0 & N/20 (38); n=17 eps=0 (43); n=18 eps=0 (48), eps=1 & N/20 (39),
  N/10 (31); n=19 N/10 (35); n=22 N/4 (26; the reduction alone took ~9 min with integer matrix products - my implementation).
  => 241 + 13 = 254 of the 263 published single covering numbers are optima certified without any solver's search;
     9 remain HiGHS-only.
* (a waiter command hit its background limit and was stopped by the harness; the computation itself was unaffected.)
* running now: own bounds for the generic table at n = 12; then own lattice enumeration n = 22 (single run, ~14 min).

### 22:47-22:54 — generic n = 12 (bounds only); entropy-growth remark; report sections filled
* `own_cover_table.py 12 12 0` (out_own_cover_table_12.txt; 5.7 min): tolerance-free LP certificate and greedy cover, no MILP.
  L=1: [755,861] [551,642] [603,697] [483,569] [250,318] [109,143]  vs published [757,788] [552,595] [605,645] [484,526] [251,284]
  [109,136]: consistent; published lower ends above the certificate by 2, 1, 2, 1, 1, 0.
  L=1/5: certificates 20, 13, 15, 11, 6, 4 vs published exact 21, 13, 15, 11, 6, 4: lower side certified in 5 cells; no cover of
  the published sizes constructed (greedy 26, 18, 20, 15, 7, 5) -> n = 12 is "consistency only", NOT replicated.
  Per-cell nearest-tie values = stored ones (3.209e-05, 2.108e-05, 3.650e-05, 6.348e-06, 2.535e-06, 3.965e-06, 2.929e-08, ...).
* `check_entropy_growth.py`: with the finite-size-consistent form g_n exp(n sigma_n - (n+1) sigma_{n+1}) the growth prediction
  at eps = N/2 is 1.79, 1.70, 1.15, 1.20, 1.26, 1.31, 1.27 vs measured 1.67, 1.40, 1.62, 1.26, 1.40, [1.42,1.50], [1.21,1.60]
  (no systematic over-prediction); at eps = N/4 still 10-30 % above.
* In x005_cost.jsonl some searched instance costs more than the flat one (max over both oracles) in ALL 468 cells
  (by > 0.001 na in 419; largest excess 1.10 na) - corrected in the report (I had written 464).
* n = 22 lattice enumeration running (single run, ~14 min of CPU).

### 22:54-23:12 — lattice n = 22 replicated; margins for n = 13, 14; ties in the entropy table; Section 1 inserted
* `own_dia_compare.py 22 22`: own enumerator 17 973 153 955 conformations, 3 319 classes, class table IDENTICAL to the Modal
  table data/dia_Sc12_n22.txt (867 s on one core, single run).  => own enumerator = engineering tables for n = 1..22.
  n = 23, 24 not run (about 40 min and 2 h of one core in prefix chunks).
* `own_gen.py 14` (out_own_gen_14.txt): min gap between distinct distance values 5.4e-6 (n=12), 2.8e-6 (n=13), 8.6e-7 (n=14);
  max spread inside a cluster <= 3.6e-14; smallest |s - 3| 0.020 (n<=13), 6.3e-3 (n=14).  `own_stats.py 13 14`: min gap to the
  cutoff 0.0114; pairs per bead 2.98/2.73/5.69 and 3.10/2.80/6.18 = ENG-RES-0009.
* `own_entropy_ties.py 5 14` (out_own_entropy_ties_5_14.json): exact ties in the entropy comparisons D <= rho N (unordered
  pairs): n=9: 3 (rho=1.25); n=10: 8 (rho=1); n=12: 48 (rho=1); n=13: 13 (rho=1/4) + 13 (rho=1); n=14: 220 (rho=1); none for
  n<=8 and n=11.  Nearest non-tie >= 3.4e-8.  Both codes count them as inside (tolerance 1e-9) = exact answer; ENG-RES-0009
  does not report them ("the tie analysis of ENG-RES-0007 applies" - that one is about the cover relation only).
* `insert_section1.py 254 9 ...`: Section 1 (verdict paragraph, 30-row verdict table, classified findings, "what is missing")
  inserted into the report.  (The harness refused a Write of a separate draft .md file; the section text lives in the
  inserter script.)

### 23:12-23:20 — final state
* Report: `docs/science/workstreams/R7_REPORT.md` (sections 1-7 complete; section 1 is generated by `insert_section1.py`
  with the final counts 254 / 9).
* Files in this directory: own code `own_*.py`, `own_*.c`, `l1kern.c`; checks of their record `check_*.py`, `x005_refit.py`,
  `x006_recount.py`; re-runs of their code `rerun_engineering.sh`, `rerun_eng_two_solvers.py`, `rerun_eng_partial_shell.py`
  (all operate on an export of commit a2f6dc7 OUTSIDE the repository); outputs `out_*`, logs `rerun_logs/`;
  `make_eng_copy.sh` re-creates the git-ignored `eng_copy/` that the read-only scripts use.
* Compiled binaries `own_dia`, `own_flip`, `l1kern.so` are regenerable (commands in the report); `own_dia` and `own_flip`
  were picked up by a snapshot commit of the coordinator - they can be dropped from the branch.
* Not mine: an untracked `NOTES.md` at the repository root (created 22:48, content of workstream R8).
* Process notes: (1) two overlaps of my own computations (about 4 s at ~20:27 and about 1 min at ~20:56) against the
  one-core rule; (2) one `until`-loop waiter was stopped by the harness at its background limit (no computation lost);
  (3) the harness refused a Write of a draft .md file - no content lost; (4) no git state was changed; `lake` not run;
  no Modal job; no file outside `ws_R7/` and the report was written by me (re-runs wrote into the scratchpad work tree).
* Not done (stated in the report, section 5): class tables n = 23, 24; flips n = 15, 16 and the envelope-validity test;
  CP-SAT proofs; nine HiGHS-only lattice optima; generic n = 12 upper ends; X-006 re-run; X-001; ENG-RES-0006 section 2.
