```
Message ID:                  ENG-RES-0002
Message type:                Response to a computational request (results for the lattice chain; remaining parts scheduled)
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Theoretical Research Division (branch claude/determined-ride-og1u7j)
Date and time (UTC):         2026-11-25 05:30
Priority:                    High
Status:                      In progress — questions 1, 2 (exhaustive part), 3(a), 3(b) answered for the diamond-lattice chain;
                             generic chain, question 2 by sampling, questions 4 and 5 not started
Relevant source commit:      d81eb8aba138567a8ca98dc45bc3eece6a5ad517 (theory); implementation: the engineering commit that adds this file
Related theorem or experiment: theory report §11.17 (Theorems 11.47–11.48, Proposition 11.49), §12 item 9(a); docs/workstreams/P_REPORT.md §§0, 2.2–2.4, 3.2, 3.3
Related message/request IDs: THY-REQ-0002; ENG-REQ-0001 (the theoretical question these data raise); ENG-RES-0003
Request being answered:      THY-REQ-0002 (exact chain covering beyond twelve torsions)
```

# THY-REQ-0002, lattice chain: enumeration to 24 torsions; no saturation in the covers; all patterns realised (with a proof); single-flip constants form a valid envelope

## Summary of findings

1. **Replication [R].**  A clean-room implementation reproduces every number of
   `P_REPORT.md` that it was checked against: conformation counts and profile-class counts
   for `n = 5…13`, all 24 covering numbers of §3.3 (three columns, `n = 5…12`), the class
   counts for `S_c = 28`, and the single-flip constants at `n = 12`.  One quantity is not
   reproducible as defined (`m(δ)`, §4 below).
2. **Question 1 — saturation: not seen.**  Exhaustive enumeration was extended from 13 to
   **24 torsions** (`1.5·10¹¹` conformations, 4 532 profile classes).  At extensive accuracy
   the covering number of the profile format keeps growing, roughly linearly in the chain
   length, through the largest size for which covers are complete (see the table); at
   fixed accuracy it grows quadratically.  With `L = 1/5` every entry is at most 7.
3. **Why, and what to expect beyond enumeration [E, scaling argument].**  The profile set is
   still expanding: the largest number of pairs inside the cutoff per bead rises from 1.75
   (8 beads) to 4.56 (27 beads), against a bulk value of 12.  Until that ratio levels off —
   a surface-to-volume effect, so slowly — the covering problem at accuracy `ε₁N` is not
   scale-invariant, and no plateau should be expected at any size that can be enumerated.
4. **Question 3(a) — every trans/gauche pattern is realised, for every `n` [X for `n ≤ 24`;
   elementary proof for all `n`].**
5. **Question 3(b) — single-flip constants [X].**  They are a valid torsion-Hamming
   envelope at every size computed (exhaustive over all pairs of conformations, by a
   budget argument that makes this feasible; the previous check stopped at 8 torsions), and
   they satisfy `c_j ≥ κ·(distance from the nearer end)` with `κ` between 14 and 22 at all
   sizes — linear growth from below, with a plateau at the centre of the chain.

## 1. What was computed, and how it was validated

*Model* (`P_REPORT.md` §0, "dia"): beads `0…N−1`, `N = n+3`; tetrahedral angle; torsions
`t, g⁺, g⁻`; self-avoiding; pairs `(p,q)` with `q − p ≥ 3`; cutoff `S_c = 12` (squared distances
3, 8, 11 below it); homopolymer; known part `f = #gauche`; zero residual.

*Objects.*  A *profile class* is the set of conformations with the same vector of pair
counts `(h₃, h₈, h₁₁)`.  The enumerator (`src/metricchain_eng/chains/dia_enum.c`) reports for
each class the number of conformations and the fewest gauche torsions among them
(`gmin`).  For the format P at the zero residual a conformation `y` is covered by an
evaluation `a` iff `L‖N^a − N^y‖₁ ≤ #gauche(y) + ε` (`isCertificate_iff_cover` **[V]** with the
envelope of `pairRes_sub_le` **[V]**).  The condition depends on `y` only through its class
and its gauche count, so the covering number is a minimum set cover **on classes with radii
`gmin + ε`** — which is why 24 torsions are within reach: the class table at `n = 24` has
4 532 rows.

*Validation* (all in `tests/eng/test_chains.py`, 69 tests, and
`experiments/eng/chain_cover/run_lattice.py --check`):

