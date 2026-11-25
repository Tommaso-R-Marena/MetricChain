# Benchmark design: what would convince, and what would refute

*Science division.  Version 2 (2026-11-25; version 1 at checkpoint 13).  A design, not a
result: nothing here has been run except where a script is named.  Revised after workstreams
P (a real force field) and K (kinetics) reported; X (alternative models of ignorance) is
still running.*

## 0. Principles

1. **Every benchmark is attached to a hypothesis that it could refute.**  A benchmark that
   can only succeed is a demonstration.
2. **Planted truth for anything that claims certainty.**  A certified interval is tested on
   instances where the true value is known by construction; one miss when the truth is
   inside the stated class is a bug, not a statistic.
3. **Negative controls and deception instances are part of the suite**, not an appendix:
   inputs on which a correct method must *decline* to conclude.
4. **Baselines are the methods a practitioner would use**, run by their own published
   recipes, including the ones that give no guarantee.  A certified method that is
   uninformative where an uncertified one is accurate has not won.
5. **Development, construction and evaluation are separated.**  Parameters (envelope
   constants, error bars, tolerances, solver settings) are fixed on development instances;
   evaluation instances are generated from seeds published in advance; the list of
   reported metrics is fixed before the run.
6. **What a success would not establish is written next to each benchmark.**
7. Fixed sequences and synthetic or public data only; no sequence design, no
   target-specific optimisation, no experiments.

## 1. The hypotheses

| id | hypothesis (the strongest constructive claims in the three branches) | who holds it |
|---|---|---|
| H1 | certificates of the verified kernels can be produced and checked at sizes of physical interest, at a cost comparable to solving | theory (kernels), engineering (E-2) |
| H2 | a native certificate format is cheaper to check than a pseudo-Boolean proof of the same run | theory report §6.4 (weakened by SCI-REV-0006, W2) |
| H3 | physical residuals lie near a cheap class (linear in pair-distance profiles, or weakly coupled second order) | theory (THY-MSG-0002, principle 2), engineering (E-3) |
| H4 | the exponents of the query-complexity theory describe the cost that matters at accessible sizes | theory (stated by them as doubtful) |
| H5 | a model, its uncertainty class and averaged data together give informative certified intervals for structural quantities | science (`INFERENCE_LIMITS.md` §11.4) |
| H6 | data can certify a non-trivial lower bound on model error that sampling cannot change | science (Theorem 8) |
| H7 | certified ranges are tighter than, or disagree informatively with, what current ensemble methods report | science |
| H8 | tractable cuts (boxes, counting statistics, small decision trees) certify a useful fraction of barrier heights on chains | science (workstream K) |

## 2. The benchmarks

### B1 — which class do residuals live in?  (tests H3; refutes it if the numbers say so)

*Instances.*  Fixed-sequence chains of increasing length (capped peptides, 2–12 residues;
later a small folded domain with a fixed backbone and rotamers).  *Residuals:* (a) the
many-body part of an implicit-solvent model against the vacuum force field; (b) the
difference between two force fields; (c) a learned potential against a classical one;
(d) where public reference data exist, a quantum-chemical energy against a force field.
*Controls:* a synthetic residual exactly in the profile class (remainder must be zero); a
random Lipschitz residual (remainder must be of the order of its range).
*Metrics, with units (`k_BT` at 300 K), each as a function of chain length and of the
position along the chain:* per-torsion bounded-difference constants; the density of mixed
second differences above a threshold as a function of sequence separation; sup-norm and
root-mean-square remainder of the best fit in (i) single-site, (ii) pairwise-in-torsions,
(iii) pair-distance-profile classes; the fraction of sharp sites.
*Refutation.*  If `β ×` (remainder of the best profile fit) grows linearly with length with
a coefficient of order one per residue, and `β ×` (per-torsion constant) exceeds one at most
sites, no cheap class contains the residual and H3 fails for that residual.
*What success would not establish.*  A small remainder on a torsion grid says nothing about
conformations outside the grid, and a fitted constant is not a certified one.
*Status.*  **Pilot run** (workstream P; SCI-RES-0002; `PHYSICAL_APPLICABILITY.md` §2), residuals
(a) and (b) on capped alanine peptides, exact on torsion grids to six and nine residues.
*Outcome against the refutation criterion:* **H3 fails for the GBn2 polarisation energy in
backbone torsions** — `β ×` per-torsion constant is 12–53 at every site and grows with
length; the sup-norm remainder of the pair-additive class is `2–16 k_BT` and grows — and
**H3 holds exactly for same-lineage force-field differences** (additive or residue-local,
remainder zero).  Both controls behaved as required in the workstream's own checks (the
exactly pair-additive Coulomb energy has the same typed-class remainder as the solvent
term, so the remainder of the typed class measures the typing).  *Lessons for the full
benchmark:* (i) report sup norms over enumerated domains only — a sampled maximum was
exceeded on held-out conformations by factors up to ten; (ii) state the domain: constants
are dominated by its most compact and most extended members and by the clash threshold
(up to 15 %); (iii) the decisive missing case is **rotamer variables on a fixed backbone**
(request P-E1), where the known part is pairwise and no lever arm exists; (iv) add the
typical-norm metrics next to the sup-norm ones (RMS, and the exact Jensen gap against the
class bound) — the gap between them is the finding.

