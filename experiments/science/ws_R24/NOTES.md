# Workstream R24 — running notes

Internal review by an AI session (not external peer review).  Times are read from the clock (`date -u`).

## 2026-11-26

- 19:38:55 UTC — start.  Branch `research/scientific-translation` checked out; working tree has untracked
  files not mine (`product_threshold*`, `r10_verification/`, `R24_brief.md`) and a modified
  `SCIENTIFIC_RESEARCH_LOG.md`.  I touch none of them.
- 19:38:59 UTC — created `experiments/science/ws_R24/` and `not_cited/`.  Machine: 4 cores, 15 GB, 14 GB free.
- Read `COMMON.md` and `R24_brief.md` in full.  Six items.  Objects: addendum item 86, part (22) items 87–90,
  SCI-MSG-0031, SCI-RES-0032, SCI-MSG-0032, scripts/logs under `pi_inference/` and `ensemble_checks/`.
  Parts (13)–(18) are NOT to be reviewed.
- 19:45:02 UTC — read in full: addendum l.3585–3878 (part (21) items 82–86, part (22) items 87–90),
  SCI-MSG-0031, SCI-RES-0032, SCI-MSG-0032, `floor_ground_state.py` + 4 logs, `floor_transition.py` + 4 logs,
  `slack_recovery.py`, `group_coupling.py` + 6 logs, `first_order_recovery.py`, `window_model.py`, P3's `BandModel`.
  First observations (to be tested, not yet findings):
  * item 86: the model's penalty is `RND*lambda*pen` (RND = 1+1e-9) — b = beta*RND*pen in the script, beta*pen in the text.
    P9's raw tables are asserted > 0 in first_order_recovery.py (not in floor_transition.py) -> pen >= 0, pen(anchor)=0.
  * item 86: lambda_c < lambda_kink in 3 of 4 cases (18.805<18.847; 1.3176<1.3349; 0.19835<0.19937); the "(h)" two-phase
    estimate takes S_d from the exact ln Z AT THE MEASURED lambda_c: lam_eq - lam_c = -ln(Z_d/Z_ref)(lam_c)/b*, so
    agreement within O(1)/c* is nearly automatic (circular); lambda_kink alone is as close (0.3, 0.2, 1.3, 0.5 %).
  * item 86: floor_ground_state K12 m4 w7 took 1070 s (theirs).  The script never runs a (min,+) pass at lambda = c*/b*
    (Dinkelbach's closing step) — the "least ratio" claim rests on a 16-step bisection + samples.  To replicate.
  * item 90: (UP) has the closed form Z(E) <= Z(m_-) - C' Z(m_+) (the iteration's fixed point) -> monotone in C trivially.
    "the rest" = ln[(Z_- - C''Z_+)/Z(m_-+s_-)], and (Z_- - C''Z_+) - Z(m_-+s_-) = sum_x (e^{beta s_-}-1)(e^{-beta(m_-+s_-)} - e^{-beta(m_+-s_+)}) >= 0.
    BUT Z(m_-+s_-) = Z(m_-) <e^{-beta s_-}>_floor: the joint law of the minus items UNDER THE FLOOR gives the put-back exactly
    (the script itself computes U0 that way for Lys12) -> "no joint law of the items touches it" looks wrong as worded;
    Bonferroni gives a certified pair version under the floor: Z(E) <= Z_-(1 - sum<zeta_g> + sum_{g<h}<zeta_g zeta_h>), zeta = 1-e^{-beta S-_g} in [0,1).
    To compute on Lys5 by enumeration.
  * item 90, Lys12 rows: the +- is only the floor-sample error of U0; C2add and Cj (heavy-tailed, 400 000 ceiling samples) have
    standard errors computed in the script (C2_se, Cj_se) but never printed.  Coordinator's totals are 1.95 and 1.6 s.e. above R19's.
- 20:00:48 UTC — snapshot of the caches/dirs I must not touch: `snapshot_before.txt` (2161 files; the coordinator's own
  `product_threshold.py` jobs are running in `pi_inference/` at the same time and write there — not mine).
  I run every script with `python3 -B` and `PYTHONDONTWRITEBYTECODE=1` (importing their modules must not write `__pycache__`).