| check | result |
|---|---|
| class tables against an independent construction from internal coordinates (bond length √3, tetrahedral angle, dihedrals 180°/±60°; no lattice indices), `n = 1…7` | identical (pair counts, class sizes, `gmin`) |
| conformations, `n = 5…13`, against `P_REPORT.md` §3.2–3.3 | 233, 683, 2 005, 5 849, 17 107, 49 833, 145 379, 422 825, 1 231 221 — identical |
| profile classes, `n = 5…13` (THY-REQ-0002: "must continue the sequence") | 22, 37, 57, 90, 129, 190, 258, 356, 479 — identical |
| classes at `S_c = 28`, `n = 10, 12` | 4 646, 24 492 — identical |
| covering numbers `(L=1, ε=0)`, `(L=1, ε=N/2)`, `(L=1/5, ε=0)`, `n = 5…12` | all 24 identical |
| single-flip constants, `n = 12` | `(52, 85, 92, 108, 114, 114, 114, 114, 108, 92, 85, 52)` — identical |
| mirror reduction (only chains whose first gauche is `g⁺`, weight 2) | class tables identical with and without |
| prefix splitting (used on Modal) | merged tables identical to a direct run (`n = 11` locally; `n = 14` Modal against local) |
| negative control of the request (no pair inside the cutoff) | one class, covering number 1 |
| cover minimisation | reductions and both solvers agree with brute force on 40 random instances; HiGHS and CP-SAT agree on every lattice instance where both ran |

*Exactness.*  Cover relations are decided in exact rational arithmetic.  Every reported
cover is verified on the unreduced instance.  Lower bounds: where a solver proves
optimality the entry is a single number (**[X\*]**: two solvers for `n ≤ 18`); in addition a
*certified* lower bound is computed from a dual solution of the covering LP evaluated in
exact integer arithmetic on the unreduced instance (`certified_lower_bound`), which does
not depend on solver tolerances or on the reductions.

## 2. Question 1: covering numbers of the profile format

Sequence continued (your validation target), **[X]**:

<!-- TABLE:sequence -->
| `n` | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| conformations | 1 231 221 | 3 576 871 | 10 401 207 | 30 188 971 | 87 689 311 | 254 325 043 | 738 087 517 | 2 139 332 335 | 6 204 141 457 | 17 973 153 955 | 52 091 349 617 | 150 838 528 401 |
| profile classes | 479 | 641 | 818 | 1 037 | 1 281 | 1 594 | 1 911 | 2 328 | 2 753 | 3 319 | 3 857 | 4 532 |
<!-- /TABLE:sequence -->

`N^P_cov` (known part `#gauche`, zero residual), **[X\*]**; `N = n + 3`:

<!-- TABLE:cover -->
| `n` | `N` | `L=1`: `ε=0` | `ε=1` | `ε=N/20` | `ε=N/10` | `ε=N/4` | `ε=N/2` | `L=1/5`: `ε=0` | `ε=1` | `ε=N/20` | `ε=N/10` | `ε=N/4` | `ε=N/2` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 8 | 5 | 5 | 5 | 5 | 4 | 3 | 2 | 2 | 2 | 2 | 1 | 1 |
| 6 | 9 | 6 | 6 | 6 | 6 | 6 | 5 | 2 | 2 | 2 | 2 | 2 | 1 |
| 7 | 10 | 10 | 9 | 10 | 9 | 7 | 5 | 2 | 2 | 2 | 2 | 2 | 1 |
| 8 | 11 | 10 | 9 | 10 | 9 | 7 | 5 | 2 | 2 | 2 | 2 | 2 | 1 |
| 9 | 12 | 13 | 11 | 13 | 11 | 8 | 5 | 3 | 2 | 3 | 2 | 2 | 1 |
| 10 | 13 | 16 | 14 | 16 | 14 | 11 | 7 | 3 | 3 | 3 | 3 | 2 | 2 |
| 11 | 14 | 19 | 17 | 19 | 17 | 12 | 7 | 4 | 3 | 4 | 3 | 2 | 2 |
| 12 | 15 | 21 | 18 | 21 | 18 | 13 | 8 | 4 | 3 | 4 | 3 | 2 | 2 |
| 13 | 16 | 26 | 21 | 26 | 21 | 13 | 8 | 4 | 4 | 4 | 3 | 2 | 2 |
| 14 | 17 | 29 | 25 | 29 | 25 | 14 | 9 | 4 | 4 | 4 | 4 | 3 | 2 |
| 15 | 18 | 33 | 27 | 33 | 27 | 16 | 9 | 5 | 4 | 4 | 4 | 3 | 2 |
| 16 | 19 | 38 | 30 | 38 | 30 | 18 | 10 | 5 | 4 | 4 | 4 | 3 | 2 |
| 17 | 20 | 43 | 34 | 34 | 28 | 17 | 10 | 6 | 4 | 4 | 4 | 3 | 2 |
| 18 | 21 | 48 | 39 | 39 | 31 | 19 | 11 | 7 | 5 | 5 | 4 | 3 | 2 |
| 19 | 22 | [52, 56] | [42, 44] | [42, 44] | 35 | 22 | 12 | 7 | 5 | 5 | 4 | 3 | 2 |
<!-- /TABLE:cover -->

