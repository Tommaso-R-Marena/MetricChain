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
  in all 24 comparisons (incl. the EMPTY ones).  [M]

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
* `t04_tight.py` finished (`out/tight_{apolar,polar,charged}.json`, 44 instances, 562 triples):
  rigorous analysis-only bound >= P2's measured c_ijk for every triple (asserted).  Ratio of sums:
    Val x206-485 | Leu x280-1420 | Phe x89-170 | Ser x38-104 | Lys x33-77 | LKSE x89-160.
  NEGATIVE RESULT: analysis alone is 1.5-3 orders of magnitude too large.
* Prior art (rule 5): 3 PubMed queries (0, 1, 0 hits) and 3 Consensus queries (3 records each), all
  read at ABSTRACT level only: Onufriev-Case-Bashford 2002 (perfect radii), Mongan et al. 2007 (R6
  integral), Onufriev et al. 2011 (gross errors of f_GB), Jain et al. 2017 (sparse residue interaction
  graphs), Jou et al. 2016 (BWM*, dynamic programming on sparse graphs), Hallen-Donald 2019 (review),
  Rahman 2014 (errors of truncated referential/anchored decompositions).  None states a sup-norm
  bound on the many-body remainder of a GB energy; not a novelty claim.
