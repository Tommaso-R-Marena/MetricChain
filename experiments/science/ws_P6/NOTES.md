# Workstream P6 — notes (kept from the first minute)

Start: 2026-11-26 02:52 UTC.  Agent works alone.  Write only in this directory and
`docs/science/workstreams/P6_REPORT.md`.

## 0. Reading log

- [x] COMMON.md  (read in full)
- [x] P6_brief.md (read in full)
- [x] P3_REPORT.md (read in full, lines 1-1296)
- [x] P4_REPORT.md: header, §0-§1.2, §2.6, §3 table, §4, §5, §6, coordinator's note (read); §2.1-2.5 not read
- [x] ws_P3 code read in full: gfbound.py, run_floor.py, pwmodel.py, p3core.py, encl.py, t02_gf.py; batch files;
      log floor_big_V20.log.  ws_P4/p4_06_p3pair.py read in full.

## 0b. Coordinator's mid-task note (received about 02:58 UTC)

If the Write/Edit tool declines `docs/science/workstreams/P6_REPORT.md`: no workaround (no script / redirection);
keep everything here and in logs, return the full findings in the hand-back.  Otherwise proceed as the brief says.
-> Tested at once: (see step 1 below for the outcome).

## 1. Steps (chronological)

### 02:52-02:58 reading; facts that matter for the work

* P3 model (`pwmodel.build_band_models`): const = c0 + d_() -/+ Gamma; one-site h_i + d_i -/+ gam_i[x_i != x0_i];
  in-band pairs P_ij = J_ij + d_ij exactly; far pairs (j-i > w): additive split a_i^-/+(x_i) + b_ij(x_j)
  (b = column mean, a = row min/max of the rest); every d_U, 3 <= |U| <= M, replaced by min/max over the other
  sites of U onto the in-band pair of U with smallest sup slack (one-site function on U[0] if U has no in-band pair).
