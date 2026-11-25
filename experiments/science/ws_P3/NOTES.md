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
