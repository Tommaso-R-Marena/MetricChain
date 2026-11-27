# A producer of "shares at the leaves" certificates and what producing and checking costs against exact solvers (registry Q-04/Q-05; SCI-RES-0014 §7, P7-E1)

**Status of this report (Computational Research Division, 2026-11-27, written during the consolidation ordered by the
research owner).**  The library `src/metricchain_eng/leafprod/`, its tests and the benchmark below are the work of a
subagent of this division; the report under the line is its own, unedited except for one sentence about a local path.
**What the coordinator checked:** the test file passes in the division's full test run (40 tests).  **What the
coordinator did not do:** read the library (2 175 lines), re-run the benchmark, or check the report's numbers against
`results/tables.txt` beyond the fact that the benchmark's own `make_tables.py --verify` is reported to pass.  The
report is therefore **unreviewed**; its negative conclusions (a certificate costs more than the search that finds
it; the binding limit is certificate size; a dense format inflates sparse instances) are consistent with what the
structural-biology division measured on its own producer, which is weak corroboration, not review.  The timings were
taken on a laptop shared with other agents and are noisy, as the report says.

---

```
REPORT — a producer for "shares at the leaves" certificates, and a first benchmark of producing + checking against exact solvers (stage C/D)

Paths are relative to the repository root (the checkout of research/ubuntu-engineering). Nothing was committed; git was used read-only (git show / cat-file / status). No package was installed. No file outside the three allowed paths was created or changed (the compiled kernel goes to the git-ignored build/ directory, as the checker's does).

Marking used below: [E] exact (integer arithmetic; every "certified" means both engines of the checker accepted, with identical counts), [M] measured (wall-clock or memory on a shared laptop CPU: noisy; medians with [min-max]), [C] conjectured.

====================================================================================================
0. BOTTOM LINE
====================================================================================================
1. [E] The producer works and is never believed on its own word: 1 844 certificates in the main pass, 36 from rounded linear programmes, 7 in the second pass and 10 in an exploratory probe were all accepted by BOTH engines; none was rejected; on 1 885 instances at least two independent exact values exist (certified L, the same search without certificate, dynamic programming, enumeration, CP-SAT, MILP) and they agree on every one (0 inconsistent of 2 026 instances).
2. [E] Where the relaxation is tight the certificate is one leaf: all 500 chain and tree instances up to 100 sites and 10 states, and 243 of 250 attractive-Potts grid instances. [M] But even there the certificate is not cheap relative to solving: at n = 100 producing + checking takes 0.36 s [0.20-0.70], 96 % of it after the search, against 4.4 ms for dynamic programming (ratio 90 [35-247]).
3. [E] On frustrated instances the tree grows geometrically and the limit is the SIZE of the certificate, not the search time: all 146 failures of the producer were stops at a size cap (101 at the cap on checker operations, 45 at the cap on integers; none at the 60 s limit). [M] A failed run stopped after a median 0.34 s of search. Where the search was run to the end on a failed instance (60 cases) the certificate would have needed a median 4.8 M integers (largest 164 M) against a cap of 2 M.
4. [M] The certificate costs more than the search: over all certified instances the producer spent 85 s searching, 60 s assembling, 146 s in check(obj, "c") and 261 s in check(obj, "python") — 15 % search, 85 % certificate. With more than 100 leaf certificates, assembling + checking took 2.3 times the search [1.04-37.8] (longer than the search in 75 of 75 cases).
5. [M] Against solving exactly without a certificate: on banded chains dynamic programming is 55-89 times faster (median) than producing + checking, up to 2 782 times, and still solves in milliseconds where no certificate fits the caps. On complete graphs it is the other way round for the general solvers: the producer's own search is faster than CP-SAT and MILP in all 15 cell/solver pairs with n >= 16, and producing AND checking was faster than every certificate-free baseline other than its own search in 42 of 160 branched instances.
6. [E] The dense format is the main cost driver on sparse instances: at n = 100 a leaf certificate is 16 to 48 times larger than a sparse variant would be (chain 42-48, grid 25-27, cubic 29-32, band2 23, band3 16; complete 1), and so is the checker's operation count.
7. [M] check(obj, "c") spends 96 % [87-99] of its time in the Python front door (strict loading + encoding), not in leafcert.c; leafcert.c alone never needed more than 91 ms, the Python engine up to 4.4 s.
8. Hypotheses stated before the runs: held H1, H2, H3a, H3c, H4a-d, H5, H8, H9, H10a-d, H11, H13; partly H3b, H3d, H6; failed H7 (I expected the integer cap to bind at n = 100; the operation cap did, 31 of 48). No defect found in the checker or its report.

====================================================================================================
1. WHAT EXISTS
====================================================================================================
Library src/metricchain_eng/leafprod/ (2 175 lines):
  __init__.py   produce(instance, L=None, *, time_limit=60, max_leaves=100000, bound="mp", branching="strong", order="best", seed=0, certificate=True, partial=True, share=True, max_cert_integers=2^26, max_check_ops=None, kernel="c", ...) -> Result(status, L, certificate, x, energy, optimal, best_bound, bound_checked, reason, stats, checks).
                status "certified" only after both engines accepted; "limit" (reason: time / leaves / cert_integers / check_ops; with partial=True a certificate for the best bound reached is assembled and checked too); "refuted" (a given L exceeds the energy of a state it returns); "rejected" (checker did not accept: a defect, never hidden; did not occur); "solved" (certificate=False: plain search).
                L=None certifies L = min E and puts the minimiser in the annotation "ref"; a given L is certified as given.
  model.py      validation and sparse integer form (pairs with a zero table are not edges; J may omit pairs); 64-bit safety rules that depend on the degree (the science division's published tables, up to 2^45.9, are accepted).
  kernel.c + ckernel.py   integer block-coordinate ascent on the dual ("pull" all pair minima into a site, "push" the excess over the minimum to the later sites in integer shares): monotone in integers, exact dynamic programming on forests; exact evaluation of messages on a box; decoding; local search; 2-core. Compiled on first use.
  pykernel.py   the same in plain Python (reference; produce(kernel="python")).
  lpbound.py    the linear programme of the pairwise relaxation with scipy linprog (HiGHS dual simplex); its multipliers are rounded (nearest / down / up, best kept) to integer messages.
  search.py     best-first or depth-first branch and bound; leaf bounds "mp", "lp", "hybrid" (mp, then lp + mp polish where mp fails); branching rules "strong", "maxdeg", "margin", "maxdom", "frac"; shared leaves; rigorous early stop at the size limits.
  exact.py      enumeration and variable elimination (oracles, baselines); families.py seeded generators; formats.py dense vs sparse counts, never-read data, split-rule counts.
How a leaf is valid whatever the search did [E]: the search only proposes integer messages; U and P2 are then computed as exact minima over the box the leaf is used on, so (S) and (P) hold by construction and only (T) decides. No float can reach a certificate (tested).
Shared leaves: after a pull at site i the value of the messages on the box with D_i = B is rest + min_{a in B} theta_i(a); so all children a with rest + theta_i(a) >= L name one leaf (used when a node branches, and again when a child is certified by its own messages).
Tests tests/eng/test_leafprod.py: 40 tests, 12.8 s on the idle machine (37-75 s while it was loaded); LEAFPROD_FUZZ=k multiplies. They cover: C kernel = Python reference on 400 random instances/boxes (identical messages), bound <= enumeration for any messages; 150 random instances x 8 method/rule combinations (certified L = enumerated minimum; the same certificate with L+1 rejected by both engines on (T); a request for min+1 refuted with a state; integers only); chains and trees with one leaf for mp, lp and hybrid (40 instances each, up to 45 sites); the ring of P7.5 for n = 4..9; frustrated triangle and 150 three-site instances (never more than one branching: P7.4(c)); one site, one state, all zeros, constant tables, ties, entries of 2^56, 15 kinds of malformed instance; limits and checked partial certificates; determinism; shared leaves; oracles; generators (one checksum pinned).
  Two cross-checks with the science division's text [E]: (i) on their four distinct published instances (nine files, read with git show, nothing executed) the producer certifies their bound L = 0 with the minimiser equal to their "ref"; trees (leaf certificates / leaf boxes / depth), ours vs theirs: Ser6 4/9/1 vs 2/9/1 (shared) and 9/9/1; Lys3 4/21/1 vs 2/21/1 and 21/21/1; LKSE:6 6/13/1 vs 3/27/1 and 13/13/1; Leu16 3/3/2 vs 3/3/2; 0.05-0.13 s each [M]. (ii) their ring (P7.5, w = 7/4, R = 10): every tree of every configuration has depth >= ceil(n/3) as they prove; the default configuration attains depth ceil(n/3) with ceil(n/3)+1 leaves for n = 4..8 and needs depth 5 at n = 9.
Benchmark experiments/eng/leafcert_bench/: PROTOCOL.txt, config.py (the protocol as data), run_bench.py, baselines.py, make_tables.py (--verify passes), integrality_probe.py (exploratory, added later), results/main (211 cells), results/compare (24), results/long (10), results/exploratory_integrality.json, results/tables.txt (every table, 1 439 lines). The results directory is 9.6 MB of indented JSON — decide whether you want it committed as it is.

====================================================================================================
2. PROTOCOL (frozen before any test-seed run) AND WHAT WAS KNOWN THEN
====================================================================================================
PROTOCOL.txt sections 0-8 were written before the first run on the test seeds (sha256 then 40432dfaf78bae04; config.py c870885c2f57e152, unchanged since); section 9 was added afterwards. Section 0 says what development had shown, so the hypotheses are informed, not blind: development used the master seed "leafprod-dev" (including three trial runs of the driver), the test seeds use "leafcert-bench-v1"; no test instance was solved before the freeze (one was generated, not solved, to pin a checksum).
Instances: integer tables, every entry uniform in {-1000..1000}; families chain, tree, band2, band3, grid, cubic (random 3-regular), complete; potts = grid with J = -w [a = b], w in {1..1000}, and random fields; alphabets 2, 3, 5, 10 and "mixed" (each site draws from {2, 3, 5, 10}); sizes 6, 12, 25, 50, 100 (grid/potts 49 for 50, cubic 24 for 25), complete 6, 8, 10, 12, 16, 20, 24, 28, 32, 36; 10 instances per cell; seeds and a sha256 of every instance stored.
Main configuration: bound mp, branching strong, best-first. Limits: 60 s for the search; at most 2 000 000 integers in the leaf certificates; at most 20 000 000 checker operations. The two caps are a budget decision (a certificate at the caps costs 20-40 s to assemble and check on this machine; the benchmark had two hours) — they, not the clock, decide where the producer stops, and the report says so everywhere.
Baselines, same machine, one thread, 60 s: the same search with certificate=False (identical tree: same nodes and leaf boxes as the producer in 1 844 of 1 844 certified instances [E]); dynamic programming (variable elimination) where the largest table has <= 2^23 entries; enumeration up to 2^24 states; CP-SAT 9.15, one worker, linearization_level 2 (the fastest single-worker setting on development instances; with default parameters it was 5-15 times slower), Booleans tied by the equalities of the relaxation; HiGHS MILP on the same relaxation (added by me as a second general solver). CP-SAT and MILP prove optimality internally and leave nothing our checker can verify.
Rules fixed in advance to fit the time: CP-SAT and MILP on instances 0-1 of a cell, ladders with k in {2, 3} plus k = 5 of chain, grid, complete, leaving a ladder at their first 60 s hit; the search without certificate on every certified instance and on the first three uncertified ones of a cell; the producer leaves a ladder after a cell with fewer than 5 of 10 certified, later cells are "extension cells" (3 instances, baselines only); budget rule (no new cell after 64 / 20 / 16 minutes for the three passes).
Machine: i5-1135G7 (4 cores, 8 threads), shared with other agents; two workers pinned to logical CPUs 5 and 7, one thread each, 3 GiB address space each. Python 3.12.16, numpy 2.5.5, scipy 1.18.1, ortools 9.15.6755.

====================================================================================================
3. HYPOTHESES AND VERDICTS
====================================================================================================
H1 Forests: all 500 chain/tree instances one leaf; at n = 100 the search is the smaller part, producer < 5 s even for k = 10, DP >= 10x faster.
   HELD. [E] 500/500 one leaf. [M] n = 100: total 0.36 s [0.20-0.70]; after the search 96 % [93-98]; k = 10: 0.64 s [0.58-0.70]; producer/DP 89.5 [35-247].
H2 Potts grid: k = 2 all one leaf; k >= 3 and mixed all certified and >= 8 of 10 one-leaf in every cell.
   HELD. [E] k = 2: 50/50 one leaf; others 200/200 certified, 193 one leaf, no cell below 8.
H3 Sparse frustrated (grid, cubic, band2, band3):
   (a) all instances with n <= 12 certified.  HELD [E] 400/400.
   (b) median leaf boxes never decrease with n; band3 (k >= 3) and band2 (k >= 5) grow by more than x4 from 25 to 50.
       PARTLY. One ladder of 20 decreases (band2 mixed, n 6 -> 12: 3 -> 1). Growth 25 -> 50: band3 k=3 x15; band3 k=5 >= x95 and band2 k=5 >= x4.1 (lower bounds: 3 and 7 instances searched at 50); band3 k=10 and band2 k=10 not measurable (the search itself hit 60 s at n = 50 on both instances tried).
   (c) producer leaves at n <= 100 in band3 k=3,5,10, band2 k=5,10, grid k=10; >= 8 of 10 at n = 100 in grid k=2, cubic k=2,3.
       HELD [E]: band3 k=3 0/10 at 100; k=5 0/10 at 50; k=10 0/10 at 25; band2 k=5 4/10 at 50; k=10 3/10 at 25; grid k=10 0/10 at 49; the three easy ladders 10/10 at 100.
   (d) failures are size caps, not the 60 s limit, and the search alone solves the instance.
       PARTLY. [E] 101 failures, all caps (79 operations, 22 integers). The search was run on 45 of them (rule) and solved 43; two hit 60 s.
H4 Complete graphs:
   (a) relative gap of the relaxation > 20 % for every instance with k = 2, n >= 16.  HELD [M, float LP]: 67 % [22-157] over 50 instances.
   (b) leaf boxes grow by x1.2-1.6 per site for k = 2, more than x1.6 for k = 5.  HELD: x1.30 (n 10 -> 28: 3 -> 357), x1.67 (n 6 -> 12: 5 -> 107). Also k=3 x1.50, k=10 x2.57, mixed x1.49 (two-point estimates).
   (c) producer leaves at 32 (k=2, >= 5/10 at 28), at 16 (k=5), at 10 or 12 (k=10).  HELD [E]: k=2 10/10 at 28, 4/10 at 32; k=5 4/10 at 16; k=10 2/10 at 12. (k=3: 10/10 at 20, 0/10 at 24; mixed 5/10 at 20, 0/10 at 24.)
   (d) there the search alone still solves at least half.  HELD within the rule: 7/7, 7/7, 5/5 of the instances searched.
H5 More than 100 leaf certificates: assemble + checks longer than the search in >= 90 %, >= 2x in the median, Python engine more than half of it.
   HELD [M]: 75 instances; ratio 2.31 [1.04-37.8]; above 1 in 75, above 2 in 52; Python share 57 % [46-71].
H6 leafcert.c alone < 1 s; > 80 % of check(obj, "c") is Python-side; Python engine 20-100x slower per operation.
   PARTLY [M]: leafcert.c at most 91 ms over 1 844 certificates; Python-side share 96 % [87-99] (564 certificates with >= 1e5 operations); time ratio Python engine / leafcert.c 41.5 in the median but [20.9-152]: above my band at the top.
H7 Density arithmetic, and "at n = 100 at least 80 % of failures are stops at the integer cap while the search completes".
   Arithmetic exact (chain k=10: 104 050 vs 2 179; grid k=10: 104 050 vs 3 880). Expectation FAILED: of 48 failures at n = 100, 17 were the integer cap and 31 the operation cap; 21 of the 23 searched completed.
H8 Leaf bounds: lp/mp leaf-box ratio within [0.5, 2] in all nine cells; lp at least 5x slower in every cell; hybrid within 20 % of lp in size, between the two in time; rounding loss at the root below 20 units.
   HELD: ratios 1.06, 1, 1, 0.88, 1.20, 1, 1, 1, 1; time lp/mp 6.9 to 52; hybrid/lp sizes 0.97-1.0, hybrid/mp time 4.4-14.6; rounding loss medians 0 to 3.1 (largest 9).
H9 Branching: strong smallest median in >= 13 of 17 cells at <= 3x maxdeg's time; maxdom = maxdeg on uniform alphabets, >= 1.5x larger on the two mixed cells.
   HELD: 16 of 17 (not complete k=5 n=10: 51 vs 47); time strong/maxdeg 0.68-1.43; maxdom/maxdeg exactly 1 on the 15 uniform cells, 6.9 and 2.5 on the mixed ones.
H10 (a) DP applies to every chain/tree/band instance and is fastest on >= 90 % with n >= 50.  HELD: 945/945; fastest on 345/345.
    (b) on complete graphs with n >= 16 the search beats MILP and CP-SAT in the median wherever they run.  HELD in all 15 cell/solver pairs with an instance solved by both (closest: k=2, n=36, 18.5 s vs MILP 19.8 s); at k=5, n=16 neither general solver finished its instance, the search solved 7/7.
    (c) CP-SAT leaves the complete ladders earlier than the search.  HELD where testable: first 60 s hit CP-SAT / search: k=2 36 / none up to 36; k=3 20 / 28; k=5 16 / 20 (MILP: none up to 36 / 24 / 16).
    (d) certified band instances that needed branching: producer >= 10x the fastest exact baseline.  HELD: 77 [7.2-2 782]; >= 10 in 217 of 218.
H11 k = 2: leaf certificates = leaf boxes always; k = 10: sharing saves 5-30 %.  HELD [E]: 433 instances, never different; k=10 11.1 %.
H12 (exploratory): relaxation tight at the root but more than one leaf: 6 of 1 266 such certified instances (cubic 4, band2 1, band3 1); see section 7.
H13 No producer run above 1 GiB resident.  HELD [M]: largest 565 MB.

====================================================================================================
4. RESULTS PER FAMILY (main pass)
====================================================================================================
Totals [E]: 211 cells, 2 026 instances, 1 990 producer runs, 1 844 certified (1 260 with one leaf), 146 not certified (all at a size cap). Largest certified: 1.91 M integers (band2 k=3 n=50); 16.4 MB of JSON and 723 leaf boxes (complete k=2 n=32); most leaf boxes 1 405 (complete k=10 n=12); deepest tree 20 (band3 k=2 n=100). [M] Slowest certified run 9.03 s in total (search 3.06, assemble 1.10, check C 1.79, check Python 3.09): every certified instance was produced AND checked by both engines well inside 60 s.
Baseline runs: search without certificate 1 935 (1 914 solved, 21 hit 60 s); CP-SAT 200 (197 optimal); MILP 202 (200 optimal); DP 1 719; enumeration 716.
Relaxation tight at the root (LP value = optimum) [M, float]: chain 250/250, tree 250/250, potts 243/250, cubic 190/248, grid 155/226, band2 87/226, band3 60/219, complete 32/297.

Columns: cert = certified / producer runs; 1L = certified with one leaf; leaf boxes, ints (integers of the leaf certificates), bytes (JSON) and the producer's times over the certified instances; produce = search + assembling; chkC / chkPy = check(obj, engine); search = the same search without certificate (solved/run, median time), boxes = its median leaf boxes; DP, CP-SAT, MILP = solved/run and median time; "e" = extension cell; "-" = not run or not applicable. Smaller sizes (all certified, mostly one leaf) are in results/tables.txt.

chain (all 250 one leaf; n = 100 shown)
  k        n   cert  1L  leaf boxes   ints  bytes             produce   chkC  chkPy      search  boxes           DP     CP-SAT       MILP
  2      100  10/10  10           1  24.9k   297k    61ms [29ms-84ms]   67ms  0.11s  10/10 10ms      1  10/10 3.8ms   2/2 50ms   2/2 34ms
  3      100  10/10  10           1  34.8k   378k    48ms [38ms-87ms]   98ms  0.13s  10/10 13ms      1  10/10 4.4ms  2/2 0.14s   2/2 55ms
  5      100  10/10  10           1  54.5k   602k   90ms [70ms-0.10s]  0.11s  0.17s  10/10 15ms      1  10/10 4.3ms  2/2 0.63s  2/2 0.12s
  10     100  10/10  10           1   104k  1.52M  0.11s [99ms-0.14s]  0.22s  0.30s  10/10 22ms      1  10/10 4.4ms          -          -
  mixed  100  10/10  10           1  55.3k   611k    87ms [69ms-99ms]  0.12s  0.17s  10/10 11ms      1  10/10 4.5ms          -          -

tree (all 250 one leaf; n = 100 shown)
  2      100  10/10  10           1  24.9k   297k    64ms [41ms-75ms]   71ms  0.12s  10/10 10ms      1  10/10 4.3ms  2/2 31ms  2/2 40ms
  3      100  10/10  10           1  34.8k   378k    41ms [30ms-85ms]  0.11s  0.13s  10/10 10ms      1  10/10 4.0ms  2/2 74ms  2/2 65ms
  5      100  10/10  10           1  54.5k   602k   87ms [78ms-0.11s]  0.12s  0.18s  10/10 14ms      1  10/10 4.5ms         -         -
  10     100  10/10  10           1   104k  1.52M  0.12s [93ms-0.13s]  0.21s  0.30s  10/10 20ms      1  10/10 4.6ms         -         -
  mixed  100  10/10  10           1  53.6k   586k   84ms [45ms-0.11s]  0.12s  0.16s  10/10 15ms      1  10/10 4.4ms         -         -

potts (250/250 certified, 243 one leaf; n = 100 shown)
  2      100  10/10  10           1  24.9k   298k     75ms [40ms-90ms]   66ms  0.11s  10/10 15ms      1  10/10 7.3ms   2/2 97ms   2/2 70ms
  3      100  10/10  10           1  34.8k   379k    84ms [37ms-0.10s]   89ms  0.14s  10/10 18ms      1  10/10 0.22s  2/2 0.36s  2/2 0.11s
  5      100  10/10  10           1  54.5k   600k   0.10s [91ms-0.11s]  0.12s  0.19s  10/10 20ms      1            -          -          -
  10     100  10/10  10           1   104k  1.50M  0.13s [0.10s-0.14s]  0.22s  0.29s  10/10 28ms      1            -          -          -
  mixed  100  10/10   9     1 [1-2]  53.3k   583k    93ms [60ms-0.10s]  0.11s  0.18s  10/10 18ms      1     1/1 38ms          -          -

grid
  k         n   cert  1L  leaf boxes   ints  bytes              produce   chkC  chkPy       search  boxes           DP     CP-SAT       MILP
  2        25  10/10  10           1  1.52k  18.3k  6.0ms [4.1ms-7.8ms]  4.7ms  8.0ms  10/10 3.5ms      1  10/10 1.5ms   2/2 22ms   2/2 29ms
  2        49  10/10   9     1 [1-4]  5.93k  71.1k     14ms [12ms-20ms]   18ms   30ms  10/10 6.4ms      1  10/10 3.2ms   2/2 44ms   2/2 34ms
  2       100  10/10   9     1 [1-5]  24.9k   298k    72ms [44ms-0.11s]   80ms  0.12s   10/10 14ms      1  10/10 8.6ms   2/2 85ms   2/2 59ms
  3        25  10/10   8     1 [1-3]  2.12k  23.9k  6.5ms [6.1ms-9.7ms]  6.1ms  9.5ms  10/10 3.9ms      1  10/10 1.6ms   2/2 84ms   2/2 51ms
  3        49  10/10   7    1 [1-13]  8.28k  91.7k     17ms [16ms-71ms]   23ms   42ms  10/10 7.3ms      1  10/10 4.4ms  2/2 0.17s   2/2 87ms
  3       100   7/10   3    3 [1-39]   104k   797k   0.12s [54ms-0.72s]  0.14s  0.24s   10/10 44ms     25  10/10 0.21s  2/2 0.38s  2/2 0.14s
  5        25  10/10   6    1 [1-13]  3.33k  39.4k   9.1ms [7.3ms-66ms]   10ms   15ms  10/10 5.7ms      1  10/10 2.8ms  2/2 0.38s   2/2 97ms
  5        49  10/10   3   13 [1-53]   156k   808k    70ms [13ms-0.18s]  0.16s  0.28s   10/10 26ms     13   10/10 56ms  2/2 0.84s  2/2 0.35s
  5       100   0/10   0           -      -      -                    -      -      -    3/3 0.55s    457            -  2/2 2.31s  2/2 4.19s
  10       25  10/10   2   19 [1-73]  85.4k   387k    38ms [12ms-0.10s]   73ms  0.24s   10/10 24ms     19   10/10 62ms          -          -
  10       49   0/10   0           -      -      -                    -      -      -    3/3 0.45s    325            -          -          -
  10     100e      -   -           -      -      -                    -      -      -        0/2 -      -            -          -          -
  mixed    25  10/10   6    1 [1-28]  3.77k  46.8k    10ms [8.0ms-73ms]   12ms   15ms  10/10 5.6ms      1  10/10 2.7ms          -          -
  mixed    49  10/10   2     3 [1-9]  37.4k   258k     29ms [13ms-64ms]   48ms   80ms   10/10 14ms      3  10/10 5.9ms          -          -
  mixed   100   7/10   1    5 [1-40]   262k  1.56M   0.13s [50ms-0.54s]  0.26s  0.47s   10/10 84ms     29    6/6 0.12s          -          -

cubic
  k        n   cert  1L   leaf boxes   ints  bytes              produce   chkC  chkPy       search  boxes           DP     CP-SAT      MILP
  2       24  10/10   8      1 [1-2]  1.40k  16.8k  7.0ms [5.5ms-9.4ms]  5.5ms  8.8ms  10/10 3.9ms      1  10/10 1.7ms   2/2 25ms  2/2 39ms
  2       50  10/10  10            1  6.17k  73.9k     16ms [11ms-77ms]   21ms   34ms  10/10 7.2ms      1  10/10 3.7ms   2/2 38ms  2/2 35ms
  2      100  10/10   9      1 [1-3]  24.9k   298k    61ms [41ms-0.10s]   77ms  0.13s   10/10 15ms      1   10/10 71ms   2/2 82ms  2/2 48ms
  3       24  10/10   9      1 [1-3]  1.96k  22.0k   7.6ms [6.5ms-15ms]  7.2ms   11ms  10/10 4.1ms      1  10/10 1.7ms  2/2 0.10s  2/2 47ms
  3       50  10/10  10            1  8.62k  95.1k     18ms [16ms-19ms]   26ms   36ms  10/10 7.6ms      1   10/10 18ms  2/2 0.15s  2/2 54ms
  3      100  10/10   9     1 [1-35]  34.8k   380k    51ms [37ms-0.45s]  0.13s  0.14s   10/10 16ms      1            -  2/2 0.29s  2/2 80ms
  5       24  10/10   6     1 [1-17]  3.06k  36.2k   8.3ms [7.5ms-39ms]   10ms   15ms  10/10 7.2ms      1  10/10 5.0ms          -         -
  5       50  10/10   7     1 [1-41]  13.5k   153k    23ms [20ms-0.18s]   38ms   55ms   10/10 10ms      1            -          -         -
  5      100   9/10   5     1 [1-37]  54.5k   606k   0.11s [62ms-0.42s]  0.13s  0.19s   10/10 34ms     13            -          -         -
  10      24  10/10   3   10 [1-127]  58.2k   282k   26ms [9.9ms-0.29s]   54ms  0.11s   10/10 18ms     10     5/5 28ms          -         -
  10      50   8/10   1  14.5 [1-46]   284k  1.28M   0.10s [53ms-0.20s]  0.24s  0.52s   10/10 51ms   23.5            -          -         -
  10     100   5/10   4     1 [1-10]   104k  1.53M  0.15s [0.10s-0.29s]  0.25s  0.34s     8/8 76ms   5.50            -          -         -
  mixed   24  10/10  10            1  3.17k  37.5k   6.9ms [5.9ms-18ms]   10ms   12ms  10/10 4.1ms      1  10/10 1.7ms          -         -
  mixed   50  10/10  10            1  13.7k   154k     22ms [14ms-77ms]   36ms   56ms  10/10 9.4ms      1   10/10 11ms          -         -
  mixed  100  10/10   9     1 [1-11]  52.8k   584k   0.10s [88ms-0.26s]  0.13s  0.19s   10/10 20ms      1            -          -         -

band2
  k         n   cert  1L     leaf boxes   ints  bytes              produce   chkC  chkPy       search  boxes           DP     CP-SAT       MILP
  2        25  10/10   7        1 [1-2]  1.52k  18.4k   8.8ms [5.5ms-16ms]  8.4ms   13ms  10/10 6.7ms      1  10/10 1.3ms   2/2 28ms   2/2 30ms
  2        50  10/10   8        1 [1-7]  6.17k  74.3k     18ms [10ms-65ms]   22ms   39ms  10/10 7.8ms      1  10/10 2.6ms   2/2 68ms   2/2 46ms
  2       100  10/10   1    5.50 [1-12]   137k  1.14M   0.12s [49ms-0.21s]  0.24s  0.40s   10/10 27ms   5.50  10/10 5.4ms  2/2 0.10s  2/2 0.11s
  3        25  10/10   3       5 [1-17]  10.6k  75.2k    12ms [6.0ms-29ms]   16ms   31ms  10/10 8.1ms      5  10/10 1.3ms  2/2 0.11s   2/2 68ms
  3        50  10/10   1     22 [1-221]   185k  1.16M   0.11s [19ms-0.87s]  0.26s  0.44s   10/10 28ms     22  10/10 2.5ms  2/2 0.21s  2/2 0.12s
  3       100   3/10   0      37 [5-37]  1.29M  7.88M  0.51s [0.10s-0.52s]  1.26s  2.46s     6/6 98ms     63  10/10 5.6ms  2/2 0.49s  2/2 0.24s
  5        25  10/10   1      37 [1-81]   111k   551k  0.11s [7.5ms-0.22s]  0.11s  0.25s   10/10 41ms     37  10/10 1.5ms          -          -
  5        50   4/10   0   105 [73-153]  1.36M  6.39M  0.46s [0.36s-0.69s]  0.93s  2.05s    7/7 0.14s    153  10/10 2.7ms          -          -
  5      100e      -   -              -      -      -                    -      -      -    2/3 22.6s  17821    3/3 6.1ms          -          -
  10       25   3/10   0  208 [127-208]  1.18M  4.41M  0.34s [0.26s-0.36s]  0.75s  1.66s    6/6 0.23s    258  10/10 1.8ms          -          -
  10      50e      -   -              -      -      -                    -      -      -        0/2 -      -    3/3 3.1ms          -          -
  mixed    25  10/10   2       3 [1-35]  9.78k  72.8k    14ms [6.4ms-51ms]   16ms   26ms  10/10 8.1ms      3  10/10 1.3ms          -          -
  mixed    50  10/10   0   10.5 [6-168]   135k   727k    62ms [38ms-0.61s]  0.14s  0.25s   10/10 29ms   10.5  10/10 3.1ms          -          -
  mixed   100   2/10   0     23 [13-33]  1.20M  5.90M  0.49s [0.40s-0.59s]  1.05s  2.06s    5/5 0.35s    106  10/10 6.6ms          -          -

band3
  k         n   cert  1L    leaf boxes   ints  bytes              produce   chkC  chkPy       search  boxes           DP     CP-SAT       MILP
  2        25  10/10   7       1 [1-3]  1.52k  18.8k   6.5ms [6.0ms-10ms]  5.2ms  9.0ms  10/10 4.1ms      1  10/10 1.6ms   2/2 43ms   2/2 34ms
  2        50  10/10   2      3 [1-15]  18.5k   168k    24ms [16ms-0.12s]   58ms   57ms   10/10 18ms      3  10/10 3.3ms   2/2 87ms   2/2 70ms
  2       100   9/10   1     15 [1-69]   373k  2.93M  0.21s [0.11s-0.96s]  0.63s  1.12s   10/10 70ms   18.5  10/10 6.7ms  2/2 0.24s  2/2 0.18s
  3        25  10/10   1      8 [1-49]    17k   117k   21ms [7.5ms-0.12s]   27ms   42ms   10/10 15ms      8  10/10 1.5ms  2/2 0.20s  2/2 0.10s
  3        50   8/10   0  107 [21-161]   901k  5.53M  0.51s [0.12s-0.75s]  0.89s  1.75s  10/10 0.19s    120  10/10 3.4ms  2/2 0.88s  2/2 2.02s
  3       100   0/10   0             -      -      -                    -      -      -    1/3 1.35s    813  10/10 6.8ms  2/2 2.76s  2/2 9.84s
  5        25  10/10   0    71 [5-189]   233k  1.17M   0.14s [18ms-0.32s]  0.27s  0.36s   10/10 87ms     71  10/10 1.9ms          -          -
  5        50   0/10   0             -      -      -                    -      -      -    3/3 9.74s   6725  10/10 3.1ms          -          -
  5      100e      -   -             -      -      -                    -      -      -        0/2 -      -    3/3 8.0ms          -          -
  10       25   0/10   0             -      -      -                    -      -      -    3/3 1.42s   1018  10/10 4.6ms          -          -
  10      50e      -   -             -      -      -                    -      -      -        0/2 -      -    3/3 8.8ms          -          -
  mixed    25  10/10   0    33 [2-117]  87.8k   458k    58ms [12ms-0.24s]   88ms  0.19s   10/10 46ms     33  10/10 2.2ms          -          -
  mixed    50   4/10   0  40.5 [4-160]   486k  2.39M   0.27s [81ms-0.61s]  0.34s  0.68s    7/7 0.32s    160  10/10 3.5ms          -          -
  mixed  100e      -   -             -      -      -                    -      -      -    3/3 23.6s   5870    3/3 9.3ms          -          -

complete (the hard case)
  k        n   cert  1L        leaf boxes   ints  bytes              produce   chkC  chkPy       search  boxes           DP     CP-SAT       MILP
  2       10  10/10   2           3 [1-6]    705  7.37k   8.0ms [3.2ms-15ms]  2.0ms  2.8ms  10/10 7.1ms      3  10/10 1.1ms   2/2 46ms   2/2 48ms
  2       12  10/10   2           4 [1-9]  1.37k  13.7k   7.2ms [3.1ms-14ms]  2.1ms  3.3ms  10/10 5.3ms      4  10/10 1.3ms   2/2 50ms   2/2 42ms
  2       16  10/10   0          9 [3-31]  5.54k  51.9k     21ms [11ms-56ms]  7.7ms   12ms   10/10 17ms      9  10/10 6.7ms  2/2 0.39s  2/2 0.24s
  2       20  10/10   0        30 [12-73]  29.1k   263k   0.13s [45ms-0.25s]   61ms  0.12s  10/10 0.13s     30  10/10 0.12s  2/2 1.10s  2/2 0.93s
  2       24  10/10   0       69 [28-234]  96.9k   869k  0.25s [0.15s-0.88s]  0.12s  0.24s  10/10 0.19s     69            -  2/2 3.55s  2/2 2.02s
  2       28  10/10   0      357 [57-753]   685k  6.15M  1.05s [0.20s-2.56s]  0.65s  1.21s  10/10 0.73s    357            -  2/2 9.86s  2/2 3.63s
  2       32   4/10   0     641 [292-723]  1.61M  14.5M  2.72s [1.38s-4.15s]  1.54s  2.66s    7/7 2.98s    723            -  2/2 24.6s  2/2 9.11s
  2      36e      -   -                 -      -      -                    -      -      -    3/3 8.33s   3025            -      0/1 -  2/2 19.8s
  3       10  10/10   0          7 [3-27]  2.27k  19.4k    14ms [7.9ms-34ms]  3.6ms  6.1ms   10/10 12ms      7  10/10 3.3ms  2/2 1.13s  2/2 0.49s
  3       12  10/10   0         10 [3-41]  4.74k  39.3k    19ms [6.3ms-55ms]  5.7ms   10ms   10/10 17ms     10   10/10 23ms  2/2 0.38s  2/2 0.66s
  3       16  10/10   0       74 [41-149]  63.3k   490k   0.15s [78ms-0.27s]   72ms  0.13s  10/10 0.12s     74            -  2/2 8.32s  2/2 8.74s
  3       20  10/10   0    571 [213-1159]   770k  5.98M  1.45s [0.52s-2.92s]  0.80s  1.52s  10/10 1.27s    571            -  1/2 41.6s  2/2 35.4s
  3       24   0/10   0                 -      -      -                    -      -      -    3/3 5.48s   2065            -          -      0/1 -
  3      28e      -   -                 -      -      -                    -      -      -        0/2 -      -            -          -          -
  5       10  10/10   0        51 [17-69]  24.7k   169k    55ms [30ms-0.12s]   22ms   42ms   10/10 51ms     51            -  2/2 5.58s  2/2 3.64s
  5       12  10/10   0      107 [41-181]  74.5k   503k   0.16s [93ms-0.25s]   62ms  0.11s  10/10 0.11s    107            -  2/2 34.6s  2/2 13.1s
  5       16   4/10   0    707 [317-1301]   939k  6.31M  1.56s [0.96s-2.49s]  0.78s  1.51s    7/7 1.99s   1301            -      0/1 -      0/1 -
  5      20e      -   -                 -      -      -                    -      -      -    2/3 41.4s  15805            -          -          -
  5      24e      -   -                 -      -      -                    -      -      -        0/2 -      -            -          -          -
  10      10  10/10   0      433 [64-712]   364k  2.15M  0.54s [0.12s-0.85s]  0.22s  0.51s  10/10 0.47s    433            -          -          -
  10      12   2/10   0  1297 [1189-1405]  1.72M  10.1M  1.75s [1.65s-1.85s]  0.98s  1.97s    5/5 3.73s   3907            -          -          -
  10     16e      -   -                 -      -      -                    -      -      -        0/2 -      -            -          -          -
  mixed   10  10/10   0       7.50 [3-20]  3.90k  31.3k     19ms [12ms-36ms]  4.0ms  6.8ms   10/10 18ms   7.50     9/9 55ms          -          -
  mixed   12  10/10   0      18.5 [9-187]  14.7k   105k    62ms [16ms-0.35s]   16ms   30ms   10/10 68ms   18.5    3/3 0.16s          -          -
  mixed   16  10/10   0      163 [26-862]   229k  1.51M  0.78s [0.15s-3.34s]  0.24s  0.44s  10/10 0.64s    163            -          -          -
  mixed   20   5/10   0      369 [90-614]   715k  4.91M  1.49s [0.43s-2.42s]  0.50s  0.97s    8/8 1.93s    536            -          -          -
  mixed   24   0/10   0                 -      -      -                    -      -      -    2/3 15.6s   4314            -          -          -
  mixed  28e      -   -                 -      -      -                    -      -      -        0/2 -      -            -          -          -

Where each ladder stops (certified 10/10 up to -> first failure): grid k=3 49 -> 100 (7/10), k=5 49 -> 100 (0/10), k=10 25 -> 49 (0/10), mixed 49 -> 100 (7/10); cubic k=5 50 -> 100 (9/10), k=10 24 -> 50 (8/10), 100 (5/10); band2 k=3 50 -> 100 (3/10), k=5 25 -> 50 (4/10), k=10 12 -> 25 (3/10), mixed 50 -> 100 (2/10); band3 k=2 50 -> 100 (9/10), k=3 25 -> 50 (8/10), 100 (0/10), k=5 25 -> 50 (0/10), k=10 12 -> 25 (0/10), mixed 25 -> 50 (4/10); complete k=2 28 -> 32 (4/10), k=3 20 -> 24 (0/10), k=5 12 -> 16 (4/10), k=10 10 -> 12 (2/10), mixed 16 -> 20 (5/10). Everything else certified at every size run. These frontiers are those of the caps: see the second pass (section 7) for what five times the caps buys.

====================================================================================================
5. WHAT THE CERTIFICATE COSTS, AND WHAT CHECKING COSTS
====================================================================================================
Producer total / the same search without certificate, and time after the search / search [M] (certified instances; medians [min-max]):
  family     tree               instances   producer / plain search   (assemble+checks) / search   Python engine share   C engine share
  chain      1 leaf                   250     7.41 [1.06-44.7]          7.00 [0.35-45.3]              48 %                  34 %
  tree       1 leaf                   250     7.09 [0.72-52.6]          6.20 [0.28-45.9]              48 %                  35 %
  potts      1 leaf                   243     6.52 [0.80-34.6]          5.14 [0.52-27.9]              48 %                  35 %
  grid       1 leaf                   155     3.69 [0.95-30.1]          2.63 [0.77-33.1]              48 %                  35 %
  grid       2-100 leaf boxes          59     13.2 [2.79-72.4]          13.4 [1.55-69.9]              58 %                  31 %
  cubic      1 leaf                   185     6.17 [0.07-33.8]          5.43 [0.69-33.9]              48 %                  36 %
  cubic      2-100 leaf boxes          56     7.31 [0.81-89.1]          5.68 [0.61-104]               60 %                  31 %
  band2      2-100 leaf boxes          98     7.50 [1.22-85.2]          7.44 [0.82-70.8]              58 %                  31 %
  band2      >100 leaf boxes            8     24.1 [14.4-35.4]          27.1 [13.2-37.8]              60 %                  29 %
  band3      2-100 leaf boxes         101     4.50 [1.44-40.4]          3.59 [0.33-41.1]              57 %                  32 %
  band3      >100 leaf boxes           11     9.53 [3.56-22.9]          11.0 [3.12-17.5]              57 %                  32 %
  complete   2-100 leaf boxes         182     2.01 [0.95-5.56]          1.01 [0.41-3.37]              55 %                  33 %
  complete   >100 leaf boxes           61     3.07 [1.82-4.65]          2.06 [1.04-3.76]              56 %                  30 %
  A caution on the ranges: the lower ends below 1 in the second column are timing noise, not a property of the producer. I checked: 7 of 1 844 instances have producer < plain, all at 3-13 ms per run; the 0.07 is one 6-site instance whose plain run took 38 ms instead of about 1.5 ms. The medians are not affected.
  The certificate is relatively cheapest on complete graphs (x2-3: the format is not wasteful there) and dearest on sparse graphs with trees (x7-24), where each leaf drags the dense n(n-1) message vectors along.

Checking [M], by number of checker operations (certified instances):
  operations   instances   integers read          leafcert.c alone    check(obj, 'c')      check(obj, 'python')   ops/s leafcert.c   ops/s Python engine
  0 - 10k            735   887 [153-4.5k]         42us [9us-246us]    1.2ms [0.27-16ms]    1.7ms [0.36-49ms]      44.6M              1.10M
  10k - 100k         545   10.9k [1.4k-44.9k]     355us [75us-2.9ms]  9.9ms [1.2ms-0.17s]  16ms [2.6ms-0.22s]     80.5M              1.79M
  100k - 1M          395   79.6k [12.3k-372k]     2.6ms [0.5-19ms]    76ms [7ms-0.66s]     0.12s [17ms-0.85s]     109M               2.41M
  1M - 10M           147   600k [92k-1.92M]       14ms [3.7-79ms]     0.31s [53ms-2.24s]   0.59s [0.14-4.40s]     157M               4.46M
  10M - 20M           22   1.56M [690k-1.91M]     56ms [29-91ms]      0.99s [0.41-1.48s]   2.18s [0.93-2.96s]     253M               6.25M
  So: the check proper is trivially cheap in C (at most 91 ms for the largest certificates); what a user pays through check(obj, "c") is 20 times that, almost all of it strict loading and encoding in Python; and the Python engine is another factor 2 on top. Checking is cheaper than producing only if one counts the C kernel; counted as the producer must count it (both engines through the front door), checking is 74 % of the total.

Producing + checking against the fastest certificate-free baseline other than the producer's own search (DP, enumeration, CP-SAT, MILP), certified instances that needed branching [M]: band2 89 (n = 106; up to 2 782), band3 55 (112; up to 2 204), grid 22.5 (57), cubic 18.3 (37), potts 11.7 (6), complete 3.8 (160; from 0.017 to 55). On complete graphs the ratio is below 1 in 42 of 160 instances — real, not noise (producer 0.01-2.2 s there; the baselines are enumeration of 2^24 states, DP with exponential tables, or CP-SAT/MILP at 8-15 s).

====================================================================================================
6. LEAF-BOUND METHODS AND BRANCHING RULES (comparison pass: searches without certificate; same instances as the main pass)
====================================================================================================
Leaf bounds, branching strong (instances 0-4; solved, median leaf boxes, median time) [M]:
  cell                mp  boxes   time   lp  boxes   time  hybrid  boxes   time  lp/frac  boxes   time
  complete k=2 n=20  5/5     33   48ms  5/5     30  0.73s     5/5     34  0.42s      5/5     42  0.84s
  complete k=3 n=12  5/5     17   23ms  5/5     17  0.38s     5/5     17  0.12s      5/5     15  0.24s
  complete k=5 n=8   5/5     13  8.2ms  5/5     13  0.17s     5/5     13   52ms      5/5     13  0.16s
  band3 k=3 n=25     5/5     11   12ms  5/5      9  0.13s     5/5      9   63ms      5/5     33  0.40s
  band3 k=5 n=25     5/5     17   14ms  5/5     25  0.73s     5/5     25  0.24s      5/5     29  0.89s
  band2 k=5 n=25     5/5     29   15ms  5/5     29  0.43s     5/5     29  0.14s      5/5     41  0.52s
  grid k=5 n=25      5/5      1  3.2ms  5/5      1   20ms     5/5      1   15ms      5/5      1   21ms
  grid k=10 n=25     5/5     37   11ms  5/5     28  0.55s     5/5     28  0.13s      5/5     10  0.30s
  cubic k=5 n=24     5/5      1  2.1ms  5/5      1   16ms     5/5      1   13ms      5/5      1   15ms
  Reading: (a) rounded LP duals and integer message passing give trees of the same size within a factor 0.88-1.20 (per-instance median ratio), so the weaker fixed points of message passing cost little here; (b) one cold LP per node costs 7 to 52 times more time; (c) rounding loses 0-3 units in the median (at most 9) against table entries up to 1000; (d) all 36 certificates built from rounded LPs (lp/strong and hybrid/strong, instances 0-1 of the nine cells) were accepted by both engines [E]; (e) branching on the LP's most fractional site ("frac") is not better than strong branching and is 3.7 times worse on band3 k=3. Not tested: LP with warm starts, larger cells (the LP is too slow there for this budget), more than 5 instances per cell — the comparison is thin.
  On forests all three methods give one leaf: by construction for mp; for lp an observation (120 instances in the test-suite, up to 45 sites; two development instances at n = 100, k = 10) — HiGHS returned integral multipliers every time, which I did not prove.

Branching rules, bound mp (10 instances; median leaf boxes, median time) [M]:
  cell                   solved  strong   time  maxdeg   time  margin   time  maxdom   time
  band3 k=3 n=50          10/10     120  0.11s     176   87ms     192  0.10s     176   85ms
  band3 k=5 n=50          10/10    5305  4.65s   12483  5.36s   12431  5.89s   12483  5.85s
  band2 k=5 n=50          10/10     291  0.15s     713  0.12s     523  0.11s     713  0.12s
  grid k=5 n=49           10/10      13   18ms      21   13ms      19   13ms      21   14ms
  cubic k=5 n=50          10/10       1  6.6ms       1  7.1ms       1  6.1ms       1  6.5ms
  complete k=2 n=20       10/10      30   48ms      42   43ms      38   42ms      42   42ms
  complete k=3 n=12       10/10      10   15ms      15   11ms      15   10ms      15   10ms
  complete k=5 n=10       10/10      51   33ms      47   22ms      47   22ms      47   24ms
  complete k=10 n=8       10/10      73   57ms      91   35ms      82   35ms      91   36ms
  complete k=mixed n=12   10/10    18.5   39ms    21.5   35ms    21.5   34ms     174   56ms
  grid k=mixed n=49       10/10       3  7.1ms       4  7.5ms    3.50  8.7ms    14.5  7.7ms
  band3 k=2 n=50          10/10       3  7.1ms      15  8.2ms    3.50  6.9ms      15  9.4ms
  band2 k=3 n=50          10/10      22   16ms      42   13ms      35   11ms      42   12ms
  grid k=3 n=49           10/10       1  4.5ms       1  4.5ms       1  4.3ms       1  4.0ms
  grid k=10 n=49          10/10     464  0.37s     676  0.29s     676  0.30s     676  0.30s
  cubic k=3 n=50          10/10       1  4.2ms       1  3.9ms       1  4.2ms       1  3.9ms
  potts k=5 n=49          10/10       1  5.6ms       1  6.1ms       1  5.8ms       1  5.2ms
  Reading: strong branching (re-optimise the children of the three sites with most free neighbours on a cycle, take the site whose weakest child is strongest) gives the smallest median tree in 16 of 17 cells, typically 1.4-3 times smaller, at 0.7-1.4 times the time; since the certificate, not the search, is the bottleneck, smaller trees are worth more than faster nodes. "Largest remaining domain" (maxdom) is the same rule as maxdeg when all alphabets are equal and is 2.5-6.9 times worse on mixed alphabets (it branches on the 10-state sites first). All rules restrict candidates to sites on a cycle of free sites (elsewhere the relaxation loses nothing).
  A rule I tried in development and removed (so it is not in the table): choosing the site whose children keep the least total gap judged by the node's own messages gave trees 10-100 times larger on bands and grids (it picks sites whose non-preferred states are pruned at once and whose preferred child gains nothing).

Shared leaves [E]: distinct leaf certificates against leaf boxes over certified instances with at least two boxes: k=2 0.0 % saved (105 instances; structurally impossible for two states), k=3 0.1 %, k=5 3.8 %, k=10 11.1 %, mixed 5.1 %. In the comparison pass the same search without sharing evaluates up to 25 % more nodes (grid k=10 n=49: ratio 0.75 [0.52-0.94]). A modest saving.

====================================================================================================
7. SECOND PASS (600 s, caps x5) AND AN EXPLORATORY PROBE
====================================================================================================
Second pass, by the rule of the protocol (first cell where a solver missed, its first two missed instances) [M]:
  instance                 solver               at 60 s / main caps      second pass   time     detail
  band3 k=3 n=50 r=0       producer (caps x5)   limit (integers)         certified     9.98s    507 boxes, 4.37M integers, search 0.53s, assemble+checks 9.45s
  band3 k=3 n=50 r=2       producer (caps x5)   limit (integers)         certified     10.2s    543 boxes, 4.65M integers, search 0.54s, assemble+checks 9.67s
  complete k=2 n=32 r=0    producer (caps x5)   limit (integers)         certified     30.0s    3041 boxes, 7.64M integers, search 6.58s, assemble+checks 23.4s
  complete k=2 n=32 r=2    producer (caps x5)   limit (integers)         certified     16.4s    1691 boxes, 4.25M integers, search 4.01s, assemble+checks 12.4s
  complete k=5 n=16 r=0    producer (caps x5)   limit (integers)         certified     8.76s    2829 boxes, 3.76M integers, search 2.64s, assemble+checks 6.12s
  complete k=5 n=16 r=1    producer (caps x5)   limit (integers)         certified     5.30s    1641 boxes, 2.18M integers, search 1.71s, assemble+checks 3.59s
  grid k=5 n=100 r=0       producer (caps x5)   limit (operations)       limit         0.24s    stopped at the operation cap again
  grid k=5 n=100 r=1       producer (caps x5)   limit (operations)       certified     5.88s    61 boxes, 3.16M integers, search 0.11s, assemble+checks 5.77s
  complete k=2 n=36 r=0    CP-SAT               limit                    optimal       125.6s
  complete k=5 n=20 r=2    search w/o cert.     limit                    optimal       105.9s   87 513 leaf boxes
  Reading: five times the caps moves the producer's frontier by about one step of the ladder at 5-30 s per instance (7 of 8), most of it assembling and checking; ten times the time moves the search and CP-SAT by a similar step. With geometric growth (x1.3-2.6 per site on complete graphs) neither changes the picture. [C] Beyond these sizes the certificate of the last instance above would have about 87 000 leaf boxes, i.e. roughly 10^8 integers: outside the C engine's 2^26 limit.

Exploratory probe (not in the protocol; integrality_probe.py) — why branch when the relaxation is tight at the root? Of 1 266 certified instances with a tight relaxation the producer needed more than one leaf in 6 [E]:
  instance                 optimum   mp root bound   short by   mp leaf boxes   lp root bound   lp leaf boxes   tables scaled
  band2 k=3 n=50 r=7        -57602          -57830        228              25          -57602               1   -
  band3 k=mixed n=25 r=9    -37955          -38241        286               2          -37956               2   x2: lp 2 leaves (root -75911 vs -75910); x6: lp 1 leaf (root -227730 = 6 x optimum)
  cubic k=10 n=100 r=7     -152992         -153016         24              10         -152992               1   -
  cubic k=10 n=50 r=3       -74813          -74851         38              10          -74813               1   -
  cubic k=10 n=50 r=6       -80893          -80945         52              10          -80893               1   -
  cubic k=5 n=100 r=8      -126561         -126570          9              37         -126561               1   -
  In five the rounded LP certifies with one leaf: integer messages exist and the message passing stalled 9-228 units below them (a weakness of coordinate ascent, curable by the hybrid bound). In one the rounded LP misses the optimum by exactly one unit, still misses at twice the unit, and certifies with one leaf at six times the unit: there the instance needs messages in thirds of its own unit, which the format cannot express — it has to branch. One such case in 1 266: rare for these tables, but it is a property of the format at zero margin (L = the minimum exactly), not of the producer.

====================================================================================================
8. FINDINGS ABOUT THE FORMAT AND THE CHECKER
====================================================================================================
No defect found in the checker or in experiments/eng/leafcert/REPORT.md; my operation formula reproduces the checker's counts on every certificate, and the two engines agreed on all 1 897 certificates of the benchmark. What follows are properties and costs, with numbers.
F1 Density [E]. Every leaf carries n + n(n-1)/2 + (n-1) sum k integers whatever the graph. At the largest certified size of each ladder a dense leaf / a sparse-variant leaf (edges only): chain and tree 42-48 (104 050 vs 2 179 integers at n = 100, k = 10), cubic 29-32, potts and grid 25-27, band2 23-24, band3 16, complete 1; the checker's operation count has the same ratios (formats.py defines the sparse counts; no checker for a sparse variant exists). Consequence [E]: at n = 100 the 2 M cap admits 19 leaf certificates for k = 10, 36 for k = 5, 57 for k = 3, 80 for k = 2; a sparse variant would admit 16-48 times more, which at the measured growth rates is roughly one more step of each sparse ladder [C].
F2 Dead data [E]. The format wants a message vector over the whole alphabet of a site; entries for states outside every box on which the leaf is used are read by no inequality. In trees with more than 100 leaf boxes 11-19.5 % of all message integers are never read (per instance 12-25 % in the median, up to 27 %); 0 % in one-leaf certificates. The checker rejects unused leaf certificates as dead data but cannot reject these.
F3 One child per state [E]. A leaf shared by several children is re-checked on every child's box. Checking each shared leaf once on the union of its boxes (a "these states | the others" rule, the science division's P7-T2) would reduce the operations of our certificates by a factor 1.00-1.18 in the median (largest 3.27, k = 10) — far less than the 3.8-6.7 they measured on their files, because our trees are deep with few shared leaves while theirs are one branching on a many-state site.
F4 Integer messages at zero margin: section 7 (one instance in 1 266 needs thirds of the unit). For the science division's use (a margin, units of 2^-40) this does not arise; for "L = min E exactly" on integer tables it can force a branching that the real-valued relaxation does not need.
F5 Optimality is not part of the verdict. The checker proves E >= L; that L is attained is only the annotation "ref" (reported as a note if E(ref) != L, never a rejection). The producer writes "ref" whenever its state attains L and the tests require an empty note list, but a consumer who wants "min E = L" certified must check the note, or the format needs an optional strict "attained" mode.
F6 Front door and limits [M]. check(obj, "c") is 96 % Python (strict loading, validation, encoding); the stand-alone C path on pre-encoded text would be about 20 times faster. Peak resident memory of a producer run was at most 565 MB at 1.9 M integers (worker baseline about 190-230 MB); the C engine's 2^26-integer limit would need several GiB through the front door — in practice memory, not the C limit, bounds certificate size. JSON is 4.6 bytes per integer for these tables (largest file 16.4 MB).
F7 Large inputs. REPORT.md section 8 lists as largest inputs the nine files, a 200-site instance and a 40-site chain; this benchmark adds 1 844 accepted certificates up to 1.91 M integers / 1.7e7 operations / 1 405 leaf boxes / depth 20 with identical verdicts and counts in both engines.

====================================================================================================
9. DEVIATIONS FROM THE PROTOCOL (all recorded in PROTOCOL.txt section 9)
====================================================================================================
No rule was changed and no budget was reached: main pass 2 047 s (budget 3 840 s), all 211 cells the stop rules allowed, none cut; comparison pass 526 s (budget 1 200 s), all 24 cells; second pass 175 s (budget 960 s), all 10 tasks the rule produced. Together 2 748 s, 2026-11-26 23:17 UTC to 2026-11-27 00:03 UTC.
Additions after the freeze, none changing a stored number: A1 integrality_probe.py (exploratory, section 7); A2 make_tables.py extended after the first results were seen (compact tables, "ended by" column, probe table, how the hypothesis numbers are printed) — it only reads stored results; A3 a spot re-run of one random instance per cell (199 runs, nothing stored): same instance checksum, same status in 199 of 199, byte-identical certificate in 186 of 186.
What did not go as assumed: B1 H7's expectation (integer cap) was wrong, the operation cap bound more often; B2 because of the rule on the search without certificate, "the search solves the failed instance" could be checked on 45 of 101 failures only; B3 the machine was less loaded than in development (load average 7.3 at the start of the main pass, 2.8 at its end, 2-3 afterwards, 9-14 during trials), so times are not comparable with the trial runs and the passes finished far inside their budgets; B4 an operator error without effect on data: a shell command queued to start the comparison pass waited on a condition that could not become true and was killed before starting anything; a corrected command ran the remaining passes in the protocol's order.
Things a reviewer should know that are not deviations: the size caps and the baseline rules were set after trial runs on development seeds showed what a cell costs (PROTOCOL section 0 says so); the CP-SAT setting was chosen on development instances; MILP is an addition of mine to the four baselines you listed.

====================================================================================================
10. WHAT WAS NOT TESTED; LIMITATIONS
====================================================================================================
* Only unstructured random tables (and one structured family, Potts); no instance with a physical origin in the benchmark (the four published instances are in the test-suite only). The frontiers are for entries of magnitude 1000 with fields as strong as couplings; other ratios will move them.
* n > 100, alphabets above 10 (the published instances have up to 30 states), other certificate formats (triplets / sum).
* The frontiers are those of two budget-driven caps (2 M integers, 20 M operations); only 8 producer runs were made at five times the caps. A producer limited by the 60 s clock alone was not run (it would need certificates of 10^7-10^8 integers and several GiB).
* CP-SAT and MILP: 2 instances per cell, ladders with k in {2, 3} and three ladders with k = 5 only; CP-SAT with one worker (its multi-worker portfolio is much stronger); no other exact solver (no toulbar2-class WCSP solver was available). The DP and enumeration baselines are my own implementations (agreeing with everything else on 1 885 instances).
* The search without certificate on certified instances and on at most three uncertified ones per cell; extension cells have 3 instances.
* Leaf-bound comparison: 9 small cells, 5 instances each; LP without warm start. Depth-first order, the "margin" and "frac" rules beyond the comparison cells, and partial certificates were not benchmarked (they are tested for correctness).
* Timings: one shared laptop CPU with three other agents running; no repetition of timed runs; medians and ranges only, no confidence intervals; growth factors are two-point estimates.
* Memory: peak resident size per producer run only (VmHWM reset before each run); reading a certificate from a file was not timed (objects were checked in memory; JSON size is reported).
* The certificate is for the integer instance in the file; nothing here concerns where the tables come from, nor Lean.
* The integer ascent has no convergence guarantee beyond monotonicity and exactness on forests; that HiGHS returns integral multipliers on forests is an observation.

====================================================================================================
11. COMMANDS AND RUN TIMES
====================================================================================================
  source "$HOME/.venvs/metricchain/bin/activate"
  python -m pytest tests/eng/test_leafprod.py -q                      40 passed; 12.8 s idle, 37-75 s on the loaded machine
  LEAFPROD_FUZZ=10 python -m pytest tests/eng/test_leafprod.py -q -s  (not run at 10; scales the random tests)
  python -m pytest tests/eng/test_leafcert.py -q                      182 passed, unchanged (118 s under load)
  python experiments/eng/leafcert_bench/run_bench.py main             2 047 s wall, two workers
  python experiments/eng/leafcert_bench/run_bench.py compare            526 s
  python experiments/eng/leafcert_bench/run_bench.py long               175 s
  python experiments/eng/leafcert_bench/integrality_probe.py              2 s   (exploratory)
  python experiments/eng/leafcert_bench/make_tables.py                    2 s   writes results/tables.txt; --verify compares (passes)
  Options of the driver: --master (seeds), --out, --budget, --only FAMILY, --levels, --resume, --time-limit (for trying it out).
Files to look at first: experiments/eng/leafcert_bench/PROTOCOL.txt; experiments/eng/leafcert_bench/results/tables.txt (all tables, including the cell-by-cell ones and the numbers behind every verdict above); src/metricchain_eng/leafprod/__init__.py (interface) and kernel.c (the header states the ascent and why it is monotone).
Every number in this report was taken from results/tables.txt or computed from the stored result files; three small summaries (time totals by phase, the count of 60 failures with a complete search and their would-be sizes, the per-family ratios against the fastest baseline, the check that the 42 ratios below 1 are all complete-graph instances and that the 7 producer-below-plain cases are millisecond noise) were computed by ad hoc scripts that are not in the repository — say if you want them added to make_tables.py.
```