- 19:58–19:59 UTC — `r24_item1_enum.py K5 4 2` (first version) ran to its last line in 35 s, 264 MB.
  RESULT: lambda_gs (brute force over 115 248 states) = 25.82545173 = Dinkelbach with my own (min,+) elimination (3 passes,
  closing value -2.8e-14) = Dinkelbach with the model's own pass; their bisection [25.825, 25.826]; lambda_kink 23.9579 (same state,
  4 of 5 sites off, b* = 0.594, c* = 15.33).  Exact transition of this floor: occupancy n/2 at 24.199, F = ln 2 at 23.575,
  penalised states carry half the weight at 23.442 -> lambda_gs is 6.7 % / 9.6 % / 10.2 % above (not 1–3 %); (lambda_gs - lambda_c) b* = 0.97 nats.
  MY ERROR: the control of check (10) ("half the Renyi term") did NOT fail (0 violations): it cannot fail because the bound is
  loose by more than a factor two in the exponent.  First-version files moved to `not_cited/` (`*_v1.*`); control replaced.
- 20:11:00 UTC — `r24_item1_enum.py K5 4 2` (final version; log `r24_item1_enum_K5_m4_w2.log`, re-run of their script in
  `rerun_floor_ground_state_K5_m4_w2.log`) and `r24_item1_band.py K12 4 4` (133 s, 1031 MB) reached their last lines.
  K12 m4 w4: Dinkelbach with my own (min,+) elimination, three starts: lambda_gs = 15.497319 (3–4 passes each; closing value -1.4e-11;
  theirs 15.49732), lambda_kink = 15.2830609 (theirs [15.283, 15.284]); EXACT lambda_c (exact occupancy, no sampling) = 15.327350
  (their sampled bracket [15.3203, 15.3281]); F = ln 2 at 15.293033.  The two-entropy estimate moves with the lambda at which S_d
  is read (+0.43 % at 0.99 lambda_c, -0.19 % at lambda_c); lambda_kink alone is -0.29 %.  Renyi bracket rigorous and loose
  (lower end 0.15 of lambda_t at t = ln 2).
- 20:06–20:09 UTC — `r24_item5_enum.py` on K5 4 2, LKSE:5 4 2, K5 4 3, K5 5 3: all four rows of the table reproduced digit for digit
  by my own enumeration from the tables.  NEW: (a) v* = ln(Z_- - C Z_+) in closed form; (b) the rest = sum_x (e^{beta s_-}-1)(e^{-beta(m_-+s_-)} - e^{-beta(m_+-s_+)})/Z_+ (identity to 1e-11);
  (c) **pair laws under the FLOOR (Bonferroni) recover the whole upper-side loss incl. "the rest"**: 0.415 / 0.470 / 0.196 / 0.538 of the width
  (against 0.104 / 0.021 / 0.019 / 0.148 for pair terms under the ceiling); (d) **single-group laws under the floor (comonotone bound) improve
  the driver's upper end on three of four instances** (by 0.386, 0.180, 0.432 of the width; worse by 0.386 on K5 4 2).
- MY ERROR (test design): first chi-square test of my sampler was unpooled (579 for 431 dof; 273 sparse cells); pooled test fine
  (`r24_sampler_test.py`, 12 models, z within ±3; control z about +100).
- 20:13:15 UTC — `r24_item5_sampled.py K5 4 2` (validation of my sampled estimators against my enumeration; 33 s, 273 MB,
  reached last line).  Floor side (bounded): S1, S2, remainder, put-back all within 1.1 s.e. of the exact values.
  CEILING side: **C' from 2e6 exact samples = 2.7617e-2 +- 2.6e-4 against the exact 3.0657e-2: 11.5 "standard errors" low**; <q>: one sample
  carries 68 % of the total, s.e. 69 %.  So on a heavy-tailed instance neither the within-sample s.e. nor the batch scatter is an error bar.
