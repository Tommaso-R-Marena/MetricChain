# Workstream P3 — running notes

(Kept from the first minute.  Newest entries at the bottom.  Times are wall-clock on the
machine, 2026-11-25.)

## 23:33  Start

* Read `docs/science/workstreams/COMMON.md` (binding rules) and `P3_brief.md` (brief).
* Created `experiments/science/ws_P3/`.
* Machine: 4 cores, 15 GB, load average ~2 at start (other jobs running).
* Theory export (read-only): `/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_658b77f`.

Plan (order of the brief):
1. Read P2 report + `fbmodel.py`; read THY-RES-0007 §4 and RESEARCH_LOG "Resume here" item 1.
2. Re-validate the GBn2 re-implementation against OpenMM on fresh states (my own check).
3. Numerics first: what do exact third differences look like vs. candidate analytic bounds.
4. Theorem + recipe (no joint enumeration), outward rounding / error budget.
5. Tightness vs P2 enumerated constants.
6. Floor: rho, Z(m)/Z(g)-1 vs length.
7. One instance beyond enumeration, end-to-end bracket.
8. Optional: sum c_i^2; OBC2.

## 23:55  Reading done (what I read and what it says)

* P2 report (`docs/science/workstreams/P2_REPORT.md`, in full), `ws_P2/fbmodel.py`, `anlib.py`,
  `an_main.py`, `an_ball_pairwise.py`, `enum_fb.py`, `test_fbmodel.py`, `scbuild.py`;
  `ws_P/fastff.py`, `ws_P/pepbuild.py` (contexts).  P2's data grids exist on disk
  (`ws_P2/data/fb_*.npz`, 584 MB, 140 models) and its JSON outputs (`ws_P2/out/an_*.json`).
* THY-RES-0007 §4 and RESEARCH_LOG "Resume here" item 1 (theory export at 658b77f): box class
  `lo <= r <= hi`, cost `Theta((Z(lo)/Z(g) - 1)/eps)`; statements (a)-(e).
* OpenMM 8.6.1 source `openmm/app/internal/customgbforces.py` (GBSAGBn2Force, _createEnergyTerms,
  _createUniqueTable).  Facts that matter for the analysis:
  - `I_p = sum_{q != p} [Ivdw(r; or_p, sr_q) + 0.826836 * Ineck(r; p, q)]`,
    `Ineck = step(radius_p + radius_q + 0.68 - r) * m0(p,q) / (1 + 100 (r-d0)^2 + 0.3e6 (r-d0)^6)`;
    the "tabulated" part of the neck is `m0, d0` as functions of the two *radii* (21x21 table,
    bilinear in the radii, turned into a Discrete2DFunction per pair of radius classes); as a
    function of `r` the neck term is closed-form but has a JUMP at the cutoff
    `r = radius_p + radius_q + 0.68 nm`.  On a rotamer grid every distance is a number, so no
    derivative in `r` is needed; for continuous chi the jump would have to be dealt with.
  - `B_p = 1/(1/or_p - tanh(alpha psi - beta psi^2 + gamma psi^3)/radius_p)`, `psi = I_p * or_p`.
  - energy `-0.5*138.935485*(1/eps_in - 1/eps_out) * [ sum_p q_p^2/B_p + 2 sum_{p<q} q_p q_q / f ]`,
    `f = sqrt(r^2 + B_p B_q exp(-r^2/(4 B_p B_q)))`.
* Structure used by everything below (P2 Statement 8 / next step 2): on a fixed backbone
  `I_p(x) = I_p^0 + sum_i A_i^p(x_i)` for fixed atoms and `I_p(x) = S_i^p(x_i) + sum_{j != i} T_ij^p(x_i, x_j)`
  for atoms of side chain `i`.

### First thoughts on the mathematics (before numerics)