* P3 fp allowance with site penalties: eps_site[i] = EPS_G * sum_{U ni i, |U|<=M} 2^|U|/|U| is ADDED to gam_i,
  constant part = EPS_G (for g(x0)).  At V20, m=5 this is 4.37e-4 kcal/mol per changed site (gamma_i <= 0.0055).
  With pair penalties this allowance would dominate a single changed site -> allocate the same allowance
  (P3's bound eps_g * sum_{U subset S(x)} 2^|U|) in pair form as well; report both.
* P3 gfbound: `total(m, exclude=i)` zeroes delta_i in every free set and skips the "host inside T" cases for
  host i.  The suprema (Bd_k, L_k, H_k) are taken over hulls over ALL states of all other sites and do not
  depend on T -> chat_T is the same number in every sum -> inclusion-exclusion over excluded sets is exact
  (up to rounding).  Two-site exclusion = the same code with a set of excluded sites.
* P3's site penalties are differences of two upward-rounded sums (tot - total(exclude=i)), then *RND: the
  cancellation is NOT rigorously outward-rounded in P3 (only heuristically: real rounding ~1e-13 relative).
  For pair sums the cancellation is worse (G_ij << Gamma for far pairs) -> I add an explicit absolute
  allowance (see report section 1) or compute G_ij directly without cancellation.
* V20/P2 ball of radius 4 is cached by P3: cache/ball_V20_P2_t0.70_gbn2_M4_78d2725e4b.npz (87441 values);
  the balls of radius 2 and 3 are prefixes of it (ball_states orders by |U| then lexicographically).
* P3's default band for enumerated instances is w = n-1 for k=3, n<=13 (no far pairs) -> to exercise the
  banded variant on enumerated instances I must run w = 1, 2, 3 explicitly (P3's batch G did w = 1, 2).
* P2's enumerated grids of g exist in ws_P2/data/fb_*.npz (584 MB) -> use them instead of re-enumerating
  where the domain matches (check as P4 did).

### 02:58 report file test
Write tool ACCEPTED `docs/science/workstreams/P6_REPORT.md` (skeleton created) -> proceed as the brief says.

### 03:01 coordinator's second mid-task note: ITEM 7 (sandwich sampler), to do after items 1-4, before item 5
Theory division, Proposition 11.113 (THY-RES-0010 section 3) -- NOT read by me unless found in the export; attribute to them.
q(x) ~ e^{-m_-} - e^{-m_+};  W = (e^{-E} - e^{-m_+})/(e^{-m_-} - e^{-m_+}) in [0,1];  Z(E) = Z(m_+) + (Z(m_-) - Z(m_+)) E_q W.
q by rejection from pi_{m_-} with acceptance 1 - e^{-(m_+ - m_-)}; only accepted points evaluated; Hoeffding on [0,1].
(a) identity + range by enumeration on 1-2 instances, coverage over a few hundred repetitions;
(b) V20: site form and banded pair form, m = 3,4,5, N = 1200 and 50000 accepted (fewer if not affordable), delta 0.05;
    acceptance rate, proposals, mean W, bracket; compare with P3's [518.2598, 518.2648] and with the theory division's
    prediction "at most 7.6e-4 nats from 50000 evaluations for a deterministic width 0.0605";
(c) say precisely what is certified; rounding of sampler and exp(); fixed recorded seed.

### 02:58-03:02 code written
* `p6lib.py`: GFBound2.total_ex (P3's loop with a set of excluded sites), GFBatch (same closed form with a batch axis
  over exclusion sets), assemble_pair_sums, enum_chat, fp_tables, site_form / pair_form / banded_pair_form,
  build_models (P3's build_band_models unchanged + in-band pair penalty tables), ball_terms (prefix of cached ball),
  enumerate_g.
* `p6_01_pairsums.py`: pair sums + `--check` against P3's exclusions, the simple subclass and explicit enumeration.
* Rounding of the inclusion-exclusion: hypothesis (P3 report 2.6) = each generating-function sum is within 1e-9
  relative; then G_ij <= Ghat_ij + 4.5e-9 Gamma, S_i <= Shat_i + 2.5e-9 Gamma; I add absallow = 5e-9 * Gamma to each
  G_ij (and (m-1+nin) units to a far sum obtained from the double-counting identity).

(Correction, 03:04: the clock times in the headings above were first written from a guess and were wrong by up to
25 minutes; they are now taken from `date` and file time stamps.  From here on every time is read from `date`.)

### 03:02-03:04 first results
* `p6_01_pairsums.py V5 E 0.70 3 --check`: batched closed form = P3's total / total(exclude) to 6.5e-16 relative;
  = P3's loop with a set of excluded sites to 6.5e-16; G_ij = explicit enumeration over the 10 subsets to 3.1e-15 kcal/mol.
* V20/P2 m = 4, all 211 exclusion sets by the batched closed form: 28.5 s (log logs/p6_01_pairsums_V20_P2_m4.log).
  Gamma_4 = 2.821341 (P3: 2.82134).  Mean G_ij by separation 1..19: 0.364 0.277 0.188 0.081 0.026 0.0080 0.0024
  8.3e-4 3.6e-4 ... 2.3e-6  -> with band 8 the out-of-band shares are < 1e-3 of the total.
* Expectation before running (written down first): mean penalty ~ Gamma * p (site) vs Gamma * p^2 (pair) with
  p = fraction of sites off the anchor ~ 0.2 -> a factor ~5; so m = 5 bracket 0.06 -> ~0.012, m = 4 bracket 1.7 -> ~0.4
  (NOT below 0.1), m = 3 useless.  A share to TRIPLES at m = 4 would give Gamma * p^3 -> ~0.09 nats: worth trying
  after the core items (needs 3-site exclusions and a band model with in-window triple terms).

### 03:04-03:12 pipeline, V20, validation batches launched
* `p6_02_sandwich.py`: site form S (P3, reproduced) and banded pair form B for several bands, floor AND ceiling;
  enumeration checks.  First test V6/E: P3's site-form ln Z(m_-), ln Z(m_+) reproduced with difference 0.0e+00;
  pair form (band 5 = all pairs): width 2.92 -> 0.0634 (m=3), 0.01526 -> 0.000171 (m=4), 0.000242 -> 0.000005 (m=5);
  floor side at m=3,4: 0.0623, 0.0000876 = P4's 0.0623, 0.000087.
* OWN ERROR 1 (03:05): my assertion "banded <= site pointwise" failed at the all-changed state by 1.3e-8 = 1e-9*Gamma:
  it compared a quantity that carries P3's outward-rounding factor RND = 1+1e-9 with one that does not.  Not a
  violation of any bound; tolerance of that comparison set to 3e-9*Gamma.
* V20/P2 (log logs/p6_02_sandwich_V20_P2.log, 22 s, complete):
      m=3 (801 evals):   site w8 width 72.79;  banded pair w8 67.79   (useless)
      m=4 (9921 evals):  site w8 [517.484288, 519.219855] 1.7356;  banded pair w8 [518.125785, 518.431429] 0.3056; w12 0.3049
      m=5 (87441 evals): site w8 [518.233156, 518.293650] 0.0605;  banded pair w8 [518.255189, 518.271430] 0.0162; w12 0.0153
  P3's own ln Z(m_-), ln Z(m_+) reproduced with difference 0.0e+00 (m=4 w8; m=5 w8, w2, w1).
  => as predicted before the run: factor 5.7 at m=4, 3.7 at m=5; m=4 does NOT reach 0.1 nats on PPII.
* 03:08:37 validation batches launched (2 processes): batch_val_small.txt (33 instances), batch_val_big.txt (9);
  103 (instance, order) pairs = P3's enumerated set (batches A/B Val lines, A2, B2, F, G, H incl. OBC2).
* 03:12 MAXSUB (explicit enumeration of subsets inside p6_02) lowered 1000 -> 500: L12 at m=5 needs 792 subsets at
  ~0.4 s each and L12/H at m=6 924 subsets -> would hit the 19-minute timeout.  Runs started before the change
  (L12/E, V12/E) still enumerate 792 subsets at m=5.
* V10/E: pair form at m=4 (all pairs in band): width 0.000403 vs site 0.0390 -> on the strand m=4 should reach 30 and
  50 residues far below 0.1 nats (to be run: p6_03).
* Theory division's Proposition 11.113 read in THY-RES-0010 section 3 and theory report lines 9113-9150 at commit
  9408e33 (scratchpad export): statement in full; (a), (b) re-derived by me in two lines.
* written: p6_04_sampler.py (item 7), p6_03a_ball.py (chunked ball for long chains).

### 03:12-03:25 validation complete; errors; adversarial check; sampler checks
* Machine is overloaded (load 6-7 on 4 cores: another workstream's `lean` at 83 %, P5's two jobs, my two) -> my
  processes get 40-60 % of a core each.  The V12/E enumeration with P3's evaluator would have taken ~13 min and the
  remaining big instances ~1 h.  KILLED the big batch at 03:18 (log -> logs/superseded/...KILLED_slow_enumeration.log).
* Enumeration source changed for domains > 20 000 states: workstream P2's stored grids (ws_P2/data), read with P4's
  loader, accepted only after comparison with P3's own evaluator at 202 states (< 1e-8; observed <= 1e-11).
  Check on V10/E: P2's grid == my own enumeration with P3's bulk evaluator at all 59 049 states (max abs diff 0.0).
  Small instances (< 20 000 states) and everything run before 03:18 (all of batch_val_small, V10/E) were enumerated
  with P3's bulk evaluator as P3 does.
* OWN ERROR 2 (03:20): `math.expm1` overflow in my reporting of the cost number for L12/H at m = 3 (ln Z(m_-) - ln Z(E)
  > 709 nats) aborted that run before its sandwich check was printed; capped at e^700; L12/H re-run alone
  (batch_val_fix1.txt), complete, 0 violations.  Failed log kept in logs/superseded/.
* OWN ERROR 3 (03:19): run_batch.sh overwrote its own $1 (set -- $line) -> the done-marker of the small batch was
  misnamed (logs/batch_L8.done, moved to logs/superseded/).  No effect on any run.  Fixed.
* OWN ERROR 4 (03:22): when I replaced `enumerate_g` in p6lib.py I cut the file from that function to the end and so
  deleted `load_or_compute_pair_sums` and `make_models`, which had been appended after it; the first adversarial
  run failed with AttributeError (log in logs/superseded/); functions restored, run restarted.  p6_02_sandwich.py
  does not use those functions, so no validation run was affected.
* VALIDATION TOTALS (out/tables.md, from 43 complete logs): 42 enumerated instances, 103 (instance, order) pairs,
  620 sandwiches (2 forms x bands x orders), 56 101 116 checks of m_- <= E and E <= m_+, 0 violations (also with
  tolerance zero); truth inside the bracket in 620 of 620; 26 455 676 checks of |remainder| <= penalty, 0 violations;
  smallest ratio penalty/|remainder|: envelope 23.1, pair/banded/site 58; pair sums vs explicit enumeration: 94
  cases, 6 746 subsets, 2 051 pair sums, largest difference 2.7e-15 relative to Gamma; P3's own site-form ln Z
  reproduced in 69 runs, largest difference 5.7e-13.
* Why an ADVERSARIAL check: the real remainder is 23 to 1e9 times below the certified bound, so "m_- <= E <= m_+ with
  the real E" cannot detect a wrong allocation (e.g. a factor 2 in a pair penalty).  p6_06_adversarial.py checks the
  two EXTREME members of the certified class, E_low/high = f + I~ -/+ (sum of explicitly enumerated chat_T inside the
  changed set + fp allowance), against the model tables at every state.  Running (small list): all cases so far
  0 violations, smallest slack ~ -1e-13 (rounding), ratio (m_+ - m_-)/(E_high - E_low) >= 1.000 with equality
  attained for the banded pair form (the form is sharp at some states) and >= 1.000..2.1 for the site form.
* Identity path (only in-band pair sums known) vs direct path on V20, m = 3,4,5, bands 1..12: pair parts identical,
  site parts differ by at most 21 allowance units (<= 1e-6 kcal/mol at m = 3, 2e-8 at m = 4).
* Sampler (item 7) on enumerated instances: V8/P2 m = 4: identity to 1.4e-13, W in [0.22, 0.53], coverage 400/400
  for both forms (N = 1200), mean width 0.034 (site, D = 0.425) and 0.0056 (pair, D = 0.0717).
* Helix control from the validation runs: L8/H, L12/H, LKSE:6/H: m = 3 and m = 4: no gain (526 -> 526, 1610 -> 1610,
  190 -> 190, 221 -> 220 nats); at m = 5 the pair form gives 0.92 -> 0.027 (L8) and 3.81 -> 0.057 (L12) but the ball
  is then 64 % and 19 % of the domain.

### 03:25-03:32 item 7 (sandwich sampler) on V20/P2, band 8, delta = 0.05; seeds 20261126(m)(0|1) recorded in the logs
(logs logs/p6_04_sampler_V_V20_P2_m{3,4,5}_{S,B}_w8.log, all complete; N = 1200 is the prefix of the N = 50000 stream)
  m form  D          acceptance  proposals  N      certified bracket (prob >= 0.95)         width
  5 S     0.060494   0.0587      851 939    50000  [518.262049, 518.262785]                 7.36e-4   (theory division's arithmetic: <= 7.6e-4)
  5 S                                       1200   [518.260027, 518.264777]                 4.75e-3   (theirs: 5e-3)
  5 B     0.016241   0.0161      3 095 718  50000  [518.262315, 518.262513]                 1.98e-4
  5 B                                       1200   [518.261752, 518.263027]                 1.28e-3
  4 S     1.735567   0.8237      60 498     50000  [518.249382, 518.275447]                 2.61e-2
  4 S                                       1200   [518.170097, 518.339436]                 1.69e-1
  4 B     0.305644   0.2634      189 024    50000  [518.260611, 518.264399]                 3.79e-3
  4 B                                       1200   [518.250348, 518.274796]                 2.44e-2
  3 S     72.79      1.0000      1 200      1200   [514.311004, 583.862456]                 69.6  (useless; N = 50000 not run)
  3 B     67.79      1.0000      1 200      1200   [517.254514, 581.806288]                 64.6  (useless; N = 50000 not run)
m_- <= E <= m_+ held at all 202 400 accepted points (W never outside [0,1]).  All useful brackets intersect in
[518.262315, 518.262513].  P3's Hoeffding bracket [518.2598, 518.2648] contains them.  Coordinator's uncertified
estimates: 518.2618 +- 0.0007 contains the point estimate 518.26241; 518.2626 +- 0.0001 overlaps the m=5 B bracket
only at its edge (518.2625..518.262513).
New evaluations of g: 20 227 (m5 S), 27 430 (m5 B), ~32 k and ~37 k distinct states at m = 4 (some already on disk).