### B2 — certificate cost on real cost-function networks  (tests H1, H2)

*Instances.*  Public fixed-sequence side-chain-positioning networks (engineering's E-2),
stratified by treewidth and by the number of sites whose gap is below a stated model
uncertainty.  *Routes:* (i) the native certificate of the Lean kernel with the reference
checker; (ii) the same search tree as a VeriPB proof checked by CakePB, and where feasible
imported into Lean 4 (PBLean); (iii) the solver with no proof.  *Metrics:* certificate
size, production overhead, checking time, the largest instance each route completes within
a fixed budget; the trusted base of each route, listed.
*Refutation.*  H2 fails if route (ii) is within a factor three of route (i) in size and
time on all instances (specification: SCI-REV-0006, E-1).  H1 fails if no route certifies
instances beyond a few tens of sites.
*Negative controls.*  A planted wrong bound must be rejected by every checker; a
certificate with one corrupted line must be rejected (mutation testing, as in the theory
division's audit).
*What success would not establish.*  That the certified minimum is physically meaningful
(see B5).

### B3 — identified sets with planted truth  (tests H5, H7)

*Instances.*  Systems where every quantity is computable exactly: lattice chains up to the
enumeration limit (the engineering tables; our own enumerator to 15 beads), and
fixed-backbone side-chain ensembles of low treewidth with pairwise energies.  *Truths:*
(a) the model itself; (b) the model plus a residual inside the stated class; (c) plus a
residual outside it, by a controlled margin; (d) the **deception instance** of
`INFERENCE_LIMITS.md` Theorem 2 — an ensemble whose low-order averages are those of the
disordered ensemble and whose entropy is near the class minimum.  *Data:* exact and noisy
averages of single-site and pairwise observables; of a scattering curve on a finite grid
of `q` (Proposition A2.1 of workstream A2 gives its place in the profile class).
*Methods.*  Ours: model-free, divergence-ball and envelope-class identified sets, each
with its dual certificate.  Baselines: maximum-entropy reweighting with its usual
uncertainty estimate; a minimal-ensemble selection; **maximum occurrence / maxOR–minOR as
practised** (penalised least squares on a finite pool with the published threshold rule);
plain sampling with standard errors.
*Metrics.*  Coverage of the truth (must be 100 % for certified intervals in cases (a), (b));
width relative to the a-priori range; for baselines, the frequency with which the truth
lies outside the reported uncertainty; the gap between a heuristic maximum occurrence and
the certified one.
*Refutation.*  H5 fails if certified intervals are within 10 % of the a-priori range
whenever the class constant is as large as B1 says it must be for a real residual.  H7
fails if the baselines' intervals cover the truth as often as ours at smaller width, on
every instance including (c) and (d).
*What success would not establish.*  Physical validity: forward models of real
observables have their own errors, and membership of the true residual in the class cannot
be verified from above.

### B4 — falsification: power and false alarms  (tests H6)

*Instances.*  As B3, truths (b) and (c) on a grid of margins and noise levels.
*Metrics.*  False-alarm rate when the truth is inside the class (must be zero for exact
data and at most the stated level for noisy data with certified error bars); the smallest
margin detected, as a function of the data type and of chain length; the certified lower
bounds `b_min` and `ρ_min` against the truth's own constants.  First numbers:
`INFERENCE_LIMITS.md` §9 and SCI-MSG-0002 §3 (the certified constant is about half the
truth's worst-case constant at 9–10 beads).
*Refutation.*  H6 fails if the certified lower bound falls to zero relative to the truth's
constant as the chain grows, for every data type.

### B5 — is the certified minimum meaningful?  (a test of meaning, not of a method)

For the instances of B2 with the model uncertainty of B1: the number of sites that are not
sharp, the size of the set of possibly optimal conformations (contact set), and the
fraction of instances on which the certified minimiser is *robustly* certified.  A
certificate of a minimum that is one of exponentially many possibly optimal conformations is correct
and uninformative; the benchmark reports both facts.

### B6 — asymptotics against finite size  (tests H4)

The engineering division's experiment X-005 is this benchmark for the adaptive algorithm:
exact evaluation counts against the claimed exponent, with an adversarial search over
instances (result so far: no violation; the flat instance is not the worst; excess decaying
like `1/√n`).  The same design applies to: the non-adaptive exponent against the class-wide
bound of Proposition A1.1 (explicit for every `n`); the limit shape against enumeration
(prediction from Newton–Okounkov theory: the number of attained profiles grows like
`vol(𝒦)·N³`; SCI-REV-0006, T-4); the lever-arm constant against chain length.

### B8 — certified kinetics  (tests a new hypothesis H8: tractable cuts certify a useful fraction of barriers on chains)

*Instances.*  Rotational-isomeric chains on the diamond lattice (exact merge trees up to
the enumeration limit); pairwise models of low treewidth; torsion-voxel models of small
molecules with nearest-voxel adjacency.  *Methods.*  Box cuts, counting cuts with an exact
counter, decision-tree cuts (formats of SCI-MSG-0005 §5); baselines: any path-finding
method (upper bounds only).  *Metrics.*  Certified fraction of each trap depth; number of
wall boxes; the gap between the best path found and the best cut certified.
*Negative controls.*  A linear multiplier on a counting constraint must never beat the
trivial bound (Proposition K3); a cut on the Hamming graph of voxel labels must fail to
converge to the continuum barrier (K8).  *Refutation.*  H8 fails if the certified fraction
tends to zero with chain length for every tractable cut family.  *Run so far:* 6–8 torsions
(`experiments/science/ws_K/t7_chain.py`): 1.00, 0.55, 0.77 — not monotone; request K-E1 asks
for 6–13.  *What success would not establish.*  Anything about physical rates: discrete
rates are sampler-relative.

### B7 — conformance and trust  (not a hypothesis test; a standing regression)

The theory division's audit; the engineering division's differential test of the Lean
definitions against the reference checker (their E-1); replication on independent machines
(done at three theory heads by engineering and at one by us).

## 3. Situations in which apparent success would not establish the claim

* **Narrow intervals on synthetic truths inside the class** establish soundness and
  tightness of the method, not that any molecule's residual is inside the class.
* **Agreement of a certified interval with a simulation** establishes nothing about the
  simulation's convergence unless the interval is narrow.
* **A small remainder of the profile fit on sampled conformations** can coexist with a
  large remainder on conformations the sampler never visits — the hidden-twin phenomenon
  of `INFERENCE_LIMITS.md` Proposition 5b at the level of fitting.
* **Low-order agreement with data** does not establish disorder or order (Theorem 2;
  Albanna et al. 2017 for the unrestricted class).
* **A profile match** does not establish a structure (homometric chains; workstream A2).
* **Fast checking of small certificates** does not establish H1; the instances must be
  stratified by the number of non-sharp sites, which is what makes certificates large.

## 4. What has been run

| benchmark | run so far | where |
|---|---|---|
| B3, lattice chains, truths (a) and one of type (c), exact data, model-free and envelope class | 7–15 beads (model-free), 6–10 beads (envelope class), 27 beads from the engineering tables for one target | `INFERENCE_LIMITS.md` §11; `experiments/science/pi_chain/` |
| B3, deception instance | exact enumeration, `n ≤ 16`; no baseline run on it yet | `experiments/science/pi_inference/code_cone_check.py` |
| B4 | three margins, two data types, 8–10 beads, exact data | `experiments/science/pi_chain/envelope_scaling.py` |
| B6 | engineering X-005 (theirs) | ENG-RES-0008 |
| B7 | audit at `5ed4072` | `docs/science/INDEPENDENT_VALIDATION.md` |
| B1 | pilot: alanine peptides, GBn2 and four force-field differences against ff14SB, exact on grids | `workstreams/SP_REPORT.md`; `experiments/science/ws_P/` |
| B8 | cut families on tiny systems (≤ 5 849 states) and one 200-site chain | `workstreams/SK_REPORT.md`; `experiments/science/ws_K/` |
| B2, B5 | nothing yet | — |