* Mixed-difference chain rule (Faa di Bruno for finite differences via multilinear interpolation
  on the 2^|T| vertices): for `u` vector-valued, `Psi` smooth,
  `|Delta_T (Psi o u)| <= sum_{partitions pi of T} sum_{a: pi -> components} sup|d_a Psi| prod_{B in pi} D_B(u_{a(B)})`.
  For `u` = sum of one-site functions only singletons survive: `|Delta_T phi(sum a_i)| <= sup|phi^{(|T|)}| prod delta_i`.
* Danger: term-by-term bounds lose (1) sign cancellation between atoms / charge pairs
  (self-cross cancellation of neutral groups), (2) max over state pairs taken atom by atom.
* Hierarchy idea: `c_ijk <= c_ijk^ref (exact, at a reference context; k^3 evaluations per triple)
  + sum_{l} chat_{ijkl}` (context dependence is a 4th-order mixed difference) -- the term-by-term
  bound is used one order higher, where it costs least.  Everything polynomial in n.
* What the floor needs: `m = f + I_2 g - sum_i gamma_i [x_i != x0_i]`, `gamma_i = (1/3) sum_{T ni i} chat_T`.
  The cost number of the theory is `Z(m)/Z(g) - 1 = E_{pi_g} e^{beta (g - m)} - 1`, the worst case `e^{beta rho}`.
* One-sided constants: the floor needs only a LOWER bound on the remainder; if the three-body
  term has a sign structure (saturating descreening), one-sided constants may be much smaller.

Next: own evaluator (per-atom tables, self/cross split), validation against OpenMM on fresh states.

## 00:25  Step 1 done: own evaluator validated on fresh states

* `p3core.py` (GBModel: own descreening tables I0/A/S/T, own energy with self/cross split, own
  table-free reference `energy_direct`, parameters read straight from the OpenMM force object;
  `pruned_domain` = P2's X' rule recomputed from clash tables).
* `t01_validate.py` -> `logs/t01_validate_gbn2.log`: 14 systems (V6/E, V5/P2, S4/H, S5/E, L5/E, L6/H,
  F3/P2, F4/E, K3/P2, K2/E, LKSE:5/E, LKSE:7/H, V12/P2, L16/H), 60 fresh random assignments each
  (seed 20261125; half raw R3 states, half from the pruned product at tau = 0.60):
  worst |tables - direct| = 5.8e-12, |tables - OpenMM Reference (double)| = 1.8e-11,
  |tables - P2 block evaluator| = 1.6e-11 kcal/mol.  pruned_domain reproduces P2's `shape_pruned`
  in all 26 comparisons (incl. the EMPTY ones) [first written as 24; corrected from the log].  [M]

## 00:40  Exploration 1 (`x01_explore.py`, `logs/x01_explore.log`): what must be bounded

Exact enumeration on S3/E, S4/E, S4/H (tau .70), V6/E (.70), L6/H, L8/H (.60), self and cross parts
separately, anchor x0 = argmin E:
* third order: c_ijk(self) and c_ijk(cross) are each 1-5 times c_ijk(total) (V6/E: total 5.8e-3,
  self 2.0e-2, cross 1.7e-2; S4/H: 5.2e-2 / 2.2e-2 / 4.6e-2; L8/H: 6.9e-2 / 1.5e-1 / 1.9e-1).
  So the self/cross cancellation, which is a factor 20 at first order for Leu (self range 62,
  total 3.4 kcal/mol), is only a factor 1.5-5 at third order.
* context dependence of c_ijk is weak on the strand (value at the anchor context within 0-20 % of
  the sup over contexts) and stronger on the helix for some triples (L6/H triple (0,1,4): 0.031 vs 0.002).
* fourth-order constants: strand 10-20 times smaller than third order (S4/E 2.5e-4 vs 4.2e-3;
  V6/E 5.5e-4 vs 5.8e-3), helix only 3 times smaller (L8/H 0.021 vs 0.069; sum over quadruples
  0.29 vs sum over triples 1.23).  Fifth order another factor 10 (L8/H: max 2.2e-3, sum 0.029).
* anchored terms d_T are two-signed; for Leu/H the large triples are positive (sum of positive
  parts 0.54, of negative parts 0.21 at n = 8).