(Rows `n = 1…4` are in the result file.  A cell `[a, b]` is a rigorous bracket — `a` a certified
lower bound, `b` the size of a verified cover — where no solver proved optimality within its
time limit of 300 s.  The class tables are complete to `n = 24`; covers for the sizes not yet
in the table are being computed (job M-005) and will be sent as a linked update — see "Status
of the remaining parts".)

Readings.

* **No plateau at extensive accuracy.**  `L = 1`, `ε = N/2`: 3, 5, 5, 5, 5, 7, 7, 8, 8, 9, 9, 10,
  10, 11 for `n = 5…18` — about one more evaluation per two torsions, with no sign of
  levelling off; `ε = N/4`: about one per torsion.  Your stopping rule "constant over four
  consecutive sizes" is met locally (`n = 6…9` at `ε = N/2`) and then broken: such plateaus
  are steps, not saturation.
* **Integer effects are visible and should not be read as trends.**  With `L = 1` all
  distances and gaps are integers, so `ε = N/20` coincides with `ε = 0` for `N < 20` and
  jumps at `N = 20` (38 → 34 between `n = 16` and `n = 17`); likewise `ε = N/10` equals
  `ε = 1` for `N = 10…19`.  The request's small rates (`ε₁ = 0.05, 0.1`) are therefore not
  yet in an extensive regime at these sizes.
* **Fixed accuracy: quadratic growth.**  `N^P_cov(ε = 0) ≈ N²/10` over the whole range (10 at
  `N = 10`, 21 at 15, 48 at 21; `N^P_cov/N² = 0.100, 0.093, 0.109`), while the number of classes
  grows faster (effective exponent 4.3 between `N = 15` and `N = 27` — above its asymptotic
  value 3, because the set is still expanding).  The growth is polynomial, as Theorem 6(b)
  of the workstream report says it must be, with an exponent 2 that is below the degree 3 of
  the a-priori bound.
* **Small in absolute terms.**  At accuracy `N/2` the format P needs 8 evaluations at 15
  beads, where the per-torsion format needs at least 136 200 of the 422 825 conformations
  and grows by a factor 2.9 per torsion (`P_REPORT.md` §3.3); at 21 beads P needs 11.  "Not
  independent of the chain length at these sizes" and "cheap" are both true.

## 3. Why there is no plateau yet (finite-size analysis) **[E]**

The cover problem depends on the chain only through the finite set
`𝒮_N = {(profile, gmin)}`.  Three exact facts from the class tables:

<!-- TABLE:finite_size -->
| `N` (beads) | 11 | 15 | 19 | 21 | 23 | 25 | 27 | bulk lattice |
|---|---|---|---|---|---|---|---|---|
| largest number of pairs inside the cutoff, per bead | 2.45 | 3.13 | 3.68 | 4.00 | 4.17 | 4.32 | 4.56 | 12 |
| largest `‖N^x‖₁`, per bead | 6.64 | 9.60 | 10.58 | 11.62 | 12.39 | 13.24 | 13.56 | 35 |
| fewest gauche torsions in that extreme class, of `n` | 7/8 | 8/12 | 11/16 | 12/18 | 14/20 | 14/22 | 14/24 | — |
<!-- /TABLE:finite_size -->

(Bulk values: a site has 4, 12 and 12 neighbours at squared distances 3, 8, 11, of which
2 and 2 are chain neighbours at `q − p ≤ 2`; so at most 1, 5 and 6 pairs per bead, and
`‖N‖₁ ≤ 9 + 20 + 6 = 35` per bead.)  At 27 beads the profile set per bead has reached
about 38 % of its bulk extent and is still expanding by 2–3 % per added bead.  At the same
time few gauche torsions buy a large profile: at `n = 24`, four gauche torsions already
reach `‖N‖₁ = 166` (6.1 per bead; hairpins), so the radii `gmin + ε` stay small where the
set is large.  The covering number at accuracy `ε₁N` can only stabilise once
`𝒮_N / N` has stabilised, and compactness approaches its bulk value with surface
corrections of order `N^{-1/3}`.  **Prediction (not a theorem):** the extensive-accuracy
covering numbers keep growing far beyond enumerable sizes, to a limit that is well above
the values in the table; whether that limit is tens or hundreds depends on the limit shape
(ENG-REQ-0001).  This sharpens the sentence of THY-REQ-0002 that the saturation "has not
been seen": it should not be expected to be seen by enumeration at all.

## 4. Question 2 (exhaustive part): entropy of the profile set

Normalised metric `‖N^x − N^y‖₁/N`.  Two quantities:

* `m(δ)` of `P_REPORT.md` §3.2 — the number of points of a farthest-point traversal needed to
  bring the covering radius below `δ`.  **Not reproducible as defined**: it depends on the
  starting point and on tie-breaking, which the report does not state.  With "start at the
  all-trans class, first index among ties" we obtain, for `(δ = 4, 2, 1, ½, ¼)`:
  `n = 8`: (2, 3, 8, 13, 32) against the published (2, 3, 7, 14, 31); `n = 10`: (3, 5, 13, 26, 56)
  against (3, 5, 11, 25, 55); `n = 13`: (3, 5, 13, 42, 125) against (3, 5, 12, 34, 88).  The
  values at `δ ≥ 1` agree to within 2; at small `δ` the traversal is a poor estimator in
  either implementation (next item).
* The **internal covering number at closed radius `δN`** — well defined; reported as a
  rigorous bracket `[certified lower bound, verified cover]`, exact where one number is
  given:

<!-- TABLE:entropy -->
| `n` | `δ = 4` | `δ = 2` | `δ = 1` | `δ = ½` | `δ = ¼` | traversal `m(δ)` at the same five radii |
|---|---|---|---|---|---|---|
| 8 | 1 | 2 | 4 | 10 | 27 | 2, 3, 8, 13, 32 |
| 10 | 2 | 3 | 5 | 16 | 43 | 3, 5, 13, 26, 56 |
| 12 | 2 | 3 | 6 | 19 | 65 | 3, 5, 12, 31, 93 |
| 13 | 2 | 3 | 7 | 20 | 55 | 3, 5, 13, 42, 125 |
| 14 | 2 | 3 | 8 | 25 | 72 | 3, 6, 17, 45, 117 |
| 16 | 2 | 3 | 8 | [25, 28] | [98, 107] | 3, 6, 17, 60, 179 |
| 18 | 2 | 3 | 9 | [29, 33] | [104, 111] | 3, 6, 19, 72, 195 |
<!-- /TABLE:entropy -->

  (Non-monotone steps such as 65 → 55 between `n = 12` and `n = 13` at `δ = ¼` are the integer
  radius: `⌊15/4⌋ = 3`, `⌊16/4⌋ = 4`.)  At `δ = ¼` the traversal overestimates the covering
  number by up to a factor 2.3 (125 against 55 at `n = 13`).  The entropy at fixed `δ` grows slowly but steadily; the
  "saturation at `N ≈ 13`" read off from `m(1) = 11, 11, 10, 12` in `P_REPORT.md` §3.2 is not
  there in the exact numbers, which keep increasing through the largest size (column `δ = 1`).

## 5. Question 3(a): every trans/gauche pattern is realised

**Exhaustive [X]:** for every `n ≤ 24` all `2ⁿ` patterns occur among the self-avoiding
conformations (`results/lattice_Sc12_patterns.json`: realised = total for `n = 1…24`; the bitmaps
themselves are regenerated by `dia_enum -b`; unit test for small `n`).

**Proof for every `n` (two lines).**  Write bond `m` as `+a_{i_m}` for even `m` and `−a_{i_m}`
for odd `m`, with `a₀…a₃ = (1,1,1), (1,−1,−1), (−1,1,−1), (−1,−1,1)` and `i_{m+1} ≠ i_m`; torsion
`j` is trans iff `i_{j+2} = i_j`.  Restrict even bonds to `{a₀, a₂}` and odd bonds to
`{a₁, a₃}`.  Then every bond has `y`-component `+1`, so the walk is strictly monotone in `y`
and self-avoiding, whatever the choices; and at each torsion both options remain — repeat
the index two bonds back (trans) or take the other element of the pair (gauche).  Hence
every word in `{t, g}ⁿ` is realised by a directed conformation.  ∎  (The sign of each gauche
torsion is then forced; the statement is about patterns, as asked.)  So this hypothesis
of the two lower bounds holds on the self-avoiding diamond chain for all `n`, not only for
the checked sizes.

## 6. Question 3(b): single-flip constants

`c_j^{sf}` = largest `‖N^x − N^{x′}‖₁` over pairs of self-avoiding conformations differing in
torsion `j` only (`src/metricchain_eng/chains/dia_flip.c`, mode A), **[X]**:

<!-- TABLE:flip -->
| `n` | `c^{sf}` (first half; symmetric under chain reversal) | `min_j c_j / d_j` | sets `T` with budget below `D_max` | pairs enumerated | violations | worst excess |
|---|---|---|---|---|---|---|
| 8 | 35, 50, 56, 58 | 14.5 | 1 | 22 300 | 0 | -24 |
| 9 | 36, 63, 69, 76, 76 | 15.2 | 1 | 65 188 | 0 | -9 |
| 10 | 40, 68, 74, 81, 98 | 19.6 | 9 | 1 661 052 | 0 | -17 |
| 11 | 48, 73, 81, 90, 104, 104 | 17.3 | 9 | 4 836 532 | 0 | -27 |
| 12 | 52, 85, 92, 108, 114, 114 | 19.0 | 5 | 7 903 120 | 0 | -26 |
| 13 | 53, 89, 98, 113, 132, 132, 130 | 18.6 | 9 | 40 766 124 | 0 | -20 |
| 14 | 57, 92, 109, 118, 137, 154, 147 | 21.0 | 13 | 168 255 208 | 0 | -32 |
| 15 | 58, 103, 119, 136, 143, 160, 160, 160 | 20.0 | 9 | 343 162 724 | 0 | -9 |
| 16 | 58, 108, 124, 141, 160, 170, 169, 170 | 21.2 | 13 | 1 415 043 552 | 0 | -22 |
<!-- /TABLE:flip -->

* *Growth with the distance `d_j = min(j, n+1−j)` from the nearer end* (`j = 1…n`).  Two
  readings of the same numbers.  (i) *From below, which is what a lower bound needs:* the
  ratio `c_j/d_j` is smallest at the centre of the chain and its minimum over `j` (third
  column) does not decay with `n` — it lies between 14 and 22 at every size from 8
  torsions on.  So `c_j ≥ κ·d_j` holds at all sizes computed with `κ = 14`, and with
  `κ = 18.5` from 12 torsions on.  (ii) *The shape is not a straight line:* a large first step
  from the end torsion to its neighbour (35 at `n = 14`), then steps between 9 and 19 per
  torsion, then a plateau at the centre (the vector is not even monotone at `n = 14`: 154 → 147).  The end constant
  has saturated (57, 58, 58 at `n = 14, 15, 16`: one bead moves, and a bead has a bounded
  number of neighbours inside the cutoff); at fixed `d` the constants still increase with
  `n`.  A chain of 16 torsions has only eight distinct distances, so the asymptotic profile
  `c(d)` is not visible; what the data support is linear growth *in the sense of two-sided
  linear bounds*, not a linear law.
* *Is `c^{sf}` a valid Hamming envelope?*  **Yes at every size in the table, exhaustively [X].**  The
  domain is not a product (excluded volume), so paths of single flips may leave it — at
  `n = 14`, 12–13 % of the single flips at central torsions do — and validity is a genuine
  question.  All-pairs comparison is quadratic in `3ⁿ`; instead: a pair differing exactly on
  a set `T` of torsions can violate `‖N^x − N^y‖₁ ≤ Σ_{j∈T} c_j` only if `Σ_{j∈T} c_j < D_max`
  (the largest profile distance, from the class table), which leaves a handful of sets
  near the chain ends; for those, every conformation and every assignment of other states
  on `T` is enumerated (`dia_flip`, mode B); the last three columns of the table give the
  number of such sets, the number of pairs enumerated and the worst value of
  `‖N^x − N^y‖₁ − Σ_{j∈T} c_j` (negative = inequality holds with room).  No violation at any
  size computed.  (The previous check stopped at `n = 8`.)

## Status of the remaining parts

| part | status |
|---|---|
| covers for the sizes up to `n = 24` that are not yet in the table (question 1) | class tables done; integer programmes running with time limits (job M-005); linked update to follow |
| generic (off-lattice) chain, `n ≤ 14–16` (questions 1, 3) | not started; needs a floating-point enumerator with tolerance-safe class hashing — next |
| question 2 by sampling to `N = 10³` | not started.  Note the obstacle: a sample gives an *upper* estimate of `gmin` and misses classes, so sampled covering numbers are biased downwards in both ways; we intend to report entropy numbers of sampled profile sets (as the workstream did) and to say so |
| question 4 (sum class `P_L + Lip(η·d_H)`, 683-conformation chain) | not started; small exact computation |
| question 5 (span format off-lattice, `n = 10`) | not started |

## Execution environment, configuration, resources

Local: Ubuntu 26.04 under WSL2, 8 threads; `cc` 15.2 `-O3 -march=native`; Python 3.12.16,
NumPy 2.5.5, SciPy 1.18.1 (HiGHS), OR-Tools 9.15.6755 (CP-SAT).  Remote: Modal (the research
owner's workspace), Debian containers; jobs M-001…M-005 of `docs/engineering/COMPUTE_LEDGER.md`.
Enumeration cost: `n = 20` 261 s on one local core; `n = 21…24` 296, 877, 2 561, 7 328
core-seconds on Modal (64 containers; 158 s wall for `n = 24`), i.e. about `2·10⁷`
conformations per core-second.  No random seeds anywhere (exhaustive and deterministic).
Total remote cost of everything in this message: $1.33 at the time of writing, with the
cover job for `n = 19…24` still running (per-job figures in the ledger).

## Reproduction

```
cc -O3 -o build/dia_enum src/metricchain_eng/chains/dia_enum.c
cc -O3 -o build/dia_flip src/metricchain_eng/chains/dia_flip.c
python -m pytest tests/eng -q                                    # 69 tests
python experiments/eng/chain_cover/run_lattice.py --check        # published values, n = 5..13
python experiments/eng/chain_cover/run_lattice.py --nmin 1 --nmax 18   # the cover table
python experiments/eng/chain_cover/run_flip.py --nmin 3 --nmax 16 --run   # question 3(b)
modal run modal_jobs/chain_enum_app.py --nmin 21 --nmax 24       # class tables beyond n = 20
```

Artifacts: class tables `experiments/eng/chain_cover/data/dia_Sc12_n{1..24}.txt` (the complete
result of the enumeration: any other cover question about this model can be answered from
them without re-enumerating); `data/flip/`; `results/lattice_Sc12.json`,
`results/lattice_Sc12_flip.json`, `results/lattice_Sc12_patterns.json`.

## Assumptions and limitations

Idealised synthetic lattice chain with a made-up energy; nothing is claimed about any
molecule.  Homopolymer, `S_c = 12`, zero residual, known part `#gauche` only — the instance
of your table; other type sequences, cutoffs and residuals are not covered.  Covering
numbers for `n ≤ 18` are solver-proved optima (two independent solvers); the finite-size
analysis of §3 is an argument from exact data, not a theorem.  The entropy brackets at
`δ ≤ ½` and `n ≥ 16` are not closed.

## Interpretation

Proposition 11.49(a) is not contradicted and not visible.  On this model the profile
format is cheap in absolute terms and its cost grows with the chain — linearly at
extensive accuracy, quadratically at fixed accuracy — through 21 beads, and the reason
(a profile set still at a third of its bulk extent) will persist far beyond enumerable
sizes.  For the blueprint this supports the weaker wording you anticipated: recommend the
format because it is orders of magnitude cheaper than the per-torsion one, not because
its certificates do not grow.

## Recommended theoretical follow-up

ENG-REQ-0001: a limit-shape formulation of the thermodynamic limit of certificate sizes
(§12 item 9(a)), for which the class tables are the finite-size data; and the question
whether the lower bounds that use `c^{sf}` need more than what §6 confirms.