- PLAN for a run above five minutes: `r24_item5_sampled.py K12 4 4 --NB 100000 --BC 60 --BF 100 --U0ref 517.128653342 --U0refse 1.2e-6`.
  Cost: the driver once (their logs: 181 s, about 2.1 GB peak with their own sampling arrays); then 60 ceiling batches and 100 floor batches
  of 1e5 samples, about 0.3–1 s each on K5 (K12: 56 groups, 337 items: estimate 1–2 s) -> 7–9 minutes in all, below 3 GB.
  Compared with: `group_coupling_K12_m4_w4.log` (pair terms 0.168 + 0.446 = 0.614; joint 0.169 + 0.475; put-back 517.1286271 +- 1.3e-5)
  and R19's put-back 517.128653342 +- 1.2e-6 (R19_REPORT §3.4).
- 20:21:01 UTC — `r24_item5_sampled.py K12 4 4` reached its last line (375 s, 1072 MB).  6e6 ceiling samples of my own sampler
  (60 batches), 1e7 floor samples: pair terms alone 0.6076 +- 0.0012 (theirs 0.614: SUPPORTED); joint under the ceiling 0.6368 +- 0.0013
  (theirs 0.644); tails mild at Lys12 (the 100 largest samples carry <= 1.1 % of each second-order mean; batch s.e. = within-sample s.e.);
  my plain put-back 517.1286483 +- 8.7e-6 agrees with R19's 517.128653342 (-0.58 s.e.) and is 1.35 s.e. above the coordinator's 517.1286271:
  the total is 0.666 +- 0.002 (not 0.708 +- 0.020), the rest 0.029 +- 0.002 (not 0.064 +- 0.020).
  Bonferroni under the floor recovers 0.498 +- 0.002 on the upper end (the whole upper-side loss but 0.00075); pair laws on both sides: 0.664.
  Comonotone-floor useless at 56 groups (-2.07).  sum_g P(S+_g > 0) = 1.0674 +- 0.0008.  Lys12 band 7 NOT repeated (their run: 2.84 GB, 735 s).
- `r24_item5_synthetic.py` (1 s): criterion and its converse by exact LP over couplings (30 + 30 cases; gap when sum P > 1: 0.059 to 3.1);
  comonotone = max over couplings (3.7e-14); soundness of (UP), C_2, C'', Bonferroni-floor, comonotone-floor on 400 random sandwiches x 3
  energies: 0 violations; control (first-order floor value as an upper bound): 373 violations.
- 20:33:50 UTC — `r24_item2_synthetic.py` (86 s; 44 412 LPs in part A): E15 (a), (b) hold for ARBITRARY envelopes when delta_i(s) is the worst
  single-site cost into the centre state (13 classes, 6 violate the triangle inequality; mu* not a member at 53 of 90 centres; largest
  violation 3e-15; control delta/2 fails in 12 of 13).  87 (c): support functions of the marginal set and of the product of one-site classes
  agree to 7e-16 for site-additive envelopes (also one-sided, also without triangle inequality); controls: not site-additive -> up to 0.75,
  non-product reference -> up to 0.40.  b_min closed form: feasible at 1.03 b_min 60/60, at 0.97 b_min 0/60; reversed formula contradicted
  46/50; explicit flow of Theorem 8 (c) valid 60/60.
