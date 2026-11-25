# Workstream R2 — notes (SCI-REV-0002: review of theory report §11.22)

Running log, newest at the bottom.  Labels as in COMMON.md rule 6.

## 2026-11-25 17:40 UTC — start

* Read `docs/science/workstreams/COMMON.md` and `R2_brief.md`.
* Created `experiments/science/ws_R2/`.
* Plan (order matters: authors' code is read only AFTER my own enumerator exists):
  1. Read §11.22, §11.17 (definitions, Prop 11.49), S_REPORT.md, DEAD_ENDS D46/D48,
     SetLimit.lean, CoverStability.lean, engineering messages + data.
  2. Write my own diamond-lattice enumerator (walks, bridges, profile = pair counts per shell
     + gauche count); compare counts with engineering tables.
  3. Re-derive Lemma 11.67 (site-set reduction) and 11.68 (concatenation), test finite
     inequalities exhaustively at small N.
  4. Re-compute computer-assisted numbers (outer polytope/dual certificates, 50, 3627, 26437,
     N^{-1/3} rate).
  5. Check Lean hypotheses vs what the lattice lemmas deliver.
  6. Scientific reading; originality paragraph.

## 17:55 — first reading done (§11.22 lines 4692–5083, §11.17 lines 3203–3526, S_REPORT whole)

Statements under review (numbering of the theory report): Lemma 11.67, Lemma 11.68, Theorem 11.69,
Lemma 11.70, Theorem 11.71 (a)(b)(c), Proposition 11.72 (a)–(e), Proposition 11.73,
Proposition 11.74, Conjecture 11.75 (i)–(iv).

Hand re-derivation while reading (before any code), all [P, re-derived by me, not yet numerically tested]:
* 11.68 counting: with S = S1 ∪ Λ ∪ S2 and no S1–S2 pair within cutoff (height gap >= 4),
  δ3 = [e3(Λ,S1)−1]+[e3(Λ,S2)−1], δ8 = [e8(Λ,S1)−2]+[e8(Λ,S2)−2], δ11 = e11(Λ,S1)+e11(Λ,S2)
  (I re-did the bookkeeping: e3(Λ)=2, e8(Λ)=1, e11(Λ)=0, N=N1+N2+3) — agrees.
  Upper bounds by heights: e3(Λ,S1)<=2, e3(Λ,S2)=1; e8(Λ,S1)<=4+4, e8(Λ,S2)<=1+4; e11(Λ,S1)<=6+2+2,
  e11(Λ,S2)<=2+2  -> (1,9,14) OK.  Norm 9+36+14+1 = 60 OK (all δ>=0 so cumulative norm = weighted sum).
* 11.69 application: Q_M = P_{M-3}, M>=6; (C): (M1-3)+(M2-3)+3 = M1+M2-3 OK; R=36 since
  9h3+4h8+h11 <= 9(N-1)+4(5N-2)+6N <= 35N and g <= N-3.  168 = 60 + 3*36 OK.
* 11.73: 3∂ >= 2Σρ_f, Loomis–Whitney, e3=(4N-∂)/2 -> e3 <= 2N - 2^{-2/3}N^{2/3} OK;
  e8 via fcc lines OK; 9*2^{-2/3}+12 = 17.67 OK; +17 = 9+8 OK.
* 11.71(b) lower-bound mechanism (no centre covers two clients) OK; upper bound (maximal
  separated set is an internal net; volume count) OK.

Things to test / questions raised so far:
 Q1. Lean hypotheses: is Q_M required for all M>=1 / non-empty?  (bridges need M>=6)
 Q2. "the plateau … at (1,1/2)": convergence is only off a countable set of ε1; nothing shows
     ε1=1/2 is not a jump, even for bridges.  So "plateau" = bracket for liminf/limsup only.
 Q3. 11.71(c) table: which columns are theorems (26 437; 3 627; 50; >=26/>=35) and which estimates.
 Q4. 11.72(c) is a limit statement without finite-N constants; 3 627 depends on it (3 719 without).
 Q5. "reached at 10^3–10^5 beads" has no theorem behind it.

## 18:10 — read DEAD_ENDS D46/D48, SetLimit.lean, CoverStability.lean, ENG-REQ-0001, ENG-RES-0002

Lean hypotheses vs use (review by reading; Lean not run yet):
* `SuperAdditive Q β β' R` quantifies `add`, `succ`, `bound` over ALL M : ℕ, and
  `SuperAdditive.hausdorff_limit` / `cover_sandwich` need `hne : ∀ M ≥ 1, (Q M).Nonempty`.
  The application takes Q_M = P_{M-3} for M >= 6 only.  With Q_M := ∅ for M<6 `hne` fails; so the
  machine-checked theorem does not literally apply.  (The paper proof, S Lemma 3.3, is stated for
  M >= M0 and is fine.)  Patch to test: Q_M := {0} for 1<=M<=5 (then need: appending k<=5 beads
  to a bridge costs norm <= 60; my hand count gives <= 9+24+10+1 = 44).  MINOR.
* `scaled Q M` = Q_M / M, i.e. division by N+3, not N.  The +3 conversion (3R/(N+3)) and, for the
  covering statement, the accuracy shift ε1·N/(N+3) are paper steps outside Lean.  MINOR.
* `cover_sandwich` uses the product (max) norm on V×ℝ; paper constants are for the sum norm
  ‖p‖_c+|g| — harmless (max <= sum).
* HasCover = internal centres (first components of clients), |A| <= k: matches N(F,ε).
* (c) right-continuity and (d) the limit statement are not in Lean (the report says so: "P").
* `upper F` is the untruncated epigraph — irrelevant for covers.

Engineering class-table format (data/dia_Sc12_n{n}.txt): rows "h3 h8 h11 | count | gmin |
count_gmin | gmax"; conformations counted with the first two bonds fixed (233 at n=5).
Did NOT read dia_enum.c (will write my own enumerator first).

## Enumerator written and validated (own code, written before reading any other enumerator)

* `r2_enum.c` (walks / bridges, first two bonds fixed; pair counts accumulated from the
  definition by look-up of ALL integer vectors of squared norm 3, 8, 11; gauche by the 1-4
  distance).  `cmp_tables.py`: my class tables (count, gmin, count_gmin, gmax per class) are
  IDENTICAL to the engineering tables for N = 4..22 (n = 1..19; 7.4e8 conformations at N=22);
  N = 23 running.  Conformation and class counts as in ENG-RES-0002.
* `r2_lemma67.py` (pure Python, O(N^2) definition): Lemma 11.67 (h = e(S) − chain pairs; the three
  local counting formulas; index rule == distance rule for gauche) holds for every walk with
  N <= 12 (17 107 walks at N=12) and the local formulas on 3000 random finite site sets.  Class
  tables of the Python enumeration == C enumeration (N<=12).
* Bridges (own): N=3..18: 1,2,5,12,29,78,201,536,1433,3824,10341,28042,76359,208832,572351,1574740
  (canonical: first two bonds fixed); classes 101/280/656 at N=12/15/18 as in S_REPORT §5.4.
  S's "508 bridges with 3<=N<=8 starting on an A site" = 4 x (1+2+5+12+29+78) = 508.  OK.

## Lemma 11.68 (concatenation) — own exhaustive test `r2_concat.c`

* All ordered pairs of canonical bridges with 3..10 beads (746 496 pairs, 856 224 concatenations
  incl. both choices of c1 when b' is down): symmetry unique in every case, result always a
  self-avoiding lattice bridge with N1+N2+3 beads, δ in [0,1]x[0,9]x[0,14]x{0,1}, δ_g = [b' down]
  in every case; observed maxima (0,3,6,1), largest norm 19.  (N<=13 and (16,8),(8,16) running.)
* `r2_concat_bounds.py`: the constants by counting lattice sites by height: (1,9,14), β=60;
  one bead (1,3,6), β'=28; appending k<=5 beads: norm <= 44 (so Q_M:={0} for M<=5 repairs the
  Lean hypothesis `hne` with the same β=60).  F1, F2 confirmed (shell sizes by height).

## Tables: finite inequalities (`r2_tables.py`, out/tables.txt)

* Prop 11.72(a) holds on every class, N=4..27 (eng tables for 23..27).
* Prop 11.72(b) walk form c.h <= bN+4M+c3+2c8 holds for the 11 rows on every class, N=4..27.
  (Observation: max(−h3+h8−h11) = 0 exactly at every N, i.e. h11 >= h8 − h3 for all walks N<=27.)
* Prop 11.73: 9h3+4h8+h11 <= 35N − 17.6N^{2/3} + 17 holds (far from tight); k_N in [1.710,1.862]
  for N = 8..27 (claimed 1.71..1.86: confirmed); 38.7 % of the bulk extent at N=27 (claimed 38 %).

## Site-cluster LP, Prop 11.72(b) — own formulation and own exact certificates (`r2_lp_site.py`)

* My derivation: oriented bonds, mu = nu/(4N); identities and the symmetrised constraints (12
  cluster symmetries; S4-invariance of the star marginal) checked exactly on 60 random site sets.
* LP values (HiGHS) equal b+c3+c8 for all 11 rows.
* For each row I found my own multipliers (integers except one row) and verified in exact
  rational arithmetic on all 45 non-empty orbits: allowed orbits <= 0, forbidden <= M_mine with
  M_mine <= the table's M (often smaller: 0 instead of 5, 6, 6, 1; 247/288 instead of 3).
  => Prop 11.72(b) REPLICATED with independent code and independent certificates.

## Results in (walks N=23; concatenation N<=13; bridges; volumes; marked LP)

* Walks N=23 (2 139 332 335 conformations, 2 328 classes, 323 s): class table IDENTICAL to the
  engineering table n=20.  So: own enumeration == engineering tables for all N = 4..23.
  N = 24..27 (n = 21..24) NOT replicated (only read; 6e9..1.5e11 conformations).
* `r2_concat` exhaustive: ALL ordered pairs of bridges with 3..13 beads: 270 997 444 pairs,
  307 987 558 concatenations (both c1 where b' is down): 0 failures; symmetry unique always;
  δ_g = [b' down] always; observed maxima (1,6,8,1), largest norm 41.
  N1<=16, N2<=8: 41 871 265 pairs, 0 failures, maxima (1,6,9,1), norm 43.
  NOTE: δ3 = 1 DOES occur (460 936 concatenations at N<=13) — the report's/authors' "observed
  maxima (0,2,4,1)/(0,2,5,1)" understate it; the constant δ3 <= 1 is attained.
* `r2_bridge_tables.py`: my bridge tables == authors' stored tables (classes, gmin, gmax, gmask)
  for N = 4..21 (their counts are exactly 2x mine: convention).  Set-level (C): 13 069 pairs of
  points, 0 failures; (E): 17 971 points, 0 failures.
* `r2_volumes.py`: K1: 12 vertices as listed, volume 697/216 = 3.226852; K2: 12 vertices as
  listed, volume 25/8 = 3.125 exactly; K2 ⊂ K1; all rows are facets.
  Bounds vol(u(X)+B1(r/2))/vol B1(r/2):
     bulk box  26437.00  191833.00  392.20  2194.60   (report: 26 437, 191 833, 392, 2 195)
     K1         3719.33   23935.67   93.95   400.73   (report: 3 719, 23 936, 94, 401)
     K2         3626.50   23272.00   92.50   392.80   (report: 3 627, 23 272, 93, 393)
     K1^(100)   4673.16   30525.89  111.16   488.42   (report: 4 673, 30 526, 111, 488)
     K1^(1000)  3809.31   24554.69   95.60   409.08   (report: 3 809, 24 555, 96, 409)
  REPLICATED.  (Remark: the table rounds to nearest, sometimes up; as bounds on an integer the
  floors 3626, 2194, 92, 392 would also be valid.  Harmless.)
  Steiner check: vol(K2+ρB1) = 46.875 + 105ρ + 38.5ρ² + (4/3)ρ³.
* `r2_lp_marked.py`: my own formulation of the marked programme: 340 configurations (339
  non-empty), 47 orbits, 13 star relations; modelling tested exactly on 25 random walks (ends
  handled as separate star patterns).  LP values = claimed b for the twelve rows of K2 and
  8, 7, 7 for the three gauche functionals; own integer certificates verified exactly on all
  orbits for all 15 statements.  => Prop 11.72(c) REPLICATED (as a limit statement).

## Lamellae, packings (own constructions)

* `r2_lamella.py`: own snake-order construction of rung-folded lamellae; every walk verified from
  coordinates (lattice walk, injective, bridge); (h,g) three ways (O(N^2) definition, look-ups,
  numpy site-set count) agree.  One row of stems: (h,g)/N -> (1/2,2,3/2;0), e.g. M=151,l=160,
  N=48 174: (0.4920,1.9710,1.4821;0.0093), g = 3(M-1) exactly.  Crystal 25x25x26, N=31 880:
  (0.9215,4.6088,5.4768;0.0587) — IDENTICAL to the authors' stored value (out/lamella.txt quoted
  in S_REPORT §4.2); 31x31x32, N=60 548: (0.9364,4.6832,5.5756;0.0476).
  (1-h3/N)N^{1/3} = 2.45..2.51; k = 2.43..2.54 ("lamellae: k ≈ 2.5": confirmed);
  distance to the crystal vertex (norm ||.||_c+|g|) ≈ 87..91 N^{-1/3} (lower bound 17.6 N^{-1/3}).
  |h − formula of Prop 4.3|/(MQ) bounded (≈ 2.9, 12.6, 14.3): consistent with "+O(MQ)".
* `r2_packing.py A`, `r2_packing_fine.py`: packings in T0, verified pairwise in exact rationals:
  51 / 158 / 7 / 15 points for (1,1/2) / (1,1/4) / (1/5,1/2) / (1/5,1/4)
  (report: 50 (52) / 157 (162) / 7 / 14).  REPLICATED (>= claimed in all four cases).
  (`r2_packing_hex.py`: a lattice packing gives only 40 at (1,1/2): the triangle is thin and
  boundary-adapted greedy packings are better.)
* `r2_packing.py B`: explicit bridges with exactly N beads (my lamellae + all-trans tail), exact
  integer check of L||h_i-h_j||_c > g_i+g_j+2 eps1 N:
      N        27  60  120  250  500  1000
   (1,1/2)      3   6   10   18   22    26     (report 3 6 10 17 22 26)
   (1,1/4)      4  11   19   30   44    55     (report 4 11 19 31 43 53)
   (1/5,1/2)    1   2    3    4    5     5     (report 1 2 3 4 5 5)
   (1/5,1/4)    2   3    5    6    8    10     (report 2 3 5 6 8 9)
  REPLICATED with an independent family (N = 2000, 5000 running).

## Review thoughts so far (no mathematical error found yet in 11.67–11.73)

* 11.72(a): the report's parenthesis "C(d,2) <= 3d/2" alone does not give h8 <= 2h3+3N+3
  (it gives e8 <= 6N); the full proof (S Prop 4.1) uses C(d,2) <= (5d-8)/2 on occupied sites
  (+3/2 for the at most two sites with d=1).  Statement true (checked N<=27).  MINOR.
* "𝒦 is a compact convex BODY": non-empty interior needs a point off the plane of T0.  Easy:
  the all-gauche 4_1 helix (bond indices 0,1,2,3,0,...) is monotone in y, hence a bridge, with
  h=(0,0,N-3), g=N-3: (0,0,1;1) in K^br.  So K^br ⊇ conv(T0x{0}, (0,0,1;1)), vol 𝒦 >= 1/12 PROVED;
  the report's "2.2 ≲ vol 𝒦" rests on the routing sketch (flagged there, but then used in the
  sentence "a thin body, 7 to 10 % of the bulk box").
* Headline sentence mixes labels: "the plateau lies between 50 and 3 627 … and is reached at
  10^3–10^5 beads".  Theorem: 50 <= liminf, limsup <= 3 627 (walks), <= 26 437 all N, >= 26 at
  N=1000.  Conjecture-dependent: existence of a limit ("plateau") for walks (Conj 11.75', and ε1
  non-exceptional); even for bridges ε1 = 1/2 might be a jump.  Estimate: "150–350", "hundreds",
  "10 to 40 times the values at 27 beads", "reached at 10^3–10^5 beads".

## Covers, flips, walks-vs-bridges, finite sets, witnesses (all own code unless stated)

* `r2_cover.py` (MILP, exact integer cover relations): walks N^P_cov(N/2), L=1: 3,5,5,8,9,11,13 at
  N=8,11,12,15,18,21,23 (= ENG-RES-0002 table; "8 and 11 at 15 and 21 beads" of §11.22 confirmed);
  N=15 with the weighted norm: 10 (D48 confirmed); eps=0: 21; L=1/5: 2; eps=N/4: 13 (N=15), 19 (N=21).
  Bridges (clients and centres bridges): eps=N/2: 5,6,8,10,11 at N=12,15,18,21,23; eps=N/4: 7,11,14,17
  at N=12,15,18,21 (= S_REPORT §5.4 table).  N=27 from the engineering table: running.
* `r2_flip.py`: hairpins t^a(+-+)t^b vs the middle fold torsion opened, 3<=a,b<=40 (1444 pairs, all
  self-avoiding): D − 14d ∈ [−15,−5]; periodicity D(a+2,b+2)=D(a,b)+28 (a,b>=5), D(a,b+2)=D(a,b)
  (b>=a+6).  Engineering exact constants (n<=16) satisfy 14d−15 <= c_j <= 70(d+3) for all d_j>=5.
  Upper bound re-derived by hand (moved arm has d_j beads; per bead cumulative changes <= 2,12,24,
  crude 4,16,28 for the two exceptional beads; the +3 absorbs them).
* `r2_walk_vs_bridge.py`: reproduces S_REPORT §5.4 exactly where I have data (N=12: 6,4,4,3 | 8,5,5,4;
  N=15: 6,4,3,3 | 7,7,6,6; N=18: 7,6,5,5 | 10,9,10,10; N=21: 5,6,5 | 7,7,5), once the lower-boundary
  distance is taken one-sided (||dh||_c + max(0, gmin_bridge − gmin_walk)) as in their code.
  walks(N)->bridges(N+1): 3..6 units for N = 11..22 (claim confirmed; N=23 needs bridges N=24).
  Remark: "covering numbers of bridges equal those of walks two to three beads shorter" is
  roughly right: 0–3 beads (bridges 21: 10 = walks 19, 20).
* `r2_finite_sets.py`: Prop 11.72(b) with n_E and Prop 11.73 (e3, e8 isoperimetric bounds) on all
  65 535 subsets of a 16-site piece, 4000 random subsets of a box, 3000 random animals, compact
  sets up to 3059 sites: no violation.  Observed min (2N−e3)/N^{2/3} = 1.657 (proved 0.630),
  min (6N−e8)/N^{2/3} = 6.0 (proved 3): the proved constants are not tight.
* `r2_rodpairs.py`: pairs per period between parallel rods: (1,4,3) at ±(1,0), ±(0,1); (0,2,4) at
  ±(1,−1); (0,0,2) at ±(1,1); none elsewhere (as in S §4.2).  All-gauche 4_1 helix (bond indices
  0,1,2,3,…) is a bridge with (h,g) = (0,0,N−3; N−3): so (0,0,1;1) ∈ K^br [new, trivial].
* `r2_verify_witness.py big`: the 166 199-bead bridge REGENERATED with the authors' builder
  (imported read-only, no bytecode written) and VERIFIED with my code: self-avoiding lattice
  bridge, (h3,h8,h11,g) = (1717, 376013, 687789, 131710), 2h11−5h3−8N = 37 401 = 0.22504N;
  with 168/(N+3) = 0.001011 and the 2-Lipschitz functional: γ(p*) >= 0.2230 (report: 0.22). OK.
* `r2_verify_witness.py nine 64`: the nine finite bridges of S §4.2 at box 64 regenerated and
  verified by my code: all nine (N, h, g) identical to out/build.txt.
* `r2_inner_volume.py`: RIGOROUS inner volume: hull of {T0 vertices, helix point, 10 verified finite
  bridges} eroded by delta = 0.01395 (support-function argument): vol 𝒦 >= 1.563 (5.2 % of the
  bulk box).  The report's "2.2 ≲ vol 𝒦" rests on the routing sketch; proved bracket is
  1.56 <= vol 𝒦 <= 3.125.
* `r2_rigorous_packing.py` (first run, coarse grid): packings in the hull of PROVED points of K^br
  with gauche credits and uncertainty margins, exact rational verification:
  77 / 323 / 7 / 16 for (1,1/2) / (1,1/4) / (1/5,1/2) / (1/5,1/4).  So the proved lower bound for
  the liminf at (1,1/2) improves from 50 to >= 77 (refinement running).
* Coordinator checks (out_s_check1..7) read AFTER my own results: all numbers agree with mine.
  Their concatenation check is much smaller (pairs <= 7 beads + 3000 random) than mine.

## Late results

* Lean (`R2Axioms.lean`, `lake env lean`, 2 min 23 s, nothing built): the eight cited declarations
  exist with the signatures I read, and depend only on [propext, Classical.choice, Quot.sound].
* `r2_rigorous_packing.py` (fine grids; T0 grid added): packings in the hull of the 14 PROVED points
  of K^br with gauche credits and uncertainty margins, exact verification:
     (1,1/2): 116   (1,1/4): 451   (1/5,1/2): 8   (1/5,1/4): 19     [report: 50, 157, 7, 14]
* `r2_cover.py eng 27 1 1 1 2`: 15 (optimal, 695 s) from the engineering table (the table itself is
  not replicated); L=1/5: 2.
* Bridges N=24: 712 195 212 canonical bridges, 2 350 classes (323 s … 1088 s under load).  My bridge
  tables == authors' for all N = 4..24.  Set-level (C): 81 519 pairs of points, (E): 49 204 points,
  0 failures.  walks(N)->bridges(N+k) now complete to N=23: identical to S_REPORT §5.4
  (N=21: 5,6,5,4 | 7,7,5,7; N=23: 7,5 | 7,7).  Bridge cover N=24, eps=N/2: 11.
* `r2_packing.py B`: N=2000: 32, 68, 6, 11 (report 31, 64, 6, 10).  The first run for 5000 was
  killed (my n x n x 3 distance tensor: 3.5 GB) -> rewritten with on-the-fly checks (same results at
  27, 250, 1000; exact re-verification added); 5000 running.
* Report draft written: docs/science/workstreams/R2_REPORT.md.