* remainder g - I_2 g: S4/E [-2.6e-3, 3.0e-3]; S4/H [-1.6e-2, 4.7e-2]; V6/E [-4.1e-3, 4.9e-3];
  L8/H [-6.7e-2, 0.249];  g - I_3 g: S4/E 1e-4; V6/E [-3.3e-4, 5.2e-4]; L8/H [-8.8e-2, 1.2e-2].

Identity used from now on (re-derived; telescoping twice/thrice): with the sites ordered,
  g(x) - I_{m-1} g(x) = sum_{T subset S(x), |T| = m} Delta_T g(z^T; x0_T -> x_T),
  z^T = (x on sites < min T, x0 elsewhere).
So what must be bounded are ANCHORED mixed differences (from x0_T to x_T) at contexts that differ
from the anchor only before min T.

Next: prototype of the term-by-term (Faa di Bruno) bound at orders 2, 3, 4 and its ratio to exact.

## 01:30-03:10  Term-by-term bound: prototype, the negative result, and the way out

* `dfun.py`: closed-form derivatives (tanh rescaling, ln B, kernel h(w; r) = e^{-w/2} eta(D)); the
  kernel derivatives are d^k h/dw^k = (2/r) zeta_k(D), zeta_k = sqrt(D) eta_k(D), with the
  recursion eta_{k+1} = -eta_k/2 - D eta_k' and an explicit monomial representation
  (exact rational coefficients; starting from the simplified eta_1 = -(1+D) e^{-D} u^{-3/2}/2 so
  that every monomial carries e^{-bD}, b >= 1).  Self-test vs mpmath numerical derivatives: 6e-16.
* `termwise.py` + `x02_termwise.py` (sampled suprema, exploration): per-subset bound, class mode.
  RESULT [N]: the SELF part is bounded within x1.3-3.3 (order 3) and x2-7 (order 4) of its exact
  constant; the CROSS part only within x80-270.  Total certified/measured at third order:
  S3/E x102, S4/E x102, V6/E x469, L6/H x477.