- `r24_item2_instances.py` K5 and LKSE:5 (final logs; first version in `not_cited/`: MY ERROR — its control "random general pairs against
  0.99 d" found 0 violations on K5, i.e. could not fail there; replaced by EVERY single-site pair at scale 1 and 0.99).
  Reproduced: sum tau 0.6517/0.7639 (K5), 0.8953/0.9775 (LKSE:5); TV 0.4275/0.5356, 0.6369; ratio test 0.3861/0.0824, 0.4117/0.3422.
  (b) at EVERY centre (exhaustive, pruning by a triangle inequality): fires up to b = 0.03 (K5 one-sided), 0.02 (K5 symmetric), never on LKSE:5.
  (b) on sub-systems: up to 0.05–0.075 (K5), 0.15/0.075 (LKSE:5).  NEW: the exact ratio test on TWO-site marginals certifies 0.984 (K5) and
  0.9992 (LKSE:5) of the true constant — "data see the typical strength, not the worst-case constant" holds for one-body data only.
- `r24_item3.py` (1 s): my rule = brute force = their upper_end on 170 boxes (4e-16); my counter pass and their count_law = enumeration on 40
  random window models (3e-12, 6e-15); 54 numbers of the table of item 88 / SCI-RES-0032 §3 agree with the log; the two order-3 rows of Val8
  (factors 1.01, 1.12) are in the log and not in the table.
- `r24_item4.py` (13 s): hub class = box also with states of zero width (pseudo-metric); COUNTEREXAMPLE (4 states, 2 means, a strictly-inside
  weight, identified); best stability constant C* = max_y (1-mu_f(y))/|f(y)-t*| (LP: 7e-13; control 0.98 C* violated 32/32); certificate with
  r = 2, 3 data = LP value at the LP's multipliers (9e-16); one rounded counter is sound and within n eps for r = 3 statistics.
- 20:38:58 UTC — snapshot after all runs (`snapshot_after.txt`): the only differences in the directories I must not touch are the
  coordinator's own new files (`pi_inference/product_threshold*`, `pair_term_mixing.py`); no cache changed, no `__pycache__` written.
- `r24_item1_toy.py`: degenerate displaced level: lambda_gs/lambda_c = 1.000 (q = 1), 1.30, 1.85, 3.25, 10.3, 110 (q = 20000);
  independent rotamer-like sites: 2.70 at every n; penalty with a constant part: lambda_gs << lambda_c.
- PRIOR ART for item 4 (generic queries only; 20:34–20:39 UTC).  Queries (WebSearch):
  1. DeRobertis Hartigan 1981 "Bayesian inference using intervals of measures" upper expectation density ratio class
  2. density ratio class robust Bayesian analysis upper expectation unique solution of equation lower upper measure ratio constraints pairs
  3. Wasserman "density ratio" priors invariance properties Hilbert projective metric neighbourhood total variation bound
  4. density ratio class with moment constraints OR "generalized moment conditions" robust Bayesian upper expectation linear programming duality density bounded class
  5. Hilbert projective metric ball probability measures total variation sharp bound tanh density ratio
  6. "density ratio class" OR "intervals of measures" prior with "moment constraints" OR "quantile constraints" range of posterior expectation Lagrange multiplier robust Bayesian
  7. sharp maximum stability bound distance to maximizer in terms of suboptimality "density ratio class" OR "likelihood ratio" class total variation "near-extremal"
  Addresses opened (WebFetch):
  a. https://projecteuclid.org/journals/annals-of-statistics/volume-9/issue-2/Bayesian-Inference-Using-Intervals-of-Measures/10.1214/aos/1176345391.full — came back EMPTY (not read)
  b. https://projecteuclid.org/download/pdf_1/euclid.aos/1176345391 — came back EMPTY (not read); not pursued by other means
  c. https://arxiv.org/pdf/0805.3209 — the tool returned the PDF as a file; text extracted with pdftotext in an isolated scratch directory; READ: title page, the passage
     with Theorem 5.1 (density-ratio class; inf and sup of a ratio of integrals as the unique solution of an equation with positive and negative parts; "see [6]" =
     DeRobertis and Hartigan 1981; also "[8], Theorem 3.9" = Ghosh, Delampady, Samanta 2006), and the reference list.  Angers and Delampady, IMS Collections 3 (2008) 89–104.
  d. https://www.foundstat.statistik.uni-muenchen.de/_assets/pdf_oberseminar/140602_walter.pdf — the tool returned the PDF as a file; READ IN FULL (9 slides): G. Walter,
     "Density Ratio Class Models and Imprecision", 2 June 2014; slide 2: the class {p : exists c > 0 : l <= c p <= u}; "If l > 0 for all theta, then
     M = {p : p(theta)/p(theta') <= u(theta)/l(theta') for all theta, theta'}, hence the name 'density ration class' [4, 1]"; slide 3: closed forms for the posterior
     probability bounds; invariance under updating.
  e. https://www.cs.cmu.edu/afs/cs/user/fgcozman/www/Research/QuasiBayesian/Global/node5.html — the tool's summary only (F. Cozman, 1997: density ratio class; LP; closed form
     for marginals citing Seidenfeld and Wasserman 1993; a sample expression for the upper expectation citing Wasserman and Kadane 1992)
  f. https://arxiv.org/abs/2309.02413 — the tool's summary of the abstract page (Cohen and Fausti: a sharp bound of total variation by the Hilbert distance); the tool
     DECLINED to quote the abstract verbatim (quote limit) — not worked around
  g. https://www.minneapolisfed.org/research/working-papers/prior-density-ratio-class-robustness-in-econometrics — the tool's summary (Geweke and Petrella, WP 553, 1995;
     JBES 16 (1998) 469–478); the tool DECLINED to quote the abstract verbatim — not worked around
  RESULT: (1) threshold rule: in print (c, with attribution to DeRobertis–Hartigan 1981, original not opened); (2) the pairwise-ratio form: the definition that gives the
  class its name (d); (3) stability bound and (4) sandwich + moment data: NOT FOUND in queries 4, 6, 7 (search summaries only) — no claim of novelty follows.
