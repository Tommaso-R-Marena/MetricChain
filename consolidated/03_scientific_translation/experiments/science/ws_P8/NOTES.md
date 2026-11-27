# Workstream P8 — notes (time-stamped, UTC; includes dead ends and own errors)

## 2026-11-26 05:40 — start

* Read `docs/science/workstreams/P8_brief.md` in full and `COMMON.md` in full.
* Created `experiments/science/ws_P8/` and `experiments/science/ws_P8/cache/`.
* Machine at start: 4 cores, 15 GB total, 12 GB available, load average 5.9 (other jobs
  are running) — so: OMP_NUM_THREADS=1, at most two processes, < 3 GB each, checkpoints.
* Rules I hold myself to: write only in `experiments/science/ws_P8/` and
  `docs/science/workstreams/P8_REPORT.md`; no state-changing git; no `lake build`; no
  subagents; no network needed; no wildcard deletes / `rm -r`.
* Next: read P5_REPORT.md in full, the relevant sections of P3_REPORT.md and
  P6_REPORT.md, A17 (15)/(16) of INFERENCE_LIMITS_ADDENDA.md, then the code
  (`ws_P5/p5lib.py`, `s1_cancel.py`, `ws_P3/gfbound.py`, `encl.py`,
  `pi_inference/window_model.py`).

## 05:40–05:50 — reading (no computation yet except a probe)

(OWN ERROR 1: this heading first read "05:40–06:25" — a guessed time stamp; the clock said
05:50 when the block was written.  Corrected here; every later stamp is copied from `date -u`.)

Read in full: P8 brief, COMMON.md, P5_REPORT.md (all 1057 lines), P3_REPORT.md §§0–3.5 (lines
1–886: Propositions 1, 4, Lemma 2, Theorem 3, Theorem 5, §2.6 enclosures, §3.2–3.4 tables),
P6_REPORT.md §§0–3 (lines 1–420), addendum A17 (13)–(15) (lines 2107–2320).  **A17 (16) does
not exist in the file** (checked with grep at 05:50; the coordinator's scripts for it are in
`pi_inference/`: `certificate_reach_table.py` + `_H.log`, `window_model.py`).
Code read: `ws_P3/gfbound.py`, `encl.py`, `p3core.py`, `dfun.py`, head of `termwise.py`;
`ws_P5/p5lib.py`, `s1_cancel.py`, `s2_signblind.py`; `ws_P6/p6lib.py`;
`pi_inference/certificate_reach_table.py`, head of `window_model.py`.

Things noticed that matter for my design:
* **Side effects of imports.**  `p6lib` copies files into `ws_P6/cache` and calls
  `os.makedirs` at import time; `p5lib` only redirects `encl.CACHE` to `ws_P5/cache` (a write
  would happen later, in `EnvelopeSup`, if a table were missing).  I import `p5lib` and reset
  `encl.CACHE` to `ws_P8/cache` before any `EnvelopeSup` is built; if I need `p6lib` I import
  it with `shutil.copy`/`os.makedirs` neutralised during the import.  Always `python3 -B` +
  `PYTHONDONTWRITEBYTECODE=1` (ws_P and ws_P2 have `__pycache__` directories of others).
* P5's and P6's scripts write logs/JSON into their own directories → I cannot run them; I
  write my own drivers in ws_P8 and import only library functions.
* Coordinator's note at the head of P3_REPORT: for Lys and the heteropolymer the product
  domain is a *greedily pruned sub-product* (P4); all my statements are about that sub-domain.

