# Workstream R19 — notes (kept from the first minute)

Started: 2026-11-26 16:02:34 UTC (read from the clock).
Repository head at start: 0930440 [SCI] Held-site passes for a window anywhere on the chain; thirteen recovery runs repeated; Lys20 within 4.05e-4 nats (addendum A17 (20)); answer to THY-RES-0016 (SCI-RES-0024).
Branch: research/scientific-translation.

Rules I work under (from the brief): write only in experiments/science/ws_R19/ and
docs/science/workstreams/R19_REPORT.md; no state-changing git; no network; no subagents;
<= 2 processes, OMP_NUM_THREADS=1, <= 4 GB, <= 20 min per run; no wildcard deletes; fresh log names.
Four kinds of checking kept apart: review / replication / re-run / read only.

## Log of steps

- 16:02 read COMMON.md and R19_brief.md in full. Created this directory and not_cited/.
- 16:05 read addenda items 65-81 (lines 3080-3577), slack_recovery.py, held_site_laws.py, first_order_recovery.py,
  window_model_occ.py, nested_sampler.py, window_model.py, ws_P3/pwmodel.py (BandModel) in full.
  First observations (to verify, not yet findings):
  * nested_sampler.py has import-time side effects: os.makedirs(CACHE) and shutil.copy of ws_P{5,6,3}/cache/{atom_,zeta_,enum_}* into
    pi_inference/serine_helix_reach_cache/ when missing there. Before importing it I must check that every such file already exists
    (otherwise importing would write into a cache directory I am forbidden to touch).
  * alloc items are on BOTH sides (kind 0). Hypotheses are separate: m+ - E >= ... + (pen - r) needs r <= env; E - m- >= ... + (pen + r)
    needs r >= -env. Both true at once -> not a double count in the hypotheses. To be re-derived carefully from code.
  * assign_routes routes plus and minus lists separately, and per class separately -> the window start of the "same" group can differ
    between plus and minus items or between classes; validity not affected (any partition into groups is valid; pairing S-_g with S+_g
    only needs S+_g <= s+), tightness may be.