- 20:48:26 UTC — report drafted (`docs/science/workstreams/R24_REPORT.md`).  `r24_numbers.py`: 128 typed numbers against 12 logs, 0 disagree.
- PLAN (runs that may exceed five minutes; two processes, 1 GB and 1.9 GB by their logs): `r24_item1_ratio_model_pass.py` for LKSE:12 3 7 and K12 3 7 —
  Dinkelbach with the MODEL'S OWN (min,+) pass and the closing test at c*/b*.  Cost: build 80 s / 130 s, then about 11 passes at 9–12 s each
  (their logs: 39 passes in 340–370 s) -> 3–5 minutes each.  Compared with: c*/b* = 0.2048638 and 1.355575, lambda_kink in [0.19937, 0.19938] and [1.3349, 1.335]
  of the committed logs.  K12 4 7 not attempted (their run: 1070 s).
- 20:58:01 UTC — `r24_item1_ratio_model_pass.py`: both runs reached their last line (LKSE:12 3 7: 492 s, 974 MB; K12 3 7: 551 s, 1918 MB; run together,
  two processes; the coordinator's own jobs `pair_term_mixing.py` / `held_pair_terms.py` were running at the same time).  lambda_gs = 0.204863829 and
  1.35557498 (theirs 0.2048638, 1.355575), closing values 0 and 2e-12; lambda_kink = 0.19937581 and 1.33494834 (inside their brackets).
- Report updated; hand-back next.
- 20:58:45 UTC — final check of the directories I must not touch (`p9_verification`, `ws_P8`, `ws_P9`, `pi_inference/serine_helix_reach_cache`, `ws_P3`,
  `ws_P5`, `ws_P6`, `ensemble_checks`): file list, sizes and times identical to `snapshot_before.txt` (`snapshot_final_protected.txt`).
  In `pi_inference/` the coordinator's own new files appeared during my work (`product_threshold*`, `pair_term_mixing*`, `held_pair_*`), and
  `pi_inference/__pycache__/nested_sampler.cpython-313.pyc` was rewritten at 20:43:51 UTC — none of my processes was running then (mine: until 20:40:16 and from
  20:48:26; all with `python3 -B` and PYTHONDONTWRITEBYTECODE=1); that directory already held .pyc files of 25–26 November.  Not mine; reported.
- 20:59:06 UTC — correction of the line above: my first snapshot listed `pi_inference/serine_helix_reach_cache` twice (once on its own, once inside `pi_inference`),
  so a raw diff showed 100 "missing" lines; after removing duplicate lines the 1 719 protected files are identical (0 differences).  MY ERROR in the snapshot command, no file affected.
- Files of this workstream: see the list at the end of the report.  Hand-back written.