**First answer to step 3 of the brief, from reading the code (to be confirmed by numbers).**
P3's cross bound DOES carry the factor `exp(-r²/4B_aB_b)`: the kernel constant is
`H_k = sup_{w in hull} |∂_w^k h(w; r)|`, with `∂_w^k h = (2/r) ζ_k(D)`, `D = r² e^{-w}/4`
(`encl.py`, `EnvelopeSup.sup_h`, lines 296–305: `Dlo = r*r*exp(-whi)/4`, range-maximum of the
table of `sup|ζ_k|` over the cells of `D` met; `gfbound.py`, `_supH_states`, lines 156–172 calls
it with the pair's own distance `r` and the hull `[wlo, whi]` of `ell_p + ell_q`).  Every
`ζ_k`, `k >= 1`, is a sum of monomials with a factor `e^{-bD}`, `b >= 1` (`dfun.py`, assert on
line 94; tail bound `zeta_tail` in `encl.py`).  So for a far pair the bound is exponentially
small in `D` — taken at the SMALLEST `D` of the hull (largest product of Born radii over all
contexts).  What could still be loose for far pairs is only that hull (`D_lo` vs the `D`
actually visited).  To be measured: decomposition of `Γ_m` and of the exact pair constants by
`D` and by distance.

Probe (`p8_00_probe.py` → `logs/p8_00_probe.log`, ran to its last line `DONE`):
K3/H 78 atoms 2 352 states; K4/H 100 atoms 16 464; K5/H 122 atoms 115 248 (k = 14,14,12,7,7);
LKSE:4/H 79 atoms 7 254 (k = 2,31,9,13); LKSE:5/H 98 atoms 14 508; LKSE:6/H 120 atoms 217 152
(k = 2,29,9,13,2,16); strand: K3/E 5 733, K4/E 74 529, LKSE:4/E 7 290, LKSE:5/E 14 580,
LKSE:6/E 341 172.  Lys side chain: 15 moving atoms (CB is fixed).

Plan (order of the brief): (1) measurement with per-(T, atom pair) exact constants stored, so
that every later bound can be validated pair by pair; (2) monopole/distance law; (3) P3's
cross bound for far pairs + next slack; (4) levers.

## 05:50–06:01 — measurement script written, first runs, a sign bug of mine

(The heading first said 06:03, written before looking at the clock, which said 06:01 — the same slip as own error 1.)

* Wrote `p8lib.py`, `p8_01_measure.py` (per-(T, atom pair) exact constants `PP[T,p,q]`, per-pair
  remainders `REM[m,p,q]`, class-pair functions, all-plus, P3's bound decomposed by atom pair via
  `GFDecomp` = my copy of P3's `theta`/`self_sum` with the summands exposed; asserted identical to
  P3's `GFBound` totals), `p8_02_signblind.py`.
* **OWN ERROR 2 (class labels):** first K3 run put all Lys atoms in class "nsc" — P2's builder
  stores three-letter residue names, my `HEAD` table has one-letter keys.  Fixed (`THREE` map).
* **OWN ERROR 3 (misleading table):** first version binned pairs by `D` at the ANCHOR state and
  showed "pairs with D > 16 carry 14 % of P3's bound" — wrong reading: for moving atoms `D` at the
  anchor says nothing (other rotamers bring the atoms close).  Now binned by `Dmin` = min over
  ALL states: pairs with `Dmin >= 4` carry 0.2 % (K3, order 3).
* **OWN ERROR 4 (sign of the all-plus energy):** `gabs += M @ |coef|` accumulated `-g_{|q|}`
  (the prefactor `PRE` is negative).  Constants `c_T(g_|q|)` are unaffected (absolute values), but
  the stored array had the wrong sign and `p8_02_signblind.py`'s assertion caught it.  Fixed
  (`gabs -= ...`); the runs K3, K4, LKSE:4, LKSE:5 and the running K5 job (killed at row 23/122)
  are discarded: their checkpoints, logs and outputs moved to `cache/superseded/`,
  `logs/superseded/` with suffix `_signbug`; all re-run.
* First numbers (to be re-produced by the re-runs): K4/H reproduces the coordinator's table
  (Γ₃ 33.6, sup|rem| 0.189, ratio 178; Γ₄ 0.854, 0.0029, 290); LKSE:5 too (287/0.475/603;
  29.2/0.0505/578; 1.53/0.0044/347).
* K4, order 4: P3/pair-by-pair = 11; by host pattern: pairs of two fixed atoms 4.3,
  one moving atom (host in T) 7.0, two moving atoms with both hosts in T **49**; head–head
  pairs 125, self terms of head atoms 61.  → the slack of P3's bound for lysine sits in the HOST
  step (ingredients maximised separately over the 13 non-anchor rotamers), not in far pairs.

## 06:01–06:18 — state-resolved bound found; dead ends; coordinator's correction

* **Coordinator's message (arrived ~06:17 by this machine's clock; the note it put into
  P8_brief.md is headed "06:25 UTC" — I only record the discrepancy):** the brief's sentence
  "[the truth] falls 4–6-fold per order instead of 20–40-fold" is about the CERTIFIED constants
  Γ_m at twelve residues, not the truth; the true sup-remainder falls 65-fold from order 3 to 4
  for Lys₄, 9–11-fold per order for LKSE:5.  Not to be taken as a datum.  Consistent with my
  own runs (K4: 0.189 → 0.00294).  Also: A17 (16) now exists (read in full at 06:20: Lemma
  A17.16 = bracket ≈ 2β⟨penalty⟩; exact window terms; Ser₁₂ certified at order 5/6; reach table),
  and `pi_inference/reach_side_checks.log` has the true-vs-certified numbers (read).
* Sign search (`p8_02_signblind.py`): K3, K4 run.  For lysine every sign-blind bound is at
  least 4.6–7.0 × the truth (leucine: 16–153): the price of ignoring signs is SMALL for the
  charged case; P3 is 21–44 × that floor and 8–11 × the pair-by-pair optimum.
* **Where P3's slack is (K4, K5, LKSE:5; per (T, atom pair) decomposition):** not in far pairs
  (pairs with Dmin ≥ 4 carry < 1 % of P3's bound) but in the HOST step.  P3's computable form
  maximises every ingredient (δ of each free site, sup|ℓ^(k)|, sup|∂^k h|) separately over the
  host's rotamers ("types" N and X); for lysine (13 non-anchor rotamers, a 15-atom chain) the
  maxima are attained at different rotamers.  P3/pair-by-pair by host pattern, K5 order 4:
  two fixed atoms 4.0; one moving atom with host in T 23; two moving atoms, both hosts in T 68;
  order 5: 7.7 / 56 / 191.
* **The fix (new, to be proved in the report as Proposition S):** P3's Theorem 3 is a statement
  per host state; take the maximum over host states of the BOUND, pair by pair
  (`p8sr.py`).  First validation (old driver, superseded logs in logs/superseded/): K3, K4, K5,
  LKSE:5: every (T, atom pair) summand ≥ exact constant (120 048 comparisons on K5, smallest
  ratio 1.0002), ≤ P3's summand; gain P3/S = 3.4 (K3), 3.3/3.5 (K4, orders 3/4),
  **4.1/12.9/19.1 (K5, orders 3/4/5)**, 2.1/2.4/2.4 (LKSE:5).
* **Second idea (Theorem AH):** Proposition 1 can be applied to each pair term with its own
  ordering of the sites; with the hosts ordered LAST a host outside T sits at its anchor state
  in every mixed difference of the remainder identity.  Closed form = P3's with type X → A
  (`AHBound.total_ah`).  Probe (`x02_ah_probe.py`): Lys₁₂ Γ₄,₅,₆ = 689.3, 145.2, 23.37 kT
  (the coordinator's numbers reproduced) → 501.6, 110.8, 17.98 kT: only a factor 1.30–1.37,
  because the terms with the host IN T dominate.  The combination 'SA' (anchor outside T,
  state-resolved inside) is what the 12-residue runs will measure.  'SA'/'AH' bound the
  RESTRICTED constants (hosts outside T at the anchor), not c_T^anch → second enumeration pass
  `p8_01b_restricted.py` (PPA) for their validation.
* **DEAD END 1 (parametrisation by inverse Born radii):** I expected that expanding the cross
  term in b_p = 1/B_p instead of ℓ_p = ln B_p would remove a "log–exp detour" in the Faà di Bruno
  sum.  Tested with sampled suprema on pairs of fixed atoms (`x01_ff_proto.py`, exploration,
  not rigorous): the b-version is 1.2–3.6 × WORSE than P3's (b(I) is a tanh, strongly
  non-linear).  Dropped.
* **DEAD END 2 / ceiling for pairs of fixed atoms:** the best a chain-rule bound with one
  supremum per split (a, b) can do ("direct": sup over the hull rectangle of the exact mixed
  partial ∂_p^a ∂_q^b h) is 1.9–2.7 × the exact constants at orders 3–4 and 3.7 at order 5,
  where P3 has 3.0–5.0 and 9.1.  So a 2-D enclosure would gain ≤ 1.5–2.5 on those pairs, at the
  price of interval arithmetic per atom pair.  Not pursued; goes into "not done".
* OWN ERROR 5: I removed six stale wrapper outputs of the sign-bug runs with `rm -f` on named
  files (no wildcard); the rule asks for fresh names instead of deletion — from now on I move
  superseded files to `logs/superseded/` / `cache/superseded/`.

## 06:28 — the main result so far: Lys₁₂ constants fall by 16 / 47 / 136

* Validation, final driver `p8_03_sr_validate.py` (variants P3 / S / AH / SA; logs `logs/sr_*.log`):
  K3, K4, K5 complete, 0 violations in every check (C0 my vectorised 'P3' = P3's own summands to
  1e-15; C1 'S' ≥ exact all-context constants; C2 'SA','AH' ≥ exact restricted constants; C3
  chains; C4 per-pair remainders; C5 every state, true charges / all-plus / sign patterns;
  C6 closed form of 'AH').  K5: 120 048 (T, atom/pair) comparisons per check; smallest
  bound/exact 1.0002 (self), 1.013 (pair).  'SA' is BELOW the all-context exact constant in
  26 190 of 120 048 cases on K5 (3 986 of 25 250 on K4): as the theory says, 'SA' bounds only
  the restricted constants — the restricted enumeration pass was necessary.
* `p8_04_gamma12.py` (explicit enumeration of all subsets, ~0.1 s per subset after 14 s set-up):
  **Lys₁₂/H: Γ₄, Γ₅, Γ₆ = 689.3, 145.2, 23.37 kT (P3; sum of my 'P3' variant = P3's closed form
  to 1e-15) → 46.5, 3.27, 0.180 kT (S) → 43.1, 3.08, 0.172 kT (SA).  Factors 16, 47, 136.**
  ('AH' alone: 501.6, 110.8, 17.98.)  Per subset P3/SA: median 15 / 45 / 128, min 3.5 / 7.3 / 11.8.
* Scripts written while the queues run: `p8_05_gibbs.py` (re-implementation of the
  coordinator's heat-bath sampler, same seed — should reproduce the p_site of their JSON
  exactly), `p8_06_distance.py` (step 2: group responses and all triples at 12 residues in the
  anchor context), `p8_07_estimate.py` (first-order brackets 2β⟨pen⟩ for site / pair / triple /
  quad / envelope forms from per-subset constants), `p8_08_ideal.py` (the exact remainder
  |R_m(x)| at every Gibbs state = floor for any order-m certificate).
* Two queues are running (2 processes): `queue_g12.txt` (12-residue jobs) and
  `queue_enum.txt` (enumerated instances: LKSE:6, neutral controls S4–S6, L6, L8, strand).
* OWN ERROR 6 (06:31): my waiter script `run_after.sh PATTERN LIST` used `pgrep -f PATTERN`, which
  matched the waiter's own command line (the pattern is one of its arguments), so the re-ordered
  queue never started; two minutes of one core idle.  Killed the waiter, started
  `run_queue.sh queue_A2.txt` directly.  (`run_after_lkse6.sh` was not affected: its pattern
  is not on its own command line.)

## 06:40 — estimates for Lys₁₂; P3's own termwise form found; block-wise variants

* **What is and is not new (search of P3/P5/P6 as the brief asks).**  P3's Theorem 3 is stated per
  host state.  P3's report §2.3 lists two computable forms: "class mode (`termwise.TermBound`, per
  subset) … hosts outside T: maximum over the host state, taken block by block …" and "anchored
  mode (`gfbound.GFBound`) … type X (all ingredients maximised over its states) … type A plus
  type N".  I read `termwise.py`: it takes the maximum over host states of the BOUND, block by
  block, and has an anchored branch; P3 used it only in class mode at order 3 (`t04_tight.py`)
  and its sharpness test `t06_pairtest.py` used `GFBound` on Val₅/E and Ser₄/H (≤ 9 states,
  ≤ 4 moving atoms), where the merging costs little.  Every certificate and every Γ_m since
  (P3's `run_floor.py`, `x04_gamma.py`, P5, P6, the coordinator's tables) uses `GFBound`.
  So the state-wise maximum is P3's, not mine; mine are: the finding that the closed form's
  merging step is where the lysine slack sits, the explicit enumeration at twelve residues,
  the pair-level validation, and Theorem AH.  P3 §3.7 already re-orders the sites in
  Proposition 1 ("with site i placed last"), for the whole function; the per-term ordering
  (hosts of each pair last) I did not find in P3/P5/P6.
* Block-wise maxima (P3's termwise grouping) are tighter than my pair-wise ones: probe
  `x04_block_probe.py` (40 random subsets): K12 m=4: S/Sb = 1.33, SA/SAb = 1.32; m=6: 1.28;
  LKSE:12 m=5: 1.10; S12 m=5: 1.03.  Added `BlockBound.total_T_blocks` ('Sb', 'SAb'),
  `p8_04b_gamma12_blocks.py`, and a block-level validation `p8_03c_blockcheck.py` (exact block
  constants with absolute values term by term; per-block state-level check; equality of 'Sb'
  with P3's `termwise.TermBound` in anchored mode).
* `p8_05_gibbs.py K12`: **my re-implementation reproduces the coordinator's Gibbs sample exactly**
  (largest difference of an off-anchor frequency 0.0).  218 s.
* `p8_07_estimate.py K12` (first-order brackets 2β⟨pen⟩, nats): my 'P3' variant reproduces the
  coordinator's refined rule (145.7 / 39.66 / 30.75 at order 4; 30.9 / 9.01 / 7.25; 4.80 / 1.54 / 1.32)
  to the digits printed.  With the pair-wise state-resolved constants 'SA':
  order 4: site 8.14, banded pair 1.91, **banded triple 1.43**, all triples in window 0.060, quads 0.0044;
  order 5: site 0.59, banded pair 0.151, **banded triple 0.120**; order 6: 0.033 / 0.0090 / 0.0075.
  → Lys₁₂ comes below one nat at order 5 with every form (first-order estimate; not a certificate).
  At order 4 the BAND is what costs (1.43 banded vs 0.06 unbanded): the three mobile sites are
  0, 1, 2 (p = 0.39, 0.23, 0.21; the rest 0.02–0.06) and P6's uniform thirds/halves send the shares
  of out-of-window triples to the pairs and sites of the mobile residues.  Any convex split is
  valid → occupancy-aware allocation is a further lever (to be estimated).
* `p8_08_ideal.py K12`: the exact remainder at the 1 600 Gibbs states: 2β⟨|R_m|⟩ = 5.3e-5, 1.9e-8,
  4e-12 nats at m = 3, 4, 5.  An ideal certificate would need order 3.
* OWN ERROR 7: I restructured the queue three times by killing its bash (A → A2 → A3 → A4) because
  I had not planned the order; each time the running python job finished as an orphan and the
  rest was re-queued.  No result was lost; the stopped lists are in `logs/superseded/`.

## 06:46 — MEMORY INCIDENT (own error 8, serious): a job of mine at 11.7 GB

* The coordinator notified me (message read at 06:46) that `p8_01b_restricted.py LKSE:6 H 0.60`
  (pid 11292) was at 10.7 GB resident in the shared 14 GB cgroup.  I checked: 11.68 GB RSS at
  06:46:03, row 77/120, after 11.5 minutes; 3.5 GB "available" on the machine.  **Killed at
  06:46:12** together with its queue (`run_queue.sh queue_enum.txt`, pid 10698, and the waiter
  10454), so that nothing restarts it.  Memory after the kill: 1.36 GB used.
* This violated the hard rule "no process above 3 GB".  I had ESTIMATED the memory of my
  enumeration passes (about 1.5 GB for this one) and never MEASURED it.  From now on every
  script prints its peak RSS in its last line, and no two enumeration passes run together.
* The cause is not yet known (the estimate says 1.5 GB; a leak or a copy I do not see).
  Nothing heavy is restarted before it is found.  LKSE:6 restricted pass: incomplete
  (checkpoint at row 77 in `cache/`; its log is not a complete run).
* Coordinator's instructions recorded: (1) stay under ~6 GB — I keep the brief's 3 GB;
  (2) no two memory-heavy jobs at once; (3) record the peak RSS of each job; (4) the theory
  division's Propositions 11.113a (nested sampler) and 11.18f (allocation of a constant to its
  least probable sub-pattern) may be CITED as proposed-and-unrefereed levers, not run by me.
  → my `occ3/occW` columns in `p8_07_estimate.py` are an estimate of what such an allocation
  would give under the Gibbs frequencies; they are not a run of 11.18f and I will label them so.

## 06:51 — memory incident: cause found, fixed; queues restarted

* **Cause.**  `ws_P5/p5lib.anch_walk` defines a recursive closure `rec` that uses `F` (the base
  array) as a free variable and refers to itself: a reference cycle (function ↔ its own closure
  cell) that keeps `F` alive after the call returns, until Python's CYCLIC collector runs.  The
  collector's thresholds here are (2000, 10, 10) (Python 3.13.18) and my row loops create only
  10–30 tracked objects per row, so ONE FULL (states × columns) ARRAY PER ROW stayed allocated
  for 60–80 rows.  Arithmetic for the killed job: 217 152 states × 8 B × Σ_{p<78}(120 − p) columns
  = 11.0 GB at row 77 — observed 11.7 GB.
* Reproduced on Lys₄ (`x05_memdiag.py`, restricted pass: RSS +13 MB per row = one row array;
  `x05b_memdiag_m1.py`, main pass: +12 MB per row) and fixed (`gc.collect()` after every walk:
  RSS flat at 100–170 MB).  The fix is in `p8lib.anch_walk` / `p8lib.anch_consts` (wrappers
  around P5's functions; P5's file untouched).  `p8_01b_restricted.py` now also works in column
  blocks of at most 60 MB.
* **Peaks of the jobs that ran BEFORE the fix were not measured.  By the same arithmetic
  (unmeasured estimates):** K5 main pass (06:02–06:10) ≈ 5 GB; K5 restricted pass (06:16–06:22)
  ≈ 6 GB; LKSE:6 main pass (06:10–06:32, two legs) ≈ 9–10 GB; LKSE:6 restricted pass 11.7 GB
  (measured, killed).  All far above the 3 GB limit.  The numbers these runs produced are not
  affected (the leak held garbage, not results), but the rule was broken four times and I
  found out only because the coordinator looked.  K3, K4, LKSE:4, LKSE:5 runs: ≤ 0.4 GB by the
  same arithmetic.  The state-level check `p8_03b` does not use `anch_walk` (no leak).
* From now on: every log ends with "peak RSS … MB" (`p8lib.Log.done`), progress lines of the
  enumeration passes print the current RSS, and enumeration passes run one at a time
  (`queue_H1.txt`), next to at most one light job (`queue_L1.txt`).  Restarted 06:50; the
  LKSE:6 restricted pass was restarted FROM SCRATCH with the fixed code (0.52 GB RSS after 1 min).
* Reported to the coordinator by message at 06:49 (job ended 06:46:12; cause; my estimates of the
  earlier peaks; the latent leak in any loop over `p5lib.anch_walk`).
* Block-wise constants for Lys₁₂ (`p8_04b`, logs `g12b_K12_*`; peak RSS 0.43 GB by `ps`):
  Γ₄, Γ₅, Γ₆ = 36.3, 2.54, 0.142 kT ('Sb'), **34.0, 2.40, 0.136 kT ('SAb')** — P3/SAb = 20.3, 60.4, 171.6.
* Estimates for Lys₁₂ with 'SAb' (band 6; first order, nats): order 4: site 6.5, banded pair 1.52,
  banded triple 1.14; order 5: 0.47 / 0.119 / 0.094; order 6: 0.026 / 0.0072 / 0.0059.
  My "occ" columns (each subset charged in full to its least-occupied in-window sub-tuple):
  0.012–0.015 at order 4 with 'SAb' and 0.41–0.53 with P3's constants — but with P3's constants
  such a penalty reaches hundreds of kT at rare states, where the first-order rule says nothing
  (A17 (16), item 44).  Coordinator (06:46): this allocation is the theory division's
  Proposition 11.18f, proposed and unrefereed, and is the coordinator's to run; I keep my columns
  as an estimate only and say so.

## 07:27 — what happened 06:53–07:27 (clock read: 07:26 UTC before writing)

* **06:50–07:09, light queue `queue_L1`** (times from `logs/queue_L1.out`): block-wise constants
  for (LKSE)₃, Ser₁₂, Leu₁₂ (`g12b_*`), Gibbs samples of the three (each reproduces the
  coordinator's sample exactly), exact remainders on the samples (`ideal_*`), group responses and
  all 220 triples (`dist_*`), estimates (`est_*`).
* **07:03 LKSE:6 restricted pass complete from scratch**: 786.7 s, **peak RSS 1086 MB** (the
  killed run had reached 11.7 GB).  Sign search LKSE:6: 315.6 s, peak 1090 MB.  Pair-wise
  validation LKSE:6 (C1: 304 920 comparisons, 0 violations): 7 s, 322 MB.
* **07:08–07:12, the pipeline with the new constants** (`p8_12_certificate.py`; beyond the brief:
  P3's band models, P6's forms, the coordinator's window model, all imported read-only, fed with
  my per-subset constants).  Enumerated: Lys₄ order 4 (SA): 0.199 / 0.0438 / 0.00845 nats (site /
  banded pair / banded triple), sandwich at all 16 464 states, exact ln Z inside; Lys₅ order 4:
  1.0024 / 0.175 / 0.0267; order 5: 0.0186 / 0.0031 / 0.00044; all 115 248 states, exact ln Z
  inside.  **Lys₁₂ order 4 ('SAb', band 6, ball 96 366): 11.05 / 4.38 / 2.81 nats**; sandwich at
  the 1 600 Gibbs states and 2 000 samples of the floor; peak RSS 1138 MB.
  - *Wrong expectation, recorded:* my first-order estimate for this case was 1.14 nats (1.32 by
    the exponential estimate on the Gibbs sample).  The certified bracket is 2.5 times that: the
    floor delocalises (7.8 sites off the anchor on average in its samples, 1.1 in the true
    ensemble) — exactly what A17 (16) item 44 warns of.  The first-order rule is a LOWER estimate.
  - *Own error 13 (small):* the first Lys₁₂ ball ran in batches of 4096 states (2.2 ms per
    evaluation, 1 GB); batches of 256 are faster (0.9–1.1 ms) and lighter.  Changed for later runs.
* **07:10** `queue_L1` stopped and re-ordered as `queue_L2` (short jobs first, the long order-5
  ball last) — the fifth re-ordering by killing the queue's shell; nothing lost.
* **07:12–07:14**: distance fits (`dfit_*`); estimates re-run with the order-3 rows (exact
  anchored terms of the triples as "constants") and the exponential estimate; the remainder
  identity for arbitrary orders (`p8_10`: 43 200 + 19 200 checks, 328 host cases, 0 bad); 'Sb'
  against P3's `termwise` at twelve residues (`tw12_*`: 16 subsets, ≤ 9.2e-16).
* **07:14** Lys₁₂ order-5 certificate started (ball 1 621 056 evaluations at about 900 per
  second while the heavy queue runs; RSS 1.32 GB; three budgeted legs queued).
* **07:19 block check Lys₅ complete**: 528 s, **peak RSS 1159 MB**; B1/B2 352 + 352 comparisons, B3
  7 606 368 per variant, B4 1 728 720 per variant, 0 violations; SAb/truth 18.1, 41.1, 66.1 and
  SAb/exact block constants (restricted) 2.52, 4.27, 8.86 at orders 3, 4, 5.
* **07:19–07:25 heavy queue**: state checks LKSE:4 (45 845 280 checks) and LKSE:5 (211 134 924),
  0 violations; neutral controls Ser₄, Ser₅, Leu₆, Leu₈ (measure, restricted, validate, block
  check) and strand Lys₃, LKSE:5 (measure, restricted, sign search, validate): all complete, 0
  violations; largest peak 629 MB (`m1_S5`).  Ser₆ measurement running since 07:24.
* **07:20–07:27 new**: `p8_14_exact_terms12.py` (the exact anchored terms of order ≤ M at twelve
  residues from the ball the certificate evaluates anyway; includes the NECESSARY condition
  "exact anchor-context term ≤ bound" for every subset and variant — the first comparison of the
  new constants with exact quantities at twelve residues; not yet run: at most two processes);
  `p8_07_estimate.py` takes these as variant "exact<m>"; `p8_09_tables.py` got table T10 (run
  times and peak RSS from the last line of every log) and totals for T5.
* **Own errors 14–16, all in the draft of §2/§3 and all "written from memory"**: (14) "ball of
  radius 2: 2 831 evaluations" — the script says 3 841 (1 + 91 + 3 749); (15) I "corrected" the
  number of moving atoms of a serine side chain from four to two without looking — the model
  says four; reverted; (16) I described the class pair head–head as including the head atoms'
  self terms — they are the separate class "self:head".  Rule (again): no number or fact goes
  into the report from memory; it is read from a log or a table at the moment of writing.
* 07:32 (clock read 07:32:29; I had first typed 07:33 here too — the same slip twice in two minutes) — own error 1 again: I wrote 'written 07:33' into the headers of queue_X1/X2 without reading the clock (it was 07:32:15); corrected to 07:32 before the queues started reading the files.

## 08:02 — what happened 07:27–08:02 (clock read: 08:02 UTC before writing)

* **07:31–07:42 heavy queue finished** (`logs/queue_H1.out`): Ser₆ (measure 402 s, peak 736 MB;
  restricted 337 s, 619 MB; validate), strand Lys₄ (measure 177 s, 632 MB; restricted; sign
  search; validate).  All fourteen enumerated instances now validated: 12 923 116 comparisons
  of a bound with an exact constant and 9 136 302 072 checks at single states, **0 violations**
  (table T5; smallest ratio 1.0001 for a self term, 1.0104 for a pair term).
* **07:46 the Lys₁₂ order-5 run finished** (two budgeted legs; 1 621 056 evaluations at 0.6–1.1 ms
  next to other jobs; peak RSS 1608 MB): site 0.812, banded pair 0.470, **banded triple 0.446
  nats** (band 6); sandwich at the 1 600 Gibbs states and at 2 000 samples of the floor (1.22 sites
  off the anchor: no delocalisation).  BELOW ONE NAT IN EVERY SHARE FORM.
  - *Wrong expectation, recorded:* I expected 0.47 / 0.12 / 0.09 (the first-order estimates).  All
    three brackets are 0.35 nats wider than that.  Cause, found by building the same models
    with all penalties set to zero (new line (3b) of `p8_12_certificate.py`; width 0.354 nats):
    the pipeline's reduction of the evaluated terms that do not fit the band of 6.  The helix's
    triples (i, i+3/4, i+7) have span 7 and carry 30 % of the third-order terms.
  - With **band 7** (`queue_C2`): order 5: 0.598 / 0.220 / **0.192 nats** (zero-penalty width 0.141;
    264.9 s; **peak RSS 2276 MB** — the largest of my runs after the fix); order 4: 10.7 / 3.27 /
    **1.56 nats** (band 6: 11.05 / 4.38 / 2.81).
  - The certificate runs K4, K5 (two), K12 order 4 and 5 were repeated with `--force` to add line
    (3b) (`queue_C1`; balls read from the cache; identical brackets); the logs of the first K12
    runs, which hold the record of the ball evaluations, are kept as `logs/ballrun_cert_K12_*.log`.
* **07:42–07:48 exact anchored terms from the balls** (`p8_14_exact_terms12.py`, `queue_X1/X2`):
  Lys₁₂ order 3 → 4: 20.03 → 0.992 kT (20-fold); Ser₁₂ 0.98 → 0.067; Leu₁₂ 4.32 → 1.29.  The
  M_T of the 220 triples agree with `p8_06_distance.py` to 0.0.  NECESSARY CONDITION "exact
  anchored term ≤ constant" for all 495 four-subsets and six variants: 0 violations in 8 910
  comparisons (Lys₁₂, Ser₁₂, Leu₁₂); smallest ratio SAb/exact 15.0, 10.6, 23.6; ratio of sums
  34, 52, 221 (P3: 695, 82, 245).  On Lys₅ / LKSE:5 (enumerated) the all-context constants are
  1.046 / 1.016 and 1.144 / 1.029 times the anchor-context terms at orders 3 / 4.
* **Running since 07:46:47**: the radius-4 ball of (LKSE)₃ (3 471 783 evaluations, about 2 000 per
  second; RSS 0.88 GB), for its exact four-body terms, the necessary condition, and then the
  pipeline at order 5 with band 7.  Decision rule: if it is not finished by 08:25 I stop it.
* Report: §0, §2.3, §4, §5 (P8-E1), §7 rewritten for the measured brackets; long tables T2, T3
  restricted in the report to three or four instances (all rows in `out/tables.md`).

## 08:23 — last runs, and the peak RSS of every job (clock read 08:23 UTC; the heading first said 08:24, typed before the clock was read — the same slip a fifth time)

* **08:18 exact four-body terms of (LKSE)₃** (`exact_LKSEc12_H_0.60_M4.log`; ball 3 471 783
  evaluations in two legs, 1 000 s + 879 s; peak RSS 1570 MB): order 3 → 4: 18.29 → 2.49 kT
  (7.3-fold); necessary condition 495 × 6 comparisons, 0 violations; smallest ratio SAb/exact
  24.0; ratio of sums 119 (P3: 752).  Over the four twelve-residue peptides: 11 880 comparisons,
  0 violations.
* **08:22 the pipeline for (LKSE)₃ at order 5, band 7, new constants**: 22.8 / 11.0 / **4.49 nats**
  (zero-penalty width 0.172); floor delocalised (8.93 sites off the anchor); 232.9 s, peak RSS
  1914 MB.  *Wrong expectation, recorded:* my estimates were 1.72 (first order) and 2.79
  (exponential on the Gibbs sample).  Third time the first-order rule understated a bracket
  whose penalties reach several kT.
* All queues ended (`queue_X2` at 08:22:22); no process of mine is running.
* No tool declined any action during the whole session.
* **Peak RSS of every job** — the last line of every log (`DONE in … s; peak RSS … MB`), as read
  by `p8_09_tables.py` into table T11 of `out/tables.md`; the list below is `grep -H '^DONE' logs/*.log`.
  Runs of before 06:46 have no memory record (four of them were far above the limit: the
  incident above).  Largest measured since the fix: 2276 MB (`cert_K12_H_0.70_m5_w7_SAb.log`).

```
ballrun_cert_K12_H_0.70_m4_w6_SAb.log:DONE in 144.8 s; peak RSS 1138 MB
ballrun_cert_K12_H_0.70_m5_w6_SAb.log:DONE in 901.9 s; peak RSS 1608 MB
bc_K3_H_0.70.log:DONE in 5.3 s; peak RSS 116 MB
bc_K4_H_0.70.log:DONE in 42.1 s; peak RSS 277 MB
bc_K5_H_0.70.log:DONE in 528.0 s; peak RSS 1159 MB
bc_L6_H_0.60.log:DONE in 5.5 s; peak RSS 97 MB
bc_L8_H_0.60.log:DONE in 20.7 s; peak RSS 110 MB
bc_LKSEc4_H_0.60.log:DONE in 12.0 s; peak RSS 134 MB
bc_LKSEc5_H_0.60.log:DONE in 22.2 s; peak RSS 242 MB
bc_S4_H_0.70.log:DONE in 2.2 s; peak RSS 91 MB
bc_S5_H_0.70.log:DONE in 14.9 s; peak RSS 235 MB
cert_K12_H_0.70_m4_w6_SAb.log:DONE in 53.1 s; peak RSS 1137 MB
cert_K12_H_0.70_m4_w7_SAb.log:DONE in 139.1 s; peak RSS 1909 MB
cert_K12_H_0.70_m5_w6_SAb.log:DONE in 62.2 s; peak RSS 1475 MB
cert_K12_H_0.70_m5_w7_SAb.log:DONE in 264.9 s; peak RSS 2276 MB
cert_K4_H_0.70_m4_w3_SA.log:DONE in 3.5 s; peak RSS 198 MB
cert_K5_H_0.70_m4_w4_SA.log:DONE in 7.0 s; peak RSS 256 MB
cert_K5_H_0.70_m5_w4_SA.log:DONE in 6.8 s; peak RSS 257 MB
cert_LKSEc12_H_0.60_m5_w7_SAb.log:DONE in 232.9 s; peak RSS 1914 MB
dfit_K12_H_0.70.log:DONE in 5.4 s; peak RSS 123 MB
dfit_L12_H_0.60.log:DONE in 0.6 s; peak RSS 76 MB
dfit_LKSEc12_H_0.60.log:DONE in 1.0 s; peak RSS 123 MB
dfit_S12_H_0.70.log:DONE in 0.5 s; peak RSS 72 MB
dist_K12_H_0.70.log:DONE in 164.7 s; peak RSS 1085 MB
dist_L12_H_0.60.log:DONE in 2.7 s; peak RSS 86 MB
dist_LKSEc12_H_0.60.log:DONE in 182.6 s; peak RSS 309 MB
dist_S12_H_0.70.log:DONE in 14.4 s; peak RSS 128 MB
est_K12_H_0.70.log:DONE in 8.8 s; peak RSS 103 MB
est_L12_H_0.60.log:DONE in 14.1 s; peak RSS 148 MB
est_LKSEc12_H_0.60.log:DONE in 10.3 s; peak RSS 103 MB
est_S12_H_0.70.log:DONE in 12.9 s; peak RSS 149 MB
exact_K12_H_0.70_M3.log:DONE in 0.3 s; peak RSS 257 MB
exact_K12_H_0.70_M4.log:DONE in 2.0 s; peak RSS 750 MB
exact_K5_H_0.70_M4.log:DONE in 0.1 s; peak RSS 151 MB
exact_L12_H_0.60_M4.log:DONE in 1.1 s; peak RSS 187 MB
exact_LKSEc12_H_0.60_M4.log:DONE in 881.5 s; peak RSS 1570 MB
exact_LKSEc5_H_0.60_M4.log:DONE in 1.5 s; peak RSS 97 MB
exact_S12_H_0.70_M4.log:DONE in 151.4 s; peak RSS 274 MB
g12_K12_H_0.70_m4.log:DONE in 39.4 s
g12_K12_H_0.70_m5.log:DONE in 70.2 s
g12_K12_H_0.70_m6.log:DONE in 102.5 s
g12_L12_H_0.60_m4.log:DONE in 10.7 s
g12_L12_H_0.60_m5.log:DONE in 21.9 s
g12_L12_H_0.60_m6.log:DONE in 31.0 s
g12_LKSEc12_H_0.60_m4.log:DONE in 27.2 s
g12_LKSEc12_H_0.60_m5.log:DONE in 52.8 s
g12_LKSEc12_H_0.60_m6.log:DONE in 80.6 s
g12_S12_H_0.70_m4.log:DONE in 10.1 s
g12_S12_H_0.70_m5.log:DONE in 19.9 s
g12_S12_H_0.70_m6.log:DONE in 30.1 s
g12b_K12_H_0.70_m4.log:DONE in 34.9 s
g12b_K12_H_0.70_m5.log:DONE in 65.4 s
g12b_K12_H_0.70_m6.log:DONE in 89.3 s
g12b_L12_H_0.60_m4.log:DONE in 5.1 s; peak RSS 102 MB
g12b_L12_H_0.60_m5.log:DONE in 10.4 s; peak RSS 106 MB
g12b_L12_H_0.60_m6.log:DONE in 15.8 s; peak RSS 110 MB
g12b_LKSEc12_H_0.60_m4.log:DONE in 24.5 s; peak RSS 249 MB
g12b_LKSEc12_H_0.60_m5.log:DONE in 46.0 s; peak RSS 286 MB
g12b_LKSEc12_H_0.60_m6.log:DONE in 70.4 s; peak RSS 322 MB
g12b_S12_H_0.70_m4.log:DONE in 7.9 s; peak RSS 95 MB
g12b_S12_H_0.70_m5.log:DONE in 14.8 s; peak RSS 99 MB
g12b_S12_H_0.70_m6.log:DONE in 18.5 s; peak RSS 102 MB
gibbs_K12_H_0.70.log:DONE in 217.6 s
gibbs_L12_H_0.60.log:DONE in 61.1 s; peak RSS 89 MB
gibbs_LKSEc12_H_0.60.log:DONE in 161.2 s; peak RSS 217 MB
gibbs_S12_H_0.70.log:DONE in 82.6 s; peak RSS 91 MB
ideal_K12_H_0.70.log:DONE in 31.9 s
ideal_L12_H_0.60.log:DONE in 0.7 s; peak RSS 84 MB
ideal_LKSEc12_H_0.60.log:DONE in 11.7 s; peak RSS 187 MB
ideal_S12_H_0.70.log:DONE in 139.7 s; peak RSS 208 MB
m1_K3_E_0.70.log:DONE in 16.0 s; peak RSS 598 MB
m1_K3_H_0.70.log:DONE in 4.0 s
m1_K4_E_0.70.log:DONE in 177.0 s; peak RSS 632 MB
m1_K4_H_0.70.log:DONE in 30.8 s
m1_K5_H_0.70.log:DONE in 497.3 s
m1_L6_H_0.60.log:DONE in 4.1 s; peak RSS 115 MB
m1_L8_H_0.60.log:DONE in 35.9 s; peak RSS 310 MB
m1_LKSEc4_H_0.60.log:DONE in 8.7 s
m1_LKSEc5_E_0.60.log:DONE in 54.4 s; peak RSS 661 MB
m1_LKSEc5_H_0.60.log:DONE in 26.5 s
m1_LKSEc6_H_0.60.log:DONE in 254.1 s
m1_S4_H_0.70.log:DONE in 3.5 s; peak RSS 352 MB
m1_S5_H_0.70.log:DONE in 19.9 s; peak RSS 629 MB
m1_S6_H_0.70.log:DONE in 402.1 s; peak RSS 736 MB
m1b_K3_E_0.70.log:DONE in 6.5 s; peak RSS 115 MB
m1b_K3_H_0.70.log:DONE in 1.3 s
m1b_K4_E_0.70.log:DONE in 103.3 s; peak RSS 462 MB
m1b_K4_H_0.70.log:DONE in 17.2 s
m1b_K5_H_0.70.log:DONE in 323.9 s
m1b_L6_H_0.60.log:DONE in 2.5 s; peak RSS 94 MB
m1b_L8_H_0.60.log:DONE in 8.4 s; peak RSS 239 MB
m1b_LKSEc4_H_0.60.log:DONE in 3.3 s
m1b_LKSEc5_E_0.60.log:DONE in 21.1 s; peak RSS 210 MB
m1b_LKSEc5_H_0.60.log:DONE in 14.8 s
m1b_LKSEc6_H_0.60.log:DONE in 786.7 s; peak RSS 1086 MB
m1b_S4_H_0.70.log:DONE in 1.5 s; peak RSS 85 MB
m1b_S5_H_0.70.log:DONE in 12.3 s; peak RSS 186 MB
m1b_S6_H_0.70.log:DONE in 336.7 s; peak RSS 619 MB
p8_00_probe.log:DONE
p8_10_order_identity.log:DONE in 0.7 s; peak RSS 59 MB
sb_K3_E_0.70.log:DONE in 4.7 s; peak RSS 119 MB
sb_K3_H_0.70.log:DONE in 1.1 s
sb_K4_E_0.70.log:DONE in 69.5 s; peak RSS 415 MB
sb_K4_H_0.70.log:DONE in 13.5 s
sb_K5_H_0.70.log:DONE in 132.3 s
sb_LKSEc4_H_0.60.log:DONE in 3.4 s
sb_LKSEc5_E_0.60.log:DONE in 18.1 s; peak RSS 215 MB
sb_LKSEc5_H_0.60.log:DONE in 11.5 s
sb_LKSEc6_H_0.60.log:DONE in 315.6 s; peak RSS 1090 MB
sc_K3_H_0.70.log:DONE in 1.3 s
sc_K4_H_0.70.log:DONE in 17.3 s
sc_K5_H_0.70.log:DONE in 331.5 s
sc_LKSEc4_H_0.60.log:DONE in 4.7 s; peak RSS 136 MB
sc_LKSEc5_H_0.60.log:DONE in 19.7 s; peak RSS 252 MB
sr_K3_E_0.70.log:DONE in 1.6 s; peak RSS 116 MB
sr_K3_H_0.70.log:DONE in 0.9 s
sr_K4_E_0.70.log:DONE in 2.2 s; peak RSS 152 MB
sr_K4_H_0.70.log:DONE in 2.0 s
sr_K5_H_0.70.log:DONE in 2.6 s
sr_L6_H_0.60.log:DONE in 3.3 s; peak RSS 167 MB
sr_L8_H_0.60.log:DONE in 14.3 s; peak RSS 644 MB
sr_LKSEc4_H_0.60.log:DONE in 0.8 s
sr_LKSEc5_E_0.60.log:DONE in 1.9 s; peak RSS 126 MB
sr_LKSEc5_H_0.60.log:DONE in 1.3 s
sr_LKSEc6_H_0.60.log:DONE in 7.0 s; peak RSS 322 MB
sr_S4_H_0.70.log:DONE in 0.4 s; peak RSS 82 MB
sr_S5_H_0.70.log:DONE in 0.8 s; peak RSS 93 MB
sr_S6_H_0.70.log:DONE in 1.8 s; peak RSS 152 MB
tw12_K12_H_0.70_m4.log:DONE in 24.1 s; peak RSS 359 MB
tw12_K12_H_0.70_m5.log:DONE in 28.1 s; peak RSS 394 MB
tw12_LKSEc12_H_0.60_m4.log:DONE in 12.9 s; peak RSS 275 MB
x04_K12_H_0.70_m4.log:DONE in 18.0 s
x04_K12_H_0.70_m6.log:DONE in 23.3 s
x04_LKSEc12_H_0.60_m5.log:DONE in 10.0 s
x04_S12_H_0.70_m5.log:DONE in 2.9 s
```

## 08:25 — hand-back (clock read first: 08:25 UTC)

* Report assembled a last time (`p8_09_tables.py`, `mk_report.py`): `docs/science/workstreams/P8_REPORT.md`,
  about 1 700 lines.  `MANIFEST.txt` lists every file of this workstream with its size.
* No process of mine is running (checked with `ps`).  Nothing was written outside `ws_P8/` and
  the report (checked: no file under ws_P2, ws_P3, ws_P5, ws_P6 is newer than my start at 05:40;
  the files changed in `pi_inference/` and `docs/science/` are the coordinator's).
* No state-changing git command was issued in the whole session; `git status` (read-only) shows
  my two paths as untracked.