* `x03_breakdown.py`: for V6/E, T=(2,3,4) (exact total 5.8e-3): fixed-fixed pairs 0.67; pairs with a
  host in T 1.8; site-site 0.4 kcal/mol; all three partition types (h' D_ijk, h'' D_ij D_k,
  h''' D_i D_j D_k) contribute comparably.  REASON: the cross sum runs over O(N * 30) pairs with
  |q_p q_q| and no sign; exactly it is a sum of screened interactions between near-neutral groups
  (C=O, N-H, CH3) which cancels to ~1 % (self part alone -640 kcal/mol, cross +600, total -37 for V6).
  A term-by-term bound cannot see that cancellation.  Each analytic refinement that keeps signed
  sums at a reference gains one factor of the small parameter (relative change of a Born radius
  under one rotamer flip) -- which is exactly what one more order of the anchored expansion gains.
* DECISION: certified truncated anchored expansion.  Evaluate g exactly on the Hamming ball of
  radius m-1 about an anchor (polynomially many evaluations: no cancellation lost), bound the
  remainder by the term-by-term bound at order m summed over all m-subsets.  The term-by-term
  sums decay by a factor 30-100 per order on the strand, so the x250-800 looseness is paid once,
  at the highest order.
* `encl.py`: rigorous enclosures (mpmath.iv, 80 bits): interval Taylor series for ib and ln B on
  cells of I (Taylor form of order 2 about the cell midpoint), monomial interval evaluation of
  zeta_k on cells of ln D with the Taylor form d zeta_k/d ln D = -zeta_{k+1} (order 3).
  Enclosure/sampled-max ratios 1.00001-1.0001.  Tables cached in `cache/`.
* `gfbound.py`: anchored-mode bound summed over ALL subsets of order m by generating functions
  (bivariate elementary symmetric polynomials x partial Bell polynomials); instance types A/N/X.
* `t02_gf.py` on V5/E (`logs/t02_gf_V5E.log`), anchor = argmin E:
    order 3: Gamma_3 = 9.04 kcal/mol (self 0.166, cross 8.87); exact sum of anchored constants 0.0114 -> x794
    order 4: Gamma_4 = 0.254 (self 0.0022);                    exact 6.2e-4  -> x412
    order 5: Gamma_5 = 0.00233;                                exact 9.5e-6  -> x244
  generating function == sum over subsets to 2e-16; bound >= exact in all 16 subsets.

## 2026-11-26 00:00-00:20  The certified pipeline exists and passes on small instances

* `pwmodel.py`: known-part tables on the domain, coordinate-descent anchor, Hamming-ball evaluation
  -> anchored terms d_U (inclusion-exclusion on full sub-grids), banded lower/upper pairwise models
  (far pairs: additive split with exact row minima; terms of order 3..m-1: exact two-site
  minorants/majorants on the in-band pair with the smallest slack), transfer-matrix ln Z, max-plus DP,
  exact backward sampling.
* `run_floor.py`: the whole chain for one instance; if the domain is small it enumerates E and checks
  m_- <= E <= m_+ at EVERY state.
* `logs/floor_V6E.log` (Val6 strand, 729 states, anchor = argmin E):
    m=3:  Gamma_3 = 12.96 kcal/mol = 21.7 kT, ball 73 evals;  cost number Z(m_-)/Z(E) - 1 = 2.8e9   (useless)
    m=4:  Gamma_4 = 0.432 = 0.73 kT, ball 233 evals; deterministic bracket 1.45 nats; cost 1.07;
          Hoeffding bracket (N = 20000, delta = .05) 0.031 nats
    m=5:  Gamma_5 = 0.0066, ball 473; deterministic bracket 0.022 nats; cost 0.011
  no violation of m_- <= E <= m_+ in any state; ln Z from the transfer matrix = enumeration to 1e-13;
  truth inside every bracket.
* Val8/PPII, m=4: 577 evaluations (8.8 % of 6561), Gamma_4 = 0.717 kcal/mol, cost 2.33,
  Hoeffding 0.059 nats, sample-range bound 0.027 nats; 576 distinct sampled states.
* `t03_fp.py` (`logs/t03_fp.log`): g in double precision vs mpmath at 40 digits from the same inputs:
  worst 1.8e-12 kcal/mol (V6/E, 108 atoms), 5.3e-13 (S4/H); descreening integrals from the tables:
  6e-15 nm^-1.  Allowances used in the certificates: 1e-7 kcal/mol per evaluation of g, 2e-10 nm^-1
  per table difference.
* Bulk evaluations use P2's block evaluator through `GBModel.bulk_energy` (1.9 ms/state for
  Val20, mine 11.6 ms); every run re-checks 48 random states against my own evaluator (< 1e-8).
* Site-resolved penalties (`GFBound.site_penalties`, `--siteres`): gamma_i = (1/m) sum_{T ni i} chat_T,
  n+1 generating-function evaluations.  Val6/E, m=4: gamma = (.043 .074 .099 .099 .074 .043);
  deterministic bracket 0.015 nats instead of 1.45, cost number 0.008 instead of 1.07 -- the floor
  "that is a function" is far better than the constant, because pi is concentrated near the anchor.
* Background jobs started 00:11: `batch_A.txt`, `batch_B.txt` (101 runs of run_floor over Val, Leu,
  Ser, Phe, Lys, LKSE; constant-Gamma form, m = 3, 4, 5) -> `logs/floor_batch_{A,B}.log`, `out/floor_*.json`;
  `run_tight.sh` (analysis-only class-mode bound per triple vs P2's enumerated c_ijk) ->
  `logs/t04_tight_*.log`, `out/tight_*.json`.
* First tightness numbers [M, rigorous bound vs P2 enumeration], ratio of sums over triples:
  Val/E x423-485, Val/P2 x206-218, Leu/E x1320-1420, Leu/P2 x306-382, Leu/H x280-706;
  the self part alone x2-30.  P2's constants are reproduced by my own enumeration
  (x01: S3/E 4.026e-3, V6/E max 5.850e-3, sum 3.075e-2).

## 00:20-00:35  Checks of the statements; tightness of the analysis-only bound; prior-art searches

* `t05_identity.py` (`logs/t05_identity.log`): remainder identity (Proposition 1) holds to 1.8e-13 on
  g_GB of Val6/PPII (40 random x, every m) and 7e-15 on a random function; Corollary L1 holds on 2000
  random cases.
* `t04_tight.py` finished (`out/tight_{apolar,polar,charged}.json`, 44 instances, 672 triples [first written as 562: a miscount of mine, corrected 01:27 from the JSON files]):
  rigorous analysis-only bound >= P2's measured c_ijk for every triple (asserted).  Ratio of sums:
    Val x206-485 | Leu x280-1420 | Phe x89-170 | Ser x38-104 | Lys x33-77 | LKSE x89-160.
  NEGATIVE RESULT: analysis alone is 1.5-3 orders of magnitude too large.
* Prior art (rule 5): 3 PubMed queries (0, 1, 0 hits) and 3 Consensus queries (3 records each), all
  read at ABSTRACT level only: Onufriev-Case-Bashford 2002 (perfect radii), Mongan et al. 2007 (R6
  integral), Onufriev et al. 2011 (gross errors of f_GB), Jain et al. 2017 (sparse residue interaction
  graphs), Jou et al. 2016 (BWM*, dynamic programming on sparse graphs), Hallen-Donald 2019 (review),
  Rahman 2014 (errors of truncated referential/anchored decompositions).  None states a sup-norm
  bound on the many-body remainder of a GB energy; not a novelty claim.

## 00:22-00:32  Val20/PPII beyond enumeration; coordinator's addition (Bennett inputs)

* `logs/floor_big_V20.log`, first run (m = 4, site penalties, band w = 8, seed 2026):
  |X| = 3^20 = 3.49e9; ball of radius 3 = 9 921 evaluations (2.85e-6 of the domain);
  Gamma_4 = 2.82 kcal/mol, gamma_i <= 0.175; deterministic certified bracket
  ln Z(E) in [517.483, 519.221] (1.74 nats); N = 50 000 exact samples of pi_{m_-} (29 321 distinct,
  mean 4.27 sites off the anchor): Hoeffding (delta = .05) ln Z(E) in [518.2442, 518.2759], width
  0.032 nats; Gibbs-Bogoliubov lower bound 518.104.  177 s wall.  The m = 5 run is in progress.
* Coordinator's message (received ~00:26): asks in addition for (a) a certified one-sided floor of
  r = beta(g - m) for a stated pairwise model m and b_cert = (upper bound of the mean of r under
  pi_m) - lo, (b) a certified upper bound of Var_{pi_m}(r), (c) W(b_cert, s2_cert) next to
  enumerated values (Bennett bracket, addendum A17 part 7; coordinator's logs in
  `experiments/science/pi_inference/bennett_bracket_real.{py,log}`, read: header and ~25 lines).
* ANSWER (all three are available, exactly computable, no sampling): with the certified sandwich
  m_- <= E <= m_+ and u := beta (m_+ - m_-) >= 0 (an explicit banded pairwise function):
    model m = m_-:  r = beta(E - m_-) in [0, u]  =>  lo = 0;  E r <= E u =: b_cert;  Var r <= E r^2 <= E u^2 =: s2_cert;
    model m_0 = (m_- + m_+)/2:  |r_0| <= u/2  =>  lo = -beta rho_cert/2;  b_cert = (E u + beta rho_cert)/2;  s2_cert = E u^2 / 4;
  E u and E u^2 under pi_m by a transfer matrix over degree-2 polynomials (`BandModel.moments`).
  Implemented in `run_floor.py` (block 4b; enumerated b, s2, K, W in block 5; Bennett bracket with
  Chebyshev + certified variance in block 6).  A bug of mine (lnZE used before assignment) made two
  runs of batch C fail between 00:27:40 and 00:28:54 (L8/H m = 4, 5 site-resolved); fixed, to be re-run.
* First numbers [M]: Val6/PPII, m = 5, site penalties: certified b = 4.4e-3 kT, s2 = 4.3e-5,
  W_cert = 2.1e-5 nats; enumerated b = 2.2e-3, s2 = 7.4e-6, true Jensen gap K = 3.7e-6 (W_enum 3.7e-6).
  Bennett bracket with N = 5000: width 8.5e-4 nats.  With the CONSTANT remainder bound (m = 4) the
  same route gives b_cert = 1.26, s2_cert = 1.58, W = 0.64 nats: useless -- the bounds [0, u] cannot
  see that r is nearly constant; site penalties are essential for this route.

## 00:36-00:42  Val20/PPII at m = 5; a sharp test of the pair bound

* Val20/PPII, m = 5, site penalties (old script, `logs/floor_big_V20_prebennett.log`): ball of radius 4 =
  87 441 evaluations (2.5e-5 of the 3.49e9 states); Gamma_5 = 0.082 kcal/mol (gamma_i <= 0.0055);
  DETERMINISTIC certified bracket ln Z(E) in [518.2211, 518.3057] (0.085 nats, no sampling);
  N = 50 000: Hoeffding [518.2598, 518.2649] (0.0051 nats).  462 s.  It lies inside the m = 4 bracket
  [518.2442, 518.2759]: two different certificates agree.
* The floating-point allowance (1e-7 per evaluated value, accumulated linearly over all 2^|U| values of
  all d_U) was 8.7e-3 kcal/mol at m = 5, n = 20: a third of the deterministic bracket.  Made it
  site-resolved (d_U is exactly zero in floating point unless U is inside the changed set):
  eps_i = eps_g sum_{U ni i} 2^|U|/|U|.  Re-running V20 (batch D) and all site-resolved small
  instances (batch E -> final batch F) with the final script.
  NOTE: 1e-7 per evaluation is an ALLOWANCE (measured error <= 2e-12); a proof for the summation order
  inside numexpr was not attempted -> "what I did not check".
* `t06_pairtest.py` (`logs/t06_pairtest.log`): all charges zero except one pair (or one atom): the
  certified bound of that single term against its exact anchored constant, all subsets of order 3, 4:
  Val5/E 60 random terms, Ser4/H 48: NO violation in 1 118 cases [first written as 1 268: a miscount, corrected 01:28]; bound/exact minimum 1.00-2.0,
  median 1.1 (self, fixed atom), 1.8-2.5 (self, side-chain atom), 1.8-2.3 (fixed-fixed pair),
  2.7-3.9 (fixed-side), 3.0-6.3 (same side chain), 4.2-5.5 (two side chains).
  => term by term the bound is nearly sharp; the factor 100-1400 of the full bound is entirely the
  lost cancellation of the pair sum.

## 00:42-00:47  Second coordinator message (chain model with a window) -- what I do with it

* Message (received ~00:44): an ANOVA chain model mc(w) with pairs within a window w along the chain
  has, by exact enumeration on 27 instances, a remainder with b <= 0.47 kT, sigma <= 0.017 kT for
  Val on strand/PPII at w = 1; suggestion: take m = chain model with w = 2 for item 4, certify floor
  and variance of r = g - m for that m, and report sampled statistics of r at the large size next to
  enumerated ones.  (Read: `pi_inference/chain_model_real.log`, header and the Val/PPII rows.)
* I was past that point (certified banded models with exact Z and exact sampling already run at
  n = 20 with band 8), but two things are worth adding and are cheap in my framework:
  (1) my band width IS the window: run the n = 20 instance with band w = 1, 2 (the pairs beyond the
      window then go into the certified slack u, explicit and small) and report certified b, s2, W;
  (2) sampled mean / variance / minimum of r at n = 20 next to enumerated values at n = 6..12.
* Implemented: cache of the ball values on disk (`cache/ball_*.npz`; re-runs with another band reuse
  the 87 441 evaluations), sample statistics of r in the JSON, `_w<band>` tag.  Batch G started 00:46.
* Test (Val8/PPII, m = 5, site penalties, band 2; 6561 states enumerated): deterministic bracket
  0.054 nats; certified b = 0.054 kT, s2 = 3.5e-3, W = 1.8e-3 nats (model m_-); midpoint model:
  certified W = 4.6e-4; enumerated for the midpoint model b = 0.053, s2 = 7.6e-5, K = 3.8e-5 -- the
  coordinator's ANOVA chain w = 2 on the same peptide: b = 0.058, sigma = 0.0071, K = 2.5e-5.
  So the anchored banded model behaves like the ANOVA chain model, and it comes with a certificate.

## 00:47-01:00  Long-chain constants; OBC2 works; report skeleton written; waiting for batches

* `logs/x04_gamma_long.log` (certified Gamma_3..6, kcal/mol; wall 8-120 s per instance):
    Val/E   n=16: 52.8  2.32  0.0609 0.00140 | n=20: 68.8 3.08 0.0828 0.00195 | n=30: 108.6 4.97 0.138 0.00334 | n=40: 148.5 6.86 0.192 0.00473
    Val/P2  n=20: 61.9  2.82  0.0822 0.00180 | n=30: 98.1 4.58 0.137 0.00311
    Leu/E   n=24: 401   36.3  2.07   0.109   | n=32: 554  50.8 2.96  0.158
    Leu/P2  n=24: 243   20.3  1.15   0.055
    Leu/H   n=24: 3468  769   140    21.6     (helix: hopeless at every order tried)
  Linear in n (Val/E: 3.99, 0.189, 0.0055, 0.00014 per residue for m = 3..6).
* OBC2: `GBModel(kind="obc2")` agrees with OpenMM Reference to 3e-12 (Val4/E, 12 fresh states).
  Batch H (9 OBC2 runs) queued.  First numbers: Val6/E Gamma_3 = 4.49, Gamma_4 = 0.084 kcal/mol
  (GBn2: 12.96, 0.432): OBC2 constants are 3-5 times smaller.
* Partial results so far (81 runs, 79 enumerated, 2.5e6 state checks): 0 violations of the sandwich;
  anchor = global minimiser in 79/79; truth inside all Hoeffding / sample-range / Bennett brackets.
* Site-penalty floors, exact cost numbers Z(m_-)/Z(E) - 1 [M]:
    m = 3 (P2's 5(d) with analysis-only constants):  Val/E n=4,6,8,10: 0.48, 16, 1.1e3, 9.6e4;
                                                    Val/P2 n=4,6,8,10: 10.5, 1.5e4, 6.1e7, 2.8e11
    m = 4:  Val/E 0.002, 0.008, 0.015, 0.022;  Val/P2 0.020, 0.118, 0.256, 0.416  (n = 4, 6, 8, 10)
    m = 5:  Val8/E 2.9e-4
  constant-bound floors: m = 3 e^{beta Gamma_3}: 1e9-1e125; m = 4 Val 0.2-13, Leu 3-4e10; m = 5 Val <= 0.05, Leu 0.1-2.5.
* Report: sections 2.9 (Proposition 6, Bennett inputs) and 3 (skeleton with table blocks filled by
  `mk_report.py --fill`) written.  Batches F (site penalties, final script), G (Val20 with bands 1, 2, 8
  + enumerated analogues), A2/B2 (constant bound: Leu, Ser, Phe, Lys, LKSE), H (OBC2) are running under
  load 13; machine shared.

## 01:00-01:25  All batches finished; tables; report complete

* Final dataset (`out/floor_*.json`): 164 runs of `run_floor.py`, 160 with full enumeration:
  5 512 504 state checks of m_- <= E <= m_+, 0 violations; transfer-matrix ln Z = enumeration to 5e-13;
  coordinate-descent anchor = global minimiser of E in 160/160; true ln Z inside the Hoeffding bracket
  160/160, sample-range 160/160, Bennett 132/132.  Three runs aborted in the reporting step (after
  their enumeration checks) because e^{-beta rho_cert} underflows: L8/H, L12/H, LKSE:5/H at m = 3
  (guard added afterwards; not re-run -- hopeless cases, Gamma_3 = 357, 1034 kcal/mol).
* Val20/PPII, final runs (`logs/floor_big_V20.log`, `logs/floor_batch_G.log`), delta = 0.05, N = 50 000:
    m=4, band 8: deterministic [517.4843, 519.2199]; Hoeffding [518.2442, 518.2759]; Bennett useless (W_cert = 1.5)
    m=5, band 8: deterministic [518.2332, 518.2937]; Hoeffding [518.2598, 518.2648]; Bennett [518.2608, 518.2659]
    m=5, band 2: deterministic [518.1350, 518.3458]; Hoeffding [518.2584, 518.2662]; Bennett [518.2576, 518.2906]
    m=5, band 1: deterministic [517.8792, 518.3699]; Hoeffding [518.2575, 518.2670]; Bennett [518.2516, 518.3892]
  intersection of all 16 brackets and 4 Gibbs-Bogoliubov bounds: [518.2608, 518.2648].
  Certified minimum: min m_- = -306.568720 <= min E <= E(x0) = -306.568715 kcal/mol (band 8, m = 4 and 5).
* Certified minima (site penalties): min m_- attained at the anchor in 5/21 runs at m = 3 (Ser4,5,6/E,
  Val4/E, Leu8/E), 19/23 at m = 4, 13/14 at m = 5.
* Bennett (coordinator's request): certified b within x2 of enumerated, s2 within x4-15, W_cert within
  x4-26 of the true gap (model m_-, all pairs in band, m >= 4).  At n = 20: b_cert = 0.061 kT,
  s2_cert = 4.8e-3, W = 2.4e-3 nats (band 8); band 2: 0.21, 0.049, 0.024; band 1: 0.49, 0.25, 0.12.
* Remainder statistics extrapolate linearly (Val/PPII, m = 5, r = beta(E - m_-) under pi_{m_-}):
  predicted from n = 10, 12 (enumerated) vs sampled at n = 20: band 2 mean 0.0819 / 0.0838,
  variance 4.5e-4 / 4.9e-4, min 0.0468 / 0.0475; band 1: 0.106 / 0.108, 1.41e-3 / 1.51e-3, 0.0484 / 0.0484.
* OBC2 (batch H, 9 runs, no violation): constants 2-8 times smaller than GBn2 for Val/Leu, equal for Ser.
  `x05_neck.py`: GBn2 with the neck term switched off (ablation): Gamma_3,4,5 smaller by 10, 26, 74 (Val6/E),
  12, 27, 69 (Leu8/E), 6, 12 (Ser4/E).  The neck dominates the size of the constants.
* Sum_i c_i^2 of certified oscillations (c_i <= 2 m gamma_i): Val20/PPII 0.109 kT^2 at m = 5, 79 at m = 4.
* Report written: `docs/science/workstreams/P3_REPORT.md` (tables filled by `mk_report.py --fill`; text
  blocks inserted by `fill_text.py`, `fill_text2.py`).  Full tables: `out/report_tables.md`, `out/tables.md`.
* Housekeeping: `experiments/science/ws_P2/__pycache__/` (anlib 23:57:50, fbmodel 00:47:02) was NOT
  written by me (all my runs use `python3 -B` and p3core sets `sys.dont_write_bytecode` before importing
  P2's modules; I never import anlib); the time stamps coincide with the coordinator's
  `pi_inference` scripts, two of which import fbmodel.  Superseded results are in `out/intermediate/`
  and `out/prebennett/`.  No git state was changed; nothing outside `ws_P3/` and the report was written.

## What I did not check (also in the report)
* no proof machine-checked; the 1e-7 kcal/mol floating-point allowance per evaluation of g is not
  proved for numexpr's summation order (measured error <= 2e-12); mpmath.iv trusted; code unreviewed;
* one large instance, one anchor, one seed; helices and charged chains beyond 4-6 residues fail or
  were not run; continuous chi not treated; prior art at abstract level only (one PubMed hit unopened).
