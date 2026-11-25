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