- 16:18 read ASSUMPTION_AUDIT.md in full, aa01_essential.py + log, SCI-RES-0024, P9_REPORT section 1 (Lemma T', Theorem R, Prop. P),
  addenda items 58-64, p6lib (setup, fp_tables, forms), the theory division's GibbsRecovery.lean at 3cf14b9 (git show; statements only).
  Checked (read-only python) that importing nested_sampler / p6lib would copy 0 files into any cache on this machine.
  snap_caches.sh written; snapshot snap_before_01.txt taken before any re-run of the coordinator's code.

## Plan
 A. Item 2: own enumeration vs HS.group_stats on random band models (r19_heldsite_fuzz.py); fuzz assign_routes; bounds edge cases.
 B. Item 1: re-run first_order_recovery --enum under a frame-capture hook (the committed file, unmodified), then my own checks on the
    captured objects: accounting IDENTITY at every state (m+ - E - s+ = env - r + allowances, with env, r, allowances computed by my
    code), per-item and per-class doubling controls, one-sided alloc control.
 C. Item 3: old logs at 90abf0e vs current logs, all thirteen; tables of items 78, 79, SCI-RES-0024.
 D. Item 4: measure-space proof; AA.2 on synthetic energies with controls; classifications; H2' toy; A8 growth.
 E. Item 5 paragraph. F. Report.

## Paper derivations so far (review level)
 * Item 1 accounting from code (window_model_occ.py l.77-116, first_order_recovery.py l.128-194):
   m+ - E = [eps_g + ghat(x0) - g(x0)] + sum_{1<=|U|<=M} (d_up[U] - d_U^true)(x_U)      (allowance - rounding, >= 0 under the tolerance)
          + sum_far [(A+B+cmax)_up - P_up]  + sum_{U out of window} [rup_up(x_keep) - d_up[U]]   (far+ and term+ items, before 'clean')
          + RND*pen(x) - r(x),   pen(x) = sum_T red_T(x_K(T)) [K off],  r = g - I_{m-1} g.
   RND*pen - r >= pen - env + (env - r) = sum_T alloc_T + (env - r) >= sum alloc  iff  r <= env.  Floor: same with + r, needs r >= -env.
   => both hypotheses hold simultaneously given |r| <= env (Theorem R) and the tolerance; the alloc item is NOT counted twice:
      (m+ - E - s+) + (E - m- - s-) >= 2 env >= 0 and each bracket separately >= env -/+ r >= 0.
   * computed d_U is EXACTLY 0 where a site of U is at the anchor (pwmodel.anchored_terms l.126-129: successive subtraction of the anchor
     slice gives exact zeros); the true term too (pairs V, V+{i} cancel). To be confirmed numerically on the captured d.
   * three-way split F/B/I of held_site_laws: re-derived, holds (first site <= s-1 -> F, cannot reach s+w; last >= s+w -> B, starts >= s).
 * Audit: A1 'ceiling holds on all of the space: T' looks mislabelled (what is T is finiteness; validity where finite is F);
   A3 'm >= 3 ... general condition hosts <= m' conflates the identity (hosts <= m) with the envelope (Lemma T' needs B = T minus hosts
   non-empty, i.e. hosts <= m-1); A8 'cost at most linearly' wrong as stated (I_{m-1} g has C(s,j) terms, j<m: grows like s^(m-1));
   A6 'loss about D^2/4': from the coordinator's own enum logs the loss/(D^2/4) is 2.2, 0.16, 0.06, 0.07.  All to be written up with numbers.

## Item 1 — re-run with identity check (16:23 UTC)
Script r19_item1_identity.py: runs the committed first_order_recovery.py UNMODIFIED in-process (profile hook copies main()'s locals at
return), then my own checks.  Logs (all reached their last line): r19_item1_identity_{K5_m4_w2,K5_m4_w3,K5_m5_w3,LKSEc5_m4_w2}.log
(35, 35, 36, 10 s; peak RSS 305, 285, 295, 113 MB).  The driver's part of each of my logs is IDENTICAL to the committed
first_order_recovery_*_enum.log once timings / RSS are removed (diff run) -> the four enumerated logs are reproduced.
Cache snapshot before/after (snap_before_01.txt / snap_after_01.txt): identical except
pi_inference/floor_transition_K12_m3_w7.log, which is being written by ANOTHER process (PID 30012, 'floor_transition.py K12 3 7',
started 16:09 by someone else - not by me; my scripts write only into ws_R19).
Results (every state of each instance):
 (a) anchored terms exactly 0 at the anchor: 0 non-zero entries; allowance tables = 2^|U| eps_g [all off] to 1.2e-15; no routed item
     outside its window; no item fits a window.
 (b) IDENTITY R+ = A + (RND-1)pen + env - r, R- = ... + r : deviations within [-4.7e-13, n_items x 1e-9] at EVERY state in all four
     cases, 0 states outside.  (b1) model - source model = far + term items (0 outside); (b2) pen - env = alloc items (0 outside);
     (b3) |r| <= env at every state; smallest env/|r| 10.75 (K5 m4), 12.49 (K5 m5), 17.03 (LKSE:5 m4).
 (c) K1 each single item doubled: the driver's hypothesis check fails for EVERY item (25/25, 11/11, 15/15, 25/25) -> every item is
     tight somewhere, no item's slack is available twice.  K2 (alloc of the floor moved to the ceiling, sum unchanged): 86594 /
     44361 / 22906 / 8804 violations.  K3 (whole penalty claimed = envelope counted as recoverable): (40889, 21383) etc.
     K4/K4b (Theta halved / divided by ten inside the alloc items): the driver's hypothesis check sees NOTHING (0, 0) in all four
     cases - my identity check sees it at every state outside the ball.  => the hypothesis check certifies the accounting of the
     reductions, NOT the size of Theta (consistent with the coordinator's own remark in item 66).
 (d) my enumeration of the five statistics agrees with the transfer matrix to 9.2e-13 / 2.5e-13 / 2.0e-13 / 7.3e-14 (same numbers
     as the driver's own check, as expected - same law, my code); four bounds recomputed: agree to 2e-10; exact ln Z inside.
 Observation for the report: routed alloc items exist in only ONE of the four enumerated cases (K5 m4 w3: 2 of 3); in the
 band-2 cases 0 of 5 alloc items have a route, so the inner-window route is tested at every state with 'term' items only (4).

## Item 2 — held-site passes against my own enumeration (16:30 UTC)
Script r19_heldsite_fuzz.py (imports ws_P3/pwmodel + pi_inference/window_model, slack_recovery, held_site_laws; NOT nested_sampler).
Logs: r19_heldsite_fuzz.log (v1: 600 instances, seed 20261126, 8 s; reached its last line; superseded: control C1 used an absolute
threshold and 'missed' 1 of 975 groups whose left-out item carried < 1e-8 of the group's mean), r19_heldsite_fuzz_v2.log (3000 instances,
seed 20261127, 24 s, 72 MB) = the cited one.  Debug run (40 instances): not_cited/r19_heldsite_fuzz_debug1.log.
v2 results: 3000 random band models (n 4..9, k 1..4 per site, w 1..4; 3.38e6 states enumerated; 7702 multi-site terms; 3191 one-state
sites), 30880 items: 14172 routed (7587 fwd, 6585 rev, 3570 through an inner window), 16708 without a route.
 A1 illegal routes 0; wrong route/no-route decisions 0; key collisions 0.
 A3 65670 statistics vs enumeration: largest relative deviation 6.35e-13; masses to 2.8e-14.  A4 old module: 6.35e-13.
 A5 LJ,LP <= lnZ(E) <= UE,UP: 0 violations in 3000 (coordinator's bounds and mine); every iterate an upper bound; iterations monotone.
 A6 loss vs 'same items put back exactly' in units of D^2/4: D<0.3 (810 inst.): quartiles 0.002 / 0.25 / 0.57, max 13.3 (!);
    D<0.05: max 1.16.   -> 'about D^2/4' is not a law (see also the enum logs: 2.2, 0.16, 0.06, 0.07).
 controls: see log line 'controls that must fail'.
 Part B (windows chosen by me incl. window right after the held site and the last window): 0 deviations > 1e-8.
 Part C (assign_routes on chains up to 40 sites, band up to 8): 237k items, 0 illegal, 0 incomplete, 0 key collisions, order-independent.
 Part D: bounds(): zero means fine; C' = inf -> UP = -inf (driver would print an EMPTY bracket, no test for lo <= up outside --enum);
    <e^(bS+)-1> = inf -> LP = +inf taken by max(LJ, LP); nan handled only by argument order of max/min;
    UP iteration NOT converged in 60 steps for wide sandwiches (D = 2.36: short by 2.3e-3; D = 7.3: short by 3.2 nats) - still valid.

## Item 3 — logs (16:36 UTC)
r19_item3_logs.py / r19_item3_logs.log (READ ONLY; old logs extracted with 'git show 90abf0e:' into old_logs_90abf0e/).
 * claim 'same items, same digits; more items, a bracket inside the old one at both ends': holds in all 13 (stage rows whose routed
   items by class are unchanged are identical to the last printed digit; changed stages lie inside the old bracket at both ends,
   K12 m5 w7 with the upper end equal at 7 digits).  3 runs identical in all rows (K5 m4 w3, K5 m5 w3, K12 m3 w7).
 * the 'far pairs and terms' row is NOT unchanged in 7 of 13 runs (term items newly routed: K5 w2, LKSE:5 w2, K12 m5 w7, K12 m4 w5,
   w4, LKSEc12 m5, S12 m5) -> the sentence of item 78 'in every row that uses only the old routes - far pairs; far pairs and terms;
   ...' is imprecise (minor).
 * table of item 78: 104 of 104 numbers agree with the logs; item 79: all numbers agree; SCI-RES-0024 3(a), 4: all agree.
 * SCI-RES-0024 section 2 '1.3e-5 of the 2.2e-5 ... 8e-5 of the 4e-4' are D^2/4 evaluated (1.27e-5, 8.22e-5), not measurements; the
   'Assumptions and limitations' paragraph says 'the size of the loss between groups is measured'.  On the 4 enumerated logs the
   measured loss is 2.24, 0.16, 0.06, 0.07 times D^2/4.
 * z-scores of 'sum <S->' in the lysine logs: -1.6, -1.4, -1.5, -1.4, -1.4, -1.6 (K12, shared seed) and -1.4 (K20): all low.
   To decide whether this is the heavy tail of the summand or a bias of the exact means: large-sample test below.

## Runs longer than five minutes — written BEFORE launching (16:36 UTC)
 r19_item1_sampled.py K12 4 4 400000  : driver part 189 s / 1.07 GB by the committed log (steps: ball+Gibbs ~130 s, models, 56 groups of
     held-site passes, 5380-state check ~90 s, 20000 samples, tables check); my part: 5380 new energy evaluations (~90 s by the
     driver's own timing), 854 single-item controls (seconds), 400000 exact samples (one transfer-matrix pass + backward sampling,
     est. < 60 s).  Expected total ~6 min, < 1.5 GB.  Compared with: (i) the committed log first_order_recovery_K12_m4_w4.log (driver
     part must be identical apart from timings); (ii) identity residual must be within 5e-10 at all 5380 states; (iii) z-scores of
     the exact means against 400000 samples: if the -1.4..-1.6 sigma of the 20000-sample comparison were a 2 % bias of the exact
     means, z would be about -6..-7 here; if it is sampling noise, |z| ~ 1.
 r19_item1_sampled.py K12 4 7 400000  : driver part 502 s / 2.84 GB by the committed log; my part as above (sampling arrays of band 7:
     ~0.7 GB temporary, as in the driver's own sampling).  Expected total ~12 min, ~3 GB (< 4 GB).  Same comparisons, against
     first_order_recovery_K12_m4_w7.log (the headline bracket 8.161e-05).

## Production-size checks (16:48 UTC)
r19_item1_sampled.py K12 4 4 400000 -> r19_item1_sampled_K12_m4_w4.log (262 s, 1.46 GB; reached its last line):
 * identity at the driver's 5380 states: residual R - P - 1e-9 x (#non-zero items) within [-3e-12, 1e-9] (8 states between 5e-10 and
   1e-9: an item with raw value in (0, 1e-9] clipped to zero) -> no slack counted twice by 1e-9 kcal/mol or more at any of them.
 * K1 single item doubled: seen by the driver's hypothesis check for 56/56 far, 336/336 term, 458/462 alloc items.
 * K4/K4b (Theta halved / divided by ten in the alloc items): hypothesis check sees nothing (0, 0).
 * exact means vs 400000 exact samples (my seed): sum<S+> +0.14 s.e.; sum<S-> -1.40; sum c -1.35; sum cp -1.37; D-hat -0.58.
   Per group (280 comparisons): mean z -0.6, sd 1.75, 15 with |z|>3, largest 12.8 (group fwd1@5, statistic e: exact 5.5e-7, sampled
   2.6e-7 +- 2.3e-8).  NOT interpretable as it stands: summands dominated by rare states (heavy right tail) give negatively biased
   z and too small standard errors.  A sampling test cannot decide whether the exact means are right at this size.
   => decided to REPLICATE the group statistics exactly with my own variable elimination (r19_groups_exact.py; needs the tables:
   r19_dump_case.py writes them into my directory).  Tested on K5 m4 w2: 30 statistics agree to 9.6e-13, both code branches.
r19_audit_tests.py (my code only) -> r19_audit_tests_v2.log (6 s) = cited; r19_audit_tests.log = first complete run (same numbers, one
 line printed a runaway iterate); not_cited/r19_audit_tests_try1.log stopped by an OverflowError of MINE in S7 (my own error: I iterated
 (UE) on an input that violates its hypotheses; fixed by reporting the first iterate).
 S1 AA.2 holds at every state, m = 2..5 (300 instances, 227561 states each m): 0 violations; attained (ratio 1.000) in some instance;
    controls: M_m halved -> 8540..15082 violations; M_m -> M_(m-1): 7647..12301; M_m -> |phi^(m)(u(x0))|: 24501..34217.
 S2 r = 2: consistent norms 0 violations; inconsistent pair (Euclidean increments, l1 operator norm): violated (deterministic example
    remainder 4 > bound 2).  -> the audit must say WHICH norm.
 S3 remainder identity with contexts: 1e-15; AA.1 per term with non-anchor context: 0 violations of 1796, max ratio 0.806.
 S4 polynomial transfer matrix for <e_j(delta)>: 923 means agree with enumeration to 7e-15.
 S5 H2': truth inside in 480/480; width/(beta Lip n h) median 0.71, max 0.93; control (one-cell allowance) fails in 2-9 of 120 random
    instances and in the adversarial instance for n = 2, 4, 8 (accumulated allowance attained).  H2' vs H3 on 9 sites: H3 envelope
    bracket 7.6, 11.8, 7.2, 1.24, 0.21 nats at m = 2..6 (ball 19..6883); H2' 0.046 nats with 1025 grid values.
 S6 A8: I_(m-1) g grows like s^(m-1) (measured exponents 1.00, 2.02, 2.85 / 1.00, 2.03, 3.06), not 'at most linearly'.
 S7 A1: finite 'ceiling' valid on one mode only -> 'lower end' 2.7188 > ln Z 0.8825 (false); A6: (UP) and (UE) violated with a
    negative group (0.405 < 0.693; -0.80 < 0.693), controls hold; A3: two hosts, m = 2: remainder 0.80 with all increments zero.

## 16:50 UTC — band-7 production check finished; two dump runs in progress
r19_item1_sampled_K12_m4_w7.log (742 s, 2.84 GB, reached its last line).  Driver part IDENTICAL to the committed
first_order_recovery_K12_m4_w7.log (timings/RSS removed); the same for K12_m4_w4.  => brackets 8.161e-05 (band 7) and 6.449e-04
(band 4) reproduced by re-run.
 * identity at the 5380 states: residual in [-3.5e-12, 1.66e-9] (two clipped items at one state), no negative residual.
 * K1: far 20/20, term 160/160, alloc 277/285 seen by the driver's hypothesis check.  K4/K4b: (0, 0) again.
 * exact means vs 400000 samples (seed 2318): sum<S+> -0.40 s.e., sum<S-> +0.78, sum c +0.78, sum cp +0.78; D-hat +0.38.
   -> at band 7 no sign of the -1.4..-1.6 of the driver's 20000-sample comparisons: sampling noise.
Launched (written at launch): r19_dump_case.py K12 4 4 (16:47, ~5 min, 1.1 GB) and r19_dump_case.py K12 4 7 (16:50, driver 502 s by
the committed log, 2.84 GB): each re-runs the driver once more only to store the tables of the two models, the items, routes and the
driver's group statistics in ws_R19/case_*.pkl.  Then r19_groups_exact.py recomputes every group statistic by my own variable
elimination (cost: band 4: arrays <= 14*14*12*7^3, seconds per group, 56 groups; band 7: held site restricted state by state,
est. 5-10 s per held state, a handful of groups) and compares with the driver's held-site passes (expected agreement ~1e-12).

## 17:04 UTC — exact replication of the group statistics
r19_dump_case_K12_m4_w4.log (225 s) and r19_dump_case_K12_m4_w7.log wrote case_K12_m4_w4.pkl (23.8 MB), case_K12_m4_w7.pkl (30 MB).
r19_groups_exact.py case_K12_m4_w4.pkl all: IN PROGRESS, 55 of 56 groups done, every statistic within 5.8e-12 (relative) of the driver's
held-site passes; ln Z(m+), ln Z(m-) by my elimination: +4.55e-13 from the driver's.  MY ERROR in the estimate: I wrote 'seconds per
group'; the 'rev' groups take up to 190 s each (my elimination order sums the sites between the window and a held site on the RIGHT in
ascending order, which builds arrays over up to 9 sites: 1.7 GB).  The run exceeded the 10-minute tool limit of the shell call and
continued in the background (it is still inside my own 20-minute limit: started 16:52:40).  Results unaffected; order fixed only for the
restricted mode used at band 7 (held site restricted state by state, then left ascending / right descending: arrays over <= 8 sites).
Launched now (written at launch): r19_groups_exact.py case_K12_m4_w7.pkl rev11@2,rev11@4,fwd3@5,rev8@5,fwd0@3
 cost: one restricted elimination pass over the chain per state of the held site (7, 7, 7, 7, 14 passes = 42), each over arrays of up
 to 14*14*12*7^5 = 4e7 doubles (0.3 GB; est. 10-20 s per pass) -> 7-14 min, < 2 GB.  Compared with: the driver's five statistics of
 these five groups (three through windows inside the chain: rev11@2, rev11@4, fwd0@3; two through the last / first window).
S8 (r19_audit_tests_v3.log): the class WITH a host: bound written from Lemma T' holds at every state (0 violations, attained);
 control 'Corollary AA.2 as stated with the host as an additive site': 1253..2630 violations -> AA.1/AA.2 do not cover hosts.
S6b: m = 2 with pair repulsion c2 = 2 > M2 delta^2 = 1: ln Z(floor) - ln Z(E) <= 1.07 nats up to n = 200 (1 nat reached at n = 181);
 with c2 = 0.5: 1 nat at n = 6; m = 3, 4: 1 nat at n = 4..7 for both.
S9: (i) F = x1x2x3, m = 2: pair mixed differences with the third site at the anchor 0, remainder 1; (ii) Proposition P needs c >= 0,
 not Phi >= 0.

## 17:07 UTC — MY ERRORS (two), recorded as they were found
 1. r19_groups_exact.py case_K12_m4_w4.pkl all (log r19_groups_exact_K12_m4_w4.log, reached its last line): 823 s and PEAK RSS 4915 MB.
    This BROKE the limit 'no process above 4 GB' (and my own estimate 'seconds per group, < 2 GB').  Cause: my elimination order for
    the groups whose held site is on the right of its window ('rev') sums the sites between window and held site in ascending order
    and builds arrays over 9 sites (7^9 doubles).  I noticed only at the end (the last line prints the peak); nothing else on the
    machine failed (free memory was 7-12 GB).  The numbers are unaffected: 56 of 56 groups, 280 statistics, largest relative
    deviation from the driver's held-site passes 5.77e-12, masses to 7.8e-13, control detected in 56 of 56, the four bounds
    reproduced to 1.5e-11.  To be re-run with a corrected order (fresh log name) so that a compliant log exists.
 2. r19_loss_between_groups.py (first version), validation on Lys5 band 2 FAILED for the lower end: my estimate of
    ln Z(m+ - s+) = 251.3476187 +- 1.9e-6 against the driver's enumeration 251.3476617 (22 standard errors off).  Cause: I estimated
    < e^(beta s+) > under the CEILING; at band 2 the far pairs are helix neighbours, the slack is of order kT and more on states
    the ceiling almost never visits, the integrand has a heavy tail and the sample mean is biased low with a far too small standard
    error (the plain estimate of <e^(beta s+) - 1> was 0.01079 +- 0.00008 against the exact 0.01529).  The log
    r19_loss_between_groups_K5_m4_w2_enum.log is therefore NOT cited for the lower end (moved to not_cited/).  New version: both ends
    from samples of the FLOOR with bounded integrands (e^(-beta W), W = m+ - s+ - m- >= 0, and e^(-beta s-)), first order exact.
    Lesson for the report: the same heavy tail makes the driver's own 'means against 20000 exact samples' comparison weak as a test
    (the coordinator says so in item 73: 'the test of the means is item 71, not this').

## 17:13 UTC — the repository moved while I worked (not by me)
HEAD at start: 0930440.  HEAD now: 5c233cc (three commits by the coordinator: 9566d44, af689cc, 5c233cc).  'git diff --stat 0930440 HEAD'
on my objects: only docs/science/ASSUMPTION_AUDIT.md (+59/-2) and R19_brief.md (the brief I was given, now committed).  The addenda,
SCI-RES-0024 and the four code files are unchanged.  In the audit: sections A1-A9, Part C rows other than H3, and Part D are as I read
them; NEW: section A10 with Proposition AA.3 (the box limit; 'added after the referee of Part A was launched; not in its brief'),
Part B table (b), a clause in row H3, G-7.  => A10 is OUTSIDE my brief and is NOT refereed; line numbers of the audit quoted in my
report are those of the file at 5c233cc (mtime 16:24), section numbers are stable.  Observation only: A10 reports, independently
of me, that halving every table violates nothing (my control K4) and env/|r| >= 10.8, 12.5, 17.0 (mine: 10.75, 12.49, 17.03);
its median for Lys5 order 5 is 449, mine over the 66 924 states outside the ball is 526 (convention not checked).

## 17:14 UTC — loss between groups MEASURED; band-7 run launched (written at launch)
r19_loss_between_groups.py, final version (v3 logs): both ends from samples of the FLOOR with bounded integrands, first order exact
(P3's moments for <m+ - m->_floor, checked by my enumeration on K5: 0.08987236088 both; held-site passes on the floor for <s+->).
Validation against the driver's enumeration ('routed items put back exactly'):
  K5 m4 w2: width 0.00163888 +- 1.3e-5 (enumeration 0.001614; +1.9 s.e.; heavy tails at band 2); loss 0.001246 +- 1.3e-5 (exact 0.001271)
  K5 m4 w3: width 5.00248e-05 +- 5.5e-07 (enumeration 4.996e-05); loss 1.435e-05 +- 5.5e-07 (exact 1.441e-05)
K12 m4 w4 (1e6 samples, 36 s, 1.09 GB): corrected width 6.449e-4; same routed items put back exactly: width 2.135e-4 +- 6e-7;
  LOSS BETWEEN GROUPS = 4.314e-4 +- 6e-7 nats = 2.085 x D^2/4 = 66.9 % of the corrected bracket (lower end 1.10e-4, upper 3.22e-4).
  What the exact treatment leaves, 2.135e-4, is about 2 x 1.06e-4 = the first-order slack of the alloc items WITHOUT a route (log:
  0.000105952 per side) plus 1.2e-5 of unrouted terms: the envelope's share is below ~1e-5.
  => item 78's sentence 'the rest of the 6.4e-4 is the loss between groups (D^2/4 = 2e-4) and the envelope' misattributes 2.2e-4.
Not_cited: the v1/v2 logs of this script (first estimator; quadrature error bar).
Launched: r19_loss_between_groups.py case_K12_m4_w7.pkl 400000 -> r19_loss_between_groups_K12_m4_w7_v3.log.  Cost: two ln Z (15 s
each), held-site passes on the floor for the stored routes (the driver's step (2) took 168 s on the ceiling), 400000 samples of the
floor (30 s), est. 5 min, ~3 GB (the driver's own peak in that step was 2.84 GB).  Compared with: D^2/4 = 1.34e-5 and the corrected
width 8.161e-5; validation as above.

## 17:20 UTC — report drafted; a WARNING to myself about placeholders
r19_groups_exact_K12_m4_w7.log finished (744 s, 1.03 GB): 5 of 20 groups at band 7 (3 through inner windows) agree with the driver to
2.79e-13; ln Z(m+), ln Z(m-) by my elimination: 0 and -4.5e-13 from the driver's.
R19_REPORT.md written in full at 17:19.  MY ERROR: I typed provisional numbers for the band-7 loss between groups (verdict line 5,
the table of M1, the replacement texts) BEFORE the run had finished - numbers that no log of mine contains.  They must be replaced
by the measured values (or removed) before anything is handed back; until then the report is NOT to be read as final in those places:
  '4.1 x D^2/4 at band 7 (two thirds again)', '2.66e-5 +- 1e-7', '5.50e-5 +- 1e-7', '4.10 +- 0.01', '0.67' (band-7 row), '2.1 and 4.1
  times', 'between 0.06 and 4.1 times'.

## 17:25 UTC — band-7 loss measured; the provisional numbers in the report REPLACED
r19_loss_between_groups_K12_m4_w7_v3.log (386 s, 1.89 GB; reached its last line): corrected width 8.16064e-05; same routed items put
back exactly [517.128513845 +- 3.1e-7, 517.128574839 +- 2.4e-7], width 6.09946e-05 +- 1.9e-7;
LOSS BETWEEN GROUPS = 2.061e-05 +- 1.9e-7 = 1.535 +- 0.014 x D^2/4 = 25.3 % of the bracket.  What is left, 6.10e-5: subsets without a
route 2 x 2.46e-6 (log), allowance 2.1e-6 (r19_allowance_first_order_K12_m4_w4.log: 2 beta <A> = 2.1-2.2e-6 at order 4, 2.2-2.3e-6 at
order 5), the envelope by difference ~5.4e-5 (item 73 says 1e-5 - 1e-4 for this row: consistent).
So my provisional '4.1 x, two thirds' was WRONG by a factor 2.7, and my sentence 'the envelope's share at band 4 is below 1e-5' was
wrong too (the envelope is ~5.4e-5 at order 4 whatever the band).  All places corrected in R19_REPORT.md (verdict line 5, title and
table of M1, consequences (i)-(iv), replacement texts, section 2.4); grep for the old strings returns nothing.
Lesson recorded as one of my errors in section 6 of the report.
Inference for order 5 (NOT a measurement): 2.178e-5 = loss + allowance 2.2e-6 + unrouted 6.5e-7 + envelope 1e-9 -> loss ~1.9e-5 ~ 1.5 D^2/4.

## 17:29 UTC — final state
All background runs finished; no process of mine is running.  Final snapshot snap_after_final.txt against snap_before_01.txt: the
only differences are files written by other processes of the division (floor_transition_*.log, subset_concentration*); no cache
directory entry changed.  Every r19_*.log in this directory ends with 'ALL DONE' (checked by a loop).
Report: docs/science/workstreams/R19_REPORT.md (about 62 kB), sections 0-6 as the brief prescribes; re-read once in full after the
band-7 numbers were put in; counts corrected (19 confirmed / 5 weakened / 3 rejected of 27 rows; six deterministic brackets, not eight).
Findings: critical 0; major 4 (M1 D^2/4 'measured'; M2 A1 ceiling 'T'; M3 AA.1/AA.2 without hosts; M4 A8 growth comparison);
minor 15 (m1-m15).
Tool actions declined: none.  (One shell call exceeded its 600 s limit and was moved to the background by the tool; not a refusal.)
Peak memory of my runs: 4915 MB once (my error, recorded above); all others <= 2.84 GB.  Longest run: 823 s (the same) / 744 s.
At most two of my processes ran at a time.
